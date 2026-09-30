# Verified computation reference — paper_2f0a4f80a37fbccd (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `partial` (PARTIAL_OR_BOUNDED)
- Verification-report terminal status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 8 | `BLOCKED` | - 最终状态：**BLOCKED** |
| 101 | `QUALIFIED` | - Evaluator/task qualification: **`QUALIFIED`** |
| 110 | `PASS` | - 论文复现结论：`PASS` |
| 138 | `QUALIFIED` | - **状态与资格**：论文子目标复现 `PASS`；结果保留 `partial` 以诚实表示 IR 映射不完整。manifest、schema、五个 evaluator 文件和第三轴审计均通过，任务资格为 **`QUALIFIED`（有界科学目标）**，不等于完整固态 IR 光谱复现。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Synthesis and characterization of dichloro- η 2-nitratobis(triphenylphosphine)iridium(III)
- DOI: `10.1016/j.poly.2025.117885`
- Task package: `tasks/final_verified_paper_reproduction/paper_2f0a4f80a37fbccd`
- Verification group: `docs/verification/group_1/paper_2f0a4f80a37fbccd`
- Paper documents: `papers/paper_2f0a4f80a37fbccd`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "candidates": [
    {
      "candidate_id": "ir_nitrato_neutral_singlet",
      "frequencies": [
        7.3055,
        19.4932,
        22.2371,
        36.1819,
        40.3883,
        45.9658,
        49.7598,
        55.4418,
        "<success-only excerpt: 8 of 219 entries>"
      ],
      "nitrate_modes": [
        {
          "frequency_cm_minus_1": 669.2026,
          "ir_intensity": 2.752,
          "mode": 71,
          "nitrate_displacement_fraction": 0.99651
        },
        {
          "frequency_cm_minus_1": 615.3906,
          "ir_intensity": 3.814,
          "mode": 64,
          "nitrate_displacement_fraction": 0.98159
        },
        {
          "frequency_cm_minus_1": 907.3165,
          "ir_intensity": 45.707,
          "mode": 97,
          "nitrate_displacement_fraction": 0.88441
        },
        {
          "frequency_cm_minus_1": 1080.7353,
          "ir_intensity": 69.011,
          "mode": 128,
          "nitrate_displacement_fraction": 0.84476
        },
        {
          "frequency_cm_minus_1": 1511.1098,
          "ir_intensity": 640.525,
          "mode": 171,
          "nitrate_displacement_fraction": 0.66076
        }
      ],
      "observables": {
        "Ir1_O1": 2.1771140278703824,
        "Ir1_O2": 2.1870548821815152,
        "N1_O1": 1.3511083097916319,
        "N1_O2": 1.3548656453796442,
        "N1_O3": 1.2413469925423752,
        "O1_Ir1_O2": 61.598867947514755,
        "O1_N1_O2": 111.34135868476322,
        "O1_N1_O3": 124.48739061656357,
        "O2_N1_O3": 124.1711737450586
      },
      "optimization": {
        "converged": true,
        "imaginary_frequencies": 0,
        "stationary_point_evidence": "Gaussian normal termination; Opt+Freq completed; 219 frequencies"
      },
      "structure_identity": {
        "atom_labels": [
          "Ir1",
          "Cl1",
          "Cl2",
          "P1",
          "P2",
          "N1",
          "O1",
          "O2",
          "<success-only excerpt: 8 of 9 entries>"
        ],
        "connectivity": "Ir1 bonded to Cl1/Cl2/P1/P2 and both nitrate O1/O2; N1-O1/O2/O3",
        "formula": "C36H30Cl2IrNO3P2"
      }
    }
  ],
  "conclusion": "Geometry and the intense 1511 cm-1 nitrate-localized mode support a bidentate nitrato assignment, but the complete experimental IR pattern is not independently mapped one-to-one.",
  "limitations": "The 1532 cm-1 band has a clear nearby calculated nitrate mode; assignments for 1561/1261/1223/802 cm-1 lack an author scaling factor and displacement-vector mapping. Harmonic isolated-molecule frequencies do not reproduce condensed-phase line shapes.",
  "method": {
    "charge": 0,
    "electronic_structure": "B3LYP/LANL2DZ Opt+Freq",
    "multiplicity": 1,
    "software": "Gaussian 16",
    "starting_structure_provenance": "Tool-generated pseudo-octahedral seed; construction record retained in provenance"
  },
  "status": "partial"
}
```

Paper/SI document hashes:

- `papers/paper_2f0a4f80a37fbccd/documents/supplementary_001.pdf` — SHA-256 `539d338737eddb8491b9e78f2202fc83f3495da450c4dd6c0a55c452b3f5c01e` (declared_match=True)
- `papers/paper_2f0a4f80a37fbccd/documents/main.pdf` — SHA-256 `76fe828053d735014dabbbcf20749bb2d180992ed7921df2190fc89bacca8438` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **20**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/status.json` — successful status record; SHA-256 `5f6dee89e71ead96de0614f1250507c96586cb2fb93383fce85d562da01ceee3`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/collection.json` — successful execution artifact; SHA-256 `71deb6b6d975b13401197f1bd5b120814040eb767c672ef45bb3a9b5c067963f`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/input.com` — successful execution artifact; SHA-256 `ea231b102053c4ecff8d56aaa6e2b632b17af6ee18bf10473a5a7d0ff2a33144`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/ir_nitrato_b3lyp_lanl2dz_optfreq_summary.json` — successful execution artifact; SHA-256 `f5181312a4ce072a3ef1f183d9268e60144a7d03a7412d8cccf6b73c3c8f80b0`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/parsed_observables.json` — successful execution artifact; SHA-256 `14b115a859db6fbfe4fa8a2e8b412c6fc3159690df1b626511672a3f1f5e2180`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_10028e8d3e7f41ed9bd8b162a771d305/status.json` — successful status record; SHA-256 `5f6dee89e71ead96de0614f1250507c96586cb2fb93383fce85d562da01ceee3`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_10028e8d3e7f41ed9bd8b162a771d305/collection.json` — successful execution artifact; SHA-256 `71deb6b6d975b13401197f1bd5b120814040eb767c672ef45bb3a9b5c067963f`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_10028e8d3e7f41ed9bd8b162a771d305/input.com` — successful execution artifact; SHA-256 `ea231b102053c4ecff8d56aaa6e2b632b17af6ee18bf10473a5a7d0ff2a33144`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_10028e8d3e7f41ed9bd8b162a771d305/request.json` — successful execution artifact; SHA-256 `720f751172d199b942ecee7a4422d5db534885013e3630e8477b7ede15b999a4`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_10028e8d3e7f41ed9bd8b162a771d305/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/status.json` — successful status record; SHA-256 `190c8a2ea9b2dabfb822b62cbe16d694ce4e4ee59803572c31cdedfd43059446`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/analysis_contract.json` — successful execution artifact; SHA-256 `843aa1cea21f65e0f6d108f04cc6be9e6905601ef50aecabb2bd9ed84dba9106`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/artifact_manifest.json` — successful execution artifact; SHA-256 `5524ae133c8a8e715fe3272e5d4e8160cfbf599b278fa689d160970b9e617971`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/collection.json` — successful execution artifact; SHA-256 `967c1847d333c8bcfc0417794d702afd816e8f9d40059ef98802bc0c178c5749`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/request.json` — successful execution artifact; SHA-256 `d9311962d6a2a03e07a4d6e9bd58eb44ff9189f4c740401b3bec50aa8bc066b6`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/status.json` — successful status record; SHA-256 `4679519394bd37a7b18c60e417232ac5281ea08849f49869f2b22f9d60b3866b`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/analysis_contract.json` — successful execution artifact; SHA-256 `b1413ed94f72d68c9227385e548f1b5d4198bba041fed0752b3f086b5e860a65`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/artifact_manifest.json` — successful execution artifact; SHA-256 `24b0ff19c172862f98aa66d04e1bcfa1c9cf860a95169b4e0ec03be1433a5e26`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/collection.json` — successful execution artifact; SHA-256 `1aef0aab3aa75b20664d242bfd3425fcb8d9eb3fb68b90bde9a1791977a6317b`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/request.json` — successful execution artifact; SHA-256 `8a219423f2760826cbf5fe94247faf97ad9737c55bba4f1924c0a90a3e536210`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/status.json` — label=Independent construction of IrCl2(eta2-NO3)(PPh3)2 starting geometry; submitted_at=2026-08-29T02:11:23.343530+00:00; command=.envs/general-modern-openmpi5/bin/python code/agent_program.py
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/analysis_contract.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/artifact_manifest.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/collection.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/request.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/researchchem_job.py`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/runtime_output_registrations.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/stderr.log`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_95c8970eff3249f08b30033b0fe9abf4/stdout.log`
2. `outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/status.json` — label=Prepare author-route Gaussian input for Ir nitrato; submitted_at=2026-08-29T02:12:24.104556+00:00; command=.envs/general-modern-openmpi5/bin/python code/agent_program.py
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/analysis_contract.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/artifact_manifest.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/collection.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/request.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/researchchem_job.py`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/runtime_output_registrations.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/stderr.log`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/outputs/execution_jobs/job_1da2cc8f7a13485d8bf651c15fa332ad/stdout.log`
3. `artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/status.json` — label=Author-route B3LYP/LANL2DZ optimization and frequency of Ir nitrato complex; submitted_at=2026-08-29T02:13:43.719992+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/LANL2DZ Opt=(CalcFC,Tight,MaxCycles=250) Freq NoSymm Integral=UltraFine SCF=(XQC,Tight,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/collection.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/input.com`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/ir_nitrato_b3lyp_lanl2dz_optfreq_summary.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/parsed_observables.json`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/stderr.log`
   - output: `docs/verification/group_1/paper_2f0a4f80a37fbccd/artifacts/gaussian_batch/ir_nitrato_b3lyp_lanl2dz_optfreq/stdout.log`

## Evaluator alignment

- Key-point IDs: `pr_process_structure, pr_process_stationary, pr_result_geometry, pr_result_ir`
- Conclusion IDs: `pr_final_assignment`
- Scoring-rule IDs: `pr_r1, pr_r2, pr_r3, pr_r4, pr_c1`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `pr_r1` → reference `pr_process_structure`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r2` → reference `pr_process_stationary`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r3` → reference `pr_result_geometry`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_r4` → reference `pr_result_ir`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `pr_c1` → reference `pr_final_assignment`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.formula` = `"C36H30Cl2IrNO3P2"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.connectivity` = `"Ir1 bonded to Cl1/Cl2/P1/P2 and both nitrate O1/O2; N1-O1/O2/O3"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[0]` = `"Ir1"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[1]` = `"Cl1"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[2]` = `"Cl2"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[3]` = `"P1"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[4]` = `"P2"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[5]` = `"N1"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[6]` = `"O1"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[7]` = `"O2"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[8]` = `"O3"`
- rule `pr_r1` / reference `pr_process_structure` / field `$.method.charge` / result path `$.method.charge` = `0`
- rule `pr_r1` / reference `pr_process_structure` / field `$.method.multiplicity` / result path `$.method.multiplicity` = `1`
- rule `pr_r2` / reference `pr_process_stationary` / field `$.candidates[*].optimization` / result path `$.candidates[*].optimization.converged` = `true`
- rule `pr_r2` / reference `pr_process_stationary` / field `$.candidates[*].optimization` / result path `$.candidates[*].optimization.stationary_point_evidence` = `"Gaussian normal termination; Opt+Freq completed; 219 frequencies"`
- rule `pr_r2` / reference `pr_process_stationary` / field `$.candidates[*].optimization` / result path `$.candidates[*].optimization.imaginary_frequencies` = `0`
- rule `pr_r3` / reference `pr_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.Ir1_O1` = `2.1771140278703824`
- rule `pr_r3` / reference `pr_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.Ir1_O2` = `2.1870548821815152`
- rule `pr_r3` / reference `pr_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.N1_O1` = `1.3511083097916319`
- rule `pr_r3` / reference `pr_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.N1_O2` = `1.3548656453796442`
- rule `pr_r3` / reference `pr_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.N1_O3` = `1.2413469925423752`
- rule `pr_r3` / reference `pr_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.O1_Ir1_O2` = `61.598867947514755`
- rule `pr_r3` / reference `pr_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.O1_N1_O2` = `111.34135868476322`
- rule `pr_r3` / reference `pr_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.O1_N1_O3` = `124.48739061656357`
- rule `pr_r3` / reference `pr_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.O2_N1_O3` = `124.1711737450586`
- rule `pr_r3` / reference `pr_result_geometry` / field `$.conclusion` / result path `$.conclusion` = `"Geometry and the intense 1511 cm-1 nitrate-localized mode support a bidentate nitrato assignment, but the complete experimental IR pattern is not independently mapped one-to-one."`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[0].mode` = `71`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[0].frequency_cm_minus_1` = `669.2026`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[0].ir_intensity` = `2.752`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[0].nitrate_displacement_fraction` = `0.99651`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[1].mode` = `64`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[1].frequency_cm_minus_1` = `615.3906`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[1].ir_intensity` = `3.814`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[1].nitrate_displacement_fraction` = `0.98159`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[2].mode` = `97`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[2].frequency_cm_minus_1` = `907.3165`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[2].ir_intensity` = `45.707`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[2].nitrate_displacement_fraction` = `0.88441`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[3].mode` = `128`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[3].frequency_cm_minus_1` = `1080.7353`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[3].ir_intensity` = `69.011`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[3].nitrate_displacement_fraction` = `0.84476`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[4].mode` = `171`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[4].frequency_cm_minus_1` = `1511.1098`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[4].ir_intensity` = `640.525`
- rule `pr_r4` / reference `pr_result_ir` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[4].nitrate_displacement_fraction` = `0.66076`
- rule `pr_r4` / reference `pr_result_ir` / field `$.limitations` / result path `$.limitations` = `"The 1532 cm-1 band has a clear nearby calculated nitrate mode; assignments for 1561/1261/1223/802 cm-1 lack an author scaling factor and displacement-vector mapping. Harmonic isolated-molecule frequencies do not reproduce condensed-phase..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: experimental boundary input removed
- Files changed in that review: `agent_input/task.md, package_manifest.json, task_info.json`
- Files deleted in that review: `agent_input/data/inputs/experimental_xray_ir_boundary.json`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data` — Self-contained specification of neutral singlet IrCl2(eta2-O2NO)(PPh3)2 and atom labels.
- `data/inputs/experimental_xray_ir_boundary.json` — X-ray geometry and IR bands

Public input files and hashes:

- `agent_input/data/inputs/complex_specification.json` — SHA-256 `5493c6d5238f6cb1940115152a0ec3090e87c2da4c873ae1143c7709209c7b49`; size=1339 bytes; explicit_boundary_fields={"$.charge": 0, "$.coordination_and_connectivity": {"central_atom": "Ir1, formal Ir(III)", "ligands": ["Cl1 and Cl2 are separate monatomic chloride ligands bound to Ir1", "P1 and P2 are separate neutral triphenylphosphine ligands; each P is bonded to three phenyl ipso carbons", "N1 is the nitrogen of one nitrate group; O1 and O2 are nitrate oxygens bonded to Ir1 and N1; O3 is the terminal nitrate oxygen bonded only to N1"], "nitrate_binding": "O1-Ir1 and O2-Ir1 are both coordination bonds; N1-O1, N1-O2 and N1-O3 complete the nitrate connectivity", "phosphine_definition": "Each PPh3 ligand is P bonded to three unsubstituted phenyl rings (six carbons per ring, one ipso carbon bonded to P and five CH carbons)."}, "$.formula": "C36H30Cl2IrNO3P2", "$.multiplicity": 1}
- `agent_input/data/inputs/experimental_xray_ir_boundary.json` — SHA-256 `b5b6e9f0776f8f94094b124e2e35e97ca6c270633ba51e8d6d1b23572df9b4ad`; size=1982 bytes; explicit_boundary_fields={"$.units": {"angle": "degree", "distance": "angstrom", "frequency": "cm-1"}}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_1/paper_2f0a4f80a37fbccd/verification_report.md` — verification record; SHA-256 `d83b073bda214773428a6570cb3e5f1b333f21b129ba0a07b63ad9b1a68290e4`
- `docs/verification/group_1/paper_2f0a4f80a37fbccd/report/results.json` — verification record; SHA-256 `4e55e074496bbca3858a203bd0d4cbaef1fca26a593f3b6f0d45acc478a0c876`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
