# Expanded-reference validation plan

Status: blocked. No new scientific calculations have been performed. No upgraded scientific PASS is claimed.

## Source actually inspected

- `papers/paper_60f4c45810428116/documents/main.pdf`, PDF pages 2, 3, 5; SHA256 7c3fb2808e4d8f7f26836f47f3947d9e773a8fbaefbe89f78156e7e1ba10d91f
- `papers/paper_60f4c45810428116/documents/supplementary_001.pdf`, PDF pages 3, 4, 5, 6, 7, 19, 22; SHA256 5a9d2e70dc461cb7731eb715a4251b800c264f87b08b89260bb41d84c6597d62

The source interprets temperature/time competition between generation and degradation; the yield surface is RBF interpolation (SI p6), not a fitted mechanistic model. B3LYP-D3/6-311+G(d,p), SMD THF potentials versus Fc are a thermochemical baseline (SI p19). This benchmark adds an independently parameterized, falsifiable kinetic model and identifiability testing. Neither reduction potentials nor RBF interpolation supply rate constants.

## Reusable old evidence and new gaps

The entire old final payload is preserved byte-for-byte in `legacy_final_snapshot/`. The former scalar/descriptor/local-path calculation is reusable only for the same object, state, method and observable. It does not validate the expanded matrix. Inspect the old raw evidence pointers in the archived source evaluator and audit; never reuse its old PASS as a completion result.

New required reference gaps:

- network: Conserved finite reaction model and independent rate intervals.
- identifiability: Numerical sensitivity/rank and parameter profiles; honest bounded ambiguity is allowed after complete analysis.
- holdout: Predictions for three genuinely held-out measured conditions, with clipping/missingness retained.

Old THF reduction potentials distinguish dissociative reduction thermodynamics (reported difference 0.794 V) on the stated absolute Fc scale. They are not independent generation, rearrangement or quench rate constants. The tabulated measured grid is reusable with its censoring intact.

Historical structured reports directly inspected in this development pass:

- `workspaces/codex_gpt56/paper_60f4c45810428116_20260918_154216_28147/runs/cli_runs/batch_20260918_154217_e1763b/autonomous_research-paper_60f4c45810428116-codex-20260918_154217-48743d/report/results.json`; SHA256 b2b7cdf52ada1307f32176d7fa2fefcdc77d3a5a5e4bb64fcee2ac671b05633b

## Blocking inputs and release conditions

- Obtain independent generation/back-quench/rearrangement/capture rate intervals or validated barriers. The supplied measured grid and old reduction potentials cannot identify those rates without independent constraints.
- Resolve the source/model-definition mismatch before assigning a back-quench channel to 1a. Main pp4-5 discusses 1h/SPh and return to starting material; it supplies neither an irreversible 1a sink nor an identified elementary reverse step. Do not assert that a 1a back-quench channel exists or retain Q as established chemistry. A justified network and its charge/electron/reagent bookkeeping require independent evidence; source 3a identifies a quenched rearrangement product but not its channel rate. Keep the development gate blocked pending source-grounded resolution; any scientific scope change requires coordinator review.

## Minimum pilot and full validation

1. Verify all graphs, hydrogens, maps, formal charge/spin and reaction ledgers; rebuild only independent reactant/candidate starters. Check the exact source excerpts and noted conflicts.
2. Reproduce one relevant old baseline and the most decisive new competing control. Check saddle mode and bidirectional endpoints, or state/parameter identity for non-path analyses. Preserve failed/restarted jobs.
3. Complete every named panel and compare at common zeros. Run one decisive model/conformer/method perturbation. Establish experimental extraction error, numerical convergence and method spread before setting any numerical tolerance.
4. Calibrate real complete/supporting, complete/refuting-or-indistinguishable, old-only and wrong-state/reference submissions. Run AR independently without author answers; do not fabricate an autonomous search history from PR evidence.
5. Measure actual engine starts, allocations and scientific job time before setting a budget; matrix cell counts are not engine calls.

### Paper-specific pilot order

Before scientific release, resolve the unsupported transfer of the 1h back-quench explanation to 1a, establish a source-grounded network, and obtain independent rate constraints with explicit electron/reagent bookkeeping. Then test ODE conservation and mixer dilution with the measured grid, pre-register three held-out measured conditions, fit a shared temperature model and profile its identifiable combinations. No invented rate ranges or detection limits may fill the current input gap.

### Scientific adversarial calibration (not executed here)

Fit an unconstrained rate at every grid point, label the RBF surface mechanistic, use a held-out point during fit, or replace clogged/trace/n.d. with measured zero: reject.

After independent rates and sink identity are supplied, a rank-deficient but completely profiled model with valid holdout intervals is acceptable. Current missing inputs are not that scientific outcome.

## Callable software and limits

Use current chemistry_toolbox/README.md, config/mcp_profiles.yaml and config/native_software_guides.yaml: Gaussian/ORCA for molecular optimization, frequencies, TD/redox; pysisyphus/IRC or explicit mode following for paths; CREST/xTB only for preparation, not substitute final DFT barriers; Multiwfn for exported wavefunction analyses and Python/SciPy for audited arithmetic/ODEs. A specific method is not validated merely because its program is installed. NBO/PyFrag are optional if available. No new paid service, HPC job or long computation was launched here.

## Scope-specific failure checks

RBF interpolation called a mechanism; free rate per condition; fitting holdout data; inventing independent rate bounds; treating clogged observations as measured zeros.

## Phase1 source correction, 2026-09-28

A source/model-definition error is distinct from missing numerical rate constants. Treating an irreversible 1a loss surrogate Q as a source-established back-quench mechanism invalidates that interpretation. A faithful report of this unresolved gate remains bounded_failure, never scientific pass.
A real 8-start/12-profile diagnostic was run in the Group4 verification workspace. Its local rank and residuals do not calibrate microscopic kinetics; see that workspace source_gap_audit.json and report/verification_report.md. Earlier no-calculation statements above describe the original development pass.
