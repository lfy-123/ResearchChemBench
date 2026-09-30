# Scientific objective

Determine the signed 300 K Gibbs free-energy difference ΔG = G_coplanar − G_perpendicular for the neutral singlet Z-cAAC^Cy complex represented by the two supplied structures. The authors' qualitative scientific route compares these two conformational arrangements to test whether their conformational stability is similar; independently plan and execute calculations that test that comparison. The primary measured quantity is ΔG in kJ mol−1.

# Public inputs and scientific boundaries

`data/inputs/perpendicular.xyz` is the SI Table S1 Z-cAAC^Cy perpendicular starting geometry; `data/inputs/coplanar.xyz` is the SI Table S2 Z-cAAC^Cy coplanar starting geometry. Each file contains the complete neutral molecular coordinate set, including one Zn atom and the C/H/N framework. Use charge 0 and singlet multiplicity unless a documented input-integrity finding prevents it. The physical boundary is the isolated molecule in its singlet ground state; the measurement boundary is a harmonic/standard-state 300 K Gibbs free-energy comparison for the two named structures. Do not infer a solution concentration, crystal packing, kinetic barrier, or experimental population from this task.

# Required scientific validation/investigation

Independently choose and document an electronic-structure route. For each named structure, verify atom count/elements, optimize or otherwise establish a stationary point, and report the final geometry and vibrational evidence. A validated minimum requires no imaginary frequencies; if either calculation cannot be completed, report the failure, diagnostics, and any partial energy rather than fabricating a result. Obtain consistent 300 K Gibbs free energies for both structures, state all method/thermal conventions, and calculate the signed subtraction exactly as defined above. The calculation is complete when both structures have auditable outputs and the signed difference is computed, or when a bounded failure report explains why that endpoint could not be obtained. Stop after the two named structures have been treated; optional sensitivity checks must be clearly separated from the primary endpoint.

# Deliverables

Submit `report/results.json` conforming to the submission schema. Include the two structure identities, input checks, methods, stationary-point/frequency validation, per-structure free energies when available, the signed ΔG when available, uncertainty/limitations, and a concise conclusion. Preserve enough file paths or embedded summaries for an evaluator to audit which result belongs to which conformer.
