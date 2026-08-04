# ResearchChemBench Data Pipeline

该目录包含 ResearchChemBench 的七阶段数据管线。主流程从 PDF 语料开始，完成去重、结构化解析、软件和资源门控、有边界的研究资产收集、候选任务构建以及独立审计。

当前设计不包含人工发布阶段，也不实现 Builder 与 Judge 的自动循环修订。Stage 07 输出 `pass`、`revise` 或 `reject` 后，流水线结束。

## 阶段概览

| 阶段 | 目录 | 目标 | 核心实现 |
|---|---|---|---|
| Stage 01 | `stage_01_inventory/` | 建立可靠 PDF 入口 | 文件哈希、DOI、标题去重；区分正文、补充材料和其他文件 |
| Stage 02 | `stage_02_grobid_extract/` | 提取论文结构 | GROBID 输出标题、摘要、作者、DOI、章节、正文、参考文献和 TEI XML |
| Stage 03 | `stage_03_software_coverage/` | 软件与工具箱覆盖门控 | Softcite 提取实际使用的软件；仅 `direct_covered` 论文进入后续阶段 |
| Stage 04 | `stage_04_resource_limits/` | 明确资源上限审查 | 关键词召回、GROBID Quantities、模型结构化解释和 Python 阈值比较 |
| Stage 05 | `stage_05_asset_collection/` | 有边界的资产发现、下载、溯源、展开和解析 | 最多三轮；Crossref、DataCite、OpenAlex、GitHub、Zenodo、OSF、Materials Cloud；安全解压；MinerU 和结构化解析 |
| Stage 06 | `stage_06_builder/` | 构建候选智能体评估任务 | 隔离 Builder Agent；支持 Codex、Claude、OpenCode；确定性校验和任务包生成 |
| Stage 07 | `stage_07_judge/` | 独立审计候选任务 | 独立 Judge Agent；检查论文忠实性、数据充分性、工具箱支持、答案泄漏、评分和资源可行性 |

Stage 01-04 是筛选门控。Stage 05 不判断论文是否一定能构造任务，而是尽可能收集并记录有来源的研究资产。Stage 06 可以返回 `candidate_ready` 或 `abstain`；只有合法候选才会进入 Stage 07。

详细设计见：

- `docs/STAGE_05_07_ASSET_AGENT_PIPELINE_DESIGN.md`

## 目录结构

```text
data_pipeline/
├── assets/                 # 工具箱、软件别名、角色规则和能力映射
├── docs/                   # 当前设计文档
├── scripts/                # 环境准备和一键运行脚本
├── src/
│   ├── agents/             # CLI Agent 运行、隔离环境和会话保存
│   ├── core/               # 配置、日志、IO 和运行时工具
│   ├── integrations/       # GROBID、Softcite、Quantities、MinerU、模型和 HTTP 适配
│   ├── orchestration/      # 七阶段编排
│   └── stages/
│       ├── stage01_inventory/
│       ├── stage02_parsing/
│       ├── stage03_software_coverage/
│       ├── stage04_resource_limits/
│       ├── stage05_asset_collection/
│       ├── stage06_builder/
│       └── stage07_judge/
├── tests/                  # 核心逻辑回归测试
├── third_party/            # 所有采用的第三方运行时源码
├── config.json             # 默认配置
└── pyproject.toml           # Python 项目与工具配置
```

`papers/` 用于放置待处理 PDF，`runs/` 用于保存运行结果。两者都是本地数据目录，
默认不提交到 Git。管线会自动创建 `runs/` 下所需的输出目录。

## 主环境安装

数据管线复用 benchmark 的主 Python 环境，不要求创建新的虚拟环境。发生依赖版本冲突时，以主环境已有版本为准；当前主环境要求 `transformers==4.57.3`。

```bash
# 从 ResearchChemBench 仓库根目录进入数据管线目录。
cd data_pipeline

python -m pip install --break-system-packages \
  httpx json-repair jsonschema openpyxl pydantic python-docx \
  python-dotenv PyYAML rdkit pytest ruff vulture

# 仅把本项目注册到主环境，不重新解析或替换依赖版本。
python -m pip install --break-system-packages --no-deps -e .
```

验证：

```bash
python - <<'PY'
import transformers
print(transformers.__version__)
PY

python -m src --help
python -m pytest -q
```

系统依赖至少包括：

- Git
- OpenJDK 21 或更新版本
- Poppler，提供 `pdftotext`
- 常用归档工具和足够的磁盘空间

Java 不需要在 `config.json` 中写机器绝对路径。若 `java` 不在 `PATH`，设置
`GROBID_JAVA_HOME` 或 `JAVA_HOME`；一键脚本在两者均未设置时也会尝试使用当前
Conda 根目录中的 Java。

## 第三方源码准备

所有第三方 GitHub 运行时源码必须位于 `data_pipeline/third_party/`。脚本会固定版本或提交并拒绝覆盖存在本地修改的 checkout。

```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DOWNLOAD_TIMEOUT=600

bash scripts/bootstrap_grobid.sh
bash scripts/bootstrap_stage_gates.sh
bash scripts/bootstrap_mineru.sh
```

对应目录和用途见 `third_party/README.md`。

### GROBID

`scripts/bootstrap_grobid.sh` 下载并构建固定版本 GROBID。Stage 02 会根据配置自动启动服务，处理完成后自动停止。

Stage 02 默认使用 GROBID。GROBID 服务整体无法启动时，流水线直接报错停止，避免把基础设施故障误当成论文解析问题。

仅当某一篇 PDF 的 GROBID 请求失败时，才使用低成本的 Poppler
`pdftotext -layout`，再将文本包装为最小 TEI XML，使 Stage 03 Softcite 可以继续处理。

回退结果位于 `stage_02_grobid_extract/fallback/`，状态记录为
`fallback_pdftotext`；`pdftotext` 也失败时记录 `failed`。每篇记录包含
`grobid_request_attempted`、`grobid_request_failed` 和 `grobid_request_error`，阶段摘要额外保存
`grobid_request_attempts`、`grobid_request_failures` 和
`grobid_request_failure_ratio`，用于事后检查 GROBID 的稳定性。

### Softcite 与 GROBID Quantities

`scripts/bootstrap_stage_gates.sh` 准备：

- `third_party/software-mentions/`
- `third_party/delft/`
- `third_party/grobid-quantities/`

脚本同时下载 Softcite 模型，并使用当前主环境的 `transformers==4.57.3`。Stage 03 或 Stage 04 服务启动失败时，流水线直接报错停止，不把基础设施故障解释为论文淘汰。

### 统一模型缓存

数据管线实际使用的本地模型统一放在一个可整体迁移的子目录中：

```text
../.model_cache/data_pipeline
```

模型来源和运行位置如下：

| 组件 | 模型来源 | 运行时位置 |
|---|---|---|
| GROBID | `grobidOrg/grobid` 0.9.0 随源码发布的 Wapiti/DeLFT 模型 | `../.model_cache/data_pipeline/grobid-home/models/` |
| Softcite | `softcite/software-mentions` 自带模型；BERT 权重来自 `sciencialab/software-mentions-models` | `../.model_cache/data_pipeline/grobid-home/models/` |
| GROBID Quantities | `lfoppiano/grobid-quantities` 自带 quantities/units/values 模型 | `../.model_cache/data_pipeline/grobid-home/models/` |
| MinerU | `opendatalab/MinerU` 模型下载器，从 Hugging Face 或 ModelScope 下载 | `../.model_cache/data_pipeline/mineru/`，配置见 `mineru/mineru.json` |

对应下载地址：

- GROBID：`https://github.com/grobidOrg/grobid`
- Softcite：`https://github.com/softcite/software-mentions`
- Softcite BERT 模型：`https://huggingface.co/sciencialab/software-mentions-models`
- GROBID Quantities：`https://github.com/lfoppiano/grobid-quantities`
- MinerU 源码：`https://github.com/opendatalab/MinerU`
- MinerU Pipeline 模型（Hugging Face）：`https://huggingface.co/opendatalab/PDF-Extract-Kit-1.0`
- MinerU Pipeline 模型（ModelScope）：`https://modelscope.cn/models/OpenDataLab/PDF-Extract-Kit-1.0`

`scripts/prepare_model_cache.py` 会把固定第三方版本中的运行模型同步到统一缓存，并生成三个 Java 服务使用的配置文件：

```text
../.model_cache/data_pipeline/grobid-home/config/grobid.yaml
../.model_cache/data_pipeline/config/software-mentions.yml
../.model_cache/data_pipeline/config/grobid-quantities.yml
../.model_cache/data_pipeline/mineru/mineru.json
../.model_cache/data_pipeline/model_manifest.json
```

上述缓存内的 YAML/JSON 使用相对路径。Java 服务相对其各自的
`third_party/<repository>/` 工作目录解析路径，MinerU 相对
`../.model_cache/data_pipeline/` 解析路径。因此迁移时应保持 `.model_cache/` 与
`data_pipeline/` 位于同一个仓库根目录，并整体移动 `.model_cache`，无需修改缓存内部配置。

可单独重新准备缓存：

```bash
python scripts/prepare_model_cache.py
```

Stage 04 的 `deepseek-v4-flash` 以及 Stage 06/07 配置的 Agent 模型通过远程 API 调用，不下载到本地，因此不属于本地模型缓存。

### MinerU

MinerU 源码位于 `third_party/MinerU/`。模型及其配置位于：

```text
../.model_cache/data_pipeline/mineru
```

默认配置通过 `MINERU_TOOLS_CONFIG_JSON` 使用：

```text
../.model_cache/data_pipeline/mineru/mineru.json
```

`bootstrap_mineru.sh` 会设置 `HF_HOME`、`HUGGINGFACE_HUB_CACHE`、
`MODELSCOPE_CACHE` 和 `MINERU_TOOLS_CONFIG_JSON`，保证新下载内容仍位于
`../.model_cache/data_pipeline/`。`mineru.json` 中的模型目录写作相对路径，例如
`mineru/PDF-Extract-Kit-1___0`；管线启动 MinerU 时会把工作目录固定到缓存根目录。

Stage 05 每发现一个新 PDF 就立即解析。页数不超过 `mineru.max_pages` 时调用 MinerU；
超长 PDF 使用 `pdftotext -layout` 提取可读文本，并在资产的 `document.json` 中记录页数、
阈值和 `mineru_skip_reason`。MinerU 不可用或失败时，主论文可回退到 Stage 02 文本；
无论使用哪种解析器，原始 PDF 都会保留。

## Agent CLI 准备

Stage 06 和 Stage 07 可分别选择以下 CLI：

- `opencode`
- `codex`
- `claude`

CLI 必须预先安装并完成认证。两阶段可以使用不同 CLI 和模型。

### OpenCode 与兼容 API

默认测试配置使用 OpenCode 和 `deepseek-v4-flash`：

```bash
export JUDGE_API_BASE='https://your-openai-compatible-endpoint/v1'
export JUDGE_API_KEY='...'

export BUILDER_AGENT_CLI=opencode
export BUILDER_AGENT_MODEL=deepseek/deepseek-v4-flash
export BUILDER_AGENT_BASE_URL="$JUDGE_API_BASE"

export JUDGE_AGENT_CLI=opencode
export JUDGE_AGENT_MODEL=deepseek/deepseek-v4-flash
export JUDGE_AGENT_BASE_URL="$JUDGE_API_BASE"
```

配置文件中的 `api_key_env` 默认是 `JUDGE_API_KEY`。OpenCode 的临时配置只写环境变量引用，不把密钥写入日志或会话文件。

### Codex 或 Claude

```bash
export BUILDER_AGENT_CLI=codex
export BUILDER_AGENT_MODEL='<codex-model>'

export JUDGE_AGENT_CLI=claude
export JUDGE_AGENT_MODEL='<claude-model>'
```

Codex 和 Claude 使用各自 CLI 的本地认证。运行器只在执行期间复制必要认证到该次隔离 HOME，不共享 Agent 会话，并在进程结束或异常退出后删除隔离目录中的凭据。

## 配置

主要配置位于 `config.json`：

```json
{
  "model_cache_directory": "../.model_cache/data_pipeline",
  "pdf_directory": "papers",
  "run_directory": "runs/current",
  "stop_after": "judge",
  "stage04": {
    "enabled": true
  },
  "resource_limits": {
    "cpu_cores": 500,
    "gpus": 8,
    "memory_gb": 1000,
    "runtime_hours": 12
  },
  "mineru": {
    "enabled": true,
    "max_pages": 100
  },
  "stage05": {
    "enabled": true,
    "download_scope": "all",
    "enable_network": true,
    "max_rounds": 3,
    "max_archive_depth": 3,
    "max_archive_children_per_archive": 300,
    "max_assets_per_paper": 500,
    "network_workers": 4,
    "default_per_host_workers": 2,
    "request_retries": 3,
    "retry_backoff_seconds": 1,
    "retry_max_seconds": 60,
    "discover_publisher_supplements": true
  },
  "stage06": {
    "agent": {
      "cli": "opencode",
      "model": "deepseek/deepseek-v4-flash"
    }
  },
  "stage07": {
    "agent": {
      "cli": "opencode",
      "model": "deepseek/deepseek-v4-flash"
    }
  }
}
```

Stage 04 和 Stage 05 均可通过 `enabled=false` 跳过：

- Stage 04 跳过时写入标准的 `resource_limits` 对象，其中
  `decision="skipped"`、`passed=true`，不启动 GROBID Quantities 或资源解释模型。
- Stage 05 跳过时不联网、不扫描同目录附件、不运行 MinerU，但仍登记主论文，并复用
  Stage 02 文本生成最小资产清单，保证 Stage 06 接口不变。

`stage05.download_scope` 支持：

- `all`：下载满足资产线索规则的补充材料、数据、代码和仓库资产。
- `supplementary_only`：只保留明确来自 Supporting Information、Supplementary
  Material、出版社附件页或 `is-supplemented-by` 关系的附件；主论文始终保留为管线输入。

`supplementary_only` 不调用 OpenAlex，也不主动扩展普通 GitHub、Zenodo、OSF 或 Materials
Cloud 线索。其网络发现只使用 Crossref、DataCite 和 DOI 出版社落地页；只有出版社明确把
补充材料托管在某个仓库时，才继续调用该仓库接口取得对应附件。Europe PMC 查询仍会
启用，因为它直接提供与 DOI 对应的官方补充材料压缩包。

Stage 05 当前实际使用的网络接口如下，不依赖额外的第三方 wrapper：

| 接口 | 用途 |
|---|---|
| Crossref REST API | DOI 元数据和明确关联关系 |
| DataCite REST API | 数据 DOI、内容地址和关联标识符 |
| Europe PMC REST API | 按 DOI 查询 PMCID，并下载排除正文内嵌图片的官方 supplementary ZIP |
| OpenAlex REST API | `all` 模式下补充论文元数据关系 |
| GitHub REST API | 解析正文明确给出的仓库并下载默认分支归档 |
| Zenodo Records API | 枚举并下载记录文件 |
| OSF API v2 | 枚举并下载节点文件 |
| Materials Cloud Archive API | 枚举并下载 Materials Cloud 记录文件 |
| DOI/出版社 HTTPS 页面 | 提取明确标注的 Supplementary/Supporting Information 链接 |

大批量运行建议在 `config.local.env` 中配置：

```bash
SCHOLARLY_API_MAILTO='contact@example.org'
OPENALEX_API_KEY='...'
GITHUB_TOKEN='...'
OSF_TOKEN='...'
ZENODO_ACCESS_TOKEN='...'
```

请求器会按主机限制并发，对 `429` 和临时 `5xx` 响应执行有限重试，并遵守
`Retry-After` 或 `X-RateLimit-Reset`。失败仍会写入事件和未解决线索清单，不会被伪装成
“未发现资产”。

可用的 `stop_after` 值：

- `grobid_extract`
- `software_coverage`
- `resource_limits`
- `asset_collection`
- `builder`
- `judge`

Stage 05 的生产默认单文件上限为 10 GiB、单压缩包展开上限为 50 GiB。测试时应使用更小上限，避免为验证流程下载超大记录。

## 运行

脚本默认读取 benchmark 根目录的 `config.local.env`，映射 Stage 04 和 Agent 所需 API 环境变量，并实时写入日志。
首先将待处理的 PDF 放入 `papers/`，或在本地配置副本中修改 `pdf_directory`。

```bash
bash scripts/run_pipeline.sh config.json runs/current/outputs/run_summary.json
```

日志：

```text
runs/current/outputs/pipeline.log
```

只从已有 Stage 04 结果运行 Stage 05-07：

```bash
python -m src run-late-stages \
  --input runs/example/outputs/stage_04_resource_limits/resource_screened_documents.jsonl \
  --config config.json \
  --workspace runs/example_late/outputs \
  --output runs/example_late/outputs/run_summary.json
```

## Stage 05 输出

核心文件：

```text
stage_05_asset_collection/
├── objects/sha256/             # 原始文件内容寻址存储
├── parsed/<asset_id>/          # JSON、Markdown/TXT、MinerU 或安全解压结果
├── rounds/                     # 每轮线索快照
├── papers/<paper_id>/          # 论文级资产索引
├── asset_manifest.jsonl        # 核心资产清单
├── clue_manifest.jsonl         # 全部线索及状态
├── unresolved_clues.jsonl      # 失败、受限、预算截断和未解决线索
├── asset_events.jsonl          # 下载、解析、去重和预算事件
└── stage_summary.json
```

每个资产记录保留来源、关系、轮次、父资产、版本、SHA-256、大小、原始路径、解析器、结构化输出和可读输出。压缩包采用路径穿越、符号链接、文件数量和展开体积检查。

网络下载遵循内容哈希去重和预算上限。每轮先收集直接资产，再按 `source_data`、`input`、`supplement`、`code` 的优先级登记，并在多个压缩包之间公平分配递归展开预算，避免单个代码仓库占满全部名额。

## Stage 06-07 Agent 隔离与会话保存

Builder 和 Judge 每次运行都创建独立目录：

```text
agent_runs/<run_id>/
├── workspace/
│   ├── input/                  # 只读输入快照
│   ├── work/                   # 临时工作区
│   └── output/                 # Agent 输出区
├── home/                       # 隔离 HOME、XDG 和 CLI 状态
├── attempts/attempt_XX/        # 每次尝试的 stdout/stderr
├── prompt.md
├── response_schema.json
├── native_events.jsonl
├── conversation.jsonl
├── final_response.json
├── stdout.log
├── stderr.log
└── run_metadata.json
```

关键约束：

- Builder 与 Judge 的工作区、HOME、session ID 和聊天记录完全分离。
- Judge 只能读取候选任务快照、论文/资产证据和公共输入探针，不能读取 Builder 聊天记录。
- `conversation.jsonl` 保存用户提示和最终结构化回复；`native_events.jsonl` 保存 CLI 原生事件。
- 日志执行前进行密钥脱敏。
- Agent 输入中的主机绝对路径被删除；压缩包成员使用 `logical_path` 保留必要的文件上下文。
- OpenCode 默认只允许 `read`、`glob`、`grep` 和 `list`，禁止编辑、shell、外部目录和网络工具。

Stage 06 的候选包包括：

```text
candidate/
├── candidate_task.json
├── task.md
├── scientific_record.json
├── evidence_map.json
├── public_inputs/
├── hidden_reference/reference.json
└── scoring/rubric.json
```

Stage 07 输出：

```text
stage_07_judge/<task_id>/
├── public_probe/report.json
├── audit_report.json
├── audit_report.md
├── judge_record.json
└── agent_runs/<judge_run_id>/
```

## 测试与质量检查

```bash
python -m pytest -q
ruff check src tests
ruff format --check src tests
vulture src --min-confidence 80
git diff --check
```

真实 Agent 测试会消耗模型 token。应先使用单论文、较小 Stage 05 预算验证流程，再扩大到完整数据集。

测试语料、历史运行产物和本地服务日志均不属于源码仓库。提交前可直接删除
`papers/` 和 `runs/`；下次运行会重新生成必要的输出。

## 当前限制

- 出版社认证、受限附件和失效链接只记录状态，当前没有自动登录或 Wayback 下载实现。
- MinerU 对非 PDF 二进制科学文件只保留原始文件和元数据；不会伪造文本内容。
- Builder/Judge 读取预算目前由提示词和输入大小共同约束，CLI 本身没有统一的硬性 tool-call 上限。
- Builder 与 Judge 的自动循环修订暂不实现，`revise` 仅作为 Stage 07 结果保存。
