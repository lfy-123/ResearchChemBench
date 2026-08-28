# Scientific objective

Independently plan and execute a calculation for the neutral singlet molecule 1-phenyl-5-(m-tolyl)-1H-tetrazole (C14H12N4). Test the authors' qualitative hypothesis that the molecule's frontier-orbital separation is consistent with a comparatively hard, kinetically stable and limited-reactivity electronic structure. Report the optimized minimum, EHOMO, ELUMO, their gap, and the derived ionization potential, electron affinity, chemical potential, electronegativity, hardness, softness and electrophilicity.

# Public inputs and scientific boundaries

Use `data/inputs/molecule.json`, whose SMILES uniquely defines the connectivity, formula, neutral formal charge and singlet multiplicity. Treat one isolated molecule as the system: no solvent, counterion, crystal lattice, protein, docking, or experimental replacement is in scope. You may choose software, method, basis, conformer-generation strategy and analysis route; document them. The XRD structure is only a qualitative comparison context, not a supplied scored coordinate set.

# Required scientific validation/investigation

Generate at least one chemically valid starting geometry and optimize it to a stationary point. Verify the final electronic state and optimization convergence, then perform a vibrational or equivalent curvature check that distinguishes a minimum from a saddle; report any imaginary modes. Extract the frontier orbital energies in eV and compute all requested descriptors with explicit formulas/sign conventions. If multiple starting conformers are explored, identify and deduplicate them and state coverage and why the selected state is representative. The calculation is complete when one validated minimum has reproducible reported observables and all required provenance is recorded. Stop after that validation, or report a bounded failure with the exact missing validation and the best completed evidence.

# Deliverables

Submit `report/results.json` conforming to the submission schema. Include system identity, computational provenance, validation evidence, all observables with units, formulas used, and a concise conclusion about the qualitative hypothesis. For `bounded_failure`, report the best completed evidence, identify the exact unmet validation or calculation, and use `null` only for observables that could not honestly be obtained, with an explanation in `availability_note`; do not fabricate placeholders. Do not cite or reproduce hidden paper values as inputs.
