# Scientific objective

Independently plan and execute a defensible calculation for the fixed neutral-singlet axial galactose-derived tributyltin molecule in `data/inputs/compound_1a_axial.xyz`. Test the authors' qualitative hypothesis that antiperiplanar donor-to-σ*(C–Sn) hyperconjugation influences one-bond tin–carbon coupling, while determining the average signed ^1J(^119Sn–^13C_Bu) coupling over the three butyl carbons bonded directly to Sn.

# Author-provided scientific guidance

The qualitative hyperconjugation proposal is interpretive context for the specified three couplings. This task does not require an equatorial analogue, NBO causal decomposition or a separate anomeric-carbon coupling.

The author hypothesis is qualitative only: stronger donation is expected to weaken/lengthen C–Sn and lower coupling magnitude, and an equatorial analogue would generally be expected to have a larger coupling; no target value or winning calculation is supplied.

# Public inputs and scientific boundaries

Report the three full signed one-bond 119Sn–13C couplings and their arithmetic mean. Do not substitute absolute values, Fermi-contact-only terms or empirical scaling for the declared full coupling. In `report/results.json`, `sn_bu_pairs` must use the original 1-based indices of the supplied XYZ: Sn=1 and butyl carbons=2,3,7. Calculation programs may reorder atoms, but map the reported pairs back to these original indices and provide the complete original-to-working index mapping with the supporting files when reordering occurs. The optional anomeric-carbon result does not affect completion.

The sole molecular input is the 62-atom XYZ file, whose first line gives atom count and whose comment declares charge 0 and multiplicity 1. The supplied atom order defines the reporting indices, not a restriction on program-internal ordering. The Sn atom is atom 1; in the supplied geometry the three directly bonded butyl carbons are the three closest carbon atoms to Sn (atoms 2, 3, and 7, approximately 2.18–2.20 Å initially). Reconfirm that assignment from the final geometry and report atom indices and distances explicitly. The system boundary is the isolated molecule; solvent may be added only as a separately labelled sensitivity test. The measured quantities are optimized-geometry minimum evidence, signed ^1J(^119Sn–^13C) for each identified Sn–butyl carbon pair, their arithmetic mean in Hz, and optionally the anomeric Sn–C coupling if the corresponding carbon is identified unambiguously. Do not use the paper, SI, general web, or hidden reference values.

# Required scientific validation/investigation

Choose and justify the electronic-structure and relativistic/NMR method. Optimize the supplied structure and perform a vibrational or equivalent stationarity check; report whether the final structure is a minimum and give the evidence (for example, imaginary-frequency count). Compute the three individual one-bond Sn–C_Bu couplings and the mean, stating sign convention, isotope treatment, units, geometry, and software. Validate atom-pair assignment from the final geometry rather than silently assuming labels. If the preferred calculation fails, submit a bounded-failure report with logs and the last valid geometry/results. Completion requires a converged, validated calculation with all three couplings and their mean. Otherwise submit a failure/partial report with reproducibility details and any completed results. Discuss how the result bears on the qualitative hypothesis without importing the paper's numerical answer.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to `submission_schema.json`, plus supporting files under `report/` as needed (input-to-output atom mapping, optimization/frequency and NMR logs, and method details). The JSON must include status, method, minimum validation, explicit pair identities, individual couplings when available, mean coupling when available, computational evidence, and a concise scientific conclusion.
