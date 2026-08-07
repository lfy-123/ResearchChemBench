# ResearchChemBench 计算化学论文筛选流程重构方案

> 状态：第八版设计已实现；严格模式已完成 500 篇缓存重放。
>
> 更新日期：2026-08-07。
>
> 适用范围：主要修改 `data_pipeline/`；仅为版本化能力目录导出对
> `chemistry_toolbox/` 做最小只读接口调整。

## 1. 本版调整

本版采纳以下设计要求：

1. Stage 00 从远端选择指定数量论文，将正文和已有补充材料整理到同一论文目录。
2. Stage 03 先用版本化规则做低成本召回；严格模式用模型复核全部规则候选，只保留作者
   未开展实验、计算为论文主体的纯计算原创研究。Stage 00 已提供的 SI 文本与正文共同参与
   Stage 02/03。
3. Stage 04 只补齐当前数据源缺失的论文正式补充材料，不解析内容，不下载论文中
   引用的数据集、代码仓库、外部结构或任意链接。
4. Stage 04 不只适配 Wiley。优先复用远端 KPS 元数据中的 `support_path`；缺失时按
   出版商调用 ACS、RSC、Elsevier、Wiley、Nature Portfolio 和 MDPI 等适配器。
5. Stage 05 使用 Stage 02 已有正文和本地 SI 文本做完整工作流软件与工具箱能力预筛；
   “命中一个支持后端”不再足以通过。
6. Stage 06 只对 Stage 05 保留的论文解析 Stage 04 新下载、尚未解析的补充材料，避免为全部下载文件运行
   GROBID/MinerU/OCR。
7. Stage 07 Builder 根据正文、SI 文本和能力证据判断可用性、构建任务并复核资源。
8. Stage 08 Judge 独立终审。

新的八阶段流程为：

```text
Stage 00  远端论文选择、复制和按论文整理
    |
Stage 01  正文 PDF 清点、身份和去重
    |
Stage 02  正文及已有 SI 解析和质量门控
    |
Stage 03  规则召回、严格模型复核的纯计算论文筛选
    |
Stage 04  缺失补充材料获取（已有 SI 则逐论文跳过）
    |
Stage 05  正文级完整工作流软件和工具箱能力预筛
    |
Stage 06  幸存论文中新下载 SI 的文本抽取
    |
Stage 07  Builder 可用性判断、任务构建和资源复核
    |
Stage 08  Judge 独立终审
```

## 2. 数据依据

远端数据详细调查见：

- [REMOTE_DATASET_JOURNAL_AUDIT.md](REMOTE_DATASET_JOURNAL_AUDIT.md)

与设计直接相关的结果如下：

### 2.1 `en-paper-hzzj` 不是单一 Wiley 数据集

本地 100 篇恰好是远端对象按名称排序后的第一批，全部为 Angew，存在明显抽样偏差。
完整远端前缀有 21,836 篇：

| 出版商 | PDF 数 | 比例 |
| --- | ---: | ---: |
| ACS | 10,048 | 46.02% |
| Wiley | 6,095 | 27.91% |
| RSC | 4,300 | 19.69% |
| Elsevier | 930 | 4.26% |
| Nature Portfolio | 463 | 2.12% |

已与 KPS 元数据成功关联的 21,121 篇覆盖 JACS、Angew、Chemical Science、ACS
Catalysis、Green Chemistry、Chem、Accounts of Chemical Research、ACS Central Science、
Chem Catalysis、Nature Chemistry 和 Nature Catalysis 等 11 种目标期刊。

### 2.2 KPS 主数据规模

KPS 20260603 元数据包含 935,148 条有效记录、107 个原始期刊名称。出版商分布为：

| 出版商 | 记录数 | 比例 |
| --- | ---: | ---: |
| ACS | 292,579 | 31.29% |
| RSC | 221,497 | 23.69% |
| Elsevier | 166,383 | 17.79% |
| Wiley | 148,832 | 15.92% |
| Nature Portfolio | 53,191 | 5.69% |
| MDPI | 25,428 | 2.72% |
| 其他 8 个 DOI 前缀 | 27,238 | 2.91% |

前六类覆盖 97.09%。Stage 04 第一批适配器按这个顺序实现，而不是只支持 Wiley。

### 2.3 远端已有大量补充材料

KPS 中 431,475 篇已有非空 `support_path`，对应 496,624 个附件；当前这些远端附件
全部是 PDF。`en-paper-hzzj` 已关联记录中也有 18,634 篇存在 `support_path`。

因此 Stage 04 的优先级必须是：

```text
同源远端 support_path
    -> 出版商正式附件页面/API
    -> 合法的预下载缓存
    -> access_blocked / not_found
```

不能对已有远端 SI 重复访问出版商网站。

## 3. 阶段职责边界

| 阶段 | 核心问题 | 成本级别 |
| --- | --- | --- |
| Stage 00 | 如何从远端取指定数量论文并将正文/SI 组成可恢复的论文包？ | 网络 I/O |
| Stage 01 | 正文身份、来源和重复关系是否可靠？ | 低 |
| Stage 02 | 正文和本地已有 SI 是否被可靠解析？ | 中 |
| Stage 03 | 正文+已有 SI 是否证明本文是纯计算化学原创研究？ | 低至中 |
| Stage 04 | 对仍缺 SI 的论文，正式 SI 文件能否获得？ | 网络 I/O |
| Stage 05 | 已解析正文/SI 的全部核心工作流软件和方法族是否被功能级能力覆盖？ | 低至中 |
| Stage 06 | 新下载 SI 中有哪些软件、参数、输入和结果证据？ | 中至高 |
| Stage 07 | 是否能构造可执行、可评分且资源可接受的任务？ | 高 |
| Stage 08 | 构建结果是否满足最终发布标准？ | 高 |

必须区分：

```text
rule_screened_computational
        != preliminary_toolbox_candidate
        != toolbox_covered
        != buildable
        != benchmark_ready
```

Stage 03 和 Stage 05 采用高精度、允许漏筛的策略。只有纯计算身份明确，并且全部核心
工作流软件均有功能验证、全部方法族均存在功能级后端的论文继续；不确定、能力等价、
单个支持软件掩盖其他未覆盖软件和服务错误均 fail closed。

## 4. Stage 00：远端复制和论文包整理

### 4.1 目标和输入

Stage 00 接收远端数据集别名或授权 S3 前缀、需要的论文数量、输出目录和可选的游标，
形成后续阶段唯一认可的本地论文包。Stage 00 可禁用；禁用时用户必须提供相同目录契约
的本地语料。

```text
dataset: en-paper-hzzj | kps-20260603-bu | ... | s3://authorized/prefix/
count: 正整数
output_directory: 本地论文包根目录
resume: true | false
selection: remote_order | manifest_order | seeded_sample
seed: 仅 seeded_sample 使用
```

### 4.2 真实对象清单优先

远端 JSONL/CSV 中的 `doi`、`relative_path`、`pdf_filename` 和 `support_path` 用于
补充论文身份和审计提示，但文件存在性以对象存储清单或 `HEAD` 验证为准。不同快照的
元数据和文件目录可能不同步，禁止将相对 `support_path` 直接拼到另一个快照根目录。

每个已知数据集显式配置 `pdf_prefix` 和 `supplementary_prefix`。中小型目录先列举真实
SI 对象，再按正文文件 stem 与 SI 去掉 `_sup_N` 后的 stem 做大小写无关匹配；数十万
对象的大目录可只对本批元数据候选逐个 `HEAD` 验证。未验证路径只保留在
`metadata_support_hints`，不能进入复制队列。Stage 00 不访问论文网页，也不搜索外部资产。

每次只选择指定数量的正文记录。`count` 以论文正文数计，不把 SI 文件计入数量。

### 4.3 论文目录契约

每篇论文必须独占一个稳定目录，正文和 SI 位于同一个 `paper_id` 目录下：

```text
corpus/
  <paper_id>/
    paper.json
    main/
      <main-pdf-name>.pdf
    supplementary/
      <supplement-1>.pdf
      <supplement-2>.pdf
```

`paper_id` 优先由规范 DOI 生成；没有 DOI 时使用来源 URI 和正文 SHA256。目录名使用安全
slug，但 `paper.json` 保存原始 DOI 和文件名。每篇只允许一个首选正文；多个版本需在
manifest 中声明关系，不能静默覆盖。

`paper.json` 至少包含：

```text
schema_version, paper_id, doi, title, journal_name, issn,
source_dataset, source_record_id, article_url,
main_document, supplementary_documents,
selection_index, copied_at, copy_status
```

每个 document 记录远端 URI、本地相对路径、大小、ETag（若有）和 SHA256。

### 4.4 恢复、原子性和输出

- 使用持久 cursor 和 source manifest，重跑不会选择或复制同一论文两次。
- 文件先写 `.part`，校验后原子改名。
- 一篇论文正文复制失败时，不提交不完整论文目录；SI 单个失败可记录 partial。
- 已存在且 hash 匹配的文件复用；冲突文件不覆盖。
- Stage 00 不删除远端或本地已有数据。

```text
stage_00_remote_corpus/
  corpus/<paper_id>/...
  source_manifest.jsonl
  selected_papers.jsonl
  copy_events.jsonl
  cursor.json
  stage_summary.json
```

## 5. Stage 01：论文包清点、身份和去重

### 5.1 输入假设

默认输入为 Stage 00 论文目录。每篇包含一个正文和零个或多个 SI；来源记录可能包含：

```text
remote_uri
doi
journal_name
issn
article_url
support_path
```

Stage 01 读取 `paper.json`，将同目录文件绑定到相同 `paper_id`。本地没有 SI 不代表论文
官网没有 SI；保留原始 `support_path` 供审计，但 Stage 04 只能重试 Stage 00 已验证的
`matched_remote_uris`，不能根据原始提示猜测对象 URI。

### 5.2 处理

1. 保存 PDF SHA256、文件大小、页数、来源 URI 和来源数据集版本。
2. SHA256 相同标记 `exact_duplicate`。
3. 从来源记录、文件名、PDF 元数据和首页提取 DOI。
4. 用 DOI 聚合同一论文的版本；标题、作者、年份和 ISSN 用于冲突检查。
5. 规范化期刊名用于统计，但保留原始 `journal_name`。
6. 多版本正文保留版本关系和首选版本，不删除审计记录。

### 5.3 输出

```text
stage_01_inventory/
  documents.jsonl
  papers.jsonl
  duplicates.jsonl
  source_metadata.jsonl
  stage_summary.json
```

## 6. Stage 02：正文和已有 SI 解析及质量门控

### 6.1 解析路由

```text
GROBID
  +-- 请求成功且质量达标 ----------------------> 接受
  +-- 单篇请求失败且有文本层 ----> pdftotext --> 质量检查
  +-- 文本/结构质量不足 ----------> MinerU/OCR --> 质量检查
  +-- 所有路径失败 ----------------------------> parse_error
```

GROBID HTTP 成功不等于正文可用。质量门控至少检查：

- 每页有效字符数、乱码比例和扫描页比例；
- 标题、摘要、章节和参考文献完整度；
- 方法、结果和图表标题是否被合理识别；
- 页眉页脚和参考文献是否大量污染正文；
- DOI、标题和页数是否与 Stage 01 冲突。

单篇解析失败必须隔离，不能终止 1000 篇批次。TEI、正文文本、解析器版本、质量报告
和回退原因长期保留。

Stage 02 必须解析 Stage 01 中所有 canonical 正文和本地已有 SI。输出保留
`document_role=main_paper|supplementary`，并生成按 `paper_id` 聚合的
`paper_text_bundle.jsonl`。一个 SI 解析失败不应使正文结果失效。

## 7. Stage 03：规则召回与纯计算模型复核

### 7.1 目标

Stage 03 判断两层问题：规则层判断作者是否可能在本研究中执行了计算化学；严格模型层
判断论文是否为纯计算原创研究，而不是实验论文附带 DFT、MD 或其他支持性计算。

本阶段：

- 默认先执行规则；严格模式必须启用模型并复核全部规则候选；
- 不判断最终工具箱覆盖；
- 不要求明确软件名称；
- 不生成完整 task skeleton；
- 严格模式以结果精度为首要目标，允许漏筛。

### 7.2 版本化规则资产

新增：

```text
assets/computational_method_ontology.yaml
assets/computation_evidence_rules.yaml
assets/computation_negative_contexts.yaml
```

方法本体至少覆盖：

| 方法族 | 术语示例 | 结果示例 |
| --- | --- | --- |
| 分子电子结构 | DFT、TDDFT、MP2、CCSD、CASSCF、semi-empirical | 能量、轨道、频率、激发态 |
| 周期材料计算 | periodic DFT、plane wave、pseudopotential | DOS、band structure、吸附能、声子 |
| 分子动力学 | MD、ab initio MD、umbrella sampling | trajectory、RDF、MSD、PMF |
| 反应与动力学 | TS、IRC、NEB、microkinetic、master equation | 势垒、路径、速率常数 |
| 自由能与统计 | FEP、TI、WHAM、metadynamics | 自由能差、平衡常数 |
| 对接与构象 | docking、conformer search、scoring | pose、score、构象分布 |
| QM/MM 和多尺度 | QM/MM、embedding、coarse graining | 局部能量、环境效应 |
| 计算化学 ML | ML potential、molecular property model | 势能面、化学性质预测 |

`simulation`、`calculation`、`model` 和 `software` 等泛词不能单独通过。

### 7.3 证据类型

规则提取五类证据：

1. `method_evidence`：具体计算方法或任务族。
2. `action_evidence`：优化、单点能、频率、动力学传播、路径搜索等动作。
3. `result_evidence`：能量、轨道、DOS、轨迹、RDF、PMF、势垒等结果。
4. `performed_here_evidence`：`we calculated`、`we performed`、`was optimized` 等本研究
   执行表达。
5. `si_computation_pointer`：`computational details are provided in the Supporting
   Information` 等指向 SI 的证据。

软件名称可以作为弱正证据，但不能成为必需条件。

### 7.4 章节和负面上下文

规则必须利用 Stage 02 的章节结构：

- 标题、摘要、方法、结果、图表标题和结论中的证据加权；
- 引言和 related work 中的证据降权；
- 参考文献、致谢、仪器列表和引用标题中的命中排除；
- `DFT was reported previously`、`unlike computational studies` 等否定或他人工作语境
  不视为本研究执行。

每条证据保存页码、章节、字符范围、原文片段和规则 ID。

### 7.5 确定性评分和路由

先以人工标注小样本校准权重，不在实现前冻结具体分数。判定原则为：

```text
strong_candidate:
  方法/动作证据 + 本研究执行证据 + 结果或 SI 指针

weak_candidate:
  存在方法/结果组合，但执行主体或章节不明确

not_computational:
  无有效证据，或证据确定只来自参考文献/背景

rule_error:
  文本或规则处理失败
```

严格模式要求启用模型，并复核规则产生的全部 strong、weak 和 rule error 候选。模型输入
除规则证据外，还定向加入作者实验行为和软件执行上下文。只有同时满足以下条件才进入
Stage 04：`performed_computation=yes`、原创研究、`computation_role=primary`、
`study_mode=pure_computational`、`author_performed_experiments=no`、置信度至少 0.90，且作者
执行证据能够逐字回映输入片段。模型还需列出带原文证据的 `required_software` 和软件清单
完整度，供 Stage 05 交叉核验。mixed/experimental 记为 `not_pure_computational`；不确定、
响应截断、API/schema 错误或证据失败记为 `llm_unconfirmed`，全部 fail closed。

`recall` 兼容模式仍只审查边界样本并保留规则回退，但批处理入口默认使用严格模式。

同一术语在长文或综述中可能重复数十次。原始命中分数保存为 `raw_score`，用于判定的
`score` 对同一 document、evidence type、rule ID 和章节类型限制贡献次数。明确方法在
非排除章节多次出现、但固定执行句式未命中时保守归入 `weak_candidate`，交给 Stage 05
继续判断，避免规则模板造成早期漏筛。

### 7.6 新软件的影响

Stage 03 不读取工具箱 capability catalog。新增软件时：

- 现有方法族不变：Stage 03 无需重跑；
- 软件别名只作为弱召回证据时，可从工具箱自动生成，不手工维护两份名单；
- 只有新增全新计算范式时才扩充方法本体。

### 7.7 输出

```text
stage_03_computation_relevance/
  decisions.jsonl
  evidence_spans.jsonl
  strong_candidates.jsonl
  weak_candidates.jsonl
  rejected.jsonl
  stage_summary.json
```

## 8. Stage 04：缺失补充材料获取

### 8.1 唯一职责和跳过条件

Stage 04 只负责将属于该论文的正式 Supplementary Information 文件补到本地，并记录
来源、状态和哈希。本阶段不做正文或 SI 文本抽取，不读取附件内容做科学判定。

若 Stage 01/02 已确认论文至少存在一个本地 canonical SI，Stage 04 对该论文直接记录
`skipped_existing_supplementary`，不访问远端对象存储、出版商页面或 API。只有
`supplementary_documents=[]` 的候选进入获取逻辑。

### 8.2 获取顺序

#### 来源 A：Stage 00 已验证对象

若 Stage 00 已保存 `supplementary_discovery.matched_remote_uris` 但初次复制失败：

1. 再次校验 URI 位于当前授权前缀内。
2. 重试复制到按 `paper_id` 隔离的 Stage 04 目录。
3. 记录远端 URI、ETag/大小、SHA256 和来源数据集版本。

原始 `source_record.support_path` 未经 Stage 00 列举或 `HEAD` 验证时不得进入该路径。

#### 来源 B：出版商正式附件

本地与已验证远端对象均无 SI 时：

1. 根据 DOI、ISSN、来源 URL 和 Crossref 元数据识别出版商。
2. 调用对应 publisher adapter。
3. 只枚举出版商页面/API 中标记为该论文 Supplementary Information 的附件。
4. 下载允许类型并保存页面/响应证据。

第一批适配器：

```text
ACSSupplementaryAdapter
RSCSupplementaryAdapter
ElsevierSupplementaryAdapter
WileySupplementaryAdapter
NatureSupplementaryAdapter
MDPISupplementaryAdapter
```

后续按远端占比增加 CSJ/OUP、Thieme、Springer、Taylor & Francis、Beilstein 等适配器。

### 8.3 严格禁止范围

即使正文或官网页面存在链接，Stage 04 也不下载：

- GitHub、GitLab 或其他代码仓库；
- Zenodo、Figshare、OSF、Materials Cloud 等数据集；
- 作者主页、实验室页面或搜索引擎结果；
- PubChem、Materials Project、PDB 等数据库内容；
- 不在出版商正式 SI 清单中的结构和输出文件；
- 需要绕过身份验证、验证码、订阅或授权的文件。

这些链接最多记录为未跟随引用，不能进入下载队列。

### 8.4 文件范围和预算

KPS 的现有 `support_path` 主要是 PDF，但出版社正式 SI 还包括 DOCX、ZIP、XLSX、CSV、
TXT 和 CIF。默认只开启这些文档/归档格式，不默认下载视频。

建议默认：

```text
allowed_extensions: [pdf, docx, zip, xlsx, csv, txt, cif]
max_attachments_per_paper: 20
max_file_bytes: 100 MiB
max_total_bytes_per_paper: 250 MiB
download_timeout_seconds: 120
```

视频默认只保存发现元数据，不下载。Stage 06 对 PDF 做文本抽取，其他正式 SI 文件作为
原始资产保留，不交给 `pdftotext`。

### 8.5 状态

发现和下载分开记录：

```text
discovery_status:
  remote_paths_found | publisher_attachments_found | not_found | metadata_error

download_status:
  skipped_existing_supplementary | downloaded | partial | access_blocked | timeout | oversize |
  unsupported_format | checksum_error | not_attempted
```

`access_blocked` 不是科学淘汰；可以由合法会话或预下载缓存补齐。Stage 04 按 DOI 和
附件哈希缓存，断点恢复不重复下载。

### 8.6 输出

```text
stage_04_supplementary_acquisition/
  supplementary_manifest.jsonl
  discovery_attempts.jsonl
  download_attempts.jsonl
  files/<paper_id>/...
  errors.jsonl
  stage_summary.json
```

## 9. Stage 05：完整工作流软件和工具箱能力预筛

### 9.1 为什么仍是“严格预筛”

Stage 05 使用 Stage 02 已解析的正文和 Stage 00 已带入的 SI 文本。Stage 04 新下载的 SI
按职责边界尚未解析，软件名称仍可能只存在于这些文件中。严格策略接受这部分漏筛，
`software_not_identified` 不再继续。

本阶段目标是只保留“现有文本已能证明完整工作流覆盖”的论文。最终覆盖判断仍由 Stage 07
Builder 在新 SI 文本可用后复核，但 Stage 05 不再以单个支持后端作为放行依据。

### 9.2 工具箱能力快照

实现前必须由 `chemistry_toolbox` 导出版本化 `toolbox_capabilities.json`，至少包含：

```text
backend_id, aliases, availability, validation_level,
actions, method_families, system_types,
elements, basis_or_pseudopotential_constraints,
periodic/excited_state/solvent/force_field support,
input_formats, output_properties, limitations,
evidence_refs, catalog_hash
```

缺失字段表示 `unknown`，不能由模型或程序常识推断为支持。

### 9.3 软件提取

使用 Stage 02 正文和已有 SI 的 TEI/文本：

1. Softcite 提取软件 mention 和上下文。
2. 工具箱别名表做确定性规范化。
3. 排除参考文献、背景引用和仪器软件。
4. 区分核心计算、辅助分析、可视化和工作流软件。
5. 将 Softcite 结果与 Stage 03 模型带原文证据的 `required_software` 合并；未登记但确认
   被用于执行的软件进入未覆盖集合。
6. 逐一检查全部核心/必需软件的 functional、执行语境和方法匹配；再检查每个方法族是否
   至少有一个工具箱中通过 scientific smoke 的后端可承担。

PXRD、SCXRD、DFT、TDDFT、NEB 等不是软件。纯绘图和通用办公软件不进入核心清单；
但用于生成或分析中心计算结果的自定义代码、工作流引擎和科学分析软件必须覆盖。

### 9.4 路由

| 状态 | 条件 | 路由 |
| --- | --- | --- |
| `direct_candidate` | 纯计算已确认；全部核心/必需软件和全部方法族均满足严格覆盖 | Stage 06 |
| `workflow_software_uncovered` | 任一核心、模型必需或执行确认的未分类软件未达到 functional | 淘汰 |
| `workflow_inventory_unconfirmed` | 软件清单无法由模型确认或与 Softcite 交叉印证 | 淘汰 |
| `method_coverage_incomplete` | 任一方法族没有 scientific-smoke 后端 | 淘汰 |
| `not_pure_computational` | Stage 03 纯计算结论不成立 | 淘汰 |
| `direct_support_unverified` | 软件存在但上下文、方法或验证级别任一不足 | 淘汰 |
| `equivalent_unverified` | 只有能力等价推断，没有直接受支持后端 | 淘汰 |
| `method_only_rejected` | 只有方法族，没有直接受支持后端 | 淘汰 |
| `software_unknown_candidate` | 计算成立但软件或能力未知 | 淘汰 |
| `explicitly_unsupported` | 正文明示必需核心软件/功能，工具箱明确不支持且不可替代 | 淘汰 |
| `not_significant` | 只有平凡后处理或辅助软件 | 淘汰/复核 |
| `stage_error` | 提取或能力查询失败 | 可重试，本次淘汰 |

严格模式只接受 `validation_level=functional`。interface、needs-complete-input 和 catalogued
级别均不足以放行。存在一个合格软件不能掩盖同篇论文中的其他不合格软件。模型对软件
清单返回 uncertain 时，只有模型必需软件与 Softcite 全文结果一致且不存在未覆盖/未分类
执行软件，才视为交叉确认。`amber vial`、AMBER force field、背景引用和普通实验软件不能
形成 direct 命中。

### 9.5 新软件扩展

新增软件时：

1. 在工具箱注册 backend、alias、action 和限制。
2. 运行 interface/scientific smoke test。
3. 重新导出 capability snapshot 和 catalog hash。
4. 只重跑历史 Stage 05 及后续阶段。

Stage 03/04 结果可继续复用。

## 10. Stage 06：新下载补充材料文本抽取

### 10.1 唯一输入范围

Stage 06 只解析 Stage 04 新下载、尚未经过 Stage 02 解析，并且论文通过 Stage 05 预筛
的正式 SI 文件。Stage 00 已带入且 Stage 02 成功解析的 SI 直接复用，不重复解析。不得
在本阶段继续联网、搜索数据集或补下载外部资产。

### 10.2 解析路由

对于 PDF SI：

```text
pdftotext 快速质量检查
  +-- 文本层和结构足够 ------------------------> 接受文本
  +-- 需要章节/表格结构 ----------> GROBID ----> 质量检查
  +-- 扫描/复杂布局 --------------> MinerU/OCR -> 质量检查
  +-- 全部失败 --------------------------------> si_parse_error
```

优先使用低成本 `pdftotext`。只有质量不足或 Builder 需要结构化表格时才升级到 GROBID、
MinerU/OCR。不同附件独立失败，单个坏附件不能使整篇或整批失败。

### 10.3 专项抽取包

在通用文本之外，确定性抽取：

- `computational details`、`theoretical methods`、`simulation details` 等章节；
- 软件名称、版本和模块；
- 方法、基组、泛函、赝势、溶剂、色散和收敛参数；
- 电荷、自旋、周期边界、k 点、cutoff、温压和 ensemble；
- 初始结构、输入/输出文件线索和附件内引用；
- 结果表、figure/table 编号、单位和潜在 ground truth；
- 正文 claim 与 SI 证据的关联。

本阶段不决定最终任务是否覆盖，只形成 `supplementary_evidence_bundle` 供 Builder 使用。

### 10.4 输出

```text
stage_06_supplementary_extraction/
  documents.jsonl
  text/<paper_id>/...
  structured_sections.jsonl
  software_evidence.jsonl
  parameter_evidence.jsonl
  result_evidence.jsonl
  extraction_errors.jsonl
  stage_summary.json
```

## 11. Stage 07：Builder 可用性判断和构建

Builder 输入：正文文本、Stage 03 规则证据、Stage 05 预筛结果、Stage 06 SI evidence
bundle 和冻结的工具箱能力快照。

每篇按以下顺序：

1. 用 SI 软件证据重新执行最终工具箱能力覆盖矩阵。
2. 若核心能力明确不支持，`abstain_capability_mismatch`。
3. 检查是否存在关联明确 claim/figure/table 的非平凡计算任务。
4. 检查输入、参数、目标和评分证据是否足够。
5. 不足时结构化 `abstain`，不勉强构造任务。
6. 可用时生成公开输入、隐藏答案、workflow、评分器和证据映射。
7. 根据最终 workflow 评估单任务和总资源；不确定时运行小规模 probe。
8. 最终能力或资源不符合时 `abstain`。

Builder 状态：

```text
candidate_ready
abstain_capability_mismatch
abstain_missing_input
abstain_missing_parameters
abstain_missing_ground_truth
abstain_not_significant
abstain_resource_limit
builder_error
```

Ground truth 等级继续区分：作者原始输出 A、SI 机器可读结果 B、冻结协议重算 C、
正文/SI 图片或文字数字化 D。D 默认不能用于高精度数值评分。

## 12. Stage 08：Judge 独立终审

Judge 在独立会话中检查：

- 任务与论文 claim/figure/table 是否一致；
- 是否包含真实计算，而不是读取或重绘已有答案；
- 工具箱 backend/action 是否真实可用；
- 公开输入是否泄漏隐藏答案；
- ground truth、单位、容差和结构映射是否可靠；
- 资源预算和 probe 证据是否完整；
- 干净环境中是否可以复现任务。

输出：

```text
pass | revise | reject | judge_error
```

本轮不实现 Builder/Judge 自动多轮修订。

## 13. 缓存、错误隔离和并发

### 13.1 论文级失败域

Stage 02-08 均以 `paper_id` 为最小失败域。单篇 HTTP、解析、Softcite、Builder 或 Judge
错误写入状态后继续。只有共享服务无法启动、配置非法或能力快照损坏时才停止整个运行。

### 13.2 缓存键

| 阶段 | 缓存键 |
| --- | --- |
| Stage 00 | 数据集版本 + 选择策略/seed + source record + 远端 ETag |
| Stage 02 | PDF hash + parser/version + quality config |
| Stage 03 | 正文/SI hash + ontology/rules hash + 可选模型/prompt/响应 hash |
| Stage 04 | DOI + source metadata + adapter version + attachment metadata |
| Stage 05 | 正文 hash + software rules + capability catalog hash |
| Stage 06 | SI file hashes + parser config/version |
| Stage 07 | 正文/SI bundle + capability/Builder/config hash |
| Stage 08 | task package + Judge/model/config hash |

新增软件只使 Stage 05、07、08 相关缓存失效；SI 文件和 Stage 06 文本仍可复用。

### 13.3 沙箱生命周期

一次管线任务使用一个大沙箱：开始前创建并启动服务，所有微批次完成后再停止。不能在
阶段之间反复开关沙箱。

Stage 04 网络并发独立限速；Stage 02/03/05/06 使用各自 worker 上限；Stage 07/08
Agent 并发较低。Stage 03 模型只处理规则边界样本，并具有独立并发上限和缓存。

## 14. 审计产物

长期保留：

- 正文来源、SHA256、TEI、文本和解析质量；
- Stage 03 的规则 ID、证据片段、分数和规则版本；
- SI 的 `support_path`/官网 URL、发现和下载状态、文件 SHA256；
- Stage 05 软件 mention、角色、能力快照和预筛理由；
- Stage 06 SI 文本、解析器和专项证据；
- Builder/Judge 输入、原始响应、结构化结果和任务包；
- 代码版本、配置快照、catalog hash、prompt hash 和模型参数。

成功批次不得默认删除这些判定证据。

## 15. 配置草案

```json
{
  "stage00_remote_corpus": {
    "enabled": true,
    "dataset": "en-paper-hzzj",
    "count": 1000,
    "output_directory": "datasets/prepared/current",
    "selection": "remote_order",
    "resume": true,
    "copy_existing_supplementary": true
  },
  "stage03_computation_relevance": {
    "screening_policy": "strict",
    "use_llm": true,
    "method_ontology": "assets/computational_method_ontology.yaml",
    "evidence_rules": "assets/computation_evidence_rules.yaml",
    "negative_contexts": "assets/computation_negative_contexts.yaml",
    "continue_decisions": ["strong_candidate"],
    "llm": {
      "minimum_confidence": 0.9,
      "allowed_computation_roles": ["primary"],
      "required_study_modes": ["pure_computational"],
      "allowed_author_performed_experiments": ["no"],
      "max_tokens": 2048
    }
  },
  "stage04_supplementary_acquisition": {
    "prefer_source_support_paths": true,
    "official_publisher_attachments_only": true,
    "publisher_adapters": ["acs", "rsc", "elsevier", "wiley", "nature", "mdpi"],
    "follow_article_links": false,
    "allowed_extensions": ["pdf", "docx", "zip", "xlsx", "csv", "txt", "cif"],
    "max_attachments_per_paper": 20,
    "max_file_bytes": 104857600,
    "max_total_bytes_per_paper": 262144000
  },
  "stage05_preliminary_coverage": {
    "capability_catalog": "assets/toolbox_capabilities.json",
    "screening_policy": "strict",
    "continue_without_software_name": false,
    "accepted_validation_levels": ["functional"],
    "require_all_core_software": true,
    "require_all_method_families": true,
    "reject_unclassified_execution_software": true,
    "require_pure_computational_review": true,
    "require_complete_software_inventory": true
  },
  "stage06_supplementary_extraction": {
    "fast_parser": "pdftotext",
    "structured_parser": "grobid",
    "complex_layout_parser": "mineru",
    "enable_ocr": true
  },
  "stage07_builder": {
    "recheck_toolbox_coverage": true,
    "require_significant_claim": true,
    "require_machine_scorable_target": true,
    "allowed_ground_truth_grades": ["A", "B", "C"],
    "run_resource_probe_when_uncertain": true
  }
}
```

## 16. 实施计划

用户确认后再修改实现，每个 Phase 独立测试和本地 Git 提交，不推送 GitHub。

### Phase 0：冻结基线和能力目录

1. 冻结旧管线配置、100 篇样本和历史运行摘要。
2. 实现工具箱只读 capability snapshot 导出和 schema 校验。
3. 生成 catalog hash，明确 `supported/unsupported/unknown` 三值语义。
4. 建立正文规则标注小样本和 SI 获取测试样本。

### Phase 1：Stage 00、来源元数据和公共 schema

1. 实现按指定数量选择论文、复制正文/SI、原子写入和断点恢复。
2. 输出每篇独立目录及 `paper.json`，并保存 source manifest/cursor。
3. 将远端 JSONL 的 DOI、journal、ISSN、article URL 和 `support_path` 接入 Stage 01。
4. 增加规则证据、附件状态、软件预筛和 SI evidence bundle schema。
5. 统一论文级错误隔离、审计和缓存。

### Phase 2：Stage 02 质量门控

1. 保留现有 GROBID 主路径，同时解析正文和 Stage 00 已复制的 SI。
2. 完善 pdftotext、MinerU/OCR 回退和真实质量阈值。
3. 输出按 `paper_id` 聚合的正文/SI 文本 bundle。
4. 增加单篇失败和断点恢复测试。

### Phase 3：重建 Stage 03

1. 将旧软件硬门控替换为正文+已有 SI 的规则型 computation relevance。
2. 实现方法本体、章节权重、负面语境和证据定位。
3. 接入可选 OpenAI-compatible 边界复核器，严格校验证据引用并支持规则回退。
4. 用人工样本校准规则阈值与模型路由，先验证 recall，再调 precision。

### Phase 4：重建 Stage 04

1. 对已有本地 SI 的论文直接跳过，并记录确定状态。
2. 对缺失 SI 的论文实现 `support_path` 同源复制和校验。
3. 实现统一 publisher adapter 接口。
4. 首批实现 ACS、RSC、Elsevier、Wiley、Nature、MDPI。
5. 严格禁止跟随外部数据/代码链接。
6. 测试已有 SI 跳过、多附件、403、超时、缓存、大小预算和不存在状态。

### Phase 5：重建 Stage 05

1. 使用正文和 Stage 02 已解析 SI 的 Softcite、别名和角色规则提取软件。
2. 实现 preliminary capability matrix。
3. 保留 method-only 和 software-unknown 通道。
4. 只有正文明确不支持时硬淘汰。

### Phase 6：新增 Stage 06

1. 只解析 Stage 05 幸存论文中由 Stage 04 新下载的 SI 文件。
2. 实现 pdftotext -> GROBID -> MinerU/OCR 的质量升级。
3. 抽取计算细节、软件、参数、输入和结果证据。
4. 单附件失败隔离，保留完整解析证据。

### Phase 7：迁移 Builder/Judge

1. 当前 Stage 06 Builder 迁移为 Stage 07。
2. 当前 Stage 07 Judge 迁移为 Stage 08。
3. Builder 增加 SI 后最终能力复核、结构化 abstain 和资源 probe。
4. Judge 更新阶段契约和终审规则。

### Phase 8：编排、脚本和 shadow run

1. 更新 pipeline、microbatch、CLI、配置和 README。
2. 保持单沙箱生命周期和阶段独立并发上限。
3. 旧结果只读保留，新增 schema/version，禁止静默覆盖。
4. 先运行规则标注集和跨出版商 SI 样本，再运行 100 篇 shadow test。
5. 指标达标后再扩展到 1000 篇和远端批量任务。

## 17. 主要文件范围

```text
data_pipeline/assets/
  computational_method_ontology.yaml
  computation_evidence_rules.yaml
  computation_negative_contexts.yaml
  toolbox_capabilities.json

data_pipeline/src/integrations/publishers/
  base.py
  acs.py
  rsc.py
  elsevier.py
  wiley.py
  nature.py
  mdpi.py

data_pipeline/src/stages/
  stage00_remote_corpus/
  stage03_computation_relevance/
  stage04_supplementary_acquisition/
  stage05_preliminary_coverage/
  stage06_supplementary_extraction/
  stage07_builder/
  stage08_judge/

data_pipeline/src/orchestration/
  pipeline.py
  microbatch.py
```

旧 Stage 03/04/05 和 Builder/Judge 目录先保留到 shadow run 通过，再迁移或删除。批量
脚本中“Stage 01-04 通过”的含义将改变，必须增加 pipeline schema 版本和迁移说明。

## 18. 验收重点

- Stage 00 指定 `count=N` 时输出 N 个完整正文论文包，正文和 SI 位于同一论文目录。
- Stage 02/03 会处理 Stage 00 已复制的 SI，Stage 04 对这些论文不发起下载。
- Stage 03 recall 模式可关闭模型；strict 模式复核全部规则候选，失败逐篇 fail closed。
- 规则命中保留可定位证据，参考文献中的 DFT/软件名不会直接通过。
- strict 模式下缺少直接软件证据、任一必需软件未覆盖或软件清单不完整都会淘汰。
- Stage 04 优先复用远端 `support_path`，且绝不跟随数据集/仓库链接。
- 六类首批出版商适配器具有离线 fixture 和真实小样本测试。
- Stage 06 只处理 Stage 05 幸存论文，不为全部 SI 运行重解析。
- 单篇下载、解析或 Agent 错误不拖垮整个微批次。
- 新增软件后 Stage 03/04/06 缓存可复用，只重跑能力相关阶段。

## 19. 已确认的设计决定

1. Stage 00 将指定数量论文的正文和远端已有 SI 复制到同一论文目录。
2. Stage 02/03 使用正文和 Stage 00 已带入的 SI；Stage 04 对已有 SI 论文跳过。
3. Stage 03 strict 模式复核全部规则候选，只保留纯计算、primary 且无作者实验的论文；
   recall 模式保留旧的边界复核行为。
4. Stage 04 默认只下载 PDF SI；ZIP/CIF/DOCX 后续按实际需要逐类开放。
5. Stage 05 是严格预筛，不宣称最终 `toolbox_covered`，但不允许部分软件覆盖通过。
6. strict 模式没有软件名不进入 Stage 06；新下载 SI 的最终覆盖变化由 Builder 复核。
7. Stage 07 Builder 在所有可用 SI 解析后执行最终工具箱覆盖复核。
8. 第一批官网适配 ACS、RSC、Elsevier、Wiley、Nature 和 MDPI，其他出版商后续按占比补齐。

本方案已经确认，后续实现按 Phase 0-8 推进；未经明确要求不推送 GitHub。
