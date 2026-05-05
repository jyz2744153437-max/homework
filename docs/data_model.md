# 图数据模型 (Data Model)

> 版本：v1.0
> 创建日期：2026-05-01
> 适用范围：共被引网络、关键词共现网络、合作网络

---

## 一、网络类型概览

| 网络类型 | 节点 | 边 | 分析目的 |
|---|---|---|---|
| 共被引网络 | 被引文献 | 共被引关系 | 揭示知识基础 |
| 关键词共现网络 | 关键词 | 共现关系 | 揭示研究主题结构 |
| 作者合作网络 | 作者 | 合作关系 | 揭示核心研究团队 |
| 机构合作网络 | 机构 | 合作关系 | 揭示核心研究机构 |

---

## 二、共被引网络 (Co-citation Network)

### 2.1 节点定义

| 属性 | 字段 | 说明 |
|---|---|---|
| 唯一标识 | CR_ID | 格式：FirstAuthor, Year, Journal, Volume, Page |
| 显示名称 | Label | 第一作者 + 年份 |
| 被引频次 | CitationCount | 被引用次数 |
| 中介中心性 | Betweenness | CiteSpace 计算 |
| 聚类归属 | Cluster | LLR 聚类结果 |

### 2.2 边定义

| 属性 | 字段 | 说明 |
|---|---|---|
| 源节点 | Source | 被引文献 A |
| 目标节点 | Target | 被引文献 B |
| 权重 | Weight | 共被引频次 |
| 相似度 | Similarity | Cosine 相似度 |

### 2.3 网络构建规则

```
共被引矩阵 C = R^T × R

其中：
- R 为"施引文献 × 被引文献"二元矩阵
- R[i,j] = 1 表示施引文献 i 引用了被引文献 j
- C[a,b] 表示被引文献 a 和 b 被共同引用的次数
```

### 2.4 阈值策略

| 参数 | 设定值 | 说明 |
|---|---|---|
| 阈值类型 | g-index (k=25) | 自适应阈值 |
| 时间切片 | 1 年 | 2015-2025 共 11 个切片 |
| 裁剪算法 | Pathfinder + Pruning sliced networks | 提取骨架结构 |

---

## 三、关键词共现网络 (Keyword Co-occurrence Network)

### 3.1 节点定义

| 属性 | 字段 | 说明 |
|---|---|---|
| 唯一标识 | Keyword | 关键词文本（规范化后） |
| 显示名称 | Label | 关键词原文 |
| 频次 | Frequency | 出现次数 |
| 聚类归属 | Cluster | LLR 聚类结果 |

### 3.2 边定义

| 属性 | 字段 | 说明 |
|---|---|---|
| 源节点 | Source | 关键词 A |
| 目标节点 | Target | 关键词 B |
| 权重 | Weight | 共现频次 |

### 3.3 关键词规范化规则

| 原始词 | 标准化词 | 规则 |
|---|---|---|
| ViT | Vision Transformer | 缩写展开 |
| Wafer Defect | Defect Detection | 同义合并 |
| Attention Mechanism | Transformer | 技术归类 |
| 大小写不同 | 统一小写 | 大小写归一 |

---

## 四、作者合作网络 (Author Collaboration Network)

### 4.1 节点定义

| 属性 | 字段 | 说明 |
|---|---|---|
| 唯一标识 | Author_ID | AU 字段（缩写格式）或 AF 字段（全名） |
| 显示名称 | Label | 作者全名（AF） |
| 发文量 | PublicationCount | 发文数量 |
| 总被引 | TotalCitations | 总被引次数 |
| 机构 | Affiliation | 所属机构 |

### 4.2 边定义

| 属性 | 字段 | 说明 |
|---|---|---|
| 源节点 | Source | 作者 A |
| 目标节点 | Target | 作者 B |
| 权重 | Weight | 合作发文次数 |

### 4.3 作者消歧规则

| 问题 | 处理方式 |
|---|---|
| 同名异人 | 结合机构（C1）和 ORCID（OI）区分 |
| 同人异名 | 使用 AF（全名）字段统一 |

---

## 五、机构合作网络 (Institution Collaboration Network)

### 5.1 节点定义

| 属性 | 字段 | 说明 |
|---|---|---|
| 唯一标识 | Institution_ID | 规范化机构名 |
| 显示名称 | Label | 机构全名 |
| 发文量 | PublicationCount | 发文数量 |
| 国家 | Country | 所在国家 |

### 5.2 边定义

| 属性 | 字段 | 说明 |
|---|---|---|
| 源节点 | Source | 机构 A |
| 目标节点 | Target | 机构 B |
| 权重 | Weight | 合作发文次数 |

### 5.3 机构规范化规则

| 原始名 | 标准化名 | 规则 |
|---|---|---|
| Tsinghua Univ | Tsinghua University | 缩写展开 |
| Chinese Acad Sci | Chinese Academy of Sciences | 缩写展开 |
| Univ of ... | University of ... | 缩写展开 |

---

## 六、数据字段映射

### 6.1 WOS 字段 → 网络节点

| WOS 字段 | 标签 | 网络用途 |
|---|---|---|
| CR | Cited References | 共被引网络节点 |
| DE/ID | Keywords | 关键词共现网络节点 |
| AU/AF | Authors | 作者合作网络节点 |
| C1/C3 | Institutions | 机构合作网络节点 |

### 6.2 WOS 字段 → 节点属性

| WOS 字段 | 标签 | 属性用途 |
|---|---|---|
| TC | Times Cited | 被引频次 |
| PY | Year Published | 时间属性 |
| SO | Source | 来源期刊 |
| C1 | Author Addresses | 机构、国家 |

---

## 七、数据存储格式

### 7.1 节点文件 (nodes.csv)

```csv
id,label,type,frequency,centrality,cluster
CR_001,"Vaswani A, 2017",reference,156,0.23,1
KW_001,"Vision Transformer",keyword,42,0.15,2
AU_001,"Zhang Y",author,4,0.08,3
```

### 7.2 边文件 (edges.csv)

```csv
source,target,weight,type
CR_001,CR_015,28,cocitation
KW_001,KW_008,15,cooccurrence
AU_001,AU_003,2,collaboration
```

---

**文档版本**：v1.0
**创建日期**：2026-05-01
