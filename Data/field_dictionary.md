# 字段字典 (Field Dictionary)

> 数据源：Web of Science Core Collection
> 导出格式：Plain Text（全记录与引用的参考文献）
> 总记录数：643 条
> 分析日期：2026-04-30

---

## 一、字段分类索引

| 类别 | 字段数 | 说明 |
|---|---|---|
| 文本分析核心字段 | 14 | 标题、摘要、关键词、参考文献等 |
| 作者/机构字段 | 7 | 作者索引、机构、通讯作者等 |
| 书目信息字段 | 11 | 期刊、卷期、页码、ISSN 等 |
| 影响力字段 | 4 | 被引次数、使用次数 |
| 资助字段 | 2 | 基金资助信息 |
| 开放获取 | 1 | OA 标记 |
| 会议/丛书 | 7 | 会议名称、地点、日期等 |
| 系统/标识 | 4 | WOS 唯一 ID、入库日期等 |
| 其他 | 2 | 专利号等特殊类型 |

---

## 二、文本分析核心字段（14个）

| 标签 | 字段名 | 完整率 | 数据类型 | 分析用途 | 示例值 |
|---|---|---|---|---|---|
| TI | Title（标题） | 100% | 字符串 | 主题判断、标题去重 | DG-ViT: a density-guided dual-stream vision transformer for wafer defect detection |
| AB | Abstract（摘要） | 99.7% | 长文本 | 相关性判断、主题建模 | Wafer defect detection is critical to semiconductor manufacturing... |
| DE | Author Keywords（作者关键词） | 90.8% | 分号分隔列表 | 关键词共现、聚类分析 | vision transformer; defect detection; graph convolutional network |
| ID | Keywords Plus®（扩展关键词） | 61.0% | 分号分隔列表 | 补充主题标引、聚类增强 | PMSM; IDENTIFICATION; ALGORITHM |
| CR | Cited References（参考文献） | 99.7% | 多行文本 | 共被引分析、引文网络 | Babu P., 2024, 2024 2 INT C DATA SC... |
| NR | Number of References（参考文献数） | 100% | 整数 | 引用规模统计 | 45 |
| DT | Document Type（文献类型） | 100% | 枚举值 | 文献类型筛选 | Article / Review / Proceedings Paper |
| LA | Language（语言） | 100% | 枚举值 | 语言筛选 | English |
| PT | Publication Type（出版类型） | 100% | 枚举值 | 文献类型识别 | J（Journal）/ B（Book）/ S（Series） |
| SC | Research Areas（研究领域） | 100% | 分号分隔列表 | 学科分布分析 | Engineering; Computer Science |
| WC | Web of Science Categories（WOS学科分类） | 100% | 分号分隔列表 | 学科分布细化 | Engineering, Electrical & Electronic |
| SO | Source Title（来源期刊） | 100% | 字符串 | 期刊来源分析 | MEASUREMENT SCIENCE AND TECHNOLOGY |
| PY | Year Published（出版年） | 100% | 整数 | 年度发文趋势 | 2024 |
| PD | Publication Date（出版日期） | 62.5% | 日期 | 精确时间分析 | MAY 2025 |

---

## 三、作者/机构相关字段（7个）

| 标签 | 字段名 | 完整率 | 数据类型 | 分析用途 | 说明 |
|---|---|---|---|---|---|
| AU | Authors（作者缩写） | 100% | 分号分隔列表 | 作者统计、合作网络 | 格式：Xu, RB（姓全拼+名首字母） |
| AF | Author Full Names（作者全名） | 100% | 分号分隔列表 | 作者识别规范化 | 格式：Xu, Rongbin |
| C1 | Author Addresses（作者机构） | 100% | 多行文本 | 机构合作网络 | 含作者名、机构名、国家、通讯作者标记 |
| C3 | Research Areas / Organizations | 96.9% | 多行文本 | 机构标准化归并 | 规范化机构名列表 |
| RP | Reprint Address（通讯作者） | 100% | 文本 | 通讯作者分析 | 含姓名、机构、邮箱 |
| EM | Email（邮箱） | 93.9% | 字符串 | 作者联系信息 | xieying@ptu.edu.cn |
| RI | Researcher ID（研究者ID） | 69.4% | 字符串 | 作者消歧 | Xu, Rongbin/MTA-9567-2025 |
| OI | ORCID | 67.7% | 字符串 | 作者唯一标识 | 0000-0002-xxxx-xxxx |

---

## 四、书目信息字段（11个）

| 标签 | 字段名 | 完整率 | 数据类型 | 说明 |
|---|---|---|---|---|
| SO | Source Title（期刊名） | 100% | 字符串 | 完整期刊名 |
| J9 | Journal Abbreviation（29字符缩写） | 90.7% | 字符串 | WOS 标准缩写 |
| JI | ISO Abbreviation（ISO缩写） | 69.2% | 字符串 | ISO 标准缩写 |
| SN | ISSN | 82.9% | 字符串 | 国际标准期刊号 |
| EI | eISSN | 63.9% | 字符串 | 电子 ISSN |
| PU | Publisher（出版商） | 100% | 字符串 | 出版商名称 |
| VL | Volume（卷号） | 71.5% | 整数 | 期刊卷号 |
| IS | Issue（期号） | 54.4% | 整数 | 期刊期号 |
| BP | Beginning Page（起始页） | 62.2% | 字符串 | 起始页码 |
| EP | Ending Page（结束页） | 62.2% | 字符串 | 结束页码 |
| AR | Article Number（文章编号） | 24.3% | 字符串 | 部分期刊用编号代替页码 |
| PG | Page Count（页数） | 100% | 整数 | 总页数 |
| GA | Document Delivery No.（文献传递号） | 100% | 字符串 | WOS 内部编号 |

---

## 五、影响力指标字段（4个）

| 标签 | 字段名 | 完整率 | 数据类型 | 分析用途 | 说明 |
|---|---|---|---|---|---|
| TC | Times Cited（WOS核心被引） | 100% | 整数 | 高影响力文献识别 | WOS Core Collection 内被引次数 |
| Z9 | Times Cited, All Databases（全库被引） | 100% | 整数 | 综合影响力 | 跨所有数据库的总被引次数 |
| U1 | Usage Count (Last 180 Days) | 100% | 整数 | 近期关注度 | 近180天的使用次数 |
| U2 | Usage Count (Since 2013) | 100% | 整数 | 累计关注度 | 自2013年以来的总使用次数 |

---

## 六、资助相关字段（2个）

| 标签 | 字段名 | 完整率 | 数据类型 | 说明 |
|---|---|---|---|---|
| FU | Funding Agency（资助机构） | 65.8% | 多行文本 | 资助项目名称和编号 |
| FX | Funding Text（资助全文） | 65.6% | 长文本 | 资助详细信息 |

---

## 七、开放获取字段（1个）

| 标签 | 字段名 | 完整率 | 数据类型 | 说明 |
|---|---|---|---|---|
| OA | Open Access（开放获取） | 24.1% | 枚举值 | 开放获取类型标记 |

---

## 八、会议/丛书相关字段（7个）

| 标签 | 字段名 | 完整率 | 说明 |
|---|---|---|---|
| CT | Conference Title（会议名称） | 32.0% | 有 206 条（约 32%）为会议论文 |
| CL | Conference Location（会议地点） | 32.0% | 同会议记录 |
| CY | Conference Date（会议日期） | 32.0% | 同会议记录 |
| SP | Conference Sponsors（会议赞助） | 25.8% | 会议赞助单位 |
| SE | Book Series Title（丛书名） | 21.5% | 会议论文所属丛书 |
| BN | ISBN | 30.2% | 国际标准书号 |
| BE | Book Editor（编者） | 5.3% | 图书/会议论文集编者 |

---

## 九、系统/标识字段（4个）

| 标签 | 字段名 | 完整率 | 用途 |
|---|---|---|---|
| UT | WOS Unique ID（WOS唯一标识） | 100% | 记录追踪和去重，格式：WOS:001234567800001 |
| DA | Date Added（入库日期） | 100% | 记录 WOS 收录日期 |
| PI | Publisher City（出版商城市） | 100% | 出版商所在城市 |
| PA | Publisher Address（出版商地址） | 100% | 出版商完整地址 |
| WE | ? | 100% | WOS 内部字段 |

---

## 十、字段使用优先级

### 必须保留（分析核心）
TI, AB, DE, CR, NR, DT, PY, AU, AF, C1, C3, RP, TC, Z9, SO, DI, SC, WC, UT, LA

### 建议保留（补充分析）
ID, EM, RI, OI, FU, FX, VL, IS, BP, EP, PG, SN, J9, PD, U1, U2, OA

### 可选保留（信息记录）
CT, CL, CY, SP, SE, BN, AR, EI, GA, DA, PU, PI, PA

### 分析时可移除
FN, VR, PT, GP, HO, BE, SI, PN, PM

---

## 十一、数据文件说明

| 文件 | 记录数 | 说明 |
|---|---|---|
| download_1-500.txt | 500 | 第一批 WOS 导出（前500条） |
| download_501-643.txt | 143 | 第二批 WOS 导出（补遗143条） |
| **合计** | **643** | 两批合并后去重 |

**数据导出格式**：WOS 标准 Plain Text，每条记录以 `PT` 开始、`ER` 结束。字段标签为两个大写字母。

---

**版本**：v1.0
**生成日期**：2026-04-30
**数据文件**：Data/download_1-500.txt, Data/download_501-643.txt
