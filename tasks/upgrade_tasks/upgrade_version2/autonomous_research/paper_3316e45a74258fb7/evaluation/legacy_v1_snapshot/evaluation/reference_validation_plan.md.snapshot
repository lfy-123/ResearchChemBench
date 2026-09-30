# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main pp2–5, Figure1 molecular layouts and excited-state analysis; official publisher SI sections I/II, S3–S6 and TableS1. Verified three systematic names with OPSIN and RDKit formulas C72H49N7/C72H47N7/C72H45N7. SI has mislabeled intermediates, a copied TD-2C product name and ambiguous basis shorthand; heading structures and HRMS resolve connectivity, not calculated state assignments.

- `papers/paper_3316e45a74258fb7/documents/main.pdf` — [2, 3, 4]
- `tasks/upgrade_tasks/coordination_20260927/batch5/source_review/paper_3316e45a74258fb7.publisher_si.docx` — Relevant methods, experimental observations and identity blocks; see source review.
- `docs/evalution/update/paper_3316e45a74258fb7.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- No new fixed-torsion, conformer, SOC or adiabatic reference matrix has been calculated.
- Resolve basis shorthand explicitly and calibrate CT-state/method uncertainty.

## Callable route and pilot

Gaussian or ORCA for DFT/TDDFT and supported SOC; Multiwfn or documented equivalent for transition densities. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Check each graph/formula and one two-conformer TD_2T calculation, SOC interface and root matching before the six-cell comparison.

## Minimum complete reference

1. Generate independently initialized conformers, build the common torsion intervention, and calculate energies, oscillator strengths, fragment-resolved transition densities and SOC for matched low states in all six cells.
2. Follow S1 and T1 relaxation for each member and explicitly separate vertical and adiabatic gaps. Preserve conformer and root-switch diagnostics.
3. Compare changes at site 11 and sites 3/6, then quantify the shift from fixed to relaxed torsions and a decisive method sensitivity. Evaluate both CT-based and geometry-based explanations.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
