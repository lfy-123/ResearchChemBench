# Scientific objective

Determine how 0%, −2% and +2% uniaxial strain along the crystallographic b (interlayer) direction changes the electronic band-gap character of the supplied K0.5WTe2 P21/m crystal. The authors propose that catalyst-free structural distortion along this direction can close the gap; independently test that hypothesis by planning and performing calculations. Report band extrema, gap character, and near-Fermi orbital character.

# Public inputs and scientific boundaries

Use `data/inputs/k05wte2_p21m.json`, which uniquely specifies formula, charge, multiplicity, space group, cell, labeled fractional coordinates, and the three b-scale perturbations. Generate Cartesian coordinates and any symmetry-complete cell deterministically. You may choose software, functional, dispersion, pseudopotentials, smearing, convergence thresholds, k mesh and band path, but disclose them. The measured object is the electronic band structure and fundamental gap/overlap in each of the three explicitly named structures. Do not use the paper, SI or general web. The experimental narrow-gap-semiconductor statement is contextual only.

# Required scientific validation/investigation

Relax or otherwise justify each starting structure, and demonstrate numerical convergence appropriate to your method. For each named strain state, compute a self-consistent electronic structure and a band path or dense reciprocal-space sampling sufficient to identify the valence maximum, conduction minimum, and any Fermi-level crossing. Deduplicate repeated calculations by state and retain state identity. Classify each state as semiconducting (positive fundamental gap), zero-gap semimetal (touching with no finite separation), or metallic (Fermi-surface crossing/overlap), with an operational definition and units. For every state, report its explicit public state id, the structure used, state-specific relaxation/justification, convergence evidence, reciprocal-space extrema or crossing basis, and orbital projections or another reproducible basis for near-Fermi orbital character. Compare all three states and report limitations. Completion is successful only when all three states have these results and validation records; stop after that criterion is met. If a method cannot resolve a state, submit a bounded-failure outcome naming the state and missing evidence, with unavailable numerical values represented as null rather than fabricated.

# Deliverables

Submit `report/results.json` conforming to the schema. Include method, per-state structures and validation records, numerical or categorical gap results, extrema, orbital evidence, comparison, limitations, and a conclusion. Include enough provenance to reproduce the actual calculations.
