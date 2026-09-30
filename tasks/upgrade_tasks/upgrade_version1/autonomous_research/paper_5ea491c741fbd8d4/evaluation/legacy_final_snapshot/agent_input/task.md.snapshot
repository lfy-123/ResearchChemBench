# Scientific objective

Determine the gas-phase frontier-orbital energetics of neutral singlet (E)-4-(4-methoxybenzylidene)-3-methylisoxazol-5(4H)-one. Independently compute its HOMO energy, LUMO energy, and LUMO-minus-HOMO gap in eV, validate the molecular state used, and conclude what these quantities do and do not imply about electronic stability or reactivity.

# Public inputs and scientific boundaries

`data/inputs/system.json` uniquely defines the research object by full name, formula, isomeric SMILES, E stereochemistry, formal charge 0, multiplicity 1, isolated gas-phase boundary, unit, and gap definition. Generate all 3D structures yourself. The endpoint is the lowest-energy validated minimum found under the declared bounded conformer investigation. Crystal packing, solvent effects, excited-state gaps, docking, reactions, and biological efficacy are outside scope. Do not use the source paper or supplementary information.

# Required scientific validation/investigation

Select and justify a defensible electronic-structure model for this neutral heteroaromatic molecule. Generate plausible conformers spanning the molecule's rotatable methoxy and aryl/exocyclic orientations while preserving the specified E isomer; deduplicate by graph, stereochemistry, and heavy-atom geometry. Optimize all advanced candidates consistently. Verify minima using frequencies or a comparably explicit Hessian-based criterion, record imaginary modes for each candidate, and compare validated conformer energies. Compute frontier orbitals for the lowest validated minimum and for any near-degenerate minimum whose inclusion is needed to assess robustness. Check arithmetic consistency of the reported gap and discuss model/conformer sensitivity.

Completion requires a reproducible method, declared search coverage, per-candidate validation evidence, a selected machine-readable geometry, converged HOMO/LUMO values and gap, and a bounded scientific conclusion. If no validated minimum or orbital result remains, stop with `bounded_failure`, preserving candidate identities and diagnostic evidence; do not invent success-only fields.

For a failed/uncomputed candidate, use null for an unavailable imaginary-frequency count and explain the missing stage in diagnostics; retain actual counts whenever computed. A successful selected minimum must have genuine stationary-point evidence. Never substitute zero for unknown. The selected candidate ID must resolve to that validated candidate.

Independent method selection does not change the definitions of orbital energies or waive numerical accuracy. Report method/conformer dependence; results from every defensible method are not asserted to be identical.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Report method/software, conformer-search definition, individual candidate records, completion status, and conclusion. A successful submission also contains the selected geometry as an XYZ string and HOMO, LUMO, and gap values in eV. A bounded-failure submission contains attempted candidates, diagnostics and any available orbital results without fabricating missing values.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
