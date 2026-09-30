# Verified computation reference — paper_3e4cad1d1d650d0c (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 6 | `PASS` | - 论文复现结论：`PASS`。两个体系均真实完成同一 CAM-B3LYP/6-311G(d)/CPCM(DMSO) Gaussian Opt/Freq，正常终止、优化收敛且 NImag=0；HOMO 数值和空间归属共同支持取代基调控结论。 |
| 7 | `PASS` | - 评估任务对照：`MATCH`；评估任务资格：`QUALIFIED`。该资格不是由科学 PASS 自动推断，而是由 `provenance/evaluation_task_qualification.json` 对全部 key point、scoring rule、reference conclusion、critical failure 和 evidence map 逐项核对后授权。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: A Rational Approach to Super-Reducing Organophotocatalysts from Fluorene Derivatives
- DOI: `10.1021/acscatal.5c06048`
- Task package: `tasks/final_verified_autonomous_research/paper_3e4cad1d1d650d0c`
- Verification group: `docs/verification/group_4/paper_3e4cad1d1d650d0c`
- Paper documents: `papers/paper_3e4cad1d1d650d0c`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": {
    "difference_eV": -0.14830204852249995,
    "statement": "The computed HOMO changes by -0.1483 eV (1e_anion minus 1a_anion). Both optimized anions are harmonic minima and both HOMOs are predominantly fluorenyl by the declared AO-coefficient diagnostic, so substituent-dependent tuning is observed."
  },
  "reproducibility": {
    "limitations": "One independently generated starting conformer per anion; Kohn-Sham HOMO energies and non-orthogonalized coefficient fractions are method dependent.",
    "settings": "CAM-B3LYP/6-311G(d), CPCM(DMSO), NoSymm, Pop=Full, SCF=(XQC,MaxCycle=512), Opt(Tight,MaxCycles=200)+Freq, charge -1 singlets.",
    "software_version": "Gaussian 16 C.01"
  },
  "status": "complete",
  "systems": [
    {
      "geometry": {
        "optimization_status": "normal Gaussian termination; Opt completed; harmonic minimum with NImag=0",
        "provenance": "artifacts/structures/smiles_001_0330c2e780.xyz; ETKDGv3 followed by MMFF94s/UFF preoptimization"
      },
      "homo_energy_eV": -4.9233558970965,
      "homo_localization": {
        "anionic_center_fraction": 0.29273675365044743,
        "diagnostic": "normalized squared AO coefficients from Gaussian Pop=Full; qualitative, non-orthogonalized",
        "fluorenyl_fraction": 0.8436898184934789,
        "pendant_aryl_fraction": 0.1563101815065211
      },
      "id": "1a_anion",
      "method": {
        "basis": "6-311G(d)",
        "charge": -1,
        "method": "CAM-B3LYP",
        "multiplicity": 1,
        "software": "Gaussian 16 C.01 native",
        "solvation": "CPCM DMSO"
      },
      "status": "complete",
      "validation": {
        "evidence": "{\"duration_seconds\": 59363.643327, \"frequency_count\": 90, \"imaginary_frequency_count\": 0, \"input_sha256\": \"3aff125bd97d72806aaea1e388ce9c2df41a916fb451293621fbdfb49b98ad46\", \"job_id\": \"job_aaaa1b7f21df4d4ca2065f76d6973e60\", \"normal_termination\": true, \"optimization_completed\": true, \"stdout_sha256\": \"a20b55a351627d4de11d5e94c0b6f92638ddfcf25dbb1db03bc20e747bdf3234\", \"walltime_seconds\": null}",
        "frequency_method": "Gaussian harmonic Freq after CAM-B3LYP/6-311G(d) CPCM(DMSO) Opt(Tight)",
        "imaginary_modes": 0
      }
    },
    {
      "geometry": {
        "optimization_status": "normal Gaussian termination; Opt completed; harmonic minimum with NImag=0",
        "provenance": "artifacts/structures/smiles_002_694d45e808.xyz; ETKDGv3 followed by MMFF94s/UFF preoptimization"
      },
      "homo_energy_eV": -5.071657945619,
      "homo_localization": {
        "anionic_center_fraction": 0.28908007451223483,
        "diagnostic": "normalized squared AO coefficients from Gaussian Pop=Full; qualitative, non-orthogonalized",
        "fluorenyl_fraction": 0.809233640210016,
        "pendant_aryl_fraction": 0.19076635978998385
      },
      "id": "1e_anion",
      "method": {
        "basis": "6-311G(d)",
        "charge": -1,
        "method": "CAM-B3LYP",
        "multiplicity": 1,
        "software": "Gaussian 16 C.01 native",
        "solvation": "CPCM DMSO"
      },
      "status": "complete",
      "validation": {
        "evidence": "{\"duration_seconds\": 86771.642078, \"frequency_count\": 99, \"imaginary_frequency_count\": 0, \"input_sha256\": \"ba3a029046a2c7e9382a55c5e282dda4127b147c32a8fa4460e9a2110f04c7ad\", \"job_id\": \"job_e1cd29c9de08415c9ddb640e1c9ca07d\", \"normal_termination\": true, \"optimization_completed\": true, \"stdout_sha256\": \"4d752a964b264c76378e52640688e965e6a7b59a7d9522160f71ef4430fb7118\", \"walltime_seconds\": null}",
        "frequency_method": "Gaussian harmonic Freq after CAM-B3LYP/6-311G(d) CPCM(DMSO) Opt(Tight)",
        "imaginary_modes": 0
      }
    }
  ]
}
```

Paper/SI document hashes:

- `papers/paper_3e4cad1d1d650d0c/documents/supplementary_001.pdf` — SHA-256 `674c2d21b7a260c23cc55a07bb394e8e67f19d18ddf217229fe5080352fe8810` (declared_match=True)
- `papers/paper_3e4cad1d1d650d0c/documents/main.pdf` — SHA-256 `ea79927bb71341d55d64f9a60c4ef6d5904528fc3f91a1ef221313c29e171094` (declared_match=True)

Report evidence lines retained:

- - 论文复现结论：`PASS`。两个体系均真实完成同一 CAM-B3LYP/6-311G(d)/CPCM(DMSO) Gaussian Opt/Freq，正常终止、优化收敛且 NImag=0；HOMO 数值和空间归属共同支持取代基调控结论。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **20**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/status.json` — successful status record; SHA-256 `627afab948b0df934dfc5185998ac9223a806e5cf7ace311f6ce9a756a7d38f1`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/1a_anion_optfreq_parsed.json` — successful execution artifact; SHA-256 `df3dc4ba2bf980942d50886c4799c57e6b8184d51d42fbc92fcffee9a7edccfa`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/collection.json` — successful execution artifact; SHA-256 `e11d5f4be353e8f76e5b45e121edbc09d02d22f7427d604bf3fa34e4f8656a5a`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/input.com` — successful execution artifact; SHA-256 `3aff125bd97d72806aaea1e388ce9c2df41a916fb451293621fbdfb49b98ad46`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/status.json` — successful status record; SHA-256 `2391cde10f479fcac3b8e21e7107147a16c6b0e5eb9f28329193eb95c64c559b`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/1e_anion_optfreq_parsed.json` — successful execution artifact; SHA-256 `a91bf1dd548911d6021b795a8bb4017fff7a7eaa7ba1e51d35e02b2dc091ba9c`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/collection.json` — successful execution artifact; SHA-256 `e09643f81b056f23318f8dbd393623dafac0880c33f0a20b620b2bbe9a38c64e`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/input.com` — successful execution artifact; SHA-256 `ba3a029046a2c7e9382a55c5e282dda4127b147c32a8fa4460e9a2110f04c7ad`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/native_workspace_batch/outputs/execution_jobs/job_aaaa1b7f21df4d4ca2065f76d6973e60/status.json` — successful status record; SHA-256 `627afab948b0df934dfc5185998ac9223a806e5cf7ace311f6ce9a756a7d38f1`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/native_workspace_batch/outputs/execution_jobs/job_aaaa1b7f21df4d4ca2065f76d6973e60/collection.json` — successful execution artifact; SHA-256 `e11d5f4be353e8f76e5b45e121edbc09d02d22f7427d604bf3fa34e4f8656a5a`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/native_workspace_batch/outputs/execution_jobs/job_aaaa1b7f21df4d4ca2065f76d6973e60/input.com` — successful execution artifact; SHA-256 `3aff125bd97d72806aaea1e388ce9c2df41a916fb451293621fbdfb49b98ad46`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/native_workspace_batch/outputs/execution_jobs/job_aaaa1b7f21df4d4ca2065f76d6973e60/request.json` — successful execution artifact; SHA-256 `a210199ffcfa58368639d34f4d4887e8761daca610e283fb2689a671505f1c73`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/native_workspace_batch/outputs/execution_jobs/job_aaaa1b7f21df4d4ca2065f76d6973e60/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/native_workspace_batch/outputs/execution_jobs/job_e1cd29c9de08415c9ddb640e1c9ca07d/status.json` — successful status record; SHA-256 `2391cde10f479fcac3b8e21e7107147a16c6b0e5eb9f28329193eb95c64c559b`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/native_workspace_batch/outputs/execution_jobs/job_e1cd29c9de08415c9ddb640e1c9ca07d/collection.json` — successful execution artifact; SHA-256 `e09643f81b056f23318f8dbd393623dafac0880c33f0a20b620b2bbe9a38c64e`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/native_workspace_batch/outputs/execution_jobs/job_e1cd29c9de08415c9ddb640e1c9ca07d/input.com` — successful execution artifact; SHA-256 `ba3a029046a2c7e9382a55c5e282dda4127b147c32a8fa4460e9a2110f04c7ad`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/native_workspace_batch/outputs/execution_jobs/job_e1cd29c9de08415c9ddb640e1c9ca07d/request.json` — successful execution artifact; SHA-256 `0aac2c0ce1ed793ac17e3bd5651ff0964ecf6e2969341b9d7e1a91021812027b`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/native_workspace_batch/outputs/execution_jobs/job_e1cd29c9de08415c9ddb640e1c9ca07d/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/1a_anion_optfreq/status.json` — label=group_4 paper_3e4cad1d1d650d0c 1a_anion_optfreq; submitted_at=2026-08-29T16:02:22.869275+00:00; software=gaussian; intent=optimization_frequency; route=#p CAM-B3LYP/6-311G(d) Opt=(Tight,MaxCycles=200) Freq Pop=Full NoSymm SCRF=(CPCM,Solvent=DMSO) SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/1a_anion_optfreq.chk`
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/1a_anion_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/input.com`
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1a_anion_optfreq/stdout.log`
2. `artifacts/gaussian_batch/1e_anion_optfreq/status.json` — label=group_4 paper_3e4cad1d1d650d0c 1e_anion_optfreq; submitted_at=2026-08-29T16:02:22.919099+00:00; software=gaussian; intent=optimization_frequency; route=#p CAM-B3LYP/6-311G(d) Opt=(Tight,MaxCycles=200) Freq Pop=Full NoSymm SCRF=(CPCM,Solvent=DMSO) SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/1e_anion_optfreq.chk`
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/1e_anion_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/input.com`
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/gaussian_batch/1e_anion_optfreq/stdout.log`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `con_ar_limitation`, `r_ar_limit`.

- Key-point IDs: `kp_ar_process_identity, kp_ar_process_minimum, kp_ar_result_A, kp_ar_result_B`
- Conclusion IDs: `con_ar_final, con_ar_limitation`
- Scoring-rule IDs: `r_ar_identity, r_ar_minimum, r_ar_A, r_ar_B, r_ar_final, r_ar_limit`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_ar_identity` → reference `kp_ar_process_identity`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert scientific verification; evaluator_target_present=False
- rule `r_ar_minimum` → reference `kp_ar_process_minimum`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert scientific verification; evaluator_target_present=False
- rule `r_ar_A` → reference `kp_ar_result_A`; type=numeric; unit=eV; tolerance=0.3; comparison=absolute difference; evaluator_target_present=True
- rule `r_ar_B` → reference `kp_ar_result_B`; type=numeric; unit=eV; tolerance=0.3; comparison=absolute difference; evaluator_target_present=True
- rule `r_ar_final` → reference `con_ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_limit` → reference `con_ar_limitation`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_ar_A` / reference `kp_ar_result_A`: target=-5.03 eV; tolerance=0.3; numeric result leaves=[-4.9233558970965]; within_tolerance=True; applicability=applicable
- rule `r_ar_B` / reference `kp_ar_result_B`: target=-5.18 eV; tolerance=0.3; numeric result leaves=[-5.071657945619]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].id` = `"1a_anion"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].homo_energy_eV` = `-4.9233558970965`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].homo_localization.diagnostic` = `"normalized squared AO coefficients from Gaussian Pop=Full; qualitative, non-orthogonalized"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].homo_localization.fluorenyl_fraction` = `0.8436898184934789`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].homo_localization.pendant_aryl_fraction` = `0.1563101815065211`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].homo_localization.anionic_center_fraction` = `0.29273675365044743`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].validation.frequency_method` = `"Gaussian harmonic Freq after CAM-B3LYP/6-311G(d) CPCM(DMSO) Opt(Tight)"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].validation.imaginary_modes` = `0`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].validation.evidence` = `"{\"duration_seconds\": 59363.643327, \"frequency_count\": 90, \"imaginary_frequency_count\": 0, \"input_sha256\": \"3aff125bd97d72806aaea1e388ce9c2df41a916fb451293621fbdfb49b98ad46\", \"job_id\": \"job_aaaa1b7f21df4d4ca2065f76d6973e60\", \"normal_termi..."`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].status` = `"complete"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].method.software` = `"Gaussian 16 C.01 native"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].method.method` = `"CAM-B3LYP"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].method.basis` = `"6-311G(d)"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].method.solvation` = `"CPCM DMSO"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].method.charge` = `-1`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].method.multiplicity` = `1`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].geometry.provenance` = `"artifacts/structures/smiles_001_0330c2e780.xyz; ETKDGv3 followed by MMFF94s/UFF preoptimization"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[0].geometry.optimization_status` = `"normal Gaussian termination; Opt completed; harmonic minimum with NImag=0"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].id` = `"1e_anion"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].homo_energy_eV` = `-5.071657945619`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].homo_localization.diagnostic` = `"normalized squared AO coefficients from Gaussian Pop=Full; qualitative, non-orthogonalized"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].homo_localization.fluorenyl_fraction` = `0.809233640210016`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].homo_localization.pendant_aryl_fraction` = `0.19076635978998385`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].homo_localization.anionic_center_fraction` = `0.28908007451223483`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].validation.frequency_method` = `"Gaussian harmonic Freq after CAM-B3LYP/6-311G(d) CPCM(DMSO) Opt(Tight)"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].validation.imaginary_modes` = `0`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].validation.evidence` = `"{\"duration_seconds\": 86771.642078, \"frequency_count\": 99, \"imaginary_frequency_count\": 0, \"input_sha256\": \"ba3a029046a2c7e9382a55c5e282dda4127b147c32a8fa4460e9a2110f04c7ad\", \"job_id\": \"job_e1cd29c9de08415c9ddb640e1c9ca07d\", \"normal_termi..."`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].status` = `"complete"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].method.software` = `"Gaussian 16 C.01 native"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].method.method` = `"CAM-B3LYP"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].method.basis` = `"6-311G(d)"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].method.solvation` = `"CPCM DMSO"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].method.charge` = `-1`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].method.multiplicity` = `1`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].geometry.provenance` = `"artifacts/structures/smiles_002_694d45e808.xyz; ETKDGv3 followed by MMFF94s/UFF preoptimization"`
- rule `r_ar_identity` / reference `kp_ar_process_identity` / field `$.systems` / result path `$.systems[1].geometry.optimization_status` = `"normal Gaussian termination; Opt completed; harmonic minimum with NImag=0"`
- rule `r_ar_final` / reference `con_ar_final` / field `$.comparison.statement` / result path `$.comparison.statement` = `"The computed HOMO changes by -0.1483 eV (1e_anion minus 1a_anion). Both optimized anions are harmonic minima and both HOMOs are predominantly fluorenyl by the declared AO-coefficient diagnostic, so substituent-dependent tuning is observed."`
- rule `r_ar_limit` / reference `con_ar_limitation` / field `$.reproducibility.limitations` / result path `$.reproducibility.limitations` = `"One independently generated starting conformer per anion; Kohn-Sham HOMO energies and non-orthogonalized coefficient fractions are method dependent."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `none recorded`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Explicit SMILES, charge, multiplicity, and DMSO continuum boundary for the two named anions.

Public input files and hashes:

- `agent_input/data/inputs/system.json` — SHA-256 `63a681d9f7f1f8a13b3e62007f13ab5bfc2c0128fc1898d734605eef677c2883`; size=621 bytes; explicit_boundary_fields={"$.solvent_boundary": "DMSO continuum; solvent model and numerical implementation are to be selected and reported by the investigator.", "$.systems[0].charge": -1, "$.systems[0].multiplicity": 1, "$.systems[0].smiles": "[C-]1(c2ccccc2)c2ccccc2-c2ccccc21", "$.systems[1].charge": -1, "$.systems[1].multiplicity": 1, "$.systems[1].smiles": "[C-]1(c2ccc(C(F)(F)F)cc2)c2ccccc2-c2ccccc21"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_4/paper_3e4cad1d1d650d0c/verification_report.md` — verification record; SHA-256 `09cebf93ca90bd25149296b8ce2deb97a810df52a97d4b4ede52775958f07561`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/report/results.json` — verification record; SHA-256 `7e6cacf40e03b9f7356d8475a1373e9f18be87865e33ce8c45a5e57b1ed2513e`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/structures/smiles_001_0330c2e780.xyz` — referenced successful evidence; SHA-256 `af796edca245beeb464b9890089e93d81f7fe8174502069cbbd4052a9eb9a6c9`
- `docs/verification/group_4/paper_3e4cad1d1d650d0c/artifacts/structures/smiles_002_694d45e808.xyz` — referenced successful evidence; SHA-256 `602436ecd3267dd79ddf4c66c23f78c84bc7034819f65982372fd4645c4e0e43`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
