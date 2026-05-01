# 检索式变更日志 (Query Changelog)

> 创建日期：2026-05-01
> 版本：v1.0

---

## 变更记录

| 版本 | 日期 | 结果数 | 变更类型 | 变更摘要 |
|---|---|---|---|---|
| v0 | 2026-04-10 | 105 | 初始 | 基础检索式 |
| v1 | 2026-04-12 | 512 | 优化 | 放宽场景词 + 扩展对象词 |
| v2-final | 2026-04-14 | 643 | 优化 | 补充排除词 |

---

## v0 → v1 详细变更

### 变更背景

v0 仅检索 105 条文献，人工核查发现大量漏检：
- Transformer 变体仅覆盖 3 个
- 场景词过于具体（defect detection）
- 遗漏光刻、封装、IC 设计等场景

### 变更内容

| 类别 | v0 | v1 | 变化 |
|---|---|---|---|
| **对象词** | Transformer, Vision Transformer, ViT | + Swin Transformer, Autoformer, Informer, PatchTST | 新增 4 个 |
| **场景词** | semiconductor manufacturing, wafer defect detection, chip defect | semiconductor, wafer, integrated circuit, lithography | 从具体 → 上位 |
| **排除词** | power transformer, voltage, current transformer, medical image, NLP, natural language | 同 v0 | 不变 |

### 变更理由

```
v0 场景词过于狭窄，导致：
1. 遗漏光刻、封装等制造环节文献
2. 遗漏 IC 设计、工艺优化等应用
3. 查全率过低，无法支撑综述

v1 采用上位词策略：
1. semiconductor 覆盖全制造流程
2. wafer/integrated circuit/lithography 覆盖核心场景
3. 查全率显著提升
```

### 变更后效果

| 指标 | v0 | v1 | 变化 |
|---|---|---|---|
| 结果数 | 105 | 512 | +387 (+487%) |
| 查全率估计 | 低 | 中高 | 提升 |
| 查准率估计 | 高 | 中 | 略降 |

---

## v1 → v2-final 详细变更

### 变更背景

v1 检索 512 条文献，人工核查发现噪声：
- 包含电力系统文献
- 包含交通预测文献（Transformer 用于交通流量预测）
- 包含金融预测文献（Transformer 用于股价预测）

### 变更内容

| 类别 | v1 | v2-final | 变化 |
|---|---|---|---|
| **对象词** | 7 个 | 7 个 | 不变 |
| **场景词** | 4 个 | 7 个（+ packaging, fabrication, chip manufacturing）| 扩展 |
| **排除词** | 6 个 | 11 个 | 新增 5 个 |

新增排除词：
- traffic（交通预测）
- power load（电力负荷）
- smart grid（智能电网）
- distribution network（配电网）
- financial（金融预测）

### 变更理由

```
v1 包含大量噪声文献：
1. Transformer 用于电力负荷预测（场景词 wafer 未排除）
2. Transformer 用于交通流量预测（场景词未排除）
3. Transformer 用于金融时序预测（场景词未排除）

v2-final 补充排除词：
1. traffic 排除交通预测文献
2. power load/smart grid/distribution network 排除电力系统文献
3. financial 排除金融预测文献
```

### 变更后效果

| 指标 | v1 | v2-final | 变化 |
|---|---|---|---|
| 结果数 | 512 | 643 | +131 (+26%) |
| 查准率估计 | 中 | 高 | 提升 |
| 噪声文献 | 多 | 少 | 减少 |

---

## 质量验证记录

### v2-final 验证

| 验证项 | 方法 | 结果 |
|---|---|---|
| NOT 误杀检查 | 随机抽样 10 条 | 0 误杀 |
| 查准率检查 | 随机抽样 10 条 | 9 高度相关，1 边缘相关 |
| 查全率检查 | Transformer 变体覆盖核查 | 主流变体已覆盖 |

---

## 后续维护建议

| 建议 | 说明 |
|---|---|---|
| 定期更新对象词 | Transformer 新变体持续涌现（如 2024 年新架构）|
| 监控排除词误杀 | 新兴应用可能被排除词误排 |
| 补充 CNKI 检索 | 覆盖国内中文文献 |

---

**文档版本**：v1.0
**创建日期**：2026-05-01
**维护者**：Transformer-Semiconductor-Bibliometrics 项目组