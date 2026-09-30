# Verified computation reference — paper_9ec8c4761c4f171b (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `completed` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 93 | `QUALIFIED` | - 评估任务资格：`QUALIFIED`。 |
| 94 | `PASS` | - 最终状态：`PASS`。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: 5-(Trifluoromethyl)-4-biarylhydrazinylidenepyrazol-3-ones: synthesis, photophysical and biological properties
- DOI: `10.1016/j.dyepig.2025.113264`
- Task package: `tasks/final_verified_paper_reproduction/paper_9ec8c4761c4f171b`
- Verification group: `docs/verification/group_6/paper_9ec8c4761c4f171b`
- Paper documents: `papers/paper_9ec8c4761c4f171b`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "chloroform": {
    "gap_eV": 3.044,
    "homo_eV": -6.0749,
    "lumo_eV": -3.0309,
    "validation_evidence": "artifacts/native/6a_chcl3_optfreq_summary.json; status success/return 0; normal_termination=true; optimization_completed=true; imaginary_frequency_count=0; stdout SHA-256 65948ab4a98c0c8711760e9d8388f4b43c1c2b63cc1cd8221ec4ccb0ba1a2b02"
  },
  "comparison": {
    "absolute_deviation_eV": 0.624,
    "experimental_optical_gap_eV": 2.42,
    "interpretation": "The validated chloroform Kohn-Sham frontier gap is 3.044 eV, 0.624 eV above the supplied 2.42 eV optical gap. The gas-to-chloroform gap change is -0.061 eV. This is a bounded orbital-gap consistency test, not an exact optical excitation or emission-energy prediction."
  },
  "completion_status": "completed",
  "conclusion": "The supplied 6a identity was preserved and both author-route environments reached validated stationary structures. The computed chloroform frontier gap is close to the recovered SI value (3.04 eV) and supports a qualitative comparison with the long-wavelength optical gap, while the nonzero deviation means it does not by itself establish exact excitation-energy agreement or causal photophysics.",
  "current_recovery": {
    "hpc_jobs": [],
    "hpc_status_counts": {},
    "local_native_jobs": [
      {
        "case": "6a_chcl3_optfreq",
        "duration_seconds": 12999.707466,
        "job_id": "job_82bdfbdb7b1749799d6275a118284ec4",
        "live_process": false,
        "live_process_pids": [],
        "return_code": 0,
        "status": "success",
        "status_path": "docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_chcl3_optfreq/outputs/execution_jobs/job_82bdfbdb7b1749799d6275a118284ec4/status.json",
        "status_sha256": "4999b45126a2d1b1dc50eacd45fd928aacddf59ad8971ad02ba0736f7588fe47"
      },
      {
        "case": "6a_gas_optfreq",
        "duration_seconds": 11678.017903,
        "job_id": "job_d9cc03414c9d48c092a46eb2c8cab755",
        "live_process": false,
        "live_process_pids": [],
        "return_code": 0,
        "status": "success",
        "status_path": "docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_gas_optfreq/outputs/execution_jobs/job_d9cc03414c9d48c092a46eb2c8cab755/status.json",
        "status_sha256": "966fc9820c54a8eda582af2fe2df1785b655763f863144cbe8b49f9953ea09ef"
      }
    ],
    "route_gate": "Author-route calculation and evaluator comparison are complete and strictly verified.",
    "scientific_conclusion": "Not upgraded: queueing/wrapper success is not application-level convergence; custom/private author inputs remain bounded.",
    "updated_at": "2026-09-13T08:56:43.584158+00:00"
  },
  "gas_phase": {
    "gap_eV": 3.105,
    "homo_eV": -6.2085,
    "lumo_eV": -3.1035,
    "validation_evidence": "artifacts/native/6a_gas_optfreq_summary.json; status success/return 0; normal_termination=true; optimization_completed=true; imaginary_frequency_count=0; stdout SHA-256 6084b95a6e152d44a22e8d7b3f4a1a60243dc1bf97bc78ac90b68c37eedff3cd"
  },
  "limitations": "The task supplies one neutral closed-shell XYZ and does not sample alternative tautomers or conformers. Kohn-Sham orbital gaps are not optical excitation energies; the implicit solvent model, functional, finite basis, and starting conformer introduce method sensitivity. The gas and chloroform jobs were run independently from the supplied geometry under the same electronic-structure protocol; TD-DFT transition energies were outside this ground-state endpoint.",
  "method": {
    "optimization": "B3LYP-D3(BJ)/6-311+G* Opt Freq; gas phase and CPCM(Chloroform), 8 cores, 2000 MB/core, TightSCF",
    "software": "ORCA 6.1.1",
    "validation": "Both jobs terminated normally, optimization converged in 4 cycles, 105 vibrational frequencies were parsed, and imaginary_frequency_count=0. HOMO/LUMO tables contain 96 rows in the final parser pass."
  },
  "structure_check": {
    "atom_count": 35,
    "charge": 0,
    "identity_confirmed": true,
    "multiplicity": 1
  }
}
```

## Re-audit source-evidence drift

- Classification: **RUNTIME_METADATA_ONLY**
- Previous `results.json` SHA-256: `2d6804c3069966ebed5eaa7336dde03ff0da9f38b729014cdae7762d78cb8b35`
- Current `results.json` SHA-256: `6ec66b6d0d1b83753befa128ac38aa44432f37e001b4876968f4b7609f97b724`
- Changed top-level result fields: `current_recovery`
- Changed execution-artifact paths: `none detected`

A source hash change is not treated as a new scientific result. Runtime-only changes remain metadata drift; any other change requires semantic comparison of the provenance record. This archive is not a scoring standard.

<!-- source-drift-json: {"changed_artifact_paths": [], "changed_top_level_keys": ["current_recovery"], "classification": "RUNTIME_METADATA_ONLY", "current_sha256": "6ec66b6d0d1b83753befa128ac38aa44432f37e001b4876968f4b7609f97b724", "detected": true, "previous_sha256": "2d6804c3069966ebed5eaa7336dde03ff0da9f38b729014cdae7762d78cb8b35"} -->

Paper/SI document hashes:

- `papers/paper_9ec8c4761c4f171b/documents/main.pdf` — SHA-256 `49d8e9997164eb5f8400e8730c64d2fc6b5929e6e5c9ba431ba766c4486c51be` (declared_match=True)
- `papers/paper_9ec8c4761c4f171b/documents/supplementary_001.pdf` — SHA-256 `29b1c6d10ffb42a053b3303aad720cad5fd49a336015dd6b2fd76a1a98ba742a` (declared_match=True)

Report evidence lines retained:

- 分别提交两个独立的 ORCA `Opt Freq` 作业：
- 依据是：公开对象可独立识别；作者路线的 gas/CPCM Opt Freq 端点均真实完成并验证为 local minima；gap 与 SI/evaluator 一致；结果和限制说明没有越界。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **20**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/status.json` — successful status record; SHA-256 `4999b45126a2d1b1dc50eacd45fd928aacddf59ad8971ad02ba0736f7588fe47`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/collection.json` — successful execution artifact; SHA-256 `a7b4b4a572057964425d276a2dfef83b3f971332365c40a4b19ac76467002d22`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/input.inp` — successful execution artifact; SHA-256 `db4489b3d8dfc45e5061a25eb04816238ad9ce4e5014c0925138f329e0c7aaa0`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/input.xyz` — successful execution artifact; SHA-256 `f7f3cda7700c85c9ce2f7a08d735db22e2c9262408a714baafb855c8dba8f879`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/input_trj.xyz` — successful execution artifact; SHA-256 `5ead69337bea0ed0330b6291fce1f25161c7dbd5575249231f67ccd67d8a2d21`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/status.json` — successful status record; SHA-256 `966fc9820c54a8eda582af2fe2df1785b655763f863144cbe8b49f9953ea09ef`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/collection.json` — successful execution artifact; SHA-256 `1896a7d8779887d92d7efafe408e78db0015df33acdd68f278e48ead4f8af116`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/input.inp` — successful execution artifact; SHA-256 `e84b9b1f28889328bcae08dfcb1634d305c954dd6061988bf9e002b7c7cf9d0e`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/input.xyz` — successful execution artifact; SHA-256 `a07a4d9e0327d32e5138f72063694402fdc94b70e4c82fa19861f9b6abce1695`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/input_trj.xyz` — successful execution artifact; SHA-256 `6cf3c92fdaa3397a22489e1e9036b22ac4b8f233655ffd3c0c8c54a6d16af127`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_chcl3_optfreq/outputs/execution_jobs/job_82bdfbdb7b1749799d6275a118284ec4/status.json` — successful status record; SHA-256 `4999b45126a2d1b1dc50eacd45fd928aacddf59ad8971ad02ba0736f7588fe47`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_chcl3_optfreq/outputs/execution_jobs/job_82bdfbdb7b1749799d6275a118284ec4/collection.json` — successful execution artifact; SHA-256 `a7b4b4a572057964425d276a2dfef83b3f971332365c40a4b19ac76467002d22`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_chcl3_optfreq/outputs/execution_jobs/job_82bdfbdb7b1749799d6275a118284ec4/input.inp` — successful execution artifact; SHA-256 `db4489b3d8dfc45e5061a25eb04816238ad9ce4e5014c0925138f329e0c7aaa0`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_chcl3_optfreq/outputs/execution_jobs/job_82bdfbdb7b1749799d6275a118284ec4/input.xyz` — successful execution artifact; SHA-256 `f7f3cda7700c85c9ce2f7a08d735db22e2c9262408a714baafb855c8dba8f879`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_chcl3_optfreq/outputs/execution_jobs/job_82bdfbdb7b1749799d6275a118284ec4/input_trj.xyz` — successful execution artifact; SHA-256 `5ead69337bea0ed0330b6291fce1f25161c7dbd5575249231f67ccd67d8a2d21`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_gas_optfreq/outputs/execution_jobs/job_d9cc03414c9d48c092a46eb2c8cab755/status.json` — successful status record; SHA-256 `966fc9820c54a8eda582af2fe2df1785b655763f863144cbe8b49f9953ea09ef`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_gas_optfreq/outputs/execution_jobs/job_d9cc03414c9d48c092a46eb2c8cab755/collection.json` — successful execution artifact; SHA-256 `1896a7d8779887d92d7efafe408e78db0015df33acdd68f278e48ead4f8af116`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_gas_optfreq/outputs/execution_jobs/job_d9cc03414c9d48c092a46eb2c8cab755/input.inp` — successful execution artifact; SHA-256 `e84b9b1f28889328bcae08dfcb1634d305c954dd6061988bf9e002b7c7cf9d0e`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_gas_optfreq/outputs/execution_jobs/job_d9cc03414c9d48c092a46eb2c8cab755/input.xyz` — successful execution artifact; SHA-256 `a07a4d9e0327d32e5138f72063694402fdc94b70e4c82fa19861f9b6abce1695`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_gas_optfreq/outputs/execution_jobs/job_d9cc03414c9d48c092a46eb2c8cab755/input_trj.xyz` — successful execution artifact; SHA-256 `6cf3c92fdaa3397a22489e1e9036b22ac4b8f233655ffd3c0c8c54a6d16af127`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/native/6a_gas_optfreq/status.json` — label=group_6 paper_9ec8c4761c4f171b 6a_gas_optfreq; submitted_at=2026-08-31T16:12:56.060513+00:00; software=orca; intent=optimization_frequency; command=orca input.inp
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/collection.json`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/input.bibtex`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/input.densities`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/input.densitiesinfo`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/input.engrad`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/input.gbw`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/input.hess`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq/input.inp`
2. `artifacts/native/6a_chcl3_optfreq/status.json` — label=group_6 paper_9ec8c4761c4f171b 6a_chcl3_optfreq; submitted_at=2026-08-31T16:12:56.508013+00:00; software=orca; intent=optimization_frequency; command=orca input.inp
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/collection.json`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/input.bibtex`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/input.cpcm`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/input.cpcm_corr`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/input.densities`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/input.densitiesinfo`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/input.engrad`
   - output: `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq/input.gbw`

## Evaluator alignment

- Key-point IDs: `kp_process, kp_gap`
- Conclusion IDs: `c_final`
- Scoring-rule IDs: `r_process, r_gap, r_final`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_process` → reference `kp_process`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_gap` → reference `kp_gap`; type=numeric; unit=eV; tolerance=0.35; comparison=absolute difference; evaluator_target_present=True
- rule `r_final` → reference `c_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_gap` / reference `kp_gap`: target=3.04 eV; tolerance=0.35; numeric result leaves=[3.044]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_process` / reference `kp_process` / field `$.method.validation` / result path `$.method.validation` = `"Both jobs terminated normally, optimization converged in 4 cycles, 105 vibrational frequencies were parsed, and imaginary_frequency_count=0. HOMO/LUMO tables contain 96 rows in the final parser pass."`
- rule `r_process` / reference `kp_process` / field `$.structure_check.identity_confirmed` / result path `$.structure_check.identity_confirmed` = `true`
- rule `r_process` / reference `kp_process` / field `$.gas_phase.validation_evidence` / result path `$.gas_phase.validation_evidence` = `"artifacts/native/6a_gas_optfreq_summary.json; status success/return 0; normal_termination=true; optimization_completed=true; imaginary_frequency_count=0; stdout SHA-256 6084b95a6e152d44a22e8d7b3f4a1a60243dc1bf97bc78ac90b68c37eedff3cd"`
- rule `r_process` / reference `kp_process` / field `$.chloroform.validation_evidence` / result path `$.chloroform.validation_evidence` = `"artifacts/native/6a_chcl3_optfreq_summary.json; status success/return 0; normal_termination=true; optimization_completed=true; imaginary_frequency_count=0; stdout SHA-256 65948ab4a98c0c8711760e9d8388f4b43c1c2b63cc1cd8221ec4ccb0ba1a2b02"`
- rule `r_gap` / reference `kp_gap` / field `$.chloroform.gap_eV` / result path `$.chloroform.gap_eV` = `3.044`
- rule `r_final` / reference `c_final` / field `$.conclusion` / result path `$.conclusion` = `"The supplied 6a identity was preserved and both author-route environments reached validated stationary structures. The computed chloroform frontier gap is close to the recovered SI value (3.04 eV) and supports a qualitative comparison wi..."`
- rule `r_final` / reference `c_final` / field `$.limitations` / result path `$.limitations` = `"The task supplies one neutral closed-shell XYZ and does not sample alternative tautomers or conformers. Kohn-Sham orbital gaps are not optical excitation energies; the implicit solvent model, functional, finite basis, and starting confor..."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Complete 6a XYZ and problem definition.

Public input files and hashes:

- `agent_input/data/inputs/compound_6a.xyz` — SHA-256 `36eb20674a8f11d2cb0d8271f69f14c2ede1aef355a4c113a18ad885b5986e34`; size=1986 bytes; xyz_atom_count=35; xyz_comment=compound 6a; neutral closed-shell starting geometry; coordinates in angstrom; explicit_boundary_fields={"units_hint": "explicit angstrom marker"}
- `agent_input/data/inputs/problem.json` — SHA-256 `858a353ed9e3ae1aded9ca3a1bd5749ea3c00fd5b1c3bb8ecdf6c299c25b8179`; size=142 bytes; explicit_boundary_fields={"$.charge": 0, "$.multiplicity": 1, "$.solvent": "chloroform"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_6/paper_9ec8c4761c4f171b/verification_report.md` — verification record; SHA-256 `bd363f346b15d610ac986e76c1ec1dd6d4fce98b07c0d968541fd6e7f5eb3f6f`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/report/results.json` — verification record; SHA-256 `6ec66b6d0d1b83753befa128ac38aa44432f37e001b4876968f4b7609f97b724`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_chcl3_optfreq_summary.json` — referenced successful evidence; SHA-256 `74003e69c6bc1ea7e1d8c172ad31891dee2b12f7bcc930ee734e38f97a603d7a`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/artifacts/native/6a_gas_optfreq_summary.json` — referenced successful evidence; SHA-256 `ffc2abd7183e929c34eb5f4a756684e3c1a9af4d1257fcf50209f39e18814737`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_chcl3_optfreq/outputs/execution_jobs/job_82bdfbdb7b1749799d6275a118284ec4/status.json` — referenced successful evidence; SHA-256 `4999b45126a2d1b1dc50eacd45fd928aacddf59ad8971ad02ba0736f7588fe47`
- `docs/verification/group_6/paper_9ec8c4761c4f171b/native_workspace/6a_gas_optfreq/outputs/execution_jobs/job_d9cc03414c9d48c092a46eb2c8cab755/status.json` — referenced successful evidence; SHA-256 `966fc9820c54a8eda582af2fe2df1785b655763f863144cbe8b49f9953ea09ef`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
