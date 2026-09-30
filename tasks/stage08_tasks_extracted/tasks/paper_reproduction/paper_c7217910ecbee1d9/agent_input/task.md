# Scientific objective

Compute the adiabatic electron affinity (AEA) of the explicitly specified isolated PAl12[B(C6F5)3]2 cluster by independently locating and validating suitable neutral and singly anionic electronic states. Determine whether the optimized states preserve the specified PAl12 metal-core framework. Report a reproducible computational conclusion with uncertainty and search limitations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that attaching two neutral B(C6F5)3 Lewis-acid ligands can substantially alter the electron-accepting behavior of the PAl12 cluster while preserving its superatomic metal-core framework. This is a qualitative claim to test for the specified isolated cluster; it does not determine the sign or magnitude of the computed AEA.

**Candidate route or mechanism.**
Prioritize testing structures in which the two intact Lewis-acid ligands bind at chemically distinct sites or orientations around the PAl12 core, including arrangements that place the ligands on different portions of the core versus on related sites. Compare plausible neutral and singly anionic electronic states and assess whether ligand-induced charge redistribution accompanies retention or distortion of the metal-core connectivity.

**Discriminating evidence.**
Use optimized, frequency-validated endpoint energies for the neutral and anion to obtain the AEA, together with spin-state and site/orientation comparisons. Distinguish the claim using core connectivity and geometry metrics, charge or population analysis, and electronic-structure indicators such as frontier orbital or superatomic-shell character; stability checks can support whether the retained framework is persistent.


# Public inputs and scientific boundaries

Use `data/inputs/system_specification.json`. It uniquely specifies one P atom, twelve Al atoms, two intact neutral B(C6F5)3 ligands, the neutral charge-0 state and charge-1 state, and an isolated gas-phase boundary. You may generate 3-D conformers and computational models. No graphene, solvent, counterion, periodic cell, atom substitution, protonation, or omitted ligand is allowed. No author route, candidate ranking, result direction, or reference numerical result is part of this task.

# Required scientific validation/investigation

Propose and justify your own candidate-generation strategy for ligand orientations/binding-site arrangements and plausible spin multiplicities for both charge states. Explore a finite, explicitly listed set, deduplicate with a stated structural criterion, optimize advanced candidates, and retain energies and convergence information. Validate each selected endpoint as a stationary minimum with a frequency calculation or clearly justified equivalent; report imaginary-mode results and failed candidates. Completion requires at least one independently generated starting geometry per state, a coverage table, and a stopping rule: stop when your declared candidate-generation classes and tested multiplicities are exhausted, or provide a bounded-failure report explaining what prevented closure. Compute AEA from validated endpoint energies, state ZPE treatment, compare the optimized core connectivity/framework with the public specification, and distinguish computed facts from hypotheses. Do not claim global-minimum status beyond the searched coverage.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include your scientific rationale, method/software, atom ordering/mapping, candidate identities and validation context, endpoint structures or coordinate-file paths, neutral and anion energies, AEA with units and ZPE convention, coverage/stopping evidence, framework comparison, final conclusion, and limitations. A bounded failure is acceptable only when all attempted calculations and missing closure are honestly documented.
