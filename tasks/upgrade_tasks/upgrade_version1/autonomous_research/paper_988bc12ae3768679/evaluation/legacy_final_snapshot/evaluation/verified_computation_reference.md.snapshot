# Verified computation reference — paper_988bc12ae3768679 (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 4 | `PASS` | 最终严格状态：**PASS**。使用论文/SI 提供的 S0 Cartesian 几何，按作者 CAM-B3LYP/6-31+G(d) 气相 TDDFT 路线分别完成 +2 singlet acid（62 atoms）和 -2 singlet base（58 atoms）的 S1-S4。两个作业均正常终止，且未把早期错误的中性/PCM 探索作业纳入结果。 |
| 59 | `PASS` | 本篇 acid/base 作者路线端点、四态光谱和 evaluator 科学闸门均已闭合，最终严格判定为 **PASS**。 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Symmetric azobenzene-substituted diketopyrrolopyrroles dyes as acid-base switchable molecular-probe for colorimetric paper-based sensors
- DOI: `10.1016/j.dyepig.2025.113288`
- Task package: `tasks/final_verified_autonomous_research/paper_988bc12ae3768679`
- Verification group: `docs/verification/group_3/paper_988bc12ae3768679`
- Paper documents: `papers/paper_988bc12ae3768679`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": "Brightest-state energies: 2a-acid=2.9342 eV; 2a-base=1.9892 eV.",
  "conclusion": "The calculated gas-phase vertical profiles are compared by brightest-state energy; a lower-energy base brightest transition supports the qualitative acid/base chromatic-switch interpretation within this boundary.",
  "limitations": "Gas-phase vertical excitations only; no solvent, vibronic, counterion or experimental band fitting. Earlier neutral/PCM exploratory jobs are excluded because their charge and phase violate the public endpoint.",
  "method": {
    "brightest_state_rule": "Within each S1-S4 set, select the state with maximum Gaussian oscillator strength.",
    "electronic_structure": "CAM-B3LYP/6-31+G(d,p) TD(Singlets,NStates=4) gas-phase vertical excitations",
    "geometry_treatment": "Supplied complete acid/base author S0 geometries; no geometry change",
    "software": "Gaussian 16 C.01; cclib parser",
    "state_coverage": "Four singlet states S1-S4 for each structure"
  },
  "structures": [
    {
      "brightest_state": "S3",
      "charge": 2,
      "input_validation": {
        "atom_count": 62,
        "converged": true,
        "geometry_provenance": "unchanged public S0 XYZ; gas-phase vertical endpoint; artifact artifacts/gaussian/acid_p2_gas_td4/stdout.log"
      },
      "multiplicity": 1,
      "name": "2a-acid",
      "states": [
        {
          "energy_eV": 2.5888,
          "gaussian_label": "Singlet-?Sym",
          "label": "S1",
          "oscillator_strength": 0.0009,
          "wavelength_nm": 478.9253646477132
        },
        {
          "energy_eV": 2.5974,
          "gaussian_label": "Singlet-?Sym",
          "label": "S2",
          "oscillator_strength": 0.0001,
          "wavelength_nm": 477.33964117964115
        },
        {
          "energy_eV": 2.9342,
          "gaussian_label": "Singlet-?Sym",
          "label": "S3",
          "oscillator_strength": 2.6631,
          "wavelength_nm": 422.548559743712
        },
        {
          "energy_eV": 2.9999,
          "gaussian_label": "Singlet-?Sym",
          "label": "S4",
          "oscillator_strength": 0.0027,
          "wavelength_nm": 413.29443781459383
        }
      ]
    },
    {
      "brightest_state": "S1",
      "charge": -2,
      "input_validation": {
        "atom_count": 58,
        "converged": true,
        "geometry_provenance": "unchanged public S0 XYZ; gas-phase vertical endpoint; artifact artifacts/gaussian/base_m2_gas_td4/stdout.log"
      },
      "multiplicity": 1,
      "name": "2a-base",
      "states": [
        {
          "energy_eV": 1.9892,
          "gaussian_label": "Singlet-?Sym",
          "label": "S1",
          "oscillator_strength": 2.2515,
          "wavelength_nm": 623.28674039815
        },
        {
          "energy_eV": 2.2631,
          "gaussian_label": "Singlet-?Sym",
          "label": "S2",
          "oscillator_strength": 0.0083,
          "wavelength_nm": 547.8511705183155
        },
        {
          "energy_eV": 2.8849,
          "gaussian_label": "Singlet-?Sym",
          "label": "S3",
          "oscillator_strength": 0.0001,
          "wavelength_nm": 429.7694838642587
        },
        {
          "energy_eV": 2.8955,
          "gaussian_label": "Singlet-?Sym",
          "label": "S4",
          "oscillator_strength": 0.0,
          "wavelength_nm": 428.1961609393887
        }
      ]
    }
  ]
}
```

Paper/SI document hashes:

- `papers/paper_988bc12ae3768679/documents/main.pdf` — SHA-256 `8ee6c2620ae4107f7fd8043982eb478ffa01714734e69416a7b186e9ff32e189` (declared_match=True)

Report evidence lines retained:

- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |
- 独立计算完成后才读取 evaluator 对照；acid/base 两套气相 CAM-B3LYP/6-31+G(d) S1–S4 光谱、最亮态和能量排序均已由原始输出闭合并与 evaluator 一致。
- 本篇 acid/base 作者路线端点、四态光谱和 evaluator 科学闸门均已闭合，最终严格判定为 **PASS**。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **60**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/status.json` — successful status record; SHA-256 `97edeb5b01014af4d035964d47cad5afb9aadf305bfba00024d9905a618c2ccd`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/acid_p2_gas_td4_optimized.xyz` — successful execution artifact; SHA-256 `b66351d1f4e3b0013a2b3e4b9e6d31cf11153ec9c317a936e1043264557c9ff6`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/collection.json` — successful execution artifact; SHA-256 `08483fca3265064b3e20e3074a60e9ce02d2f28630ceddfaa919fd454b615514`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/formchk.log` — successful execution artifact; SHA-256 `597af31a5394846865cadbce48496732b47a62f9be1473a1b05c343a27d43117`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/input.com` — successful execution artifact; SHA-256 `b1454568ccaf88069c355f1f3f5d62d78ed8b63f53519932f2f48128f5593956`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/status.json` — successful status record; SHA-256 `c233caecd389ed07b56418f02d184636597305af5edd0851627a02366b14722b`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/acid_td_optimized.xyz` — successful execution artifact; SHA-256 `05006f9472c9779e53c2364c0b1212cee163c7ae59ffe876342c3662d9882873`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/collection.json` — successful execution artifact; SHA-256 `2e6332eb30c773690f79d305f5c4f66c0fb911b8ec7d451e6281c6a1123df22a`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/formchk.log` — successful execution artifact; SHA-256 `9107195e5bc67128d7dfb4937a06506a742938d1285d29b9ea2a990444c2942c`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/input.com` — successful execution artifact; SHA-256 `3931bd49f9499a74f878d52282aa3d455132838896f8bea1c7e2848084e4835e`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/status.json` — successful status record; SHA-256 `546f302a205ba9fcdb6e35924a4405ea6a33a20ee0069ef1f087d22f3fb0177a`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/acid_td_td4_optimized.xyz` — successful execution artifact; SHA-256 `8d914b58300661ecebc1dcc06e984c79791728e4e163d0d8f83f11c926066453`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/collection.json` — successful execution artifact; SHA-256 `ff48ac4c76a8baf6db10cff57116b952e005a8d116a4195a604f1b39de10ddc4`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/formchk.log` — successful execution artifact; SHA-256 `52ff6ff1715ba5c723b52570bca72f58c088e8cd120fea9206caf1dcd628f062`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/input.com` — successful execution artifact; SHA-256 `c06efd32dc33116b0c9c9cdf5a0eabfb505199b58bf3e7d296d04acc935167d2`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/status.json` — successful status record; SHA-256 `961a18df0d7ce35eb2441ed399990c4b8704089c4ef56159bfeaa46304ff1ea6`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/base_m2_gas_td4_optimized.xyz` — successful execution artifact; SHA-256 `60137b0272ac49c2791225227d065b072ca59a1319ef5114201a61bb47353200`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/collection.json` — successful execution artifact; SHA-256 `cb0620060f36bcd7dd63738953dec14bf46e695f8092e64e30b829fbc7b3c19e`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/formchk.log` — successful execution artifact; SHA-256 `177349ffcea80d33775d7506f4cd41d26946616f9fea3e7020386f5f63e2e903`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/input.com` — successful execution artifact; SHA-256 `d3a0848465d1ed04fd3afd7b8239cc998aa4d9e02e2226f2533d3a74da3d6c1d`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/status.json` — successful status record; SHA-256 `3713fa58ce3f7c9863b593bf813b3c054524c81c07f1ddcc4eb5f2656a437269`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/base_td_optimized.xyz` — successful execution artifact; SHA-256 `66a2aa72281142b7d1ae08b25fb5f8ba700057b6610752ab846c9409070ee5f9`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/collection.json` — successful execution artifact; SHA-256 `48245d2dd07e79798b08090d586f4f89be39e4814356e6c2ae4482120f0402d8`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/formchk.log` — successful execution artifact; SHA-256 `3516a8739cf4553389809c0cdf932a89e2429a74bdbbbb3fa764b5ef2432b671`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/input.com` — successful execution artifact; SHA-256 `ef219bd0438fa787cfdddf55f3aab2c07374b53568077b8cd895ee64a16bc23a`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/status.json` — successful status record; SHA-256 `fafea56cee3ac861371c53ac30d07d8b928dbc68640fddac8d54e02a8d39ed54`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/base_td_td4_optimized.xyz` — successful execution artifact; SHA-256 `e2e47a03e8685543d2af490e09194df7eefc66e2f734f87ef0734164b424677e`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/collection.json` — successful execution artifact; SHA-256 `8670e18a469b73cba324bb33e3b4f3adccddc53aa3d126b4f05ce613c7771445`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/formchk.log` — successful execution artifact; SHA-256 `03041aaeec78052b234d88a5266171ad4bb345e633a8466fb7524229d1e5ba32`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/input.com` — successful execution artifact; SHA-256 `8c731e8e32e188a3d5db7fd94bc2bb2494f279c976149ace772a775d32be98a0`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_p2_gas_td4/outputs/execution_jobs/job_92c82311b04347d7b2b91f95493d3887/status.json` — successful status record; SHA-256 `97edeb5b01014af4d035964d47cad5afb9aadf305bfba00024d9905a618c2ccd`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_p2_gas_td4/outputs/execution_jobs/job_92c82311b04347d7b2b91f95493d3887/collection.json` — successful execution artifact; SHA-256 `08483fca3265064b3e20e3074a60e9ce02d2f28630ceddfaa919fd454b615514`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_p2_gas_td4/outputs/execution_jobs/job_92c82311b04347d7b2b91f95493d3887/input.com` — successful execution artifact; SHA-256 `b1454568ccaf88069c355f1f3f5d62d78ed8b63f53519932f2f48128f5593956`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_p2_gas_td4/outputs/execution_jobs/job_92c82311b04347d7b2b91f95493d3887/request.json` — successful execution artifact; SHA-256 `827f72283cca47146a2e41920f468cef662f20befd8fb72db8cdfcb2cdd3d856`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_p2_gas_td4/outputs/execution_jobs/job_92c82311b04347d7b2b91f95493d3887/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td/outputs/execution_jobs/job_cd7798863d5b44af8d72ce2c1dbe37e2/status.json` — successful status record; SHA-256 `c233caecd389ed07b56418f02d184636597305af5edd0851627a02366b14722b`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td/outputs/execution_jobs/job_cd7798863d5b44af8d72ce2c1dbe37e2/collection.json` — successful execution artifact; SHA-256 `2e6332eb30c773690f79d305f5c4f66c0fb911b8ec7d451e6281c6a1123df22a`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td/outputs/execution_jobs/job_cd7798863d5b44af8d72ce2c1dbe37e2/input.com` — successful execution artifact; SHA-256 `3931bd49f9499a74f878d52282aa3d455132838896f8bea1c7e2848084e4835e`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td/outputs/execution_jobs/job_cd7798863d5b44af8d72ce2c1dbe37e2/request.json` — successful execution artifact; SHA-256 `55282771dfa8100f2bb181bf0d37911658d8a074092e57ebef00ad8521b8bb30`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td/outputs/execution_jobs/job_cd7798863d5b44af8d72ce2c1dbe37e2/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td_td4/outputs/execution_jobs/job_5a8f59fa978b48a2a1e8ffbe8932166c/status.json` — successful status record; SHA-256 `546f302a205ba9fcdb6e35924a4405ea6a33a20ee0069ef1f087d22f3fb0177a`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td_td4/outputs/execution_jobs/job_5a8f59fa978b48a2a1e8ffbe8932166c/collection.json` — successful execution artifact; SHA-256 `ff48ac4c76a8baf6db10cff57116b952e005a8d116a4195a604f1b39de10ddc4`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td_td4/outputs/execution_jobs/job_5a8f59fa978b48a2a1e8ffbe8932166c/input.com` — successful execution artifact; SHA-256 `c06efd32dc33116b0c9c9cdf5a0eabfb505199b58bf3e7d296d04acc935167d2`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td_td4/outputs/execution_jobs/job_5a8f59fa978b48a2a1e8ffbe8932166c/request.json` — successful execution artifact; SHA-256 `a928c1756cee554115f4e00c0a930ba1623ef533922699d31ab830832b4ca392`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/acid_td_td4/outputs/execution_jobs/job_5a8f59fa978b48a2a1e8ffbe8932166c/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_m2_gas_td4/outputs/execution_jobs/job_69408b8068b24a0593e39a07cd0225c8/status.json` — successful status record; SHA-256 `961a18df0d7ce35eb2441ed399990c4b8704089c4ef56159bfeaa46304ff1ea6`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_m2_gas_td4/outputs/execution_jobs/job_69408b8068b24a0593e39a07cd0225c8/collection.json` — successful execution artifact; SHA-256 `cb0620060f36bcd7dd63738953dec14bf46e695f8092e64e30b829fbc7b3c19e`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_m2_gas_td4/outputs/execution_jobs/job_69408b8068b24a0593e39a07cd0225c8/input.com` — successful execution artifact; SHA-256 `d3a0848465d1ed04fd3afd7b8239cc998aa4d9e02e2226f2533d3a74da3d6c1d`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_m2_gas_td4/outputs/execution_jobs/job_69408b8068b24a0593e39a07cd0225c8/request.json` — successful execution artifact; SHA-256 `04f3b89bb49d8509f4cc42b593148847aafa64e641d501c3ca1f6cfce2351147`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_m2_gas_td4/outputs/execution_jobs/job_69408b8068b24a0593e39a07cd0225c8/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td/outputs/execution_jobs/job_d730ce92732045c99382b6cf9b06ce7d/status.json` — successful status record; SHA-256 `3713fa58ce3f7c9863b593bf813b3c054524c81c07f1ddcc4eb5f2656a437269`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td/outputs/execution_jobs/job_d730ce92732045c99382b6cf9b06ce7d/collection.json` — successful execution artifact; SHA-256 `48245d2dd07e79798b08090d586f4f89be39e4814356e6c2ae4482120f0402d8`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td/outputs/execution_jobs/job_d730ce92732045c99382b6cf9b06ce7d/input.com` — successful execution artifact; SHA-256 `ef219bd0438fa787cfdddf55f3aab2c07374b53568077b8cd895ee64a16bc23a`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td/outputs/execution_jobs/job_d730ce92732045c99382b6cf9b06ce7d/request.json` — successful execution artifact; SHA-256 `0740035c84c5fe1ae69b9d0ae52825c90ec563722cfdf78565e2030208298937`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td/outputs/execution_jobs/job_d730ce92732045c99382b6cf9b06ce7d/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td_td4/outputs/execution_jobs/job_5aa6abeff057475ea957b5a466633840/status.json` — successful status record; SHA-256 `fafea56cee3ac861371c53ac30d07d8b928dbc68640fddac8d54e02a8d39ed54`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td_td4/outputs/execution_jobs/job_5aa6abeff057475ea957b5a466633840/collection.json` — successful execution artifact; SHA-256 `8670e18a469b73cba324bb33e3b4f3adccddc53aa3d126b4f05ce613c7771445`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td_td4/outputs/execution_jobs/job_5aa6abeff057475ea957b5a466633840/input.com` — successful execution artifact; SHA-256 `8c731e8e32e188a3d5db7fd94bc2bb2494f279c976149ace772a775d32be98a0`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td_td4/outputs/execution_jobs/job_5aa6abeff057475ea957b5a466633840/request.json` — successful execution artifact; SHA-256 `465772304d6137c6a7b27a5a9e9a87d24a808f0f066299b7e0c747cf3349501b`
- `docs/verification/group_3/paper_988bc12ae3768679/native_workspace/base_td_td4/outputs/execution_jobs/job_5aa6abeff057475ea957b5a466633840/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/base_td/status.json` — label=group_3 paper_988bc12ae3768679 base_td; submitted_at=2026-08-29T07:42:30.795787+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/base_td.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/base_td.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/base_td_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td/stderr.log`
2. `artifacts/gaussian/acid_td/status.json` — label=group_3 paper_988bc12ae3768679 acid_td; submitted_at=2026-08-29T07:42:31.538047+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/acid_td.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/acid_td.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/acid_td_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td/stderr.log`
3. `artifacts/gaussian/acid_td_td4/status.json` — label=group_3 paper_988bc12ae3768679 acid_td_td4; submitted_at=2026-08-29T15:53:50.955091+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD(NStates=4) SCRF=(PCM,Solvent=Water) Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/acid_td_td4.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/acid_td_td4.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/acid_td_td4_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_td_td4/stderr.log`
4. `artifacts/gaussian/base_td_td4/status.json` — label=group_3 paper_988bc12ae3768679 base_td_td4; submitted_at=2026-08-29T15:53:51.733918+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD(NStates=4) SCRF=(PCM,Solvent=Water) Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/base_td_td4.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/base_td_td4.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/base_td_td4_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_td_td4/stderr.log`
5. `artifacts/gaussian/acid_p2_gas_td4/status.json` — label=group_3 paper_988bc12ae3768679 acid_p2_gas_td4; submitted_at=2026-08-30T02:13:11.951180+00:00; software=gaussian; intent=single_point; route=#p CAM-B3LYP/6-31+G(d,p) TD=(Singlets,NStates=4) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/acid_p2_gas_td4.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/acid_p2_gas_td4.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/acid_p2_gas_td4_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/stderr.log`
6. `artifacts/gaussian/base_m2_gas_td4/status.json` — label=group_3 paper_988bc12ae3768679 base_m2_gas_td4; submitted_at=2026-08-30T02:13:16.466203+00:00; software=gaussian; intent=single_point; route=#p CAM-B3LYP/6-31+G(d,p) TD=(Singlets,NStates=4) NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/base_m2_gas_td4.chk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/base_m2_gas_td4.fchk`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/base_m2_gas_td4_optimized.xyz`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/collection.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/formchk.log`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/input.com`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/parsed_observables.json`
   - output: `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/stderr.log`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `ar_limitations`, `ar_r6`.

- Key-point IDs: `ar_process_inputs, ar_process_coverage, ar_result_acid, ar_result_base`
- Conclusion IDs: `ar_final_switch, ar_limitations`
- Scoring-rule IDs: `ar_r1, ar_r2, ar_r3, ar_r4, ar_r5, ar_r6`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `ar_r1` → reference `ar_process_inputs`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert validation; evaluator_target_present=False
- rule `ar_r2` → reference `ar_process_coverage`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert validation; evaluator_target_present=False
- rule `ar_r3` → reference `ar_result_acid`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=state identity and numeric comparison; evaluator_target_present=False
- rule `ar_r4` → reference `ar_result_base`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=state identity and numeric comparison; evaluator_target_present=False
- rule `ar_r5` → reference `ar_final_switch`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `ar_r6` → reference `ar_limitations`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].name` = `"2a-acid"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].charge` = `2`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].multiplicity` = `1`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].input_validation.atom_count` = `62`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].input_validation.geometry_provenance` = `"unchanged public S0 XYZ; gas-phase vertical endpoint; artifact artifacts/gaussian/acid_p2_gas_td4/stdout.log"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].input_validation.converged` = `true`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[0].label` = `"S1"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[0].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[0].energy_eV` = `2.5888`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[0].wavelength_nm` = `478.9253646477132`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[0].oscillator_strength` = `0.0009`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[1].label` = `"S2"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[1].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[1].energy_eV` = `2.5974`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[1].wavelength_nm` = `477.33964117964115`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[1].oscillator_strength` = `0.0001`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[2].label` = `"S3"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[2].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[2].energy_eV` = `2.9342`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[2].wavelength_nm` = `422.548559743712`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[2].oscillator_strength` = `2.6631`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[3].label` = `"S4"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[3].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[3].energy_eV` = `2.9999`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[3].wavelength_nm` = `413.29443781459383`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].states[3].oscillator_strength` = `0.0027`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[0].brightest_state` = `"S3"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].name` = `"2a-base"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].charge` = `-2`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].multiplicity` = `1`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].input_validation.atom_count` = `58`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].input_validation.geometry_provenance` = `"unchanged public S0 XYZ; gas-phase vertical endpoint; artifact artifacts/gaussian/base_m2_gas_td4/stdout.log"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].input_validation.converged` = `true`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[0].label` = `"S1"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[0].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[0].energy_eV` = `1.9892`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[0].wavelength_nm` = `623.28674039815`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[0].oscillator_strength` = `2.2515`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[1].label` = `"S2"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[1].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[1].energy_eV` = `2.2631`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[1].wavelength_nm` = `547.8511705183155`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[1].oscillator_strength` = `0.0083`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[2].label` = `"S3"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[2].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[2].energy_eV` = `2.8849`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[2].wavelength_nm` = `429.7694838642587`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[2].oscillator_strength` = `0.0001`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[3].label` = `"S4"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[3].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[3].energy_eV` = `2.8955`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[3].wavelength_nm` = `428.1961609393887`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].states[3].oscillator_strength` = `0.0`
- rule `ar_r1` / reference `ar_process_inputs` / field `$.structures` / result path `$.structures[1].brightest_state` = `"S1"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].label` = `"S1"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].energy_eV` = `2.5888`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].wavelength_nm` = `478.9253646477132`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].oscillator_strength` = `0.0009`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].label` = `"S2"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].energy_eV` = `2.5974`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].wavelength_nm` = `477.33964117964115`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].oscillator_strength` = `0.0001`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].label` = `"S3"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].energy_eV` = `2.9342`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].wavelength_nm` = `422.548559743712`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].oscillator_strength` = `2.6631`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].label` = `"S4"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].gaussian_label` = `"Singlet-?Sym"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].energy_eV` = `2.9999`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].wavelength_nm` = `413.29443781459383`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].oscillator_strength` = `0.0027`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].energy_eV` = `1.9892`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].wavelength_nm` = `623.28674039815`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[0].oscillator_strength` = `2.2515`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].energy_eV` = `2.2631`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].wavelength_nm` = `547.8511705183155`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[1].oscillator_strength` = `0.0083`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].energy_eV` = `2.8849`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].wavelength_nm` = `429.7694838642587`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[2].oscillator_strength` = `0.0001`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].energy_eV` = `2.8955`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].wavelength_nm` = `428.1961609393887`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].states` / result path `$.structures[*].states[3].oscillator_strength` = `0.0`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].brightest_state` / result path `$.structures[*].brightest_state` = `"S3"`
- rule `ar_r2` / reference `ar_process_coverage` / field `$.structures[*].brightest_state` / result path `$.structures[*].brightest_state` = `"S1"`
- rule `ar_r5` / reference `ar_final_switch` / field `$.comparison` / result path `$.comparison` = `"Brightest-state energies: 2a-acid=2.9342 eV; 2a-base=1.9892 eV."`
- rule `ar_r5` / reference `ar_final_switch` / field `$.conclusion` / result path `$.conclusion` = `"The calculated gas-phase vertical profiles are compared by brightest-state energy; a lower-energy base brightest transition supports the qualitative acid/base chromatic-switch interpretation within this boundary."`
- rule `ar_r6` / reference `ar_limitations` / field `$.limitations` / result path `$.limitations` = `"Gas-phase vertical excitations only; no solvent, vibronic, counterion or experimental band fitting. Earlier neutral/PCM exploratory jobs are excluded because their charge and phase violate the public endpoint."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized/final structure is exposed as agent input for a scored comparison; redesign with neutral or independently generated starting geometry
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Complete XYZ geometries for named 2a-acid (+2, singlet) and 2a-base (-2, singlet) S0 structures.

Public input files and hashes:

- `agent_input/data/inputs/2a-acid.xyz` — SHA-256 `97e77fb559a4358b103df2fb1b1d8a1287c3744158bb3c7b55e70dd021403695`; size=4238 bytes; xyz_atom_count=62; xyz_comment=2a-acid Provided Cartesian geometry (angstrom); explicit_boundary_fields={"units_hint": "explicit angstrom marker"}
- `agent_input/data/inputs/2a-base.xyz` — SHA-256 `55e0e8ae86e4bf6aa39d33c313d30e82e6044a4ff8e6b31effca5a9cd623490e`; size=3960 bytes; xyz_atom_count=58; xyz_comment=2a-base Provided Cartesian geometry (angstrom); explicit_boundary_fields={"units_hint": "explicit angstrom marker"}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_988bc12ae3768679/verification_report.md` — verification record; SHA-256 `422c9a2d064e2c7203428ad6f232de484912e1c7304b63d29de7a57062f81987`
- `docs/verification/group_3/paper_988bc12ae3768679/report/results.json` — verification record; SHA-256 `f40049c6d112e5e1af72df5075f1cce643a5e209e8ffa67b9d1a3ec1df59373e`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/acid_p2_gas_td4/stdout.log` — referenced successful evidence; SHA-256 `ace4a1a89048726ebc75a07317520c01463a8ee0b805a8147c44433e0c139fa4`
- `docs/verification/group_3/paper_988bc12ae3768679/artifacts/gaussian/base_m2_gas_td4/stdout.log` — referenced successful evidence; SHA-256 `5669b89b9807dd2c73a1350179dedd9c9c73ffe7454176f01388ed71d6c80684`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
