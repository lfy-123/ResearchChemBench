# Scientific objective

Determine by independent computation the neutral-singlet HOMO/LUMO energies of 2BT-TTA, 2BF-TTA, and 2(C8Ph)-TTA and assess what their relative frontier levels can and cannot establish about electronic alignment relevant to SWCNT p-type doping. Report energies in eV, ordering, sensitivity, and a calculation-based conclusion.

# Public inputs and scientific boundaries

The molecules are exactly the atom-labelled XYZ files in `data/inputs`; atom order and element symbols define identity. Each is an isolated neutral singlet. No explicit SWCNT, solvent, counterion, aggregate, or temperature model is required. Formulate the interpretation from this objective and distinguish isolated-molecule evidence from interface claims. Do not use the paper, SI, general web, or hidden evaluator.

This is a fixed-structure property track: the supplied coordinates are public inputs for the named property comparison, not a scored structure discovery answer. Do not claim that the input geometry itself was rediscovered; report any optimization or conformer search separately.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

# Required scientific validation/investigation

Choose and document a defensible electronic-structure protocol independently. Optimize each supplied structure or justify a documented single-point alternative; identify converged neutral-singlet HOMO/LUMO; record software, method, basis, convergence evidence, and sensitivity checks. Deduplicate additional conformers by connectivity and geometry RMSD, and report coverage. Scientific completion requires validated results for all three molecules and their comparison. Do not infer composite charge transfer from isolated orbitals alone.

# Deliverables

Submit `report/results.json` and `report/methods.md`. Results must identify every molecule, charge/multiplicity, and per-molecule validation evidence. For each molecule either report converged HOMO/LUMO values with units and the evidence supporting them, or use the bounded-failure outcome with a specific reason; do not fabricate values. Report the observed ordering when the required results are available, interpretation, coverage and completion status. The root validation field must summarize the protocol and cross-system checks, while each molecule's validation evidence must support its own result.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
