# 图数据模型

## 节点类型

- Work: seed paper in the OpenAlex query result.
- Reference: cited work ID appearing in `referenced_works`.
- Keyword: keyword or topic extracted from OpenAlex records.
- Author: author display name.

## 边类型

- Co-citation: two references are cited by the same seed works. Matrix C = A.T @ A.
- Bibliographic coupling: two seed works share references. Matrix B = A @ A.T.
- Keyword co-occurrence: two keywords appear in the same seed work. Matrix W = K.T @ K.
- Coauthorship: two authors co-author the same seed work. Matrix N = M.T @ M.

## 质量检查

- Record node, edge, weight, and threshold definitions in config/query.yaml.
- Report graph density, connected components, and largest component ratio.
- For weighted betweenness, convert similarity weight to distance = 1 / weight.
