## 📝 更新日志 (Changelog) - 2026-04-14-纪彦泽

### ✅ 已完成任务
* **检索式更新**：
    * 优化了 `NOT` 排除逻辑，增加了 `smart grid`、`financial`、`natural language` 等过滤词。
    * 数据量从初始测试状态更新为 **643 条** 核心文献，确保了后续分析的代表性。
* **仓库环境规范化**：
    * 建立了 `/baseline/params.md`：固化了 g-index (k=25) 和 Pathfinder 裁剪算法。
    * 建立了 `/baseline/tool_selection.md`：明确了 CiteSpace (GUI) + WOS (Data) + Agent 的技术路线。
* **数据清洗**：
    * 删除了仓库内早期测试用 `download.txt` 文件，保持 Data 目录纯净。
* **初步图像生成与优化 (Visual Output)**：
    - 成功生成基于 643 条文献的初始关键词知识图谱（Analysis_v1_Initial_Map_20260414.png）。
