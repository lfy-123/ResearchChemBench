# Private paper route and benchmark interpretation

## Scientific object and author route

Compound 7a is the source-labeled neutral singlet C20H17ClN6OS, with the correct pyrazole substitution, E C17=N3 imine and N5-H thione. See main PDF Fig.3/section 3.2 and private CCDC 2266402. The paper's section 2.4 (PDF pp3–4) uses gas-phase B3LYP and CAM-B3LYP with 6-311+G(d,p); section 3.3 compares molecular geometry with SCXRD. The conclusion (p11) favors CAM for geometry and IR. The current task isolates geometry comparison; frequencies validate minima and do not require an experimental IR comparison.

## Source observations and unresolved source-table issues

SI Tables S1–S3 (pp8–10) have 13 bond, 24 angle and 11 torsion rows. C6-N1-C7 repeats in the angle table, leaving 23 unique angles. Cl1/Cl2 refer to the same chlorine. The public 47-row CSV contains experimental observations only and is unchanged. Two theoretical columns coincide in 39/47 unique rows, including all torsions; B3LYP's N5-C18/N6-C19 entries appear exchanged. Record these observations without correcting the source or claiming how the authors produced the tables.

## Actual successful verification

Four correct-object G16 C.01 Opt/Freq logs exist in group_2. Two methods from the same source-CIF molecular start give a uniform CAM advantage in the six separately measured MAE/RMSE metrics. Another common correct-object start, partially reconstructed with SI information, yields lower CAM bond/angle errors but lower B3LYP torsion errors. Each endpoint has 132 positive frequencies. Exact SI theoretical small-decimal values were not reproduced. Main text software naming and reference [27] differ; the actual verification settings, not assumed author defaults, are recorded in evaluation/verified_computation_reference.md.

The earliest successful logs used a wrong positional isomer and cannot certify current 7a. They remain historical in task_provenance, not operative evidence.

## Approved comparison and scoring repair

The benchmark-authored geometry_comparison.json defines signed torsions, circular differences and whole-vector reference inversion equivalence. ONE sign applies to all 11 torsions for each model, chosen by minimum SSE then MAE/tie rules; raw values remain signed. This resolves representational mirror sensitivity, not real conformer dependence. Bonds/angles/torsions retain separate units and six metrics; no hidden aggregate or preferred winner.

The task asks for the supported method comparison: uniform dominance, mixed results or a numerical tie can all be complete. The author CAM-wins claim remains a source hypothesis, not a requirement for every independently generated legal conformer. A mixed result completes the task but does not confirm that hypothesis. Missing/invalid calculations remain incomplete. AR independently selects and justifies its models; PR retains the author pair and basis. Four substantive key points support ONE primary final conclusion. Generic limitation prose and unrelated IR claims earn no independent points.

## Data boundary

The agent receives the mapped E-imine/N5-H graph, fixed selectors, pure experimental reference observations, and a calculation-independent public comparison protocol. It generates initial 3D coordinates itself; no private crystal or optimized endpoint is provided. Historical source-informed verification demonstrates scientific calculability, not blind-agent replay, all-start convergence or global conformer search. All private references and provenance must remain evaluator-side. Directory remains HOLD during this authorized repair; no automatic release move is performed.
