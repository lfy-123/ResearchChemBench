# Scientific objective

Independently determine whether four specified phenanthroimidazole molecules have strongly non-planar ground-state donor–acceptor geometries and frontier-orbital localization consistent with a mixed local/charge-transfer electronic design. Quantify and compare the relevant twist dihedrals and characterize where the HOMO and LUMO reside, then state what structural substitutions change those properties.

# Public inputs and scientific boundaries

Use every molecule in `data/inputs/compound_definitions.json`. It defines the systematic identity, formula, neutral charge (0) and singlet multiplicity (1). Construct starting geometries yourself. The research object is the isolated neutral ground-state molecule; solvent, crystal packing, and experimental measurements are outside the required boundary. Define α3 as the dihedral between the acridine donor and phenyl π-bridge, and β1 as the dihedral between fluorene and the directly connected spiro-acridine aryl system; report four atom indices for each. Compare absolute dihedral magnitudes but retain signs.

# Required scientific validation/investigation

Choose and justify a computational protocol without being given a paper protocol. For each molecule, record structure construction, charge/multiplicity, optimization termination, orbital visualization and fragment definitions. Completion requires converged optimized geometries for all four molecules, traceable α3/β1 measurements, HOMO/LUMO localization, and paired Me/Tf and AC/ACFy comparisons. Validate at least one result per molecule with an independent starting geometry, stationarity/frequency evidence, or an equivalent explicit check; if minima differ, retain and discuss them rather than silently selecting one. Stop when all four systems and required validation checks are complete, or provide a bounded failure report naming the failed system, evidence, and limitation. Report candidate/conformer coverage and why further search would not change the conclusion.

# Deliverables

Submit `report/results.json` following the schema. Include per-compound calculations, atom-index definitions, twist results, frontier-orbital localization/eigenvalues when available, validation evidence, paired comparisons, limitations, and a final independently reasoned conclusion. Do not claim a universal mechanism from these ground-state calculations alone.
