# Scientific objective

For the supplied isoxazole 1a identity, compute the gas-phase HOMO energy, LUMO energy, and LUMO-minus-HOMO gap in eV. The numerical values and result direction are not supplied; the primary method is specified below.

# Author-provided scientific guidance

Independently test the authors' qualitative proposal that an optimized isolated-molecule geometry of neutral singlet (E)-4-(4-methoxybenzylidene)-3-methylisoxazol-5(4H)-one supports a frontier-orbital description with a moderate HOMO–LUMO separation.

# Public inputs and scientific boundaries

`data/inputs/system.json` uniquely defines 1a by full name, formula, isomeric SMILES, E stereochemistry, formal charge 0, multiplicity 1, gas-phase boundary, unit, and gap definition. Generate all 3D structures yourself. Treat one isolated molecule, not a crystal or aggregate. The target is the validated optimized conformer used for the reported orbital result. Crystal packing, solvent effects, excited-state gaps, docking, reactions, and biological efficacy are out of scope. Do not use the source paper or its supplementary information.

# Required scientific validation/investigation

Use the primary method specified below and document implementation and numerical settings. Generate distinct plausible conformers by varying rotatable methoxy and aryl/exocyclic orientations while preserving connectivity and E stereochemistry; deduplicate them by molecular graph, stereochemistry, and heavy-atom geometry. Optimize every advanced conformer under the same stated conditions. Establish that the reported conformer is a stationary minimum using an analytic frequency calculation or a comparably explicit Hessian-based test, and report imaginary-mode results. Advance the lowest-energy validated minimum to the orbital calculation; if minima are close enough that method or conformer choice could alter the conclusion, compute orbitals for those minima too and report sensitivity.

Completion requires a reproducible method specification, conformer coverage, per-conformer optimization/minimum evidence, the selected conformer's machine-readable geometry, HOMO and LUMO energies, an internally consistent gap, and a scientific interpretation. If that bounded search cannot yield a validated minimum or orbital result, stop after exhausting the declared search and report `bounded_failure` with attempted candidates, diagnostics; do not fabricate energies.

For a failed/uncomputed candidate, use null for an unavailable imaginary-frequency count and explain the missing stage in diagnostics; retain actual counts whenever computed. A successful selected minimum must have genuine stationary-point evidence. Never substitute zero for unknown. The selected candidate ID must resolve to that validated candidate.

Use gas-phase B3LYP/6-311+G(d,p) for the primary optimized-geometry/frontier-orbital comparison; retain the specified E molecular identity. Other methods may be reported separately as sensitivity. Choose representative valid minima by the declared energy/structure policy, not by orbital agreement with an external answer.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. It must identify the method and software, document conformer generation and individual candidate validation, state completion status, provide the selected geometry as an XYZ string and the three orbital quantities on success, and give a conclusion limited to what the calculations support. For bounded failure, provide attempted-candidate records, diagnostics, and identify the required results that remain unavailable.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
