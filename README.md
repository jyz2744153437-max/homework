# 基于 Transformer 的半导体制造关键技术研究热点与发展趋势 —— 文献计量分析（2015-2025）

## 1. 项目简介

本项目通过文献计量学方法，系统分析 2015-2025 年间 Transformer 架构在半导体制造领域的研究热点、演化路径与前沿趋势。

**核心问题**：
- Transformer 在半导体制造中的应用场景有哪些？
- 研究热点如何随时间演化？
- 核心文献、作者、机构网络结构如何？

## 2. 数据来源

| 项目 | 说明 |
|---|---|
| 数据库 | Web of Science Core Collection |
| 时间跨度 | 2015-2025 |
| 文献类型 | Article / Review / Proceedings Paper |
| 语言 | English |
| **最终文献量** | **643 篇** |

### 检索式

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

详细检索式设计见 [docs/query_rationale.md](docs/query_rationale.md)，迭代历史见 [docs/query_changelog.md](docs/query_changelog.md)。

## 3. 研究方法

| 方法 | 工具 | 用途 |
|---|---|---|
| 关键词共现分析 | Python (bibliometrics-mini) | 识别研究热点 |
| 共被引网络分析 | Python | 揭示知识基础 |
| 文献耦合分析 | Python | 发现研究前沿 |
| 合作网络分析 | Python | 识别核心团队 |
| 突现检测 | Python (Kleinberg 算法) | 检测新兴趋势 |

方法学详见 [reports/methodology.md](reports/methodology.md)。

## 4. 项目结构

```
Transformer-Semiconductor-Bibliometrics/
├── Data/                    # 原始数据
│   ├── download_*.txt       # WoS 导出文件
│   ├── screened_final.csv   # 筛选后文献
│   └── field_dictionary.md  # 字段字典
├── config/                  # 配置文件
│   └── query.yaml           # 检索式配置
├── docs/                    # 文档
│   ├── query_rationale.md   # 检索设计思路
│   ├── query_changelog.md   # 检索式变更日志
│   └── data_model.md        # 图数据模型
├── reports/                 # 分析报告
│   ├── data_quality.md      # 数据质量报告
│   ├── screening_record.md  # 筛选记录 (PRISMA)
│   ├── novelty_search_v0.md # 查新报告
│   └── metrics_spec.md      # 指标规范
├── outputs/                 # 分析产出
│   ├── *_network.png/html   # 网络图谱
│   ├── keyword_bursts.csv   # 突现检测结果
│   └── descriptive_indicators.csv
├── src/                     # 分析脚本
│   ├── burst_detection.py   # 突现检测
│   └── create_screening.py  # 筛选记录生成
└── paper/                   # 论文草稿
    └── manuscript_v1.md
```

## 5. 核心发现

### 5.1 研究热点

基于关键词共现网络，识别出以下核心研究主题：

| 主题 | 代表关键词 |
|---|---|
| 缺陷检测 | defect detection, wafer, classification |
| 时序预测 | time series, forecasting, Informer |
| 图像识别 | Vision Transformer, feature extraction |

### 5.2 突现趋势

| 关键词 | 突现区间 | 强度 | 解读 |
|---|---|---|---|
| transformers | 2023-2025 | 2 | Transformer 架构应用爆发 |
| deep learning | 2024-2025 | 2 | 深度学习方法普及 |
| vision transformer | 2025 | 1 | ViT 在半导体视觉任务中的应用兴起 |

**核心结论**：Transformer 在半导体领域的研究从 2023 年开始进入爆发期。

详见 [outputs/keyword_burst_report.md](outputs/keyword_burst_report.md)。

### 5.3 核心指标

| 指标 | 数值 |
|---|---|
| 文献总数 | 643 篇 |
| 时间范围 | 2015-2025 |
| 总被引次数 | 313,600 |
| h-index | 226 |
| 作者数 | 17,892 |

## 6. 可视化产出

| 图谱 | 文件 |
|---|---|
| 关键词共现网络 | [outputs/keyword_cooccurrence_network.png](outputs/keyword_cooccurrence_network.png) |
| 共被引网络 | [outputs/co_citation_network.png](outputs/co_citation_network.png) |
| 文献耦合网络 | [outputs/bibliographic_coupling_network.png](outputs/bibliographic_coupling_network.png) |
| 合作网络 | [outputs/coauthorship_network.png](outputs/coauthorship_network.png) |
| 突现时间线 | [outputs/keyword_burst_timeline.png](outputs/keyword_burst_timeline.png) |

## 7. 快速复现

```bash
# 安装依赖
pip install -r requirements.txt

# 运行突现检测
python src/burst_detection.py
python src/burst_visualize.py

# 运行完整分析管道
python run_pipeline.js  # Node.js 环境
```

## 8. 参考文献

- PRISMA 声明：系统综述报告规范
- Kleinberg, J. (2003). Bursty and Hierarchical Structure in Streams
- bibliometrics-mini: Python 文献计量分析工具

---

## 👥 团队分工

| 姓名 | GitHub ID | 关键贡献 |
|---|---|---|

---

**项目进度**：M2 计量分析产出已完成，详见 [PROGRESS.md](PROGRESS.md)
