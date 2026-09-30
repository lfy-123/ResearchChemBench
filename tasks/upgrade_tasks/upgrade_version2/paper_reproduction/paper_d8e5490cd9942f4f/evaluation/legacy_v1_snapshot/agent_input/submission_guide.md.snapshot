# Submission guide

Test whether La/Tb/Lu conformer preferences are explained by metal replacement, structural relaxation or explicit coordination water within a controlled 4f-core molecular model.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `conformer_hydration_matrix`

Use and verify the supplied exact ECP/basis files in the selected engine, then validate dry/hydrated syn/anti models for all metals and report matched thermochemistry with collapse evidence where appropriate.

Audit: Verify exact ECP coefficients/core counts/explicit electron counts and original ligand charge. Inspect frequencies, qRRHO and standard states. A lost-water endpoint is an evidenced collapse/separated limit, not a falsely bound minimum.

## `replacement_and_cycles`

Calculate dry frozen La-skeleton metal replacements and matched water-addition cycles; separate relaxation and hydration contributions to within-metal preferences.

Audit: Recompute every balanced difference and cycle. Cross-metal raw total energies or unbalanced water counts cannot support selectivity. Frozen states use E only.

## `ecp_and_sensitivity`

Audit ECP/basis electron counts and repeat the decisive low-frequency or solvation choice. Explain conformational trends only within the validated model.

Audit: Audit source numerical ECP/basis and pseudo-spin before interpreting comparison. Install reports are not coefficient or pilot evidence. Check low-frequency sensitivity against small conformer gaps; do not transfer old La tolerance to Tb/Lu/hydration.

## Scientific failures

Reject small-core/all-electron calculations called equivalent without calibration, real Tb singlet claims from pseudo-spin, wrong ligand charge, cross-metal total-energy selectivity, unbalanced hydration or duplicated thermal corrections.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.
