# Scientific objective

Establish, by an independent computational investigation, how 0%, −2% and +2% uniaxial strain along the crystallographic b (interlayer) direction changes the electronic band-gap character of the supplied K0.5WTe2 P21/m crystal. Determine whether either perturbation closes the gap and explain the electronic origin using reproducible calculations; do not assume a mechanism or preferred outcome.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that small uniaxial structural distortions along the interlayer b direction can substantially reduce the electronic gap of K0.5WTe2, with either sign of a 2% distortion potentially driving a gap-closing electronic response. The authors associate tensile distortion with the appearance of Te-derived states near the Fermi energy.

**Candidate route or mechanism.**
Compare the unstrained structure with b-axis compression and tension while retaining the stated strain definitions. The proposed comparison is that compression may produce a Fermi-level band crossing, whereas tension may produce a band touching or near-touching through changes in near-Fermi band dispersion and Te-related states. These are candidate interpretations to test for the three supplied states.

**Discriminating evidence.**
Use relaxed or justified structures, converged self-consistent electronic structures, and a sufficiently resolved band path or reciprocal-space sampling to distinguish a finite indirect gap, a zero-gap touching, and a Fermi-surface crossing or overlap. Inspect orbital projections or another reproducible near-Fermi orbital analysis, especially for Te contributions under tensile strain, and compare the curvature and extrema across all three states.

# Public inputs and scientific boundaries

Use `data/inputs/k05wte2_p21m.json`, which uniquely specifies formula, charge, multiplicity, space group, cell, labeled fractional coordinates, and the three b-scale perturbations. Generate Cartesian coordinates and any symmetry-complete cell deterministically. You may choose software, functional, dispersion, pseudopotentials, smearing, convergence thresholds, k mesh and band path, but disclose them. The measured object is the electronic band structure and fundamental gap/overlap in each of the three explicitly named structures. Do not use the paper, SI or general web. The experimental narrow-gap-semiconductor statement is contextual only.

# Required scientific validation/investigation

Formulate plausible explanations for strain-dependent changes, then discriminate them with calculations. Relax or otherwise justify each starting structure, and demonstrate numerical convergence appropriate to your method. For each named strain state, compute a self-consistent electronic structure and a band path or dense reciprocal-space sampling sufficient to identify the valence maximum, conduction minimum, and any Fermi-level crossing. Deduplicate repeated calculations by state and retain state identity. Classify each state as semiconducting (positive fundamental gap), zero-gap semimetal (touching with no finite separation), or metallic (Fermi-surface crossing/overlap), with an operational definition and units. For every state, report its explicit public state id, the structure used, state-specific relaxation/justification, convergence evidence, reciprocal-space extrema or crossing basis, and orbital projections or another reproducible basis for near-Fermi orbital character. Compare all three states and report independently formulated hypotheses, their tests and limitations. Completion is successful only when all three states have these results and validation records; stop after that criterion is met. If a method cannot resolve a state, submit a bounded-failure outcome naming the state and missing evidence, with unavailable numerical values represented as null rather than fabricated.

# Deliverables

Submit `report/results.json` conforming to the schema. Include method, per-state structures and validation records, numerical or categorical gap results, extrema, orbital evidence, comparison, independently formulated hypotheses and conclusion, limitations, and provenance sufficient to reproduce the actual calculations.
