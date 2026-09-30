# Submission guide

Test whether donor type and placement alter singlet–triplet proximity through charge-transfer localization, geometric relaxation or both, while retaining optically active states.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `vertical_matrix`

Generate independently initialized conformers, build the common torsion intervention, and calculate energies, oscillator strengths, fragment-resolved transition densities and SOC for matched low states in all six cells.

Audit: Check graph and donor position rather than inconsistent SI product prose. Recompute gaps, fragment weights and SOC norms. State roots must be tracked by densities. A small gap alone is not mechanistic proof.

## `relaxation_matrix`

Follow S1 and T1 relaxation for each member and explicitly separate vertical and adiabatic gaps. Preserve conformer and root-switch diagnostics.

Audit: Verify S1/T1 energies and geometries on consistent surfaces; inspect conformer outcomes. A collapsed state must be evidenced and alternative starts examined; no invented state minimum.

## `causal_comparison`

Compare changes at site 11 and sites 3/6, then quantify the shift from fixed to relaxed torsions and a decisive method sensitivity. Evaluate both CT-based and geometry-based explanations.

Audit: Use like-defined transition observables at common conditions. Report what fixed torsion does and does not isolate; multiple donor replacements are not equivalent to a single-site substitution. Require a CT-sensitive method or solvent sensitivity with actual calculations.

## Scientific failures

Reject swapped CD/TD donor layouts, unequal state/solvent definitions, root-index-only matches, missing SOC or oscillator evidence, or an OLED efficiency claim based solely on a molecular gap.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.
