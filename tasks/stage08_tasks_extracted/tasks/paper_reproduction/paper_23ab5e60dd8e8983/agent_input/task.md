# Scientific objective

Independently determine the HOMO and LUMO energies and fragment localization of the fixed neutral zwitterionic singlet NI(O)-Qu chromophore, then decide whether the computed donor/acceptor pattern supports an intramolecular charge-transfer interpretation of a long-wavelength transition.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors use the deprotonated merocyanine NI(O)-Qu form to support the qualitative hypothesis that the long-wavelength optical transition has intramolecular charge-transfer character, with electron density moving from the hydroxynaphthalimide donor region toward the N-methylquinolinium acceptor region.

**Candidate route or mechanism.**
The proposed electronic picture is a donor-to-acceptor change between those two structural regions across the styryl-linked chromophore: the hydroxynaphthalimide portion supplies the donor character and the quinolinium portion supplies the acceptor character. Treat this as a candidate interpretation to test for the specified molecule.

**Discriminating evidence.**
Use frontier-orbital energies together with fragment-resolved HOMO and LUMO localization, supported by reproducible orbital images, cube files, populations, or equivalent analysis. Compare the localization pattern with the assignment of the long-wavelength transition to determine whether the proposed ICT interpretation is supported.

# Public inputs and scientific boundaries

Use `data/inputs/ni_o_qu.smiles` and `data/inputs/system.json`. The molecule is the explicitly specified E-styryl NI(O)-Qu constitution, formula C26H19N2O5, net charge 0, multiplicity 1, with phenoxide anion and N-methylquinolinium cation. The naphthalimide, quinolinium and linker fragments are defined in `system.json`. The physical system is one isolated molecule; no iodide, explicit solvent, biomolecule or crystal is part of the target. Report orbital eigenvalues in eV and spatial/fragment localization. These are model-dependent orbital observables, not experimental excitation energies.

# Required scientific validation/investigation

Choose and justify a computational method, generate a reasonable 3D structure, and optimize it or otherwise establish a documented stationary/representative geometry. Verify connectivity, E alkene, charge, multiplicity and the absence of unintended protonation changes. Record software, method, basis/parameters, solvent treatment, convergence criteria, geometry provenance and calculation status. Identify HOMO/LUMO unambiguously and provide orbital images, cube files, fragment populations, or another reproducible localization analysis that binds each orbital to the named fragments. Consider at least one plausible alternative geometry or method when practical and explain whether it changes the conclusion; do not manufacture a discovery story. Completion requires one valid converged calculation with all requested observables and validation evidence. If the calculation is explicitly bounded-failed before those observables can be established, submit the bounded-failure branch with a specific failure reason and attempted coverage; do not invent orbital values or localization. Stop when the selected geometry is converged and localization is documented, or when the stated finite failure boundary is reached.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include the selected structure/state, method and convergence record, HOMO/LUMO energies, per-orbital localization evidence, independently reasoned conclusion, limitations, and any alternate calculations. Attach referenced files under `report/` when used. Every numeric value must include units and provenance.
