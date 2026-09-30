# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main pp4–6; SI pp7–8 method, source S0/S1/T1/T2 coordinate sections pp24–30. Derived only IR780/Cy1/Cy2 graph identities; verified rubrene named graph C42H28. Formulas show backbone differences, so a simple I-versus-Se matched causal claim is not supported by identities.

- `papers/paper_e0791c047a731974/documents/main.pdf` — [4, 5, 6]
- `papers/paper_e0791c047a731974/documents/supplementary_001.pdf` — [7, 8, 24, 30]
- `docs/evalution/update/paper_e0791c047a731974.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- New SOC, independent rubrene energetics, geometry intervention and relativistic uncertainty are uncomputed.

## Callable route and pilot

ORCA TDDFT/SOC with supported relativistic basis/operator; Gaussian for source-condition energies; Multiwfn transition analysis. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Verify Cy2 heavy-element SOC and root tracking, then rubrene T1/S1 identity before expanding three sensitizers.

## Minimum complete reference

1. Generate independent conformers for all sensitizers, validate S0 and calculate state-resolved energy, oscillator/NTO and SOC windows with root tracking.
2. Calculate independent rubrene S1/T1 and sensitizer T1 adiabatic energies and form the stated TTET and acceptor-annihilation balances.
3. Run the Cy2 planar/released intervention and a real SOC-method sensitivity; assess localized heavy-atom character and scope of any mechanistic inference.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
