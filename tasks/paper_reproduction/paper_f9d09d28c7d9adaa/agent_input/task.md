# Scientific objective

For MeAC, TfAC, MeACFy and TfACFy, independently plan and execute calculations that test the authors' qualitative proposal that the acridine/phenanthroimidazole donor–acceptor designs are highly twisted and can support HLCT-like electronic structure. Report optimized ground-state geometries, the labeled α3 and β1 dihedrals, frontier-orbital localization, and a reasoned comparison of methyl versus trifluoromethyl and acridine versus spirofluorene variants. Do not assume the authors' method or numerical result; choose and justify your own defensible computational route.

# Public inputs and scientific boundaries

Use every molecule in `data/inputs/compound_definitions.json`. It defines the systematic identity, formula, neutral charge (0) and singlet multiplicity (1). Construct any starting geometry or conformer ensemble yourself. The research object is the isolated molecule in its electronic ground state. Solvent, crystal packing, experimental CV values, and excited-state calculations are optional context only and are not required endpoints. Define α3 as the dihedral between the acridine donor and the phenyl π-bridge, and β1 as the dihedral between the fluorene and its directly connected spiro-acridine aryl system; provide the four atom indices for every measured dihedral. Use absolute magnitudes for comparison, while retaining signed values.

# Required scientific validation/investigation

For each named molecule, document the structure construction, charge/multiplicity, method, basis/model choices, and optimization termination. A result is complete only if the final geometry is a stationary-point optimization with an explicit convergence record, the atom identities for α3/β1 are unambiguous, and HOMO/LUMO density is inspected on named fragments. If multiple starting conformers are used, deduplicate by graph and geometry, state the selection rule, and report whether distinct minima remain. Check at least one geometry/orbital artifact (for example, an independent starting geometry, frequency/stationarity check, or visualization cross-check). Compare MeAC–TfAC and MeACFy–TfACFy, and explain whether the computed trends support or limit the stated twisted HLCT design hypothesis. Stop when all four compounds have converged and the required checks are complete; if a calculation fails, stop after documenting the failure, attempted remedies and the scientifically bounded conclusion rather than inventing a value.

# Deliverables

Submit `report/results.json` following the schema. Include one record per named compound, method and convergence evidence, atom-index definitions, α3 and β1 where structurally present, optional α1/α2, HOMO/LUMO localization and any eigenvalues, paired comparisons, limitations, and a final conclusion. Include enough provenance to reproduce the actual investigation.
