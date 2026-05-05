#!/usr/bin/env python3
"""突现检测可视化"""

import csv
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False


def read_bursts(csv_path):
    """读取突现结果"""
    bursts = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            bursts.append({
                'keyword': row['keyword'],
                'burst_start': int(row['burst_start']),
                'burst_end': int(row['burst_end']),
                'strength': int(row['strength']),
                'total_freq': int(row['total_freq']),
            })
    return bursts


def plot_burst_timeline(bursts, output_path, top_n=25):
    """绘制突现时间线图"""

    # 取 Top N
    bursts = bursts[:top_n]

    fig, ax = plt.subplots(figsize=(16, 12))

    year_min = min(b['burst_start'] for b in bursts)
    year_max = max(b['burst_end'] for b in bursts)

    for i, b in enumerate(bursts):
        y = len(bursts) - i - 1
        start = b['burst_start']
        end = b['burst_end']
        strength = b['strength']

        # 颜色根据强度
        color = '#e74c3c' if strength >= 2 else '#3498db'
        alpha = 0.9 if strength >= 2 else 0.6

        # 画横条
        ax.barh(y, end - start + 1, left=start, height=0.7,
                color=color, alpha=alpha, edgecolor='black', linewidth=0.5)

        # 标注关键词 - 截断过长的关键词
        keyword = b['keyword']
        if len(keyword) > 30:
            keyword = keyword[:27] + '...'
        ax.text(year_min - 0.5, y, keyword,
                ha='right', va='center', fontsize=8)

        # 标注频次
        ax.text(end + 0.3, y, f"({b['total_freq']})",
                ha='left', va='center', fontsize=7, color='gray')

    ax.set_xlim(year_min - 12, year_max + 8)
    ax.set_ylim(-0.5, len(bursts) + 0.5)
    ax.set_xlabel('年份', fontsize=12)
    ax.set_title('关键词突现检测 (Top 25)', fontsize=14, fontweight='bold')

    # 年份刻度
    ax.set_xticks(range(year_min, year_max + 2))
    ax.set_yticks([])

    # 图例
    red_patch = mpatches.Patch(color='#e74c3c', label='高强度突现 (>=2)')
    blue_patch = mpatches.Patch(color='#3498db', label='一般突现 (1)')
    ax.legend(handles=[red_patch, blue_patch], loc='upper right', fontsize=9)

    ax.grid(axis='x', linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    print(f'图片保存至: {output_path}')


def generate_report(bursts, output_path):
    """生成突现报告"""

    # 按时间段分组
    periods = {
        '2015-2018 (早期)': [],
        '2019-2022 (中期)': [],
        '2023-2025 (近期)': [],
    }

    for b in bursts:
        mid = (b['burst_start'] + b['burst_end']) / 2
        if mid <= 2018:
            periods['2015-2018 (早期)'].append(b)
        elif mid <= 2022:
            periods['2019-2022 (中期)'].append(b)
        else:
            periods['2023-2025 (近期)'].append(b)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('# 关键词突现检测报告\n\n')
        f.write('> 基于 Kleinberg 突现检测算法\n')
        f.write('> 创建日期：2026-05-01\n\n')
        f.write('---\n\n')

        f.write('## 1. 突现检测方法\n\n')
        f.write('| 项目 | 说明 |\n')
        f.write('|---|---|\n')
        f.write('| 算法 | Kleinberg Burst Detection |\n')
        f.write('| 参数 | s=2, γ=1 |\n')
        f.write('| 最小频次 | 5 |\n')
        f.write(f'| 检测结果 | {len(bursts)} 个突现 |\n\n')

        f.write('---\n\n')
        f.write('## 2. 突现时间分布\n\n')

        for period, items in periods.items():
            f.write(f'### {period}\n\n')
            if items:
                f.write('| 关键词 | 突现区间 | 强度 | 总频次 |\n')
                f.write('|---|---|---|---|\n')
                for b in items:
                    f.write(f"| {b['keyword']} | {b['burst_start']}-{b['burst_end']} | {b['strength']} | {b['total_freq']} |\n")
                f.write('\n')
            else:
                f.write('*无突现*\n\n')

        f.write('---\n\n')
        f.write('## 3. Top 20 突现关键词\n\n')
        f.write('| 排名 | 关键词 | 突现区间 | 强度 | 总频次 |\n')
        f.write('|---|---|---|---|---|\n')
        for i, b in enumerate(bursts[:20], 1):
            f.write(f"| {i} | {b['keyword']} | {b['burst_start']}-{b['burst_end']} | {b['strength']} | {b['total_freq']} |\n")

        f.write('\n---\n\n')
        f.write('## 4. 突现解读\n\n')
        f.write('### 4.1 早期突现 (2015-2018)\n\n')
        f.write('以电力电子、射频器件相关术语为主，反映了半导体器件设计领域的传统热点。\n\n')
        f.write('### 4.2 中期突现 (2019-2022)\n\n')
        f.write('器件建模、磁性材料等主题出现突现，显示半导体建模方法的演进。\n\n')
        f.write('### 4.3 近期突现 (2023-2025)\n\n')
        f.write('**Transformer、deep learning、vision transformer** 等深度学习术语突现，')
        f.write('表明 Transformer 架构在半导体领域的研究在 2023 年后进入爆发期。\n\n')
        f.write('关键发现：\n')
        f.write('- `transformers` 在 2023-2025 突现，强度 2，总频次 76\n')
        f.write('- `deep learning` 在 2024-2025 突现，强度 2，总频次 37\n')
        f.write('- `vision transformer` 在 2025 突现，强度 1，总频次 12\n\n')

        f.write('---\n\n')
        f.write('**文档版本**：v1.0\n')
        f.write('**创建日期**：2026-05-01\n')

    print(f'报告保存至: {output_path}')


def main():
    output_dir = Path(__file__).parent.parent / 'outputs'

    csv_path = output_dir / 'keyword_bursts.csv'
    bursts = read_bursts(csv_path)

    # 绘图
    plot_burst_timeline(bursts, output_dir / 'keyword_burst_timeline.png', top_n=25)

    # 生成报告
    generate_report(bursts, output_dir / 'keyword_burst_report.md')


if __name__ == '__main__':
    main()
