# Scientific objective

Determine the electronic structure of the isolated neutral HL ligand in the supplied input. Optimize a defensible equilibrium geometry and report HOMO energy, LUMO energy, HOMO–LUMO gap, and spatial localization of each frontier orbital. Use the calculations to state what the orbital evidence supports about electronic stability and possible intramolecular charge redistribution. This is a direct computational investigation and does not require a discovery narrative.

# Public inputs and scientific boundaries

Use `data/inputs/hl_ligand.json` as the complete molecular identity: its SMILES, formula C20H20N4O6, formal charge 0, singlet multiplicity, E imines, and isolated-molecule scope define the system. You may generate starting conformers and choose software, electronic-structure method, basis, convergence settings, and orbital-analysis tools. Do not add metals, solvent, counterions, crystal packing, or implicit environment unless you provide a separate clearly labelled sensitivity calculation. The measured quantities are orbital energies in eV, their difference calculated as E(LUMO) − E(HOMO), and qualitative atom/group localization from orbital data.

# Required scientific validation/investigation

Generate at least one valid starting geometry, and if multiple materially distinct conformers are investigated, deduplicate them by connectivity and a stated geometric/energy criterion. Advance only calculations that converge to a chemically interpretable structure. Validate convergence and a stationary point (frequency analysis when available, or a documented force/gradient and optimization-convergence check), verify charge and multiplicity, and independently recompute the gap from the submitted orbital energies. Inspect orbital density or an equivalent population/localization analysis and bind every localization statement to the submitted structure. Completion requires one converged, validated structure and a complete observable set, or a bounded-failure report identifying attempted work and the limiting failure. Stop when that condition is met; for any conformer or method comparison, stop after the declared coverage is exhausted and report scope and limitations.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. A complete report includes the chosen structure, method/software, charge/multiplicity, convergence and validation evidence, HOMO/LUMO/gap with units, orbital-localization statements, and a concise evidence-based conclusion. If completion is impossible after bounded attempts, submit the bounded-failure branch with `failure_details`, attempted candidates, and limitations; do not invent unavailable values or structures. Do not assume or cite an author-specific route as a task hint.
