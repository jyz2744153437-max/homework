# 对标差距分析：EnergySys-AI-Trends vs 我们

> 参照组：ro111Doc/EnergySys-AI-Trends（LSTM × 电力负荷预测）
> 我们：jyz2744153437-max/Transformer-Semiconductor-Bibliometrics（Transformer × 半导体制造）

---

## 一、直接对比

| 交付物 | 参照组 | 我们 | 状态 |
|---|---|---|---|
| **data/README.md** | README2.md 完整记录数据来源、时间戳、字段说明 | 无 | ❌ 缺失 |
| **data/field_dictionary.md** | CNKI+WoS 双数据库，30+字段，含映射规则 | 无 | ❌ 缺失 |
| **reports/data_quality.md** | 缺失率/重复率/一致性/适用场景/改进建议，16条量化分析 | 无 | ❌ 缺失 |
| **reports/screening_rule.md** | 纳入/排除标准 + PRISMA + 代码辅助筛选 | 无 | ❌ 缺失 |
| **reports/novelty_search_v0.md** | 5维度 25指标对比表 + 研究空白论述 | 无 | ❌ 缺失 |
| **reports/metrics_spec.md** | 4大类 16指标，含公式/质量阈值/脚本关联 | 有基础文档 | 需升级 |
| **docs/data_model.md** | 6类节点 + 7类边 + 唯一标识规则 + 字段映射 | 无 | ❌ 缺失 |
| **baseline/params.md** | 四层工具栈 + 核心参数 + 风险控制 + 职责边界 | 有基础版 | 需升级 |
| **baseline/tool_selection.md** | 含选择理由和风险点 | 有基础版 | 可用 |
| **config/query.yaml** | 检索式 + 同义词 YAML | 无 | ❌ 缺失 |
| **docs/query_rationale.md** | 检索设计思路说明 | 无 | ❌ 缺失 |
| **docs/query_changelog.md** | 检索式变更日志 | 无 | ❌ 缺失 |
| **src/（Python脚本）** | co_citation.py, novelty_analyzer, stage1/2_screen, metrics/ | 无 | ❌ 缺失 |
| **outputs/（分析输出）** | 筛选结果、共被引输出、耦合输出 | 只有初始图 | 需补充 |
| **paper/** | 论文框架 | 无 | ❌ 缺失 |
| **Requirements.txt** | 有 | 有(自动生成) | 需核实 |

---

## 二、结论

**参照组大概完成了 M2 中后期阶段**，文档体系完整，代码也有。我们目前 M1 的文档缺口较多。

### 优先补齐（本周可完成）
1. `data/field_dictionary.md` — 字段字典（只读我们的 2 个 WOS txt 文件即可）
2. `reports/data_quality.md` — 数据质量报告
3. `config/query.yaml` — 检索式配置文件
4. `reports/screening_rule.md` — 筛选规则
5. `docs/data_model.md` — 图数据模型

### 后续推进（M2 阶段）
6. `src/` Python 分析脚本
7. `reports/metrics_spec.md` 升级
8. `reports/novelty_search_v0.md`
9. `outputs/` 系统化输出

---

## 三、关于数据的说明

参照组用了 CNKI+WoS 双数据源（156条），我们只用 WOS 单数据源（643条）。**我们的数据量是他们的4倍**，但他们的文档写了 30 多个字段，我们连字段字典都没有。

好消息是：WOS 数据比 CNKI 规范，字段完整度更高，写文档反而更简单。
