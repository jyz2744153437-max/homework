from __future__ import annotations

from pathlib import Path
import json
import yaml


def load_config(path: str | Path) -> dict:
    """Load a YAML configuration file."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def ensure_dirs(config: dict) -> None:
    """Create standard output directories defined in the config."""
    for key in ['processed_dir', 'tables_dir', 'figures_dir', 'reports_dir']:
        Path(config['outputs'][key]).mkdir(parents=True, exist_ok=True)


def read_jsonl(path: str | Path) -> list[dict]:
    """Read a JSONL file into a list of dictionaries."""
    rows = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(path: str | Path, rows: list[dict]) -> None:
    """Write dictionaries as JSONL."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')
