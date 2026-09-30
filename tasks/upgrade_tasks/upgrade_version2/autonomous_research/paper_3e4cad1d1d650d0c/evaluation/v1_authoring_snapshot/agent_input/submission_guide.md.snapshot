# Submission guide

The contract requires both report/results.json and report/report.md. `status=complete` requires every named panel and every member of its matrix; it does not guarantee scientific validity. `bounded_failure` or `blocked` requires a failure_report and verdict not_established.

Each numerical row binds to calculation_ids and evidence_files. These IDs must resolve to calculation_records. Evidence paths must be relative below outputs/, structures/ or analysis/; a harmless ./ segment is permitted, while .. traversal is prohibited. Supply actual files, not only names. Electronic-structure records require basis, q/M and geometry role; completed engine records additionally require geometry, electronic energy and state identity. Analysis records instead require analysis_type and source_evidence_files and do not invent an electronic energy. A pre-engine failure may submit zero calculation_records and engine_calls=0 with an actual attempt/diagnostic log and failure_report; it cannot claim scientific completion. Record method/version, solvent, units and energy zero. Preserve absolute energies before taking differences; report constrained single points separately from free energies of minima.

## results.oxidation_cycle

Calculate and minimum-validate all four donor/radical states in DMSO; record electronic/thermal terms, radical spin contamination and a common solution standard state. Recompute the anchored relative cycle and compare its ordering with HOMO ordering. Never use gas ΔSCF directly as a solution potential.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.excited_ET

Use the measured crossings and one-electron convention to compute Eox* and ΔGET for both donors with the same acceptor and SCE zero. Distinguish electrochemical uncertainty, dissociative reduction and equilibrium free energies.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## results.quenching_challenge

Freeze the redox cycle before evaluating the intensity/lifetime challenge. Use the supplied original Figure3 crop to test dynamic and static/association explanations. A numerical lifetime-change upper bound must explicitly be a plot-resolution estimate, with axis/marker calibration and analysis evidence; it is not an instrument uncertainty. If a quantitative bound cannot be justified, submit lifetime_evidence_kind=qualitative_only and lifetime_change_fraction=null with the supported qualitative challenge and its resolution limit. Raw individual lifetime measurements and errors are unavailable and must not be invented. Favorable ΔGET does not settle the quenching mechanism or yield.

Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.

## Evidence and interpretation

Submit calculation input/output, final geometries with atom correspondence, frequency results when claiming minima, state/tensor/orbital data when relevant, and analysis code/tables sufficient to recompute the panels. Report per-attempt provenance and failures. The resources object records actual engine-call count, elapsed time and available CPU/memory accounting; null CPU or memory means unmeasured, never zero-cost evidence. Sensitivity requires numerical baseline and perturbation under a stated unit and uncertainty model. Do not invent a precision or tolerance from the old task. `indistinguishable` is a conclusion after the required comparisons, not an alternative to doing them. Optional extensions are not required.
