# Verified computation reference — paper_86a0b654270a8ce7 (autonomous_research)

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
| 132 | `PASS` | - 论文复现结论：`PASS`；作者路线的两个 minimum、频率和 Gibbs/比例推导均有原始日志证据。 |
| 143 | `QUALIFIED` | - Evaluator/task qualification: **`QUALIFIED`** |
| 152 | `PASS` | - 论文复现结论：`PASS` |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Cyclometalated iridium(III)–Salen NHC complexes: Gibbs energy–driven isomer distribution, structures, and Photophysical properties
- DOI: `10.1016/j.ica.2025.122961`
- Task package: `tasks/final_verified_autonomous_research/paper_86a0b654270a8ce7`
- Verification group: `docs/verification/group_1/paper_86a0b654270a8ce7`
- Paper documents: `papers/paper_86a0b654270a8ce7`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "conclusion": "Both isolated neutral singlet structures are validated minima. Positive G(1)-G(2) makes isomer 2 lower in Gibbs free energy and gives a population ratio [2]/[1] of about 2.80 at 339 K, consistent with the evaluator target.",
  "derived": {
    "delta_delta_G_kJ_mol": 2.901177099530381,
    "equation": "[2]/[1] = exp((G1-G2)*1000/(R*T))",
    "gas_constant": "R=8.31446261815324 J mol-1 K-1",
    "population_ratio_2_over_1": 2.7990950585088634
  },
  "limitations": "The result is model-dependent on B3LYP/def2SVP and SMD(THF); it does not establish kinetic control or solution speciation beyond the two supplied isomers.",
  "method": {
    "electronic_structure": "B3LYP/def2SVP Opt(Tight,CalcFC)+Freq with SMD(THF)",
    "software": "Gaussian 16",
    "solvent": "THF (SMD)",
    "standard_state": "Gaussian thermal convention; delta-G population ratio at 339 K",
    "temperature_K": 339.0
  },
  "status": "complete",
  "systems": [
    {
      "charge": 0,
      "frequency_validation": {
        "evidence": "384 frequencies; minimum frequency 11.3669 cm-1",
        "imaginary_frequency_count": 0
      },
      "gibbs_free_energy_hartree": -2795.462325,
      "input_file": "data/inputs/complex_1.xyz",
      "label": "1",
      "minimum_status": "minimum",
      "multiplicity": 1,
      "optimization_evidence": "native_workspace_batch/outputs/execution_jobs/job_9eb9b024f9014d9984fe971d5fcb1779/stdout.log; normal termination and optimization completed"
    },
    {
      "charge": 0,
      "frequency_validation": {
        "evidence": "384 frequencies; minimum frequency 12.38 cm-1",
        "imaginary_frequency_count": 0
      },
      "gibbs_free_energy_hartree": -2795.46343,
      "input_file": "data/inputs/complex_2.xyz",
      "label": "2",
      "minimum_status": "minimum",
      "multiplicity": 1,
      "optimization_evidence": "native_workspace_batch/outputs/execution_jobs/job_e7bc33da985f40b8b8875e410d16ffca/stdout.log; normal termination and optimization completed"
    }
  ]
}
```

Paper/SI document hashes:

- `papers/paper_86a0b654270a8ce7/documents/main.pdf` — SHA-256 `b19110f192c994ade2406a46c6cc62346d465b27568db22c2b86df46f3af5879` (declared_match=True)
- `papers/paper_86a0b654270a8ce7/documents/supplementary_001.pdf` — SHA-256 `59edd5baf1ea3027779a0ba8fef20348da233372dfdccdaf0ea2fa1f3f5886fb` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **20**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/status.json` — successful status record; SHA-256 `5295f745a241c8f21c9c15f753e08e9eb1626fa572c4785ded2d46468acb1f7b`
- `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/collection.json` — successful execution artifact; SHA-256 `b857c7ec27603bd68f8220c9bab3fd2a1f0c2b7af2f1ba44eaede5e2506d97b8`
- `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/complex1_b3lyp_def2svp_smdthf_optfreq_339k.xyz` — successful execution artifact; SHA-256 `d85f3c80b09415de0fde892776a10808321a0c410d16cc2502153d34fb753775`
- `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/complex1_b3lyp_def2svp_smdthf_optfreq_339k_summary.json` — successful execution artifact; SHA-256 `1752e63dc7c04f70a6705b2506343da159609f2766f6e660f9f95251a6d3c4ce`
- `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/input.com` — successful execution artifact; SHA-256 `b3f77f599b06db52a1d8753dbd8dd0332b2b59793bb6ea113ddffe9ad405a828`
- `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/status.json` — successful status record; SHA-256 `cbd5938e059bd988b9bb007b3be45af963fe80d6807c7eb914300f36908a6eec`
- `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/collection.json` — successful execution artifact; SHA-256 `2cef24c0a421854d59be810b6d304a21daa74e12c6d4c62224baeb4cbb63a56d`
- `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/complex2_b3lyp_def2svp_smdthf_optfreq_339k.xyz` — successful execution artifact; SHA-256 `69146d17a2cd563f15f058b32230d51359d6b345a598a03c1496c9a390cb3384`
- `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/complex2_b3lyp_def2svp_smdthf_optfreq_339k_summary.json` — successful execution artifact; SHA-256 `2664bd7d9600608135dfc1b816f7c746b49665afc81f4ac760eec4ea656986ff`
- `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/input.com` — successful execution artifact; SHA-256 `7f98df2ae75d19130ee1d580d0c829f425fc33b5c33fdec953d146e41223f173`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_9eb9b024f9014d9984fe971d5fcb1779/status.json` — successful status record; SHA-256 `5295f745a241c8f21c9c15f753e08e9eb1626fa572c4785ded2d46468acb1f7b`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_9eb9b024f9014d9984fe971d5fcb1779/collection.json` — successful execution artifact; SHA-256 `b857c7ec27603bd68f8220c9bab3fd2a1f0c2b7af2f1ba44eaede5e2506d97b8`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_9eb9b024f9014d9984fe971d5fcb1779/input.com` — successful execution artifact; SHA-256 `b3f77f599b06db52a1d8753dbd8dd0332b2b59793bb6ea113ddffe9ad405a828`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_9eb9b024f9014d9984fe971d5fcb1779/request.json` — successful execution artifact; SHA-256 `e2a17dc121d7a27f4f04762836a55d070287887e1d985cf9134b10b8f2490ee0`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_9eb9b024f9014d9984fe971d5fcb1779/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_e7bc33da985f40b8b8875e410d16ffca/status.json` — successful status record; SHA-256 `cbd5938e059bd988b9bb007b3be45af963fe80d6807c7eb914300f36908a6eec`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_e7bc33da985f40b8b8875e410d16ffca/collection.json` — successful execution artifact; SHA-256 `2cef24c0a421854d59be810b6d304a21daa74e12c6d4c62224baeb4cbb63a56d`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_e7bc33da985f40b8b8875e410d16ffca/input.com` — successful execution artifact; SHA-256 `7f98df2ae75d19130ee1d580d0c829f425fc33b5c33fdec953d146e41223f173`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_e7bc33da985f40b8b8875e410d16ffca/request.json` — successful execution artifact; SHA-256 `f05d3ebe01b9f3ba67466aa7b2d7363a489cc6decdb26f152cdf5940b93ef9af`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_e7bc33da985f40b8b8875e410d16ffca/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/status.json` — label=paper_86a0b654270a8ce7 complex1_b3lyp_def2svp_smdthf_optfreq_339k unbounded_gaussian; submitted_at=2026-08-30T12:51:51.237879+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/Def2SVP SCRF=(SMD,Solvent=THF) Opt=(Tight,CalcFC,MaxCycles=300) Freq Temperature=339 Int=UltraFine SCF=(Tight,XQC,MaxCycle=512) NoSymm; command=g16 < input.com
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/collection.json`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/complex1_b3lyp_def2svp_smdthf_optfreq_339k.chk`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/complex1_b3lyp_def2svp_smdthf_optfreq_339k.xyz`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/complex1_b3lyp_def2svp_smdthf_optfreq_339k_summary.json`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/fort.7`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/input.com`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/stderr.log`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex1_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log`
2. `artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/status.json` — label=paper_86a0b654270a8ce7 complex2_b3lyp_def2svp_smdthf_optfreq_339k unbounded_gaussian; submitted_at=2026-08-30T13:07:52.976585+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/Def2SVP SCRF=(SMD,Solvent=THF) Opt=(Tight,CalcFC,MaxCycles=300) Freq Temperature=339 Int=UltraFine SCF=(Tight,XQC,MaxCycle=512) NoSymm; command=g16 < input.com
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/collection.json`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/complex2_b3lyp_def2svp_smdthf_optfreq_339k.chk`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/complex2_b3lyp_def2svp_smdthf_optfreq_339k.xyz`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/complex2_b3lyp_def2svp_smdthf_optfreq_339k_summary.json`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/fort.7`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/input.com`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/stderr.log`
   - output: `docs/verification/group_1/paper_86a0b654270a8ce7/artifacts/gaussian_batch/complex2_b3lyp_def2svp_smdthf_optfreq_339k/stdout.log`

## Evaluator alignment

- Key-point IDs: `kp_minima, kp_thermo, kp_delta, kp_ratio`
- Conclusion IDs: `c_final`
- Scoring-rule IDs: `r_minima, r_thermo, r_delta, r_ratio, r_final`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_minima` → reference `kp_minima`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert process comparison; evaluator_target_present=False
- rule `r_thermo` → reference `kp_thermo`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert process comparison; evaluator_target_present=False
- rule `r_delta` → reference `kp_delta`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_ratio` → reference `kp_ratio`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_final` → reference `c_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_minima` / reference `kp_minima` / field `$.systems[].frequency_validation.evidence` / result path `$.systems[].frequency_validation.evidence` = `"384 frequencies; minimum frequency 11.3669 cm-1"`
- rule `r_minima` / reference `kp_minima` / field `$.systems[].frequency_validation.evidence` / result path `$.systems[].frequency_validation.evidence` = `"384 frequencies; minimum frequency 12.38 cm-1"`
- rule `r_thermo` / reference `kp_thermo` / field `$.method.standard_state` / result path `$.method.standard_state` = `"Gaussian thermal convention; delta-G population ratio at 339 K"`
- rule `r_thermo` / reference `kp_thermo` / field `$.method.temperature_K` / result path `$.method.temperature_K` = `339.0`
- rule `r_delta` / reference `kp_delta` / field `$.derived.delta_delta_G_kJ_mol` / result path `$.derived.delta_delta_G_kJ_mol` = `2.901177099530381`
- rule `r_ratio` / reference `kp_ratio` / field `$.derived.population_ratio_2_over_1` / result path `$.derived.population_ratio_2_over_1` = `2.7990950585088634`
- rule `r_final` / reference `c_final` / field `$.conclusion` / result path `$.conclusion` = `"Both isolated neutral singlet structures are validated minima. Positive G(1)-G(2) makes isomer 2 lower in Gibbs free energy and gives a population ratio [2]/[1] of about 2.80 at 339 K, consistent with the evaluator target."`
- rule `r_final` / reference `c_final` / field `$.limitations` / result path `$.limitations` = `"The result is model-dependent on B3LYP/def2SVP and SMD(THF); it does not establish kinetic control or solution speciation beyond the two supplied isomers."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: stale incomplete endpoint coordinates plus leakage
- Files changed in that review: `agent_input/data/inputs/complex_1.xyz, agent_input/data/inputs/complex_2.xyz, agent_input/task.md, package_manifest.json, task_info.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Two complete source-SI XYZ files, each C60H63IrN4O2 (130 atoms), for labeled neutral-singlet endpoints complex_1 and complex_2.

Public input files and hashes:

- `agent_input/data/inputs/complex_1.xyz` — SHA-256 `ea5e3f5c15047137cfb92f81e125568cdc034a0c7d2fb1ae85b3b1ee37e4969b`; size=3247 bytes; xyz_atom_count=130; xyz_comment=complex_1: complete coordinates recovered from SI Gibbs-energy table; charge 0 multiplicity 1; explicit_boundary_fields={"charge": "0", "multiplicity": "1"}
- `agent_input/data/inputs/complex_2.xyz` — SHA-256 `8b232597af8650c8cbea7a455ded42829f44b591d63e88591c1cb91cf6e66d1e`; size=3236 bytes; xyz_atom_count=130; xyz_comment=complex_2: complete coordinates recovered from SI Gibbs-energy table; charge 0 multiplicity 1; explicit_boundary_fields={"charge": "0", "multiplicity": "1"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `agent_input/data/inputs/complex_1.xyz, agent_input/data/inputs/complex_2.xyz`

## Evidence files

- `docs/verification/group_1/paper_86a0b654270a8ce7/verification_report.md` — verification record; SHA-256 `b3f5e1f85cb7789ba0d20523677d7205aee6a7c777de3d40b1731a254eb99309`
- `docs/verification/group_1/paper_86a0b654270a8ce7/report/results.json` — verification record; SHA-256 `3d5dca93b44cc79caa2a946f67720670980e9b780ceec153c51adee0936e9b00`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_9eb9b024f9014d9984fe971d5fcb1779/stdout.log` — referenced successful evidence; SHA-256 `8f406c07e68157faf3942ef7cc5359338cfd2ed584c4852ebb4a1bbf0ce1432c`
- `docs/verification/group_1/paper_86a0b654270a8ce7/native_workspace_batch/outputs/execution_jobs/job_e7bc33da985f40b8b8875e410d16ffca/stdout.log` — referenced successful evidence; SHA-256 `96ba7d4b682d213b37d6a94b3a759faa61d31210bb21adb9ba0b973e1e42cede`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
