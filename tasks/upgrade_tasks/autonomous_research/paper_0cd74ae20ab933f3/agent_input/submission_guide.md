# Submission guide

Determine whether axial-pyridine substitution changes exchange primarily through electronic effects or core geometry, and whether the H/Me/OMe ranking survives the uncertainty of the spin treatment.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `exchange_matrix`

Construct the mapped series and evaluate relaxed triplet references plus common-core controls, retaining S2 and spin-density evidence for singlet/BS and triplet states. Report projected exchange, population and core distances.

Audit: Resolve six correct matched geometries and associated triplet and singlet/BS outputs. Recompute projection, J and P_T using degeneracy 3. Check S2, Cu2O8 mapping and local spin distributions. Compare common-core versus relaxed substitution differences; multiple spin contaminations cannot be treated as the same unprojected gap.

## `spin_calibration`

Before expanding the series, calibrate the R_H spin gap at a common geometry using an available high-level/spin-adapted route and document the active orbitals and numerical stability.

Audit: Inspect actual higher-level output, state/root identities, occupations and active-space completeness. CASSCF(2,2) is a starting calibration, not a guaranteed converged correlation reference. Do not claim the paper-specific PySCF-forge implementation exists without evidence.

## `effect_comparison`

Compute the substituent differences at both geometrical regimes and the method-sensitive comparison of the closest pair. Decide what the intervention resolves about ligand electronics.

Audit: Differences derive from the named exchange matrix. Uncertainty includes method/projection and geometry sensitivity. Accept ties or reversals when supported; do not force a few-cm^-1 ordering despite larger uncertainty.

## Scientific failures

Reject incorrect paddlewheel stoichiometry, wrong J sign/factor, missing triplet degeneracy, unprojected differently contaminated BS energy differences, or declaring material thermochromism from the isolated dimer.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.
