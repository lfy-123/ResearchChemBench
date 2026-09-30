# Scientific objective

Identifiability of a finite carbenoid competition network. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Author-provided scientific guidance

The source interprets temperature/time competition between generation and degradation; the yield surface is RBF interpolation (SI p6), not a fitted mechanistic model. B3LYP-D3/6-311+G(d,p), SMD THF potentials versus Fc are a thermochemical baseline (SI p19). This benchmark adds an independently parameterized, falsifiable kinetic model and identifiability testing. Neither reduction potentials nor RBF interpolation supply rate constants.

# Public inputs and scientific boundaries

Use precursor 1a in THF to investigate Li-naphthalenide generation, MeOH capture and decomposition/rearrangement. SI p5: 0.050 M substrate at 10 mL/min mixed with 0.30 M LiNp at 5 mL/min; the first reactor has substrate 1/30 M and LiNp 0.10 M. MeOH 0.30 M at 5 mL/min is added downstream. Treat reactor dilution explicitly. The source contour has 23 measured grid positions and two clogged/missing positions; interpolation is not an observation. The measured rearrangement product is 2-methylbenzenemethanethiol 3a, obtained after quenching its thiolate. Source correction: main pp4-5 discusses a quench pathway returning to starting material for the SPh-leaving precursor 1h. It does not establish an irreversible A -> Q back-quench sink for the 1a grid. The originally proposed S -> A, A -> D, A -> Q, A + MeOH -> P model may be used only as an explicitly unvalidated diagnostic hypothesis; its Q channel is not an author-identified process. Release remains blocked by this source/model-definition mismatch as well as missing independent rate constraints and unresolved microscopic species/reservoir bookkeeping. Retaining the diagnostic does not resolve the intended mechanistic network.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

**Development input gate — blocked.** Obtain independent generation/back-quench/rearrangement/capture rate intervals or validated barriers. The supplied measured grid and old reduction potentials cannot identify those rates without independent constraints. Resolve the source/model-definition mismatch before assigning a back-quench channel to 1a. Main pp4-5 discusses 1h/SPh and return to starting material; it supplies neither an irreversible 1a sink nor an identified elementary reverse step. Do not assert that a 1a back-quench channel exists or retain Q as established chemistry. A justified network and its charge/electron/reagent bookkeeping require independent evidence; source 3a identifies a quenched rearrangement product but not its channel rate. Keep the development gate blocked pending source-grounded resolution; any scientific scope change requires coordinator review. This package defines the completed development contract, but the scientific task must not be released as runnable until those items are supplied. A bounded failure can document the missing data; it cannot pass the intended expanded science.

# Required scientific validation/investigation

Write the mass-balance ODE and dilution maps, link every parameter range to independent measurement or validated pathway, and distinguish a lumped loss channel from a chemically identified product.

Fit shared temperature dependence only where identifiable, use profile likelihood or a rank/sensitivity analysis, and propagate independent parameter ranges. Do not fit an independent rate to each condition.

Hold out complete time/temperature conditions before fitting, report interval predictions and residuals, and distinguish evidence-backed non-identifiability from missing inputs.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: Full flow optimization and C-class pathway discovery are optional future work.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `network`: Conserved finite reaction model and independent rate intervals.
- `identifiability`: Numerical sensitivity/rank and parameter profiles; honest bounded ambiguity is allowed after complete analysis.
- `holdout`: Predictions for three genuinely held-out measured conditions, with clipping/missingness retained.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
