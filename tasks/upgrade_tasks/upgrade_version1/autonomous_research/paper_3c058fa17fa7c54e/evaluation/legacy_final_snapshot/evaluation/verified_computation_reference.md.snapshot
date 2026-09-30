# Verified computation reference — paper_3c058fa17fa7c54e (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

> Source-order resolution (2026-09-23): main Figure 2 explicitly labels Ph S1=3.1457 eV and T1/T2=1.7347 eV, unlike the reversed p.4 prose. Numerical verification outputs below are unchanged. Local optimization uses D3BJ not specified in the supplied SI, so these are independent calculations, not exact source-geometry reproduction.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **PARTIAL**
- Group result status: `success` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 3 | `IN_PROGRESS` | > **当前状态：`IN_PROGRESS`。** 本节只记录已经发生的审计和计算，不构成 |
| 80 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |
| 85 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |
| 90 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |
| 95 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |
| 100 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |
| 105 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |
| 110 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |
| 115 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |
| 120 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |
| 125 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |
| 130 | `QUALIFIED` | Four shell-fixed TD-DFT cases passed local exact-route gates and then terminated normally on HPC. `report/results.json` contains the parsed S1/T1 values, both inequalities and all evaluator ID checks. The strict qualification record is `QUALIFIED`; the conclusion remains model-bounded and does not claim that energetics alone prove the mechanism. |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: σ-Bond unit strategy: Constructing deep-blue triplet-triplet annihilation emitters based on anthracene core for efficient non-doped OLEDs
- DOI: `10.1016/j.dyepig.2025.113436`
- Task package: `tasks/final_verified_autonomous_research/paper_3c058fa17fa7c54e`
- Verification group: `docs/verification/group_4/paper_3c058fa17fa7c54e`
- Paper documents: `papers/paper_3c058fa17fa7c54e`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "conclusion": "Both An-sigma-Ph and An-sigma-DA satisfy 2T1>S1 and S1-T1>0.5 eV in the submitted B3LYP/6-31G(d,p) model, supporting the evaluator's TTA energetic conclusion within the model and with the stated mechanistic limitation.",
  "coverage": "Both named systems, optimized S0 minima, explicit lowest singlet/triplet roots, both derived gaps, and both evaluator inequalities are covered. No claim is made that energetics alone prove the TTA mechanism.",
  "limitations": "TD-DFT values are model-dependent; the calculation does not establish OLED kinetics, non-radiative rates, conformer populations, or a unique mechanism.",
  "sensitivity": "The same four exact-route TD calculations first passed the local stability gate and then terminated normally on HPC. Local and HPC lowest-root energies agree to the reported 0.0001 eV precision. The paper's hidden/source comparator values are retained as an audit note (historical prose reported Ph 1.7347/3.1457; Figure 2 resolves Ph S1/T1 as 3.1457/1.7347; DA remains 2.9835/1.7284 eV); the current task separately assesses traceable state energies, their quantitative source comparability and the requested signed inequalities. Local feasibility does not certify exact source-number reproduction.",
  "status": "success",
  "systems": [
    {
      "geometry": {
        "basis": "6-31G(d,p)",
        "converged": true,
        "method": "B3LYP",
        "roots": "S0 neutral singlet; TD roots read from this optimized checkpoint",
        "software": "Gaussian 16",
        "spin_treatment": "charge 0, multiplicity 1",
        "stationary_point_evidence": "Optimization completed; 279 frequencies; NImag=0; input=docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/input.com; stdout=docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log; input_sha256=cbb2bff5443b70ce6cbf1171802138e05ff977d59d625d238df9df5e97d4cf21; stdout_sha256=c14084a692a88c3dcd55b1003c39f1861fcb32cbb84c65dd1ae2e40559ed6566"
      },
      "inequality_assessment": "2T1>S1: PASS (0.4239 eV); S1-T1>0.5 eV: PASS (1.3147 eV).",
      "s1_eV": 3.0533,
      "s1_minus_t1_eV": 1.3147000000000002,
      "system_id": "An-sigma-Ph",
      "t1_eV": 1.7386,
      "two_t1_minus_s1_eV": 0.4238999999999997,
      "validation": {
        "identity_check": "Manifest identity, charge 0 and multiplicity 1 retained; TD input uses the corresponding optimized checkpoint.",
        "provenance": "{\"geometry\": {\"basis\": \"6-31G(d,p)\", \"converged\": true, \"method\": \"B3LYP\", \"roots\": \"S0 neutral singlet; TD roots read from this optimized checkpoint\", \"software\": \"Gaussian 16\", \"spin_treatment\": \"charge 0, multiplicity 1\", \"stationary_point_evidence\": \"Optimization completed; 279 frequencies; NImag=0; input=docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/input.com; stdout=docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log; input_sha256=cbb2bff5443b70ce6cbf1171802138e05ff977d59d625d238df9df5e97d4cf21; stdout_sha256=c14084a692a88c3dcd55b1003c39f1861fcb32cbb84c65dd1ae2e40559ed6566\"}, \"singlet\": {\"case\": \"An_sigma_Ph_singlet\", \"checkpoint_sha256\": \"5ec250f31bee5105c2f6f69d70f1fa29b971391a3d1c6a87f53d692c18fed601\", \"input\": \"docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_...",
        "spin_check": "Singlet route has Singlet roots; triplet route has TD=(NStates=3,Triplets) and Triplet roots; both Gaussian jobs exit 0.",
        "state_assignment": "Lowest explicit singlet root S1=3.0533 eV and lowest explicit triplet root T1=1.7386 eV; root labels and <S**2> are present in stdout."
      }
    },
    {
      "geometry": {
        "basis": "6-31G(d,p)",
        "converged": true,
        "method": "B3LYP",
        "roots": "S0 neutral singlet; TD roots read from this optimized checkpoint",
        "software": "Gaussian 16",
        "spin_treatment": "charge 0, multiplicity 1",
        "stationary_point_evidence": "Optimization completed; 294 frequencies; NImag=0; input=docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/input.com; stdout=docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log; input_sha256=1849591c5ae9e34883b51472763816365e457e50e56f497efd9ab79e26a78a4d; stdout_sha256=c0bfe80cd3a3b7ef95653a312d9fbac08a011dbd67ecd35518ea0d69d96ff191"
      },
      "inequality_assessment": "2T1>S1: PASS (0.6406 eV); S1-T1>0.5 eV: PASS (1.0932 eV).",
      "s1_eV": 2.827,
      "s1_minus_t1_eV": 1.0932,
      "system_id": "An-sigma-DA",
      "t1_eV": 1.7338,
      "two_t1_minus_s1_eV": 0.6406000000000001,
      "validation": {
        "identity_check": "Manifest identity, charge 0 and multiplicity 1 retained; TD input uses the corresponding optimized checkpoint.",
        "provenance": "{\"geometry\": {\"basis\": \"6-31G(d,p)\", \"converged\": true, \"method\": \"B3LYP\", \"roots\": \"S0 neutral singlet; TD roots read from this optimized checkpoint\", \"software\": \"Gaussian 16\", \"spin_treatment\": \"charge 0, multiplicity 1\", \"stationary_point_evidence\": \"Optimization completed; 294 frequencies; NImag=0; input=docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/input.com; stdout=docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log; input_sha256=1849591c5ae9e34883b51472763816365e457e50e56f497efd9ab79e26a78a4d; stdout_sha256=c0bfe80cd3a3b7ef95653a312d9fbac08a011dbd67ecd35518ea0d69d96ff191\"}, \"singlet\": {\"case\": \"An_sigma_DA_singlet\", \"checkpoint_sha256\": \"7540b721eaffcf577a6e4dd1732bf9b1882eda71b642a79514cb1d44e0164e1f\", \"input\": \"docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_...",
        "spin_check": "Singlet route has Singlet roots; triplet route has TD=(NStates=3,Triplets) and Triplet roots; both Gaussian jobs exit 0.",
        "state_assignment": "Lowest explicit singlet root S1=2.8270 eV and lowest explicit triplet root T1=1.7338 eV; root labels and <S**2> are present in stdout."
      }
    }
  ]
}
```

Paper/SI document hashes:

- `papers/paper_3c058fa17fa7c54e/documents/main.pdf` — SHA-256 `38002008855a03bf3bd90f3315f0008ae9fff275c1305e6fca20494ff3850e86` (declared_match=True)

No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **20**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/status.json` — successful status record; SHA-256 `1f04783a4cc2b1b8fbe130834b1c28ae977eb9a199bcb3b43477b299e2d0d5a3`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/An_sigma_DA_s0_optfreq_parsed.json` — successful execution artifact; SHA-256 `175a191da5c90612884fd37172463774fdbc7224035591469350695f548a885f`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/collection.json` — successful execution artifact; SHA-256 `e64e41e8f1387141f0dd79a2ddaaf196e6fa67271cfedaf30d0b85f375257286`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/input.com` — successful execution artifact; SHA-256 `798c3c86e601a90bde7ca2c394e559b6465c4962536018a72db118d2412635ad`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/status.json` — successful status record; SHA-256 `1e557237791f59912c1a631dc36f20842530d8b4430c905920e10c36e3f77f04`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/An_sigma_Ph_s0_optfreq_parsed.json` — successful execution artifact; SHA-256 `327c841216551603a6f6c1171bbf17d93889e63c52b5c3d8f9ff2949354045a4`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/collection.json` — successful execution artifact; SHA-256 `6dc066df8034bbb044f87a01a2b8319a7431a93b07878e9d858811d7c0948dd7`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/input.com` — successful execution artifact; SHA-256 `1ba36bb408f16135aefd915446cd8f4bdcccc7acccad2b48ad27b1b51e0d6c81`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/native_workspace_batch/outputs/execution_jobs/job_020cec8eca3d423f9d2e4f3b3b9d1d8f/status.json` — successful status record; SHA-256 `1e557237791f59912c1a631dc36f20842530d8b4430c905920e10c36e3f77f04`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/native_workspace_batch/outputs/execution_jobs/job_020cec8eca3d423f9d2e4f3b3b9d1d8f/collection.json` — successful execution artifact; SHA-256 `6dc066df8034bbb044f87a01a2b8319a7431a93b07878e9d858811d7c0948dd7`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/native_workspace_batch/outputs/execution_jobs/job_020cec8eca3d423f9d2e4f3b3b9d1d8f/input.com` — successful execution artifact; SHA-256 `1ba36bb408f16135aefd915446cd8f4bdcccc7acccad2b48ad27b1b51e0d6c81`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/native_workspace_batch/outputs/execution_jobs/job_020cec8eca3d423f9d2e4f3b3b9d1d8f/request.json` — successful execution artifact; SHA-256 `95b6228ee41174edb830a19d867e01ff232541c874e8a3bf1ba8f1c1169415c9`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/native_workspace_batch/outputs/execution_jobs/job_020cec8eca3d423f9d2e4f3b3b9d1d8f/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/native_workspace_batch/outputs/execution_jobs/job_efd6ab36517046de9aaffa8dfcdbd51c/status.json` — successful status record; SHA-256 `1f04783a4cc2b1b8fbe130834b1c28ae977eb9a199bcb3b43477b299e2d0d5a3`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/native_workspace_batch/outputs/execution_jobs/job_efd6ab36517046de9aaffa8dfcdbd51c/collection.json` — successful execution artifact; SHA-256 `e64e41e8f1387141f0dd79a2ddaaf196e6fa67271cfedaf30d0b85f375257286`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/native_workspace_batch/outputs/execution_jobs/job_efd6ab36517046de9aaffa8dfcdbd51c/input.com` — successful execution artifact; SHA-256 `798c3c86e601a90bde7ca2c394e559b6465c4962536018a72db118d2412635ad`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/native_workspace_batch/outputs/execution_jobs/job_efd6ab36517046de9aaffa8dfcdbd51c/request.json` — successful execution artifact; SHA-256 `f668e53b87fa59cc1aae61d90e113f2c51ee4fe0c69785148eec603c00a3dd35`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/native_workspace_batch/outputs/execution_jobs/job_efd6ab36517046de9aaffa8dfcdbd51c/stderr.log` — successful execution artifact; SHA-256 `26d422b0a44e4f756144e1c3fde97aaeb3b0e308dc74279a303e17249c0bfa25`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/status.json` — label=group_4 paper_3c058fa17fa7c54e An_sigma_Ph_s0_optfreq; submitted_at=2026-08-29T17:55:25.305989+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d,p) Opt=(Tight,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/An_sigma_Ph_s0_optfreq.chk`
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/An_sigma_Ph_s0_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/input.com`
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_Ph_s0_optfreq/stdout.log`
2. `artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/status.json` — label=group_4 paper_3c058fa17fa7c54e An_sigma_DA_s0_optfreq; submitted_at=2026-08-29T17:55:25.338920+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d,p) Opt=(Tight,MaxCycles=300) Freq NoSymm SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/An_sigma_DA_s0_optfreq.chk`
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/An_sigma_DA_s0_optfreq_parsed.json`
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/collection.json`
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/input.com`
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/stderr.log`
   - output: `docs/verification/group_4/paper_3c058fa17fa7c54e/artifacts/gaussian_batch/An_sigma_DA_s0_optfreq/stdout.log`

## Evaluator alignment

- Key-point IDs: `kp_geometry, kp_states, kp_energies`
- Conclusion IDs: `c_final`
- Scoring-rule IDs: `r_geometry, r_states, r_energies, r_final`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `QUALIFIED` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_geometry` → reference `kp_geometry`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert process validation; evaluator_target_present=False
- rule `r_states` → reference `kp_states`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert process validation; evaluator_target_present=False
- rule `r_energies` → reference `kp_energies`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison with source values or bounded-failure validation; evaluator_target_present=False
- rule `r_final` → reference `c_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].geometry` / result path `$.systems[].geometry.method` = `"B3LYP"`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].geometry` / result path `$.systems[].geometry.basis` = `"6-31G(d,p)"`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].geometry` / result path `$.systems[].geometry.software` = `"Gaussian 16"`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].geometry` / result path `$.systems[].geometry.roots` = `"S0 neutral singlet; TD roots read from this optimized checkpoint"`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].geometry` / result path `$.systems[].geometry.spin_treatment` = `"charge 0, multiplicity 1"`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].geometry` / result path `$.systems[].geometry.converged` = `true`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].geometry` / result path `$.systems[].geometry.stationary_point_evidence` = `"Optimization completed; 279 frequencies; NImag=0; input=docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfr..."`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].geometry` / result path `$.systems[].geometry.stationary_point_evidence` = `"Optimization completed; 294 frequencies; NImag=0; input=docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfr..."`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].validation` / result path `$.systems[].validation.identity_check` = `"Manifest identity, charge 0 and multiplicity 1 retained; TD input uses the corresponding optimized checkpoint."`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].validation` / result path `$.systems[].validation.state_assignment` = `"Lowest explicit singlet root S1=3.0533 eV and lowest explicit triplet root T1=1.7386 eV; root labels and <S**2> are present in stdout."`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].validation` / result path `$.systems[].validation.spin_check` = `"Singlet route has Singlet roots; triplet route has TD=(NStates=3,Triplets) and Triplet roots; both Gaussian jobs exit 0."`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].validation` / result path `$.systems[].validation.provenance` = `"{\"geometry\": {\"basis\": \"6-31G(d,p)\", \"converged\": true, \"method\": \"B3LYP\", \"roots\": \"S0 neutral singlet; TD roots read from this optimized checkpoint\", \"software\": \"Gaussian 16\", \"spin_treatment\": \"charge 0, multiplicity 1\", \"stationary_..."`
- rule `r_geometry` / reference `kp_geometry` / field `$.systems[].validation` / result path `$.systems[].validation.state_assignment` = `"Lowest explicit singlet root S1=2.8270 eV and lowest explicit triplet root T1=1.7338 eV; root labels and <S**2> are present in stdout."`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].system_id` = `"An-sigma-Ph"`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].s1_eV` = `3.0533`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].t1_eV` = `1.7386`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].s1_minus_t1_eV` = `1.3147000000000002`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].two_t1_minus_s1_eV` = `0.4238999999999997`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].inequality_assessment` = `"2T1>S1: PASS (0.4239 eV); S1-T1>0.5 eV: PASS (1.3147 eV)."`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].system_id` = `"An-sigma-DA"`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].s1_eV` = `2.827`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].t1_eV` = `1.7338`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].s1_minus_t1_eV` = `1.0932`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].two_t1_minus_s1_eV` = `0.6406000000000001`
- rule `r_energies` / reference `kp_energies` / field `$.systems[]` / result path `$.systems[].inequality_assessment` = `"2T1>S1: PASS (0.6406 eV); S1-T1>0.5 eV: PASS (1.0932 eV)."`
- rule `r_final` / reference `c_final` / field `$.conclusion` / result path `$.conclusion` = `"Both An-sigma-Ph and An-sigma-DA satisfy 2T1>S1 and S1-T1>0.5 eV in the submitted B3LYP/6-31G(d,p) model, supporting the evaluator's TTA energetic conclusion within the model and with the stated mechanistic limitation."`
- rule `r_final` / reference `c_final` / field `$.sensitivity` / result path `$.sensitivity` = `"The same four exact-route TD calculations first passed the local stability gate and then terminated normally on HPC. Local and HPC lowest-root energies agree to the reported 0.0001 eV precision. The paper's hidden/source comparator value..."`
- rule `r_final` / reference `c_final` / field `$.coverage` / result path `$.coverage` = `"Both named systems, optimized S0 minima, explicit lowest singlet/triplet roots, both derived gaps, and both evaluator inequalities are covered. No claim is made that energetics alone prove the TTA mechanism."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: autonomous boundary weakened
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Public systematic molecular names, formulas, charge and multiplicity.

Public input files and hashes:

- `agent_input/data/inputs/molecule_manifest.json` — SHA-256 `2775b4e0be25af7cbf1250a24efea84cde4ed5ff8aabc1ebc71dd44c82f3fede`; size=506 bytes; explicit_boundary_fields={"$.systems[0].charge": 0, "$.systems[0].formula": "C55H34F6", "$.systems[0].ground_state_multiplicity": 1, "$.systems[1].charge": 0, "$.systems[1].formula": "C57H35F6NO", "$.systems[1].ground_state_multiplicity": 1}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_4/paper_3c058fa17fa7c54e/verification_report.md` — verification record; SHA-256 `476f8e714765207020807e46cb8870952661ffa6731d3b76d97259295d89467f`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/report/results.json` — verification record; SHA-256 `244e86b934978cd846bf38d19afc59f53e2f983e7a61ceccd0fd3e8bd0d2cf55`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/input.com` — referenced successful evidence; SHA-256 `1849591c5ae9e34883b51472763816365e457e50e56f497efd9ab79e26a78a4d`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_DA_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log` — referenced successful evidence; SHA-256 `c0bfe80cd3a3b7ef95653a312d9fbac08a011dbd67ecd35518ea0d69d96ff191`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/input.com` — referenced successful evidence; SHA-256 `cbb2bff5443b70ce6cbf1171802138e05ff977d59d625d238df9df5e97d4cf21`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/An_sigma_Ph_author_b3lyp_d3bj_optfreq_hpc20_p6/stdout.log` — referenced successful evidence; SHA-256 `c14084a692a88c3dcd55b1003c39f1861fcb32cbb84c65dd1ae2e40559ed6566`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/input.com` — referenced successful evidence; SHA-256 `89ea6cf83f18d923f39e835258b0de590cb12c7b79197ffbc823c6ccbcb3e2a7`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_singlet/stdout.log` — referenced successful evidence; SHA-256 `5592423f10cb61ca2b786c8ef509fb30479fcb1454d65a8b463459b461a76876`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/input.com` — referenced successful evidence; SHA-256 `ace2a744a1efd2c3693ea9e4c4d33cf9f3ad2be82d59a205eb0cc72c7198a74c`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_DA_triplet/stdout.log` — referenced successful evidence; SHA-256 `ce328f666d0c989eac933ff1585c04e6509ac004323168dfcbc105505b15d510`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/input.com` — referenced successful evidence; SHA-256 `3e02a95b653f2b1a75170e8efd2bcb31c4aa63dbb92099be25ab1a90c70dadd4`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_singlet/stdout.log` — referenced successful evidence; SHA-256 `d15c8e48c12a34eb3b77b6fdffdff6a76a1c588bb83c1465eb2c8113b9f56b7b`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/input.com` — referenced successful evidence; SHA-256 `82872f1d6518c14be16095d045abb2b07a109741795ed18f25e2d812ecd3614a`
- `docs/verification/group_4/paper_3c058fa17fa7c54e/hpc_runs/td_exact_route_hpc20_p6_20260910_attempt6_shellfix/An_sigma_Ph_triplet/stdout.log` — referenced successful evidence; SHA-256 `bd8f73fb747992360d617076c122a49ee1ea84539d4387ca06adbd7a9a05b8c1`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
