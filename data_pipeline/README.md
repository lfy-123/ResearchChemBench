# ResearchChemBench Data Pipeline

This subproject converts a local PDF corpus into reviewed ResearchChemBench task
candidates. It uses low-cost filtering first, applies MinerU only to shortlisted
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
    bootstrap_mineru.sh       install the environment and MinerU
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
  "pdf_directory": "../PDF论文打包",
  "run_directory": "runs/current",
  "stop_after": "model_ensemble",
  "prompt_examples": "assets/prompt_examples.json",
  "verify_asset_urls": true,
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
- `run_directory`: all intermediate and final outputs for the current run.
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

1. Inventory and hash every PDF.
2. Extract cheap text with `pdftotext`.
3. Reject non-computational and wet-lab-only papers.
4. Apply low-cost toolbox, data-signal, and task-potential screening.
5. Send only shortlisted papers to MinerU.
6. Reclassify papers using the higher-quality MinerU text.
7. Group related main-text and supplementary files into a StudyBundle.
8. Extract a source-grounded ScientificRecord.
9. Discover external data, code, SI, DOI, and repository signals.
10. Use the fast model to select exactly one best-supported task type.
11. Use the generation model to construct the task instruction, public inputs,
    hidden reference findings, evidence gates, and scoring rubric.
12. Run deterministic scientific, toolbox, data, leakage, and package checks.
13. Run role-separated LLM review and generate the human curation queue.
14. After assets, reference runs, and expert approval exist, materialize and validate
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
__pycache__/
```

`runs/` may be copied separately when historical outputs are needed, but it is not part
of environment construction. `third_party/MinerU/` is cloned again at the pinned commit
by the bootstrap script.

## Reproducible Environment

The reproducibility contract is:

- Python 3.12;
- base and development dependencies locked by `uv.lock`;
- MinerU pinned in `scripts/bootstrap_mineru.sh` to commit
  `79d6d8d79fb8f3ddba5cc34c07a16f0ec36f56c7`;
- configuration and prompt/toolbox assets versioned with the source;
- API keys supplied only through environment variables or the local run script.

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
