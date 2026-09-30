# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main p4 and SI pp10–11 computational/electronic-state discussion. Verified 165-atom full neutral complex formula and source method partition. Old isolated adiabatic scalar is only a baseline audit, not the new electronic-state matrix.

- `papers/paper_72822e4ddb5d9b11/documents/main.pdf` — [1, 4, 5]
- `papers/paper_72822e4ddb5d9b11/documents/supplementary_001.pdf` — [10, 11]
- `docs/evalution/update/paper_72822e4ddb5d9b11.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- New BS starts, stability/occupation evidence, BP86/B3LYP matched controls and their uncertainty remain uncomputed.

## Callable route and pilot

ORCA or Gaussian with unrestricted guesses, stability and population/natural-orbital output. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Map the source first coordination sphere, converge CS/triplet plus two BS starts with full model, then inspect wavefunction and vibrational stability.

## Minimum complete reference

1. Optimize/test CS, triplet and distinct BS starts at each method; retain stability, natural-orbital and spin-population outputs. Document any repeated convergence to the same state.
2. Evaluate the triplet on the CS geometry and independently relax the triplet, validating geometries and comparing their electronic gaps.
3. Compare method-dependent gaps and occupations; test localized-metal versus ligand-radical descriptions against the actual spin densities.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
