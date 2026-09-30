# Submission guide

The schema is the exact field contract. A JSON-valid submission is not a scientific PASS.

Each `calculation_records` entry identifies a real input, raw log, method, object, charge/spin and job. A `minimum` or `transition_state` needs the corresponding geometry and state/curvature evidence. `constrained_diagnostic` is never a free minimum. Electronic energy is hartree; the thermal G correction includes ZPE, so G=E+thermal_G_correction without adding ZPE twice. For a composite method retain both constituent jobs and the exact assembly equation. Every record ID in a panel must resolve, and every cited evidence file must contain the claimed data.

For every path, report local and common separated-reactant/reservoir reference, all spectators, temperature and standard state. `gibbs_barrier_kcal_mol` uses the common reference; `preorganization_G_kcal_mol` is immediate-precursor minus that reference. Recover the local barrier by subtraction. Electrode/proton terms are needed only when stoichiometry changes. Do not compare raw total energies between different formulas or electronic states. A validated saddle requires its negative frequency, actual displacement and both endpoint artifacts. `evidenced_collapse`/`evidenced_no_distinct_saddle` requires a sampled profile and explicit exclusions; no fictitious zero barrier is required.

`PAIR`-style comparisons use right-minus-left and require numeric operands, source IDs and the common definition. For strain/interaction panels, strain = (E_A_frozen−E_A_relaxed)+(E_B_frozen−E_B_relaxed); interaction=E_AB−E_A_frozen−E_B_frozen; total=E_AB−E_A_relaxed−E_B_relaxed. Convert hartree consistently, state counterpoise and fragment charge/spin, and report the closure residual. Compare identical reaction progress.

Sensitivity difference = alternative−baseline from genuinely different settings. Hypotheses must cite discriminatory evidence, not merely restate the prompt. A failed launched calculation may omit uncomputed result panels but requires `failure_report`, its actual raw attempt logs and `conclusion.assessment=incomplete`. A pre-engine input or capability gate instead uses `failure_report.stage=pre_engine`, `calculation_records=[]`, `methods={}`, actual diagnostic files, the missing endpoints and a specific cause. All scientific job counters, core allocations and job/core hours must be zero; elapsed preparation time may be nonzero. Do not submit uncomputed result panels, hypotheses or sensitivity, and do not fabricate a calculation input or log. Both failure forms are admissible diagnostics and cannot earn scientific completion. Do not fill missing values with guessed numbers. Evidence paths may begin with `./` or contain harmless `./` segments; absolute paths and any `..` segment are forbidden.

For `comparison_outcome=numeric_difference`, all numeric operands are required. `same_basin_after_evidenced_collapse` permits omission of nonexistent separate energies only with independent search records, mapped retained-basin evidence and complete profiles. It is not available merely because a solver failed. In a multistep path, `sequence_segments` must cover all chemically necessary transformations and the effective-maximum ledger must place every segment on one starting inventory; the outer path identifies the controlling segment, without summing activation barriers. For candidate exclusions/collapse, supply the mapped exclusion trace instead of an invented relative G.

## `HH_formation`

Connected H–H formation saddle and bound-H2 endpoint.

## `release_and_recoordination`

Real separated and re-ligated states, not relabelled eta2-H2.

## `standard_state_control`

Explicit H2 pressure and gas/solute standard-state conversions.
