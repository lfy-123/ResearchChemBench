# Scientific objective

Determine the gas-phase frontier-orbital energetics of neutral singlet (E)-4-(4-methoxybenzylidene)-3-methylisoxazol-5(4H)-one. Independently compute its HOMO energy, LUMO energy, and LUMO-minus-HOMO gap in eV, validate the molecular state used, and conclude what these quantities do and do not imply about electronic stability or reactivity.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the isolated neutral singlet E-isomer has a frontier-orbital description with a moderate HOMO–LUMO separation, consistent with electronic stability while retaining potential charge-transfer character.

**Candidate route or mechanism.**
The relevant author-proposed route is a structure-to-property analysis: optimize the molecular geometry, then evaluate the frontier orbitals and the energy difference between them. Koopmans-style descriptors are used to interpret the orbital energies.

**Discriminating evidence.**
Test the proposal using a validated optimized geometry, the HOMO and LUMO energies, their arithmetic difference, and comparisons across independently generated conformers when needed. Interpret the result as a model-dependent electronic-structure claim, with geometry validation and orbital sensitivity helping distinguish a robust qualitative interpretation from a conformer or method artifact.


# Public inputs and scientific boundaries

`data/inputs/system.json` uniquely defines the research object by full name, formula, isomeric SMILES, E stereochemistry, formal charge 0, multiplicity 1, isolated gas-phase boundary, unit, and gap definition. Generate all 3D structures yourself. The endpoint is the lowest-energy validated minimum found under the declared bounded conformer investigation. Crystal packing, solvent effects, excited-state gaps, docking, reactions, and biological efficacy are outside scope. Do not use the source paper or supplementary information.

# Required scientific validation/investigation

Select and justify a defensible electronic-structure model for this neutral heteroaromatic molecule. Generate plausible conformers spanning the molecule's rotatable methoxy and aryl/exocyclic orientations while preserving the specified E isomer; deduplicate by graph, stereochemistry, and heavy-atom geometry. Optimize all advanced candidates consistently. Verify minima using frequencies or a comparably explicit Hessian-based criterion, record imaginary modes for each candidate, and compare validated conformer energies. Compute frontier orbitals for the lowest validated minimum and for any near-degenerate minimum whose inclusion is needed to assess robustness. Check arithmetic consistency of the reported gap and discuss model/conformer sensitivity.

Completion requires a reproducible method, declared search coverage, per-candidate validation evidence, a selected machine-readable geometry, converged HOMO/LUMO values and gap, and a bounded scientific conclusion. Stop when the declared rotatable-bond/conformer strategy is exhausted and every generated candidate is validated, deduplicated, or documented as failed. If no validated minimum or orbital result remains, stop with `bounded_failure`, preserving candidate identities and diagnostic evidence; do not invent success-only fields.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Report method/software, conformer-search definition, individual candidate records, completion status, and conclusion. A successful submission also contains the selected geometry as an XYZ string and HOMO, LUMO, and gap values in eV. A bounded-failure submission contains attempted candidates, diagnostics, and limitations instead of fabricated orbital values.
