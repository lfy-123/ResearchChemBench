# Second review, 2026-10-28

The original question concerns local interactions and their implications for epoxide activation and chain-end association. Its two P-O distances and three P-ADCH charges were intermediate evidence in the original rubric. Whether their promotion to five mandatory final quantities worth 30 points unduly constrains an explanatory task remains an expert design question; the newer public checklist alone does not resolve it. Existing numerical targets, tolerances, weights and required results are unchanged. Local reconstructed-model and probe evidence is reusable within its stated limits, not a new whole-task pass. The prior scope note below is retained as history, not proof that all old supporting quantities must become final endpoints. TFPO encounter Hessians are positive, but their frequency-link predicted displacements retain the documented Tight residual-step caveats. No new chemistry was computed.

# 本次V3范围与逐命题证据复用（2026-10-28）

局部分子解释范围保留；9个最终命题，5个明确最终局部物性各6分、接触网络20、空间静电20、两类作用解释各15。保留原五数值目标/容差；不按作者中间结构交付计分，不把给定NMR当预测或把局部接触升格为聚合动力学。

- `po_op`：正文Figure6；原生free/PO/PA频率波函数及final_adch_baseline_reparse和postprocessing_audit覆盖；原距离±0.02Å/电荷±0.03e保持。
- `pa_op`：正文Figure6；原生free/PO/PA频率波函数及final_adch_baseline_reparse和postprocessing_audit覆盖；原距离±0.02Å/电荷±0.03e保持。
- `free_p_adch`：正文Figure6；原生free/PO/PA频率波函数及final_adch_baseline_reparse和postprocessing_audit覆盖；原距离±0.02Å/电荷±0.03e保持。
- `po_p_adch`：正文Figure6；原生free/PO/PA频率波函数及final_adch_baseline_reparse和postprocessing_audit覆盖；原距离±0.02Å/电荷±0.03e保持。
- `pa_p_adch`：正文Figure6；原生free/PO/PA频率波函数及final_adch_baseline_reparse和postprocessing_audit覆盖；原距离±0.02Å/电荷±0.03e保持。
- `contact_reorganization`：PO O-P/O-CH2H/O-CH3H=1.829262/2.125093/2.440470Å；PA=2.652210/2.311797/2.363291Å，映射H角色已核对。
- `charge_separated_electrostatics`：signed ESP rho=.001au、spacing=.15bohr完整表面导出审查；P局部正区与羧酸氧负区，不能由蓝色说电子密度增加。
- `epoxide_association_role`：PA61/TFPO及Et3B/TFPO实际SMD苯探针最低点；实验NMR只作给定背景，未计算化学位移或开环速率。
- `chain_end_association_role`：完整PA局部O/H接触与signedESP+ethoxide实验；支持关联，缺真实长链结合G/回咬势垒，未要求。

未提交新计算；以下历史正文逐字保留。历史PASS不代表新V3全部命题重新验证通过。

---

# V2 验证计算参考：PA/膦局部相互作用

论文：`paper_ef26687d63a37e29`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：核心约0.823 Å结构重组与约0.47e极化幅度恢复，误差小于相关效应且定义相同；没有用不完整图或色图当密度量。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

加入PA如何改变局部相互作用及其对环氧活化/链端稳定的解释限度。

冻结题面中的科学目标：

How does adding phthalic anhydride change the local molecular interactions in the (Et2N)3P/Et3B system, and what can those changes establish about epoxide activation and chain-end stabilization during CO2/propylene-oxide copolymerization?

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The authors propose that PA reacts with the Lewis base to generate an intramolecular phosphonium/carboxylate zwitterion, interacting with Et3B and influencing both epoxide activation and chain-end association (main pp9–10). Their DFT comparison concerns free(Et2N)3P, the PO adduct and the PA adduct, not a full polymer propagation/backbiting network. SI pp4–5 specifies Gaussian16 B3LYP/6-31G(d) with D3(BJ), with ADCH populations from Multiwfn using vibrational-analysis wavefunctions. The source does not explicitly specify a continuum solvent for these molecular calculations. Main p10 reports PO-adduct O···P1.828 Å versus PA-adduct2.651 Å and differing O···H contacts/populations; those local observations support an interpretation but do not directly prove suppressed backbiting. Reproduce and assess the local molecular baseline or justify controlled substitutions. NMR probe results use TFPO/C6D6 and sodium ethoxide/CDCl3, with preparation details inSI p4. Source polymer kinetics and dilution behavior are a separate scale. The fixed PA-containing two-PO/one-CO2 oligomer, no-PA chain pair, two-Et3B path inventory and tenfold-PO test inV1 were benchmark additions.

Source-coordinate limitation: SI physical pp39-40 lists 51 atoms (C14H30N3O3P) for the PA adduct; the complete stoichiometric (Et2N)3P + PA model has 61 atoms (C20H34N3O3P), a C6H4 difference. The complete PA reagent connectivity in systems.json remains valid. Reconstruction must identify retained source atoms, added atoms and the resulting graph; a reconstructed model is not an unchanged source geometry. No missing coordinates are supplied or invented here. For main physical p8 Figure 6 and p10, distinguish a specified H-site ADCH population, the nearest-contact H and a declared alpha/beta-H family statistic. Define sites from the N-ethyl CH2/CH3 graph and map them explicitly; do not equate a figure-labelled H with a nearest site or family mean without evidence. Report signed electrostatic potential with its units and surface definition separately from electron density; source colour/prose alone is not a density measurement. These local observables do not by themselves establish polymer propagation or backbiting rates.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_ef26687d63a37e29/documents/main.pdf](../../../../papers/paper_ef26687d63a37e29/documents/main.pdf) | `bf0ec692ef2eec7d4342ed722884bcabb2137396dcb3fc6c6a867eed7f62b0b8` |
| [papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf](../../../../papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf) | `bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

B3LYP/6-31G(d)-D3BJ完整free/PO/PA模型，Multiwfn ADCH；按完整化学图明示重建PA缺失C6H4，61原子而非沿用残缺51原子。

1. 完整核对 free/PO/PA 图。源 PA 坐标缺 C6H4 的 51 原子块已明示重建成 61 原子，不继续使用残缺模型；free/PO/PA 为 46/56/61 原子，保持 O49/P46 与 N-ethyl α/β 氢映射。

2. 按作者 B3LYP/6-31G(d) 实际 Opt/Freq，核收 132/162/177 正模；从原生波函数运行 Multiwfn ADCH 及有符号 ESP，保留完整三十个 N-ethyl H 的接触分布。

3. 提取 P-ADCH=−0.01900749/0.44705269/0.45568970 e；PO→PA 的 O–P=1.829262→2.652210 Å，对源 1.828→2.651，α/β 接触逐项对照，不按图注含混只选一个最近 H。

4. 核收 PA/TFPO 71 原子与 Et3B/TFPO 32 原子的真实配对最低点（207/90 正模），标明这些是验证者 SMD 苯接触扩展；原文 31P/19F/1H NMR 为实验观察，不能写成已经计算了化学位移。

5. 结合结构重组、局部静电、氧探针接触支持有限局部解释；不由电荷/接触推出开环势垒、结合自由能、回咬速率、体相抗稀释或聚合分子量。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

#### required_calculations（冻结记录 E0006）

```json
[
  {
    "id": "free_minimum",
    "purpose": "作者自由膦/PO加合物/PA加合物局部结构",
    "author_or_added": "AUTHOR_ACTUAL",
    "source_locator": "SI4–5; main8 Fig6; SI39–40 PA缺C6H4",
    "identity": {
      "atoms": 46,
      "charge": 0,
      "multiplicity": 1,
      "PA_reconstruction": null
    },
    "method": "Gaussian16 B3LYP-D3BJ/6-31G(d), gas phase; source specifies no continuum. Multiwfn ADCH uses frequency wavefunctions.",
    "status": "COMPLETE_REUSED",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_native.log",
        "sha256": "b41cff05390e6a2d83e02078e96368cb8a822a3c4820c84395223391881a43fa"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_postprocessing_audit.json",
        "sha256": "907cd8bf3f028fba3f06f08a9d0bbaa71705848a73fc396ef6a116289b88eff3"
      }
    ],
    "native_validity": {
      "normal": true,
      "Opt_complete": true,
      "positive_modes": 132,
      "postFreq_prediction_not_Opt_certificate": true
    }
  },
  {
    "id": "PO_minimum",
    "purpose": "作者自由膦/PO加合物/PA加合物局部结构",
    "author_or_added": "AUTHOR_ACTUAL",
    "source_locator": "SI4–5; main8 Fig6; SI39–40 PA缺C6H4",
    "identity": {
      "atoms": 56,
      "charge": 0,
      "multiplicity": 1,
      "PA_reconstruction": null
    },
    "method": "Gaussian16 B3LYP-D3BJ/6-31G(d), gas phase; source specifies no continuum. Multiwfn ADCH uses frequency wavefunctions.",
    "status": "COMPLETE_REUSED",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_native.log",
        "sha256": "ad358229b1eef687bc782b70557c5f0236bf03ec84b38f559db7fb09cb7992c6"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_postprocessing_audit.json",
        "sha256": "7f50a845f255580b34ac2a3721be19fffe835db47440a9b71d198a102ae07f7a"
      }
    ],
    "native_validity": {
      "normal": true,
      "Opt_complete": true,
      "positive_modes": 162,
      "postFreq_prediction_not_Opt_certificate": true
    }
  },
  {
    "id": "PA_minimum",
    "purpose": "作者自由膦/PO加合物/PA加合物局部结构",
    "author_or_added": "AUTHOR_ACTUAL_WITH_DECLARED_RECONSTRUCTION",
    "source_locator": "SI4–5; main8 Fig6; SI39–40 PA缺C6H4",
    "identity": {
      "atoms": 61,
      "charge": 0,
      "multiplicity": 1,
      "PA_reconstruction": "C20H34N3O3P, 61 atoms, retained source core plus C6H4"
    },
    "method": "Gaussian16 B3LYP-D3BJ/6-31G(d), gas phase; source specifies no continuum. Multiwfn ADCH uses frequency wavefunctions.",
    "status": "COMPLETE_REUSED",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_native.log",
        "sha256": "97736ab5df99445f9b5d7f2f2e47495419921cedda620ee938bf91572347f228"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_postprocessing_audit.json",
        "sha256": "6fcb0a083ed5d841409a1e725f257390948a9fb839e448daab4c907fe06ad3ba"
      }
    ],
    "native_validity": {
      "normal": true,
      "Opt_complete": true,
      "positive_modes": 177,
      "postFreq_prediction_not_Opt_certificate": true
    }
  },
  {
    "id": "normalized_ADCH_and_contacts",
    "purpose": "同一波函数上的归一化P/H电荷、逐原子映射和接触定义",
    "author_or_added": "AUTHOR_ACTUAL",
    "source_locator": "SI4–5; main8/10",
    "identity": {
      "objects": [
        "free46",
        "PO56",
        "PA61"
      ],
      "site": "P46; alpha/beta H from N-ethyl graph"
    },
    "method": "Gaussian16 B3LYP-D3BJ/6-31G(d), gas phase; source specifies no continuum. Multiwfn ADCH uses frequency wavefunctions.",
    "status": "COMPLETE_REUSED",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W07/papers/paper_ef26687d63a37e29/cases/final_adch_baseline_reparse_20261007/run/results.json",
        "sha256": "cd9d7977b91e1d05f1aaa9a3ce57775b1fb47681aae240a61964bf3aa2de06af"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_ADCH.out",
        "sha256": "9d8070dc7af5daa9b4a8c994b908edbfba262bd8eafd7285bdd577d0ed2e7941"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_ADCH.out",
        "sha256": "26e89078fb21994a8ee64e70300cdc78caa5c9861ab9f97c4210099b4ffa5e08"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_ADCH.out",
        "sha256": "fa5888a0300aaa919419b865a159d63855ee07b67cd858652474c83f67662a05"
      }
    ],
    "native_validity": {
      "job_id": "hpc-job-23e54e57-38c1-401e-93d9-f979ccd283ba",
      "native_rc": 0,
      "P_e": [
        -0.01900749,
        0.44705269,
        0.4556897
      ],
      "normalized": true,
      "unmapped_figure_H_not_fitted": true
    }
  },
  {
    "id": "signed_ESP",
    "purpose": "有单位与等密度面定义的局部静电势",
    "author_or_added": "AUTHOR_ACTUAL_WITH_EXPLICIT_ANALYSIS_DEFINITION",
    "source_locator": "main8 Fig6; SI4–5",
    "identity": {
      "objects": [
        "free46",
        "PO56",
        "PA61"
      ],
      "charge": 0,
      "multiplicity": 1
    },
    "method": "Gaussian16 B3LYP-D3BJ/6-31G(d), gas phase; source specifies no continuum. Multiwfn ADCH uses frequency wavefunctions.; ESP at rho=.001 au, spacing=.15 bohr, signed kcal/mol.",
    "status": "COMPLETE_REUSED",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/surface_export_correction_20260930.json",
        "sha256": "a21c8362fce82f758a0708dfc65696477afb173d0d1b77b1e2a5f5673fab34d7"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_MEP.out",
        "sha256": "600cc0ad76dfac5e19329ea135352a70cea102d9d5d072099bc0c2249cb1a82f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_MEP.out",
        "sha256": "73972ebf93bc54d3fffc0ff9384fb804e0ba6ee18856df4cc816fdd93b331cee"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_MEP.out",
        "sha256": "13e516e387d0d5f5946ceeb89a080b59abcb1bb9e334b464c4380ab7756bb0ff"
      }
    ],
    "native_validity": {
      "native_surface_complete": true,
      "full_post_elimination_exports_verified": true,
      "density_not_equated_to_ESP": true
    }
  },
  {
    "id": "PA61_TFPO_C6D6proxy_contact_pilot",
    "purpose": "独立检验含氧探针接触可行性；与NMR证据边界对应",
    "author_or_added": "ADDED_CURRENT_INVESTIGATION",
    "source_locator": "SI4实验探针；当前V2局部分子问题",
    "identity": {
      "atoms": 71,
      "charge": 0,
      "multiplicity": 1
    },
    "method": "B3LYP-D3BJ/6-31G(d), SMD benzene representing C6D6; not neat80C polymerization.",
    "status": "COMPLETE_REUSED",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log",
        "sha256": "4856a47f40ed9a0dc7382574c00a584832ffe97858695c04493420020fd7eddc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/PA_TFPO_minimum_review_20260930.json",
        "sha256": "80aaef355740c5d766a41a5efe3f212818672fd016979af4465d3ebec55082c9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_probe_protocol_review_20260930.json",
        "sha256": "0cf4a53d0ff56d0eb6d6eaf789f300af7caacb709125782dd88608b78a6b286d"
      }
    ],
    "native_validity": {
      "normal": true,
      "original_Opt_four_YES": true,
      "positive_modes": 207,
      "no_binding_G_or_kinetics_claim": true
    }
  },
  {
    "id": "Et3B_TFPO_C6D6proxy_contact_pilot",
    "purpose": "独立检验含氧探针接触可行性；与NMR证据边界对应",
    "author_or_added": "ADDED_CURRENT_INVESTIGATION",
    "source_locator": "SI4实验探针；当前V2局部分子问题",
    "identity": {
      "atoms": 32,
      "charge": 0,
      "multiplicity": 1
    },
    "method": "B3LYP-D3BJ/6-31G(d), SMD benzene representing C6D6; not neat80C polymerization.",
    "status": "COMPLETE_REUSED",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log",
        "sha256": "da10cbd4c49705269d2e32667ccf997aa27093a00447db69c7e24b6f7a23bcf8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/Et3B_TFPO_minimum_review_20260930.json",
        "sha256": "da068c1aa70491594ec17847d4dd95e623719821a286120b2d7aa5dc71349684"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_probe_protocol_review_20260930.json",
        "sha256": "0cf4a53d0ff56d0eb6d6eaf789f300af7caacb709125782dd88608b78a6b286d"
      }
    ],
    "native_validity": {
      "normal": true,
      "original_Opt_four_YES": true,
      "positive_modes": 90,
      "no_binding_G_or_kinetics_claim": true
    }
  }
]
```


#### reused_results（冻结记录 E0006）

```json
[
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_native.log",
    "sha256": "b41cff05390e6a2d83e02078e96368cb8a822a3c4820c84395223391881a43fa"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_postprocessing_audit.json",
    "sha256": "907cd8bf3f028fba3f06f08a9d0bbaa71705848a73fc396ef6a116289b88eff3"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_native.log",
    "sha256": "ad358229b1eef687bc782b70557c5f0236bf03ec84b38f559db7fb09cb7992c6"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_postprocessing_audit.json",
    "sha256": "7f50a845f255580b34ac2a3721be19fffe835db47440a9b71d198a102ae07f7a"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_native.log",
    "sha256": "97736ab5df99445f9b5d7f2f2e47495419921cedda620ee938bf91572347f228"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_postprocessing_audit.json",
    "sha256": "6fcb0a083ed5d841409a1e725f257390948a9fb839e448daab4c907fe06ad3ba"
  },
  {
    "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W07/papers/paper_ef26687d63a37e29/cases/final_adch_baseline_reparse_20261007/run/results.json",
    "sha256": "cd9d7977b91e1d05f1aaa9a3ce57775b1fb47681aae240a61964bf3aa2de06af"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_ADCH.out",
    "sha256": "9d8070dc7af5daa9b4a8c994b908edbfba262bd8eafd7285bdd577d0ed2e7941"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_ADCH.out",
    "sha256": "26e89078fb21994a8ee64e70300cdc78caa5c9861ab9f97c4210099b4ffa5e08"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_ADCH.out",
    "sha256": "fa5888a0300aaa919419b865a159d63855ee07b67cd858652474c83f67662a05"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/surface_export_correction_20260930.json",
    "sha256": "a21c8362fce82f758a0708dfc65696477afb173d0d1b77b1e2a5f5673fab34d7"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_MEP.out",
    "sha256": "600cc0ad76dfac5e19329ea135352a70cea102d9d5d072099bc0c2249cb1a82f"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_MEP.out",
    "sha256": "73972ebf93bc54d3fffc0ff9384fb804e0ba6ee18856df4cc816fdd93b331cee"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_MEP.out",
    "sha256": "13e516e387d0d5f5946ceeb89a080b59abcb1bb9e334b464c4380ab7756bb0ff"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log",
    "sha256": "4856a47f40ed9a0dc7382574c00a584832ffe97858695c04493420020fd7eddc"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/PA_TFPO_minimum_review_20260930.json",
    "sha256": "80aaef355740c5d766a41a5efe3f212818672fd016979af4465d3ebec55082c9"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_probe_protocol_review_20260930.json",
    "sha256": "0cf4a53d0ff56d0eb6d6eaf789f300af7caacb709125782dd88608b78a6b286d"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log",
    "sha256": "da10cbd4c49705269d2e32667ccf997aa27093a00447db69c7e24b6f7a23bcf8"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/Et3B_TFPO_minimum_review_20260930.json",
    "sha256": "da068c1aa70491594ec17847d4dd95e623719821a286120b2d7aa5dc71349684"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_probe_protocol_review_20260930.json",
    "sha256": "0cf4a53d0ff56d0eb6d6eaf789f300af7caacb709125782dd88608b78a6b286d"
  }
]
```

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| PO_O49P46 (angstrom) | 1.828 | 1.8292620003859479 | sameO49 andP46 / separatelynearestH within authenticatedNethylCH2/CH3sets Inherited0.25Å appliesonlytothissamecontactstructuralexistence baseline;actualerrors0.000203–0.003470Å are reported. Do notuse0.25 tocertify smallrelativeaffinity/rateeffects. LargeOPreorganization~0.823Å farlargerthanactualresiduals; no newtolerance chosen.；源定位：mainPDF8Fig6c/d,p10 |
| PO_O49alphaH5 (angstrom) | 2.124 | 2.125092709230588 | sameO49 andP46 / separatelynearestH within authenticatedNethylCH2/CH3sets Inherited0.25Å appliesonlytothissamecontactstructuralexistence baseline;actualerrors0.000203–0.003470Å are reported. Do notuse0.25 tocertify smallrelativeaffinity/rateeffects. LargeOPreorganization~0.823Å farlargerthanactualresiduals; no newtolerance chosen.；源定位：mainPDF8Fig6c/d,p10 |
| PO_O49betaH45 (angstrom) | 2.437 | 2.440469877075724 | sameO49 andP46 / separatelynearestH within authenticatedNethylCH2/CH3sets Inherited0.25Å appliesonlytothissamecontactstructuralexistence baseline;actualerrors0.000203–0.003470Å are reported. Do notuse0.25 tocertify smallrelativeaffinity/rateeffects. LargeOPreorganization~0.823Å farlargerthanactualresiduals; no newtolerance chosen.；源定位：mainPDF8Fig6c/d,p10 |
| PA_O49P46 (angstrom) | 2.651 | 2.6522103098455445 | sameO49 andP46 / separatelynearestH within authenticatedNethylCH2/CH3sets Inherited0.25Å appliesonlytothissamecontactstructuralexistence baseline;actualerrors0.000203–0.003470Å are reported. Do notuse0.25 tocertify smallrelativeaffinity/rateeffects. LargeOPreorganization~0.823Å farlargerthanactualresiduals; no newtolerance chosen.；源定位：mainPDF8Fig6c/d,p10 |
| PA_O49alphaH27 (angstrom) | 2.312 | 2.311797024928443 | sameO49 andP46 / separatelynearestH within authenticatedNethylCH2/CH3sets Inherited0.25Å appliesonlytothissamecontactstructuralexistence baseline;actualerrors0.000203–0.003470Å are reported. Do notuse0.25 tocertify smallrelativeaffinity/rateeffects. LargeOPreorganization~0.823Å farlargerthanactualresiduals; no newtolerance chosen.；源定位：mainPDF8Fig6c/d,p10 |
| PA_O49betaH29 (angstrom) | 2.363 | 2.3632905567333444 | sameO49 andP46 / separatelynearestH within authenticatedNethylCH2/CH3sets Inherited0.25Å appliesonlytothissamecontactstructuralexistence baseline;actualerrors0.000203–0.003470Å are reported. Do notuse0.25 tocertify smallrelativeaffinity/rateeffects. LargeOPreorganization~0.823Å farlargerthanactualresiduals; no newtolerance chosen.；源定位：mainPDF8Fig6c/d,p10 |
| free P46 ADCH (e) | -0.018 | -0.01900749 | FinalnormalizedADCH onsameP46fromfrequencywavefunction InheritedabsoluteP±0.03e rule onsamemethod/model scopedproperty;actualresidual−0.00100749/+0.00005269/+0.00068970e. Normalizationchanges<=1.45e−5e do notchange thelargefree-to-oniumpositivePresult. Tolerance isnot transferred tosourceHlabels orkinetic claims.；源定位：mainPDF8Fig6b-d |
| PO P46 ADCH (e) | 0.447 | 0.44705269 | FinalnormalizedADCH onsameP46fromfrequencywavefunction InheritedabsoluteP±0.03e rule onsamemethod/model scopedproperty;actualresidual−0.00100749/+0.00005269/+0.00068970e. Normalizationchanges<=1.45e−5e do notchange thelargefree-to-oniumpositivePresult. Tolerance isnot transferred tosourceHlabels orkinetic claims.；源定位：mainPDF8Fig6b-d |
| PA P46 ADCH (e) | 0.455 | 0.4556897 | FinalnormalizedADCH onsameP46fromfrequencywavefunction InheritedabsoluteP±0.03e rule onsamemethod/model scopedproperty;actualresidual−0.00100749/+0.00005269/+0.00068970e. Normalizationchanges<=1.45e−5e do notchange thelargefree-to-oniumpositivePresult. Tolerance isnot transferred tosourceHlabels orkinetic claims.；源定位：mainPDF8Fig6b-d |
| source selectedH labels | {"PAalpha":0.092,"PAbeta":0.111} | 未给出／不适用 | Unmapped figure-selectedH differsfrom nearestcontactH andfamilymean Excludedfromexactnumericclaim, not silentlymatched. V2requiresdistinction, notauthenticationofhiddenlabelsonallfigures. Full30mappedHindividualvaluesandcontactvaluesareavailable.；源定位：mainPDF8/10 |

原始最后坐标重算PO→PA O49–P46=1.8292620→2.6522103 Å，对1.828→2.651。原生ADCH P=-0.01900749/0.44705269/0.45568970e，对-0.018/0.447/0.455。132/162/177正模。

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Chemically defined source components and derived models

冻结要求：Preserve source reagent identities and explicitly define any adduct/chain-end graph, charge/spin and composition. Constructed oligomers must be labeled models. Reference comparisons must conserve inventories or account for reservoirs and coproducts. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists. Source-coordinate limitation: SI physical pp39-40 lists 51 atoms (C14H30N3O3P) for the PA adduct; the complete stoichiometric (Et2N)3P + PA model has 61 atoms (C20H34N3O3P), a C6H4 difference. The complete PA reagent connectivity in systems.json remains valid. Reconstruction must identify retained source atoms, added atoms and the resulting graph; a reconstructed model is not an unchanged source geometry. No missing coordinates are supplied or invented here.

当前复审：身份/重建映射、正曲率、O/P/H接触、原始ADCH/有符号ESP、TFPO对照构成有效局部分子解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainPDF8 Fig6,SI35–40;SI4–5",
    "actual_result": "free/PO/PA=46/56/61 atoms,q0singlet,132/162/177 positive modes;sourcePA51atoms missingC6H4 explicitly reconstructed. O49/P46 retained; alpha/beta=N-CH2/CH3.",
    "reason": "Currentrubric explicitlyallows declared reconstruction. Composition/graph verified; the incomplete51atom historical model isnot reused; exactsourcecoordinates not claimed.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_native.log",
        "sha256": "b41cff05390e6a2d83e02078e96368cb8a822a3c4820c84395223391881a43fa"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_native.log",
        "sha256": "ad358229b1eef687bc782b70557c5f0236bf03ec84b38f559db7fb09cb7992c6"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_native.log",
        "sha256": "97736ab5df99445f9b5d7f2f2e47495419921cedda620ee938bf91572347f228"
      },
      {
        "path": "docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/provenance/complete_pa_closure_20260915.json",
        "sha256": "74edd933842fc4b2168a511bb3a328ffcb8327da3824e767bd942cfa84671fd0"
      }
    ]
  }
]
```


证据记录：`E0006`。

```json
[
  {
    "actual_result": "free/PO/PA=46/56/61 atoms,q0singlet,132/162/177 positive modes;sourcePA51atoms missingC6H4 explicitly reconstructed. O49/P46 retained; alpha/beta=N-CH2/CH3."
  }
]
```

### kp_interactions — Auditable quantitative local interaction evidence

冻结要求：Generate results that address how PA addition changes relevant molecular interactions. Distances, populations, binding thermodynamics and reactivity metrics support different claims; their interpretation must match their definition. No mandatory PA/no-PA chain or named pathway matrix. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists. For main physical p8 Figure 6 and p10, distinguish a specified H-site ADCH population, the nearest-contact H and a declared alpha/beta-H family statistic. Define sites from the N-ethyl CH2/CH3 graph and map them explicitly; do not equate a figure-labelled H with a nearest site or family mean without evidence. Report signed electrostatic potential with its units and surface definition separately from electron density; source colour/prose alone is not a density measurement. These local observables do not by themselves establish polymer propagation or backbiting rates.

当前复审：身份/重建映射、正曲率、O/P/H接触、原始ADCH/有符号ESP、TFPO对照构成有效局部分子解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainPDF8Fig6b–d,p10;SI4–5",
    "actual_result": "FinalP_ADCH=−0.01900749/0.44705269/0.45568970e. PO O-P/Halpha/Hbeta=1.829262/2.125093/2.440470Å;PA=2.652210/2.311797/2.363291Å. Full30NethylH tables,finalnormalizedcharges andsignedESP preserved.",
    "reason": "Sameobject/method/observable olddistance andabsoluteP tolerances inherited only for matchingclaimed scope. MappedindividualH,nearestcontactH andsourceunmappedlabels explicitly separated; no hiddenlabels inferred from closeness.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W07/papers/paper_ef26687d63a37e29/cases/final_adch_baseline_reparse_20261007/run/results.json",
        "sha256": "cd9d7977b91e1d05f1aaa9a3ce57775b1fb47681aae240a61964bf3aa2de06af"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_native.log",
        "sha256": "ad358229b1eef687bc782b70557c5f0236bf03ec84b38f559db7fb09cb7992c6"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_ADCH.out",
        "sha256": "26e89078fb21994a8ee64e70300cdc78caa5c9861ab9f97c4210099b4ffa5e08"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_postprocessing_audit.json",
        "sha256": "7f50a845f255580b34ac2a3721be19fffe835db47440a9b71d198a102ae07f7a"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_native.log",
        "sha256": "97736ab5df99445f9b5d7f2f2e47495419921cedda620ee938bf91572347f228"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_ADCH.out",
        "sha256": "fa5888a0300aaa919419b865a159d63855ee07b67cd858652474c83f67662a05"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_postprocessing_audit.json",
        "sha256": "6fcb0a083ed5d841409a1e725f257390948a9fb839e448daab4c907fe06ad3ba"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/surface_export_correction_20260930.json",
        "sha256": "a21c8362fce82f758a0708dfc65696477afb173d0d1b77b1e2a5f5673fab34d7"
      }
    ]
  }
]
```


证据记录：`E0006`。

```json
[
  {
    "actual_result": "FinalP_ADCH=−0.01900749/0.44705269/0.45568970e. PO O-P/Halpha/Hbeta=1.829262/2.125093/2.440470Å;PA=2.652210/2.311797/2.363291Å. Full30NethylH tables,finalnormalizedcharges andsignedESP preserved."
  }
]
```

### kp_mechanistic — Connection from interaction to chemical role

冻结要求：Assess whether evidence establishes activation, association or a kinetic effect. A contact or more positiveP charge alone does not prove faster propagation or suppressed backbiting. If a reaction barrier is claimed, establish the corresponding physical path; alternative bounded interaction arguments remain eligible. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：身份/重建映射、正曲率、O/P/H接触、原始ADCH/有符号ESP、TFPO对照构成有效局部分子解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainPDF7–10,SI4/S10–S12",
    "actual_result": "PA/TFPO intact71atom complex207positive modes,O65-H12=2.44765Å;Et3B/TFPO32atom90positive modes,B3-O26=2.29784Å. ExperimentalTFPO19F−75.24→−75.19(PA)/−75.16(Et3B);methylene1H2.20→2.25/2.39ppm. NaOEt perturbszwitterionH2.98→3.00/0.99→1.00.",
    "reason": "Thisestablishescontactfeasibility andexperimentalinteractionconsistency. The taskasks what theycanestablish; boundedassociation evidence with explicitlackofkineticcausality answers that question. NeithernewbindingG norbackbitingbarrier isclaimed.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log",
        "sha256": "4856a47f40ed9a0dc7382574c00a584832ffe97858695c04493420020fd7eddc"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log",
        "sha256": "da10cbd4c49705269d2e32667ccf997aa27093a00447db69c7e24b6f7a23bcf8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_probe_protocol_review_20260930.json",
        "sha256": "0cf4a53d0ff56d0eb6d6eaf789f300af7caacb709125782dd88608b78a6b286d"
      }
    ]
  }
]
```


证据记录：`E0006`。

```json
[
  {
    "actual_result": "PA/TFPO intact71atom complex207positive modes,O65-H12=2.44765Å;Et3B/TFPO32atom90positive modes,B3-O26=2.29784Å. ExperimentalTFPO19F−75.24→−75.19(PA)/−75.16(Et3B);methylene1H2.20→2.25/2.39ppm. NaOEt perturbszwitterionH2.98→3.00/0.99→1.00."
  }
]
```

### kp_sensitivity — Conformation, composition and concentration limits

冻结要求：Address model uncertainties capable of changing the conclusion with actual evidence. Association comparisons must use consistent standard states and concentration/solvent assumptions. No forced10-fold dilution or fixedEt3B count per molecular cluster. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：身份/重建映射、正曲率、O/P/H接触、原始ADCH/有符号ESP、TFPO对照构成有效局部分子解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "SI4–5,mainPDF8/10;sourcepreparation",
    "actual_result": "SourcegasDFT andverifierSMDbenzeneTFPO contacts distinguished;observedC6D6/CDCl3+THF conditions notequated withneat80Cpolymerisation. IndividualHdistributions retained;PAreconstruction/figureleader ambiguity documented. BothcompletedTFPOOpt tables passedTight;postFreqsoftdisplacementcaveats recorded.",
    "reason": "Completedsourcebaseline +actualsolvatedprobe calculations are distinctevidence, notan ensembleorcontrolledbindingaffinity sensitivity claim. No universalconformation/concentration claim ismade; uncertainties are bounded to theobservablesactuallyused.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/PA_TFPO_minimum_review_20260930.json",
        "sha256": "80aaef355740c5d766a41a5efe3f212818672fd016979af4465d3ebec55082c9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/Et3B_TFPO_minimum_review_20260930.json",
        "sha256": "da068c1aa70491594ec17847d4dd95e623719821a286120b2d7aa5dc71349684"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/selected_H_registration_review_20260930.json",
        "sha256": "9d437411f3d66668c9e93235f720d5a26dfa73170126d4382e25acd65df0382a"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_probe_protocol_review_20260930.json",
        "sha256": "0cf4a53d0ff56d0eb6d6eaf789f300af7caacb709125782dd88608b78a6b286d"
      }
    ]
  }
]
```


证据记录：`E0006`。

```json
[
  {
    "actual_result": "SourcegasDFT andverifierSMDbenzeneTFPO contacts distinguished;observedC6D6/CDCl3+THF conditions notequated withneat80Cpolymerisation. IndividualHdistributions retained;PAreconstruction/figureleader ambiguity documented. BothcompletedTFPOOpt tables passedTight;postFreqsoftdisplacementcaveats recorded."
  }
]
```

### kp_scope — Local versus polymer-scale evidence

冻结要求：Relate local findings to source probe observations with explicit representativeness limits. Support, correction and well-investigated unresolved conclusions are eligible. No direct prediction of bulk molecular weight, productivity or antidilution performance from a short isolated model. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：身份/重建映射、正曲率、O/P/H接触、原始ADCH/有符号ESP、TFPO对照构成有效局部分子解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainPDF5,7–10;SI4/S10–S12",
    "actual_result": "The supportedresult islocalstructural/electrostaticchange andfeasibleoxygen-probecontacts. NeitherpolymerMw/productivity,dilutionlaw norwholepropagationnetwork follows;sourceNMRisobserved evidence,notcomputedshift.",
    "reason": "V2 explicitly excludesbulkMw/productivity/fullnetwork. Failedfree55 andmissingkineticroutes remainunusedratherthan relabeledcompleted/nonexistent. The molecularanswer addresses both epoxide andchainend role without claimingrates.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_probe_protocol_review_20260930.json",
        "sha256": "0cf4a53d0ff56d0eb6d6eaf789f300af7caacb709125782dd88608b78a6b286d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/surface_export_correction_20260930.json",
        "sha256": "a21c8362fce82f758a0708dfc65696477afb173d0d1b77b1e2a5f5673fab34d7"
      }
    ]
  }
]
```


证据记录：`E0006`。

```json
[
  {
    "actual_result": "The supportedresult islocalstructural/electrostaticchange andfeasibleoxygen-probecontacts. NeitherpolymerMw/productivity,dilutionlaw norwholepropagationnetwork follows;sourceNMRisobserved evidence,notcomputedshift."
  }
]
```

### conclusion_investigation — How does adding phthalic anhydride change the local molecular interactions in the (Et2N)3P/Et3B system, and what can those changes establish about epoxide activation and chain-end stabilization during CO2/propylene-oxide copolymerization?

冻结要求：Answer the bounded question with claims proportional to the evidence. Support, correction, refutation and demonstrated unresolved conclusions are equally eligible. Partial/failure status preserves real work but does not confer completion credit. No required author winner or named control list. Assess completion against the original public scientific question, not a self-narrowed addressed_scope. Missing necessary investigation, a failed calculation, copied public source values or a statement of source ambiguity earns no credit for the missing work and cannot yield whole-task full credit. Preserve credit for independently valid completed parts and accept sufficiently supported non-author conclusions without a fixed route or extra method matrix.

当前复审：身份/重建映射、正曲率、O/P/H接触、原始ADCH/有符号ESP、TFPO对照构成有效局部分子解释。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "currentAR/PRquestion;mainFig6,SI4–5/S10–S12",
    "actual_result": "PA与(Et2N)3P形成完整磷鎓/羧酸盐局部模型后，P中心由近中性转为明显正电，负势集中到含氧末端，且相对于PO加合物，指定O49–P46距离由1.8293增至2.6522Å，O49与N-ethyl CH2/CH3氢保持约2.31/2.36Å近接。这说明PA改变了局部配位方式及静电分布，支持磷鎓区域参与环氧/含氧链端相互作用的分子解释。独立TFPO配对最低点和原文31P/19F/1H观测与这一解释相容；Et3B对TFPO的实验位移更大，支持它保留Lewis酸活化角色。该证据能建立局部结构、极化和关联相容性，不能单凭电荷/接触推出更低开环势垒、链端结合自由能或回咬速率，也不能推出体相抗稀释规律。未收敛free55没有进入这些正面结论。",
    "reason": "The entirecurrentlocal-question account is supported byreused originalthree-minimumcharge/ESP chain, upgradedprobecontacts, andsourceexperimentlimits. No legacy oligomermatrix isreinstated. Candidate isnot formalPASS.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W07/papers/paper_ef26687d63a37e29/cases/final_adch_baseline_reparse_20261007/run/results.json",
        "sha256": "cd9d7977b91e1d05f1aaa9a3ce57775b1fb47681aae240a61964bf3aa2de06af"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/PA_TFPO_minimum_review_20260930.json",
        "sha256": "80aaef355740c5d766a41a5efe3f212818672fd016979af4465d3ebec55082c9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/Et3B_TFPO_minimum_review_20260930.json",
        "sha256": "da068c1aa70491594ec17847d4dd95e623719821a286120b2d7aa5dc71349684"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_probe_protocol_review_20260930.json",
        "sha256": "0cf4a53d0ff56d0eb6d6eaf789f300af7caacb709125782dd88608b78a6b286d"
      }
    ]
  }
]
```


证据记录：`E0006`。

```json
[
  {
    "actual_result": "PA与(Et2N)3P形成完整磷鎓/羧酸盐局部模型后，P中心由近中性转为明显正电，负势集中到含氧末端，且相对于PO加合物，指定O49–P46距离由1.8293增至2.6522Å，O49与N-ethyl CH2/CH3氢保持约2.31/2.36Å近接。这说明PA改变了局部配位方式及静电分布，支持磷鎓区域参与环氧/含氧链端相互作用的分子解释。独立TFPO配对最低点和原文31P/19F/1H观测与这一解释相容；Et3B对TFPO的实验位移更大，支持它保留Lewis酸活化角色。该证据能建立局部结构、极化和关联相容性，不能单凭电荷/接触推出更低开环势垒、链端结合自由能或回咬速率，也不能推出体相抗稀释规律。未收敛free55没有进入这些正面结论。"
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 2.87 小时；5 份计时日志/10 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 20 线程/进程；Gaussian %Mem=100GB,16GB,80GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0010 · v2_execution_20260929/data/free_native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_native.log) | Gaussian:390.2；Gaussian:157.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0011 · v2_execution_20260929/data/PO_native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_native.log) | Gaussian:1568；Gaussian:298.2 | 正常；正常 | {"threads":[20],"Gaussian_mem":["100GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0012 · v2_execution_20260929/data/PA_native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_native.log) | Gaussian:1268.1；Gaussian:602 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0015 · v2_execution_20260929/data/PO_ADCH.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_ADCH.out) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0017 · v2_execution_20260929/data/PA_ADCH.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_ADCH.out) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0020 · PA61_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log) | Gaussian:4605.4；Gaussian:953.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0021 · Et3B_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log) | Gaussian:405.1；Gaussian:74.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["16GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0055 · v2_execution_20260929/data/free_ADCH.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_ADCH.out) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0056 · v2_execution_20260929/data/free_MEP.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_MEP.out) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0057 · v2_execution_20260929/data/PO_MEP.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_MEP.out) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0058 · v2_execution_20260929/data/PA_MEP.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_MEP.out) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0066 · Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/multwfn_adch_mep/multiwfn_mep.out](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/multwfn_adch_mep/multiwfn_mep.out) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0068 · artifacts/pa_complete_adch_mep_20260915/mep_complete_stackfix.out](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/mep_complete_stackfix.out) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0104 · Et2N3P_si_recovered_v2_hpc_685c4cb0/multwfn_adch_mep/multiwfn_mep.out](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/multwfn_adch_mep/multiwfn_mep.out) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

源特定H标签、最近接触H及家族平均不能混用；不是全聚合循环、链端反应自由能或回咬速率验证。

未绑定源图任意选中H标签不算精确复现；30个实际H映射数据保留。不要求全聚合循环、链端自由能或回咬势垒；失败free55未使用。


原独立审查的 `source_exceptions_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "The source 51-atom PA listing is incomplete; the accepted model is a declared 61-atom reconstruction, not unchanged source coordinates.",
  "Unmapped figure H labels are not assigned by numerical proximity. Full normalized ADCH site data and nearest contacts remain distinct.",
  "No propagation/backbiting rate, actual chain-end binding free energy, NMR chemical-shift calculation, polymer productivity or dilution law is certified.",
  "The failed free55 and retired oligomer/NaOEt matrix are not counted as successful computations."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_ef26687d63a37e29.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_ef26687d63a37e29/verified_computation_reference.md)；SHA-256 `5ecbe5db4a416b2d1b40263e31f14648ca1f79e7c2eecf6615796b4017239382`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_ef26687d63a37e29.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_ef26687d63a37e29.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_ef26687d63a37e29.json) | `ec4233d1392227518a81b6b751c3c0b751e81b20d8a35e1d3b82b0c59b0754a8` | evidence_or_analysis |
| E0002 | [tasks/v2_autonomous_research/paper_ef26687d63a37e29/agent_input/task.md](../../../v2_autonomous_research/paper_ef26687d63a37e29/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0002_task.md) | `565160bf2ca946b8222f64d7ac109000e0143b61e27db762b76799f726f0017a` | historical_task_binding |
| E0003 | [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0003_task.md) | `1bfdeb9b2f46133daf7807be3a39de3d8cb3d3d40e587d53e4c8b54d985828a4` | historical_task_binding |
| E0004 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_PRIMARY_SOURCE_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_PRIMARY_SOURCE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_ROOT_PRIMARY_SOURCE_READBACK.json) | `a131458d308b52199eb86e1c6e7fc3efefd0cc69c93f52a2a5001ed2c3df60d0` | evidence_or_analysis |
| E0005 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_NATIVE_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/ROOT_NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_ROOT_NATIVE_READBACK.json) | `9f8ce2f290d610c66701f38fed799081fc653cd1cec06332a98de64ed1a3ea31` | evidence_or_analysis |
| E0006 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_ef26687d63a37e29/COMPUTATION_STAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_ef26687d63a37e29/COMPUTATION_STAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_COMPUTATION_STAGE.json) | `7639221f3a673445f1bb3f1daeff3b0a307a23230acff54632fd4b851bcc4bf4` | evidence_or_analysis |
| E0007 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_ef26687d63a37e29.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_ef26687d63a37e29.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_paper_ef26687d63a37e29.md) | `e072e875454e4a6b8df5e005737755c3f6a0b61897d0fe022886c9ed21cf0480` | evidence_or_analysis |
| E0008 | [docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `f1b38baa37d7c3cebc2e4ed094756c11b2caa0dfd8cea1f9bf45407bf99bc70b` | historical_task_binding |
| E0009 | [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot) | `f1b38baa37d7c3cebc2e4ed094756c11b2caa0dfd8cea1f9bf45407bf99bc70b` | historical_task_binding |
| E0010 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_native_excerpt.json) | `b41cff05390e6a2d83e02078e96368cb8a822a3c4820c84395223391881a43fa` | native_output |
| E0011 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_native_excerpt.json) | `ad358229b1eef687bc782b70557c5f0236bf03ec84b38f559db7fb09cb7992c6` | native_output |
| E0012 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_native.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_native.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_native_excerpt.json) | `97736ab5df99445f9b5d7f2f2e47495419921cedda620ee938bf91572347f228` | native_output |
| E0013 | [docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/provenance/complete_pa_closure_20260915.json](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/provenance/complete_pa_closure_20260915.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_complete_pa_closure_20260915.json) | `74edd933842fc4b2168a511bb3a328ffcb8327da3824e767bd942cfa84671fd0` | evidence_or_analysis |
| E0014 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W07/papers/paper_ef26687d63a37e29/cases/final_adch_baseline_reparse_20261007/run/results.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W07/papers/paper_ef26687d63a37e29/cases/final_adch_baseline_reparse_20261007/run/results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_results.json) | `cd9d7977b91e1d05f1aaa9a3ce57775b1fb47681aae240a61964bf3aa2de06af` | evidence_or_analysis |
| E0015 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_ADCH.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_ADCH.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_native_excerpt.json) | `26e89078fb21994a8ee64e70300cdc78caa5c9861ab9f97c4210099b4ffa5e08` | native_output |
| E0016 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_postprocessing_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_postprocessing_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_PO_postprocessing_audit.json) | `7f50a845f255580b34ac2a3721be19fffe835db47440a9b71d198a102ae07f7a` | evidence_or_analysis |
| E0017 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_ADCH.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_ADCH.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_native_excerpt.json) | `fa5888a0300aaa919419b865a159d63855ee07b67cd858652474c83f67662a05` | native_output |
| E0018 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_postprocessing_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_postprocessing_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_PA_postprocessing_audit.json) | `6fcb0a083ed5d841409a1e725f257390948a9fb839e448daab4c907fe06ad3ba` | evidence_or_analysis |
| E0019 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/surface_export_correction_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/surface_export_correction_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_surface_export_correction_20260930.json) | `a21c8362fce82f758a0708dfc65696477afb173d0d1b77b1e2a5f5673fab34d7` | evidence_or_analysis |
| E0020 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0020_native_excerpt.json) | `4856a47f40ed9a0dc7382574c00a584832ffe97858695c04493420020fd7eddc` | native_output |
| E0021 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_native_excerpt.json) | `da10cbd4c49705269d2e32667ccf997aa27093a00447db69c7e24b6f7a23bcf8` | native_output |
| E0022 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_probe_protocol_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_probe_protocol_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_source_probe_protocol_review_20260930.json) | `0cf4a53d0ff56d0eb6d6eaf789f300af7caacb709125782dd88608b78a6b286d` | evidence_or_analysis |
| E0023 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/PA_TFPO_minimum_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/PA_TFPO_minimum_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_PA_TFPO_minimum_review_20260930.json) | `80aaef355740c5d766a41a5efe3f212818672fd016979af4465d3ebec55082c9` | evidence_or_analysis |
| E0024 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/Et3B_TFPO_minimum_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/Et3B_TFPO_minimum_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0024_Et3B_TFPO_minimum_review_20260930.json) | `da068c1aa70491594ec17847d4dd95e623719821a286120b2d7aa5dc71349684` | evidence_or_analysis |
| E0025 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/selected_H_registration_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/selected_H_registration_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0025_selected_H_registration_review_20260930.json) | `9d437411f3d66668c9e93235f720d5a26dfa73170126d4382e25acd65df0382a` | evidence_or_analysis |
| E0026 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_ef26687d63a37e29/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_ef26687d63a37e29/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0026_task.md) | `565160bf2ca946b8222f64d7ac109000e0143b61e27db762b76799f726f0017a` | historical_task_binding |
| E0027 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_ef26687d63a37e29/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_ef26687d63a37e29/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0027_reference_key_points.json) | `ec5f8dcf6695d9b79a185aea103e413249cbd3c886e673216e245a7a6bb48e2b` | historical_task_binding |
| E0028 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_ef26687d63a37e29/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_ef26687d63a37e29/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_reference_conclusions.json) | `8690f379736c61eed95c31f11f16864d0cef15f106761d2f213d5a9d0ba8540b` | historical_task_binding |
| E0029 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_ef26687d63a37e29/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_ef26687d63a37e29/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_scoring_rules.json) | `6aedff4647615acab73abc8adb324706d044b9d4161191fe3c2f2d1a506e3799` | historical_task_binding |
| E0030 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_ef26687d63a37e29/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_ef26687d63a37e29/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_task.md) | `1bfdeb9b2f46133daf7807be3a39de3d8cb3d3d40e587d53e4c8b54d985828a4` | historical_task_binding |
| E0031 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_ef26687d63a37e29/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_ef26687d63a37e29/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_reference_key_points.json) | `ec5f8dcf6695d9b79a185aea103e413249cbd3c886e673216e245a7a6bb48e2b` | historical_task_binding |
| E0032 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_ef26687d63a37e29/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_ef26687d63a37e29/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_reference_conclusions.json) | `8690f379736c61eed95c31f11f16864d0cef15f106761d2f213d5a9d0ba8540b` | historical_task_binding |
| E0033 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_ef26687d63a37e29/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_ef26687d63a37e29/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_scoring_rules.json) | `6aedff4647615acab73abc8adb324706d044b9d4161191fe3c2f2d1a506e3799` | historical_task_binding |
| E0034 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/84ccec20fe32100d_W07.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/84ccec20fe32100d_W07.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_84ccec20fe32100d_W07.json) | `84ccec20fe32100d7e4d43b71de3a048e63a1930cf0e3615ae86b2d634623dc1` | evidence_or_analysis |
| E0035 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/W07.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/W07.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_W07.json) | `84ccec20fe32100d7e4d43b71de3a048e63a1930cf0e3615ae86b2d634623dc1` | evidence_or_analysis |
| E0036 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/83fecf90740bcb43_paper_ef26687d63a37e29_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/83fecf90740bcb43_paper_ef26687d63a37e29_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_83fecf90740bcb43_paper_ef26687d63a37e29_delivery_integrity.json) | `83fecf90740bcb43f10786dd2606b7dfdd0c18fa4008d05607cd9cb41f4a0b79` | evidence_or_analysis |
| E0037 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_ef26687d63a37e29_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_ef26687d63a37e29_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_paper_ef26687d63a37e29_delivery_integrity.json) | `83fecf90740bcb43f10786dd2606b7dfdd0c18fa4008d05607cd9cb41f4a0b79` | evidence_or_analysis |
| E0038 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/b1f558e594e06f81_paper_ef26687d63a37e29_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/b1f558e594e06f81_paper_ef26687d63a37e29_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_b1f558e594e06f81_paper_ef26687d63a37e29_primary_pages.json) | `b1f558e594e06f81816e64a10e6ca89c2ae371fe1f16cd3cd7075b1ec41ecae6` | evidence_or_analysis |
| E0039 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_ef26687d63a37e29_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_ef26687d63a37e29_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_paper_ef26687d63a37e29_primary_pages.json) | `b1f558e594e06f81816e64a10e6ca89c2ae371fe1f16cd3cd7075b1ec41ecae6` | evidence_or_analysis |
| E0040 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/e0e31b241c1751f6_G4_PA_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/e0e31b241c1751f6_G4_PA_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0040_e0e31b241c1751f6_G4_PA_native_readback.json) | `e0e31b241c1751f622de318b4d83c8e8ec43abe8f39b5b8aaeb6013bb664450b` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/G4_PA_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/G4_PA_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0041_G4_PA_native_readback.json) | `e0e31b241c1751f622de318b4d83c8e8ec43abe8f39b5b8aaeb6013bb664450b` | evidence_or_analysis |
| E0046 | [papers/paper_ef26687d63a37e29/documents/main.pdf](../../../../papers/paper_ef26687d63a37e29/documents/main.pdf) | `bf0ec692ef2eec7d4342ed722884bcabb2137396dcb3fc6c6a867eed7f62b0b8` | source_document |
| E0047 | [papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf](../../../../papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf) | `bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96` | source_document |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_postprocessing_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_postprocessing_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0054_free_postprocessing_audit.json) | `907cd8bf3f028fba3f06f08a9d0bbaa71705848a73fc396ef6a116289b88eff3` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_ADCH.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_ADCH.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_native_excerpt.json) | `9d8070dc7af5daa9b4a8c994b908edbfba262bd8eafd7285bdd577d0ed2e7941` | native_output |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_MEP.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_MEP.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0056_native_excerpt.json) | `600cc0ad76dfac5e19329ea135352a70cea102d9d5d072099bc0c2249cb1a82f` | native_output |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_MEP.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_MEP.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0057_native_excerpt.json) | `73972ebf93bc54d3fffc0ff9384fb804e0ba6ee18856df4cc816fdd93b331cee` | native_output |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_MEP.out](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_MEP.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_native_excerpt.json) | `13e516e387d0d5f5946ceeb89a080b59abcb1bb9e334b464c4380ab7756bb0ff` | native_output |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_reconstructed_initial.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_reconstructed_initial.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_PA_reconstructed_initial.xyz) | `764b9c5281596b5e11f076eb7d37f8eb84da7f02ed90fc9a26a1d7a603d0b41f` | input_or_analysis_code |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_reconstruction_code.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_reconstruction_code.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_PA_reconstruction_code.py) | `bad809c5047cb32e06848d7ede01649362439a9c5836938c7bec583baf27c794` | input_or_analysis_code |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_PA_input.com) | `d177e03702eabdaa40f19e962407d3b4e0b39bb8924c1a126c7074d5b1643be4` | input_or_analysis_code |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_free_input.com) | `493924911aa605f375dda46ffa1735a571834528c44674543777b0639c6ff09f` | input_or_analysis_code |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_PO_input.com) | `c7a500d17ebfeed4bad1e9599df38aeef8b89f6b31b35dc90e2710820db494ee` | input_or_analysis_code |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/reuse_postprocessing_review.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/reuse_postprocessing_review.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_reuse_postprocessing_review.py) | `e5b6076b9dc8ae0da96ea2de1e0aa475ab5feab9618dd778c58e1b656749d280` | input_or_analysis_code |
| E0065 | [docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/multwfn_adch_mep/vtx.pdb](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/multwfn_adch_mep/vtx.pdb) | `0f0635dafd237e8f0c620f08d22c39b5a974fd28b57dd46b4c12dc3f9d1f2deb` | evidence_or_analysis |
| E0066 | [docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/multwfn_adch_mep/multiwfn_mep.out](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_PO_si_recovered_v2_hpc_6e9ad747/multwfn_adch_mep/multiwfn_mep.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_native_excerpt.json) | `73972ebf93bc54d3fffc0ff9384fb804e0ba6ee18856df4cc816fdd93b331cee` | native_output |
| E0067 | [docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/vtx.pdb](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/vtx.pdb) | `a3a4c86b60b3b01d5a681a6d4d5c4fc3f21ca3efa76615cfaece2e32b0dde7a5` | evidence_or_analysis |
| E0068 | [docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/mep_complete_stackfix.out](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/pa_complete_adch_mep_20260915/mep_complete_stackfix.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_native_excerpt.json) | `13e516e387d0d5f5946ceeb89a080b59abcb1bb9e334b464c4380ab7756bb0ff` | native_output |
| E0069 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/review_history/before_surface_correction_20260930/report/results.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/review_history/before_surface_correction_20260930/report/results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0069_results.json) | `5300ecc0a898947265f88d3eb9a5923d24b336026dc05a4047270482a1ad1dc7` | evidence_or_analysis |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/review_history/before_surface_correction_20260930/report/report.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/review_history/before_surface_correction_20260930/report/report.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_report.md) | `fb4e06df85edd77893864a9c9bd94d7e612813ecfd4dee33c0091afedfcb5993` | evidence_or_analysis |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/contract_snapshot/20260930_final_repair/binding.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/contract_snapshot/20260930_final_repair/binding.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_binding.json) | `76dcb9a1a868fb5072c658a71cbf3ed08e6afccd05ad7a9b8bffa56e363759c6` | evidence_or_analysis |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_signed_ESP_vertices.pdb](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/free_signed_ESP_vertices.pdb) | `c7982606bf18edc1558817e0bb877fa4b9b7d7025c9f9c7b232c4696fc58a41b` | evidence_or_analysis |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_signed_ESP_vertices.pdb](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_signed_ESP_vertices.pdb) | `0f0635dafd237e8f0c620f08d22c39b5a974fd28b57dd46b4c12dc3f9d1f2deb` | evidence_or_analysis |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_signed_ESP_vertices.pdb](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_signed_ESP_vertices.pdb) | `a3a4c86b60b3b01d5a681a6d4d5c4fc3f21ca3efa76615cfaece2e32b0dde7a5` | evidence_or_analysis |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | input_or_analysis_code |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0076_input.com) | `017be705c493ccc45ae164c116fe7fe4e19933c3efe77881f8506ccd3183aaf5` | input_or_analysis_code |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0077_run.sh) | `13b538a8bb442d88cae306783c6eb4a138966203c9265165e5c2bd6aab3b0be2` | input_or_analysis_code |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0078_input.com) | `606efb0212f4282da4cfcaa029cc072215375e77f2cde89a309d88e133035647` | input_or_analysis_code |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/main.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/main.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0079_main.txt) | `3a7e92ae3a4f0f26416874552a08ad119a78255b9a88633835e227deaf5678e4` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/supplementary_001.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/supplementary_001.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0080_supplementary_001.txt) | `dd99304d9634ebc7fab12720a5474e0cac2f078ebbcc2f9bf24bb7403babea7e` | evidence_or_analysis |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_readback_20260930/main_physical8.png](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_readback_20260930/main_physical8.png) | `a55218c78ebb351f1f4e4dcbede808153dc5255f8f599de1d9891783a9d50c50` | evidence_or_analysis |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_readback_20260930/supplementary_001_physical11.png](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_readback_20260930/supplementary_001_physical11.png) | `179fd3670323cf26c8a7501df90d6c3d8dc67246f423db3aad17b99b357d06c7` | evidence_or_analysis |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_readback_20260930/supplementary_001_physical12.png](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_readback_20260930/supplementary_001_physical12.png) | `33500fd95099219d819802752c7c9c112c180fa2f2fbc6b7234ca490efc4eafb` | evidence_or_analysis |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0084_submission.json) | `ce387a33bd097f5fa6e51d407878bf08ee85c04461b9246b7d643ec86ec6bc59` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0085_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/PA61_TFPO_C6D6proxy_contact_pilot/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0086_status.json) | `46b039f72d5bbb171f285b06472b28d439cca656a70595da0b79bd2c91aa435b` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/v2_completion_execution_20260930T1255Z/NATIVE_JOB_READBACK_1841UTC.json](../../../../docs/v2_verification/history/v2_completion_execution_20260930T1255Z/NATIVE_JOB_READBACK_1841UTC.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0087_NATIVE_JOB_READBACK_1841UTC.json) | `277fe7ed07144d68d4d895f8a005b1c9745f7e9a8d26ad7a616f472d40a079aa` | evidence_or_analysis |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_TFPO_preparation_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_TFPO_preparation_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0088_source_TFPO_preparation_20260930.json) | `08cd3689f1a513c60c48ea3d171222461d441e43fcce64e8e3db2f8f493e5fcc` | evidence_or_analysis |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0089_submission.json) | `fe8a3a68083a03c13c6cd88e1f21016d63a048df8c1d7767c45ae8b3ba7f08ba` | evidence_or_analysis |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/job.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/job.chk) | `02d8f93e596aa43bedcdfc156c388c583724712b6da69f28d6ae679e0a356925` | evidence_or_analysis |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0091_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/outputs/Et3B_TFPO_C6D6proxy_contact_pilot/a01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0092_status.json) | `89ffe49c961296e2a18a68aa4f9bc36eef188921aff8957e9442068887557c6a` | evidence_or_analysis |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/Et3B_TFPO_pilot_launch_review_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/Et3B_TFPO_pilot_launch_review_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0093_Et3B_TFPO_pilot_launch_review_20260930.json) | `9f5ba4f3710b30eba95f7026913f7f501a28e404e21b693675219d8d01d7327e` | evidence_or_analysis |
| E0094 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_readback_20260930/Figure6bcd_highres.png](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_readback_20260930/Figure6bcd_highres.png) | `1a054bbed976b50f5cb8d70ec9fae85b7d4465ca711fad9b1018790dc3a311d8` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_identity_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PO_identity_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0095_PO_identity_audit.json) | `bd638ad88e10a2b4463ef8793036dc223dfd0c95d293767ca46bef65b896b3cb` | evidence_or_analysis |
| E0096 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_identity_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/PA_identity_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0096_PA_identity_audit.json) | `c8d96297257e519bf501f99d58aa26723ee321185a4c68af89c2f72bbfbb041d` | evidence_or_analysis |
| E0097 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_observable_comparison.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/data/source_observable_comparison.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0097_source_observable_comparison.json) | `cf9ad00510ed02171d49c5c0bf454541b1f5dffda47e9bcbfb951055c9bb7b42` | evidence_or_analysis |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_readback_20260930/Figure6d_atoms_highres.png](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/v2_execution_20260929/source_readback_20260930/Figure6d_atoms_highres.png) | `1e296cfc1fac9b34b63a9a62bfadaece8551317a1f22d15a9728b24f1139ef12` | evidence_or_analysis |
| E0099 | [tasks/final_verified_paper_reproduction/paper_ef26687d63a37e29/evaluation/verified_computation_reference.md](../../../final_verified_paper_reproduction/paper_ef26687d63a37e29/evaluation/verified_computation_reference.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0099_verified_computation_reference.md) | `f1b38baa37d7c3cebc2e4ed094756c11b2caa0dfd8cea1f9bf45407bf99bc70b` | historical_task_binding |
| E0100 | [tasks/final_verified_paper_reproduction/paper_ef26687d63a37e29/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_ef26687d63a37e29/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0100_scoring_rules.json) | `4135663765eb851994d83031e0e3e28f96294b8c855f892f96f67d989e805374` | historical_task_binding |
| E0101 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_ef26687d63a37e29/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_ef26687d63a37e29/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0101_critical_failures.json) | `801cede7da43eb49ff9bf5395786963e0443b7b7a67da7c5f8efc80f83a9308b` | historical_task_binding |
| E0102 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_ef26687d63a37e29/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_ef26687d63a37e29/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0102_critical_failures.json) | `801cede7da43eb49ff9bf5395786963e0443b7b7a67da7c5f8efc80f83a9308b` | historical_task_binding |
| E0103 | [docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/multwfn_adch_mep/vtx.pdb](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/multwfn_adch_mep/vtx.pdb) | `c7982606bf18edc1558817e0bb877fa4b9b7d7025c9f9c7b232c4696fc58a41b` | evidence_or_analysis |
| E0104 | [docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/multwfn_adch_mep/multiwfn_mep.out](../../../../docs/v2_verification/history/verification/group_1/paper_ef26687d63a37e29/artifacts/gaussian_batch/Et2N3P_si_recovered_v2_hpc_685c4cb0/multwfn_adch_mep/multiwfn_mep.out)；[冻结副本](../../../../docs/v2_verification/papers/paper_ef26687d63a37e29/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0104_native_excerpt.json) | `600cc0ad76dfac5e19329ea135352a70cea102d9d5d072099bc0c2249cb1a82f` | native_output |
| N0095 | [tasks/v2_autonomous_research/paper_ef26687d63a37e29/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_ef26687d63a37e29/evaluation/reference_key_points.json) | `ec5f8dcf6695d9b79a185aea103e413249cbd3c886e673216e245a7a6bb48e2b` | latest_review_evidence |
| N0096 | [tasks/v2_autonomous_research/paper_ef26687d63a37e29/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_ef26687d63a37e29/evaluation/reference_conclusions.json) | `8690f379736c61eed95c31f11f16864d0cef15f106761d2f213d5a9d0ba8540b` | latest_review_evidence |
| N0097 | [tasks/v2_autonomous_research/paper_ef26687d63a37e29/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_ef26687d63a37e29/evaluation/scoring_rules.json) | `6aedff4647615acab73abc8adb324706d044b9d4161191fe3c2f2d1a506e3799` | latest_review_evidence |
| N0098 | [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/evaluation/reference_key_points.json](reference_key_points.json) | `ec5f8dcf6695d9b79a185aea103e413249cbd3c886e673216e245a7a6bb48e2b` | latest_review_evidence |
| N0099 | [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/evaluation/reference_conclusions.json](reference_conclusions.json) | `8690f379736c61eed95c31f11f16864d0cef15f106761d2f213d5a9d0ba8540b` | latest_review_evidence |
| N0100 | [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/evaluation/scoring_rules.json](scoring_rules.json) | `6aedff4647615acab73abc8adb324706d044b9d4161191fe3c2f2d1a506e3799` | latest_review_evidence |
| N0101 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0102 | [docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json) | `3045e1e783ab41ea75b761599ea05ea0e0df1f8a9a6c1d65c3ca10bdd6daea91` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/agent_input/task.md](../agent_input/task.md) | `1bfdeb9b2f46133daf7807be3a39de3d8cb3d3d40e587d53e4c8b54d985828a4` |
| [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/evaluation/reference_key_points.json](reference_key_points.json) | `ec5f8dcf6695d9b79a185aea103e413249cbd3c886e673216e245a7a6bb48e2b` |
| [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/evaluation/reference_conclusions.json](reference_conclusions.json) | `8690f379736c61eed95c31f11f16864d0cef15f106761d2f213d5a9d0ba8540b` |
| [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/evaluation/scoring_rules.json](scoring_rules.json) | `6aedff4647615acab73abc8adb324706d044b9d4161191fe3c2f2d1a506e3799` |
| [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/evaluation/critical_failures.json](critical_failures.json) | `801cede7da43eb49ff9bf5395786963e0443b7b7a67da7c5f8efc80f83a9308b` |
| [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/evaluation/evidence_map.json](evidence_map.json) | `9280edb08621d3b1891291c340ba960424861efefd2dde49171ef2f0d9dc1b62` |
| [tasks/v2_paper_reproduction/paper_ef26687d63a37e29/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `23932ef0fdb945b1e9f68e0b8448282dba00006a6a242613db0ed865b46a6947` |

## Current scoring migration — 2026-10-19
Active paper_science_v2: 100 binary scientific-result points, intermediate findings plus final conclusions. Historical weights/freezes are superseded only as scoring policy. No process score or multiplier. No new chemical calculation or validation. Acceptance: PASS_STRICT_CURRENT_FROZEN_SCOPE. The Figure6 selected-H ADCH labels are not uniquely mapped. Neither nearest-contact H nor family mean may be declared the exact source selected H; 0.092/0.111 e are not active numeric targets. Signed ESP is not electron density; the source blue-region density wording is not adopted as a physical target. Historical TFPO contact extensions support local association, not newly computed NMR shifts. No propagation/backbiting barrier, binding free energy, absolute rate, bulk productivity or complete catalytic mechanism is certified.


## 2026-10-19 — Round 3 scoring-contract repair (not a chemical acceptance update)

The original verification history above remains verbatim. Current scoring uses the physical object/state/reference definitions in scoring_rules.json; author software and previous user acceptance are evaluator provenance, not facts a new agent must report. Numeric targets, tolerances, recorded residuals, reference acceptance status and scientific scope are unchanged. PR still addresses the disclosed baseline. Relevant final-claim evidence is assessed directly rather than requiring every intermediate numeric window or an unrelated branch to pass.
