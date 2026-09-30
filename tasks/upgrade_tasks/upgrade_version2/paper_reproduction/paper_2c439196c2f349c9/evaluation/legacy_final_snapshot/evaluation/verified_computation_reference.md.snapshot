# Verified computation reference — paper_2c439196c2f349c9 (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `completed` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 5 | `PASS` | 最终严格状态：**PASS**。作者路线为气相 B3LYP/6-31G(d,p) 优化/频率及同层级前线轨道分析；Gaussian 16 C.01 在公开身份生成的合法结构上完成了该科学路线。与 `evaluation/scoring_rules.json` 对照：HOMO、LUMO 和 gap 分别与 −0.23029 au、−0.10866 au 和 3.31 eV 相差 0.00763 au、0.01175 au 和 0.11193 eV，均在容差内；驻点、宽带隙/有限极化率和分子带隙不等于固体带隙的限制也一致。 |
| 12 | `PASS` | - 论文复现结论： **PASS**。中间驻点验证和最终前线轨道数值均由真实 Gaussian 作业产生，且事后与论文正文第 4 页独立对照一致。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Synthesis, characterization, nonlinear optical properties, and DFT analysis of a new azo-Schiff base dye
- DOI: `10.1016/j.molstruc.2025.145051`
- Task package: `tasks/final_verified_paper_reproduction/paper_2c439196c2f349c9`
- Verification group: `docs/verification/group_3/paper_2c439196c2f349c9`
- Paper documents: `papers/paper_2c439196c2f349c9`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "conclusion": "The converged neutral-singlet INP optimization and zero-imaginary-frequency check support a valid stationary point. The computed HOMO/LUMO values (-0.222660281/-0.0969067781 hartree) give a 3.42193 eV isolated-molecule gap. A post-calculation comparison with the article's page-4 values (-0.23029/-0.10866 hartree; 3.31 eV) gives absolute differences of 0.00763/0.01175 hartree and 0.11193 eV. This supports the paper's wide-gap and limited-electronic-polarizability interpretation, while the descriptor must not be treated as a measured solid-state band gap; the reported CW NLO response remains primarily a thermal-lensing effect.",
  "coverage": {
    "limitations": "The calculation is an isolated-molecule, gas-phase B3LYP/6-31G(d,p) descriptor and is method-, geometry-, and tautomer-dependent. One starting conformer does not establish global-minimum coverage. The frontier gap is not a solid-state experimental band gap; the paper's CW nonlinear-optical response is interpreted mainly as thermal-lensing rather than as a direct consequence of this orbital gap.",
    "starting_geometry_count": 1,
    "starting_geometry_diversity": "One chemically valid 3-D structure generated from the public SMILES with RDKit ETKDG and MMFF preoptimization; no exhaustive conformer/global-minimum search was claimed."
  },
  "frontier_orbitals": {
    "gap_ev": 3.4219288688,
    "gap_formula": "(E_LUMO - E_HOMO) * 27.2114 = (-0.0969067781 - (-0.222660281)) * 27.2114 eV = 3.4219288688 eV",
    "homo_au": -0.222660281,
    "lumo_au": -0.0969067781
  },
  "geometry_validation": {
    "evidence": "Gaussian stdout contains 'Optimization completed', 'Normal termination of Gaussian 16', and 120 parsed frequencies; minimum frequency 10.4271 cm^-1. The final checkpoint was converted to formatted checkpoint with formchk.",
    "frequency_check": "Local minimum validated: Gaussian optimization completed and the subsequent harmonic frequency calculation returned 120 real frequencies with zero imaginary frequencies.",
    "imaginary_frequency_count": 0,
    "optimized_geometry_or_path": "artifacts/gaussian/inp_b3lyp_opt_freq_unlimited_optimized.xyz (also artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/inp_b3lyp_opt_freq_unlimited.fchk)"
  },
  "method": {
    "model": "B3LYP/6-31G(d,p)",
    "optimization_converged": true,
    "settings": "Isolated neutral singlet; RDKit ETKDG with MMFF preoptimization for one starting geometry; Gaussian route #p B3LYP/6-31G(d,p) Opt Freq Pop=Full; 16 CPU cores, 60000 MB memory, no solvent, no symmetry constraint in the input geometry.",
    "software": "Gaussian 16 C.01 (g16), parsed with cclib 1.8.1"
  },
  "molecule": {
    "charge": 0,
    "compound_id": "INP",
    "multiplicity": 1,
    "stereochemistry": "E about the imine C=N and E about the azo N=N linkage; no stereocenters"
  },
  "status": "completed",
  "verification_metadata": {
    "difficulty": "easy",
    "doi": "10.1016/j.molstruc.2025.145051",
    "independent_calculation_completed_before_paper_comparison": true,
    "paper_comparison": "After the independent calculation, the article main text page 4 was read for comparison: HOMO -0.23029 au, LUMO -0.10866 au, gap 3.31 eV; absolute differences are 0.00763 au, 0.01175 au, and 0.11193 eV, respectively. No tasks/*/evaluation content is used or cited.",
    "paper_id": "paper_2c439196c2f349c9",
    "task_mode": "paper_reproduction"
  }
}
```

Paper/SI document hashes:

- `papers/paper_2c439196c2f349c9/documents/main.pdf` — SHA-256 `1470f926af7414723c25e43c91ebe0fc964aa269e3943752deb4d469907ae3e7` (declared_match=True)
- `papers/paper_2c439196c2f349c9/documents/supplementary_001.pdf` — SHA-256 `2f1a3ca284a417a10d01c535fe535c5fcfc4d3f39d1ad9391a835f06094b2669` (declared_match=True)

Report evidence lines retained:

- 由公开 SMILES 用 RDKit ETKDG 生成一套 3-D 初猜并做 MMFF 预优化；未使用正文结论或 `tasks/*/evaluation/` 设计几何、路线或预期数值。Gaussian 16 C.01 路线为气相 B3LYP/6-31G(d,p) `Opt Freq Pop=Full`，电荷/多重度 `(0,1)`，16 核、60000 MB。Gaussian 无墙钟上限；单构象不代表全局最低点覆盖。
- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **10**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/status.json` — successful status record; SHA-256 `b076856268142896de6067f12360e3a33b76bece23432720a1b1a580b0f5152e`
- `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/collection.json` — successful execution artifact; SHA-256 `269bdabe1b6980beba6ae2e3a5e5a44585653c3ff00b9941183e132cc6d5f589`
- `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/inp_b3lyp_opt_freq_unlimited_optimized.xyz` — successful execution artifact; SHA-256 `05f61c47a15c2ca5c777a596b983f06bbccfcc2fe2b042a5a8758bade4e6a21c`
- `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/input.com` — successful execution artifact; SHA-256 `906ceedcd711aae30a53602048a7cc6fcf0d0d4ff6693ff6abf8c03e37022eab`
- `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/parsed_observables.json` — successful execution artifact; SHA-256 `449edcb0694f0252ef5178de188354a5c84b13aca179360e30d148eeaac453fe`
- `docs/verification/group_3/paper_2c439196c2f349c9/native_workspace/inp_b3lyp_opt_freq_unlimited/outputs/execution_jobs/job_2ed548c1d41b44ceb94858e4dc16df4a/status.json` — successful status record; SHA-256 `b076856268142896de6067f12360e3a33b76bece23432720a1b1a580b0f5152e`
- `docs/verification/group_3/paper_2c439196c2f349c9/native_workspace/inp_b3lyp_opt_freq_unlimited/outputs/execution_jobs/job_2ed548c1d41b44ceb94858e4dc16df4a/collection.json` — successful execution artifact; SHA-256 `269bdabe1b6980beba6ae2e3a5e5a44585653c3ff00b9941183e132cc6d5f589`
- `docs/verification/group_3/paper_2c439196c2f349c9/native_workspace/inp_b3lyp_opt_freq_unlimited/outputs/execution_jobs/job_2ed548c1d41b44ceb94858e4dc16df4a/input.com` — successful execution artifact; SHA-256 `906ceedcd711aae30a53602048a7cc6fcf0d0d4ff6693ff6abf8c03e37022eab`
- `docs/verification/group_3/paper_2c439196c2f349c9/native_workspace/inp_b3lyp_opt_freq_unlimited/outputs/execution_jobs/job_2ed548c1d41b44ceb94858e4dc16df4a/request.json` — successful execution artifact; SHA-256 `8e66e7e2d7f04d89bcace67ff71d5e7e9490c85f175f281c9dedc1e5fbec7e13`
- `docs/verification/group_3/paper_2c439196c2f349c9/native_workspace/inp_b3lyp_opt_freq_unlimited/outputs/execution_jobs/job_2ed548c1d41b44ceb94858e4dc16df4a/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/status.json` — label=group_3 paper_2c439196c2f349c9 inp_b3lyp_opt_freq_unlimited; submitted_at=2026-08-29T06:31:27.525794+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d,p) Opt Freq Pop=Full; command=g16 < input.com
   - output: `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/collection.json`
   - output: `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/inp_b3lyp_opt_freq_unlimited.chk`
   - output: `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/inp_b3lyp_opt_freq_unlimited.fchk`
   - output: `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/inp_b3lyp_opt_freq_unlimited_optimized.xyz`
   - output: `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/input.com`
   - output: `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/parsed_observables.json`
   - output: `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/stderr.log`
   - output: `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/stdout.log`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `c_limit`, `r_limit`.

- Key-point IDs: `kp_process, kp_result`
- Conclusion IDs: `c_final, c_limit`
- Scoring-rule IDs: `r_process, r_homo, r_lumo, r_gap, r_final, r_limit`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_process` → reference `kp_process`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert validation; evaluator_target_present=False
- rule `r_homo` → reference `kp_result`; type=numeric; unit=hartree; tolerance=0.03; comparison=absolute difference; evaluator_target_present=True
- rule `r_lumo` → reference `kp_result`; type=numeric; unit=hartree; tolerance=0.03; comparison=absolute difference; evaluator_target_present=True
- rule `r_gap` → reference `kp_result`; type=numeric; unit=eV; tolerance=0.2; comparison=absolute difference; evaluator_target_present=True
- rule `r_final` → reference `c_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_limit` → reference `c_limit`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_homo` / reference `kp_result`: target=-0.23029 hartree; tolerance=0.03; numeric result leaves=[-0.222660281]; within_tolerance=True; applicability=applicable
- rule `r_lumo` / reference `kp_result`: target=-0.10866 hartree; tolerance=0.03; numeric result leaves=[-0.0969067781]; within_tolerance=True; applicability=applicable
- rule `r_gap` / reference `kp_result`: target=3.31 eV; tolerance=0.2; numeric result leaves=[3.4219288688]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_process` / reference `kp_process` / field `$.molecule` / result path `$.molecule.compound_id` = `"INP"`
- rule `r_process` / reference `kp_process` / field `$.molecule` / result path `$.molecule.charge` = `0`
- rule `r_process` / reference `kp_process` / field `$.molecule` / result path `$.molecule.multiplicity` = `1`
- rule `r_process` / reference `kp_process` / field `$.molecule` / result path `$.molecule.stereochemistry` = `"E about the imine C=N and E about the azo N=N linkage; no stereocenters"`
- rule `r_process` / reference `kp_process` / field `$.method.optimization_converged` / result path `$.method.optimization_converged` = `true`
- rule `r_process` / reference `kp_process` / field `$.geometry_validation` / result path `$.geometry_validation.frequency_check` = `"Local minimum validated: Gaussian optimization completed and the subsequent harmonic frequency calculation returned 120 real frequencies with zero imaginary frequencies."`
- rule `r_process` / reference `kp_process` / field `$.geometry_validation` / result path `$.geometry_validation.imaginary_frequency_count` = `0`
- rule `r_process` / reference `kp_process` / field `$.geometry_validation` / result path `$.geometry_validation.evidence` = `"Gaussian stdout contains 'Optimization completed', 'Normal termination of Gaussian 16', and 120 parsed frequencies; minimum frequency 10.4271 cm^-1. The final checkpoint was converted to formatted checkpoint with formchk."`
- rule `r_process` / reference `kp_process` / field `$.geometry_validation` / result path `$.geometry_validation.optimized_geometry_or_path` = `"artifacts/gaussian/inp_b3lyp_opt_freq_unlimited_optimized.xyz (also artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/inp_b3lyp_opt_freq_unlimited.fchk)"`
- rule `r_homo` / reference `kp_result` / field `$.frontier_orbitals.homo_au` / result path `$.frontier_orbitals.homo_au` = `-0.222660281`
- rule `r_lumo` / reference `kp_result` / field `$.frontier_orbitals.lumo_au` / result path `$.frontier_orbitals.lumo_au` = `-0.0969067781`
- rule `r_gap` / reference `kp_result` / field `$.frontier_orbitals.gap_ev` / result path `$.frontier_orbitals.gap_ev` = `3.4219288688`
- rule `r_final` / reference `c_final` / field `$.conclusion` / result path `$.conclusion` = `"The converged neutral-singlet INP optimization and zero-imaginary-frequency check support a valid stationary point. The computed HOMO/LUMO values (-0.222660281/-0.0969067781 hartree) give a 3.42193 eV isolated-molecule gap. A post-calcul..."`
- rule `r_limit` / reference `c_limit` / field `$.coverage.limitations` / result path `$.coverage.limitations` = `"The calculation is an isolated-molecule, gas-phase B3LYP/6-31G(d,p) descriptor and is method-, geometry-, and tautomer-dependent. One starting conformer does not establish global-minimum coverage. The frontier gap is not a solid-state ex..."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Self-contained INP molecular identity and physical boundary.

Public input files and hashes:

- `agent_input/data/inputs/inp_molecule.json` — SHA-256 `70c8b53f724f33bf18f25389b92a5f2137435ff4f07fe808cf5ef9b01ead8456`; size=498 bytes; explicit_boundary_fields={"$.charge": 0, "$.formula": "C17H18N4O3", "$.multiplicity": 1, "$.smiles": "CC(C)C/N=C/c1cc(N=N/c2ccc([N+](=O)[O-])cc2)ccc1O"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_2c439196c2f349c9/verification_report.md` — verification record; SHA-256 `a40993505139af6a354747f24487537bcfb74213833bd650eb7163bcfd9f797c`
- `docs/verification/group_3/paper_2c439196c2f349c9/report/results.json` — verification record; SHA-256 `64a7279ee6936ae7f7217ba5fcbfdd629443e49eedef43ecf5c118ed49dca6de`
- `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited/inp_b3lyp_opt_freq_unlimited.fchk` — referenced successful evidence; SHA-256 `b46c33e657faaff36a83fa9319e2775bfaba3f870b8f46ba1bbbf506be56679d`
- `docs/verification/group_3/paper_2c439196c2f349c9/artifacts/gaussian/inp_b3lyp_opt_freq_unlimited_optimized.xyz` — referenced successful evidence; SHA-256 `5f10d4ca33609307b5b22691799bfbd263a563873b3be026fdf033bfe6094eb2`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
