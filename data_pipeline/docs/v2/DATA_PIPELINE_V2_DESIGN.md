# ResearchChemBench 数据管线 v2 详细设计

状态：设计已进入 v2 基线实现；实现对应关系见 `IMPLEMENTATION_LOG.md`（2026-08-07）。

## 1. 目标与非目标

### 1.1 最终目标

数据管线的最终产物不是“包含某个软件名的论文”，也不是“纯计算化学论文”，而是能够通过
Chemistry MCP 工具箱真实执行、形成新计算证据并被客观评分的 ResearchChemBench 成对任务：

- 自主科研模式；
- 论文复现模式。

同一任务对必须共享科学对象、核心结论、质量门和可比较资源预算，同时控制两种模式的信息披露。

### 1.2 早期筛选目标

Stage 00-04 只负责建立可靠论文证据和排除明确不适用对象：

- 论文和 SI 没有形成可靠绑定；
- 文档无法解析；
- 没有可信计算化学内容；
- 核心工作流明确依赖工具箱不支持的软件；
- 代表性计算明确超过评测资源预算。

Stage 00-04 不负责写任务，不要求判断论文创新性，也不要求作者完全没有实验工作。

### 1.3 非目标

v2 第一版不做以下工作：

- 下载论文引用的任意外部数据集、GitHub 仓库或第三方数据库；
- 根据 LLM 常识声明某个工具箱能力存在；
- 修改或覆盖原始 PDF 和补充材料；
- 把模型调用失败当作科学淘汰；
- 自动发布未经 Gold Run 的任务；
- 在旧运行目录中原地升级结果。

## 2. 总体流程

```text
Stage 00 远端语料选择
    |
    v
Stage 01 论文身份、去重、正式 SI 补齐和论文包冻结
    |
    v
Stage 02 按角色解析、回退解析和确定性质量控制
    |
    v
Stage 03 计算化学内容判断 -------------+
    |                                   | 同一个部署 LLM
    v                                   |
Stage 04 软件/工作流审查、工具箱匹配和成本预筛 ----+
    |
    v
Stage 05 十个方向与完整科研流程判断
    |
    v
Stage 06 自主科研/论文复现双模式 Builder
    |
    v
Stage 07 确定性检查、独立 Judge 和 Gold Run
```

每个阶段以 `paper_id` 为最小失败域。Stage 06 起以 `candidate_id` 和 `task_pair_id` 为失败域。

## 3. 公共数据契约

### 3.1 标识符

| 标识符 | 生成依据 | 稳定性 |
| --- | --- | --- |
| `paper_id` | 规范 DOI；无 DOI 时使用规范标题、年份和主 PDF hash | 同一论文跨运行稳定 |
| `document_id` | `paper_id + document_role + sha256` | 同一文件跨运行稳定 |
| `evidence_id` | `document_id + page/section/span + normalized_text_hash` | 文本表示不变时稳定 |
| `workflow_id` | `paper_id + workflow evidence set hash` | Stage 04 证据不变时稳定 |
| `candidate_id` | `paper_id + direction + scientific question hash` | Stage 05 候选不变时稳定 |
| `task_pair_id` | `candidate_id + builder contract hash` | 构建规范不变时稳定 |

禁止使用批次序号作为唯一身份。批次序号只能用于调度和目录排序。

### 3.2 通用记录头

所有 JSONL 记录包含：

```json
{
  "pipeline_contract": "researchchembench-data-pipeline/v2",
  "record_type": "paper_package",
  "record_schema_version": 1,
  "run_id": "...",
  "paper_id": "paper_...",
  "created_at": "ISO-8601 UTC",
  "producer": {
    "stage": "stage_01",
    "code_commit": "...",
    "config_hash": "..."
  }
}
```

当前代码中的数字 `schema_version: 2` 与本设计的“v2”不是同一概念。实现时必须增加
`pipeline_contract`，不得只依赖一个全局整数。

### 3.3 处理状态与科学状态

所有阶段分别记录：

```text
processing_status = success | retryable_error | permanent_error | skipped
decision_status   = pass | reject | hold | not_applicable
```

`retryable_error/permanent_error` 不得自动转换为 `reject`。`reject_reason` 只能描述科学、能力、
数据完整性或资源原因；基础设施错误写入 `error_code`。

### 3.4 原始证据不可变

- 原始 PDF/SI 只读保存并记录 SHA-256、字节数、来源和获取时间。
- MinerU、GROBID、`pdftotext`、LLM 输出都是派生产物。
- 后续模型引用必须使用 `evidence_id`，并能回映到原始文件、页码或文本范围。
- 不允许用清理后的文本覆盖原始抽取结果。

## 4. Stage 00：远端语料选择

### 4.1 职责

从授权远端数据集中按指定策略选择 N 篇论文，复制正文和远端已正确配置的 SI，并保存选择依据。
Stage 00 不访问出版商网页，不执行文本解析，不进行计算化学判断。

### 4.2 输入

- 数据集名称或远端前缀；
- 只读访问凭据；
- `count`；
- `selection = remote_order | seeded_sample | cursor`；
- `seed/cursor`；
- 历史选择 manifest 排除列表；
- 远端 source record：DOI、标题、期刊、ISSN、正文路径、SI 路径提示。

### 4.3 处理

1. 枚举真实远端对象，不能仅相信元数据字符串。
2. 规范 DOI、标题和文件名。
3. 按选择策略获得论文记录。
4. 原子复制主 PDF。
5. 对远端已经验证存在的 SI 一并复制。
6. 计算 SHA-256、大小、ETag 和相对路径。
7. 单篇复制失败不破坏其他论文；失败项进入重试队列。

### 4.4 输出

```text
stage_00_remote_corpus/
  corpus/<paper_id>/
    main/*
    supplementary/*
    source_record.json
  selected_papers.jsonl
  copy_failures.jsonl
  cursor.json
  stage_summary.json
```

`selected_papers.jsonl` 的核心字段：

```json
{
  "paper_id": "paper_...",
  "source_dataset": "en-paper-hzzj",
  "doi": "10....",
  "title": "...",
  "journal_name": "...",
  "article_url": "...",
  "main_document": {"path": "main/...pdf", "sha256": "..."},
  "copied_supplementary": [],
  "supplementary_source_hints": [],
  "selection": {"strategy": "seeded_sample", "seed": 1, "index": 1},
  "processing_status": "success"
}
```

### 4.5 通过条件

主 PDF 复制成功、hash 可计算且文件签名为有效 PDF。Stage 00 不因为缺少 SI 淘汰论文。

## 5. Stage 01：论文包闭合

### 5.1 职责

Stage 01 在任何语义筛选之前完成：

- 论文身份和版本归一化；
- DOI/标题/主 PDF 的重复关系；
- 正文与 SI 的可靠绑定；
- 缺失正式 SI 的发现和下载；
- 论文包冻结。

补充材料属于原始论文对象，不再是后期增强阶段。

### 5.2 输入

- Stage 00 `selected_papers.jsonl`；
- `corpus/<paper_id>` 中的文件；
- source record 和远端 SI 提示；
- 出版商适配器配置；
- 允许下载的正式 SI 类型和大小限制；
- 网络重试、代理和 host 并发配置。

### 5.3 身份和去重顺序

1. 校验主 PDF 文件签名、页数、hash 和基本元数据。
2. 规范 DOI；DOI 相同视为同一 paper group。
3. DOI 缺失时，以规范标题、年份、作者和内容近重复判断。
4. 区分 publisher version、accepted manuscript 和 preprint。
5. 选择 canonical main document，其余版本保留但不进入默认解析。
6. 在 canonical paper group 上执行 SI 获取，避免重复网络请求。

### 5.4 SI 获取范围

只获取论文正式补充材料：

- Stage 00 已复制的远端 SI；
- 已验证但复制失败的远端对象；
- 出版商 article landing page 或正式附件 API 返回的 SI；
- 与 DOI、文章 ID 或 landing page 明确绑定的正式附件。

v2 第一版不下载正文中出现的 GitHub、Zenodo、OSF、DataCite 或普通 URL。可以记录线索，
但不进入下载队列。

### 5.5 正文与 SI 映射证据

每个附件至少保存一种强证据：

- 出版商 landing page 的 attachment relation；
- 正式 API 的 article identifier；
- 远端对象表中经列举验证的 DOI 文件名；
- SI 首页标题/DOI 与正文一致。

仅凭相似文件名不能冻结绑定。下载后校验 MIME、PDF 签名、大小和 hash，HTML 错误页不得伪装为 PDF。

### 5.6 论文包状态

```text
complete_with_si
complete_confirmed_no_si
incomplete_si_unavailable
identity_conflict
retryable_acquisition_error
invalid_main_document
```

`complete_confirmed_no_si` 必须保存检查来源、时间和证据；“没有下载到”不等于“确认不存在”。

### 5.7 输出

```text
stage_01_paper_package/
  packages/<paper_id>/
    main/*
    supplementary/*
    paper_identity.json
    package_manifest.json
    acquisition_attempts.jsonl
  papers.jsonl
  documents.jsonl
  duplicate_groups.jsonl
  acquisition_attempts.jsonl
  rejected.jsonl
  stage_summary.json
```

`package_manifest.json` 包含所有原始文件的角色、hash、来源、映射证据和 canonical 状态。

### 5.8 通过条件

仅以下状态进入 Stage 02：

- `complete_with_si`；
- `complete_confirmed_no_si`。

网络错误先按 host 策略重试；超过重试上限进入 `hold/permanent_error`，不得记录为论文科学淘汰。

## 6. Stage 02：低成本文档标准化与质量控制

### 6.1 职责

对 Stage 01 论文包中的 canonical 正文和全部 canonical SI 生成足以支持 Stage 03/04 前筛的统一、
可定位文本，同时完成确定性质量控制。Stage 02 不做计算化学语义筛选，也不执行 MinerU 深解析。

### 6.2 输入

- Stage 01 `papers.jsonl` 和 `documents.jsonl`；
- frozen package 中的原始 PDF/SI；
- GROBID 和 Poppler 的版本及配置；
- 文档质量阈值；
- parser cache。

### 6.3 解析路由

PDF 使用统一的低成本路由：

```text
canonical main paper
  -> GROBID full text
  -> pdftotext -layout
  -> parse_failed

canonical supplementary PDF
  -> GROBID full text
  -> pdftotext -layout
  -> parse_failed

manifest 中的非 PDF SI
  -> 对应结构化 parser / text extractor
  -> parse_failed
```

全部 canonical SI 的文本和证据都必须进入 Stage 03/04。GROBID 请求失败、TEI 无法解析或抽取结果未
通过字符/可读性/重复度质量门时，执行一次 `pdftotext -layout` 回退。回退仍失败时按文档隔离并记录
`parse_failed`。不在低成本筛选前对数万页 PDF 做图片、公式和版面深解析。

### 6.4 低成本规范化结果

每个文档保留 GROBID TEI、抽取文本、规范化 Markdown、内容块、请求状态、回退原因和质量报告。
Stage02 的块主要服务自然语言前筛，不承诺可靠还原公式、复杂化学排版、图片或表格；这些要求由
Stage04 通过后的 MinerU 深解析承担。

统一表示中的每个内容块至少包含：

```json
{
  "block_id": "block_...",
  "document_id": "doc_...",
  "page": 3,
  "section_path": ["Methods", "Computational details"],
  "block_type": "paragraph | table | equation | figure_caption | list",
  "text": "...",
  "bbox": [0, 0, 100, 100],
  "source_parser": "grobid | pdftotext",
  "source_ref": "content_list_v2:123"
}
```

### 6.5 统一文本要求

下游模型使用 `normalized_document.md` 和 `content_blocks.jsonl`，但原始 parser 输出全部保留。

期望结果：

- 正文与 SI 分开标识，不拼接成无法定位的大字符串；
- 标题、摘要、章节、表格、公式和图注边界可识别；
- 参考文献与正文分区；
- 每段能回映 `document_id/page/section/block_id`；
- 保留化学式、上下标、单位、电荷、自旋和数值；
- 不用 LLM 改写科学内容；
- 明确记录截断、缺页、OCR 和布局风险。

### 6.6 确定性质量指标

每个 parser attempt 和最终选中表示均计算：

- `page_coverage_ratio`；
- `readable_character_ratio`；
- `characters_per_page`；
- `replacement_character_ratio`；
- `repeated_line_ratio`；
- `empty_page_ratio`；
- `section_recovery`；
- `table_caption_count/figure_caption_count/equation_count`；
- `title_doi_consistency`；
- `truncated`；
- `needs_ocr`。

初始建议阈值仅作为配置默认值，必须用人工样本校准：

```text
page_coverage_ratio >= 0.95
readable_character_ratio >= 0.90
replacement_character_ratio <= 0.01
empty_page_ratio <= 0.10
truncated = false
```

字符数不能单独作为硬门，因为表格型 SI 可能文本很少。正文和 SI 使用独立阈值。

### 6.7 文档类型规则

出版商或 Crossref 明确标记为 Editorial、Correction、Retraction、Masthead 或 Review 时，可以
确定性淘汰。元数据缺失时不允许模型在 Stage 02 猜测原创性。

### 6.8 输出

```text
stage_02_document_normalization/
  documents.jsonl
  paper_bundles.jsonl
  parser_attempts.jsonl
  quality_reports.jsonl
  normalized/<document_id>/
    normalized_document.md
    content_blocks.jsonl
    metadata.json
  raw/grobid/<document_id>/...
  raw/pdftotext/<document_id>/...
  rejected.jsonl
  stage_summary.json
```

### 6.9 通过条件

- canonical 正文必须解析成功并通过正文质量门；
- `complete_with_si` 的论文必须成功解析全部已知、规范化后的正式 SI；
- 任意一个已知 SI 解析失败都会标记 `partial_si_parse` 或 `supplementary_parse_ok=false`，整篇论文在
  Stage 02 淘汰，不得进入 Stage 03；
- 所有处理错误按文档隔离。

## 7. Stage 03：计算化学内容筛选

### 7.1 职责边界

Stage 03 回答：完整论文包中是否存在可信、完整且作为主要科学工作的计算化学流程，并按当前严格策略
确认它是否为纯计算原创研究。

它不回答：

- 软件是否被工具箱覆盖；
- 计算是否能构造成 Benchmark 任务；
- 任务是否有完整输入和 ground truth。

### 7.2 输入

- Stage 02 `paper_bundles.jsonl`；
- 正文和全部 SI 的 `content_blocks.jsonl`；
- 方法、动作、结果和软件词典；
- 排除章节和负面上下文规则；
- 共享 screening LLM 服务配置；
- Stage 03 prompt/schema 版本。

### 7.3 处理

1. 检查 Stage02 正文和全部已知 SI 均解析成功，部分 SI 成功的旧记录不得进入。
2. 读取正文和全部 SI 的规范化文本块，删除大段原子坐标，按默认 9000 UTF-8 bytes 分块。
3. 使用共享部署模型分别抽取当前作者的计算证据、实体实验反证和背景引用。
4. 确定性检查 quote 是否逐字存在、`evidence_id` 是否可回映、作者归因及实验语义是否有效。
5. 使用同一模型的独立 reduce 调用合成论文级结论。
6. 确定性执行纯计算门控；截断响应重试，未验证证据不能支持通过或淘汰。

### 7.4 决策

```text
computational_content_confirmed
not_pure_computational
computational_content_not_found
background_only
uncertain
processing_failed
```

通过条件为 `computational_content_confirmed`。`uncertain` 默认重试一次，并可升级输入范围；仍不确定时
进入 hold，不伪装成 `not_found`。

### 7.5 输出

```text
stage_03_computational_content/
  evidence_packets.jsonl
  chunk_reviews.jsonl
  decisions.jsonl
  llm_cache/
  rejected.jsonl
  held.jsonl
  stage_summary.json
```

论文级结果至少包含 article role、computation role、study mode、完整工作流、method families、计算
actions、软件/资源线索、计算和作者实验引用、冲突证据、模型审计和路由状态。当前准确的数据流、prompt
和 schema 见 `STAGE03_PROMPT_AND_DATA_FLOW.md`。

## 8. Stage 04：软件覆盖与资源预筛

### 8.1 职责

Stage 04 对 Stage 03 通过论文建立论文级计算工作流清单，审查软件角色，使用冻结工具箱快照做
确定性覆盖判断，并对代表性成本做初步筛选。完成门控后，仅对通过论文执行 MinerU 深度解析，
为 Stage05-07 生成公式、表格和版面质量更高的新证据集。

Stage 04 不选择最终科学问题，也不生成任务。

### 8.2 输入

- Stage 02 完整规范化文本；
- Stage 03 计算证据和线索；
- Softcite 输出；
- 软件别名和角色规则；
- `toolbox_capabilities.json` 中的活动软件 backend、别名和 catalog hash；
- 资源预算；
- Stage 04 prompt/schema 版本；
- 与 Stage 03 共用的 LLM endpoint。

### 8.3 三层处理

#### A. 高召回抽取

- Softcite 软件 mention；
- 工具箱别名精确/大小写/版本规范化；
- `using/implemented with/calculations performed with` 等执行上下文；
- 方法、动作、输入输出和依赖词；
- CPU/GPU/内存/wall time 和体系规模表达；
- 参考文献、仪器软件和普通办公软件排除规则。

#### B. LLM 审查

共享部署模型负责：

- 补充 Softcite 漏掉的软件；
- 区分实际使用、背景引用和歧义 mention；
- 区分 `core_compute`、`required_preprocessing`、`required_analysis`、
  `optional_auxiliary`、`visualization`、`instrumentation`；
- 将软件绑定到工作流步骤；
- 判断清单是否完整；
- 抽取报告资源和复杂度事实；
- 引用原文证据。

LLM 不负责声明工具箱支持，也不负责最终数值比较。

#### C. 确定性判定

程序依据冻结快照检查：

- normalized backend 是否存在；
- 所有核心和必要软件是否覆盖；
- 软件清单是否存在未命名实现或未分类的实际执行程序；
- 资源事实与配置预算的关系。

删除的软件不会出现在能力快照中，LLM 不能把它们重新加入可用范围。

### 8.4 三层工具箱与 Stage04 判定边界

工具箱可以通过三层完成任务：

```text
预设通用 Action
依据软件文档直接调用活动 backend 对应的原生软件
编写任务特定的 Python 程序完成辅助处理
```

因此 Stage04 的软件覆盖只按“论文必需的命名软件是否存在于活动 backend catalog”判定。预设 Action
缺失、adapter 参数范围较窄、`local_installation_status=not_evaluated`，以及方法未出现在 Action schema
中，都不能在 Stage04 淘汰论文。原生调用方案、Python 辅助代码和实际执行可行性由 Builder/Judge 在
后续阶段结合软件文档和最终任务验证。

第三层 Python 只允许实现通用数据处理或任务特定逻辑，不能把明确缺失的必要程序、插件或闭源自研
代码伪装成已覆盖。例如 VASP 存在时 HSE 仍属于软件覆盖；Molpro、TURBOMOLE 或 VASPsol 不在 catalog
时仍属于 `core_software_uncovered`。

### 8.5 资源事实

至少抽取：

- CPU cores、GPU 数量/型号、内存、单 job wall time；
- core-hours、GPU-hours 和总 job 数；
- 原子数、电子数、体系数、构象数、结构数；
- 方法层级、基组、赝势、周期性、k 点和 cutoff；
- 优化、频率、TS、IRC、MD 步数、时间步长、窗口数和轨迹长度；
- 高通量规模和采样规模；
- 原文未报告但可以从体系/方法得到的复杂度边界。

物理实验时长不得误判为计算 wall time。每条事实记录 `scope = single_job | aggregate_study |
physical_experiment | unknown`。

### 8.6 资源事实只作为下游元数据

```text
within_preliminary_budget
exceeds_minimum_budget
cost_unconfirmed
```

Stage04 可以抽取上述初步资源事实并记录 `resource_profile`，但这些状态不参与 Stage04 的 pass/reject。
`cost_unconfirmed` 或论文总高通量成本不能在本阶段挡住软件已覆盖的论文。Stage05、Builder/Judge 和
Gold Run 根据选定的具体任务子流程重新评估实际成本。

#### D. 通过后 MinerU 深度解析

- 只调度软件覆盖通过的论文，不解析 Stage04 已淘汰论文；
- 正文和现有 PDF SI 全部执行 MinerU，非 PDF SI 复用 Stage02 的结构化解析结果；
- MinerU 原始输出、Markdown、page-level content list、图片、公式、表格、bbox、命令和日志全部保留；
- 任一必需 PDF 深解析失败或正文没有成功的 MinerU 表示时，论文改记 `deep_parse_failed`；
- GROBID 证据 ID 与 MinerU 证据 ID 属于不同命名空间。Stage04 粗筛证据只用于审计，Stage05-07
  只能引用 `deep_normalization/documents.jsonl` 指向的新 content blocks。

### 8.7 通过条件

- Stage 03 已确认计算化学内容；
- 软件清单审查完整；
- 至少一条主要计算工作流被识别；
- 该工作流的全部核心和必要命名软件存在于活动 backend catalog；
- 不存在未分类的实际执行软件；
- 未明确超过资源预算；
- LLM 引用和 schema 校验通过。
- 正文及论文包中必需的 PDF 文档通过 MinerU 深度解析质量门。

### 8.8 输出

```text
stage_04_toolbox_resource_gate/
  rule_mentions.jsonl
  softcite_mentions.jsonl
  llm_reviews.jsonl
  workflow_inventories.jsonl
  software_mappings.jsonl
  resource_profiles.jsonl
  decisions.jsonl
  deep_normalization/
    documents.jsonl
    parser_attempts.jsonl
    failed.jsonl
    normalized/<document_id>/
    raw/mineru/<document_id>/
  llm_cache/
  rejected.jsonl
  held.jsonl
  stage_summary.json
```

最终决策建议枚举：

```text
software_covered
software_inventory_unconfirmed
core_software_uncovered
processing_failed
```

## 9. Stage 03/04 共用模型服务

### 9.1 生命周期

1. 整次管线开始时由 runtime manager 检查或启动一个 screening LLM worker。
2. worker 启动一次，Stage 03 和 Stage 04 的所有微批次复用。
3. 两阶段使用相同 `base_url/model/api_key`，但独立并发 semaphore。
4. Stage 05 以后不依赖该 worker时可以释放；默认在整次任务 finally 中停止，保证异常清理。
5. 外部 API 模式不负责停止服务，只关闭本地 client。

### 9.2 推荐模型

本地默认模型为 `Qwen3-30B-A3B-Instruct-2507`，通过 vLLM 和 OpenAI-compatible gateway 部署。
Stage 03/04 使用非 thinking、低温度和结构化 JSON。模型名称和 endpoint 必须配置化，不写死在阶段代码中。

### 9.3 隔离

```text
cache/stage03/<request_hash>.json
cache/stage04/<request_hash>.json
```

request hash 至少包括：输入 evidence hashes、system/user prompt、schema、模型完整名称、温度、seed、
最大输出 token 和工具箱 catalog hash（Stage 04）。Stage 03 不应因工具箱更新失效。

### 9.4 并发

- 一个服务可以同时承载 Stage 03/04；
- `stage03.max_inflight` 和 `stage04.max_inflight` 分开配置；
- 为避免 Stage 04 长响应饿死 Stage 03，可使用加权队列或预留并发槽；
- 单篇失败只重试该调用；
- 服务健康失败暂停取新任务，恢复后重领队列；
- 不在每个微批次、每个阶段反复创建和停止 rlaunch worker。

## 10. Stage 05：Benchmark 适用性筛选

### 10.1 职责

使用强推理模型判断一篇已通过软件/成本门控的论文是否包含符合十个方向的完整计算化学科研流程，
并输出 0-3 个候选。Stage 05 不写最终任务文件。

### 10.2 输入

- Stage 02 正文和全部 SI 的结构化文本；
- Stage 03 计算化学证据；
- Stage 04 工作流、软件映射、能力和资源证据；
- 十个任务方向 taxonomy；
- Benchmark 最低科学意义和评分要求；
- frozen toolbox/runtime snapshot；
- 强模型配置，例如 `deepseek-v4-pro`。

### 10.3 候选要求

每个候选必须：

1. 对应一个明确科学问题；
2. 属于十个方向之一；
3. 包含至少三个相互依赖的计算阶段；
4. 有至少一个科学验证门；
5. 有至少一个机器可评分的结果；
6. 有可获得的起始输入或可由合法公开信息确定性构造的输入；
7. 公开输入与隐藏目标可分离；
8. 工作流软件与 Stage 04 覆盖结论一致；
9. 代表性成本可控；
10. 不是读取已有输出、抄录数值、重绘图或单次平凡计算。

### 10.4 十个方向

枚举固定为：

```text
reaction_mechanism_selectivity
conformer_thermochemistry_property_calibration
periodic_surface_adsorption_bonding
electron_density_topology_bonding
reaction_kinetics_master_equation_microkinetics
excited_state_spectroscopy_photochemistry
high_pressure_phase_stability
phonons_vibrations_thermal_transport
molecular_dynamics_free_energy
descriptor_discovery_catalyst_design
```

### 10.5 Ground truth 等级

```text
A = 作者原始输出/source data
B = SI 中机器可读的完整结果
C = 固定协议重算且经独立验证
D = 正文/SI 文字、表格或图片数字化
```

A/B 可直接作为强真值；C 需要 Gold Run；D 只能作为弱目标，不能默认承担高精度数值评分。

### 10.6 输出

```text
stage_05_benchmark_suitability/
  requests/<paper_id>.json
  responses/<paper_id>.json
  candidates.jsonl
  abstentions.jsonl
  evidence_validation.jsonl
  stage_summary.json
```

论文可以 `pass` 但产生多个候选，也可以结构化 abstain：

```text
no_supported_direction
incomplete_scientific_question
insufficient_workflow_depth
missing_validation_gate
missing_input
missing_parameters
missing_ground_truth
not_machine_scorable
resource_limit
not_significant
processing_failed
```

## 11. Stage 06：双模式任务构建

### 11.1 职责

对 Stage 05 的每个候选构建共享科学记录，以及相互隔离的信息披露版本：

- autonomous research；
- paper reproduction。

建议使用当前最强可用 Builder 模型，例如配置的 `gpt5.6`，但模型名必须配置化。

### 11.2 输入

- 单个 Stage 05 candidate；
- candidate 引用的原始证据和必要资产；
- frozen toolbox/runtime snapshot；
- 公开/隐藏信息策略；
- 任务、隐藏真值和 Rubric schema；
- 评测预算。

### 11.3 构建隔离

1. 先冻结共享 `scientific_record` 和 `hidden_reference`。
2. 自主模式 Builder 只获得科学问题、起始输入和允许公开的实验条件，不获得论文路线和答案。
3. 复现模式 Builder 获得协议、软件、参数和验证要求，但不获得作者答案性结果。
4. 两次 Builder 使用独立 workspace 和会话。
5. Builder 只允许引用 Stage 05 已验证 evidence IDs，不允许自行搜索或发明文件。

### 11.4 输出

```text
stage_06_task_builder/<task_pair_id>/
  shared/scientific_record.json
  shared/hidden_reference.json
  autonomous/task_info.json
  autonomous/task.md
  autonomous/data/benchmark_data/...
  reproduction/task_info.json
  reproduction/task.md
  reproduction/data/benchmark_data/...
  target_study/ground_truth.json
  scoring/rubric.json
  evidence_map.json
  builder_audit.json
```

Builder 可返回 `candidate_ready` 或结构化 `abstain`。一次论文可以产生多个 task pair，但每个
`candidate_id` 默认只构建一对。

### 11.5 确定性构建校验

- public asset ID 和文件 hash 存在；
- allowed backend/action 在 frozen snapshot 中；
- Rubric 总分为 100；
- 两种模式共享科学结论；
- 自主模式不泄漏方法路线；
- 复现模式不泄漏目标结果；
- hidden result 不在公开文本中出现；
- 任务至少要求三个依赖步骤和一个验证门；
- 公开输入不包含答案性输出归档。

## 12. Stage 07：独立审核与 Gold Run

### 12.1 输入

- Stage 06 完整 task pair；
- 原始论文/SI 和 evidence map；
- frozen toolbox/runtime snapshot；
- 独立 Judge prompt/schema；
- 干净评测沙箱配置。

### 12.2 三层审核

#### A. 确定性审计

检查 schema、文件、hash、backend/action、Rubric、公开/隐藏边界、单位和明显泄漏。

#### B. 独立 LLM Judge

Judge 不读取 Builder 的会话、草稿或推理轨迹。检查：

- 论文忠实性；
- 科学问题和工作流深度；
- 输入充分性；
- 工具箱真实支持；
- 两种模式披露是否正确；
- ground truth、容差和评分质量；
- 资源可行性。

输出 `pass | revise | reject | judge_error`。`revise` 只生成修改建议；是否允许自动回到 Builder 由
运行配置决定，默认不自动循环。

#### C. Gold Run

仅 Judge pass 的任务进入干净沙箱：

- 验证公开输入可读；
- 验证至少一条参考路线真实执行；
- 记录实际 CPU/GPU、内存和 wall time；
- 校准数值容差和 evidence gates；
- 确认不会访问隐藏信息或外部动态资源。

### 12.3 输出

```text
stage_07_task_judge/<task_pair_id>/
  deterministic_audit.json
  judge_request.json
  judge_response.json
  gold_run/
    manifest.json
    execution_trace.jsonl
    artifacts/...
    resource_report.json
  release_decision.json
```

只有 `judge=pass` 且 `gold_run=pass` 才标记 `benchmark_ready=true`。

## 13. LLM 使用和可复现性

每次模型调用保存：

- provider、base URL 的非敏感标识和完整模型返回名；
- system/user prompt 原文和 prompt version；
- JSON schema；
- temperature、seed、max tokens、thinking 配置；
- 原始响应、解析响应和响应 hash；
- token usage、延迟、重试和 cache hit；
- 输入 evidence hashes；
- 证据回映报告。

严格复现依赖缓存回放。远程模型的新调用只要求结构和判定在验收容差内一致，不要求逐 token 相同。

## 14. 微批次、并发和服务生命周期

### 14.1 调度模型

```text
1000 papers
  -> 100 microbatches x 10 papers
  -> at most N active microbatches
  -> each microbatch follows Stage 00/01/02/... in order
  -> stage-specific semaphores control shared services
```

一个微批次完成当前阶段后立即进入下一阶段，不等待同一轮所有论文完成。Stage 00/01 的语料级操作可在
微批次调度前完成，也可以按冻结 paper package 分批提交。

### 14.2 建议并发资源

| 阶段 | 并发控制 |
| --- | --- |
| Stage 00 | 远端存储 worker + host 限速 |
| Stage 01 | publisher host semaphore，按 DOI 缓存 |
| Stage 02 | GROBID worker 数和 `pdftotext` 回退 worker 数分别限制 |
| Stage 03 | shared LLM `stage03.max_inflight` |
| Stage 04 | Softcite 实例池 + shared LLM `stage04.max_inflight` + 通过后 MinerU 微批并发 |
| Stage 05 | 强模型 API 并发，通常低于 Stage 03/04 |
| Stage 06 | Builder Agent 并发，按 workspace 隔离 |
| Stage 07 | Judge/Gold Run 并发，受评测沙箱资源限制 |

### 14.3 沙箱和模型生命周期

- CPU/内存沙箱在整次任务开始前创建，Stage 00-07 共用，任务 finally 中关闭；
- GROBID、Softcite 等服务启动一次并复用；
- Stage 03/04 的 rlaunch LLM worker 启动一次并复用；
- 不在阶段边界反复启动和停止同一服务；
- 模型 worker state 文件放在运行目录，权限为 0600；
- 异常退出后下次启动先执行 stale worker audit，再决定复用或清理。

## 15. 缓存键

| 阶段 | 缓存键主要内容 |
| --- | --- |
| Stage 00 | dataset version + selection config + source record + ETag |
| Stage 01 | paper identity + remote inventory + adapter version + attachment metadata |
| Stage 02 | PDF hash + GROBID/Poppler version + parser config +低成本质量策略 |
| Stage 03 | selected text/block hashes + prompt/schema + model config + evidence rules |
| Stage 04 | Stage 03 evidence + Softcite/rules + prompt/model + capability/runtime hashes + resource policy + MinerU config/model hash |
| Stage 05 | complete evidence bundle + taxonomy + prompt/schema + strong model config |
| Stage 06 | candidate + asset hashes + disclosure policy + toolbox/runtime + Builder config |
| Stage 07 | task pair hash + Judge config + Gold Run environment hash |

新增工具箱软件只使 Stage 04 及后续能力相关缓存失效，不应使 Stage 00-03 失效。

## 16. 审计和统计

每个阶段必须报告：

- 输入、成功、拒绝、hold、处理错误和重试数；
- stage pass rate 和 cumulative pass rate；
- 拒绝原因分布；
- 每种 parser/model 的调用数、时间和 token；
- 每个模型/schema 失败率；
- 每个出版商的 SI 成功率；
- 每种文档角色的解析质量；
- 每个软件/backend/任务方向的覆盖分布。

最终效果指标：

- 每 1000 篇得到的 Stage 05 候选数；
- 每 1000 篇得到的 task pair 数；
- Judge pass 数；
- Gold Run pass 数；
- 每个 benchmark-ready task 的筛选和构建成本；
- 十个方向和 backend 的分布；
- 人工审查的 Stage 03 recall、Stage 04 软件角色 precision 和 Stage 05 candidate precision。

## 17. 安全与数据边界

- API key 只从环境变量读取，不写入 prompt、日志或缓存；
- 下载附件不执行；
- archive 解压必须防路径穿越和压缩炸弹；
- Builder/Judge 工作区只暴露 manifest 允许的文件；
- 自主模式不暴露论文计算路线或答案；
- 复现模式不暴露作者最终答案；
- LLM 无网络工具，Stage 05-07 只读取冻结证据；
- 原始运行、prompt、工具箱和任务均保存版本与 hash。

## 18. 验收标准

### Stage 00/01

- `count=N` 时形成 N 个可审计选择记录；
- 正文和 SI 映射有强证据；
- “确认无 SI”和“未下载到 SI”严格区分；
- 旧 Stage 04 下载样本能在新 Stage 01 重放。

### Stage 02

- Stage02 不调用 MinerU，所有 PDF 首选 GROBID；
- 每份文档保留全部 parser attempts；
- GROBID 错误或低质量结果能自动回退到 `pdftotext`；
- 文本块可以回映页码和原始 PDF；
- 已知低质量 SI 不再被“服务成功”掩盖。

### Stage 03

- prompt 不包含 pure、no experiments 或 originality 硬门；
- 规则 reject 不会绕过模型；
- 引用无法回映时进入 uncertain/hold；
- 标注集上报告计算化学内容 recall 和 background-only 假阳性率。

### Stage 04

- Softcite 漏掉的软件可由 LLM 补充；
- LLM 不能添加工具箱能力；
- 核心、必要、辅助、可视化和背景软件有独立测试；
- 单篇 LLM/schema 错误不会拖垮批次；
- 资源范围、上下界、物理实验时长和 aggregate cost 有测试；
- 当前 catalog 与 runtime 状态不会混淆。
- 只有门控通过论文进入 MinerU 队列，深解析失败不会进入 Stage05；
- Stage05 引用的是 MinerU 新 evidence IDs，不会把 GROBID evidence IDs 当作深解析证据。

### Stage 05-07

- 候选至少三个依赖阶段、一个验证门和一个机器可评分结果；
- 两种模式的信息披露通过确定性检查；
- Builder 与 Judge 完全隔离；
- Gold Run 不通过的任务不能标记 benchmark ready。
