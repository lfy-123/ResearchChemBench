# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main pp3 and 8–10/Figure7, SI p2 computational methods and pp20–26 including TableS3 and S16/S17 figures. Checked final public coordinates: 96 atoms, C87H7Y2, Y rows81/82, neutral odd-electron state.

- `papers/paper_3d1d9b7f6df049da/documents/main.pdf` — [3, 8, 9, 10]
- `papers/paper_3d1d9b7f6df049da/documents/supplementary_001.pdf` — [2, 20, 21, 22, 23, 24, 25, 26]
- `docs/evalution/update/paper_3d1d9b7f6df049da.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- No new mode projection matrix, negative-control derivatives or frame/step uncertainty reference has been run.

## Callable route and pilot

ORCA for open-shell DFT/Hessian and ZORA EPR tensors, Python/NumPy for mapped displacements and covariance. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Validate one cage doublet, one lateral eigenvector, a stable g/A tensor and h versus h/2 before extending mode classes.

## Minimum complete reference

1. Optimize and validate both doublets, calculate modes and document projection-based assignment, including the four leading lateral candidates. Select three mode classes per cage by the declared rule.
2. Calculate a consistent g or A tensor for each central and four displaced geometries, retaining full components, normal coordinate units and spin-density validation.
3. Perform the rigid-rotation check; compare bare derivative norms and thermal weights at both temperatures, and determine which mechanism explains differences between mode classes and cages.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
