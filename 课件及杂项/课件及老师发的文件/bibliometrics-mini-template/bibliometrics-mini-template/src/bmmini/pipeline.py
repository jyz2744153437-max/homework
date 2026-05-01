from __future__ import annotations

import argparse
import os
from pathlib import Path
from datetime import datetime

import pandas as pd

from .utils import load_config, ensure_dirs, read_jsonl
from .normalize import save_normalized
from .parse_wos import parse_wos_dir, save_normalized_wos
from .matrices import (
    bibliographic_coupling_edges,
    co_citation_edges,
    keyword_cooccurrence_edges,
    coauthorship_edges,
)
from .metrics import graph_from_edges, node_metrics, network_summary, descriptive_indicators, cluster_summary
from .visualize import draw_network, draw_network_interactive


def run_pipeline(config: dict, use_sample: bool = False, use_wos: bool = False) -> None:
    """Run the full minimal bibliometrics pipeline."""
    ensure_dirs(config)

    processed_dir = Path(config['outputs']['processed_dir'])
    tables_dir = Path(config['outputs']['tables_dir'])
    figures_dir = Path(config['outputs']['figures_dir'])
    reports_dir = Path(config['outputs']['reports_dir'])

    if use_wos:
        wos_dir = config['data'].get('wos_dir', 'data/sample-wos')
        records = parse_wos_dir(wos_dir)
        paths = save_normalized_wos(records, config['outputs']['processed_dir'])
        raw_path = wos_dir
    else:
        raw_path = Path(config['data']['sample_jsonl'] if use_sample else config['data']['raw_jsonl'])
        records = read_jsonl(raw_path)
        paths = save_normalized(records, config['outputs']['processed_dir'])

    works = pd.read_csv(paths['works'])
    refs = pd.read_csv(paths['references'])
    authors = pd.read_csv(paths['authors'])
    keywords = pd.read_csv(paths['keywords'])

    min_w = config['analysis'].get('min_edge_weight', 1)
    top_edges = config['analysis'].get('top_edges', 200)
    seed = config['analysis'].get('layout_seed', 42)
    top_labels = config['analysis'].get('top_labels', 12)

    edge_tables = {
        'keyword_cooccurrence': keyword_cooccurrence_edges(keywords, min_weight=min_w, top_edges=top_edges),
        'co_citation': co_citation_edges(refs, min_weight=min_w, top_edges=top_edges),
        'bibliographic_coupling': bibliographic_coupling_edges(refs, min_weight=min_w, top_edges=top_edges),
        'coauthorship': coauthorship_edges(authors, min_weight=min_w, top_edges=top_edges),
    }

    summaries = []
    network_results = {}
    for name, edges in edge_tables.items():
        edge_path = tables_dir / f'{name}_edges.csv'
        edges.to_csv(edge_path, index=False)
        G = graph_from_edges(edges)
        metrics = node_metrics(G)
        metrics.to_csv(tables_dir / f'network_metrics_{name}.csv', index=False)
        csum = cluster_summary(metrics)
        if not csum.empty:
            csum.to_csv(tables_dir / f'cluster_summary_{name}.csv', index=False)
        summary = network_summary(G)
        summary['network'] = name
        summaries.append(summary)

        title_display = name.replace('_', ' ').title()
        draw_network(G, figures_dir / f'{name}_network.png', title=title_display, top_labels=top_labels, seed=seed)
        draw_network_interactive(
            G, figures_dir / f'{name}_network.html',
            title=title_display, metrics_df=metrics, seed=seed
        )

        network_results[name] = {
            'graph': G,
            'edges': edges,
            'metrics': metrics,
            'cluster_summary': csum,
            'summary': summary,
        }

    pd.DataFrame(summaries).to_csv(tables_dir / 'network_qc_summary.csv', index=False)
    desc_indicators = descriptive_indicators(works, authors)
    desc_indicators.to_csv(tables_dir / 'descriptive_indicators.csv', index=False)

    _generate_html_report(
        reports_dir=reports_dir,
        tables_dir=tables_dir,
        figures_dir=figures_dir,
        network_results=network_results,
        desc_indicators=desc_indicators,
        raw_data_source=str(raw_path),
        n_works=len(works), n_refs=len(refs), n_authors=len(authors), n_keywords=len(keywords),
        seed=seed, top_edges=top_edges, min_edge_weight=min_w,
    )

    with open(reports_dir / 'method_note.md', 'w', encoding='utf-8') as f:
        f.write('# Method note\n\n')
        f.write(f"Raw data: `{raw_path}`\n\n")
        f.write(f"Seed works: {len(works)}; reference pairs: {len(refs)}; authorship rows: {len(authors)}; keyword rows: {len(keywords)}.\n\n")
        f.write('Matrices: keyword W=K.T@K; co-citation C=A.T@A; bibliographic coupling B=A@A.T.\n')
        f.write('Betweenness centrality uses distance=1/weight for similarity networks.\n')

    print('Pipeline finished. See outputs/tables, outputs/figures, and reports.')


def _df_to_html_table(df: pd.DataFrame, caption: str = '', max_rows: int = 50) -> str:
    """Convert a DataFrame to a styled HTML table string."""
    if df is None or df.empty:
        return f'<p class="text-muted">No data available for <b>{caption}</b>.</p>'
    display_df = df.head(max_rows).copy()
    display_df = display_df.map(lambda x: round(x, 4) if isinstance(x, float) else x)
    html = display_df.to_html(classes='table table-striped table-hover table-sm table-bordered', index=False, escape=False)
    if caption:
        html = f'<h5>{caption}</h5>\n{html}'
    return html


def _generate_html_report(reports_dir: Path, tables_dir: Path, figures_dir: Path,
                           network_results: dict, desc_indicators: pd.DataFrame,
                           raw_data_source: str, n_works: int, n_refs: int,
                           n_authors: int, n_keywords: int,
                           seed: int, top_edges: int, min_edge_weight: int) -> None:
    """Generate a comprehensive HTML report embedding all figures and tables."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    fig_rel_base = Path(os.path.relpath(figures_dir.resolve(), reports_dir.resolve()))

    network_sections = []
    net_names_order = ['keyword_cooccurrence', 'co_citation', 'bibliographic_coupling', 'coauthorship']
    net_titles = {
        'keyword_cooccurrence': 'Keyword Co-occurrence Network (W = K.T @ K)',
        'co_citation': 'Co-citation Network (C = A.T @ A)',
        'bibliographic_coupling': 'Bibliographic Coupling Network (B = A @ A.T)',
        'coauthorship': 'Co-authorship Collaboration Network',
    }

    for name in net_names_order:
        if name not in network_results:
            continue
        res = network_results[name]
        s = res['summary']
        m = res['metrics']
        cs = res.get('cluster_summary', pd.DataFrame())
        title = net_titles.get(name, name.replace('_', ' ').title())

        png_rel = figures_dir / f'{name}_network.png'
        html_rel = figures_dir / f'{name}_network.html'
        png_href = fig_rel_base / png_rel.name
        html_href = fig_rel_base / html_rel.name

        section_parts = [
            f'<div id="section-{name}" class="network-section mb-5">',
            f'<h3 class="mt-4 mb-3">{title}</h3>',
        ]

        section_parts.append('<div class="row"><div class="col-md-6">')
        section_parts.append(f'<h5>Network Overview</h5>')
        overview_items = [
            ('Nodes', s.get('n_nodes', '-')),
            ('Edges', s.get('n_edges', '-')),
            ('Density', f"{s.get('density', 0):.4f}"),
            ('Communities', s.get('n_communities', '-')),
            ('Modularity', f"{s.get('modularity', 0):.4f}"),
            ('Avg Clustering Coefficient', f"{s.get('avg_clustering_coefficient', 0):.4f}"),
            ('Avg Degree', f"{s.get('avg_degree', 0):.2f}"),
            ('Avg Weighted Degree', f"{s.get('avg_weighted_degree', 0):.2f}"),
            ('Components', s.get('n_components', '-')),
            ('Largest Component Ratio', f"{s.get('largest_component_ratio', 0):.2%}" if isinstance(s.get('largest_component_ratio'), float) else str(s.get('largest_component_ratio', '-'))),
        ]
        if s.get('diameter_largest_component', 0) > 0:
            overview_items.append(('Diameter (Largest CC)', s['diameter_largest_component']))
        if s.get('avg_path_length_largest_component', 0) > 0:
            overview_items.append(('Avg Path Length (Largest CC)', f"{s['avg_path_length_largest_component']:.3f}"))
        section_parts.append('<table class="table table-sm table-bordered">')
        section_parts.append('<tbody>')
        for label, val in overview_items:
            section_parts.append(f'<tr><th style="width:45%">{label}</th><td>{val}</td></tr>')
        section_parts.append('</tbody></table>')

        section_parts.append('</div><div class="col-md-6">')
        section_parts.append(f'<h5>Static Network Map</h5>')
        if png_rel.exists():
            section_parts.append(f'<a href="{png_href}" target="_blank"><img src="{png_href}" class="img-fluid rounded border shadow-sm" alt="{title}" style="max-width:100%;"></a>')
            section_parts.append(f'<p class="small text-muted mt-1">Click to enlarge. Nodes colored by community/cluster.</p>')
        else:
            section_parts.append('<p class="text-muted">Image not available.</p>')
        section_parts.append('</div></div>')

        section_parts.append(f'<hr class="my-3"><h5>Interactive Network Map</h5>')
        section_parts.append(f'<iframe src="{html_href}" width="100%" height="600" frameborder="0" class="border rounded shadow-sm" allowfullscreen></iframe>')
        section_parts.append(f'<p class="small text-muted mt-1">Hover over nodes to see detailed metrics. Drag nodes to reposition. Scroll to zoom.</p>')

        section_parts.append(f'<hr class="my-3"><h5>Top-20 Node Metrics</h5>')
        m_top = m.head(20)[['node','degree','weighted_degree','betweenness','pagerank','closeness','community']].copy()
        m_top = m_top.map(lambda x: round(x, 4) if isinstance(x, float) else x)
        m_top.columns = ['Node', 'Degree', 'Weighted Deg.', 'Betweenness', 'PageRank', 'Closeness', 'Cluster']
        section_parts.append(m_top.to_html(classes='table table-striped table-hover table-sm table-bordered', index=False))

        if cs is not None and not cs.empty:
            section_parts.append(f'<hr class="my-3"><h5>Cluster / Community Summary</h5>')
            cs_disp = cs.copy()
            cs_disp = cs_disp.map(lambda x: round(x, 4) if isinstance(x, float) else x)
            cs_disp.columns = [c.replace('_', ' ').title() for c in cs_disp.columns]
            section_parts.append(cs_disp.to_html(classes='table table-striped table-hover table-sm table-bordered', index=False))

        section_parts.append('</div>')
        network_sections.append('\n'.join(section_parts))

    desc_items = []
    if not desc_indicators.empty:
        row = desc_indicators.iloc[0]
        labels_map = {
            'n_works': 'Total Seed Works',
            'year_min': 'Earliest Year',
            'year_max': 'Latest Year',
            'total_citations': 'Total Citations',
            'mean_citations': 'Mean Citations per Work',
            'h_index_seed_works': 'H-index (Seed Works)',
            'n_authors': 'Unique Authors',
        }
        for col, lbl in labels_map.items():
            val = row.get(col)
            if val is None:
                continue
            if isinstance(val, float):
                desc_items.append((lbl, f'{val:.2f}'))
            else:
                desc_items.append((lbl, str(val)))

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Bibliometrics Report - {now.split()[0]}</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background-color: #f8f9fa; }}
.report-header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem 0; margin-bottom: 2rem; }}
.report-header h1 {{ margin-bottom: 0.3rem; }}
.network-section {{ background: white; border-radius: 8px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
.table {{ font-size: 0.9rem; }}
.table th {{ background-color: #f1f3f5; position: sticky; top: 0; }}
.badge-cluster {{ font-size: 0.75em; }}
.toc-nav {{ position: sticky; top: 1rem; }}
@media print {{ .no-print {{ display: none !important; }} iframe {{ display: none; }} img {{ max-width: 100%; page-break-inside: avoid; }} .network-section {{ break-inside: avoid; }} }}
</style>
</head>
<body>

<div class="report-header">
<div class="container">
<h1>Bibliometrics Analysis Report</h1>
<p class="mb-0 opacity-75">Generated on {now} | Data source: <code>{raw_data_source}</code></p>
</div>
</div>

<div class="container">
<nav aria-label="breadcrumb" class="mb-3 no-print">
<ol class="breadcrumb">
<li class="breadcrumb-item active">Report Home</li>
</ol>
</nav>

<div class="row">
<div class="col-lg-3 no-print">
<div class="card sticky-top toc-nav" style="top:1rem;">
<div class="card-header bg-light fw-bold">Table of Contents</div>
<ul class="list-group list-group-flush">
<li class="list-group-item list-group-item-action"><a href="#overview">Overview</a></li>
'''
    for name in net_names_order:
        if name in network_results:
            html_content += f'<li class="list-group-item list-group-item-action"><a href="#section-{name}">{net_titles.get(name, name)}</a></li>\n'
    html_content += '''</ul></div></div>

<div class="col-lg-9">

<section id="overview" class="network-section mb-4">
<h3>Data Overview & Descriptive Indicators</h3>
<div class="row">
<div class="col-md-6">
<table class="table table-sm table-bordered">
<tbody>
<tr><th>Seed Works</th><td>{n_works:,}</td></tr>
<tr><th>Reference Pairs</th><td>{n_refs:,}</td></tr>
<tr><th>Authorship Rows</th><td>{n_authors:,}</td></tr>
<tr><th>Keyword Rows</th><td>{n_keywords:,}</td></tr>
</tbody>
</table>
</div>
<div class="col-md-6">
<table class="table table-sm table-bordered">
<tbody>
'''.format(n_works=n_works, n_refs=n_refs, n_authors=n_authors, n_keywords=n_keywords)

    for i, (label, value) in enumerate(desc_items):
        if i > 0 and i % 2 == 0:
            pass
        html_content += f'<tr><th>{label}</th><td>{value}</td></tr>\n'
    html_content += '''</tbody></table></div></div>
<hr>
<p><strong>Analysis Parameters:</strong> layout_seed={seed}, top_edges={top_edges}, min_edge_weight={min_edge_weight}</p>
<p><strong>Formulas:</strong> Keyword co-occurrence W = K.T @ K | Co-citation C = A.T @ A | Bibliographic coupling B = A @ A.T<br>
Betweenness centrality uses distance = 1/weight for similarity-weighted networks.</p>
</section>

'''

    html_content += '\n'.join(network_sections)

    html_content += '''
</div>
</div>

<footer class="text-center text-muted py-4 mt-5 border-top no-print">
<small>Bibliometrics-mini Pipeline Report | Generated automatically</small>
</footer>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
'''

    report_path = reports_dir / 'bibliometrics_report.html'
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='config/query.yaml')
    parser.add_argument('--use-sample', action='store_true')
    parser.add_argument('--use-wos', action='store_true')
    args = parser.parse_args()
    run_pipeline(load_config(args.config), use_sample=args.use_sample, use_wos=args.use_wos)


if __name__ == '__main__':
    main()
