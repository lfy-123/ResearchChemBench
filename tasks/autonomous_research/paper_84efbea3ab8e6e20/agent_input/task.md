# Scientific objective

Independently investigate whether positional isomerism of Bpin-substituted carbazole (CZ1B, CZ2B, CZ4B) changes excited-state structure and SOC in a way that can explain differences in blue RTP persistence in PVA films. Formulate and discriminate plausible explanations using calculations and report what the evidence does and does not establish.

# Public inputs and scientific boundaries

Use `data/inputs/molecules.json`. It defines the uniquely named neutral singlet molecules CZ1B (1-substituted), CZ2B (2-substituted), and CZ4B (4-substituted), all C18H20BNO2 with charge 0 and multiplicity 1. The listed CCDC identifiers are provenance metadata only: no CIF is supplied or required, and CCDC database retrieval is not required or scored. Generate molecular geometries from the explicit names and positional identities. Computation concerns isolated molecules; 0.5 wt% PVA is only the experimental measurement boundary. The task does not provide or imply an author route, preferred mechanism, winning isomer, result direction, software, model chemistry, geometry, or state. Do not use the paper or SI as an Agent input.

# Required scientific validation/investigation

Define a finite, reproducible candidate/state plan before calculation, including geometry alternatives if used, deduplication, advancement criteria, and a stopping rule. Attempt all three named molecules, optimize or otherwise validate usable ground-state structures, calculate S1 and nearby triplets, and define a quantitative near-state window or justify another common state-selection rule. For every retained SOC pair report state identity, energies, units, and validation evidence; provide NTOs or an equivalent state-character analysis and compare at least two plausible explanations for any lifetime trend. Completion requires three-molecule coverage, explicit search coverage/stopping, and a conclusion or bounded failure report. Stop after the planned candidate/state space is exhausted or all three systems have defensible validated calculations; preserve failed candidates and limitations instead of silently dropping them.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include the search plan and coverage, per-candidate identity and validation context, computed observables, discriminated hypotheses, and a conclusion tied to the experimental PVA lifetime boundary. A bounded-failure branch must report what was attempted and why a final comparison could not be made. Do not invent a discovery story or claim that an uncomputed host effect was directly calculated.
