# 更新日志 (Changelog)

## 2026-05-06 — 分析报告问题全面修复

- 时间范围最终统一 2015-2025：README、manuscript、项目展示.html、三阶段技术演进.html 全部核查修正
- bibliometrics-mini 完整 pipeline 运行：基于 DL 纯净集 147 篇，生成 4 个交互式 Plotly 网络图（关键词共现/共被引/文献耦合/合作网络）+ 综合 HTML 报告
- 网络指标对齐模板验证：确认 node metrics 包含全部 8 个字段，与 bmmini.metrics.py 完全一致
- 项目展示.html 嵌入交互式网络图入口链接
- 两份参考文件（分析报告 + 课程要求细则）归档至 `质量基准/`
- 仓库体积排查 + 138MB 大文件清除（git filter-branch）
- gh-pages 部署更新至最新版
- README 新增 TL;DR、PROGRESS 更新至 95%、run_pipeline.py 更新

## 2026-05-05 — 仓库优化与文档归档

- README 重写：更新项目结构、核心发现七大板块、时间范围修正为 2015-2025
- 清理过期文档：删除 benchmark_gap_analysis.md（已过时）、method_note.md（残留笔记）
- .gitignore 完善：新增 .claude/、*.tmp 忽略规则
- 桌面过程文件归档至 `工作底稿/`：5 轮修改意见 + AI 插图 prompt 与产物 + CiteSpace 识图记录
- 文件夹重命名：`CiteSpace图谱制作包` → `CiteSpace分析套件`
- CHANGELOG 与 PROGRESS 同步更新

## 2026-05-05 — 结论丰富化与排版优化

- 结论部分（第六部分）大幅丰富：P27 从 4 张卡片扩展为 6 项核心发现 + 底部总结
- 全文小标题序号重新梳理：1.1→1.2、2.1→2.2 等全部修正
- 新增"突现主题三阶段技术演进解读"页面（P20B）：三波浪卡片 + 递进箭头 + 五列时间线详情
- 3.2 国家分布页重设计：中国 KPI 大区块 + 级联进度条动画（@keyframes）
- 3.1 发文趋势柱状图加深颜色 + 左浅右深渐变
- 多处排版微调：3.4/3.5 图左字右、3.6/3.7 图片上移、感谢页简化

## 2026-05-03 — DL 主题二次筛选

- 643 篇 → 147 篇纯 DL+半导体论文（排除 496 篇电力电子变压器）
- 创建 screened_dl_final.csv，网页数据同步更新
- 项目文件大清理：删除 ~200MB 无用文件（安装包、聊天记录、重复数据）

## 2026-05-01 — 项目展示网页最终版

- 网页替换为独立 HTML（CDN 版，无需构建），部署至 GitHub Pages
- 插入 6 张 CiteSpace 图谱，图谱接口扩展
- Mini Review 初稿完成
- 突现检测（Kleinberg 算法）完成：keyword_bursts.csv + 报告
- Python 文献计量分析（bibliometrics-mini）：4 种网络图 + 指标 + HTML 报告

## 2026-04-30 — M1 阶段文档完成

- 52 字段字典、数据质量报告（A 级）、检索式配置（v0/v1/v2 三版本）
- 筛选规则 + 排除原因编码表、查新报告、PRISMA 流程图
- 研究方法论、对标参照组分析、项目大纲
- 图数据模型、指标规范文档

## 2026-04-14 — 项目初始化

- 检索式三轮迭代：v0 (105) → v1 (512) → v2-final (643)
- CiteSpace 参数固化：g-index k=25, Pathfinder 剪枝, LLR 聚类
- 生成初始关键词知识图谱，完成数据去重
