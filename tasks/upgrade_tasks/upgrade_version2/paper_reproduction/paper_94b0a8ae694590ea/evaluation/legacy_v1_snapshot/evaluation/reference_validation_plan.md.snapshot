# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main methods/SWCNT specification and molecular-DFT discussion; SI pp10,15,20 coordinate identities. The source does not select a chirality, so prepared ideal (10,10) geometry is explicitly benchmark-defined. ASE construction checks only; no interface energy/density computed.

- `papers/paper_94b0a8ae694590ea/documents/main.pdf` — [3, 4, 5]
- `papers/paper_94b0a8ae694590ea/documents/supplementary_001.pdf` — [10, 15, 20]
- `docs/evalution/update/paper_94b0a8ae694590ea.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- Adsorption structures, work functions, density analysis and size/convergence reference have not been calculated.
- Source tube chirality distribution is not known; benchmark conclusions remain model-conditional.

## Callable route and pilot

Configured GPAW, Quantum ESPRESSO or CP2K with explicit compatible periodic basis/pseudopotential and ASE; no NEGF dependency. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Validate clean (10,10) tube and one 2BF-TTA pose, then compare k sampling, vacuum and doubled cell at fixed coverage.

## Minimum complete reference

1. Optimize the pristine tube, isolated molecules and two adsorption starts per molecule, then calculate same-geometry fragments, density differences and vacuum-referenced work functions.
2. Compute the fixed-coverage size control for 2BF-TTA and paired k-grid/vacuum sensitivities before trusting the three-member ranking.
3. Compare molecular electron gain and work-function changes against adsorption/deformation, distinguish donation and dipole explanations, and state the model-conditional conclusion.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
