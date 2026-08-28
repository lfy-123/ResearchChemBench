# Scientific objective

Determine by independent computation the neutral-singlet HOMO/LUMO energies of 2BT-TTA, 2BF-TTA, and 2(C8Ph)-TTA and assess what their relative frontier levels can and cannot establish about electronic alignment relevant to SWCNT p-type doping. Report energies in eV, ordering, sensitivity, and a bounded conclusion.

# Public inputs and scientific boundaries

The molecules are exactly the atom-labelled XYZ files in `data/inputs`; atom order and element symbols define identity. Each is an isolated neutral singlet. No explicit SWCNT, solvent, counterion, aggregate, or temperature model is required. Formulate the interpretation from this objective and distinguish isolated-molecule evidence from interface claims. Do not use the paper, SI, general web, or hidden evaluator.

# Required scientific validation/investigation

Choose and document a defensible electronic-structure protocol independently. Optimize each supplied structure or justify a documented single-point alternative; identify converged neutral-singlet HOMO/LUMO; record software, method, basis, convergence evidence, and sensitivity checks. Deduplicate additional conformers by connectivity and geometry RMSD, and report coverage. Complete when all three molecules have validated results or explicitly documented bounded failure. Stop after the supplied structures and any pre-declared finite conformer set are exhausted. Do not infer composite charge transfer from isolated orbitals alone.

# Deliverables

Submit `report/results.json` and `report/methods.md`. Results must identify every molecule, charge/multiplicity, and per-molecule validation evidence. For each molecule either report converged HOMO/LUMO values with units and the evidence supporting them, or use the bounded-failure outcome with a specific reason; do not fabricate values. Report the observed ordering when the required results are available, interpretation, limitations, coverage, completion status, and explicit stopping rule. The root validation field must summarize the protocol and cross-system checks, while each molecule's validation evidence must support its own result.
