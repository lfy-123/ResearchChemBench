# Scientific objective

Using independent computational chemistry, determine which of the two specified diastereomeric configurations of neutral compound 10 is better supported by the supplied experimental 13C and 1H NMR data.

# Public inputs and scientific boundaries

Use every field in `data/inputs/compound10_nmr.json`. The research object is the neutral, closed-shell C11H16O4 molecule with the supplied constitution, atom-label convention, and candidates candidate_A (7R,8R) and candidate_B (7R,8S). The measured observables are the listed DMSO-d6 13C and 1H chemical shifts. You may generate conformers and select computational methods, but do not alter connectivity, charge, multiplicity, atom labels, or experimental observations. Base the scored comparison on this supplied system and these observables.

# Required scientific validation/investigation

Propose and execute an independent finite comparison of both candidates. Choose and justify the computational approach; generate and document a conformer set, deduplicate it, validate optimized/stable structures, predict atom-matched 13C and 1H shifts, and compute fit statistics. Apply DP4+ or a mathematically specified equivalent probabilistic comparison to the same candidate set. Explain why the candidate set and conformer search are adequate for this objective, report coverage and all failures, and state a stopping rule: stop after the declared conformer-generation and validation protocol is exhausted. Completion requires auditable evidence for both candidates; a bounded-failure outcome must identify the failed calculation and remaining limitation. The submission must use the bounded-failure outcome when a required calculation cannot be completed; it must not invent shifts, fit values or probabilities.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include candidate identities, per-candidate conformer and validation context, calculated carbon/proton shifts or an explicit bounded-failure branch, fit metrics, probabilities, method details, uncertainty/limitations, and a conclusion identifying the better-supported candidate only when supported by the submitted evidence.
