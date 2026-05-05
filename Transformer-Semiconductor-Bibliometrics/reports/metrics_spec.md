# 指标规范文档 (Metrics Specification)

> 版本：v2.0
> 更新日期：2026-05-01
> 适用范围：M1 指标定义 + M2 计算口径

---

## 一、数量指标

### 1.1 年度发文量 (Annual Publication Count)

| 项目 | 说明 |
|---|---|
| 定义 | 某一年度发表的文献数量 |
| 公式 | N_year = Count(PY = year) |
| 口径 | 按 WOS 的 PY（出版年）字段统计 |
| 局限 | Early Access 论文 PY 可能与在线发表年不一致 |
| 本项目数值 | 2015: 30, 2016: 30, 2017: 31, 2018: 31, 2019: 33, 2020: 41, 2021: 58, 2022: 53, 2023: 57, 2024: 101, 2025: 167 |

### 1.2 发文增长率 (Growth Rate)

| 项目 | 说明 |
|---|---|
| 定义 | 相邻年度发文量的变化率 |
| 公式 | GR = (N_year - N_prev) / N_prev × 100% |
| 口径 | 基于年度发文量计算 |
| 局限 | 基数小时增长率波动大（如 2019→2020） |
| 关键拐点 | 2020 (+24.2%), 2024 (+77.2%) |

### 1.3 累计发文量 (Cumulative Publication Count)

| 项目 | 说明 |
|---|---|
| 定义 | 截至某年的发文总量 |
| 公式 | C_year = Σ N_y (y ≤ year) |
| 口径 | 同年度发文量 |

---

## 二、影响力指标

### 2.1 总被引次数 (Total Citations, TC)

| 项目 | 说明 |
|---|---|
| 定义 | 文献在 WOS Core Collection 中被引用的总次数 |
| 公式 | TC = Σ citations |
| 口径 | 使用 WOS 的 TC 字段（WOS Core Collection 被引） |
| 局限 | 不同数据库被引数不同（TC vs Z9） |
| 本项目数值 | 总计 5,974 次 |

### 2.2 篇均被引 (Average Citations per Paper)

| 项目 | 说明 |
|---|---|
| 定义 | 平均每篇文献的被引次数 |
| 公式 | ACP = TC_total / N |
| 口径 | 基于全部 643 条记录 |
| 局限 | 受新发表文献拉低（零被引占 24.3%） |
| 本项目数值 | 9.29 次/篇 |

### 2.3 被引中位数 (Median Citations)

| 项目 | 说明 |
|---|---|
| 定义 | 所有文献被引次数的中位数 |
| 公式 | Median(TC_sorted) |
| 口径 | 同 TC |
| 局限 | 比均值更能反映"典型"文献的影响力 |
| 本项目数值 | 3 次 |

### 2.4 h-index

| 项目 | 说明 |
|---|---|
| 定义 | 有 h 篇论文各被引用至少 h 次 |
| 公式 | max{h: TC_i ≥ h for i = 1, ..., h}，TC 降序排列 |
| 口径 | 基于全部 643 条记录的 TC 字段 |
| 局限 | 对高被引文献不敏感，无法区分极高被引 |
| 本项目数值 | 37 |

### 2.5 零被引率 (Zero-Citation Ratio)

| 项目 | 说明 |
|---|---|
| 定义 | 未被引用的文献占比 |
| 公式 | ZCR = Count(TC = 0) / N × 100% |
| 口径 | 基于 TC 字段 |
| 局限 | 新发表文献尚未积累引用，属正常现象 |
| 本项目数值 | 24.3% (156/643) |

---

## 三、网络指标

### 3.1 Modularity Q (模块度)

| 项目 | 说明 |
|---|---|
| 定义 | 衡量网络社区结构的显著性 |
| 公式 | Q = Σ[e_ii - (Σ_j e_ij)²]，其中 e_ij 为社区间边占比 |
| 口径 | CiteSpace 自动计算 |
| 质量阈值 | Q > 0.3 表示结构显著 |
| 本项目数值 | 待 CiteSpace 分析后填入 |

### 3.2 Weighted Mean Silhouette (加权平均轮廓系数)

| 项目 | 说明 |
|---|---|
| 定义 | 衡量聚类内部同质性 |
| 公式 | S = mean(s_i)，s_i = (b_i - a_i) / max(a_i, b_i) |
| 口径 | CiteSpace 自动计算 |
| 质量阈值 | S > 0.7 表示聚类高度可信 |
| 本项目数值 | 待 CiteSpace 分析后填入 |

### 3.3 Betweenness Centrality (中介中心性)

| 项目 | 说明 |
|---|---|
| 定义 | 节点在网络最短路径中出现的频率，衡量桥接作用 |
| 公式 | BC(v) = Σ[σ_st(v) / σ_st]，σ_st 为 s→t 最短路径数 |
| 口径 | CiteSpace 自动计算 |
| 质量阈值 | BC > 0.1 通常认为具有关键桥接作用 |
| 本项目数值 | 待 CiteSpace 分析后填入 |

### 3.4 Degree Centrality (度中心性)

| 项目 | 说明 |
|---|---|
| 定义 | 节点的连接数（度），衡量节点的直接影响力 |
| 公式 | DC(v) = degree(v) / (N - 1) |
| 口径 | CiteSpace 自动计算 |

---

## 四、突现指标

### 4.1 Burst Strength (突现强度)

| 项目 | 说明 |
|---|---|
| 定义 | 关键词或被引文献在特定时期被引用量突然激增的强度 |
| 算法 | Kleinberg 突发检测算法 |
| 口径 | CiteSpace 自动计算 |
| 局限 | 对时间窗口敏感 |

### 4.2 Burst Duration (突现持续时间)

| 项目 | 说明 |
|---|---|
| 定义 | 突现状态持续的年份范围 |
| 口径 | CiteSpace 自动计算 |

---

## 五、分布指标

### 5.1 期刊集中度 (Journal Concentration)

| 项目 | 说明 |
|---|---|
| 定义 | 发文量集中在少数期刊的程度 |
| 公式 | Top N 期刊发文量 / 总发文量 |
| 本项目数值 | Top 10 期刊发文 147 篇，占 22.9% |

### 5.2 国家/地区分布

| 项目 | 说明 |
|---|---|
| 定义 | 各国家/地区的发文量 |
| 口径 | 基于 C1 字段提取国家 |
| 本项目 Top 3 | China (260), USA (80), South Korea (57) |

### 5.3 核心作者发文量

| 项目 | 说明 |
|---|---|
| 定义 | 各作者的发文数量 |
| 口径 | 基于 AU 字段统计 |
| 局限 | 同名异人问题（AU 为缩写格式） |
| 本项目 Top 5 | Li Y (4), Chen CN (4), Yu YM (4), Zhang H (4), Zhang Y (3) |

---

## 六、指标计算工具映射

| 指标 | 计算工具 | 输出位置 |
|---|---|---|
| 年度发文量、增长率 | Node.js 脚本 | outputs/metrics_report.md |
| 被引统计、h-index | Node.js 脚本 | outputs/metrics_report.md |
| 期刊/作者/机构/国家分布 | Node.js 脚本 | outputs/metrics_report.md |
| 关键词频次 | Node.js 脚本 | outputs/metrics_report.md |
| Modularity Q | CiteSpace | 待分析 |
| Silhouette S | CiteSpace | 待分析 |
| Betweenness Centrality | CiteSpace | 待分析 |
| Burst Strength/Duration | CiteSpace | 待分析 |

---

**文档版本**：v2.0
**更新日期**：2026-05-01
**计算脚本**：src/metrics_calculator.js
