# Scientific objective

For the two explicitly defined singlet fluorene anions in `data/inputs/system.json`, independently determine whether their substituent identities produce different Kohn–Sham HOMO energies in a DMSO continuum. Optimize, validate, and compare the two systems without relying on an author-proposed mechanism or route. Report each HOMO energy in eV and a cautious conclusion about the observed electronic difference.

# Public inputs and scientific boundaries

The public objects are `system_A` (9-phenylfluoren-9-yl anion) and `system_B` (9-[4-(trifluoromethyl)phenyl]fluoren-9-yl anion), with explicit SMILES, charge −1, and singlet multiplicity in `data/inputs/system.json`. Use isolated molecules without counterions and a DMSO continuum. The scored observables are the HOMO energy of each named object in eV and the sign of their submitted difference; the process observables are geometry convergence and harmonic-minimum evidence. Choose and report the computational method, basis, solvation implementation, settings, and any conformer coverage independently. The paper and SI are not available as task inputs.

# Required scientific validation/investigation

Construct at least one chemically valid 3D starting geometry for each named molecule and optimize both while preserving the supplied connectivity, charge, and multiplicity. If you explore multiple initial conformers or aryl orientations, state the generation and deduplication rule, retain the identity of every candidate, and explain why the reported candidate is used. Validate every reported structure with harmonic frequencies or an explicitly justified stationary-point test and report imaginary modes. Extract each HOMO from its validated final wavefunction. Completion requires validated HOMO values for both systems and a comparison based on those values; if convergence or validation fails, use the bounded-failure branch and document attempts and limitations. Stop after validated minima are obtained for both systems, or after three independently initialized failures for a system share the same diagnosed cause. Do not replace a failed system with another molecule.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include exactly one named per-system record for each public ID, in the same order as `data/inputs/system.json`; the `id` field is the binding identity for each record. Include methods and versions, starting-geometry provenance, convergence and frequency evidence, HOMO values where available, the computed difference when both values exist, and a conclusion with uncertainty/limitations. If bounded failure prevents a two-value comparison, explicitly state that the comparison is unavailable and identify the limitation. Do not cite or infer any paper-specific route.
