# Submission guide

Determine whether metal–ligand orbital mixing is needed to explain the Ir–Ir bonding response, using full and exactly truncated dimers, fixed fragment definitions and distance/twist interventions.

`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.

Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.

Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.

## `dimer_states`

Assemble full/truncated A,C dimers independently, test singlet/BS/triplet solutions and validate retained minima with spin/occupation evidence.

Audit: Check actual full/truncated graph/mapping, opposite-helicity starts, spin/occupation and curvature. Mononuclear energy differences are irrelevant to Ir–Ir bond validation. Do not force a source symmetry saddle into a minimum.

## `fragment_interventions`

Using the fixed neutral-doublet decomposition, calculate equilibrium and rigid distance/twist controls, fragment relaxation terms and density differences at both model sizes.

Audit: Recompute fragment arithmetic; no missing ligand/metal atoms or state-dependent reference swaps. Examine basis superposition and scalar/SOC Hamiltonian choices. An energy decomposition alone does not uniquely isolate pi causation.

## `bonding_evidence`

Compare orbital mixing, densities, bond indices and interaction response to identify which explanations survive truncation and method/fragment sensitivity.

Audit: Require correlated response to the explicit interventions in both model sizes and a real sensitivity. Accept direct-metal, ligand-assisted or indistinguishable explanations when evidence supports them; do not award a cartoon or single bond order as causal proof.

## Scientific failures

Reject one-Ir surrogates, Egan/egan/Hap truncations conflated, wrong fragment charge/spin, unsupported effective minima, or a unique pi-causality claim from a single bond index. A mononuclear isomer gap is not an Ir–Ir bond energy.

A `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.
