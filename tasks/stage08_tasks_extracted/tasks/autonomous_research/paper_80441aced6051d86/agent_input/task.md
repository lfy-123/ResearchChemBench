# Scientific objective

Determine, from independent computation, how the supplied G1 monomer and dimer geometries are organized and whether their structural descriptors support a twisted isolated molecule and a distinct offset π-stacked dimer. Report two benzyl–pyridinium dihedrals and two pyridinium–naphthalene dihedrals for the monomer, plus naphthalene-ring centroid separation and slip angle for the dimer, together with a defensible structural interpretation.

# Public inputs and scientific boundaries

`data/inputs/g1_monomer.xyz` is the 52-atom G1 monomer, charge +2, singlet. `data/inputs/g1_dimer.xyz` is the 104-atom assembly of two identical G1 dications, charge +4, singlet. Treat the scored systems as these isolated molecules and assembly: keep the supplied atoms and connectivity fixed, do not add a host, counterions, or solvent, and state electronic-structure, conformer, ring-plane, centroid and dihedral sign conventions. The endpoint is a relaxed ground-state geometry and geometric interpretation; photophysical observables are outside scope.

# Required scientific validation/investigation

Verify atom counts, elements, charge, multiplicity, and connectivity. Independently select and justify a computational route, relax both systems, and validate minimum or stability using frequencies or a justified alternative. Define exact atom selections and retain object identity for every reported quantity. Generate and test your own structural explanation of the computed organization. Completion requires reproducible endpoints and all six observables, or a truthful per-system bounded-failure report containing attempts, diagnostics, and limitations. Stop after the selected route converges and validation is complete; if convergence or validation fails, stop after the documented bounded alternative is exhausted and explain what cannot be concluded.

# Deliverables

Write `report/results.json` conforming to the local `submission_schema.json`. Include the chosen route, input verification, per-system validation, values with units, structure paths or inline coordinates, and an evidence-based conclusion about the computed packing organization. Do not claim uniqueness beyond the searched structures.
