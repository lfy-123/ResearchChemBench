# Submission guide

Test how host size and guest stoichiometry change low optical excited-state character, separating the contribution of confined guest geometry from interguest coupling and the explicit host response.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `host_matrix`

Build and validate both complete host–guest systems from independent placements; calculate state-resolved optical properties before and after frozen host deletion.

Audit: Verify chemical stoichiometry/charge and exact guest-coordinate identity. Compare actual TD/density outputs and states, not labels assigned from an emission cartoon.

## `coupling_controls`

Perform the four frozen partner-deletion controls and relaxed isolated monomer/dimer baselines. Preserve mappings, placements, raw TD vectors and transition densities.

Audit: Single guests have charge +2; two guests +4. Keep host and retained guest coordinates fixed on deletion. For monomers bright/dark are the selected lowest optically active/inactive states, not fictitious exciton partners; explicitly state if no suitable dark state occurs in the calculated window.

## `mechanism_comparison`

Compare host response, guest–guest coupling and geometric confinement with a common state definition, and quantify one basis/solvent/placement sensitivity.

Audit: Require density-based state correspondence and quantitative differences. An isolated dimer splitting alone cannot establish host causality. Full-host deletion includes electrostatics, polarization and exchange; pure electrostatic attribution requires an additional frozen-charge control, which is optional.

## Scientific failures

Reject wrong host ring size/guest charge, source bound coordinates used as discovered minima, comparisons with relaxed versus frozen geometries silently mixed, or calling total host response exclusively electrostatic. Static transition properties do not prove fluorescence quantum yield.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.
