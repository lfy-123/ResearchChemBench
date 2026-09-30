# Verified computation reference — paper_0de37d01e35c27df (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Public-input maintenance note (2026-09-14)

The SI Table S3 neutral endpoint is retained only under `evaluation/author_results/`. The public 26-atom XYZ is an RDKit ETKDGv3 topology-only starter (seed 1337), with formula, atom order, and sulfur indices preserved. No new quantum calculation was run; the historical author-route result supports the evaluator target but does not certify reachability from this changed public starter.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `success` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **AUTHOR_ROUTE_ONLY_PUBLIC_STARTER_NOT_REPLAYED**
- Applicability note: Public norDTCO endpoint coordinates from SI Table S3 were replaced by an independent topology-only starter; the historical group verification used the author endpoint. Under the accepted author-route verification policy this starter difference is not itself a task/evaluator mismatch; no independent discovery or public-starter replay is claimed.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 8 | `PASS` | - 论文复现结论：**PASS（核心结构端点）**。两态 BP86/TZVP 优化+频率均真实完成、正常终止、无虚频，S–S 收缩与论文定性结论一致。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Structural Studies Provide Insight on the Fate of 1,5-Dithiacanes: Two Electron Reversible Oxidation versus Irreversible Oxidation
- DOI: `10.1021/acs.joc.5c01731`
- Task package: `tasks/final_verified_autonomous_research/paper_0de37d01e35c27df`
- Verification group: `docs/verification/group_2/paper_0de37d01e35c27df`
- Paper documents: `papers/paper_0de37d01e35c27df`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "conclusion": "Oxidation contracts the S16-S17 separation by 0.072901 Å. The direction and magnitude provide structural support for the paper's qualitative transannular 2c-3e interaction hypothesis within the stated gas-phase two-state boundary.",
  "coverage": "Two required states (neutral singlet and radical-cation doublet); one optimized candidate per state; gas-phase BP86/TZVP Opt Freq.",
  "distance_change": {
    "definition": "radical-cation S16-S17 distance minus neutral S16-S17 distance",
    "value_angstrom": -0.072900758
  },
  "limitations": [
    "No dication, solvent, redox free-energy, or exhaustive alternative-conformer search was required or performed.",
    "Absolute distances are method-dependent and the contraction alone is supporting, not definitive bonding proof."
  ],
  "states": [
    {
      "charge": 0,
      "multiplicity": 1,
      "provenance": {
        "atom_indices": [
          16,
          17
        ],
        "file": "artifacts/norDTCO_neutral_optimized.xyz"
      },
      "state": "neutral singlet norDTCO",
      "sulfur_distance_angstrom": 4.056140073,
      "validation": {
        "converged": true,
        "imaginary_frequency_count": 0,
        "spin_diagnostic": "Closed-shell singlet (S2 diagnostic not applicable).",
        "stationary_point_evidence": "Gaussian optimization completed; stationary point found; normal termination; frequency job completed."
      }
    },
    {
      "charge": 1,
      "multiplicity": 2,
      "provenance": {
        "atom_indices": [
          16,
          17
        ],
        "file": "artifacts/norDTCO_radical_cation_optimized.xyz"
      },
      "state": "norDTCO radical cation doublet",
      "sulfur_distance_angstrom": 3.983239316,
      "validation": {
        "converged": true,
        "imaginary_frequency_count": 0,
        "spin_diagnostic": "UBP86 doublet; final Gaussian archive reports <S2> about 0.7515 (spin contamination small).",
        "stationary_point_evidence": "Gaussian optimization completed; stationary point found; normal termination; 72 vibrational frequencies parsed."
      }
    }
  ],
  "status": "success",
  "validation": [
    "Both states used the supplied 26-atom XYZ atom order and explicit charge/multiplicity.",
    "Both native Gaussian jobs have normal termination and completed optimization/frequency evidence.",
    "No imaginary frequencies were detected in either state.",
    "Distance extraction independently parsed the final Gaussian orientation and measured atoms 16 and 17."
  ]
}
```

Paper/SI document hashes:

- `papers/paper_0de37d01e35c27df/documents/main.pdf` — SHA-256 `0e7674491acb0b2565ea4dbec1dc37cad1a408c963344f839db245d3b7f85177` (declared_match=True)
- `papers/paper_0de37d01e35c27df/documents/supplementary_001.pdf` — SHA-256 `5db011e6236dc4acc437de3264214f79e39ea967de00ab8459a83934f55623a1` (declared_match=True)

Report evidence lines retained:

- `#p BP86/TZVP Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512)`（自由基为 `UBP86`），16 个共享 CPU、48000 MB 请求；首篇作业在长时策略切换前提交，保留其实际监督记录。原始 input、stdout、stderr、checkpoint、status、collection 和 SHA-256 均在 `artifacts/gaussian_batch/`。
- `Δd = d_radical − d_neutral = −0.072900758 Å`（约 −0.072901 Å，收缩 0.0729 Å）。优化均报告 `Optimization completed`、`Stationary point found` 和 `Normal termination of Gaussian 16`；自由基输出 `<S^2>` 接近双重态理论值（摘要和 archive 中可追溯），未见导致结论失效的自旋异常。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **20**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/status.json` — successful status record; SHA-256 `db77e8a8311cf34efa5f6bcb9d54bea3608c875a76431b27017e2a03703eca16`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/collection.json` — successful execution artifact; SHA-256 `37bdf2cb974c159f4e0c875a1f2edc8046957fe3aa78f6df2a21d821edc75ba0`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/input.com` — successful execution artifact; SHA-256 `7e290f2cacd0387eadf46730e9010c8e5bdce5a87f166f0db8ac3be095f3edee`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/stdout.log` — successful execution artifact; SHA-256 `1d7e740146cb4474ae66a826c734ba1771a865e1cd0a9aa4a04dbc87e519a073`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/status.json` — successful status record; SHA-256 `44156a28ad86ed9e88517ab9aef83025e75551c88ffd2e1b8e4cc2c406dac430`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/collection.json` — successful execution artifact; SHA-256 `0c4cb2447d31b46050d61b3814d4a7b00b1b5ba249a961d5cbf62a35c141c5b4`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/input.com` — successful execution artifact; SHA-256 `276c75560b840f02d039da1c84c9743afdad6c987eb9b68586f39584259b7750`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/stdout.log` — successful execution artifact; SHA-256 `ce1e282e4368fbcac1f12bbf19686f2851cdd3129b1796a61baa7679e5aaa42f`
- `docs/verification/group_2/paper_0de37d01e35c27df/native_workspace_batch/outputs/execution_jobs/job_a12946a15d5d451bac04c2b4a1477311/status.json` — successful status record; SHA-256 `db77e8a8311cf34efa5f6bcb9d54bea3608c875a76431b27017e2a03703eca16`
- `docs/verification/group_2/paper_0de37d01e35c27df/native_workspace_batch/outputs/execution_jobs/job_a12946a15d5d451bac04c2b4a1477311/collection.json` — successful execution artifact; SHA-256 `37bdf2cb974c159f4e0c875a1f2edc8046957fe3aa78f6df2a21d821edc75ba0`
- `docs/verification/group_2/paper_0de37d01e35c27df/native_workspace_batch/outputs/execution_jobs/job_a12946a15d5d451bac04c2b4a1477311/input.com` — successful execution artifact; SHA-256 `7e290f2cacd0387eadf46730e9010c8e5bdce5a87f166f0db8ac3be095f3edee`
- `docs/verification/group_2/paper_0de37d01e35c27df/native_workspace_batch/outputs/execution_jobs/job_a12946a15d5d451bac04c2b4a1477311/request.json` — successful execution artifact; SHA-256 `f1ce375288be23952e8cb2c76e7a51dc6045f1b7b80a08159051b64c6140f6a7`
- `docs/verification/group_2/paper_0de37d01e35c27df/native_workspace_batch/outputs/execution_jobs/job_a12946a15d5d451bac04c2b4a1477311/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_0de37d01e35c27df/native_workspace_batch/outputs/execution_jobs/job_b77a70756f0d47dbbe67ae58d7040704/status.json` — successful status record; SHA-256 `44156a28ad86ed9e88517ab9aef83025e75551c88ffd2e1b8e4cc2c406dac430`
- `docs/verification/group_2/paper_0de37d01e35c27df/native_workspace_batch/outputs/execution_jobs/job_b77a70756f0d47dbbe67ae58d7040704/collection.json` — successful execution artifact; SHA-256 `0c4cb2447d31b46050d61b3814d4a7b00b1b5ba249a961d5cbf62a35c141c5b4`
- `docs/verification/group_2/paper_0de37d01e35c27df/native_workspace_batch/outputs/execution_jobs/job_b77a70756f0d47dbbe67ae58d7040704/input.com` — successful execution artifact; SHA-256 `276c75560b840f02d039da1c84c9743afdad6c987eb9b68586f39584259b7750`
- `docs/verification/group_2/paper_0de37d01e35c27df/native_workspace_batch/outputs/execution_jobs/job_b77a70756f0d47dbbe67ae58d7040704/request.json` — successful execution artifact; SHA-256 `85c539f42ffd486e8e274441558f6f46edf794113e51783d37568a2ab15dbae5`
- `docs/verification/group_2/paper_0de37d01e35c27df/native_workspace_batch/outputs/execution_jobs/job_b77a70756f0d47dbbe67ae58d7040704/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/status.json` — label=group_1 docs/verification/group_2/paper_0de37d01e35c27df norDTCO_neutral_bp86_tzvp_optfreq; submitted_at=2026-08-29T06:07:06.110078+00:00; software=gaussian; intent=optimization_frequency; route=#p BP86/TZVP Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/norDTCO_neutral_bp86_tzvp_optfreq.chk`
   - output: `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_neutral_bp86_tzvp_optfreq/stdout.log`
2. `artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/status.json` — label=group_2 paper_0de37d01e35c27df norDTCO_radical_cation_bp86_tzvp_optfreq; submitted_at=2026-08-29T06:20:13.982468+00:00; software=gaussian; intent=optimization_frequency; route=#p UBP86/TZVP Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/norDTCO_radical_cation_bp86_tzvp_optfreq.chk`
   - output: `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/gaussian_batch/norDTCO_radical_cation_bp86_tzvp_optfreq/stdout.log`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `con_ar_limit`, `r_ar_con_limit`.

- Key-point IDs: `kp_ar_process_identity, kp_ar_process_validation, kp_ar_result_change`
- Conclusion IDs: `con_ar_final, con_ar_limit`
- Scoring-rule IDs: `r_ar_kp_identity, r_ar_kp_validation, r_ar_kp_change, r_ar_con_final, r_ar_con_limit`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_ar_kp_identity` → reference `kp_ar_process_identity`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_kp_validation` → reference `kp_ar_process_validation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_kp_change` → reference `kp_ar_result_change`; type=numeric; unit=angstrom; tolerance=0.2; comparison=absolute difference; evaluator_target_present=True
- rule `r_ar_con_final` → reference `con_ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_con_limit` → reference `con_ar_limit`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_ar_kp_change` / reference `kp_ar_result_change`: target=0.073 angstrom; tolerance=0.2; numeric result leaves=[4.056140073, 3.983239316, -0.072900758]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].state` = `"neutral singlet norDTCO"`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].charge` = `0`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].multiplicity` = `1`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].sulfur_distance_angstrom` = `4.056140073`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].provenance.file` = `"artifacts/norDTCO_neutral_optimized.xyz"`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].provenance.atom_indices[0]` = `16`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].provenance.atom_indices[1]` = `17`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].validation.converged` = `true`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].validation.stationary_point_evidence` = `"Gaussian optimization completed; stationary point found; normal termination; frequency job completed."`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].validation.imaginary_frequency_count` = `0`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[0].validation.spin_diagnostic` = `"Closed-shell singlet (S2 diagnostic not applicable)."`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].state` = `"norDTCO radical cation doublet"`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].charge` = `1`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].multiplicity` = `2`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].sulfur_distance_angstrom` = `3.983239316`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].provenance.file` = `"artifacts/norDTCO_radical_cation_optimized.xyz"`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].provenance.atom_indices[0]` = `16`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].provenance.atom_indices[1]` = `17`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].validation.converged` = `true`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].validation.stationary_point_evidence` = `"Gaussian optimization completed; stationary point found; normal termination; 72 vibrational frequencies parsed."`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].validation.imaginary_frequency_count` = `0`
- rule `r_ar_kp_identity` / reference `kp_ar_process_identity` / field `$.states` / result path `$.states[1].validation.spin_diagnostic` = `"UBP86 doublet; final Gaussian archive reports <S2> about 0.7515 (spin contamination small)."`
- rule `r_ar_kp_validation` / reference `kp_ar_process_validation` / field `$.states[*].validation` / result path `$.states[*].validation.converged` = `true`
- rule `r_ar_kp_validation` / reference `kp_ar_process_validation` / field `$.states[*].validation` / result path `$.states[*].validation.stationary_point_evidence` = `"Gaussian optimization completed; stationary point found; normal termination; frequency job completed."`
- rule `r_ar_kp_validation` / reference `kp_ar_process_validation` / field `$.states[*].validation` / result path `$.states[*].validation.imaginary_frequency_count` = `0`
- rule `r_ar_kp_validation` / reference `kp_ar_process_validation` / field `$.states[*].validation` / result path `$.states[*].validation.spin_diagnostic` = `"Closed-shell singlet (S2 diagnostic not applicable)."`
- rule `r_ar_kp_validation` / reference `kp_ar_process_validation` / field `$.states[*].validation` / result path `$.states[*].validation.stationary_point_evidence` = `"Gaussian optimization completed; stationary point found; normal termination; 72 vibrational frequencies parsed."`
- rule `r_ar_kp_validation` / reference `kp_ar_process_validation` / field `$.states[*].validation` / result path `$.states[*].validation.spin_diagnostic` = `"UBP86 doublet; final Gaussian archive reports <S2> about 0.7515 (spin contamination small)."`
- rule `r_ar_kp_validation` / reference `kp_ar_process_validation` / field `$.validation` / result path `$.validation[0]` = `"Both states used the supplied 26-atom XYZ atom order and explicit charge/multiplicity."`
- rule `r_ar_kp_validation` / reference `kp_ar_process_validation` / field `$.validation` / result path `$.validation[1]` = `"Both native Gaussian jobs have normal termination and completed optimization/frequency evidence."`
- rule `r_ar_kp_validation` / reference `kp_ar_process_validation` / field `$.validation` / result path `$.validation[2]` = `"No imaginary frequencies were detected in either state."`
- rule `r_ar_kp_validation` / reference `kp_ar_process_validation` / field `$.validation` / result path `$.validation[3]` = `"Distance extraction independently parsed the final Gaussian orientation and measured atoms 16 and 17."`
- rule `r_ar_kp_change` / reference `kp_ar_result_change` / field `$.states[*].sulfur_distance_angstrom` / result path `$.states[*].sulfur_distance_angstrom` = `4.056140073`
- rule `r_ar_kp_change` / reference `kp_ar_result_change` / field `$.states[*].sulfur_distance_angstrom` / result path `$.states[*].sulfur_distance_angstrom` = `3.983239316`
- rule `r_ar_kp_change` / reference `kp_ar_result_change` / field `$.distance_change.value_angstrom` / result path `$.distance_change.value_angstrom` = `-0.072900758`
- rule `r_ar_con_final` / reference `con_ar_final` / field `$.conclusion` / result path `$.conclusion` = `"Oxidation contracts the S16-S17 separation by 0.072901 Å. The direction and magnitude provide structural support for the paper's qualitative transannular 2c-3e interaction hypothesis within the stated gas-phase two-state boundary."`
- rule `r_ar_con_limit` / reference `con_ar_limit` / field `$.limitations` / result path `$.limitations[0]` = `"No dication, solvent, redox free-energy, or exhaustive alternative-conformer search was required or performed."`
- rule `r_ar_con_limit` / reference `con_ar_limit` / field `$.limitations` / result path `$.limitations[1]` = `"Absolute distances are method-dependent and the contraction alone is supporting, not definitive bonding proof."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `none recorded`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Self-contained topology-generated, unoptimized norDTCO starter XYZ and system definition with atom indices, charges, multiplicities and sulfur identity; author endpoint coordinates are evaluator-private.

Public input files and hashes:

- `agent_input/data/inputs/norDTCO_neutral.xyz` — SHA-256 `3d08e7f4267c4bd145aa1b90a3486c497ee5d2b844f5a68e8c49f2604dbb8dde`; size=1059 bytes; xyz_atom_count=26; xyz_comment=norDTCO neutral independent topology-only ETKDG starter; unoptimized; atom indices are fixed by row order; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/starting_geometry_definition.json` — SHA-256 `bb7764001e0d2d822b9ac5538e7a5d0c9ecfb54cee44699a2cfc4e4bbb8b99f3`; size=749 bytes; explicit_boundary_fields={"$.atom_count": 26, "$.charge": 0, "$.formula": "C10H14S2", "$.mapped_smiles": "[C:1]1([H:6])([H:8])[C:2]([H:7])([H:9])[S:16][C:5]2([H:12])[C:4]3([H:11])[C:3]([H:10])([S:17][C:13]1([H:14])[H:15])[C:22]1([H:23])[C:18]2([H:19])[C:24]1([H:25])[C:20]3([H:21])[H:26]", "$.multiplicity": 1, "$.states.neutral.charge": 0, "$.states.neutral.multiplicity": 1, "$.states.radical_cation.charge": 1, "$.states.radical_cation.multiplicity": 2, "$.sulfur_atom_map_ids": [16, 17]}
- `agent_input/data/inputs/system_definition.json` — SHA-256 `ed4d55a6d199fab8cef2cde6bb22ad2609b8124e40e233d04b9115d02b0e5d12`; size=386 bytes; explicit_boundary_fields={"$.coordinate_units": "angstrom", "$.formula": "C10H14S2", "$.neutral.charge": 0, "$.neutral.multiplicity": 1, "$.radical_cation.charge": 1, "$.radical_cation.multiplicity": 2}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_2/paper_0de37d01e35c27df/verification_report.md` — verification record; SHA-256 `67f9475c96a2848d9e4c3ebbf3f1252bde33e03d8d9d8951afca39f8f4768651`
- `docs/verification/group_2/paper_0de37d01e35c27df/report/results.json` — verification record; SHA-256 `1d2d38b44e5059939bc5fbef76a6ef2ac697e2a63a47b575e6d0ee0e94a1f0ff`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/norDTCO_neutral_optimized.xyz` — referenced successful evidence; SHA-256 `9010b6a86ab9773059173c158073957ea3a86d70c727d94489e42213762b1df1`
- `docs/verification/group_2/paper_0de37d01e35c27df/artifacts/norDTCO_radical_cation_optimized.xyz` — referenced successful evidence; SHA-256 `02475f55c0bdbf311d4af6a2e4498efd26ead7ff8626a9a0197220b8a0ea2a5f`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
