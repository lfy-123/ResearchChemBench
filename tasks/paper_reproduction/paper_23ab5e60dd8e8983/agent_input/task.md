# Scientific objective

Determine, by an independently planned electronic-structure calculation, the HOMO and LUMO energies and fragment localization of the fixed neutral zwitterionic singlet NI(O)-Qu chromophore. Test the authors' qualitative hypothesis that its long-wavelength optical transition has donor-to-acceptor ICT character from the hydroxynaphthalimide part toward the N-methylquinolinium part; do not assume that hypothesis is correct.

# Public inputs and scientific boundaries

Use `data/inputs/ni_o_qu.smiles` and `data/inputs/system.json`. The molecule is the explicitly specified E-styryl NI(O)-Qu constitution, formula C26H18N2O5, net charge 0, multiplicity 1, with phenoxide anion and N-methylquinolinium cation. The naphthalimide, quinolinium and linker fragments are defined in `system.json`. The physical system is one isolated molecule; no iodide, explicit solvent, biomolecule or crystal is part of the target. Report orbital eigenvalues in eV and spatial/fragment localization. These are model-dependent orbital observables, not experimental excitation energies.

# Required scientific validation/investigation

Choose and justify a computational method, generate a reasonable 3D structure, and optimize it or otherwise establish a documented stationary/representative geometry. Verify connectivity, E alkene, charge, multiplicity and the absence of unintended protonation changes. Record software, method, basis/parameters, solvent treatment, convergence criteria, geometry provenance and calculation status. Identify HOMO/LUMO unambiguously and provide orbital images, cube files, fragment populations, or another reproducible localization analysis that binds each orbital to the named fragments. If multiple conformers or methods are investigated, retain their identities and summarize sensitivity; do not hide disagreement. Completion requires one valid converged calculation with all requested observables and validation evidence. If the calculation is explicitly bounded-failed before those observables can be established, submit the bounded-failure branch with a specific failure reason and attempted coverage; do not invent orbital values or localization. Stop when the selected geometry is converged and localization is documented, or when the stated finite failure boundary is reached.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include the selected structure/state, method and convergence record, HOMO/LUMO energies, per-orbital localization evidence, ICT conclusion, limitations, and any alternate calculations. Attach referenced files under `report/` when used. Every numeric value must include units and provenance.
