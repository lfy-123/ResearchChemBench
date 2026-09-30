# Submission guide

Discover which bounded protonation/tautomer candidates, or mixtures, can jointly explain the measured acid/base optical and NMR response of 2a, while testing solvent and proton-reference sensitivity.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `candidate_registry`

Construct the supplied site and tautomer alternatives, add further symmetry-distinct candidates only when motivated, and document conformers, charges and bond/proton maps without presupposing the acid/base assignment.

Audit: Check charges, H counts, mapping, candidate classes and actual attempted geometries. Both acid and base must contain distinct site/bond alternatives; source endpoint relabeling is insufficient. Evidenced collapse may close a candidate, but missing convergence cannot.

## `joint_evidence`

Calculate matched-solvent NMR and UV predictions for all retained competitors; test individual and bounded-mixture interpretations with one uncertainty policy.

Audit: Check measured observations and the different NMR/optical solvent conditions. All retained competing acid/base candidates require both predictions under identical predeclared calibration; collapse must be evidenced, not counted as a missing spectrum. Include neutral-parent NMR calibration. The neutral experimental UV maximum is not supplied: use null for that observation/residual, never an invented value. Reject treating author-calculated shifts as measurements.

## `thermodynamic_and_robustness`

Close proton-reference cycles, compare populations consistently and repeat the decisive solvent/reference/model choice. Report only assignments supported jointly by both observations.

Audit: Recompute cycle energies, charge/proton balances and populations. Gas-phase dianion artifacts do not invalidate a solvated state or prove it stable; distinguish electron binding, solvation and proton equilibria. Accept supported ambiguity after the complete candidate/spectral comparison.

## Scientific failures

Reject answer geometries as discovered candidates, unequal atom counts without balanced cycles, source calculated shifts passed off as measurements, fitting each observable to unrelated species without a population model, or gas dianion failure called proof of solution instability.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.
