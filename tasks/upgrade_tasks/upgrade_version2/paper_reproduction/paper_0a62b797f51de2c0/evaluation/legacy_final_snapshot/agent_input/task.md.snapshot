# Scientific objective

Independently test the authors' qualitative edge-activation hypothesis: increasing electron-withdrawing cyano substitution on the thiophene building block should alter charge polarization. For the three public monomers, compute optimized neutral-singlet ground-state structures, dipole moments, and a clearly defined electrostatic-potential asymmetry. Report the direction and strength of the substitution trend, and distinguish calculated evidence from interpretation. A three-repeat-unit polymer-fragment extension is optional and must be identified separately.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that electron-withdrawing cyano groups positioned opposite the electron-rich sulfur side of the thiophene building block create opposing electron-rich and electron-deficient sectors, strengthening molecular polarization.

**Candidate route or mechanism.**
Consider redistribution of ground-state electron density between the thiophene and cyano regions as a candidate explanation for substitution-dependent dipole and ESP asymmetry. The proposed edge-activation picture links the spatial arrangement of these regions to a molecular dipole field.

**Discriminating evidence.**
The authors use DFT geometry optimization followed by dipole calculations and spatial MESP maps to examine this picture. Compare the dipoles and the locations and separation of electrostatic-potential regions across the substitution series to assess whether they support the proposed spatial polarization.

# Public inputs and scientific boundaries

Use `data/inputs/monomer_series.json`. It defines M-Th-0CN (2,5-dibromothiophene), M-Th-1CN (2,5-dibromo-3-cyanothiophene), and M-Th-2CN (2,5-dibromo-3,4-dicyanothiophene) by SMILES, with charge 0 and multiplicity 1. The physical boundary is isolated neutral closed-shell ground-state molecules; no solvent, periodic polymer, excited-state, photochemical, or experimental calculation is required. The measured quantities are dipole moment (D) and electrostatic-potential asymmetry/potential difference (state units and the exact extrema, surface, grid, or other convention). Do not use the paper, SI, general web, or source-derived coordinates.

Use the electrostatic potential for a positive unit test charge and identify the actual molecular regions used for each reported minimum, maximum or potential difference. Declare the density isosurface or spatial grid, units and regional statistic consistently across the three monomers. Donor/acceptor labels and electron-density values are not substitutes for the signed electrostatic potential.

# Required scientific validation/investigation

Generate at least one reproducible 3-D starting geometry per molecule, optimize each structure, and document software, method, basis, charge, multiplicity, convergence, and whether a stationary-point/frequency or equivalent validation was performed. Deduplicate materially different optimized conformers using a stated structural criterion; if multiple conformers remain, calculate/report the selected conformer and coverage/selection rationale. Calculate dipoles and ESP asymmetry for all three named molecules using one consistently stated convention. Validate atom identity/connectivity and report failures or unavailable observables honestly. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` plus any files needed to substantiate it. The JSON must contain per-molecule identity, structures or structure-file paths, method metadata, dipole and ESP results when available, validation evidence, and a conclusion about how cyano count changes polarization. If the optional polymer extension is performed, keep it in a separate field and define its fragment identity. A bounded-failure branch is allowed only with molecule-specific reasons and completed work recorded.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
