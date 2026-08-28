# Scientific objective

Determine which of the two specified diastereomeric configurations of neutral compound 10 is better supported by independent computational comparison to the supplied experimental 13C and 1H NMR data. The paper’s qualitative hypothesis is that NMR comparison of these two candidates can resolve the configuration; test that hypothesis independently without using the paper’s numerical answer.

# Public inputs and scientific boundaries

Use every field in `data/inputs/compound10_nmr.json`. The research object is the neutral, closed-shell C11H16O4 molecule with the supplied constitution, atom-label convention, and candidates candidate_A (7R,8R) and candidate_B (7R,8S). The measured observables are the listed DMSO-d6 13C and 1H chemical shifts. You may generate conformers and choose computational methods, but do not alter connectivity, charge, multiplicity, atom labels, or experimental observations. Do not use the paper, SI or general web as an input.

# Required scientific validation/investigation

For both candidates, choose and justify a computational approach, generate a documented finite conformer set, state how conformers were deduplicated and advanced, and optimize or otherwise validate the structures as minima/stable states. Predict atom-matched 13C and 1H shifts, report the method/solvent/shielding convention, and compute fit statistics for each candidate. Apply DP4+ or a mathematically specified equivalent probabilistic comparison to the same candidate set. Completion requires both candidates to have auditable conformer coverage, atom matching, predicted shifts, fit metrics and probability outputs. Stop when the stated conformer-generation/validation protocol is exhausted; if a calculation fails, report the failed candidate and a scientifically justified bounded limitation rather than silently substituting data. The submission must use the bounded-failure outcome when a required calculation cannot be completed; it must not invent shifts, fit values or probabilities.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include candidate identities, per-candidate conformer and validation context, calculated carbon/proton shifts or an explicit bounded-failure branch, fit metrics, probabilities, method details, uncertainty/limitations, and a conclusion identifying the better-supported candidate only when supported by the submitted evidence.
