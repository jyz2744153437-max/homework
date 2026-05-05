# 基于 Transformer 的半导体制造关键技术研究热点与发展趋势 —— 文献计量分析（2015-2025）

> **TL;DR**：2015-2025 年，Transformer 架构在半导体制造领域的研究经历了"传统硬件主导→AI 方法渗透→Transformer 大爆发"三阶段技术演进。中国以 260 篇（40.4%）断层式领先，但奠基性工作仍由非中国机构完成。2024 年是关键历史拐点——vision transformers、ViT、SEM 等 6 个术语同步突现。前沿正从"已知缺陷分类"向"未知异常检测"升级。

## 1. 项目简介

本项目基于 Web of Science 核心合集，运用 CiteSpace 文献计量工具，系统分析 Transformer 架构在半导体制造领域的研究热点、知识基础与前沿趋势。

**核心问题**：
- Transformer 在半导体制造中的应用场景与技术迁移路径是什么？
- 研究热点如何从"传统硬件"向"AI 方法"演化？
- 知识基础呈现怎样的引文结构？前沿正在往哪走？

### 研究背景

Transformer 自 2017 年 Vaswani 等人提出后，历经 ViT（2021）、Swin Transformer（2021）等里程碑，已从 NLP 扩展到计算机视觉、时序预测。在半导体制造领域，晶圆缺陷检测、工艺参数预测、设备故障诊断等任务对 AI 技术有强需求。2022 年以来，该交叉领域发文量以年均 83%–182% 的速度爆发式增长，但尚缺乏系统性的文献计量综述。本项目通过 CiteSpace + Kleinberg 突现检测 + LLR 聚类，量化刻画该领域的研究热点、知识基础与前沿趋势。

## 2. 数据来源

| 项目 | 说明 |
|---|---|
| 数据库 | Web of Science Core Collection (SCI-EXPANDED, SSCI, CPC-S) |
| 时间跨度 | 2015-2025 |
| 文献类型 | Article / Review / Proceedings Paper |
| 语言 | English |
| **最终文献量** | **643 篇（DL 纯净集 147 篇）** |

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

### 数据清洗

"Transformer" 在 WoS 中同时匹配深度学习架构和电子变压器，检索结果混入大量电力电子、射频电路论文。进行了两轮清洗：

| 阶段 | 方法 | 输入 | 输出 | 说明 |
|---|---|---|---|---|
| 去重 | UT + DOI 双重校验 | 643 | 643 | 零重复 |
| DL 语义筛选 | 标题/摘要关键词匹配 | 643 | **147** | 保留 DL Transformer 文献，排除电力电子变压器论文 |

**DL 语义筛选逻辑**：识别 "attention mechanism"、"vision transformer"、"deep learning" 等 DL 特征词作为纳入信号；排除 "power amplifier"、"MMIC"、"DC-DC"、"Doherty" 等电力电子术语。最终保留 147 篇真正使用深度学习 Transformer 架构的半导体相关论文。

筛选细则见 [reports/screening_rule.md](reports/screening_rule.md)。

## 3. 研究方法

| 方法 | 工具 | 用途 |
|---|---|---|
| 关键词共现分析 | CiteSpace 6.4.1 | 识别研究热点与聚类 |
| 共被引网络分析 | CiteSpace | 揭示知识基础 |
| 文献耦合分析 | CiteSpace | 发现研究前沿 |
| 合作网络分析 | CiteSpace | 识别核心团队 |
| 突现检测 | CiteSpace (Kleinberg) | 检测新兴趋势 |
| 时间线分析 | CiteSpace (Timeline View) | 展示聚类演变 |

- CiteSpace 参数：g-index k=25，Pathfinder 剪枝，LLR 聚类算法
- 全量集（643 篇）作为 CiteSpace 输入，DL 纯净集（147 篇）作为核心解读对象
- 方法学详见 [reports/methodology.md](reports/methodology.md)

## 4. 项目结构

```
Transformer-Semiconductor-Bibliometrics/
├── 项目展示.html                   # 交互式单页幻灯片（成果展示主页）
├── CiteSpace分析套件/              # CiteSpace 复现包（数据+参数+操作步骤）
├── Data/                         # 原始数据
│   ├── download_1-500.txt        # WoS 导出（第1批）
│   ├── download_501-643.txt      # WoS 导出（第2批）
│   ├── download_1-147.txt        # DL 纯净集导出
│   ├── screened_*.csv            # 筛选结果
│   ├── field_dictionary.md       # 52字段完整字典
│   └── README.md                 # 数据说明文档
├── config/                       # 配置文件
│   └── query.yaml                # 检索式配置（含 v0/v1/v2 三版本）
├── baseline/                     # 基线文档
│   ├── params.md                 # CiteSpace 参数固化
│   └── tool_selection.md         # 四层工具选型对照
├── docs/                         # 项目文档
│   ├── project_outline.md        # 项目大纲
│   ├── query_rationale.md        # 检索设计思路
│   ├── query_changelog.md        # 检索式变更日志
│   ├── data_model.md             # 图数据模型
│   ├── cleaning_rules.md         # 数据清洗规则
│   └── 团队分工.md                 # 团队分工说明
├── reports/                      # 分析报告
│   ├── data_quality.md           # 数据质量报告（A级评级）
│   ├── methodology.md            # 研究方法论
│   ├── screening_rule.md         # 筛选规则文档
│   ├── screening_record.md       # 筛选记录
│   ├── prisma_flowchart.md       # PRISMA 流程图
│   ├── novelty_search_v0.md      # 查新报告
│   └── metrics_spec.md           # 指标规范
├── outputs/                      # 分析产出
│   ├── cluster_summary_*.csv     # 聚类摘要
│   ├── network_metrics_*.csv     # 网络指标
│   ├── keyword_bursts.csv        # 突现检测结果
│   ├── keyword_burst_report.md   # 突现分析报告
│   ├── *_network.html            # 交互式 Plotly 网络图（4 种网络 × 可拖拽缩放悬停）
│   ├── bibliometrics_report.html # 综合文献计量报告（模板标准产出）
│   └── network_qc_summary.csv    # 网络质量汇总
├── Visual output/                # 可视化产出
│   ├── *.png                     # 6 张 CiteSpace 图谱
│   └── 三阶段技术演进.html             # 三阶段技术演进解读独立页
├── src/                          # 分析脚本
│   ├── burst_detection.py        # 突现检测（Kleinberg 算法）
│   ├── burst_visualize.py        # 突现可视化
│   ├── create_screening.py       # 筛选记录生成
│   └── metrics_calculator.*      # 指标计算
├── paper/                        # 论文草稿
│   └── manuscript_v1.md          # Mini Review 初稿
├── 工作底稿/                     # 过程文档存档
│   ├── 1_意见反馈/               # 迭代修改意见
│   ├── 2_AI插图生成/             # 插图生成提示词与产物
│   └── 3_CiteSpace识图/          # 图谱识图任务
├── run_pipeline.py               # 分析管道入口
└── run_pipeline.js               # Node.js 分析入口
```

## 5. 核心发现

### 5.1 发文趋势：从涓涓细流到指数爆发

2017-2021 年间年均发文不足 3 篇。2021 年 ViT 与 Swin Transformer 发表后，经过约 1 年学术传导延迟，2022 年起发文量以年均 83%–182% 的速度爆发增长。至 2024-2025 年，DL 纯净集中 78% 的论文集中涌现（115/147 篇），领域正式进入"白热化上升期"。

### 5.2 知识基础：ViT/Swin 双核心的三层引文结构

共被引网络（N=383, E=1,262, Q=0.8411, S=0.9522）呈现三层倒金字塔：

- **L1 架构奠基层**：Vaswani (2017) → Dosovitskiy (2021) ViT → Liu Z (2021) Swin Transformer
- **L2 方法改进层**：DETR、DeiT、PVT 等通用视觉技术传递
- **L3 应用落地层**：Wei YX (2022) 晶圆缺陷识别、Fan SKS (2024) 晶圆图分类

知识基础非内生，而是"从通用 AI 外部输出 → 半导体场景内部吸收"的知识溢出路径，完整传导链耗时约 5 年。

### 5.3 技术迁移路径：NLP Attention → CV Backbone → Wafer Defect

突现检测与聚类时间线共同绘制了三阶段轨迹：

| 阶段 | 时间 | 特征 |
|---|---|---|
| 萌芽期 | 2017-2019 | 传统硬件主导：RFID、电感耦合、反激变换器 |
| 加速期 | 2020-2022 | AI 方法渗透：mathematical model (1.20)、classification (1.90)、CNN (1.19) |
| 爆发期 | 2023-2025 | Transformer 接管：2024 年 6 词同步突现，anomaly detection 接棒至 2025 |

### 5.4 突现检测：三阶段技术演进与 2024 历史拐点

Kleinberg 算法识别 25 个突现词，2024 年是关键拐点——vision transformers、ViT、super resolution、SEM、load modeling、data augmentation 六个术语同步突现。2025 年前沿向 anomaly detection 收敛。

### 5.5 国家竞争格局：中国断层式领先

中国 260 篇（40.4%），是第二名美国（80 篇，12.4%）的 3.25 倍。东南大学、中科院、电子科大、浙大、西交大构成 Top 5 核心机构。但奠基性工作（ViT/Swin）仍由非中国机构完成，挑战已从"能不能发更多"转向"能不能定义方向"。

### 5.6 聚类格局：AI 崛起与传统退场

10 个 LLR 聚类中，AI 方向 4 个（#1 machine learning、#2 annotation、#3 defect detection、#8 cnn）全部活跃至 2025；传统硬件聚类 #4 inductors、#9 parallel processing 于 2022 年后系统性"学术死亡"。此消彼长的结构比单纯关键词频次增长更具说服力。

### 5.7 核心指标

| 指标 | 全量集 (643) | DL 纯净集 (147) |
|---|---|---|
| 时间范围 | 2015-2025 | 2015-2025 |
| 总被引次数 | 5,974 | 884 |
| h-index | 37 | 16 |
| 作者数 | 2,517 | — |
| 共被引网络 Q 值 | 0.8411 | — |
| 共被引网络 S 值 | 0.9522 | — |
| 聚类 Q 值 | 0.673 | — |
| 聚类 S 值 | 0.902 | — |

> 注：Q/S 值为 CiteSpace 全量集分析结果。DL 纯净集文献量（147 篇）不足以构建稳定的共被引网络，故未单独计算网络指标。作者数因 CSV 作者字段格式不统一暂未统计。

## 6. 可视化产出

### 关键词共现网络
![关键词共现网络](Visual%20output/outputs_keyword_cooccurrence_network.png)

### 关键词聚类图 (LLR)
![关键词聚类图](Visual%20output/outputs_keyword_cluster.png)

### 共被引网络
![共被引网络](Visual%20output/outputs_co_citation_network.png)

### 共被引聚类图
![共被引聚类图](Visual%20output/outputs_co_citation_cluster.png)

### 突现检测时间线
![突现检测时间线](Visual%20output/outputs_burst_timeline.png)

### 聚类时间线演化图
![聚类时间线演化图](Visual%20output/outputs_timeline_view.png)

| 其他产出 | 文件 | 状态 |
|---|---|---|
| 三阶段技术演进解读 | Visual output/三阶段技术演进.html | 已生成 |
| 项目展示页面 | 项目展示.html | 在线 |

## 7. 快速复现

```bash
# 1. 数据准备
# 将 WoS 导出的 download_*.txt 放入 Data/ 目录

# 2. CiteSpace 分析
# 参数设置见 baseline/params.md

# 3. Python 辅助分析（可选）
pip install -r requirements.txt
python run_pipeline.py
```

## 8. 团队分工

详见 [docs/团队分工.md](docs/团队分工.md)

| 成员 | 角色 |
|---|---|
| 高宇翔 | 数据与图谱主负责人 |
| 纪彦泽 | 项目推进与成果负责人 |
| 韩建财 | 数据质控与图谱协理 |
| 王贺东 | 文献分析与成果协理 |

## 9. 致谢

本项目在以下 AI 工具的辅助下完成：

| 工具/模型 | 用途 |
|---|---|
| Claude Code (接入 DeepSeek API) | 项目总成与推进：数据分析、Git 管理、文档撰写 |
| Gemini 3 Pro | HTML 开发（主体） |
| DeepSeek-v4-pro | 代码生成与优化 |
| GLM-5.1 | 辅助分析 |
| GPT-5.4 | 辅助分析 |
| NanoBanana 2 | AI 图片生成 |
| GPT Image 2 | AI 图片生成 |

## 10. 参考文献

### 方法论文献
1. Kleinberg J. Bursty and hierarchical structure in streams[J]. Data Mining and Knowledge Discovery, 2003, 7(4): 373-397.
2. Chen C. CiteSpace II: Detecting and visualizing emerging trends and transient patterns in scientific literature[J]. Journal of the American Society for Information Science and Technology, 2006, 57(3): 359-377.

### 分析发现的核心文献
3. Wei YX, Wang H. Mixed-type wafer defect recognition with multi-scale information fusion transformer[J]. IEEE Transactions on Semiconductor Manufacturing, 2022, 35: 341-352.
4. Fan SKS, Chiu SH. A new ViT-based augmentation framework for wafer map defect classification to enhance the resilience of semiconductor supply chains[J]. International Journal of Production Economics, 2024, 273: 109275.
5. Chen KQ, Cai N, Wu ZS, et al. Multi-scale GAN with transformer for surface defect inspection of IC metal packages[J]. Expert Systems with Applications, 2023, 212: 118788.
6. Liu YL, Wu H. Automatic solder defect detection in electronic components using transformer architecture[J]. IEEE Transactions on Components, Packaging and Manufacturing Technology, 2024, 14: 166.
7. Wen L, Zhu Y, Ye L, et al. LayouTransformer: Generating layout patterns with transformer via sequential pattern modeling[C]. IEEE/ACM International Conference on Computer Aided Design (ICCAD), 2022.

---

**项目展示网页**：https://jyz2744153437-max.github.io/Transformer-Semiconductor-Bibliometrics/

**项目进度**：M3 终稿与 Release 进行中，详见 [PROGRESS.md](PROGRESS.md)
