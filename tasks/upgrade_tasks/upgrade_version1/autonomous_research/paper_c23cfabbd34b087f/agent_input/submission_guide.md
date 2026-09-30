# Submission guide

Determine how backbone topology and substituent changes affect open-shell character and low-energy optical states, separating relaxation and electronic effects with matched scaffolds and spin diagnostics.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `relaxed_series`

Build all four structures and evaluate stable CS, BS and triplet alternatives with conformer/collapse evidence; calculate matched low optical states in a consistent medium.

Audit: Verify source model graphs, H counts and neutral spin spaces; inspect stability/occupation and TD evidence. The former 1M-TIPS geometry was not a new minimum validation.

## `frozen_scaffold`

Generate common-scaffold interventions for both substitution pairs using the public mapped graph correspondence and evaluate electronic-state differences without borrowing equilibrium thermal corrections.

Audit: Check exact retained common scaffold coordinates and fragment valence; compare effects within each topology first. Frozen BS collapse is documented in its record, not a fabricated distinct solution.

## `calibrated_interpretation`

Select one ambiguous representative by a recorded rule, perform independent spin calibration, and quantify topology/substituent/relaxation effects with a method sensitivity.

Audit: Cross-check occupations, spin gaps and optical state character against an independent electronic model. An unrestricted instability or large oscillator strength does not alone prove a diradical assignment or experimental spectrum.

## Scientific failures

Reject confusing full TIPS with SiH3 truncation, using oxidized 2M-prime as a conformer, raw cross-formula total-energy rankings, unvalidated BS minima or unsupported TD certainty under strong multireference character.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.
