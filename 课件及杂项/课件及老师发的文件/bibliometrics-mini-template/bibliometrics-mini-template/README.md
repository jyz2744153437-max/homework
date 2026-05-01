# bibliometrics-mini

A minimal Python bibliometrics project for course practice: OpenAlex / Web of Science data fetching, data cleaning, co-citation, bibliographic coupling, collaboration/co-occurrence networks, metrics, interactive visualizations, and comprehensive reports.

## Quick start

### Using Web of Science data (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
$env:PYTHONPATH="src"           # PowerShell
python -m bmmini.pipeline --config config/query.yaml --use-wos
```

### Using OpenAlex sample data

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
$env:PYTHONPATH="src"
python -m bmmini.pipeline --config config/query.yaml --use-sample
```

Outputs are written to `outputs/tables/`, `outputs/figures/`, and `reports/`.

## Data sources

### Web of Science (WoS)

Place WoS tagged export `.txt` files in `data/sample-wos/`. The pipeline parses all `.txt` files in that directory, extracting:

- **PT** → publication type | **AU** → authors | **TI** → title | **SO** → source (journal)
- **DE** → author keywords | **ID** → Keywords Plus | **CR** → cited references
- **PY** → publication year | **TC** → times cited | **DI** → DOI | **UT** → WoS unique ID

Run with `--use-wos` flag:

```bash
$env:PYTHONPATH="src"
python -m bmmini.pipeline --config config/query.yaml --use-wos
```

### OpenAlex API key

Create `.env` at project root:

```bash
OPENALEX_API_KEY=your_key_here
```

Then run:

```bash
$env:PYTHONPATH="src"
python -m bmmini.fetch_openalex --config config/query.yaml
python -m bmmini.pipeline --config config/query.yaml
```

## Makefile commands

| Command | Description |
|---------|-------------|
| `make wos` | Run pipeline with WoS data |
| `make sample` | Run pipeline with OpenAlex sample data |
| `make fetch` | Fetch data from OpenAlex API |
| `make run` | Run pipeline with OpenAlex data |
| `make test` | Run tests |

## What is produced

### Processed data (`data/processed/`)

- `works_clean.csv`: normalized seed works (work_id, title, doi, year, venue, cited_by_count, n_references)
- `work_references.csv`: paper-reference pairs
- `work_authors.csv`: paper-author pairs
- `work_keywords.csv`: paper-keyword pairs

### Network edge tables (`outputs/tables/`)

- `*_edges.csv`: network edge lists (keyword_cooccurrence, co_citation, bibliographic_coupling, coauthorship)

### Network node metrics (`outputs/tables/`)

- `network_metrics_*.csv`: **node-level metrics** — degree, weighted_degree, betweenness, pagerank, closeness, eigenvector, community cluster ID
- `cluster_summary_*.csv`: **per-cluster summary** — n_nodes, mean weighted degree / betweenness / pagerank / closeness / eigenvector, total_weighted_degree, top nodes, pct_nodes
- `network_qc_summary.csv`: **graph-level indicators** — n_nodes, n_edges, density, n_components, largest_component_ratio, **n_communities**, **modularity**, **avg_clustering_coefficient**, **avg_degree**, **avg_weighted_degree**, **diameter_largest_component**, **avg_path_length_largest_component**
- `descriptive_indicators.csv`: descriptive bibliometric indicators (n_works, year range, total citations, h-index, n_authors)

### Network maps (`outputs/figures/`)

Each of the 4 networks produces **two output files**:

| File | Type | Description |
|------|------|-------------|
| `*_network.png` | Static image (PNG) | Cluster-colored network map with legend; top-n labeled nodes |
| `*_network.html` | **Interactive (Plotly)** | Hover to see node metrics; drag to reposition; zoom with scroll; color-coded by cluster |

### Reports (`reports/`)

- **`bibliometrics_report.html`**: Comprehensive HTML report with:
  - Bootstrap-styled responsive layout with sticky table-of-contents navigation
  - Data overview & descriptive indicators section
  - Per-network sections containing:
    - Network overview table (nodes, edges, density, communities, modularity, clustering coefficient, diameter, avg path length)
    - Static cluster-colored PNG map (clickable to enlarge)
    - **Embedded interactive Plotly network map** (hover for details, drag, zoom)
    - Top-20 node metrics table (degree, weighted degree, betweenness, PageRank, closeness, cluster)
    - Cluster/community summary table (size, mean metrics, representative nodes)
  - Print-friendly CSS (iframes hidden when printing)
- `method_note.md`: method documentation with data source and parameter summary

## Visualization features

### Cluster coloring (static PNG)

Nodes are colored by community detected via greedy modularity maximization (Newman-Girvan). A legend shows each cluster with its size. Node size is proportional to weighted degree.

### Interactive HTML maps (Plotly)

- **Hover on any node** → shows name, degree, weighted degree, betweenness, PageRank, and cluster ID
- **Hover on any edge** → shows source, target, and weight
- **Drag nodes** to reposition the layout
- **Scroll to zoom** in/out
- **Legend** shows clusters with node counts
- Color scheme matches the static PNG for consistency

## WoS sample data results

Running with `data/sample-wos/` (4165 works, 2000–2009):

| Indicator | Value |
|-----------|-------|
| Seed works | 4,165 |
| Year range | 2000–2009 |
| Total citations | 307,626 |
| Mean citations | 73.86 |
| H-index (seed works) | 225 |
| Unique authors | 15,693 |
| Reference pairs | 233,246 |
| Unique references | 142,767 |

### Network-level results (top_edges=200)

| Network | Nodes | Edges | Communities | Modularity | Avg Clustering |
|---------|-------|------|-------------|------------|----------------|
| Keyword Co-occurrence | 113 | 200 | 12 | 0.5632 | 0.3139 |
| Co-citation | 118 | 200 | 16 | 0.7937 | 0.5403 |
| Bibliographic Coupling | 247 | 200 | 89 | 0.9706 | 0.2572 |
| Co-authorship | 123 | 200 | 26 | 0.8254 | 0.5451 |

## Core formulas

- **Co-citation matrix**: C = A.T @ A (A = paper-reference incidence)
- **Bibliographic coupling matrix**: B = A @ A.T
- **Keyword co-occurrence**: W = K.T @ K (K = paper-keyword incidence)
- **Betweenness centrality**: uses distance = 1/weight for similarity-weighted networks
- **Community detection**: greedy modularity maximization (NetworkX)
