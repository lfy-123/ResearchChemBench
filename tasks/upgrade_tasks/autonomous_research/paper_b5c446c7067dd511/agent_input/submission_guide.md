# Submission guide

Determine whether proposed high-triplet singlet-transfer channels remain plausible after direct SOC, neighboring-state competition and geometric/method controls across the source emitter series.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `series_states`

Calibrate Ph-mP and An-mP first, then calculate the four-member window with states, oscillator strengths, transition densities and actual SOC pairs.

Audit: Check actual SOC matrix and NTO outputs; fragment weights must normalize consistently. Do not assume author Tn labels remain physical states when method or geometry changes.

## `representative_controls`

For the two representatives enlarge the root set and repeat the fixed 45-degree terminal torsion, recording state overlap and changed gaps/couplings.

Audit: Require independent enlarged-window and frozen-torsion outputs. Root permutation is handled through state-density matching, not forced energy ordering.

## `channel_competition`

Compare each representative candidate against neighboring triplets and a CT-sensitive method contrast; state what necessary conditions are supported and which kinetics remain unknown.

Audit: Compare direct coupling, energy proximity and state character together. Adjacent triplet internal conversion can compete even when S1/Tn gaps are small; its rate is not computed by a spacing. Accept rejection/ambiguity after the required evidence.

## Scientific failures

Reject high-state selection solely by author index, absent SOC outputs, mismatched geometries/solvents, non-normalized fragment populations or a rate/efficiency inferred from a small gap alone.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.
