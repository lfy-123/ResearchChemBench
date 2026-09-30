# Scientific objective

Test the authors' qualitative hypothesis that the supplied naphthalene-derived dication G1 is twisted as a monomer and forms an offset, parallel π-stacked aggregate as a dimer. Independently choose and execute a defensible quantum-chemical geometry workflow, then report the optimized structures and the following measured quantities: two benzyl–pyridinium dihedrals and two pyridinium–naphthalene dihedrals for the monomer; naphthalene-ring interplanar stacking separation and slip angle, with full centroid separation reported separately for the dimer.

# Public inputs and scientific boundaries

`data/inputs/g1_monomer.xyz` is the 64-atom G1 monomer, charge +2, singlet. `data/inputs/g1_dimer.xyz` is the 128-atom assembly of two identical G1 dications, charge +4, singlet. These are starting geometries only; no target structures or values are supplied. Treat atoms and connectivity implied by the XYZ coordinates as fixed, omit counterions, and state any solvent, electronic-structure, conformer, ring-plane, centroid and dihedral sign conventions. The endpoint is a relaxed ground-state geometry for each supplied system, not an emission-energy prediction.

# Required scientific validation/investigation

Verify atom counts, elemental identity, charge and connectivity before calculation. Relax both systems or give a scientifically justified bounded-failure explanation. Establish minimum status with a frequency calculation or a clearly described alternative stability check, recording imaginary modes if present. Define the exact atom selections used for each dihedral and each naphthalene ring centroid/plane, preserve monomer/dimer identity, and report convergence evidence. Completion requires both systems to have a reproducible endpoint and all six observable values, or an explicit per-system failure branch with attempted methods, diagnostics and limitations. Stop when the chosen protocol converges and validation is complete; if it does not, stop after documenting the bounded alternative and why further work would not be interpretable.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include method, input verification, per-system validation, measured values with units, structure file paths or inline coordinates, and a conclusion that explicitly assesses the twisted-monomer/offset-stack hypothesis within the reported scope. Report uncertainty and limitations without inventing reference values.

Define plane separation as the absolute projection of the centroid-to-centroid vector on the normalized mean of the two consistently oriented least-squares ring normals. Also report both individual-plane projections and the angle between planes, because distorted rings need not be exactly parallel. Define slip as the acute angle between the centroid vector and that mean plane, and report its complementary angle to the normal. Do not conflate either projection with the full centroid-vector length.
