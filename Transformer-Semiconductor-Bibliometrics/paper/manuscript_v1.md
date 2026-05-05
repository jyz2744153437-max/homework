# Mini Review 初稿

## 基于 Transformer 的半导体制造关键技术研究热点与发展趋势——文献计量分析（2015-2025）

---

## 摘要

本研究基于 Web of Science 核心合集（SCI-EXPANDED、SSCI、CPCI-S），经三轮检索式迭代与 PRISMA 2020 标准筛选流程，纳入 643 篇全量文献，并进一步通过 DL 语义筛选获得 147 篇深度学习 Transformer 纯净文献。运用 CiteSpace 6.4.1 进行关键词共现分析、共被引分析、LLR 聚类及 Kleinberg 突现检测，系统揭示了该交叉领域的研究热点、知识基础与前沿趋势。研究发现：（1）发文量从 2022 年起以年均 83%–182% 的速度爆发增长，DL 纯净集中 78% 的论文发表于 2024–2025 年；（2）共被引网络（Q=0.8411, S=0.9522）呈现 ViT/Swin 双核心的三层引文结构——架构奠基→方法改进→应用落地，知识传导链完整耗时约 5 年；（3）Kleinberg 算法识别 25 个突现词，呈现三波清晰的技术浪潮（2017–2019 传统硬件→2020–2022 AI 渗透→2023–2025 Transformer 爆发），2024 年为关键拐点（6 词同步突现）；（4）中国以 260 篇（40.4%）的发文量断层式领先，是第二名美国的 3.25 倍，但基础架构创新仍由海外主导。本研究填补了 Transformer × 半导体制造交叉领域系统综述的空白。

**关键词**：Transformer；半导体制造；文献计量分析；CiteSpace；突现检测；知识图谱

---

## 1 引言

### 1.1 研究背景

Transformer 架构自 2017 年 Vaswani 等人在 "Attention Is All You Need" 中提出以来，凭借自注意力机制在序列建模中取得突破性进展。2021 年，Vision Transformer (ViT, Dosovitskiy et al.) 与 Swin Transformer (Liu Z et al.) 两篇奠基论文将其推向计算机视觉领域，成为学科分水岭。经过约 1 年的学术传导延迟，Transformer 架构开始规模性导入半导体制造场景。

半导体制造涉及光刻、刻蚀、沉积、封装等数百道精密工序，晶圆缺陷检测、工艺参数预测、设备故障诊断等任务对 AI 技术有刚性需求。2022 年以来，该交叉领域发文量爆发式增长，但尚缺乏系统性的文献计量综述。本研究通过 CiteSpace 量化分析，刻画该领域的研究热点、知识基础与前沿趋势。

### 1.2 研究问题

1. 2015–2025 年间，Transformer 架构在半导体制造领域的研究热点如何演化？
2. 该领域的知识基础呈现怎样的引文结构？核心节点是哪些文献？
3. 哪些主题近年突然兴起？前沿趋势指向哪里？
4. 国家与机构的竞争格局如何？

### 1.3 研究意义

- **学术意义**：填补 Transformer × 半导体制造交叉领域系统综述的空白，提供第一份文献计量全景扫描
- **实践意义**：为半导体制造企业的 AI 技术选型与科研布局提供数据参照

---

## 2 数据与方法

### 2.1 数据来源

| 项目 | 说明 |
|---|---|
| 数据库 | Web of Science Core Collection |
| 引文索引 | SCI-EXPANDED, SSCI, CPCI-S |
| 检索日期 | 2026-04-14 |
| 文献类型 | Article / Review / Proceedings Paper |
| 语言 | English |
| 全量文献量 | 643 篇 |
| DL 纯净文献量 | 147 篇 |
| 时间范围 | 2015–2025 |

### 2.2 检索策略

采用三层检索式设计，经三轮迭代优化至 v2-final：

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

| 迭代版本 | 文献量 | 主要变更 |
|---|---|---|
| v0 | 105 | 初步检索，基础关键词 |
| v1 | 512 | 扩展 Transformer 变体，补充场景词 |
| v2-final | 643 | 新增 5 类排除词，覆盖电力电子/金融/交通等 |

### 2.3 DL 语义二次筛选

"Transformer" 在 WoS 中同时匹配深度学习架构与电子变压器，检索结果混入大量电力电子、射频电路论文。为此对 643 篇文献进行标题/摘要级别的 DL 语义筛选：

| 纳入信号 | 排除信号 |
|---|---|
| attention mechanism, vision transformer, deep learning, ViT, Swin, self-attention | power amplifier, MMIC, DC-DC converter, Doherty, RFID tag, inductive coupling, flyback converter |

| 阶段 | 输入 | 输出 | 方法 |
|---|---|---|---|
| 去重 | 643 | 643 | UT + DOI 双重校验（零重复） |
| DL 语义筛选 | 643 | 147 | 标题/摘要关键词匹配 + 人工核验 |

筛选细则与 PRISMA 2020 流程见 reports/screening_rule.md 与 reports/prisma_flowchart.md。

**双集设计逻辑**：全量 643 篇作为 CiteSpace 输入（保证统计稳健性），DL 纯净集 147 篇作为核心解读对象（保证 AI 方法论聚焦）。两集互为正交、交叉验证。

### 2.4 分析工具与参数

| 工具 | 版本 | 用途 |
|---|---|---|
| CiteSpace | 6.4.1 | 关键词共现、共被引聚类、突现检测、时间线 |
| Python (bibliometrics-mini) | — | 辅助指标计算与数据清洗 |

| 参数 | 设定值 | 依据 |
|---|---|---|
| 时间切片 | 2015–2025 (Slice=1) | 精细追踪年度变化 |
| 节点选择 | g-index (k=25) | 自适应各时间切片文献量差异 |
| 网络裁剪 | Pathfinder + Pruning sliced networks | 提取骨架结构，突出关键路径 |
| 聚类标签 | LLR (Log-Likelihood Ratio) | 从施引文献标题/摘要提取代表性术语 |

---

## 3 结果

### 3.1 发文趋势

2017–2021 年间，该交叉领域年均发文不足 3 篇，学术界对 "Transformer + 半导体制造" 的组合几乎处于无意识状态。2021 年 ViT 与 Swin Transformer 发表后，经过约 1 年的学术传导延迟，2022 年起发文量开始以年均 83%–182% 的爆发速度增长。至 2024–2025 年，DL 纯净集中 78% 的论文集中涌现（115/147 篇），领域正式进入白热化上升期。

| 阶段 | 时间 | 特征 |
|---|---|---|
| 萌芽期 | 2017–2021 | 年均不足 3 篇，传统电力电子话语权主导 |
| 加速期 | 2022–2023 | ViT/Swin 传导生效，AI 方法首次规模化导入 |
| 爆发期 | 2024–2025 | 78% 论文集中涌现，Transformer 架构全面接管 |

该曲线呈现典型的技术 S 曲线早期特征——跳跃式增长后，预计未来 2–3 年内将趋于理性沉淀。

### 3.2 国家/地区分布

| 排名 | 国家 | 发文量 | 占比 |
|---|---|---|---|
| 1 | China | 260 | 40.4% |
| 2 | USA | 80 | 12.4% |
| 3 | South Korea | 57 | 8.9% |
| 4 | UK | 38 | 5.9% |
| 5 | Germany | 36 | 5.6% |

中国以 260 篇的发文量断层式领先，是第二名美国（80 篇）的 3.25 倍，直观反映了近年来中国在面临外部技术封锁背景下，对"半导体智能制造 × AI 工业赋能"交叉科研投入的巨大强度。但需注意——中国的主导地位主要体现在发文量层面，ViT (Google)、Swin Transformer (Microsoft) 等奠基性工作仍由非中国机构完成。中国面临的挑战已从"能不能发更多"转向"能不能定义方向"。

### 3.3 核心机构

| 排名 | 机构 | 发文量 |
|---|---|---|
| 1 | Southeast University | 14 |
| 2 | Chinese Academy of Sciences | 12 |
| 3 | Univ Elect Sci & Technol China | 12 |
| 4 | Zhejiang University | 10 |
| 5 | Xi'an Jiao Tong University | 10 |

Top 5 机构全部来自中国，以工科强校为主，分布均衡（差距仅 4 篇），未出现单极集中。

### 3.4 关键词共现与 LLR 聚类

CiteSpace 关键词共现网络经 LLR 算法聚类，共识别 10 个聚类（Q=0.673, S=0.902），呈现"方法论（AI）× 应用场景（半导体器件）"的自然共生结构：

**AI 方向（4/10, 40%）**：

| 聚类 | 标签 | 状态 |
|---|---|---|
| #1 | machine learning | 活跃至 2025 |
| #2 | annotation | 活跃至 2025 |
| #3 | defect detection | 活跃至 2025 |
| #8 | cnn | 活跃至 2025 |

**传统方向（6/10, 60%）**：

| 聚类 | 标签 | 状态 |
|---|---|---|
| #0 | lithium-ion batteries | 持续活跃 |
| #4 | inductors | 2022 年后学术死亡 |
| #5 | forward converter | 持续活跃 |
| #6 | energy efficiency | 持续活跃 |
| #7 | eigenvalues | 持续活跃 |
| #9 | parallel processing | 2022 年后学术死亡 |

**关键判断**：#4 inductors 与 #9 parallel processing 于 2022 年后系统性"学术死亡"，与 AI 聚类的"高速崛起"形成"此消彼长"结构。这不是关键词偏好的微调，而是整个研究共同体的注意力结构发生了代际级别的重组。

### 3.5 共被引网络：三层引文结构

共被引网络（N=383, E=1,262, Q=0.8411, S=0.9522）呈现高度结构化的三层倒金字塔：

| 层级 | 角色 | 代表节点 | 时间 |
|---|---|---|---|
| L1 架构奠基 | 理论源头 | Vaswani (2017) Attention Is All You Need → Dosovitskiy (2021) ViT → Liu Z (2021) Swin Transformer | 2017–2021 |
| L2 方法改进 | 技术桥梁 | DETR、DeiT、PVT、Medical Image Segmentation | 2020–2021 |
| L3 应用落地 | 半导体场景 | Wei YX (2022) 晶圆缺陷识别、Fan SKS (2024) 晶圆图分类、Wen L (2022) 版图生成、Yu JB 系列 | 2022–2024 |

三层引文结构有力地证明：该交叉领域的知识基础并非内生，而是"从通用 AI 外部输出 → 半导体场景内部吸收"的知识溢出路径。从 L1 理论奠基到 L3 工业落地，完整知识传导链耗时约 5 年。Q=0.8411 的高模块度表明网络结构分化清晰，S=0.9522 的轮廓值表明聚类质量优良。

### 3.6 突现检测：三波技术浪潮

Kleinberg 突现检测算法共识别 25 个突现词（2015–2025），按时间顺序呈现三波清晰的技术浪潮：

**第一波 (2017–2019) · 传统器件**：RFID、电感耦合、反激变换器、电荷均衡、负载调制——突现强度均 < 0.7，信号微弱。Transformer 尚未进入半导体文献视野。

**第二波 (2020–2022) · AI 方法渗透**：mathematical model (Burst 1.20)、classification (Burst 1.90，全时段最强)、CNN (Burst 1.19)——标志 AI 分类方法正式进入半导体领域。

**第三波 (2023–2025) · Transformer 大爆发**：
- 2024 年为关键历史拐点——vision transformers (1.05)、ViT (1.05)、super resolution (1.05)、scanning electron microscope (1.59)、load modeling (1.05)、data augmentation (0.89) 六个术语同步突现
- 2025 年 anomaly detection (0.97) 接棒成为最新前沿

突现强度绝对值普遍不高（最高 1.90），这与交叉领域仍处高速扩张初期、文献基数快速增长导致词频基线抬高的统计特征有关，不削弱趋势信号的结构性意义。

### 3.7 技术迁移路径

突现检测与聚类时间线共同绘制了一条跨领域技术迁移的清晰轨迹：

```
NLP Attention (Vaswani 2017)
    ↓
CV Backbone (ViT/Swin 2021)
    ↓
Wafer Defect & Layout (2022–2025)
    ↓
Anomaly Detection + Predictive Maintenance (2025)
```

2023 年 ChatGPT/GPT-4 引发的全球 AI 热潮极大地加速了 Transformer 架构向非 NLP 领域的渗透。2023 与 2024 两个拐点的时间叠加形成了该领域的"压缩式爆发"——在 24 个月内完成了通常需要 5–8 年的学术范式转型。

### 3.8 合作网络

合作网络呈现高度模块化特征（Q=0.83），表明研究团队相对独立，跨团队、跨国合作较少。中国内部机构间合作相对紧密，但国际合作强度偏低。

---

## 4 讨论

### 4.1 研究热点演变

基于突现检测与聚类时间线，研究热点呈现清晰的三阶段演变：

| 阶段 | 时间 | 主导方向 | 代表术语 |
|---|---|---|---|
| 萌芽期 | 2017–2019 | 传统电力电子硬件 | RFID, flyback converter, inductive coupling |
| 加速期 | 2020–2022 | AI 分类方法导入 | mathematical model, classification, CNN |
| 爆发期 | 2023–2025 | Transformer 架构全面接管 | vision transformers, ViT, anomaly detection |

传统硬件聚类（#4 inductors, #9 parallel processing）2022 年后系统性"学术死亡"与 AI 聚类齐头并进活跃至 2025 年的此消彼长结构，比单纯的 AI 关键词频次增长更具说服力地证明了学术资源的系统性转移。

### 4.2 知识基础

该交叉领域的知识基础呈现"外部输入"而非"内部增生"的独特特征。L1（Vaswani → ViT → Swin）与 L2（DETR、DeiT、PVT）的高被引节点全部发表于 2017–2021 年，均属于通用 AI/计算机视觉领域；L3 层节点集中于 2022–2024 年，才真正落地半导体制造场景。这与传统成熟学科"知识基础与前沿同域"的格局截然不同。

### 4.3 突现检测强度解读

25 个突现词中，最高强度仅 1.90（classification），远低于成熟领域的典型值。这一现象需从统计机制层面理解：Kleinberg 算法以词频的"相对爆发"为核心信号，当文献基数快速增长时，单一术语的频率抬升被更宽的基线"稀释"。因此，绝对值不高不意味趋势不重要——三阶段技术演进的时间结构、2024 年 6 词同步突现的"共现验证"，以及聚类格局的此消彼长，构成了多条独立证据线。

### 4.4 竞争格局反思

中国发文量断层式领先（260 篇，40.4%）是该交叉领域最显著的结构特征之一。然而，奠基性工作从 Vaswani (Google, 2017) 到 ViT (Google, 2021) 到 Swin (Microsoft, 2021) 均由海外机构完成。中国当前更接近"应用验证者"角色——大量论文集中在将现有架构迁移到晶圆/封装缺陷检测等具体场景。如何在基础架构创新（而非应用层微调）上形成可比肩的原创性贡献，是该领域下一阶段的核心课题。

### 4.5 局限性

1. **单数据库依赖**：仅使用 WoS 核心合集，未覆盖 Scopus、IEEE Xplore 等工程类数据库，部分半导体制造方向的会议论文可能遗漏
2. **DL 语义筛选的边界模糊性**：147 篇 DL 纯净集依赖人工读标题与摘要判断，存在少量主观偏差
3. **CiteSpace 参数敏感性**：g-index k=25 与 Pathfinder 剪枝为标准配置，不同参数可能影响网络局部形态
4. **静态快照局限**：检索截止 2026-04-14，2026 年数据未满全年，趋势解读需谨慎
5. **全量集噪声**：643 篇全量集中约 77% 为电力电子变压器等非 DL 文献，部分分析（如核心期刊排名）受此影响

---

## 5 结论

### 5.1 主要发现

本研究通过 643 篇文献的系统计量分析，全景式地扫描了 Transformer 架构从 NLP 基础研究跨界渗透至半导体制造这一"硬科技"场景的完整路径：

1. **爆发式增长**：DL 纯净集中 78% 论文发表于 2024–2025 年，领域处于技术 S 曲线早期
2. **三层引文结构**：知识基础呈"架构奠基→方法改进→应用落地"三层倒金字塔，知识传导链约 5 年
3. **三波技术浪潮**：25 个突现词呈三波清晰递进，2024 年为关键历史拐点（6 词同步突现）
4. **范式代际重组**：AI 聚类崛起与传统聚类学术死亡的此消彼长结构，标志学术资源系统性转移
5. **中国断层领先**：发文量 40.4%，但需从"量"向"质"转型

**核心判断**：Transformer 在半导体制造领域的应用已越过技术可行性的临界点，进入工程落地与规模化验证阶段。学术资源已系统性转移——下一个五年，答案不在"会不会继续增长"，而在"谁能定义这个领域的基准方法与评估体系"。

### 5.2 未来方向

**【技术层】**
1. 多模态大统一：将 Vision Transformer 扩展到"光学图像 + SEM 图像 + 电性测试时序数据"的多模态联合表征
2. 小样本迁移学习：晶圆缺陷标注成本极高，Few-shot/ViT 迁移是工业落地的首要瓶颈
3. 从检测到预测：当前 90% 以上文献集中于表观缺陷检测，向设备预测性维护、工艺良率预判等上游场景的迁移几乎是空白
4. 边缘端轻量化部署：ViT 的蒸馏/剪枝/量化变体在边缘节点的 < 50ms 低延迟推理是量产前提

**【方法论层】**
5. 动态演进追踪：建立定期（半年）更新机制，追踪聚类的新生/分裂/合并
6. 跨库交叉验证：引入 Scopus/IEEE Xplore 数据源，检验 WoS 单库结论的外部有效性

**【战略层】**
7. 中国从"量"到"质"的转型：在基础架构创新上形成与 ViT/Swin 比肩的原创贡献
8. 产学研闭环：纳入专利与产线部署报告，揭示"实验室→Fab 厂"的技术转化效率

---

## 参考文献

[1] Kleinberg J. Bursty and hierarchical structure in streams[J]. Data Mining and Knowledge Discovery, 2003, 7(4): 373-397.

[2] Chen C. CiteSpace II: Detecting and visualizing emerging trends and transient patterns in scientific literature[J]. Journal of the American Society for Information Science and Technology, 2006, 57(3): 359-377.

[3] Vaswani A, Shazeer N, Parmar N, et al. Attention is all you need[C]. Advances in Neural Information Processing Systems (NeurIPS), 2017: 5998-6008.

[4] Dosovitskiy A, Beyer L, Kolesnikov A, et al. An image is worth 16x16 words: Transformers for image recognition at scale[C]. International Conference on Learning Representations (ICLR), 2021.

[5] Liu Z, Lin YT, Cao Y, et al. Swin Transformer: Hierarchical vision transformer using shifted windows[C]. IEEE/CVF International Conference on Computer Vision (ICCV), 2021: 10012-10022.

[6] Wei YX, Wang H. Mixed-type wafer defect recognition with multi-scale information fusion transformer[J]. IEEE Transactions on Semiconductor Manufacturing, 2022, 35: 341-352.

[7] Fan SKS, Chiu SH. A new ViT-based augmentation framework for wafer map defect classification to enhance the resilience of semiconductor supply chains[J]. International Journal of Production Economics, 2024, 273: 109275.

[8] Chen KQ, Cai N, Wu ZS, et al. Multi-scale GAN with transformer for surface defect inspection of IC metal packages[J]. Expert Systems with Applications, 2023, 212: 118788.

[9] Liu YL, Wu H. Automatic solder defect detection in electronic components using transformer architecture[J]. IEEE Transactions on Components, Packaging and Manufacturing Technology, 2024, 14: 166.

[10] Wen L, Zhu Y, Ye L, et al. LayouTransformer: Generating layout patterns with transformer via sequential pattern modeling[C]. IEEE/ACM International Conference on Computer Aided Design (ICCAD), 2022.

---

**稿件版本**：v3.0
**更新日期**：2026-05-06
**状态**：已同步 DL 二次筛选、CiteSpace 真实数据、三阶段技术演进、三层引文结构、2024拐点等最新发现
