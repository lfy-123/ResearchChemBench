# Scientific objective

Reproduce the authors' gas-phase geometry-comparison route for compound 7a using B3LYP and CAM-B3LYP, both with 6-311+G(d,p). The object is the isolated neutral singlet E-imine, N5-H thione C20H17ClN6OS. Compare actual validated structures with the supplied experimental observations and reach an evidence-supported method comparison within the computed conformers.

# Author-provided scientific guidance

Test the qualitative hypothesis that gas-phase DFT describes the experimental molecular geometry and that a range-separated hybrid can improve the agreement. Use the primary method pair above; other methods are supplementary, not replacements. No author numerical result, optimized coordinate, or winning ranking is provided. Completing this calculation comparison and supporting the author hypothesis are distinct: a valid mixed result can complete the task without establishing a universal method preference.

# Public inputs and scientific boundaries

Use `data/inputs/molecule.json` for complete molecular identity, including E-imine geometry at C17=N3 (C8 and N4 on opposite sides), neutral charge, singlet state and N5-H thione. The mapped SMILES specifies identities, not coordinate row numbers. Single-bond conformations are not prescribed.

Use `data/inputs/atom_map.json` for the 13 bond, 23 unique angle and 11 torsion selectors; Cl1/Cl2 name the same chlorine. `data/inputs/experimental_geometry.csv` contains only the experimental comparison observations. `data/inputs/geometry_comparison.json` defines the complete calculation-independent comparison convention, including signed torsions and whole-molecule inversion equivalence.

Generate starting 3D coordinates independently. Experimental crystal coordinates, author-computed geometry columns and private verification results are not authorized inputs. Do not read the paper, SI, hidden evaluator/reference files or general web. The physical model is an isolated gas-phase molecule, not a periodic crystal. No experimental FT-IR comparison, packing, biological activity or global conformer search is required.

# Required scientific validation/investigation

Use B3LYP/6-311+G(d,p) and CAM-B3LYP/6-311+G(d,p) for the primary pair, without solvent, empirical dispersion or geometric constraints. Use the same independently generated initial conformer for a comparable primary pair, then optimize independently with each model. Report the starting and final coordinate artifacts and actual method, basis, environment and numerical settings. Verify the correct graph, E-imine, N5-H tautomer, charge and multiplicity. Establish converged local minima using frequency/Hessian evidence, or an explicit scientifically equivalent stationarity test. A normal exit alone is insufficient. Additional starts are allowed but not mandatory; retain their outcomes without selecting one retrospectively to manufacture a winner.

Preserve a whole-molecule source-label mapping, with per-model row maps when ordering changes. Extract all 47 unique observables per model from the actual optimized coordinates. Keep raw signed torsions in selector order. Do not take their individual absolute values, change atom labels row by row, substitute experimental numbers for computed ones or omit unfavorable rows.

Apply the public comparison protocol. For each complete model, compare its full 11-torsion vector with both the supplied reference vector and its global sign inverse. Select one sign for the entire vector by minimum summed squared circular error, then the specified MAE/tie rule. Report both branch summaries and the selected sign. This is a representation convention, not a new geometry or a per-row choice. Calculate bond/angle errors normally; use the selected branch for torsion MAE/RMSE. Report MAE and RMSE separately for the 13/23/11 rows; never combine Angstrom and degree errors into an undeclared global score.

Compare the actual per-kind metrics. A uniform preference, a mixed comparison or a tie within the public reporting precision can all be scientifically complete when supported by valid full-coverage calculations. Do not interpret a conformer-specific ranking as universal. If models land in different basins, identify that the observed difference contains both method and conformer effects. Missing/failed calculations are not evidence for a mixed result.

# Deliverables

Submit `report/results.json` conforming to the schema, with model records, starting/final coordinate and raw-output references, mapping, all observations, six metric records for a two-model comparison, the global-inversion records, and a structured primary-pair comparison plus a concise evidence-based conclusion. The evaluator checks actual geometry and arithmetic, not agreement with a hidden preferred method.

Use `complete` only when the primary comparison and all 47 rows for each reported primary model are validated. Use `bounded_failure` for missing/failed calculations, retaining real partial results and row-specific reasons. Incomplete full-set metrics are null, never zero; do not label them as a complete mixed result. Optional extra analyses or a generic limitations paragraph are not required and earn no independent points.

Submission organization: `models`, `observables`, `metrics` and `inversion_comparison` contain only the declared primary pair's available results; `comparison.model_pair` identifies that pair. Put failed/not-started primary attempts, earlier failed retries and supplementary models or starts in the optional `attempts` array. Each attempt states `model`, `role` (`primary` or `supplementary`) and `status` (`completed`, `failed` or `not_started`); failed/not-started attempts require a `reason`. Link only real files in `artifacts`; a completed supplementary attempt requires artifact evidence and may link a separate `result_file`. Do not put supplementary records into the primary arrays. An additional failed attempt does not invalidate an otherwise complete primary comparison, and a successful retry may coexist with its earlier failure record.

For `bounded_failure`, keep zero, one or two primary model records for which actual geometry/artifacts are available. A required model that has not produced those outputs belongs in `attempts`, not a fabricated model record. If nothing is available, use `models: []`, `observables: []`, `metrics: []` and `mapping: null`; keep the intended model names already chosen in `comparison.model_pair`, which may be empty only if no selection was made. Once a primary model or numerical observable is reported, provide its real mapping. Explain the missing work in `failure_reason` and set `comparison.overall` to `unresolved_incomplete`; retain any supported per-kind results. Do not invent coordinates, mapping rows, output paths or numerical values just to fill fields. This permits an honest report, not a claim of task completion or full scientific credit.
