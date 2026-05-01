from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.sparse import coo_matrix, csr_matrix


def build_incidence_matrix(edge_df: pd.DataFrame, row_col: str, col_col: str) -> tuple[csr_matrix, list[str], list[str]]:
    """Build a sparse 0/1 incidence matrix from an edge list.

    Example: paper-reference pairs -> A[paper, reference] = 1.
    """
    clean = edge_df[[row_col, col_col]].dropna().drop_duplicates()
    row_ids = pd.Index(sorted(clean[row_col].unique()))
    col_ids = pd.Index(sorted(clean[col_col].unique()))
    row_pos = row_ids.get_indexer(clean[row_col])
    col_pos = col_ids.get_indexer(clean[col_col])
    data = np.ones(len(clean), dtype=np.float32)
    mat = coo_matrix((data, (row_pos, col_pos)), shape=(len(row_ids), len(col_ids))).tocsr()
    return mat, row_ids.tolist(), col_ids.tolist()


def sparse_matrix_to_edges(mat: csr_matrix, ids: list[str], min_weight: float = 1, top_edges: int | None = None) -> pd.DataFrame:
    """Convert a square sparse matrix to an undirected edge list without self-loops."""
    coo = mat.tocoo()
    rows = []
    for i, j, w in zip(coo.row, coo.col, coo.data):
        if i >= j or w < min_weight:
            continue
        rows.append({'source': ids[i], 'target': ids[j], 'weight': float(w)})
    df = pd.DataFrame(rows)
    if df.empty:
        return pd.DataFrame(columns=['source','target','weight'])
    df = df.sort_values('weight', ascending=False)
    if top_edges is not None:
        df = df.head(int(top_edges))
    return df.reset_index(drop=True)


def bibliographic_coupling_edges(ref_df: pd.DataFrame, min_weight: float = 1, top_edges: int | None = None) -> pd.DataFrame:
    """Calculate bibliographic coupling edges.

    A is paper-reference incidence. Coupling matrix B = A @ A.T.
    B[i,j] is the number of shared references between two seed papers.
    """
    A, paper_ids, _ = build_incidence_matrix(ref_df, 'work_id', 'reference_id')
    B = (A @ A.T).tocsr()
    B.setdiag(0)
    B.eliminate_zeros()
    return sparse_matrix_to_edges(B, paper_ids, min_weight=min_weight, top_edges=top_edges)


def co_citation_edges(ref_df: pd.DataFrame, min_weight: float = 1, top_edges: int | None = None) -> pd.DataFrame:
    """Calculate co-citation edges among cited references.

    A is paper-reference incidence. Co-citation matrix C = A.T @ A.
    C[i,j] is the number of seed papers that cite both references i and j.
    """
    A, _, ref_ids = build_incidence_matrix(ref_df, 'work_id', 'reference_id')
    C = (A.T @ A).tocsr()
    C.setdiag(0)
    C.eliminate_zeros()
    return sparse_matrix_to_edges(C, ref_ids, min_weight=min_weight, top_edges=top_edges)


def keyword_cooccurrence_edges(keyword_df: pd.DataFrame, min_weight: float = 1, top_edges: int | None = None) -> pd.DataFrame:
    """Calculate keyword co-occurrence edges with W = K.T @ K."""
    if keyword_df.empty:
        return pd.DataFrame(columns=['source','target','weight'])
    K, _, keyword_ids = build_incidence_matrix(keyword_df, 'work_id', 'keyword')
    W = (K.T @ K).tocsr()
    W.setdiag(0)
    W.eliminate_zeros()
    return sparse_matrix_to_edges(W, keyword_ids, min_weight=min_weight, top_edges=top_edges)


def coauthorship_edges(author_df: pd.DataFrame, min_weight: float = 1, top_edges: int | None = None) -> pd.DataFrame:
    """Calculate author collaboration edges with M.T @ M."""
    if author_df.empty:
        return pd.DataFrame(columns=['source','target','weight'])
    clean = author_df.dropna(subset=['work_id','author_name']).copy()
    clean['author_name'] = clean['author_name'].str.strip()
    M, _, author_ids = build_incidence_matrix(clean, 'work_id', 'author_name')
    C = (M.T @ M).tocsr()
    C.setdiag(0)
    C.eliminate_zeros()
    return sparse_matrix_to_edges(C, author_ids, min_weight=min_weight, top_edges=top_edges)
