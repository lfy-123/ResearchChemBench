# 本次V3范围与逐命题证据复用（2026-10-28）

保持局部Pd/XantPhos氢演化和恢复问题；4条最终命题30/30/25/15，保留0.9±0.5势垒窗。二氢化物结构/连通性转为势垒的证据条件，移除低势垒结论与数值的重复分；释放条件、Pd可用性与气体实验含义分别评分。

- `terminal_barrier`：native_evidence.json的RRHO势垒0.764432；已核对INT-G/TS6原生日志与SI50–53；原0.9±0.5硬窗保持。
- `release_reference_sensitivity`：native_evidence.json records/reactions：释放+0.0115819 kcal/mol，0.1atm为−1.352665、10atm为+1.375829；RTlnp响应已存在。
- `pd_availability`：native_evidence.json：完整释放Pd及DMAc捕获A/B，+0.402490/+0.658922 kcal/mol，近零且低频/活度敏感；不认证催化周转。
- `gas_experiment_inference`：main p4与SI10两腔实验+本地形成/释放模型支持相容性；实验未测局部Pd物种/速率。

未提交新计算；以下历史正文逐字保留。历史PASS不代表新V3全部命题重新验证通过。

---

# V2 验证计算参考：Pd/XantPhos 局部 H2 生成

论文：`paper_9132719dbf91c978`；模式：`autonomous_research`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：源低势垒H2形成的完整77原子最小点、唯一虚频TS、双向IRC及高层/热项组合均为实际计算；势垒0.764432对源0.883282/印刷0.9 kcal/mol。恢复催化剂部分实算但只能条件性解释。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

How well does molecular evidence support H2 evolution and recovery of a usable Pd/XantPhos species from the source dihydride composition, and which local steps or assumptions limit that conclusion?

冻结题面中的科学目标：

How well does molecular evidence support H2 evolution and recovery of a usable Pd/XantPhos species from the source dihydride composition, and which local steps or assumptions limit that conclusion?

自主科研模式向 agent 提供科学问题、物种/数据和边界，由其自主选择方法。以下作者路线是维护者验证采用的参考，不要求 agent 照抄该流程，也不是一次新的盲测自主发现记录。

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_9132719dbf91c978/documents/supplementary_001.pdf](../../../../papers/paper_9132719dbf91c978/documents/supplementary_001.pdf) | `ae27addc290464f1b17ef3fbd0dd6cac8eb0830aa03cc0aaa686fd57321d2817` |
| [papers/paper_9132719dbf91c978/documents/main.pdf](../../../../papers/paper_9132719dbf91c978/documents/main.pdf) | `3d08d907aafb9175e71858913e8f6671891645f0479d189eab246a24d442faeb` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

Native PBE0-D3BJ/def2-SVP optimization/frequency and MN15/def2-TZVP SMD(DMAc) single points were directly read. Full 77-atom dihydride and H2-bound endpoints have 225 positive modes; the H2-elimination saddle has one −478.5853 cm−1 mode. Both genuine IRC logs, optimized endpoints, released Pd and H2 native files were read.

1. 核对完整 Pd/XantPhos 二氢化物、H2 结合物与 TS 的 77 原子、q=0/singlet，以及释放后 75 原子 Pd 配体、H2 和 DMAc 的守恒计量。

2. 按 PBE0-D3BJ/def2-SVP 优化/频率，随后 MN15/def2-TZVP/SMD(DMAc) 高层单点。两个主要端点各 225 正模，TS 有唯一约 −478.6 cm⁻¹ 虚频，氢运动参与由真实位移核实。

3. 复用并核收双向 IRC 54/8 点和两端重新优化，H–H 约 0.885929/1.746720 Å 区分结合 H2 与二氢化物；不能只凭作业正常结束或一个虚频认定连接正确。

4. 按 298.15 K、溶质及 DMAc 1 M、H2 1 atm 的明示参照合并高层 E 与低层热项，局部势垒 0.7644320 kcal/mol，对源重建 0.8832823。源坐标及 CPHF/UltraFine 控制与 INT-G 热项约 0.000278 Eh 残差另列。

5. 核收游离 Pd/H2 最低点和溶剂捕获计算；H2 释放 +0.011582、DMAc 捕获 A/B +0.402490/+0.658922 kcal/mol 接近零，不能把势垒容差搬来强定方向。结论是低势垒 H2 生成及有条件的催化剂恢复，非完整催化循环认证。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

### 最近一次原生有效性复核

本轮读取原端点/TS、双向IRC、重新优化端点、MN15单点、游离Pd/H2日志。TS唯一负频-478.5853 cm^-1，端点225正频；低层/高层方法与SI原文匹配。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| Composite terminal H2-elimination free-energy barrier (kcal/mol) | {"printed":0.9,"reconstructed":0.883282} | 0.7644320412514988 | Actual residual vs source reconstruction −0.11885 kcal/mol. The pre-existing r_barrier ±2 kcal/mol rule applies to this identical terminal observable only; the actual residual is much narrower. Independent TS curvature and two-sided connectivity support the low-barrier conclusion. |
| INT-G thermal correction (Eh) | 0.545137 | 0.545424 | Residual 0.000287 Eh at the optimized native structure; the fixed-source control residual is about 0.000278 Eh. This incomplete component match is disclosed and does not overturn the explicitly matched terminal composite barrier. |
| Released H2 and solvent capture thermodynamics (kcal/mol) | Source qualitative release/regeneration proposal | {"H2_release_1M_solutes_1atm_H2":0.0115818924,"DMAc_capture_A":0.4024898888} | Both are near zero and reference-sensitive; the barrier tolerance is not transferred. The honest result is conditional recovery, not a computed turnover rate. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Full ligand and hydrogen inventory

冻结要求：Preserve fullXantPhos/Pd/2H, actual charge/spin and any solvent/reagent inventory. ValidateP coordination and hydrogen mapping from submitted structures. Arbitrary solvent omission/addition must not create an unbalanced energy comparison. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：XantPhos/Pd/H2全守恒

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "SI S50–53; main p4 Scheme3",
    "actual_result": "完整XantPhos/Pd/2H，77原子、0/1态、Pd75及H76/77；游离Pd配体75原子/H2双原子、DMAc加入均配平。",
    "reason": "实际配体图、P配位和氢映射保留，所有补充恢复循环原子/电荷守恒。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "feac759505b56f8aca946c0d1679c4a0d0ebaf278e3c3cdeab49070a8ad63d7d",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "0ad35b6d99f5d3b1c80fd59a57fc775eaffcf8db5f23ab0116f9bd3342697ac8",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log",
        "sha256": "bc0b01f71277550216b987008792da153c5163a3ecc8104eb2a206d0e81dd45f",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log",
        "sha256": "c041c72e962810d5fc9e54c9e729733e9cb8aae9de67d0922ff1a170e8dfdf33",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "eb403e351db5d2189986792e4128a7229ab94eeb998283d26ef5d2d656055ca7",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "4e94272743d191e733022d26a1e90a3addd77d779262eddf54c20a95f080ace9",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/native_evidence.json",
        "sha256": "e9732a2b03c35b5a7bb2fba5ea1bf9a9c3d108a3a81488cdc307cccb00d012c0",
        "kind": "retained_HPC_native_reparse"
      }
    ]
  }
]
```


证据记录：`E0040`。

```json
[
  {
    "source_locator": "SI S50–53; main p4 Scheme3",
    "actual_result": "完整XantPhos/Pd/2H，77原子、0/1态、Pd75及H76/77；游离Pd配体75原子/H2双原子、DMAc加入均配平。",
    "reason": "实际配体图、P配位和氢映射保留，所有补充恢复循环原子/电荷守恒。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "feac759505b56f8aca946c0d1679c4a0d0ebaf278e3c3cdeab49070a8ad63d7d",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "0ad35b6d99f5d3b1c80fd59a57fc775eaffcf8db5f23ab0116f9bd3342697ac8",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log",
        "sha256": "bc0b01f71277550216b987008792da153c5163a3ecc8104eb2a206d0e81dd45f",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log",
        "sha256": "c041c72e962810d5fc9e54c9e729733e9cb8aae9de67d0922ff1a170e8dfdf33",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "eb403e351db5d2189986792e4128a7229ab94eeb998283d26ef5d2d656055ca7",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "4e94272743d191e733022d26a1e90a3addd77d779262eddf54c20a95f080ace9",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/native_evidence.json",
        "sha256": "e9732a2b03c35b5a7bb2fba5ea1bf9a9c3d108a3a81488cdc307cccb00d012c0",
        "kind": "retained_HPC_native_reparse"
      }
    ]
  }
]
```

### kp_evolution — Quantitative local hydrogen-evolution evidence

冻结要求：Auditable new evidence must address formation/evolution and the extent of catalyst recovery claimed. An old0.9 barrier copied fromSI or anH–H distance alone is insufficient. Evaluate an adequate alternative route on its evidence rather than an obligatory3-endpoint sequence. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：真实低势垒和释放/捕获

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "SI S10/12, FigS4 and S50–53",
    "actual_result": "原优化链ΔG‡0.764432；固定源标准取向0.708834702；主文/源约0.9、SI分量0.883282336kcal/mol。双点CPHFUltraFine后0.708834702不变；INTG225正模、TS6唯一−478.6044cm−1。",
    "reason": "同一77原子/态/低高层复合定义，旧±2kcal验收尺度仅继承到该局部势垒；实际结果仍正且<1kcal，非仅靠宽门判低势垒。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "feac759505b56f8aca946c0d1679c4a0d0ebaf278e3c3cdeab49070a8ad63d7d",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "0ad35b6d99f5d3b1c80fd59a57fc775eaffcf8db5f23ab0116f9bd3342697ac8",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log",
        "sha256": "bc0b01f71277550216b987008792da153c5163a3ecc8104eb2a206d0e81dd45f",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log",
        "sha256": "c041c72e962810d5fc9e54c9e729733e9cb8aae9de67d0922ff1a170e8dfdf33",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/result.json",
        "sha256": "5e07b695904542d070aeb9480ee503c90f26edc76059383160349966c26f7507",
        "kind": "returned_HPC_comparison"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/INTG/gaussian.log",
        "sha256": "1e77e30b7c0377e8a7cf0ec8401ba8e8056b07f1433b94d91d7567175229642b",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/TS6/gaussian.log",
        "sha256": "a53b5d449c792ec7b9c0ed79f05cc4f68685d4b7a542d33a95392e09a0f50642",
        "kind": "raw_native_output"
      }
    ]
  }
]
```


证据记录：`E0040`。

```json
[
  {
    "source_locator": "SI S10/12, FigS4 and S50–53",
    "actual_result": "原优化链ΔG‡0.764432；固定源标准取向0.708834702；主文/源约0.9、SI分量0.883282336kcal/mol。双点CPHFUltraFine后0.708834702不变；INTG225正模、TS6唯一−478.6044cm−1。",
    "reason": "同一77原子/态/低高层复合定义，旧±2kcal验收尺度仅继承到该局部势垒；实际结果仍正且<1kcal，非仅靠宽门判低势垒。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "feac759505b56f8aca946c0d1679c4a0d0ebaf278e3c3cdeab49070a8ad63d7d",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "0ad35b6d99f5d3b1c80fd59a57fc775eaffcf8db5f23ab0116f9bd3342697ac8",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log",
        "sha256": "bc0b01f71277550216b987008792da153c5163a3ecc8104eb2a206d0e81dd45f",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log",
        "sha256": "c041c72e962810d5fc9e54c9e729733e9cb8aae9de67d0922ff1a170e8dfdf33",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/result.json",
        "sha256": "5e07b695904542d070aeb9480ee503c90f26edc76059383160349966c26f7507",
        "kind": "returned_HPC_comparison"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/INTG/gaussian.log",
        "sha256": "1e77e30b7c0377e8a7cf0ec8401ba8e8056b07f1433b94d91d7567175229642b",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/TS6/gaussian.log",
        "sha256": "a53b5d449c792ec7b9c0ed79f05cc4f68685d4b7a542d33a95392e09a0f50642",
        "kind": "raw_native_output"
      }
    ]
  }
]
```

### kp_mechanism — Validity of pathway and recovery claims

冻结要求：Require saddle/connectivity evidence only for claims that need it; establish whether claimed bound versus releasedH2 species are genuine within the model. A solvent-binding ΔG cannot by itself show kinetic availability. Well-evidenced collapse to a common basin is not failure. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：TS/IRC及bound-vs-free H2

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "main Scheme3 and SI S10–12; retained genuine IRC",
    "actual_result": "旧双向IRC54/8点和两端自由最低点都具225模式；前端H–H0.885929Å为结合H2，后端1.746720Å为dihydride；游离Pd/H2后续219/1正模。TS6虚频氢动能参与0.985912。",
    "reason": "一虚频与真实连接共同支持局部H–H形成。结合H2不等于释放，保留成功释放区域/独立片段；无催化再生速率臆断。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_forward_irc_20260915_hpc20_p6/stdout.log",
        "sha256": "bdba081b46f8f220ffe545b79a35c6cc2ac68c2c41b016db0d93ee2c31a51e0c",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_reverse_irc_20260915_hpc20_p6/stdout.log",
        "sha256": "bc9cc3d5ea8a2f85c78250e14841c562d3a8d3a5c064e590ef07e099a8155b1a",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log",
        "sha256": "bc0b01f71277550216b987008792da153c5163a3ecc8104eb2a206d0e81dd45f",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log",
        "sha256": "c041c72e962810d5fc9e54c9e729733e9cb8aae9de67d0922ff1a170e8dfdf33",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "eb403e351db5d2189986792e4128a7229ab94eeb998283d26ef5d2d656055ca7",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "4e94272743d191e733022d26a1e90a3addd77d779262eddf54c20a95f080ace9",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/irc_continuation_audit.json",
        "sha256": "bbd237c2e3f43dbf053782f22f2d91f2b0707d57ca8405872d38de5c817ea3ee",
        "kind": "retained_HPC_connection_audit"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_RRHO_decomposition_20261007/Pd_RRHO_DECOMPOSITION.json",
        "sha256": "34801f3d232718f9dba50acd8d91f6d230f30398d2e33bed81b6d4cc848850bd",
        "kind": "returned_HPC_analysis"
      }
    ]
  }
]
```


证据记录：`E0040`。

```json
[
  {
    "source_locator": "main Scheme3 and SI S10–12; retained genuine IRC",
    "actual_result": "旧双向IRC54/8点和两端自由最低点都具225模式；前端H–H0.885929Å为结合H2，后端1.746720Å为dihydride；游离Pd/H2后续219/1正模。TS6虚频氢动能参与0.985912。",
    "reason": "一虚频与真实连接共同支持局部H–H形成。结合H2不等于释放，保留成功释放区域/独立片段；无催化再生速率臆断。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_forward_irc_20260915_hpc20_p6/stdout.log",
        "sha256": "bdba081b46f8f220ffe545b79a35c6cc2ac68c2c41b016db0d93ee2c31a51e0c",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_reverse_irc_20260915_hpc20_p6/stdout.log",
        "sha256": "bc9cc3d5ea8a2f85c78250e14841c562d3a8d3a5c064e590ef07e099a8155b1a",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log",
        "sha256": "bc0b01f71277550216b987008792da153c5163a3ecc8104eb2a206d0e81dd45f",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log",
        "sha256": "c041c72e962810d5fc9e54c9e729733e9cb8aae9de67d0922ff1a170e8dfdf33",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "eb403e351db5d2189986792e4128a7229ab94eeb998283d26ef5d2d656055ca7",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "4e94272743d191e733022d26a1e90a3addd77d779262eddf54c20a95f080ace9",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/irc_continuation_audit.json",
        "sha256": "bbd237c2e3f43dbf053782f22f2d91f2b0707d57ca8405872d38de5c817ea3ee",
        "kind": "retained_HPC_connection_audit"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_RRHO_decomposition_20261007/Pd_RRHO_DECOMPOSITION.json",
        "sha256": "34801f3d232718f9dba50acd8d91f6d230f30398d2e33bed81b6d4cc848850bd",
        "kind": "returned_HPC_analysis"
      }
    ]
  }
]
```

### kp_reference — Pressure and solution reference consistency

冻结要求：Declare and consistently applyH2 gas/solute andDMAc standard states, temperature, entropy and pressure assumptions. Relevant sensitivity must support the claimed sign or scale. No universal numerical tolerance or fixed one-solvent model. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：温度/1M与1atm

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "SI S10 composite convention; main gas experiment",
    "actual_result": "298.15K，溶质与分子DMAc1M，H2气体1atm。MN15下H2释放ΔG+0.011582，DMAc捕获A/B+0.402490/+0.658922，合并+0.414072/+0.670504kcal/mol；气压与低频处理可改变接近零结论。",
    "reason": "同标准态配平。旧±2不移作释放/捕获误差条；对这类近零符号不给稳健自发再生判断。等分子数局部势垒的1M移位相消，无重复ZPE。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/native_evidence.json",
        "sha256": "e9732a2b03c35b5a7bb2fba5ea1bf9a9c3d108a3a81488cdc307cccb00d012c0",
        "kind": "retained_HPC_native_reparse"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_RRHO_decomposition_20261007/Pd_RRHO_DECOMPOSITION.json",
        "sha256": "34801f3d232718f9dba50acd8d91f6d230f30398d2e33bed81b6d4cc848850bd",
        "kind": "returned_HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "eb403e351db5d2189986792e4128a7229ab94eeb998283d26ef5d2d656055ca7",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "4e94272743d191e733022d26a1e90a3addd77d779262eddf54c20a95f080ace9",
        "kind": "raw_native_output"
      }
    ]
  }
]
```


证据记录：`E0040`。

```json
[
  {
    "source_locator": "SI S10 composite convention; main gas experiment",
    "actual_result": "298.15K，溶质与分子DMAc1M，H2气体1atm。MN15下H2释放ΔG+0.011582，DMAc捕获A/B+0.402490/+0.658922，合并+0.414072/+0.670504kcal/mol；气压与低频处理可改变接近零结论。",
    "reason": "同标准态配平。旧±2不移作释放/捕获误差条；对这类近零符号不给稳健自发再生判断。等分子数局部势垒的1M移位相消，无重复ZPE。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/native_evidence.json",
        "sha256": "e9732a2b03c35b5a7bb2fba5ea1bf9a9c3d108a3a81488cdc307cccb00d012c0",
        "kind": "retained_HPC_native_reparse"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_RRHO_decomposition_20261007/Pd_RRHO_DECOMPOSITION.json",
        "sha256": "34801f3d232718f9dba50acd8d91f6d230f30398d2e33bed81b6d4cc848850bd",
        "kind": "returned_HPC_analysis"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "eb403e351db5d2189986792e4128a7229ab94eeb998283d26ef5d2d656055ca7",
        "kind": "raw_native_output"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log",
        "sha256": "4e94272743d191e733022d26a1e90a3addd77d779262eddf54c20a95f080ace9",
        "kind": "raw_native_output"
      }
    ]
  }
]
```

### kp_conclusion — Gas evidence and local inference separated

冻结要求：Accept supported, refuted or evidence-backed unresolved local evolution/regeneration. Thetwo-chamber observation does not establish a uniquePd mechanism, and local steps cannot prove the full photochemical turnover or productyield. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：局部低势垒不同于整体光催化；最终有限结论闭合。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "main p4 Scheme2d/3; SI12",
    "actual_result": "分子模型支持低势垒H–H生成；实际可用Pd回收受H2离去/溶剂竞争/标准态与熵处理限制。双室可氢化气体证据不唯一识别局部Pd中间体。",
    "reason": "回应整个当前问题及证据强度，没有把附加DMAc序列或全光周期变成作者必做。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/native_evidence.json",
        "sha256": "e9732a2b03c35b5a7bb2fba5ea1bf9a9c3d108a3a81488cdc307cccb00d012c0",
        "kind": "retained_HPC_native_reparse"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/irc_continuation_audit.json",
        "sha256": "bbd237c2e3f43dbf053782f22f2d91f2b0707d57ca8405872d38de5c817ea3ee",
        "kind": "retained_HPC_connection_audit"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/result.json",
        "sha256": "5e07b695904542d070aeb9480ee503c90f26edc76059383160349966c26f7507",
        "kind": "returned_HPC_comparison"
      }
    ]
  }
]
```


证据记录：`E0040`。

```json
[
  {
    "source_locator": "main p4 Scheme2d/3; SI12",
    "actual_result": "分子模型支持低势垒H–H生成；实际可用Pd回收受H2离去/溶剂竞争/标准态与熵处理限制。双室可氢化气体证据不唯一识别局部Pd中间体。",
    "reason": "回应整个当前问题及证据强度，没有把附加DMAc序列或全光周期变成作者必做。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/native_evidence.json",
        "sha256": "e9732a2b03c35b5a7bb2fba5ea1bf9a9c3d108a3a81488cdc307cccb00d012c0",
        "kind": "retained_HPC_native_reparse"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/irc_continuation_audit.json",
        "sha256": "bbd237c2e3f43dbf053782f22f2d91f2b0707d57ca8405872d38de5c817ea3ee",
        "kind": "retained_HPC_connection_audit"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/result.json",
        "sha256": "5e07b695904542d070aeb9480ee503c90f26edc76059383160349966c26f7507",
        "kind": "returned_HPC_comparison"
      }
    ]
  }
]
```

### conclusion_investigation — How well does molecular evidence support H2 evolution and recovery of a usable Pd/XantPhos species from the source dihydride composition, and which local steps or assumptions limit that conclusion?

冻结要求：Answer the bounded question with claims proportional to the evidence. Support, correction, refutation and demonstrated unresolved conclusions are equally eligible. Partial/failure status preserves real work but does not confer completion credit. No required author winner or named control list.

当前复审：kp_identity：XantPhos/Pd/H2全守恒；kp_evolution：真实低势垒和释放/捕获；kp_mechanism：TS/IRC及bound-vs-free H2；kp_reference：温度/1M与1atm；kp_conclusion：局部低势垒不同于整体光催化；最终有限结论闭合。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`E0001`。

```json
[
  {
    "source_locator": "main p4; SI10–12,50–53",
    "actual_result": "低势垒局部H2生成与有效Pd物种的条件性恢复得到真实路径/端点/配平热力学支持；精确INTG热项仍差0.000278Eh，但不改变该范围内的源核心低势垒结论，且不被用作校准速率。",
    "reason": "原尺度适用于同一势垒并有新取向/响应网格/公式控制；更强动力学及精确源分量是明确例外。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/native_evidence.json",
        "sha256": "e9732a2b03c35b5a7bb2fba5ea1bf9a9c3d108a3a81488cdc307cccb00d012c0",
        "kind": "retained_HPC_native_reparse"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/irc_continuation_audit.json",
        "sha256": "bbd237c2e3f43dbf053782f22f2d91f2b0707d57ca8405872d38de5c817ea3ee",
        "kind": "retained_HPC_connection_audit"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/result.json",
        "sha256": "5e07b695904542d070aeb9480ee503c90f26edc76059383160349966c26f7507",
        "kind": "returned_HPC_comparison"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_RRHO_decomposition_20261007/Pd_RRHO_DECOMPOSITION.json",
        "sha256": "34801f3d232718f9dba50acd8d91f6d230f30398d2e33bed81b6d4cc848850bd",
        "kind": "returned_HPC_analysis"
      }
    ]
  }
]
```


证据记录：`E0040`。

```json
[
  {
    "source_locator": "main p4; SI10–12,50–53",
    "actual_result": "低势垒局部H2生成与有效Pd物种的条件性恢复得到真实路径/端点/配平热力学支持；精确INTG热项仍差0.000278Eh，但不改变该范围内的源核心低势垒结论，且不被用作校准速率。",
    "reason": "原尺度适用于同一势垒并有新取向/响应网格/公式控制；更强动力学及精确源分量是明确例外。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/native_evidence.json",
        "sha256": "e9732a2b03c35b5a7bb2fba5ea1bf9a9c3d108a3a81488cdc307cccb00d012c0",
        "kind": "retained_HPC_native_reparse"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/irc_continuation_audit.json",
        "sha256": "bbd237c2e3f43dbf053782f22f2d91f2b0707d57ca8405872d38de5c817ea3ee",
        "kind": "retained_HPC_connection_audit"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/result.json",
        "sha256": "5e07b695904542d070aeb9480ee503c90f26edc76059383160349966c26f7507",
        "kind": "returned_HPC_comparison"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_RRHO_decomposition_20261007/Pd_RRHO_DECOMPOSITION.json",
        "sha256": "34801f3d232718f9dba50acd8d91f6d230f30398d2e33bed81b6d4cc848850bd",
        "kind": "returned_HPC_analysis"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 43.54 小时；30 份计时日志/39 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 4,20 线程/进程；Gaussian %Mem=12GB,24GB,80GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0003 · Pd_CPHF_grid_control/INTG/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/INTG/gaussian.log) | Gaussian:4355.2 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0004 · Pd_CPHF_grid_control/TS6/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/TS6/gaussian.log) | Gaussian:4397.3 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0005 · H2_MN15_gas_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/gaussian.log) | Gaussian:3.2 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0006 · boundH2_MN15_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/gaussian.log) | Gaussian:1999.4 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0007 · hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log) | Gaussian:3993.5；Gaussian:3080.1 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0008 · hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_forward_irc_20260915_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_forward_irc_20260915_hpc20_p6/stdout.log) | Gaussian:10453.8 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0009 · hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_reverse_irc_20260915_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_reverse_irc_20260915_hpc20_p6/stdout.log) | Gaussian:3947.2 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0010 · hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log) | Gaussian:2.5；Gaussian:1.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0011 · hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/stdout.log) | Gaussian:2237.6 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0012 · hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log) | Gaussian:3303.9；Gaussian:3027.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0013 · local_stage_tests_20260914/int_g_full_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/stdout.log) | Gaussian:3842.3 | 正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0014 · local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/stdout.log) | Gaussian:7154.4；Gaussian:6387.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0015 · local_stage_tests_20260914/ts6_full77_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/stdout.log) | Gaussian:3144.7 | 正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0016 · local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/stdout.log) | Gaussian:6320；Gaussian:6466.2 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0017 · local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log) | Gaussian:7028.1；Gaussian:4586.2 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0077 · hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/stdout.log) | Gaussian:1.1 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0078 · DMAc_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/gaussian.log) | Gaussian:77.5；Gaussian:13.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0079 · DMAc_MN15_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/gaussian.log) | Gaussian:17.4 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0080 · PdDMAc_A_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/gaussian.log) | Gaussian:14197.4；Gaussian:4323.2 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0081 · PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/gaussian.log) | Gaussian:2862.4 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0082 · PdDMAc_B_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/gaussian.log) | Gaussian:16430.6；Gaussian:4687 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0083 · PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/gaussian.log) | Gaussian:3434.8 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0084 · Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log) | Gaussian:1843.3 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0085 · H2_PBE0D3_TZ_gas_sp/attempt_01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_PBE0D3_TZ_gas_sp/attempt_01/stdout.log) | Gaussian:1.2 | 正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0086 · boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log) | Gaussian:2459 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0087 · DMAc_PBE0D3_TZ_DMAC_sp/attempt_01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_PBE0D3_TZ_DMAC_sp/attempt_01/stdout.log) | Gaussian:40.2 | 正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0088 · PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log) | Gaussian:2745.2 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0089 · PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log) | Gaussian:11800 | 正常 | {"threads":[4],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0134 · cases/w12_Pd_standard_orientation_control/INTG_low.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/INTG_low.log) | Gaussian:3055.1 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0135 · reopen_Pd_fixpath_TS6_components/attempt_01/low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/low.log) | Gaussian:3004.5 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

INT-G热项有0.000287 Eh残差。近零H2释放+0.01158、溶剂捕获+0.40249 kcal/mol受标准态影响，不能借势垒容差认定唯一方向或完整催化循环。

```json
[
  "INT-G thermal component is not exact. The source fixed-geometry control has displacement failures and is a diagnostic; the actual optimized baseline is independently valid.",
  "Gas pressure, solution standard state and flexible-mode treatment matter for near-zero release/capture values.",
  "No unique photocycle, kinetic regeneration rate or full product yield is certified."
]
```


原独立审查的 `source_exceptions_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "The INTG thermal correction retains an unexplained ~.000278 Eh difference; source thermal components are not all numerically reproduced.",
  "The historical ±2 kcal/mol applies only to the same terminal barrier, not the near-zero release/capture energies or kinetic rates.",
  "Bound H2, released H2 and solvent-bound Pd are distinct models. No unique global mechanism, turnover frequency or kinetic regeneration proof is certified.",
  "The two-chamber gas experiment does not uniquely identify the computed local Pd intermediate."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/autonomous_research/paper_9132719dbf91c978.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_9132719dbf91c978/verified_computation_reference.md)；SHA-256 `51b2bd32a53718ffd2c6b50cee7c8185734f0d36e0e9bdea6054a622a2fa1b05`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_9132719dbf91c978.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_9132719dbf91c978.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0001_paper_9132719dbf91c978.json) | `47a945980f7b4e7a90a1f63ab26a2a858215e67eaa552382897df4d1e567b95b` | evidence_or_analysis |
| E0002 | [papers/paper_9132719dbf91c978/documents/supplementary_001.pdf](../../../../papers/paper_9132719dbf91c978/documents/supplementary_001.pdf) | `ae27addc290464f1b17ef3fbd0dd6cac8eb0830aa03cc0aaa686fd57321d2817` | source_document |
| E0003 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/INTG/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/INTG/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0003_native_excerpt.json) | `1e77e30b7c0377e8a7cf0ec8401ba8e8056b07f1433b94d91d7567175229642b` | native_output |
| E0004 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/TS6/gaussian.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/TS6/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0004_native_excerpt.json) | `a53b5d449c792ec7b9c0ed79f05cc4f68685d4b7a542d33a95392e09a0f50642` | native_output |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0005_native_excerpt.json) | `aeeb2a7a1a602753dce578e48f71e018766966724bd1c5ae132963e33c399f96` | native_output |
| E0006 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `8d135661977358f50159e502361d6118e31fa776c12273a383ccb9f1a2b89724` | native_output |
| E0007 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `bc0b01f71277550216b987008792da153c5163a3ecc8104eb2a206d0e81dd45f` | native_output |
| E0008 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_forward_irc_20260915_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_forward_irc_20260915_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `bdba081b46f8f220ffe545b79a35c6cc2ac68c2c41b016db0d93ee2c31a51e0c` | native_output |
| E0009 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_reverse_irc_20260915_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_reverse_irc_20260915_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0009_native_excerpt.json) | `bc9cc3d5ea8a2f85c78250e14841c562d3a8d3a5c064e590ef07e099a8155b1a` | native_output |
| E0010 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0010_native_excerpt.json) | `4e94272743d191e733022d26a1e90a3addd77d779262eddf54c20a95f080ace9` | native_output |
| E0011 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0011_native_excerpt.json) | `c0802ae95df10802eea1934925b066b2a19762772b2880cc6548ccea5405d88e` | native_output |
| E0012 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0012_native_excerpt.json) | `eb403e351db5d2189986792e4128a7229ab94eeb998283d26ef5d2d656055ca7` | native_output |
| E0013 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0013_native_excerpt.json) | `951fe8d36d36ab59070c53e3c2085085063f58c791a19e7687290516b7a6faa6` | native_output |
| E0014 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0014_native_excerpt.json) | `feac759505b56f8aca946c0d1679c4a0d0ebaf278e3c3cdeab49070a8ad63d7d` | native_output |
| E0015 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0015_native_excerpt.json) | `f0f59ea8268056ea6a13d4c1ab197ca46b650e1f2869fd554b25c435cb4c1cbf` | native_output |
| E0016 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0016_native_excerpt.json) | `0ad35b6d99f5d3b1c80fd59a57fc775eaffcf8db5f23ab0116f9bd3342697ac8` | native_output |
| E0017 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0017_native_excerpt.json) | `c041c72e962810d5fc9e54c9e729733e9cb8aae9de67d0922ff1a170e8dfdf33` | native_output |
| E0018 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/native_evidence.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/native_evidence.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0018_native_evidence.json) | `e9732a2b03c35b5a7bb2fba5ea1bf9a9c3d108a3a81488cdc307cccb00d012c0` | evidence_or_analysis |
| E0019 | [tasks/final_verified_paper_reproduction/paper_9132719dbf91c978/evaluation/scoring_rules.json](../../../final_verified_paper_reproduction/paper_9132719dbf91c978/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0019_scoring_rules.json) | `78e096eb4a6cfb9a86a01f676d4cbcefc7cf67894540cbe265dc3bd569773fdb` | historical_task_binding |
| E0020 | [tasks/v2_paper_reproduction/paper_9132719dbf91c978/agent_input/task.md](../../../v2_paper_reproduction/paper_9132719dbf91c978/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0020_task.md) | `888e4c34a43d1279c27ab73e69523e8d19d639250891a432c104034b1c7b1447` | historical_task_binding |
| E0021 | [tasks/v2_paper_reproduction/paper_9132719dbf91c978/evaluation/reference_key_points.json](../../../v2_paper_reproduction/paper_9132719dbf91c978/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0021_reference_key_points.json) | `746ab3113c9ddbb15ba25a1ae01ca9481cc3aaeb8121db6116e84dc807a7f664` | historical_task_binding |
| E0022 | [tasks/v2_paper_reproduction/paper_9132719dbf91c978/evaluation/reference_conclusions.json](../../../v2_paper_reproduction/paper_9132719dbf91c978/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0022_reference_conclusions.json) | `08fc4869b123b3a02580a4186d2e269101d800f6a74197af98a2aaab90b2596e` | historical_task_binding |
| E0023 | [tasks/v2_autonomous_research/paper_9132719dbf91c978/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0023_task.md) | `41e78fee8f36514bf672a64633bdf4ea61b6b7fd344c4aff940902e31e4a1415` | historical_task_binding |
| E0024 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_9132719dbf91c978/FILE_INTEGRITY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_9132719dbf91c978/FILE_INTEGRITY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0024_FILE_INTEGRITY.json) | `3fef6d3db389d79364ac039168470214886b24e9f0c3a9dc1a2cafa9108092d7` | evidence_or_analysis |
| E0025 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_9132719dbf91c978/COMPUTATION_COVERAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_9132719dbf91c978/COMPUTATION_COVERAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0025_COMPUTATION_COVERAGE.json) | `917cd72dba72595e817a1ea6c8b0c6973e627e347d5f282135df6bfc2bdc4070` | evidence_or_analysis |
| E0026 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_9132719dbf91c978.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_9132719dbf91c978.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0026_paper_9132719dbf91c978.md) | `7ee7a499e615221ee767e9ff983cdd600c721be2674cefd42dfc80d827f812b1` | evidence_or_analysis |
| E0027 | [docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `ba94b5cfae61557acac091b753eee5972c44f1293b01f7a68443956ec8e953a4` | historical_task_binding |
| E0028 | [tasks/v2_paper_reproduction/paper_9132719dbf91c978/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/paper_reproduction/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot) | `ba94b5cfae61557acac091b753eee5972c44f1293b01f7a68443956ec8e953a4` | historical_task_binding |
| E0029 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/result.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0029_result.json) | `5e07b695904542d070aeb9480ee503c90f26edc76059383160349966c26f7507` | evidence_or_analysis |
| E0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/irc_continuation_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/v2_execution_20260929/papers/paper_9132719dbf91c978/irc_continuation_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0030_irc_continuation_audit.json) | `bbd237c2e3f43dbf053782f22f2d91f2b0707d57ca8405872d38de5c817ea3ee` | evidence_or_analysis |
| E0031 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_RRHO_decomposition_20261007/Pd_RRHO_DECOMPOSITION.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_RRHO_decomposition_20261007/Pd_RRHO_DECOMPOSITION.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0031_Pd_RRHO_DECOMPOSITION.json) | `34801f3d232718f9dba50acd8d91f6d230f30398d2e33bed81b6d4cc848850bd` | evidence_or_analysis |
| E0032 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_9132719dbf91c978/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_9132719dbf91c978/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0032_task.md) | `41e78fee8f36514bf672a64633bdf4ea61b6b7fd344c4aff940902e31e4a1415` | historical_task_binding |
| E0033 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_9132719dbf91c978/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_9132719dbf91c978/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0033_reference_key_points.json) | `746ab3113c9ddbb15ba25a1ae01ca9481cc3aaeb8121db6116e84dc807a7f664` | historical_task_binding |
| E0034 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_9132719dbf91c978/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_9132719dbf91c978/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0034_reference_conclusions.json) | `08fc4869b123b3a02580a4186d2e269101d800f6a74197af98a2aaab90b2596e` | historical_task_binding |
| E0035 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_9132719dbf91c978/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_9132719dbf91c978/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0035_scoring_rules.json) | `b04fed9553eec51f934e2b60ef42b7c9f48ff9b84f98f6c83566fb348796a0d9` | historical_task_binding |
| E0036 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_9132719dbf91c978/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_9132719dbf91c978/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0036_task.md) | `888e4c34a43d1279c27ab73e69523e8d19d639250891a432c104034b1c7b1447` | historical_task_binding |
| E0037 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_9132719dbf91c978/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_9132719dbf91c978/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0037_reference_key_points.json) | `746ab3113c9ddbb15ba25a1ae01ca9481cc3aaeb8121db6116e84dc807a7f664` | historical_task_binding |
| E0038 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_9132719dbf91c978/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_9132719dbf91c978/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0038_reference_conclusions.json) | `08fc4869b123b3a02580a4186d2e269101d800f6a74197af98a2aaab90b2596e` | historical_task_binding |
| E0039 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_9132719dbf91c978/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_9132719dbf91c978/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0039_scoring_rules.json) | `b04fed9553eec51f934e2b60ef42b7c9f48ff9b84f98f6c83566fb348796a0d9` | historical_task_binding |
| E0040 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/959aa9a16414e679_W12.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/959aa9a16414e679_W12.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0040_959aa9a16414e679_W12.json) | `959aa9a16414e67923a5adbb0d13062155577e783d6da486a04f2f1fc516be3a` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W12.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W12.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0041_W12.json) | `959aa9a16414e67923a5adbb0d13062155577e783d6da486a04f2f1fc516be3a` | evidence_or_analysis |
| E0042 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/5cbac0a34b1eda0d_paper_9132719dbf91c978_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/5cbac0a34b1eda0d_paper_9132719dbf91c978_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0042_5cbac0a34b1eda0d_paper_9132719dbf91c978_delivery_integrity.json) | `5cbac0a34b1eda0da4e91ebba07072eb918a635c7a03492cdcd33f8b6ee8fec9` | evidence_or_analysis |
| E0043 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_9132719dbf91c978_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_9132719dbf91c978_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0043_paper_9132719dbf91c978_delivery_integrity.json) | `5cbac0a34b1eda0da4e91ebba07072eb918a635c7a03492cdcd33f8b6ee8fec9` | evidence_or_analysis |
| E0044 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/481b09efed3f0eaa_paper_9132719dbf91c978_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/481b09efed3f0eaa_paper_9132719dbf91c978_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0044_481b09efed3f0eaa_paper_9132719dbf91c978_primary_pages.json) | `481b09efed3f0eaadcd4364edf7586a9bacdeb67c0e4a4c4fa3409babf4aa376` | evidence_or_analysis |
| E0045 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_9132719dbf91c978_primary_pages.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_9132719dbf91c978_primary_pages.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0045_paper_9132719dbf91c978_primary_pages.json) | `481b09efed3f0eaadcd4364edf7586a9bacdeb67c0e4a4c4fa3409babf4aa376` | evidence_or_analysis |
| E0046 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/5506695a100bd836_paper_9132719dbf91c978_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/frozen/5506695a100bd836_paper_9132719dbf91c978_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0046_5506695a100bd836_paper_9132719dbf91c978_native_readback.json) | `5506695a100bd836e8665312af6c0a8fa5572ecb238450db55d6a806e14b5ffe` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_9132719dbf91c978_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/coordinator_review/paper_9132719dbf91c978_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0047_paper_9132719dbf91c978_native_readback.json) | `5506695a100bd836e8665312af6c0a8fa5572ecb238450db55d6a806e14b5ffe` | evidence_or_analysis |
| E0048 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/INTG/input.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/INTG/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0048_input.com) | `df4e372c6cfacdc8f6d7242d8271a08a6b5f0a6f83a7ad1f50976d906f7f9ab3` | input_or_analysis_code |
| E0049 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/TS6/input.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/TS6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0049_input.com) | `69a2609755cdee77739f2f9d4a1edec17122fa65fd322aee597581fa38bd01e2` | input_or_analysis_code |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0050_geometry.xyz) | `4daf0003ecd45825715a4f1a988a85d8c69c97c0b6455b536a07e589e1dd21f6` | input_or_analysis_code |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0051_final_geometry.xyz) | `4d1319cb328400ec0eb64a654c0af3795e93c4d0b8c2518860ecb1b9395f4420` | input_or_analysis_code |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0052_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0053_input.com) | `9539b7c772d9b6ea669659f4a19d3b1d2ccf8913a74bfe17e823d543fb202d6e` | input_or_analysis_code |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0054_geometry.xyz) | `0dbead182e10288045b9ee78393844a8f3aba25042d690911769f00ccdc504f2` | input_or_analysis_code |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0055_final_geometry.xyz) | `8f24f0df22613b56cbfd28af517536fddf39796c1b3036dd78abb9531821f7bd` | input_or_analysis_code |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0056_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0057_input.com) | `72135219d9f9c729a2e287ba4132303849df0227bd5381d211667b34407ff4cd` | input_or_analysis_code |
| E0058 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_forward_irc_endpoint_optfreq_20260916_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0058_input.com) | `b7c767759274bb7d0096c1022b6eb60c7cc2a82a67b8290e5ec36bbc2d75212a` | input_or_analysis_code |
| E0059 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_forward_irc_20260915_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_forward_irc_20260915_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0059_input.com) | `6d1caea1887e72898e4775861e861d58b66e04cccb7a34aff1226009efc244a1` | input_or_analysis_code |
| E0060 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_reverse_irc_20260915_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_full77_si_pbe1pbe_computed_parent_reverse_irc_20260915_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0060_input.com) | `2caa3af5f3d6b03d020f6923c8afee9821d3414f74b175b8d2c2711b803a8474` | input_or_analysis_code |
| E0061 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/entrypoint.sh](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0061_entrypoint.sh) | `e7b8fe2066e911e45aebd73f23efc6e83f7443bd4d62de86a63372074e8e7570` | input_or_analysis_code |
| E0062 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/production.sh](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/production.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0062_production.sh) | `e1a3ccee63c25cb70a0168524054223009b9aef9dd45a337d23613550dd8556e` | input_or_analysis_code |
| E0063 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_optfreq_20260922_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0063_input.com) | `31b59001b75f828ae1aff29694d4fc916a64f276520cde82ed839fab4a27f7a2` | input_or_analysis_code |
| E0064 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/entrypoint.sh](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0064_entrypoint.sh) | `b3d49fe91a452b46d5412246630d6e4f389f67ed679b208fbd8553ae962883d2` | input_or_analysis_code |
| E0065 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/production.sh](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/production.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0065_production.sh) | `21061fe82fa9e38bb9f5aa3e97929fc4a5a5e9332d62f280315fdd99dfafbbc4` | input_or_analysis_code |
| E0066 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_mn15_dmac_sp_20260922_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0066_input.com) | `87cd8cbc20895ec2ad258c174a26f203383889b485b7f288506a1d8ddfba1770` | input_or_analysis_code |
| E0067 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/entrypoint.sh](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0067_entrypoint.sh) | `f927fb2759131cf43aa7b6399e4a49fd95d4c507ccd82a07442d3beb3e8de7a8` | input_or_analysis_code |
| E0068 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/production.sh](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/production.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0068_production.sh) | `ea11e870289de2844b9914e77af7f8498f2d498d5d95733fd7c06d5aa6c7f4f2` | input_or_analysis_code |
| E0069 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_pd0_source_optfreq_20260922_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0069_input.com) | `f6b51f2e36d0757c7746fc9d4fe8f3a964da3c16b8f1b817275d51c31655901b` | input_or_analysis_code |
| E0070 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0070_input.com) | `2fb085fec70ae569d073cfd4ae12543d23bbbb2aa85fa9e54271d011bd0c5e61` | input_or_analysis_code |
| E0071 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/int_g_full_si_pbe1pbe_optfreq_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0071_input.com) | `2931e5d2f9c7cc3c707f39d44a1565504f85eb90b3466c96cbe5edcbeeac9091` | input_or_analysis_code |
| E0072 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_computed_parent_mn15_dmac_sp_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0072_input.com) | `f62ead93e303b45445a073c2de70a8402efef25111f0712800af8107e5eb2802` | input_or_analysis_code |
| E0073 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_full77_si_pbe1pbe_optfreq_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0073_input.com) | `e97796f6b53d2f3b039cad22487d0508df2ecd5487bb12d43df69b43c563e474` | input_or_analysis_code |
| E0074 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/local_stage_tests_20260914/ts6_reverse_irc_endpoint_optfreq_20260916/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0074_input.com) | `1ed8e64f30c6a68307e026554364157454be944a280618c67dd763e5846a14ba` | input_or_analysis_code |
| E0075 | [papers/paper_9132719dbf91c978/documents/main.pdf](../../../../papers/paper_9132719dbf91c978/documents/main.pdf) | `3d08d907aafb9175e71858913e8f6671891645f0479d189eab246a24d442faeb` | source_document |
| E0076 | [.software_cache/installations/gaussian/g16/install/g16/l202.exe](../../../../.software_cache/installations/gaussian/g16/install/g16/l202.exe) | `2dfb4983c8ea6b0c23808c20bdbee38cf39092d25314fae41dcbb920108d94ac` | evidence_or_analysis |
| E0077 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0077_native_excerpt.json) | `2f9661aa7f20506522cc83233b3137ecfd88befe0a6550e3925391683cc9c80a` | native_output |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0078_native_excerpt.json) | `3951f5c6c0588f133eef3ab410f9c077fc4233dff4038f79919e1ff4688e62f7` | native_output |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0079_native_excerpt.json) | `c9c3a8c3fe5da7341320a67ddfeeedc995bfbed89b00ed34e87feac5ea283cf1` | native_output |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0080_native_excerpt.json) | `73c9443ffe7a057998432ee3942abe99ae49999021487e09bf20880aed463376` | native_output |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0081_native_excerpt.json) | `52216ca6248a6d922e4e2b14ccea7af7afe8ea04b1944cd16d850b119b5f2b86` | native_output |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0082_native_excerpt.json) | `093e87debd244da4997f8cd35fe73cfec653eed22429e7c9162b6df1f33cd799` | native_output |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0083_native_excerpt.json) | `ccd42efd21668438e16a92d5a8da95a0e3cca3ad332b305d56220780aaefada4` | native_output |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0084_native_excerpt.json) | `9c76b583c17aa5631e14ca7e629e0da2e64dbf72cb5e62730d448564023cf6a9` | native_output |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_PBE0D3_TZ_gas_sp/attempt_01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_PBE0D3_TZ_gas_sp/attempt_01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0085_native_excerpt.json) | `eb47eef5bc4f5e577548502f2aad3cde50cd3b7c5f1546d1db49acef989b0163` | native_output |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0086_native_excerpt.json) | `b8979b786c3b018a758a7debde540adbd32c62e11a394405a6051d72994534ba` | native_output |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_PBE0D3_TZ_DMAC_sp/attempt_01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_PBE0D3_TZ_DMAC_sp/attempt_01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0087_native_excerpt.json) | `58bcc3fee76090b839537ab349e0fbd4d106e620b54f8c0b1d459e89b0091945` | native_output |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0088_native_excerpt.json) | `58b80aea7680fa86854951034caea628eb0558cc0525c5bafae49ea6b0f763b3` | native_output |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0089_native_excerpt.json) | `b64cec90e058ae0da19dfb773fc0d55a2aac537d375a03783811e854218600f2` | native_output |
| E0090 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/SOURCE_MANIFEST.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/SOURCE_MANIFEST.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0090_SOURCE_MANIFEST.json) | `8821b2978fa927c91c54178ac919406cc38b05c09f3d46923145fe068e42fc02` | evidence_or_analysis |
| E0091 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_9132719dbf91c978/REVIEW.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_9132719dbf91c978/REVIEW.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0091_REVIEW.json) | `2eb8f8b85a0e4a821471def4ffa97100d06a782c5579ac8ba37865c498d6f022` | evidence_or_analysis |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0092_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0093_submission.json) | `1330353f01a4bfa81378ee3b155ff2e5788c530f2044330cc4ed41b5233eed32` | evidence_or_analysis |
| E0094 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0094_status.json) | `42f1bc78f12c812545b004670de2441ea05f9149238e7608f4d9301693a7b9e5` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/submit-intent.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0095_submit-intent.json) | `5434452dd2fc123f4b5436f02a9329bcbedd3a46cf1307f7b5c787ce19b15afd` | evidence_or_analysis |
| E0096 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0096_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0097 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0097_submission.json) | `2daef2febe25ecbf9d0c645f88e24b5a5f88fd0aabb84285e9416ed90936f8b8` | evidence_or_analysis |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0098_status.json) | `537ee6c41464218de833a88cd07f5c1ebbb867c85882646296ca0b3555663c61` | evidence_or_analysis |
| E0099 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/submit-intent.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0099_submit-intent.json) | `f3d76e580311f369a1a81d4d1afd8c95bab660fcb7e0d5ab0066e5c7cfee0e05` | evidence_or_analysis |
| E0100 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0100_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0101 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0101_submission.json) | `50383cda2bd86955ae86170a5c784166512507cbcaa08af7fade728bb4a45116` | evidence_or_analysis |
| E0102 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0102_status.json) | `e24ad7839913347ed306b9e50142f7f8b8f7470f486551af14accf78a6011d79` | evidence_or_analysis |
| E0103 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/submit-intent.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0103_submit-intent.json) | `045c1c84bd523e0d6e46d330ee7e0cca93dd6bb077dba7d6eda4cfbd9dfb8c8d` | evidence_or_analysis |
| E0104 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0104_input.com) | `19e377dc35ef8b7cf855d292d68b7b174695d2ce155b24359b161419801143a1` | input_or_analysis_code |
| E0105 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0105_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0106 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0106_submission.json) | `d39ccc05c2f86302ad83042037b0bc7d37e17cc062046f31849490b4ecf6ddbb` | evidence_or_analysis |
| E0107 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0107_status.json) | `8d4d4587a234f6e5bf986ef55c319d5c330e0001f19c92c04081907d6eed0972` | evidence_or_analysis |
| E0108 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/submit-intent.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0108_submit-intent.json) | `261ad1ff9365d9bd8f63186a5053a6bf277bff3beab47000145546ed935e3b3e` | evidence_or_analysis |
| E0109 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0109_input.com) | `90d642faddaeae9aeead2d150ed6340dfe50141decbef53c70a955cf0c62dfbc` | input_or_analysis_code |
| E0110 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0110_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0111 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0111_submission.json) | `1fb925db5ad16e7b5ac112a4214716b032728f714721b521e6f40fd8021fadbe` | evidence_or_analysis |
| E0112 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0112_status.json) | `d9cdce842b8cb8a898a5746281754ce98222ed2dc1465ba55cc2091cfcda8097` | evidence_or_analysis |
| E0113 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/submit-intent.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0113_submit-intent.json) | `e44276ace8293967c2d9e68d879237911e69164f5c6afe91fef73fc638e12432` | evidence_or_analysis |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0114_input.com) | `41eb038455e3725174f1631a39d6cdc8aed426b2be29f0718f3d5ab8b3e37a50` | input_or_analysis_code |
| E0115 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0115_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0116 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0116_submission.json) | `31f4d9bcd79c7486517451bae51d6f183498f887aae1e3468bb40825147ca4d8` | evidence_or_analysis |
| E0117 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0117_status.json) | `1dfe2ae88f2ec5e66405536423cfef89d5b55eff14c971dd29421f1a784ca5bd` | evidence_or_analysis |
| E0118 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/submit-intent.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0118_submit-intent.json) | `12ff7ae91abf9f2a4a5efd7590adb406ccfb8e76d9ff72439121d802409b6799` | evidence_or_analysis |
| E0119 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0119_input.com) | `c23317d606f01128501cc068daa4a542bd58a958f4e475666cd55421cc9895ca` | input_or_analysis_code |
| E0120 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0120_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0121 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0121_submission.json) | `1fe0a3624906235c63b1ac933c65b4cc4334bad6e94338bed38febf4e080e3eb` | evidence_or_analysis |
| E0122 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0122_status.json) | `d6670c84efb2a07261e90f5eea6e3b68d03cfd6d9e95cf9260fe828377a178ef` | evidence_or_analysis |
| E0123 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/submit-intent.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0123_submit-intent.json) | `87a1bb9ae10369a5f304f7217f5131888a0b1c2ceace0445fc7ea81a82beda07` | evidence_or_analysis |
| E0124 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0124_input.com) | `5fcbca3623a5c9d2fd590df1e9d9187bbd6c498d638e79d83a10cfa2a699490a` | input_or_analysis_code |
| E0125 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/native-return-code.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0125_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0126 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/submission.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/submission.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0126_submission.json) | `4cd373cc50af8e4e876d764923f59c92b46b5dfb327b250ca97cc3e2396bf59a` | evidence_or_analysis |
| E0127 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0127_status.json) | `c881f5d5022bbff4ad533678101160e679f90aeb98254612b56ccbf217609e44` | evidence_or_analysis |
| E0128 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/submit-intent.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/submit-intent.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0128_submit-intent.json) | `873369a3b3950e5d6e8c4721bc6a055997b1ebffd8c4fd6c9575a2ebc2b4aade` | evidence_or_analysis |
| E0129 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0129_input.com) | `f6b836c2c6fffc70a110d823862ccbf0436cbb40636b688e0122d20395484ca7` | input_or_analysis_code |
| E0130 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/INTG/native-return-code.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/INTG/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0130_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0131 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/TS6/native-return-code.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/reaudit_20261008/Pd_CPHF_grid_control/TS6/native-return-code.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0131_native-return-code.txt) | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` | evidence_or_analysis |
| E0132 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_RRHO_decomposition_20261007/result.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_RRHO_decomposition_20261007/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0132_result.json) | `9246d778acc621fe81f44e363ea47cd17b0ed02e237220f4361cd0531712bea3` | evidence_or_analysis |
| E0133 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_orientation_component_intake/result.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_orientation_component_intake/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0133_result.json) | `f7e705552f0b3e870bdc6f79575600a6a3698c9acf52f4c6d74e7ac2a1b0b848` | evidence_or_analysis |
| E0134 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/INTG_low.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/INTG_low.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0134_native_excerpt.json) | `bc3448ee127cf1b4d5c0add0d95a9033dabfd056d95dd68fc80a1fbb81adb982` | native_output |
| E0135 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/low.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/low.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0135_native_excerpt.json) | `e01a82df4d995057cfc4578c072a10155166f5e6a6a6a70ee8ae62a1c902dbc8` | native_output |
| E0136 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/terminal_h2_closure_20260923/result.json](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/provenance/terminal_h2_closure_20260923/result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0136_result.json) | `71ae33985e006817eb1fe4c8ef9e39f590d75c2bab9498c329685e0cd88d1be4` | evidence_or_analysis |
| E0137 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W12_JOB_INTAKE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/deliveries/W12_JOB_INTAKE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0137_W12_JOB_INTAKE.json) | `3939baf1dd2d8636548b98d33da4624dc1c9a24077d973a7962fd4919019d904` | evidence_or_analysis |
| E0138 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_9132719dbf91c978/REPORT.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_9132719dbf91c978/REPORT.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0138_REPORT.md) | `b672e592316dd0bc40f2bea67eba7da6c10e2ae2221ed2b36ee4a2a728e30440` | evidence_or_analysis |
| E0139 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/entrypoint.sh](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/entrypoint.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0139_entrypoint.sh) | `baa0240d6a6c453ab276b1ffb7e98ddd6dcf64e14a3e8bd2c5f33e383da8a4f2` | input_or_analysis_code |
| E0140 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/production.sh](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/production.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0140_production.sh) | `ab8810cee095dbb3f9bf105c29fc893c51e334a5c8bc176c6f0b303727b8088f` | input_or_analysis_code |
| E0141 | [docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_9132719dbf91c978/hpc_runs/ts6_released_h2_source_mn15_dmac_sp_20260922_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0141_input.com) | `55a675b1161c813ef4c3be9de822663fb06755034b17899793c4d076d9162c75` | input_or_analysis_code |
| E0142 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0142_geometry.xyz) | `139e2dea96d40af34394412fa5756c7ba8e67de4c566694b6cea3716dcd703be` | input_or_analysis_code |
| E0143 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0143_final_geometry.xyz) | `bacbed8ec8c3cf3f4e0fddc7517a6d3c0ec908e1ffbf47d7f9a2c973d04bb18c` | input_or_analysis_code |
| E0144 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0144_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0145 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0145_geometry.xyz) | `25056f2221fe6f102ab5cec74e890d142cb86f0d7fb04a3f9b1976f994341a44` | input_or_analysis_code |
| E0146 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0146_final_geometry.xyz) | `bf6cb9e9de993fb6dabce8f4a413bbf19a031880c28e0f3a22c7827cec2d5edd` | input_or_analysis_code |
| E0147 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0147_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0148 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0148_geometry.xyz) | `ce3773b5d8078c1dea9417858440554e867295d87c4dfcf1ef1ee93c13de5b8a` | input_or_analysis_code |
| E0149 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0149_final_geometry.xyz) | `f8db2860ba632bc40ac79724a7754aa4fc473fa0a2b9ae4f1956bbd3a479a584` | input_or_analysis_code |
| E0150 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0150_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0151 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0151_geometry.xyz) | `2552d3e88a5ec9a29a3f944a67791410b17f36bd0843b4ffd88c109b93738b8c` | input_or_analysis_code |
| E0152 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0152_final_geometry.xyz) | `6fa739d69ea0d3a3d9e80ff545b51e26597b3ae091d9cad11695176380ffff4c` | input_or_analysis_code |
| E0153 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0153_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0154 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0154_geometry.xyz) | `c5ad9880171a533e9523d48520d95f7aa71826060086d7b49148c5ebe92d8e88` | input_or_analysis_code |
| E0155 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0155_final_geometry.xyz) | `5d83410a666a21d2487f1c2b13f82e567eb25d66897d6adccf99e6fa370ecfee` | input_or_analysis_code |
| E0156 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0156_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0157 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0157_geometry.xyz) | `0d31708e2696e99643141035faa9c323d01e5280b3c19bf3144937acb9d825ad` | input_or_analysis_code |
| E0158 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0158_final_geometry.xyz) | `9115ad094043923f7121e85019b8f0af78e2584b92a15f6c0962d8886eefeed9` | input_or_analysis_code |
| E0159 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0159_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0160 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0160_geometry.xyz) | `3d9cdac1189d054e0ba8f08dde2aa20d8da22e637fe07f772b901738c39e893e` | input_or_analysis_code |
| E0161 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0161_final_geometry.xyz) | `6cabefda1d265f375af4044914ff7c02c0be391985998b1420be1ddb785f45ed` | input_or_analysis_code |
| E0162 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0162_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0163 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/Pd0_PBE0D3_TZ_DMAC_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0163_input.com) | `4c78d2b3004376a68e5f385136c6540f1dba3ad0fbb68b36abf0bf2a4a3c5ddb` | input_or_analysis_code |
| E0164 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_PBE0D3_TZ_gas_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_PBE0D3_TZ_gas_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0164_geometry.xyz) | `b1d7de856061e34238a1c4f59df1b47a4986c129c734be0755ef63191045b130` | input_or_analysis_code |
| E0165 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_PBE0D3_TZ_gas_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_PBE0D3_TZ_gas_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0165_final_geometry.xyz) | `d8d3d6faaf6a1cc1f7ab3429457296e5923fc1cb6fbfe07c43237f667e502500` | input_or_analysis_code |
| E0166 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_PBE0D3_TZ_gas_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_PBE0D3_TZ_gas_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0166_input.com) | `e313292726cf3f6fd0566b5e9d36deab8d84fcfc55a3fe6f89f5f9d3ed375506` | input_or_analysis_code |
| E0167 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0167_geometry.xyz) | `e08b0a8c03574cd48fd672bf4a34735bc85d401dbda9d6c8906bd66c771cd35f` | input_or_analysis_code |
| E0168 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0168_final_geometry.xyz) | `823634754cec1947bc8ebc08fbe60d984d0e04ca7ad296b52b04df4c98b3d565` | input_or_analysis_code |
| E0169 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0169_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0170 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_PBE0D3_TZ_DMAC_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0170_input.com) | `f5355aea51d5a7487eb1dfafd38b04abfb7e9878a949bd3698352820e30b2aa9` | input_or_analysis_code |
| E0171 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_PBE0D3_TZ_DMAC_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_PBE0D3_TZ_DMAC_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0171_geometry.xyz) | `f5e8ba2004446c9e56f3fb3277b3eccf6cf0d3a7d13f6bf047b3b7e3707fdbc9` | input_or_analysis_code |
| E0172 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_PBE0D3_TZ_DMAC_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_PBE0D3_TZ_DMAC_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0172_final_geometry.xyz) | `4ac4fa2d5e13e2270b4d4fe805b7c856f0df34ea0d6faa5aede88d2cbb582e8c` | input_or_analysis_code |
| E0173 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_PBE0D3_TZ_DMAC_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_PBE0D3_TZ_DMAC_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0173_input.com) | `6ce74cf6d3e8ea00b16dbf04d6344d7de724c4cbfbda234721d32dabf2b845ca` | input_or_analysis_code |
| E0174 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0174_geometry.xyz) | `2552d3e88a5ec9a29a3f944a67791410b17f36bd0843b4ffd88c109b93738b8c` | input_or_analysis_code |
| E0175 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0175_final_geometry.xyz) | `5616c46c3dc33c63140201369aa240bb0066ca52388e16bf4c819e9d064616e4` | input_or_analysis_code |
| E0176 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0176_run.sh) | `e6ceca5bb8f5e15c8655b543b6e0dcb7064a72fac8c8f6cdb7011fb44eef255e` | input_or_analysis_code |
| E0177 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_PBE0D3_TZ_DMAC_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0177_input.com) | `2c1ce258d14725262ed7d3fcee4d481add764127820402d378fb175f39afe282` | input_or_analysis_code |
| E0178 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0178_geometry.xyz) | `0d31708e2696e99643141035faa9c323d01e5280b3c19bf3144937acb9d825ad` | input_or_analysis_code |
| E0179 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/final_geometry.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/final_geometry.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0179_final_geometry.xyz) | `d87929508249ea539f9a06393a29a7e56f0a105beb00aa69ebd106659ee7aeb9` | input_or_analysis_code |
| E0180 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0180_run.sh) | `8afbf517f7c9c80e40f5efb4cbf944caa0bd8beefc58b687d37a60993d5c9041` | input_or_analysis_code |
| E0181 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_PBE0D3_TZ_DMAC_sp/attempt_01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0181_input.com) | `6a0698afe6992a93b16303849b620261fd1471a0bddb5ff3902f592ea0abfbc1` | input_or_analysis_code |
| E0182 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/inputs.sha256](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/boundH2_MN15_DMAC_sp/attempt_01/inputs.sha256) | `1d05d42d857caae9238629b1119c8b627d6872cd3fc630b8ab0302c407e475b4` | evidence_or_analysis |
| E0183 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/inputs.sha256](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/H2_MN15_gas_sp/attempt_01/inputs.sha256) | `b5b36fd58970154ab8245c11e3e5ca33560b36565635ffb5a8fa0b324c40a025` | evidence_or_analysis |
| E0184 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/inputs.sha256](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_source_optfreq/attempt_01/inputs.sha256) | `79662ea018787c7a8f76e761085c6e0458679f85336a531d5b7a9259d522ecbc` | evidence_or_analysis |
| E0185 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/inputs.sha256](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/DMAc_MN15_DMAC_sp/attempt_01/inputs.sha256) | `9af95e575b3271ccc1cc55cde99547a3384e113296213a9bac53d9886ee114ff` | evidence_or_analysis |
| E0186 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/inputs.sha256](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_source_optfreq/attempt_01/inputs.sha256) | `293e7b57f2b3075fb817d1b93a618f505c903349fa89dc6a0c3b44d985398599` | evidence_or_analysis |
| E0187 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/inputs.sha256](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_A_MN15_TZ_DMAC_sp/attempt_01/inputs.sha256) | `5f4ae18c0e1948bf402141049286e4efb667398116413e0664310c71fd82783c` | evidence_or_analysis |
| E0188 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/inputs.sha256](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_source_optfreq/attempt_01/inputs.sha256) | `a0d61a803611b0558d626e3cdc49ab66c6702d7e2bec334d180701fdd38541b7` | evidence_or_analysis |
| E0189 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/inputs.sha256](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/PdDMAc_B_MN15_TZ_DMAC_sp/attempt_01/inputs.sha256) | `83fe74ca43cb4c3bd800126fdf6b591d232b6ed56d4efd320ca3ce6a206174df` | evidence_or_analysis |
| E0190 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/analysis.py](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0190_analysis.py) | `cf9b57f7f1eba42188e3ac01039c40db7f85e6644ca3fe4ab2b02d062daef414` | input_or_analysis_code |
| E0191 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/run.sh](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0191_run.sh) | `444da105d85cf6838a2f71270fb890ef0a80a120bed9c2ce8f861c2d0ea05f0a` | input_or_analysis_code |
| E0192 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/TS6_high.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/TS6_high.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0192_TS6_high.com) | `a906c78ff1ecc669bcc711e0e365cd2beeda839833961eb32975ebaeb4166b89` | input_or_analysis_code |
| E0193 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/INTG_low.com](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W12/papers/paper_9132719dbf91c978/cases/w12_Pd_standard_orientation_control/INTG_low.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0193_INTG_low.com) | `06809a612bcd2b54015a59b80e58b1ce186629cc05428127feec3552a21f9d4d` | input_or_analysis_code |
| E0194 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/analysis.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/analysis.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0194_analysis.py) | `56b7265ba23ef46e8f20d1595f7de4cbce0584a8b4468075cbff45a44775f282` | input_or_analysis_code |
| E0195 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/low.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/low.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0195_low.com) | `d9c1502ed362f2f449ba6681bb68f868cb25e0c06d26d50d54e9f854e7b07440` | input_or_analysis_code |
| E0196 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/source.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/source.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0196_source.xyz) | `86194e7aa4f92663fd7b1a7480d4ad575ea94776a003e1178839048a1e568e95` | input_or_analysis_code |
| E0197 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/run.sh](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/run.sh)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0197_run.sh) | `2cef7a27f3010c8fab1e58bff7a32fed1205ff6d3e0b19eb89b798967788066f` | input_or_analysis_code |
| E0198 | [docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/high.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_6/papers/paper_9132719dbf91c978/outputs/reopen_Pd_fixpath_TS6_components/attempt_01/high.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_9132719dbf91c978/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0198_high.com) | `acdf4fe3a3e03fa938b1b7bf0a99e9b98aa8549b559b09d1d8807de994fbef3b` | input_or_analysis_code |
| N0199 | [tasks/v2_autonomous_research/paper_9132719dbf91c978/evaluation/reference_key_points.json](reference_key_points.json) | `746ab3113c9ddbb15ba25a1ae01ca9481cc3aaeb8121db6116e84dc807a7f664` | latest_review_evidence |
| N0200 | [tasks/v2_autonomous_research/paper_9132719dbf91c978/evaluation/reference_conclusions.json](reference_conclusions.json) | `08fc4869b123b3a02580a4186d2e269101d800f6a74197af98a2aaab90b2596e` | latest_review_evidence |
| N0201 | [tasks/v2_autonomous_research/paper_9132719dbf91c978/evaluation/scoring_rules.json](scoring_rules.json) | `b04fed9553eec51f934e2b60ef42b7c9f48ff9b84f98f6c83566fb348796a0d9` | latest_review_evidence |
| N0202 | [tasks/v2_autonomous_research/paper_9132719dbf91c978/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `f079b060fb427461eb04e85aa4b15dc60adeeff7a4938e577824ac45e6cd3311` | latest_review_evidence |
| N0203 | [tasks/v2_paper_reproduction/paper_9132719dbf91c978/evaluation/scoring_rules.json](../../../v2_paper_reproduction/paper_9132719dbf91c978/evaluation/scoring_rules.json) | `b04fed9553eec51f934e2b60ef42b7c9f48ff9b84f98f6c83566fb348796a0d9` | latest_review_evidence |
| N0204 | [tasks/v2_paper_reproduction/paper_9132719dbf91c978/evaluation/reference_validation_plan.md](../../../v2_paper_reproduction/paper_9132719dbf91c978/evaluation/reference_validation_plan.md) | `f079b060fb427461eb04e85aa4b15dc60adeeff7a4938e577824ac45e6cd3311` | latest_review_evidence |
| N0205 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0206 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_b_results.json) | `66b4df5fb10f6b54e16cafe1cc04f2dd2ed2ff67af141ca58d0b02b4d1b922f1` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_autonomous_research/paper_9132719dbf91c978/agent_input/task.md](../agent_input/task.md) | `41e78fee8f36514bf672a64633bdf4ea61b6b7fd344c4aff940902e31e4a1415` |
| [tasks/v2_autonomous_research/paper_9132719dbf91c978/evaluation/reference_key_points.json](reference_key_points.json) | `746ab3113c9ddbb15ba25a1ae01ca9481cc3aaeb8121db6116e84dc807a7f664` |
| [tasks/v2_autonomous_research/paper_9132719dbf91c978/evaluation/reference_conclusions.json](reference_conclusions.json) | `08fc4869b123b3a02580a4186d2e269101d800f6a74197af98a2aaab90b2596e` |
| [tasks/v2_autonomous_research/paper_9132719dbf91c978/evaluation/scoring_rules.json](scoring_rules.json) | `b04fed9553eec51f934e2b60ef42b7c9f48ff9b84f98f6c83566fb348796a0d9` |
| [tasks/v2_autonomous_research/paper_9132719dbf91c978/evaluation/critical_failures.json](critical_failures.json) | `5abb046d9e94a519f9e4ee5f4ff5604d0f59dd16b221af5c835965c1880b7956` |
| [tasks/v2_autonomous_research/paper_9132719dbf91c978/evaluation/evidence_map.json](evidence_map.json) | `604088d5082444bb0fec139f350f3839fd1d1a77e0f47c89a13b50ad5b52b035` |
| [tasks/v2_autonomous_research/paper_9132719dbf91c978/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `f079b060fb427461eb04e85aa4b15dc60adeeff7a4938e577824ac45e6cd3311` |

## Current scoring migration — 2026-10-19
Active policy: paper_science_v2, 100 binary scientific-result points with intermediate and final conclusions. Active rule/reference files supersede historical scoring weights or freezes. No process score or multiplier remains. This migration is not new computation or new chemical acceptance; independently strict frozen-scope status remains unchanged. Preserved limitations: INT-G thermal correction differs by about 0.000287 Eh (fixed-geometry control about 0.000278 Eh). Verified composite barrier 0.764432 versus source reconstruction 0.883282/printed 0.9 kcal/mol. Release +0.011582 and DMAc capture +0.402490/+0.658922 kcal/mol are verifier results, not paper targets, and their signs are reference-sensitive. No unique photocycle, local release rate, kinetic catalyst regeneration or yield is established.

## Scoring-contract repair — 2026-10-19, round 3

- Confirmed: the former universal near-thermoneutral requirement incorrectly elevated verifier +0.011582 kcal/mol at 1 atm into a paper result. Replaced with the concrete atom-balanced release/chemical-potential relation at the submitted pressure; source 0.9 kcal/mol formation barrier unchanged.

The source and native calculations above remain unchanged historical evidence. Active mode-specific rules govern current scoring; this edit does not certify a new chemistry run or alter strict acceptance.
