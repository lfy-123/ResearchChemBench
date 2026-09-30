# Verified computation reference — paper_72f60526b64ce1b6 (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `success` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 40 | `QUALIFIED` | 因此本篇任务资格为 **`QUALIFIED`**。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Effect of bridge type on electronic structure and rectification in molecular junctions
- DOI: `10.1039/d5cp03687a`
- Task package: `tasks/final_verified_paper_reproduction/paper_72f60526b64ce1b6`
- Verification group: `docs/verification/group_2/paper_72f60526b64ce1b6`
- Paper documents: `papers/paper_72f60526b64ce1b6`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "calculation": {
    "axis_convention": "Input Cartesian X/Y/Z axes; report total magnitude Tot, so sign is axis-independent.",
    "convergence_evidence": "Author optimization job_81239147439c49ba85e15657e6e8ef12 success; Optimization completed; Normal termination; 60 frequencies and zero imaginary frequencies; refinement job_6ebfe972a5e64ee385d3d93a6485b1cc success with converged SCF and Normal termination.",
    "dipole_magnitude_debye": 2.6765,
    "field_v": 0.0,
    "method": "Author route: B3LYP/6-31+G(d) Opt=(ModRedundant; terminal S fixed) Freq, followed by B3LYP/6-311++G(d,p) single point",
    "software": "Gaussian 16 C.01 native runner"
  },
  "conclusion": {
    "limitations": "No external-field sweep, Au electrodes, or NEGF transport was computed; those are outside the scored isolated-molecule endpoint. The reported value is for the supplied SI geometry after the terminal-S-fixed optimization and the stated large-basis single-point refinement.",
    "text": "The author-route zero-field isolated A-D dipole is 2.6765 D, consistent with the paper's approximately 2.67 D value and its donor-acceptor asymmetry interpretation."
  },
  "status": "success",
  "system": {
    "atom_count": 22,
    "charge": 0,
    "multiplicity": 1,
    "structure_file": "artifacts/AD_optimized.xyz"
  },
  "validation": {
    "details": "22-atom public XYZ order preserved; isolated neutral singlet, zero external field; terminal S atoms fixed only during the author-style geometry optimization; final coordinates archived under artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq_optimized.xyz and the refinement output under author_zero_field_s_fixed_6311pp_sp/.",
    "geometry_or_stationarity": "Optimized stationary point with Gaussian frequency check; no imaginary frequencies.",
    "independent_check": "Dipole total parsed directly from the author-level 6-311++G(d,p) Gaussian output: X=-2.6153, Y=-0.0365, Z=0.5677, Tot=2.6765 D; the preceding 6-31+G(d) optimization/frequency is independently converged and has zero imaginary frequencies."
  }
}
```

Paper/SI document hashes:

- `papers/paper_72f60526b64ce1b6/documents/supplementary_001.pdf` — SHA-256 `bd0915de22a3e9db944c0c98421c2ffa50ae7d5524896fb28597e8d7cf76935a` (declared_match=True)
- `papers/paper_72f60526b64ce1b6/documents/main.pdf` — SHA-256 `c8aa3ceb687608453545f2b907f5e3f96f4c238484974fcf65c347ab02da7a15` (declared_match=True)

Report evidence lines retained:

- - `kp_process_validation`：作者级 Opt/Freq 的 60 个频率和 0 个虚频，加上大基组独立 SCF 精修，**通过**；
- - 作者路线：终端 S 固定的 B3LYP/6-31+G(d) Opt/Freq 与 B3LYP/6-311++G(d,p) 单点均有原始 Gaussian 输出；

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **40**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/status.json` — successful status record; SHA-256 `55f189ffce7a4d5341fc969d08c6d153d2c14d5f5841e5ac087f7cf5d060f4cd`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/collection.json` — successful execution artifact; SHA-256 `bc0d095b83cd8d584a8e577b1b2d44e55001b03e619aa3780db07c2c63413b09`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/input.com` — successful execution artifact; SHA-256 `86aef8ded0ac1137e5e8b2f24034c962a4c0362bbaccf1fb35e48d6c6678a60c`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/stdout.log` — successful execution artifact; SHA-256 `c713c70362dc97e97ede22315932f1443c7a0c259720aa9ac8dc9abe7003c144`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/status.json` — successful status record; SHA-256 `c1436c1c0d30667f64deb3d25003f8d82b76885be3babbe7686a67aff1ac4bed`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/collection.json` — successful execution artifact; SHA-256 `cee67081fd65b95fb7568c47bee520bc1377623f0c0c006ead4373a2169e379c`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/input.com` — successful execution artifact; SHA-256 `0ba062abb1aa18d76b8bc3a3af77028fc837ba2585f4ab51a7bf572efec7319a`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/stdout.log` — successful execution artifact; SHA-256 `d72a02f511a9d131eb09efbb5669bf6abf8b758d7c54c63e498d2305a91e965f`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/status.json` — successful status record; SHA-256 `5d872a2b2d34a88612d5990140c395cbbc6101527f0053f6d75075d0fae6f039`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/collection.json` — successful execution artifact; SHA-256 `c07fd87c3f94d61f6f44f3acf937439879fef1c034728ee405ba633b447ac6e7`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/input.com` — successful execution artifact; SHA-256 `b77ce37e10ecb56c7ad066da2c3a982788648a484921abd850a635571b2dad38`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/stdout.log` — successful execution artifact; SHA-256 `eae05b7029c296d491b702caacf6b887ae87384c53ae2094da19add0a4b4a9a8`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/status.json` — successful status record; SHA-256 `af38d164d360defc53865f19503a0a897a9b7ba9d9c2d0e221ea49ed84f1325f`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/collection.json` — successful execution artifact; SHA-256 `cc116cbccb3c6d88c3ce97daf4e89b33edc5554a1b03c411b559bb5293618f82`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/input.com` — successful execution artifact; SHA-256 `ed02b41a852c373a416233231d5c521acf6ae520ce4288e09879c68002615dff`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/stdout.log` — successful execution artifact; SHA-256 `3ee05a9add7205f71bd3316e18d7e22ecbbaf8b64a908012e802a57b5b9026fa`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_2ecb680a744347b8b5a7c70c1580e993/status.json` — successful status record; SHA-256 `55f189ffce7a4d5341fc969d08c6d153d2c14d5f5841e5ac087f7cf5d060f4cd`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_2ecb680a744347b8b5a7c70c1580e993/collection.json` — successful execution artifact; SHA-256 `bc0d095b83cd8d584a8e577b1b2d44e55001b03e619aa3780db07c2c63413b09`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_2ecb680a744347b8b5a7c70c1580e993/input.com` — successful execution artifact; SHA-256 `86aef8ded0ac1137e5e8b2f24034c962a4c0362bbaccf1fb35e48d6c6678a60c`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_2ecb680a744347b8b5a7c70c1580e993/request.json` — successful execution artifact; SHA-256 `ca114fd1b1bac869bf7f9801a59e0a98381c9b509ccb5d98f9ea033f34ceb9a4`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_2ecb680a744347b8b5a7c70c1580e993/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_4f7926c0fc0f4bd58a4b1280eec43d77/status.json` — successful status record; SHA-256 `c1436c1c0d30667f64deb3d25003f8d82b76885be3babbe7686a67aff1ac4bed`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_4f7926c0fc0f4bd58a4b1280eec43d77/collection.json` — successful execution artifact; SHA-256 `cee67081fd65b95fb7568c47bee520bc1377623f0c0c006ead4373a2169e379c`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_4f7926c0fc0f4bd58a4b1280eec43d77/input.com` — successful execution artifact; SHA-256 `0ba062abb1aa18d76b8bc3a3af77028fc837ba2585f4ab51a7bf572efec7319a`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_4f7926c0fc0f4bd58a4b1280eec43d77/request.json` — successful execution artifact; SHA-256 `17aab378fbb7313a65ce175e216448ed7a3ec3724655f3cce3537c4d3457d53f`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_4f7926c0fc0f4bd58a4b1280eec43d77/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_6ebfe972a5e64ee385d3d93a6485b1cc/status.json` — successful status record; SHA-256 `5d872a2b2d34a88612d5990140c395cbbc6101527f0053f6d75075d0fae6f039`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_6ebfe972a5e64ee385d3d93a6485b1cc/collection.json` — successful execution artifact; SHA-256 `c07fd87c3f94d61f6f44f3acf937439879fef1c034728ee405ba633b447ac6e7`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_6ebfe972a5e64ee385d3d93a6485b1cc/input.com` — successful execution artifact; SHA-256 `b77ce37e10ecb56c7ad066da2c3a982788648a484921abd850a635571b2dad38`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_6ebfe972a5e64ee385d3d93a6485b1cc/request.json` — successful execution artifact; SHA-256 `3e03ebdde16fa2f3c8e5fd523decfd596ab2b4fed7107ffac6439bcce48be57b`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_6ebfe972a5e64ee385d3d93a6485b1cc/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_81239147439c49ba85e15657e6e8ef12/status.json` — successful status record; SHA-256 `af38d164d360defc53865f19503a0a897a9b7ba9d9c2d0e221ea49ed84f1325f`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_81239147439c49ba85e15657e6e8ef12/collection.json` — successful execution artifact; SHA-256 `cc116cbccb3c6d88c3ce97daf4e89b33edc5554a1b03c411b559bb5293618f82`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_81239147439c49ba85e15657e6e8ef12/input.com` — successful execution artifact; SHA-256 `ed02b41a852c373a416233231d5c521acf6ae520ce4288e09879c68002615dff`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_81239147439c49ba85e15657e6e8ef12/request.json` — successful execution artifact; SHA-256 `00e816245c36c4f03e155171fdf4afd336ea15f054684be2da973b7d1eae56ae`
- `docs/verification/group_2/paper_72f60526b64ce1b6/native_workspace_batch/outputs/execution_jobs/job_81239147439c49ba85e15657e6e8ef12/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/status.json` — label=group_2 paper_72f60526b64ce1b AD_zero_field_b3lyp_optfreq; submitted_at=2026-08-29T06:59:48.557166+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31+G(d) Opt Freq NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/AD_zero_field_b3lyp_optfreq.chk`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/input.com`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/AD_zero_field_b3lyp_optfreq/stdout.log`
2. `artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/status.json` — label=group_2 paper_72f60526b64ce1b6 author_zero_field_s_fixed_optfreq; submitted_at=2026-08-30T16:52:04.614244+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31+G(d) Opt=(ModRedundant,CalcFC,MaxCycles=300) Freq NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/author_zero_field_s_fixed_optfreq.chk`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/input.com`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_optfreq/stdout.log`
3. `artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/status.json` — label=group_2 paper_72f60526b64ce1b6 author_zero_field_s_fixed_6311pp_sp; submitted_at=2026-08-31T16:07:35.441556+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-311++G(d,p) NoSymm SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/author_zero_field_s_fixed_6311pp_sp.chk`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/collection.json`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/input.com`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/stderr.log`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_zero_field_s_fixed_6311pp_sp/stdout.log`
4. `artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/status.json` — label=group_2 paper_72f60526b64ce1b6 author_b3lyp_6311ppdp_zero_field_sp; submitted_at=2026-08-31T16:22:25.441942+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-311++G(d,p) SP NoSymm SCF=(Tight,XQC,MaxCycle=512) Int=UltraFine; command=g16 < input.com
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/author_b3lyp_6311ppdp_zero_field_sp.chk`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/collection.json`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/input.com`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/stderr.log`
   - output: `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/gaussian_batch/author_b3lyp_6311ppdp_zero_field_sp/stdout.log`

## Evaluator alignment

- Key-point IDs: `kp_process_state, kp_process_validation, kp_result_dipole`
- Conclusion IDs: `c_final_dipole`
- Scoring-rule IDs: `r_state, r_validation, r_dipole, r_conclusion`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_state` → reference `kp_process_state`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert check of stated system and provenance; evaluator_target_present=False
- rule `r_validation` → reference `kp_process_validation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific validation; evaluator_target_present=False
- rule `r_dipole` → reference `kp_result_dipole`; type=numeric; unit=Debye; tolerance=0.35; comparison=absolute difference; evaluator_target_present=True
- rule `r_conclusion` → reference `c_final_dipole`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_dipole` / reference `kp_result_dipole`: target=2.67 Debye; tolerance=0.35; numeric result leaves=[2.6765]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_state` / reference `kp_process_state` / field `$.system.charge` / result path `$.system.charge` = `0`
- rule `r_state` / reference `kp_process_state` / field `$.system.multiplicity` / result path `$.system.multiplicity` = `1`
- rule `r_state` / reference `kp_process_state` / field `$.system.atom_count` / result path `$.system.atom_count` = `22`
- rule `r_state` / reference `kp_process_state` / field `$.calculation.field_v` / result path `$.calculation.field_v` = `0.0`
- rule `r_state` / reference `kp_process_state` / field `$.calculation.method` / result path `$.calculation.method` = `"Author route: B3LYP/6-31+G(d) Opt=(ModRedundant; terminal S fixed) Freq, followed by B3LYP/6-311++G(d,p) single point"`
- rule `r_state` / reference `kp_process_state` / field `$.calculation.software` / result path `$.calculation.software` = `"Gaussian 16 C.01 native runner"`
- rule `r_validation` / reference `kp_process_validation` / field `$.validation.geometry_or_stationarity` / result path `$.validation.geometry_or_stationarity` = `"Optimized stationary point with Gaussian frequency check; no imaginary frequencies."`
- rule `r_validation` / reference `kp_process_validation` / field `$.validation.independent_check` / result path `$.validation.independent_check` = `"Dipole total parsed directly from the author-level 6-311++G(d,p) Gaussian output: X=-2.6153, Y=-0.0365, Z=0.5677, Tot=2.6765 D; the preceding 6-31+G(d) optimization/frequency is independently converged and has zero imaginary frequencies."`
- rule `r_validation` / reference `kp_process_validation` / field `$.validation.details` / result path `$.validation.details` = `"22-atom public XYZ order preserved; isolated neutral singlet, zero external field; terminal S atoms fixed only during the author-style geometry optimization; final coordinates archived under artifacts/gaussian_batch/author_zero_field_s_f..."`
- rule `r_dipole` / reference `kp_result_dipole` / field `$.calculation.dipole_magnitude_debye` / result path `$.calculation.dipole_magnitude_debye` = `2.6765`
- rule `r_conclusion` / reference `c_final_dipole` / field `$.conclusion.text` / result path `$.conclusion.text` = `"The author-route zero-field isolated A-D dipole is 2.6765 D, consistent with the paper's approximately 2.67 D value and its donor-acceptor asymmetry interpretation."`
- rule `r_conclusion` / reference `c_final_dipole` / field `$.conclusion.limitations` / result path `$.conclusion.limitations` = `"No external-field sweep, Au electrodes, or NEGF transport was computed; those are outside the scored isolated-molecule endpoint. The reported value is for the supplied SI geometry after the terminal-S-fixed optimization and the stated la..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized/Cartesian result geometry provenance is not proven answer-neutral; confirm starting-vs-final status before release
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — 22-atom XYZ and system metadata for the isolated neutral singlet A–D molecule.

Public input files and hashes:

- `agent_input/data/inputs/AD_isolated.xyz` — SHA-256 `3676366bae0d21b208ca9560218191a544ef15476bb20d3591bd16e8c1ce6717`; size=891 bytes; xyz_atom_count=22; xyz_comment=A-D isolated molecule; SI Cartesian coordinates, no external field; neutral singlet; explicit_boundary_fields={"units_hint": "explicit angstrom marker"}
- `agent_input/data/inputs/system.json` — SHA-256 `022b28f41d5b4dc5a8cbd1151a5dbe0d1ca1d4625e4bfd60b713505539c2e44d`; size=484 bytes; explicit_boundary_fields={"$.atom_order_note": "Atom order is exactly the order in the supplied SI coordinate block; retain it in submitted provenance.", "$.charge": 0, "$.coordinate_units": "angstrom", "$.multiplicity": 1}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `agent_input/data/inputs/AD_isolated.xyz`

## Evidence files

- `docs/verification/group_2/paper_72f60526b64ce1b6/verification_report.md` — verification record; SHA-256 `623058a17d32c9103c2b44e2fdb13f1337db584054a6b62e6345219bb2264a66`
- `docs/verification/group_2/paper_72f60526b64ce1b6/report/results.json` — verification record; SHA-256 `1a67b97caeab6105328584c0c62c5bfcbe6476012f3728ca296f5c484c065059`
- `docs/verification/group_2/paper_72f60526b64ce1b6/artifacts/AD_optimized.xyz` — referenced successful evidence; SHA-256 `1390f9af5215118705f299b7c362b747d8789c8ce300fd6972e07996de6b4420`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
