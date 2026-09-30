# Submission guide

The contract requires both report/results.json and report/report.md. `status=complete` requires every named panel and every member of its matrix; it does not guarantee scientific validity. `bounded_failure` or `blocked` requires a failure_report and verdict not_established.

Each numerical row binds to calculation_ids and evidence_files. These IDs must resolve to calculation_records. Evidence paths must be relative below outputs/, structures/ or analysis/; a harmless ./ segment is permitted, while .. traversal is prohibited. Supply actual files, not only names. Electronic-structure records require basis, q/M and geometry role; completed engine records additionally require geometry, electronic energy and state identity. Analysis records instead require analysis_type and source_evidence_files and do not invent an electronic energy. A pre-engine failure may submit zero calculation_records and engine_calls=0 with an actual attempt/diagnostic log and failure_report; it cannot claim scientific completion. Record method/version, solvent, units and energy zero. Preserve absolute energies before taking differences; report constrained single points separately from free energies of minima.

## results.bridge_torsion

Validate all four neutral singlet structures; evaluate corresponding singlet/triplet states and NTO/CT character at relaxed and common 60° arm torsions. Report actual mapped dihedrals, f for allowed singlets and state windows. Recompute 2T1−S1 with a single vertical reference.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.adiabatic_states

Optimize/track S1 and T1 and report absolute energies alongside adiabatic gaps relative to S0. Inspect identity, root changes and triplet spin. A failed excited-state optimization must be bounded failure, not a vertical energy relabeled adiabatic.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.difference_of_effects

Calculate bridge effects on the specified TTA margin in relaxed and matched-torsion panels and their difference. Compare localization changes with the proposed explanation. Composition and geometry confounds must be explicit; compatible energetics cannot prove bimolecular TTA.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## Evidence and interpretation

Submit calculation input/output, final geometries with atom correspondence, frequency results when claiming minima, state/tensor/orbital data when relevant, and analysis code/tables sufficient to recompute the panels. Report per-attempt provenance and failures. The resources object records actual engine-call count, elapsed time and available CPU/memory accounting; null CPU or memory means unmeasured, never zero-cost evidence. Sensitivity requires numerical baseline and perturbation under a stated unit and uncertainty model. Do not invent a precision or tolerance from the old task. `indistinguishable` is a conclusion after the required comparisons, not an alternative to doing them. Optional extensions are not required.
