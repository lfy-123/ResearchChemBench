# Scientific objective

Determine whether the three supplied stationary-point candidates of a charge −1 singlet free-base subporphyrin monoanion exhibit a Hessian/PES relationship consistent with a connectivity-motion graph for H tautomerism. Independently characterize each candidate and infer, from the structures and calculated modes, what graph/PES relationships are supported. Do not assume any author labels, route, mechanism assignment or result direction.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the connectivity-motion graph for H tautomerism in this free-base subporphyrin monoanion can correspond to the topology of the real-space potential-energy surface. Their interpretation uses stationary points whose Hessian order tracks the order of the associated connectivity motion, with normal modes directed toward graph neighbours.

**Candidate route or mechanism.**
A useful candidate interpretation is to examine whether the supplied set spans a local-minimum-like structure, a first-order saddle associated with one H-bonder motion between inner N sites, and a second-order saddle associated with two such independent connectivity motions. Test possible first-order links between adjacent stationary-point characters and a possible second-order relationship between the minimum-like and second-order-saddle-like structures, while allowing the coordinates to support a different assignment.

**Discriminating evidence.**
Use optimized stationary-point character, Hessian eigenvalue or imaginary-frequency counts, and inspection of the displacement patterns of the lowest modes, especially H motion between the inner N sites. Compare the explicit connectivity changes among candidates with those mode directions, and use energies and harmonic free energies as supporting observables rather than as substitutes for Hessian and mode evidence.

# Public inputs and scientific boundaries

The three public files `data/inputs/candidate_a.xyz`, `candidate_b.xyz` and `candidate_c.xyz` provide candidates A, B and C. Each record has an explicit atom order, element symbols and Cartesian coordinates in Å; all are the same single-molecule composition. Use charge −1 and singlet multiplicity for every record. The physical boundary is a single nondissociating free-base subporphyrin monoanion in implicit chloroform; the three inner N atoms are the connectivity sites and the inner H is the mobile bonder. Choose and justify the computational model and solvation treatment. The scored observables are electronic energy, the three lowest-frequency values including sign, harmonic thermal free energy, imaginary-frequency count, and mode/path interpretation.

# Required scientific validation/investigation

For each named candidate A/B/C, independently generate a defensible stationary-point calculation or documented equivalent. Verify convergence, inspect the Hessian, count negative/imaginary modes, and inspect whether imaginary modes involve H motion between inner N sites. Define an explicit structure/connectivity comparison and use it to infer plausible first- or second-order relationships; compare alternatives if the evidence is ambiguous. Completion requires either validated results for all three candidates or a bounded-failure report naming each failed candidate, cause, attempted remedy and the remaining conclusions that are and are not supported. Stop when all three candidates have a converged characterization or after two documented remediation attempts per failed candidate; report search coverage, method sensitivity and limitations.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus calculation logs/output and a short `report/methods.md`. The JSON must retain candidate identity A/B/C, units, raw values, validation evidence, an independently reasoned graph/PES conclusion, alternative interpretations where relevant, and limitations.
