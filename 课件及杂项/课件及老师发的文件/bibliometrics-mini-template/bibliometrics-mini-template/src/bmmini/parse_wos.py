from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd


_WOS_TWO_LETTER_TAGS = {
    'PT', 'AU', 'AF', 'TI', 'SO', 'LA', 'DT', 'DE', 'ID', 'AB',
    'C1', 'RP', 'EM', 'FU', 'FX', 'CR', 'NR', 'TC', 'Z9', 'U1',
    'U2', 'PU', 'PI', 'PA', 'SN', 'EI', 'J9', 'JI', 'PD', 'PY',
    'VL', 'IS', 'BP', 'EP', 'DI', 'PG', 'WC', 'SC', 'GA', 'UT',
    'PM', 'OA', 'DA', 'ER', 'BN', 'CL', 'CT', 'CY', 'HO', 'OB',
    'OP', 'SE', 'BS', 'AR', 'SU', 'MA', 'NR',
}


def parse_wos_file(path: str | Path) -> list[dict]:
    """Parse a single Web of Science tagged export file into a list of record dicts.

    Each record is a dict mapping two-letter WoS tags to their string values.
    Multi-line fields (AU, AF, CR, C1, ID, DE, etc.) are joined with '; '.
    """
    path = Path(path)
    records = []
    current: dict[str, list[str]] = {}
    current_tag = ''

    with open(path, 'r', encoding='utf-8-sig') as f:
        for raw_line in f:
            line = raw_line.rstrip('\n\r')
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


def parse_wos_dir(dir_path: str | Path) -> list[dict]:
    """Parse all WoS .txt files in a directory and return combined records."""
    dir_path = Path(dir_path)
    all_records = []
    for txt_file in sorted(dir_path.glob('*.txt')):
        all_records.extend(parse_wos_file(txt_file))
    return all_records


def _parse_cr_reference(cr_str: str) -> str:
    """Normalize a single CR line into a reference identifier.

    Format: Author, Year, Source, V(volume), P(page) or DOI.
    We use 'Author_Year_Source' as a stable identifier.
    """
    parts = [p.strip() for p in cr_str.split(',')]
    if len(parts) >= 3:
        author = parts[0].strip()
        year = parts[1].strip()
        source = parts[2].strip()
        return f"{author}_{year}_{source}"
    return cr_str.strip()


def normalize_wos_records(records: Iterable[dict]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Normalize raw WoS records into works, reference pairs, authors, and keywords.

    Returns the same four DataFrames as normalize_openalex_records so the
    downstream pipeline (matrices, metrics, visualize) works unchanged.
    """
    works_list, refs_list, authors_list, keywords_list = [], [], [], []

    for rec in records:
        ut = rec.get('UT', '').strip()
        if not ut:
            continue
        work_id = ut

        works_list.append({
            'work_id': work_id,
            'title': rec.get('TI', '').strip(),
            'doi': rec.get('DI', '').strip(),
            'year': int(rec['PY']) if rec.get('PY', '').strip().isdigit() else None,
            'publication_date': rec.get('PD', '').strip(),
            'venue': rec.get('SO', '').strip(),
            'cited_by_count': int(rec['TC']) if rec.get('TC', '').strip().isdigit() else 0,
            'n_references': int(rec['NR']) if rec.get('NR', '').strip().isdigit() else 0,
        })

        cr_text = rec.get('CR', '')
        if cr_text:
            for cr_line in cr_text.split('; '):
                cr_line = cr_line.strip()
                if cr_line:
                    ref_id = _parse_cr_reference(cr_line)
                    refs_list.append({'work_id': work_id, 'reference_id': ref_id})

        au_text = rec.get('AU', '')
        if au_text:
            for position, au_name in enumerate(au_text.split('; '), start=1):
                au_name = au_name.strip()
                if au_name:
                    authors_list.append({
                        'work_id': work_id,
                        'author_id': '',
                        'author_name': au_name,
                        'author_position': position,
                        'institutions': '',
                    })

        kw_fields = []
        de_text = rec.get('DE', '')
        if de_text:
            for kw in de_text.split('; '):
                kw = kw.strip().lower()
                if kw:
                    kw_fields.append({'work_id': work_id, 'keyword': kw, 'source': 'author_keywords'})
        id_text = rec.get('ID', '')
        if id_text:
            for kw in id_text.split('; '):
                kw = kw.strip().lower()
                if kw:
                    kw_fields.append({'work_id': work_id, 'keyword': kw, 'source': 'keywords_plus'})
        keywords_list.extend(kw_fields)

    works_df = pd.DataFrame(works_list).drop_duplicates('work_id') if works_list else pd.DataFrame(
        columns=['work_id', 'title', 'doi', 'year', 'publication_date', 'venue', 'cited_by_count', 'n_references']
    )
    refs_df = pd.DataFrame(refs_list).drop_duplicates() if refs_list else pd.DataFrame(
        columns=['work_id', 'reference_id']
    )
    authors_df = pd.DataFrame(authors_list).drop_duplicates() if authors_list else pd.DataFrame(
        columns=['work_id', 'author_id', 'author_name', 'author_position', 'institutions']
    )
    keywords_df = pd.DataFrame(keywords_list).drop_duplicates() if keywords_list else pd.DataFrame(
        columns=['work_id', 'keyword', 'source']
    )

    return works_df, refs_df, authors_df, keywords_df


def save_normalized_wos(records: Iterable[dict], processed_dir: str | Path) -> dict[str, Path]:
    """Normalize WoS records and save the standard processed CSV files."""
    processed_dir = Path(processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)
    works, refs, authors, keywords = normalize_wos_records(records)
    paths = {
        'works': processed_dir / 'works_clean.csv',
        'references': processed_dir / 'work_references.csv',
        'authors': processed_dir / 'work_authors.csv',
        'keywords': processed_dir / 'work_keywords.csv',
    }
    works.to_csv(paths['works'], index=False)
    refs.to_csv(paths['references'], index=False)
    authors.to_csv(paths['authors'], index=False)
    keywords.to_csv(paths['keywords'], index=False)
    return paths
