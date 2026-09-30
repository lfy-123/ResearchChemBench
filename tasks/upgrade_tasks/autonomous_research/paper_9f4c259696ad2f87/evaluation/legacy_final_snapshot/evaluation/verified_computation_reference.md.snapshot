# Verified computation reference — paper_9f4c259696ad2f87 (autonomous_research)

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
| 8 | `BLOCKED` | - 最终状态：**BLOCKED** |
| 118 | `QUALIFIED` | - Evaluator/task qualification: **`QUALIFIED`** |
| 127 | `PASS` | - 论文复现结论：`PASS` |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Benzoyl-Xanthenoxanthenes: Versatile Chromophores for Light-Engaging Applications
- DOI: `10.1002/anie.202523349`
- Task package: `tasks/final_verified_autonomous_research/paper_9f4c259696ad2f87`
- Verification group: `docs/verification/group_1/paper_9f4c259696ad2f87`
- Paper documents: `papers/paper_9f4c259696ad2f87`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "conclusion": "The archived TD-DFT calculation gives S1=2.2955 eV (540.11 nm, f=0.4108) with dominant 155->156 HOMO->LUMO character (97.91% coefficient-weight estimate). This supports the lowest-band HOMO-to-LUMO assignment within the supplied-geometry, PCM(CH2Cl2) scope.",
  "input_validation": {
    "atom_count": 74,
    "charge": 0,
    "formula": "C43H28O3",
    "geometry_validated": true,
    "multiplicity": 1
  },
  "limitations": "The supplied file is used as the optimized ground-state geometry; no conformer search or harmonic Hessian was performed. The transition percentage is derived from the printed Gaussian amplitude (2*c^2), and the result is a vertical single-geometry calculation.",
  "protocol": {
    "basis": "6-31G(d)",
    "excited_state_method": "TD(B3LYP), singlets, NStates=64",
    "geometry_strategy": "Use supplied 74-atom compound_1_optimized.xyz; validate identity and retain as the ground-state geometry (no reoptimization required by task)",
    "method": "B3LYP",
    "solvation": "PCM(CH2Cl2)"
  },
  "provenance": {
    "gaussian_log": "artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log",
    "gaussian_log_sha256": "a8769bf1de95537d8028e4afeff240a12ea6122a2ec0d878d8be69304043a4d5",
    "input_xyz": "tasks/paper_reproduction/paper_9f4c259696ad2f87/agent_input/data/inputs/compound_1_optimized.xyz",
    "input_xyz_sha256": "96e6df67736be8fb248c6b1a1f37841a74f280258b41a972b89f89962090389f"
  },
  "results": {
    "coefficient_amplitude": 0.69968,
    "dominant_contribution_percent": 97.91,
    "dominant_transition": "155->156 (HOMO->LUMO)",
    "s1_energy_eV": 2.2955,
    "s1_oscillator_strength": 0.4108,
    "s1_wavelength_nm": 540.11,
    "state": 1
  },
  "status": "complete",
  "validation_evidence": [
    "artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log",
    "Normal termination of Gaussian 16",
    "SCF cycles=1; final SCF=-1881.21706688 Eh",
    "Supplied XYZ identity: 74 atoms, C43H28O3, charge 0, singlet"
  ]
}
```

Paper/SI document hashes:

- `papers/paper_9f4c259696ad2f87/documents/main.pdf` — SHA-256 `592534cc448b295773af43b0783196ac34170f0e847fb7412d873e8a6e98c2ba` (declared_match=True)
- `papers/paper_9f4c259696ad2f87/documents/supplementary_001.pdf` — SHA-256 `f3436ca99f362b00e082f3bc28926ef30d56c7f4cfffaf92faa92708a24569ad` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **22**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/status.json` — successful status record; SHA-256 `2c18830efd6c388dc5cce8de6fceb9f444beb6a98451210dc8ffbeaf6247024a`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log` — successful execution artifact; SHA-256 `a8769bf1de95537d8028e4afeff240a12ea6122a2ec0d878d8be69304043a4d5`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/hpc_summary.json` — successful execution artifact; SHA-256 `8c3426a3adf83839ad86da64175e31f984f4605efb6a59d2018f753543266066`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/input.com` — successful execution artifact; SHA-256 `0eb02ba13cd6c22a8be1a19e082c314a098cc7d0716fff2feeea09e09e4f5e65`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/status.json` — successful status record; SHA-256 `87a5c7c2b7001be11a1fe78492a19982703e54d4ef05495fecf254e29c591562`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/collection.json` — successful execution artifact; SHA-256 `52ddc5b32066b6cf35ff9b2baf7a05bd0a13c3a9e42d2e3936a41ba94b061e50`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/input.com` — successful execution artifact; SHA-256 `81585e627802be2517eeccb0d18bf74a990352b63cd53e7a3d1f84d7afc08191`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/stdout.log` — successful execution artifact; SHA-256 `0be90be21b17c5439803e018fd92df07c19e4a66b53870d1991aaf51f6d053f2`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_b1c7ec4e60324285882357c92bbee8e8/status.json` — successful status record; SHA-256 `87a5c7c2b7001be11a1fe78492a19982703e54d4ef05495fecf254e29c591562`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_b1c7ec4e60324285882357c92bbee8e8/collection.json` — successful execution artifact; SHA-256 `52ddc5b32066b6cf35ff9b2baf7a05bd0a13c3a9e42d2e3936a41ba94b061e50`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_b1c7ec4e60324285882357c92bbee8e8/input.com` — successful execution artifact; SHA-256 `81585e627802be2517eeccb0d18bf74a990352b63cd53e7a3d1f84d7afc08191`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_b1c7ec4e60324285882357c92bbee8e8/request.json` — successful execution artifact; SHA-256 `ee302405d83cd69450c2e4ee569aba03f4d9534c771a5512891fd4ba8cb283a7`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_b1c7ec4e60324285882357c92bbee8e8/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/status.json` — successful status record; SHA-256 `36aec1f36ab9980fe1fd4a5976e8b2eae17943607c0172ae69e6421aa79bb1f8`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/collection.json` — successful execution artifact; SHA-256 `6e3326ffcef07edd558f4b072f88a2272290040610a1c7a1207f815ded855734`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/input.com` — successful execution artifact; SHA-256 `bfa3dd09bd316d10522b0d24b3d861fad48a425b39a6b851932b5cd724e41549`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/request.json` — successful execution artifact; SHA-256 `e4e3e7f8d975574577979c3e7cb65d114778ad8bbc7a6dfead285c8ce222242d`
- `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/status.json` — successful status record; SHA-256 `2c18830efd6c388dc5cce8de6fceb9f444beb6a98451210dc8ffbeaf6247024a`
- `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/gaussian.log` — successful execution artifact; SHA-256 `a8769bf1de95537d8028e4afeff240a12ea6122a2ec0d878d8be69304043a4d5`
- `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/input.com` — successful execution artifact; SHA-256 `0eb02ba13cd6c22a8be1a19e082c314a098cc7d0716fff2feeea09e09e4f5e65`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/status.json` — label=group_1 paper_9f4c259696ad2f87 xanthenoxanthene_b3lyp_optfreq unbounded_timeout_retry; submitted_at=2026-09-01T04:50:45.078724+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt=(CalcFC,MaxCycles=160) Freq NoSymm SCF=(XQC,MaxCycle=256); command=g16 < input.com
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/collection.json`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/fort.7`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/input.com`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/stderr.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/stdout.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/xanthenoxanthene_b3lyp_optfreq.chk`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/xanthenoxanthene_b3lyp_optfreq_unbounded_retry/xanthenoxanthene_b3lyp_optfreq_unbounded_retry_summary.json`
2. `native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/status.json` — label=paper_9f4c259696ad2f87 compound1_author_b3lyp_pcm_td64 unbounded_gaussian; submitted_at=2026-09-02T22:12:47.046607+00:00; software=gaussian; intent=single_point; route=#p B3LYP/6-31G(d) TD=(Singlets,NStates=64) SCRF=(PCM,Solvent=Dichloromethane) NoSymm Int=UltraFine SCF=(XQC,MaxCycle=512) Pop=Full; command=g16 < input.com
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/collection.json`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/compound1_author_b3lyp_pcm_td64.chk`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/fort.7`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/input.com`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/request.json`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/stderr.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/stdout.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/native_workspace_batch/outputs/execution_jobs/job_e2ee7db19e2b4c37af581a4fc14a3aef/supervisor_spec.json`
3. `artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/status.json` — label=artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/status.json
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/compound1_author_b3lyp_pcm_td64.chk`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/fort.7`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/hpc_summary.json`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/input.com`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/sha256sums.txt`
4. `provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/status.json` — label=provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/status.json
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/compound1_author_b3lyp_pcm_td64.chk`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/fort.7`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/gaussian.log`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/input.com`
   - output: `docs/verification/group_1/paper_9f4c259696ad2f87/provenance/qzcli_hpc/compound1_author_b3lyp_pcm_td64/hpc_20260902T112121Z_1315557/sha256sums.txt`

## Evaluator alignment

- Key-point IDs: `kp_ar_input, kp_ar_state, kp_ar_energy, kp_ar_character`
- Conclusion IDs: `c_ar_final`
- Scoring-rule IDs: `r_ar_input, r_ar_state, r_ar_energy, r_ar_character, r_ar_conclusion`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_ar_input` → reference `kp_ar_input`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_state` → reference `kp_ar_state`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_energy` → reference `kp_ar_energy`; type=numeric; unit=eV; tolerance=0.1; comparison=absolute difference; evaluator_target_present=True
- rule `r_ar_character` → reference `kp_ar_character`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ar_conclusion` → reference `c_ar_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_ar_energy` / reference `kp_ar_energy`: target=2.204 eV; tolerance=0.1; numeric result leaves=[2.2955]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_ar_input` / reference `kp_ar_input` / field `$.input_validation` / result path `$.input_validation.atom_count` = `74`
- rule `r_ar_input` / reference `kp_ar_input` / field `$.input_validation` / result path `$.input_validation.formula` = `"C43H28O3"`
- rule `r_ar_input` / reference `kp_ar_input` / field `$.input_validation` / result path `$.input_validation.charge` = `0`
- rule `r_ar_input` / reference `kp_ar_input` / field `$.input_validation` / result path `$.input_validation.multiplicity` = `1`
- rule `r_ar_input` / reference `kp_ar_input` / field `$.input_validation` / result path `$.input_validation.geometry_validated` = `true`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.protocol` / result path `$.protocol.method` = `"B3LYP"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.protocol` / result path `$.protocol.basis` = `"6-31G(d)"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.protocol` / result path `$.protocol.solvation` = `"PCM(CH2Cl2)"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.protocol` / result path `$.protocol.geometry_strategy` = `"Use supplied 74-atom compound_1_optimized.xyz; validate identity and retain as the ground-state geometry (no reoptimization required by task)"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.protocol` / result path `$.protocol.excited_state_method` = `"TD(B3LYP), singlets, NStates=64"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.validation_evidence` / result path `$.validation_evidence[0]` = `"artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.validation_evidence` / result path `$.validation_evidence[1]` = `"Normal termination of Gaussian 16"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.validation_evidence` / result path `$.validation_evidence[2]` = `"SCF cycles=1; final SCF=-1881.21706688 Eh"`
- rule `r_ar_state` / reference `kp_ar_state` / field `$.validation_evidence` / result path `$.validation_evidence[3]` = `"Supplied XYZ identity: 74 atoms, C43H28O3, charge 0, singlet"`
- rule `r_ar_energy` / reference `kp_ar_energy` / field `$.results.s1_energy_eV` / result path `$.results.s1_energy_eV` = `2.2955`
- rule `r_ar_character` / reference `kp_ar_character` / field `$.results.dominant_transition` / result path `$.results.dominant_transition` = `"155->156 (HOMO->LUMO)"`
- rule `r_ar_character` / reference `kp_ar_character` / field `$.results.dominant_contribution_percent` / result path `$.results.dominant_contribution_percent` = `97.91`
- rule `r_ar_conclusion` / reference `c_ar_final` / field `$.conclusion` / result path `$.conclusion` = `"The archived TD-DFT calculation gives S1=2.2955 eV (540.11 nm, f=0.4108) with dominant 155->156 HOMO->LUMO character (97.91% coefficient-weight estimate). This supports the lowest-band HOMO-to-LUMO assignment within the supplied-geometry..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized input leakage review
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Self-contained XYZ geometry for neutral singlet compound 1.

Public input files and hashes:

- `agent_input/data/inputs/compound_1_start.xyz` — SHA-256 `3bb3f780d1f81587d9364c23c3d066e6ea0b66b570089f6657bf079b11e5f0ca`; size=3217 bytes; xyz_atom_count=74; xyz_comment=Provided starting geometry of compound 1; neutral singlet; CH2Cl2 PCM; explicit_boundary_fields=not recorded

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_1/paper_9f4c259696ad2f87/verification_report.md` — verification record; SHA-256 `a72a6db7162258c06e61994f070aa4997990514d4cbe2f2dce7d3f91855d3eab`
- `docs/verification/group_1/paper_9f4c259696ad2f87/report/results.json` — verification record; SHA-256 `d011b88e731e9ce082cab5c0f7ba78f73563b56a981a61844ff660dca275ce78`
- `docs/verification/group_1/paper_9f4c259696ad2f87/artifacts/gaussian_batch/compound1_author_b3lyp_pcm_td64_hpc_6280c9ea/gaussian.log` — referenced successful evidence; SHA-256 `a8769bf1de95537d8028e4afeff240a12ea6122a2ec0d878d8be69304043a4d5`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
