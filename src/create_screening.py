#!/usr/bin/env python3
"""筛选记录生成脚本"""

import re
from pathlib import Path
import pandas as pd

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

def create_screening_csv(records, output_path):
    """创建筛选记录 CSV"""
    rows = []
    for rec in records:
        ut = rec.get('UT', '').strip()
        if not ut:
            continue

        rows.append({
            'work_id': ut,
            'title': rec.get('TI', '').strip(),
            'doi': rec.get('DI', '').strip(),
            'year': int(rec['PY']) if rec.get('PY', '').strip().isdigit() else None,
            'venue': rec.get('SO', '').strip(),
            'cited_by_count': int(rec['TC']) if rec.get('TC', '').strip().isdigit() else 0,
            'n_references': int(rec['NR']) if rec.get('NR', '').strip().isdigit() else 0,
            'stage1_status': 'include',
            'stage1_reason': '',
            'stage2_status': 'include',
            'stage2_reason': '',
        })

    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
    return len(df)

if __name__ == '__main__':
    data_dir = Path(__file__).parent.parent / 'Data'

    # 解析 WoS 数据
    records = parse_wos_dir(data_dir)
    print(f'解析到 {len(records)} 条文献')

    # 创建筛选记录
    stage1_path = data_dir / 'screened_stage1.csv'
    n = create_screening_csv(records, stage1_path)
    print(f'生成 screened_stage1.csv: {n} 条')

    # 复制为 final
    final_path = data_dir / 'screened_final.csv'
    pd.read_csv(stage1_path).to_csv(final_path, index=False)
    print(f'生成 screened_final.csv: {n} 条')