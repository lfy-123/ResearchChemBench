# Submission guide

Compare actual state character and SOC in the three sensitizers and determine whether a consistently defined rubrene energy-transfer cycle supports their proposed sensitization role.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `sensitizer_states`

Generate independent conformers for all sensitizers, validate S0 and calculate state-resolved energy, oscillator/NTO and SOC windows with root tracking.

Audit: Check complete graphs, cation charge and hole/electron localization on heavy atoms. Compare physically matched states; chemistry differences forbid attributing all changes exclusively to atom mass or position.

## `rubrene_energy_cycle`

Calculate independent rubrene S1/T1 and sensitizer T1 adiabatic energies and form the stated TTET and acceptor-annihilation balances.

Audit: Recompute rubrene and donor adiabatic energies under matching conditions. Do not subtract vertical donor states from adiabatic acceptor states or use different solvent corrections silently.

## `geometry_and_method_test`

Run the Cy2 planar/released intervention and a real SOC-method sensitivity; assess localized heavy-atom character and scope of any mechanistic inference.

Audit: Verify real SOC vectors, supported heavy-element operators, frozen geometry and state density overlap. More SOC or favorable TTET energetics does not by itself demonstrate a faster ISC/transfer process.

## Scientific failures

Reject wrong cation/counterion model, scalar-relativistic energy mistaken for SOC, Cy2 used as the annihilator instead of rubrene, mixed vertical/adiabatic references, or full efficiency/position-only causation from non-isostructural compounds.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.
