# V3 scope and evidence reuse — 2026-10-28

Same bounded full-complex geometry and vibrational interpretation, with seven final propositions and no separate intermediate or process credit.

Reuse coordination/bond evidence from analysis_result.json and SOURCE_VS_NATIVE.json for r_coordination_geometry and r_nitrate_bonding_vibrations; mode projections/frequencies from IR_DIRECT_NATIVE_READBACK.json establish the stretching interpretation. OBSERVATION_MODE_READBACK.json and ir_21_peak_native_audit.json support r_observation_1261/1223/802, r_high_band_comparison and r_molecular_scope. Raw nitrate modes 906.6623/1079.7096/1511.2095 cm^-1 differ from printed 926/1102/1541 by -19.3377/-22.2904/-29.7905 cm^-1. The source correction remains undefined; no numeric window is added or widened. Historical acceptance was qualitative with numerical deviation, not strict source-frequency reproduction.

Final rules: r_coordination_geometry, r_nitrate_bonding_vibrations, r_observation_1261, r_observation_1223, r_observation_802, r_high_band_comparison, r_molecular_scope.

The following text is unchanged historical verification, including its old policy/status wording. It is not a declaration of a new V3 PASS. No new calculations were performed.

---

# Iridium eta2 nitrato structure and vibration: verified computation reference

## Current acceptance — 2026-10-20

**ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**. Formal scoring is permitted for the unchanged bounded task. Original numerical gates have not been declared passed. No new quantum chemistry or HPC jobs were run during this scoring migration. This is a retrospective source/native verification, not an information-limited blind Agent experiment.

Current scientific scope: Full molecular bonding geometry, nitrate coordination and vibrational interpretation of the supplied KBr observations; no formation mechanism, CO/NO electrochemistry or solid-state populations.

Current scoring is paper_science_v2: 100 points, independent binary intermediate and conclusion leaves, no process score or multiplier. AR retains method freedom; PR follows the disclosed baseline or substantiates an equivalent. The public contract is byte-frozen, including stale process/calibration wording; current private scoring supersedes those legacy evaluator statements.

## Object, source method and actual implementation

Full C36H30Cl2IrNO3P2 = IrCl2(NO3)(PPh3)2, 75 atoms, neutral singlet; retain full two triphenylphosphines and nitrate. Native harmonic spectrum is an isolated molecular model with no PCM, distinct from KBr measurement. LANL2DZ ECP leaves318 explicit electrons (159alpha/159beta), not318 total all-electron charge inventory. Nitrate eta2 has two coordinated O and one remote O.

Source main physical p7 states Gaussian09/WebMO B3LYP/LANL2DZ optimization and frequencies with a correction factor, but supplies no authenticated numeric factor. Actual retained calculations use Gaussian16 C.01, B3LYP/LANL2DZ (5D,7F),474 basis functions, with G09Defaults, NoSymm, SCF=(Tight,XQC,MaxCycle=512). The relaxed calculation uses Opt=(RCFC,NoFreeze,MaxCycles=20) followed by same-geometry Freq. Source-version substitution is documented; it is not asserted to cause the residuals.

## Actual workflow and physical validation

The verifier reused the original full-complex minimum, computed a fixed-geometry G09Defaults frequency control, then relaxed under G09Defaults and recomputed219 harmonic modes. Native optimization completed on negligible forces: max force0.000002Eh/bohr and RMS force printed0, while max displacement0.003985bohr exceeds0.001800 and RMS displacement0.000859 meets0.001200. This is preserved as a native negligible-force stop, not rewritten as four YES criteria. All219 modes are positive, minimum8.7353cm−1. All-mode mass-weighted overlap establishes mode identity across the controls without choosing modes by source frequency.

## Source versus actual geometry

| Quantity | Source DFT | Actual | Signed residual | Absolute residual | Unit |
| --- | --- | --- | --- | --- | --- |
| Ir–O1 | 2.181 | 2.1761519353744583 | -0.004848065 | 0.004848065 | Å |
| Ir–O2 | 2.182 | 2.1871116023863526 | +0.005111602 | 0.005111602 | Å |
| O–Ir–O bite | 61.635 | 61.63421982780845 | -0.000780172 | 0.000780172 | degree |
| N–O1 | 1.354 | 1.3515097966711154 | -0.002490203 | 0.002490203 | Å |
| N–O2 | 1.352 | 1.3550491430457419 | +0.003049143 | 0.003049143 | Å |
| N–O3 | 1.242 | 1.2413248451054222 | -0.000675155 | 0.000675155 | Å |

The third Ir–O is3.877924082Å, P–Ir–P99.459329° (not trans P), and Cl–Ir–Cl170.429622°. Against crystal Ir–O2.173/2.174Å, actual differences are+0.003151935/+0.013111602Å; bite61.634219828° versus60.02° differs+1.614219828°. Crystal N–O1.294/1.291/1.209Å and isolated DFT N–O values are distinct environmental references.

## Nitrate mode identity, raw frequencies and printed-source mismatch

| Native mode | Source printed cm−1 | Actual raw cm−1 | Signed difference | Absolute difference | IR km/mol | Nitrate displacement fraction | Signed N–O projections (two bound, terminal) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 97 | 926 | 906.6623 | -19.3377 | 19.3377 | 46.0938 | 0.9885653521930593 | [-0.6859709497616413, -0.721769610846944, -0.17257116983273574] |
| 128 | 1102 | 1079.7096 | -22.2904 | 22.2904 | 69.0038 | 0.9778157665798757 | [-0.9587050566031385, 0.9561796744792708, -0.014764755963871928] |
| 171 | 1541 | 1511.2095 | -29.7905 | 29.7905 | 638.0185 | 0.9400587040462708 | [0.44304522908921223, 0.4221274431899932, -1.1419184634998605] |

The three reciprocal-best squared overlaps are0.998798,0.998492,0.996280. The source printed1541/1102/926cm−1 may be corrected; these are raw-to-printed diagnostic differences, not authenticated same-definition residuals. No source correction is fitted. An independently public0.9612 control gives871.483803/1037.816868/1452.574571cm−1 and is retained only as a diagnostic, not an author factor or scoring gate. Relative percentage errors are omitted because scaling provenance is unresolved.

## Comparison with actual KBr observations

| Observed KBr cm−1 | Nearby native mode | Actual raw cm−1 | Signed difference | Absolute difference | IR intensity | Nitrate fraction | PPh3 fraction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1532 | 177 | 1519.818 | -12.1820 | 12.1820 | 61.3916 | 0.025987097805835333 | 0.9740129021941646 |
| 1532 | 176 | 1519.0129 | -12.9871 | 12.9871 | 3.5159 | 0.015570720437844469 | 0.9844292795621555 |
| 1532 | 175 | 1518.0919 | -13.9081 | 13.9081 | 30.6163 | 0.0007527905110541352 | 0.9992472094889456 |
| 1261 | 152 | 1241.1071 | -19.8929 | 19.8929 | 1.5406 | 0.0 | 1.0 |
| 1261 | 151 | 1240.2943 | -20.7057 | 20.7057 | 10.686 | 0.0 | 0.9999999999999997 |
| 1261 | 150 | 1237.8926 | -23.1074 | 23.1074 | 5.2142 | 0.0 | 0.9999999999999996 |
| 1223 | 147 | 1233.0815 | +10.0815 | 10.0815 | 2.6609 | 0.0 | 1.0000000000000002 |
| 1223 | 148 | 1235.4374 | +12.4374 | 12.4374 | 2.953 | 0.0 | 1.0 |
| 1223 | 146 | 1209.4634 | -13.5366 | 13.5366 | 0.5474 | 0.0 | 0.9999999999999998 |
| 802 | 90 | 792.1647 | -9.8353 | 9.8353 | 19.1347 | 0.0 | 0.9999999999999999 |
| 802 | 89 | 788.9548 | -13.0452 | 13.0452 | 33.1088 | 0.0 | 0.9999999999999997 |
| 802 | 88 | 787.9837 | -14.0163 | 14.0163 | 1.6152 | 0.0 | 0.9999999999999997 |

These are explicit neighborhood diagnostics, not nearest-neighbor experimental assignments. The1261/1223/802 neighborhoods are ligand dominated in the actual model. Near1532 several ligand modes coexist with the strong nitrate mode1511.2095; its difference from1532 is−20.7905cm−1 and from1561 is−49.7905cm−1. Main p3/Table2 report1561 as well as1532, while detailed main p8 lists1532/1261/1223/802; both source accounts remain visible. Source FigS12 is SI physical p29.

## Recorded resources and timing

| Run | Requested resources | Native CPU/elapsed |
| --- | --- | --- |
| Ir_relaxed_opt | %NProcShared=20; %Mem=12GB | Job cpu time:       0 days  3 hours 53 minutes 36.6 seconds.; Elapsed time:       0 days  0 hours 12 minutes  0.4 seconds. |
| Ir_relaxed_freq | %NProcShared=20; %Mem=12GB | Job cpu time:       0 days  3 hours 48 minutes  0.1 seconds.; Elapsed time:       0 days  0 hours 11 minutes 32.6 seconds. |
| Ir_fixed_G09_freq | %NProcShared=20; %Mem=12GB | Job cpu time:       0 days  3 hours 34 minutes 41.3 seconds.; Elapsed time:       0 days  0 hours 10 minutes 50.1 seconds. |

Resources are input requests, not measured peak use. Total project elapsed/queue time, cumulative memory and cost are not recorded and are not inferred. Raw input/output hashes follow. No new quantum computations were submitted in this migration.

## Remaining limits

- The source correction/scaling factor is unambiguously unavailable in disclosed text; raw-to-printed differences remain−19.3377/−22.2904/−29.7905cm−1. No correction factor or numerical tolerance is fitted.
- Crystal assignment plus actual eta2 geometry supports coordination; molecular IR alone does not prove an exhaustive unique structural assignment, and KBr environment is not explicitly modeled.
- Displacement analysis supports selective nitrate/ligand distinctions, not exact assignment of all21 observed bands.1561/1532 discrepancy and other-species FMO naming issues remain outside claimed resolution.

## Auditable raw/source artifact inventory

| Artifact | SHA-256 |
| --- | --- |
| docs/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_2f0a4f80a37fbccd/returned_a9805ec3b3ad0fc2/SOURCE_COMPARISON_RETURNED.json | ff6ef196f8077d732d50a39c49dd52dfbdecaa61d487858a12c396257cb4a6b1 |
| papers/paper_2f0a4f80a37fbccd/documents/main.pdf | 76fe828053d735014dabbbcf20749bb2d180992ed7921df2190fc89bacca8438 |
| papers/paper_2f0a4f80a37fbccd/documents/supplementary_001.pdf | 539d338737eddb8491b9e78f2202fc83f3495da450c4dd6c0a55c452b3f5c01e |
| docs/v2_verification/maintenance/closeout_push_20261017T0719Z/papers/paper_2f0a4f80a37fbccd/SOURCE_DEFINITION_RESOLUTION.json | d73336cd39975959ede8adec2c483dda0b103275ce0eb965bc09f21a291cc55c |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/analysis_result.json | 120fa663460f484402d9d791ecf6f609c0f96bc4246367f76dd4220607bfa21a |
| docs/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_2f0a4f80a37fbccd/returned_a9805ec3b3ad0fc2/OBSERVATION_MODE_READBACK.json | 0e39f8de44f85b0546c12c62f80ea653b11563fce0bf871318771af4c987d97f |
| docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/report/v2_execution_20260929/ir_21_peak_native_audit.json | 77a1f039fd292abd53d0e011a86009bc5ee7e0e4f73e1e340d9cc73e23bd96e5 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/opt/input.com | f03bcac7cd1ca0b2b1da874361290a24da1e8787530205b74bd2eea3b0f0c90a |
| docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/outputs/v2_author_Ir_source_G09Defaults_Freq_20261002_a01/checkpoint.chk | 44e3d8a8e4902da0a97dc34b2558f5f530b652353e9a8d411e837e4a3f750b5c |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/opt/gaussian.log | 955ec95a3002207940b90ce9014ba1e2458b3045567d9c7b3ad852ca2d5e1950 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/opt/format/wavefunction.fchk | 09b544a3934a83d96f7d1a962333bc783926681801e72b69a465cabef8c226c3 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/freq/input.com | f959cc40813f12a3a315e65081882520f3335a37d4a9236d07b7e601b29e9f86 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/opt/checkpoint.chk | 8ba454ad3bf248ed91311796e2d70ba56a7530aa160cf71a5bb80e0a0cf6bdc0 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/freq/gaussian.log | 07f686b7e3a90b29feec60b950d2dda8c45f048a8455a264ed05c32a8068844d |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/freq/format/wavefunction.fchk | c39bffcc3b13ad04402072250468e523fc3505424ef0b4081ffb97d5f6755373 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/parent_validation/wavefunction.fchk | e7dd72b83dd7d6e800e8b92db2af8820a1548dff544f9699365dee1a168026e3 |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/modes/analysis.json | 218161ffe820a884c3fe96372946b4b2c7673e142e114c11fd6eaeb42faeb778 |
| docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/outputs/v2_author_Ir_source_G09Defaults_Freq_20261002_a01/input.com | 67535b40fbb9157d076e733c4eee44434275767b438f1dd7e45fc3986ad73e50 |
| docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/outputs/v2_author_Ir_source_G09Defaults_Freq_20261002_a01/gaussian.log | 93712b0d0874eaa08fa5e55622f6b69363c57eb14887be4b078c8aea4112776b |
| docs/v2_verification/maintenance/closeout_push_20261017T0719Z/papers/paper_2f0a4f80a37fbccd/SOURCE_VS_NATIVE.json | faecc17200820430ff1f71abad632852814f0305d53e7c0158f48f879df908de |
| docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_2f0a4f80a37fbccd/cases/w01_Ir_G09_relaxed_20261009_a01/outputs/analysis_result.json | 120fa663460f484402d9d791ecf6f609c0f96bc4246367f76dd4220607bfa21a |
| docs/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_2f0a4f80a37fbccd/returned_a9805ec3b3ad0fc2/OBSERVATION_MODE_READBACK.json | 0e39f8de44f85b0546c12c62f80ea653b11563fce0bf871318771af4c987d97f |
| docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_2f0a4f80a37fbccd/NATIVE_ROUTE_FIELDS.json | 6bbe71e151b4af239bf55f2a6bfd26f822299c2fa699254fec499d2e80be3f2c |
| docs/v2_verification/maintenance/qualitative_acceptance_review_20261020/IR_DIRECT_NATIVE_READBACK.json | 124c8415759c1dbe7d12facb67264b10dd60df86080f9c92c699f397c4fef0f5 |

## Preserved earlier reference

No root-level verified_computation_reference.md existed in the source package. Historical evaluation snapshots are preserved byte-for-byte in the external archive indexed by evaluation/history_archive_index.json; source/native computation records remain at the artifact paths above.


## Historical reference text — non-current, preserved verbatim

Original location: legacy_v1_archive/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot. Historical PASS/pending, numeric windows, search matrices and scoring prescriptions below are not the current scientific scoring policy.

# Verified computation reference — paper_2f0a4f80a37fbccd (autonomous_research)

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
- Task package: `tasks/final_verified_autonomous_research/paper_2f0a4f80a37fbccd`
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

- Key-point IDs: `ar_process_structure, ar_process_validation, ar_result_geometry, ar_result_spectrum`
- Conclusion IDs: `ar_final_assignment`
- Scoring-rule IDs: `ar_r1, ar_r2, ar_r3, ar_r4, ar_c1`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `ar_r1` → reference `ar_process_structure`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_r2` → reference `ar_process_validation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_r3` → reference `ar_result_geometry`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_r4` → reference `ar_result_spectrum`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_c1` → reference `ar_final_assignment`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.formula` = `"C36H30Cl2IrNO3P2"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.connectivity` = `"Ir1 bonded to Cl1/Cl2/P1/P2 and both nitrate O1/O2; N1-O1/O2/O3"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[0]` = `"Ir1"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[1]` = `"Cl1"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[2]` = `"Cl2"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[3]` = `"P1"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[4]` = `"P2"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[5]` = `"N1"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[6]` = `"O1"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[7]` = `"O2"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.candidates[*].structure_identity` / result path `$.candidates[*].structure_identity.atom_labels[8]` = `"O3"`
- rule `ar_r1` / reference `ar_process_structure` / field `$.method.charge` / result path `$.method.charge` = `0`
- rule `ar_r1` / reference `ar_process_structure` / field `$.method.multiplicity` / result path `$.method.multiplicity` = `1`
- rule `ar_r2` / reference `ar_process_validation` / field `$.candidates[*].optimization` / result path `$.candidates[*].optimization.converged` = `true`
- rule `ar_r2` / reference `ar_process_validation` / field `$.candidates[*].optimization` / result path `$.candidates[*].optimization.stationary_point_evidence` = `"Gaussian normal termination; Opt+Freq completed; 219 frequencies"`
- rule `ar_r2` / reference `ar_process_validation` / field `$.candidates[*].optimization` / result path `$.candidates[*].optimization.imaginary_frequencies` = `0`
- rule `ar_r2` / reference `ar_process_validation` / field `$.limitations` / result path `$.limitations` = `"The 1532 cm-1 band has a clear nearby calculated nitrate mode; assignments for 1561/1261/1223/802 cm-1 lack an author scaling factor and displacement-vector mapping. Harmonic isolated-molecule frequencies do not reproduce condensed-phase..."`
- rule `ar_r3` / reference `ar_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.Ir1_O1` = `2.1771140278703824`
- rule `ar_r3` / reference `ar_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.Ir1_O2` = `2.1870548821815152`
- rule `ar_r3` / reference `ar_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.N1_O1` = `1.3511083097916319`
- rule `ar_r3` / reference `ar_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.N1_O2` = `1.3548656453796442`
- rule `ar_r3` / reference `ar_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.N1_O3` = `1.2413469925423752`
- rule `ar_r3` / reference `ar_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.O1_Ir1_O2` = `61.598867947514755`
- rule `ar_r3` / reference `ar_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.O1_N1_O2` = `111.34135868476322`
- rule `ar_r3` / reference `ar_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.O1_N1_O3` = `124.48739061656357`
- rule `ar_r3` / reference `ar_result_geometry` / field `$.candidates[*].observables` / result path `$.candidates[*].observables.O2_N1_O3` = `124.1711737450586`
- rule `ar_r3` / reference `ar_result_geometry` / field `$.conclusion` / result path `$.conclusion` = `"Geometry and the intense 1511 cm-1 nitrate-localized mode support a bidentate nitrato assignment, but the complete experimental IR pattern is not independently mapped one-to-one."`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[0].mode` = `71`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[0].frequency_cm_minus_1` = `669.2026`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[0].ir_intensity` = `2.752`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[0].nitrate_displacement_fraction` = `0.99651`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[1].mode` = `64`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[1].frequency_cm_minus_1` = `615.3906`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[1].ir_intensity` = `3.814`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[1].nitrate_displacement_fraction` = `0.98159`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[2].mode` = `97`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[2].frequency_cm_minus_1` = `907.3165`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[2].ir_intensity` = `45.707`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[2].nitrate_displacement_fraction` = `0.88441`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[3].mode` = `128`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[3].frequency_cm_minus_1` = `1080.7353`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[3].ir_intensity` = `69.011`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[3].nitrate_displacement_fraction` = `0.84476`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[4].mode` = `171`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[4].frequency_cm_minus_1` = `1511.1098`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[4].ir_intensity` = `640.525`
- rule `ar_r4` / reference `ar_result_spectrum` / field `$.candidates[*].nitrate_modes` / result path `$.candidates[*].nitrate_modes[4].nitrate_displacement_fraction` = `0.66076`

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

- `agent_input/data/inputs/complex_specification.json` — SHA-256 `e34ce5d708e0576cf80d9cd65f42fd0ba9c9ca5b0d2702ea4622dbbfca5f326c`; size=1241 bytes; explicit_boundary_fields={"$.charge": 0, "$.coordination_and_connectivity": {"central_atom": "Ir1, formal Ir(III)", "ligands": ["Cl1 and Cl2 are separate monatomic chloride ligands bound to Ir1", "P1 and P2 are separate neutral triphenylphosphine ligands; each P is bonded to three phenyl ipso carbons", "N1 is the nitrogen of one nitrate group; O1 and O2 are nitrate oxygens bonded to Ir1 and N1; O3 is the terminal nitrate oxygen bonded only to N1"], "nitrate_binding": "O1-Ir1 and O2-Ir1 are both coordination bonds; N1-O1, N1-O2 and N1-O3 complete the nitrate connectivity", "phosphine_definition": "Each PPh3 ligand is P bonded to three unsubstituted phenyl rings (six carbons per ring, one ipso carbon bonded to P and five CH carbons)."}, "$.formula": "C36H30Cl2IrNO3P2", "$.multiplicity": 1}
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


## Historical reference text — non-current, preserved verbatim

Original location: legacy_v1_archive/verified_computation_reference.md. Historical PASS/pending, numeric windows, search matrices and scoring prescriptions below are not the current scientific scoring policy.

# 第一版扩展科学参考：已完成限定范围实算验证

更新：2026-09-28T13:31:58.771771+00:00。论文 `paper_2f0a4f80a37fbccd`；模式 `AR`。

这是作者知情的参考验证，科学矩阵已通过组内验收。语义评分器校准和盲测AR未执行，主协调最终验收仍待完成。

机器可读入口：`phase1_reference_binding.json`；包含原始证据索引、SHA256、实际测试包版本和限制。

当前正式结果：`docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/report/results.json`。

逐项evaluator对应：`docs/upgrade_tasks_verification/group_1/papers/paper_2f0a4f80a37fbccd/evaluator_mapping.json`。

修改前完整包已保存：`docs/upgrade_tasks_v2_review_20260928/group_1/phase1/history/reference_binding/paper_2f0a4f80a37fbccd/AR/135040a1d7e1f9e1530853158b2d5e7d79fe04a613182900b644acdcce90f0bf`。历史final快照保持不变。

## 已完成端点

- five_full_identity_minima
- eta1_eta2_competition
- relative_ligand_geometry_alternatives
- native_modes_and_nitrate_PPh3_mixing
- four_and_five_band_comparisons
- uniform_scale_sensitivity
- bounded_candidate_set

## 适用范围与限制

- 作者知情的参考验证，非盲AR。有限五起点而非全局构象穷尽；气相B3LYP/LANL2DZ含ECP，无显式自旋轨道/晶体堆积/固态环境。统一0.96/0.98/1.00比例只测试敏感性，不能消除方法与固态误差；没有预设任意光谱通过容差，没有以缺峰降低RMSE后宣布胜者。电子能与谐振G分别保留，但不推断固态群体或氧/NO生成路径。

## 本次真实计算报告

# Ir 硝酸根配位：科学验证报告

更新：2026-09-28T13:27:18.129773+00:00。当前冻结第一版；作者知情参考验证。

## 结论

在完整分子B3LYP/LANL2DZ有限构型搜索中，最低eta2比最低eta1低65.264 kJ/mol，支持eta2的气相电子稳定性；但稳定eta1极小值确实存在，且统一光谱匹配有未匹配观测、显著残差及配体混合，不能仅靠这些KBr峰唯一确定配位模型或相对配体排列。

## 构型和驻点

|初始候选|最终配位|相对电子能(kJ/mol)|Ir–O三距离(Å)|Cl–Ir–Cl/P–Ir–P(°)|

|---|---|---:|---|---|

|ir_nitrato_b3lyp_lanl2dz_optfreq|eta2|12.9309|2.1771/2.1871/3.8787|170.27/99.41|

|eta1_O7_release|eta1|72.0380|2.0502/4.0900/3.4137|166.90/101.80|

|eta1_O8_release_recovery2|eta1|65.2637|4.1567/2.0551/3.3458|164.41/103.74|

|eta2_cisCl_transP_release|eta2|0.0000|2.1940/2.1431/3.8786|93.68/176.62|

|eta2_cisCl_cisP_release|eta2|36.6216|2.2528/2.1350/3.8947|89.46/105.31|

全部75原子、两完整PPh3、两Cl及完整NO3保留；各219内部模式均为正。原生ECP显式电子318（159α/159β），与全核418之间100个芯电子差有明确记录。所有相对能量采用同一个最低电子能零点；没有把气相电子偏好换算成固态比例。

## 同一规则下的光谱比较

原始频率窗口700–1650 cm⁻¹；硝酸根质量加权位移分数≥0.15才进入一对一匹配。先保留unity，再以0.96和0.98统一缩放重算。并列报告1532/1261/1223/802四峰与额外1561五峰，不选有利来源。

|候选|观测数|匹配数|原频率RMSE(cm⁻¹)|未匹配观测|

|---|---:|---:|---:|---|

|ir_nitrato_b3lyp_lanl2dz_optfreq|4|3|102.903|1261|

|ir_nitrato_b3lyp_lanl2dz_optfreq|5|3|102.903|1561,1261|

|eta1_O7_release|4|4|112.324||

|eta1_O7_release|5|5|177.838||

|eta1_O8_release_recovery2|4|4|187.689||

|eta1_O8_release_recovery2|5|4|187.689|1561|

|eta2_cisCl_transP_release|4|4|196.222||

|eta2_cisCl_transP_release|5|4|196.222|1561|

|eta2_cisCl_cisP_release|4|3|97.595|1261|

|eta2_cisCl_cisP_release|5|3|97.595|1561,1261|

残差只覆盖成功匹配的观测。较少模式不能因RMSE较小就获得优先；全部未匹配项保留为证据缺口。全1095个正常模及N–O有符号投影见ir_all_modes.csv和mode_analysis，未入选模式同样保留。

## 真实对照与解释

相同组成的Cl/P位点重新排列并完整释放，实际改变了最低电子构型及振动混合；两个独立eta1起点均有真实极小值，因此不能宣称eta1不存在。晶体结构证据与本次自含分子/IR问题的证据权限区分；本文不借晶体答案替代当前反例搜索。

所有比例敏感性数值及构型能量变化见results.sensitivity。没有为任一峰单独拟合比例，也没有预设任意RMSE阈值强行通过。

## 来源、资源与限制

作者知情的参考验证，非盲AR。有限五起点而非全局构象穷尽；气相B3LYP/LANL2DZ含ECP，无显式自旋轨道/晶体堆积/固态环境。统一0.96/0.98/1.00比例只测试敏感性，不能消除方法与固态误差；没有预设任意光谱通过容差，没有以缺峰降低RMSE后宣布胜者。电子能与谐振G分别保留，但不推断固态群体或氧/NO生成路径。

复用1个源eta2原生日志并重新审查；新增引擎实际启动6次，已测总作业时6.596h，已测分配核时131.930。未知中断耗时不填零；AR/PR共享物理结果。两套schema、引用文件、记录ID和当前冻结包哈希均通过；evaluator_mapping逐条对应科学证据。

入口：report/results.json、validation/ir_quality.json、validation/contract_checks.json、resource_summary.json、ir_all_modes.csv；完整原始失败/恢复记录保留在outputs和provenance。

