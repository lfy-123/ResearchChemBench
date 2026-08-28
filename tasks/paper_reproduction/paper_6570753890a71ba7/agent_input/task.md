# Scientific objective

Test the authors' qualitative hypothesis that the Polytope Formalism connectivity-motion graph for H-tautomerism in a free-base subporphyrin monoanion is reflected in the real-space PES. Independently calculate and characterize the three supplied stationary-point candidates, then assess whether their Hessians and normal modes support the proposed LM → first-order saddle → second-order saddle relationship and the associated first-/second-order graph links. Do not assume the labels or the paper's numerical values are correct.

# Public inputs and scientific boundaries

The three public files `data/inputs/candidate_a.xyz`, `candidate_b.xyz` and `candidate_c.xyz` provide candidates A, B and C. Each record has an explicit atom order, element symbols and Cartesian coordinates in Å; all are the same single-molecule composition. Use charge −1 and singlet multiplicity for every record. The physical boundary is a single nondissociating free-base subporphyrin monoanion in implicit chloroform; the three inner N atoms are the connectivity sites and the inner H is the mobile bonder. You may choose software, electronic structure method, solvation treatment and convergence settings, but state them. The scored observables are electronic energy, the three lowest-frequency values including sign, harmonic thermal free energy, imaginary-frequency count, and mode/path interpretation.

# Required scientific validation/investigation

For each named candidate A/B/C, generate a defensible stationary-point calculation or a documented equivalent. Verify optimization/convergence, inspect the Hessian, count negative/imaginary modes, and identify whether the lowest imaginary mode(s) are chemically associated with H motion between the inner N sites. Compare candidate relationships using an explicitly defined connectivity change and report whether the supplied three-point set supports the stated first-/second-order graph/PES correspondence. Completion requires either validated results for all three candidates or a bounded-failure report naming each failed candidate, cause, attempted remedy and the remaining conclusions that are and are not supported. Stop when all three candidates have a converged characterization or after two documented remediation attempts per failed candidate; report method sensitivity or incomplete mode inspection as limitations.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus calculation logs/output and a short `report/methods.md`. The JSON must retain candidate identity A/B/C, units, raw values, validation evidence, a graph/PES conclusion, and limitations. Do not cite the paper or SI as a substitute for calculations.
