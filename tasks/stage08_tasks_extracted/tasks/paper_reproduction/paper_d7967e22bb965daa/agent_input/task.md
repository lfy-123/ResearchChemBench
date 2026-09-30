# Scientific objective

Using the four supplied, labeled quartet starting geometries for TS3A-quartet, TS3B-quartet, TS3C-quartet, and TS3D-quartet, compute and compare their relative free-energy barriers for the model reaction of 1,1,2,2-tetraphenyldisilane (1a) with 4-phenyl-1-butyne (2a) catalyzed by L10·FeCl2. Assess whether the quartet migratory-insertion transition-state comparison supports a regioselectivity explanation in the stated model. The research object is the quartet migratory-insertion transition-state comparison, not an exhaustive search for additional transition states.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors attribute the regioselectivity of the L10-supported iron-catalyzed hydrodisilylation model to alkyne migratory insertion into an Fe–H species. They propose that the chiral oxazoline/quinoline environment of the OPQ ligand favors one approach through steric organization around the transition state.

**Candidate route or mechanism.**
The relevant proposed alternatives are the four supplied quartet migratory-insertion approaches, TS3A-quartet through TS3D-quartet, compared against the assembled INT1A-sextet plus 2a reference. The comparison concerns competing regioisomeric alkyne-insertion approaches within the L10·FeCl2/1a/2a model cycle and should retain the candidate labels throughout refinement and analysis.

**Discriminating evidence.**
Use stationary-point optimization or refinement, vibrational classification and imaginary-mode displacement analysis, consistent relative free-energy assembly against the stated reference, and comparison of the candidates' steric or distortion characteristics. Spin-surface checks and method or conformational sensitivity analyses can be used to test whether the proposed regioselectivity interpretation is supported by the computed quartet comparison.

# Public inputs and scientific boundaries

The directory `data/inputs` contains four XYZ files named `TS3A_quartet.xyz`, `TS3B_quartet.xyz`, `TS3C_quartet.xyz`, and `TS3D_quartet.xyz`. Each file has 68 atoms, Cartesian coordinates in Å, and a label identifying the candidate; atom ordering must be preserved within each candidate. These are starting geometries for quartet Fe-containing transition-state candidates in the L10·FeCl2/1a/2a model system. The chemical model is neutral overall with the quartet spin state (multiplicity 4) for each supplied structure. The reference system is the separately assembled INT1A-sextet complex plus one 4-phenyl-1-butyne (2a) molecule, with the INT1A-sextet component on multiplicity 6 and 2a closed shell; define and document the reference geometry and atom mapping used to assemble it. If an independent calculation uses a different but explicitly documented reference convention, report the transformation and do not silently mix conventions.

The requested observables are (i) the number and character of imaginary frequencies for each optimized candidate, (ii) each candidate's relative barrier in kcal/mol on a stated thermochemical convention, and (iii) the resulting ordering and mechanistic interpretation. The task boundary is the four named inputs and their quartet state. Do not use the paper, SI, general web, or undisclosed source coordinates during the investigation.

# Required scientific validation/investigation

For every one of the four named candidates, perform a documented optimization or equivalent stationary-point refinement, a vibrational analysis, and an energy/free-energy assembly that makes the reference state and solvent/thermal treatment explicit. Validate a transition-state assignment by showing exactly one imaginary frequency and explaining from the displacement/eigenvector evidence that it corresponds to the intended Fe–H/alkyne migratory-insertion bond-making/bond-breaking motion. If a candidate does not converge or fails this test, retain its identity, report the failure and the attempted remedies, and give a bounded conclusion rather than replacing it with an unnamed structure.

Deduplicate only if an independently generated refinement is demonstrably the same stationary point; preserve the supplied candidate label and report any discarded duplicate. Completion requires either validated results for all four labels or an explicit bounded-failure report that identifies every unresolved label and why the four-way comparison cannot be completed. If the four-way comparison is incomplete, report no invented barrier value or ordering for unresolved labels. Stop after all four supplied labels have been attempted, validated or documented as failed, and no further unnamed candidate search is required. Report method sensitivity, spin-contamination concerns, conformational limitations, and any alternative validation method used.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. It must contain a per-candidate record for TS3A-quartet through TS3D-quartet, including status, optimized-structure evidence, imaginary-frequency evidence, relative barrier when available, and limitations. Include the barrier ordering when a four-way comparison is possible, a final mechanistic conclusion, the reference-state/energy convention, and a concise coverage/stopping statement. Include enough provenance (software, method, charge, multiplicity, coordinates/optimization and frequency outputs or hashes) for an evaluator to audit that each result belongs to the named 68-atom input.
