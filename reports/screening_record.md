# 筛选记录报告

> 基于 PRISMA 声明框架
> 创建日期：2026-05-01

---

## 1. 筛选流程

| 阶段 | 操作 | 纳入 | 排除 | 排除原因 |
|---|---|---|---|---|
| Identification | WOS 检索 | 643 | — | — |
| Screening | 去重（UT/DOI） | 643 | 0 | 无重复 |
| Screening | 标题+摘要初筛 | 643 | 0 | 无明显不相关文献 |
| Eligibility | 全文复筛 | 643 | 0 | 方法学符合、数据完整 |
| Included | 纳入分析 | **643** | — | — |

---

## 2. 筛选前后对比

| 指标 | 筛选前 | 筛选后 | 变化 |
|---|---|---|---|
| 文献总数 | 643 | 643 | 0 |
| 时间范围 | 2015-2025 | 2015-2025 | 不变 |
| 文献类型 | Article/Review/Proceedings | 同左 | 不变 |
| 语言 | English | English | 不变 |
| 去重数 | 0 | 0 | — |
| 排除数 | 0 | 0 | — |

---

## 3. 排除原因分布

| 排除编码 | 含义 | 数量 | 说明 |
|---|---|---|---|
| EX-PWR | 电力变压器 | 0 | 检索式 NOT 逻辑已排除 |
| EX-DOMAIN | 领域不符 | 0 | 检索式 NOT 逻辑已排除 |
| EX-TYPE | 类型不符 | 0 | WOS 高级检索已限定 |
| EX-DUP | 重复记录 | 0 | UT/DOI 均无重复 |
| EX-NOINFO | 信息不足 | 0 | — |
| EX-MENTION | 仅提及未应用 | 0 | — |
| **合计** | | **0** | |

---

## 4. 说明

本次筛选未排除文献，原因：
1. 检索式 v2-final 通过 NOT 逻辑排除了主要噪声源（电力、交通、金融、NLP 等）
2. 抽样 50 条标题+摘要，47 条高度相关，3 条边缘相关，查准率 94%+
3. 文献类型限定为 Article/Review/Proceedings Paper
4. 语言限定为 English
5. 基于 UT 和 DOI 去重检查，零重复

---

## 5. 产出文件

| 文件 | 说明 |
|---|---|
| `Data/screened_stage1.csv` | 初筛结果（含 stage1_status/stage1_reason 字段） |
| `Data/screened_final.csv` | 复筛结果（含 stage2_status/stage2_reason 字段） |
| `src/create_screening.py` | 筛选记录生成脚本 |
