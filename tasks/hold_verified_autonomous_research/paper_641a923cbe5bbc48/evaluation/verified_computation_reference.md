> **HOLD — 2026-09-24, user-directed source review.** The main paper and synthetic SI identify C15H25N4S+, but SI S113–S118, the public XYZ files and the archived Gaussian verification actually describe C15H25N4O+. Historical success below verifies the oxygen model, not the stated thiourea. Do not use it as evidence that the sulfur task is validated. Resolve the scientific identity and complete the appropriate verification before release. See [source conflict and verification handoff](../../../HOLD_paper_641a923cbe5bbc48_HANDOFF.md).

# Verified computation reference — paper_641a923cbe5bbc48 (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 87 | `QUALIFIED` | 最终严格判定：**QUALIFIED（scope-limited）**。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: d5ob01845e 1369..1378 ++
- DOI: `10.1039/d5ob01845e`
- Task package: `tasks/final_verified_autonomous_research/paper_641a923cbe5bbc48`
- Verification group: `docs/verification/group_2/paper_641a923cbe5bbc48`
- Paper documents: `papers/paper_641a923cbe5bbc48`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": {
    "ordering": [
      "ZE",
      "ZZ",
      "EZ"
    ],
    "reference_id": "lowest_G",
    "relative_energies_kcal_mol": {
      "EZ": 10.215854,
      "ZE": 0.0,
      "ZZ": 1.063629
    }
  },
  "conclusion": {
    "claim": "The validated isolated-cation conformer ordering supports conformational relevance, but does not by itself establish solution populations or a full mechanism. Three supplied conformers are compared only after all three charge +1/singlet minima are validated.",
    "limitations": "Legacy charge-0 attempts are retained but excluded; no result is inferred from a running or failed job. The calculation is an isolated-molecule comparison and does not alone prove solution populations or a full reaction mechanism."
  },
  "conformers": [
    {
      "free_energy_kcal_mol": -552452.2218146174,
      "frequency_validation": "minimum (zero imaginary frequencies)",
      "id": "ZZ",
      "optimization": "converged",
      "target_job_id": "job_4a1bb3dc16a641b498cf058553a8ecff",
      "validation_evidence": {
        "duration_seconds": 498.0,
        "electronic_energy_hartree": -880.737765862,
        "evidence_directory": "docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z",
        "frequency_count": 129,
        "gibbs_free_energy_hartree": -880.388655,
        "imaginary_frequency_count": 0,
        "job_id": "hpc-job-2939762e-a67a-419a-a4f0-1fd580e8c8b1",
        "normal_termination": true,
        "optimization_completed": true,
        "status": "success",
        "stdout": "artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_summary_hpc.json"
      }
    },
    {
      "free_energy_kcal_mol": -552443.0695889391,
      "frequency_validation": "minimum (zero imaginary frequencies)",
      "id": "EZ",
      "optimization": "converged",
      "target_job_id": "job_949acb9376724f5084c7c3d685074286",
      "validation_evidence": {
        "duration_seconds": 826.0,
        "electronic_energy_hartree": -880.723925702,
        "evidence_directory": "docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z",
        "frequency_count": 129,
        "gibbs_free_energy_hartree": -880.37407,
        "imaginary_frequency_count": 0,
        "job_id": "hpc-job-c5bc14e0-ba41-480a-a6fb-cb9008450012",
        "normal_termination": true,
        "optimization_completed": true,
        "status": "success",
        "stdout": "artifacts/gaussian_batch/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_summary_hpc.json"
      }
    },
    {
      "free_energy_kcal_mol": -552453.2854431758,
      "frequency_validation": "minimum (zero imaginary frequencies)",
      "id": "ZE",
      "optimization": "converged",
      "target_job_id": "job_a191b20e56654741be7586ddf89d4042",
      "validation_evidence": {
        "duration_seconds": 25578.920055,
        "electronic_energy_hartree": -880.740663308,
        "frequency_count": 129,
        "gibbs_free_energy_hartree": -880.39035,
        "imaginary_frequency_count": 0,
        "job_id": "job_a191b20e56654741be7586ddf89d4042",
        "normal_termination": true,
        "optimization_completed": true,
        "status": "success",
        "stdout": "native_workspace_batch/outputs/execution_jobs/job_a191b20e56654741be7586ddf89d4042/stdout.log"
      }
    }
  ],
  "method": {
    "approach_justification": "Same charge-corrected route and supplied identity for all three conformers",
    "free_energy_convention": "Gaussian electronic + thermal free energy; common isolated-molecule convention",
    "level": "B3LYP/6-31G(d,p) Opt/Freq",
    "standard_state_correction": "No additional correction; differences use identical convention",
    "temperature_K": 298.15
  },
  "status": "complete"
}
```

Paper/SI document hashes:

- `papers/paper_641a923cbe5bbc48/documents/supplementary_001.pdf` — SHA-256 `aec6aebad6109e008a2b9e99e48d2baf5d2992dc460c183fc4072518d251798c` (declared_match=True)
- `papers/paper_641a923cbe5bbc48/documents/main.pdf` — SHA-256 `40b9da19fd0d7305b7c46f0da7dfa0fd38387970bb4f1d451fa68e7abe0fabd5` (declared_match=True)

Report evidence lines retained:

- - 三个 +1/singlet B3LYP/6-31G(d,p) Opt/Freq 端点均正常终止、129 个频率且 0 虚频。
- - 从独立冻结能量得到排序 `ZE < ZZ < EZ`，与 evaluator 预期 `ZE < ZZ < EZ` 一致；结论保留构象相关性及孤立体系范围限制。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **70**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/status.json` — successful status record; SHA-256 `82cbc1f995f373d579c4217477d81f640bd9c6adddd8bbab4265d737c38c74c1`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/collection.json` — successful execution artifact; SHA-256 `87517998d7ca61e3b8594cf03d4d1993bd12f5c9921a6432fc629246f3713c40`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/input.com` — successful execution artifact; SHA-256 `0d76665302d661ee4f146a9d350770039590eaf5ed43bebf10b18a4a8c1d732d`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/stdout.log` — successful execution artifact; SHA-256 `3c1143c73b36d0d2370a572361b87d231101f36f2e3063ce0e26c9097817b02b`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/status.json` — successful status record; SHA-256 `430f5590bfb2d47d699b573f4f312fd52f28a40e62b33d00f00eb299604f6f09`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/input.com` — successful execution artifact; SHA-256 `219edb73044278ba1e940eced62463d0e72283c1422b8ead92ea9bf78dabb3f9`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/route_manifest.json` — successful execution artifact; SHA-256 `a6bd1c812b5879aec3ce291ce71a86ab588483101cd2150d6a41b36ac6fa6649`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/source_input.com` — successful execution artifact; SHA-256 `219edb73044278ba1e940eced62463d0e72283c1422b8ead92ea9bf78dabb3f9`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/status.json` — successful status record; SHA-256 `52da4b2a1129d3c32a55649fe31f6d4bad72675571ec37465532a881509bf95b`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/collection.json` — successful execution artifact; SHA-256 `c3fde104e851684ae685e8df1dc843c786d6009021cd8fe49c5c25eabbc5456e`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/input.com` — successful execution artifact; SHA-256 `0bc8936ab90f5ccdf5e4387e22ef8ea4cce0fc445153eb18ec48da3b6178bc67`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/route_manifest.json` — successful execution artifact; SHA-256 `5ad72e58d5cd633dcbae3e889e3abdf7193fc633ad42d916a44119611f426a88`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ez_optfreq/status.json` — successful status record; SHA-256 `9f4436f243bbf2a2ce731a590473e3c47700447378677861fc9d7ae0620dfa57`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ez_optfreq/collection.json` — successful execution artifact; SHA-256 `d02c0fff44e39d499c1c48c93d08aed4dae8b4fb1420c33a816df7a36572a4e5`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ez_optfreq/input.com` — successful execution artifact; SHA-256 `0d7724a3fcdd813c2da247faa7fa47fdbb17c0cf65165bf7fed32b97085fb307`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ez_optfreq/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ez_optfreq/stdout.log` — successful execution artifact; SHA-256 `56c9700090a566946a37427f167b9724c7267f7d328a04df92beaed3f21cfe56`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ze_optfreq/status.json` — successful status record; SHA-256 `14ffe4413e300d0779aec6a421cc8c6889e9de5872af8f6deaf3c0a362cbf5e5`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ze_optfreq/collection.json` — successful execution artifact; SHA-256 `749da34041fb4dd0695ee0f382c5ddd858f5dbc296294d4c82a46478e0bb1e0a`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ze_optfreq/input.com` — successful execution artifact; SHA-256 `9b8de582e3d15c5eb55eaf2b9e4490ed26dbbf0d3e49556102467643f75765dd`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ze_optfreq/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ze_optfreq/stdout.log` — successful execution artifact; SHA-256 `d715ca069b4a1a2578c79bb3907227ae05cd76b509913028da452bf5a488c0f0`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/zz_optfreq/status.json` — successful status record; SHA-256 `310c60d612cc23f4684b5db69cd6d07ef7f733ee51fdf10053c796ab6068b0eb`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/zz_optfreq/collection.json` — successful execution artifact; SHA-256 `2dd3bd880b65b1bfdd79c29d1e823df53b8e2d2afc5d100655a5569c55407929`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/zz_optfreq/input.com` — successful execution artifact; SHA-256 `c74ea30db625a2af404d405b91f4cde81731054ca0b3022b55ab3789a9482cab`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/zz_optfreq/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/zz_optfreq/stdout.log` — successful execution artifact; SHA-256 `48c3183eba20905bcbb7e4835627147eab7c2a8deec291b103e3af15f4fdb4c2`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_45efa5292d704503b07390820a69df5a/status.json` — successful status record; SHA-256 `310c60d612cc23f4684b5db69cd6d07ef7f733ee51fdf10053c796ab6068b0eb`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_45efa5292d704503b07390820a69df5a/collection.json` — successful execution artifact; SHA-256 `2dd3bd880b65b1bfdd79c29d1e823df53b8e2d2afc5d100655a5569c55407929`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_45efa5292d704503b07390820a69df5a/input.com` — successful execution artifact; SHA-256 `c74ea30db625a2af404d405b91f4cde81731054ca0b3022b55ab3789a9482cab`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_45efa5292d704503b07390820a69df5a/request.json` — successful execution artifact; SHA-256 `5b4626e87d7bbdb23d096ec5431bdaee32c9f0665cb868930428c821144d788a`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_45efa5292d704503b07390820a69df5a/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_4a1bb3dc16a641b498cf058553a8ecff/status.json` — successful status record; SHA-256 `52da4b2a1129d3c32a55649fe31f6d4bad72675571ec37465532a881509bf95b`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_4a1bb3dc16a641b498cf058553a8ecff/collection.json` — successful execution artifact; SHA-256 `c3fde104e851684ae685e8df1dc843c786d6009021cd8fe49c5c25eabbc5456e`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_4a1bb3dc16a641b498cf058553a8ecff/input.com` — successful execution artifact; SHA-256 `0bc8936ab90f5ccdf5e4387e22ef8ea4cce0fc445153eb18ec48da3b6178bc67`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_4a1bb3dc16a641b498cf058553a8ecff/request.json` — successful execution artifact; SHA-256 `9e5690c67942baacb8ec9110b74e83ceee12e4f326e8c92f1cc793585145790e`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_4a1bb3dc16a641b498cf058553a8ecff/status.interruption_recovery.json` — successful execution artifact; SHA-256 `fa78b7f3421933ba9ed4de4647082e2b7724396d32729202c5a4f7c10fe3b342`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_58576811a08843219b0d322d63a96c5b/status.json` — successful status record; SHA-256 `9f4436f243bbf2a2ce731a590473e3c47700447378677861fc9d7ae0620dfa57`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_58576811a08843219b0d322d63a96c5b/collection.json` — successful execution artifact; SHA-256 `d02c0fff44e39d499c1c48c93d08aed4dae8b4fb1420c33a816df7a36572a4e5`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_58576811a08843219b0d322d63a96c5b/input.com` — successful execution artifact; SHA-256 `0d7724a3fcdd813c2da247faa7fa47fdbb17c0cf65165bf7fed32b97085fb307`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_58576811a08843219b0d322d63a96c5b/request.json` — successful execution artifact; SHA-256 `d761fb34293741563a998938bb5fc9cca0dcb4576c847e2801723f00111056b8`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_58576811a08843219b0d322d63a96c5b/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_a191b20e56654741be7586ddf89d4042/status.json` — successful status record; SHA-256 `82cbc1f995f373d579c4217477d81f640bd9c6adddd8bbab4265d737c38c74c1`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_a191b20e56654741be7586ddf89d4042/collection.json` — successful execution artifact; SHA-256 `87517998d7ca61e3b8594cf03d4d1993bd12f5c9921a6432fc629246f3713c40`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_a191b20e56654741be7586ddf89d4042/input.com` — successful execution artifact; SHA-256 `0d76665302d661ee4f146a9d350770039590eaf5ed43bebf10b18a4a8c1d732d`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_a191b20e56654741be7586ddf89d4042/request.json` — successful execution artifact; SHA-256 `efacb42d6861b70321f733f81ec1b9abf172cadc89849dd6d785e2d30f9c2222`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_a191b20e56654741be7586ddf89d4042/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_c340575af7ee4cd3bbdbe8a93e3d729e/status.json` — successful status record; SHA-256 `14ffe4413e300d0779aec6a421cc8c6889e9de5872af8f6deaf3c0a362cbf5e5`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_c340575af7ee4cd3bbdbe8a93e3d729e/collection.json` — successful execution artifact; SHA-256 `749da34041fb4dd0695ee0f382c5ddd858f5dbc296294d4c82a46478e0bb1e0a`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_c340575af7ee4cd3bbdbe8a93e3d729e/input.com` — successful execution artifact; SHA-256 `9b8de582e3d15c5eb55eaf2b9e4490ed26dbbf0d3e49556102467643f75765dd`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_c340575af7ee4cd3bbdbe8a93e3d729e/request.json` — successful execution artifact; SHA-256 `440e44c322bb48eb8443242554b72865b6b47966a93cfd47e62b863eced51f36`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_c340575af7ee4cd3bbdbe8a93e3d729e/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/status.json` — successful status record; SHA-256 `325d70b158e418f1e2bfde2d915251d6b5317eef0c7dc01d180957bae262918a`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `09824bc57d5f9f7f72103d610bc06c14c4a54d0f0cb0add4422a006a88ecd997`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/input.com` — successful execution artifact; SHA-256 `9086bd1c726f37e125d66694f1a544a8d41bb0eb7c13e2639d1fa32ab08facc9`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/route_manifest.json` — successful execution artifact; SHA-256 `edd21cddee0f3c4d9d3aaa94d8c3f75fbfa3b5e3946c34257db6e49b23ea148c`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/status.json` — successful status record; SHA-256 `430f5590bfb2d47d699b573f4f312fd52f28a40e62b33d00f00eb299604f6f09`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `ba24e555079726211dd3de9d5b18ab748f5ad9bbd061da113efb3297604e8998`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/input.com` — successful execution artifact; SHA-256 `219edb73044278ba1e940eced62463d0e72283c1422b8ead92ea9bf78dabb3f9`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/route_manifest.json` — successful execution artifact; SHA-256 `a6bd1c812b5879aec3ce291ce71a86ab588483101cd2150d6a41b36ac6fa6649`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/source_input.com` — successful execution artifact; SHA-256 `219edb73044278ba1e940eced62463d0e72283c1422b8ead92ea9bf78dabb3f9`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/status.json` — successful status record; SHA-256 `6aac739018c81e7d95e218d395f3077cb79f4b80525ca7c5fba4303fa4697063`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `9c83718350ad12b1da82730128231d358bb4816368536d4a966ef51b6169cd7a`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/input.com` — successful execution artifact; SHA-256 `3da537cf85de2ccfcebdeed0b93b08fbbd4db393785dbf5713432e6d3e05cfed`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/route_manifest.json` — successful execution artifact; SHA-256 `5ad72e58d5cd633dcbae3e889e3abdf7193fc633ad42d916a44119611f426a88`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/zz_optfreq/status.json` — label=group_2 paper_641a923cbe5bbc48 zz_optfreq; submitted_at=2026-08-29T19:21:20.745042+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31+G(d,p) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/zz_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/zz_optfreq/input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/zz_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/zz_optfreq/stdout.log`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/zz_optfreq/zz_optfreq.chk`
2. `artifacts/gaussian_batch/ez_optfreq/status.json` — label=group_2 paper_641a923cbe5bbc48 ez_optfreq; submitted_at=2026-08-29T19:21:21.291773+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31+G(d,p) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ez_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ez_optfreq/ez_optfreq.chk`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ez_optfreq/input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ez_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ez_optfreq/stdout.log`
3. `artifacts/gaussian_batch/ze_optfreq/status.json` — label=group_2 paper_641a923cbe5bbc48 ze_optfreq; submitted_at=2026-08-29T19:21:21.825468+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31+G(d,p) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ze_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ze_optfreq/input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ze_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ze_optfreq/stdout.log`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/ze_optfreq/ze_optfreq.chk`
4. `artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/status.json` — label=group_2 paper_641a923cbe5bbc48 author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry; submitted_at=2026-08-31T18:06:48.806093+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d,p) Opt=(CalcFC,MaxCycles=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry.chk`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/collection.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/route_manifest.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/stderr.log`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry/stdout.log`
5. `artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/status.json` — label=group_2 paper_641a923cbe5bbc48 author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry; submitted_at=2026-08-31T18:16:50.445554+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d,p) Opt=(CalcFC,MaxCycles=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry.chk`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/collection.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/stderr.log`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ze_b3lyp_631gdp_optfreq_charge_corrected_retry/stdout.log`
6. `artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/status.json` — label=artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/status.json
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20.chk`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/route_manifest.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/source_input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/stderr.log`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20/stdout.log`
7. `provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/status.json` — label=provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/status.json
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc_migration.chk`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/complete.marker`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/stderr.log`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/stdout.log`
8. `provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/status.json` — label=provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/status.json
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20.chk`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/complete.marker`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/source_input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_hpc20_20260905T031615Z/stderr.log`
9. `provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/status.json` — label=provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/status.json
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry.chk`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/complete.marker`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/input.com`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/stderr.log`
   - output: `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/stdout.log`

## Evaluator alignment

- Key-point IDs: `ar_process, ar_result`
- Conclusion IDs: `ar_final`
- Scoring-rule IDs: `r1, r2, r3`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r1` → reference `ar_process`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert identity-by-identity verification; records must collectively cover zz, ez and ze; evaluator_target_present=False
- rule `r2` → reference `ar_result`; type=ordering; unit=not recorded; tolerance=not recorded; comparison=exact ordering; evaluator_target_present=False
- rule `r3` → reference `ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].id` = `"ZZ"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].optimization` = `"converged"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].frequency_validation` = `"minimum (zero imaginary frequencies)"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].free_energy_kcal_mol` = `-552452.2218146174`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.status` = `"success"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.job_id` = `"hpc-job-2939762e-a67a-419a-a4f0-1fd580e8c8b1"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.normal_termination` = `true`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.optimization_completed` = `true`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.frequency_count` = `129`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.imaginary_frequency_count` = `0`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.gibbs_free_energy_hartree` = `-880.388655`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.electronic_energy_hartree` = `-880.737765862`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.duration_seconds` = `498.0`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.stdout` = `"artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_summary_hpc.json"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].validation_evidence.evidence_directory` = `"docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[0].target_job_id` = `"job_4a1bb3dc16a641b498cf058553a8ecff"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].id` = `"EZ"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].optimization` = `"converged"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].frequency_validation` = `"minimum (zero imaginary frequencies)"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].free_energy_kcal_mol` = `-552443.0695889391`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.status` = `"success"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.job_id` = `"hpc-job-c5bc14e0-ba41-480a-a6fb-cb9008450012"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.normal_termination` = `true`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.optimization_completed` = `true`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.frequency_count` = `129`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.imaginary_frequency_count` = `0`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.gibbs_free_energy_hartree` = `-880.37407`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.electronic_energy_hartree` = `-880.723925702`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.duration_seconds` = `826.0`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.stdout` = `"artifacts/gaussian_batch/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_summary_hpc.json"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].validation_evidence.evidence_directory` = `"docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T..."`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[1].target_job_id` = `"job_949acb9376724f5084c7c3d685074286"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].id` = `"ZE"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].optimization` = `"converged"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].frequency_validation` = `"minimum (zero imaginary frequencies)"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].free_energy_kcal_mol` = `-552453.2854431758`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].validation_evidence.status` = `"success"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].validation_evidence.job_id` = `"job_a191b20e56654741be7586ddf89d4042"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].validation_evidence.normal_termination` = `true`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].validation_evidence.optimization_completed` = `true`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].validation_evidence.frequency_count` = `129`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].validation_evidence.imaginary_frequency_count` = `0`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].validation_evidence.gibbs_free_energy_hartree` = `-880.39035`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].validation_evidence.electronic_energy_hartree` = `-880.740663308`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].validation_evidence.duration_seconds` = `25578.920055`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].validation_evidence.stdout` = `"native_workspace_batch/outputs/execution_jobs/job_a191b20e56654741be7586ddf89d4042/stdout.log"`
- rule `r1` / reference `ar_process` / field `$.conformers` / result path `$.conformers[2].target_job_id` = `"job_a191b20e56654741be7586ddf89d4042"`
- rule `r2` / reference `ar_result` / field `$.comparison.ordering` / result path `$.comparison.ordering[0]` = `"ZE"`
- rule `r2` / reference `ar_result` / field `$.comparison.ordering` / result path `$.comparison.ordering[1]` = `"ZZ"`
- rule `r2` / reference `ar_result` / field `$.comparison.ordering` / result path `$.comparison.ordering[2]` = `"EZ"`
- rule `r3` / reference `ar_final` / field `$.conclusion` / result path `$.conclusion.claim` = `"The validated isolated-cation conformer ordering supports conformational relevance, but does not by itself establish solution populations or a full mechanism. Three supplied conformers are compared only after all three charge +1/singlet ..."`
- rule `r3` / reference `ar_final` / field `$.conclusion` / result path `$.conclusion.limitations` = `"Legacy charge-0 attempts are retained but excluded; no result is inferred from a running or failed job. The calculation is an isolated-molecule comparison and does not alone prove solution populations or a full reaction mechanism."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized/final structure is exposed as agent input for a scored comparison; redesign with neutral or independently generated starting geometry
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Three explicit XYZ starting geometries for 7+ conformers, charge +1 singlet.

Public input files and hashes:

- `agent_input/data/inputs/ez.xyz` — SHA-256 `5cd4c901381e706b730f981ede98bc6f98cebb4f9e0bb2761ec1c70305a7293d`; size=1481 bytes; xyz_atom_count=45; xyz_comment=7+ isolated catalyst conformer E,Z conformer; charge +1, multiplicity 1; SI B3LYP coordinate block; explicit_boundary_fields={"charge": "+1", "multiplicity": "1"}
- `agent_input/data/inputs/ze.xyz` — SHA-256 `38a018a9abdafed5372be9ab4ff33d18d676d953e1b4a133b242575f36479875`; size=1472 bytes; xyz_atom_count=45; xyz_comment=7+ isolated catalyst conformer Z,E conformer; charge +1, multiplicity 1; SI B3LYP coordinate block; explicit_boundary_fields={"charge": "+1", "multiplicity": "1"}
- `agent_input/data/inputs/zz.xyz` — SHA-256 `c9c9ced3c90c6f20b08bd16bb37403f3dc76ce7c1f6f65f523140ab7353e2ad4`; size=1481 bytes; xyz_atom_count=45; xyz_comment=7+ isolated catalyst conformer Z,Z conformer; charge +1, multiplicity 1; SI B3LYP coordinate block; explicit_boundary_fields={"charge": "+1", "multiplicity": "1"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `agent_input/data/inputs/ez.xyz, agent_input/data/inputs/ze.xyz, agent_input/data/inputs/zz.xyz`

## Evidence files

- `docs/verification/group_2/paper_641a923cbe5bbc48/verification_report.md` — verification record; SHA-256 `1f5237af41cd778fba3100e05d5134f1bc0f85ea058ce5690bf9b0bf945bed99`
- `docs/verification/group_2/paper_641a923cbe5bbc48/report/results.json` — verification record; SHA-256 `c836ca4903267985bba8ee5eeffaa9a8d7afc7666b732de341b61f4086712c2d`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_summary_hpc.json` — referenced successful evidence; SHA-256 `fa3b41f7b0097a9a7e6d864a6f2a2303a038487706038877c80a343b810cc25a`
- `docs/verification/group_2/paper_641a923cbe5bbc48/artifacts/gaussian_batch/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_summary_hpc.json` — referenced successful evidence; SHA-256 `d35f3c8db2f266393e6dc0f5a3b6e040f36d7b2e69633f83c36473da458d251f`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_ez_b3lyp_631gdp_optfreq_charge_corrected_retry_local_migration_20260905T024151Z/status.json` — referenced successful evidence; SHA-256 `325d70b158e418f1e2bfde2d915251d6b5317eef0c7dc01d180957bae262918a`
- `docs/verification/group_2/paper_641a923cbe5bbc48/provenance/qzcli_hpc/author_zz_b3lyp_631gdp_optfreq_charge_corrected_retry_hpc20_20260905T221454Z/status.json` — referenced successful evidence; SHA-256 `6aac739018c81e7d95e218d395f3077cb79f4b80525ca7c5fba4303fa4697063`
- `docs/verification/group_2/paper_641a923cbe5bbc48/native_workspace_batch/outputs/execution_jobs/job_a191b20e56654741be7586ddf89d4042/stdout.log` — referenced successful evidence; SHA-256 `3c1143c73b36d0d2370a572361b87d231101f36f2e3063ce0e26c9097817b02b`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
