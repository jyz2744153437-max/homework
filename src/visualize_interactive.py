"""重新生成交互式网络图——优化标签显示和可读性"""
from pathlib import Path
import pandas as pd
import networkx as nx
import plotly.graph_objects as go
import numpy as np

CLUSTER_COLORS = [
    '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6',
    '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b',
    '#2980b9', '#27ae60', '#d35400', '#8e44ad', '#f1c40f',
    '#7f8c8d', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4',
]

NETWORK_NAMES = {
    'keyword_cooccurrence': '关键词共现网络',
    'co_citation': '共被引网络',
    'bibliographic_coupling': '文献耦合网络',
    'coauthorship': '合作网络',
}

EDGE_FILES = {
    'keyword_cooccurrence': 'outputs/keyword_cooccurrence_edges.csv',
    'co_citation': 'outputs/co_citation_edges.csv',
    'bibliographic_coupling': 'outputs/bibliographic_coupling_edges.csv',
    'coauthorship': 'outputs/coauthorship_edges.csv',
}

METRIC_FILES = {
    'keyword_cooccurrence': 'outputs/network_metrics_keyword_cooccurrence.csv',
    'co_citation': 'outputs/network_metrics_co_citation.csv',
    'bibliographic_coupling': 'outputs/network_metrics_bibliographic_coupling.csv',
    'coauthorship': 'outputs/network_metrics_coauthorship.csv',
}


def build_graph(edge_file, metric_file):
    edges = pd.read_csv(edge_file)
    G = nx.Graph()
    for _, row in edges.iterrows():
        G.add_edge(str(row['source']), str(row['target']), weight=float(row['weight']))
    metrics = pd.read_csv(metric_file)
    return G, metrics


def make_interactive(G, metrics, out_path, title, top_labels=30):
    if G.number_of_nodes() == 0:
        return

    # 用 spring_layout 但增大 k 让节点更分散
    pos = nx.spring_layout(G, seed=42, weight='weight', k=3.5 / np.sqrt(max(G.number_of_nodes(), 1)), iterations=100)
    weighted_degree = dict(G.degree(weight='weight'))

    # 社团颜色
    comm_map = {}
    if 'community' in metrics.columns:
        for _, row in metrics.iterrows():
            comm_map[str(row['node'])] = int(row['community'])
    if not comm_map:
        for cid, nodes in enumerate(nx.algorithms.community.greedy_modularity_communities(G, weight='weight')):
            for n in nodes:
                comm_map[n] = cid

    # 指标查找表
    metric_lookup = {}
    if not metrics.empty:
        for _, row in metrics.iterrows():
            metric_lookup[str(row['node'])] = row.to_dict()

    # === 边（只显示最强的 N 条） ===
    edge_traces = []
    max_w = max((G[u][v].get('weight', 1) for u, v in G.edges()), default=1)
    sorted_edges = sorted(G.edges(data=True), key=lambda e: e[2].get('weight', 1), reverse=True)[:150]
    for u, v, data in sorted_edges:
        w = data.get('weight', 1)
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        width = 0.3 + 2.5 * (w / max_w)
        opacity = 0.12 + 0.28 * (w / max_w)
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode='lines',
            line=dict(width=width, color='#bdc3c7'),
            hoverinfo='text',
            text=f'{u[:40]} ↔ {v[:40]}<br>权重: {w:.1f}',
            hoverlabel=dict(bgcolor='white', font_size=10),
            showlegend=False,
        ))

    # === 节点 ===
    node_x, node_y, node_text, node_colors, node_sizes_arr = [], [], [], [], []
    max_wd = max(weighted_degree.values()) if weighted_degree else 1
    min_size, max_size = 10, 55
    top_nodes = sorted(G.nodes(), key=lambda n: weighted_degree.get(n, 0), reverse=True)[:top_labels]

    for n in G.nodes():
        x, y = pos[n]
        node_x.append(x)
        node_y.append(y)
        wd = weighted_degree.get(n, 1)
        comm_id = comm_map.get(n, 0)
        node_colors.append(CLUSTER_COLORS[comm_id % len(CLUSTER_COLORS)])
        node_sizes_arr.append(min_size + (max_size - min_size) * (wd / max(max_wd, 1)))

        m = metric_lookup.get(n, {})
        deg = m.get('degree', 0)
        btwn = m.get('betweenness', 0)
        pr = m.get('pagerank', 0)
        display = str(n)
        if len(display) > 55:
            display = display[:52] + '...'
        hover = (
            f'<b>{display}</b><br>'
            f'<span style="color:#888">────────────────</span><br>'
            f'度 (Degree): {deg}<br>'
            f'加权度: {wd:.1f}<br>'
            f'中介中心性: {btwn:.4f}<br>'
            f'PageRank: {pr:.4f}'
        )
        node_text.append(hover)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        marker=dict(
            showscale=False, color=node_colors, size=node_sizes_arr,
            line=dict(width=1.5, color='#2c3e50'), opacity=0.9,
        ),
        text=node_text, hoverinfo='text',
        hoverlabel=dict(bgcolor='white', font_size=11, align='left'),
        showlegend=False,
    )

    # === 为 top N 节点单独加标签层 ===
    label_x, label_y, label_texts = [], [], []
    for n in top_nodes:
        if n in pos:
            label_x.append(pos[n][0])
            label_y.append(pos[n][1])
            short = str(n)
            if len(short) > 18:
                short = short[:16] + '..'
            label_texts.append(short)

    label_trace = go.Scatter(
        x=label_x, y=label_y,
        mode='text',
        text=label_texts,
        textposition='top center',
        textfont=dict(size=8, color='#2c3e50'),
        hoverinfo='none',
        showlegend=False,
    )

    # === 图例 ===
    fig = go.Figure(data=edge_traces + [node_trace, label_trace])
    unique_comms = sorted(set(comm_map.values()))
    for c in unique_comms:
        color = CLUSTER_COLORS[c % len(CLUSTER_COLORS)]
        count = sum(1 for v in comm_map.values() if v == c)
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode='markers',
            marker=dict(size=11, color=color, line=dict(width=1, color='#2c3e50')),
            name=f'社团 {c} ({count}节点)',
            showlegend=True,
        ))

    fig.update_layout(
        title=dict(text=f'<b>{title}</b>', font_size=17),
        showlegend=True,
        legend=dict(x=1.02, y=1.0, bgcolor='rgba(255,255,255,0.9)', bordercolor='#ddd', font_size=10),
        hovermode='closest',
        margin=dict(l=20, r=160, b=20, t=55),
        paper_bgcolor='white', plot_bgcolor='white',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )

    config = {'scrollZoom': True, 'displayModeBar': True, 'modeBarButtonsToRemove': ['lasso2d']}
    fig.write_html(str(out_path), config=config, include_plotlyjs='cdn')
    print(f'  OK {out_path}  ({G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {top_labels} labels)')


def main():
    import sys
    names = sys.argv[1:] if len(sys.argv) > 1 else list(NETWORK_NAMES.keys())

    for key in names:
        if key not in NETWORK_NAMES:
            print(f'  Skipping unknown: {key}')
            continue
        print(f'Generating {NETWORK_NAMES[key]}...')
        G, metrics = build_graph(EDGE_FILES[key], METRIC_FILES[key])
        out = f'outputs/{key}_network.html'
        make_interactive(G, metrics, out, NETWORK_NAMES[key])


if __name__ == '__main__':
    main()
