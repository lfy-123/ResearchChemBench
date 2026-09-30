# Scientific objective

Independently determine whether the two reduced double-B←N isomers p-2BN and m-2BN exhibit different S1→S0 structural relaxation, using reorganization energy, RMSD, and mode-resolved displacement, and assess what structural explanation is supported by the calculations. Propose and discriminate plausible explanations from the computed evidence; do not assume an author route or mechanism.

# Public inputs and scientific boundaries

Use exactly the two objects in `data/inputs/molecular_records.json`. Resolve CCDC 1941938 as p-2BN and CCDC 2480480 as m-2BN, replace every octyl side chain by methyl as specified, and preserve connectivity/stereochemistry. Both objects are isolated, neutral, singlet molecules. The endpoint is relaxation between their lowest relevant singlet excited state S1 and singlet ground state S0. The scored system is each isolated molecule; do not add a host or solvent. Crystal packing, counterions, and experimental observables are outside the target.

# Required scientific validation/investigation

Define a finite candidate set of state geometries/conformers generated from the two fixed structures, deduplicate it by a stated structural criterion, and explain which candidates advance to state optimization. Document optimization and frequency/stationary-point evidence, state definition, atom mapping, alignment and λ/RMSD formulas. Validate that no imaginary mode is being mistaken for a minimum (or explain and bound any exception). Calculate λ in eV and RMSD in Å for both named objects, provide per-object mode or chemically grouped contributions with atom/group identity, and test at least one sensitivity or alternative validation route where feasible. Completion has two truthful branches: in `success`, candidate coverage is accounted for and both objects have traceable state calculations, observables, validation evidence, sensitivity, and an evidence-based explanation; in `bounded_failure`, preserve completed evidence and identify each missing object/state and the concrete boundary, without fabricated numbers or structures. Stop when the stated candidate set and checks are exhausted or at a documented computational boundary.

# Deliverables

Write `report/results.json` following the submission schema. Include candidate-generation and deduplication records, provenance, structure mapping, methods, state-validation records, per-object observables, mode/group evidence, uncertainty/sensitivity, comparison, independently argued explanation, and limitations. A bounded-failure branch must identify the missing object/state and preserve all completed evidence. Conform all result keys and values to the local `submission_schema.json`.
