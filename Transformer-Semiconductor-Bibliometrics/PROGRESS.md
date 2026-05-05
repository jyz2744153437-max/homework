# 项目进度追踪

> 最后更新：2026-05-06
> 当前阶段：M3 终稿与 Release（进行中）

---

## 总览

| 里程碑 | 截止 | 状态 | 完成度 |
|---|---|---|---|
| M1 数据与检索方案 | 第4周末 | ✅ 完成 | ██████████ 100% |
| M2 计量分析产出 | 第10周末 | ✅ 完成 | ██████████ 100% |
| M3 终稿与Release | 第15周末 | 🔄 进行中 | █████████░ 95% |

---

## 阶段 1：M1 基础文档

| # | 任务 | 状态 | 产出 |
|---|---|---|---|
| 1.1 | data/field_dictionary.md | ✅ 完成 | 52字段完整字典，含完整率与用途 |
| 1.2 | reports/data_quality.md | ✅ 完成 | 零重复、A级质量评级、年度趋势、期刊分布 |
| 1.3 | config/query.yaml | ✅ 完成 | 检索式配置文件（含v0/v1/v2-final三版本） |
| 1.4 | reports/screening_rule.md | ✅ 完成 | 筛选规则 + 排除原因编码表 |
| 1.5 | reports/novelty_search_v0.md | ✅ 完成 | 查新报告（确认无直接竞争综述） |
| 1.6 | PRISMA 流程图 | ✅ 完成 | reports/prisma_flowchart.md（Mermaid格式） |
| 1.7 | data/README.md | ✅ 完成 | 数据说明文档 |

## 阶段 2：M2 计量分析

| # | 任务 | 状态 | 产出 |
|---|---|---|---|
| 2.1 | 关键词聚类图谱（更新版） | ✅ 完成 | outputs/keyword_cooccurrence_network.png/html |
| 2.2 | 共被引网络分析 | ✅ 完成 | outputs/co_citation_network.png/html + cluster_summary |
| 2.3 | 突现检测 | ✅ 完成 | outputs/keyword_bursts.csv + timeline + report |
| 2.4 | 关键词时间线 | ✅ 已有初版 | Timeline_v1 |
| 2.5 | 文献耦合分析 | ✅ 完成 | outputs/bibliographic_coupling_network.png/html |
| 2.6 | 合作网络分析 | ✅ 完成 | outputs/coauthorship_network.png/html |
| 2.7 | 指标计算 | ✅ 完成 | outputs/network_metrics_*.csv + descriptive_indicators.csv |
| 2.8 | reports/metrics_spec.md 升级 | ✅ 完成 | 补全指标公式和口径 |
| 2.9 | docs/data_model.md | ✅ 完成 | 图数据模型文档 |

## 阶段 3：M3 终稿

| # | 任务 | 状态 | 产出 |
|---|---|---|---|
| 3.1 | mini review 初稿 | ✅ 完成 | paper/manuscript_v1.md |
| 3.2 | CiteSpace 操作指南 | ✅ 完成 | docs/citespace_guide.md（桌面备份） |
| 3.3 | PPT 内容大纲 | ✅ 完成 | 桌面 CiteSpace操作指南与PPT大纲.md |
| 3.4 | GitHub Release v1.0 | ✅ 完成 | https://github.com/.../releases/tag/v1.0 |
| 3.5 | CiteSpace 图表生成 | ✅ 完成 | Visual output/*.png（6类图谱） |
| 3.6 | 期末汇报 PPT | 🔄 进行中 | ppt制作/项目展示_无动画.pptx（半成品，HTML转PPT已完成，待精排） |
| 3.7 | 项目展示网页 | ✅ 完成 | gh-pages（独立 HTML，CDN 版） |

---

## 已完成记录

| 日期 | 事项 | 产出 |
|---|---|---|
| 04-14 | 检索式三轮迭代、数据清洗、CiteSpace 初图 | 643 条数据、关键词图、时间线图 |
| 04-14 | 仓库规范化、params.md、tool_selection.md | baseline 文档 |
| 04-14 | CHANGELOG 初版 | CHANGELOG.md |
| 04-30 | GitHub 仓库克隆到本地、Git 配置 | 本地仓库 |
| 04-30 | 课件 L1-L9 阅读 | 课程要求梳理 |
| 04-30 | 项目大纲 | docs/project_outline.md |
| 04-30 | 对标参照组分析 | docs/benchmark_gap_analysis.md |
| 04-30 | 研究方法论 | reports/methodology.md |
| 04-30 | 进度文件 | PROGRESS.md |
| 04-30 | 字段字典（52字段完整分析） | data/field_dictionary.md |
| 04-30 | 数据质量报告（A级评级） | reports/data_quality.md |
| 04-30 | 综述范本 + L17-18案例讲解（五步法框架） | 课件及杂项/README.md |
| 05-01 | 检索式配置文件（含三版本迭代历史） | config/query.yaml |
| 05-01 | 筛选规则文档 + 排除原因编码表 | reports/screening_rule.md |
| 05-01 | 查新报告 v0（确认无直接竞争综述） | reports/novelty_search_v0.md |
| 05-01 | PRISMA 流程图（Mermaid 格式） | reports/prisma_flowchart.md |
| 05-01 | 数据说明文档 | Data/README.md |
| 05-01 | 指标计算脚本（Node.js） | src/metrics_calculator.js |
| 05-01 | 指标规范文档 v2.0 | reports/metrics_spec.md |
| 05-01 | 图数据模型 | docs/data_model.md |
| 05-01 | 分析管道脚本 | run_pipeline.js |
| 05-01 | Python 依赖清单 | requirements.txt |
| 05-01 | Mini Review 初稿 | paper/manuscript_v1.md |
| 05-01 | 指标统计报告 | outputs/metrics_report.md |
| 05-01 | Python 文献计量分析（bibliometrics-mini） | 4 种网络图 + 指标 + HTML 报告 |
| 05-01 | 筛选记录脚本 + 报告 | src/create_screening.py, reports/screening_record.md |
| 05-01 | 检索式设计文档 | docs/query_rationale.md, docs/query_changelog.md |
| 05-01 | 查新报告升级（五维度详细对比表） | reports/novelty_search_v0.md |
| 05-01 | 突现检测（Kleinberg 算法） | outputs/keyword_bursts.csv, keyword_burst_timeline.png, keyword_burst_report.md |
| 05-01 | README 重写——补背景、更新结构、修正引用 | README.md |
| 05-01 | Repo 设置——Description + 7 个 Topics | GitHub |
| 05-01 | 项目展示网页部署至 GitHub Pages | site/ → gh-pages |
| 05-01 | 网页图谱接口扩至 7 张 | site/src/App.jsx |
| 05-01 | 清理 Python 网络图 HTML 废案 | outputs/*.html, reports/bibliometrics_report.html |
| 05-01 | 网站替换为独立 HTML（CDN 版，无需构建） | gh-pages 更新，旧 site/ 归档 |
| 05-01 | .git 误删恢复（rm -rf .* 炸了） | 从 GitHub 克隆恢复，经验已记录 |
| 05-03 | PPT 半成品（HTML转PPT） | ppt制作/项目展示_无动画.pptx（37MB，待精排） |
| 05-03 | 项目文件大清理 | 删200MB无用文件（安装包/聊天记录/重复数据），去重整理目录，对标分析更新 |
| 05-03 | DL 主题二次筛选 | 643→147 篇纯 DL+半导体论文（排除 496 篇电力电子变压器），创建 screened_dl_final.csv |
| 05-05 | 结论丰富化 | 第六部分从 4 卡片扩展至 7 项核心发现 + 底部总结 |
| 05-05 | 全文序号重理 | 1.1→1.2、2.1→2.2 等全部修正，消除重复编号 |
| 05-05 | 三阶段技术演进页 | 新增 P20B：三波浪卡片 + 递进箭头 + 五列时间线详情 |
| 05-05 | 进度条动画 | 3.2 国家分布页：级联进度条爬升动画 + 圆角渐变 |
| 05-05 | 柱状图渐变 | 3.1 发文趋势柱状图加深 + 左浅右深 9 阶渐变 |
| 05-05 | 仓库优化 | README 重写、过期文档清理、.gitignore 完善、CiteSpace分析套件改名 |
| 05-05 | 桌面文件归档 | 5 轮修改意见 + AI 插图 prompt/产物 + 识图记录 → 工作底稿/ |

---

## 下一步

→ 精排期末汇报 PPT → 更新 GitHub Release → 项目收尾

---

## 2026-05-06 分析报告问题全面修复

| # | 事项 | 产出 |
|---|---|---|
| 6.1 | 时间范围统一 2015-2025 | README、manuscript_v1.md、项目展示.html、三阶段技术演进.html 中所有 "2023-2026"/"2025-2026"→"2023-2025"/"2025" |
| 6.2 | bibliometrics-mini 完整 pipeline 运行 | 基于 DL 纯净集 147 篇，生成 4 个交互式 Plotly 网络图 + 综合报告 + method_note.md |
| 6.3 | 网络指标对齐模板验证 | 确认所有 8 个字段（degree/weighted_degree/betweenness/pagerank/closeness/eigenvector/community）齐全 |
| 6.4 | README 加 TL;DR | 一句话总结置于标题下方 |
| 6.5 | 项目展示页增强 | 嵌入交互式网络图 iframe、更新三阶段技术演进时间 |
| 6.6 | 仓库体积排查 | 159MB：.git 95MB + 工作底稿 25MB + Visual output 23MB |
| 6.7 | 文档同步更新 | PROGRESS.md、CHANGELOG.md、run_pipeline.py 更新 |
| 6.8 | 课程要求对照验证 | 逐一核对课程详细要求细则，确认所有产出齐全 |
