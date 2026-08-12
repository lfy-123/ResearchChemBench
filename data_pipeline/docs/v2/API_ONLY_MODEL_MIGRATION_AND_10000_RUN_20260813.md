# API-only model migration and 10,000-paper run (2026-08-13)

## Scope

This change removes the GPU worker requirement from the Stage00-05 batch workflow. It does not
remove the legacy managed-worker implementation: existing configurations that explicitly select
the shared `screening` role continue to work. New API-only configurations use dedicated model
roles and never start, prewarm, switch, or stop an rlaunch worker.

## Model assignment

The models were selected from the models exposed by the New API endpoint documented in
`data_pipeline/如何调用所有模型.md`. Connectivity, model discovery, and JSON responses were
verified before resource allocation.

| Role | Model | Thinking | Reason |
|---|---|---:|---|
| Stage02 computational-content screening | `Qwen3.6-27B` | off | Fastest tested general screening model with valid JSON output |
| Stage03 toolbox/resource gate | `DeepSeek-V4-Flash` | off | Better semantic software review while retaining low latency |
| Stage05A evidence router | `DeepSeek-V4-Flash-DSpark` | off | High-throughput evidence localization |
| Stage05B candidate auditor | `DeepSeek-V4-Flash` | off | DeepSeek audit over routed high-quality evidence |

`DeepSeek-V4-Pro` was not selected because repeated preflight requests returned upstream HTTP
500 errors. The batch preflight checks `/models` and sends a JSON probe to every distinct selected
model. Infrastructure loss and HTTP 5xx errors abort the current batch instead of being recorded
as scientific rejections.

New API thinking controls are sent in the required top-level `chat_template_kwargs` object.
Loopback API calls explicitly bypass cluster proxy variables. The batch entry accepts either
`RCB_NEW_API_KEY` / `RCB_NEW_API_BASE_URL` or the documented `OPENAI_API_KEY` /
`OPENAI_BASE_URL` variables.

## Stage05 flow

Stage05 remains a two-pass API gate; no Agent harness is used.

1. Stage05A receives the MinerU document inventory, Stage03 workflow/software facts, section
   blocks, captions, and deterministic keyword windows. It routes up to three candidate workflow
   clusters and identifies input, method, result, and claim evidence IDs.
2. Stage05B receives only the routed evidence plus immutable Stage03 toolbox facts. It audits
   scientific significance, workflow completeness, input assets, parameters, ground truth,
   software execution, cost, and target-leakage risk.
3. Deterministic validation checks evidence IDs, workflow dependencies, software facts, cost,
   recovery plans, and hard-blocker contracts. A schema-only retry may repair response shape but
   may not reverse the scientific decision.
4. A validated `pass` or `needs_builder_review` candidate is written for Stage06. Stage05 rejects
   are retained in the registry and do not delete the Stage00 source package.

## Regression result

The first New API attempt was invalid because loopback requests inherited a proxy and all 24
papers failed with `HTTP 502: EOF`. The evaluation script was fixed to bypass the proxy and the
invalid run is excluded from quality conclusions.

The valid no-thinking regression processed all 24 papers with zero processing errors in 475.896
seconds. It forwarded 3 papers and rejected 21.

| Reference | Forward precision | Forward recall | Forward overlap |
|---|---:|---:|---:|
| GPT-5.6-sol full-text Agent | 33.3% | 25.0% | 1/4 |
| Manual full-text labels | 100.0% | 25.0% | 3/12 |

The result shows high precision but insufficient recall. The model migration is operationally
valid, but `DeepSeek-V4-Flash` remains conservative as the final Stage05 auditor. This 24-paper set
is a calibration set rather than an independent holdout, so no paper-specific rules were added.
The long batch preserves every Stage05 decision and evidence packet for later recalibration.

An auditor-thinking experiment was stopped after 17/24 router calls because it was materially
slower than the validated no-thinking run and had not reached the audit stage. The production
batch therefore uses no-thinking mode for predictable throughput.

Artifacts:

- `data_pipeline/runs/stage05-new-api-flash-eval-20260813-r2/`
- `data_pipeline/docs/stage05_gpt56_fulltext_agent_reference_20260812.jsonl`
- `data_pipeline/runs/stage05-deepseek-v4-pro-eval-20260812-iteration1/manual_labels.jsonl`

## 10,000-paper workflow

The new entry point is `scripts/workflows/run_stage00_05_api_batches.sh`. It processes ten
sequential outer batches of 1,000 papers. Each batch runs Stage00 through Stage05 in order; the
next remote copy begins only after the current batch completes.

One 64 CPU / 128 GiB sandbox is shared for the whole job. It hosts GROBID and CPU MinerU, but no
GPU worker is created. Stage01, Stage02, Stage03, and Stage05 retain bounded microbatch parallelism.
Stage04 defaults to one in-flight microbatch with eight MinerU jobs inside it, giving a real global
MinerU concurrency of eight instead of accidentally multiplying two concurrency controls to 64.

The batch status, per-batch configurations, selected-paper exclusions, shared screening registry,
and resumable outputs live below:

`data_pipeline/runs/stage00-05-api-batches-10000-20260813/`

## Verification

- 317 data-pipeline tests passed.
- Ruff passed for source, tests, workflow, and evaluation scripts.
- `git diff --check` passed.
- New API model discovery and JSON probes passed for Qwen3.6-27B, DeepSeek-V4-Flash, and
  DeepSeek-V4-Flash-DSpark.
