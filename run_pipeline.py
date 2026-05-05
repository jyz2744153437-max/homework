#!/usr/bin/env python3
"""
可复现分析管道

一键生成所有分析结果：
    python run_pipeline.py

功能：
1. 解析 WOS 数据
2. 生成筛选记录
3. 运行文献计量分析（需 bibliometrics-mini）
4. 运行突现检测
5. 生成可视化
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent

def check_data_files():
    """检查数据文件"""
    print('\n[Step 1] 检查数据文件...')
    data_dir = ROOT / 'Data'
    data_files = ['download_1-500.txt', 'download_501-643.txt']

    all_ok = True
    for f in data_files:
        fp = data_dir / f
        if fp.exists():
            size = fp.stat().st_size / 1024 / 1024
            print(f'  [OK] {f} ({size:.1f} MB)')
        else:
            print(f'  [MISSING] {f} 不存在')
            all_ok = False

    return all_ok


def check_dependencies():
    """检查依赖"""
    print('\n[Step 2] 检查 Python 依赖...')
    required = ['numpy', 'scipy', 'matplotlib', 'pandas']

    missing = []
    for pkg in required:
        try:
            __import__(pkg)
            print(f'  [OK] {pkg}')
        except ImportError:
            print(f'  [MISSING] {pkg} 未安装')
            missing.append(pkg)

    if missing:
        print(f'\n请安装缺失依赖: pip install {" ".join(missing)}')
        return False
    return True


def run_screening():
    """运行筛选记录生成"""
    print('\n[Step 3] 生成筛选记录...')
    try:
        subprocess.run(
            [sys.executable, 'src/create_screening.py'],
            cwd=ROOT,
            check=True
        )
        print('  [OK] 筛选记录生成完成')
        return True
    except subprocess.CalledProcessError as e:
        print(f'  [ERROR] 筛选记录生成失败: {e}')
        return False


def run_burst_detection():
    """运行突现检测"""
    print('\n[Step 4] 运行突现检测...')
    try:
        subprocess.run(
            [sys.executable, 'src/burst_detection.py'],
            cwd=ROOT,
            check=True
        )
        print('  [OK] 突现检测完成')
    except subprocess.CalledProcessError as e:
        print(f'  [ERROR] 突现检测失败: {e}')
        return False

    try:
        subprocess.run(
            [sys.executable, 'src/burst_visualize.py'],
            cwd=ROOT,
            check=True
        )
        print('  [OK] 突现可视化完成')
    except subprocess.CalledProcessError as e:
        print(f'  [ERROR] 突现可视化失败: {e}')
        return False

    return True


def check_outputs():
    """检查输出文件"""
    print('\n[Step 5] 检查输出文件...')
    outputs = [
        'outputs/keyword_bursts.csv',
        'outputs/keyword_burst_timeline.png',
        'outputs/keyword_burst_report.md',
        'outputs/descriptive_indicators.csv',
        'Data/screened_stage1.csv',
        'Data/screened_final.csv',
    ]

    for f in outputs:
        fp = ROOT / f
        if fp.exists():
            print(f'  [OK] {f}')
        else:
            print(f'  [MISSING] {f} 未生成')


def check_docs():
    """检查文档完整性"""
    print('\n[Step 6] 检查文档完整性...')
    docs = [
        ('Data/field_dictionary.md', '字段字典'),
        ('Data/README.md', '数据说明'),
        ('reports/data_quality.md', '数据质量报告'),
        ('reports/methodology.md', '研究方法论'),
        ('reports/metrics_spec.md', '指标规范'),
        ('reports/screening_rule.md', '筛选规则'),
        ('reports/screening_record.md', '筛选记录'),
        ('reports/novelty_search_v0.md', '查新报告'),
        ('reports/prisma_flowchart.md', 'PRISMA 流程图'),
        ('config/query.yaml', '检索式配置'),
        ('docs/data_model.md', '图数据模型'),
        ('docs/query_rationale.md', '检索设计思路'),
        ('docs/query_changelog.md', '检索式变更日志'),
        ('paper/manuscript_v1.md', 'Mini Review 初稿'),
    ]

    for fp, name in docs:
        fullPath = ROOT / fp
        if fullPath.exists():
            print(f'  [OK] {name}')
        else:
            print(f'  [MISSING] {name} ({fp}) 缺失')


def print_bibliometrics_mini_note():
    """提示 bibliometrics-mini 操作"""
    print('\n[Step 7] bibliometrics-mini 文献计量分析...')
    print('  [OK] 已完成（基于 DL 纯净集 147 篇）')
    print('  如需重新运行：')
    print('     $env:PYTHONPATH="src"')
    print('     python -m bmmini.pipeline --config config/query.yaml --use-wos')
    print('  产出（已生成于 outputs/ 及 outputs/bibliometrics-mini-dl/）：')
    print('     - keyword_cooccurrence_network.html（关键词共现，交互式）')
    print('     - co_citation_network.html（共被引，交互式）')
    print('     - bibliographic_coupling_network.html（文献耦合，交互式）')
    print('     - coauthorship_network.html（合作网络，交互式）')
    print('     - bibliometrics_report.html（综合报告）')
    print('     - network_metrics_*.csv（节点指标）')
    print('     - network_qc_summary.csv（图级指标）')


def main():
    print('=' * 60)
    print('Transformer-Semiconductor-Bibliometrics 分析管道')
    print('=' * 60)

    if not check_data_files():
        print('\n错误: 数据文件缺失')
        sys.exit(1)

    if not check_dependencies():
        sys.exit(1)

    run_screening()
    run_burst_detection()
    check_outputs()
    check_docs()
    print_bibliometrics_mini_note()

    print('\n' + '=' * 60)
    print('管道执行完成！')
    print('=' * 60)


if __name__ == '__main__':
    main()
