# Verified computation reference — paper_3235db287859287e (paper_reproduction)

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
| 3 | `QUALIFIED` | > **当前状态：`QUALIFIED`（2026-09-11）。** evaluator 所要求的 E/Z 子路线已完成 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: d5gc05810d 2109..2122 ++
- DOI: `10.1039/d5gc05810d`
- Task package: `tasks/final_verified_paper_reproduction/paper_3235db287859287e`
- Verification group: `docs/verification/group_4/paper_3235db287859287e`
- Paper documents: `papers/paper_3235db287859287e`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": {
    "basis": "Difference of exact mixed-basis M06-2X/Gen SMD(MeCN) 298 K thermal Gibbs energies.",
    "delta_G_E_minus_Z_kcal_mol": 1.6327796513633224,
    "favored_object": "3aa_Z"
  },
  "coverage": {
    "conformer_count_by_object": {
      "3aa_E": 1,
      "3aa_Z": 1
    },
    "deduplication_and_stopping": "One evaluator-defined conformer per named stereoisomer; old retries are technical attempts of the same input."
  },
  "limitations": "Single conformer per named stereoisomer; comparison is limited to the evaluator scientific question and does not establish a global conformer ensemble or kinetics.",
  "objects": [
    {
      "configuration": "Z",
      "connectivity_verified": true,
      "dihedral_deg": 2.410489071910912,
      "free_energy_hartree": -1280.56295,
      "free_energy_kcal_mol": 0.0,
      "id": "3aa_Z",
      "input_sha256": "542161c22d5285162e1af10be54a69fa25bc8ef82778ccdb88adc11b276dadc3",
      "job_dir": "docs/verification/group_4/paper_3235db287859287e/hpc_runs/3aa_E_author_exact_route_optfreq__retry_005_hpc20_p6",
      "minimum_validation": {
        "frequency_count": 105,
        "imaginary_frequency_count": 0,
        "normal_termination": true,
        "optimization_completed": true,
        "vibrational_analysis": true
      },
      "stdout_sha256": "6f46e582a9e701adfc15f69b1f9b567a1d3b8115829f671eee36d83dd86657cd"
    },
    {
      "configuration": "E",
      "connectivity_verified": true,
      "dihedral_deg": 175.40186777030567,
      "free_energy_hartree": -1280.560348,
      "free_energy_kcal_mol": 1.6327796513633224,
      "id": "3aa_E",
      "input_sha256": "a8c7177d89573587de4ce53510b5ced362f30288c47addc65fde212f90a5afec",
      "job_dir": "docs/verification/group_4/paper_3235db287859287e/hpc_runs/3aa_Z_author_exact_route_optfreq_hpc20_p3",
      "minimum_validation": {
        "frequency_count": 105,
        "imaginary_frequency_count": 0,
        "normal_termination": true,
        "optimization_completed": true,
        "vibrational_analysis": true
      },
      "stdout_sha256": "f7a0c790c01ac478660e1860b0f89b55f10d3814a472e81936c9965736721818"
    }
  ],
  "protocol": {
    "energy_convention": "Sum of electronic and thermal free energy at 298.15 K and 1 atm",
    "method": "Gaussian 16 M06-2X/Gen; C,H 6-31G; O,S 6-311G(d,p); Opt=(Tight,MaxCycles=300) Freq; SMD(MeCN)",
    "rationale": "Exact author route recovered from SI; only the two evaluator-defined neutral singlet E/Z objects were calculated. The ETKDG coordinate export had an inverted file-to-configuration annotation; optimized dihedral checks therefore associate the cis output with authoritative 3aa_Z and trans output with authoritative 3aa_E. Raw inputs and this reconciliation are retained.",
    "solvent_or_environment": "SMD acetonitrile",
    "temperature_K": 298.15
  },
  "status": "complete"
}
```

Paper/SI document hashes:

- `papers/paper_3235db287859287e/documents/main.pdf` — SHA-256 `2e417419fc4e482fb87a3a8545ab10eba95d2cbff12baa254e30fbbe3cef1925` (declared_match=True)
- `papers/paper_3235db287859287e/documents/supplementary_001.pdf` — SHA-256 `4946aeb29d0288c3c0e7b788fe6bd3c51c121b1463b4353ad3a764d10ca53341` (declared_match=True)

Report evidence lines retained:

- > 作者/SI 模型下的真实 Gaussian Opt/Freq、构型核验、Gibbs 比较和逐条资格审计；完整
- Opt/Freq 完成、零虚频和 E/Z 构型检查后写入 `report/results.json`、科学闭环及
- stereoisomer 均完成 Opt/Freq、零虚频和自由能解析前，不作论文结论。
- Gaussian/evaluator 科学闭环，不能据此授权 PASS；提交与输入哈希见
- block or `Normal termination`; it is not scientific evidence. The complete output and 1.8-GB core
- Both have complete optimization, full harmonic frequencies and zero imaginary modes.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **60**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/status.json` — successful status record; SHA-256 `fefa4f88c26361e48cea866fbe228ca0e45c55d5238332bc92d38e409bcc9536`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/3aa_E_optfreq_retry2_parsed.json` — successful execution artifact; SHA-256 `5b8c6910117dc85da5e626db6a0e9b56e5358fcab7bcbfc9a6d42156c6576ea5`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/collection.json` — successful execution artifact; SHA-256 `06048f1ef15671d9a68151e36efffefe35b4021b8ed7661a20b954803ce5ae61`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/input.com` — successful execution artifact; SHA-256 `388ebc460a566ba9da8bfbe280f0fa86035e67811d63e8e5f27bdc6b2de0f5df`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/status.json` — successful status record; SHA-256 `0798b32aac1e1b733141fd4d8dc607ccf4dc7b105fd510f61c18752e10021999`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/3aa_E_optfreq_routefix_parsed.json` — successful execution artifact; SHA-256 `49c4557e490ed86ca40a5f0592085f6d1cba4b29667cc16e6f0edf81fdf68d08`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/collection.json` — successful execution artifact; SHA-256 `bb3e0f181193907e3e8a9474008d4dc2d2f164c2f252d618ffd0071e162d6bb3`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/input.com` — successful execution artifact; SHA-256 `4e1b6bcf8cd199c66470f86fd21083e666dce3143916943423e3599e44f418fa`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/status.json` — successful status record; SHA-256 `0510b6e125b46d84c816b572cbce6b4f2b2ebd6f33339ea3e9f5c504f08c9752`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/3aa_Z_optfreq_retry2_parsed.json` — successful execution artifact; SHA-256 `a5e9ae10fc5b954657849f5a44015559a959ff76f2ccc9fb66348d1dec8009a9`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/collection.json` — successful execution artifact; SHA-256 `baa52546d27aae55bdbf94082e08450a13bd8b7fa4c921c7778ed09dc723b0f1`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/input.com` — successful execution artifact; SHA-256 `2689a5fe0fd68403301e6ce4322bf9b361b08152776304aa6fe368758967f85d`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/status.json` — successful status record; SHA-256 `d58df330ac7968355b15f601b3fadaef170139deba7bf83af34f842e89c12d08`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/3aa_Z_optfreq_retry2__segfault_retry1_parsed.json` — successful execution artifact; SHA-256 `e4b796d34215ff0bcccac78844586d2ae84ab10f73ba9ee7e4a7480d140f1f4b`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/collection.json` — successful execution artifact; SHA-256 `65347c53902b0615ceb0087a0eebf894ef5b2cef2558c76db5bfd051428f12c9`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/input.com` — successful execution artifact; SHA-256 `2689a5fe0fd68403301e6ce4322bf9b361b08152776304aa6fe368758967f85d`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/status.json` — successful status record; SHA-256 `3f580468d6794826fad62164760c457a6e7dbf7840cb8cc5c92d437d053e048a`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/3aa_Z_optfreq_routefix_parsed.json` — successful execution artifact; SHA-256 `d1db9121dfc565a82d2afd509257cbcdcf9055881b2d237f4e35a4dc04a56f49`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/collection.json` — successful execution artifact; SHA-256 `f0bbe0cc803b429a3b446fe63875145d8c0a856e706b540af06587bf08944d1b`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/input.com` — successful execution artifact; SHA-256 `4574c3f8fb427d5046bc279500d94bbbf8f335bec9c70c5c02557d6af4937a14`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/status.json` — successful status record; SHA-256 `81f873316be2009d657a666904103cca1459e7c3b4c10d80b10756d3f5feb34b`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/3aa_Z_optfreq_routefix__segfault_retry1_parsed.json` — successful execution artifact; SHA-256 `83b96a561d198b4c3b3d881d6711c6ea715755223cce9f20fa6c628793fb8f28`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/collection.json` — successful execution artifact; SHA-256 `a9cf31a6256a0e76e444054bce960f8e3e8b98bd0892d7125a8024e3944e6f02`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/input.com` — successful execution artifact; SHA-256 `4574c3f8fb427d5046bc279500d94bbbf8f335bec9c70c5c02557d6af4937a14`
- `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_1088c7eded184452bbf1f84fad803447/status.json` — successful status record; SHA-256 `3f580468d6794826fad62164760c457a6e7dbf7840cb8cc5c92d437d053e048a`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_1088c7eded184452bbf1f84fad803447/collection.json` — successful execution artifact; SHA-256 `f0bbe0cc803b429a3b446fe63875145d8c0a856e706b540af06587bf08944d1b`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_1088c7eded184452bbf1f84fad803447/input.com` — successful execution artifact; SHA-256 `4574c3f8fb427d5046bc279500d94bbbf8f335bec9c70c5c02557d6af4937a14`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_1088c7eded184452bbf1f84fad803447/request.json` — successful execution artifact; SHA-256 `4775b93874df0837d67ad203b1c2f20959abf5aba59c85fa87a0a894b3969974`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_1088c7eded184452bbf1f84fad803447/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_13240aaa9ebf4cf8b40003bee06b6a73/status.json` — successful status record; SHA-256 `81f873316be2009d657a666904103cca1459e7c3b4c10d80b10756d3f5feb34b`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_13240aaa9ebf4cf8b40003bee06b6a73/collection.json` — successful execution artifact; SHA-256 `a9cf31a6256a0e76e444054bce960f8e3e8b98bd0892d7125a8024e3944e6f02`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_13240aaa9ebf4cf8b40003bee06b6a73/input.com` — successful execution artifact; SHA-256 `4574c3f8fb427d5046bc279500d94bbbf8f335bec9c70c5c02557d6af4937a14`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_13240aaa9ebf4cf8b40003bee06b6a73/request.json` — successful execution artifact; SHA-256 `9dea4414369bf6e90a2bcc24e42f409847a7bfd39a1bfe50d092c572cd36ceb0`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_13240aaa9ebf4cf8b40003bee06b6a73/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_312374af4268409eb5e57912055a3de5/status.json` — successful status record; SHA-256 `0510b6e125b46d84c816b572cbce6b4f2b2ebd6f33339ea3e9f5c504f08c9752`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_312374af4268409eb5e57912055a3de5/collection.json` — successful execution artifact; SHA-256 `baa52546d27aae55bdbf94082e08450a13bd8b7fa4c921c7778ed09dc723b0f1`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_312374af4268409eb5e57912055a3de5/input.com` — successful execution artifact; SHA-256 `2689a5fe0fd68403301e6ce4322bf9b361b08152776304aa6fe368758967f85d`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_312374af4268409eb5e57912055a3de5/request.json` — successful execution artifact; SHA-256 `b1458aff8f3eb15c0686e0553a85276a838fae464f077ad306185dff211409d4`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_312374af4268409eb5e57912055a3de5/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_899b0f99e0224b2590494831e9fa7c6c/status.json` — successful status record; SHA-256 `d58df330ac7968355b15f601b3fadaef170139deba7bf83af34f842e89c12d08`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_899b0f99e0224b2590494831e9fa7c6c/collection.json` — successful execution artifact; SHA-256 `65347c53902b0615ceb0087a0eebf894ef5b2cef2558c76db5bfd051428f12c9`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_899b0f99e0224b2590494831e9fa7c6c/input.com` — successful execution artifact; SHA-256 `2689a5fe0fd68403301e6ce4322bf9b361b08152776304aa6fe368758967f85d`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_899b0f99e0224b2590494831e9fa7c6c/request.json` — successful execution artifact; SHA-256 `5d9b04aebdc195ee09f28b0cd25d3de3dbc60721e5f98484353bfc9e8723b422`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_899b0f99e0224b2590494831e9fa7c6c/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_a9c1613615bd49d6b1a6e5bdfe2c836f/status.json` — successful status record; SHA-256 `fefa4f88c26361e48cea866fbe228ca0e45c55d5238332bc92d38e409bcc9536`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_a9c1613615bd49d6b1a6e5bdfe2c836f/collection.json` — successful execution artifact; SHA-256 `06048f1ef15671d9a68151e36efffefe35b4021b8ed7661a20b954803ce5ae61`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_a9c1613615bd49d6b1a6e5bdfe2c836f/input.com` — successful execution artifact; SHA-256 `388ebc460a566ba9da8bfbe280f0fa86035e67811d63e8e5f27bdc6b2de0f5df`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_a9c1613615bd49d6b1a6e5bdfe2c836f/request.json` — successful execution artifact; SHA-256 `45d09657b3a44d89b999f455601a44f50cebc3ccce46402f15eb6b333de455b0`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_a9c1613615bd49d6b1a6e5bdfe2c836f/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_d84f784ec29643f38e89cc1eb55db0d9/status.json` — successful status record; SHA-256 `0798b32aac1e1b733141fd4d8dc607ccf4dc7b105fd510f61c18752e10021999`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_d84f784ec29643f38e89cc1eb55db0d9/collection.json` — successful execution artifact; SHA-256 `bb3e0f181193907e3e8a9474008d4dc2d2f164c2f252d618ffd0071e162d6bb3`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_d84f784ec29643f38e89cc1eb55db0d9/input.com` — successful execution artifact; SHA-256 `4e1b6bcf8cd199c66470f86fd21083e666dce3143916943423e3599e44f418fa`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_d84f784ec29643f38e89cc1eb55db0d9/request.json` — successful execution artifact; SHA-256 `ba261ae4925e5b1813202ae2e33d8ad1eaa5c18bb8620405a3d58adad7340437`
- `docs/verification/group_4/paper_3235db287859287e/native_workspace_batch/outputs/execution_jobs/job_d84f784ec29643f38e89cc1eb55db0d9/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/3aa_Z_optfreq_retry2/status.json` — label=group_4 paper_3235db287859287e 3aa_Z_optfreq_retry2; submitted_at=2026-08-29T16:30:25.192996+00:00; software=gaussian; intent=optimization_frequency; route=#p M062X/6-311+G(d,p) Opt=(Tight,MaxCycles=200) Freq SCRF=(SMD,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/3aa_Z_optfreq_retry2.chk`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/3aa_Z_optfreq_retry2_parsed.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/collection.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/input.com`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/stderr.log`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2/stdout.log`
2. `artifacts/gaussian_batch/3aa_E_optfreq_retry2/status.json` — label=group_4 paper_3235db287859287e 3aa_E_optfreq_retry2; submitted_at=2026-08-29T16:30:25.264923+00:00; software=gaussian; intent=optimization_frequency; route=#p M062X/6-311+G(d,p) Opt=(Tight,MaxCycles=200) Freq SCRF=(SMD,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/3aa_E_optfreq_retry2.chk`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/3aa_E_optfreq_retry2_parsed.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/collection.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/input.com`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/stderr.log`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_retry2/stdout.log`
3. `artifacts/gaussian_batch/3aa_Z_optfreq_routefix/status.json` — label=group_4 paper_3235db287859287e 3aa_Z_optfreq_routefix; submitted_at=2026-08-29T19:37:26.525582+00:00; software=gaussian; intent=optimization_frequency; route=#p M062X/6-311+G(d,p) Opt=(Tight,MaxCycles=200) Freq SCRF=(SMD,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/3aa_Z_optfreq_routefix.chk`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/3aa_Z_optfreq_routefix_parsed.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/collection.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/input.com`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/stderr.log`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix/stdout.log`
4. `artifacts/gaussian_batch/3aa_E_optfreq_routefix/status.json` — label=group_4 paper_3235db287859287e 3aa_E_optfreq_routefix; submitted_at=2026-08-29T19:37:26.683966+00:00; software=gaussian; intent=optimization_frequency; route=#p M062X/6-311+G(d,p) Opt=(Tight,MaxCycles=200) Freq SCRF=(SMD,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/3aa_E_optfreq_routefix.chk`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/3aa_E_optfreq_routefix_parsed.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/collection.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/input.com`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/stderr.log`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_E_optfreq_routefix/stdout.log`
5. `artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/status.json` — label=group_4 paper_3235db287859287e 3aa_Z_optfreq_retry2__segfault_retry1; submitted_at=2026-08-31T20:00:50.467982+00:00; software=gaussian; intent=optimization_frequency; route=#p M062X/6-311+G(d,p) Opt=(Tight,MaxCycles=200) Freq SCRF=(SMD,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/3aa_Z_optfreq_retry2.chk`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/3aa_Z_optfreq_retry2__segfault_retry1_parsed.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/collection.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/input.com`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/stderr.log`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_retry2__segfault_retry1/stdout.log`
6. `artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/status.json` — label=group_4 paper_3235db287859287e 3aa_Z_optfreq_routefix__segfault_retry1; submitted_at=2026-08-31T20:00:51.646100+00:00; software=gaussian; intent=optimization_frequency; route=#p M062X/6-311+G(d,p) Opt=(Tight,MaxCycles=200) Freq SCRF=(SMD,Solvent=Acetonitrile) NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/3aa_Z_optfreq_routefix.chk`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/3aa_Z_optfreq_routefix__segfault_retry1_parsed.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/collection.json`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/input.com`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/stderr.log`
   - output: `docs/verification/group_4/paper_3235db287859287e/artifacts/gaussian_batch/3aa_Z_optfreq_routefix__segfault_retry1/stdout.log`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `c_limitation`, `r_limit`.

- Key-point IDs: `kp_process_minima, kp_process_common_protocol, kp_result_signed_difference`
- Conclusion IDs: `c_final_preference, c_limitation`
- Scoring-rule IDs: `r_kp_process_minima, r_kp_protocol, r_kp_difference, r_final, r_limit`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_kp_process_minima` → reference `kp_process_minima`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_kp_protocol` → reference `kp_process_common_protocol`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_kp_difference` → reference `kp_result_signed_difference`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=absolute difference; evaluator_target_present=False
- rule `r_final` → reference `c_final_preference`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_limit` → reference `c_limitation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_kp_process_minima` / reference `kp_process_minima` / field `$.objects[*].connectivity_verified` / result path `$.objects[*].connectivity_verified` = `true`
- rule `r_kp_process_minima` / reference `kp_process_minima` / field `$.objects[*].minimum_validation` / result path `$.objects[*].minimum_validation.vibrational_analysis` = `true`
- rule `r_kp_process_minima` / reference `kp_process_minima` / field `$.objects[*].minimum_validation` / result path `$.objects[*].minimum_validation.imaginary_frequency_count` = `0`
- rule `r_kp_process_minima` / reference `kp_process_minima` / field `$.objects[*].minimum_validation` / result path `$.objects[*].minimum_validation.frequency_count` = `105`
- rule `r_kp_process_minima` / reference `kp_process_minima` / field `$.objects[*].minimum_validation` / result path `$.objects[*].minimum_validation.optimization_completed` = `true`
- rule `r_kp_process_minima` / reference `kp_process_minima` / field `$.objects[*].minimum_validation` / result path `$.objects[*].minimum_validation.normal_termination` = `true`
- rule `r_kp_protocol` / reference `kp_process_common_protocol` / field `$.protocol` / result path `$.protocol.method` = `"Gaussian 16 M06-2X/Gen; C,H 6-31G; O,S 6-311G(d,p); Opt=(Tight,MaxCycles=300) Freq; SMD(MeCN)"`
- rule `r_kp_protocol` / reference `kp_process_common_protocol` / field `$.protocol` / result path `$.protocol.temperature_K` = `298.15`
- rule `r_kp_protocol` / reference `kp_process_common_protocol` / field `$.protocol` / result path `$.protocol.solvent_or_environment` = `"SMD acetonitrile"`
- rule `r_kp_protocol` / reference `kp_process_common_protocol` / field `$.protocol` / result path `$.protocol.energy_convention` = `"Sum of electronic and thermal free energy at 298.15 K and 1 atm"`
- rule `r_kp_protocol` / reference `kp_process_common_protocol` / field `$.protocol` / result path `$.protocol.rationale` = `"Exact author route recovered from SI; only the two evaluator-defined neutral singlet E/Z objects were calculated. The ETKDG coordinate export had an inverted file-to-configuration annotation; optimized dihedral checks therefore associate..."`
- rule `r_kp_difference` / reference `kp_result_signed_difference` / field `$.comparison.delta_G_E_minus_Z_kcal_mol` / result path `$.comparison.delta_G_E_minus_Z_kcal_mol` = `1.6327796513633224`
- rule `r_final` / reference `c_final_preference` / field `$.status` / result path `$.status` = `"complete"`
- rule `r_final` / reference `c_final_preference` / field `$.comparison` / result path `$.comparison.favored_object` = `"3aa_Z"`
- rule `r_final` / reference `c_final_preference` / field `$.comparison` / result path `$.comparison.basis` = `"Difference of exact mixed-basis M06-2X/Gen SMD(MeCN) 298 K thermal Gibbs energies."`
- rule `r_limit` / reference `c_limitation` / field `$.limitations` / result path `$.limitations` = `"Single conformer per named stereoisomer; comparison is limited to the evaluator scientific question and does not establish a global conformer ensemble or kinetics."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Authoritative structure, configuration, charge, and multiplicity definitions for 3aa_Z and 3aa_E.

Public input files and hashes:

- `agent_input/data/inputs/3aa_stereoisomers.json` — SHA-256 `1ffa941e76aef470e93498208de61fd33c1821e4dd7ab7aeabafd4a7b5dd6f47`; size=633 bytes; explicit_boundary_fields={"$.charge": 0, "$.formula": "C17H16O3S", "$.multiplicity": 1, "$.stereoisomers[0].isomeric_smiles": "COC(=O)/C(=C\\c1ccccc1)C[S](=O)c1ccccc1", "$.stereoisomers[1].isomeric_smiles": "COC(=O)/C(=C/c1ccccc1)C[S](=O)c1ccccc1"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_4/paper_3235db287859287e/verification_report.md` — verification record; SHA-256 `461f9b8e9508d695f16d595d2590db0649ca1890169617ffe354a46c95c7004a`
- `docs/verification/group_4/paper_3235db287859287e/report/results.json` — verification record; SHA-256 `011d2a98370f60bf6d91fe3bdbfd48be93bed94cdd64b8f5b508c50137d0b5d3`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
