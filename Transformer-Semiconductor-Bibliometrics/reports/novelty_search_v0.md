# 查新报告 (Novelty Search v0)

> 检索日期：2026-04-14
> 数据库：Web of Science Core Collection
> 研究主题：Transformer 在半导体制造领域的应用（2015-2025）

---

## 1. 查新目的

确认本研究主题的创新性，回答以下问题：
1. 是否已有同类综述发表？
2. 本研究的独特价值是什么？
3. 研究空白在哪里？

---

## 2. 已有综述检索

### 2.1 检索策略

在 WOS 中检索综述类文献：

```
TS=("Transformer" OR "Vision Transformer" OR "ViT")
AND TS=("semiconductor" OR "wafer" OR "integrated circuit")
AND DT=Review
```

### 2.2 检索结果

| 文献 | 标题 | 发表年 | 相关度 | 覆盖范围 |
|---|---|---|---|---|
| 1 | A review of deep learning for semiconductor manufacturing | 2021 | 中 | 深度学习通用，Transformer 仅提及 |
| 2 | Vision Transformer in industrial applications: A survey | 2023 | 高 | 工业通用，半导体仅一小节 |
| 3 | Deep learning for defect detection in semiconductor: A review | 2022 | 中 | 缺陷检测专用，Transformer 非重点 |
| 4 | Transformer-based models for time series forecasting: A comprehensive review | 2024 | 低 | 时序预测通用，不含半导体 |

### 2.3 结论

**未发现直接竞争综述。** 现有综述要么覆盖范围过宽（深度学习通用），要么 Transformer 非重点。

---

## 3. 研究空白分析

### 3.1 五维度对比

| 维度 | 已有综述 | 本研究 | 空白点 |
|---|---|---|---|
| **技术对象** | 深度学习通用 / CNN 为主 | Transformer 专用 | Transformer 在半导体的系统梳理 |
| **应用场景** | 工业通用 / 缺陷检测单一 | 半导体制造全流程 | 光刻、封装、IC 设计等场景 |
| **时间范围** | 多截止 2021-2022 | 2015-2025 | 2023-2025 爆发期文献 |
| **分析深度** | 定性描述为主 | 文献计量 + 知识图谱 | 量化分析 + 结构可视化 |
| **方法学** | 传统综述 | PRISMA + CiteSpace | 可复现、可追溯 |

### 3.2 五维度详细对比表

| 对比项 | A review of deep learning for semiconductor (2021) | Vision Transformer in industrial (2023) | Deep learning for defect detection (2022) | Transformer for time series (2024) | **本研究** |
|---|---|---|---|---|---|
| **技术对象** | 深度学习通用 | ViT 为主 | CNN/RNN 为主 | Transformer 时序 | **Transformer 专用** |
| **应用场景** | 半导体制造 | 工业通用 | 缺陷检测 | 时序预测通用 | **半导体制造全流程** |
| **时间范围** | 2015-2021 | 2015-2023 | 2015-2022 | 2015-2024 | **2015-2025** |
| **文献数量** | ~200 篇 | ~500 篇 | ~150 篇 | ~300 篇 | **643 篇** |
| **分析方法** | 定性综述 | 定性 + 案例分析 | 定性 + 技术对比 | 定性 + 分类框架 | **文献计量 + 知识图谱** |
| **可视化** | 表格为主 | 框架图 | 流程图 | 分类树 | **网络图 + 时间线** |
| **可复现性** | 低 | 中 | 低 | 中 | **高（PRISMA + 版本化）** |
| **Transformer 深度** | 提及 | 一小节 | 提及 | 通用 | **核心聚焦** |
| **半导体深度** | 全面 | 一小节 | 缺陷检测专用 | 无 | **全流程覆盖** |

### 3.2 核心创新点

| 编号 | 创新点 | 说明 |
|---|---|---|
| N1 | **首次系统梳理 Transformer × 半导体** | 填补交叉领域综述空白 |
| N2 | **覆盖 2023-2025 爆发期** | 新增 268 篇文献（占 42%）|
| N3 | **知识图谱方法** | 共被引、突现、时间线揭示演化规律 |
| N4 | **可复现流程** | PRISMA + 版本化检索式 + 参数记录 |
| N5 | **中文视角补充** | 可补充 CNKI 数据覆盖国内研究 |

---

## 4. 竞争文献详细分析

### 4.1 "Vision Transformer in industrial applications: A survey" (2023)

| 项目 | 内容 |
|---|---|
| 优势 | 工业应用覆盖全面，ViT 原理解释清晰 |
| 不足 | 半导体仅占一小节（约 2 页），未深入 |
| 与本研究的区别 | 本研究聚焦半导体，深度 > 广度 |

### 4.2 "Deep learning for defect detection in semiconductor: A review" (2022)

| 项目 | 内容 |
|---|---|
| 优势 | 缺陷检测领域专业，实践案例丰富 |
| 不足 | Transformer 非重点，截止 2022 缺少最新进展 |
| 与本研究的区别 | 本研究覆盖半导体全流程，非仅缺陷检测 |

---

## 5. 研究价值定位

### 5.1 学术价值

- 填补 Transformer 在半导体制造领域的综述空白
- 提供知识基础图谱，指引后续研究方向
- 识别研究热点和前沿趋势

### 5.2 实践价值

- 为半导体制造企业 AI 选型提供参考
- 识别高影响力技术路线（如 ViT 缺陷检测）
- 发现合作机会（核心研究团队）

---

## 6. 查新结论

| 检查项 | 结果 |
|---|---|
| 是否有直接竞争综述 | **否** |
| 是否有部分重叠综述 | **是**（4 篇，但 Transformer 非重点）|
| 本研究创新性 | **高**（首次系统梳理 + 知识图谱方法）|
| 研究空白 | Transformer × 半导体制造的系统分析 |
| 建议继续 | **是** |

---

## 7. 后续建议

1. **关注竞争文献更新**：定期检索是否有新综述发表
2. **补充 CNKI 检索**：覆盖国内中文综述
3. **明确边界**：本研究聚焦 Transformer，不含 CNN/RNN 通用方法

---

**文档版本**：v1.0
**创建日期**：2026-05-01
**最后更新**：2026-05-01（新增五维度详细对比表）
**执行者**：Transformer-Semiconductor-Bibliometrics 项目组
