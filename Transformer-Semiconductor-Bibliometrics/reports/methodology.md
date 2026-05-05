# 研究方法论

## 基于 Transformer 的半导体制造关键技术研究热点与发展趋势——文献计量分析（2015-2025）

---

## 1. 研究问题

本研究旨在回答以下核心问题：

1. **研究热点**：2015-2025 年间，Transformer 架构在半导体制造领域的研究热点是什么？不同时期的热点如何演变？
2. **知识结构**：该领域的知识基础是什么？哪些文献构成了知识的核心节点和桥接文献？
3. **前沿趋势**：哪些主题在近年突然兴起？未来的研究方向指向哪里？
4. **合作格局**：核心研究团队和机构有哪些？合作网络的拓扑结构如何？

---

## 2. 数据获取

### 2.1 数据源

| 项目 | 说明 |
|---|---|
| 数据库 | Web of Science Core Collection |
| 引文索引 | SCI-EXPANDED, SSCI, CPCI-S |
| 导出格式 | Plain Text（全记录与引用的参考文献） |
| 导出时间 | 2026年4月 |

### 2.2 检索式

最终检索式（WOS 高级检索）：

```
TS=("Transformer" OR "Vision Transformer" OR "ViT" OR "Swin Transformer"
   OR "Autoformer" OR "Informer" OR "PatchTST")
AND TS=("semiconductor" OR "wafer" OR "integrated circuit" OR "lithography"
   OR "semiconductor packaging" OR "wafer fabrication" OR "chip manufacturing")
NOT TS=("power transformer" OR "voltage" OR "current transformer"
   OR "medical image" OR "NLP" OR "natural language"
   OR "traffic" OR "power load" OR "smart grid"
   OR "distribution network" OR "financial")
```

**检索设计逻辑**：

| 层次 | 内容 | 说明 |
|---|---|---|
| 对象词 | Transformer 及其 6 种变体 | 覆盖主流 Transformer 架构 |
| 场景词 | semiconductor, wafer, IC, lithography 等 | 限定半导体制造领域 |
| 排除词 | power transformer, medical image, NLP, traffic 等 11 类 | 排除电力变压器、医疗影像、NLP 等无关领域 |

检索过程中经历 3 轮迭代优化：
- **v0（105条）**：初始检索，过度依赖具体应用场景词
- **v1（512条）**：放宽场景限定，但噪声较高
- **v2-final（643条）**：平衡查全率与查准率，新增 smart grid、distribution network 等排除词

### 2.3 数据规模

| 指标 | 数值 |
|---|---|
| 原始检索文献 | 643 条 |
| 时间跨度 | 2015-2025 |
| 文献类型 | Article + Review |
| 语言 | English |
| 数据文件 | download_1-500.txt (前500条), download_501-643.txt (后143条) |

### 2.4 导出字段

WOS 导出文献包含以下核心字段：

| 字段标签 | 含义 | 分析用途 |
|---|---|---|
| PT | 文献类型 | 筛选 Article/Review |
| AU / AF | 作者（缩写/全名） | 作者合作网络 |
| TI | 标题 | 主题判断 |
| SO | 来源期刊 | 期刊分布 |
| DE / ID | 关键词（作者/扩展） | 关键词共现与聚类 |
| AB | 摘要 | 相关性判断 |
| C1 / C3 | 作者机构 | 机构合作网络 |
| CR | 参考文献列表 | 共被引分析 |
| TC / Z9 | 被引次数 | 影响力评估 |
| PY | 出版年 | 时间分析 |
| DI | DOI | 去重与文献追踪 |
| RP | 通讯作者 | 通讯作者分析 |
| FU | 基金资助 | 研究支持背景 |

---

## 3. 数据筛选与清洗

### 3.1 筛选流程（PRISMA）

| 阶段 | 操作 | 纳入 | 排除 | 排除标准 |
|---|---|---|---|---|
| Identification | WOS 检索 | 643 | — | — |
| Screening | 去重 | — | 待统计 | 基于 DOI 去重 |
| Screening | 标题+摘要初筛 | 待统计 | 待统计 | 排除明显不相关文献 |
| Eligibility | 全文复筛 | 待统计 | 待统计 | 排除方法不符、数据不全文献 |
| Included | 纳入分析 | **643** | — | — |

### 3.2 数据清洗规则

#### 关键词消歧（同义映射）

| 原始词 | 映射标准词 | 理由 |
|---|---|---|
| ViT | Vision Transformer | 缩写统一 |
| Wafer Defect | Defect Detection | 语义合并 |
| Attention Mechanism | Transformer | 核心技术归类 |

#### 排除说明

通过 NOT 逻辑人工剔除了 100+ 条关于电力变压器（power transformer）的干扰文献。Transformer 在电力领域指物理变压器，与本研究关注的深度学习架构完全不同。

---

## 4. 分析工具与参数配置

### 4.1 技术路线

本组采用 **路线 A（GUI 驱动路线）**，四层工具栈如下：

| 工具 | 层级 | 版本 | 解决问题 | 方案 |
|---|---|---|---|---|
| Web of Science | 数据层 | Core Collection | 文献检索与数据导出 | 主方案 |
| CiteSpace | GUI 层 | 6.4.1 (Standard) | 共被引聚类、突现检测、时间线 | 主方案 |
| VOSviewer | GUI 层 | — | 合作网络可视化（备选） | 备选方案 |
| GPT-4o | Agent 层 | — | 术语扩展、证据表初稿 | 辅助解释 |
| Python (pandas/networkx) | 开源分析层 | 3.10+ | 数据清洗、指标计算 | 辅助 |

**选择理由**：CiteSpace 6.4.1 支持 LLR 聚类算法和突现检测，适合处理 643 条文献规模的知识图谱分析。GUI 路线能快速建立参数直觉，产出 baseline 图谱。

### 4.2 CiteSpace 核心参数

| 参数 | 设定值 | 选择理由 |
|---|---|---|
| 时间切片 | 2015-2025 (Slice = 1) | 以年为单位，11 个时间切片，精细追踪年度变化 |
| 节点类型 | Keyword + Reference | 关键词揭示研究热点，被引文献揭示知识基础 |
| 阈值策略 | g-index (k=25) | 相比 Top-N 策略，g-index 能自适应不同时间切片的文献量 |
| 裁剪算法 | Pathfinder + Pruning sliced networks | 提取骨架结构，消除冗余连接，突出核心路径 |
| 聚类标签算法 | LLR (对数似然比) | 从施引文献中提取最具代表性的术语作为聚类名 |
| 相似度 | Cosine | 适合高维稀疏数据 |

### 4.3 网络定义四要素

| 要素 | 共被引网络 | 关键词共现网络 |
|---|---|---|
| 节点 | 被引文献（Reference） | 关键词（Keyword） |
| 边 | 两篇文献被同一篇施引文献引用 | 两个关键词出现在同一篇文章中 |
| 权重 | 共被引频次 | 共现频次 |
| 阈值 | g-index (k=25) | g-index (k=25) |

---

## 5. 分析方法

### 5.1 发文趋势分析

统计 2015-2025 年各年度发文量及增长率，绘制年度发文趋势图。通过发文量变化识别领域发展阶段（萌芽期、增长期、爆发期、稳定期）。

### 5.2 关键词共现与聚类分析

基于关键词共现网络，使用 Louvain 社区检测算法进行聚类，以 LLR 算法提取聚类标签。通过关键词聚类图谱识别领域的研究主题结构。

**聚类质量评估**：
- **Modularity Q**：衡量网络社区结构的显著性，Q > 0.3 表示结构显著
- **Weighted Mean Silhouette**：衡量聚类内部同质性，S > 0.7 表示聚类高度可信

### 5.3 共被引分析（Co-citation Analysis）

当两篇文献（A 和 B）同时被第三篇文献（C）引用时，A 与 B 构成共被引关系。共被引网络反映了领域的**知识基础**——被引频次越高的节点对该领域越重要。

共被引矩阵构建：
> C = Rᵀ × R

其中 R 为"施引文献 × 被引文献"的二元矩阵，C 为共被引矩阵。

### 5.4 突现检测（Burst Detection）

使用 Kleinberg 突发检测算法，识别在特定时期内引用量突然激增的关键词或被引文献。突现值高表示该主题在该时期受到了超常关注。

### 5.5 时间线分析（Timeline View）

以年份为横轴、聚类编号为纵轴，将聚类内文献按发表时间排列，展示各研究主题的时间演化轨迹，识别主题的兴起、持续和消退。

### 5.6 文献耦合分析（Bibliographic Coupling）

当两篇文献引用同一批参考文献时，它们构成文献耦合关系。与共被引（"向后看"）不同，耦合分析是"向前看"的视角，反映文献发表时的知识背景。

### 5.7 合作网络分析

构建作者合作网络和机构合作网络，计算 Degree 中心性、Betweenness 中心性，识别核心研究团队和桥接机构。

---

## 6. 指标体系

| 类别 | 指标 | 说明 |
|---|---|---|
| 数量指标 | 年度发文量 | 各年文献数量，反映研究活跃度 |
| | 发文增长率 | 年度变化率，识别增长拐点 |
| 影响力指标 | 总被引次数 | WOS 被引次数 |
| | 篇均被引 | 平均每篇被引次数 |
| | h-index | 综合文献数量与影响力的指标 |
| 网络指标 | Modularity Q | 聚类结构显著性 |
| | Weighted Silhouette | 聚类同质性 |
| | Betweenness Centrality | 节点桥接作用 |
| 突现指标 | Burst Strength | 关键词突现强度 |
| | Burst Duration | 突现持续时间 |

---

## 7. 质量控制

### 7.1 检索质量控制
- 检索式落盘到 `config/query.yaml`，版本化管理
- 每次检索式修改记录到变更日志（query_changelog.md）
- 抽样核查 10 条文献，确认检索准确性

### 7.2 数据质量控制
- 基于 DOI 去重
- 统计各字段缺失率
- 导出字段完整性检查（必须包含作者、机构、关键词、摘要、参考文献、DOI）

### 7.3 参数质量控制
- 所有 CiteSpace 参数记录到 `baseline/params.md`
- 至少做一次阈值敏感性对照实验
- 聚类结果需明确 Modularity Q 和 Silhouette 值

### 7.4 可复现保证
- 固定数据版本（下载时间戳）
- 固定软件版本（CiteSpace 6.4.1, Python 3.10+）
- 固定检索式版本
- 所有图表可追溯到原始参数

---

## 8. 分析产出一览

| 分析类型 | 预期产出 | 工具 |
|---|---|---|
| 关键词聚类图谱 | 研究领域主题结构图 | CiteSpace |
| 关键词时间线图 | 主题演化轨迹图 | CiteSpace |
| 共被引网络图 | 知识基础结构图 | CiteSpace |
| 突现检测 | Burst 关键词与被引文献列表 | CiteSpace |
| 发文趋势图 | 年度发文量折线图 | Python/matplotlib |
| 合作网络图 | 作者/机构合作图谱 | VOSviewer 或 Python/networkx |
| 指标统计表 | 各项计量指标汇总 | Python/pandas |

---

**文档版本**：v1.0
**创建日期**：2026-04-30
**适用范围**：M1 方法论 + M2 分析框架
