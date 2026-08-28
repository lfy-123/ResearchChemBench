# Scientific objective

Independently test the authors' qualitative proposal that Lewis-acid ligation can change the electron-accepting behavior of the explicitly specified isolated PAl12[B(C6F5)3]2 cluster while retaining its metal-core framework. Compute its adiabatic electron affinity (AEA) by comparing independently optimized neutral and singly anionic states. Report energies, structures, spin choices, and the sign/unit convention. Do not use a paper-reported coordinate, energy, AEA, or selected conformer as an input.

# Public inputs and scientific boundaries

Use `data/inputs/system_specification.json`. It uniquely specifies one P atom, twelve Al atoms, two intact neutral B(C6F5)3 ligands, the neutral charge-0 state and charge-1 state, and an isolated gas-phase boundary. You may generate 3-D conformers and computational models. No graphene, solvent, counterion, periodic cell, atom substitution, protonation, or omitted ligand is allowed. The author hypothesis to test is only that the ligand field may enhance electron acceptance and preserve the superatomic metal-core framework; no direction, magnitude, or winning structure is supplied.

# Required scientific validation/investigation

Choose and document a defensible electronic-structure method. Explore a finite, explicitly listed set of chemically distinct ligand orientations/binding-site arrangements and plausible spin multiplicities for both charge states. Deduplicate candidates using a stated structural criterion, optimize every advanced candidate, and retain energies and convergence information. Validate each selected endpoint as a stationary minimum with a frequency calculation or a clearly justified equivalent; report imaginary-mode results and any failed candidates. A complete investigation requires at least one independently generated starting geometry per state, a stated coverage table, and a stopping rule: stop when all initially enumerated site/orientation classes and tested multiplicities have been optimized and either frequency-validated or reported as failures. If computational limitations prevent that closure, submit a bounded-failure report with the attempted coverage and limitation. Compute AEA from the two validated endpoint energies, state whether ZPE is included, and separately assess whether the PAl12 core connectivity/framework is retained after optimization. Do not claim global-minimum status beyond the searched coverage.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method and software, atom ordering/mapping, candidate identities and validation context, endpoint structures or coordinate-file paths, neutral and anion energies, AEA with units and ZPE convention, coverage/stopping evidence, framework comparison, conclusion, and limitations. A bounded failure is acceptable only when all attempted calculations and missing closure are honestly documented.
