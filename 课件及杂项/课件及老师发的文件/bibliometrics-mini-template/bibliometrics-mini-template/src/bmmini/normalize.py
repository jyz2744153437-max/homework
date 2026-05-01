from __future__ import annotations

from pathlib import Path
import re
from typing import Iterable

import pandas as pd


def _short_openalex_id(url_or_id: str | None) -> str | None:
    """Convert an OpenAlex URL to its short ID, e.g. https://openalex.org/W123 -> W123."""
    if not url_or_id:
        return None
    return str(url_or_id).rstrip('/').split('/')[-1]


def _clean_text(text: str | None) -> str:
    """Normalize whitespace in a text field."""
    if not text:
        return ''
    return re.sub(r'\s+', ' ', str(text)).strip()


def _get_source_name(work: dict) -> str:
    loc = work.get('primary_location') or {}
    source = loc.get('source') or {}
    return source.get('display_name') or ''


def _extract_authors(work: dict) -> list[dict]:
    rows = []
    work_id = _short_openalex_id(work.get('id'))
    for position, au in enumerate(work.get('authorships') or [], start=1):
        author = au.get('author') or {}
        institutions = au.get('institutions') or []
        inst_names = [i.get('display_name','') for i in institutions if i.get('display_name')]
        rows.append({
            'work_id': work_id,
            'author_id': _short_openalex_id(author.get('id')),
            'author_name': author.get('display_name') or '',
            'author_position': position,
            'institutions': '; '.join(inst_names),
        })
    return rows


def _extract_keywords(work: dict) -> list[dict]:
    rows = []
    work_id = _short_openalex_id(work.get('id'))
    # OpenAlex has keywords and topics; use both as a minimal classroom-friendly vocabulary.
    for kw in work.get('keywords') or []:
        name = kw.get('display_name') or kw.get('keyword') or ''
        if name:
            rows.append({'work_id': work_id, 'keyword': name.lower().strip(), 'source': 'keywords'})
    for topic in work.get('topics') or []:
        name = topic.get('display_name') or ''
        if name:
            rows.append({'work_id': work_id, 'keyword': name.lower().strip(), 'source': 'topics'})
    # De-duplicate within the work.
    seen = set()
    unique = []
    for r in rows:
        key = (r['work_id'], r['keyword'])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def normalize_openalex_records(records: Iterable[dict]) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Normalize raw OpenAlex records into works, reference pairs, authors, and keywords."""
    works, refs, authors, keywords = [], [], [], []
    for work in records:
        work_id = _short_openalex_id(work.get('id'))
        if not work_id:
            continue
        works.append({
            'work_id': work_id,
            'title': _clean_text(work.get('display_name')),
            'doi': work.get('doi') or '',
            'year': work.get('publication_year'),
            'publication_date': work.get('publication_date') or '',
            'venue': _get_source_name(work),
            'cited_by_count': int(work.get('cited_by_count') or 0),
            'n_references': len(work.get('referenced_works') or []),
        })
        for ref in work.get('referenced_works') or []:
            ref_id = _short_openalex_id(ref)
            if ref_id:
                refs.append({'work_id': work_id, 'reference_id': ref_id})
        authors.extend(_extract_authors(work))
        keywords.extend(_extract_keywords(work))

    return (
        pd.DataFrame(works).drop_duplicates('work_id'),
        pd.DataFrame(refs).drop_duplicates(),
        pd.DataFrame(authors).drop_duplicates(),
        pd.DataFrame(keywords).drop_duplicates(),
    )


def save_normalized(records: Iterable[dict], processed_dir: str | Path) -> dict[str, Path]:
    """Normalize and save the standard processed CSV files."""
    processed_dir = Path(processed_dir)
    processed_dir.mkdir(parents=True, exist_ok=True)
    works, refs, authors, keywords = normalize_openalex_records(records)
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
