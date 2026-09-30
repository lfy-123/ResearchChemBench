# Scientific objective

Independently determine whether the two reduced double-B←N isomers p-2BN and m-2BN exhibit different S1→S0 structural relaxation, using reorganization energy, RMSD, and mode-resolved displacement, and assess what structural explanation is supported by the calculations. Propose and discriminate plausible explanations from the computed evidence; do not assume an author route or mechanism.

# Public inputs and scientific boundaries

Use exactly the two objects in `data/inputs/molecular_records.json` and the supplied immutable CCDC files `data/inputs/ccdc_1941938.cif` (p-2BN) and `data/inputs/ccdc_2480480.cif` (m-2BN) directly. The CCDC record numbers are provenance only; CCDC database retrieval is not required or scored. Verify each CIF's internal archive ID, formula, element set, occupancy and cell, select the documented molecular component, then replace every octyl side chain by methyl as specified while preserving connectivity/stereochemistry and recording atom mapping. Do not edit the raw CIFs. Both objects are isolated, neutral, singlet molecules. The endpoint is relaxation between their lowest relevant singlet excited state S1 and singlet ground state S0. Solvent, crystal packing, counterions, and experimental observables are outside the target.

# Required scientific validation/investigation

Define a finite candidate set of state geometries/conformers generated from the two fixed structures, deduplicate it by a stated structural criterion, and explain which candidates advance to state optimization. Document optimization and frequency/stationary-point evidence, state definition, atom mapping, alignment and λ/RMSD formulas. Validate that no imaginary mode is being mistaken for a minimum (or explain and bound any exception). Calculate λ in eV and RMSD in Å for both named objects, provide per-object mode or chemically grouped contributions with atom/group identity, and test at least one sensitivity or alternative validation route where feasible. Completion has two truthful branches: in `success`, candidate coverage is accounted for and both objects have traceable state calculations, observables, validation evidence, sensitivity, and an evidence-based explanation; in `bounded_failure`, preserve completed evidence and identify each missing object/state and the concrete boundary, without fabricated numbers or structures. Stop when the stated candidate set and checks are exhausted or at a documented computational boundary.

# Deliverables

Write `report/results.json` following the submission schema. Include candidate-generation and deduplication records, provenance, structure mapping, methods, state-validation records, per-object observables, mode/group evidence, uncertainty/sensitivity, comparison, independently argued explanation, and limitations. A bounded-failure branch must identify the missing object/state and preserve all completed evidence.
