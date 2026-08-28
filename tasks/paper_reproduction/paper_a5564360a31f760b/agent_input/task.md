# Scientific objective

Test the authors' qualitative hypothesis that B←N orientation and diazine identity alter S1→S0 structural relaxation: independently compute and compare the reorganization energy, RMSD, and mode-resolved displacement of reduced neutral-singlet p-2BN and m-2BN. The author hypothesis may guide interpretation, but no published numerical result or winning outcome is supplied.

# Public inputs and scientific boundaries

Use exactly the two objects in `data/inputs/molecular_records.json`. Resolve CCDC 1941938 as p-2BN and CCDC 2480480 as m-2BN, replace every octyl side chain by methyl as specified, and preserve connectivity/stereochemistry. Both objects are isolated, neutral, singlet molecules. The endpoint is relaxation between their lowest relevant singlet excited state S1 and singlet ground state S0. Solvent, crystal packing, counterions, and experimental observables are outside the target.

# Required scientific validation/investigation

Generate at least one defensible S0 and S1 geometry for each object and document optimization and frequency/stationary-point evidence, software/model choices, state definition, atom mapping, alignment and λ/RMSD formulas. Validate that no imaginary mode is being mistaken for a minimum (or explain and bound any exception). Calculate λ in eV and RMSD in Å for both named objects, and provide per-object mode or chemically grouped contributions with enough context to identify the atoms/groups. Check numerical stability with a stated alternative conformer, optimization, alignment, or analysis sensitivity where feasible. Completion has two truthful branches: in `success`, both objects have traceable state calculations, observables, validation evidence, sensitivity, and a conclusion; in `bounded_failure`, preserve completed calculations and identify each missing object/state and the concrete boundary, without fabricated numbers or structures. Stop after the stated checks are complete or at a documented computational boundary.

# Deliverables

Write `report/results.json` following the submission schema. Include provenance, structure mapping, methods, state-validation records, per-object observables, mode/group evidence, uncertainty/sensitivity, comparison, interpretation of the author hypothesis, and limitations. A successful result must identify both objects; a bounded-failure branch must identify the missing object/state and still report all completed calculations.
