from __future__ import annotations

import networkx as nx
import pandas as pd


def graph_from_edges(edges: pd.DataFrame) -> nx.Graph:
    """Build an undirected weighted graph from an edge table."""
    G = nx.Graph()
    for _, r in edges.iterrows():
        G.add_edge(str(r['source']), str(r['target']), weight=float(r['weight']))
    return G


def add_distance_from_weight(G: nx.Graph) -> nx.Graph:
    """Add distance=1/weight for similarity networks.

    NetworkX betweenness interprets the weight argument as distance, while bibliometric edges usually store similarity/strength.
    """
    H = G.copy()
    for _, _, d in H.edges(data=True):
        w = float(d.get('weight', 1.0))
        d['distance'] = 1.0 / max(w, 1e-12)
    return H


def network_summary(G: nx.Graph) -> dict:
    """Calculate graph-level quality-control indicators."""
    n = G.number_of_nodes()
    m = G.number_of_edges()
    comps = list(nx.connected_components(G)) if n else []
    largest = max((len(c) for c in comps), default=0)
    modularity = 0.0
    n_communities = 0
    if G.number_of_edges() > 0 and n > 0:
        try:
            communities = list(nx.algorithms.community.greedy_modularity_communities(G, weight='weight'))
            modularity = nx.algorithms.community.modularity(G, communities, weight='weight')
            n_communities = len(communities)
        except Exception:
            pass
    avg_clustering = nx.average_clustering(G) if n > 1 else 0.0
    avg_degree = sum(dict(G.degree()).values()) / n if n > 0 else 0.0
    avg_weighted_degree = sum(dict(G.degree(weight='weight')).values()) / n if n > 0 else 0.0
    diameter = 0
    avg_path_length = 0.0
    if n > 1:
        largest_cc = max(nx.connected_components(G), key=len)
        subG = G.subgraph(largest_cc).copy()
        if subG.number_of_nodes() > 1:
            try:
                diameter = nx.diameter(subG)
                avg_path_length = nx.average_shortest_path_length(subG)
            except Exception:
                pass
    return {
        'n_nodes': n,
        'n_edges': m,
        'density': nx.density(G) if n > 1 else 0.0,
        'n_components': len(comps),
        'largest_component_ratio': largest / n if n else 0.0,
        'n_communities': n_communities,
        'modularity': round(modularity, 4),
        'avg_clustering_coefficient': round(avg_clustering, 4),
        'avg_degree': round(avg_degree, 2),
        'avg_weighted_degree': round(avg_weighted_degree, 2),
        'diameter_largest_component': diameter,
        'avg_path_length_largest_component': round(avg_path_length, 3),
    }


def node_metrics(G: nx.Graph) -> pd.DataFrame:
    """Calculate node-level metrics: degree, weighted degree, betweenness, PageRank, and community."""
    if G.number_of_nodes() == 0:
        return pd.DataFrame(columns=['node','degree','weighted_degree','betweenness','pagerank','community'])
    H = add_distance_from_weight(G)
    degree = dict(G.degree())
    weighted_degree = dict(G.degree(weight='weight'))
    betweenness = nx.betweenness_centrality(H, weight='distance', normalized=True)
    pagerank = nx.pagerank(G, weight='weight') if G.number_of_edges() else {n: 0 for n in G.nodes()}
    communities = {}
    if G.number_of_edges() > 0:
        for cid, nodes in enumerate(nx.algorithms.community.greedy_modularity_communities(G, weight='weight')):
            for n in nodes:
                communities[n] = cid
    else:
        communities = {n: 0 for n in G.nodes()}
    closeness = nx.closeness_centrality(G)
    eigenvector = {}
    try:
        eigenvector = nx.eigenvector_centrality(G, max_iter=1000, weight='weight')
    except Exception:
        eigenvector = {n: 0 for n in G.nodes()}
    rows = []
    for n in G.nodes():
        rows.append({
            'node': n,
            'degree': degree.get(n, 0),
            'weighted_degree': weighted_degree.get(n, 0.0),
            'betweenness': betweenness.get(n, 0.0),
            'pagerank': pagerank.get(n, 0.0),
            'closeness': closeness.get(n, 0.0),
            'eigenvector': eigenvector.get(n, 0.0),
            'community': communities.get(n, -1),
        })
    return pd.DataFrame(rows).sort_values(['weighted_degree','betweenness'], ascending=False)


def cluster_summary(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """Generate a per-cluster/community summary statistics table."""
    if metrics_df is None or metrics_df.empty or 'community' not in metrics_df.columns:
        return pd.DataFrame()
    stats = metrics_df.groupby('community').agg(
        n_nodes=('node', 'count'),
        mean_weighted_degree=('weighted_degree', 'mean'),
        mean_betweenness=('betweenness', 'mean'),
        mean_pagerank=('pagerank', 'mean'),
        mean_closeness=('closeness', 'mean'),
        mean_eigenvector=('eigenvector', 'mean'),
        total_weighted_degree=('weighted_degree', 'sum'),
        top_node=('node', lambda x: '; '.join(x.head(5).tolist())),
    ).reset_index().sort_values('total_weighted_degree', ascending=False)
    stats['pct_nodes'] = (stats['n_nodes'] / stats['n_nodes'].sum() * 100).round(1)
    return stats.reset_index(drop=True)


def h_index(citations: list[int] | pd.Series) -> int:
    """Compute the h-index from a list of citation counts."""
    vals = sorted([int(x) for x in citations if pd.notna(x)], reverse=True)
    h = 0
    for i, c in enumerate(vals, start=1):
        if c >= i:
            h = i
        else:
            break
    return h


def descriptive_indicators(works: pd.DataFrame, authors: pd.DataFrame) -> pd.DataFrame:
    """Calculate minimal descriptive bibliometric indicators."""
    indicators = {
        'n_works': len(works),
        'year_min': int(works['year'].min()) if not works.empty else None,
        'year_max': int(works['year'].max()) if not works.empty else None,
        'total_citations': int(works['cited_by_count'].fillna(0).sum()) if 'cited_by_count' in works else 0,
        'mean_citations': float(works['cited_by_count'].fillna(0).mean()) if not works.empty else 0,
        'h_index_seed_works': h_index(works['cited_by_count']) if 'cited_by_count' in works else 0,
        'n_authors': authors['author_name'].nunique() if not authors.empty else 0,
    }
    return pd.DataFrame([indicators])
