# Scientific objective

Determine, for the uniquely specified singly deprotonated E-imine dye-3 chromophore in implicit dichloromethane, the lowest-energy visible singlet Franck–Condon excitation from an optimized ground-state structure. Report the excitation energy in kcal/mol, oscillator strength when available, and the evidence supporting the electronic assignment. The object is the molecule in `data/inputs/dye3_phenolate.smiles`; do not substitute dyes 2 or 4–6.

# Author-provided scientific guidance

Test the authors' qualitative hypothesis that this band is a phenolate-donor to nitroaryl-acceptor intramolecular charge-transfer (ICT) transition.

# Public inputs and scientific boundaries

For this task, the primary visible comparison window is 400–700 nm (inclusive), an operational benchmark definition rather than a paper-reported numerical result. Select the lowest-energy singlet within that window, not the brightest root or the root nearest a reference; use its computed electronic character to interpret, not to preselect, the result. If no root falls within the window, report the computed roots and a partial/failure outcome rather than silently substituting a UV state. A band shifted across a window boundary may be discussed separately with its physical correspondence; it is not an automatic alternative main result. Retain the lower-lying roots needed to justify the assignment. Report donor, acceptor and bridge contributions with the same declared partition; bridge delocalization is allowed and no hidden >50% acceptor threshold applies.

`data/inputs/dye3_phenolate.smiles` is the authoritative connectivity and formal charge: the E-imine of 4-aminophenol and 4-(5-nitrothiophen-2-yl)benzaldehyde, with a singly deprotonated phenolate (net charge −1). `data/inputs/system_spec.json` fixes charge −1, singlet multiplicity 1, dichloromethane implicit continuum (ε=9.08, n=1.424), and the target as the lowest-energy visible singlet excitation from the optimized ground-state minimum. Generate 3-D coordinates and document stereochemical/conformer choices. This is a vertical electronic-structure benchmark; solvent dynamics, vibronic envelopes, photochemistry, and an ensemble-average spectrum are outside scope. The paper's software, method, ordered protocol, numerical result, and selected geometry are not public instructions.

# Required scientific validation/investigation

Independently choose and justify a computational route compatible with the fixed system and boundary. Optimize the ground-state geometry, then demonstrate that the reported structure is a minimum using a frequency, Hessian, or an explicitly justified equivalent validation. Compute and identify the lowest-energy visible singlet transition, retaining state index, energy, oscillator strength, and orbital or transition-density evidence. Explicitly test the qualitative phenolate-to-nitroaryl ICT hypothesis by locating the donor and acceptor character in the computed transition. Record convergence settings, any alternative starting conformers or state assignments examined, and sensitivity that materially affects the conclusion. The calculation is complete when one converged candidate structure has a documented minimum validation and a state assignment supported by quantitative and electronic evidence.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to `submission_schema.json`. Include the validated structure or a reproducible structure reference, calculation provenance, minimum-validation evidence, the selected transition and its energy, and an evidence-based final conclusion. A bounded failure is acceptable only when the failure branch contains the attempted route, diagnostic evidence, and a scientifically specific failure cause.
