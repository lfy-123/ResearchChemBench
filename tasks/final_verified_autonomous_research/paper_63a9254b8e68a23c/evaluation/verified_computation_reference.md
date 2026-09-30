# Verified computation reference — paper_63a9254b8e68a23c (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 10 | `QUALIFIED` | - 评估任务资格：`QUALIFIED`（结果、单位、分支、停驻性和局限性均可审查）。 |
| 11 | `PASS` | - 最终状态：`PASS`。 |
| 80 | `PASS` | 最终判定：`PASS`，仅限公开连续体模型边界，不扩张为原子级 MD 复现。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Controlling Spontaneously-Formed Nanoscrolls by In-Plane Janus TMD/Traditional TMD Heterostructures
- DOI: `10.1021/acsami.5c22081`
- Task package: `tasks/final_verified_autonomous_research/paper_63a9254b8e68a23c`
- Verification group: `docs/verification/group_6/paper_63a9254b8e68a23c`
- Paper documents: `papers/paper_63a9254b8e68a23c`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "author_hypothesis_assessment": "Supported within the supplied continuum model: a stable positive radius exists, nonzero MoSSe spontaneous curvature contributes to the driving term, and competition among bending stiffness, spontaneous curvature and interlayer attraction selects the minimum. The selected 2.524 nm radius is within the evaluator's method-aware 0.2 nm comparison tolerance of the published validation case, while the computed result is a continuum prediction rather than an atomistic trajectory reproduction.",
  "current_recovery": {
    "hpc_jobs": [],
    "hpc_status_counts": {},
    "local_native_jobs": [],
    "route_gate": "Author-route calculation and evaluator comparison are complete and strictly verified.",
    "scientific_conclusion": "Not upgraded: queueing/wrapper success is not application-level convergence; custom/private author inputs remain bounded.",
    "updated_at": "2026-09-13T08:56:43.584158+00:00"
  },
  "evidence": {
    "energy_components_per_width_eV_per_A": {
      "bending": 2.3544938986499733,
      "interface_vdw": -9.318101428419792,
      "self_vdw": -37.41632163188862
    },
    "energy_scan": "artifacts/continuum_energy_scan.csv",
    "equation_source_page": "artifacts/source_pages/main_page_3.png",
    "evaluator_read_after_independent_calculation": true,
    "incomplete_branch_best_energy_per_width_eV_per_A": -28.145902638955143,
    "incomplete_branch_boundary_inner_radius_A": 149.53085917338836,
    "primary_artifact": "artifacts/continuum_minimization.json",
    "selected_energy_per_width_eV_per_A": -44.379929161658445
  },
  "limitations": "The public task does not provide an atomistic LAMMPS data file or a unique stacking trajectory; no MD claim is made. The incomplete-outer-turn branch uses the source-consistent truncated overlap integral, while the source's closed-form Eq. 6 assumes complete turns. The result is per unit width and depends on the supplied material constants, ideal Archimedean geometry, area conservation and vdW contact approximation. The complete/incomplete boundary is at Rin=149.531 A; the selected state has 4.148 and 2.671 turns for the two segments, so both satisfy the complete-turn condition.",
  "method_summary": "Using the public two-segment MoSSe/MoS2 continuum inputs, I implemented the paper's area-conserved joined-Archimedean-spiral geometry and E_total/W=E_bending/W+E_self-vdW/W+E_interface-vdW/W. The MoSSe and MoS2 lengths are 100 nm each; W was set to 1 A because it factors from the stationarity equation. The physically admissible inner-radius domain was searched from 0.01 A to 10000 A. A 2001-point scan (0.5-250 A), bounded scalar minimization, and an independent Brent root of the analytic complete-branch derivative were used. For the outer segment, the overlap integral was evaluated for theta_2<2pi and the one-full-turn expression for theta_2>=2pi; the complete-turn minimum was selected only after checking its angle and comparing the incomplete branch boundary/best value.",
  "outer_angle_rad": 16.780235314638592,
  "outer_radii_A": [
    51.493816061272945,
    67.69402382886607
  ],
  "radius_nm": 2.5239449734393964,
  "regime": "complete_outer_segment_turn",
  "status": "complete",
  "validation": {
    "converged": true,
    "independent_check_agreement_nm": 6.276463047072411e-08,
    "local_minimum_evidence": "The bounded scalar minimizer and an independent analytic derivative root agree within 6.3e-8 nm; centered finite-difference d(E/W)/dR=6.09e-9 eV/A^2; finite-difference second derivative=9.93e-3 eV/A^3>0; E(R-0.1 A) and E(R+0.1 A) are both higher than E(R).",
    "stationarity_residual": 2.189173244309851e-17
  }
}
```

## Re-audit source-evidence drift

- Classification: **RUNTIME_METADATA_ONLY**
- Previous `results.json` SHA-256: `974c102e07c2e5bac13c166cb467d3e38fb0ebfba9097a29ca63e525bc24a306`
- Current `results.json` SHA-256: `6fcdade3ac0f54f64cf2733c875f40ab989f02049a357a9081e303f36b5622a6`
- Changed top-level result fields: `current_recovery`
- Changed execution-artifact paths: `none detected`

A source hash change is not treated as a new scientific result. Runtime-only changes remain metadata drift; any other change requires semantic comparison of the provenance record. This archive is not a scoring standard.

<!-- source-drift-json: {"changed_artifact_paths": [], "changed_top_level_keys": ["current_recovery"], "classification": "RUNTIME_METADATA_ONLY", "current_sha256": "6fcdade3ac0f54f64cf2733c875f40ab989f02049a357a9081e303f36b5622a6", "detected": true, "previous_sha256": "974c102e07c2e5bac13c166cb467d3e38fb0ebfba9097a29ca63e525bc24a306"} -->

Paper/SI document hashes:

- `papers/paper_63a9254b8e68a23c/documents/supplementary_001.pdf` — SHA-256 `d0403ec700692ec13adc892fe9f20d30eb63dcc04385eb9d7f572b8507ad71ff` (declared_match=True)
- `papers/paper_63a9254b8e68a23c/documents/main.pdf` — SHA-256 `c02fdc9490e2c29f21190d6523ba50e791c4cb85b3ddf02dd2eb2619d2fdedb9` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **2**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_minimization.json` — analytic minimization result; SHA-256 `2a84e72232e55d2e073a6c56d6ddcdb421fba86874cc613216c3680afbea0831`
- `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_energy_scan.csv` — bounded branch scan; SHA-256 `ba14ba61f2813c1ec062d546348f6162d0165e7af75ffc22dc98885294c35f1c`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/continuum_minimization.json` — label=Read the public two-segment continuum parameters and area-conserved joined Archimedean geometry.; intent=analytic_continuum_step; route=recorded mathematical workflow; no scheduler job
   - output: `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_minimization.json`
   - output: `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_energy_scan.csv`
2. `artifacts/continuum_minimization.json` — label=Evaluate total energy per width over the bounded 2001-point inner-radius scan and retain complete/incomplete branches.; intent=analytic_continuum_step; route=recorded mathematical workflow; no scheduler job
   - output: `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_minimization.json`
   - output: `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_energy_scan.csv`
3. `artifacts/continuum_minimization.json` — label=Minimize the admissible complete-turn branch with the bounded scalar minimizer.; intent=analytic_continuum_step; route=recorded mathematical workflow; no scheduler job
   - output: `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_minimization.json`
   - output: `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_energy_scan.csv`
4. `artifacts/continuum_minimization.json` — label=Independently solve the analytic complete-branch derivative with a Brent root and compare the radii.; intent=analytic_continuum_step; route=recorded mathematical workflow; no scheduler job
   - output: `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_minimization.json`
   - output: `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_energy_scan.csv`
5. `artifacts/continuum_minimization.json` — label=Check stationarity, positive second derivative, neighboring radii and incomplete-branch boundary before selecting the regime.; intent=analytic_continuum_step; route=recorded mathematical workflow; no scheduler job
   - output: `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_minimization.json`
   - output: `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_energy_scan.csv`

## Evaluator alignment

- Key-point IDs: `ar_process_candidates, ar_process_coverage, ar_result_radius, ar_result_physics`
- Conclusion IDs: `ar_final`
- Scoring-rule IDs: `ar_r1, ar_r2, ar_r3, ar_r4, ar_c1`
- Bound result-field status: **BRANCH_INAPPLICABLE_FIELDS_ONLY**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `$.candidate_models, $.conclusion, $.search_coverage`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `ar_r1` → reference `ar_process_candidates`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_r2` → reference `ar_process_coverage`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_r3` → reference `ar_result_radius`; type=numeric; unit=nm; tolerance=0.2; comparison=absolute difference; evaluator_target_present=True
- rule `ar_r4` → reference `ar_result_physics`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_c1` → reference `ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `ar_r3` / reference `ar_result_radius`: target=2.69 nm; tolerance=0.2; numeric result leaves=[2.5239449734393964]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `ar_r2` / reference `ar_process_coverage` / field `$.validation` / result path `$.validation.converged` = `true`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.validation` / result path `$.validation.stationarity_residual` = `2.189173244309851e-17`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.validation` / result path `$.validation.independent_check_agreement_nm` = `6.276463047072411e-08`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.validation` / result path `$.validation.local_minimum_evidence` = `"The bounded scalar minimizer and an independent analytic derivative root agree within 6.3e-8 nm; centered finite-difference d(E/W)/dR=6.09e-9 eV/A^2; finite-difference second derivative=9.93e-3 eV/A^3>0; E(R-0.1 A) and E(R+0.1 A) are bot..."`
- rule `ar_r3` / reference `ar_result_radius` / field `$.radius_nm` / result path `$.radius_nm` = `2.5239449734393964`
- rule `ar_r4` / reference `ar_result_physics` / field `$.limitations` / result path `$.limitations` = `"The public task does not provide an atomistic LAMMPS data file or a unique stacking trajectory; no MD claim is made. The incomplete-outer-turn branch uses the source-consistent truncated overlap integral, while the source's closed-form E..."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Closed JSON specification of the ordered two-segment ribbon and continuum material parameters.

Public input files and hashes:

- `agent_input/data/inputs/system.json` — SHA-256 `a5923ffbf580fb862d55c3ff7850250e7c0fdc30571a67d2667baf3fc5e5601f`; size=787 bytes; explicit_boundary_fields={"$.units": {"curvature": "A^-1", "energy": "eV", "length": "A unless field ends in _nm"}}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_6/paper_63a9254b8e68a23c/verification_report.md` — verification record; SHA-256 `99234af6df2ad37f273cdccf341cb6e01da39d4e68bd25a38eaadf788cb615a2`
- `docs/verification/group_6/paper_63a9254b8e68a23c/report/results.json` — verification record; SHA-256 `6fcdade3ac0f54f64cf2733c875f40ab989f02049a357a9081e303f36b5622a6`
- `docs/verification/group_6/paper_63a9254b8e68a23c/artifacts/continuum_minimization.json` — referenced successful evidence; SHA-256 `2a84e72232e55d2e073a6c56d6ddcdb421fba86874cc613216c3680afbea0831`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
