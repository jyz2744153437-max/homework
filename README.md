# homework
# 基于 Transformer 的半导体制造关键技术研究热点与发展趋势 —— 文献计量分析（2015-2025）

## 1. 项目简介
本项目通过文献计量学方法，探索 Transformer 架构在半导体制造（如晶圆缺陷检测、工艺优化等）领域的应用图谱。

## 2. 数据获取
* **核心检索式**：`TS=("Transformer" OR "Vision Transformer" OR "ViT" OR "Swin Transformer" OR "Autoformer" OR "Informer" OR "PatchTST") AND TS=("semiconductor" OR "wafer" OR "integrated circuit" OR "lithography" OR "semiconductor packaging" OR "wafer fabrication" OR "chip manufacturing") NOT TS=("power transformer" OR "voltage" OR "current transformer" OR "medical image" OR "NLP" OR "natural language" OR "traffic" OR "power load" OR "smart grid" OR "distribution network" OR "financial")`
* **时间跨度**：2015 年 - 2025 年
* **文献规模**：共计 **643** 条核心有效数据。

## 3. 技术栈选型（路线 A）
[cite_start]根据课程 Lesson 9 要求，本组采用 GUI 驱动路线 [cite: 628-634, 704-710]：
* [cite_start]**GUI 层**：CiteSpace（主方案，用于聚类与热点分析） [cite: 704-710]。
* **数据层**：WOS 网页端（主方案，用于全记录数据导出）。
