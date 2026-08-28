# Scientific objective

For neutral singlet compound 2d, independently plan and execute a gas-phase quantum-chemical conformational characterization. Test the authors' qualitative proposal that the ortho-hydroxy substituent can stabilize an endo/type-II bridge arrangement through an intramolecular interaction, but do not assume that proposal is correct. Report an optimized minimum, the two explicitly defined bridge dihedrals φ1−2−3−4 and φ2−3−4−5 (use the paper's bridge numbering: 1 = imine carbon, 2 = imine nitrogen, 3 = Cα, 4 = adjacent arene ipso carbon, and 5 = the adjacent arene atom on the fused-ring side of atom 4, as identified in your atom mapping), electronic energy, and dipole if available.

# Public inputs and scientific boundaries

The input file `data/inputs/compound_2d.json` defines the exact E-isomer connectivity, formula C19H14N2O, neutral charge, singlet multiplicity, and isolated gas-phase boundary. No crystal lattice, solvent, counterion, or biological endpoint is part of the calculation. Generate starting 3-D conformers yourself and preserve the atom mapping used for the two named dihedrals. You may use any defensible quantum-chemistry software and model chemistry, but state them completely.

# Required scientific validation/investigation

Generate at least two non-duplicate starting conformers that differ in the naphthyl/bridge orientation, optimize each with the same stated protocol, and deduplicate the resulting minima by connectivity plus a stated geometric criterion. Advance only converged structures with chemically intact connectivity. For every attempted conformer, report its start identity, convergence/connectivity outcome, and validation evidence; for every advanced minimum, report the two dihedrals, energy and frequency result. A true minimum requires no imaginary frequency, or you must report bounded failure and explain the unresolved mode. Stop when all generated starting conformers have been optimized or failed reproducibly and no additional starting-conformer source remains within your stated search rule; record the start count, deduplication criterion, and stopping rule explicitly. Completion requires an auditable mapping, a selected lowest-energy validated minimum or an explicit bounded-failure branch, and a limitation statement about method dependence. Compare your geometry and qualitative interpretation with the crystallographic comparison described in the paper without treating it as a gas-phase calculation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include a per-candidate record, selected candidate identity, atom mapping, method, validation evidence, requested observables and a concise conclusion. Include paths to raw output or logs when available. Do not quote or reproduce the paper/SI as a substitute for calculations.
