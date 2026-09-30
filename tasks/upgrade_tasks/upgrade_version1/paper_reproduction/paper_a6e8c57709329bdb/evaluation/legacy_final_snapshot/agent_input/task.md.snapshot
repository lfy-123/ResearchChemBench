# Scientific objective

Independently determine the electronic structure of the isolated neutral HL ligand in the supplied input. Optimize a chemically defensible equilibrium geometry and report its HOMO energy, LUMO energy, HOMO–LUMO gap, and spatial localization of each frontier orbital. The author hypothesis to test is that the conjugated diacylhydrazone ligand has a stable frontier electronic structure with donor-atom/aromatic HOMO character and ICT-relevant LUMO character. This is a computational test, not a request to reproduce an experimental spectrum or metal-binding free energy.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret the conjugated diacylhydrazone ligand's frontier electronic structure as consistent with electronic stability, donor-site behavior, and possible intramolecular charge transfer. They propose donor-atom and nearby aromatic character for the HOMO, with LUMO character extending across conjugated aromatic and imine regions.

**Candidate route or mechanism.**
The relevant candidate is an optimized neutral singlet free-ligand structure followed by frontier-orbital analysis. Examine whether the conjugated azomethine and donor-atom framework supports the proposed HOMO/LUMO localization and charge-redistribution interpretation, while allowing the calculation to determine the actual geometry and orbital character.

**Discriminating evidence.**
Use a converged optimized structure, stationary-point or force/gradient validation, HOMO and LUMO energies, the independently computed energy gap, and orbital-density or equivalent localization analysis tied to the submitted atom ordering. These observations distinguish the proposed donor/conjugated orbital picture from other localization patterns.

# Public inputs and scientific boundaries

Use `data/inputs/hl_ligand.json` as the complete molecular identity: its SMILES, formula C20H22N4O6, formal charge 0, singlet multiplicity, E imines, and isolated-molecule scope define the system. You may generate starting conformers and choose software, electronic-structure method, basis, convergence settings, and orbital-analysis tools. Do not add Mn, Fe, solvent, counterions, crystal packing, or implicit environmental terms unless you provide a separate clearly labelled sensitivity calculation. The measured quantities are orbital energies in eV, their difference calculated as E(LUMO) − E(HOMO), and qualitative atom/group localization from orbital data.

# Required scientific validation/investigation

Generate at least one valid starting geometry, and if multiple materially distinct conformers are investigated, deduplicate them by connectivity and a stated geometric/energy criterion. Advance only calculations that converge to a chemically interpretable structure. Validate convergence and a stationary point (frequency analysis when available, or a documented force/gradient and optimization-convergence check), verify the charge and multiplicity, and independently recompute the reported gap from the submitted orbital energies. Inspect orbital density or an equivalent population/localization analysis and bind every localization statement to the submitted structure. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. A complete report includes the chosen structure (prefer XYZ or a structure file plus atom ordering), method/software, charge/multiplicity, convergence and validation evidence, HOMO/LUMO/gap with units, orbital-localization statements, and a concise conclusion about the author hypothesis. If completion is impossible after bounded attempts, submit the bounded-failure branch with `failure_details`, attempted candidates; do not invent unavailable values or structures. Do not copy the paper or use its reported numerical values as inputs.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
