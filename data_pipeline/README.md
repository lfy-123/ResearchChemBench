# ResearchChemBench Data Pipeline

This subproject converts a local PDF corpus into reviewed ResearchChemBench task
candidates. It removes byte-identical duplicate records after inventory, uses GROBID
for structured metadata and full-text extraction, applies MinerU only to shortlisted
papers, then uses LLMs for scientific extraction, single-task selection, package
generation, and role-separated review.

## Repository Layout

```text
data_pipeline/
  DESIGN_PRINCIPLES.md        benchmark principles and relationship to ARCHE
  .python-version             Python 3.12 selection for uv
  config.json                 the only pipeline configuration file
  uv.lock                     locked cross-platform Python dependencies
  assets/
    prompt_examples.json      editable complete examples for four task types
    toolbox.json              available chemistry software and actions
  papers/                     optional local design-reference PDFs, ignored by Git
  src/
    core/                     configuration, data models, paths, and JSON helpers
    ingestion/                PDF inventory, parsing, deduplication, StudyBundle
    discovery/                relevance screening, search, and seed guidance
    curation/                 extraction, task selection, package generation, review
    delivery/                 task build, validation, reference runs, agent pilots
    orchestration/            end-to-end pipeline coordination
    cli.py                    command-line interface
  scripts/
    bootstrap_grobid.sh       clone and build pinned GROBID 0.9.0
    bootstrap_mineru.sh       install the environment and MinerU
    build_main_paper_corpus.py build a symlink corpus of unique main papers
    run_stage02.sh            run inventory and GROBID only; auto-start/stop service
    run_pipeline.sh           run config.json
  tests/                      automated tests and test-only fixtures
  runs/                       generated outputs, ignored by Git
```

There are no separate example, schema, resource, documentation, or configuration
directories. Runtime contracts are enforced directly by the Python validation code.

The benchmark rationale, four task contracts, evidence requirements, cost-increasing
screening funnel, and relationship to ARCHE are documented in
[`DESIGN_PRINCIPLES.md`](DESIGN_PRINCIPLES.md).

## Configuration

Edit only [`config.json`](config.json):

```json
{
  "pdf_directory": "runs/pdf_bundle_main_papers/PDF论文打包",
  "exclude_supplementary": true,
  "run_directory": "runs/current",
  "stop_after": "model_ensemble",
  "prompt_examples": "assets/prompt_examples.json",
  "verify_asset_urls": true,
  "grobid": {
    "base_url": "http://127.0.0.1:8070",
    "working_directory": "third_party/grobid",
    "start_command": ["./gradlew", "--no-daemon", "run"],
    "java_home": "/path/to/jdk-21",
    "auto_start": true,
    "consolidate_header": 0,
    "consolidate_citations": 0
  },
  "mineru": {
    "enabled": true,
    "command": ".venv/bin/mineru",
    "backend": "pipeline",
    "timeout_seconds": 3600
  },
  "llm": {
    "enabled": true,
    "max_workers": 3,
    "extraction": {
      "url": "https://api.deepseek.com/v1",
      "api_key_env": "EXTRACTION_LLM_API_KEY",
      "model_name": "deepseek-v4-flash"
    },
    "classification": {
      "url": "https://api.deepseek.com/v1",
      "api_key_env": "TASK_CLASSIFICATION_LLM_API_KEY",
      "model_name": "deepseek-v4-flash"
    },
    "generation": {
      "url": "https://api.deepseek.com/v1",
      "api_key_env": "TASK_GENERATION_LLM_API_KEY",
      "model_name": "deepseek-v4-pro"
    },
    "review": {
      "url": "https://api.deepseek.com/v1",
      "api_key_env": "REVIEW_LLM_API_KEY",
      "model_name": "deepseek-v4-flash",
      "roles": [
        "scientific_grounding",
        "tool_data_feasibility",
        "evaluation_design",
        "leakage_difficulty"
      ]
    }
  },
  "toolbox": {
    "file": "assets/toolbox.json",
    "enabled_software": ["*"],
    "enabled_actions": ["*"],
    "priority_software": []
  }
}
```

Important fields:

- `pdf_directory`: directory containing the source PDF corpus.
- `exclude_supplementary`: exclude SI, ESM, appendices, and peer-review attachments
  before GROBID and every later stage. Keep this `true` for benchmark tests.
- `run_directory`: all intermediate and final outputs for the current run.
- `grobid`: local GROBID REST service used by Stage 02. Consolidation is disabled so
  extraction stays deterministic and does not depend on Crossref.
- `stop_after`: use `model_ensemble` to stop after candidate review; set to `null`
  only when reference runs and expert approvals are ready for formal task building.
- `extraction`: source-grounded ScientificRecord extraction LLM.
- `classification`: single best task-type classification LLM.
- `generation`: public task, hidden reference, evidence gate, and rubric generation LLM.
- `review`: role-separated candidate-review LLM.
- `enabled_software`: use `['*']` for the full toolbox or list selected software.
- Every LLM stage has its own `url`, `api_key_env`, and `model_name`; endpoints and
  providers do not need to be the same.

API keys are read from the environment and must not be placed in `config.json`.

## Editable Assets

`assets/prompt_examples.json` contains one complete case string for each task type:

- `paper_reproduction`
- `conclusion_guided_reconstruction`
- `autonomous_research`
- `mechanistic_rule_discovery`

Each value is an ordinary string rather than a nested object, so the complete case can
be edited continuously. The examples teach disclosure boundaries and output structure.
They must not contain answers copied into generated tasks.

`assets/toolbox.json` is the stable inventory of available software, aliases,
capabilities, and actions. `config.json` controls which entries are enabled for a run.

## Pipeline Flow

1. Inventory, hash, and label every PDF as `main_paper` or `supplementary`.
2. Retain duplicate and supplementary paths in Stage 01 audit files, but send only
   unique main papers to GROBID when `exclude_supplementary` is enabled.
3. Store GROBID TEI XML, structured metadata, and expanded text for each main paper.
4. Reject non-computational and wet-lab-only papers.
5. Apply low-cost toolbox, data-signal, and task-potential screening.
6. Send only shortlisted papers to MinerU.
7. Reclassify papers using the higher-quality MinerU text.
8. Group related files and discovered assets into a StudyBundle.
9. Extract a source-grounded ScientificRecord.
10. Discover external data, code, SI, DOI, and repository signals.
11. Use the fast model to select exactly one best-supported task type.
12. Use the generation model to construct the task instruction, public inputs,
    hidden reference findings, evidence gates, and scoring rubric.
13. Run deterministic scientific, toolbox, data, leakage, and package checks.
14. Run role-separated LLM review and generate the human curation queue.
15. After assets, reference runs, and expert approval exist, materialize and validate
    the formal ResearchChemBench task.

## Can `.venv` Be Moved To A Server?

No. Do not copy the existing `.venv` to the server as an executable environment.
Python virtual environments contain absolute interpreter paths, generated entry-point
scripts, platform-specific native libraries, Python ABI assumptions, and OS/CPU-specific
wheels. The current local environment is macOS ARM64, so it cannot run on a typical
Linux x86_64 or Linux ARM64 server. Even a second macOS host can break when the project
is placed at a different absolute path.

Move the source code, `uv.lock`, configuration, assets, papers, and source PDF corpus.
Recreate `.venv` on the destination server. The following directories are generated or
machine-specific and should normally not be transferred:

```text
.venv/
runs/
third_party/MinerU/
third_party/grobid/
__pycache__/
```

`runs/` may be copied separately when historical outputs are needed, but it is not part
of environment construction. `third_party/MinerU/` is cloned again at the pinned commit
by the bootstrap script.

## Reproducible Environment

The reproducibility contract is:

- Python 3.12;
- base and development dependencies locked by `uv.lock`;
- GROBID pinned to `0.9.0` and built with OpenJDK 21;
- MinerU pinned in `scripts/bootstrap_mineru.sh` to commit
  `79d6d8d79fb8f3ddba5cc34c07a16f0ec36f56c7`;
- configuration and prompt/toolbox assets versioned with the source;
- API keys supplied only through environment variables or the local run script.

## 当前服务器复现步骤

当前服务器已经完成一次性环境准备：Python 库安装在 benchmark 主环境中，
OpenJDK 21 位于
`/inspire/hdd/global_user/lifangyuan-253108110077/Anaconda3`，GROBID 0.9.0
源码位于 `third_party/grobid`。MinerU 模型缓存位于 benchmark 根目录的
`.model_cache`。

原始测试目录包含 38 份 PDF，其中有 14 份补充材料或其他附件、7 份重复的
正文 PDF。下面的命令会建立一个不复制 PDF 的符号链接语料，只保留 17 篇
唯一正式论文：

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/data_pipeline

./scripts/build_main_paper_corpus.py \
  --source runs/pdf_bundle_input/PDF论文打包 \
  --output runs/pdf_bundle_main_papers/PDF论文打包
```

筛选审计保存在
`runs/pdf_bundle_main_papers/main_paper_corpus_manifest.json`。当前清单记录为：原始
38 份、排除 14 份附件、排除 7 份重复正文、最终保留 17 篇唯一正文。

`config.json` 和本机使用的 `config_pdf_bundle.json` 已指向该目录，并设置：

```json
{
  "pdf_directory": "runs/pdf_bundle_main_papers/PDF论文打包",
  "exclude_supplementary": true
}
```

只复现第一阶段和第二阶段时执行：

```bash
./scripts/run_stage02.sh \
  config_pdf_bundle.json \
  runs/pdf_bundle_20260802/outputs/stage_02_run_summary.json
```

`run_stage02.sh` 不需要 LLM API Key。它会自动完成以下操作：

1. 扫描、哈希和再次检查正文/附件类型。
2. 排除重复 PDF 和 `supplementary` PDF。
3. 如果 8070 端口没有 GROBID，自动启动本地 GROBID。
4. 等待 `/api/isalive` 返回成功后处理 PDF。
5. 保存 TEI、正文和结构化 `documents.jsonl`。
6. 第二阶段结束后停止它自己启动的 GROBID 服务。

如果 8070 端口上原本已经有外部 GROBID 服务，流水线会复用它，并且不会停止
这个外部进程。如果流水线自己启动服务，即使抽取抛出普通异常，也会在
`finally` 中停止进程组；`kill -9` 或机器断电不在此保证范围内。

运行完整数据管线时执行：

```bash
./scripts/run_pipeline.sh \
  config_pdf_bundle.json \
  runs/pdf_bundle_20260802/outputs/run_summary.json
```

完整管线还需要四组 LLM API Key。脚本会从环境变量或
`../config.local.env` 读取。第二阶段仍然使用相同的自动启动、自动停止逻辑。

关键输出位置：

```text
runs/<run_name>/outputs/pipeline.log
runs/<run_name>/outputs/stage_01_inventory/corpus_inventory.jsonl
runs/<run_name>/outputs/stage_01_inventory/main_paper_pdf_paths.jsonl
runs/<run_name>/outputs/stage_01_inventory/supplementary_pdf_paths.jsonl
runs/<run_name>/outputs/stage_02_grobid_extract/grobid_service.log
runs/<run_name>/outputs/stage_02_grobid_extract/tei/*.tei.xml
runs/<run_name>/outputs/stage_02_grobid_extract/text/*.txt
runs/<run_name>/outputs/stage_02_grobid_extract/documents.jsonl
```

## 在新服务器复现第二阶段

第二阶段只依赖 Python 管线、Poppler、OpenJDK 21 和 GROBID。它不依赖
Transformers、MinerU、CUDA 或 LLM API。只有继续运行第七阶段 MinerU 及后续
阶段时，才需要准备这些组件。

### 1. 系统依赖

Ubuntu/Debian：

```bash
sudo apt-get update
sudo apt-get install -y git curl build-essential poppler-utils
```

需要保证本机 8070 端口可用，并预留至少数 GB 空间给 GROBID 源码、Gradle
依赖和模型。首次构建需要访问 GitHub 和 Gradle/Maven 仓库。

### 2. Python 主环境

进入希望复用的 benchmark 主环境，然后安装当前项目。若允许 pip 根据项目的
最低依赖自动补齐：

```bash
cd /path/to/ResearchChemBench/data_pipeline
python -m pip install -e .
```

若必须完全保留主环境中已有库版本，可以先安装项目本身而不解析依赖，再只补
缺失库：

```bash
python -m pip install -e . --no-deps
python -m pip install json-repair pydantic python-dotenv PyYAML rdkit
```

本项目对这些库使用最低版本约束，不要求为数据管线建立单独环境。应以主环境
现有版本为准，只要通过后面的测试即可。

### 3. OpenJDK 21

GROBID 0.9.0 需要 Java 21。使用现有 Conda/Anaconda 主环境时：

```bash
mamba install -n base -y 'openjdk>=21,<22'
export GROBID_JAVA_HOME="$(conda info --base)"
"$GROBID_JAVA_HOME/bin/java" -version
```

也可以使用系统 JDK，但必须把 `config.json` 中的 `grobid.java_home` 改成真实
JDK 根目录，而不是 `bin/java` 文件路径。

### 4. 下载并构建固定版本 GROBID

```bash
cd /path/to/ResearchChemBench/data_pipeline
chmod +x scripts/bootstrap_grobid.sh scripts/run_stage02.sh
GROBID_JAVA_HOME="$(conda info --base)" ./scripts/bootstrap_grobid.sh
```

该脚本会从 `https://github.com/grobidOrg/grobid.git` 浅克隆 0.9.0 到
`third_party/grobid`，切换到固定标签并构建 `grobid-service`。该目录是生成的
第三方源码，不提交到 ResearchChemBench Git 仓库。

验证固定版本：

```bash
git -C third_party/grobid describe --tags --exact-match
# 预期输出：0.9.0
```

### 5. 准备不含附件的 PDF 语料

```bash
./scripts/build_main_paper_corpus.py \
  --source /path/to/original_pdf_corpus \
  --output /path/to/main_paper_corpus
```

脚本使用内容哈希去重，并通过路径、文件名和 PDF 标题识别 SI、ESM、MOESM、
appendix、peer-review 等附件。输出使用符号链接，不复制 PDF。随后在配置中设置：

```json
{
  "pdf_directory": "/path/to/main_paper_corpus",
  "exclude_supplementary": true
}
```

即使输入目录中后来又混入附件，`exclude_supplementary=true` 仍会在第一阶段
审计后阻止附件进入 GROBID 和后续阶段。

### 6. 运行与验收

```bash
./scripts/run_stage02.sh config.json runs/current/outputs/stage_02_run_summary.json
```

验收命令：

```bash
python -m unittest discover -s tests -v
ruff check src scripts tests

wc -l runs/current/outputs/stage_02_grobid_extract/documents.jsonl
find runs/current/outputs/stage_02_grobid_extract/tei -name '*.tei.xml' | wc -l
find runs/current/outputs/stage_02_grobid_extract/text -name '*.txt' | wc -l
```

三个文档数量应一致。检查 Stage 01 的 `stage_summary.json`，其中
`supplementary_excluded` 应等于识别出的附件数，`downstream_main_papers` 应等于
实际交给 GROBID 的唯一正文数。

### Ubuntu Or Debian Server

Install operating-system packages:

```bash
sudo apt-get update
sudo apt-get install -y \
  git curl build-essential poppler-utils ghostscript \
  libgl1 libglib2.0-0
```

Install `uv` and Python 3.12:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
uv python install 3.12
```

Create the environment and install the pinned MinerU checkout:

```bash
cd /path/to/ResearchChemBench/data_pipeline
chmod +x scripts/bootstrap_mineru.sh scripts/run_pipeline.sh
./scripts/bootstrap_mineru.sh
```

The script creates `.venv`, installs the project from `uv.lock`, clones MinerU at the
pinned commit, installs MinerU in the same environment, downloads the pipeline models,
and checks both command-line entry points. Model download requires network access and
substantial disk space. On an offline compute node, run this step on a networked machine
with the same server OS and architecture, then transfer the completed model cache using
the cache location reported by MinerU.

For an NVIDIA server, install a driver and a PyTorch/CUDA combination supported by that
server before relying on GPU parsing. CUDA packages are deliberately not locked here
because they depend on the driver and accelerator image. CPU parsing remains available
but is substantially slower. Keep the MinerU `backend` in `config.json` consistent with
the server installation.

### GROBID

Install OpenJDK 21 into the existing environment, then build the pinned source checkout:

```bash
mamba install -n base -y 'openjdk>=21,<22'
cd ResearchChemBench/data_pipeline
./scripts/bootstrap_grobid.sh
```

Stage 02 calls `/api/processFulltextDocument`. The pipeline reuses an already-running
service at `grobid.base_url`; otherwise it starts `./gradlew --no-daemon run`, waits for
`/api/isalive`, processes the canonical PDFs, and stops the service after extraction.

### macOS

```bash
brew install uv git poppler ghostscript
uv python install 3.12
cd ResearchChemBench/data_pipeline
chmod +x scripts/bootstrap_mineru.sh scripts/run_pipeline.sh
./scripts/bootstrap_mineru.sh
```

### Minimal Installation Without MinerU

This is useful for tests, configuration inspection, and native-text-only development:

```bash
uv sync --frozen --extra dev --python 3.12
.venv/bin/python -m src --help
.venv/bin/python -m pytest -q
```

Set `mineru.enabled` to `false` only when the selected corpus does not require deep PDF
parsing. A formal corpus run should keep the configured fallback available.

### Transfer Example

From the local machine, transfer the reproducible project files while excluding local
environments and generated outputs:

```bash
rsync -av --progress \
  --exclude '.venv/' \
  --exclude 'runs/' \
  --exclude 'third_party/MinerU/' \
  /local/path/ResearchChemBench/data_pipeline/ \
  user@server:/remote/path/ResearchChemBench/data_pipeline/
```

Transfer the large source PDF corpus separately, then update `pdf_directory` and
`run_directory` in `config.json` to paths visible on the server. Relative paths are
resolved from the data-pipeline root and are preferred when the repository layout is
the same across machines.

### Verify A New Server Environment

```bash
cd /remote/path/ResearchChemBench/data_pipeline
.venv/bin/python --version
.venv/bin/mineru --version
.venv/bin/python -m src --help
.venv/bin/ruff format --check src tests
.venv/bin/ruff check src tests
.venv/bin/vulture src --min-confidence 80
.venv/bin/python -m pytest -q
```

Record the environment when producing a formal dataset release:

```bash
uname -a > environment.txt
.venv/bin/python --version >> environment.txt
.venv/bin/mineru --version >> environment.txt
uv pip freeze --python .venv/bin/python >> environment.txt
```

Do not add `environment.txt` when it contains local filesystem paths or credentials.

## Running

Edit the parameter block at the top of `scripts/run_pipeline.sh`, or provide the same
variables through the shell environment. The four independent groups are:

```text
EXTRACTION_LLM_URL / EXTRACTION_LLM_API_KEY / EXTRACTION_LLM_MODEL_NAME
TASK_CLASSIFICATION_LLM_URL / TASK_CLASSIFICATION_LLM_API_KEY / TASK_CLASSIFICATION_LLM_MODEL_NAME
TASK_GENERATION_LLM_URL / TASK_GENERATION_LLM_API_KEY / TASK_GENERATION_LLM_MODEL_NAME
REVIEW_LLM_URL / REVIEW_LLM_API_KEY / REVIEW_LLM_MODEL_NAME
```

Then run:

```bash
./scripts/run_pipeline.sh
```

The script also accepts an optional config path and summary-output path:

```bash
./scripts/run_pipeline.sh config_pdf_bundle.json \
  runs/pdf_bundle_20260802/outputs/run_summary.json
```

Equivalent direct command:

```bash
.venv/bin/python -m src run \
  --output runs/current/outputs/run_summary.json
```

Useful checks:

```bash
.venv/bin/python -m src --help
.venv/bin/chem-pipeline --help
.venv/bin/ruff format --check src tests
.venv/bin/ruff check src tests
.venv/bin/vulture src --min-confidence 80
.venv/bin/python -m pytest -q
```

## Outputs

All corpus-pipeline outputs are stored below `runs/current/outputs`. Each processing
step has its own `stage_*` subdirectory, and `stage_index.json` describes the complete
layout. Screening stages include `selected_pdf_paths.jsonl`; these files point to the
original PDFs and do not copy them. The main candidate products are:

- `pipeline.log`: live stage starts/completions, per-document progress bars, failures,
  and a 15-second heartbeat while each MinerU document is running.
- `stage_01_inventory/corpus_inventory.jsonl`: all PDF paths, hashes, and duplicate
  mappings. `main_paper_pdf_paths.jsonl`, `supplementary_pdf_paths.jsonl`,
  `canonical_pdf_paths.jsonl`, and `duplicate_pdf_paths.jsonl` split the audit.
- `stage_02_grobid_extract/tei/`: one original GROBID TEI XML file per canonical PDF.
- `stage_02_grobid_extract/text/`: body text expanded from TEI for downstream matching.
- `stage_02_grobid_extract/documents.jsonl`: structured title, abstract, authors, DOI,
  publication metadata, keywords, section headings, paths, and extraction quality.
- `stage_13_task_selection/selected_records.jsonl`: selected task type and reason.
- `stage_14_package_generation/candidate_packages/`: generated benchmark candidates.
- `stage_15_quality_gates/quality_gated_records.jsonl`: deterministic gate results.
- `stage_16_model_ensemble/model_reviewed_records.jsonl`: role-separated reviews.
- `stage_17_curation_queue/curation_queue.jsonl`: candidates for human inspection.
- `stage_18_dataset_build/`: formal build inputs, manifest, dataset, and validation.
- `run_summary.json`: compact run statistics.

Candidate packages are not automatically formal benchmark tasks. Formal release also
requires materialized inputs, a successful reference run, stable tolerances, expert
approval, and parent-benchmark validation.

## Tests And Generated Files

`tests/test_pipeline.py` contains regression tests for filtering, toolbox matching,
task selection, prompt examples, package construction, leakage checks, reference runs,
and parent ResearchChemBench compatibility. `tests/fixtures/` contains two small
curated records used only by these tests. Neither directory is read by a normal
pipeline run, but both are retained to detect regressions.

The remaining non-source directories are intentional:

- `.venv/`: local Python and MinerU environment; regenerable and never portable.
- `third_party/MinerU/`: pinned MinerU checkout used for PDF parsing.
- `runs/`: ignored historical and generated outputs; not imported by the code.
- `papers/`: optional local ARCHE paper and supplementary material; ignored by Git.

Python caches, Ruff/Pytest caches, package metadata, old configs, old examples, old
schemas, and duplicate documentation directories are removed from the maintained tree.
