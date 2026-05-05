# 数据说明 (Data README)

> 数据源：Web of Science Core Collection
> 导出日期：2026-04-14
> 总记录数：643 条

---

## 1. 数据来源

| 项目 | 说明 |
|---|---|
| 数据库 | Web of Science Core Collection |
| 引文索引 | SCI-EXPANDED, SSCI, CPCI-S |
| 检索式版本 | v2-final（详见 `config/query.yaml`）|
| 检索日期 | 2026-04-14 |
| 导出格式 | Plain Text（Full Record and Cited References）|
| 时间范围 | 2015-2025 |
| 文献类型 | Article, Review, Proceedings Paper |
| 语言 | English |

---

## 2. 文件结构

```
Data/
├── download_1-500.txt        ← 第一批导出（前 500 条）
├── download_501-643.txt      ← 第二批导出（后 143 条）
├── screened_stage1.csv       ← 初筛结果（643 条）
├── screened_final.csv        ← 终筛结果（643 条，含排除原因）
├── screened_dl_final.csv     ← DL 主题筛选（147 条，纯 DL+半导体）
├── field_dictionary.md       ← 字段字典（52 字段详细说明）
└── README.md                 ← 本文件
```

| 文件 | 记录数 | 说明 |
|---|---|---|
| download_1-500.txt | 500 | WOS 单次导出上限 500 条 |
| download_501-643.txt | 143 | 补遗导出 |
| screened_stage1.csv | 643 | 初筛（去重+类型过滤）|
| screened_final.csv | 643 | 终筛（含排除原因编码）|
| **screened_dl_final.csv** | **147** | **DL Transformer 主题筛选** |
| 原始合计 | **643** | — |
| DL 纯净集 | **147** | 排除电力电子变压器论文 |

**关于 DL 主题筛选**：原始 643 篇检索结果中包含大量电力电子/射频电路领域的 "transformer"（电子变压器、耦合变压器）论文，这些与深度学习 Transformer 架构无关。通过标题/摘要/关键词的语义筛选（识别 "attention mechanism"、"vision transformer"、"deep learning" 等 DL 特征词，排除 "power amplifier"、"MMIC"、"DC-DC"、"Doherty" 等电力电子术语），最终保留 147 篇真正使用深度学习 Transformer 架构的半导体相关论文。

---

## 3. 数据格式

### 3.1 记录结构

每条记录以 `PT` 开始，`ER` 结束：

```
PT J
AU Zhang, Y; Li, X; Wang, H
TI Title of the paper
SO Journal Name
...
ER
```

### 3.2 字段标签

WOS Plain Text 格式使用两位字母标签：

| 标签 | 含义 | 示例 |
|---|---|---|
| PT | Publication Type | J (Journal) |
| AU | Authors | Zhang, Y; Li, X |
| TI | Title | Deep learning for... |
| AB | Abstract | This paper proposes... |
| DE | Author Keywords | transformer; defect detection |
| CR | Cited References | Smith J, 2020, NATURE, V1, P1 |
| C1 | Author Addresses | Tsinghua Univ, Beijing, China |
| PY | Year Published | 2024 |
| TC | Times Cited | 15 |
| UT | WOS Unique ID | WOS:001234567800001 |

完整字段说明见 `field_dictionary.md`。

---

## 4. 数据质量摘要

| 指标 | 数值 | 说明 |
|---|---|---|
| 总记录数 | 643 | — |
| 重复记录 | 0 | 基于 UT + DOI 双重验证 |
| 核心字段完整率 | 99%+ | TI, AU, C1, PY, AB, CR |
| DOI 完整率 | 87.4% | 562/643 |
| 参考文献完整率 | 99.7% | 641/643 |
| 整体质量评级 | **A** | 可直接用于分析 |

详细质量报告见 `reports/data_quality.md`。

---

## 5. 使用说明

### 5.1 导入 CiteSpace

1. 打开 CiteSpace 6.4.1
2. File → Import/Export → WOS
3. 选择 `download_1-500.txt` 和 `download_501-643.txt`
4. 点击 Import

### 5.2 导入 VOSviewer

1. 打开 VOSviewer
2. Create → Create a map based on bibliographic database files
3. 选择 WOS 格式
4. 选择 `download_1-500.txt` 和 `download_501-643.txt`

### 5.3 Python 处理

```python
# 读取 WOS Plain Text 格式
def parse_wos_txt(filepath):
    records = []
    current = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('PT '):
                current = {'PT': line[3:]}
            elif line.startswith('ER'):
                records.append(current)
            elif len(line) >= 3 and line[2] == ' ':
                tag = line[:2]
                value = line[3:]
                if tag in current:
                    current[tag] += ' ' + value
                else:
                    current[tag] = value
    return records
```

---

## 6. 版本控制

| 版本 | 日期 | 说明 |
|---|---|---|
| raw_v1 | 2026-04-14 | 初始导出，643 条 |

---

## 7. 相关文档

| 文档 | 路径 | 说明 |
|---|---|---|
| 字段字典 | `Data/field_dictionary.md` | 52 字段详细说明 |
| 数据质量报告 | `reports/data_quality.md` | 完整性、重复率分析 |
| 检索式配置 | `config/query.yaml` | 检索式版本历史 |
| 筛选规则 | `reports/screening_rule.md` | PRISMA 筛选标准 |

---

**文档版本**：v1.0
**创建日期**：2026-05-01
**维护者**：Transformer-Semiconductor-Bibliometrics 项目组
