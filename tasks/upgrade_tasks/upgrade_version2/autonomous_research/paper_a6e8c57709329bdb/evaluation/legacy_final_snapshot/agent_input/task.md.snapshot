# Scientific objective

Determine the electronic structure of the isolated neutral HL ligand in the supplied input. Optimize a defensible equilibrium geometry and report HOMO energy, LUMO energy, HOMO–LUMO gap, and spatial localization of each frontier orbital. Use the calculations to state what the orbital evidence supports about electronic stability and possible intramolecular charge redistribution. This is a direct computational investigation and does not require a discovery narrative.

# Public inputs and scientific boundaries

Use `data/inputs/hl_ligand.json` as the complete molecular identity: its SMILES, formula C20H22N4O6, formal charge 0, singlet multiplicity, E imines, and isolated-molecule scope define the system. You may generate starting conformers and choose software, electronic-structure method, basis, convergence settings, and orbital-analysis tools. Do not add metals, solvent, counterions, crystal packing, or implicit environment unless you provide a separate clearly labelled sensitivity calculation. The measured quantities are orbital energies in eV, their difference calculated as E(LUMO) − E(HOMO), and qualitative atom/group localization from orbital data.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

# Required scientific validation/investigation

Generate at least one valid starting geometry, and if multiple materially distinct conformers are investigated, deduplicate them by connectivity and a stated geometric/energy criterion. Advance only calculations that converge to a chemically interpretable structure. Validate convergence and a stationary point (frequency analysis when available, or a documented force/gradient and optimization-convergence check), verify charge and multiplicity, and independently recompute the gap from the submitted orbital energies. Inspect orbital density or an equivalent population/localization analysis and bind every localization statement to the submitted structure. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. A complete report includes the chosen structure, method/software, charge/multiplicity, convergence and validation evidence, HOMO/LUMO/gap with units, orbital-localization statements, and a concise evidence-based conclusion. If completion is impossible after bounded attempts, submit the bounded-failure branch with `failure_details`, attempted candidates; do not invent unavailable values or structures. Do not assume or cite an author-specific route as a task hint.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
