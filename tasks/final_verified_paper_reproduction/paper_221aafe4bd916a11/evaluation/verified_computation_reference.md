# Verified computation reference — paper_221aafe4bd916a11 (paper_reproduction)

> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.

## Connection interpretation correction (2026-09-18)

The existing forward/reverse IRC calculations support the local P–H cleavage/C–H formation event around the hydride-transfer TS. They do **not** by themselves demonstrate optimization all the way to the separated reactant and product basins. The separately computed 2a/CO2 minima and product-side minimum are independent endpoint evidence, not IRC endpoint optimizations. The historical sentence below claiming direct connection to separated basins is an overstatement and is superseded by this paragraph.

Keep the successful local hydride-transfer task and its independently referenced barrier (19.8719700 kcal/mol in the archived branch). A finite 100-point path is not automatically a failure, and this correction does not add an unrequested full-cycle or separated-basin requirement. No new calculation was performed; historical group results remain untouched.

## Status

Historical status below describes the archived group calculation; it is not a new run from any modified public starter.

- Computation-chain status: **EVIDENCE_COMPLETE**
- Group result status: `complete` (SUCCESS_EVIDENCE_CANDIDATE)
- Verification-report terminal status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE)
- Applicability to current final package: **AUTHOR_ROUTE_ONLY_PUBLIC_STARTER_NOT_REPLAYED**
- Applicability note: Public 2a geometry was replaced by a deterministic displaced starter; group verification used the original author endpoint. Under the accepted author-route verification policy this starter difference is not itself a task/evaluator mismatch; no independent discovery or public-starter replay is claimed.

Verification-report status history (explicit terminal-status statements):

| line | status | statement |
|---:|---|---|
| 7 | `BLOCKED` | - 论文复现结论：**BLOCKED**。反应物端点已真实完成 Opt/Freq，但任务公开输入没有 product、TS candidate 或 IRC 终点，不能从反应物猜测势垒。 |
| 28 | `BLOCKED` | - 由于任务公开输入只提供反应物 2a，没有可验证的 product/TS 候选，论文复现结论保持 **BLOCKED**；不报告猜测的势垒。 |
| 83 | `PASS` | - evaluator 五文件在独立计算冻结后逐项读取并记录哈希；本轮结果：`PASS`。 |
| 92 | `PASS` | 字段均由真实成功输出支持，当前作者路线资格为 **PASS**（仅限声明的 2a+CO₂、 |

The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.

## Source identity

- Paper: Protonated bisphosphines: a new class of powerful hydride donors capable of CO2 reduction
- DOI: `10.1039/d5cc06952a`
- Task package: `tasks/final_verified_paper_reproduction/paper_221aafe4bd916a11`
- Verification group: `docs/verification/group_2/paper_221aafe4bd916a11`
- Paper documents: `papers/paper_221aafe4bd916a11`
- Input identity audit: **MATCHED** (title_match=True, doi_match=True)

## Selected barrier convention (clarified 2026-09-18)

The archived 19.8719700 kcal/mol branch uses G(TS) = -2324.733530 Eh from the successful standalone frequency output, G(2a) = -2136.233723 Eh from `artifacts/gaussian_batch/2a_reactant_optfreq/stdout.log`, and G(CO2) = -188.531475 Eh from `artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/stdout.log`. Each raw thermochemistry block specifies 298.150 K and 1 atm. The barrier is their stoichiometric difference; no separate 1 M correction was applied. This historical low-basis verification branch is not the SI high-basis single-point composite route. No new calculation or scientific target change is asserted.

## Successful calculation chain

The structured excerpt below is derived from `report/results.json`. Entries whose status/outcome indicates failure, retry, interruption, queueing, or unresolved work were omitted. Large arrays are represented by a bounded success-only excerpt.

```json
{
  "barrier_kcal_mol": 19.871970024681406,
  "candidates": [
    {
      "candidate_id": "2a_reactant_in_out",
      "disposition": "reactant endpoint validated",
      "frequency_summary": "Gaussian Opt/Freq normal=True; frequencies=231; imaginary=0",
      "geometry_or_source": "artifacts/gaussian_batch/2a_reactant_optfreq_optimized.xyz",
      "role": "reactant minimum"
    },
    {
      "candidate_id": "TS2_2a_si_recovered_ts_optfreq",
      "disposition": "validated TS with bidirectional IRC",
      "frequency_summary": "status=success; normal=True; opt_complete=True; frequencies=240; imaginary=1",
      "geometry_or_source": "SI-recovered TS optimization followed by successful standalone frequency calculation; frequency/Gibbs evidence: artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/stdout.log (the early optfreq summary alone does not contain complete frequencies)",
      "role": "hydride-transfer transition-state candidate"
    },
    {
      "candidate_id": "2a_dication_formate_si_recovered_optfreq",
      "disposition": "frequency-validated product-side endpoint",
      "frequency_summary": "status=success; normal=True; frequencies=240; imaginary=0",
      "geometry_or_source": "SI-recovered candidate; managed Gaussian evidence under artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq_summary.json",
      "role": "product-side dication/formate endpoint"
    },
    {
      "candidate_id": "author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20",
      "disposition": "validated CO2 component",
      "frequency_summary": "status=success; normal=True; frequencies=4; imaginary=0",
      "geometry_or_source": "Independent component; managed Gaussian evidence under artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_summary.json",
      "role": "neutral CO2 reactant component"
    }
  ],
  "hypotheses": [
    {
      "candidate_tests": [
        "Frequency validation of the SI-recovered TS2 gives exactly one imaginary mode.",
        "Forward and reverse IRC calculations both terminate normally and connect the TS basin to the separated reactant/product-side basins."
      ],
      "description": "A single-step hydride transfer from the in-out 2a cation to CO2, without a discrete intermediate.",
      "discrimination_test": "Validate a one-imaginary-frequency TS and inspect both forward and reverse IRC paths for direct connection versus a discrete intermediate.",
      "evidence": [
        "validation.transition_state",
        "validation.connectivity_test",
        "mechanism_conclusion"
      ],
      "hypothesis_id": "direct_hydride_transfer",
      "outcome": "supported"
    },
    {
      "candidate_tests": [
        "The same bidirectional IRC path was inspected for a separate stationary intermediate between the validated TS and endpoint basins."
      ],
      "description": "Hydride transfer proceeds through a discrete intermediate before the product-side endpoint.",
      "discrimination_test": "Inspect the validated bidirectional IRC path for a separate stationary intermediate between the TS and endpoint basins.",
      "evidence": [
        "validation.connectivity_test",
        "mechanism_conclusion",
        "limitations"
      ],
      "hypothesis_id": "stepwise_intermediate",
      "outcome": "not_observed_under_stated_model"
    }
  ],
  "limitations": "SI-recovered coordinates are verification-stage facts and are not task-visible inputs. The barrier is reported only after validating the separated 2a and CO2 reactant components and matching their summed stoichiometry to the TS/product; no incomparable-energy subtraction is used.",
  "mechanism_conclusion": "The SI-recovered 2a+CO2 candidate supports a direct hydride-transfer path with no discrete intermediate under the stated model; the barrier is computed from the validated TS Gibbs energy minus the separated 2a and CO2 reactant Gibbs energies.",
  "method": {
    "charge": 1,
    "electronic_structure": "wB97XD/6-31G(d,p)",
    "multiplicity": 1,
    "solvent": "PCM acetonitrile",
    "temperature_K": 298
  },
  "status": "complete",
  "validation": {
    "co2_component": "status=success; normal=True; optimization_completed=True; imaginary_frequency_count=0; valid=True",
    "connectivity_test": "forward/reverse IRC successes=['forward', 'reverse']; bidirectional_complete=True",
    "reactant_minimum": "optimization_completed=True, normal_termination=True, imaginary_frequency_count=0",
    "reactant_pair_gibbs_hartree": -2324.765198,
    "stoichiometry": "2a={'C': 26, 'P': 2, 'N': 8, 'H': 43} + CO2={'C': 1, 'O': 2} -> TS={'C': 27, 'P': 2, 'N': 8, 'O': 2, 'H': 43} / product={'C': 27, 'P': 2, 'N': 8, 'H': 43, 'O': 2}; match=True",
    "transition_state": "TS status=success; one_imaginary_frequency=True; TS/product SI recovery is isolated from agent-visible branch"
  }
}
```

## Re-audit source-evidence drift

- Classification: **SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW**
- Previous `results.json` SHA-256: `9bbb3c42314d30e2c4a64decd7b1ff787e2ad780bcf2990ebd86030aa894cb62`
- Current `results.json` SHA-256: `ab038a64ef375bb445a3618034b62cbc00b3290332330568aa33e90a5d7be989`
- Changed top-level result fields: `hypotheses`
- Changed execution-artifact paths: `none detected`

A source hash change is not treated as a new scientific result. Runtime-only changes remain metadata drift; any other change requires semantic comparison of the provenance record. This archive is not a scoring standard.

<!-- source-drift-json: {"changed_artifact_paths": [], "changed_top_level_keys": ["hypotheses"], "classification": "SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW", "current_sha256": "ab038a64ef375bb445a3618034b62cbc00b3290332330568aa33e90a5d7be989", "detected": true, "previous_sha256": "9bbb3c42314d30e2c4a64decd7b1ff787e2ad780bcf2990ebd86030aa894cb62"} -->

Paper/SI document hashes:

- `papers/paper_221aafe4bd916a11/documents/main.pdf` — SHA-256 `9ab7929cb298e4351c64bdb02eca8bf833e107be8150df9d35cc992c96b12d74` (declared_match=True)
- `papers/paper_221aafe4bd916a11/documents/supplementary_001.pdf` — SHA-256 `c845d5d84e548a9d87d0193a131c9673de378c86f7e31bc979938a66d84ca3fc` (declared_match=True)

Report evidence lines retained:

- 任务可见输入为 `tasks/paper_reproduction/paper_221aafe4bd916a11/agent_input/data/inputs/2a_inout.xyz`（79 原子）。验证阶段采用 Gaussian 16 C.01，`wB97XD/6-31G(d,p) Opt Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm`，charge `1`、multiplicity `1`。最小反应物端点要求优化正常终止、频率输出完整且无虚频；势垒要求另外有可验证 product/TS/IRC 结构，这些输入未提供。
- 作业 `job_88b46c33af654acb8c9efb5c3df76aa5` 通过原生 Gaussian supervisor 提交，使用 8 CPU、24000 MB，`walltime_seconds=null`（无人工墙钟上限）。Gaussian 输出有 `Optimization completed`、`Stationary point found` 和 `Normal termination of Gaussian 16`；频率数 231，虚频数 0，最低频率 22.1385 cm⁻¹，最终 SCF 能量 −2136.84554897 Eh。优化结构由通用 orientation 提取器保存。
- - evaluator 五文件在独立计算冻结后逐项读取并记录哈希；本轮结果：`PASS`。

## Provenance anchors for the retained chain

- Successful status/output inventory entries: **100**
- Concrete input anchor present: **True**
- Concrete output/log anchor present: **True**

The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.

- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/status.json` — successful status record; SHA-256 `a447749d76e417c6ed1041dd3f2b79fafd95ba61e719efdfe942c6b4e77c677f`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/collection.json` — successful execution artifact; SHA-256 `3957ce5a6d70992f0059484773a95b1a3065793e522f33dccd55b18177b75208`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/input.com` — successful execution artifact; SHA-256 `b7fc4e468bc4509687ed403f258f5befb36f56ac2af23457efda1c9373d71acb`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/stdout.log` — successful execution artifact; SHA-256 `c61f150b52f53694456d6f11a01a3a1c67e5da5a457baedf3c7c4051d193a95b`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/status.json` — successful status record; SHA-256 `7efadbefd1785ce18203aa5bcf404e6f0c220c777ea5fa84a3d2a8eba8c1d743`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/collection.json` — successful execution artifact; SHA-256 `eecd61acc5dbfd792919dd8364eceafbc411496de6c53226741291504950843d`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/input.com` — successful execution artifact; SHA-256 `fc5a274764bfa39b1234af1f20eee994723e397ceb191159ebcfd96dd6e3dcee`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/stdout.log` — successful execution artifact; SHA-256 `c3f6a3ea6995f59adc2451ad044f72bbbff6dab8ed2f7eb60e2c6c592f214338`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/status.json` — successful status record; SHA-256 `b75b758e66720026462de1a1ec034e157fdbb31ff5bb564f99223a26cf154135`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/collection.json` — successful execution artifact; SHA-256 `8f4066888d23c3f745befc8592dc166ce58b9c6d03a42a3980f42ccf2502e49f`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/input.com` — successful execution artifact; SHA-256 `47b5ec8e27743c37b2647a0f0f5a753108f0026c88065557fb74e0ffb186bebc`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/stdout.log` — successful execution artifact; SHA-256 `77b514d80bae65addc190ba07db2001493d837d6753ad10563a5d3ed96275c2c`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/status.json` — successful status record; SHA-256 `70e5e7c9bf89cbab7f2ca8024c0fdfbb66f7b35e7683491866bc31832b7a8038`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/collection.json` — successful execution artifact; SHA-256 `9e67e37c62995b5e8ebbcab9b86c493437813513da3caca28deda73e6e9a5cd1`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/input.com` — successful execution artifact; SHA-256 `6f9bd835888a14ae79ca7d5de5c3834493011455dc9667cea927349511809a7e`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/repair.xyz` — successful execution artifact; SHA-256 `f6557496ea5147080fbb610b54f9cfc0a3014ef8d62dd445ebfe1efcc294a734`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/route_manifest.json` — successful execution artifact; SHA-256 `b193ddb00ede61f58d3979e74669574d1c616c5a4a58507584fa204f2e322a26`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/status.json` — successful status record; SHA-256 `e5163288aedcd821ca8cdc831485b2ee798e50205801e1a2892fff07b76e4511`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/input.com` — successful execution artifact; SHA-256 `07f72cd5514bdc7624647277c6c6588ff04b4f05b5fac79be847298131b26c2f`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/route_manifest.json` — successful execution artifact; SHA-256 `6ca69b177b0568551830c29048eb6bf505bb1a9a36d1a2d887f6d15d95e0b63f`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/source_input.com` — successful execution artifact; SHA-256 `07f72cd5514bdc7624647277c6c6588ff04b4f05b5fac79be847298131b26c2f`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/status.json` — successful status record; SHA-256 `c0739a336e838aa189a46affe3529d11fce7b58bb196ddf46f2958f3ed8371d2`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/input.com` — successful execution artifact; SHA-256 `5bf57f19bde3c2a58db4ce16d27849ba5db425d77eb27d52c0d74c4658b90ca1`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/route_manifest.json` — successful execution artifact; SHA-256 `d1d08791fc3c50b61ad1ae7e59dae94384c1c9ef9a79612728a2453769c96138`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/source_input.com` — successful execution artifact; SHA-256 `5bf57f19bde3c2a58db4ce16d27849ba5db425d77eb27d52c0d74c4658b90ca1`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/status.json` — successful status record; SHA-256 `60b3dee5e627c59faf8ae3867d234c63adbfec48246b91092bc3316e23770647`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/input.com` — successful execution artifact; SHA-256 `d1e322d1f84c77d3c83e8a4a3d3c4815abda484f853e38bbcf132b4868ce5e28`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/route_manifest.json` — successful execution artifact; SHA-256 `5a587d36381c2ae344ebb197a191caca2de44c79472b9c37e67c3dff0037bb78`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/source_input.com` — successful execution artifact; SHA-256 `d1e322d1f84c77d3c83e8a4a3d3c4815abda484f853e38bbcf132b4868ce5e28`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/status.json` — successful status record; SHA-256 `6f619bce7c7e1c87e7690682de3d02dfcf749c29728bc97d9bdf814cc63780c0`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/input.com` — successful execution artifact; SHA-256 `1e5346c8cb5d7512071664645550440b04ac9e45bb3d265696c465fe0688e78b`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/route_manifest.json` — successful execution artifact; SHA-256 `e754d72bc409267b3e8656cfedfda96633966b83db4c8bd845b1081ab38a51e6`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/source_input.com` — successful execution artifact; SHA-256 `1e5346c8cb5d7512071664645550440b04ac9e45bb3d265696c465fe0688e78b`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/status.json` — successful status record; SHA-256 `da0ec43a12d8292f145ef166a007b9aa1816352b770d25d8f5f549f357e65dce`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/collection.json` — successful execution artifact; SHA-256 `c347864fbea851cff7c0830be43a0e274cc4983d93952848000afbc974769655`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/input.com` — successful execution artifact; SHA-256 `e6b851762022c3097bbd15d21c54b81e82fbeb88bae5938bce2003e5dcef7b42`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/route_manifest.json` — successful execution artifact; SHA-256 `60e374b28d8ff7ac820075e1f16168d5cd884bb84766f5082c09d735cff52664`
- `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_02a6e32e9c04476da0ef929682a89124/status.json` — successful status record; SHA-256 `da0ec43a12d8292f145ef166a007b9aa1816352b770d25d8f5f549f357e65dce`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_02a6e32e9c04476da0ef929682a89124/collection.json` — successful execution artifact; SHA-256 `c347864fbea851cff7c0830be43a0e274cc4983d93952848000afbc974769655`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_02a6e32e9c04476da0ef929682a89124/input.com` — successful execution artifact; SHA-256 `e6b851762022c3097bbd15d21c54b81e82fbeb88bae5938bce2003e5dcef7b42`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_02a6e32e9c04476da0ef929682a89124/request.json` — successful execution artifact; SHA-256 `02a113d8f44ec062cef0764f1213929fcb986855c32da9a0fd5f9582f3aa6b26`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_02a6e32e9c04476da0ef929682a89124/status.interruption_recovery.json` — successful execution artifact; SHA-256 `556309a921584d000df93c61812495abbda4649979a73c630925cd6e8374005f`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_0ab508cf3b014ec1a5f03c10d26efd8f/status.json` — successful status record; SHA-256 `b75b758e66720026462de1a1ec034e157fdbb31ff5bb564f99223a26cf154135`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_0ab508cf3b014ec1a5f03c10d26efd8f/collection.json` — successful execution artifact; SHA-256 `8f4066888d23c3f745befc8592dc166ce58b9c6d03a42a3980f42ccf2502e49f`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_0ab508cf3b014ec1a5f03c10d26efd8f/group2_stop_reconciliation.json` — successful execution artifact; SHA-256 `28ccbfa1f23579b20c978176c50efef318d3d29bcb5cb3e15bf6a126f66214aa`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_0ab508cf3b014ec1a5f03c10d26efd8f/input.com` — successful execution artifact; SHA-256 `47b5ec8e27743c37b2647a0f0f5a753108f0026c88065557fb74e0ffb186bebc`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_0ab508cf3b014ec1a5f03c10d26efd8f/request.json` — successful execution artifact; SHA-256 `b89d8ab13f33c1f1c7f602c36adce9f6cc748589e7452e9ec3946d149f693146`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_88b46c33af654acb8c9efb5c3df76aa5/status.json` — successful status record; SHA-256 `7efadbefd1785ce18203aa5bcf404e6f0c220c777ea5fa84a3d2a8eba8c1d743`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_88b46c33af654acb8c9efb5c3df76aa5/collection.json` — successful execution artifact; SHA-256 `eecd61acc5dbfd792919dd8364eceafbc411496de6c53226741291504950843d`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_88b46c33af654acb8c9efb5c3df76aa5/input.com` — successful execution artifact; SHA-256 `fc5a274764bfa39b1234af1f20eee994723e397ceb191159ebcfd96dd6e3dcee`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_88b46c33af654acb8c9efb5c3df76aa5/request.json` — successful execution artifact; SHA-256 `2950600ba8ddb299fc8144fbff4aaf916a63d383516a657fb028d3f79a44543a`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_88b46c33af654acb8c9efb5c3df76aa5/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_be697211c6a1491eaea5a95589b3e105/status.json` — successful status record; SHA-256 `70e5e7c9bf89cbab7f2ca8024c0fdfbb66f7b35e7683491866bc31832b7a8038`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_be697211c6a1491eaea5a95589b3e105/collection.json` — successful execution artifact; SHA-256 `9e67e37c62995b5e8ebbcab9b86c493437813513da3caca28deda73e6e9a5cd1`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_be697211c6a1491eaea5a95589b3e105/input.com` — successful execution artifact; SHA-256 `6f9bd835888a14ae79ca7d5de5c3834493011455dc9667cea927349511809a7e`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_be697211c6a1491eaea5a95589b3e105/request.json` — successful execution artifact; SHA-256 `354b609127bf851c991acc35c695eb318e06cd0a3b22fc607e562271cce68e67`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_be697211c6a1491eaea5a95589b3e105/status.interruption_recovery.json` — successful execution artifact; SHA-256 `fa78b7f3421933ba9ed4de4647082e2b7724396d32729202c5a4f7c10fe3b342`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_c065592ec41c4aebbc13f603395d86d8/status.json` — successful status record; SHA-256 `a447749d76e417c6ed1041dd3f2b79fafd95ba61e719efdfe942c6b4e77c677f`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_c065592ec41c4aebbc13f603395d86d8/collection.json` — successful execution artifact; SHA-256 `3957ce5a6d70992f0059484773a95b1a3065793e522f33dccd55b18177b75208`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_c065592ec41c4aebbc13f603395d86d8/input.com` — successful execution artifact; SHA-256 `b7fc4e468bc4509687ed403f258f5befb36f56ac2af23457efda1c9373d71acb`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_c065592ec41c4aebbc13f603395d86d8/request.json` — successful execution artifact; SHA-256 `b6bcfe623e19a5081f78229ee646089d1a612a39d0b984645ddccb9447a3bf7b`
- `docs/verification/group_2/paper_221aafe4bd916a11/native_workspace_batch/outputs/execution_jobs/job_c065592ec41c4aebbc13f603395d86d8/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/status.json` — successful status record; SHA-256 `9a61aade67d8a8e80cc419d1c3dbf63a8934e011c210e482527af494126b8871`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `1b2e3c55266d5935696796f088b5fe068c2d91ddfdc317d5f1d2560b412ec3a9`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/input.com` — successful execution artifact; SHA-256 `973fec7ea4cc42bf53a06fa71abae9cd9e96fadb47a729fb50ff001e5729eeb7`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/route_manifest.json` — successful execution artifact; SHA-256 `b193ddb00ede61f58d3979e74669574d1c616c5a4a58507584fa204f2e322a26`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/status.json` — successful status record; SHA-256 `e5163288aedcd821ca8cdc831485b2ee798e50205801e1a2892fff07b76e4511`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `d11b228f7590105d7ca7790c99aecdb350a0068fd6e9d5bc35746595a7c1ddcf`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/input.com` — successful execution artifact; SHA-256 `07f72cd5514bdc7624647277c6c6588ff04b4f05b5fac79be847298131b26c2f`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/route_manifest.json` — successful execution artifact; SHA-256 `6ca69b177b0568551830c29048eb6bf505bb1a9a36d1a2d887f6d15d95e0b63f`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/source_input.com` — successful execution artifact; SHA-256 `07f72cd5514bdc7624647277c6c6588ff04b4f05b5fac79be847298131b26c2f`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/status.json` — successful status record; SHA-256 `c0739a336e838aa189a46affe3529d11fce7b58bb196ddf46f2958f3ed8371d2`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `84506db6a119fa34796edff09fbe91bc4bc2b03fae3d9e86bbf3d380ef2ccdd8`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/input.com` — successful execution artifact; SHA-256 `5bf57f19bde3c2a58db4ce16d27849ba5db425d77eb27d52c0d74c4658b90ca1`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/route_manifest.json` — successful execution artifact; SHA-256 `d1d08791fc3c50b61ad1ae7e59dae94384c1c9ef9a79612728a2453769c96138`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/source_input.com` — successful execution artifact; SHA-256 `5bf57f19bde3c2a58db4ce16d27849ba5db425d77eb27d52c0d74c4658b90ca1`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/status.json` — successful status record; SHA-256 `60b3dee5e627c59faf8ae3867d234c63adbfec48246b91092bc3316e23770647`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `6d245037fffed9e858474b521547a1c4f2e5ea50f647b524b2720d07a20a3195`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/input.com` — successful execution artifact; SHA-256 `d1e322d1f84c77d3c83e8a4a3d3c4815abda484f853e38bbcf132b4868ce5e28`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/route_manifest.json` — successful execution artifact; SHA-256 `5a587d36381c2ae344ebb197a191caca2de44c79472b9c37e67c3dff0037bb78`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/source_input.com` — successful execution artifact; SHA-256 `d1e322d1f84c77d3c83e8a4a3d3c4815abda484f853e38bbcf132b4868ce5e28`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/status.json` — successful status record; SHA-256 `6f619bce7c7e1c87e7690682de3d02dfcf749c29728bc97d9bdf814cc63780c0`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `3bb7500e2cc19bf01061029af3cfddb9f2f607876c6921091fd96fd4759575a0`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/input.com` — successful execution artifact; SHA-256 `1e5346c8cb5d7512071664645550440b04ac9e45bb3d265696c465fe0688e78b`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/route_manifest.json` — successful execution artifact; SHA-256 `e754d72bc409267b3e8656cfedfda96633966b83db4c8bd845b1081ab38a51e6`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/source_input.com` — successful execution artifact; SHA-256 `1e5346c8cb5d7512071664645550440b04ac9e45bb3d265696c465fe0688e78b`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/status.json` — successful status record; SHA-256 `96db83154561cfa2adcff9459dc03561495d6340c452ba321888857b5e2f7f46`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/hpc_collection_record.json` — successful execution artifact; SHA-256 `66fe5d351b6a68b6eea1b9edcc1f3ab715ba8c000b2ea839e299449619d54ada`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/input.com` — successful execution artifact; SHA-256 `5d870d2f1a91187e6cec878b02e8cd5fa5bfe296356c2736acabc917eb38dd9a`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/route_manifest.json` — successful execution artifact; SHA-256 `60e374b28d8ff7ac820075e1f16168d5cd884bb84766f5082c09d735cff52664`
- `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/stderr.log` — successful execution artifact; SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`

## Ordered successful execution steps

Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.

1. `artifacts/gaussian_batch/2a_reactant_optfreq/status.json` — label=group_2 paper_221aafe4bd916a11 2a_reactant_optfreq; submitted_at=2026-08-29T09:32:41.694489+00:00; software=gaussian; intent=optimization_frequency; route=#p wB97XD/6-31G(d,p) Opt Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm; command=g16 < input.com
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/2a_reactant_optfreq.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_reactant_optfreq/stdout.log`
2. `artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/status.json` — label=group_2 paper_221aafe4bd916a11 TS2_2a_si_recovered_ts_optfreq; submitted_at=2026-08-30T02:44:52.051203+00:00; software=gaussian; intent=transition_state; route=#p wB97XD/6-31G(d,p) Opt=(TS,CalcFC,NoEigenTest,MaxCycles=200) Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm Int=UltraFine SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/TS2_2a_si_recovered_ts_optfreq.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/TS2_2a_si_recovered_ts_optfreq/stdout.log`
3. `artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/status.json` — label=group_2 paper_221aafe4bd916a11 2a_dication_formate_si_recovered_optfreq; submitted_at=2026-08-30T02:46:08.658734+00:00; software=gaussian; intent=optimization_frequency; route=#p wB97XD/6-31G(d,p) Opt=(CalcFC,MaxCycles=200) Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm Int=UltraFine SCF=(XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/2a_dication_formate_si_recovered_optfreq.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/2a_dication_formate_si_recovered_optfreq/stdout.log`
4. `artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/status.json` — label=group_2 paper_221aafe4bd916a11 author_2a_reactant_wb97xd_631gdp_pcm_optfreq; submitted_at=2026-08-31T17:12:39.083476+00:00; software=gaussian; intent=optimization_frequency; route=#p wB97XD/6-31G(d,p) Opt=(CalcFC,MaxCycles=300) Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm Int=UltraFine SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/author_2a_reactant_wb97xd_631gdp_pcm_optfreq.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/collection.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/repair.xyz`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/stdout.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_2a_reactant_wb97xd_631gdp_pcm_optfreq/tmp.fchk`
5. `artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/status.json` — label=group_2 paper_221aafe4bd916a11 author_TS2_2a_wb97xd_631gdp_pcm_ts; submitted_at=2026-08-31T17:17:39.674855+00:00; software=gaussian; intent=transition_state; route=#p wB97XD/6-31G(d,p) Opt=(TS,CalcFC,NoEigenTest,MaxCycles=300) Freq SCRF=(PCM,Solvent=Acetonitrile) NoSymm Int=UltraFine SCF=(Tight,XQC,MaxCycle=512); command=g16 < input.com
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/author_TS2_2a_wb97xd_631gdp_pcm_ts.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/collection.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_ts/stdout.log`
6. `artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/status.json` — label=artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20/stdout.log`
7. `artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/status.json` — label=artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20/stdout.log`
8. `artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/status.json` — label=artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20/stdout.log`
9. `artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/status.json` — label=artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/artifacts/gaussian_batch/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20/stdout.log`
10. `provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/status.json` — label=provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/author_2a_reactant_wb97xd_631gdp_pcm_optfreq.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_2a_reactant_wb97xd_631gdp_pcm_optfreq_hpc20_20260906T051030Z/stdout.log`
11. `provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/status.json` — label=provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_CO2_wb97xd_631gdp_pcm_optfreq_hpc20_20260904T103459Z/stderr.log`
12. `provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/status.json` — label=provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_forward_hpc20_20260903T052237Z/stderr.log`
13. `provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/status.json` — label=provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_irc_reverse_hpc20_20260903T055013Z/stderr.log`
14. `provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/status.json` — label=provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/source_input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_standalone_freq_repair_hpc20_20260903T031127Z/stderr.log`
15. `provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/status.json` — label=provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/status.json
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/author_TS2_2a_wb97xd_631gdp_pcm_ts.chk`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/complete.marker`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/hpc_collection_record.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/input.com`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/route_manifest.json`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/sha256sums.txt`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/stderr.log`
   - output: `docs/verification/group_2/paper_221aafe4bd916a11/provenance/qzcli_hpc/author_TS2_2a_wb97xd_631gdp_pcm_ts_hpc20_20260906T051040Z/stdout.log`

## Evaluator alignment

- Key-point IDs: `pr_process_freq, pr_process_path, pr_result_barrier, pr_result_mechanism`
- Conclusion IDs: `pr_final`
- Scoring-rule IDs: `r1, r2, r3, r4, r5`
- Bound result-field status: **PRESENT**
- Missing bound fields in the archived group result: `none detected`
- Fields in an inapplicable submission-schema branch (expected for this result status): `none detected`
- Submission-schema branch selected for the archived result: `0`
- Verification-report status: `PASS` (SUCCESS_EVIDENCE_CANDIDATE); any result/report disagreement requires manual semantic review.

This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.

Evaluator rule units/tolerances and result correspondence:

- rule `r1` → reference `pr_process_freq`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r2` → reference `pr_process_path`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r3` → reference `pr_result_barrier`; type=numeric; unit=kcal/mol; tolerance=3.0; comparison=absolute difference; evaluator_target_present=True
- rule `r4` → reference `pr_result_mechanism`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False
- rule `r5` → reference `pr_final`; type=semantic; unit=not recorded; tolerance=not recorded; comparison=expert semantic comparison; evaluator_target_present=False

Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):

- rule `r3` / reference `pr_result_barrier`: target=21.8 kcal/mol; tolerance=3.0; numeric result leaves=[19.871970024681406]; within_tolerance=True; applicability=applicable

Actual result scalars selected by evaluator bindings:

These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.

- rule `r1` / reference `pr_process_freq` / field `$.validation.reactant_minimum` / result path `$.validation.reactant_minimum` = `"optimization_completed=True, normal_termination=True, imaginary_frequency_count=0"`
- rule `r2` / reference `pr_process_path` / field `$.validation.connectivity_test` / result path `$.validation.connectivity_test` = `"forward/reverse IRC successes=['forward', 'reverse']; bidirectional_complete=True"`
- rule `r3` / reference `pr_result_barrier` / field `$.barrier_kcal_mol` / result path `$.barrier_kcal_mol` = `19.871970024681406`
- rule `r4` / reference `pr_result_mechanism` / field `$.mechanism_conclusion` / result path `$.mechanism_conclusion` = `"The SI-recovered 2a+CO2 candidate supports a direct hydride-transfer path with no discrete intermediate under the stated model; the barrier is computed from the validated TS Gibbs energy minus the separated 2a and CO2 reactant Gibbs ener..."`

## Historical final-assembly review flag

- Previous assembly decision: **HOLD**
- Previous review reason: SI optimized input leakage review
- Files changed in that review: `agent_input/task.md, package_manifest.json`
- Files deleted in that review: `none recorded`

This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.

## Agent-visible input identity and boundaries

Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.

Declared public data:

- `data/inputs` — Self-contained XYZ geometry for 79-atom protonated bisphosphine 2a in the in-out conformer; charge +1 and singlet are stated in the task.

Public input files and hashes:

- `agent_input/data/inputs/2a_inout.xyz` — SHA-256 `a8bc04b720f4653ef0bc98fc1c8823c245a1fb170fcf7ad7b8813fe4180ec03a`; size=2970 bytes; xyz_atom_count=79; xyz_comment=independently displaced starting geometry; source endpoint retained evaluator-private; explicit_boundary_fields=not recorded

## Input and visibility audit

- Declared data missing: `none`
- JSON/XYZ parse errors: `none`
- XYZ rows with non-element labels: `none`
- Absolute agent references: `none`
- Potential high-risk data markers: `none detected`
- Exact evaluator-target/expected literals in agent-visible files: `none detected`
- SI provenance markers requiring semantic review: `none`

## Evidence files

- `docs/verification/group_2/paper_221aafe4bd916a11/verification_report.md` — verification record; SHA-256 `596db298293cafa149ba51d4a42f81e4dadac025ddf97ada95a3885dffb72dfa`
- `docs/verification/group_2/paper_221aafe4bd916a11/report/results.json` — verification record; SHA-256 `ab038a64ef375bb445a3618034b62cbc00b3290332330568aa33e90a5d7be989`

## Exclusion policy

Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.

The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.

## Evidence scope review (2026-09-19)

The saved direct hydride-transfer IRC and barrier support the local path. Repeated guesses using that same IRC do not demonstrate discrimination of every AR direct/stepwise alternative. Preserve the existing successful path; do not certify complete AR hypothesis coverage without its actual discriminating evidence.
