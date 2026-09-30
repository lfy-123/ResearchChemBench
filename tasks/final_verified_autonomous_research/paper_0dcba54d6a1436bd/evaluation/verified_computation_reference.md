# Verified computation reference — paper_0dcba54d6a1436bd (autonomous_research)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `success` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **APPLICABLE_TO_CURRENT_FINAL**
- Applicability note: No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 9 | `PASS` | - 论文复现/最终判定：**PASS**。两套作者路线均正常终止，S0 为零虚频 minima，S1–S5 能量、波长、振子强度及顺序逐项符合 SI；保存的 S1 NTO hole/electron cube 给出明确的空间分离。 |
| 51 | `PASS` | 严格结论：作者路线的中间结论（两个 S0 minima、五个逐态垂直激发、dominant configurations、S1 NTO 空间分离）和最终结论（两套 SI 光谱被复现并支持 ICT-like S1）均由实际计算得到且与 evaluation 一致，本篇为 **PASS**。 |
| 106 | `PASS` | 本篇所有作者路线端点及 evaluation 科学闸门均已闭合，最终判定为 **PASS**。 |
| 112 | `PASS` | 论文复现结论： **PASS**（结构化结果对象已满足本篇定义的终态科学闸门；详细数值与原始证据见 report/results.json、artifacts/gaussian/ 和 provenance/。） |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Diketone Acceptor Modulation as a Structural Design Strategy for Tunable Carbazole–Cyanostilbene Emitters
- DOI: `10.1021/acs.joc.5c02866`
- Task package: `tasks/final_verified_autonomous_research/paper_0dcba54d6a1436bd`
- Verification group: `docs/verification/group_3/paper_0dcba54d6a1436bd`
- Paper documents: `papers/paper_0dcba54d6a1436bd`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "comparison": "Both NPCZCS and AQCZCS have five singlet roots on their frequency-validated final S0 geometries and explicit S1 NTO evidence.",
  "limitations": [
    "Isolated-molecule continuum model; no aggregate/solid-state effects.",
    "D>=2.0 Å is a transparent screening convention, not a universal boundary between LE and CT; fragment-resolved charge-transfer numbers would further refine the assignment."
  ],
  "methods": {
    "excited_state_method": "M06/6-31G(d,p) TD(Singlets,NStates=5,Root=1), PCM dichloromethane, Density=(Transition=1), Pop=(NTO,SaveNTO,Full)",
    "geometry_method": "B3LYP/6-31G(d,p) Opt/Freq",
    "software": "Gaussian 16 C.01; cclib plus cubegen density integration",
    "state_assignment": "Ascending TD roots; orbital contributions parsed per root; S1 NTO pair quantified by hole/electron centroid distance"
  },
  "status": "success",
  "systems": [
    {
      "outcome": {
        "kind": "success",
        "s1_analysis": {
          "conclusion": "S1 NTO centroid separation D=5.4703 Å; by the disclosed D>=2.0 Å screening rule this is ICT-like spatial separation.",
          "evidence": "<nested value omitted>",
          "method": "Gaussian S1 transition density with SaveNTO; dominant NTO hole/electron cubes integrated on a common grid"
        },
        "states": [
          "<nested value omitted>",
          "<nested value omitted>",
          "<nested value omitted>",
          "<nested value omitted>",
          "<nested value omitted>"
        ]
      },
      "system_id": "NPCZCS",
      "validation": {
        "charge": 0,
        "diagnostics": [
          "Gaussian Opt/Freq normal termination",
          "nonempty Hessian with zero imaginary frequencies"
        ],
        "minimum_status": "validated_minimum",
        "multiplicity": 1
      }
    },
    {
      "outcome": {
        "kind": "success",
        "s1_analysis": {
          "conclusion": "S1 NTO centroid separation D=7.2722 Å; by the disclosed D>=2.0 Å screening rule this is ICT-like spatial separation.",
          "evidence": "<nested value omitted>",
          "method": "Gaussian S1 transition density with SaveNTO; dominant NTO hole/electron cubes integrated on a common grid"
        },
        "states": [
          "<nested value omitted>",
          "<nested value omitted>",
          "<nested value omitted>",
          "<nested value omitted>",
          "<nested value omitted>"
        ]
      },
      "system_id": "AQCZCS",
      "validation": {
        "charge": 0,
        "diagnostics": [
          "Gaussian Opt/Freq normal termination",
          "nonempty Hessian with zero imaginary frequencies"
        ],
        "minimum_status": "validated_minimum",
        "multiplicity": 1
      }
    }
  ]
}
```

Paper/SI document hashes:

- `papers/paper_0dcba54d6a1436bd/documents/main.pdf` — SHA-256 `1f5313ccf56ae62c57d8601e056099404ee5a1080b2d31189c5c7b9365b8e6ff` (declared_match=True)
- `papers/paper_0dcba54d6a1436bd/documents/supplementary_001.pdf` — SHA-256 `3f9dab0079efd4f0e2879bf457db34f03f8e6cee529e9fd1c2cbe17e43795198` (declared_match=True)

Report evidence lines retained:

- NPCZCS 与 AQCZCS 的 B3LYP/6-31G(d,p) `Opt Freq Int=UltraFine NoSymm` 均正常终止，分别解析到 255 和 225 个振动频率、零虚频。最终生产 TD 作业使用 `M06/6-31G(d,p) TD=(Singlets,NStates=5,Root=1) Density=(Transition=1) Pop=(NTO,SaveNTO,Full) SCRF=(PCM,Solvent=Dichloromethane) NoSymm SCF=XQC`，两个作业均正常终止并各有五个可追踪 singlet roots 和 dominant configurations。
- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |
- 本篇所有作者路线端点及 evaluation 科学闸门均已闭合，最终判定为 **PASS**。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **80**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/status.json` — successful status record; SHA-256 `1c70411362b26b12fce8c3f1524a242974df1fab6d9147911bb7485454f6c44b`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/AQCZCS_b3lyp_opt_freq_restored_optimized.xyz` — successful execution artifact; SHA-256 `302828876476ac6c550621095d80e4b7b6a8d1bf4acf3200cdd9bd75217e4193`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/collection.json` — successful execution artifact; SHA-256 `21a7de9edaea67c6973dd9f00930ecf2ce943f9aa71d1c36358122f1c5ac093e`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/formchk.log` — successful execution artifact; SHA-256 `099d3610a65d4b631f953b23338bb3462d85748ea9087f0fe53de55a813d0480`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/input.com` — successful execution artifact; SHA-256 `a0328046fb332f61bcd5645c487bd4652f432918661136333139bdf38dfc0303`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/status.json` — successful status record; SHA-256 `2293f5da70f40a6d0d5c551b3481d1136f43e114b1a1976c0a54293a2ec16207`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry_optimized.xyz` — successful execution artifact; SHA-256 `ca1c101c5cd317abf6dc40ef90b163391d1ec4d0527b090e56806389d598595d`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/collection.json` — successful execution artifact; SHA-256 `c84b438ccf590c8fa2c669389d66582d52e268262d1f2b68af407a0cdac34dbf`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/formchk.log` — successful execution artifact; SHA-256 `9011f6760e140e7df44cc0aa8f34e937fcf451af49594b70d69832daaa182b96`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/input.com` — successful execution artifact; SHA-256 `20677281d1b53704e0d538d73b938651eff6f817bfc67d95140028c5885279cc`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/status.json` — successful status record; SHA-256 `8c3194a7089d9a56de576e3d83fd0364fb2630591230f97198e67ebf1c6d475e`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/AQCZCS_m06_td5_nto_syntax_retry_optimized.xyz` — successful execution artifact; SHA-256 `f1a246a070d1beb667884a931329db05d73b8d3a98611e8b140b549c75d976ba`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/collection.json` — successful execution artifact; SHA-256 `d96a55213a091321611a1152bfca687f4fccc7ad33404756b3dd9886c466dae0`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/formchk.log` — successful execution artifact; SHA-256 `e3d49ccc82ac18ff9d0460d82c1902a18925f4c47c0e817de0fac07fb8dc139c`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/input.com` — successful execution artifact; SHA-256 `a87e8af0c965477f7a996a6625a91c12f46f6684ce49f74ec3892ef58f7bc8e8`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/status.json` — successful status record; SHA-256 `6db504b78666379bb793e0d71c06320258ab869791217ef79a96cd429f45f698`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/AQCZCS_m06_td5_restored_optimized.xyz` — successful execution artifact; SHA-256 `c20446cec9957540faecc753fa34676fc156811ef403c343e78986d79dbc9255`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/collection.json` — successful execution artifact; SHA-256 `42f99d664055885ab49f136b82aa4cf0f2ceb07da697ad9df5724e3d53aa26a6`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/formchk.log` — successful execution artifact; SHA-256 `82321ce379dcc8927f8f4edd657b0dc4a16dc1ff57c1f0341994f5fef03c28b3`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/input.com` — successful execution artifact; SHA-256 `9ea7ba19fdec8b3fb00f53f38bbe5aa40cf68f44871bb569563a726535ebe4ea`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/status.json` — successful status record; SHA-256 `940980160a2dfce41b898ecd09d2b2bdb6fc70bbd611367d218e25c27e2ddf70`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/NPCZCS_b3lyp_opt_freq_restored_optimized.xyz` — successful execution artifact; SHA-256 `a941b547a66d930d6fba36d8dea7f569feb21a28d8b4c11c5d5dda182cf64aac`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/collection.json` — successful execution artifact; SHA-256 `864538f26d25badf3b511d6d73a382d3d17e27e468b0e5f601951e0c506ffc71`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/formchk.log` — successful execution artifact; SHA-256 `e058257a8e37cfea278231e86161b99d16020e96fc976ca5f0fc60b9b249aa68`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/input.com` — successful execution artifact; SHA-256 `83bdb7df00b1861df23119dc7dac41321e8dce1f5e4b9039e41b180947949032`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/status.json` — successful status record; SHA-256 `0736f58e641b8affbefe683c48f72964a472d884c34186d12a925acea7d31426`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry_optimized.xyz` — successful execution artifact; SHA-256 `83c241f601987be167e5b9d54aa0603c305441a4da5598267a362733cf7282cf`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/collection.json` — successful execution artifact; SHA-256 `bb655f03046fecab0337e0dc946d8a2e4e2b2c2008b87f877607625eedd6c1ab`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/formchk.log` — successful execution artifact; SHA-256 `94a6f16ddbacb2448ec7600c92ad89311d1676ac1a322a8b33f32a1abc2715ef`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/input.com` — successful execution artifact; SHA-256 `bd87ca9641090ea808f27282e8121753512f6bf2d0b6bdd126a74069e4701fb7`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/status.json` — successful status record; SHA-256 `59b2ebf26255e96d35af4dc2eb036b620269be50303abfe23dd6494bae46bc0f`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/NPCZCS_m06_td5_nto_syntax_retry_optimized.xyz` — successful execution artifact; SHA-256 `af8bf92ca923ef8dc6f25bfb9aef91d34f54846aaba370bea9ca50a16d02397c`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/collection.json` — successful execution artifact; SHA-256 `98b33165584417757bf48eceb0cdf92a345b6db4b68291f0f6c4707a9240c8ae`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/formchk.log` — successful execution artifact; SHA-256 `72a72de71893fb384e9bb42299a8ee0e657a81792ac248cf7cfd40bf2084b48c`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/input.com` — successful execution artifact; SHA-256 `1a66c76d0b42fcacd4a0434469e88efa137264a4cbe9d3c408b5f4451b08a366`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/status.json` — successful status record; SHA-256 `7f0d300ad84dc4d4eb1287c44f5552b891be290d02b672ebae524aad5c867d9b`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/NPCZCS_m06_td5_restored_optimized.xyz` — successful execution artifact; SHA-256 `45ddb64e7d2ce85d1a7b5a73b1bff90c0d4ea81e7645cccd88d14a202022b64f`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/collection.json` — successful execution artifact; SHA-256 `0e20dc26ad5d78d2860d9bc8fdf1e919f0e39635eb1e70164cec1b42acc1ae67`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/formchk.log` — successful execution artifact; SHA-256 `25fec84a4606e5e5aae1c182d2824c80eca8a5231ff892cb4c6c99045aebb82b`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/input.com` — successful execution artifact; SHA-256 `4b9442a1c0e463551f420ed1b80081719632a9c6aa8de4651631fb6d65120106`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_b3lyp_opt_freq_restored/outputs/execution_jobs/job_cf8eebaffbd042b6b3f546472ed24d8c/status.json` — successful status record; SHA-256 `1c70411362b26b12fce8c3f1524a242974df1fab6d9147911bb7485454f6c44b`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_b3lyp_opt_freq_restored/outputs/execution_jobs/job_cf8eebaffbd042b6b3f546472ed24d8c/collection.json` — successful execution artifact; SHA-256 `21a7de9edaea67c6973dd9f00930ecf2ce943f9aa71d1c36358122f1c5ac093e`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_b3lyp_opt_freq_restored/outputs/execution_jobs/job_cf8eebaffbd042b6b3f546472ed24d8c/input.com` — successful execution artifact; SHA-256 `a0328046fb332f61bcd5645c487bd4652f432918661136333139bdf38dfc0303`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_b3lyp_opt_freq_restored/outputs/execution_jobs/job_cf8eebaffbd042b6b3f546472ed24d8c/request.json` — successful execution artifact; SHA-256 `831bf7166050264e73a711ba648fe07b749eb329c9e975be6e6fa7da0c0f0f76`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_b3lyp_opt_freq_restored/outputs/execution_jobs/job_cf8eebaffbd042b6b3f546472ed24d8c/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_nto_savento_retry/outputs/execution_jobs/job_655cfb4f5e7a4801b62e3c0e8ac4b314/status.json` — successful status record; SHA-256 `2293f5da70f40a6d0d5c551b3481d1136f43e114b1a1976c0a54293a2ec16207`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_nto_savento_retry/outputs/execution_jobs/job_655cfb4f5e7a4801b62e3c0e8ac4b314/collection.json` — successful execution artifact; SHA-256 `c84b438ccf590c8fa2c669389d66582d52e268262d1f2b68af407a0cdac34dbf`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_nto_savento_retry/outputs/execution_jobs/job_655cfb4f5e7a4801b62e3c0e8ac4b314/input.com` — successful execution artifact; SHA-256 `20677281d1b53704e0d538d73b938651eff6f817bfc67d95140028c5885279cc`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_nto_savento_retry/outputs/execution_jobs/job_655cfb4f5e7a4801b62e3c0e8ac4b314/request.json` — successful execution artifact; SHA-256 `71689a7ef0ab91bfd2194cd50e188cf9036413654db74e08a2636a69655d7d80`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_nto_savento_retry/outputs/execution_jobs/job_655cfb4f5e7a4801b62e3c0e8ac4b314/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_nto_syntax_retry/outputs/execution_jobs/job_9e63045ef9c44119b30dbbd156f5f9d5/status.json` — successful status record; SHA-256 `8c3194a7089d9a56de576e3d83fd0364fb2630591230f97198e67ebf1c6d475e`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_nto_syntax_retry/outputs/execution_jobs/job_9e63045ef9c44119b30dbbd156f5f9d5/collection.json` — successful execution artifact; SHA-256 `d96a55213a091321611a1152bfca687f4fccc7ad33404756b3dd9886c466dae0`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_nto_syntax_retry/outputs/execution_jobs/job_9e63045ef9c44119b30dbbd156f5f9d5/input.com` — successful execution artifact; SHA-256 `a87e8af0c965477f7a996a6625a91c12f46f6684ce49f74ec3892ef58f7bc8e8`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_nto_syntax_retry/outputs/execution_jobs/job_9e63045ef9c44119b30dbbd156f5f9d5/request.json` — successful execution artifact; SHA-256 `18d98722ef125e1fc0880c316292d814e8fb2f9f1ce944b4155c38a06c62fd2d`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_nto_syntax_retry/outputs/execution_jobs/job_9e63045ef9c44119b30dbbd156f5f9d5/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_restored/outputs/execution_jobs/job_c3f005859206428dac0d1270438d9c80/status.json` — successful status record; SHA-256 `6db504b78666379bb793e0d71c06320258ab869791217ef79a96cd429f45f698`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_restored/outputs/execution_jobs/job_c3f005859206428dac0d1270438d9c80/collection.json` — successful execution artifact; SHA-256 `42f99d664055885ab49f136b82aa4cf0f2ceb07da697ad9df5724e3d53aa26a6`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_restored/outputs/execution_jobs/job_c3f005859206428dac0d1270438d9c80/input.com` — successful execution artifact; SHA-256 `9ea7ba19fdec8b3fb00f53f38bbe5aa40cf68f44871bb569563a726535ebe4ea`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_restored/outputs/execution_jobs/job_c3f005859206428dac0d1270438d9c80/request.json` — successful execution artifact; SHA-256 `643f52a3fcc27651f03105895db63744585e985a07380f7344ec01308f21a389`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/AQCZCS_m06_td5_restored/outputs/execution_jobs/job_c3f005859206428dac0d1270438d9c80/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_b3lyp_opt_freq_restored/outputs/execution_jobs/job_e17435dfabea427e8298ad328cb3c6fe/status.json` — successful status record; SHA-256 `940980160a2dfce41b898ecd09d2b2bdb6fc70bbd611367d218e25c27e2ddf70`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_b3lyp_opt_freq_restored/outputs/execution_jobs/job_e17435dfabea427e8298ad328cb3c6fe/collection.json` — successful execution artifact; SHA-256 `864538f26d25badf3b511d6d73a382d3d17e27e468b0e5f601951e0c506ffc71`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_b3lyp_opt_freq_restored/outputs/execution_jobs/job_e17435dfabea427e8298ad328cb3c6fe/input.com` — successful execution artifact; SHA-256 `83bdb7df00b1861df23119dc7dac41321e8dce1f5e4b9039e41b180947949032`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_b3lyp_opt_freq_restored/outputs/execution_jobs/job_e17435dfabea427e8298ad328cb3c6fe/request.json` — successful execution artifact; SHA-256 `330942986c9b5a57746272d2b8bfb58450a465a921694a3ebaf27f6844c9707e`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_b3lyp_opt_freq_restored/outputs/execution_jobs/job_e17435dfabea427e8298ad328cb3c6fe/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_nto_savento_retry/outputs/execution_jobs/job_947b5c108de442849da7ab6c695ee29f/status.json` — successful status record; SHA-256 `0736f58e641b8affbefe683c48f72964a472d884c34186d12a925acea7d31426`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_nto_savento_retry/outputs/execution_jobs/job_947b5c108de442849da7ab6c695ee29f/collection.json` — successful execution artifact; SHA-256 `bb655f03046fecab0337e0dc946d8a2e4e2b2c2008b87f877607625eedd6c1ab`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_nto_savento_retry/outputs/execution_jobs/job_947b5c108de442849da7ab6c695ee29f/input.com` — successful execution artifact; SHA-256 `bd87ca9641090ea808f27282e8121753512f6bf2d0b6bdd126a74069e4701fb7`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_nto_savento_retry/outputs/execution_jobs/job_947b5c108de442849da7ab6c695ee29f/request.json` — successful execution artifact; SHA-256 `9333ef58b2379181086fa5da4c979d50d089c9aa80e84b695f099d66935f05d5`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_nto_savento_retry/outputs/execution_jobs/job_947b5c108de442849da7ab6c695ee29f/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_nto_syntax_retry/outputs/execution_jobs/job_d9521390298943fb8a8e16360a5507b4/status.json` — successful status record; SHA-256 `59b2ebf26255e96d35af4dc2eb036b620269be50303abfe23dd6494bae46bc0f`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_nto_syntax_retry/outputs/execution_jobs/job_d9521390298943fb8a8e16360a5507b4/collection.json` — successful execution artifact; SHA-256 `98b33165584417757bf48eceb0cdf92a345b6db4b68291f0f6c4707a9240c8ae`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_nto_syntax_retry/outputs/execution_jobs/job_d9521390298943fb8a8e16360a5507b4/input.com` — successful execution artifact; SHA-256 `1a66c76d0b42fcacd4a0434469e88efa137264a4cbe9d3c408b5f4451b08a366`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_nto_syntax_retry/outputs/execution_jobs/job_d9521390298943fb8a8e16360a5507b4/request.json` — successful execution artifact; SHA-256 `609e3cd8fdc2ef76a868d3f6c6ea1ee491e09477bd93024007e2fedf291eccc2`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_nto_syntax_retry/outputs/execution_jobs/job_d9521390298943fb8a8e16360a5507b4/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_restored/outputs/execution_jobs/job_48f64f47702340a8807f0bb4f3e4f6fe/status.json` — successful status record; SHA-256 `7f0d300ad84dc4d4eb1287c44f5552b891be290d02b672ebae524aad5c867d9b`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_restored/outputs/execution_jobs/job_48f64f47702340a8807f0bb4f3e4f6fe/collection.json` — successful execution artifact; SHA-256 `0e20dc26ad5d78d2860d9bc8fdf1e919f0e39635eb1e70164cec1b42acc1ae67`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_restored/outputs/execution_jobs/job_48f64f47702340a8807f0bb4f3e4f6fe/input.com` — successful execution artifact; SHA-256 `4b9442a1c0e463551f420ed1b80081719632a9c6aa8de4651631fb6d65120106`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_restored/outputs/execution_jobs/job_48f64f47702340a8807f0bb4f3e4f6fe/request.json` — successful execution artifact; SHA-256 `c9b2405790d7d642de51c873345162807f2865a6286a807558a5818526ffdcc9`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/native_workspace/NPCZCS_m06_td5_restored/outputs/execution_jobs/job_48f64f47702340a8807f0bb4f3e4f6fe/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/status.json` — label=group_3 paper_0dcba54d6a1436bd NPCZCS_b3lyp_opt_freq_restored; submitted_at=2026-08-29T15:46:55.156375+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d,p) Opt Freq Int=UltraFine NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/NPCZCS_b3lyp_opt_freq_restored.chk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/NPCZCS_b3lyp_opt_freq_restored.fchk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/NPCZCS_b3lyp_opt_freq_restored_optimized.xyz`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/collection.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/formchk.log`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/input.com`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/parsed_observables.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_b3lyp_opt_freq_restored/stderr.log`
2. `artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/status.json` — label=group_3 paper_0dcba54d6a1436bd AQCZCS_b3lyp_opt_freq_restored; submitted_at=2026-08-29T15:46:56.143981+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d,p) Opt Freq Int=UltraFine NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/AQCZCS_b3lyp_opt_freq_restored.chk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/AQCZCS_b3lyp_opt_freq_restored.fchk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/AQCZCS_b3lyp_opt_freq_restored_optimized.xyz`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/collection.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/formchk.log`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/input.com`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/parsed_observables.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_b3lyp_opt_freq_restored/stderr.log`
3. `artifacts/gaussian/NPCZCS_m06_td5_restored/status.json` — label=group_3 paper_0dcba54d6a1436bd NPCZCS_m06_td5_restored; submitted_at=2026-08-29T15:51:03.665004+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD(NStates=5) SCRF=(PCM,Solvent=Dichloromethane) Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/NPCZCS_m06_td5_restored.chk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/NPCZCS_m06_td5_restored.fchk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/NPCZCS_m06_td5_restored_optimized.xyz`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/collection.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/formchk.log`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/input.com`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/parsed_observables.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_restored/stderr.log`
4. `artifacts/gaussian/AQCZCS_m06_td5_restored/status.json` — label=group_3 paper_0dcba54d6a1436bd AQCZCS_m06_td5_restored; submitted_at=2026-08-29T15:51:04.649055+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD(NStates=5) SCRF=(PCM,Solvent=Dichloromethane) Pop=Full NoSymm; command=g16 < input.com
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/AQCZCS_m06_td5_restored.chk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/AQCZCS_m06_td5_restored.fchk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/AQCZCS_m06_td5_restored_optimized.xyz`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/collection.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/formchk.log`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/input.com`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/parsed_observables.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_restored/stderr.log`
5. `artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/status.json` — label=group_3 paper_0dcba54d6a1436bd NPCZCS_m06_td5_nto_syntax_retry; submitted_at=2026-08-30T14:05:05.525221+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD=(Singlets,NStates=5,Root=1) Pop=(NTO,Full) SCRF=(PCM,Solvent=Dichloromethane) NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/NPCZCS_m06_td5_nto_syntax_retry.chk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/NPCZCS_m06_td5_nto_syntax_retry.fchk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/NPCZCS_m06_td5_nto_syntax_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/collection.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/formchk.log`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/input.com`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_syntax_retry/stderr.log`
6. `artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/status.json` — label=group_3 paper_0dcba54d6a1436bd AQCZCS_m06_td5_nto_syntax_retry; submitted_at=2026-08-30T14:05:38.079332+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD=(Singlets,NStates=5,Root=1) Pop=(NTO,Full) SCRF=(PCM,Solvent=Dichloromethane) NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/AQCZCS_m06_td5_nto_syntax_retry.chk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/AQCZCS_m06_td5_nto_syntax_retry.fchk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/AQCZCS_m06_td5_nto_syntax_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/collection.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/formchk.log`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/input.com`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/parsed_observables.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_syntax_retry/stderr.log`
7. `artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/status.json` — label=group_3 paper_0dcba54d6a1436bd AQCZCS_m06_td5_nto_savento_retry; submitted_at=2026-08-30T14:19:59.766108+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD=(Singlets,NStates=5,Root=1) Density=(Transition=1) Pop=(NTO,SaveNTO,Full) SCRF=(PCM,Solvent=Dichloromethane) NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry.chk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry.fchk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry_S1_electron.cube`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry_S1_hole.cube`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/collection.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/formchk.log`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/input.com`
8. `artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/status.json` — label=group_3 paper_0dcba54d6a1436bd NPCZCS_m06_td5_nto_savento_retry; submitted_at=2026-08-30T14:20:04.776941+00:00; software=gaussian; intent=single_point; route=#p M06/6-31G(d,p) TD=(Singlets,NStates=5,Root=1) Density=(Transition=1) Pop=(NTO,SaveNTO,Full) SCRF=(PCM,Solvent=Dichloromethane) NoSymm SCF=XQC; command=g16 < input.com
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry.chk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry.fchk`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry_S1_electron.cube`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry_S1_hole.cube`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry_optimized.xyz`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/collection.json`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/formchk.log`
   - output: `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/input.com`

## Evaluator alignment

- Key-point IDs: `kp_process_minima, kp_process_states, kp_result_npc, kp_result_aqc`
- Conclusion IDs: `c_final_spectra, c_final_ict`
- Scoring-rule IDs: `kp_process_minima_rule, kp_process_states_rule, kp_result_npc_rule, kp_result_aqc_rule, c_final_spectra_rule, c_final_ict_rule`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `kp_process_minima_rule` → reference `kp_process_minima`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `kp_process_states_rule` → reference `kp_process_states`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `kp_result_npc_rule` → reference `kp_result_npc`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `kp_result_aqc_rule` → reference `kp_result_aqc`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `c_final_spectra_rule` → reference `c_final_spectra`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False
- rule `c_final_ict_rule` → reference `c_final_ict`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert scientific comparison; evaluator_target_present=False

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].system_id` = `"NPCZCS"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].validation.minimum_status` = `"validated_minimum"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].validation.diagnostics[0]` = `"Gaussian Opt/Freq normal termination"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].validation.diagnostics[1]` = `"nonempty Hessian with zero imaginary frequencies"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].validation.charge` = `0`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].validation.multiplicity` = `1`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.kind` = `"success"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].state` = `1`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].energy_eV` = `2.9477`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].wavelength_nm` = `420.61335414051626`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].oscillator_strength` = `0.5127`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].dominant_configuration.from_orbital` = `167`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].dominant_configuration.from_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].dominant_configuration.direction` = `"->"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].dominant_configuration.to_orbital` = `168`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].dominant_configuration.to_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].dominant_configuration.coefficient` = `0.65729`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[0].dominant_configuration.weight` = `0.43203014410000007`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].state` = `2`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].energy_eV` = `3.2982`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].wavelength_nm` = `375.9147365229519`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].oscillator_strength` = `0.8813`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].dominant_configuration.from_orbital` = `167`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].dominant_configuration.from_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].dominant_configuration.direction` = `"->"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].dominant_configuration.to_orbital` = `169`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].dominant_configuration.to_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].dominant_configuration.coefficient` = `0.65023`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[1].dominant_configuration.weight` = `0.42279905289999997`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].state` = `3`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].energy_eV` = `3.3599`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].wavelength_nm` = `369.011572963481`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].oscillator_strength` = `0.228`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].dominant_configuration.from_orbital` = `166`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].dominant_configuration.from_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].dominant_configuration.direction` = `"->"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].dominant_configuration.to_orbital` = `168`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].dominant_configuration.to_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].dominant_configuration.coefficient` = `0.6477`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[2].dominant_configuration.weight` = `0.4195152900000001`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].state` = `4`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].energy_eV` = `3.65`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].wavelength_nm` = `339.6827353424657`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].oscillator_strength` = `0.0665`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].dominant_configuration.from_orbital` = `166`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].dominant_configuration.from_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].dominant_configuration.direction` = `"->"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].dominant_configuration.to_orbital` = `169`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].dominant_configuration.to_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].dominant_configuration.coefficient` = `0.53006`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[3].dominant_configuration.weight` = `0.2809636036`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].state` = `5`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].energy_eV` = `3.779`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].wavelength_nm` = `328.0873204551468`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].oscillator_strength` = `0.1214`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].dominant_configuration.from_orbital` = `165`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].dominant_configuration.from_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].dominant_configuration.direction` = `"->"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].dominant_configuration.to_orbital` = `168`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].dominant_configuration.to_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].dominant_configuration.coefficient` = `0.63043`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.states[4].dominant_configuration.weight` = `0.39744198490000004`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.method` = `"Gaussian S1 transition density with SaveNTO; dominant NTO hole/electron cubes integrated on a common grid"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.conclusion` = `"S1 NTO centroid separation D=5.4703 Å; by the disclosed D>=2.0 Å screening rule this is ICT-like spatial separation."`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.distance_angstrom` = `5.470278360306731`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.hole_centroid_angstrom[0]` = `1.9479915122707505`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.hole_centroid_angstrom[1]` = `0.10067805911730385`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.hole_centroid_angstrom[2]` = `-0.526373974145936`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.electron_centroid_angstrom[0]` = `-3.4637519160665478`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.electron_centroid_angstrom[1]` = `-0.17239640620892843`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.electron_centroid_angstrom[2]` = `0.22356518436957107`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.hole_orbital_index_1based` = `167`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.electron_orbital_index_1based` = `168`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.grid` = `"Gaussian cubegen coarse (-2), identical automatic box for the paired saved NTOs"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.evidence[0]` = `"artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry_S1_hole.cube"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.evidence[1]` = `"artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry_S1_electron.cube"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[0].outcome.s1_analysis.evidence.evidence[2]` = `"artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry.fchk"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].system_id` = `"AQCZCS"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].validation.minimum_status` = `"validated_minimum"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].validation.diagnostics[0]` = `"Gaussian Opt/Freq normal termination"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].validation.diagnostics[1]` = `"nonempty Hessian with zero imaginary frequencies"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].validation.charge` = `0`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].validation.multiplicity` = `1`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.kind` = `"success"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].state` = `1`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].energy_eV` = `2.5851`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].wavelength_nm` = `479.6108405864376`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].oscillator_strength` = `0.1946`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].dominant_configuration.from_orbital` = `154`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].dominant_configuration.from_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].dominant_configuration.direction` = `"->"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].dominant_configuration.to_orbital` = `155`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].dominant_configuration.to_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].dominant_configuration.coefficient` = `0.6838`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[0].dominant_configuration.weight` = `0.46758243999999993`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].state` = `2`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].energy_eV` = `3.0281`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].wavelength_nm` = `409.44552161421353`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].oscillator_strength` = `0.0837`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].dominant_configuration.from_orbital` = `153`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].dominant_configuration.from_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].dominant_configuration.direction` = `"->"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].dominant_configuration.to_orbital` = `155`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].dominant_configuration.to_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].dominant_configuration.coefficient` = `0.67455`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[1].dominant_configuration.weight` = `0.45501770249999995`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].state` = `3`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].energy_eV` = `3.1087`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].wavelength_nm` = `398.8297307556213`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].oscillator_strength` = `0.004`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].dominant_configuration.from_orbital` = `149`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].dominant_configuration.from_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].dominant_configuration.direction` = `"->"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].dominant_configuration.to_orbital` = `155`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].dominant_configuration.to_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].dominant_configuration.coefficient` = `0.68054`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[2].dominant_configuration.weight` = `0.46313469160000004`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].state` = `4`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].energy_eV` = `3.2397`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].wavelength_nm` = `382.7027144488687`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].oscillator_strength` = `1.0222`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].dominant_configuration.from_orbital` = `154`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].dominant_configuration.from_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].dominant_configuration.direction` = `"->"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].dominant_configuration.to_orbital` = `156`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].dominant_configuration.to_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].dominant_configuration.coefficient` = `0.69019`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[3].dominant_configuration.weight` = `0.47636223609999995`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].state` = `5`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].energy_eV` = `3.39`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].wavelength_nm` = `365.7350985250737`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].oscillator_strength` = `0.0006`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].dominant_configuration.from_orbital` = `145`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].dominant_configuration.from_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].dominant_configuration.direction` = `"->"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].dominant_configuration.to_orbital` = `155`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].dominant_configuration.to_spin` = `null`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].dominant_configuration.coefficient` = `0.66631`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.states[4].dominant_configuration.weight` = `0.44396901609999995`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.method` = `"Gaussian S1 transition density with SaveNTO; dominant NTO hole/electron cubes integrated on a common grid"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.conclusion` = `"S1 NTO centroid separation D=7.2722 Å; by the disclosed D>=2.0 Å screening rule this is ICT-like spatial separation."`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.distance_angstrom` = `7.272162453161108`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.hole_centroid_angstrom[0]` = `1.2944032075860938`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.hole_centroid_angstrom[1]` = `-0.20381312281528727`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.hole_centroid_angstrom[2]` = `-0.35043329843327437`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.electron_centroid_angstrom[0]` = `-5.965726118600306`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.electron_centroid_angstrom[1]` = `-0.1885856432723588`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.electron_centroid_angstrom[2]` = `0.06746266479342457`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.hole_orbital_index_1based` = `154`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.electron_orbital_index_1based` = `155`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.grid` = `"Gaussian cubegen coarse (-2), identical automatic box for the paired saved NTOs"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.evidence[0]` = `"artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry_S1_hole.cube"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.evidence[1]` = `"artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry_S1_electron.cube"`
- rule `kp_process_minima_rule` / reference `kp_process_minima` / field `$.systems` / result path `$.systems[1].outcome.s1_analysis.evidence.evidence[2]` = `"artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry.fchk"`
- rule `c_final_spectra_rule` / reference `c_final_spectra` / field `$.limitations` / result path `$.limitations[0]` = `"Isolated-molecule continuum model; no aggregate/solid-state effects."`
- rule `c_final_spectra_rule` / reference `c_final_spectra` / field `$.limitations` / result path `$.limitations[1]` = `"D>=2.0 Å is a transparent screening convention, not a universal boundary between LE and CT; fragment-resolved charge-transfer numbers would further refine the assignment."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Public molecule identities, formulas, charge and multiplicity.

Public input files and hashes:

- `agent_input/data/inputs/systems.json` — SHA-256 `5757a24178f4bf21510d57e80cb35a55b09154741bc51d305ff00898ee00c889`; size=613 bytes; explicit_boundary_fields={"$.systems[0].charge": 0, "$.systems[0].formula": "C43H39N3O2", "$.systems[0].multiplicity": 1, "$.systems[1].charge": 0, "$.systems[1].formula": "C41H32N2O2", "$.systems[1].multiplicity": 1}

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_3/paper_0dcba54d6a1436bd/verification_report.md` — verification record; SHA-256 `29f060c025ca10fec87b2ccd0239b05e6c80ff5da71eddfb55db7bfb24fb0c99`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/report/results.json` — verification record; SHA-256 `df8a6559c71cd8c7193f0fc3bb1ddcf363674bb8d30136656a7cd1705117a944`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry.fchk` — referenced successful evidence; SHA-256 `e9bfddcc10fc1738d4c96915a3c8e03036220d08b9a73bae5501c9c98f63c0e9`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry_S1_electron.cube` — referenced successful evidence; SHA-256 `05ab2f794c05088b241ad7b90eb93984313fca181c1e3d60657136b34ddd4a92`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/AQCZCS_m06_td5_nto_savento_retry/AQCZCS_m06_td5_nto_savento_retry_S1_hole.cube` — referenced successful evidence; SHA-256 `580f3c092811915278df628a45f49b5c60f2b3d15d7f7d573c4fbec0508a24e7`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry.fchk` — referenced successful evidence; SHA-256 `636b428cc4397be7f4195537727e2154d9c5e718788119bba55ae46ece38234e`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry_S1_electron.cube` — referenced successful evidence; SHA-256 `c958cad347d389ca6c0f0fdb3b3a0107bcb2ba9f07d029fb8cb5d436731d107d`
- `docs/verification/group_3/paper_0dcba54d6a1436bd/artifacts/gaussian/NPCZCS_m06_td5_nto_savento_retry/NPCZCS_m06_td5_nto_savento_retry_S1_hole.cube` — referenced successful evidence; SHA-256 `12c4fdd8fe571c1bec108629f0ad1dd224e5f983f05d524b27ea7ba457b0a02e`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
