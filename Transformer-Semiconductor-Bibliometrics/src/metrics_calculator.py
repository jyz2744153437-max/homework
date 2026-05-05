"""
WOS 数据解析与指标计算脚本

功能：
1. 解析 WOS Plain Text 格式
2. 计算发文量趋势、h-index、核心作者/机构/期刊
3. 输出统计表格和可视化图表
"""

import os
import re
from collections import defaultdict, Counter
from pathlib import Path

# === 配置 ===
DATA_DIR = Path(__file__).parent.parent / "Data"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs"

# === WOS 解析器 ===

def parse_wos_file(filepath):
    """解析单个 WOS Plain Text 文件"""
    records = []
    current = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')

            # 跳过文件头
            if line.startswith('FN ') or line.startswith('VR '):
                continue

            # 记录结束
            if line == 'ER':
                if current:
                    records.append(current)
                current = {}
                continue

            # 解析字段
            if len(line) >= 3 and line[2] == ' ':
                tag = line[:2]
                value = line[3:].strip()

                if tag in current:
                    # 多值字段追加
                    if isinstance(current[tag], list):
                        current[tag].append(value)
                    else:
                        current[tag] = [current[tag], value]
                else:
                    current[tag] = value
            elif line.startswith('   ') and current:
                # 续行
                last_tag = list(current.keys())[-1]
                if isinstance(current[last_tag], list):
                    current[last_tag][-1] += ' ' + line.strip()
                else:
                    current[last_tag] += ' ' + line.strip()

    return records


def parse_all_wos_files():
    """解析所有 WOS 数据文件"""
    all_records = []

    for filename in ['download_1-500.txt', 'download_501-643.txt']:
        filepath = DATA_DIR / filename
        if filepath.exists():
            records = parse_wos_file(filepath)
            all_records.extend(records)
            print(f"解析 {filename}: {len(records)} 条记录")

    print(f"总计: {len(all_records)} 条记录")
    return all_records


# === 指标计算 ===

def calc_yearly_publication(records):
    """年度发文量统计"""
    year_counts = Counter()
    for r in records:
        py = r.get('PY', '')
        if py:
            year_counts[int(py)] += 1

    # 排序
    sorted_years = sorted(year_counts.items())
    return sorted_years


def calc_document_types(records):
    """文献类型分布"""
    dt_counts = Counter()
    for r in records:
        dt = r.get('DT', 'Unknown')
        dt_counts[dt] += 1
    return dt_counts.most_common()


def calc_journal_distribution(records, top_n=20):
    """期刊分布"""
    journal_counts = Counter()
    for r in records:
        so = r.get('SO', '')
        if so:
            journal_counts[so] += 1
    return journal_counts.most_common(top_n)


def extract_authors(record):
    """提取作者列表"""
    au = record.get('AU', '')
    if isinstance(au, list):
        return au
    elif au:
        # 分号分隔
        return [a.strip() for a in au.split(';') if a.strip()]
    return []


def extract_institutions(record):
    """提取机构列表"""
    c1 = record.get('C1', '')
    institutions = set()

    if isinstance(c1, list):
        c1 = ' '.join(c1)

    # 匹配机构名（方括号后的内容）
    # 格式: [Author] Institution, City, Country
    matches = re.findall(r'\[([^\]]+)\]\s*([^,\[\]]+(?:University|Univ|Institute|College|Laboratory|Lab|Hospital|Company|Corp|Inc)[^,\[\]]*)', c1, re.IGNORECASE)

    for author, inst in matches:
        # 清理机构名
        inst = inst.strip()
        inst = re.sub(r'\s+', ' ', inst)
        institutions.add(inst)

    # 如果上面没匹配到，尝试简单分割
    if not institutions and c1:
        parts = c1.split('[')
        for part in parts[1:]:
            if ']' in part:
                inst_part = part.split(']')[1].strip()
                if inst_part:
                    # 取第一个逗号前的部分作为机构
                    inst = inst_part.split(',')[0].strip()
                    institutions.add(inst)

    return list(institutions)


def extract_countries(record):
    """提取国家"""
    c1 = record.get('C1', '')
    countries = set()

    if isinstance(c1, list):
        c1 = ' '.join(c1)

    # 常见国家名
    country_keywords = [
        'China', 'Peoples R China', 'P R China', 'PR China',
        'USA', 'United States', 'U S A',
        'Japan', 'South Korea', 'Korea',
        'Germany', 'France', 'UK', 'England', 'Scotland',
        'Taiwan', 'Hong Kong', 'Singapore',
        'India', 'Australia', 'Canada',
        'Netherlands', 'Switzerland', 'Italy', 'Spain',
        'Brazil', 'Russia', 'Poland', 'Sweden', 'Norway',
        'Belgium', 'Austria', 'Denmark', 'Finland', 'Ireland'
    ]

    c1_lower = c1.lower()
    for country in country_keywords:
        if country.lower() in c1_lower:
            # 标准化
            if 'china' in country.lower() or 'peoples r china' in country.lower():
                countries.add('China')
            elif country in ['USA', 'United States', 'U S A']:
                countries.add('USA')
            elif 'korea' in country.lower():
                countries.add('South Korea')
            elif country in ['UK', 'England', 'Scotland']:
                countries.add('UK')
            else:
                countries.add(country)

    return list(countries)


def calc_author_stats(records, top_n=20):
    """作者发文统计"""
    author_counts = Counter()
    author_citations = defaultdict(int)

    for r in records:
        authors = extract_authors(r)
        tc = int(r.get('TC', 0) or 0)

        for author in authors:
            author_counts[author] += 1
            author_citations[author] += tc

    # 发文量 Top N
    top_authors = author_counts.most_common(top_n)

    # 计算篇均被引
    author_stats = []
    for author, count in top_authors:
        avg_cite = author_citations[author] / count if count > 0 else 0
        author_stats.append({
            'author': author,
            'publications': count,
            'total_citations': author_citations[author],
            'avg_citations': round(avg_cite, 2)
        })

    return author_stats


def calc_institution_stats(records, top_n=20):
    """机构发文统计"""
    inst_counts = Counter()

    for r in records:
        insts = extract_institutions(r)
        for inst in insts:
            inst_counts[inst] += 1

    return inst_counts.most_common(top_n)


def calc_country_stats(records, top_n=20):
    """国家发文统计"""
    country_counts = Counter()

    for r in records:
        countries = extract_countries(r)
        for country in countries:
            country_counts[country] += 1

    return country_counts.most_common(top_n)


def calc_h_index(records):
    """计算整体 h-index"""
    citations = []
    for r in records:
        tc = int(r.get('TC', 0) or 0)
        citations.append(tc)

    citations.sort(reverse=True)

    h = 0
    for i, c in enumerate(citations):
        if c >= i + 1:
            h = i + 1
        else:
            break

    return h


def calc_citation_stats(records):
    """被引统计"""
    citations = []
    for r in records:
        tc = int(r.get('TC', 0) or 0)
        citations.append(tc)

    if not citations:
        return {'total': 0, 'mean': 0, 'median': 0, 'max': 0, 'zero_count': 0}

    citations.sort()
    n = len(citations)

    return {
        'total': sum(citations),
        'mean': round(sum(citations) / n, 2),
        'median': citations[n // 2] if n % 2 == 1 else (citations[n // 2 - 1] + citations[n // 2]) / 2,
        'max': max(citations),
        'zero_count': citations.count(0),
        'zero_ratio': round(citations.count(0) / n * 100, 1)
    }


def calc_keyword_stats(records, top_n=30):
    """关键词统计"""
    kw_counts = Counter()

    for r in records:
        # 作者关键词
        de = r.get('DE', '')
        if isinstance(de, list):
            de = ';'.join(de)

        if de:
            for kw in de.split(';'):
                kw = kw.strip()
                if kw:
                    kw_counts[kw] += 1

        # 扩展关键词
        id_kw = r.get('ID', '')
        if isinstance(id_kw, list):
            id_kw = ';'.join(id_kw)

        if id_kw:
            for kw in id_kw.split(';'):
                kw = kw.strip()
                if kw:
                    kw_counts[kw] += 1

    return kw_counts.most_common(top_n)


# === 报告生成 ===

def generate_report(records):
    """生成统计报告"""
    report = []
    report.append("# 文献计量指标统计报告\n")
    report.append(f"> 分析日期: 2026-05-01")
    report.append(f"> 总记录数: {len(records)}\n")

    # 1. 年度发文量
    report.append("## 1. 年度发文量趋势\n")
    report.append("| 年份 | 发文量 | 增长率 |")
    report.append("|---|---|---|")

    yearly = calc_yearly_publication(records)
    prev_count = None
    for year, count in yearly:
        if prev_count is not None and prev_count > 0:
            growth = f"+{round((count - prev_count) / prev_count * 100, 1)}%" if count > prev_count else f"{round((count - prev_count) / prev_count * 100, 1)}%"
        else:
            growth = "-"
        report.append(f"| {year} | {count} | {growth} |")
        prev_count = count

    # 2. 文献类型
    report.append("\n## 2. 文献类型分布\n")
    report.append("| 类型 | 数量 | 占比 |")
    report.append("|---|---|---|")
    for dt, count in calc_document_types(records):
        ratio = round(count / len(records) * 100, 1)
        report.append(f"| {dt} | {count} | {ratio}% |")

    # 3. 被引统计
    report.append("\n## 3. 被引统计\n")
    cite_stats = calc_citation_stats(records)
    report.append(f"- 总被引次数: {cite_stats['total']}")
    report.append(f"- 篇均被引: {cite_stats['mean']}")
    report.append(f"- 被引中位数: {cite_stats['median']}")
    report.append(f"- 最高被引: {cite_stats['max']}")
    report.append(f"- 零被引文献: {cite_stats['zero_count']} ({cite_stats['zero_ratio']}%)")
    report.append(f"- 整体 h-index: {calc_h_index(records)}")

    # 4. 核心期刊
    report.append("\n## 4. 核心期刊 (Top 20)\n")
    report.append("| 期刊 | 发文量 |")
    report.append("|---|---|")
    for journal, count in calc_journal_distribution(records):
        report.append(f"| {journal} | {count} |")

    # 5. 核心作者
    report.append("\n## 5. 核心作者 (Top 20)\n")
    report.append("| 作者 | 发文量 | 总被引 | 篇均被引 |")
    report.append("|---|---|---|---|")
    for stat in calc_author_stats(records):
        report.append(f"| {stat['author']} | {stat['publications']} | {stat['total_citations']} | {stat['avg_citations']} |")

    # 6. 核心机构
    report.append("\n## 6. 核心机构 (Top 20)\n")
    report.append("| 机构 | 发文量 |")
    report.append("|---|---|")
    for inst, count in calc_institution_stats(records):
        report.append(f"| {inst} | {count} |")

    # 7. 国家分布
    report.append("\n## 7. 国家/地区分布 (Top 15)\n")
    report.append("| 国家/地区 | 发文量 |")
    report.append("|---|---|")
    for country, count in calc_country_stats(records, top_n=15):
        report.append(f"| {country} | {count} |")

    # 8. 高频关键词
    report.append("\n## 8. 高频关键词 (Top 30)\n")
    report.append("| 关键词 | 频次 |")
    report.append("|---|---|")
    for kw, count in calc_keyword_stats(records):
        report.append(f"| {kw} | {count} |")

    return '\n'.join(report)


def main():
    """主函数"""
    print("=" * 50)
    print("WOS 文献计量指标计算")
    print("=" * 50)

    # 解析数据
    records = parse_all_wos_files()

    if not records:
        print("错误: 未找到数据文件")
        return

    # 生成报告
    report = generate_report(records)

    # 保存报告
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / "metrics_report.md"

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"\n报告已保存到: {output_file}")

    # 同时输出到控制台
    print("\n" + "=" * 50)
    print(report)


if __name__ == "__main__":
    main()
