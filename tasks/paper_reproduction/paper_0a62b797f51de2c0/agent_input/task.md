# Scientific objective

Independently test the authors' qualitative edge-activation hypothesis: increasing electron-withdrawing cyano substitution on the thiophene building block should alter charge polarization. For the three public monomers, compute optimized neutral-singlet ground-state structures, dipole moments, and a clearly defined electrostatic-potential asymmetry. Report the direction and strength of the substitution trend, and distinguish calculated evidence from interpretation. A three-repeat-unit polymer-fragment extension is optional and must be identified separately.

# Public inputs and scientific boundaries

Use `data/inputs/monomer_series.json`. It defines M-Th-0CN (2,5-dibromothiophene), M-Th-1CN (2,5-dibromo-3-cyanothiophene), and M-Th-2CN (2,5-dibromo-3,4-dicyanothiophene) by SMILES, with charge 0 and multiplicity 1. The physical boundary is isolated neutral closed-shell ground-state molecules; no solvent, periodic polymer, excited-state, photochemical, or experimental calculation is required. The measured quantities are dipole moment (D) and electrostatic-potential asymmetry/potential difference (state units and the exact extrema, surface, grid, or other convention). Do not use the paper, SI, general web, or source-derived coordinates.

# Required scientific validation/investigation

Generate at least one reproducible 3-D starting geometry per molecule, optimize each structure, and document software, method, basis, charge, multiplicity, convergence, and whether a stationary-point/frequency or equivalent validation was performed. Deduplicate materially different optimized conformers using a stated structural criterion; if multiple conformers remain, calculate/report the selected conformer and coverage/selection rationale. Calculate dipoles and ESP asymmetry for all three named molecules using one consistently stated convention. Validate atom identity/connectivity and report failures or unavailable observables honestly. The calculation is complete when every molecule has either a validated result or a bounded, explicitly explained failure, and the report contains a cross-series comparison. Stop after the stated conformer/validation coverage is exhausted or after the agent documents why further searches would not change the conclusion; do not claim exhaustive conformer sampling without evidence.

# Deliverables

Submit `report/results.json` plus any files needed to substantiate it. The JSON must contain per-molecule identity, structures or structure-file paths, method metadata, dipole and ESP results when available, validation evidence, uncertainty/limitations, and a conclusion about how cyano count changes polarization. If the optional polymer extension is performed, keep it in a separate field and define its fragment identity. A bounded-failure branch is allowed only with molecule-specific reasons and completed work recorded.
