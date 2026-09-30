# Scientific objective

Independently discover and validate low-energy structures of the fixed isolated Cu2In2Te2 cluster in charge states 0 and −1, then calculate the neutral HOMO–LUMO gap and binding energy and the anion adiabatic and vertical detachment energies. If multiple plausible structural explanations remain, discriminate them with calculations and state the surviving interpretation.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that this n=2 composition is especially stable and that its neutral low-energy structure is three-dimensional, associated with a flat rhombus and triangular-prism motif. They also describe a large neutral frontier-orbital gap and a distinct low-lying anion geometry.

**Candidate route or mechanism.**
Among the candidate structures, compare symmetric and nonsymmetric arrangements in both planar and three-dimensional forms, including three-dimensional motifs related to a flat rhombus or triangular prism. For the anion, examine whether relaxation produces or favors an In–In contact and associated changes in Cu–Te and Cu–In connectivity. These are candidate interpretations to test.

**Discriminating evidence.**
Use optimized relative energies across distinct candidates, structural metrics such as contacts and angles, and electronic-property calculations. Compare neutral and anion structures and use restart or method/basis/cutoff/cell sensitivity together with structural or electronic cross-checks to determine whether the proposed motifs and property trends remain supported.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. It defines exactly two Cu atoms, two In atoms and two Te atoms (six atoms total), charge 0 and −1, singlet neutral and doublet anion unless a documented method-specific alternative is justified, and an isolated-cluster vacuum boundary with no solvent, ligands or counterions. No author route, candidate structure, paper label or result is supplied. Generate 3-D coordinates yourself. Report atom identities, connectivity interpretation, charge, multiplicity, cell/vacuum treatment, method and all energy conventions. Lengths are in Å and energies are in eV.

# Required scientific validation/investigation

Define and execute a finite, chemically diverse candidate-generation protocol covering plausible planar and non-planar arrangements for both charge states, and explain its coverage. Optimize every advanced candidate with a stated electronic-structure method. Deduplicate using an explicit geometry/connectivity criterion, retain candidate identity, and report failed or discarded optimizations. A candidate may advance to property calculations only if the optimization converges, has no imaginary mode if a vibrational check is performed (or the limitation is stated), and is not a duplicate. Compute relative energies within each charge state and identify the submitted lowest-energy candidate for each state. For the neutral minimum calculate the HOMO–LUMO gap and binding energy with an explicit atom/reference convention. For the anion calculate ADE from independently optimized neutral/anion minima and VDE at a clearly stated fixed geometry; report sign conventions. Validate with at least one independent restart, method/basis or cutoff/cell sensitivity check and one structural/electronic cross-check. Completion requires a reproducible candidate table and either (i) a success report containing both charge-state minima and all requested observables, or (ii) a bounded-failure report naming the failed stage, reason, and every result established before failure; do not invent minima or observables. Stop when the stated generation protocol has been exhausted and at least one additional generation/restart fails to produce a distinct, converged lower-energy minimum; otherwise report the unclosed search and its limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include candidate identities and structures (file paths or inline coordinates), energies, validation evidence, selected minima, requested observables, method metadata, uncertainty/limitations, and a conclusion about the discovered structural/electronic picture. A bounded-failure submission must identify the failed stage and still provide all successfully established candidates and evidence.
