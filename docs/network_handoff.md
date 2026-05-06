# 交互式网络图重做 —— Codex 交接文档

> 最后更新：2026-05-06

## 数据来源

DL 纯净集 147 篇（已排除电力电子变压器噪声），WoS 导出文件在 `Data/download_1-147.txt`。

## 输入文件（都在 `outputs/`）

每种网络有一对 CSV：

| 网络 | 边表 | 指标表 |
|------|------|--------|
| 关键词共现 | `keyword_cooccurrence_edges.csv` | `network_metrics_keyword_cooccurrence.csv` |
| 共被引 | `co_citation_edges.csv` | `network_metrics_co_citation.csv` |
| 文献耦合 | `bibliographic_coupling_edges.csv` | `network_metrics_bibliographic_coupling.csv` |
| 合作网络 | `coauthorship_edges.csv` | `network_metrics_coauthorship.csv` |

**边表格式**：`source,target,weight`（三列）  
**指标表格式**：`node,degree,weighted_degree,betweenness,pagerank,closeness,eigenvector,community`

## 技术方案

按老师课件（L9 工具生态）和 bibliometrics-mini 模板标准：**Python + NetworkX + Plotly → 独立 HTML 文件**。

输入 CSV → NetworkX 构建无向加权图 → Plotly go.Scatter 渲染 → `write_html()` 输出。项目展示页通过链接打开。

## 当前方案（Python Plotly 版，供参考）

`src/visualize_interactive.py` — 现有实现，可从 CSV 生成独立 HTML 文件。

参数参考：top_labels=30, min_size=10, max_size=55, k=3.5, edges_limit=150

## 四种网络

| 网络 | 节点数 | 节点含义 | 边含义 |
|------|--------|----------|--------|
| keyword_cooccurrence | 84 | 关键词 | 同时出现在同一论文 |
| co_citation | 89 | 被引文献（作者_年份_期刊） | 被同一篇论文引用 |
| bibliographic_coupling | 91 | 施引文献（WOS ID） | 引用了相同参考文献 |
| coauthorship | 106 | 作者名 | 共同发表论文 |

## 期望功能

- 节点按社团着色（community 字段）
- 节点大小按加权度（weighted_degree）
- 前 30 个核心节点显示名称标签
- 悬停显示指标（度、加权度、中介中心性、PageRank）
- 拖拽、缩放、图例点击筛选
- 只显示最强 150 条边

## 四种网络的解读方向

- **关键词共现** → 识别研究热点，同色=同主题聚类
- **共被引** → 揭示知识基础，球大=奠基文献
- **文献耦合** → 发现研究前沿
- **合作网络** → 识别核心团队/机构
