# ResearchChemBench Data Pipeline

该目录包含 ResearchChemBench 的七阶段数据管线。主流程从 PDF 语料开始，完成去重、结构化解析、软件和资源门控、有边界的研究资产收集、候选任务构建以及独立审计。

`data_pipeline/` 可以脱离 benchmark 的其他模块单独复制和运行。Conda 环境、第三方源码、模型缓存、API 配置和运行产物均收敛在该目录内，不依赖 benchmark 根目录中的绝对路径。

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
├── .model_cache/           # 本地模型和服务配置，不提交 Git
├── assets/                 # 工具箱、软件别名、角色规则和能力映射
├── docs/                   # 当前设计文档
├── papers/                 # 待处理 PDF，不提交 Git
├── runs/                   # 阶段输出和日志，不提交 Git
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
├── config.local.env.example # API 和 Agent 配置模板
├── environment.yml          # 唯一 Conda 环境定义
└── pyproject.toml           # Python 项目与工具配置
```

`papers/` 用于放置待处理 PDF，`runs/` 用于保存运行结果。两者都是本地数据目录，
默认不提交到 Git。管线会自动创建 `runs/` 下所需的输出目录。

## Conda 环境

数据管线只使用一个 Conda 环境。`environment.yml` 安装 Python 3.12、OpenJDK 21、Poppler、Git、项目依赖和 Softcite 需要的固定版本。MinerU、DeLFT 和 JEP 由 bootstrap 脚本安装到同一环境，不创建第二个环境。

```bash
cd data_pipeline
conda env create -f environment.yml
conda activate researchchem-data-pipeline
```

更新已有环境：

```bash
conda env update -f environment.yml --prune
conda activate researchchem-data-pipeline
```

验证：

```bash
python --version
java -version
pdftotext -v
python -m src --help
python -m pytest -q
```

建议为第三方源码和模型预留至少 30 GB 磁盘空间。环境文件已包含：

- Git
- OpenJDK 21 或更新版本
- Poppler，提供 `pdftotext`
- Git LFS、curl 和 unzip

Java 不需要在 `config.json` 中写机器绝对路径。若 `java` 不在 `PATH`，设置
`GROBID_JAVA_HOME` 或 `JAVA_HOME`；脚本会优先使用当前激活环境的 `CONDA_PREFIX`。

## 第三方源码准备

所有第三方 GitHub 运行时源码位于 `third_party/`。GitHub 仓库不直接提交这些大型 checkout，只保存上游链接、固定版本、bootstrap 脚本和必要补丁。

| 本地目录 | 上游仓库 | 固定版本 | 用途 |
|---|---|---|---|
| `third_party/grobid/` | [grobidOrg/grobid](https://github.com/grobidOrg/grobid) | tag `0.9.0` | Stage 02 PDF 到 TEI |
| `third_party/software-mentions/` | [softcite/software-mentions](https://github.com/softcite/software-mentions) | `c7c83852a3cad8f2d9d07ce3de6fbe852e23c19a` | Stage 03 软件抽取 |
| `third_party/delft/` | [kermitt2/delft](https://github.com/kermitt2/delft) | `d8505592c38058b9b0abbde14d4ddedff3ad7d0f` | Softcite 模型运行时 |
| `third_party/grobid-quantities/` | [lfoppiano/grobid-quantities](https://github.com/lfoppiano/grobid-quantities) | `d0d55592f4d0ddbe6a549e06613349adaa2d1cd7` | Stage 04 数值与单位抽取 |
| `third_party/MinerU/` | [opendatalab/MinerU](https://github.com/opendatalab/MinerU) | `79d6d8d79fb8f3ddba5cc34c07a16f0ec36f56c7` | Stage 05 PDF 深度解析 |

一键准备全部源码、补丁、本地依赖和模型：

```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DOWNLOAD_TIMEOUT=600

bash scripts/bootstrap_all.sh
```

分步下载方式：

```bash
bash scripts/bootstrap_grobid.sh
bash scripts/bootstrap_stage_gates.sh
bash scripts/bootstrap_mineru.sh
```

脚本会拒绝覆盖有本地修改的 checkout。手工 clone 和补丁方式见 [third_party/README.md](third_party/README.md)。

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

脚本同时下载 Softcite 模型，并使用 `transformers==4.57.3`。Stage 03 或 Stage 04 服务启动失败时，流水线直接报错停止，不把基础设施故障解释为论文淘汰。

### 统一模型缓存

数据管线实际使用的本地模型统一放在一个可整体迁移的子目录中：

```text
.model_cache
```

模型来源和运行位置如下：

| 组件 | 模型来源 | 运行时位置 |
|---|---|---|
| GROBID | `grobidOrg/grobid` 0.9.0 随源码发布的 Wapiti/DeLFT 模型 | `.model_cache/grobid-home/models/` |
| Softcite | `softcite/software-mentions` 自带模型；BERT 权重来自 `sciencialab/software-mentions-models` | `.model_cache/grobid-home/models/` |
| GROBID Quantities | `lfoppiano/grobid-quantities` 自带 quantities/units/values 和 ClearNLP 模型 | `.model_cache/grobid-home/models/` 和 `.model_cache/grobid-quantities/` |
| MinerU | `opendatalab/MinerU` 模型下载器，从 Hugging Face 或 ModelScope 下载 | `.model_cache/mineru/` |

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
.model_cache/grobid-home/config/grobid.yaml
.model_cache/config/software-mentions.yml
.model_cache/config/grobid-quantities.yml
.model_cache/mineru/mineru.json
.model_cache/model_manifest.json
```

上述缓存内的 YAML/JSON 使用相对路径。Java 服务相对其各自的
`third_party/<repository>/` 工作目录解析路径，MinerU 相对 `.model_cache/` 解析。迁移时整体复制 `data_pipeline/` 即可。

可单独重新准备缓存：

```bash
python scripts/prepare_model_cache.py
```

Stage 04 的 `deepseek-v4-flash` 以及 Stage 06/07 配置的 Agent 模型通过远程 API 调用，不下载到本地，因此不属于本地模型缓存。

### MinerU

MinerU 源码位于 `third_party/MinerU/`。模型及其配置位于：

```text
.model_cache/mineru
```

默认配置通过 `MINERU_TOOLS_CONFIG_JSON` 使用：

```text
.model_cache/mineru/mineru.json
```

`bootstrap_mineru.sh` 会设置 `HF_HOME`、`HUGGINGFACE_HUB_CACHE`、
`MODELSCOPE_CACHE` 和 `MINERU_TOOLS_CONFIG_JSON`，保证新下载内容仍位于
`.model_cache/`。`mineru.json` 中的模型目录写作相对路径，例如
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

官方仓库：[anomalyco/opencode](https://github.com/anomalyco/opencode)

```bash
curl -fsSL https://opencode.ai/install | bash
opencode --version
```

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

Codex 官方仓库：[openai/codex](https://github.com/openai/codex)

```bash
npm install -g @openai/codex
codex --version
codex
```

Claude Code 官方文档：[Claude Code Setup](https://code.claude.com/docs/en/getting-started)

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
claude
```

完成 CLI 登录后再设置阶段选项：

```bash
export BUILDER_AGENT_CLI=codex
export BUILDER_AGENT_MODEL='<codex-model>'

export JUDGE_AGENT_CLI=claude
export JUDGE_AGENT_MODEL='<claude-model>'
```

Codex 和 Claude 使用各自 CLI 的本地认证。运行器只在执行期间复制必要认证到该次隔离 HOME，不共享 Agent 会话，并在进程结束或异常退出后删除隔离目录中的凭据。

### 本地 API 配置文件

```bash
cp config.local.env.example config.local.env
```

`scripts/run_pipeline.sh` 默认读取该文件。`config.local.env` 已被 Git 忽略，不要提交真实密钥。

| 环境变量 | 用途 |
|---|---|
| `RESOURCE_LLM_URL` | Stage 04 OpenAI-compatible API 地址 |
| `RESOURCE_LLM_API_KEY` | Stage 04 API 密钥 |
| `RESOURCE_LLM_MODEL_NAME` | Stage 04 模型名 |
| `BUILDER_AGENT_CLI` / `JUDGE_AGENT_CLI` | `opencode`、`codex` 或 `claude` |
| `BUILDER_AGENT_COMMAND` / `JUDGE_AGENT_COMMAND` | CLI 命令或可执行文件路径 |
| `BUILDER_AGENT_MODEL` / `JUDGE_AGENT_MODEL` | Agent 模型名 |
| `BUILDER_AGENT_BASE_URL` / `JUDGE_AGENT_BASE_URL` | OpenCode 兼容 API 地址 |
| `JUDGE_API_BASE` / `JUDGE_API_KEY` | Builder/Judge 共用的默认端点和密钥 |
| `SCHOLARLY_API_MAILTO` | Crossref/OpenAlex polite pool 联系邮箱 |
| `OPENALEX_API_KEY` | OpenAlex 额外配额 |
| `GITHUB_TOKEN` | GitHub REST API 额外配额 |
| `OSF_TOKEN` | OSF 受限数据 |
| `ZENODO_ACCESS_TOKEN` | Zenodo 受限数据或额外配额 |
| `HF_ENDPOINT` | Hugging Face 镜像 |

## 配置

主要配置位于 `config.json`：

```json
{
  "model_cache_directory": ".model_cache",
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

所有相对路径按配置文件所在目录解析。建议保留 `config.json` 作为版本化默认值，将本地实验配置写入已忽略的 `config.local.json`：

```bash
cp config.json config.local.json
bash scripts/run_pipeline.sh config.local.json
```

### 全局参数

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `model_cache_directory` | `.model_cache` | 本地模型缓存 |
| `pdf_directory` | `papers` | 输入 PDF 根目录 |
| `exclude_supplementary` | `true` | 只将去重正文传给 Stage 02 |
| `run_directory` | `runs/current` | 运行目录 |
| `stop_after` | `judge` | 最后运行的阶段 |

### Stage 02: GROBID

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `grobid.base_url` | `http://127.0.0.1:8070` | 服务地址 |
| `grobid.working_directory` | `third_party/grobid` | 源码目录 |
| `grobid.auto_start` | `true` | 自动启动和停止服务 |
| `grobid.startup_timeout_seconds` | `600` | 启动超时 |
| `grobid.timeout_seconds` | `900` | 单篇请求超时 |
| `grobid.retries` | `2` | 请求重试次数 |
| `grobid.consolidate_header` | `0` | Header consolidation |
| `grobid.consolidate_citations` | `0` | Citation consolidation |
| `grobid.max_chars` | `2000000` | 单篇文本上限 |
| `grobid.reuse_existing` | `true` | 复用已有 TEI |
| `grobid.fallback.enabled` | `true` | 允许单篇请求回退 |
| `grobid.fallback.pdftotext_enabled` | `true` | 使用 `pdftotext -layout` |
| `grobid.fallback.pdftotext_timeout_seconds` | `300` | 回退超时 |

GROBID 服务整体无法启动时管线停止。只有单篇 PDF 请求失败时才回退，并记录失败次数和比例。

### Stage 03: 软件覆盖

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `softcite.base_url` | `http://127.0.0.1:8060` | Softcite 地址 |
| `softcite.working_directory` | `third_party/software-mentions` | 源码目录 |
| `softcite.auto_start` | `true` | 自动启动和停止 |
| `softcite.startup_timeout_seconds` | `900` | 启动超时 |
| `softcite.timeout_seconds` | `600` | 单篇超时 |
| `softcite.retries` | `2` | 重试次数 |
| `softcite.aliases_file` | `assets/software_aliases.json` | 软件别名 |
| `softcite.role_rules_file` | `assets/software_role_rules.json` | 核心/辅助软件规则 |
| `softcite.capability_map_file` | `assets/software_capability_map.json` | 等价能力映射 |
| `toolbox.file` | `assets/toolbox.json` | 工具箱清单 |
| `toolbox.enabled_software` | `["*"]` | 启用软件 |
| `toolbox.enabled_actions` | `["*"]` | 启用 Action |
| `toolbox.priority_software` | `[]` | 优先软件 |

只有 `direct_covered` 论文进入后续阶段；`capability_equivalent` 只保留备选记录。

### Stage 04: 资源审查

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `stage04.enabled` | `true` | 是否执行资源审查 |
| `resource_limits.cpu_cores` | `500` | CPU 核数上限 |
| `resource_limits.gpus` | `8` | GPU 数量上限 |
| `resource_limits.memory_gb` | `1000` | 内存上限，GB |
| `resource_limits.runtime_hours` | `12` | 单次运行时间上限，小时 |
| `resource_interpretation.enabled` | `true` | 是否调用解释模型 |
| `resource_interpretation.url` | `https://api.deepseek.com/v1` | API 地址 |
| `resource_interpretation.api_key_env` | `RESOURCE_LLM_API_KEY` | 密钥环境变量名 |
| `resource_interpretation.model_name` | `deepseek-v4-flash` | 模型名 |
| `resource_interpretation.timeout_seconds` | `900` | API 超时 |
| `resource_interpretation.retries` | `2` | API 重试 |
| `resource_interpretation.max_tokens` | `3000` | 最大输出 token |
| `resource_interpretation.validation_retries` | `1` | JSON 纠正次数 |
| `grobid_quantities.base_url` | `http://127.0.0.1:8062` | Quantities 地址 |
| `grobid_quantities.auto_start` | `true` | 自动启动和停止 |
| `grobid_quantities.startup_timeout_seconds` | `600` | 启动超时 |
| `grobid_quantities.timeout_seconds` | `120` | 请求超时 |
| `grobid_quantities.retries` | `2` | 重试次数 |

Stage 04 只比较论文中明确召回并被模型确认的资源表达，不估算真实成本。无资源信息、表达含糊或只提到超算平台时放行。

### MinerU

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `mineru.enabled` | `true` | 是否使用 MinerU |
| `mineru.command` | `mineru` | CLI 命令 |
| `mineru.backend` | `pipeline` | Backend |
| `mineru.timeout_seconds` | `3600` | 单文件超时 |
| `mineru.max_pages` | `100` | 超过后使用低成本文本解析 |
| `mineru.reuse_existing` | `true` | 复用解析结果 |
| `mineru.min_markdown_chars` | `100` | 有效 Markdown 最小长度 |

### Stage 05: 资产收集

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `stage05.enabled` | `true` | 是否执行 |
| `stage05.download_scope` | `all` | `all` 或 `supplementary_only` |
| `stage05.enable_network` | `true` | 是否联网 |
| `stage05.max_rounds` | `3` | 最大发现轮次 |
| `stage05.max_archive_depth` | `3` | 压缩包递归深度 |
| `stage05.max_archive_children_per_archive` | `300` | 单压缩包成员登记上限 |
| `stage05.max_assets_per_paper` | `500` | 单论文资产上限 |
| `stage05.max_clues_per_paper` | `500` | 单论文线索上限 |
| `stage05.max_single_file_bytes` | `10737418240` | 单文件上限，10 GiB |
| `stage05.max_archive_expanded_bytes` | `53687091200` | 展开上限，50 GiB |
| `stage05.max_archive_files` | `5000` | 压缩包文件数上限 |
| `stage05.max_text_chars` | `2000000` | 单资产文本上限 |
| `stage05.max_targets_per_clue` | `200` | 单线索目标上限 |
| `stage05.network_workers` | `4` | 总网络并发 |
| `stage05.default_per_host_workers` | `2` | 默认单主机并发 |
| `stage05.per_host_workers` | 见 `config.json` | 指定 API 并发 |
| `stage05.request_retries` | `3` | 请求重试 |
| `stage05.retry_backoff_seconds` | `1` | 初始退避 |
| `stage05.retry_max_seconds` | `60` | 最大退避 |
| `stage05.metadata_timeout_seconds` | `30` | 元数据超时 |
| `stage05.download_timeout_seconds` | `120` | 下载超时 |
| `stage05.include_local_siblings` | `true` | 扫描同目录附件 |
| `stage05.query_metadata` | `true` | 查询元数据 API |
| `stage05.discover_publisher_supplements` | `true` | 扫描出版社附件 |
| `stage05.paper_limit` | `null` | 调试论文数量限制 |

### Stage 06/07: Agent

| 参数 | 默认值 | 说明 |
|---|---:|---|
| `stage06.enabled` / `stage07.enabled` | `true` | 是否启用 |
| `max_agent_readable_bytes` | `52428800` | Agent 可读输入上限，50 MiB |
| `agent.cli` | `opencode` | `opencode`、`codex` 或 `claude` |
| `agent.command` | 与 CLI 同名 | 命令或路径 |
| `agent.model` | `deepseek/deepseek-v4-flash` | 模型 |
| `agent.base_url` | 空 | OpenCode 兼容 API |
| `agent.api_key_env` | `JUDGE_API_KEY` | 密钥变量名 |
| `agent.timeout_seconds` | `1800` | 单次超时 |
| `agent.retries` | `2` | 重试次数 |
| `agent.max_output_chars` | `200000` | 响应字符上限 |
| `agent.environment` | `{}` | 额外环境变量 |

`preserve_conversation` 和 `isolate_workspace` 在代码中固定为 `true`。Builder 和 Judge 的工作区、HOME、session 和聊天记录完全隔离。

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

脚本默认读取 `data_pipeline/config.local.env`，映射 Stage 04 和 Agent 所需 API 环境变量，并实时写入日志。
首先将待处理的 PDF 放入 `papers/`，或在本地配置副本中修改 `pdf_directory`。

```bash
bash scripts/run_pipeline.sh

# 或显式指定配置和摘要输出。
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
ruff check src tests scripts
ruff format --check src tests scripts
vulture src --min-confidence 80
git diff --check
```

真实 Agent 测试会消耗模型 token。应先使用单论文、较小 Stage 05 预算验证流程，再扩大到完整数据集。

测试语料、历史运行产物和本地服务日志均不属于源码仓库。提交前可直接删除
`papers/` 和 `runs/`；下次运行会重新生成必要的输出。
同样不应提交 `.model_cache/`、第三方 checkout、`config.local.env` 或 `config.local.json`。

## 当前限制

- 出版社认证、受限附件和失效链接只记录状态，当前没有自动登录或 Wayback 下载实现。
- MinerU 对非 PDF 二进制科学文件只保留原始文件和元数据；不会伪造文本内容。
- Builder/Judge 读取预算目前由提示词和输入大小共同约束，CLI 本身没有统一的硬性 tool-call 上限。
- Builder 与 Judge 的自动循环修订暂不实现，`revise` 仅作为 Stage 07 结果保存。
