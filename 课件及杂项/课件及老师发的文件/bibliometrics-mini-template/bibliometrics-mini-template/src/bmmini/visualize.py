from __future__ import annotations

from pathlib import Path
import json

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


_CLUSTER_COLORS = [
    '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6',
    '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b',
    '#2980b9', '#27ae60', '#d35400', '#8e44ad', '#f1c40f',
    '#7f8c8d', '#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4',
]


def _get_community_colors(G: nx.Graph, metrics_df: dict | None = None) -> dict[str, str]:
    """Assign a distinct color to each community/cluster."""
    if metrics_df is not None and 'community' in metrics_df.columns:
        comm_map = dict(zip(metrics_df['node'], metrics_df['community']))
    else:
        comm_map = {}
        for cid, nodes in enumerate(nx.algorithms.community.greedy_modularity_communities(G, weight='weight')):
            for n in nodes:
                comm_map[n] = cid
    unique_comms = sorted(set(comm_map.values()))
    color_map = {c: _CLUSTER_COLORS[c % len(_CLUSTER_COLORS)] for c in unique_comms}
    return {n: color_map.get(comm_map.get(n, 0), _CLUSTER_COLORS[0]) for n in G.nodes()}


def draw_network(G: nx.Graph, out_path: str | Path, title: str = '', top_labels: int = 12, seed: int = 42,
                 show_clusters: bool = True) -> None:
    """Draw a readable network map with optional cluster coloring.

    Args:
        G: NetworkX graph.
        out_path: Output path for the PNG file.
        title: Plot title.
        top_labels: Number of top weighted-degree nodes to label.
        seed: Random seed for layout reproducibility.
        show_clusters: If True, color nodes by community.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(16, 12))
    if G.number_of_nodes() == 0:
        plt.title(title + ' (empty graph)')
        plt.savefig(out_path, dpi=200, bbox_inches='tight')
        plt.close()
        return
    pos = nx.spring_layout(G, seed=seed, weight='weight', k=2.5/np.sqrt(max(G.number_of_nodes(), 1)))
    weighted_degree = dict(G.degree(weight='weight'))
    node_sizes = [80 + 35 * weighted_degree.get(n, 1) for n in G.nodes()]
    edge_widths = [0.4 + 0.15 * G[u][v].get('weight', 1) for u, v in G.edges()]

    if show_clusters:
        node_colors = list(_get_community_colors(G).values())
    else:
        node_colors = '#3498db'

    nx.draw_networkx_edges(G, pos, width=edge_widths, alpha=0.30, edge_color='#bdc3c7')
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, alpha=0.88, node_color=node_colors, edgecolors='#2c3e50', linewidths=0.6)
    top_nodes = sorted(G.nodes(), key=lambda n: weighted_degree.get(n, 0), reverse=True)[:top_labels]
    labels = {n: (n[:25] + '...' if len(n) > 25 else n) for n in top_nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=6.5, font_weight='normal')

    if show_clusters:
        comm_map = {}
        for cid, nodes in enumerate(nx.algorithms.community.greedy_modularity_communities(G, weight='weight')):
            for n in nodes:
                comm_map[n] = cid
        unique_comms = sorted(set(comm_map.values()))
        legend_handles = []
        for c in unique_comms[:10]:
            color = _CLUSTER_COLORS[c % len(_CLUSTER_COLORS)]
            size = sum(1 for v in comm_map.values() if v == c)
            legend_handles.append(plt.scatter([], [], c=color, s=80, label=f'Cluster {c} ({size} nodes)', edgecolors='#2c3e50', linewidths=0.6))
        if legend_handles:
            plt.legend(handles=legend_handles, loc='upper left', fontsize=7, framealpha=0.85, title='Communities')

    plt.title(title, fontsize=13, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()


def draw_network_interactive(G: nx.Graph, out_path: str | Path, title: str = '',
                              metrics_df=None, seed: int = 42) -> None:
    """Draw an interactive network graph as an HTML file using Plotly.

    Nodes are colored by community and sized by weighted degree.
    Hovering on a node shows its bibliometric metrics.
    Edges show source-target-weight information.

    Args:
        G: NetworkX graph.
        out_path: Output path for the HTML file.
        title: Plot title.
        metrics_df: DataFrame with node metrics (node, degree, betweenness, pagerank, community).
        seed: Random seed for layout.
    """
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if G.number_of_nodes() == 0:
        fig = go.Figure()
        fig.update_layout(title=title + ' (empty graph)')
        fig.write_html(str(out_path), include_plotlyjs=True)
        return

    pos = nx.spring_layout(G, seed=seed, weight='weight', k=2 / np.sqrt(max(G.number_of_nodes(), 1)))
    weighted_degree = dict(G.degree(weight='weight'))
    degree_dict = dict(G.degree())

    comm_map = {}
    for cid, nodes in enumerate(nx.algorithms.community.greedy_modularity_communities(G, weight='weight')):
        for n in nodes:
            comm_map[n] = cid

    metric_lookup = {}
    if metrics_df is not None and not metrics_df.empty:
        for _, row in metrics_df.iterrows():
            metric_lookup[row['node']] = row.to_dict()

    edge_traces = []
    max_w = max((G[u][v].get('weight', 1) for u, v in G.edges()), default=1)
    seen_edges = set()
    for u, v, data in G.edges(data=True):
        key = tuple(sorted([u, v]))
        if key in seen_edges:
            continue
        seen_edges.add(key)
        w = data.get('weight', 1)
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        width = 0.5 + 3 * (w / max_w)
        opacity = 0.15 + 0.25 * (w / max_w)
        hover_text = f'{u} <-> {v}<br>Weight: {w:.1f}'
        edge_traces.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            mode='lines',
            line=dict(width=width, color='#bdc3c7'),
            hoverinfo='text',
            text=hover_text,
            hoverlabel=dict(bgcolor='white', font_size=11),
            showlegend=False,
        ))

    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    node_sizes_arr = []

    max_wd = max(weighted_degree.values()) if weighted_degree else 1
    min_size, max_size = 8, 45
    for n in G.nodes():
        x, y = pos[n]
        node_x.append(x)
        node_y.append(y)
        wd = weighted_degree.get(n, 1)
        deg = degree_dict.get(n, 0)
        comm_id = comm_map.get(n, 0)
        color = _CLUSTER_COLORS[comm_id % len(_CLUSTER_COLORS)]
        node_colors.append(color)
        size = min_size + (max_size - min_size) * (wd / max(max_wd, 1))
        node_sizes_arr.append(size)
        m = metric_lookup.get(n, {})
        btwn = m.get('betweenness', 0)
        pr = m.get('pagerank', 0)
        comm_label = m.get('community', comm_id)
        display_name = str(n)
        if len(display_name) > 50:
            display_name = display_name[:47] + '...'
        hover = (
            f'<b>{display_name}</b><br>'
            f'-------------------<br>'
            f'Degree: {deg}<br>'
            f'Weighted Degree: {wd:.1f}<br>'
            f'Betweenness: {btwn:.4f}<br>'
            f'PageRank: {pr:.4f}<br>'
            f'Community: {comm_label}'
        )
        node_text.append(hover)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text' if G.number_of_nodes() <= 50 else 'markers',
        marker=dict(
            showscale=False,
            color=node_colors,
            size=node_sizes_arr,
            line=dict(width=1.2, color='#2c3e50'),
            opacity=0.88,
        ),
        text=node_text,
        hoverinfo='text',
        hoverlabel=dict(bgcolor='white', font_size=11, align='left'),
        customdata=list(range(len(node_x))),
        showlegend=False,
    )

    if G.number_of_nodes() <= 50:
        labels_short = {n: (str(n)[:20] + '...' if len(str(n)) > 20 else str(n)) for n in G.nodes()}
        node_trace.textposition = 'top center'
        node_trace.textfont = dict(size=7, color='#2c3e50')

    fig = go.Figure(data=edge_traces + [node_trace])

    unique_comms = sorted(set(comm_map.values()))
    for c in unique_comms:
        color = _CLUSTER_COLORS[c % len(_CLUSTER_COLORS)]
        count = sum(1 for v in comm_map.values() if v == c)
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode='markers',
            marker=dict(size=12, color=color, line=dict(width=1, color='#2c3e50')),
            name=f'Cluster {c} ({count} nodes)',
            showlegend=True,
        ))

    fig.update_layout(
        title=dict(text=f'<b>{title}</b>', font_size=16),
        showlegend=True,
        legend=dict(x=1.02, y=1.0, bgcolor='rgba(255,255,255,0.85)', bordercolor='#ddd', font_size=10),
        hovermode='closest',
        margin=dict(l=20, r=160, b=20, t=50),
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    )

    config = {'scrollZoom': True, 'displayModeBar': True, 'modeBarButtonsToRemove': ['lasso2d']}
    fig.write_html(str(out_path), config=config, include_plotlyjs='cdn')


def draw_cluster_summary(metrics_df, out_path: str | Path, network_name: str = '') -> None:
    """Generate a cluster/community summary table as HTML snippet."""
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if metrics_df is None or metrics_df.empty:
        return
    cluster_stats = metrics_df.groupby('community').agg(
        n_nodes=('node', 'count'),
        mean_weighted_degree=('weighted_degree', 'mean'),
        mean_betweenness=('betweenness', 'mean'),
        mean_pagerank=('pagerank', 'mean'),
        total_weighted_degree=('weighted_degree', 'sum'),
        top_node=('node', lambda x: '; '.join(x.head(3).tolist())),
    ).reset_index().sort_values('total_weighted_degree', ascending=False)

    modularity = 0.0
    return cluster_stats
