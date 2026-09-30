# Scientific objective

Independently test the authors' qualitative hypothesis that the rigid, axially chiral C[2]BNDI macrocycle can support strong circularly polarized luminescence by calculating its ground-state structure, an optimized emitting S1 state, the S1→S0 transition dipoles, and the dimensionless CPL dissymmetry magnitude |g_lum|. The evaluated system is the methyl-truncated C[2]BNDI model specified in the public inputs, not the full octyl-substituted experimental material.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors attribute the CPL potential of C[2]BNDI to its rigid chiral conformation. Their structure–property interpretation focuses on the relative orientation of the electric and magnetic emission transition dipoles as a determinant of the dissymmetry magnitude.

**Candidate route or mechanism.**
Examine whether the optimized emitting conformation supports an electric–magnetic transition-dipole alignment that yields appreciable CPL, considering how an approximately orthogonal alignment would suppress the dipole contribution to dissymmetry. The authors' computational route uses ground-state DFT and excited-state TD-DFT optimization to investigate this connection between conformation and emission.

**Discriminating evidence.**
The authors use vibrational analysis to establish the ground-state minimum and analyze electric and magnetic transition dipoles for emission from the optimized S1 state. Assess the dipole magnitudes together with their mutual angle and the resulting |g_lum| to test the proposed structure–property connection.

# Public inputs and scientific boundaries

Use `data/inputs/c2bndi_start.xyz` as the immutable 92-atom atom-order and connectivity specification and `data/inputs/system_spec.json` for molecular identity, neutral charge, singlet multiplicity, methyl truncation and the declared implicit-chloroform benchmark boundary. The supplied coordinates are deliberately non-stationary and do not define a target conformation. The research object is this single molecular system. The measured quantities are an optimized ground-state geometry, vibrational frequencies establishing stationarity, an optimized S1 emitting-state geometry, the S1 state identity, S1→S0 transition electric and magnetic dipole vectors or signed/magnitude-equivalent data, their mutual angle, and |g_lum| reported as a dimensionless magnitude with the equation and convention used. You may generate conformers or alter starting coordinates only while preserving atom identity and connectivity and documenting the transformation. Do not use the paper, SI or general web.

# Required scientific validation/investigation

Plan and execute a reproducible electronic-structure calculation with a method and numerical settings justified for this system; the paper's software, model chemistry and ordered protocol are not prescribed. Optimize the neutral-singlet ground state without constraints, calculate frequencies, and retain the final geometry, convergence diagnostics and complete frequency evidence. Advance to excited-state calculations only from a converged ground-state structure. Determine and optimize the emitting S1 state, or use a scientifically equivalent adiabatic-emission treatment and justify the equivalence; document root/state tracking and retain the emitting-state geometry. Obtain electric and magnetic transition-dipole data for S1→S0 at that emitting-state geometry, calculate their angle and |g_lum| from an explicitly stated formula, and record the calculation/artifact provenance for each observable. Perform at least one internal robustness check that directly probes a material choice, such as a second starting conformer, tighter numerical convergence, an alternative justified electronic-structure treatment, or an independently implemented dipole analysis.

Successful completion requires a demonstrated ground-state minimum, a validated optimized/adiabatic S1 emission treatment, traceable transition-dipole data, a reproducible |g_lum| calculation and an interpretable robustness result. Stop when those conditions are satisfied. If any required stage remains unsuccessful after reasonable remedies, stop and submit a bounded failure containing the failed stage, attempted remedies, diagnostics, any validated intermediate results and the strongest scientifically warranted bounded conclusion; do not fabricate unavailable success-only values.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. In the completed branch include calculation provenance and rationale, ground- and emitting-state geometry artifact paths, convergence and frequency/minimum evidence, state-tracking and dipole provenance, robustness evidence, |g_lum| and its units/convention, and an evidence-based conclusion about whether the result supports the qualitative promise of C[2]BNDI as a chiral emitter within this model. Every numeric result must have units or an explicitly dimensionless designation and enough provenance to reproduce it. A bounded failure must use the failure branch and may report validated intermediate results without supplying unavailable success-only fields.
