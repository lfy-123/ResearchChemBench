# Scientific objective

Independently choose and execute a defensible quantum-chemical geometry workflow, then report the optimized structures and the following measured quantities: two benzyl–pyridinium dihedrals and two pyridinium–naphthalene dihedrals for the monomer; naphthalene-ring interplanar stacking separation and slip angle, with full centroid separation reported separately for the dimer.

# Author-provided scientific guidance

Test the authors' qualitative hypothesis that the supplied naphthalene-derived dication G1 is twisted as a monomer and forms an offset, parallel π-stacked aggregate as a dimer.

# Public inputs and scientific boundaries

`data/inputs/g1_monomer.xyz` is an independently generated, unoptimized 64-atom G1 starter (C34H28N2, charge +2, singlet). `data/inputs/g1_dimer.xyz` is an independently assembled, unoptimized two-monomer starter (128 atoms, charge +4, singlet). Neither is an optimized answer. The corresponding `*_identity.json` files define complete atom-mapped chemical graphs and dimer fragment membership. Preserve chemical identity, not initial distances or orientation; explore and relax the geometries. Omit counterions. The primary comparison uses an aqueous continuum (water); disclose the electronic-structure and solvent implementation. Other media may be reported separately as sensitivity results. The task concerns relaxed ground-state geometry, not emission energies.

For the primary monomer comparison, fit least-squares planes to the ring atom sets in `g1_monomer_identity.json` and report their acute interplanar angle θ = acos(|n1·n2|/(|n1||n2|)), in degrees from 0 to 90. The legacy `benzyl_pyridinium_dihedrals_deg` field denotes terminal phenyl–pyridinium plane angles; `pyridinium_naphthalene_dihedrals_deg` denotes pyridinium–naphthalene plane angles. Report each right/left pair and its arithmetic mean. Signed four-atom torsions may be additional diagnostics, not substitutes for these primary plane angles. For the dimer use the least-squares planes of the two naphthalene cores. Interplanar separation is the absolute projection of the centroid vector onto the normalized mean of consistently oriented ring normals; also report individual-plane projections and interplane angle. Slip is the acute angle of the centroid vector to that mean plane; its complement is the angle to the normal. Report full centroid-vector length separately, not as the interplanar spacing.

# Required scientific validation/investigation

Verify atom counts, elemental identity, charge and connectivity before calculation. Relax both systems or give a scientifically justified bounded-failure explanation. Establish minimum status with a frequency calculation or a clearly described alternative stability check, recording imaginary modes if present. Define the exact atom selections used for each dihedral and each naphthalene ring centroid/plane, preserve monomer/dimer identity, and report convergence evidence. Completion requires both systems to have a reproducible endpoint and all requested observables; otherwise submit per-system attempted methods and failure diagnostics.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Write `report/results.json` conforming to the submission schema. Include method, input verification, per-system validation, measured values with units, nonempty `structure_path` values pointing to submitted coordinate files for both systems, and a conclusion that explicitly assesses the twisted-monomer/offset-stack hypothesis within the reported scope. Report uncertainty without inventing reference values.
