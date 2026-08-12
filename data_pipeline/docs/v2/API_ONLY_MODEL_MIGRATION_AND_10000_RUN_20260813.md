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
| Stage05B candidate auditor | Runtime-selected strong model | off | First stable model from `DeepSeek-V4-Pro`, `GLM-5.2`, `Nex-N2-Pro`, `Nex-N2-Pro-w8a8` |

Stage05B no longer falls back to a Flash model. Before sandbox allocation, the workflow probes
the strong-model candidates in priority order and requires three consecutive valid structured
responses. `DeepSeek-V4-Pro`, `GLM-5.2`, and the full-precision `Nex-N2-Pro` currently return an
upstream HTTP 500 from the configured service. `Nex-N2-Pro-w8a8` passed all three probes and is
therefore the current selection. If every strong candidate is unavailable, the run aborts before
copying papers or allocating a sandbox. The selected model and every probe outcome are persisted
in `batch_status.json`.

The auditor keeps the full routed evidence budget (up to 90,000 characters) but uses an 8,192-token
output budget. Historical 24-paper traces show a maximum final audit response of 6,897 completion
tokens. A 4,096-token live test clipped a valid Nex response, while the earlier 16,000-token setting
allowed unnecessary generation until the 20-minute request timeout. The selected middle bound
limits verbose generation without truncating the known response range; it does not reduce input
context and is exposed as `--stage05-auditor-max-tokens`. A full-context smoke test also showed
that the w8a8 endpoint otherwise spends the entire output budget on hidden reasoning and returns
no JSON body. The workflow therefore explicitly sends `enable_thinking=false`; this behavior is
validated against the live endpoint even though the local model table does not document a
dedicated switch for this variant.

The final representative smoke used the same 90,000-character evidence path as production. The
auditor returned a complete JSON object with `finish_reason=stop`, 4,225 completion tokens, and a
235.159-second model-call duration; Stage05 completed with zero processing errors. Its scientific
decision remains subject to the normal deterministic contract gate and later quality calibration.

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

The earlier valid no-thinking Flash regression processed all 24 papers with zero processing
errors in 475.896 seconds. It forwarded 3 papers and rejected 21.

| Reference | Forward precision | Forward recall | Forward overlap |
|---|---:|---:|---:|
| GPT-5.6-sol full-text Agent | 33.3% | 25.0% | 1/4 |
| Manual full-text labels | 100.0% | 25.0% | 3/12 |

The result shows high precision but insufficient recall and is the reason Flash is no longer
permitted as the final Stage05 auditor. This 24-paper set is a calibration set rather than an
independent holdout, so no paper-specific rules were added. The long batch preserves every
Stage05 decision and evidence packet for later recalibration.

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
- The Stage05B strong-model selector chose `Nex-N2-Pro-w8a8` only after three consecutive
  structured probes; it did not fall back to Flash.
