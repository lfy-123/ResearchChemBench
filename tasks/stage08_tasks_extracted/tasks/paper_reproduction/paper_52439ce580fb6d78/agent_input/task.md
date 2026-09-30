# Scientific objective

Investigate the isolated neutral monolayer 2H-VSe2 in the supplied structure. Determine independently whether it has a stable magnetic ground state and quantify its spin-orbit-coupling K/K' valley splitting. Report relaxed geometry, magnetic ground state, V moment, and E_VBM(K)-E_VBM(K') in meV, with a calculation-based interpretation.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that monolayer 2H-VSe2 supports ferromagnetic order and that its magnetic order produces spin-polarized valley physics, including a SOC-induced difference between the K and K' valence-band maxima.

**Candidate route or mechanism.**
For reproduction, test the proposed ferromagnetic solution against competing magnetic arrangements, including antiferromagnetic and nonmagnetic alternatives. Then evaluate whether non-collinear spin-orbit coupling lifts the K/K' valence-band degeneracy in the relaxed magnetic state.

**Discriminating evidence.**
The relevant evidence is comparative total energies and local V moments for the tested magnetic states, together with explicit spin-resolved or non-collinear band energies at K and K' and a sensitivity check establishing whether the observed valley difference is numerically stable.

# Public inputs and scientific boundaries

`data/inputs/vse2_2h_primitive.json` uniquely specifies neutral VSe2, the three-atom hexagonal primitive cell, fractional coordinates, 20 Å c vector, and 2H sandwich ordering. The scored system is this isolated molecule-like monolayer periodic in x/y with vacuum along z; add no substrate, defects, dopants, solvent, or atoms. K=[1/3,1/3,0] and K'=[-1/3,-1/3,0] are fractional reciprocal coordinates. The measured quantity is the difference between the highest occupied valence-band energies at these points in a non-collinear SOC calculation. Choose and disclose software and model chemistry.

# Required scientific validation/investigation

Relax the structure and document final cell/coordinates plus energy and force criteria. Establish the magnetic solution by comparing at least two distinct spin arrangements or a justified equivalent check, identify the lowest-energy state, and report the V local moment and its definition. Perform non-collinear SOC calculations at explicit K and K' points, identify each VBM and compute signed and absolute splitting. Perform one stated convergence or sensitivity check for the observable and report uncertainty. Completion requires all endpoints and validation evidence; then stop. If resources prevent completion, report the missing endpoint and attempted investigation instead of inventing values; in that bounded-failure outcome, numerical fields for uncomputed endpoints may be null and the failure_details field is required.

# Deliverables

Submit `report/results.json` following the local `submission_schema.json`, including methods, relaxed structure, magnetic candidates and context, selected state, V moment, K/K' VBM energies, signed/absolute splitting, validation evidence, completion status, and final interpretation. A bounded-failure branch must identify the failed endpoint and limitation.
