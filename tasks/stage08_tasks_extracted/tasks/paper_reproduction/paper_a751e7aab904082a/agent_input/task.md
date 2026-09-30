# Scientific objective

Determine how catalyst F interacts with the four explicitly supplied molecules 2g, 3g, 2w, and 3w by computing ΔE(X–F)=E(X–F)−E(X)−E(F) in kcal/mol for the four named 1:1 noncovalent complexes. Use validated structures and the resulting comparisons to formulate a scientifically bounded conclusion about whether interaction strength differs between phenolic and alcoholic members and between each acceptor/product pair. Generate and test your own explanations or pathways; do not assume any particular ordering or mechanistic explanation before performing the calculations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that catalyst organization or binding may differ between phenolic and alcoholic acceptors: binding to phenolic substrate 2g may be preferential, while alcohol product 3w may compete effectively with alcohol substrate 2w. They present this as a comparative explanation relevant to incomplete conversion and possible product inhibition.

**Candidate route or mechanism.**
Compare the catalyst complexes for phenolic substrate/product (2g-F and 3g-F) with those for alcoholic substrate/product (2w-F and 3w-F). In particular, examine whether stronger association is concentrated at the phenolic substrate and whether the alcohol product remains competitive with its alcohol acceptor; treat these as proposed comparisons to test rather than established outcomes.

**Discriminating evidence.**
Use consistently computed electronic interaction energies for all four complexes, validated optimized stationary points or an explicitly justified limited alternative, and documented structure searches. Contact or electrostatic analyses may be used to interpret the computed comparisons qualitatively, while recognizing that interaction energies alone do not establish catalytic kinetics.

# Public inputs and scientific boundaries

The files `data/inputs/2g.xyz`, `2w.xyz`, `3g.xyz`, `3w.xyz`, and `F.xyz` are the complete Cartesian coordinates in Å for the named molecules, each with charge 0 and spin multiplicity 1. The XYZ comment line identifies the molecule. Use the atom identities and coordinates exactly as supplied; do not alter protonation, connectivity, stereochemistry, charge, or multiplicity. The four complexes are exactly 2g-F, 3g-F, 2w-F, and 3w-F. The scored system is the isolated molecule or isolated 1:1 complex; do not add a host, explicit solvent, extra species, reaction transition state, or kinetic model. An optional implicit toluene model may be chosen and justified. The measured quantity is the electronic interaction energy assembled from consistently computed complex and monomer energies.

# Required scientific validation/investigation

Plan and execute a finite, reproducible search over starting arrangements for every named complex. Define arrangement generation, duplicate removal, advancement, and stopping criteria. For every advanced structure, report its pair identity, geometry-validation outcome, charge and multiplicity, and a structure identifier. A valid minimum must have no imaginary frequency when frequencies are computed, or explicitly justify an alternative validation and mark the result limited. Compute isolated-monomer and complex energies consistently and show the arithmetic for all four ΔE values. Completion requires validated advanced structures and final interaction energies for all four pairs, or a bounded-failure branch that identifies failed pairs, attempted coverage, and the limitation. Stop when all four energy assemblies and validation records are complete, or when additional attempts no longer yield validated structures within available resources; report the stopping reason and coverage. Interpret only the calculated comparison and state uncertainty; do not infer a reaction mechanism or global minimum without evidence.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. It must contain the required local result keys, including completion status, per-pair identity and validation context, energies or a truthful bounded-failure branch, search coverage, and an independently reasoned conclusion with limitations. Include units and the chosen computational method details, and retain unsuccessful attempts.
