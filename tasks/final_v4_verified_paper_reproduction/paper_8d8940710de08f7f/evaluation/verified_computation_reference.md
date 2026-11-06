# Second expert review — 2026-10-28

Existing preference rules now require actual relative energies and matched vacuum/methanol gap comparison; flexibility requires quantitative mapped torsional/path evidence, not merely a nonzero penalty. No hard target, mesh or TS calculation is added. Source Table S8 Gibbs ambiguity and finite-path limits remain. No new scientific calculations were run.

# V3 final-result evidence reuse — 2026-10-28

Unchanged full neutral-singlet SNaft/SAntr molecular preferences, intramolecular-contact explanation and finite torsional flexibility in vacuum/methanol. AR and PR have the same final questions and weights; PR alone discloses the author baseline and source ambiguity.

Four environment-specific preference rules reuse 12 R2SCAN/def2-TZVP/def2-J/RI minima. Existing qRRHO Z−lowest V gaps (SNaft/SAntr) are 3.487848/3.547305 kcal/mol in vacuum and 2.649947/2.679484 in methanol; electronic methanol gaps 3.039562/3.004860. Two contact explanations reuse separate ωB97M-V methanol QTAIM evidence (H/rho≈0.170, |V|/G≈0.789). Two flexibility results reuse the seven-point scans and released paths (sample maxima 6.283805/6.460401 kcal/mol). Redundant stability/flexibility synthesis and cross-medium restatements are no longer separately scored; their physical relations remain part of the relevant final answers.

Limitations: SI Table S8 is printed in vacuo but its electronic energies match methanol better; source Gibbs temperature/environment are unresolved, so no exact Table S8 G reproduction is certified. Very small V+/V− differences do not establish unique populations. Finite scans and release paths do not certify continuous TS barriers or rates. Local Espinosa estimates do not decompose total conformer stabilization. Historical strict acceptance applies only to the bounded frozen scope, not a new V3 evaluation.

The current policy is paper_science_v3 / final_results_100. The text below is an unchanged historical record; its old policies, scores and PASS labels are not current V3 certification. No new calculation was run.

---

# V2 验证计算参考：SNaft/SAntr 构象偏好与柔性

论文：`paper_8d8940710de08f7f`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：中性SNaft/SAntr的源主要电子能差、弱接触性质和约6–7 kcal/mol有限扫描尺度由真实作者级别计算恢复；真空和甲醇分别完成，支持有限的V优于Z结论。没有混用两介质声称同一个G。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

Determine the conformational preferences of neutral SNaft and SAntr and develop an evidence-supported explanation of their molecular stability and flexibility. Assess how far the interpretation can be maintained between the source in-vacuo and methanol molecular settings.

冻结题面中的科学目标：

Determine the conformational preferences of neutral SNaft and SAntr and develop an evidence-supported explanation of their molecular stability and flexibility. Assess how far the interpretation can be maintained between the source in-vacuo and methanol molecular settings.

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The source uses ORCA6.0.1 R2SCAN/def2-TZVP with def2/J, split-RI-J, relaxed C–S–N–C scans, optimizations and vibrational checks; C-PCM represents specified solvents (main p5). No extra D3 correction is declared for this R2SCAN route. The authors describe near-equivalent V(+)/V(−) and a less favourable Z geometry and discuss an aromatic C–H···O contact in the neutral molecules (pp9–10). Their QTAIM and dipole analyses instead use ωB97M-V/methanol wavefunctions; keep this separate from the geometry functional. SI Table S8 (physical pp8–11) labels its coordinates and electronic/Gibbs energies as calculated in vacuo. Preserve that reported label and distinguish it from independently established calculation provenance. If your evidence indicates an inconsistent source label, document the diagnosis and its limits rather than claiming an author-confirmed correction. Electronic-energy agreement alone does not establish the Gibbs-energy conditions. V1 D3 toggles, contact-disfavoring restraints, forced initial torsion bins and paired thermal panels were later benchmark interventions, not source protocols.

Reproduce the disclosed author baseline within this scope, or justify a substitute scientifically and assess its consequences. Clearly distinguish this reproduction from your additional investigation. Source conclusions are conditional evidence, not an answer that must be affirmed; scientifically justified corrections or unresolved results remain eligible. The V1 benchmark interventions were not part of the author protocol and are not required in this version.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_8d8940710de08f7f/documents/main.pdf](../../../../papers/paper_8d8940710de08f7f/documents/main.pdf) | `a69619c718ff7d48e4dd23ce129bb8ea5a7cb58e4fcb0114ab68587d688fe9bc` |
| [papers/paper_8d8940710de08f7f/documents/supplementary_001.pdf](../../../../papers/paper_8d8940710de08f7f/documents/supplementary_001.pdf) | `d903b517aab2dfd6c2a223020cb7d93ae6d66dc85eb489ab86c4aa854561bd13` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

Actual ORCA R2SCAN/def2-TZVP/def2-J/RI without extra D3, separate vacuum and CPCM methanol Opt/Freq; 12 native endpoints have 99/117 positive internal modes. Separate ωB97M-V methanol density is used for genuine QTAIM. Native scan-release trajectories were read.

1. 按完整 35/41 原子 SNaft/SAntr 中性单重态，分别建立 V(+)、V(−)、Z 的真空与 CPCM 甲醇分支。实际 ORCA R2SCAN/def2-TZVP/def2-J/RI 不额外加 D3。

2. 核收十二个 Opt/Freq 端点及 99/117 正内模，从原始 E 与热项分别重构各环境的 RRHO/qRRHO Gibbs 能；不按哪个数值更接近源来替换 SI 的环境标签。

3. 比较甲醇 Z−V 电子能 3.0395618/3.0048604 kcal/mol 与源 3.05/3.03；同时保留真空/甲醇的 G 差、近简并 V 对以及 Table S8 环境/热项冲突。

4. 使用独立 ωB97M-V 甲醇密度执行真正 QTAIM，识别 H···O BCP，计算 H/ρ≈0.170、|V|/G≈0.789 及局部 Espinosa 估计。它们支持弱闭壳层接触，不等于整个构象能差分解。

5. 核收七点约束旋转扫描与真实释放轨迹，最大采样升高约 6.28380/6.46040 kcal/mol，39/38 帧释放到 V(+) 盆地。支持有限柔性/可达性；不将采样最大点称为已验证连续 TS 或据此给精确速率。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

### 最近一次原生有效性复核

本轮直接读12个真空/甲醇端点，每个99或117正内模；从甲醇原生能量独立重算3.039561834/3.004860360 kcal/mol（源3.05/3.03）。本轮读取真实CPprop和Multiwfn输出定位弱闭壳层H···O BCP。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| Neutral Z−V electronic gap: SNaft,SAntr (kcal/mol) | [3.05,3.03] | [3.0395618343108035,3.004860360225426] | Main p9 core gaps are reproduced with residuals −0.01044/−0.02514 kcal/mol (<0.9%). This comparison is at matched methanol source narrative conditions; it is not relabelled as exact Table S8 vacuum Gibbs agreement. |
| H/ρ and \|V\|/G at genuine C–H···O BCPs (atomic units / dimensionless) | [0.17,0.79] | {"SNaft":[0.1703463526,0.7886411989],"SAntr":[0.1701337865,0.7882220206]} | Native CPprop identifies the H···O bond critical points and density properties; both diagnostic ratios reproduce source weak closed-shell character. |
| Local Espinosa EHB: SNaft-V+,SAntr-V+ (kcal/mol) | [2.52,2.42] | [2.5134497325,2.4675606951] | Residuals −0.00655/+0.04756 kcal/mol for an empirical local estimate; they do not define the total conformer stabilization energy. The approximately 2.4–2.55 source weak-contact scale is quantitatively retained. |
| Finite V-to-V sampled rotational maximum (kcal/mol) | Main p9 approximately 6–7 | [6.2838045716,6.4604014636] | Actual seven-point relaxed scans and released paths support the finite rotational-flexibility statement at the source approximate scale; they do not certify continuous TS barriers or rates. |
| Methanol/vacuum Z−lowest qRRHO G (kcal/mol) | Source qualitative V near-equivalence below Z; Table S8 Gibbs conditions uncertain | {"methanol":[2.6499474087,2.6794842796],"vacuum":[3.4878482591,3.5473047818]} | Both independently run media support preference. The old ±0.8 kcal/mol methanol allowance is not applied to source vacuum G; exact Table S8 G reconstruction is expressly unproven. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Verify complete SNaft/SAntr neutral graphs, charge/spin, model environments and atom correspondence. Do not mix charged species or different environments in an unqualified conformational population.

冻结要求：Verify complete SNaft/SAntr neutral graphs, charge/spin, model environments and atom correspondence. Do not mix charged species or different environments in an unqualified conformational population.

当前复审：中性完整分子和各构象

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainPDF5§2.8;SI8–11TableS8; supplied neutral graphs",
    "actual_result": "12个独立气相/甲醇端点保持完整35/41原子、中性singlet图；99/117正内模。原生梯度超额停止有效，未把约束扫描点当自由最低点。",
    "reason": "所比能量按分子及环境独立参照；没有带电物种混入，也没有给重复V端点额外统计权重。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log",
        "sha256": "ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.inp",
        "sha256": "c299eb25e395b29b8c0795756fd3fa97748d12c0005e4ccaa43fa0c34e364934",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.hess",
        "sha256": "c62c19412663b77155560ac2f62d2d4672b00804b36e23c90cdc5b25085ed30e",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log",
        "sha256": "517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.inp",
        "sha256": "bab269dca09e16de9d89f8e039cfa7a8f8e8a956a80bff8b8af9da562742075f",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.hess",
        "sha256": "701e81df3feb0ab8c77475ab7ebca245941ff58b582eca2c6a89d778b665bc2d",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log",
        "sha256": "b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.inp",
        "sha256": "d88b16b65979e4b3d7157ef7b2ef40698b18316e64facf3b10fc3f86184ad04f",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.hess",
        "sha256": "35df19f4f68d6d3f5432eeb649fc45d23f8a28a746914958d5c99ed17945a344",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log",
        "sha256": "956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.inp",
        "sha256": "29c8cac1bfbed4a19fa3c3b91aa982cffc18e1a762a1fe889c4077ec1a8c3f15",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.hess",
        "sha256": "2a388f9d91646b67aa722f353a5d76ad92f0846f6cf6afafc8a629324d3dbc95",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log",
        "sha256": "b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.inp",
        "sha256": "90548484fa8195e3d89422c6183895cb2816a593b669444acf2eb64e44eccc43",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.hess",
        "sha256": "b223e7e1d461f2e0fd17af9e18812a5030a38840c5e019782229dab50d1824de",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log",
        "sha256": "cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.inp",
        "sha256": "78bb14568f4ea020730da969cb55b59cc8d024eba4d1a9a2f0b277751fd6d918",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.hess",
        "sha256": "03399a2863a7e981660c54e5ca563ba8257443f4167d8b235f7e6dd36abc0199",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "0eb1b1043075ffacfa001cde319829447d5238daecce5b44ed782d9b748eb9c7",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "2764d0d6110f98e8d247f1c4233e3cdd1893a9c8c0a241e19665dae7122b726f",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log",
        "sha256": "18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.inp",
        "sha256": "3a1be9c90b2e8d66d559c9dfa4e36ae8d8dcdf2c342a30dbbf7cf6062dd092e1",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.hess",
        "sha256": "a0b48423c60e9529b041d24384e6a6d4b914594f57e01b76dc75b289d988b9d2",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "bba1725c3ffd11f54cde79057d5c5e0ae389d85357b578fa86a101b1ae300679",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "c958c004d0d7cb6db94f3f4994a60875c5eaa15ae13256a5a6a3390bd18e5148",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "3a0cc5db7eb410dba6942c161067821883528d371bc803a78c9306704f22e632",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "7c9618b13aff220a75761c2c7170b9b63ef2f41294011b15aaff9946872a1756",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "06f3fd32219150f740842fc5d5bb630c7ea5d7ce42757b6ab2bd7e258624d296",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "084edc203a0651157d0684760a2e003ba5b0ed3284f3a43ddda2f94adf3aafd8",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "fac82cdf3f9e3ccb0091fe8d694435b5adefe42787e27ab6d0d447e6a09354a4",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "e10f7f0540fe8beb1a67fcf8d78a9ed657394195cbb041513a549a010087bb0e",
        "role": "raw_Hessian"
      }
    ]
  }
]
```


证据记录：`E0091`。

```json
[
  {
    "source_locator": "mainPDF5§2.8;SI8–11TableS8; supplied neutral graphs",
    "actual_result": "12个独立气相/甲醇端点保持完整35/41原子、中性singlet图；99/117正内模。原生梯度超额停止有效，未把约束扫描点当自由最低点。",
    "reason": "所比能量按分子及环境独立参照；没有带电物种混入，也没有给重复V端点额外统计权重。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log",
        "sha256": "ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.inp",
        "sha256": "c299eb25e395b29b8c0795756fd3fa97748d12c0005e4ccaa43fa0c34e364934",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.hess",
        "sha256": "c62c19412663b77155560ac2f62d2d4672b00804b36e23c90cdc5b25085ed30e",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log",
        "sha256": "517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.inp",
        "sha256": "bab269dca09e16de9d89f8e039cfa7a8f8e8a956a80bff8b8af9da562742075f",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.hess",
        "sha256": "701e81df3feb0ab8c77475ab7ebca245941ff58b582eca2c6a89d778b665bc2d",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log",
        "sha256": "b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.inp",
        "sha256": "d88b16b65979e4b3d7157ef7b2ef40698b18316e64facf3b10fc3f86184ad04f",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.hess",
        "sha256": "35df19f4f68d6d3f5432eeb649fc45d23f8a28a746914958d5c99ed17945a344",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log",
        "sha256": "956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.inp",
        "sha256": "29c8cac1bfbed4a19fa3c3b91aa982cffc18e1a762a1fe889c4077ec1a8c3f15",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.hess",
        "sha256": "2a388f9d91646b67aa722f353a5d76ad92f0846f6cf6afafc8a629324d3dbc95",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log",
        "sha256": "b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.inp",
        "sha256": "90548484fa8195e3d89422c6183895cb2816a593b669444acf2eb64e44eccc43",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.hess",
        "sha256": "b223e7e1d461f2e0fd17af9e18812a5030a38840c5e019782229dab50d1824de",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log",
        "sha256": "cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.inp",
        "sha256": "78bb14568f4ea020730da969cb55b59cc8d024eba4d1a9a2f0b277751fd6d918",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.hess",
        "sha256": "03399a2863a7e981660c54e5ca563ba8257443f4167d8b235f7e6dd36abc0199",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "0eb1b1043075ffacfa001cde319829447d5238daecce5b44ed782d9b748eb9c7",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "2764d0d6110f98e8d247f1c4233e3cdd1893a9c8c0a241e19665dae7122b726f",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log",
        "sha256": "18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.inp",
        "sha256": "3a1be9c90b2e8d66d559c9dfa4e36ae8d8dcdf2c342a30dbbf7cf6062dd092e1",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.hess",
        "sha256": "a0b48423c60e9529b041d24384e6a6d4b914594f57e01b76dc75b289d988b9d2",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "bba1725c3ffd11f54cde79057d5c5e0ae389d85357b578fa86a101b1ae300679",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "c958c004d0d7cb6db94f3f4994a60875c5eaa15ae13256a5a6a3390bd18e5148",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "3a0cc5db7eb410dba6942c161067821883528d371bc803a78c9306704f22e632",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "7c9618b13aff220a75761c2c7170b9b63ef2f41294011b15aaff9946872a1756",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "06f3fd32219150f740842fc5d5bb630c7ea5d7ce42757b6ab2bd7e258624d296",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "084edc203a0651157d0684760a2e003ba5b0ed3284f3a43ddda2f94adf3aafd8",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "fac82cdf3f9e3ccb0091fe8d694435b5adefe42787e27ab6d0d447e6a09354a4",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "e10f7f0540fe8beb1a67fcf8d78a9ed657394195cbb041513a549a010087bb0e",
        "role": "raw_Hessian"
      }
    ]
  }
]
```

### kp_results — Assess auditable structures, energies and any other claim-relevant conformational quantities. Distinguish an electronic-energy difference from a free-energy difference, constrained points from minima and repeated endpoints from distinct states. No source torsion bin or predetermined family count is mandatory.

冻结要求：Assess auditable structures, energies and any other claim-relevant conformational quantities. Distinguish an electronic-energy difference from a free-energy difference, constrained points from minima and repeated endpoints from distinct states. No source torsion bin or predetermined family count is mandatory.

当前复审：两介质端点/实能量/曲率

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainPDF9–10Fig7/8;SI8–11TableS8",
    "actual_result": "甲醇/真空E与G分开；两环境V低Z高。12个G逐项重构，qRRHO/RRHO结果保持Z不利，电子源3.05/3.03对实算3.03956/3.00486。",
    "reason": "继承同对象、R2SCAN无D3、甲醇298.15K/1atm G−本分子最低G的旧2.57±0.8kcal/mol有效尺度，仅适用于该甲醇G量；不用于真空、E、偶极或源未明G环境。当前Z−最低G2.64995/2.67948且稳健序关系满足此依据。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log",
        "sha256": "ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.inp",
        "sha256": "c299eb25e395b29b8c0795756fd3fa97748d12c0005e4ccaa43fa0c34e364934",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.hess",
        "sha256": "c62c19412663b77155560ac2f62d2d4672b00804b36e23c90cdc5b25085ed30e",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log",
        "sha256": "517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.inp",
        "sha256": "bab269dca09e16de9d89f8e039cfa7a8f8e8a956a80bff8b8af9da562742075f",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.hess",
        "sha256": "701e81df3feb0ab8c77475ab7ebca245941ff58b582eca2c6a89d778b665bc2d",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log",
        "sha256": "b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.inp",
        "sha256": "d88b16b65979e4b3d7157ef7b2ef40698b18316e64facf3b10fc3f86184ad04f",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.hess",
        "sha256": "35df19f4f68d6d3f5432eeb649fc45d23f8a28a746914958d5c99ed17945a344",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log",
        "sha256": "956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.inp",
        "sha256": "29c8cac1bfbed4a19fa3c3b91aa982cffc18e1a762a1fe889c4077ec1a8c3f15",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.hess",
        "sha256": "2a388f9d91646b67aa722f353a5d76ad92f0846f6cf6afafc8a629324d3dbc95",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log",
        "sha256": "b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.inp",
        "sha256": "90548484fa8195e3d89422c6183895cb2816a593b669444acf2eb64e44eccc43",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.hess",
        "sha256": "b223e7e1d461f2e0fd17af9e18812a5030a38840c5e019782229dab50d1824de",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log",
        "sha256": "cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.inp",
        "sha256": "78bb14568f4ea020730da969cb55b59cc8d024eba4d1a9a2f0b277751fd6d918",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.hess",
        "sha256": "03399a2863a7e981660c54e5ca563ba8257443f4167d8b235f7e6dd36abc0199",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "0eb1b1043075ffacfa001cde319829447d5238daecce5b44ed782d9b748eb9c7",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "2764d0d6110f98e8d247f1c4233e3cdd1893a9c8c0a241e19665dae7122b726f",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log",
        "sha256": "18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.inp",
        "sha256": "3a1be9c90b2e8d66d559c9dfa4e36ae8d8dcdf2c342a30dbbf7cf6062dd092e1",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.hess",
        "sha256": "a0b48423c60e9529b041d24384e6a6d4b914594f57e01b76dc75b289d988b9d2",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "bba1725c3ffd11f54cde79057d5c5e0ae389d85357b578fa86a101b1ae300679",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "c958c004d0d7cb6db94f3f4994a60875c5eaa15ae13256a5a6a3390bd18e5148",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "3a0cc5db7eb410dba6942c161067821883528d371bc803a78c9306704f22e632",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "7c9618b13aff220a75761c2c7170b9b63ef2f41294011b15aaff9946872a1756",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "06f3fd32219150f740842fc5d5bb630c7ea5d7ce42757b6ab2bd7e258624d296",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "084edc203a0651157d0684760a2e003ba5b0ed3284f3a43ddda2f94adf3aafd8",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "fac82cdf3f9e3ccb0091fe8d694435b5adefe42787e27ab6d0d447e6a09354a4",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "e10f7f0540fe8beb1a67fcf8d78a9ed657394195cbb041513a549a010087bb0e",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/s8_thermal_reuse_20261008/attempt_001/SULFONAMIDE_S8_THERMAL_RESULTS.json",
        "sha256": "6403fe05c758cc85426be67b5f282de69b29560138f5f20cf42965b18b6888cf",
        "role": "HPC_analysis"
      },
      {
        "path": "tasks/final_verified_paper_reproduction/paper_8d8940710de08f7f/evaluation/scoring_rules.json",
        "sha256": "b90bda7f443a01f7e59e67074672f1b2a3ce925a181b5cfb5fdcb50f7050d15f",
        "role": "inherited_acceptance_basis"
      }
    ]
  }
]
```


证据记录：`E0091`。

```json
[
  {
    "source_locator": "mainPDF9–10Fig7/8;SI8–11TableS8",
    "actual_result": "甲醇/真空E与G分开；两环境V低Z高。12个G逐项重构，qRRHO/RRHO结果保持Z不利，电子源3.05/3.03对实算3.03956/3.00486。",
    "reason": "继承同对象、R2SCAN无D3、甲醇298.15K/1atm G−本分子最低G的旧2.57±0.8kcal/mol有效尺度，仅适用于该甲醇G量；不用于真空、E、偶极或源未明G环境。当前Z−最低G2.64995/2.67948且稳健序关系满足此依据。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log",
        "sha256": "ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.inp",
        "sha256": "c299eb25e395b29b8c0795756fd3fa97748d12c0005e4ccaa43fa0c34e364934",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.hess",
        "sha256": "c62c19412663b77155560ac2f62d2d4672b00804b36e23c90cdc5b25085ed30e",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log",
        "sha256": "517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.inp",
        "sha256": "bab269dca09e16de9d89f8e039cfa7a8f8e8a956a80bff8b8af9da562742075f",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.hess",
        "sha256": "701e81df3feb0ab8c77475ab7ebca245941ff58b582eca2c6a89d778b665bc2d",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log",
        "sha256": "b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.inp",
        "sha256": "d88b16b65979e4b3d7157ef7b2ef40698b18316e64facf3b10fc3f86184ad04f",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.hess",
        "sha256": "35df19f4f68d6d3f5432eeb649fc45d23f8a28a746914958d5c99ed17945a344",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log",
        "sha256": "956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.inp",
        "sha256": "29c8cac1bfbed4a19fa3c3b91aa982cffc18e1a762a1fe889c4077ec1a8c3f15",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.hess",
        "sha256": "2a388f9d91646b67aa722f353a5d76ad92f0846f6cf6afafc8a629324d3dbc95",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log",
        "sha256": "b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.inp",
        "sha256": "90548484fa8195e3d89422c6183895cb2816a593b669444acf2eb64e44eccc43",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.hess",
        "sha256": "b223e7e1d461f2e0fd17af9e18812a5030a38840c5e019782229dab50d1824de",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log",
        "sha256": "cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.inp",
        "sha256": "78bb14568f4ea020730da969cb55b59cc8d024eba4d1a9a2f0b277751fd6d918",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.hess",
        "sha256": "03399a2863a7e981660c54e5ca563ba8257443f4167d8b235f7e6dd36abc0199",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "0eb1b1043075ffacfa001cde319829447d5238daecce5b44ed782d9b748eb9c7",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "2764d0d6110f98e8d247f1c4233e3cdd1893a9c8c0a241e19665dae7122b726f",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log",
        "sha256": "18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.inp",
        "sha256": "3a1be9c90b2e8d66d559c9dfa4e36ae8d8dcdf2c342a30dbbf7cf6062dd092e1",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.hess",
        "sha256": "a0b48423c60e9529b041d24384e6a6d4b914594f57e01b76dc75b289d988b9d2",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "bba1725c3ffd11f54cde79057d5c5e0ae389d85357b578fa86a101b1ae300679",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "c958c004d0d7cb6db94f3f4994a60875c5eaa15ae13256a5a6a3390bd18e5148",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "3a0cc5db7eb410dba6942c161067821883528d371bc803a78c9306704f22e632",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "7c9618b13aff220a75761c2c7170b9b63ef2f41294011b15aaff9946872a1756",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "06f3fd32219150f740842fc5d5bb630c7ea5d7ce42757b6ab2bd7e258624d296",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "084edc203a0651157d0684760a2e003ba5b0ed3284f3a43ddda2f94adf3aafd8",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp",
        "sha256": "fac82cdf3f9e3ccb0091fe8d694435b5adefe42787e27ab6d0d447e6a09354a4",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess",
        "sha256": "e10f7f0540fe8beb1a67fcf8d78a9ed657394195cbb041513a549a010087bb0e",
        "role": "raw_Hessian"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/s8_thermal_reuse_20261008/attempt_001/SULFONAMIDE_S8_THERMAL_RESULTS.json",
        "sha256": "6403fe05c758cc85426be67b5f282de69b29560138f5f20cf42965b18b6888cf",
        "role": "HPC_analysis"
      },
      {
        "path": "tasks/final_verified_paper_reproduction/paper_8d8940710de08f7f/evaluation/scoring_rules.json",
        "sha256": "b90bda7f443a01f7e59e67074672f1b2a3ce925a181b5cfb5fdcb50f7050d15f",
        "role": "inherited_acceptance_basis"
      }
    ]
  }
]
```

### kp_interpretation — Judge whether the proposed explanation of stability/flexibility is supported by meaningful evidence and whether consequential alternatives or environmental limitations are addressed. A contact picture alone is insufficient for energetic attribution. Evidence-supported near-degeneracy, collapse or lack of unique attribution can be a full bounded scientific conclusion.

冻结要求：Judge whether the proposed explanation of stability/flexibility is supported by meaningful evidence and whether consequential alternatives or environmental limitations are addressed. A contact picture alone is insufficient for energetic attribution. Evidence-supported near-degeneracy, collapse or lack of unique attribution can be a full bounded scientific conclusion.

当前复审：实BCP支持弱接触

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainPDF9–10;SI11–12TableS9",
    "actual_result": "BCP H/rho≈0.170、|V|/G≈0.79；SNaft局部|V|/2≈2.51345kcal/mol。7点路径最大采样升高6.28380/6.46040kcal/mol，39/38帧释放未增加更高峰，终态到V+盆地。",
    "reason": "真实拓扑和有限路径超过接触图/排序本身的解释力度；限制为弱氢键可作贡献、不唯一归因、无TS/速率主张，符合当前开放解释节点。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPprop.txt",
        "sha256": "48fe4f9abe72a98ae29120ca8cf6f25ed189ce96ab7cb0aed7cc23d7f8198a65",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPs.txt",
        "sha256": "0a128415ef802cc735f5f0510e699945d05f387a99413ee50e5c0f34912315ac",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/paths.txt",
        "sha256": "d0e8dadfd0f3669699f30a9a3f357e315ff3a4b3b9da00e71793116fd83df9ad",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/multiwfn.log",
        "sha256": "deed38a513f8dee33898d5a96a5e1d7e6a65a1aa86431d72246478bdffb567ad",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPprop.txt",
        "sha256": "830d34ef62ba31a0bdf23b7f78c1e62acbb651c9b227db97ff5e940b67f4e2c5",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPs.txt",
        "sha256": "35d1ee6e54a945f496c2d3502362ff9deb0aff9dc9854109f4d8ad6c831c91ba",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/paths.txt",
        "sha256": "5e059f8940edc18eb1c3d34c12c8308790e4a60579609d1ce042ef90048790f3",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/multiwfn.log",
        "sha256": "acd074c8c2e8b382b12bd8c98ba26b9cb39d0c86acb0855d843b7ae838b57d4e",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_objects_20261004/sulfonamide_scan_release_path/attempt_001/sulfonamide_path_closure_results.json",
        "sha256": "6f9af0180bf3852e2e2c97add648dcf726e24e01deaf8708b46178967c544d9c",
        "role": "HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/stdout.log",
        "sha256": "a1993b85c1b8da5bc66653ab552b4c5e1c6e1f86673bb35053a97aedc96b461a",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input.inp",
        "sha256": "06b6f554588b7028484534f22913fc8ecf65a135b73ce26695acea610ea580dd",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz",
        "sha256": "afc663a8c3c16e77ae26e71f0ecba05a78d382e39a2efd236d9873151bd9cf6e",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/stdout.log",
        "sha256": "4116be201706cc9eb6f586a3e3fe81b99b4b51ecf5f767c7bd5b70b2b873e12c",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input.inp",
        "sha256": "de70936bcb11cf4bacfc2a32ecfb8113fdd7000f5e889689bc05fb38ff474891",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz",
        "sha256": "fed6fca599d0dcea26b8ed08d93b436767b1bc1bb70fa6023749991393267cda",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/sulfonamide_source_path_minima_topology_join.json",
        "sha256": "029cfe32f1c927f9b4d51c1c1b3fefdfb2fc28641a4188efd70e4fcfdb2ba975",
        "role": "analysis"
      }
    ]
  }
]
```


证据记录：`E0091`。

```json
[
  {
    "source_locator": "mainPDF9–10;SI11–12TableS9",
    "actual_result": "BCP H/rho≈0.170、|V|/G≈0.79；SNaft局部|V|/2≈2.51345kcal/mol。7点路径最大采样升高6.28380/6.46040kcal/mol，39/38帧释放未增加更高峰，终态到V+盆地。",
    "reason": "真实拓扑和有限路径超过接触图/排序本身的解释力度；限制为弱氢键可作贡献、不唯一归因、无TS/速率主张，符合当前开放解释节点。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPprop.txt",
        "sha256": "48fe4f9abe72a98ae29120ca8cf6f25ed189ce96ab7cb0aed7cc23d7f8198a65",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPs.txt",
        "sha256": "0a128415ef802cc735f5f0510e699945d05f387a99413ee50e5c0f34912315ac",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/paths.txt",
        "sha256": "d0e8dadfd0f3669699f30a9a3f357e315ff3a4b3b9da00e71793116fd83df9ad",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/multiwfn.log",
        "sha256": "deed38a513f8dee33898d5a96a5e1d7e6a65a1aa86431d72246478bdffb567ad",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPprop.txt",
        "sha256": "830d34ef62ba31a0bdf23b7f78c1e62acbb651c9b227db97ff5e940b67f4e2c5",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPs.txt",
        "sha256": "35d1ee6e54a945f496c2d3502362ff9deb0aff9dc9854109f4d8ad6c831c91ba",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/paths.txt",
        "sha256": "5e059f8940edc18eb1c3d34c12c8308790e4a60579609d1ce042ef90048790f3",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/multiwfn.log",
        "sha256": "acd074c8c2e8b382b12bd8c98ba26b9cb39d0c86acb0855d843b7ae838b57d4e",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_objects_20261004/sulfonamide_scan_release_path/attempt_001/sulfonamide_path_closure_results.json",
        "sha256": "6f9af0180bf3852e2e2c97add648dcf726e24e01deaf8708b46178967c544d9c",
        "role": "HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/stdout.log",
        "sha256": "a1993b85c1b8da5bc66653ab552b4c5e1c6e1f86673bb35053a97aedc96b461a",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input.inp",
        "sha256": "06b6f554588b7028484534f22913fc8ecf65a135b73ce26695acea610ea580dd",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz",
        "sha256": "afc663a8c3c16e77ae26e71f0ecba05a78d382e39a2efd236d9873151bd9cf6e",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/stdout.log",
        "sha256": "4116be201706cc9eb6f586a3e3fe81b99b4b51ecf5f767c7bd5b70b2b873e12c",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input.inp",
        "sha256": "de70936bcb11cf4bacfc2a32ecfb8113fdd7000f5e889689bc05fb38ff474891",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz",
        "sha256": "fed6fca599d0dcea26b8ed08d93b436767b1bc1bb70fa6023749991393267cda",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/sulfonamide_source_path_minima_topology_join.json",
        "sha256": "029cfe32f1c927f9b4d51c1c1b3fefdfb2fc28641a4188efd70e4fcfdb2ba975",
        "role": "analysis"
      }
    ]
  }
]
```

### kp_uncertainty — Assess sampling and claim-relevant numerical, low-frequency/thermochemical or solvent-model uncertainty. Do not infer a robust tiny ordering from uncalibrated energy digits. When a submission uses or diagnoses SI Table S8 data, preserve its reported in-vacuo label while distinguishing that label from independently established calculation provenance. Evidence-supported diagnosis of a source-label inconsistency is eligible; unsupported relabelling or mixing environments is not. An independent route that does not use Table S8 is not required to retrieve or discuss that table and must not lose credit solely for omitting it; the same scientific uncertainty and evidence standards still apply. A single-point electronic-energy diagnosis does not establish the Gibbs-energy environment or conformer populations. No fixed correction toggle or acceptance interval applies.

冻结要求：Assess sampling and claim-relevant numerical, low-frequency/thermochemical or solvent-model uncertainty. Do not infer a robust tiny ordering from uncalibrated energy digits. When a submission uses or diagnoses SI Table S8 data, preserve its reported in-vacuo label while distinguishing that label from independently established calculation provenance. Evidence-supported diagnosis of a source-label inconsistency is eligible; unsupported relabelling or mixing environments is not. An independent route that does not use Table S8 is not required to retrieve or discuss that table and must not lose credit solely for omitting it; the same scientific uncertainty and evidence standards still apply. A single-point electronic-energy diagnosis does not establish the Gibbs-energy environment or conformer populations. No fixed correction toggle or acceptance interval applies.

当前复审：介质、qRRHO、S8标签与有限扫描限制

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainPDF5;SI8–11literal in-vacuo caption; current kp_uncertainty",
    "actual_result": "源S8 G在假定甲醇qRRHO模型下仍有0.14–0.75kcal/mol绝对差；假定真空差约17.6–20.8。单一RRHO替換改变Z相对G约−0.19至−0.25，未逆转V/Z。不能按接近度替源改标签。",
    "reason": "未知原G协议不构成本题无法比较两个已算环境；精确V+/V−布居不作结论。SAntrZ偶极差−0.01126D及grid否证保留，但不是稳定性/柔性核心的硬数值靶。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/s8_thermal_reuse_20261008/attempt_001/SULFONAMIDE_S8_THERMAL_RESULTS.json",
        "sha256": "6403fe05c758cc85426be67b5f282de69b29560138f5f20cf42965b18b6888cf",
        "role": "HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log",
        "sha256": "ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log",
        "sha256": "517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log",
        "sha256": "b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log",
        "sha256": "956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log",
        "sha256": "b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log",
        "sha256": "cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log",
        "sha256": "18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "d1e14d5fab243edda9ac69d1212744953a654a86aba24be6637e71c1b411d0a3",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "28e7482fbf0ba29749760b64ee3c4197f479a4e1bc9dff822620ca9dbd55b369",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "278629e2044078feed1b057bffea8701622c5e910bde901bfca539cfb97ae2c3",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "6e4257c9bb4f6eea8b2f0f2a9bdc4ba44242efa2eb808be79718b3dfb36853f1",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "f40f00255f44f2d59c71f40b9352ebbbb843f4e70d2d3cfb109c93579e5448e9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "b7e203be5c5f144ccbd90b2135ed4d7ae960f61c602f2c774262e35a6bc28077",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "4b7e166c07edf42189fa1d6d40991584d9716f0ce5f30787fdbc645316bc1076",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "af2de3b8d8a00de18fc05f9b9ad0a9926b24028d4fc0de5578fba741821fe3d1",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "27df44985bc6fbe2d091905685b717dcc019d3cf2c23bbf58b53b1bef5e5027e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "6b3913638a5cd2ffe46368f62e4f35d7368e6a0a1ca85c8dcc5a494fb1f5ea31",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "9fea9ae40b61549eadca35936b68929a643237b7a747524bb6207d5b99dbaeaa",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "19fa2442afd6ae7fe1419c67f2d18db1c49f976b0632caa81037af1a283196f8",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/OPT_STOP_REVIEW_20261007.json",
        "sha256": "50dedd40f3b13f4d9802d42f1e480e140fabb4bebad946586f0480f82e9e52f2",
        "role": "evidence"
      }
    ]
  }
]
```


证据记录：`E0091`。

```json
[
  {
    "source_locator": "mainPDF5;SI8–11literal in-vacuo caption; current kp_uncertainty",
    "actual_result": "源S8 G在假定甲醇qRRHO模型下仍有0.14–0.75kcal/mol绝对差；假定真空差约17.6–20.8。单一RRHO替換改变Z相对G约−0.19至−0.25，未逆转V/Z。不能按接近度替源改标签。",
    "reason": "未知原G协议不构成本题无法比较两个已算环境；精确V+/V−布居不作结论。SAntrZ偶极差−0.01126D及grid否证保留，但不是稳定性/柔性核心的硬数值靶。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/s8_thermal_reuse_20261008/attempt_001/SULFONAMIDE_S8_THERMAL_RESULTS.json",
        "sha256": "6403fe05c758cc85426be67b5f282de69b29560138f5f20cf42965b18b6888cf",
        "role": "HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log",
        "sha256": "ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log",
        "sha256": "517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log",
        "sha256": "b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log",
        "sha256": "956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log",
        "sha256": "b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log",
        "sha256": "cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log",
        "sha256": "18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "d1e14d5fab243edda9ac69d1212744953a654a86aba24be6637e71c1b411d0a3",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "28e7482fbf0ba29749760b64ee3c4197f479a4e1bc9dff822620ca9dbd55b369",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "278629e2044078feed1b057bffea8701622c5e910bde901bfca539cfb97ae2c3",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "6e4257c9bb4f6eea8b2f0f2a9bdc4ba44242efa2eb808be79718b3dfb36853f1",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "f40f00255f44f2d59c71f40b9352ebbbb843f4e70d2d3cfb109c93579e5448e9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "b7e203be5c5f144ccbd90b2135ed4d7ae960f61c602f2c774262e35a6bc28077",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "4b7e166c07edf42189fa1d6d40991584d9716f0ce5f30787fdbc645316bc1076",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "af2de3b8d8a00de18fc05f9b9ad0a9926b24028d4fc0de5578fba741821fe3d1",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "27df44985bc6fbe2d091905685b717dcc019d3cf2c23bbf58b53b1bef5e5027e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "6b3913638a5cd2ffe46368f62e4f35d7368e6a0a1ca85c8dcc5a494fb1f5ea31",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log",
        "sha256": "9fea9ae40b61549eadca35936b68929a643237b7a747524bb6207d5b99dbaeaa",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp",
        "sha256": "19fa2442afd6ae7fe1419c67f2d18db1c49f976b0632caa81037af1a283196f8",
        "role": "raw_input"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/OPT_STOP_REVIEW_20261007.json",
        "sha256": "50dedd40f3b13f4d9802d42f1e480e140fabb4bebad946586f0480f82e9e52f2",
        "role": "evidence"
      }
    ]
  }
]
```

### kp_audit — Verify that evidence IDs resolve to actual hash-matched raw artifacts, models/methods are linked, and numerical transformations can be reproduced. Inspect research_log against real tool traces for process claims. Neither schema validity, normal termination, hypothesis count nor self-written chronology proves scientific validity.

冻结要求：Verify that evidence IDs resolve to actual hash-matched raw artifacts, models/methods are linked, and numerical transformations can be reproduced. Inspect research_log against real tool traces for process claims. Neither schema validity, normal termination, hypothesis count nor self-written chronology proves scientific validity.

当前复审：原生可追溯；最终有限偏好/柔性与主文一致。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "sourcePDFs; all retained raw/hessian/result/job receipts",
    "actual_result": "4505489c原生rc0/wrapper0，2秒完成12热项重分析；其输入、源E/G、12父日志/Hessian均有哈希，失败历史未覆盖。",
    "reason": "本轮只核收及重定当前题覆盖，无新增量化；原真空历史路径如无jobID不虚构平台ID，原像和原生正常标志可核。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/s8_thermal_reuse_20261008/attempt_001/SULFONAMIDE_S8_THERMAL_RESULTS.json",
        "sha256": "6403fe05c758cc85426be67b5f282de69b29560138f5f20cf42965b18b6888cf",
        "role": "HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log",
        "sha256": "ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log",
        "sha256": "517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log",
        "sha256": "b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log",
        "sha256": "956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log",
        "sha256": "b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log",
        "sha256": "cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log",
        "sha256": "18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W04_RETURNED_JOB_INTAKE.json",
        "sha256": "46d18cf5955fe1b814a482e0e6c3619ff53027942a48df73c44ffd99715e76f4",
        "role": "evidence"
      }
    ]
  }
]
```


证据记录：`E0091`。

```json
[
  {
    "source_locator": "sourcePDFs; all retained raw/hessian/result/job receipts",
    "actual_result": "4505489c原生rc0/wrapper0，2秒完成12热项重分析；其输入、源E/G、12父日志/Hessian均有哈希，失败历史未覆盖。",
    "reason": "本轮只核收及重定当前题覆盖，无新增量化；原真空历史路径如无jobID不虚构平台ID，原像和原生正常标志可核。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/s8_thermal_reuse_20261008/attempt_001/SULFONAMIDE_S8_THERMAL_RESULTS.json",
        "sha256": "6403fe05c758cc85426be67b5f282de69b29560138f5f20cf42965b18b6888cf",
        "role": "HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log",
        "sha256": "ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log",
        "sha256": "517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log",
        "sha256": "b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log",
        "sha256": "956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log",
        "sha256": "b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log",
        "sha256": "cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log",
        "sha256": "18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W04_RETURNED_JOB_INTAKE.json",
        "sha256": "46d18cf5955fe1b814a482e0e6c3619ff53027942a48df73c44ffd99715e76f4",
        "role": "evidence"
      }
    ]
  }
]
```

### conclusion_answer — State the supported conformational preferences and their explanation within the neutral molecular settings, distinguishing resolved preferences from approximate equivalence or incomplete coverage. Do not infer pharmacological potency, membrane transport or crystal equilibrium from these isolated-molecule findings.

冻结要求：State the supported conformational preferences and their explanation within the neutral molecular settings, distinguishing resolved preferences from approximate equivalence or incomplete coverage. Do not infer pharmacological potency, membrane transport or crystal equilibrium from these isolated-molecule findings.

当前复审：kp_identity：中性完整分子和各构象；kp_results：两介质端点/实能量/曲率；kp_interpretation：实BCP支持弱接触；kp_uncertainty：介质、qRRHO、S8标签与有限扫描限制；kp_audit：原生可追溯；最终有限偏好/柔性与主文一致。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "mainPDF9–10; current V2 neutral conformational question",
    "actual_result": "中性 SNaft 与 SAntr 的 V(+) / V(−) 是近简并的低能构象，Z 较不利；这一方向在显式区分的真空与 CPCM 甲醇计算中均保持。甲醇电子 Z−V 为3.03956/3.00486 kcal/mol，真空为3.78937/3.86845；298.15K/1atm qRRHO 的甲醇 Z−最低G 为2.64995/2.67948，真空为3.48785/3.54730。甲醇 V 对G差仅0.03035/0.02499 kcal/mol，RRHO替换及旧数值控制显示不能可靠地区分两V的细小顺序或给精确布居。真实CH···O键临界点和弱闭壳层相互作用支持V稳定化的一个贡献，但没有把局部Espinosa估计当整个构象能差的因果分解。实际约束扫描及释放轨迹支持有限旋转柔性和V盆地可达性，未证明连续鞍点、速率。SI TableS8的in-vacuo标签保留；同坐标E更符合甲醇的诊断和新G热项比较不足以证明作者G介质/温度。上述来源冲突不改变两环境内已实际建立的偏好方向。",
    "reason": "所交完整答案解释可维护的中性偏好与柔性，明确边界；没有把源G标签推断成确定更正，也没有扩展到药效/膜/晶体平衡。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/s8_thermal_reuse_20261008/attempt_001/SULFONAMIDE_S8_THERMAL_RESULTS.json",
        "sha256": "6403fe05c758cc85426be67b5f282de69b29560138f5f20cf42965b18b6888cf",
        "role": "HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log",
        "sha256": "ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log",
        "sha256": "517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log",
        "sha256": "b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log",
        "sha256": "956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log",
        "sha256": "b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log",
        "sha256": "cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log",
        "sha256": "18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPprop.txt",
        "sha256": "48fe4f9abe72a98ae29120ca8cf6f25ed189ce96ab7cb0aed7cc23d7f8198a65",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPs.txt",
        "sha256": "0a128415ef802cc735f5f0510e699945d05f387a99413ee50e5c0f34912315ac",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/paths.txt",
        "sha256": "d0e8dadfd0f3669699f30a9a3f357e315ff3a4b3b9da00e71793116fd83df9ad",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/multiwfn.log",
        "sha256": "deed38a513f8dee33898d5a96a5e1d7e6a65a1aa86431d72246478bdffb567ad",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPprop.txt",
        "sha256": "830d34ef62ba31a0bdf23b7f78c1e62acbb651c9b227db97ff5e940b67f4e2c5",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPs.txt",
        "sha256": "35d1ee6e54a945f496c2d3502362ff9deb0aff9dc9854109f4d8ad6c831c91ba",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/paths.txt",
        "sha256": "5e059f8940edc18eb1c3d34c12c8308790e4a60579609d1ce042ef90048790f3",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/multiwfn.log",
        "sha256": "acd074c8c2e8b382b12bd8c98ba26b9cb39d0c86acb0855d843b7ae838b57d4e",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_objects_20261004/sulfonamide_scan_release_path/attempt_001/sulfonamide_path_closure_results.json",
        "sha256": "6f9af0180bf3852e2e2c97add648dcf726e24e01deaf8708b46178967c544d9c",
        "role": "HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/stdout.log",
        "sha256": "a1993b85c1b8da5bc66653ab552b4c5e1c6e1f86673bb35053a97aedc96b461a",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input.inp",
        "sha256": "06b6f554588b7028484534f22913fc8ecf65a135b73ce26695acea610ea580dd",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz",
        "sha256": "afc663a8c3c16e77ae26e71f0ecba05a78d382e39a2efd236d9873151bd9cf6e",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/stdout.log",
        "sha256": "4116be201706cc9eb6f586a3e3fe81b99b4b51ecf5f767c7bd5b70b2b873e12c",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input.inp",
        "sha256": "de70936bcb11cf4bacfc2a32ecfb8113fdd7000f5e889689bc05fb38ff474891",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz",
        "sha256": "fed6fca599d0dcea26b8ed08d93b436767b1bc1bb70fa6023749991393267cda",
        "role": "raw_path"
      }
    ]
  }
]
```


证据记录：`E0091`。

```json
[
  {
    "source_locator": "mainPDF9–10; current V2 neutral conformational question",
    "actual_result": "中性 SNaft 与 SAntr 的 V(+) / V(−) 是近简并的低能构象，Z 较不利；这一方向在显式区分的真空与 CPCM 甲醇计算中均保持。甲醇电子 Z−V 为3.03956/3.00486 kcal/mol，真空为3.78937/3.86845；298.15K/1atm qRRHO 的甲醇 Z−最低G 为2.64995/2.67948，真空为3.48785/3.54730。甲醇 V 对G差仅0.03035/0.02499 kcal/mol，RRHO替换及旧数值控制显示不能可靠地区分两V的细小顺序或给精确布居。真实CH···O键临界点和弱闭壳层相互作用支持V稳定化的一个贡献，但没有把局部Espinosa估计当整个构象能差的因果分解。实际约束扫描及释放轨迹支持有限旋转柔性和V盆地可达性，未证明连续鞍点、速率。SI TableS8的in-vacuo标签保留；同坐标E更符合甲醇的诊断和新G热项比较不足以证明作者G介质/温度。上述来源冲突不改变两环境内已实际建立的偏好方向。",
    "reason": "所交完整答案解释可维护的中性偏好与柔性，明确边界；没有把源G标签推断成确定更正，也没有扩展到药效/膜/晶体平衡。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/s8_thermal_reuse_20261008/attempt_001/SULFONAMIDE_S8_THERMAL_RESULTS.json",
        "sha256": "6403fe05c758cc85426be67b5f282de69b29560138f5f20cf42965b18b6888cf",
        "role": "HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log",
        "sha256": "ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log",
        "sha256": "517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log",
        "sha256": "b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log",
        "sha256": "956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log",
        "sha256": "b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log",
        "sha256": "cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log",
        "sha256": "18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log",
        "sha256": "ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb",
        "role": "raw"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPprop.txt",
        "sha256": "48fe4f9abe72a98ae29120ca8cf6f25ed189ce96ab7cb0aed7cc23d7f8198a65",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPs.txt",
        "sha256": "0a128415ef802cc735f5f0510e699945d05f387a99413ee50e5c0f34912315ac",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/paths.txt",
        "sha256": "d0e8dadfd0f3669699f30a9a3f357e315ff3a4b3b9da00e71793116fd83df9ad",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/multiwfn.log",
        "sha256": "deed38a513f8dee33898d5a96a5e1d7e6a65a1aa86431d72246478bdffb567ad",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPprop.txt",
        "sha256": "830d34ef62ba31a0bdf23b7f78c1e62acbb651c9b227db97ff5e940b67f4e2c5",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPs.txt",
        "sha256": "35d1ee6e54a945f496c2d3502362ff9deb0aff9dc9854109f4d8ad6c831c91ba",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/paths.txt",
        "sha256": "5e059f8940edc18eb1c3d34c12c8308790e4a60579609d1ce042ef90048790f3",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/multiwfn.log",
        "sha256": "acd074c8c2e8b382b12bd8c98ba26b9cb39d0c86acb0855d843b7ae838b57d4e",
        "role": "raw_topology"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_objects_20261004/sulfonamide_scan_release_path/attempt_001/sulfonamide_path_closure_results.json",
        "sha256": "6f9af0180bf3852e2e2c97add648dcf726e24e01deaf8708b46178967c544d9c",
        "role": "HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/stdout.log",
        "sha256": "a1993b85c1b8da5bc66653ab552b4c5e1c6e1f86673bb35053a97aedc96b461a",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input.inp",
        "sha256": "06b6f554588b7028484534f22913fc8ecf65a135b73ce26695acea610ea580dd",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz",
        "sha256": "afc663a8c3c16e77ae26e71f0ecba05a78d382e39a2efd236d9873151bd9cf6e",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/stdout.log",
        "sha256": "4116be201706cc9eb6f586a3e3fe81b99b4b51ecf5f767c7bd5b70b2b873e12c",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input.inp",
        "sha256": "de70936bcb11cf4bacfc2a32ecfb8113fdd7000f5e889689bc05fb38ff474891",
        "role": "raw_path"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz",
        "sha256": "fed6fca599d0dcea26b8ed08d93b436767b1bc1bb70fa6023749991393267cda",
        "role": "raw_path"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 7.81 小时；67 份计时日志/67 个计时段；部分覆盖**。

已记录资源：ORCA 6.1.1；原生设置 20 线程/进程；ORCA MaxCore=2000,4000 MB/进程。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0004 · SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log) | ORCA:1757.58 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0005 · SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log) | ORCA:1755.66 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0006 · SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log) | ORCA:1796.25 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0007 · SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log) | ORCA:1549.89 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0008 · SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log) | ORCA:1139.41 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0009 · SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log) | ORCA:1537.6 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0010 · resume_SAntr_actual_direct_endpoint_free_release/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/stdout.log) | ORCA:1965.38 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0011 · resume_SNaft_actual_direct_endpoint_free_release/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/stdout.log) | ORCA:1592.94 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0012 · v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0013 · v2_SNaft_MeOH_precision_topology_normalization/attempt_001/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0014 · santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log) | ORCA:1323.37 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0015 · santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log) | ORCA:1402.11 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0016 · santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log) | ORCA:1469.14 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0017 · snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log) | ORCA:968.228 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0018 · snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log) | ORCA:812.978 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0019 · snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log) | ORCA:937.643 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0067 · author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log) | ORCA:497.971 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0069 · author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log) | ORCA:565.419 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0071 · author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log) | ORCA:456.11 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0073 · author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log) | ORCA:582.794 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0075 · author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log) | ORCA:648.66 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0077 · author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log) | ORCA:541.872 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0152 · attempt_001/point_1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_1/stdout.log) | ORCA:142.495 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0154 · attempt_001/point_2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_2/stdout.log) | ORCA:101.406 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0156 · attempt_001/point_3/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_3/stdout.log) | ORCA:108.369 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0158 · attempt_001/point_4/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_4/stdout.log) | ORCA:104.042 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0160 · attempt_001/point_5/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_5/stdout.log) | ORCA:98.994 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0162 · attempt_001/point_6/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_6/stdout.log) | ORCA:102.296 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0164 · attempt_001/point_7/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_7/stdout.log) | ORCA:99.255 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0166 · attempt_001/point_8/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_8/stdout.log) | ORCA:106.596 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0168 · attempt_001/point_9/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_9/stdout.log) | ORCA:99.836 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0169 · v2_SNaft_Zside_point9_constrained_precision/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/stdout.log) | ORCA:198.023 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0170 · attempt_001/point_10/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_10/stdout.log) | ORCA:102.189 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0172 · attempt_001/point_11/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_11/stdout.log) | ORCA:101.951 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0174 · attempt_001/point_12/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_12/stdout.log) | ORCA:100.627 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0175 · v2_SNaft_Zside_point12_constrained_precision/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/stdout.log) | ORCA:185.985 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0176 · attempt_001/point_13/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_13/stdout.log) | ORCA:109.758 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0178 · attempt_001/point_14/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_14/stdout.log) | ORCA:102.231 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0180 · attempt_001/point_15/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_15/stdout.log) | ORCA:130.475 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0182 · attempt_001/point_1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_1/stdout.log) | ORCA:100.169 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0184 · attempt_001/point_2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_2/stdout.log) | ORCA:97.455 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0186 · attempt_001/point_3/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_3/stdout.log) | ORCA:108.8 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0188 · attempt_001/point_4/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_4/stdout.log) | ORCA:90.213 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0190 · attempt_001/point_5/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_5/stdout.log) | ORCA:106.26 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0192 · attempt_001/point_6/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_6/stdout.log) | ORCA:87.262 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0194 · attempt_001/point_7/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_7/stdout.log) | ORCA:92.038 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0196 · attempt_001/point_8/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_8/stdout.log) | ORCA:90.326 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0198 · attempt_001/point_9/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_9/stdout.log) | ORCA:92.381 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0200 · attempt_001/point_10/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_10/stdout.log) | ORCA:96.91 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0202 · attempt_001/point_11/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_11/stdout.log) | ORCA:91.367 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0203 · v2_SAntr_Zside_point11_constrained_precision/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/stdout.log) | ORCA:176.032 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0204 · attempt_001/point_12/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_12/stdout.log) | ORCA:92.127 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0206 · attempt_001/point_13/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_13/stdout.log) | ORCA:95.006 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0207 · v2_SAntr_Zside_point13_constrained_precision/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/stdout.log) | ORCA:234.541 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0208 · attempt_001/point_14/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_14/stdout.log) | ORCA:93.371 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0210 · attempt_001/point_15/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_15/stdout.log) | ORCA:90.662 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |
| [E0223 · snaft_vplus_literal_vacuum_crosscheck_20260916/20260916T062855_257959_1303864/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_vacuum_crosscheck_20260916/20260916T062855_257959_1303864/orca_stdout.log) | ORCA:44.216 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0226 · snaft_vplus_literal_methanol_crosscheck_20260916/20260916T062945_350519_1330577/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_methanol_crosscheck_20260916/20260916T062945_350519_1330577/orca_stdout.log) | ORCA:53.558 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0229 · snaft_vminus_literal_vacuum_crosscheck_20260916/20260916T063045_265126_1361080/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_vacuum_crosscheck_20260916/20260916T063045_265126_1361080/orca_stdout.log) | ORCA:45.774 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0232 · snaft_vminus_literal_methanol_crosscheck_20260916/20260916T063137_087049_1385729/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_methanol_crosscheck_20260916/20260916T063137_087049_1385729/orca_stdout.log) | ORCA:57.867 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0235 · snaft_z_literal_vacuum_crosscheck_20260916/20260916T063241_185941_1420366/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_vacuum_crosscheck_20260916/20260916T063241_185941_1420366/orca_stdout.log) | ORCA:47.715 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0238 · snaft_z_literal_methanol_crosscheck_20260916/20260916T063638_266158_1534956/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_methanol_crosscheck_20260916/20260916T063638_266158_1534956/orca_stdout.log) | ORCA:50.656 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0241 · santr_vplus_literal_vacuum_crosscheck_20260916/20260916T065900_153287_2198637/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_vacuum_crosscheck_20260916/20260916T065900_153287_2198637/orca_stdout.log) | ORCA:62.252 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0244 · santr_vplus_literal_methanol_crosscheck_20260916/20260916T070008_461425_2232466/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_methanol_crosscheck_20260916/20260916T070008_461425_2232466/orca_stdout.log) | ORCA:66.469 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0247 · santr_vminus_literal_vacuum_crosscheck_20260916/20260916T070120_918988_2266770/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_vacuum_crosscheck_20260916/20260916T070120_918988_2266770/orca_stdout.log) | ORCA:58.907 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0250 · santr_vminus_literal_methanol_crosscheck_20260916/20260916T070226_896546_2300719/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_methanol_crosscheck_20260916/20260916T070226_896546_2300719/orca_stdout.log) | ORCA:70.175 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0253 · santr_si_literal_vacuum_defaultgrid_diagnostic_closure_20260915/20260916T061232_220955_816365/orca_stdout.log](../../../../runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_vacuum_defaultgrid_diagnostic_closure_20260915/20260916T061232_220955_816365/orca_stdout.log) | ORCA:48.7 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0256 · santr_si_literal_methanol_defaultgrid_diagnostic_closure_20260915/20260916T061328_053500_837719/orca_stdout.log](../../../../runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_methanol_defaultgrid_diagnostic_closure_20260915/20260916T061328_053500_837719/orca_stdout.log) | ORCA:59.727 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[2000]} |
| [E0304 · author_route_SAntr_Z_literalSI_wB97MV_DEFGRID2_control/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_wB97MV_DEFGRID2_control/attempt_001/stdout.log) | ORCA:317.667 | 正常 | {"threads":[20],"Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":[4000]} |

## 6. 已知偏差、失败分支和不能外推的结论

SI TableS8 标in vacuo但电子能更接近甲醇；其完整G条件/温度仍未证明，不能宣称精确重现该表。有限7点扫描不是连续TS/速率；小V+/V−差不建立唯一构象顺序。

```json
[
  "Table S8 says in vacuo, but its electronic values are much closer to the methanol calculation; source Gibbs environment/temperature remain unresolved.",
  "Tiny V+/V− gaps cannot establish a robust unique order or exact populations. This pass does not certify the printed SI Gibbs table.",
  "Neither coarse scans nor local contact energies prove a unique full pathway, rate, biological activity, membrane transport or crystal equilibrium."
]
```


原独立审查的 `source_exceptions_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "SI TableS8 Gibbs-energy environment and temperature are not established; electronic agreement cannot authenticate those conditions or author populations.",
  "The tiny V+/V− splitting does not support a robust unique ordering or exact populations.",
  "Finite relaxed scans and released endpoints do not certify a continuous transition-state path or rate.",
  "Local hydrogen-bond energy is not the total conformational stabilization energy; no biological, membrane or crystal-equilibrium claim is certified."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_8d8940710de08f7f.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_8d8940710de08f7f/verified_computation_reference.md)；SHA-256 `7c4e186c4323bdbea17f89436e06caf07125a2a0d061531e8c4c0ebfbbbeb4c0`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_8d8940710de08f7f.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_8d8940710de08f7f.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_8d8940710de08f7f.json) | `183510b6c9d671f9eaa25df93590a802476a089a789fb83efc417fb00aa69b9c` | evidence_or_analysis |
| E0002 | [papers/paper_8d8940710de08f7f/documents/main.pdf](../../../../papers/paper_8d8940710de08f7f/documents/main.pdf) | `a69619c718ff7d48e4dd23ce129bb8ea5a7cb58e4fcb0114ab68587d688fe9bc` | source_document |
| E0003 | [papers/paper_8d8940710de08f7f/documents/supplementary_001.pdf](../../../../papers/paper_8d8940710de08f7f/documents/supplementary_001.pdf) | `d903b517aab2dfd6c2a223020cb7d93ae6d66dc85eb489ab86c4aa854561bd13` | source_document |
| E0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_native_excerpt.json) | `c2b1a26445fb99d9a3f2858aabb2c56687598e058fab3a8ee8d0c83246988424` | native_output |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_native_excerpt.json) | `7d5a6aba7355db10bd19232a7abe2a16897a426e2e8a6c0cbbbefd6232d92282` | native_output |
| E0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `ba58d6e10bf0fe30c3b57663f42102bf9da18a3ab4b6a4fa24c86f9cd4bf42fb` | native_output |
| E0007 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `31a1b02cb0164c2662db5172ba7fd5ea31c0e02ea1b7dc7c157e998bf5532552` | native_output |
| E0008 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `18dc53b12f0328b70d9d1f5106021b8989ef61ef01c2591a6dae8d8feeba47ce` | native_output |
| E0009 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_native_excerpt.json) | `deb94057d19f1f8df76b7fbb3521e8fd8f96aced4c66dedfc22d10f722e3b57f` | native_output |
| E0010 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_native_excerpt.json) | `4116be201706cc9eb6f586a3e3fe81b99b4b51ecf5f767c7bd5b70b2b873e12c` | native_output |
| E0011 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_native_excerpt.json) | `a1993b85c1b8da5bc66653ab552b4c5e1c6e1f86673bb35053a97aedc96b461a` | native_output |
| E0012 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_native_excerpt.json) | `acd074c8c2e8b382b12bd8c98ba26b9cb39d0c86acb0855d843b7ae838b57d4e` | native_output |
| E0013 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_native_excerpt.json) | `deed38a513f8dee33898d5a96a5e1d7e6a65a1aa86431d72246478bdffb567ad` | native_output |
| E0014 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_native_excerpt.json) | `ed8b765bb4162b572bb2f64ea29457179e4bdb0e217c8d76644cbac66ee35fa0` | native_output |
| E0015 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_native_excerpt.json) | `517428ed53454202d18aebc14995ccfd6dc8a411ce9ca36ebf685c53383f6339` | native_output |
| E0016 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_native_excerpt.json) | `b6290701c8d2751dcd526c54e3b7941f419308372882aa3d421ea26b94627874` | native_output |
| E0017 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_native_excerpt.json) | `956a4cd3e89bea730390bb56efd8c28f7acdb5abd671744c30c0f6d083f046b9` | native_output |
| E0018 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_native_excerpt.json) | `b2ea0863823c7048f5ef3e44def3bbef0e045184c3d30f04e7ffa174aeddcf70` | native_output |
| E0019 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_native_excerpt.json) | `cfebdf9d1aeaecb99520802aa11751c0a577c753df887d910192ca9359422d1e` | native_output |
| E0020 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPprop.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPprop.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0020_CPprop.txt) | `48fe4f9abe72a98ae29120ca8cf6f25ed189ce96ab7cb0aed7cc23d7f8198a65` | evidence_or_analysis |
| E0021 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPprop.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPprop.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_CPprop.txt) | `830d34ef62ba31a0bdf23b7f78c1e62acbb651c9b227db97ff5e940b67f4e2c5` | evidence_or_analysis |
| E0022 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/sulfonamide_source_path_minima_topology_join.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/sulfonamide_source_path_minima_topology_join.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_sulfonamide_source_path_minima_topology_join.json) | `029cfe32f1c927f9b4d51c1c1b3fefdfb2fc28641a4188efd70e4fcfdb2ba975` | evidence_or_analysis |
| E0023 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_objects_20261004/sulfonamide_scan_release_path/attempt_001/sulfonamide_path_closure_results.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/reopen_objects_20261004/sulfonamide_scan_release_path/attempt_001/sulfonamide_path_closure_results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_sulfonamide_path_closure_results.json) | `6f9af0180bf3852e2e2c97add648dcf726e24e01deaf8708b46178967c544d9c` | evidence_or_analysis |
| E0024 | [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0024_task.md) | `ad20817a5e540a0344066f1cb5972af2b9d1bed1a40a3ea13986e732782b870d` | historical_task_binding |
| E0025 | [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/evaluation/reference_key_points.json](reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0025_reference_key_points.json) | `b40e42938ba6c376b16a153a847f7d614d68e8a9a158b1009efb00001b96422e` | historical_task_binding |
| E0026 | [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/evaluation/reference_conclusions.json](reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0026_reference_conclusions.json) | `bc8d96ed5b7907d40fdefe4452eb4e7ab2a6128fb69f7f727fbf26adb4f93f38` | historical_task_binding |
| E0027 | [tasks/v2_autonomous_research/paper_8d8940710de08f7f/agent_input/task.md](../../../v2_autonomous_research/paper_8d8940710de08f7f/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0027_task.md) | `f1a4ce9cda2489cb32a3dff9b142dfe867b76859ee47b14045645b329f75ee29` | historical_task_binding |
| E0028 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_8d8940710de08f7f/SOURCE_ROUTE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_8d8940710de08f7f/SOURCE_ROUTE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_SOURCE_ROUTE_READBACK.json) | `20c60af3c8bff0ece8fa95f3075ad4420bf584a09f9acd689d1342c8786d2b1a` | evidence_or_analysis |
| E0029 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_8d8940710de08f7f/NATIVE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_8d8940710de08f7f/NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_NATIVE_READBACK.json) | `4cccc64d53d670dd448dc3f5f872435aa47521029e518c1b98fa4665af7e3eb6` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_8d8940710de08f7f/COMPUTATION_COVERAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_8d8940710de08f7f/COMPUTATION_COVERAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_COMPUTATION_COVERAGE.json) | `94763a3a290840c27b773fdd087a9211972feca5a55090c22c209aa78d0f68e8` | evidence_or_analysis |
| E0031 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_8d8940710de08f7f.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_8d8940710de08f7f.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_paper_8d8940710de08f7f.md) | `bf5cb5df806637cd06ae31ee5662582222fd07e3e36869cd52c8f7b63d0d49ab` | evidence_or_analysis |
| E0032 | [docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `d371aa41a26b588ceb8ebb1929b857885761b946daff48a8edcc869595e20627` | historical_task_binding |
| E0033 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.inp](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_input.inp) | `c299eb25e395b29b8c0795756fd3fa97748d12c0005e4ccaa43fa0c34e364934` | input_or_analysis_code |
| E0034 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.hess](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.hess) | `c62c19412663b77155560ac2f62d2d4672b00804b36e23c90cdc5b25085ed30e` | evidence_or_analysis |
| E0035 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.inp](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_input.inp) | `bab269dca09e16de9d89f8e039cfa7a8f8e8a956a80bff8b8af9da562742075f` | input_or_analysis_code |
| E0036 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.hess](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.hess) | `701e81df3feb0ab8c77475ab7ebca245941ff58b582eca2c6a89d778b665bc2d` | evidence_or_analysis |
| E0037 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.inp](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_input.inp) | `d88b16b65979e4b3d7157ef7b2ef40698b18316e64facf3b10fc3f86184ad04f` | input_or_analysis_code |
| E0038 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.hess](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.hess) | `35df19f4f68d6d3f5432eeb649fc45d23f8a28a746914958d5c99ed17945a344` | evidence_or_analysis |
| E0039 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.inp](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_input.inp) | `29c8cac1bfbed4a19fa3c3b91aa982cffc18e1a762a1fe889c4077ec1a8c3f15` | input_or_analysis_code |
| E0040 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.hess](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.hess) | `2a388f9d91646b67aa722f353a5d76ad92f0846f6cf6afafc8a629324d3dbc95` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.inp](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0041_input.inp) | `90548484fa8195e3d89422c6183895cb2816a593b669444acf2eb64e44eccc43` | input_or_analysis_code |
| E0042 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.hess](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.hess) | `b223e7e1d461f2e0fd17af9e18812a5030a38840c5e019782229dab50d1824de` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.inp](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0043_input.inp) | `78bb14568f4ea020730da969cb55b59cc8d024eba4d1a9a2f0b277751fd6d918` | input_or_analysis_code |
| E0044 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.hess](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.hess) | `03399a2863a7e981660c54e5ca563ba8257443f4167d8b235f7e6dd36abc0199` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0045_input.inp) | `0eb1b1043075ffacfa001cde319829447d5238daecce5b44ed782d9b748eb9c7` | input_or_analysis_code |
| E0046 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess) | `2764d0d6110f98e8d247f1c4233e3cdd1893a9c8c0a241e19665dae7122b726f` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0047_input.inp) | `3a1be9c90b2e8d66d559c9dfa4e36ae8d8dcdf2c342a30dbbf7cf6062dd092e1` | input_or_analysis_code |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.hess](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.hess) | `a0b48423c60e9529b041d24384e6a6d4b914594f57e01b76dc75b289d988b9d2` | evidence_or_analysis |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0049_input.inp) | `bba1725c3ffd11f54cde79057d5c5e0ae389d85357b578fa86a101b1ae300679` | input_or_analysis_code |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess) | `c958c004d0d7cb6db94f3f4994a60875c5eaa15ae13256a5a6a3390bd18e5148` | evidence_or_analysis |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0051_input.inp) | `3a0cc5db7eb410dba6942c161067821883528d371bc803a78c9306704f22e632` | input_or_analysis_code |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.hess) | `7c9618b13aff220a75761c2c7170b9b63ef2f41294011b15aaff9946872a1756` | evidence_or_analysis |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0053_input.inp) | `06f3fd32219150f740842fc5d5bb630c7ea5d7ce42757b6ab2bd7e258624d296` | input_or_analysis_code |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.hess](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.hess) | `084edc203a0651157d0684760a2e003ba5b0ed3284f3a43ddda2f94adf3aafd8` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_input.inp) | `fac82cdf3f9e3ccb0091fe8d694435b5adefe42787e27ab6d0d447e6a09354a4` | input_or_analysis_code |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.hess) | `e10f7f0540fe8beb1a67fcf8d78a9ed657394195cbb041513a549a010087bb0e` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/s8_thermal_reuse_20261008/attempt_001/SULFONAMIDE_S8_THERMAL_RESULTS.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/s8_thermal_reuse_20261008/attempt_001/SULFONAMIDE_S8_THERMAL_RESULTS.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0057_SULFONAMIDE_S8_THERMAL_RESULTS.json) | `6403fe05c758cc85426be67b5f282de69b29560138f5f20cf42965b18b6888cf` | evidence_or_analysis |
| E0058 | [tasks/final_verified_paper_reproduction/paper_8d8940710de08f7f/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_8d8940710de08f7f/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_scoring_rules.json) | `b90bda7f443a01f7e59e67074672f1b2a3ce925a181b5cfb5fdcb50f7050d15f` | historical_task_binding |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPs.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/CPs.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_CPs.txt) | `0a128415ef802cc735f5f0510e699945d05f387a99413ee50e5c0f34912315ac` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/paths.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/paths.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_paths.txt) | `d0e8dadfd0f3669699f30a9a3f357e315ff3a4b3b9da00e71793116fd83df9ad` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPs.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/CPs.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_CPs.txt) | `35d1ee6e54a945f496c2d3502362ff9deb0aff9dc9854109f4d8ad6c831c91ba` | evidence_or_analysis |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/paths.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/paths.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_paths.txt) | `5e059f8940edc18eb1c3d34c12c8308790e4a60579609d1ce042ef90048790f3` | evidence_or_analysis |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_input.inp) | `06b6f554588b7028484534f22913fc8ecf65a135b73ce26695acea610ea580dd` | input_or_analysis_code |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_input_trj.xyz) | `afc663a8c3c16e77ae26e71f0ecba05a78d382e39a2efd236d9873151bd9cf6e` | input_or_analysis_code |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_input.inp) | `de70936bcb11cf4bacfc2a32ecfb8113fdd7000f5e889689bc05fb38ff474891` | input_or_analysis_code |
| E0066 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_input_trj.xyz) | `fed6fca599d0dcea26b8ed08d93b436767b1bc1bb70fa6023749991393267cda` | input_or_analysis_code |
| E0067 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_native_excerpt.json) | `d1e14d5fab243edda9ac69d1212744953a654a86aba24be6637e71c1b411d0a3` | native_output |
| E0068 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_input.inp) | `28e7482fbf0ba29749760b64ee3c4197f479a4e1bc9dff822620ca9dbd55b369` | input_or_analysis_code |
| E0069 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0069_native_excerpt.json) | `278629e2044078feed1b057bffea8701622c5e910bde901bfca539cfb97ae2c3` | native_output |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_input.inp) | `6e4257c9bb4f6eea8b2f0f2a9bdc4ba44242efa2eb808be79718b3dfb36853f1` | input_or_analysis_code |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_native_excerpt.json) | `f40f00255f44f2d59c71f40b9352ebbbb843f4e70d2d3cfb109c93579e5448e9` | native_output |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_input.inp) | `b7e203be5c5f144ccbd90b2135ed4d7ae960f61c602f2c774262e35a6bc28077` | input_or_analysis_code |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_native_excerpt.json) | `4b7e166c07edf42189fa1d6d40991584d9716f0ce5f30787fdbc645316bc1076` | native_output |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_input.inp) | `af2de3b8d8a00de18fc05f9b9ad0a9926b24028d4fc0de5578fba741821fe3d1` | input_or_analysis_code |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_native_excerpt.json) | `27df44985bc6fbe2d091905685b717dcc019d3cf2c23bbf58b53b1bef5e5027e` | native_output |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0076_input.inp) | `6b3913638a5cd2ffe46368f62e4f35d7368e6a0a1ca85c8dcc5a494fb1f5ea31` | input_or_analysis_code |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0077_native_excerpt.json) | `9fea9ae40b61549eadca35936b68929a643237b7a747524bb6207d5b99dbaeaa` | native_output |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0078_input.inp) | `19fa2442afd6ae7fe1419c67f2d18db1c49f976b0632caa81037af1a283196f8` | input_or_analysis_code |
| E0079 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/OPT_STOP_REVIEW_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W04/papers/paper_8d8940710de08f7f/OPT_STOP_REVIEW_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0079_OPT_STOP_REVIEW_20261007.json) | `50dedd40f3b13f4d9802d42f1e480e140fabb4bebad946586f0480f82e9e52f2` | evidence_or_analysis |
| E0080 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W04_RETURNED_JOB_INTAKE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W04_RETURNED_JOB_INTAKE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0080_W04_RETURNED_JOB_INTAKE.json) | `46d18cf5955fe1b814a482e0e6c3619ff53027942a48df73c44ffd99715e76f4` | evidence_or_analysis |
| E0081 | [tasks/final_verified_paper_reproduction/paper_8d8940710de08f7f/evaluation/verified_computation_reference.md](../../../final_verified_paper_reproduction/paper_8d8940710de08f7f/evaluation/verified_computation_reference.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0081_verified_computation_reference.md) | `d371aa41a26b588ceb8ebb1929b857885761b946daff48a8edcc869595e20627` | historical_task_binding |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/source_s8_paired12_reuse_20261001.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/source_s8_paired12_reuse_20261001.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0082_source_s8_paired12_reuse_20261001.json) | `5d273a57c5d3a91e3f50101317f343d88c49599cc35d20e5931caddf624d7dc8` | evidence_or_analysis |
| E0083 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_8d8940710de08f7f/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_8d8940710de08f7f/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0083_task.md) | `f1a4ce9cda2489cb32a3dff9b142dfe867b76859ee47b14045645b329f75ee29` | historical_task_binding |
| E0084 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_8d8940710de08f7f/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_8d8940710de08f7f/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0084_reference_key_points.json) | `b40e42938ba6c376b16a153a847f7d614d68e8a9a158b1009efb00001b96422e` | historical_task_binding |
| E0085 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_8d8940710de08f7f/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_8d8940710de08f7f/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0085_reference_conclusions.json) | `bc8d96ed5b7907d40fdefe4452eb4e7ab2a6128fb69f7f727fbf26adb4f93f38` | historical_task_binding |
| E0086 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_8d8940710de08f7f/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_8d8940710de08f7f/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0086_scoring_rules.json) | `98a6bda4c94e92ebe7316b3e1ee0a4f09e762864db32bfe30911b861c369333e` | historical_task_binding |
| E0087 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_8d8940710de08f7f/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_8d8940710de08f7f/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0087_task.md) | `ad20817a5e540a0344066f1cb5972af2b9d1bed1a40a3ea13986e732782b870d` | historical_task_binding |
| E0088 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_8d8940710de08f7f/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_8d8940710de08f7f/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0088_reference_key_points.json) | `b40e42938ba6c376b16a153a847f7d614d68e8a9a158b1009efb00001b96422e` | historical_task_binding |
| E0089 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_8d8940710de08f7f/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_8d8940710de08f7f/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0089_reference_conclusions.json) | `bc8d96ed5b7907d40fdefe4452eb4e7ab2a6128fb69f7f727fbf26adb4f93f38` | historical_task_binding |
| E0090 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_8d8940710de08f7f/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_8d8940710de08f7f/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0090_scoring_rules.json) | `98a6bda4c94e92ebe7316b3e1ee0a4f09e762864db32bfe30911b861c369333e` | historical_task_binding |
| E0091 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/7e48901e63a15059_W04.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/7e48901e63a15059_W04.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0091_7e48901e63a15059_W04.json) | `7e48901e63a15059936089b33ece6b774151892dbe137228118e7f852a03f9f6` | evidence_or_analysis |
| E0092 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W04.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W04.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0092_W04.json) | `7e48901e63a15059936089b33ece6b774151892dbe137228118e7f852a03f9f6` | evidence_or_analysis |
| E0093 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/d0109278318ce648_paper_8d8940710de08f7f_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/d0109278318ce648_paper_8d8940710de08f7f_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0093_d0109278318ce648_paper_8d8940710de08f7f_delivery_integrity.json) | `d0109278318ce648006e60aac1a4a313b4eb3110fbf7d7b4fc4cf210b003dad3` | evidence_or_analysis |
| E0094 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_8d8940710de08f7f_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_8d8940710de08f7f_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0094_paper_8d8940710de08f7f_delivery_integrity.json) | `d0109278318ce648006e60aac1a4a313b4eb3110fbf7d7b4fc4cf210b003dad3` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/1fa1d5f0940cbcbe_paper_8d8940710de08f7f_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/1fa1d5f0940cbcbe_paper_8d8940710de08f7f_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0095_1fa1d5f0940cbcbe_paper_8d8940710de08f7f_primary_pages.json) | `1fa1d5f0940cbcbe1dea59336db78e1a57553b60b7904ebe067c096862303857` | evidence_or_analysis |
| E0096 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_8d8940710de08f7f_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_8d8940710de08f7f_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0096_paper_8d8940710de08f7f_primary_pages.json) | `1fa1d5f0940cbcbe1dea59336db78e1a57553b60b7904ebe067c096862303857` | evidence_or_analysis |
| E0097 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/08259aabc1ca228b_paper_8d8940710de08f7f_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/08259aabc1ca228b_paper_8d8940710de08f7f_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0097_08259aabc1ca228b_paper_8d8940710de08f7f_native_readback.json) | `08259aabc1ca228bfc168868b011e28413a925eda69134cd64c0385cb76ecf48` | evidence_or_analysis |
| E0098 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_8d8940710de08f7f_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_8d8940710de08f7f_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0098_paper_8d8940710de08f7f_native_readback.json) | `08259aabc1ca228bfc168868b011e28413a925eda69134cd64c0385cb76ecf48` | evidence_or_analysis |
| E0099 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0099_entrypoint.sh) | `ef1aa89ee202f3d266e5cfaa839a0589f50f7a5ad66679e76541be2d1d042058` | input_or_analysis_code |
| E0100 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0100_input_trj.xyz) | `acc5bed4521fcd75abbb8d34dc835b97fff26730e6c96eee03ab11941e82b9fa` | input_or_analysis_code |
| E0101 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0101_input.xyz) | `d97bf2f5c6ce5a8809bfc18957067edf50bdb18bf547ac8fe5846bae835bc3b9` | input_or_analysis_code |
| E0102 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0102_entrypoint.sh) | `ef1aa89ee202f3d266e5cfaa839a0589f50f7a5ad66679e76541be2d1d042058` | input_or_analysis_code |
| E0103 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0103_input_trj.xyz) | `3659bfb5cc396d7fe5c21199436120086fa144eda5cc8f181b0d329b20d820b4` | input_or_analysis_code |
| E0104 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_V_plus_methanol_D3off_grid3_optfreq/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0104_input.xyz) | `a16a2a174ed0379291613a633fbbceac5d11db44f34164543e162058b348f02f` | input_or_analysis_code |
| E0105 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0105_entrypoint.sh) | `ef1aa89ee202f3d266e5cfaa839a0589f50f7a5ad66679e76541be2d1d042058` | input_or_analysis_code |
| E0106 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0106_input_trj.xyz) | `7f2dec65f3c701098878248af5e7925d6bcd9b4890b2c5e8839b7260696a8058` | input_or_analysis_code |
| E0107 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SAntr_Z_methanol_D3off_grid3_optfreq/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0107_input.xyz) | `45cce806e2856be12eab8d66844cf8d4334eb28eefd4f025c71207dc7e4a67bf` | input_or_analysis_code |
| E0108 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0108_entrypoint.sh) | `ef1aa89ee202f3d266e5cfaa839a0589f50f7a5ad66679e76541be2d1d042058` | input_or_analysis_code |
| E0109 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0109_input_trj.xyz) | `3b8f93604c9da9a87fd9f0d13d3449b6eedd58cb5e46363440ad107032efc81c` | input_or_analysis_code |
| E0110 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/final.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/final.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0110_final.xyz) | `60747a3656ee1014f37745487042ffc7f47ebabeab28fa9b8d8e0216dd581c28` | input_or_analysis_code |
| E0111 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_V_minus_methanol_D3off_grid3_optfreq/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0111_input.xyz) | `82466a3e884a8cd838fa7c0f640d201dfc935fd332f45b6e9ecd731064931efb` | input_or_analysis_code |
| E0112 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0112_entrypoint.sh) | `ef1aa89ee202f3d266e5cfaa839a0589f50f7a5ad66679e76541be2d1d042058` | input_or_analysis_code |
| E0113 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0113_input_trj.xyz) | `ca7e265bbf58999d407203d0b59b562fea9b8ba6c26a09bafea8ff094803b647` | input_or_analysis_code |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/final.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/final.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0114_final.xyz) | `6a3204861882cac2361f3e63d34a7e9bf530c87a5463709ccde80ccae56fd9e6` | input_or_analysis_code |
| E0115 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Vplus_methanol_grid3_repair/attempt_002/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0115_input.xyz) | `e98297ebc4b3ad91c5f585d539411d77fc16341a16091a575e8d6c911f90cace` | input_or_analysis_code |
| E0116 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0116_entrypoint.sh) | `ef1aa89ee202f3d266e5cfaa839a0589f50f7a5ad66679e76541be2d1d042058` | input_or_analysis_code |
| E0117 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0117_input_trj.xyz) | `56ecba502babb85cb11ce06a990701bb8c1e2537de1ea64164bfc093134bd2fb` | input_or_analysis_code |
| E0118 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/final.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/final.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0118_final.xyz) | `35e51e69f951d174e1636e1d5a1a6ec44d010d87a521132a140f04d68f6677c8` | input_or_analysis_code |
| E0119 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/SNaft_Z_methanol_D3off_grid3_optfreq/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0119_input.xyz) | `96de276cea04fb591f896f643b014b59a3e5646c8dbc08058292690c2ee144ef` | input_or_analysis_code |
| E0120 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0120_entrypoint.sh) | `3d2a138ddf7cda208c0d567c4dee515c6d8c3cac455d1d103fea2dcc890d6880` | input_or_analysis_code |
| E0121 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SAntr_actual_direct_endpoint_free_release/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0121_input.xyz) | `b2cda33c0cecb540cb4e814bb9ee9a318a195f3f1b6108fd9d350e2e835fca6e` | input_or_analysis_code |
| E0122 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0122_entrypoint.sh) | `3d2a138ddf7cda208c0d567c4dee515c6d8c3cac455d1d103fea2dcc890d6880` | input_or_analysis_code |
| E0123 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/resume_SNaft_actual_direct_endpoint_free_release/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0123_input.xyz) | `1134f9d0e9b6c0fe961d5e2e88725bf233896866f78ec31749d6e702561f807d` | input_or_analysis_code |
| E0124 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0124_entrypoint.sh) | `84112459f3ac719ea541540b57e47a1fb6e7159503ce8a1b58546d97e5bf381c` | input_or_analysis_code |
| E0125 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/runtime.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/runtime.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0125_runtime.py) | `ea431f4389d45d84635b866b4fe113f9589c1fa471857689a8aa417674ab88fe` | input_or_analysis_code |
| E0126 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/input.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Vplus_MeOH_topology_normalization/attempt_001/input.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0126_input.json) | `cf40352540127bab2351fa48fc2180af6a6daf2a866fc20c91a0007d8b3fdfee` | evidence_or_analysis |
| E0127 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0127_entrypoint.sh) | `84112459f3ac719ea541540b57e47a1fb6e7159503ce8a1b58546d97e5bf381c` | input_or_analysis_code |
| E0128 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/runtime.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/runtime.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0128_runtime.py) | `ea431f4389d45d84635b866b4fe113f9589c1fa471857689a8aa417674ab88fe` | input_or_analysis_code |
| E0129 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/input.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_precision_topology_normalization/attempt_001/input.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0129_input.json) | `5e15bd69b491eb27f2a70f5f85a3cc896527c80c13868b36fc52ec92a71773b2` | evidence_or_analysis |
| E0130 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input_trj.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0130_input_trj.xyz) | `af4494c1b5ccb53e9739f166da0fa1637bd8c4957101c182fc2f85425480f9f3` | input_or_analysis_code |
| E0131 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_minus_vacuum_grid3_minimum_20260914/20260914T123834_333288_343/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0131_input.xyz) | `9fddc91e4043cb8a0cfd245b29e45f7bc47c09443190011edaddc8202463cf7f` | input_or_analysis_code |
| E0132 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input_trj.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0132_input_trj.xyz) | `a51e3b1d1db5c76825ced6a28f74671f457a3ca6858db625b510b4ae314cff76` | input_or_analysis_code |
| E0133 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_v_plus_vacuum_grid3_minimum_20260914/20260914T123834_353497_267/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0133_input.xyz) | `031932409ea32b4d15fa4e6906bc4f2c2c1417f9881cf48be8074ff0803ed856` | input_or_analysis_code |
| E0134 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input_trj.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0134_input_trj.xyz) | `27813aadd67bffe13da30a8756e7d6bef493a6e7c4d3cf41e808b33e91e39252` | input_or_analysis_code |
| E0135 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/santr_z_vacuum_grid3_minimum_20260914/20260914T124824_093789_344/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0135_input.xyz) | `303443746e90199854d7d621d09644e83093b05b642a921a390df57aaf57188c` | input_or_analysis_code |
| E0136 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input_trj.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0136_input_trj.xyz) | `a0790b1a3e3c0f649d1192d83dd52e0b225d3cb1edd709c9894508e0cd52321e` | input_or_analysis_code |
| E0137 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_minus_vacuum_grid3_minimum_20260914/20260914T123010_689249_577/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0137_input.xyz) | `4e8c610d978a6a3185b129c40f789a2f90792f876503ab0e78b583987794f005` | input_or_analysis_code |
| E0138 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input_trj.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0138_input_trj.xyz) | `36440781f7643e2c82a77453999f1a25877a6403a07cd9dfdd651cf207771bb4` | input_or_analysis_code |
| E0139 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_v_plus_vacuum_grid3_minimum_20260914/20260914T123010_692980_421/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0139_input.xyz) | `5b3762b50cae43a2c621d9451dc6b548c8db2625b5e4c7ca7692f11caf1c369e` | input_or_analysis_code |
| E0140 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input_trj.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0140_input_trj.xyz) | `539ec24c7cd25e5231505f7bfe7d499971f025f84c31b64cfa1218ff4626ce17` | input_or_analysis_code |
| E0141 | [docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.xyz](../../../../docs/v2_verification/history/verification/group_5/paper_8d8940710de08f7f/provenance/qzcli_hpc/snaft_z_uniform_grid3_minimum_20260915/20260915T100426_075876_187/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0141_input.xyz) | `979c41bfd164339d53184e451d46566f3766a02ff2ab57c04f838e4c483314a6` | input_or_analysis_code |
| E0142 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/provenance/source_text/main.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/provenance/source_text/main.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0142_main.txt) | `2f54aa3113325e5818f04441ca89a46af9c945081b81bac595eb7140ce4177cd` | evidence_or_analysis |
| E0143 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/provenance/source_text/supplementary_001.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/provenance/source_text/supplementary_001.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0143_supplementary_001.txt) | `981583f2e2b53bf85773203d5364046a9fad17a326b7ff0ae824af699c3c3c5e` | evidence_or_analysis |
| E0144 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/sulfonamide_reuse.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/sulfonamide_reuse.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0144_sulfonamide_reuse.json) | `df1d4209ad30e08f8cf227b54af41e80b2a7138c35eb0c13969df06b3bf36641` | evidence_or_analysis |
| E0145 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/gas_profile_returns.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/gas_profile_returns.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0145_gas_profile_returns.json) | `291d0a54bc5fde7c0d54c9b4d9409d9451fc89f2e414ed1e3c3f3ddbc04d3cca` | evidence_or_analysis |
| E0146 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/sulfonamide_zside_returns.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/sulfonamide_zside_returns.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0146_sulfonamide_zside_returns.json) | `aaf692aa8931593b9022ea5c49dcf2eeab5d347198cf2122dca67a34eeed2935` | evidence_or_analysis |
| E0147 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/return_precision_returns.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/return_precision_returns.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0147_return_precision_returns.json) | `b11d5ddfa72d2d652fdfa43b7eaf6dd548d05ee0bc1ce80b2737f3b85331d17a` | evidence_or_analysis |
| E0148 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/zside_returned_mapping_returns.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/zside_returned_mapping_returns.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0148_zside_returned_mapping_returns.json) | `39942e77648e10ca6000c23d645e897765902e4d9d469fb4a6e501eb9af1094e` | evidence_or_analysis |
| E0149 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/snaft_scan_direction_comparison.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/snaft_scan_direction_comparison.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0149_snaft_scan_direction_comparison.json) | `c33e24be1164387f8c9071c6d8ba0f5912766400bf2310cc6be220fc24ba384c` | evidence_or_analysis |
| E0150 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/qtaim_sensitivity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/qtaim_sensitivity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0150_qtaim_sensitivity.json) | `b827a353e9d683369af8348c4c146451b7746c80b826d27988b834c20a012624` | evidence_or_analysis |
| E0151 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/santr_topology_returns.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/santr_topology_returns.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0151_santr_topology_returns.json) | `0f6661ac7c1af0f33207f97188636fe05ac2a60af4e72d2dd18cade4dcb15907` | evidence_or_analysis |
| E0152 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0152_native_excerpt.json) | `120d097db9db1d77fbcde1bbe2beca723bf28c307cbc390bf9e63168767301d6` | native_output |
| E0153 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.001.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.001.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0153_input.001.xyz) | `240c9786c2ba5615ddf896b08498885fed9291ecbc713be6568413070c902852` | input_or_analysis_code |
| E0154 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_2/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0154_native_excerpt.json) | `0dc781940834597ce2e5a6c50d946ea74e8b3176bdccfde5aeef2a563c6e092e` | native_output |
| E0155 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.002.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.002.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0155_input.002.xyz) | `df590a334a55e6be7533a368e27c1b184ab23c0ba452fbcdf085e802aa3ac4ab` | input_or_analysis_code |
| E0156 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_3/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_3/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0156_native_excerpt.json) | `85a4d9a533501cb1c3bf6b1ecf078c9e60db6ae87eb4294b56bfb7bde6df9cd7` | native_output |
| E0157 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.003.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.003.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0157_input.003.xyz) | `984a97d79a25c7e60f47b23a38e61425df51283f5abfdd93565d033df7ae50fe` | input_or_analysis_code |
| E0158 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_4/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_4/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0158_native_excerpt.json) | `486478a94f8f1d5a6990a4a89287bebfa50dd86f4dd27d7f2fb91e5f274103f2` | native_output |
| E0159 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.004.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.004.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0159_input.004.xyz) | `7a4798d7ef70aeec2a034e61b5bf45e0213e9defbc5f0e287b812f7616db43bc` | input_or_analysis_code |
| E0160 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_5/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_5/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0160_native_excerpt.json) | `298506a873ec5185f23c0a172213f26d03f08124dddebfb356ad9b67fe72d908` | native_output |
| E0161 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.005.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.005.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0161_input.005.xyz) | `76fb7695a486979679d46f13f7ce692de9b77bb9b8f464e18c7c55c1f948736b` | input_or_analysis_code |
| E0162 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_6/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0162_native_excerpt.json) | `04126d58dc5a9500c9008baee646da69c5b130e17f15f613e7d157f7dc6cf3a7` | native_output |
| E0163 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.006.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.006.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0163_input.006.xyz) | `b6df9bddc5c61b0e58461785be1cd28cb0453635cd0000a188dc40854fb9e1de` | input_or_analysis_code |
| E0164 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_7/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_7/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0164_native_excerpt.json) | `5e547979ca72c4c798dc9a2d4255ee7a25a1eb3f8b16e643cd2c82954ef6870b` | native_output |
| E0165 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.007.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.007.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0165_input.007.xyz) | `1df863a011fa5c5e39945fcec69a71b078bf0a5a75cb6ba493dbcf17654bc774` | input_or_analysis_code |
| E0166 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_8/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_8/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0166_native_excerpt.json) | `ebb9ba046994f404e1794704b62a9a5a9deb0c91adcf277d4d24449430800683` | native_output |
| E0167 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.008.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.008.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0167_input.008.xyz) | `a0f5ba8aca842152da1c82aa5c5a8632160685cab0b969b71bd315550809a16d` | input_or_analysis_code |
| E0168 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_9/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_9/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0168_native_excerpt.json) | `2e5704a1fbcfd0c9a42cf7aa99e24c45e084c7671233e82c6eac0a5f92804f8c` | native_output |
| E0169 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0169_native_excerpt.json) | `56b705e3dadbedf0570d89b3dc457c29d873f4a730ad44f6a1ca7bb156020835` | native_output |
| E0170 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_10/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_10/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0170_native_excerpt.json) | `918c2da136a5ec58e8fc3d826568a4137073855befd01622fe17c062a3797033` | native_output |
| E0171 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.010.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.010.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0171_input.010.xyz) | `74c90793eefe26a0c97fa3af97adbcbc82183bbad4d1db7120ed3f64d2eb66a1` | input_or_analysis_code |
| E0172 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_11/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_11/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0172_native_excerpt.json) | `e4e82845767aa18d3049b24563fe928c9bdcf1e7dd81201e516f0af64f77720c` | native_output |
| E0173 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.011.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.011.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0173_input.011.xyz) | `3dd1f545750ab0995ee9d71d45a8f689cc6546fa013966e375d28c91ecee0e5b` | input_or_analysis_code |
| E0174 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_12/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_12/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0174_native_excerpt.json) | `0f52b7e796f9b14eec2afa13558d1a4f3b57983fe42022a41c2a3a2ab9d35212` | native_output |
| E0175 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0175_native_excerpt.json) | `7d5b1130682559caf0a16445664cc1563f615ea0eef1f65a682f521ccceb0feb` | native_output |
| E0176 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_13/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_13/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0176_native_excerpt.json) | `d7d688262e7841eba2d45d2bda20b7a0bb4c9306ed64cf4e2db2eca2541df091` | native_output |
| E0177 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.013.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.013.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0177_input.013.xyz) | `b1271d058fecbcd77e81a39e4096394dab7416cb1a4990e452b095761263f09e` | input_or_analysis_code |
| E0178 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_14/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_14/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0178_native_excerpt.json) | `dda099e6515bb5f007c973557854dccccc99e79dae2c38c500d235e932ed4aab` | native_output |
| E0179 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.014.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.014.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0179_input.014.xyz) | `611ede8949312d62d4857ea7be95a66e3b2a163bf37154dd85d05d9825c96f54` | input_or_analysis_code |
| E0180 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_15/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_15/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0180_native_excerpt.json) | `ad112798d1c8cd431860deea67a4b6a1ed248e7d3d2fff849f3d816bcc03f5cf` | native_output |
| E0181 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.015.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_MeOH_source_CSNC_Zside_scan15/attempt_001/input.015.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0181_input.015.xyz) | `143b4b6dfe08ffda42735433031995237d020b85d363f4e202c6c75c5ac92614` | input_or_analysis_code |
| E0182 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_1/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_1/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0182_native_excerpt.json) | `3826111686f9b2f4fc9a3b9a0cfde3055619ed65536fcbf74bd7fb636d417ccb` | native_output |
| E0183 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.001.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.001.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0183_input.001.xyz) | `7d298facbe182a6baefba8b163fab3d9f3756f797d9da9e43fee543ffb28c9cf` | input_or_analysis_code |
| E0184 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_2/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_2/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0184_native_excerpt.json) | `1075b4b184b6e2d750aac44a44806c5aae9887c52fab75ec2176faf0b60bed04` | native_output |
| E0185 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.002.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.002.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0185_input.002.xyz) | `b61bbfdd60f748e53436f179a2a4e3f16dcf0c284b8bb0d3bb997d37ed15f1ff` | input_or_analysis_code |
| E0186 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_3/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_3/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0186_native_excerpt.json) | `6aab542e3da34ce5975df25ba6999f3d0a4031bf50e8ca2eee326ddb37862921` | native_output |
| E0187 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.003.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.003.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0187_input.003.xyz) | `6d92b069f0f1cf8402023aab9de98c645a81005f2eaa78599b4629defb82e8bd` | input_or_analysis_code |
| E0188 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_4/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_4/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0188_native_excerpt.json) | `0a787489f29c18e9ea64b560ed4659cef5d2060d4d1e984ef7266c3d8f0b0320` | native_output |
| E0189 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.004.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.004.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0189_input.004.xyz) | `de8645075d2fb874315be2d402826dbe9822807b80f32c225187256834445736` | input_or_analysis_code |
| E0190 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_5/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_5/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0190_native_excerpt.json) | `b8cdce2cc063ec460d44317995dadc57d35ff3f0eb3f9fbfe477197ef6b1e66b` | native_output |
| E0191 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.005.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.005.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0191_input.005.xyz) | `d0b63e0ea27f173ae4ff90b499b11104264a6eb020eb8c6061424640165d7e71` | input_or_analysis_code |
| E0192 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_6/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0192_native_excerpt.json) | `15fc4ae0d2f134e5e10950b94239dc2b7e4df674294f94c785d75ff5aa31bcf0` | native_output |
| E0193 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.006.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.006.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0193_input.006.xyz) | `201bd866fd88784e11f131b0cf71f1784b33ab7e6a413d7862bef7c0149447d7` | input_or_analysis_code |
| E0194 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_7/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_7/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0194_native_excerpt.json) | `47f9b32cd85496d5521811bd60686b92b45ad3b0e083daeddd02ddfc075c898c` | native_output |
| E0195 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.007.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.007.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0195_input.007.xyz) | `6fdf8308f87b4f2777ead92da271913e329fc133471fee2dd98c230394578eba` | input_or_analysis_code |
| E0196 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_8/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_8/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0196_native_excerpt.json) | `a48b43e1b53af421ef95c99bca9d4632b690526fa7a0c1bfc6a8743e0139eb3d` | native_output |
| E0197 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.008.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.008.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0197_input.008.xyz) | `5396dcd22b7f34fdedc7293fd003c70f524d8de656748a127995bb474106289b` | input_or_analysis_code |
| E0198 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_9/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_9/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0198_native_excerpt.json) | `d89bf18a62801512d5c42fdc1867f2e13eb3616eea5d23a497df6b20b51a380f` | native_output |
| E0199 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.009.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.009.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0199_input.009.xyz) | `d68a9b05190f7786026c5f75fc25d48f10d9018a3535818c14c53b66d871521b` | input_or_analysis_code |
| E0200 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_10/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_10/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0200_native_excerpt.json) | `1a3d063b4eb3cbf77aa832599e0a3e1eb892315a3db092a8a2968b54a073659f` | native_output |
| E0201 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.010.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.010.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0201_input.010.xyz) | `eb0e9012f20d0897df658acd7209e97b756c2d633c0cb27243b7312484886087` | input_or_analysis_code |
| E0202 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_11/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_11/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0202_native_excerpt.json) | `c8da16188e0edaac99294530d5a4c4c19e1e850018ef2fd59a389ed7213e3065` | native_output |
| E0203 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0203_native_excerpt.json) | `0efb2f6609cd74b9a1cc2d1655dd63da02eba628d528c81b9a566dec9c87f4b8` | native_output |
| E0204 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_12/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_12/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0204_native_excerpt.json) | `28e0eee1104e9d997b22d27b2cc7422c7da7142264e4527f3790f9549e382dc3` | native_output |
| E0205 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.012.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.012.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0205_input.012.xyz) | `5cf178c4ae377e8b74477bd96a14b30e95f6720f5a88d32c5acdc13e19973a7e` | input_or_analysis_code |
| E0206 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_13/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_13/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0206_native_excerpt.json) | `4d72334ec46924dfb5ddf3c7a8d45310f2023338f643be7e085e6e1965e572f2` | native_output |
| E0207 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0207_native_excerpt.json) | `db77a4b411499ae541c2f3bbd68eb48e7d9436edfe39ed170fb815ba319a9dbe` | native_output |
| E0208 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_14/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_14/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0208_native_excerpt.json) | `444987cc156e2cfb27a69ae4b4e827d5f18898963a5649bc9aa64ef850a1b2e9` | native_output |
| E0209 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.014.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.014.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0209_input.014.xyz) | `e6ce68a694dba5d7f87272b07f24d9a639c551b01ff3757d76569f5f7c346d0a` | input_or_analysis_code |
| E0210 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_15/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_15/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0210_native_excerpt.json) | `17e1f83c82e10ab31242a9c3a56c225f676526246b45c1ef33d4ed8b3ba99a88` | native_output |
| E0211 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.015.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_MeOH_source_CSNC_Zside_scan15/attempt_001/input.015.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0211_input.015.xyz) | `e7049f758ae7d9d262523d01c3ce260d21ced1ecec8ec43e31341fedcbad6fe5` | input_or_analysis_code |
| E0212 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/resume_after_quota_20261002/SULFONAMIDE_SOURCE_TABLE4.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group2/resume_after_quota_20261002/SULFONAMIDE_SOURCE_TABLE4.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0212_SULFONAMIDE_SOURCE_TABLE4.json) | `7de6b8fc85975e9bb7080ba9e40b8e26442f64e305c313cfb0716d5eb65fbcb3` | evidence_or_analysis |
| E0213 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_8d8940710de08f7f/REVIEW_PACKAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_8d8940710de08f7f/REVIEW_PACKAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0213_REVIEW_PACKAGE.json) | `34b9be7f220de669061ae9e2727f650e469c2ce675d71bc8d3f73eb3bdc72fca` | evidence_or_analysis |
| E0214 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Vplus_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0214_entrypoint.sh) | `a73e01755be30aea573e93e4d431475bd3a920b9f58fdefb6440743e0f3c9c2d` | input_or_analysis_code |
| E0215 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0215_entrypoint.sh) | `a73e01755be30aea573e93e4d431475bd3a920b9f58fdefb6440743e0f3c9c2d` | input_or_analysis_code |
| E0216 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SNaft_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0216_entrypoint.sh) | `a73e01755be30aea573e93e4d431475bd3a920b9f58fdefb6440743e0f3c9c2d` | input_or_analysis_code |
| E0217 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_plus_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0217_entrypoint.sh) | `a73e01755be30aea573e93e4d431475bd3a920b9f58fdefb6440743e0f3c9c2d` | input_or_analysis_code |
| E0218 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_V_minus_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0218_entrypoint.sh) | `a73e01755be30aea573e93e4d431475bd3a920b9f58fdefb6440743e0f3c9c2d` | input_or_analysis_code |
| E0219 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_MeOH_wB97MV_dipole/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0219_entrypoint.sh) | `a73e01755be30aea573e93e4d431475bd3a920b9f58fdefb6440743e0f3c9c2d` | input_or_analysis_code |
| E0221 | [docs/v2_verification/history/v2_completion_execution_20260930T1255Z/AUTHOR2_S8_COORDINATOR_SOURCE_CHECK.json](../../../../docs/v2_verification/history/v2_completion_execution_20260930T1255Z/AUTHOR2_S8_COORDINATOR_SOURCE_CHECK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0221_AUTHOR2_S8_COORDINATOR_SOURCE_CHECK.json) | `041875e97a5f67303facbbc72c96fe473c2f7fb504260ebd4ac6109a9b037f20` | evidence_or_analysis |
| E0222 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_vacuum_crosscheck_20260916/20260916T062855_257959_1303864/input.inp](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_vacuum_crosscheck_20260916/20260916T062855_257959_1303864/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0222_input.inp) | `99b6253fb4fe511c2c70ad5d9466e39d4bfcf195f14d3e36fb661a73b2c4ab5a` | input_or_analysis_code |
| E0223 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_vacuum_crosscheck_20260916/20260916T062855_257959_1303864/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_vacuum_crosscheck_20260916/20260916T062855_257959_1303864/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0223_native_excerpt.json) | `7445eaad56fa66c80a133d1e7770e9b92bf1f101dd8c0cf697733013e0b5e0b2` | native_output |
| E0224 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_vacuum_crosscheck_20260916/20260916T062855_257959_1303864/status.json](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_vacuum_crosscheck_20260916/20260916T062855_257959_1303864/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0224_status.json) | `c6c9cc1265fa9063a31c41ed11601fdafad0542b3bd20715b715317a53f5538c` | evidence_or_analysis |
| E0225 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_methanol_crosscheck_20260916/20260916T062945_350519_1330577/input.inp](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_methanol_crosscheck_20260916/20260916T062945_350519_1330577/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0225_input.inp) | `2f155a2495fc9745bf97c19d97e266d99241225fc60230cdfa38c3bf3855a5ca` | input_or_analysis_code |
| E0226 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_methanol_crosscheck_20260916/20260916T062945_350519_1330577/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_methanol_crosscheck_20260916/20260916T062945_350519_1330577/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0226_native_excerpt.json) | `efc3bea1ed4ea7f730bfe6787c4a3cd0cfffc4d382c3fa0a27fe66007da7598e` | native_output |
| E0227 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_methanol_crosscheck_20260916/20260916T062945_350519_1330577/status.json](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vplus_literal_methanol_crosscheck_20260916/20260916T062945_350519_1330577/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0227_status.json) | `d053fb822c7c94fa65750d0ad25c69909260d04812beba9218987bf9bf605378` | evidence_or_analysis |
| E0228 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_vacuum_crosscheck_20260916/20260916T063045_265126_1361080/input.inp](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_vacuum_crosscheck_20260916/20260916T063045_265126_1361080/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0228_input.inp) | `7a35c54e8b40d15c6c211fda25c78faa38992991233cfc80da5e25361dc1b639` | input_or_analysis_code |
| E0229 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_vacuum_crosscheck_20260916/20260916T063045_265126_1361080/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_vacuum_crosscheck_20260916/20260916T063045_265126_1361080/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0229_native_excerpt.json) | `e3383fcef1f9ab8e1a41ee60ab738d4398a537656e8aea6bc97b6c3fbfe40445` | native_output |
| E0230 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_vacuum_crosscheck_20260916/20260916T063045_265126_1361080/status.json](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_vacuum_crosscheck_20260916/20260916T063045_265126_1361080/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0230_status.json) | `7e3303944bb8ec09195d5b1125c10f0167f11308f6021ac74e1a2688bf8d0354` | evidence_or_analysis |
| E0231 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_methanol_crosscheck_20260916/20260916T063137_087049_1385729/input.inp](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_methanol_crosscheck_20260916/20260916T063137_087049_1385729/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0231_input.inp) | `d51dc2f588804d001b3b24f1f958fb4876b15a2c0c84649bcd7d61a43ff5908f` | input_or_analysis_code |
| E0232 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_methanol_crosscheck_20260916/20260916T063137_087049_1385729/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_methanol_crosscheck_20260916/20260916T063137_087049_1385729/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0232_native_excerpt.json) | `384019640c917234b36efe3323756cbba33cfe9d179617ba6449bc4d61eca4c4` | native_output |
| E0233 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_methanol_crosscheck_20260916/20260916T063137_087049_1385729/status.json](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_vminus_literal_methanol_crosscheck_20260916/20260916T063137_087049_1385729/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0233_status.json) | `5ee4d8debea22671953aa54064e0bf5241e502d3bd29c1e83a931befdaf5274e` | evidence_or_analysis |
| E0234 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_vacuum_crosscheck_20260916/20260916T063241_185941_1420366/input.inp](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_vacuum_crosscheck_20260916/20260916T063241_185941_1420366/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0234_input.inp) | `5c9be28cecae6e91e9436270aad4b143f715be596f8f39c2dc6cd18b0e29c96e` | input_or_analysis_code |
| E0235 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_vacuum_crosscheck_20260916/20260916T063241_185941_1420366/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_vacuum_crosscheck_20260916/20260916T063241_185941_1420366/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0235_native_excerpt.json) | `36f6a66890613c668f1908b9ce5895c0bf828e0bf7e774740b25a29e63929498` | native_output |
| E0236 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_vacuum_crosscheck_20260916/20260916T063241_185941_1420366/status.json](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_vacuum_crosscheck_20260916/20260916T063241_185941_1420366/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0236_status.json) | `f2c2729baa1269b391e7a54fc6a780c8f9334f5e1cffa8f43fe07392f1681f86` | evidence_or_analysis |
| E0237 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_methanol_crosscheck_20260916/20260916T063638_266158_1534956/input.inp](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_methanol_crosscheck_20260916/20260916T063638_266158_1534956/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0237_input.inp) | `f9c894fc1f8cc78d1f0c222c39ef2ae778519e9bb416a511eee660be2790f03a` | input_or_analysis_code |
| E0238 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_methanol_crosscheck_20260916/20260916T063638_266158_1534956/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_methanol_crosscheck_20260916/20260916T063638_266158_1534956/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0238_native_excerpt.json) | `57410fabc34b4f247118694ee99ec173b99b23647165861dca7f9729b0121755` | native_output |
| E0239 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_methanol_crosscheck_20260916/20260916T063638_266158_1534956/status.json](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/snaft_z_literal_methanol_crosscheck_20260916/20260916T063638_266158_1534956/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0239_status.json) | `7068242e358b5803001089c42dfbb378be3684ab36194a770b04c1a69a832424` | evidence_or_analysis |
| E0240 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_vacuum_crosscheck_20260916/20260916T065900_153287_2198637/input.inp](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_vacuum_crosscheck_20260916/20260916T065900_153287_2198637/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0240_input.inp) | `7890b94e76353cc60e0d8eece8a9c03f86ba08aac1c916231b0fbb02e754c87c` | input_or_analysis_code |
| E0241 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_vacuum_crosscheck_20260916/20260916T065900_153287_2198637/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_vacuum_crosscheck_20260916/20260916T065900_153287_2198637/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0241_native_excerpt.json) | `f772bdfc519063677681ab909e93de4526ced65f829592fc3926f9dd2fa7a55d` | native_output |
| E0242 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_vacuum_crosscheck_20260916/20260916T065900_153287_2198637/status.json](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_vacuum_crosscheck_20260916/20260916T065900_153287_2198637/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0242_status.json) | `20456ca6c2cc1b40ce1900a25fc9219e0ba3ad276a7f384b4e94087e8ae47f5a` | evidence_or_analysis |
| E0243 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_methanol_crosscheck_20260916/20260916T070008_461425_2232466/input.inp](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_methanol_crosscheck_20260916/20260916T070008_461425_2232466/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0243_input.inp) | `0f3d5a7c48b1b8d99d1b79ba9a883842b14ae894af36408cb12a264d6bff9eec` | input_or_analysis_code |
| E0244 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_methanol_crosscheck_20260916/20260916T070008_461425_2232466/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_methanol_crosscheck_20260916/20260916T070008_461425_2232466/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0244_native_excerpt.json) | `03e1914ff0d86858528933268e549a9794640efa1d0b487aa27e5f324ecc0f9c` | native_output |
| E0245 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_methanol_crosscheck_20260916/20260916T070008_461425_2232466/status.json](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vplus_literal_methanol_crosscheck_20260916/20260916T070008_461425_2232466/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0245_status.json) | `4c34447e038d3f770e80fd69e62bcd4e0fd406b1d1db5fb2d0d57e7125810ecf` | evidence_or_analysis |
| E0246 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_vacuum_crosscheck_20260916/20260916T070120_918988_2266770/input.inp](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_vacuum_crosscheck_20260916/20260916T070120_918988_2266770/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0246_input.inp) | `384bc2d2bb4701f8b54334d474bc4e2ced540ec22c682d853eb065048747a8d5` | input_or_analysis_code |
| E0247 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_vacuum_crosscheck_20260916/20260916T070120_918988_2266770/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_vacuum_crosscheck_20260916/20260916T070120_918988_2266770/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0247_native_excerpt.json) | `fee9ef5ca9d000cddb679ca594e303d02eb5ed21ee2b8563a1f27e6f2131791f` | native_output |
| E0248 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_vacuum_crosscheck_20260916/20260916T070120_918988_2266770/status.json](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_vacuum_crosscheck_20260916/20260916T070120_918988_2266770/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0248_status.json) | `452ffa3f2bd344a14b4123ffda2e53ab0621adcf948a7f3dbf53f8d3f14ced6f` | evidence_or_analysis |
| E0249 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_methanol_crosscheck_20260916/20260916T070226_896546_2300719/input.inp](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_methanol_crosscheck_20260916/20260916T070226_896546_2300719/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0249_input.inp) | `48c17b99825da38e8c19bf410a84f012535c35a610fa2e89d8758105e64ac469` | input_or_analysis_code |
| E0250 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_methanol_crosscheck_20260916/20260916T070226_896546_2300719/orca_stdout.log](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_methanol_crosscheck_20260916/20260916T070226_896546_2300719/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0250_native_excerpt.json) | `d6819088069dc1754f8cdb09eba4201146d576eddb368311c761845caf960ffd` | native_output |
| E0251 | [runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_methanol_crosscheck_20260916/20260916T070226_896546_2300719/status.json](../../../../runs/hold_verification/group_5/santr_source_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_vminus_literal_methanol_crosscheck_20260916/20260916T070226_896546_2300719/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0251_status.json) | `68f820b415bdf500d8a15fba340e3ed5596f4a33ae5c298a282c19aae72d32dd` | evidence_or_analysis |
| E0252 | [runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_vacuum_defaultgrid_diagnostic_closure_20260915/20260916T061232_220955_816365/input.inp](../../../../runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_vacuum_defaultgrid_diagnostic_closure_20260915/20260916T061232_220955_816365/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0252_input.inp) | `452a16f78a8e3f4010448d60ed311d396ea5745a0008cb9a0bbe64185db4bfa8` | input_or_analysis_code |
| E0253 | [runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_vacuum_defaultgrid_diagnostic_closure_20260915/20260916T061232_220955_816365/orca_stdout.log](../../../../runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_vacuum_defaultgrid_diagnostic_closure_20260915/20260916T061232_220955_816365/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0253_native_excerpt.json) | `74a5f3eb9280c0c18d3852dfca40987456c16f46d25c3bdcde54d55f95c9481e` | native_output |
| E0254 | [runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_vacuum_defaultgrid_diagnostic_closure_20260915/20260916T061232_220955_816365/status.json](../../../../runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_vacuum_defaultgrid_diagnostic_closure_20260915/20260916T061232_220955_816365/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0254_status.json) | `8cf56e74aaa355769408607c9054dd09e33b8eb95ff8fc248e58d4ba40b87f85` | evidence_or_analysis |
| E0255 | [runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_methanol_defaultgrid_diagnostic_closure_20260915/20260916T061328_053500_837719/input.inp](../../../../runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_methanol_defaultgrid_diagnostic_closure_20260915/20260916T061328_053500_837719/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0255_input.inp) | `0e88d1755719c39e6738e340169b130ac0cba5f9fb6858145e44be729bed7407` | input_or_analysis_code |
| E0256 | [runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_methanol_defaultgrid_diagnostic_closure_20260915/20260916T061328_053500_837719/orca_stdout.log](../../../../runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_methanol_defaultgrid_diagnostic_closure_20260915/20260916T061328_053500_837719/orca_stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0256_native_excerpt.json) | `cabcffceadcac7e4e8f6da997d7fa31d6a2be22cabd86fb2b6f1ad68a36b758d` | native_output |
| E0257 | [runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_methanol_defaultgrid_diagnostic_closure_20260915/20260916T061328_053500_837719/status.json](../../../../runs/hold_verification/group_5/continuation_20260916/paper_8d8940710de08f7f/provenance/local_tests/recovery_20260914/santr_si_literal_methanol_defaultgrid_diagnostic_closure_20260915/20260916T061328_053500_837719/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0257_status.json) | `2d2d105971b9a21e0933cbc341b27a0c5e20d8f3d222d716a172ee05b7654592` | evidence_or_analysis |
| E0258 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_1/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_1/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0258_input.inp) | `92fb5990e18a00404cdcbd04a096eff562e4e109342f65034d2116e8529ab7fb` | input_or_analysis_code |
| E0259 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_2/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_2/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0259_input.inp) | `55c666f11694a45db235a16df43c48cbb78fd300fac0490477713b28e7ec4b85` | input_or_analysis_code |
| E0260 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_3/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_3/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0260_input.inp) | `ec9f1bc1b0ebf74c0de54a5fba3dfdf0e4764d1ca033343752ea9c1fae454154` | input_or_analysis_code |
| E0261 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_4/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_4/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0261_input.inp) | `805a49189fb7d665f96aa94a93ee90285502b9c09f306bc5884bca6404406d00` | input_or_analysis_code |
| E0262 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_5/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_5/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0262_input.inp) | `d9d3dfb5933c2daef962bc71c52a1f1467f91ae0abd658bfb725cb6c19150597` | input_or_analysis_code |
| E0263 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_6/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_6/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0263_input.inp) | `9b5dc2eba6939a414359347881a86f272ec064dd459ad0c9b1ac771530e64a15` | input_or_analysis_code |
| E0264 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_7/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_7/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0264_input.inp) | `04a8347a76c9569e2d12568dc03cd3c145df2f228bac159370941e30fe6a355e` | input_or_analysis_code |
| E0265 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_8/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_8/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0265_input.inp) | `4e86682b9ba7b6627d91494b40284c5518ff6b028735a021caf42e559239799c` | input_or_analysis_code |
| E0266 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_9/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_9/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0266_input.inp) | `d7f5d930b6b14de7d5fb0d123e010daf4606037401c33ee8d539cabe9014c5d3` | input_or_analysis_code |
| E0267 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0267_entrypoint.sh) | `ef1aa89ee202f3d266e5cfaa839a0589f50f7a5ad66679e76541be2d1d042058` | input_or_analysis_code |
| E0268 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0268_input_trj.xyz) | `87839b9096dcf4ed89395a40e60542a6e82b587c42da956dfc1cd301f34ee6ec` | input_or_analysis_code |
| E0269 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0269_input.inp) | `ee015a85f5025888a397da0a7309c70554958342769a3e078d5c5edefa3937bd` | input_or_analysis_code |
| E0270 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point9_constrained_precision/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0270_input.xyz) | `3140924c87476c66b43d31dbcd0ff09ca0ac2cfc4f17404f307bcf8a38e3b4ea` | input_or_analysis_code |
| E0271 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_10/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_10/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0271_input.inp) | `d787dd185cafee74fa1a2c8f63232a0923441c8d849403d7caa38066eda3b8d4` | input_or_analysis_code |
| E0272 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_11/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_11/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0272_input.inp) | `eac1360732cc688c564257b8fd2c05f458cb052705ecd38cb7e4d8b8e43af0a2` | input_or_analysis_code |
| E0273 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_12/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_12/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0273_input.inp) | `9ee1abc87b9dc2ca3abf819eafef1916a4cb83bd603513ef069e91ebc610a774` | input_or_analysis_code |
| E0274 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0274_entrypoint.sh) | `ef1aa89ee202f3d266e5cfaa839a0589f50f7a5ad66679e76541be2d1d042058` | input_or_analysis_code |
| E0275 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0275_input_trj.xyz) | `62ae825bbbebf44824ade4a1674c892acadb4fca4286169fb89e5df61d0d7849` | input_or_analysis_code |
| E0276 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0276_input.inp) | `40c6ea094f4cb8edae754d5e8c2219fa612c6181f028e4fe7aa2cc9e3aee93c6` | input_or_analysis_code |
| E0277 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SNaft_Zside_point12_constrained_precision/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0277_input.xyz) | `2d12c7c567ae309118189852ae17ed48bebc2f41d51ae019583e7a3f20b6b200` | input_or_analysis_code |
| E0278 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_13/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_13/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0278_input.inp) | `4fb04a3ac303402f3d1f98d51c25afd4320a79eff0e44a7490b2784684cb651d` | input_or_analysis_code |
| E0279 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_14/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_14/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0279_input.inp) | `537f1cc9310c68f529fd530410e1fe2aa3bef565e1ba0506e28ea05737d19ea9` | input_or_analysis_code |
| E0280 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_15/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SNaft_matched_MeOH_path_gas_SP15/attempt_001/point_15/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0280_input.inp) | `3a836271d85f25a776719fecd0e2964c22dfe12c2646a97d031002fe317160ab` | input_or_analysis_code |
| E0281 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_1/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_1/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0281_input.inp) | `84a3d54ceb93abc27c555026352a0627f7a0f052a631fe47a4aa905ac04cba29` | input_or_analysis_code |
| E0282 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_2/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_2/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0282_input.inp) | `66ce57537458651b690b60906e35a2cde6acdb688e312aaca4a04d15328e9bae` | input_or_analysis_code |
| E0283 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_3/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_3/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0283_input.inp) | `650b02aafe7cedf08c26ab730edf561a306fe19c375d647321c0f69925383944` | input_or_analysis_code |
| E0284 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_4/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_4/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0284_input.inp) | `2d612582d55193fc5c372fa6335b03d6cd2fe86e76fb6682c66e2d7ccf700af8` | input_or_analysis_code |
| E0285 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_5/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_5/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0285_input.inp) | `ca261bee866bad940795c1c32ad940759540f39a71be797bff7a4cf688d527cd` | input_or_analysis_code |
| E0286 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_6/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_6/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0286_input.inp) | `f2bf1ef66e2f5c186d806e1459bf6a7144c424f82c918d463236a27ebb7586ab` | input_or_analysis_code |
| E0287 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_7/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_7/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0287_input.inp) | `2ca17951bc566eacbe6a55630586ba96506a0bb48e7aa7f337a6dda1a6802536` | input_or_analysis_code |
| E0288 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_8/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_8/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0288_input.inp) | `4dc5a9b915fe48a1e75a250d06c9f789a1cd513b76d8d55df131c0b58e956794` | input_or_analysis_code |
| E0289 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_9/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_9/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0289_input.inp) | `cf4949682bbf63c560d79cc4f52bbd00a2982031a6e033e194f5fbe01090f3a3` | input_or_analysis_code |
| E0290 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_10/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_10/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0290_input.inp) | `a7c355b8b34bce172618ae91baef12c9d9407fb70a290011aa7c1f08b6e950b3` | input_or_analysis_code |
| E0291 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_11/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_11/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0291_input.inp) | `6ab1ff0fa11c0937b2fc352027a980ef527d6abaceaedbdd1adf8c2e3d91906a` | input_or_analysis_code |
| E0292 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0292_entrypoint.sh) | `ef1aa89ee202f3d266e5cfaa839a0589f50f7a5ad66679e76541be2d1d042058` | input_or_analysis_code |
| E0293 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0293_input_trj.xyz) | `42f27bce70b1cb4fce5e0406684b674703735c957c0ebc2180b6120949fb8a8e` | input_or_analysis_code |
| E0294 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0294_input.inp) | `8ee649ee03ed99be8dcb05c7f8e0c3edf40a1992bc787383c3eee8b121c2d640` | input_or_analysis_code |
| E0295 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point11_constrained_precision/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0295_input.xyz) | `8fb20e356c9550204af8788c8e574d07262bd786ed37b5b24922db776c7c666c` | input_or_analysis_code |
| E0296 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_12/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_12/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0296_input.inp) | `d9d68f6ab58611821dfa1e4f9cc3b1810d75d6ec26ac8c43bca7d5beff6f6143` | input_or_analysis_code |
| E0297 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_13/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_13/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0297_input.inp) | `d029bb124000bef922d8df781872012eaf6170e7aee681aeed487710afa7cf68` | input_or_analysis_code |
| E0298 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0298_entrypoint.sh) | `ef1aa89ee202f3d266e5cfaa839a0589f50f7a5ad66679e76541be2d1d042058` | input_or_analysis_code |
| E0299 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/input_trj.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/input_trj.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0299_input_trj.xyz) | `eb53579ddf66d7623ef251baa5a5c9d828b5100b64c0834bd9f02e1bffcf1183` | input_or_analysis_code |
| E0300 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0300_input.inp) | `2b2fd971ddd2265572bf5774b286dec89658927bbe52f5a52545c2f9ba9763a4` | input_or_analysis_code |
| E0301 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/input.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/v2_SAntr_Zside_point13_constrained_precision/attempt_001/input.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0301_input.xyz) | `fa6aaa46852dfb2ac85ff4933ac8770cc745649d54ef5b6463bb24f0757d7310` | input_or_analysis_code |
| E0302 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_14/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_14/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0302_input.inp) | `4d89eac5d593754aaadc7dc19cdaf8db1c062ea52b1a32ba27fcb7a2bcc86522` | input_or_analysis_code |
| E0303 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_15/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/strict_SAntr_matched_MeOH_path_gas_SP15/attempt_001/point_15/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0303_input.inp) | `47e55699374665d49b6c8bdb686bfeeb534cc466039ed2271aaff81dbafba6ed` | input_or_analysis_code |
| E0304 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_wB97MV_DEFGRID2_control/attempt_001/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_wB97MV_DEFGRID2_control/attempt_001/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0304_native_excerpt.json) | `189f90ddc99551e70be9f6ebbcea4f4daa1e15011216950b24199c25f5d78be3` | native_output |
| E0305 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_wB97MV_DEFGRID2_control/attempt_001/entrypoint.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_wB97MV_DEFGRID2_control/attempt_001/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0305_entrypoint.sh) | `3d2a138ddf7cda208c0d567c4dee515c6d8c3cac455d1d103fea2dcc890d6880` | input_or_analysis_code |
| E0306 | [docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_wB97MV_DEFGRID2_control/attempt_001/input.inp](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_2/papers/paper_8d8940710de08f7f/outputs/author_route_SAntr_Z_literalSI_wB97MV_DEFGRID2_control/attempt_001/input.inp)；[冻结副本](../../../../docs/v2_verification/papers/paper_8d8940710de08f7f/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0306_input.inp) | `e178bf0f5fa0833391dad8557f9a47275e6e4fbcb4caff8691dd2b786a097c43` | input_or_analysis_code |
| N0306 | [tasks/v2_autonomous_research/paper_8d8940710de08f7f/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_8d8940710de08f7f/evaluation/reference_key_points.json) | `b40e42938ba6c376b16a153a847f7d614d68e8a9a158b1009efb00001b96422e` | latest_review_evidence |
| N0307 | [tasks/v2_autonomous_research/paper_8d8940710de08f7f/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_8d8940710de08f7f/evaluation/reference_conclusions.json) | `bc8d96ed5b7907d40fdefe4452eb4e7ab2a6128fb69f7f727fbf26adb4f93f38` | latest_review_evidence |
| N0308 | [tasks/v2_autonomous_research/paper_8d8940710de08f7f/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_8d8940710de08f7f/evaluation/scoring_rules.json) | `98a6bda4c94e92ebe7316b3e1ee0a4f09e762864db32bfe30911b861c369333e` | latest_review_evidence |
| N0309 | [tasks/v2_autonomous_research/paper_8d8940710de08f7f/evaluation/reference_validation_plan.md](../../../v2_autonomous_research/paper_8d8940710de08f7f/evaluation/reference_validation_plan.md) | `8de17a1b8c767d64ac212a23924aa597966c78bc070ccaa5623614c0fa0b279f` | latest_review_evidence |
| N0310 | [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/evaluation/scoring_rules.json](scoring_rules.json) | `98a6bda4c94e92ebe7316b3e1ee0a4f09e762864db32bfe30911b861c369333e` | latest_review_evidence |
| N0311 | [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `8de17a1b8c767d64ac212a23924aa597966c78bc070ccaa5623614c0fa0b279f` | latest_review_evidence |
| N0312 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0313 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json) | `66b4df5fb10f6b54e16cafe1cc04f2dd2ed2ff67af141ca58d0b02b4d1b922f1` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/agent_input/task.md](../agent_input/task.md) | `ad20817a5e540a0344066f1cb5972af2b9d1bed1a40a3ea13986e732782b870d` |
| [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/evaluation/reference_key_points.json](reference_key_points.json) | `b40e42938ba6c376b16a153a847f7d614d68e8a9a158b1009efb00001b96422e` |
| [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/evaluation/reference_conclusions.json](reference_conclusions.json) | `bc8d96ed5b7907d40fdefe4452eb4e7ab2a6128fb69f7f727fbf26adb4f93f38` |
| [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/evaluation/scoring_rules.json](scoring_rules.json) | `98a6bda4c94e92ebe7316b3e1ee0a4f09e762864db32bfe30911b861c369333e` |
| [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/evaluation/critical_failures.json](critical_failures.json) | `67080d08406625f54c77cd144f35d9b19cf96b0255f0f5789eb253a5fde3269e` |
| [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/evaluation/evidence_map.json](evidence_map.json) | `ce358f4d3111741073d40157a28e44e313f7ef55bfcf37f7fc14bfcaf84322fe` |
| [tasks/v2_paper_reproduction/paper_8d8940710de08f7f/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `8de17a1b8c767d64ac212a23924aa597966c78bc070ccaa5623614c0fa0b279f` |


## Current scoring migration — 2026-10-19
Active policy: paper_science_v2; 100 binary scientific-result points across intermediate findings and final conclusions. Active rules supersede historical scoring weights and freezes. No process score or multiplier. This migration performs no new chemical calculation and preserves the existing frozen V2 acceptance with all scientific limitations. SI TableS8 explicitly labels data in vacuo; electronic energies fit methanol better, but Gibbs environment and temperature remain unproven. Tiny V splitting does not certify a robust unique order/population. Seven-point relaxed scans and released paths establish finite flexibility, not continuous transition states or exact rates. Local Espinosa energy is not total conformational stabilization; ionisation, membrane, biology and crystals are outside scope.


## Authorized scoring-contract repair — 2026-10-19 (round3)
Split final18+10 into SNaft9+5 and SAntr9+5. Each final retains a genuine within-molecule stability/flexibility or cross-medium relation, with only that molecule supporting it. AR need not criticize an inaccessible TableS8 or replicate source software choices. Public scoring prose now describes100-point binary scientific results; reporting a contrary/unresolved answer does not automatically satisfy another target. This append changes the current evaluation contract only; original verification history remains verbatim, no new chemistry or acceptance upgrade is claimed.
