# Scientific objective

Independently investigate whether positional isomerism of Bpin-substituted carbazole (CZ1B, CZ2B, CZ4B) changes excited-state structure and SOC in a way that can explain differences in blue RTP persistence in PVA films. Formulate and discriminate plausible explanations using calculations and report what the evidence does and does not establish.

# Public inputs and scientific boundaries

Use `data/inputs/molecules.json`. It defines the uniquely named neutral singlet molecules CZ1B (1-substituted), CZ2B (2-substituted), and CZ4B (4-substituted), all C18H20BNO2 with charge 0 and multiplicity 1. The listed CCDC identifiers are provenance metadata only: no CIF is supplied or required, and CCDC database retrieval is not required or scored. Generate molecular geometries from the explicit names and positional identities. Computation concerns isolated molecules; 0.5 wt% PVA is only the experimental measurement boundary. The task does not provide or imply an author route, preferred mechanism, winning isomer, result direction, software, model chemistry, geometry, or state. Do not use the paper or SI as an Agent input.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

Experimental lifetimes and their ordering are not supplied. The evaluator will compare your molecular evidence with its private experimental reference. You are not required to reproduce or infer that hidden experimental ranking, predict absolute film lifetimes, or access the paper. Submit `conclusion.computed_comparison`, `interpretation`; all required SOC and state-character evidence remains mandatory.

# Required scientific validation/investigation

Define a finite, reproducible candidate/state plan before calculation, including geometry alternatives if used, deduplication and advancement criteria. Attempt all three named molecules, optimize or otherwise validate usable ground-state structures, calculate S1 and nearby triplets, and define a quantitative near-state window or justify another common state-selection rule. For every retained SOC pair report state identity, energies, units, and validation evidence; provide NTOs or an equivalent state-character analysis and interpret the computed cross-isomer differences using the calculated state-character evidence. Do not guess an unprovided experimental lifetime trend. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include the search plan and coverage, per-candidate identity and validation context, computed observables, discriminated hypotheses, and a computed cross-isomer comparison supported by the calculated molecular observables. A bounded-failure branch must report what was attempted and why a final comparison could not be made. Do not invent a discovery story or claim that an uncomputed host effect was directly calculated.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
