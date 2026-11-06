# 2026-10-28 V3范围与证据复用（group_07）

逐命题复用：吸收解释由真实80原子DCM TD S1/S2=3.4122/3.8949 eV及态特征支持；发射解释由234正模的S1、cLR垂直发射424.781160 nm与E00=409.2456 nm分别支持；两种模型适用性由50/80映射与吸收/发射不同敏感性支持。PR保留气相50原子HOMO/LUMO最终量原窗。未新计算或新V3验收。

The common final questions are absorption explanation, emission/relaxation explanation, absorption applicability and emission applicability. AR weights are 35/35/15/15. PR preserves its pre-existing extra final source-model HOMO/LUMO eigenvalues at 5/5 with unchanged targets -5.62/-1.71 eV and ±0.25 eV; common PR weights are 30/30/15/15. This explicit baseline exception is not imposed on AR. Frontier-localization nodes and duplicate all-in-one optical/transfer syntheses are retained only as unscored evidence. No optical tolerance is invented.

- 50-atom gas frontier eigenvalues and 80-atom solution optical transitions are different quantities and identities; the PR-only baseline exception remains explicit.
- Exact vibronic peak assignment, full line shapes, AIE, rates and aggregates are not verified or required.
- G09 author calculations were realized with G16 and source-default controls; cLR vertical emission, LR roots and E00 must remain distinct.

以下历史正文原样保留；历史PASS不代表本次V3全面通过。

---

# V2 验证计算参考：PBNA 光学响应与截断转移

论文：`paper_94e7481ded3b6a75`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：源50原子计算模型的E/ZPE/G/S按印刷精度恢复；升级要求的50→80原子模型转移也有实际溶液S0/S1/响应证据。关键中间点不再只是把小模型标签改为完整分子。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

What molecular account of PBNA optical response is supported by its supplied dilute-solution absorption and emission observations? Determine what can be established about the relevant molecular electronic states and the limitations of that account.

冻结题面中的科学目标：

What molecular account of PBNA optical response is supported by its supplied dilute-solution absorption and emission observations? Determine what can be established about the relevant molecular electronic states and the limitations of that account.

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The source uses Gaussian09 B3LYP/6-31G(d) molecular calculations and discusses PBNA HOMO/LUMO density concentrated on the BN-anthracene scaffold (main pp5–6 Fig3). It compares solution spectra and aggregation measurements as different experiments. Main Table1 reports PBNA absorption321/375/392nm, onset404nm and emission409/427nm under321nm excitation in DCM. The source interpretation of limited CT from solvent behavior is conditional, not proof from one descriptor. Reproduce the PBNA molecular baseline or justified substitutions; the old excited-motion intervention grid was an added benchmark design.

Source identity distinction: main physical pp2–3 (section 2.2.3), SI physical p4 FigS3 and p6 TableS2 identify experimental N-hexyl PBNA, C34H42B2N2. The PBNA coordinate block in SI physical pp19–20 TableS12 instead contains the N-methyl computational approximation C24H22B2N2 (50 atoms). The experimental graph is in data/inputs/objects.json; data/inputs/author_model.json and data/inputs/author_model_mapping.json identify this approximation and its retained-core/truncation map. Reproduce the disclosed computational baseline or justify substitutions, then assess the transfer to the experimental molecule; the author approximation is not a second experimental identity and does not itself validate that transfer.

Interpret and reproduce the disclosed author approach within this task’s bounded question. Explain justified substitutions and distinguish replication, new checks and disagreement. Source agreement is not a substitute for valid evidence.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_94e7481ded3b6a75/documents/supplementary_001.pdf](../../../../papers/paper_94e7481ded3b6a75/documents/supplementary_001.pdf) | `d806f9e3af0e9faa3be4ac6098097c936f2418e1f3151fb4c4206620806d90c6` |
| [papers/paper_94e7481ded3b6a75/documents/main.pdf](../../../../papers/paper_94e7481ded3b6a75/documents/main.pdf) | `3f8646e8d8d8a74dffa3f64435459cdf2446757ce7c5c6507bd92d0b79fbe09c` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

B3LYP/6-31G(d) source gas baseline was genuinely calculated; the native optimized 50-atom model has 144 positive modes. A G09-default source-geometry frequency control reproduces SI thermochemistry. Actual 80-atom full-molecule DCM S0/S1/TD and non-equilibrium emission calculations assess the explicitly mapped model truncation; S1 has 234 positive modes.

1. 建立源 N-methyl 50 原子模型与实验 N-hexyl C34H42B2N2 的 80 原子全分子映射，明确保留骨架与尾链差异；不能将截断模型文件改名当作全分子。

2. 实际执行源气相 B3LYP/6-31G(d) Opt/Freq，50 原子独立最低点 144 正模；在源几何上进行 G09-default 频率控制，按源精度恢复 E=−1087.1445139、ZPE=0.410542、G=−1086.786988 Eh、S=161.102 cal mol⁻¹ K⁻¹。

3. 核收真实 80 原子 DCM S0/S1 优化、频率与 TD 及非平衡发射分析；S1 有 234 正模。将 50/80 的垂直吸收、平衡端点差 E00 与 cLR 垂直发射分别计算和报告。

4. 由保存的波函数/态分析检验 BN-anthracene 骨架主导及有限跨片段重排。80 原子 E00=3.0295791 eV/409.2456 nm、cLR 发射 424.7812 nm，分别与实验 409/427 nm 的不同光学量讨论；不得将一个离散根拟配全部精细峰。

5. 以真实全分子控制评估截断可迁移性，保留吸收与松弛发射不同的取代敏感性；不外推体相 AIE、TPA/TPE、非辐射速率或唯一振动指派。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

#### required_calculations（冻结记录 E0016）

```json
[
  {
    "id": "PBNA_MAPPING",
    "purpose": "Make the source approximation and transfer target explicit.",
    "author_or_added": "TECHNICAL_PREREQUISITE",
    "source_locator": "SI pp19–20 versus experimental identity on main pp2–3/SI pp4,6",
    "identity": {
      "experimental": "N-hexyl C34H42B2N2 /80 atoms /135α+135β",
      "author_model": "N-methyl C24H22B2N2 /50 atoms /95α+95β",
      "charge": 0,
      "multiplicity": 1,
      "mapping": "48 retained atoms including28 heavy atoms;32 experimental tail atoms removed and2 model capH inserted"
    },
    "method": {
      "functional": "B3LYP",
      "basis": "6-31G(d)",
      "source_engine": "Gaussian09",
      "actual_engine": "Gaussian16 plus G09Defaults technical control",
      "author_medium": "gas phase",
      "optical_extension": "IEFPCM(DCM), same specified S0/S1 and field definitions for each molecule"
    },
    "expected_output_type": "native quantum output and traceable numerical analysis",
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      }
    ],
    "job_id": null,
    "native_validity": "Explicit retained-core/cap/tail atom and bond mapping; model50 is not relabeled full80 and source approximation alone is not taken as transfer evidence."
  },
  {
    "id": "PBNA_AUTHOR_S0",
    "purpose": "Reproduce the source50-atom optimized ground-state/frontier baseline.",
    "author_or_added": "AUTHOR",
    "source_locator": "main pp5–6Fig3; SI p19TablesS11/S12",
    "identity": {
      "experimental": "N-hexyl C34H42B2N2 /80 atoms /135α+135β",
      "author_model": "N-methyl C24H22B2N2 /50 atoms /95α+95β",
      "charge": 0,
      "multiplicity": 1,
      "mapping": "48 retained atoms including28 heavy atoms;32 experimental tail atoms removed and2 model capH inserted"
    },
    "method": {
      "functional": "B3LYP",
      "basis": "6-31G(d)",
      "source_engine": "Gaussian09",
      "actual_engine": "Gaussian16 plus G09Defaults technical control",
      "author_medium": "gas phase",
      "optical_extension": "IEFPCM(DCM), same specified S0/S1 and field definitions for each molecule"
    },
    "expected_output_type": "native quantum output and traceable numerical analysis",
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log",
        "sha256": "30f12e30885280ccfd735cc779591538187adca36a7f66f1b0bef2438d442805"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/gaussian.log",
        "sha256": "570f01634db7289cfa09cb24c308ebb3d30bc55bcb26cbe5d74d4dbaea94107a"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/author_PBNA_legacy_Hessian_acceptance_20261002.json",
        "sha256": "f5de4d29e7c085720f4babc3d0c857d62ae45f5f41a19bb40f442bc5ddd4a0f7"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out",
        "sha256": "b6a0cd65a35467c3154fa14236d84b8145dfd577e7b3000afed373ad9b1851d7"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      }
    ],
    "job_id": null,
    "native_validity": "144 positive modes; independent overlap-aware orbital populations86.27071%/92.21407% on scaffold. G09-default E/ZPE/G/S = −1087.14451390/0.410542/−1086.786988Eh/161.102cal mol−1K−1. Frontier residual tolerance is a comparison criterion, not missing computation."
  },
  {
    "id": "PBNA_DCM_ABSORPTION",
    "purpose": "Compute solution transitions and characterize transfer from source model to experimental molecule.",
    "author_or_added": "ADDED_FOR_CURRENT_QUESTION",
    "source_locator": "V2 experimental80-atom optical question; mainTable1 DCM",
    "identity": {
      "experimental": "N-hexyl C34H42B2N2 /80 atoms /135α+135β",
      "author_model": "N-methyl C24H22B2N2 /50 atoms /95α+95β",
      "charge": 0,
      "multiplicity": 1,
      "mapping": "48 retained atoms including28 heavy atoms;32 experimental tail atoms removed and2 model capH inserted"
    },
    "method": {
      "functional": "B3LYP",
      "basis": "6-31G(d)",
      "source_engine": "Gaussian09",
      "actual_engine": "Gaussian16 plus G09Defaults technical control",
      "author_medium": "gas phase",
      "optical_extension": "IEFPCM(DCM), same specified S0/S1 and field definitions for each molecule"
    },
    "expected_output_type": "native quantum output and traceable numerical analysis",
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_DCM/gaussian.log",
        "sha256": "28bb0131435953b198e17de6b1a94612072e40b74b118cf5daa378de4dbfb509"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_DCM_TD10_a01/gaussian.log",
        "sha256": "483d812c7c43684681dadd44dfba789c27f74b817fee7c383ddfabbd99b6e4fc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      }
    ],
    "job_id": null,
    "native_validity": "Native50/80 verticalS1=3.4243/3.4122eV with molecular/state mappings. Declared gas-geometry vertical-solvent response is distinguished from separately optimized DCM endpoint calculations; no silent geometry equivalence."
  },
  {
    "id": "PBNA_DCM_S0_S1_HESSIANS",
    "purpose": "Validate the same-medium relaxed-state and mode evidence used in optical interpretation.",
    "author_or_added": "ADDED_FOR_CURRENT_QUESTION",
    "source_locator": "V2 relaxation/mode/transfer claims; source Hamiltonian",
    "identity": {
      "experimental": "N-hexyl C34H42B2N2 /80 atoms /135α+135β",
      "author_model": "N-methyl C24H22B2N2 /50 atoms /95α+95β",
      "charge": 0,
      "multiplicity": 1,
      "mapping": "48 retained atoms including28 heavy atoms;32 experimental tail atoms removed and2 model capH inserted"
    },
    "method": {
      "functional": "B3LYP",
      "basis": "6-31G(d)",
      "source_engine": "Gaussian09",
      "actual_engine": "Gaussian16 plus G09Defaults technical control",
      "author_medium": "gas phase",
      "optical_extension": "IEFPCM(DCM), same specified S0/S1 and field definitions for each molecule",
      "states": "S0 and S1 root1 in DCM"
    },
    "expected_output_type": "native quantum output and traceable numerical analysis",
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA50_S0_DCM_optfreq_a01/outputs/gaussian.log",
        "sha256": "e84d96fe8b884e50d4825b5a9386181327410cb04ce7a6ce1cb84be148b64341"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_DCM_optfreq_a01/gaussian.log",
        "sha256": "00a160c8d8fbf198bced3489a95e89697e10a87624e6f3a5575a360eb6b28f8d"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_Newton_refine_a01/outputs/refinement/gaussian.log",
        "sha256": "e5fca8613991a13aa9cb25b52e958f07fed701ffd192f13e0b1b734f94bb972e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/gaussian.log",
        "sha256": "3ec33b141d5115136fc5f8bbce550d3e8ecc99e1cd9c7ceb7726a4fa8e874b55"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json",
        "sha256": "6ff37e99ba5b72df1259a60c98e7314b9b5dc75e7a950bc0799c10c201846bc8"
      }
    ],
    "job_id": null,
    "native_validity": "Same-medium50 endpoints144 positive modes and80 endpoints234 positive modes. Refined S0 minimum12.7533cm−1; S1 minimum9.9255cm−1. Actual Opt and Freq displacement predictions separated; native negligible-forceS0 stop supported by gradient and curvature."
  },
  {
    "id": "PBNA_DCM_EMISSION",
    "purpose": "Compute relaxation-sensitive same-field vertical emission for each mapped molecule.",
    "author_or_added": "ADDED_FOR_CURRENT_QUESTION",
    "source_locator": "V2 solution-emission account; mainTable1",
    "identity": {
      "experimental": "N-hexyl C34H42B2N2 /80 atoms /135α+135β",
      "author_model": "N-methyl C24H22B2N2 /50 atoms /95α+95β",
      "charge": 0,
      "multiplicity": 1,
      "mapping": "48 retained atoms including28 heavy atoms;32 experimental tail atoms removed and2 model capH inserted"
    },
    "method": {
      "functional": "B3LYP",
      "basis": "6-31G(d)",
      "source_engine": "Gaussian09",
      "actual_engine": "Gaussian16 plus G09Defaults technical control",
      "author_medium": "gas phase",
      "optical_extension": "IEFPCM(DCM), same specified S0/S1 and field definitions for each molecule",
      "emission_definition": "cLR S1 equilibrium field and same geometry/slow field S0 NonEquilibriumRead"
    },
    "expected_output_type": "native quantum output and traceable numerical analysis",
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_cLR_Save_a01/gaussian.log",
        "sha256": "cccb9ad74037b094ed479398442cbb6cb94076f4f2f3af8d91d371c98e1f61bd"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S0_NonEq_Read_a01/gaussian.log",
        "sha256": "cf09ecb62bf2bc984c9a4ef1db58944304847aeff33df7a1a455c0d2176900e4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/gaussian.log",
        "sha256": "3a65e82f99359acf6ff62f396f3bb26e00fac0f84093d9088604d0fa7f48c9b1"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/gaussian.log",
        "sha256": "356f2df6d8ff3816fb7a911d339ad93e5d49edc2296c202af9b6de75b4ef913e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      }
    ],
    "job_id": null,
    "native_validity": "All accepted field/state/geometry dependencies complete.50 emission2.969830286eV/417.479069nm;80 emission2.918778188eV/424.781160nm. Field consistency, charge/spin, parent hashes and state audits retained."
  },
  {
    "id": "PBNA_MODE_TRANSFER_ANALYSIS",
    "purpose": "Quantify vibrational/endpoint transfer and soft-mode limits without substituting E00 for a band maximum.",
    "author_or_added": "ADDED_FOR_CURRENT_QUESTION",
    "source_locator": "V2 relaxation evidence and approximation limitations",
    "identity": {
      "experimental": "N-hexyl C34H42B2N2 /80 atoms /135α+135β",
      "author_model": "N-methyl C24H22B2N2 /50 atoms /95α+95β",
      "charge": 0,
      "multiplicity": 1,
      "mapping": "48 retained atoms including28 heavy atoms;32 experimental tail atoms removed and2 model capH inserted"
    },
    "method": {
      "functional": "B3LYP",
      "basis": "6-31G(d)",
      "source_engine": "Gaussian09",
      "actual_engine": "Gaussian16 plus G09Defaults technical control",
      "author_medium": "gas phase",
      "optical_extension": "IEFPCM(DCM), same specified S0/S1 and field definitions for each molecule"
    },
    "expected_output_type": "native quantum output and traceable numerical analysis",
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA_matched_hessians_a01/outputs/analysis_result.json",
        "sha256": "81f65d516f6d1ba18eec5024ec123cdb5f92799e1cb462002599707370a47110"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json",
        "sha256": "6ff37e99ba5b72df1259a60c98e7314b9b5dc75e7a950bc0799c10c201846bc8"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/PBNA80_RETURN_ACCEPTANCE_20261007.json",
        "sha256": "b33b0c4fb3365271b02ebcc5b40b55356e65161782387163d545888243e5327c"
      }
    ],
    "job_id": null,
    "native_validity": "Finala02 native0/27.2617s, actual234+234 modes and Hessian reconstruction checks accepted. Full80 E00=3.029579143eV; low-frequency15modes dominate~54% vibrational entropy. No RRHO population/rate inference, no fullFC-band reproduction asserted."
  }
]
```


#### reused_results（冻结记录 E0016）

```json
[
  {
    "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/provenance/pbna_raw_reaudit_20260916.json",
    "sha256": "d3e1f3789cb1126a37a12fad5b710fff3fe9e1b4329480930e65ed47c582de92"
  },
  {
    "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out",
    "sha256": "b6a0cd65a35467c3154fa14236d84b8145dfd577e7b3000afed373ad9b1851d7"
  },
  {
    "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log",
    "sha256": "30f12e30885280ccfd735cc779591538187adca36a7f66f1b0bef2438d442805"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/author_PBNA_legacy_Hessian_acceptance_20261002.json",
    "sha256": "f5de4d29e7c085720f4babc3d0c857d62ae45f5f41a19bb40f442bc5ddd4a0f7"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
    "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
    "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
  },
  {
    "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json",
    "sha256": "6ff37e99ba5b72df1259a60c98e7314b9b5dc75e7a950bc0799c10c201846bc8"
  },
  {
    "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/PBNA80_RETURN_ACCEPTANCE_20261007.json",
    "sha256": "b33b0c4fb3365271b02ebcc5b40b55356e65161782387163d545888243e5327c"
  },
  {
    "path": "tasks/final_verified_paper_reproduction/paper_94e7481ded3b6a75/evaluation/scoring_rules.json",
    "sha256": "7409d39e2262b2b8e8d5da659dbc61b238692bc18c6679fca8cac480039afad9"
  }
]
```

### 最近一次原生有效性复核

本轮直接读G09Defaults源几何Freq的E=-1087.14451390 Eh、G=-1086.786988 Eh、144正频；独立50原子优化144正频；完整80原子S1 OptFreq 234正频及TD/非平衡读入日志均在场，TD第一根3.4122eV。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| Author-model gas HOMO/LUMO (eV) | [-5.62,-1.71] | [-5.5598200702,-1.6407202128] | Residuals +0.06018/+0.06928 eV lie within pre-existing same-observable ±0.25 eV. That allowance is not applied to optical spectra or small substituent effects. |
| Author-model E/ZPE/G/S (Eh,Eh,Eh,cal mol−1 K−1) | [-1087.1445139,0.410542,-1086.786988,161.102] | [-1087.1445139,0.410542,-1086.786988,161.102] | The native G09-default frequency control directly reproduces SI Table S11 values at printed precision; source geometry and valid independently optimized baseline are distinguished. |
| Dilute-solution absorption/emission context (nm) | {"absorption_nm":[321,375,392],"onset_nm":404,"emission_nm":[409,427]} | {"full80_vertical_absorption_nm":[363.36,318.32],"full80_cLR_vertical_emission_nm":424.7811599,"full80_E00_nm":409.2456165} | These are different observables. No new band tolerance or unique vibronic assignment is asserted. Failure to put every measured peak on a discrete root is not failure to reproduce the authors molecular theory baseline. |
| Actual truncation transfer (eV) | 50-atom N-methyl approximation for 80-atom experimental N-hexyl molecule | {"S1_eV_50_80":[3.4243,3.4122],"cLR_emission_eV_50_80":[2.9698303,2.9187782]} | Actual matched computations show small absorption shift and a distinct emission response; retained-core/state-population evidence supports bounded transfer instead of assuming it. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Verify experimental PBNA as N-hexyl C34H42B2N2, neutral singlet, and distinguish it from TPA/TPE derivatives and any computational approximation. Accept the full graph or an explicitly disclosed chemically valid approximation with retained-core/substituent and atom mapping, charge/spin and a justified domain of use. A different model formula alone is not an identity failure; falsely calling a truncated graph the full experimental molecule is.

冻结要求：Verify experimental PBNA as N-hexyl C34H42B2N2, neutral singlet, and distinguish it from TPA/TPE derivatives and any computational approximation. Accept the full graph or an explicitly disclosed chemically valid approximation with retained-core/substituent and atom mapping, charge/spin and a justified domain of use. A different model formula alone is not an identity failure; falsely calling a truncated graph the full experimental molecule is. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question.

当前复审：实验80与作者50原子明确映射

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "main pp2–3/§2.2.3; SI pp4,6 and pp19–20 TableS12",
    "actual_result": "80原子C34H42B2N2，0/1，135α/135β；50原子C24H22B2N2，0/1，95α/95β。保留48原子/28重原子、32尾链原子被替换为2个封端H，保留键序相同。",
    "reason": "完整实验物种与作者近似分别标记，实际原子映射和80原子对照证明限定转移。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_DCM_TD10_a01/gaussian.log",
        "sha256": "483d812c7c43684681dadd44dfba789c27f74b817fee7c383ddfabbd99b6e4fc"
      }
    ]
  }
]
```


证据记录：`E0035`。

```json
[
  {
    "source_locator": "main pp2–3/§2.2.3; SI pp4,6 and pp19–20 TableS12",
    "actual_result": "80原子C34H42B2N2，0/1，135α/135β；50原子C24H22B2N2，0/1，95α/95β。保留48原子/28重原子、32尾链原子被替换为2个封端H，保留键序相同。",
    "reason": "完整实验物种与作者近似分别标记，实际原子映射和80原子对照证明限定转移。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_DCM_TD10_a01/gaussian.log",
        "sha256": "483d812c7c43684681dadd44dfba789c27f74b817fee7c383ddfabbd99b6e4fc"
      }
    ]
  }
]
```

### kp_quantitative_evidence — Check quantitative molecular optical evidence against appropriately defined PBNA absorption/emission observations, accounting for vertical versus relaxed states and spectral structure. Do not count matching the disclosed values as independent computation.

冻结要求：Check quantitative molecular optical evidence against appropriately defined PBNA absorption/emission observations, accounting for vertical versus relaxed states and spectral structure. Do not count matching the disclosed values as independent computation. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question.

当前复审：真实吸收/松弛发射/0-0分开

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "main pp5–7 Fig3/Table1; SI p19 TableS11",
    "actual_result": "源HOMO/LUMO−5.62/−1.71 eV；旧有效同对象气相结果−5.55982007/−1.64072021 eV，差0.06018/0.06928 eV，小于原已验收±0.25 eV。G09默认控制同时再现源E/ZPE/G/S。DCM垂直吸收S1/S2：50为3.4243/3.8534，80为3.4122/3.8949 eV；实验321/375/392、onset404和em409/427 nm分别比较。",
    "reason": "继承同分子、同方法、同气相KS能级定义的原容差，不继承到TD、cLR或实验谱峰；不因末位差否定已成立骨架结论。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/provenance/pbna_raw_reaudit_20260916.json",
        "sha256": "d3e1f3789cb1126a37a12fad5b710fff3fe9e1b4329480930e65ed47c582de92"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out",
        "sha256": "b6a0cd65a35467c3154fa14236d84b8145dfd577e7b3000afed373ad9b1851d7"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log",
        "sha256": "30f12e30885280ccfd735cc779591538187adca36a7f66f1b0bef2438d442805"
      },
      {
        "path": "tasks/final_verified_paper_reproduction/paper_94e7481ded3b6a75/evaluation/scoring_rules.json",
        "sha256": "7409d39e2262b2b8e8d5da659dbc61b238692bc18c6679fca8cac480039afad9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/gaussian.log",
        "sha256": "570f01634db7289cfa09cb24c308ebb3d30bc55bcb26cbe5d74d4dbaea94107a"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_DCM/gaussian.log",
        "sha256": "28bb0131435953b198e17de6b1a94612072e40b74b118cf5daa378de4dbfb509"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_DCM_TD10_a01/gaussian.log",
        "sha256": "483d812c7c43684681dadd44dfba789c27f74b817fee7c383ddfabbd99b6e4fc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      }
    ]
  }
]
```


证据记录：`E0035`。

```json
[
  {
    "source_locator": "main pp5–7 Fig3/Table1; SI p19 TableS11",
    "actual_result": "源HOMO/LUMO−5.62/−1.71 eV；旧有效同对象气相结果−5.55982007/−1.64072021 eV，差0.06018/0.06928 eV，小于原已验收±0.25 eV。G09默认控制同时再现源E/ZPE/G/S。DCM垂直吸收S1/S2：50为3.4243/3.8534，80为3.4122/3.8949 eV；实验321/375/392、onset404和em409/427 nm分别比较。",
    "reason": "继承同分子、同方法、同气相KS能级定义的原容差，不继承到TD、cLR或实验谱峰；不因末位差否定已成立骨架结论。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/provenance/pbna_raw_reaudit_20260916.json",
        "sha256": "d3e1f3789cb1126a37a12fad5b710fff3fe9e1b4329480930e65ed47c582de92"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out",
        "sha256": "b6a0cd65a35467c3154fa14236d84b8145dfd577e7b3000afed373ad9b1851d7"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log",
        "sha256": "30f12e30885280ccfd735cc779591538187adca36a7f66f1b0bef2438d442805"
      },
      {
        "path": "tasks/final_verified_paper_reproduction/paper_94e7481ded3b6a75/evaluation/scoring_rules.json",
        "sha256": "7409d39e2262b2b8e8d5da659dbc61b238692bc18c6679fca8cac480039afad9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/gaussian.log",
        "sha256": "570f01634db7289cfa09cb24c308ebb3d30bc55bcb26cbe5d74d4dbaea94107a"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_DCM/gaussian.log",
        "sha256": "28bb0131435953b198e17de6b1a94612072e40b74b118cf5daa378de4dbfb509"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_DCM_TD10_a01/gaussian.log",
        "sha256": "483d812c7c43684681dadd44dfba789c27f74b817fee7c383ddfabbd99b6e4fc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      }
    ]
  }
]
```

### kp_scientific_answer — Judge the proposed molecular-state explanation and its demonstrated limits. Different valid state analyses or models and unresolved assignments may earn credit; a fixed S1 torsion grid, charge-transfer descriptor or motion-restriction cause is not required.

冻结要求：Judge the proposed molecular-state explanation and its demonstrated limits. Different valid state analyses or models and unresolved assignments may earn credit; a fixed S1 torsion grid, charge-transfer descriptor or motion-restriction cause is not required. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question.

当前复审：主骨架态身份

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "main pp5–6 §3.2–3.3; SI TableS12",
    "actual_result": "旧重叠感知Mulliken轨道布居：骨架HOMO86.27071%、LUMO92.21407%；后续Löwdin86.0656%/92.1955%同样骨架主导。映射S1特征余弦0.993318，50/80吸收差−0.0121 eV；松弛cLR发射差−0.0510521 eV。",
    "reason": "不同布居定义和实算80分子支持骨架主导，同时量化了近似对不同光学量的非均匀影响，不以作者采用近似本身当验证。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/provenance/pbna_raw_reaudit_20260916.json",
        "sha256": "d3e1f3789cb1126a37a12fad5b710fff3fe9e1b4329480930e65ed47c582de92"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out",
        "sha256": "b6a0cd65a35467c3154fa14236d84b8145dfd577e7b3000afed373ad9b1851d7"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log",
        "sha256": "30f12e30885280ccfd735cc779591538187adca36a7f66f1b0bef2438d442805"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      }
    ]
  }
]
```


证据记录：`E0035`。

```json
[
  {
    "source_locator": "main pp5–6 §3.2–3.3; SI TableS12",
    "actual_result": "旧重叠感知Mulliken轨道布居：骨架HOMO86.27071%、LUMO92.21407%；后续Löwdin86.0656%/92.1955%同样骨架主导。映射S1特征余弦0.993318，50/80吸收差−0.0121 eV；松弛cLR发射差−0.0510521 eV。",
    "reason": "不同布居定义和实算80分子支持骨架主导，同时量化了近似对不同光学量的非均匀影响，不以作者采用近似本身当验证。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/provenance/pbna_raw_reaudit_20260916.json",
        "sha256": "d3e1f3789cb1126a37a12fad5b710fff3fe9e1b4329480930e65ed47c582de92"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out",
        "sha256": "b6a0cd65a35467c3154fa14236d84b8145dfd577e7b3000afed373ad9b1851d7"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log",
        "sha256": "30f12e30885280ccfd735cc779591538187adca36a7f66f1b0bef2438d442805"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      }
    ]
  }
]
```

### kp_validity_and_uncertainty — Define the relationship between computed transitions, absorption bands/onset and emission. Provide physical evidence for state character and any geometry-dependent or relaxation claim; quantify relevant limitations rather than assume that one calculated root explains every optical feature. Chosen validations must address the account actually asserted. Evaluate approximation-to-experiment transfer for the optical claims, including the role and limitations of changed N substituents. Source use of an approximation is not independent validation of its adequacy; no fixed additional full-molecule matrix is required.

冻结要求：Define the relationship between computed transitions, absorption bands/onset and emission. Provide physical evidence for state character and any geometry-dependent or relaxation claim; quantify relevant limitations rather than assume that one calculated root explains every optical feature. Chosen validations must address the account actually asserted. Evaluate approximation-to-experiment transfer for the optical claims, including the role and limitations of changed N substituents. Source use of an approximation is not independent validation of its adequacy; no fixed additional full-molecule matrix is required. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question.

当前复审：实际全分子转移控制而非假定；kp_bounded_conclusion及最终结论限稀溶液分子解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "main pp6–7 optical definitions; SI p19 method",
    "actual_result": "50自由端点144正模；80同DCM S0/S1各234正模。Hessian重建最大误差0.0000598/0.0006644 cm−1，原始/修复最大频率变化0.00384081 cm−1；实际Opt与Freq预测分开。15个<100 cm−1软模承担约54%振动熵，熵未用于人口/速率。E00、LR根和cLR垂直发射三种量不互换。",
    "reason": "实际曲率、态/溶剂场链和模型敏感性均有数据；不要求完整FC/ensemble来支持未作出的精确谱形/人口主张。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/PBNA80_RETURN_ACCEPTANCE_20261007.json",
        "sha256": "b33b0c4fb3365271b02ebcc5b40b55356e65161782387163d545888243e5327c"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json",
        "sha256": "6ff37e99ba5b72df1259a60c98e7314b9b5dc75e7a950bc0799c10c201846bc8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/gaussian.log",
        "sha256": "3ec33b141d5115136fc5f8bbce550d3e8ecc99e1cd9c7ceb7726a4fa8e874b55"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/gaussian.log",
        "sha256": "356f2df6d8ff3816fb7a911d339ad93e5d49edc2296c202af9b6de75b4ef913e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      }
    ]
  }
]
```


证据记录：`E0035`。

```json
[
  {
    "source_locator": "main pp6–7 optical definitions; SI p19 method",
    "actual_result": "50自由端点144正模；80同DCM S0/S1各234正模。Hessian重建最大误差0.0000598/0.0006644 cm−1，原始/修复最大频率变化0.00384081 cm−1；实际Opt与Freq预测分开。15个<100 cm−1软模承担约54%振动熵，熵未用于人口/速率。E00、LR根和cLR垂直发射三种量不互换。",
    "reason": "实际曲率、态/溶剂场链和模型敏感性均有数据；不要求完整FC/ensemble来支持未作出的精确谱形/人口主张。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/PBNA80_RETURN_ACCEPTANCE_20261007.json",
        "sha256": "b33b0c4fb3365271b02ebcc5b40b55356e65161782387163d545888243e5327c"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json",
        "sha256": "6ff37e99ba5b72df1259a60c98e7314b9b5dc75e7a950bc0799c10c201846bc8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/gaussian.log",
        "sha256": "3ec33b141d5115136fc5f8bbce550d3e8ecc99e1cd9c7ceb7726a4fa8e874b55"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/gaussian.log",
        "sha256": "356f2df6d8ff3816fb7a911d339ad93e5d49edc2296c202af9b6de75b4ef913e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      }
    ]
  }
]
```

### kp_bounded_conclusion — A finite PBNA molecular model does not establish AIE, aggregate/crystal packing, two-photon cross section or the behavior of TPA/TPE substituted relatives. Do not infer a radiative or nonradiative rate from a gap or a single oscillator strength alone. Do not equate a truncated-model result with an established experimental PBNA optical explanation without evidence for the transfer; preserve valid model-scoped partial credit.

冻结要求：A finite PBNA molecular model does not establish AIE, aggregate/crystal packing, two-photon cross section or the behavior of TPA/TPE substituted relatives. Do not infer a radiative or nonradiative rate from a gap or a single oscillator strength alone. Do not equate a truncated-model result with an established experimental PBNA optical explanation without evidence for the transfer; preserve valid model-scoped partial credit. Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question.

当前复审：kp_identity：实验80与作者50原子明确映射；kp_quantitative_evidence：真实吸收/松弛发射/0-0分开；kp_scientific_answer：主骨架态身份；kp_validity_and_uncertainty：实际全分子转移控制而非假定；kp_bounded_conclusion及最终结论限稀溶液分子解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "main pp5–7 versus later AIE/two-photon sections",
    "actual_result": "结论限孤立PBNA模型与10^-5 M DCM光学事实；单构象/谐振/连续介质和近似转移边界保留，不外推TPA/TPE、bulk AIE或knr。",
    "reason": "边界由实际计算内容限定，不通过删去已要求的吸收/发射比较缩小问题。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json",
        "sha256": "6ff37e99ba5b72df1259a60c98e7314b9b5dc75e7a950bc0799c10c201846bc8"
      }
    ]
  }
]
```


证据记录：`E0035`。

```json
[
  {
    "source_locator": "main pp5–7 versus later AIE/two-photon sections",
    "actual_result": "结论限孤立PBNA模型与10^-5 M DCM光学事实；单构象/谐振/连续介质和近似转移边界保留，不外推TPA/TPE、bulk AIE或knr。",
    "reason": "边界由实际计算内容限定，不通过删去已要求的吸收/发射比较缩小问题。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json",
        "sha256": "6ff37e99ba5b72df1259a60c98e7314b9b5dc75e7a950bc0799c10c201846bc8"
      }
    ]
  }
]
```

### bounded_answer — A source-bounded evidence-supported answer to: What molecular account of PBNA optical response is supported by its supplied dilute-solution absorption and emission observations? Determine what can be established about the relevant molecular electronic states and the limitations of that account.

冻结要求：Accept scientifically defensible alternative methods and evidence-supported support, refutation or unresolved answers. Judge sufficiency for the actual question and claims; do not require any retired V1 matrix, author winner, fixed hypothesis count or particular software. Full points require linked genuine artifacts that sustain the claim; partial points scale with valid question coverage; absent/invalid evidence receives zero dependent credit. Missing research cannot establish non-identifiability. A self-selected narrower addressed_scope, copied disclosed facts or an input-gap description alone cannot earn whole-question full credit; credit only evidenced components against the actual public question. A finite PBNA molecular model does not establish AIE, aggregate/crystal packing, two-photon cross section or the behavior of TPA/TPE substituted relatives. Do not infer a radiative or nonradiative rate from a gap or a single oscillator strength alone. Do not equate a truncated-model result with an established experimental PBNA optical explanation without evidence for the transfer; preserve valid model-scoped partial credit.

当前复审：kp_identity：实验80与作者50原子明确映射；kp_quantitative_evidence：真实吸收/松弛发射/0-0分开；kp_scientific_answer：主骨架态身份；kp_validity_and_uncertainty：实际全分子转移控制而非假定；kp_bounded_conclusion及最终结论限稀溶液分子解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "main pp5–7; SI p19–20",
    "actual_result": "PBNA 的稀溶液光学响应可用 BN-anthracene 骨架主导的分子激发与松弛来解释，但一个电子根不能对应所有精细谱峰。实验为 N-hexyl C34H42B2N2；作者 N-methyl 50 原子模型明确映射到它，保留48原子/28重原子，尾链差异通过实际80原子对照评估。50/80 的 DCM 垂直 S1 分别3.4243/3.4122 eV，cLR 发射分别2.9698303/2.9187782 eV；取代近似对吸收与松弛发射的影响不同，不能按一个统一偏移转移。HOMO/LUMO 骨架布居与态分析共同支持局域为主而有有限跨片段重排；不是只凭近零 CT 质心距判断。80原子模型 E00=3.0295791 eV/409.2456 nm 是含ZPE的平衡端点差，cLR垂直发射为424.7812 nm，二者均与实验409/427 nm逐项区分。支持当前有界分子解释；不推出AIE、量子产率、速率或完整振动线形。",
    "reason": "当前整个有界问题已有源基态、真实溶液吸收/发射、状态和80/50转移证据。残余逐峰指派不被冒称已证明，也不是漏算声明。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/provenance/pbna_raw_reaudit_20260916.json",
        "sha256": "d3e1f3789cb1126a37a12fad5b710fff3fe9e1b4329480930e65ed47c582de92"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out",
        "sha256": "b6a0cd65a35467c3154fa14236d84b8145dfd577e7b3000afed373ad9b1851d7"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log",
        "sha256": "30f12e30885280ccfd735cc779591538187adca36a7f66f1b0bef2438d442805"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json",
        "sha256": "6ff37e99ba5b72df1259a60c98e7314b9b5dc75e7a950bc0799c10c201846bc8"
      }
    ]
  }
]
```


证据记录：`E0035`。

```json
[
  {
    "source_locator": "main pp5–7; SI p19–20",
    "actual_result": "PBNA 的稀溶液光学响应可用 BN-anthracene 骨架主导的分子激发与松弛来解释，但一个电子根不能对应所有精细谱峰。实验为 N-hexyl C34H42B2N2；作者 N-methyl 50 原子模型明确映射到它，保留48原子/28重原子，尾链差异通过实际80原子对照评估。50/80 的 DCM 垂直 S1 分别3.4243/3.4122 eV，cLR 发射分别2.9698303/2.9187782 eV；取代近似对吸收与松弛发射的影响不同，不能按一个统一偏移转移。HOMO/LUMO 骨架布居与态分析共同支持局域为主而有有限跨片段重排；不是只凭近零 CT 质心距判断。80原子模型 E00=3.0295791 eV/409.2456 nm 是含ZPE的平衡端点差，cLR垂直发射为424.7812 nm，二者均与实验409/427 nm逐项区分。支持当前有界分子解释；不推出AIE、量子产率、速率或完整振动线形。",
    "reason": "当前整个有界问题已有源基态、真实溶液吸收/发射、状态和80/50转移证据。残余逐峰指派不被冒称已证明，也不是漏算声明。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/provenance/pbna_raw_reaudit_20260916.json",
        "sha256": "d3e1f3789cb1126a37a12fad5b710fff3fe9e1b4329480930e65ed47c582de92"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out",
        "sha256": "b6a0cd65a35467c3154fa14236d84b8145dfd577e7b3000afed373ad9b1851d7"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log",
        "sha256": "30f12e30885280ccfd735cc779591538187adca36a7f66f1b0bef2438d442805"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json",
        "sha256": "660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json",
        "sha256": "bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json",
        "sha256": "6ff37e99ba5b72df1259a60c98e7314b9b5dc75e7a950bc0799c10c201846bc8"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 11.88 小时；15 份计时日志/22 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 4,8,20 线程/进程；Gaussian %Mem=12GB,20GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0004 · outputs/PBNA_free_TD10_DCM/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_DCM/gaussian.log) | Gaussian:143.6 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0005 · outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/gaussian.log) | Gaussian:185 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0006 · outputs/v2_strict_PBNA_full80_DCM_TD10_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_DCM_TD10_a01/gaussian.log) | Gaussian:266.7 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0007 · outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/gaussian.log) | Gaussian:57.3 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0008 · outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/gaussian.log) | Gaussian:17718；Gaussian:2622.8 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0009 · execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log](../../../../docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log) | Gaussian:721；Gaussian:630.1 | 正常；正常 | {"threads":[8],"Gaussian_mem":["20GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0023 · artifacts/orbital_reaudit_20260916/frontier_mulliken.out](../../../../docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0054 · outputs/PBNA_free_TD10_pilot/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_pilot/gaussian.log) | Gaussian:293.4 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0060 · w01_PBNA50_S0_DCM_optfreq_a01/outputs/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA50_S0_DCM_optfreq_a01/outputs/gaussian.log) | Gaussian:427.2；Gaussian:329.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0061 · outputs/v2_PBNA_S1_DCM_optfreq_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_DCM_optfreq_a01/gaussian.log) | Gaussian:2216.7；Gaussian:939.5 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0062 · outputs/refinement/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_Newton_refine_a01/outputs/refinement/gaussian.log) | Gaussian:1354.1；Gaussian:4469.3 | 正常；正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0063 · outputs/v2_PBNA_S1_cLR_Save_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_cLR_Save_a01/gaussian.log) | Gaussian:411.1 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0064 · outputs/v2_PBNA_S0_NonEq_Read_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S0_NonEq_Read_a01/gaussian.log) | Gaussian:27.6 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0065 · outputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/gaussian.log) | Gaussian:898.6 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0071 · w01_PBNA80_S0_DCM_optfreq_a01/outputs/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_S0_DCM_optfreq_a01/outputs/gaussian.log) | Gaussian:1687.3；Gaussian:904.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0120 · outputs/evidence/S0_free_geometry_native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/S0_free_geometry_native.log) | Gaussian:721；Gaussian:630.1 | 正常；正常；此日志为同内容副本，已从累计排除 | {"threads":[8],"Gaussian_mem":["20GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0121 · outputs/PBNA_S1_free_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_S1_free_optfreq/gaussian.log) | Gaussian:5321.2；Gaussian:1135.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

363.36nm垂直吸收不是逐峰重现321/375/392nm振动结构；424.781nm cLR发射和409.246nm E00是不同量。未做精确振动态线形、AIE、荧光速率或所有取代物；本任务不要求这些。

```json
[
  "The G09-default fixed-source frequency control is not a separately optimized minimum; the separate optimized model has a positive Hessian.",
  "No exact vibronic lineshape, unique assignment of all peaks, conformer populations, AIE, fluorescence yield or rate is established."
]
```


原独立审查的 `source_exceptions_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "The ±.25 eV historical tolerance applies only to the same gas-phase Kohn–Sham frontier energies, not optical peaks or small substitution effects.",
  "Discrete TD states, cLR vertical emission, E00 and measured band maxima are different observables; full fine structure and unique peak assignments are not certified.",
  "Local harmonic minima and one-conformer continuum models do not establish conformer populations, rates, quantum yields or aggregation behavior.",
  "No AIE, two-photon response or full Franck–Condon lineshape is certified."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_94e7481ded3b6a75.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_94e7481ded3b6a75/verified_computation_reference.md)；SHA-256 `1b6019b385cbc04e573570ad01935225851d716e065182af0640edb68e237b94`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_94e7481ded3b6a75.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_94e7481ded3b6a75.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_94e7481ded3b6a75.json) | `8393890e858e2f53a2d38d43787d5e8345c1d9f5a9889baf6cea70c138692a5d` | evidence_or_analysis |
| E0002 | [papers/paper_94e7481ded3b6a75/documents/supplementary_001.pdf](../../../../papers/paper_94e7481ded3b6a75/documents/supplementary_001.pdf) | `d806f9e3af0e9faa3be4ac6098097c936f2418e1f3151fb4c4206620806d90c6` | source_document |
| E0003 | [papers/paper_94e7481ded3b6a75/documents/main.pdf](../../../../papers/paper_94e7481ded3b6a75/documents/main.pdf) | `3f8646e8d8d8a74dffa3f64435459cdf2446757ce7c5c6507bd92d0b79fbe09c` | source_document |
| E0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_DCM/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_DCM/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_native_excerpt.json) | `28bb0131435953b198e17de6b1a94612072e40b74b118cf5daa378de4dbfb509` | native_output |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_native_excerpt.json) | `570f01634db7289cfa09cb24c308ebb3d30bc55bcb26cbe5d74d4dbaea94107a` | native_output |
| E0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_DCM_TD10_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_DCM_TD10_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `483d812c7c43684681dadd44dfba789c27f74b817fee7c383ddfabbd99b6e4fc` | native_output |
| E0007 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `356f2df6d8ff3816fb7a911d339ad93e5d49edc2296c202af9b6de75b4ef913e` | native_output |
| E0008 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `3ec33b141d5115136fc5f8bbce550d3e8ecc99e1cd9c7ceb7726a4fa8e874b55` | native_output |
| E0009 | [docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log](../../../../docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_native_excerpt.json) | `30f12e30885280ccfd735cc779591538187adca36a7f66f1b0bef2438d442805` | native_output |
| E0010 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/PBNA_final_mapping_optical_transfer_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_PBNA_final_mapping_optical_transfer_20260930.json) | `660fa1c52c541410013af84140c04aed99765f0f11971803245af28fef077003` | evidence_or_analysis |
| E0011 | [tasks/final_verified_paper_reproduction/paper_94e7481ded3b6a75/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_94e7481ded3b6a75/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_scoring_rules.json) | `7409d39e2262b2b8e8d5da659dbc61b238692bc18c6679fca8cac480039afad9` | historical_task_binding |
| E0012 | [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_task.md) | `b4df32d8e00a36935bdf57873ac6e6b56182a936e7515830b08a8d3d14409769` | historical_task_binding |
| E0013 | [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/evaluation/reference_key_points.json](reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_reference_key_points.json) | `fab8073bb7bdc3c73cd54eee287a2f929bcfb72129a93ed3568c37b93fc7f39e` | historical_task_binding |
| E0014 | [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/evaluation/reference_conclusions.json](reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_reference_conclusions.json) | `b410b03e3c57df83a5733d70b8c6779e684d24eadb45571ebe7a8aa4b1f30291` | historical_task_binding |
| E0015 | [tasks/v2_autonomous_research/paper_94e7481ded3b6a75/agent_input/task.md](../../../v2_autonomous_research/paper_94e7481ded3b6a75/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_task.md) | `68546b71b77109db8fa63af95cea8cba71e9ef9cfd0e3f5d30f47a3f75b27a77` | historical_task_binding |
| E0016 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_94e7481ded3b6a75/COMPUTATION_STAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_94e7481ded3b6a75/COMPUTATION_STAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_COMPUTATION_STAGE.json) | `95c7a6a11499686ba6e77ea3450e3fd17e3ec3bba33ae5595c11c7052127b27f` | evidence_or_analysis |
| E0017 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_94e7481ded3b6a75/NATIVE_INTAKE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_94e7481ded3b6a75/NATIVE_INTAKE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_NATIVE_INTAKE.json) | `dfd585b6cfa704ba038904848f40994c6a64f83fbdb68a1530eaea3fb7b57d80` | evidence_or_analysis |
| E0018 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_94e7481ded3b6a75.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_94e7481ded3b6a75.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_paper_94e7481ded3b6a75.md) | `c4dfb4a69b5d8857254a5eac7d85719236d2d0f7058dc8a2792fda3511ecfff0` | evidence_or_analysis |
| E0019 | [docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `a3a855bc76582ae8571f341f33aea14ef976c4186f88c899c11d599b51be9bc4` | historical_task_binding |
| E0020 | [docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/v1_development_snapshot/evaluation/verified_computation_reference.md.snapshot) | `6367b345c215c11c389f018df5836fb02345e300ea9d0a87223c6485275e3fcf` | historical_task_binding |
| E0021 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_v2_strict_PBNA_full80_transfer_accept_20261002_a01_acceptance.json) | `bb07605596028b16706a7cb4f11725ebac5916e0df4d09079fc925a4a5ff5039` | evidence_or_analysis |
| E0022 | [docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/provenance/pbna_raw_reaudit_20260916.json](../../../../docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/provenance/pbna_raw_reaudit_20260916.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_pbna_raw_reaudit_20260916.json) | `d3e1f3789cb1126a37a12fad5b710fff3fe9e1b4329480930e65ed47c582de92` | evidence_or_analysis |
| E0023 | [docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out](../../../../docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_native_excerpt.json) | `b6a0cd65a35467c3154fa14236d84b8145dfd577e7b3000afed373ad9b1851d7` | native_output |
| E0024 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/PBNA80_RETURN_ACCEPTANCE_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/PBNA80_RETURN_ACCEPTANCE_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0024_PBNA80_RETURN_ACCEPTANCE_20261007.json) | `b33b0c4fb3365271b02ebcc5b40b55356e65161782387163d545888243e5327c` | evidence_or_analysis |
| E0025 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/analysis_result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0025_analysis_result.json) | `6ff37e99ba5b72df1259a60c98e7314b9b5dc75e7a950bc0799c10c201846bc8` | evidence_or_analysis |
| E0026 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/author_PBNA_legacy_Hessian_acceptance_20261002.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/author_PBNA_legacy_Hessian_acceptance_20261002.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0026_author_PBNA_legacy_Hessian_acceptance_20261002.json) | `f5de4d29e7c085720f4babc3d0c857d62ae45f5f41a19bb40f442bc5ddd4a0f7` | evidence_or_analysis |
| E0027 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_94e7481ded3b6a75/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_94e7481ded3b6a75/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0027_task.md) | `68546b71b77109db8fa63af95cea8cba71e9ef9cfd0e3f5d30f47a3f75b27a77` | historical_task_binding |
| E0028 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_reference_key_points.json) | `fab8073bb7bdc3c73cd54eee287a2f929bcfb72129a93ed3568c37b93fc7f39e` | historical_task_binding |
| E0029 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_reference_conclusions.json) | `b410b03e3c57df83a5733d70b8c6779e684d24eadb45571ebe7a8aa4b1f30291` | historical_task_binding |
| E0030 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_94e7481ded3b6a75/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_94e7481ded3b6a75/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_scoring_rules.json) | `17adc53125e571d6b430a569b952729d5abb5b94184b170446094b5b1fbd89a6` | historical_task_binding |
| E0031 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_94e7481ded3b6a75/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_94e7481ded3b6a75/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_task.md) | `b4df32d8e00a36935bdf57873ac6e6b56182a936e7515830b08a8d3d14409769` | historical_task_binding |
| E0032 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_94e7481ded3b6a75/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_94e7481ded3b6a75/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_reference_key_points.json) | `fab8073bb7bdc3c73cd54eee287a2f929bcfb72129a93ed3568c37b93fc7f39e` | historical_task_binding |
| E0033 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_94e7481ded3b6a75/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_94e7481ded3b6a75/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_reference_conclusions.json) | `b410b03e3c57df83a5733d70b8c6779e684d24eadb45571ebe7a8aa4b1f30291` | historical_task_binding |
| E0034 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_94e7481ded3b6a75/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_94e7481ded3b6a75/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_scoring_rules.json) | `17adc53125e571d6b430a569b952729d5abb5b94184b170446094b5b1fbd89a6` | historical_task_binding |
| E0035 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/c36b293fb09167ce_W01.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/c36b293fb09167ce_W01.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_c36b293fb09167ce_W01.json) | `c36b293fb09167ced77cc49841256facbf5604edc815f91721120d6c07602c06` | evidence_or_analysis |
| E0036 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/W01.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/W01.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_W01.json) | `c36b293fb09167ced77cc49841256facbf5604edc815f91721120d6c07602c06` | evidence_or_analysis |
| E0037 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/09f83b10706f793b_paper_94e7481ded3b6a75_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/09f83b10706f793b_paper_94e7481ded3b6a75_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_09f83b10706f793b_paper_94e7481ded3b6a75_delivery_integrity.json) | `09f83b10706f793bec56e2f5f91a99411dab9636de9fca062918463134deb0e5` | evidence_or_analysis |
| E0038 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_94e7481ded3b6a75_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_94e7481ded3b6a75_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_paper_94e7481ded3b6a75_delivery_integrity.json) | `09f83b10706f793bec56e2f5f91a99411dab9636de9fca062918463134deb0e5` | evidence_or_analysis |
| E0039 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/4deba901618f53c3_paper_94e7481ded3b6a75_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/4deba901618f53c3_paper_94e7481ded3b6a75_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_4deba901618f53c3_paper_94e7481ded3b6a75_primary_pages.json) | `4deba901618f53c3d859a85a8a8ce771085e6bdf28d5886de6d71e1572f97389` | evidence_or_analysis |
| E0040 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_94e7481ded3b6a75_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_94e7481ded3b6a75_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0040_paper_94e7481ded3b6a75_primary_pages.json) | `4deba901618f53c3d859a85a8a8ce771085e6bdf28d5886de6d71e1572f97389` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/ac0809e02b9fc909_paper_94e7481ded3b6a75_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/ac0809e02b9fc909_paper_94e7481ded3b6a75_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0041_ac0809e02b9fc909_paper_94e7481ded3b6a75_native_readback.json) | `ac0809e02b9fc90932dba9279400d72de2c4e97ebe643f8a55383965baa6307a` | evidence_or_analysis |
| E0042 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_94e7481ded3b6a75_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_94e7481ded3b6a75_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0042_paper_94e7481ded3b6a75_native_readback.json) | `ac0809e02b9fc90932dba9279400d72de2c4e97ebe643f8a55383965baa6307a` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_DCM/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_DCM/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0043_input.com) | `072ae410c48dd6cb645f54a85af823125ae2811a2251cb234b8539c8f01a0976` | input_or_analysis_code |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0044_input.com) | `bff7083eab793584666ffc0a21880a92379560866f213f6882110cd576906529` | input_or_analysis_code |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_DCM_TD10_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_DCM_TD10_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0045_input.com) | `40572f299bb66a61f750058b81c2052b20322926343a837be87172ac34f50d0d` | input_or_analysis_code |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0046_input.com) | `41012cd07b72ab4e90d35c27e811b0947fb81e65d26ba511efaccab313db5bf2` | input_or_analysis_code |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0047_input.com) | `f4b53460c5c4c408fa0093a1bc1c44ae1e4ded9194a7b25571e837e347955e9b` | input_or_analysis_code |
| E0048 | [docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/input.com](../../../../docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0048_input.com) | `821159a4c9a021b1c3642f748c91e6fd62e4f84d80fb6d060b9d9ce61bd20d31` | input_or_analysis_code |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_final_mapping_optical_transfer_a01/objects.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_final_mapping_optical_transfer_a01/objects.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0049_objects.json) | `8047212ed5d03589ddcd84981c744db01728169ad6589b5f388bff9326a448ca` | evidence_or_analysis |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_final_mapping_optical_transfer_a01/author_model.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_final_mapping_optical_transfer_a01/author_model.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0050_author_model.json) | `41c7f525db71b7992a9df4dceb21d0652b3e343c0a11b8785e2a2150597ffafd` | evidence_or_analysis |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_final_mapping_optical_transfer_a01/author_model_mapping.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_final_mapping_optical_transfer_a01/author_model_mapping.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0051_author_model_mapping.json) | `11afacf81fded5359427af3df7a50a33c5ebcdfe7a8a4201665f37b69acc21f6` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_final_mapping_optical_transfer_a01/observations.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_final_mapping_optical_transfer_a01/observations.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0052_observations.json) | `73039a3f8706e31b0f8abc3990eafc7363b4dae0469ab44912ac68dcaf489acd` | evidence_or_analysis |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_hole_electron_high/wavefunction.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_hole_electron_high/wavefunction.fchk) | `c4e89d6e3730eccb16e5469fada755f5b0a47ac417e8d804f4bc78282c1ea601` | evidence_or_analysis |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_pilot/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_pilot/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0054_native_excerpt.json) | `512cf6c6b3d27f0b53e1d8986a62c58c832e32434f3270e6266f33c12436489f` | native_output |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_transition_moments_v2/PBNA_free_TD10_pilot/transition_character.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_transition_moments_v2/PBNA_free_TD10_pilot/transition_character.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_transition_character.json) | `18747efa0984d78d91eca6290a7f8e01bb1ad1da0d8ea3940c949029afc4f418` | evidence_or_analysis |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_transition_moments_v2/PBNA_free_TD10_pilot/transition_density.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_transition_moments_v2/PBNA_free_TD10_pilot/transition_density.npz) | `7610607c1921d7fd4b4654255bb7f93206b1bc9aefac7c4dc5ca8d707ea27036` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_transition_moments_v2/PBNA_free_TD10_DCM/wavefunction.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_transition_moments_v2/PBNA_free_TD10_DCM/wavefunction.fchk) | `e1c1087c524b8dec0f939615c73525c3e790cb94aae69ffe8197aeed89fe48e2` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_transition_moments_v2/PBNA_free_TD10_DCM/transition_character.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_transition_moments_v2/PBNA_free_TD10_DCM/transition_character.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_transition_character.json) | `57a08bac428af00135083a3a7042902379dff25e5d9e931aad8ad791d2657d06` | evidence_or_analysis |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_transition_moments_v2/PBNA_free_TD10_DCM/transition_density.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_transition_moments_v2/PBNA_free_TD10_DCM/transition_density.npz) | `abb4e1f3a85619635dfb71186ef469c6d820e09d8bee43f9238408cdc977341f` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA50_S0_DCM_optfreq_a01/outputs/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA50_S0_DCM_optfreq_a01/outputs/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_native_excerpt.json) | `e84d96fe8b884e50d4825b5a9386181327410cb04ce7a6ce1cb84be148b64341` | native_output |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_DCM_optfreq_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_DCM_optfreq_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_native_excerpt.json) | `00a160c8d8fbf198bced3489a95e89697e10a87624e6f3a5575a360eb6b28f8d` | native_output |
| E0062 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_Newton_refine_a01/outputs/refinement/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_Newton_refine_a01/outputs/refinement/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_native_excerpt.json) | `e5fca8613991a13aa9cb25b52e958f07fed701ffd192f13e0b1b734f94bb972e` | native_output |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_cLR_Save_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_cLR_Save_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_native_excerpt.json) | `cccb9ad74037b094ed479398442cbb6cb94076f4f2f3af8d91d371c98e1f61bd` | native_output |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S0_NonEq_Read_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S0_NonEq_Read_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_native_excerpt.json) | `cf09ecb62bf2bc984c9a4ef1db58944304847aeff33df7a1a455c0d2176900e4` | native_output |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_native_excerpt.json) | `3a65e82f99359acf6ff62f396f3bb26e00fac0f84093d9088604d0fa7f48c9b1` | native_output |
| E0066 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA_matched_hessians_a01/outputs/analysis_result.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA_matched_hessians_a01/outputs/analysis_result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_analysis_result.json) | `81f65d516f6d1ba18eec5024ec123cdb5f92799e1cb462002599707370a47110` | evidence_or_analysis |
| E0067 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_94e7481ded3b6a75/REVIEW.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/papers/paper_94e7481ded3b6a75/REVIEW.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_REVIEW.json) | `e82f1c622238ce715da9977e2ff8bf65b435cc3fbf5150dfd820b1092b403b5b` | evidence_or_analysis |
| E0068 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA50_S0_DCM_optfreq_a01/outputs/execution.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA50_S0_DCM_optfreq_a01/outputs/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_execution.json) | `638c23e8ab76b4df5dedc4c6864f261953864646904425d6df9b091a238f28fc` | evidence_or_analysis |
| E0069 | [.software_cache/installations/gaussian/g16/install/g16/g16](../../../../.software_cache/installations/gaussian/g16/install/g16/g16) | `384f3baca38297d3f11ed2168bb9be836778fa4c5f5d07cb38751e3ed1a66db5` | evidence_or_analysis |
| E0070 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_Newton_refine_a01/outputs/refinement/execution.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_Newton_refine_a01/outputs/refinement/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_execution.json) | `d04699d8ec30012747dfc7b5d7f8bca06f058c83578e19f7ff99c34a682c9bf2` | evidence_or_analysis |
| E0071 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_S0_DCM_optfreq_a01/outputs/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_S0_DCM_optfreq_a01/outputs/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_native_excerpt.json) | `2b5e8f7af3f33c84990e21c16bba9f55702138e1c60e7a37f2d0cfe65e281054` | native_output |
| E0072 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_S0_DCM_optfreq_a01/outputs/execution.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_S0_DCM_optfreq_a01/outputs/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_execution.json) | `c1e68e4603490e15ae68964041848104ea7f2398145320723d8f3880c47d01b3` | evidence_or_analysis |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S0_NonEq_Read_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S0_NonEq_Read_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_execution.json) | `8cc555f1855847dac7bc77722ad04188ded98fb32d7482a6b7b9574e921f6cc0` | evidence_or_analysis |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S0_NonEq_Read_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S0_NonEq_Read_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_input.com) | `41012cd07b72ab4e90d35c27e811b0947fb81e65d26ba511efaccab313db5bf2` | input_or_analysis_code |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S0_NonEq_Read_a01/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S0_NonEq_Read_a01/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_DCM_optfreq_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_DCM_optfreq_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0076_execution.json) | `1b9f7bcd163cb844e32476e8818e52750d85c3c88ef8ee64a35f4140f478638c` | evidence_or_analysis |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S1_DCM_optfreq_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S1_DCM_optfreq_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0077_input.com) | `854bcbe5ddc6ec74fe8afd9dfbd2dfd3ea54dc4b1ec57b331acff217feffdee8` | input_or_analysis_code |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S1_DCM_optfreq_a01/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S1_DCM_optfreq_a01/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0078_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_cLR_Save_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_cLR_Save_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0079_execution.json) | `0dc4888646614496762256c3dc30eb85fdc44f5f9bc8f220bc3d590830865958` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S1_cLR_Save_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S1_cLR_Save_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0080_input.com) | `37d9f048a8b5a5866d10f556e4c7d769de443191dbffbaadeb89e761264ddf47` | input_or_analysis_code |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S1_cLR_Save_a01/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_PBNA_S1_cLR_Save_a01/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0081_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0082_execution.json) | `5eb3f39b9e6120ac1d0c4b13bda1453303ee52a49ea051bda75e90afe30c0462` | evidence_or_analysis |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0083_input.com) | `bff7083eab793584666ffc0a21880a92379560866f213f6882110cd576906529` | input_or_analysis_code |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0084_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0085_execution.json) | `ac1e1bc2df393a6a0eb1e77d6b5bbcf88c13a38ec161285c2c4cdd14bf66eed4` | evidence_or_analysis |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0086_input.com) | `41012cd07b72ab4e90d35c27e811b0947fb81e65d26ba511efaccab313db5bf2` | input_or_analysis_code |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0087_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0088_execution.json) | `592adaf3443e3bf3cbf134577ff8bdcf37bf8d141823a1ae8db24a83c00f3687` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0089_input.com) | `f4b53460c5c4c408fa0093a1bc1c44ae1e4ded9194a7b25571e837e347955e9b` | input_or_analysis_code |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S1_DCM_optfreq_a01/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0090_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0091_execution.json) | `e63b81fd62834c67b3cf00e505d0dc40f80f792e7b3a8322fe6c0a84aff5ae4c` | evidence_or_analysis |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0092_input.com) | `37d9f048a8b5a5866d10f556e4c7d769de443191dbffbaadeb89e761264ddf47` | input_or_analysis_code |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0093_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0094 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_strict_PBNA_full80_S0_NonEq_Read_a01/identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0094_identity.json) | `2cf52c29964e439ec501a5911f597409e16066bcbcce7c1398f2ad3fc6109c7f` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/strict_PBNA_full80_S1_chain_gate_20261001.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/strict_PBNA_full80_S1_chain_gate_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0095_strict_PBNA_full80_S1_chain_gate_20261001.json) | `6ff9f8a5466b96dd739f529a2e8872c7d9a9f0ed6ae60fd8c46dbb2a9124ea15` | evidence_or_analysis |
| E0096 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/strict_PBNA_full80_field_chain_gate_20261001.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/strict_PBNA_full80_field_chain_gate_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0096_strict_PBNA_full80_field_chain_gate_20261001.json) | `9b45ab6c9ed395e6ac9b4d1900066a1c0c713d6c9dbc0badba23abef20eeaf80` | evidence_or_analysis |
| E0097 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_PBNA_solution_emission_accept_a01_acceptance.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/v2_PBNA_solution_emission_accept_a01_acceptance.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0097_v2_PBNA_solution_emission_accept_a01_acceptance.json) | `c854359469f8e9cd06981317161f15e13242c11fd62b6ba3fb14859a6f185baa` | evidence_or_analysis |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_cLR_state_gate_chain_a01/field_transition/transition_character.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_cLR_state_gate_chain_a01/field_transition/transition_character.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0098_transition_character.json) | `b45a02eaa182d6bae6272a3bb9b18cd3d0f14b327764a0a3ce99615d18ee93c9` | evidence_or_analysis |
| E0099 | [docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/status.json](../../../../docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/native_workspace/outputs/execution_jobs/job_8b7c43a8ec8a43a493c9200b841f5b91/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0099_status.json) | `c63b329b9c952d2644727f5fef851eb36865405962190b5a480dfe8ce0d1699a` | evidence_or_analysis |
| E0100 | [tasks/paper_reproduction/paper_94e7481ded3b6a75/agent_input/data/inputs/pbna.xyz](../../../paper_reproduction/paper_94e7481ded3b6a75/agent_input/data/inputs/pbna.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0100_pbna.xyz) | `164a887817e8768675fc684fd063f5871ff18fcec8005e129b84accdcfad97b7` | input_or_analysis_code |
| E0101 | [tasks/paper_reproduction/paper_94e7481ded3b6a75/agent_input/data/inputs/system.json](../../../paper_reproduction/paper_94e7481ded3b6a75/agent_input/data/inputs/system.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0101_system.json) | `9d1d2fc560b9c7f4ba1de6c962293ec5ff81c38a3fdf4e69d1c4cb1853aab349` | historical_task_binding |
| E0102 | [docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.json](../../../../docs/v2_verification/history/verification/group_1/paper_94e7481ded3b6a75/artifacts/orbital_reaudit_20260916/frontier_mulliken.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0102_frontier_mulliken.json) | `d6bbdf58f814d879c6a026e64f44c8016312c0ddbc88505625f046dd3e3a0c2e` | evidence_or_analysis |
| E0103 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/execution.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0103_execution.json) | `acfc7ba8a06c7356ec31340acf0abfc977f19278a70555303626935f22b904ab` | evidence_or_analysis |
| E0104 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/config.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/config.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0104_config.json) | `ef0b5d855ce106004401a6598065ab126164d4626fe7e5527f1ffc9993a303f3` | evidence_or_analysis |
| E0105 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/DCM_80_native_refined_modes.npz](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_native_mode_closure_a02/outputs/DCM_80_native_refined_modes.npz) | `1cfd914844cb301c577300bf22ad5304d83b68032ef80a74b67d7b460a6d4907` | evidence_or_analysis |
| E0106 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_S0_DCM_optfreq_a01/outputs/wavefunction.fchk](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_S0_DCM_optfreq_a01/outputs/wavefunction.fchk) | `d0629146fcfe411fa086148d9cc0a7cb6f039c79d490aa33f1b7f3ace3077d00` | evidence_or_analysis |
| E0107 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_Newton_refine_a01/outputs/refinement/wavefunction.fchk](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_Newton_refine_a01/outputs/refinement/wavefunction.fchk) | `d26625ba7bc0927b9284e469c8f7bb629366798b0b548a8705dfcad025432e67` | evidence_or_analysis |
| E0108 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/inputs/v2_author_PBNA_SI_G09Defaults_Freq_20261002_a01/identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0108_identity.json) | `5e5ab92bfe94f062066fc04f9721e262c4739e1f4482a740a2fac79f7217be9a` | evidence_or_analysis |
| E0109 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/pbna_native_source_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/report/v2_execution_20260929/pbna_native_source_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0109_pbna_native_source_audit.json) | `629643f4cdfe33d48fa930721b4727a0784e98c93a5ad6dc106ac097c38789b3` | evidence_or_analysis |
| E0110 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_94e7481ded3b6a75/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_94e7481ded3b6a75/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0110_critical_failures.json) | `d0c87fbb56038ccecdfc2faa1ee74335babb2349e36e99fbd340387114c72b46` | historical_task_binding |
| E0111 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_94e7481ded3b6a75/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_94e7481ded3b6a75/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0111_critical_failures.json) | `d0c87fbb56038ccecdfc2faa1ee74335babb2349e36e99fbd340387114c72b46` | historical_task_binding |
| E0112 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_pilot/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_free_TD10_pilot/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0112_input.com) | `dc5ca66c310e80847deb3193301e38a684a21e4bbd60941a97115e4245e54d87` | input_or_analysis_code |
| E0113 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA50_S0_DCM_optfreq_a01/outputs/input.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA50_S0_DCM_optfreq_a01/outputs/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0113_input.com) | `39a5ee75b52bcf0486617dec74f82ab8dbd86574fbffdf8edfbf8a690df11aac` | input_or_analysis_code |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_DCM_optfreq_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_DCM_optfreq_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0114_input.com) | `854bcbe5ddc6ec74fe8afd9dfbd2dfd3ea54dc4b1ec57b331acff217feffdee8` | input_or_analysis_code |
| E0115 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_Newton_refine_a01/outputs/refinement/input.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_Newton_refine_a01/outputs/refinement/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0115_input.com) | `f0c75bd48a17ffe6c45c9996110c6cd4b3849155fea11443bf7cc50068815af3` | input_or_analysis_code |
| E0116 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_cLR_Save_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S1_cLR_Save_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0116_input.com) | `37d9f048a8b5a5866d10f556e4c7d769de443191dbffbaadeb89e761264ddf47` | input_or_analysis_code |
| E0117 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S0_NonEq_Read_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_PBNA_S0_NonEq_Read_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0117_input.com) | `41012cd07b72ab4e90d35c27e811b0947fb81e65d26ba511efaccab313db5bf2` | input_or_analysis_code |
| E0118 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/v2_strict_PBNA_full80_S1_cLR_Save_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0118_input.com) | `37d9f048a8b5a5866d10f556e4c7d769de443191dbffbaadeb89e761264ddf47` | input_or_analysis_code |
| E0119 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA50_S0_DCM_optfreq_a01/outputs/wavefunction.fchk](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA50_S0_DCM_optfreq_a01/outputs/wavefunction.fchk) | `8b55598043d266f723afb1d3ee433184309567b778dbad6ac65d1369b97ccb6d` | evidence_or_analysis |
| E0120 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/S0_free_geometry_native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/S0_free_geometry_native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0120_native_excerpt.json) | `30f12e30885280ccfd735cc779591538187adca36a7f66f1b0bef2438d442805` | native_output |
| E0121 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_S1_free_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_S1_free_optfreq/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0121_native_excerpt.json) | `398f220b8f5939450d403925437379a61961116faf9e1baecd80c1ec871fcdbf` | native_output |
| E0122 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_S0_DCM_optfreq_a01/outputs/input.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W01/papers/paper_94e7481ded3b6a75/cases/w01_PBNA80_S0_DCM_optfreq_a01/outputs/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0122_input.com) | `39a5ee75b52bcf0486617dec74f82ab8dbd86574fbffdf8edfbf8a690df11aac` | input_or_analysis_code |
| E0123 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/S0_free_geometry_native_input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/S0_free_geometry_native_input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0123_S0_free_geometry_native_input.com) | `821159a4c9a021b1c3642f748c91e6fd62e4f84d80fb6d060b9d9ce61bd20d31` | input_or_analysis_code |
| E0124 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_free_TD10_DCM.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_free_TD10_DCM.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0124_PBNA_free_TD10_DCM.xyz) | `f27660a8c9c33496925cbf5e829c7b2cab1c4281747b5c16117f2e3d8af7f081` | input_or_analysis_code |
| E0125 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_both30_fixed_TD10_DCM.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_both30_fixed_TD10_DCM.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0125_PBNA_both30_fixed_TD10_DCM.xyz) | `4340491ac15fbfa3722c1d4a705b3f877e1cd72d68d43617a8fec2d82d10b80a` | input_or_analysis_code |
| E0126 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_free_optfreq.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_free_optfreq.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0126_PBNA_S1_free_optfreq.xyz) | `414f5e9d99ccf7b78308efba23ad8c4f7bdba5d67aa8a790771c59d55bd12402` | input_or_analysis_code |
| E0127 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_both30_fixed_TD10.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_both30_fixed_TD10.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0127_PBNA_both30_fixed_TD10.xyz) | `0281e0c7b81abe2f2aaf155d48626fcc1e9a9044bcf63414d200dcde5e38a942` | input_or_analysis_code |
| E0128 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S0_both75_restrained.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S0_both75_restrained.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0128_PBNA_S0_both75_restrained.xyz) | `c228aada6699453d3ca0d8ef822dacfba4c58106284d725628b70cade52e7478` | input_or_analysis_code |
| E0129 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/S0_free_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/S0_free_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0129_S0_free_geometry.xyz) | `76f54ee12c3e0426fbe9639e6122539a3693926ad422efc49403aa77102488dc` | input_or_analysis_code |
| E0130 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S0_both75_restrained_TD10.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S0_both75_restrained_TD10.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0130_PBNA_S0_both75_restrained_TD10.xyz) | `11a1cf61b6f7be8fc8400898ca01aac8e77cefa049f43ea18db3d30ae50d5e63` | input_or_analysis_code |
| E0131 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_both30_restrained.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_both30_restrained.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0131_PBNA_S1_both30_restrained.xyz) | `6c08075c6f977507a30402cce4a9e0db66c7a3a1a6d3b364c06bb8cd69c79e0e` | input_or_analysis_code |
| E0132 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_free_TD10_pilot.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_free_TD10_pilot.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0132_PBNA_free_TD10_pilot.xyz) | `324cfe1508c8b15a9a126e9635e68cb75da7781ea3af062016b9564f6c8793d8` | input_or_analysis_code |
| E0133 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_both75_restrained_TD10.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_both75_restrained_TD10.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0133_PBNA_S1_both75_restrained_TD10.xyz) | `3e5c370b46824129d41b31183768ec96687e24ba910db9030143c48807e06792` | input_or_analysis_code |
| E0134 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_both30_relaxed_TD10.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_both30_relaxed_TD10.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0134_PBNA_both30_relaxed_TD10.xyz) | `d3f5e497425124e7613307785cb2efd6819ec2b105b044e4bb9adfb3c50a21db` | input_or_analysis_code |
| E0135 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_both75_restrained.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_both75_restrained.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0135_PBNA_S1_both75_restrained.xyz) | `0fc07ae9173825cc26a5b0acb501b5383f5c49678b919d40ee11a8b6865ad378` | input_or_analysis_code |
| E0136 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_both30_restrained_TD10.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_both30_restrained_TD10.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0136_PBNA_S1_both30_restrained_TD10.xyz) | `fd3a9c81b7ccda17961d8603d65c9df05db9863ccb88f486078f40fef4cd77e2` | input_or_analysis_code |
| E0137 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_both75_fixed_TD10.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_both75_fixed_TD10.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0137_PBNA_both75_fixed_TD10.xyz) | `ecb6e17af1365e4f9288a509ac563076c66ecb5dcda8ef98849000483621bc16` | input_or_analysis_code |
| E0138 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S0_both30_restrained.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S0_both30_restrained.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0138_PBNA_S0_both30_restrained.xyz) | `861af5745eaf3fb233834ffe765df9e0685f38453c0a31f8f927aeed4c652a64` | input_or_analysis_code |
| E0139 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_free_optfreq_TD10.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/evidence/PBNA_S1_free_optfreq_TD10.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0139_PBNA_S1_free_optfreq_TD10.xyz) | `3ee3cb0c1e8856e1f67f4a793390629f68e17aa85348918a6cc1d572cc5f5f6c` | input_or_analysis_code |
| E0140 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_S1_free_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_94e7481ded3b6a75/outputs/PBNA_S1_free_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_94e7481ded3b6a75/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0140_input.com) | `48c374be9771b9e52100b9bed7e9f4536e407a43afd23dade3b1516ce788ebe3` | input_or_analysis_code |
| N0141 | [tasks/v2_autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_key_points.json) | `fab8073bb7bdc3c73cd54eee287a2f929bcfb72129a93ed3568c37b93fc7f39e` | latest_review_evidence |
| N0142 | [tasks/v2_autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_conclusions.json) | `b410b03e3c57df83a5733d70b8c6779e684d24eadb45571ebe7a8aa4b1f30291` | latest_review_evidence |
| N0143 | [tasks/v2_autonomous_research/paper_94e7481ded3b6a75/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_94e7481ded3b6a75/evaluation/scoring_rules.json) | `17adc53125e571d6b430a569b952729d5abb5b94184b170446094b5b1fbd89a6` | latest_review_evidence |
| N0144 | [tasks/v2_autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_validation_plan.md](../../../v2_autonomous_research/paper_94e7481ded3b6a75/evaluation/reference_validation_plan.md) | `9c0ac9695390877356c9ba81182d995294eb882808bdd58ad7e6c9c6dadab821` | latest_review_evidence |
| N0145 | [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/evaluation/scoring_rules.json](scoring_rules.json) | `17adc53125e571d6b430a569b952729d5abb5b94184b170446094b5b1fbd89a6` | latest_review_evidence |
| N0146 | [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `fd9193efd73cdec5430e1948048d56d79445bb147d6a8627bce7c19404176a8d` | latest_review_evidence |
| N0147 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0148 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json) | `66b4df5fb10f6b54e16cafe1cc04f2dd2ed2ff67af141ca58d0b02b4d1b922f1` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/agent_input/task.md](../agent_input/task.md) | `b4df32d8e00a36935bdf57873ac6e6b56182a936e7515830b08a8d3d14409769` |
| [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/evaluation/reference_key_points.json](reference_key_points.json) | `fab8073bb7bdc3c73cd54eee287a2f929bcfb72129a93ed3568c37b93fc7f39e` |
| [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/evaluation/reference_conclusions.json](reference_conclusions.json) | `b410b03e3c57df83a5733d70b8c6779e684d24eadb45571ebe7a8aa4b1f30291` |
| [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/evaluation/scoring_rules.json](scoring_rules.json) | `17adc53125e571d6b430a569b952729d5abb5b94184b170446094b5b1fbd89a6` |
| [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/evaluation/critical_failures.json](critical_failures.json) | `d0c87fbb56038ccecdfc2faa1ee74335babb2349e36e99fbd340387114c72b46` |
| [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/evaluation/evidence_map.json](evidence_map.json) | `6be5b399b5f9a3c7cf6be0cd25db4150c4c1bb9baf7241d3f5083e469c84ae94` |
| [tasks/v2_paper_reproduction/paper_94e7481ded3b6a75/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `fd9193efd73cdec5430e1948048d56d79445bb147d6a8627bce7c19404176a8d` |

## Current scoring migration — 2026-10-19
Active policy: paper_science_v2, 100 binary scientific-result points with intermediate and final conclusions. Active rule/reference files supersede historical scoring weights or freezes. No process score or multiplier remains. This migration is not new computation or new chemical acceptance; independently strict frozen-scope status remains unchanged. Preserved limitations: Author source-model E/ZPE/G/S were reproduced at printed precision using genuine frequency output; independently optimized50-atom and80-atom states are valid. Frontier residuals+0.06018/+0.06928eV remain. Actual50/80 S1 values3.4243/3.4122eV and cLR emission2.9698303/2.9187782eV are verification findings, not source numeric targets. Full80 E00=3.0295791eV (409.2456nm) and cLR emission424.7812nm are distinct observables. Exact experimental fine structure, rates and AIE are not reproduced.

## Scoring-contract repair — 2026-10-19, round 3

- Both modes now state the direct full-80-atom route explicitly for absorption/emission adequacy, alongside justified approximation transfer. PR disclosed surrogate numerical reproduction remains. Source observations, 50/80 verification and accepted limitations are preserved.

The source and native calculations above remain unchanged historical evidence. Active mode-specific rules govern current scoring; this edit does not certify a new chemistry run or alter strict acceptance.
