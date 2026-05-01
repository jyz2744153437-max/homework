#!/usr/bin/env python3
"""突现检测脚本 - 基于 Kleinberg 算法"""

import re
import math
from pathlib import Path
from collections import defaultdict
import numpy as np
from scipy.stats import poisson

# WoS 标签字段
_WOS_TAGS = {
    'PT', 'AU', 'AF', 'TI', 'SO', 'LA', 'DT', 'DE', 'ID', 'AB',
    'C1', 'RP', 'EM', 'FU', 'FX', 'CR', 'NR', 'TC', 'Z9', 'U1',
    'U2', 'PU', 'PI', 'PA', 'SN', 'EI', 'J9', 'JI', 'PD', 'PY',
    'VL', 'IS', 'BP', 'EP', 'DI', 'PG', 'WC', 'SC', 'GA', 'UT',
    'PM', 'OA', 'DA', 'ER', 'BN', 'CL', 'CT', 'CY', 'HO', 'OB',
    'OP', 'SE', 'BS', 'AR', 'SU', 'MA', 'NR',
}


def parse_wos_file(path):
    """解析单个 WoS 文件"""
    records = []
    current = {}
    current_tag = ''

    with open(path, 'r', encoding='utf-8-sig') as f:
        for line in f:
            line = line.rstrip('\n\r')
            if not line.strip():
                continue

            tag_match = re.match(r'^([A-Z][A-Z0-9])(?:\s|$)', line)
            if tag_match:
                tag = tag_match.group(1)
                rest = line[tag_match.end():]
                value = rest.strip()
                if tag == 'ER':
                    if current:
                        records.append({k: '; '.join(v) for k, v in current.items()})
                    current = {}
                    current_tag = ''
                    continue
                if tag not in current:
                    current[tag] = []
                current[tag].append(value)
                current_tag = tag
            elif current_tag and line.startswith('   '):
                value = line.strip()
                if current_tag in current:
                    current[current_tag].append(value)

    if current:
        records.append({k: '; '.join(v) for k, v in current.items()})

    return records


def parse_wos_dir(dir_path):
    """解析目录下所有 WoS 文件"""
    all_records = []
    for txt_file in sorted(Path(dir_path).glob('*.txt')):
        all_records.extend(parse_wos_file(txt_file))
    return all_records


def extract_keywords(records):
    """提取关键词（DE + ID 字段）"""
    keyword_year = defaultdict(list)

    for rec in records:
        year = rec.get('PY', '').strip()
        if not year or not year.isdigit():
            continue
        year = int(year)

        # 作者关键词 (DE) + WoS 关键词 (ID)
        de = rec.get('DE', '').strip()
        id_ = rec.get('ID', '').strip()

        keywords = set()
        for kw_str in [de, id_]:
            if kw_str:
                for kw in kw_str.split(';'):
                    kw = kw.strip().lower()
                    if kw and len(kw) > 2:
                        keywords.add(kw)

        for kw in keywords:
            keyword_year[kw].append(year)

    return keyword_year


def kleinberg_burst(years, s=2, gamma=1):
    """
    Kleinberg 突现检测算法

    参数:
        years: 关键词出现的年份列表
        s: 状态转移参数（默认2）
        gamma: 突现强度参数（默认1）

    返回:
        burst_periods: [(start, end, strength), ...]
    """
    if not years:
        return []

    years = sorted(years)
    year_min, year_max = min(years), max(years)

    if year_min == year_max:
        return []

    # 构建年份序列
    year_range = list(range(year_min, year_max + 1))
    n = len(year_range)

    # 统计每年出现次数
    year_counts = defaultdict(int)
    for y in years:
        year_counts[y] += 1

    counts = np.array([year_counts[y] for y in year_range], dtype=float)

    # 计算平均频率
    total = counts.sum()
    avg_rate = total / n

    if avg_rate == 0:
        return []

    # 定义状态：状态 i 对应频率 2^i * avg_rate
    # 状态数由数据决定
    max_count = counts.max()
    max_state = max(1, int(np.log2(max_count / avg_rate)) + 1) if avg_rate > 0 else 1

    # 转移代价
    def transition_cost(i, j):
        if i >= j:
            return 0
        return (j - i) * gamma * np.log(n)

    # 发射概率（泊松分布）
    def emission_cost(state, count):
        rate = (2 ** state) * avg_rate
        if rate == 0:
            return float('inf') if count > 0 else 0
        # 负对数似然
        return -poisson.logpmf(count, rate)

    # Viterbi 算法找最优状态序列
    # cost[t][state] = 到时刻 t 状态 state 的最小代价
    cost = np.full((n, max_state + 1), np.inf)
    parent = np.full((n, max_state + 1), -1, dtype=int)

    # 初始化
    for state in range(max_state + 1):
        cost[0, state] = emission_cost(state, counts[0])

    # 递推
    for t in range(1, n):
        for j in range(max_state + 1):
            emit_cost = emission_cost(j, counts[t])
            for i in range(max_state + 1):
                trans_cost = transition_cost(i, j)
                new_cost = cost[t-1, i] + trans_cost + emit_cost
                if new_cost < cost[t, j]:
                    cost[t, j] = new_cost
                    parent[t, j] = i

    # 回溯
    states = np.zeros(n, dtype=int)
    states[n-1] = np.argmin(cost[n-1])
    for t in range(n-2, -1, -1):
        states[t] = parent[t+1, states[t+1]]

    # 提取突现区间
    bursts = []
    in_burst = False
    burst_start = None
    burst_strength = 0

    for t, state in enumerate(states):
        if state > 0:
            if not in_burst:
                in_burst = True
                burst_start = t
                burst_strength = state
            else:
                burst_strength = max(burst_strength, state)
        else:
            if in_burst:
                bursts.append((year_range[burst_start], year_range[t-1], burst_strength))
                in_burst = False

    if in_burst:
        bursts.append((year_range[burst_start], year_range[n-1], burst_strength))

    return bursts


def detect_keyword_bursts(keyword_year, min_freq=5, s=2, gamma=1):
    """检测所有关键词的突现"""

    results = []

    for keyword, years in keyword_year.items():
        if len(years) < min_freq:
            continue

        bursts = kleinberg_burst(years, s, gamma)

        if bursts:
            for start, end, strength in bursts:
                results.append({
                    'keyword': keyword,
                    'burst_start': start,
                    'burst_end': end,
                    'strength': strength,
                    'total_freq': len(years),
                })

    # 按强度排序
    results.sort(key=lambda x: (-x['strength'], x['burst_start']))

    return results


def main():
    data_dir = Path(__file__).parent.parent / 'Data'
    output_dir = Path(__file__).parent.parent / 'outputs'
    output_dir.mkdir(exist_ok=True)

    print('解析 WoS 数据...')
    records = parse_wos_dir(data_dir)
    print(f'共 {len(records)} 条文献')

    print('提取关键词...')
    keyword_year = extract_keywords(records)
    print(f'共 {len(keyword_year)} 个关键词')

    print('检测突现...')
    bursts = detect_keyword_bursts(keyword_year, min_freq=5, s=2, gamma=1)
    print(f'发现 {len(bursts)} 个突现')

    # 保存结果
    import csv

    output_csv = output_dir / 'keyword_bursts.csv'
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['keyword', 'burst_start', 'burst_end', 'strength', 'total_freq'])
        writer.writeheader()
        writer.writerows(bursts)

    print(f'结果保存至: {output_csv}')

    # 打印 Top 20
    print('\n=== Top 20 突现关键词 ===')
    for i, b in enumerate(bursts[:20], 1):
        print(f"{i:2}. {b['keyword']:30} | {b['burst_start']}-{b['burst_end']} | 强度:{b['strength']} | 频次:{b['total_freq']}")


if __name__ == '__main__':
    main()
