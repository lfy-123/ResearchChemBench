# Scientific objective

Compute the adiabatic electron affinity (AEA) of the isolated PAl12[B(C6F5)3]2 cluster by comparing independently optimized neutral and singly anionic states. Report energies, structures, spin choices, and the sign/unit convention. Do not use a paper-reported coordinate, energy, AEA, or selected conformer as an input.

# Author-provided scientific guidance

Independently test the authors' qualitative proposal that Lewis-acid ligation can change the electron-accepting behavior of the explicitly specified isolated PAl12[B(C6F5)3]2 cluster while retaining its metal-core framework.

# Public inputs and scientific boundaries

AEA = E(neutral minimum) − E(anion minimum), in eV. State whether ZPE is included and retain separate electronic and ZPE terms where computed; use a consistent convention for both charge states. Framework retention here means structural preservation of the specified PAl12 core and ligand connectivity, not an additional electronic-shell or superatom-orbital proof.

Use `data/inputs/system_specification.json`. It uniquely specifies one P atom, twelve Al atoms, two intact neutral B(C6F5)3 ligands, the neutral charge-0 state and charge −1 state, and an isolated gas-phase boundary. You may generate 3-D conformers and computational models. No graphene, solvent, counterion, periodic cell, atom substitution, protonation, or omitted ligand is allowed. The author hypothesis to test is only that the ligand field may enhance electron acceptance and preserve the superatomic metal-core framework; no direction, magnitude, or winning structure is supplied.

# Required scientific validation/investigation

Choose and document a defensible electronic-structure method. Explore a finite, explicitly listed set of chemically distinct ligand orientations/binding-site arrangements and plausible spin multiplicities for both charge states. Deduplicate candidates using a stated structural criterion, optimize every advanced candidate, and retain energies and convergence information. Validate each selected endpoint as a stationary minimum with a frequency calculation or a clearly justified equivalent; report imaginary-mode results and any failed candidates. A complete investigation requires at least one independently generated starting geometry per state, a stated coverage table, and a selection record. If computations prevent that closure, submit the attempted coverage and specific failure diagnostics. Compute AEA from the two validated endpoint energies, state whether ZPE is included, and separately assess whether the PAl12 core connectivity/framework is retained after optimization. Support the selected lowest-energy structures with the actual candidate energies and structural checks; additional exploration is allowed.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to `submission_schema.json`. Include method and software, atom ordering/mapping, candidate identities and validation context, endpoint structures or coordinate-file paths, neutral and anion energies, AEA with units and ZPE convention, calculation coverage evidence, framework comparison, conclusion. A bounded failure is acceptable only when all attempted calculations and missing closure are honestly documented.
