# Verified computation reference — paper_2f302589e5e9e420 (autonomous_research)

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
| 4 | `PASS` | 最终严格状态：**PASS**。EPI1/EPI2 已按正文/SI 的 B3LYP-D3(BJ)/6-31G*（即 6-31G(d)）Opt/Freq 路线完成，并在相同的作者属性层 B3LYP-D3BJ/ma-def2-TZVPP 上完成偶极单点。修订后的 evaluator 将正值 reduction 作为科学目标，ESP 缺失按规则显式允许。 |
| 58 | `PASS` | 论文复现结论：**PASS**。EPI1 和 EPI2 均由 Gaussian B3LYP-D3BJ/6-31G* Opt/Freq 验证为零虚频局部极小点，并在这两个几何上以 ORCA B3LYP-D3BJ/ma-def2-TZVPP 作者层级单点重新计算偶极矩。得到 EPI1=2.223986 D、EPI2=1.899047 D，signed change = −14.6107%，正值 reduction = 14.6107%；因此在任务定义的孤立片段边界内，邻位甲氧基降低分子偶极极性。ESP 未计算，但依据 scoring rule 属于允许的缺失可选输出。 |
| 66 | `PASS` | 论文复现结论： **PASS**（结构化结果对象已满足本篇定义的终态科学闸门；详细数值与原始证据见 report/results.json、artifacts/gaussian/ 和 provenance/。） |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: d5gc04984a 2376..2384 ++
- DOI: `10.1039/d5gc04984a`
- Task package: `tasks/final_verified_autonomous_research/paper_2f302589e5e9e420`
- Verification group: `docs/verification/group_3/paper_2f302589e5e9e420`
- Paper documents: `papers/paper_2f302589e5e9e420`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "candidate_records": [
    {
      "advanced": true,
      "candidate_id": "EPI1_strict_author_ma_def2_tzvpp_sp",
      "fragment_id": "EPI1",
      "generation_rationale": "Public displaced XYZ geometry optimized at common Gaussian protocol; ORCA author-layer property single point",
      "validation_evidence": "ORCA normal termination; dipole parsed."
    },
    {
      "advanced": true,
      "candidate_id": "EPI2_strict_author_ma_def2_tzvpp_sp",
      "fragment_id": "EPI2",
      "generation_rationale": "Public displaced XYZ geometry optimized at common Gaussian protocol; ORCA author-layer property single point",
      "validation_evidence": "ORCA normal termination; dipole parsed."
    }
  ],
  "comparison_basis": "Dipoles evaluated at identical author-layer B3LYP-D3BJ/ma-def2-TZVPP protocol on both frequency-validated geometries.",
  "conclusion": "Author-layer EPI1 dipole=2.2240 D and EPI2 dipole=1.8990 D; EPI2 is lower by 14.61% (signed change -14.61%).",
  "evidence_files": [
    "artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/stdout.log",
    "artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/stdout.log"
  ],
  "fragments": [
    {
      "dipole_debye": 2.223986032,
      "esp_definition": "Not calculated.",
      "id": "EPI1",
      "optimization_evidence": "Geometry inherited from validated Gaussian EPI1_author_b3d3_631gstar_opt_freq Opt/Freq endpoint.",
      "property_evidence": "Dipole parsed from ORCA Dipole moment block: 2.223986 D.",
      "validated": true,
      "validation_evidence": "ORCA normal termination, author-layer ma-def2-TZVPP single point on frequency-validated 6-31G* geometry; artifact artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/stdout.log"
    },
    {
      "dipole_debye": 1.899046595,
      "esp_definition": "Not calculated.",
      "id": "EPI2",
      "optimization_evidence": "Geometry inherited from validated Gaussian EPI2_author_b3d3_631gstar_opt_freq Opt/Freq endpoint.",
      "property_evidence": "Dipole parsed from ORCA Dipole moment block: 1.899047 D.",
      "validated": true,
      "validation_evidence": "ORCA normal termination, author-layer ma-def2-TZVPP single point on frequency-validated 6-31G* geometry; artifact artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/stdout.log"
    }
  ],
  "limitations": "Author property layer is a single point on Gaussian-optimized isolated fragments; ESP not calculated and conformer/functional sensitivity remains. Low-layer Gaussian dipoles are retained in evidence artifacts for sensitivity.",
  "method": {
    "minimum_test": "Inherited from Gaussian Opt/Freq endpoints",
    "model": "B3LYP-D3BJ/ma-def2-TZVPP",
    "optimization_protocol": "Single point on Gaussian B3LYP-D3BJ/6-31G* (6-31G(d)) frequency-validated geometries",
    "software": "ORCA 6.1.1; parser"
  },
  "percent_change_ePI2_vs_EPI1": -14.610677959509776,
  "percent_reduction_EPI2_vs_EPI1": 14.610677959509776,
  "status": "complete",
  "uncertainty_sensitivity": "Single supplied starting geometry per fragment; no exhaustive conformer ensemble."
}
```

Paper/SI document hashes:

- `papers/paper_2f302589e5e9e420/documents/supplementary_001.pdf` — SHA-256 `d4a715bfc18bff524f50298937739473903e9fb1012e7cdd5daf9692e42ae942` (declared_match=True)
- `papers/paper_2f302589e5e9e420/documents/main.pdf` — SHA-256 `a97be22902a7ec8a348c8112368e5422ea2af4782e0d4af6f818237fa2a30563` (declared_match=True)

Report evidence lines retained:

- 最终严格状态：**PASS**。EPI1/EPI2 已按正文/SI 的 B3LYP-D3(BJ)/6-31G*（即 6-31G(d)）Opt/Freq 路线完成，并在相同的作者属性层 B3LYP-D3BJ/ma-def2-TZVPP 上完成偶极单点。修订后的 evaluator 将正值 reduction 作为科学目标，ESP 缺失按规则显式允许。
- | case | job ID | status | wall-clock s | CPU/memory | normal termination | optimization | imaginary modes |
- 论文复现结论：**PASS**。EPI1 和 EPI2 均由 Gaussian B3LYP-D3BJ/6-31G* Opt/Freq 验证为零虚频局部极小点，并在这两个几何上以 ORCA B3LYP-D3BJ/ma-def2-TZVPP 作者层级单点重新计算偶极矩。得到 EPI1=2.223986 D、EPI2=1.899047 D，signed change = −14.6107%，正值 reduction = 14.6107%；因此在任务定义的孤立片段边界内，邻位甲氧基降低分子偶极极性。ESP 未计算，但依据 scoring rule 属于允许的缺失可选输出。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **80**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/status.json` — successful status record; SHA-256 `607936841dd48a30e45819574f22b89a25e23284cf552b894b0247d93c1e49b8`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/EPI1_author_b3d3_631gstar_opt_freq_optimized.xyz` — successful execution artifact; SHA-256 `94d5691856ae72d2df9d453dad825f013f8db52a2af0e1001e54361d8fab0838`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/collection.json` — successful execution artifact; SHA-256 `c2feeeb6449183febd2e422bed7468d6e2cbaac75ba9825c317cdb2422c8cff8`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/formchk.log` — successful execution artifact; SHA-256 `0e4f9afc079196095e5fe67ba44bda3bc7ec45bfe1642ba0c0aeb321639a8d11`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/input.com` — successful execution artifact; SHA-256 `2b79b2d88bc154f83a0f1157a7d3759f970d3f752d773d99416cd263da0ef95f`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/status.json` — successful status record; SHA-256 `be91b6a52cec635b04a9dcf4e1f4487c9b4cf5908126ae7c36e66bc2e8bd08fb`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/collection.json` — successful execution artifact; SHA-256 `0ea5c1507975884f7d81b6b5bc7134fa10b4c6b0acee625db21d6a672aaedb6b`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/input.inp` — successful execution artifact; SHA-256 `c502c30755e1c4caf4b3acfbc2bdcf0f025ddf82b77584a6d8c94003c918705e`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/parsed_observables.json` — successful execution artifact; SHA-256 `4b1862ac9a3b01f69b4ec7e345e5f4a65f6287a97ab5185614d01425ffc46fe7`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/status.json` — successful status record; SHA-256 `985978eeaaacfd01998e93053d20f51e84f8b6bdd691ce2463af7ff3d30a2fe9`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/EPI1_b3lyp_d3_opt_freq_optimized.xyz` — successful execution artifact; SHA-256 `8bd271cdc315dde6271a8f26e1884a2abb5c8f5deb6e28bb536fcbe8fdaf803c`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/collection.json` — successful execution artifact; SHA-256 `a7d51df58ced026128f1c8cc685b3f68d58ab808f5f1e2b69fea48673a303b06`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/formchk.log` — successful execution artifact; SHA-256 `31d6145fd2c11e04bc33c45f63cbb56c8d585163578b58b2905f376991172c50`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/input.com` — successful execution artifact; SHA-256 `21fff2e35db910792230aaaf097c21926a28cfa416c01c9005cbb8f54ccbd799`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/status.json` — successful status record; SHA-256 `a7eb956bc5fc22bda252c3ff34a77cf21e5e211581dd47288da64b46c1f0de99`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/collection.json` — successful execution artifact; SHA-256 `7d08288a771999fa59e71b174439aeaccec0f3b71243fa554a6111fccea3e813`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/input.inp` — successful execution artifact; SHA-256 `270b4a8390914ba45067dcb801f04822d52ea3302bfbc60984ae190481b7e134`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/parsed_observables.json` — successful execution artifact; SHA-256 `0a1ee232e78b24f6f2803552749c2beb5cc25037aa80ec8940e27fb2e0008a39`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/status.json` — successful status record; SHA-256 `4906317e80e08fe976d764dbd78b6da10fd07afe9473b273e79c86616d2122af`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g_optimized.xyz` — successful execution artifact; SHA-256 `379e7e03ff83d0b1dcf759959ba843a4fa2f99ab01fc3b22aa01e3a53c42f1b7`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/collection.json` — successful execution artifact; SHA-256 `5208c41705438496ab46c53ea673bcb5e87b01c396c639975744ec01e51ac128`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/formchk.log` — successful execution artifact; SHA-256 `72bf9fea5b6738f5c7642aa89e3463620343027f6ac7664f8d8ecda9d318ce4a`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/input.com` — successful execution artifact; SHA-256 `84da96a8adcc32cc0f6e1bd0e068e143796e6e8495305d5dbddce854a18b8a13`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/status.json` — successful status record; SHA-256 `70aea57942c38c6cb9d7adca09ab0d15d51e406bcc123cb24331d495682b6546`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/collection.json` — successful execution artifact; SHA-256 `a69b57328829a1b5f0476634193326563058c277516675e6689b08bc936db721`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/input.inp` — successful execution artifact; SHA-256 `8d28ad873330c02d08a9d1fdb413d1538776ec99343bd4a706a586b434c1d495`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/parsed_observables.json` — successful execution artifact; SHA-256 `3a70f030e0cadbdb29ed1b33a6455b8b54439f5a094fc8b7aa6232145cc9dac4`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/status.json` — successful status record; SHA-256 `5ec0dd8a8e26cc150d448449cd121a72080af65711ad022549ed2e33e9508979`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/EPI2_b3lyp_d3_opt_freq_optimized.xyz` — successful execution artifact; SHA-256 `8996ee1e84f7dfe45232439335da685dcea0616a5605ea6b88b1db6f5134b5e4`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/collection.json` — successful execution artifact; SHA-256 `07bde654869a62dbd5ab6643076dd5bf871f8605b42dc52134510eba0e4d05c5`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/formchk.log` — successful execution artifact; SHA-256 `b35c803a7bf0d26e7a75a93ef8d6e874da3fbe272d1fa288b0a499498d51ba2d`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/input.com` — successful execution artifact; SHA-256 `f3b64684e9b50d5a3a1cd8a3b021f26d8e83929bce71698c41ff37704910ba35`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/status.json` — successful status record; SHA-256 `4a8df84aad87a7d7444cc7dd78eedb3838291ad340b15fd213d42aa4ac103f4c`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/collection.json` — successful execution artifact; SHA-256 `2e6beb183e407bef54b1dcbc432b75fc7aa4a44e3c5dcd5ff1616588a5883248`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/input.inp` — successful execution artifact; SHA-256 `df43b7e9fd74e3445c2cf444fa6850e464c6cf880bdbd1043a0f7a49e1402353`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/parsed_observables.json` — successful execution artifact; SHA-256 `a63957d6d3005db3c5d55c47fb66496b57449836e767f4c0b15a0f5c4b88b5b6`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_author_b3d3_631gstar_opt_freq/outputs/execution_jobs/job_fadba05fb77047ea925e820a8fae1ced/status.json` — successful status record; SHA-256 `607936841dd48a30e45819574f22b89a25e23284cf552b894b0247d93c1e49b8`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_author_b3d3_631gstar_opt_freq/outputs/execution_jobs/job_fadba05fb77047ea925e820a8fae1ced/collection.json` — successful execution artifact; SHA-256 `c2feeeb6449183febd2e422bed7468d6e2cbaac75ba9825c317cdb2422c8cff8`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_author_b3d3_631gstar_opt_freq/outputs/execution_jobs/job_fadba05fb77047ea925e820a8fae1ced/input.com` — successful execution artifact; SHA-256 `2b79b2d88bc154f83a0f1157a7d3759f970d3f752d773d99416cd263da0ef95f`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_author_b3d3_631gstar_opt_freq/outputs/execution_jobs/job_fadba05fb77047ea925e820a8fae1ced/request.json` — successful execution artifact; SHA-256 `aa1ce50f0558a9eefe94f257b7195a5a2414725d8efc42eec647ea9b8a0fcdb5`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_author_b3d3_631gstar_opt_freq/outputs/execution_jobs/job_fadba05fb77047ea925e820a8fae1ced/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_fdf488d7da4146619299b91e36f66300/status.json` — successful status record; SHA-256 `be91b6a52cec635b04a9dcf4e1f4487c9b4cf5908126ae7c36e66bc2e8bd08fb`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_fdf488d7da4146619299b91e36f66300/collection.json` — successful execution artifact; SHA-256 `0ea5c1507975884f7d81b6b5bc7134fa10b4c6b0acee625db21d6a672aaedb6b`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_fdf488d7da4146619299b91e36f66300/input.inp` — successful execution artifact; SHA-256 `c502c30755e1c4caf4b3acfbc2bdcf0f025ddf82b77584a6d8c94003c918705e`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_fdf488d7da4146619299b91e36f66300/request.json` — successful execution artifact; SHA-256 `cf2d2dec7eeed8a328d085aa09a18c78397c05279986dc448bae81288cb272b2`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_fdf488d7da4146619299b91e36f66300/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_b3lyp_d3_opt_freq/outputs/execution_jobs/job_256a96b77c7044afa6ff72d25fe7acba/status.json` — successful status record; SHA-256 `985978eeaaacfd01998e93053d20f51e84f8b6bdd691ce2463af7ff3d30a2fe9`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_b3lyp_d3_opt_freq/outputs/execution_jobs/job_256a96b77c7044afa6ff72d25fe7acba/collection.json` — successful execution artifact; SHA-256 `a7d51df58ced026128f1c8cc685b3f68d58ab808f5f1e2b69fea48673a303b06`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_b3lyp_d3_opt_freq/outputs/execution_jobs/job_256a96b77c7044afa6ff72d25fe7acba/input.com` — successful execution artifact; SHA-256 `21fff2e35db910792230aaaf097c21926a28cfa416c01c9005cbb8f54ccbd799`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_b3lyp_d3_opt_freq/outputs/execution_jobs/job_256a96b77c7044afa6ff72d25fe7acba/request.json` — successful execution artifact; SHA-256 `9cd8124c9e0a99fdcbf20304c990a3660709f07cc95351826376ff0577b16887`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_b3lyp_d3_opt_freq/outputs/execution_jobs/job_256a96b77c7044afa6ff72d25fe7acba/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_strict_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_7ee09490c0734bbebbe2d2b99d949099/status.json` — successful status record; SHA-256 `a7eb956bc5fc22bda252c3ff34a77cf21e5e211581dd47288da64b46c1f0de99`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_strict_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_7ee09490c0734bbebbe2d2b99d949099/collection.json` — successful execution artifact; SHA-256 `7d08288a771999fa59e71b174439aeaccec0f3b71243fa554a6111fccea3e813`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_strict_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_7ee09490c0734bbebbe2d2b99d949099/input.inp` — successful execution artifact; SHA-256 `270b4a8390914ba45067dcb801f04822d52ea3302bfbc60984ae190481b7e134`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_strict_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_7ee09490c0734bbebbe2d2b99d949099/request.json` — successful execution artifact; SHA-256 `a5b544d5241f5060779cb6bd8b6b54dbbb17d6ce9b27b2b5a7e7e2964ea4fe6e`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI1_strict_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_7ee09490c0734bbebbe2d2b99d949099/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/outputs/execution_jobs/job_a395998b53764301859d972a1d53d128/status.json` — successful status record; SHA-256 `4906317e80e08fe976d764dbd78b6da10fd07afe9473b273e79c86616d2122af`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/outputs/execution_jobs/job_a395998b53764301859d972a1d53d128/collection.json` — successful execution artifact; SHA-256 `5208c41705438496ab46c53ea673bcb5e87b01c396c639975744ec01e51ac128`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/outputs/execution_jobs/job_a395998b53764301859d972a1d53d128/input.com` — successful execution artifact; SHA-256 `84da96a8adcc32cc0f6e1bd0e068e143796e6e8495305d5dbddce854a18b8a13`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/outputs/execution_jobs/job_a395998b53764301859d972a1d53d128/request.json` — successful execution artifact; SHA-256 `cc3b3a05923712fdc8fb923b27bf3d1a48ba3bffb973c8fe18d2e37759523719`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/outputs/execution_jobs/job_a395998b53764301859d972a1d53d128/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_8f4299fc52144097b64b5bdea28fd23d/status.json` — successful status record; SHA-256 `70aea57942c38c6cb9d7adca09ab0d15d51e406bcc123cb24331d495682b6546`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_8f4299fc52144097b64b5bdea28fd23d/collection.json` — successful execution artifact; SHA-256 `a69b57328829a1b5f0476634193326563058c277516675e6689b08bc936db721`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_8f4299fc52144097b64b5bdea28fd23d/input.inp` — successful execution artifact; SHA-256 `8d28ad873330c02d08a9d1fdb413d1538776ec99343bd4a706a586b434c1d495`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_8f4299fc52144097b64b5bdea28fd23d/request.json` — successful execution artifact; SHA-256 `04065658dbbd833fa5e562d99e9c8fb4deb0035a0a936e3154506ab8d6bb4bc7`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_8f4299fc52144097b64b5bdea28fd23d/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_b3lyp_d3_opt_freq/outputs/execution_jobs/job_27a0825eb93d411281c9e2c505342c52/status.json` — successful status record; SHA-256 `5ec0dd8a8e26cc150d448449cd121a72080af65711ad022549ed2e33e9508979`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_b3lyp_d3_opt_freq/outputs/execution_jobs/job_27a0825eb93d411281c9e2c505342c52/collection.json` — successful execution artifact; SHA-256 `07bde654869a62dbd5ab6643076dd5bf871f8605b42dc52134510eba0e4d05c5`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_b3lyp_d3_opt_freq/outputs/execution_jobs/job_27a0825eb93d411281c9e2c505342c52/input.com` — successful execution artifact; SHA-256 `f3b64684e9b50d5a3a1cd8a3b021f26d8e83929bce71698c41ff37704910ba35`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_b3lyp_d3_opt_freq/outputs/execution_jobs/job_27a0825eb93d411281c9e2c505342c52/request.json` — successful execution artifact; SHA-256 `02905cd3ee059de41b1090c0c3e51363e7522f87848d8327e63b129aa516bd55`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_b3lyp_d3_opt_freq/outputs/execution_jobs/job_27a0825eb93d411281c9e2c505342c52/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_strict_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_62de595fb0da4bc8b98c9c8e58a4abb0/status.json` — successful status record; SHA-256 `4a8df84aad87a7d7444cc7dd78eedb3838291ad340b15fd213d42aa4ac103f4c`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_strict_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_62de595fb0da4bc8b98c9c8e58a4abb0/collection.json` — successful execution artifact; SHA-256 `2e6beb183e407bef54b1dcbc432b75fc7aa4a44e3c5dcd5ff1616588a5883248`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_strict_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_62de595fb0da4bc8b98c9c8e58a4abb0/input.inp` — successful execution artifact; SHA-256 `df43b7e9fd74e3445c2cf444fa6850e464c6cf880bdbd1043a0f7a49e1402353`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_strict_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_62de595fb0da4bc8b98c9c8e58a4abb0/request.json` — successful execution artifact; SHA-256 `ed6547cd9bd6757dcca4bb46f9187213ff768cac7f8b0a2e36db08853317c97e`
- `docs/verification/group_3/paper_2f302589e5e9e420/native_workspace/EPI2_strict_author_ma_def2_tzvpp_sp/outputs/execution_jobs/job_62de595fb0da4bc8b98c9c8e58a4abb0/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/status.json` — label=group_3 paper_2f302589e5e9e420 EPI1_b3lyp_d3_opt_freq; submitted_at=2026-08-29T07:29:43.710548+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/EPI1_b3lyp_d3_opt_freq.chk`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/EPI1_b3lyp_d3_opt_freq.fchk`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/EPI1_b3lyp_d3_opt_freq_optimized.xyz`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/collection.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/formchk.log`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/input.com`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/parsed_observables.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_opt_freq/stderr.log`
2. `artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/status.json` — label=group_3 paper_2f302589e5e9e420 EPI2_b3lyp_d3_opt_freq; submitted_at=2026-08-29T07:29:43.711210+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt Freq; command=g16 < input.com
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/EPI2_b3lyp_d3_opt_freq.chk`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/EPI2_b3lyp_d3_opt_freq.fchk`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/EPI2_b3lyp_d3_opt_freq_optimized.xyz`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/collection.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/formchk.log`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/input.com`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/parsed_observables.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_opt_freq/stderr.log`
3. `artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/status.json` — label=group_3 paper_2f302589e5e9e420 EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp; submitted_at=2026-08-30T04:01:59.015143+00:00; software=orca; intent=single_point; command=orca input.inp
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/collection.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/input.gbw`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/input.inp`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/stderr.log`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_b3lyp_d3_author_ma_def2_tzvpp_sp/stdout.log`
4. `artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/status.json` — label=group_3 paper_2f302589e5e9e420 EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp; submitted_at=2026-08-30T04:02:05.266266+00:00; software=orca; intent=single_point; command=orca input.inp
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/collection.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/input.gbw`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/input.inp`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/stderr.log`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_b3lyp_d3_author_ma_def2_tzvpp_sp/stdout.log`
5. `artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/status.json` — label=group_3 paper_2f302589e5e9e420 EPI1_author_b3d3_631gstar_opt_freq; submitted_at=2026-08-30T17:22:31.766055+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt=(CalcFC,MaxCycles=512) Freq Int=UltraFine NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/EPI1_author_b3d3_631gstar_opt_freq.chk`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/EPI1_author_b3d3_631gstar_opt_freq.fchk`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/EPI1_author_b3d3_631gstar_opt_freq_optimized.xyz`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/collection.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/formchk.log`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/input.com`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/parsed_observables.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_author_b3d3_631gstar_opt_freq/stderr.log`
6. `artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/status.json` — label=group_3 paper_2f302589e5e9e420 EPI1_strict_author_ma_def2_tzvpp_sp; submitted_at=2026-08-31T01:40:05.864089+00:00; software=orca; intent=single_point; command=orca input.inp
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/collection.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/input.gbw`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/input.inp`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/stderr.log`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/stdout.log`
7. `artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/status.json` — label=group_3 paper_2f302589e5e9e420 EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g; submitted_at=2026-09-01T01:30:27.556569+00:00; software=gaussian; intent=optimization_frequency; route=#p B3LYP/6-31G(d) EmpiricalDispersion=GD3BJ Opt=(Cartesian,MaxCycles=256,MaxStep=5) Freq Int=UltraFine NoSymm SCF=(XQC,MaxCycle=1024); command=g16 < input.com
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g.chk`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g.fchk`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g_optimized.xyz`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/collection.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/formchk.log`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/input.com`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/parsed_observables.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_author_b3d3_631gstar_retry2_cartesian_unbounded32g/stderr.log`
8. `artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/status.json` — label=group_3 paper_2f302589e5e9e420 EPI2_strict_author_ma_def2_tzvpp_sp; submitted_at=2026-09-01T10:51:10.554785+00:00; software=orca; intent=single_point; command=orca input.inp
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/collection.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/input.gbw`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/input.inp`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/parsed_observables.json`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/stderr.log`
   - output: `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/stdout.log`

## Historical evaluator alignment (archived snapshot)

> Maintenance clarification (2026-09-18): this section and its rule/value correspondence record the evaluator at the time of the archived calculation, not the current scoring contract. Retired or renamed IDs here are historical, not active scoring requirements. The current five evaluator JSON files are authoritative. This clarification does not change the successful calculations, scientific values or historical logs. Inactive IDs in the header below: `c_limitations`, `r_limits`.

- Key-point IDs: `kp_process_minimum, kp_process_consistent, kp_result_dipole, kp_result_esp`
- Conclusion IDs: `c_final_polarity, c_limitations`
- Scoring-rule IDs: `r_process_minimum, r_process_consistent, r_result_dipole, r_result_percent, r_final, r_limits, r_result_esp`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `None`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r_process_minimum` → reference `kp_process_minimum`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert validation of per-fragment evidence; evaluator_target_present=False
- rule `r_process_consistent` → reference `kp_process_consistent`; type=condition; unit=not recorded; tolerance=not recorded; comparison=expert process comparison; evaluator_target_present=False
- rule `r_result_dipole` → reference `kp_result_dipole`; type=numeric; unit=Debye for EPI2; EPI1 reference 2.2223 Debye; tolerance=0.25; comparison=absolute difference after matching fragment id; evaluator_target_present=True
- rule `r_result_percent` → reference `kp_result_dipole`; type=numeric; unit=percent reduction EPI2 relative to EPI1; tolerance=2.0; comparison=absolute difference; evaluator_target_present=True
- rule `r_final` → reference `c_final_polarity`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_limits` → reference `c_limitations`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r_result_esp` → reference `kp_result_esp`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r_result_dipole` / reference `kp_result_dipole`: target=1.9036 Debye for EPI2; EPI1 reference 2.2223 Debye; tolerance=0.25; numeric result leaves=[2.223986032, 1.899046595]; within_tolerance=True; applicability=applicable
- rule `r_result_percent` / reference `kp_result_dipole`: target=14.3 percent reduction EPI2 relative to EPI1; tolerance=2.0; numeric result leaves=[14.610677959509776]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[0].id` = `"EPI1"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[0].validated` = `true`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[0].validation_evidence` = `"ORCA normal termination, author-layer ma-def2-TZVPP single point on frequency-validated 6-31G* geometry; artifact artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/stdout.log"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[0].dipole_debye` = `2.223986032`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[0].hydroxyl_oxygen_esp_kcal_mol` = `null`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[0].esp_definition` = `"Not calculated."`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[0].optimization_evidence` = `"Geometry inherited from validated Gaussian EPI1_author_b3d3_631gstar_opt_freq Opt/Freq endpoint."`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[0].property_evidence` = `"Dipole parsed from ORCA Dipole moment block: 2.223986 D."`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[1].id` = `"EPI2"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[1].validated` = `true`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[1].validation_evidence` = `"ORCA normal termination, author-layer ma-def2-TZVPP single point on frequency-validated 6-31G* geometry; artifact artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/stdout.log"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[1].dipole_debye` = `1.899046595`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[1].hydroxyl_oxygen_esp_kcal_mol` = `null`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[1].esp_definition` = `"Not calculated."`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[1].optimization_evidence` = `"Geometry inherited from validated Gaussian EPI2_author_b3d3_631gstar_opt_freq Opt/Freq endpoint."`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.fragments` / result path `$.fragments[1].property_evidence` = `"Dipole parsed from ORCA Dipole moment block: 1.899047 D."`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.method.minimum_test` / result path `$.method.minimum_test` = `"Inherited from Gaussian Opt/Freq endpoints"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[0].candidate_id` = `"EPI1_strict_author_ma_def2_tzvpp_sp"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[0].fragment_id` = `"EPI1"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[0].generation_rationale` = `"Public displaced XYZ geometry optimized at common Gaussian protocol; ORCA author-layer property single point"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[0].energy` = `null`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[0].validation_evidence` = `"ORCA normal termination; dipole parsed."`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[0].advanced` = `true`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[1].candidate_id` = `"EPI2_strict_author_ma_def2_tzvpp_sp"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[1].fragment_id` = `"EPI2"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[1].generation_rationale` = `"Public displaced XYZ geometry optimized at common Gaussian protocol; ORCA author-layer property single point"`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[1].energy` = `null`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[1].validation_evidence` = `"ORCA normal termination; dipole parsed."`
- rule `r_process_minimum` / reference `kp_process_minimum` / field `$.candidate_records` / result path `$.candidate_records[1].advanced` = `true`
- rule `r_process_consistent` / reference `kp_process_consistent` / field `$.method` / result path `$.method.software` = `"ORCA 6.1.1; parser"`
- rule `r_process_consistent` / reference `kp_process_consistent` / field `$.method` / result path `$.method.model` = `"B3LYP-D3BJ/ma-def2-TZVPP"`
- rule `r_process_consistent` / reference `kp_process_consistent` / field `$.method` / result path `$.method.optimization_protocol` = `"Single point on Gaussian B3LYP-D3BJ/6-31G* (6-31G(d)) frequency-validated geometries"`
- rule `r_result_dipole` / reference `kp_result_dipole` / field `$.fragments[*].dipole_debye` / result path `$.fragments[*].dipole_debye` = `2.223986032`
- rule `r_result_dipole` / reference `kp_result_dipole` / field `$.fragments[*].dipole_debye` / result path `$.fragments[*].dipole_debye` = `1.899046595`
- rule `r_result_percent` / reference `kp_result_dipole` / field `$.percent_reduction_EPI2_vs_EPI1` / result path `$.percent_reduction_EPI2_vs_EPI1` = `14.610677959509776`
- rule `r_final` / reference `c_final_polarity` / field `$.conclusion` / result path `$.conclusion` = `"Author-layer EPI1 dipole=2.2240 D and EPI2 dipole=1.8990 D; EPI2 is lower by 14.61% (signed change -14.61%)."`
- rule `r_limits` / reference `c_limitations` / field `$.limitations` / result path `$.limitations` = `"Author property layer is a single point on Gaussian-optimized isolated fragments; ESP not calculated and conformer/functional sensitivity remains. Low-layer Gaussian dipoles are retained in evidence artifacts for sensitivity."`
- rule `r_result_esp` / reference `kp_result_esp` / field `$.fragments[*].hydroxyl_oxygen_esp_kcal_mol` / result path `$.fragments[*].hydroxyl_oxygen_esp_kcal_mol` = `null`
- rule `r_result_esp` / reference `kp_result_esp` / field `$.fragments[*].esp_definition` / result path `$.fragments[*].esp_definition` = `"Not calculated."`

## Historical final-assembly review flag

- Previous assembly decision: **EQUIVALENT_SAFE**
- Previous review reason: Only wording/heading/schema-reference normalization; no input/evaluator semantic change.
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Complete neutral singlet EPI1 and EPI2 starting XYZ geometries with fixed atom identities.

Public input files and hashes:

- `agent_input/data/inputs/EPI1_start.xyz` — SHA-256 `af480e708779a22588b951bc59f9afa701de956939207a25f33bff5fd5683475`; size=1209 bytes; xyz_atom_count=37; xyz_comment=SI-derived starting coordinates; neutral singlet; preserve atom order.; explicit_boundary_fields=not recorded
- `agent_input/data/inputs/EPI2_start.xyz` — SHA-256 `2a136d9d85e583b7b3cc3557a88d907e8bc667e69fa9b6e682007b6ba3fec6d9`; size=1331 bytes; xyz_atom_count=41; xyz_comment=SI-derived starting coordinates; neutral singlet; preserve atom order.; explicit_boundary_fields=not recorded

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `agent_input/data/inputs/EPI1_start.xyz, agent_input/data/inputs/EPI2_start.xyz`

## Evidence files

- `docs/verification/group_3/paper_2f302589e5e9e420/verification_report.md` — verification record; SHA-256 `2899ac7227e1864f2f376066f07bfcec376ee295d974ad015a4866efabf3928f`
- `docs/verification/group_3/paper_2f302589e5e9e420/report/results.json` — verification record; SHA-256 `f6219e432679bffc20c57ddc1e008002684d7c9551e7c54708404eab9cf28823`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI1_strict_author_ma_def2_tzvpp_sp/stdout.log` — referenced successful evidence; SHA-256 `0d363ae806b9439c17ecbd03013dad8256d978a26362da5c1452b4f32cedbc0f`
- `docs/verification/group_3/paper_2f302589e5e9e420/artifacts/gaussian/EPI2_strict_author_ma_def2_tzvpp_sp/stdout.log` — referenced successful evidence; SHA-256 `a8b9304da645a5aafecdfd3f8455e2fb8394aac763e6b3cd44d31aa171fab9bc`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.
