# ResearchChemBench 数据管线 Stage 05-07 设计方案

> 状态：方案草案，等待确认后再修改代码。
>
> 编写日期：2026-08-03。
>
> 本文只重新设计 Stage 05、Stage 06 和 Stage 07。Stage 01-04 保持当前实现不变。

## 1. 设计结论

后半段数据管线收敛为三个阶段：

```text
Stage 01-04：保持不变
        |
        v
Stage 05：有边界的资产发现、下载、溯源与增量解析
        |
        v
Stage 06：Builder Agent 构建候选计算化学任务
        |
        v
Stage 07：Judge Agent 独立审计候选任务
        |
        v
数据管线结束
```

主要调整如下：

1. 原本分离的资产搜索和 MinerU 解析合并为一个顶层阶段，但内部仍保留“发现、下载、解析、再发现”的职责边界。
2. Stage 05 最多执行三轮。新文件下载完成后立即进入解析队列，不等待整轮下载结束。
3. 每项资产必须保留原始文件、结构化 JSON，以及供智能体阅读的 Markdown/TXT；无法文本化的科学二进制文件也必须保留。
4. `asset_manifest.jsonl` 是 Stage 05 的核心产物和后续阶段唯一可信的资产索引。
5. Stage 06 使用一个 Builder Agent 构建候选任务，并在 Agent 输出后执行确定性程序校验。
6. Stage 07 使用一个独立 Judge Agent 审计任务，不再使用多模型 API 投票。
7. 当前版本不实现 Builder 和 Judge 之间的自动循环修订。Judge 输出 `revise` 时只保存问题和修改建议，然后结束数据管线。
8. 人工审核、正式数据集发布和版本发布不再作为数据管线阶段。

## 2. 总体设计原则

### 2.1 阶段职责单一

- Stage 05 只负责尽可能完整、可追溯且有边界地收集和解析研究资产，不判断任务是否足够好。
- Stage 06 只负责根据已有证据构建一个可评估的候选任务，不负责最终批准。
- Stage 07 只负责审计候选任务，不直接改写 Builder 的结果。

### 2.2 有限而非穷尽

资产搜索无法证明“已经找到全部文件”。Stage 05 的目标是：

- 覆盖论文明确声明和主要学术仓库中的高价值资产。
- 在固定轮次、深度、时间、文件数和容量预算内递归发现。
- 对所有未解决线索进行记录，而不是无限搜索或悄悄忽略。

### 2.3 原始资产不可丢失

解析产物不能替代原始文件。PDF、压缩包、结构文件、轨迹、波函数、检查点、输入文件和输出文件均保留原始字节，并计算哈希。

### 2.4 决策和来源可审计

任何资产和任务都必须能够回答：

- 从哪里发现。
- 由哪条论文证据或哪个外部 API 关联到本文。
- 下载的是哪个版本。
- 原始 URL、最终 URL、时间、许可证和哈希是什么。
- 经历了哪些解析器，解析是否成功。
- Builder 和 Judge 使用了哪些证据。

### 2.5 基础设施失败与论文结果分离

- 核心服务无法启动、配置错误、清单损坏等基础设施错误应停止对应阶段。
- 单个链接失效、单个受限附件、单个文件无法解析属于论文级结果，记录后继续处理其他资产。
- Builder/Judge 模型调用失败属于阶段基础设施错误，不应伪装为 `reject`。

## 3. Stage 05：有边界的资产发现、下载、溯源与增量解析

### 3.1 阶段目标

以通过 Stage 04 的正式论文为入口，收集论文计算部分涉及的正文、补充材料、代码、输入输出、结构、数据表、轨迹、配置和仓库快照，并将其转换为可供 Builder Agent 使用的统一资产集合。

Stage 05 不负责：

- 判断论文是否可完全复现。
- 判断资产是否足够构建任务。
- 根据缺少文件淘汰论文。
- 执行下载到的脚本或二进制程序。
- 自动绕过登录、付费墙、验证码或访问控制。

### 3.2 输入

每篇论文至少接收：

```text
paper_id
source_pdf_path
doi
grobid_tei_path
grobid_structured_json
title
authors
publication_year
stage03_software_evidence
stage04_resource_result
```

Stage 02 的 GROBID TEI、正文文本和论文 DOI 是首轮线索来源。正式论文 PDF 也在 Stage 05 开始时进入 MinerU 深度解析队列。

### 3.3 三轮有限循环

Stage 05 最多执行三轮发现。每轮采用稳定的 frontier：本轮产生的新线索进入下一轮，避免同一轮不断扩张导致边界失效。

```text
初始化：论文 DOI + GROBID TEI + 正文 PDF
   |
   v
Round 1：论文明确链接、出版社附件、Availability 声明
   |      下载完成即解析；解析得到的新线索写入下一轮 frontier
   v
Round 2：外部关系图、数据仓库、代码仓库和已下载附件中的线索
   |      下载完成即解析；解析得到的新线索写入下一轮 frontier
   v
Round 3：递归压缩包、README、CITATION、脚本和配置中的剩余线索
   |
   v
输出资产清单、未解决线索和阶段状态
```

提前停止条件：

- 本轮没有新增规范化线索，也没有新增资产。
- 已达到任一全局预算。
- 所有队列均为空。

`max_rounds=3` 和 `max_archive_depth=3` 是两个独立限制：前者限制网络发现轮次，后者限制嵌套压缩包展开深度。

### 3.4 每轮的主要任务

#### Round 1：直接证据优先

1. 从 GROBID TEI、MinerU 文本和结构化章节提取 DOI、HTTP/HTTPS URL、代码仓库地址、数据库编号、文件名和压缩包名。
2. 重点解析 Data Availability、Code Availability 和 Supplementary Information 声明。
3. 查询 DOI 落地页和出版社公开元数据。
4. 获取出版社直接附件和论文明确给出的下载链接。
5. 将正文 PDF 和新发现 PDF 立即提交 MinerU。

#### Round 2：关系和仓库发现

1. 根据论文 DOI 查询 Crossref、DataCite 和 OpenAlex 的关联标识符及关系。
2. 使用论文标题、DOI、作者、明确软件名称和文件名生成受控 GitHub 搜索查询。
3. 对候选 GitHub 仓库计算关联分数，只有超过阈值的仓库才下载或克隆。
4. 查询 Zenodo、OSF、Dataverse 等已识别仓库记录并下载文件。
5. 扫描 Round 1 新文件中的 DOI、URL、仓库地址和文件名。

#### Round 3：递归补全

1. 扫描 README、CITATION、LICENSE、环境文件、工作流、脚本和配置中的外部链接。
2. 安全展开新下载压缩包并将子文件登记为独立资产。
3. 根据尚未解决的高置信度文件名或仓库标识执行最后一轮搜索。
4. 对已失效且高置信度的公开 URL，可选查询 Wayback Machine 快照。
5. Round 3 发现但因轮次上限未继续追踪的线索写入 `unresolved_clues.jsonl`。

### 3.5 并发执行模型

Stage 05 不是“全部下载后再统一解析”，而是由四类有界队列组成：

```text
discovery_queue -> download_queue -> parse_queue -> clue_queue
```

- 发现器负责生成候选线索，不直接写最终文件。
- 下载器完成校验后立即登记资产并提交解析队列。
- 解析器按文件类型路由；PDF 可单独限制 MinerU 并发数。
- 线索提取器从解析结果生成下一轮 frontier。
- 同一 `asset_id` 或相同 SHA-256 的资产只解析一次。
- 每次状态变化追加写入事件日志，进程异常后可从清单恢复。

推荐的初始并发配置：

```yaml
network_workers: 8
metadata_workers: 4
mineru_workers: 1
light_parser_workers: 4
archive_workers: 2
```

MinerU 并发数应根据 GPU 显存和当前服务模式单独配置，不能随网络并发一起放大。

### 3.6 线索类型和关系置信度

所有线索必须保存 `relation_type`、`evidence` 和 `confidence`。

| 等级 | 线索来源 | 默认置信度 |
| --- | --- | --- |
| A | 出版社附件、论文正文中的明确 URL/DOI、明确 Availability 声明 | 高 |
| B | DataCite relatedIdentifier、Zenodo/Dataverse/OSF 记录中的明确论文 DOI | 高 |
| C | 仓库 README/CITATION 中的论文 DOI 或完整标题 | 中高 |
| D | 基于标题、作者和软件名的搜索推断 | 中低 |
| E | 只有相似文件名、模糊标题或 Wayback 快照 | 低 |

低置信度线索可以登记，但默认不自动下载大文件。GitHub 搜索结果不得仅因名称相似就认定为论文资产。

### 3.7 下载、版本和去重

下载管理器统一负责：

- URL 规范化和重定向链记录。
- 超时、重试、速率限制和 `Retry-After`。
- Content-Type 与实际文件签名校验。
- 流式下载和大小上限。
- SHA-256 计算。
- ETag、Last-Modified、仓库 commit、release/tag 和 DOI 版本记录。
- URL 去重、内容哈希去重和仓库身份去重。
- 断点恢复和失败原因记录。

内容相同但来源不同的文件只存储一份原始对象，清单保留多条来源关系。不同版本即使文件名相同也不得覆盖。

### 3.8 安全展开和文件处理

压缩包处理必须防止：

- `../` 路径穿越。
- 绝对路径写入。
- 符号链接和硬链接逃逸。
- 压缩炸弹。
- 超深目录和超长文件名。
- 单文件或展开总量超过预算。

下载内容默认只读，不执行仓库脚本、不加载不可信 pickle、不运行宏、不调用附件中的安装脚本。下载器还应禁止访问回环地址、私网地址和非允许协议，避免由论文中的恶意链接触发 SSRF。

### 3.9 解析路由

| 文件类型 | 处理方式 | 必须保留 |
| --- | --- | --- |
| PDF | MinerU 深度解析；失败时保留错误，并可用 GROBID/文本提取形成降级阅读结果 | 原 PDF、MinerU 目录、结构化 JSON、MD/TXT |
| XML/HTML/TEI/JATS | 结构化解析章节、链接、表格和元数据 | 原文件、JSON、MD/TXT |
| DOCX/ODT/RTF | 提取段落、表格和链接 | 原文件、JSON、MD/TXT |
| CSV/TSV/Excel | 提取表结构、列类型、行列统计和有限预览 | 原文件、JSON、MD/TXT 摘要 |
| JSON/YAML/TOML/INI | 安全结构化加载和键路径摘要 | 原文件、规范化 JSON、MD/TXT |
| ZIP/TAR/GZ 等 | 安全递归展开，子文件单独登记 | 原压缩包、展开关系、子资产 |
| 结构文件 | 使用 pymatgen/Open Babel 等识别格式、原子、晶胞和构型 | 原文件、结构化 JSON、可读摘要 |
| 量化计算输入输出 | 使用 cclib 和软件专用轻量解析器提取方法、基组、能量、收敛状态等 | 原文件、JSON、可读摘要 |
| 轨迹 | 使用 MDAnalysis 等提取格式、帧数、原子数和基本元数据 | 原轨迹、JSON、可读摘要 |
| 波函数/检查点/其他二进制 | 不强制文本化，只识别格式、大小、哈希和可能的软件来源 | 原文件、元数据 JSON、可读说明 |

解析失败不能删除资产，也不能将零字节文本标记为解析成功。

### 3.10 `asset_manifest.jsonl`

`asset_manifest.jsonl` 每行描述一个逻辑资产的最终状态，是 Stage 06 的核心输入。建议字段：

```json
{
  "schema_version": "1.0",
  "asset_id": "asset_sha256_prefix_or_stable_id",
  "paper_id": "paper_xxx",
  "parent_asset_id": null,
  "discovery_round": 1,
  "archive_depth": 0,
  "role": "main_paper|supplement|source_data|code|input|output|structure|trajectory|config|other",
  "relation_type": "publisher_attachment|explicit_url|related_identifier|repository_match|archive_child",
  "discovered_by": "tei_regex|datastet|crossref|datacite|openalex|github|somef|archive_scan",
  "evidence": "Data and code are available at ...",
  "confidence": "high|medium|low",
  "source_url": "https://example.org/file.zip",
  "resolved_url": "https://cdn.example.org/file.zip",
  "identifier": "doi/repository/database identifier",
  "version": "tag, release, commit or record version",
  "license": "SPDX expression or unknown",
  "access_status": "downloaded|restricted|not_found|failed|skipped_by_policy",
  "sha256": "...",
  "size_bytes": 1234,
  "media_type": "application/zip",
  "original_path": "objects/sha256/ab/...",
  "parser": "mineru|cclib|pymatgen|generic_text|none",
  "parse_status": "success|partial|unsupported|failed|pending",
  "structured_path": "parsed/asset_xxx/document.json",
  "readable_paths": ["parsed/asset_xxx/content.md", "parsed/asset_xxx/content.txt"],
  "error": null,
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601"
}
```

同时保存：

- `asset_events.jsonl`：追加式状态变化日志，用于恢复和审计。
- `clue_manifest.jsonl`：全部线索及其去重、调度和解决状态。
- `unresolved_clues.jsonl`：失效、受限、低置信度、超预算或轮次耗尽的线索。
- `paper_asset_index.jsonl`：论文到资产的汇总索引。

### 3.11 输出目录

```text
stage_05_asset_collection/
├── asset_manifest.jsonl
├── asset_events.jsonl
├── clue_manifest.jsonl
├── unresolved_clues.jsonl
├── paper_asset_index.jsonl
├── stage_summary.json
├── rounds/
│   ├── round_01/
│   ├── round_02/
│   └── round_03/
├── objects/
│   └── sha256/
├── parsed/
│   └── <asset_id>/
│       ├── document.json
│       ├── content.md
│       ├── content.txt
│       └── parser_artifacts/
├── papers/
│   └── <paper_id>/asset_index.json
└── ro_crate/                 # 可选标准化导出
```

### 3.12 阶段状态

Stage 05 对每篇论文输出：

- `complete`：所有已调度高置信度线索均已处理，没有关键失败。
- `partial`：存在受限、失效、超预算或解析失败资产，但已有可用资产集合。
- `no_external_assets`：除论文正文外没有发现可下载资产。
- `failed`：论文级清单无法建立或正文资产无法登记。

`partial` 和 `no_external_assets` 不在 Stage 05 淘汰论文，由 Builder 决定是否有足够证据构建任务。

## 4. 第三方工具采用策略

维护状态按 2026-08-03 的 GitHub 仓库状态检查。是否采用不仅取决于更新时间，还取决于职责是否与管线匹配。

| 项目 | 定位 | 采用级别 | 设计决定 |
| --- | --- | --- | --- |
| [DataStet](https://github.com/kermitt2/datastet) | 从 PDF/TEI/JATS 等识别数据集提及 | 可选增强 | 适合补充数据集线索，但服务较重、依赖 GROBID/DeLFT，默认关闭；启用时端口不得与 Softcite 的 8060 冲突 |
| [suppdata](https://github.com/ropensci/suppdata) | 按 DOI 下载部分出版社补充材料 | 可选适配器 | R 包且出版社覆盖有限，近年维护较少；不能作为出版社附件发现的唯一实现 |
| [citations-collector](https://github.com/con/citations-collector) | 聚合 Crossref、OpenCitations、DataCite、OpenAlex 关系和溯源 | 条件采用 | 项目当前活跃，可用于关系发现和合并；它以学术引用收集为核心，不能替代论文附件和仓库专用解析器 |
| [PyGithub](https://github.com/PyGithub/PyGithub) | GitHub REST API 客户端 | 主要依赖 | 用于仓库搜索、release、commit、文件和速率限制信息；搜索结果仍需本地相关性评分 |
| [SOMEF](https://github.com/KnowledgeCaptureAndDiscovery/somef) | 解析仓库 README、CITATION、许可证、依赖、运行说明和下载链接 | 主要依赖 | 只处理已通过相关性门槛的候选仓库，不负责搜索仓库 |
| [Pooch](https://github.com/fatiando/pooch) | 下载、缓存、哈希校验和后处理 | 主要依赖 | 作为统一下载管理器的底层组件；发现、来源关系和安全策略由本项目封装 |
| [zenodo_get](https://github.com/dvolgyes/zenodo_get) | 下载 Zenodo record/DOI 中的全部或指定文件 | 主要适配器 | 支持校验、重试和 Python API，负责 Zenodo 下载；元数据和关系仍写入统一清单 |
| [pyDataverse](https://github.com/gdcc/pyDataverse) | Dataverse API 客户端 | 主要适配器 | 用于浏览数据集和下载文件，保留 persistent ID、版本和实例 URL |
| [osfclient](https://github.com/osfclient/osfclient) | OSF 文件客户端 | 可选兼容 | 代码更新频率较低；主路径优先直接调用官方 OSF API v2，必要时才使用该客户端 |
| [cos-labs/osf-cli](https://github.com/cos-labs/osf-cli) | 旧 OSF CLI | 不采用 | 最后代码活动年代过久，不进入实现和依赖 |
| [waybackpy](https://github.com/akamhy/waybackpy) | Wayback Machine API 客户端 | 可选失败恢复 | 只查询高置信度失效公开链接；历史快照必须标为 archived，不能等同于原始当前版本 |
| [ro-crate-py](https://github.com/ResearchObject/ro-crate-py) | 将文件及其关系导出为 RO-Crate | 可选标准化输出 | Stage 05 完成后根据 `asset_manifest.jsonl` 生成，不作为主清单替代品 |

### 4.1 推荐的主路径

```text
内部线索抽取器
  + Crossref/DataCite/OpenAlex 直接 API
  + PyGithub -> SOMEF
  + Zenodo -> zenodo_get
  + OSF API v2
  + Dataverse -> pyDataverse
  + Pooch/内部下载管理器
```

可选增强：

```text
DataStet
suppdata
citations-collector
waybackpy
ro-crate-py
```

### 4.2 第三方源码管理

所有实际采用的 GitHub 项目均放置在：

```text
data_pipeline/third_party/<project_name>/
```

每个项目必须：

- 固定 commit SHA 或 release tag。
- 在 `third_party/THIRD_PARTY_LOCK.json` 记录仓库、commit、许可证、获取时间和用途。
- 不自动跟随默认分支更新。
- Python 包从固定源码或兼容发布版本安装到 `environment.yml` 定义的唯一数据管线 Conda 环境。
- 服务型项目使用独立端口和受控启动/停止脚本。

## 5. Stage 06：Builder Agent 构建候选任务

### 5.1 阶段目标

让一个具备本地文件读取和 ResearchChemBench 工具箱调用能力的 Builder Agent，根据论文、资产清单和解析结果构建一个智能体评估任务。

每篇论文只允许：

- 生成一个最有证据、最适合工具箱执行的候选任务；或
- 输出 `abstain` 并说明缺少哪些必要数据。

这样可以避免同一论文生成大量弱任务，也便于 Judge 独立审计。

### 5.2 Agent CLI 选择

Stage 06 和 Stage 07 共用统一的 Agent CLI 适配层，运行时可以分别选择：

```text
codex
claude
opencode
```

Builder 和 Judge 可以使用相同 CLI，也可以分别配置。统一适配层负责命令构造、
工作目录隔离、超时、日志、结构化结果解析、Schema 校验和 token/费用统计，不允许
业务代码直接依赖某一种 CLI 的事件格式。

| CLI | 非交互调用 | 结构化输出策略 |
| --- | --- | --- |
| Codex | `codex exec` | 使用 `--json` 保存事件流、`--output-schema` 约束最终结果、`--output-last-message` 保存最终 JSON |
| Claude Code | `claude --print` | 使用 `--output-format stream-json` 保存事件流，并通过 `--json-schema` 约束最终结果 |
| OpenCode | `opencode run` | 使用 `--format json` 保存事件流，提取最终文本后由本地 JSON Schema 严格校验 |

模型名称按 CLI 单独配置，不能假定三个 CLI 使用相同模型标识。例如 OpenCode 测试
DeepSeek V4 Flash 时使用：

```text
deepseek/deepseek-v4-flash
```

每次调用必须使用新的独立会话，不自动继续历史会话。CLI 找不到、模型不可用、认证
失败、超时或最终结果不符合 Schema 时，该阶段输出 `error` 并停止，不能自动换用其他
CLI 或模型，以免测试结果不可追溯。

### 5.3 Agent 工作空间与聊天记录

每次 Builder 或 Judge 调用都创建独立的运行目录，不能直接将 Agent 的工作目录设置为
仓库根目录：

```text
agent_runs/<run_id>/
├── workspace/
│   ├── input/               # 本次允许读取的只读快照
│   ├── work/                # Agent 可写临时区
│   └── output/              # Agent 正式输出
├── home/                    # 本次 CLI 独立 HOME/配置副本
├── prompt.md
├── response_schema.json
├── native_events.jsonl      # CLI 原生事件流
├── conversation.jsonl       # 统一 user/assistant/tool 聊天记录
├── final_response.json
├── stdout.log
├── stderr.log
└── run_metadata.json
```

隔离要求：

- Builder 和 Judge 使用不同 `run_id`、不同工作目录、不同会话 ID 和不同临时 HOME。
- Agent 只读取复制到 `workspace/input/` 的快照，不依赖可变化的上游目录。
- Judge 的输入快照只包含正式候选包、允许的论文证据、Stage 05 资产索引和验证报告。
- Judge 不得挂载 Builder 的 `native_events.jsonl`、`conversation.jsonl`、临时 HOME 或
  `workspace/work/`。
- CLI 使用自身可用的 sandbox/permission 选项；Linux 环境支持时再增加独立 user/mount
  namespace，不能只依靠 prompt 声明隔离。
- 认证配置可以从主配置复制最小必要项到临时 HOME，但聊天历史、插件缓存和项目记忆不得复制。

`conversation.jsonl` 使用统一格式保存用户提示、Agent 最终回答和可公开的工具调用摘要；
三种 CLI 的完整原生事件仍保存在 `native_events.jsonl`，以便排查事件解析和 token 统计。
任何密钥、Authorization header 和带签名下载 URL 在落盘前必须脱敏。

### 5.4 Builder 输入

- Stage 02 的 GROBID 元数据和 TEI。
- Stage 03 的核心软件及工具箱覆盖证据。
- Stage 04 的资源审查结果。
- Stage 05 的 `asset_manifest.jsonl`、解析文本和原始资产索引。
- ResearchChemBench 工具箱的软件、Action、输入输出和限制清单。
- 候选任务 JSON Schema。
- 少量经过人工确认的正反例模板。

Builder 只允许读取本地资产，不在本阶段继续联网发现文件。

### 5.5 Builder 工作内容

1. 建立科学记录：计算对象、软件、方法、参数、输入、执行步骤、预期输出、论文结果和证据位置。
2. 选择最适合形成评估任务的独立计算单元。
3. 将必要且允许公开的文件复制或链接到 `public_inputs/`。
4. 将参考输出、论文答案和评分所需隐藏信息放入 `hidden_reference/`。
5. 生成任务说明、可用工具、交付物要求和评分规则。
6. 建立每个任务字段到论文段落或资产的 `evidence_map`。
7. 明确无法从证据确定的内容，禁止凭空补齐参数。

### 5.6 候选任务包

```text
stage_06_builder/
└── <paper_id>/
    ├── builder_request.json
    ├── builder_response.json
    ├── scientific_record.json
    ├── candidate_task.json
    ├── task.md
    ├── evidence_map.json
    ├── public_inputs/
    ├── hidden_reference/
    ├── scoring/
    │   ├── rubric.json
    │   └── evaluator_config.json
    ├── validation_report.json
    └── builder_run.json
```

`candidate_task.json` 至少包含：

```text
task_id
paper_id
objective
scientific_context
allowed_tools
public_inputs
expected_deliverables
hidden_reference
scoring_rubric
evidence_map
resource_requirements
known_limitations
```

### 5.7 Agent 后的确定性校验

Builder 的模型输出不能直接进入 Judge。Python 校验器至少检查：

- JSON Schema 和必填字段。
- 所有文件路径存在且位于任务目录内。
- 文件哈希与 Stage 05 清单一致。
- `public_inputs` 与 `hidden_reference` 没有交叉引用。
- 题目文本和公开文件不直接泄漏隐藏答案。
- 关键参数和参考值均有 `evidence_map`。
- 指定的软件和 Action 确实存在于工具箱。
- 评分项总分、范围、容差和失败规则合法。
- 交付物可以由公开输入和允许工具产生。
- 任务资源要求不违反 Stage 04 的硬限制。
- 可执行任务至少完成输入加载或最小 smoke test；不能执行时必须说明原因。

校验失败时当前版本不自动要求 Builder 修改。该候选记录为 `builder_invalid`，保存错误并结束该论文的后续处理。

### 5.8 Builder 输出状态

- `candidate_ready`：候选任务和确定性校验均通过。
- `abstain`：资产不足、证据不足或无法形成独立可评分任务。
- `builder_invalid`：Agent 生成了候选，但确定性校验失败。
- `error`：模型、工具或基础设施调用失败。

只有 `candidate_ready` 进入 Stage 07。

## 6. Stage 07：Judge Agent 独立审计

### 6.1 阶段目标

使用一个与 Builder 隔离的 Judge Agent，检查候选任务是否忠实、完整、可执行、可评分且不泄漏答案。Stage 07 是数据管线最后一个阶段。

### 6.2 隔离要求

Judge 不得读取：

- Builder 的思维过程或临时草稿。
- Builder 未写入正式候选包的隐式判断。
- 其他候选任务的隐藏参考信息。

Judge 可以读取：

- 候选任务包。
- 原论文及 Stage 05 资产。
- `evidence_map`。
- 工具箱能力清单。
- 确定性验证报告。
- 公共输入试运行报告。

Judge 通过与 Builder 相同的 Agent CLI 适配层运行，但必须创建新的会话 ID 和独立
工作目录。Judge 的 CLI 类型、模型和超时可以独立于 Builder 配置。不得使用
`continue`、`resume` 或任何继承 Builder 会话上下文的选项。

Stage 07 保存的聊天记录位于 `stage_07_judge/<task_id>/agent_runs/<run_id>/`；Stage 06
记录位于 `stage_06_builder/<paper_id>/agent_runs/<run_id>/`。Judge 运行目录中不得出现
指向 Stage 06 Agent 私有运行目录的符号链接或路径。

### 6.3 公共输入试运行

在 Judge 审计前，使用隔离工作目录执行一次 public-only probe：

- 只挂载 `task.md`、`candidate_task.json` 中的公开字段和 `public_inputs/`。
- 不挂载论文、隐藏参考答案和 `hidden_reference/`。
- 检查文件能否打开、工具能否识别输入、最小命令能否启动。
- 保存 stdout、stderr、退出码、耗时和资源统计。

该 probe 是 Stage 07 的确定性辅助检查，不是第二个模型，也不尝试完整解题。

### 6.4 Judge 审计维度

1. **论文忠实性**：任务目标、方法、参数和参考结论是否有论文或资产证据。
2. **数据完整性**：公开输入是否足以让智能体开始并完成任务。
3. **工具箱支持**：任务是否只依赖当前可用核心软件和能力。
4. **独立性**：任务是否形成可单独执行和评分的计算单元。
5. **答案泄漏**：题面、文件名、README、示例输出和公开数据是否暴露参考答案。
6. **评分合理性**：评分项是否客观、可计算、覆盖核心目标且容差合理。
7. **资源可行性**：公开任务的预期资源是否在配置边界内。
8. **可复核性**：Judge 的每个问题能否定位到具体字段、文件或证据。

### 6.5 Judge 输出

Judge 必须输出固定结构：

```json
{
  "decision": "pass|revise|reject",
  "summary": "...",
  "checks": {
    "paper_fidelity": {"status": "pass|fail|uncertain", "evidence": []},
    "data_sufficiency": {"status": "pass|fail|uncertain", "evidence": []},
    "toolbox_support": {"status": "pass|fail|uncertain", "evidence": []},
    "answer_leakage": {"status": "pass|fail|uncertain", "evidence": []},
    "scoring_quality": {"status": "pass|fail|uncertain", "evidence": []},
    "resource_feasibility": {"status": "pass|fail|uncertain", "evidence": []}
  },
  "blocking_issues": [],
  "revision_suggestions": [],
  "residual_risks": []
}
```

决策含义：

- `pass`：没有阻断问题，可作为通过审计的候选任务。
- `revise`：问题原则上可以修复，但当前候选不合格。
- `reject`：论文或资产无法支持该任务，或存在不可修复的科学/数据问题。

当前版本中 `revise` 不自动回传 Builder。三种状态都作为最终审计结果保存。

### 6.6 Stage 07 输出目录

```text
stage_07_judge/
└── <task_id>/
    ├── public_probe/
    │   ├── report.json
    │   ├── stdout.log
    │   └── stderr.log
    ├── judge_request.json
    ├── judge_response.json
    ├── audit_report.json
    ├── audit_report.md
    └── judge_run.json
```

`builder_run.json` 和 `judge_run.json` 均应记录：

- 模型名称和部署地址标识，不记录密钥。
- prompt 模板版本。
- 输入和输出 token。
- 调用耗时、重试和 finish reason。
- Agent 可用工具及其版本。
- 输入文件清单和哈希。

## 7. 阶段状态流转

| 上游状态 | 下游动作 |
| --- | --- |
| Stage 05 `complete/partial/no_external_assets` | 进入 Builder，由 Builder 判断能否构建任务 |
| Stage 05 `failed` | 停止该论文，记录失败 |
| Stage 06 `candidate_ready` | 进入 Judge |
| Stage 06 `abstain/builder_invalid` | 不进入 Judge，作为终态保存 |
| Stage 06 `error` | 阶段报错，不伪装成论文淘汰 |
| Stage 07 `pass/revise/reject` | 保存为数据管线最终状态 |
| Stage 07 `error` | 阶段报错，保留可重试状态 |

## 8. 建议配置

```yaml
stage05:
  enabled: true
  max_rounds: 3
  max_archive_depth: 3
  max_assets_per_paper: 500
  max_total_bytes_per_paper: 53687091200   # 50 GiB
  max_single_file_bytes: 10737418240       # 10 GiB
  max_round_walltime_minutes: 60
  network_workers: 8
  mineru_workers: 1
  light_parser_workers: 4
  github_search_max_results: 20
  min_repository_confidence: 0.75
  enable_datastet: false
  enable_suppdata: false
  enable_citations_collector: true
  enable_wayback: false
  export_ro_crate: true

stage06:
  enabled: true
  max_tasks_per_paper: 1
  allow_network: false
  require_evidence_map: true
  run_input_smoke_test: true
  agent:
    cli: opencode                    # codex | claude | opencode
    command: opencode
    model: deepseek/deepseek-v4-flash
    timeout_seconds: 1800
    max_output_chars: 200000
    preserve_conversation: true
    isolate_workspace: true
    environment: {}

stage07:
  enabled: true
  public_probe_timeout_seconds: 600
  allow_network_in_probe: false
  decision_values: [pass, revise, reject]
  agent:
    cli: opencode                    # codex | claude | opencode
    command: opencode
    model: deepseek/deepseek-v4-flash
    timeout_seconds: 1800
    max_output_chars: 200000
    preserve_conversation: true
    isolate_workspace: true
    environment: {}
```

具体文件和时间预算应在使用真实论文集测试后调整。达到预算不是错误，应在 `unresolved_clues.jsonl` 中写明 `budget_exhausted`。

## 9. 日志和可观测性

每个阶段继续写入实时日志，并额外记录机器可读事件：

```text
STAGE_START
ROUND_START
CLUE_DISCOVERED
DOWNLOAD_START/DONE/FAILED
PARSE_START/DONE/FAILED
ROUND_SUMMARY
BUILDER_START/DONE
VALIDATION_DONE
PUBLIC_PROBE_DONE
JUDGE_START/DONE
STAGE_SUMMARY
```

Stage 05 进度至少显示：

```text
paper=3/17 round=2/3 clues=24 resolved=18 downloads=12 parses=10 queue=6
```

所有日志不得输出 API token、Authorization header、私有下载签名参数或隐藏参考答案正文。

## 10. 确认后拟执行的代码调整

用户确认本方案后，再按以下顺序修改代码：

1. 冻结当前本地 Git 状态，建立后半段重构的本地提交基线，不推送 GitHub。
2. 删除现有 Stage 05-17 中被新方案替代的队列、合并、任务选择、多模型审计、人工队列和发布流程代码。
3. 实现统一的资产模型、线索模型、下载管理器、解析路由和三轮调度器。
4. 将 MinerU 纳入 Stage 05 的增量解析队列，并补充非 PDF 解析器。
5. 将选定第三方源码放入 `data_pipeline/third_party/`，固定版本并记录许可证。
6. 实现 Builder Agent 接口、任务 Schema、证据映射和确定性验证器。
7. 实现独立 Judge Agent、公有输入 probe 和结构化审计报告。
8. 更新 `run_pipeline.sh`、配置、README、阶段索引和输出目录命名。
9. 添加单元测试、下载/压缩安全测试、断点恢复测试和端到端小样本测试。
10. 使用此前筛选后的论文集运行 Stage 05-07，监督三轮发现、解析、Builder 和 Judge 的全部过程并修复问题。
11. 形成实施记录和测试结果分析文档，只保存到本地 Git，等待确认后再推送 main。

## 11. 暂不实现但保留的改进方向

Builder/Judge 自动循环修订可以作为后续版本：Judge 输出结构化 `revision_suggestions`，Builder 在隔离的新会话中最多修订一至两次，再由 Judge 复审。

当前版本明确不实现该循环，原因是需要先验证：

- Judge 的问题定位是否稳定。
- Builder 是否会在修复一个问题时引入新问题。
- 循环是否显著增加 token、运行时间和不可重复性。
- 如何保存每轮差异和防止无限修订。

现阶段保留 `revise` 状态和结构化修改建议，已经为未来循环提供接口，但不会自动执行。
