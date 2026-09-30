# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main computational methods p3, Table1, halochromic/NMR discussion pp4–6 and official SI acid/neutral/base NMR and coordinate blocks. Extracted only the neutral C30H20N6O4 graph. Source aqueous absorption and DMSO NMR require distinct solution models. Formal SI Table S2 resolves exact experimental assignments; no expanded spectral/cycle reference exists. Formal SI Table S2 directly resolves the columns: experimental neutral 6.80, base 6.10, acid 6.95 ppm; calculated 6.95/6.35/7.98 are private reference values. Added a valence-checked neutral lactam-to-lactim seed by moving mapped H8 from N11 to O9 and swapping N11-C6/C6-O9 bond orders. This is a candidate-generation intervention, not a new chemical result. Explicit failed/collapsed branches do not require fictional free energies.

- `papers/paper_988bc12ae3768679/documents/main.pdf` — [5, 6]
- `tasks/upgrade_tasks/coordination_20260927/batch5/source_review/paper_988bc12ae3768679.publisher_si.docx` — Relevant methods, experimental observations and identity blocks; see source review.
- `docs/evalution/update/paper_988bc12ae3768679.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- New candidate energies, collapse checks, joint spectral residuals and balanced proton reference are uncomputed.
- Per-observable calibrated uncertainty and mixture identifiability remain uncomputed; experimental Table S2 assignments are verified.

## Callable route and pilot

Gaussian or ORCA DFT/TDDFT/NMR with diffuse functions and explicit solvent conventions; Python/RDKit for graph and mixture audits. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Check parent graph, two distinct acid/base seed valences and paired solvent calculations; validate NMR reference and proton-exchange convention before expanding.

## Minimum complete reference

1. Construct the supplied site and tautomer alternatives, add further symmetry-distinct candidates only when motivated, and document conformers, charges and bond/proton maps without presupposing the acid/base assignment.
2. Calculate matched-solvent NMR and UV predictions for all retained competitors; test individual and bounded-mixture interpretations with one uncertainty policy.
3. Close proton-reference cycles, compare populations consistently and repeat the decisive solvent/reference/model choice. Report only assignments supported jointly by both observations.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
