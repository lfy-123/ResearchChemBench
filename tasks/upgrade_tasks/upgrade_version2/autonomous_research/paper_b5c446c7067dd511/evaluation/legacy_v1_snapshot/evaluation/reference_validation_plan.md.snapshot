# Expanded reference validation plan

Status: **implemented_pending_expanded_reference**. New scientific engine calculations in this upgrade: **0**.

## Sources actually reviewed

Read main pp3–5/Figure3 and SI pp2–6 low/high-state table, NTO and IFCT definitions. Source gives energies and characters, not a calibrated full SOC/kinetic reference; a tabulated Py CT/LE percentage pair is internally inconsistent, so re-normalize from actual densities rather than copy it. The original AR file had names only while PR also had source-derived SMILES; both upgraded modes now share formula-checked full graphs and explicit terminal/bridge mappings, without the author high-state labels.

- `papers/paper_b5c446c7067dd511/documents/main.pdf` — [3, 4, 5]
- `papers/paper_b5c446c7067dd511/documents/supplementary_001.pdf` — [2, 3, 4, 5, 6]
- `docs/evalution/update/paper_b5c446c7067dd511.md` — First-version specification, not scientific evidence

## Historical reference boundary

The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.

## Missing inputs / reference gaps

- Expanded high-state SOC, geometry intervention and state-window/method uncertainty remain uncomputed.

## Callable route and pilot

ORCA TDDFT/SOC with Gaussian baseline comparison; Multiwfn/transition-density analysis. Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.

Demonstrate reproducible Ph-mP/An-mP state matching and high-state SOC with expanded roots before extending to Na/Py.

## Minimum complete reference

1. Calibrate Ph-mP and An-mP first, then calculate the four-member window with states, oscillator strengths, transition densities and actual SOC pairs.
2. For the two representatives enlarge the root set and repeat the fixed 45-degree terminal torsion, recording state overlap and changed gaps/couplings.
3. Compare each representative candidate against neighboring triplets and a CT-sensitive method contrast; state what necessary conditions are supported and which kinetics remain unknown.

Keep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.

## Resource and release gate

Record actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.
