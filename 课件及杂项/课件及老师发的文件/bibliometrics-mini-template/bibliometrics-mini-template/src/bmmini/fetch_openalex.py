from __future__ import annotations

import argparse
import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from tqdm import tqdm

from .utils import load_config, write_jsonl

OPENALEX_WORKS_URL = 'https://api.openalex.org/works'


def fetch_openalex_works(config: dict) -> list[dict]:
    """Fetch works from OpenAlex using cursor pagination and save raw JSON records.

    Requires an OpenAlex API key in environment variable OPENALEX_API_KEY.
    The key must never be committed to Git.
    """
    load_dotenv()
    api_key = os.getenv('OPENALEX_API_KEY')
    if not api_key:
        raise RuntimeError('OPENALEX_API_KEY is missing. Put it in .env or your shell environment.')

    data_cfg = config['data']
    max_records = int(data_cfg.get('max_records', 200))
    per_page = int(data_cfg.get('per_page', 50))
    filters = [
        f"publication_year:{data_cfg['from_year']}-{data_cfg['to_year']}",
        'has_references:true',
    ]
    if data_cfg.get('type'):
        filters.append(f"type:{data_cfg['type']}")

    params = {
        'search': data_cfg['query'],
        'filter': ','.join(filters),
        'per_page': per_page,
        'cursor': '*',
        'sort': '-cited_by_count',
        'api_key': api_key,
        'select': ','.join([
            'id','display_name','doi','publication_year','publication_date','cited_by_count',
            'authorships','keywords','topics','primary_location','referenced_works','abstract_inverted_index'
        ]),
    }

    all_works = []
    pbar = tqdm(total=max_records, desc='Fetching OpenAlex works')
    while len(all_works) < max_records:
        resp = requests.get(OPENALEX_WORKS_URL, params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        batch = payload.get('results', [])
        if not batch:
            break
        take = batch[: max_records - len(all_works)]
        all_works.extend(take)
        pbar.update(len(take))
        cursor = payload.get('meta', {}).get('next_cursor')
        if not cursor:
            break
        params['cursor'] = cursor
    pbar.close()
    return all_works


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config/query.yaml')
    args = parser.parse_args()
    config = load_config(args.config)
    works = fetch_openalex_works(config)
    out = Path(config['data']['raw_jsonl'])
    write_jsonl(out, works)
    print(f'Wrote {len(works)} records to {out}')


if __name__ == '__main__':
    main()
