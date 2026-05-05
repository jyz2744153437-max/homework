# 项目大纲与阶段目标

> Transformer 在半导体制造中的文献计量分析（2015-2025）
> 课程：文献计量学和前沿趋势追踪 | 杨其晟 副教授 | 湖南大学 | 2026 春

---

## 一、课程要求回顾

| 里程碑 | 截止周次 | 交付物 | 分值 |
|---|---|---|---|
| M1 | 第 4 周末 | 数据 + 检索方案 + 筛选流程 | 20/60 |
| M2 | 第 10 周末 | 计量分析产出（图谱 + 指标） | 20/60 |
| M3 | 第 15 周末 | 终稿论文 + 可复现 Release | 20/60 |

**评分权重：** 考勤 20% + 综述实践 60% + 汇报 20%

**核心原则：** 参数不是细节，所有选择必须有可辩护理由，不说"随便试的"。

---

## 二、当前状态评估

### 已完成
- ✅ 研究方向确定：Transformer × 半导体制造
- ✅ 检索式构建（WOS，643 条核心文献）
- ✅ 数据导出与清洗规则（消歧映射表）
- ✅ 技术路线选型：路线 A（CiteSpace GUI + WOS + Agent 辅助）
- ✅ CiteSpace 参数固化（g-index k=25, Pathfinder 裁剪）
- ✅ 初始关键词聚类图谱（Analysis_v1_Initial_Map_20260414.png）
- ✅ GitHub 仓库规范化（目录结构、CHANGELOG）

### 待完成 / 需补充
- ❌ M1 正式文档（data/README.md 缺字段字典和数据质量报告）
- ❌ PRISMA 筛选流程图
- ❌ 共被引网络分析
- ❌ 文献耦合分析
- ❌ 合作网络分析
- ❌ 完整指标体系计算
- ❌ M3 终稿论文（mini review 6-8 页）
- ❌ 可复现 Release（一键运行命令）

---

## 三、阶段目标规划

### 阶段 1：夯实 M1 基础（Week 4-5，当前）

> 目标：把 M1 的文档缺口补齐，为 M2 打地基

| # | 任务 | 产出 | 验收标准 |
|---|---|---|---|
| 1.1 | 编写 data/README.md | 数据来源、时间戳、字段说明 | 别人能照着复现数据导出 |
| 1.2 | 编写 field_dictionary.md | 字段名、类型、示例值、缺失率 | 每个字段都有统计 |
| 1.3 | 生成数据质量报告 | reports/data_quality.md | 缺失率/重复率/歧义率三项齐全 |
| 1.4 | 绘制 PRISMA 流程图 | reports/prisma_flowchart.png | 四阶段（识别→初筛→资格→纳入） |
| 1.5 | 更新筛选表 | screening.csv（含 reason code） | 每条排除都有原因可追溯 |
| 1.6 | 更新 params.md | 补充所有 CiteSpace 参数及选择理由 | 别人能照着按出一模一样的图 |

---

### 阶段 2：M2 计量分析产出（Week 6-10）

> 目标：用 CiteSpace + 补充 Python 脚本，产出完整的计量分析

| # | 任务 | 产出 | 验收标准 |
|---|---|---|---|
| 2.1 | CiteSpace 共被引聚类分析 | 共被引网络图 + 聚类标签表 | Silhouette > 0.7 |
| 2.2 | CiteSpace 突现检测 | Burst 列表 + 时间轴图 | 识别出核心突现文献 |
| 2.3 | 关键词时间线分析 | Timeline 图（更新版） | 时间切片清晰 |
| 2.4 | 文献耦合分析 | 耦合网络图 | 与共被引结果可对照 |
| 2.5 | 作者/机构合作网络 | 合作网络图 | 识别核心合作群体 |
| 2.6 | 指标计算（Python） | 发文量趋势、h-index、篇均被引 | 含去自引/不去自引两种口径对比 |
| 2.7 | 指标规范文档 | reports/metrics_spec.md | 每个指标含定义/公式/口径/局限 |
| 2.8 | 阈值敏感性分析 | 至少一组对照实验 | 解释稳定/不稳定现象 |

---

### 阶段 3：M3 终稿与 Release（Week 11-15）

> 目标：写出 6-8 页 mini review，发布可复现 Release

| # | 任务 | 产出 | 验收标准 |
|---|---|---|---|
| 3.1 | mini review 初稿 | paper/manuscript_v1.md | 6-8 页，含方法论/结果/讨论 |
| 3.2 | 图表定稿 | outputs/ 目录下所有终版图 | 每张图有明确标题和来源 |
| 3.3 | 可复现脚本 | run_pipeline.py 或 Makefile | 一键生成所有分析结果 |
| 3.4 | 依赖锁定 | requirements.txt / environment.yml | 版本号明确 |
| 3.5 | GitHub Release | v1.0 Release | 包含数据 + 代码 + 报告 + 论文 |
| 3.6 | 期末汇报 PPT | reports/final_presentation.pdf | 15 分钟报告 |

---

## 四、仓库目录结构

```
Transformer-Semiconductor-Bibliometrics/
├── data/
│   ├── raw/              ← 原始 WOS 导出文件
│   └── processed/        ← 清洗后数据
├── src/                  ← Python 分析脚本
├── outputs/              ← 图谱和图表输出
├── reports/              ← 报告文档
│   ├── data_quality.md
│   ├── metrics_spec.md
│   ├── prisma_flowchart.png
│   └── ... 
├── paper/                ← 论文稿件
├── baseline/             ← 参数记录
│   ├── params.md
│   └── tool_selection.md
├── docs/                 ← 文档
│   ├── cleaning_rules.md
│   ├── field_dictionary.md
│   └── project_outline.md
├── config/
│   └── query.yaml        ← 检索式配置
├── README.md
├── CHANGELOG.md
└── .gitignore
```

---

## 五、QC 检查清单

每完成一个阶段，自检以下项目：

- [ ] 检索式已落盘到 config/query.yaml
- [ ] 变更日志完整记录每次修改
- [ ] NOT 误杀检查（抽样 10 条）
- [ ] 导出字段齐全（作者/机构/关键词/摘要/参考文献/DOI）
- [ ] 筛选表含 reason code
- [ ] 网络定义四要素写清（节点/边/权重/阈值）
- [ ] 消歧规则版本化
- [ ] 阈值做了敏感性对照
- [ ] 所有结论指向具体图表

---

## 六、下一步行动

**当前优先级：阶段 1 → 任务 1.1（编写 data/README.md）**

需要我帮你做哪个？
1. 从 task 1.1 开始逐个推进
2. 直接跳到某一步
3. 先调整这个大纲
