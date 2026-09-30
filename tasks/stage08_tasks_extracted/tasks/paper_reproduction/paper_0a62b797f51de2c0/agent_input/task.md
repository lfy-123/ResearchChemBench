# Scientific objective

Determine computationally how adding zero, one, or two cyano substituents to the explicitly supplied dibromothiophene series changes molecular dipole moment and electrostatic-potential asymmetry. Formulate and test your own explanation of any trend. Report calculated evidence, uncertainty, and the limits of inferring charge-transfer behavior from these ground-state observables.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that electron-withdrawing cyano groups positioned opposite the electron-rich sulfur side of the thiophene building block create opposing electron-rich and electron-deficient sectors, strengthening molecular polarization.

**Candidate route or mechanism.**
Consider redistribution of ground-state electron density between the thiophene and cyano regions as a candidate explanation for substitution-dependent dipole and ESP asymmetry. The proposed edge-activation picture links the spatial arrangement of these regions to a molecular dipole field.

**Discriminating evidence.**
The authors use DFT geometry optimization followed by dipole calculations and spatial MESP maps to examine this picture. Compare the dipoles and the locations and separation of electrostatic-potential regions across the substitution series to assess whether they support the proposed spatial polarization.

# Public inputs and scientific boundaries

Use `data/inputs/monomer_series.json`. It defines M-Th-0CN (2,5-dibromothiophene), M-Th-1CN (2,5-dibromo-3-cyanothiophene), and M-Th-2CN (2,5-dibromo-3,4-dicyanothiophene) by SMILES, with charge 0 and multiplicity 1. The boundary is isolated neutral closed-shell ground-state molecules. Solvent, periodic polymer, excited-state, photochemical, and experimental claims are outside scope. Measure dipole moment (D) and a precisely defined ESP asymmetry/potential difference, including units and the extrema/surface/grid convention.

# Required scientific validation/investigation

Plan an independent calculation for all three named molecules. Generate and, where useful, compare conformers; state deduplication, selection, and coverage criteria. Document geometry and electronic-state validation, software/method/basis, convergence, and reproducibility metadata. Calculate both observables consistently, preserve molecule identity in every result, and explain disagreements or failed calculations. Completion requires a validated result or a molecule-specific bounded failure for each molecule, plus an evidence-based cross-series conclusion. Stop when the documented conformer and validation search is exhausted or when additional work is unlikely to change the stated conclusion; report that limitation rather than implying exhaustive search.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`, and supporting artifacts. Include per-molecule identity, structure or path, method metadata, dipole and ESP results when available, validation records, uncertainty/limitations, and your independently reasoned conclusion. Optional polymer calculations must be clearly separated and must define their structures; they are not required for completion. Bounded failure is acceptable only when molecule-specific reasons and all completed validation work are reported.
