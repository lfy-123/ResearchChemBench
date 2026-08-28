# Scientific objective

Test the qualitative author hypothesis that an Fe(III) porphyrin site with an axial halide can explain the ligand-nucleus paramagnetic NMR pattern of Fe@PCN-224. Independently plan and execute calculations for the supplied Fe(III)Cl@TCPP cluster; do not assume the paper's method or numerical answer. Report site-resolved isotropic 1H and 13C shifts, fit quality, and whether the calculated local geometry is compatible with the stated experimental boundaries.

# Public inputs and scientific boundaries

`data/inputs/feiii_cl_tcpp.xyz` is the 86-atom Fe(III)Cl@TCPP Cartesian model from SI Table S14. It is neutral with multiplicity 6; the atom order and coordinates are fixed. The physical boundary is this isolated cluster, not the periodic MOF or solvent. The measurement boundary is comparison to Fe@PCN-224 ligand 1H/13C MAS NMR site shifts and Fe coordination distances, but the numerical observations are intentionally withheld. Evaluate the three aromatic proton environments (beta, meta, ortho) and eight carbon environments (alpha, beta, meso, ipso, ortho, meta, para, carboxylate carbon); define your atom/site mapping explicitly.

# Required scientific validation/investigation

Choose and document an independent computational route for geometry, hyperfine/orbital shielding and spin-Hamiltonian contributions, or a scientifically justified alternative. Verify the optimized structure is a minimum (or report a bounded failure), state charge/spin, convergence and software/model choices, and preserve provenance from each calculation to each reported site. Calculate isotropic shifts at a stated temperature and report the mapping and any equivalent-site averaging. Quantify fit quality separately for 1H and 13C and compare Fe--N and Fe--Cl distances to the experimental boundary without inventing values. Completion requires all requested observables or an explicit bounded-failure report with diagnostics and the reason further work would not resolve it; stop after the chosen route is complete and all failed/omitted calculations and sensitivity limitations are recorded.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include calculation provenance, validation status, per-site predictions with units and atom/site identity, fit metrics, structural distances, a conclusion about the hypothesis, and limitations. A bounded-failure branch is acceptable only when it contains diagnostics, completed partial results and a concrete stopping explanation.
