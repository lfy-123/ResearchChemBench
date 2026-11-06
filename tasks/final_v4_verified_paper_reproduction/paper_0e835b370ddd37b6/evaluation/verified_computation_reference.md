# 本次V3范围与逐命题证据复用（2026-10-28）

原三模型H2活化问题不变；保留六个最终G值及原±1.5 kcal/mol硬窗，取消排序重复分，将该项改为放能性不能证明快速活化的物理判别，取消逐模型TS/极化及轨道节点的独立分，保留两个独立电子解释。AR隐藏目标和机理；PR保留作者基线。

- `barrier_one`：正文Table 2；已核对原生日志G和finite_path_terminal_synthesis.json；六个G差均在原±1.5 kcal/mol窗口内。
- `reaction_one`：正文Table 2；已核对原生日志G和finite_path_terminal_synthesis.json；六个G差均在原±1.5 kcal/mol窗口内。
- `barrier_vprime`：正文Table 2；已核对原生日志G和finite_path_terminal_synthesis.json；六个G差均在原±1.5 kcal/mol窗口内。
- `reaction_vprime`：正文Table 2；已核对原生日志G和finite_path_terminal_synthesis.json；六个G差均在原±1.5 kcal/mol窗口内。
- `barrier_four`：正文Table 2；已核对原生日志G和finite_path_terminal_synthesis.json；六个G差均在原±1.5 kcal/mol窗口内。
- `reaction_four`：正文Table 2；已核对原生日志G和finite_path_terminal_synthesis.json；六个G差均在原±1.5 kcal/mol窗口内。
- `kinetic_thermodynamic_distinction`：原生势垒29.842468 < 33.065984 < 47.132237 kcal/mol；与正文排序一致。
- `one_vprime_explanation`：Si供体轨道实算−5.585887/−6.818064 eV及实际H-H/Si-H变化支持；OccSi定义未认证，不作硬指标。
- `four_design_explanation`：4/1受体−1.742499/−0.994000 eV、供体−5.980212/−5.585887 eV；模型4有限路径加端点证据，不等于完整IRC。

未提交新计算；以下历史正文逐字保留。历史PASS不代表新V3全部命题重新验证通过。

---

# V2 验证计算参考：三个silylene模型活化H2

论文：`paper_0e835b370ddd37b6`；模式：`paper_reproduction`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：冻结 V2 科学范围内独立严格通过（PASS_STRICT_CURRENT_FROZEN_SCOPE）。** 这不表示作者整篇所有数字、实验现象或题外机理都已重现。

当前验收依据：相对活化次序与放能性、限定的双亲电子解释支持当前核心科学问题。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

作者1/V′/4模型苯环境中的H2活化相对能力与有边界的电子/重组解释。

冻结题面中的科学目标：

Do the source silylene models1,V′ and4 differ meaningfully in their ability to activate H2, and what molecular explanation is supported by reproducible evidence within these model definitions?

论文复现模式还向 agent 披露下列作者计算基线；所需基线和有依据的替代路线均按本模式题面核对。

The authors use Gaussian09 PBE0-D3BJ/def2-TZVP withSMD benzene, frequencies andIRC,298K/1atm Gibbs energies; they also check singlet wavefunction stability and compare singlet–triplet gaps withB3PW91 andωB97XD (mainpp3–4; SIp7). They attribute H2 activation to Si donor/H–H antibonding interaction and ligand electronic properties. Table2 reports H2 activation barriers32.9,47.4 and29.0kcal/mol for1,V′,4, respectively, with source reaction energies; these are model-dependent computational claims, not measured barriers for the complete bulky experimental ligands. Reproduce/audit this baseline and examine whether it supports the explanation. SI TableS2 gives TS geometry/NBO summaries. Fixed strain–interaction decomposition and matched-HH scans were added by the benchmark and are not source obligations.

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_0e835b370ddd37b6/documents/main.pdf](../../../../papers/paper_0e835b370ddd37b6/documents/main.pdf) | `4481b439479e8874cffa309e47cec459ec33ca4d18be30b921e08b43a3233971` |
| [papers/paper_0e835b370ddd37b6/documents/supplementary_001.pdf](../../../../papers/paper_0e835b370ddd37b6/documents/supplementary_001.pdf) | `df2f9a3f458bd80190146adb77300f8cc65385fc12d2a5bba829e8d60a0e189c` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

PBE0-D3BJ/def2-TZVP、SMD苯、298K/1atm；各reactant/H2/TS/product的真实G与频率及有限路径证据。

1. 由 SI 绑定源 1、V′、4 与 H2 的完整模型：裸硅烯 55/36/48 原子，TS/产物 57/38/50 原子；4 的 N-phenyl、两个 SiMe3 与羰基结构保留。反应物为中性单重态硅烯和 H2，V′ 的截断模型不冒充实验大配体。

2. 复用已完成的 1/V′ 作者路线端点，补齐并核收模型 4 的反应物、TS、产物 Opt/Freq 及频率恢复。统一使用 PBE1PBE=PBE0/def2-TZVP、GD3BJ、SMD 苯、298 K/1 atm。三个反应物/产物为正曲率最低点，三个 TS 有对应 H–H/Si–H 运动的单虚频。

3. 检查实际路径/端点与相关键长变化以确认同一局部 H2 活化通道；只将已有有限连通证据用于其能支持的通道，不虚称未保存的完整路径计算。

4. 从原生 Gibbs 记录计算 G(TS)−G(silylene)−G(H2) 及 G(product)−G(silylene)−G(H2)。势垒为 33.065984/47.132237/29.842468 kcal/mol，反应 G 为 −29.098869/−20.574781/−33.808328；逐行对照正文 Table 2。

5. 将源/实算残差拆成 E+ZPE 与剩余热项，保留模型 4 约 0.8425 kcal/mol 势垒残差；结合实际供体/受体轨道、Si 投影及重组相关证据检验解释。支持 4<1≪V′ 的势垒顺序和双向供受电子/可变形性联合解释，不能由 donor 能量单独推出该顺序或精确速率。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

本篇没有统一格式的 COMPUTATION_STAGE 表；完整执行结果分别保存在独立复审和原 worker/原生分析记录。以下逐节点展开这些结果，原始运行、输入和脚本逐文件列于第 6 节及附件，不以缺少统一表格代替计算证据。

## 3. 论文结果、实际结果与合理误差依据

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| ΔG‡ 1/V′/4,kcal/mol | [32.9,47.4,29.0] | [33.0659842,47.1322366,29.8424681] | 实算−论文：[0.1659842,-0.2677634,0.8424681]； 本轮从原生G重算；0.84残差明显高于打印精度，不能宣称逐位复现，但4<1≪V′及3.22/14.07/17.29差与源同一反应比较一致。原生热项分解和已算控制限定误差。；源定位：main Table2 |
| ΔG反应1/V′/4,kcal/mol | [-29.4,-21.3,-33.9] | [-29.0988693,-20.5747806,-33.8083279] | 实算−论文：[0.3011307,0.7252194,0.0916721]； 三个显著放能结论保持；此为模型比较验收，非速率精度认证。；源定位：main Table2 |

### 既有验证保留的补充量与完整定义

| 量与单位 | 论文值／定义 | 实际结果 | 差值及接受依据 |
|---|---|---|---|
| 1 activation_barrier (kcal/mol) | 32.9 | 33.06598422628099 | PBE0-D3BJ/def2-TZVP, SMD benzene, 298 K/1 atm Gibbs energy relative to separated same-model silylene + H2. Native−source = 0.165984; E+ZPE component = 0.095381, remaining thermal component = 0.070603. Component accounting localizes the residual; it does not identify its cause or constitute an error bar. |
| 1 reaction_G (kcal/mol) | -29.4 | -29.098869331254072 | PBE0-D3BJ/def2-TZVP, SMD benzene, 298 K/1 atm Gibbs energy relative to separated same-model silylene + H2. Native−source = 0.301131; E+ZPE component = 0.124874, remaining thermal component = 0.176256. Component accounting localizes the residual; it does not identify its cause or constitute an error bar. |
| Vprime activation_barrier (kcal/mol) | 47.4 | 47.132236596879444 | PBE0-D3BJ/def2-TZVP, SMD benzene, 298 K/1 atm Gibbs energy relative to separated same-model silylene + H2. Native−source = -0.267763; E+ZPE component = -0.143072, remaining thermal component = -0.124691. Component accounting localizes the residual; it does not identify its cause or constitute an error bar. |
| Vprime reaction_G (kcal/mol) | -21.3 | -20.57478063558092 | PBE0-D3BJ/def2-TZVP, SMD benzene, 298 K/1 atm Gibbs energy relative to separated same-model silylene + H2. Native−source = 0.725219; E+ZPE component = -0.468750, remaining thermal component = 1.193969. Component accounting localizes the residual; it does not identify its cause or constitute an error bar. |
| 4 activation_barrier (kcal/mol) | 29.0 | 29.842468058018845 | PBE0-D3BJ/def2-TZVP, SMD benzene, 298 K/1 atm Gibbs energy relative to separated same-model silylene + H2. Native−source = 0.842468; E+ZPE component = 0.642570, remaining thermal component = 0.199898. Component accounting localizes the residual; it does not identify its cause or constitute an error bar. |
| 4 reaction_G (kcal/mol) | -33.9 | -33.80832793409764 | PBE0-D3BJ/def2-TZVP, SMD benzene, 298 K/1 atm Gibbs energy relative to separated same-model silylene + H2. Native−source = 0.091672; E+ZPE component = 0.277987, remaining thermal component = -0.186315. Component accounting localizes the residual; it does not identify its cause or constitute an error bar. |
| Si donor / acceptor orbital energies (eV) | {"1":[-5.59,-0.99],"Vprime":[-6.82,-1.32],"4":[-5.99,-1.75]} | {"1":[-5.5858866,-0.9940002],"Vprime":[-6.8180642,-1.3157514],"4":[-5.9802123,-1.7424993]} | Geometry-declared Si-localized donor/acceptor character in stable canonical MOs; not a claim to reproduce author OccSi. Energy and orbital identity agreement independently corroborates the mechanistic comparison; model4 differences are about 0.01 eV. |

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_identity — Exact source-model identity and H2 inventory

冻结要求：Preserve source1,V′,4 graphs including all specified substituents; distinguish truncatedV′ from the experimental bulky system. Validate any chosen states and H2/Si atom mapping; unconverged seeds are not minima. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：55/36/48反应物原子与57/38/50TS/产物对象正确，model4保留NPh/两个SiMe3/羰基。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Exact 1/V′/4 models including model4 N-phenyl and both SiMe3 groups; V′ remains an explicitly truncated experimental model; H2/Si atoms and states are tracked."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Mainpp3–5;SI1/4/Vprime/H2coordinates",
    "actual_result": {
      "neutral_reactant_atoms": {
        "1": 55,
        "Vprime": 36,
        "4": 48
      },
      "TS_product_atoms": {
        "1": 57,
        "Vprime": 38,
        "4": 50
      },
      "source_model4": "N-phenyl+twoSiMe3+carbonyl/lactamretained",
      "reference": "neutral singlet source silylene + neutral singlet H2"
    },
    "reason": "Threeexactgraphs/stoichiometryandcentralSiareverified;fullbulkyexperimentalsystemsnot substituted.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/stdout.log",
        "sha256": "3b29216c1e8bd0f9502daea80836eebc770a6d622f6187664fe1e729686c685d"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "fb01082a4ef71ff340e6f08b7b72694a211f04cdb71d2f2de1f2e536d30ce9ba"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "49079e2dbbebd3c4358a99295822fb9c2d428a0ded09f6dcbe072723f0035d0c"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "6a2312a3c0fa673222b4cfddab3c951d051cd8b6ba6c463d50791b45d52ade63"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "5faca63ba98b91f74baa374ea3eb33c0c4ec457da5345b0fb65423a9a0b71534"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/stdout.log",
        "sha256": "2cdc7b0026136305f676221edcb1385df94562cedca63ce8bed4d66dfe70e30b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_source_optfreq/gaussian.log",
        "sha256": "c133dc62d8dda6fbb8545f9cc5c639858a68d79b6ca38c15d230ecaf33d9563b"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq_freq_recovery1/gaussian.log",
        "sha256": "dd1a603388ab3100176f88ae6515eeb3a6469582c4a1e13281e654842780e3a2"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_product_optfreq/gaussian.log",
        "sha256": "27ca56d36d497768ff355de9fd20700ceec04a9ba5200ec1e035fd0cb078883a"
      }
    ]
  }
]
```

### kp_reactivity — Evidence establishes or limits reactivity differences

冻结要求：Generate auditable quantitative evidence relevant to H2 activation across the bounded source models. Old barrier copying or lone gap/charge values do not establish the explanation. Valid alternative methods and evidence-backed unresolved differences are acceptable. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：原生日志重算六个G差；每个TS有一个负模，产品/反应物末次频率正。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "All six source barrier/reaction ΔG quantities have independently generated native values with identical separated-reactant definitions; all three paths are actually investigated."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Mainp5Table2;SIH2TSs/S2",
    "actual_result": {
      "barriers_kcalmol": {
        "1": 33.06598422628099,
        "Vprime": 47.132236596879444,
        "4": 29.842468058018845
      },
      "reactionG_kcalmol": {
        "1": -29.098869331254072,
        "Vprime": -20.57478063558092,
        "4": -33.80832793409764
      },
      "pairwise_barrier_contrasts": [
        {
          "higher_barrier_model": "Vprime",
          "lower_barrier_model": "1",
          "source_difference_kcalmol": 14.5,
          "native_difference_kcalmol": 14.066252370598455
        },
        {
          "higher_barrier_model": "Vprime",
          "lower_barrier_model": "4",
          "source_difference_kcalmol": 18.4,
          "native_difference_kcalmol": 17.2897685388606
        },
        {
          "higher_barrier_model": "1",
          "lower_barrier_model": "4",
          "source_difference_kcalmol": 3.8999999999999986,
          "native_difference_kcalmol": 3.223516168262144
        }
      ],
      "frequencies": {
        "1": {
          "reactant": {
            "final_mode_count": 159,
            "negative_frequencies_cm1": [],
            "minimum_internal_frequency_cm1": 9.8946
          },
          "H2": {
            "final_mode_count": 1,
            "negative_frequencies_cm1": [],
            "minimum_internal_frequency_cm1": 4406.4137
          },
          "TS": {
            "final_mode_count": 165,
            "negative_frequencies_cm1": [
              -1243.4664
            ],
            "minimum_internal_frequency_cm1": -1243.4664
          },
          "product": {
            "final_mode_count": 165,
            "negative_frequencies_cm1": [],
            "minimum_internal_frequency_cm1": 31.7962
          }
        },
        "Vprime": {
          "reactant": {
            "final_mode_count": 102,
            "negative_frequencies_cm1": [],
            "minimum_internal_frequency_cm1": 21.0877
          },
          "H2": {
            "final_mode_count": 1,
            "negative_frequencies_cm1": [],
            "minimum_internal_frequency_cm1": 4406.4137
          },
          "TS": {
            "final_mode_count": 108,
            "negative_frequencies_cm1": [
              -1328.1352
            ],
            "minimum_internal_frequency_cm1": -1328.1352
          },
          "product": {
            "final_mode_count": 108,
            "negative_frequencies_cm1": [],
            "minimum_internal_frequency_cm1": 20.2353
          }
        },
        "4": {
          "reactant": {
            "final_mode_count": 138,
            "negative_frequencies_cm1": [],
            "minimum_internal_frequency_cm1": 20.6295
          },
          "H2": {
            "final_mode_count": 1,
            "negative_frequencies_cm1": [],
            "minimum_internal_frequency_cm1": 4406.4137
          },
          "TS": {
            "final_mode_count": 144,
            "negative_frequencies_cm1": [
              -1256.7848
            ],
            "minimum_internal_frequency_cm1": -1256.7848
          },
          "product": {
            "final_mode_count": 144,
            "negative_frequencies_cm1": [],
            "minimum_internal_frequency_cm1": 16.6306
          }
        }
      }
    },
    "reason": "NativeTSseachoneHHstretchimaginarymode;acceptedminimaandfiniteconnectedbasins. Separatedreferenceisnotreplacedbybindingcomplex. StrongVprimevs1/4differenceandmodel4vs1orderingwithinthisHamiltonianareactuallyresolved.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/stdout.log",
        "sha256": "3b29216c1e8bd0f9502daea80836eebc770a6d622f6187664fe1e729686c685d"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "fb01082a4ef71ff340e6f08b7b72694a211f04cdb71d2f2de1f2e536d30ce9ba"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "49079e2dbbebd3c4358a99295822fb9c2d428a0ded09f6dcbe072723f0035d0c"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "6a2312a3c0fa673222b4cfddab3c951d051cd8b6ba6c463d50791b45d52ade63"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "5faca63ba98b91f74baa374ea3eb33c0c4ec457da5345b0fb65423a9a0b71534"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/stdout.log",
        "sha256": "2cdc7b0026136305f676221edcb1385df94562cedca63ce8bed4d66dfe70e30b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_source_optfreq/gaussian.log",
        "sha256": "c133dc62d8dda6fbb8545f9cc5c639858a68d79b6ca38c15d230ecaf33d9563b"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq_freq_recovery1/gaussian.log",
        "sha256": "dd1a603388ab3100176f88ae6515eeb3a6469582c4a1e13281e654842780e3a2"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_product_optfreq/gaussian.log",
        "sha256": "27ca56d36d497768ff355de9fd20700ceec04a9ba5200ec1e035fd0cb078883a"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/gaussian.log",
        "sha256": "a36aa2c888fd4a936647553d07fd1b0eeef6feef9f13d1cdcac225db2580f4b6"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_strict_silylene_terminal_accept_20261002_a02/finite_path_terminal_synthesis.json",
        "sha256": "69ef7c34291cc2ae9975a5d3cd8367f36540fe0bdccfc36e747884de15e0a372"
      },
      {
        "path": "tasks/final_verified_paper_reproduction/paper_0e835b370ddd37b6/evaluation/verified_computation_reference.md",
        "sha256": "242a4aec88efca037b3c1873d5596c3953b36c186d4289938d98bd2195d90a84"
      }
    ]
  }
]
```

### kp_explanation — Explanatory account challenged by discriminating evidence

冻结要求：Judge whether the selected investigation differentiates the submitted physical explanation from correlation alone. No prescribed strain/interaction partition, donor-acceptor label or HH grid. Claiming a transition state or pathway requires appropriate saddle/connectivity evidence. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：实际路径、供受电子与重组对比可区分单纯供体能解释；4供体比1低这一反例未隐藏。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Si donor/acceptor energy/shape and H–H/Si–H bonding/TS evidence accompany the barriers. The model4-versus1 contrast rules out an exclusive donor-level explanation; no mandatory strain decomposition is assumed."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "MainFig1/Table1;SIp8TableS2",
    "actual_result": {
      "trusted_sigma_pi_candidates": [
        {
          "model": "1",
          "source_Esigma_eV": -5.59,
          "source_Epi_star_eV": -0.99,
          "native_sigma": {
            "MO_1based": 95,
            "occupied": true,
            "frontier_offset": 0,
            "energy_Eh": -0.205277545,
            "energy_eV": -5.585886564623182,
            "Si_total_Loewdin_weight": 0.632637439688117,
            "Si_s_weight": 0.1545638743845572,
            "Si_p_normal_weight": 7.117039672716352e-05,
            "Si_p_inplane_weight": 0.44257011372204463,
            "Si_s_plus_p_inplane_score": 0.5971339881066018
          },
          "native_pi_star": {
            "MO_1based": 96,
            "occupied": false,
            "frontier_offset": 0,
            "energy_Eh": -0.0365288319,
            "energy_eV": -0.9940001539456678,
            "Si_total_Loewdin_weight": 0.5573153788905,
            "Si_s_weight": 0.0001089730944003316,
            "Si_p_normal_weight": 0.5012488244147011,
            "Si_p_inplane_weight": 0.0007452254641698852,
            "Si_s_plus_p_inplane_score": 0.0008541985585701628
          },
          "MO_norm_max_error": 4.777023552872406e-07,
          "electron_trace": 190.00000000731131,
          "native_log": {
            "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/gaussian.log",
            "sha256": "059422d5ebef4429d897a6a8ba374a571933fc18395f37e96555dd2cfa451bfd"
          },
          "projection_report": {
            "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/1/frontier_projection.json",
            "sha256": "913204db30b81ecdb6bc147f2bd5485f15868df11a61e846f99d18db0fe0201d"
          }
        },
        {
          "model": "4",
          "source_Esigma_eV": -5.99,
          "source_Epi_star_eV": -1.75,
          "native_sigma": {
            "MO_1based": 90,
            "occupied": true,
            "frontier_offset": 0,
            "energy_Eh": -0.219768747,
            "energy_eV": -5.980212259413816,
            "Si_total_Loewdin_weight": 0.5704462084156812,
            "Si_s_weight": 0.1387270716601961,
            "Si_p_normal_weight": 0.0004212209092151089,
            "Si_p_inplane_weight": 0.40039517277057235,
            "Si_s_plus_p_inplane_score": 0.5391222444307684
          },
          "native_pi_star": {
            "MO_1based": 91,
            "occupied": false,
            "frontier_offset": 0,
            "energy_Eh": -0.0640356677,
            "energy_eV": -1.742499287304438,
            "Si_total_Loewdin_weight": 0.6011200400473419,
            "Si_s_weight": 0.000140260871584935,
            "Si_p_normal_weight": 0.5607539215946609,
            "Si_p_inplane_weight": 0.0009480053603364569,
            "Si_s_plus_p_inplane_score": 0.0010882662319213754
          },
          "MO_norm_max_error": 1.2693222982591845e-07,
          "electron_trace": 180.00000002564764,
          "native_log": {
            "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/gaussian.log",
            "sha256": "4621d7292e22de3f148ec550182a50c3e8a57e2449eefba8ff26f2d57c15165a"
          },
          "projection_report": {
            "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/4/frontier_projection.json",
            "sha256": "0f2cf5fb79e7c1e07aa6545b7cc905316beff5a152753a071ac7b7219567bbab"
          }
        },
        {
          "model": "Vprime",
          "source_Esigma_eV": -6.82,
          "source_Epi_star_eV": -1.32,
          "native_sigma": {
            "MO_1based": 72,
            "occupied": true,
            "frontier_offset": -1,
            "energy_Eh": -0.250559238,
            "energy_eV": -6.818064202718434,
            "Si_total_Loewdin_weight": 0.7420507770824256,
            "Si_s_weight": 0.2802506998799822,
            "Si_p_normal_weight": 0.0001297923630249908,
            "Si_p_inplane_weight": 0.42125002776270914,
            "Si_s_plus_p_inplane_score": 0.7015007276426913
          },
          "native_pi_star": {
            "MO_1based": 74,
            "occupied": false,
            "frontier_offset": 0,
            "energy_Eh": -0.0483529704,
            "energy_eV": -1.3157513536952248,
            "Si_total_Loewdin_weight": 0.5999104069880561,
            "Si_s_weight": 1.848213254364647e-05,
            "Si_p_normal_weight": 0.5512723967163513,
            "Si_p_inplane_weight": 9.904295968421462e-05,
            "Si_s_plus_p_inplane_score": 0.00011752509222784369
          },
          "MO_norm_max_error": 1.2402196458499107e-07,
          "electron_trace": 145.999999996944,
          "native_log": {
            "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/gaussian.log",
            "sha256": "3aea1cc0d1a74d199b47261394043401829ec730f3fbc3340baa9e5b50ea8892"
          },
          "projection_report": {
            "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/Vprime/frontier_projection.json",
            "sha256": "9783aa6ce681e07b6d6e62c741f43750b42973cc2ddd93b7d6a18457d09ce98c"
          }
        }
      ],
      "HH_WBI_at_TS": [
        {
          "model": "1",
          "native_HH_WBI": 0.2533,
          "source_HH_WBI": 0.253
        },
        {
          "model": "Vprime",
          "native_HH_WBI": 0.2067,
          "source_HH_WBI": 0.207
        },
        {
          "model": "4",
          "native_HH_WBI": 0.2465,
          "source_HH_WBI": 0.246
        }
      ],
      "source_and_native_donor_acceptor_energy_agreement": "about0.01eVwithoutselectingbyclosesttarget",
      "counterexample_to_donor_only": "4donor−5.9802eVbelow1−5.5859eVyetbarrierlower;4acceptor−1.7425below1−0.9940",
      "S_T_EZPE_gap_kcalmol": {
        "1": 41.00711662053022,
        "4": 38.00009122084986,
        "Vprime": 44.541877487920694
      }
    },
    "reason": "Coordinate/graph-declaredprojectionandreactionWBIchangesprovidediscriminatingevidence. Supportsjointdonor/acceptor+reorganizationaccount;neitherexactOccSi noruniquemechanismisnecessaryforthisqualifiedanswer.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/gaussian.log",
        "sha256": "059422d5ebef4429d897a6a8ba374a571933fc18395f37e96555dd2cfa451bfd"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/gaussian.log",
        "sha256": "4621d7292e22de3f148ec550182a50c3e8a57e2449eefba8ff26f2d57c15165a"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/gaussian.log",
        "sha256": "3aea1cc0d1a74d199b47261394043401829ec730f3fbc3340baa9e5b50ea8892"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/1/frontier_projection.json",
        "sha256": "913204db30b81ecdb6bc147f2bd5485f15868df11a61e846f99d18db0fe0201d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/4/frontier_projection.json",
        "sha256": "0f2cf5fb79e7c1e07aa6545b7cc905316beff5a152753a071ac7b7219567bbab"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/Vprime/frontier_projection.json",
        "sha256": "9783aa6ce681e07b6d6e62c741f43750b42973cc2ddd93b7d6a18457d09ce98c"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_TS_source_NBO_a01/gaussian.log",
        "sha256": "a629fa7c87168e5875fc057c6a22add3b502d60e3b1c557b32bdb386c2b51182"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_TS_source_NBO_a01/gaussian.log",
        "sha256": "ded6569b4130a6e71a087faf5f585b518041ec1f547549e57cd3e1f1e601010e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_TS_source_NBO_a01/gaussian.log",
        "sha256": "0e56ba8ac2c220f1a7c6ff8091b503fc30d3b1af88a1f85e143281274f920338"
      }
    ]
  }
]
```

### kp_uncertainty — State, model and reference reliability

冻结要求：Account for decisive conformer/state, solvation and thermal/standard-state effects in the actual comparison. If decomposition is used, fragments and references must reconstruct the stated quantity. Do not compare gasH2 and solute conventions without conversion or invent reliable ranking from small unbounded gaps. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：源/原生电子+ZPE和热项残差有逐项分解；不新造统一±1阈值。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Valid stationary points, stable singlets, source-method state-gap controls, explicit 298 K/1 atm/benzene reference and partitioned source/native residuals are retained. Source OccSi/NBO algorithm details and residual causes remain unresolved."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Mainmethods/Table2;SITableS1;newsource/nativeenergyaccounting",
    "actual_result": {
      "energy_partition": [
        {
          "model": "1",
          "quantity": "activation_barrier",
          "source_Table2_G_kcal_mol": 32.9,
          "native_G_kcal_mol": 33.06598422628099,
          "source_E_plus_ZPE_difference_kcal_mol": 25.016920202473607,
          "native_E_plus_ZPE_difference_kcal_mol": 25.1123016425312,
          "source_inferred_remaining_thermal_term_kcal_mol": 7.883079797526392,
          "native_remaining_thermal_term_kcal_mol": 7.953682583749792,
          "residual_G_kcal_mol": 0.1659842262809914,
          "residual_EZPE_kcal_mol": 0.0953814400575912,
          "residual_remaining_thermal_kcal_mol": 0.0706027862234002,
          "decomposition_closure_verified": true,
          "source_G_printing_half_step_kcal_mol": 0.05,
          "source_EZPE_difference_printing_bound_kcal_mol": 0.00094126421109465,
          "source_remaining_term_printing_bound_kcal_mol": 0.05094126421109465,
          "printing_bounds_are_not_scientific_tolerance": true,
          "source_remaining_term_not_independently_published_entropy": true
        },
        {
          "model": "1",
          "quantity": "reaction_G",
          "source_Table2_G_kcal_mol": -29.4,
          "native_G_kcal_mol": -29.098869331254072,
          "source_E_plus_ZPE_difference_kcal_mol": -37.12722554241738,
          "native_E_plus_ZPE_difference_kcal_mol": -37.00235115707882,
          "source_inferred_remaining_thermal_term_kcal_mol": 7.727225542417375,
          "native_remaining_thermal_term_kcal_mol": 7.903481825824745,
          "residual_G_kcal_mol": 0.3011306687459268,
          "residual_EZPE_kcal_mol": 0.1248743853385569,
          "residual_remaining_thermal_kcal_mol": 0.1762562834073699,
          "decomposition_closure_verified": true,
          "source_G_printing_half_step_kcal_mol": 0.05,
          "source_EZPE_difference_printing_bound_kcal_mol": 0.00094126421109465,
          "source_remaining_term_printing_bound_kcal_mol": 0.05094126421109465,
          "printing_bounds_are_not_scientific_tolerance": true,
          "source_remaining_term_not_independently_published_entropy": true
        },
        {
          "model": "Vprime",
          "quantity": "activation_barrier",
          "source_Table2_G_kcal_mol": 47.4,
          "native_G_kcal_mol": 47.132236596879444,
          "source_E_plus_ZPE_difference_kcal_mol": 39.96231334623446,
          "native_E_plus_ZPE_difference_kcal_mol": 39.819241186148076,
          "source_inferred_remaining_thermal_term_kcal_mol": 7.43768665376554,
          "native_remaining_thermal_term_kcal_mol": 7.312995410731367,
          "residual_G_kcal_mol": -0.267763403120559,
          "residual_EZPE_kcal_mol": -0.1430721600863868,
          "residual_remaining_thermal_kcal_mol": -0.1246912430341722,
          "decomposition_closure_verified": true,
          "source_G_printing_half_step_kcal_mol": 0.05,
          "source_EZPE_difference_printing_bound_kcal_mol": 0.00094126421109465,
          "source_remaining_term_printing_bound_kcal_mol": 0.05094126421109465,
          "printing_bounds_are_not_scientific_tolerance": true,
          "source_remaining_term_not_independently_published_entropy": true
        },
        {
          "model": "Vprime",
          "quantity": "reaction_G",
          "source_Table2_G_kcal_mol": -21.3,
          "native_G_kcal_mol": -20.57478063558092,
          "source_E_plus_ZPE_difference_kcal_mol": -27.16676766061379,
          "native_E_plus_ZPE_difference_kcal_mol": -27.635517237738924,
          "source_inferred_remaining_thermal_term_kcal_mol": 5.866767660613788,
          "native_remaining_thermal_term_kcal_mol": 7.060736602158001,
          "residual_G_kcal_mol": 0.7252193644190772,
          "residual_EZPE_kcal_mol": -0.4687495771251357,
          "residual_remaining_thermal_kcal_mol": 1.193968941544213,
          "decomposition_closure_verified": true,
          "source_G_printing_half_step_kcal_mol": 0.05,
          "source_EZPE_difference_printing_bound_kcal_mol": 0.00094126421109465,
          "source_remaining_term_printing_bound_kcal_mol": 0.05094126421109465,
          "printing_bounds_are_not_scientific_tolerance": true,
          "source_remaining_term_not_independently_published_entropy": true
        },
        {
          "model": "4",
          "quantity": "activation_barrier",
          "source_Table2_G_kcal_mol": 29.0,
          "native_G_kcal_mol": 29.842468058018845,
          "source_E_plus_ZPE_difference_kcal_mol": 21.93459366587566,
          "native_E_plus_ZPE_difference_kcal_mol": 22.577163367316274,
          "source_inferred_remaining_thermal_term_kcal_mol": 7.065406334124339,
          "native_remaining_thermal_term_kcal_mol": 7.265304690702572,
          "residual_G_kcal_mol": 0.8424680580188467,
          "residual_EZPE_kcal_mol": 0.6425697014406144,
          "residual_remaining_thermal_kcal_mol": 0.1998983565782323,
          "decomposition_closure_verified": true,
          "source_G_printing_half_step_kcal_mol": 0.05,
          "source_EZPE_difference_printing_bound_kcal_mol": 0.00094126421109465,
          "source_remaining_term_printing_bound_kcal_mol": 0.05094126421109465,
          "printing_bounds_are_not_scientific_tolerance": true,
          "source_remaining_term_not_independently_published_entropy": true
        },
        {
          "model": "4",
          "quantity": "reaction_G",
          "source_Table2_G_kcal_mol": -33.9,
          "native_G_kcal_mol": -33.80832793409764,
          "source_E_plus_ZPE_difference_kcal_mol": -41.77769825469901,
          "native_E_plus_ZPE_difference_kcal_mol": -41.499711557689054,
          "source_inferred_remaining_thermal_term_kcal_mol": 7.877698254699009,
          "native_remaining_thermal_term_kcal_mol": 7.691383623591417,
          "residual_G_kcal_mol": 0.0916720659023613,
          "residual_EZPE_kcal_mol": 0.2779866970099533,
          "residual_remaining_thermal_kcal_mol": -0.186314631107592,
          "decomposition_closure_verified": true,
          "source_G_printing_half_step_kcal_mol": 0.05,
          "source_EZPE_difference_printing_bound_kcal_mol": 0.00094126421109465,
          "source_remaining_term_printing_bound_kcal_mol": 0.05094126421109465,
          "printing_bounds_are_not_scientific_tolerance": true,
          "source_remaining_term_not_independently_published_entropy": true
        }
      ],
      "model4_residual_G_EZPE_other_kcalmol": [
        0.8424680580188467,
        0.6425697014406144,
        0.1998983565782323
      ],
      "wavefunction_checks": "SourcePBE0singletsStable;acceptedS/Tminimaandfouralternativepairsretainpositivegapand1>4gaporder",
      "model4_reverse_end": "144positivefinalmodes,min14.9463cm-1;HH0.74833085A",
      "warnings": "Ryd/Rydinversionsnotvalence-pcontamination;GSVDsignificance/OccSiexactaxisnotcertified"
    },
    "reason": "ComponentclosureexcludesmixingE+ZPEwithG/wrongH2reference. No+/-1kcalruleintroduced:expertacceptanceislimitedtoreproducedordinal/coremulti-kcalconclusion,notratesorlastdigits. FiniteIRCandlow-mode/modeluncertaintyretained.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene_source_energy_partition_20261008.json",
        "sha256": "50c97adc86da884c44b25bdc2b5793d32744de6ecfb7a46b4e166f9e94584cf5"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene4_paired_stability_acceptance_20260930.json",
        "sha256": "c78f15bf54b9f045081c3202005a3c9794c197dd8340f364c3a4f50f5d2761d9"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/author_silylene_restarted_final_pair_20261004.json",
        "sha256": "695d95467e36d31661c6d5fd26171536a22c07d22d5be025887b8d3dd3fdc20d"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/SILYLENE_WARNING_SCOPE_ACCEPTANCE_20261007.json",
        "sha256": "ea2d252de5a100065b841d9beaa1c10198c175bbe1fa670b0ba6c6f48bb43cbd"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/gaussian.log",
        "sha256": "a36aa2c888fd4a936647553d07fd1b0eeef6feef9f13d1cdcac225db2580f4b6"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_strict_silylene_terminal_accept_20261002_a02/finite_path_terminal_synthesis.json",
        "sha256": "69ef7c34291cc2ae9975a5d3cd8367f36540fe0bdccfc36e747884de15e0a372"
      },
      {
        "path": "tasks/final_verified_paper_reproduction/paper_0e835b370ddd37b6/evaluation/verified_computation_reference.md",
        "sha256": "242a4aec88efca037b3c1873d5596c3953b36c186d4289938d98bd2195d90a84"
      }
    ]
  }
]
```

### kp_conclusion — Model-level conclusions only

冻结要求：Accept supported differences, refuted source rationale or sufficiently established indistinguishability. Do not claim experimentalH2 rates, full-ligand behaviour or other substrate catalysis from these finite source models. Score only the part supported by valid artifacts: full credit for a sufficient valid argument within scope; partial credit for a correct but incomplete evidential chain; no credit for assertions, wrong objects/references or missing decisive evidence. Do not penalize absence of a particular author/V1 operation when an adequate alternative exists.

当前复审：相对活化次序与放能性、限定的双亲电子解释支持当前核心科学问题。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "Results concern these finite models and this channel. Large 1/4 versus V′ differences and strong exergonicity are reproduced; no experimental rate, precise rate ratio or full-ligand claim."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "Mainp5H2discussion;currentkp_conclusion",
    "actual_result": {
      "order": "4<1<<Vprime barrier",
      "all_exergonic": true,
      "not_claimed": [
        "experimentalkinetics",
        "fullDipp/adamantyl",
        "ammoniaborane/CO2/acetylene",
        "causalityfromchargealone"
      ]
    },
    "reason": "Samequalitativecorecomputationalsourcefindingwithactualenergydifferencesandboundedjointinterpretation;notusingmerepermissionfornegativeanswerasPASS.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/stdout.log",
        "sha256": "3b29216c1e8bd0f9502daea80836eebc770a6d622f6187664fe1e729686c685d"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "fb01082a4ef71ff340e6f08b7b72694a211f04cdb71d2f2de1f2e536d30ce9ba"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "49079e2dbbebd3c4358a99295822fb9c2d428a0ded09f6dcbe072723f0035d0c"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "6a2312a3c0fa673222b4cfddab3c951d051cd8b6ba6c463d50791b45d52ade63"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "5faca63ba98b91f74baa374ea3eb33c0c4ec457da5345b0fb65423a9a0b71534"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/stdout.log",
        "sha256": "2cdc7b0026136305f676221edcb1385df94562cedca63ce8bed4d66dfe70e30b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_source_optfreq/gaussian.log",
        "sha256": "c133dc62d8dda6fbb8545f9cc5c639858a68d79b6ca38c15d230ecaf33d9563b"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq_freq_recovery1/gaussian.log",
        "sha256": "dd1a603388ab3100176f88ae6515eeb3a6469582c4a1e13281e654842780e3a2"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_product_optfreq/gaussian.log",
        "sha256": "27ca56d36d497768ff355de9fd20700ceec04a9ba5200ec1e035fd0cb078883a"
      }
    ]
  }
]
```

### conclusion_investigation — Do the source silylene models1,V′ and4 differ meaningfully in their ability to activate H2, and what molecular explanation is supported by reproducible evidence within these model definitions?

冻结要求：Answer the bounded question with claims proportional to the evidence. Support, correction, refutation and demonstrated unresolved conclusions are equally eligible. Partial/failure status preserves real work but does not confer completion credit. No required author winner or named control list.

当前复审：相对活化次序与放能性、限定的双亲电子解释支持当前核心科学问题。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

证据记录：`strict_reaudit`。

```json
[
  {
    "evidence_assessment": "A bounded comparative molecular account is complete and agrees with the source at a scientifically material accuracy for the question."
  }
]
```


证据记录：`E0001`。

```json
[
  {
    "source_locator": "CurrentV2AR/PRquestion",
    "actual_result": {
      "answer": "Source1/Vprimeandadded4differmeaningfullyinthespecifiedH2model;boundedambiphilic/reorganizationaccountsupported",
      "source_comparative_result": "reproduced"
    },
    "reason": "Allcurrentnodescoveredbyexistingnativeevidenceandnewlyacceptedenergyaccounting. NoextraV1strain/HHmatrixneeded.",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/stdout.log",
        "sha256": "3b29216c1e8bd0f9502daea80836eebc770a6d622f6187664fe1e729686c685d"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "fb01082a4ef71ff340e6f08b7b72694a211f04cdb71d2f2de1f2e536d30ce9ba"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "49079e2dbbebd3c4358a99295822fb9c2d428a0ded09f6dcbe072723f0035d0c"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "6a2312a3c0fa673222b4cfddab3c951d051cd8b6ba6c463d50791b45d52ade63"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log",
        "sha256": "5faca63ba98b91f74baa374ea3eb33c0c4ec457da5345b0fb65423a9a0b71534"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/stdout.log",
        "sha256": "2cdc7b0026136305f676221edcb1385df94562cedca63ce8bed4d66dfe70e30b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_source_optfreq/gaussian.log",
        "sha256": "c133dc62d8dda6fbb8545f9cc5c639858a68d79b6ca38c15d230ecaf33d9563b"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log",
        "sha256": "ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq_freq_recovery1/gaussian.log",
        "sha256": "dd1a603388ab3100176f88ae6515eeb3a6469582c4a1e13281e654842780e3a2"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_product_optfreq/gaussian.log",
        "sha256": "27ca56d36d497768ff355de9fd20700ceec04a9ba5200ec1e035fd0cb078883a"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/author_silylene_trusted_stable_frontiers_20261002.json",
        "sha256": "25cb97efe46970249ac5f8dcbe5f34f245e9b7a19520d3d650556aea03caf4c5"
      }
    ]
  }
]
```

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 73.17 小时；失败/状态未确认阶段 22.30 小时；31 份计时日志/43 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 20 线程/进程；Gaussian %Mem=12GB,24GB,80GB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0006 · hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/stdout.log) | Gaussian:55666.7；Gaussian:5764.4 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0007 · outputs/silylene4_source_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_source_optfreq/gaussian.log) | Gaussian:5545.1；Gaussian:4846 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0008 · local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log) | Gaussian:5150.1；Gaussian:4193.4 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0009 · local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log) | Gaussian:3.2；Gaussian:3.3 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0010 · local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log) | Gaussian:15077；Gaussian:12887.4 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0011 · outputs/silylene4_H2_TS_source_optfreq_freq_recovery1/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq_freq_recovery1/gaussian.log) | Gaussian:6007.6 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0012 · local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log) | Gaussian:4842.5；Gaussian:4365 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0013 · local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log) | Gaussian:14329.7；Gaussian:14986.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0014 · outputs/silylene4_H2_product_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_product_optfreq/gaussian.log) | Gaussian:6927.9；Gaussian:5374.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0015 · hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/stdout.log) | Gaussian:7203.7；Gaussian:2165.1 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0028 · outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/gaussian.log) | Gaussian:15504.3；Gaussian:5580.7 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0030 · outputs/v2_silylene1_singlet_stable_check_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/gaussian.log) | Gaussian:1421.2 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0032 · outputs/v2_silylene4_singlet_stable_check_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/gaussian.log) | Gaussian:1158.3 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0034 · outputs/v2_silyleneVprime_singlet_stable_check_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/gaussian.log) | Gaussian:587.3 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0036 · outputs/v2_silylene1_TS_source_NBO_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_TS_source_NBO_a01/gaussian.log) | Gaussian:454 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0037 · outputs/v2_silyleneVprime_TS_source_NBO_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_TS_source_NBO_a01/gaussian.log) | Gaussian:201.2 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0038 · outputs/v2_silylene4_TS_source_NBO_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_TS_source_NBO_a01/gaussian.log) | Gaussian:338.9 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0053 · outputs/silylene4_H2_TS_source_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq/gaussian.log) | Gaussian:6493 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0054 · outputs/silylene4_H2_IRC_forward/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_IRC_forward/gaussian.log) | Gaussian:21083.7 | 其他/未确认 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0055 · outputs/silylene4_H2_IRC_reverse/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_IRC_reverse/gaussian.log) | Gaussian:32650.3 | 其他/未确认 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0059 · outputs/v2_silylene4_IRC_forward_p43_optfreq_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_IRC_forward_p43_optfreq_a01/gaussian.log) | Gaussian:8867.4；Gaussian:4626.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0070 · outputs/v2_silylene4_reverse_recalcfc_optfreq_a03/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_reverse_recalcfc_optfreq_a03/gaussian.log) | Gaussian:26538.5 | 其他/未确认 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0071 · outputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/gaussian.log) | Gaussian:4598.5 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0072 · outputs/v2_author_silylene1_wB97XD_triplet_optfreq_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_optfreq_20261002_a01/gaussian.log) | Gaussian:19091.5 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0073 · outputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/gaussian.log) | Gaussian:585.5 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0074 · outputs/v2_author_silylene1_wB97XD_singlet_Stable_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_20261002_a01/gaussian.log) | 未知 | 无独立计时 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0075 · outputs/v2_reopen_silylene1_exactSI_NBO_20261004_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silylene1_exactSI_NBO_20261004_a01/gaussian.log) | Gaussian:482.2 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0076 · outputs/v2_reopen_silylene4_exactSI_NBO_20261004_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silylene4_exactSI_NBO_20261004_a01/gaussian.log) | Gaussian:514.1 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0077 · outputs/v2_reopen_silyleneVprime_exactSI_NBO_20261004_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silyleneVprime_exactSI_NBO_20261004_a01/gaussian.log) | Gaussian:214.6 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0078 · outputs/v2_silylene1_exactSI_G09Defaults_NBO_20261005_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_exactSI_G09Defaults_NBO_20261005_a01/gaussian.log) | Gaussian:200.8 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0101 · outputs/v2_silylene4_triplet_stable_check_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_triplet_stable_check_a01/gaussian.log) | Gaussian:1490.5 | 正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0103 · outputs/v2_silylene4_source_triplet_optfreq_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_source_triplet_optfreq_a01/gaussian.log) | Gaussian:8231.5；Gaussian:7423.3 | 正常；正常 | {"threads":[20],"Gaussian_mem":["12GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |

## 6. 已知偏差、失败分支和不能外推的结论

最高势垒残差0.8425kcal/mol和V′反应残差0.7252必须保留，非精确速率验证。；精确OccSi/GSVD独特定义及完整Dipp/其他底物反应不在本次认证。

```json
[
  "The 0.842468 kcal/mol model4 barrier and 0.725219 kcal/mol V′ reaction residuals exceed source printing error and are not hidden.",
  "Residual decomposition does not prove a grid/geometry/frequency cause.",
  "The 1−4 barrier advantage is reproduced only approximately; exact kinetic consequences are not certified.",
  "Historical model4 parent-checkpoint hash drift and OccSi/NBO warnings do not certify a complete original IRC; independently validated terminal evidence supports the bounded connectivity claim.",
  "Other substrates, full bulky ligands, exact experimental rates and arbitrary fixed decomposition controls are outside scope."
]
```


原独立审查的 `source_exceptions_not_certified`（如与后续状态冲突，以第 1 节最终裁决为准）：

```json
[
  "Absolute reaction/barrier residuals, especially model4 activation andVprime reaction thermal component, remain explicitly recorded.",
  "Exact OccSi/authorGSVD definition and a unique orbital cause are not certified.",
  "No experimental rates, bulky full-ligand catalytic outcomes, NH3BH3/CO2/acetylene claims or retired strain/HH matrix are required or certified."
]
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/paper_reproduction/paper_0e835b370ddd37b6.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_0e835b370ddd37b6/verified_computation_reference.md)；SHA-256 `5fc4d3d95f9081cdd055bc4d7a2d4fbd1aebed261186c3540a68e33c162432c8`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_0e835b370ddd37b6.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_0e835b370ddd37b6.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0001_paper_0e835b370ddd37b6.json) | `470648f7d82c09fea452a9113103ecdda26595fc226f1a346c8f95ac22f1494f` | evidence_or_analysis |
| E0002 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene_source_energy_partition_20261008.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene_source_energy_partition_20261008.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0002_silylene_source_energy_partition_20261008.json) | `50c97adc86da884c44b25bdc2b5793d32744de6ecfb7a46b4e166f9e94584cf5` | evidence_or_analysis |
| E0003 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/provenance/source_text/main.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/provenance/source_text/main.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0003_main.txt) | `3c4c214a54373112c731e98900055d460f1b3aabdcbed63816adf39de7b5fa23` | evidence_or_analysis |
| E0004 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/provenance/source_text/supplementary_001.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/provenance/source_text/supplementary_001.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0004_supplementary_001.txt) | `6f64b95fc4c46cc8ec167b1c7e214066c6e9f5bcca90753839a4619633758067` | evidence_or_analysis |
| E0005 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_strict_silylene_terminal_accept_20261002_a02/finite_path_terminal_synthesis.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_strict_silylene_terminal_accept_20261002_a02/finite_path_terminal_synthesis.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0005_finite_path_terminal_synthesis.json) | `69ef7c34291cc2ae9975a5d3cd8367f36540fe0bdccfc36e747884de15e0a372` | evidence_or_analysis |
| E0006 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0006_native_excerpt.json) | `3b29216c1e8bd0f9502daea80836eebc770a6d622f6187664fe1e729686c685d` | native_output |
| E0007 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_source_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_source_optfreq/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0007_native_excerpt.json) | `c133dc62d8dda6fbb8545f9cc5c639858a68d79b6ca38c15d230ecaf33d9563b` | native_output |
| E0008 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0008_native_excerpt.json) | `6a2312a3c0fa673222b4cfddab3c951d051cd8b6ba6c463d50791b45d52ade63` | native_output |
| E0009 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0009_native_excerpt.json) | `ac2ea2cee81d1933c44c0e6773417c2677851ce80c76b5e6a935df09e8bf7318` | native_output |
| E0010 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0010_native_excerpt.json) | `fb01082a4ef71ff340e6f08b7b72694a211f04cdb71d2f2de1f2e536d30ce9ba` | native_output |
| E0011 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq_freq_recovery1/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq_freq_recovery1/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0011_native_excerpt.json) | `dd1a603388ab3100176f88ae6515eeb3a6469582c4a1e13281e654842780e3a2` | native_output |
| E0012 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0012_native_excerpt.json) | `5faca63ba98b91f74baa374ea3eb33c0c4ec457da5345b0fb65423a9a0b71534` | native_output |
| E0013 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0013_native_excerpt.json) | `49079e2dbbebd3c4358a99295822fb9c2d428a0ded09f6dcbe072723f0035d0c` | native_output |
| E0014 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_product_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_product_optfreq/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0014_native_excerpt.json) | `27ca56d36d497768ff355de9fd20700ceec04a9ba5200ec1e035fd0cb078883a` | native_output |
| E0015 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0015_native_excerpt.json) | `2cdc7b0026136305f676221edcb1385df94562cedca63ce8bed4d66dfe70e30b` | native_output |
| E0016 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0016_task.md) | `ef1854a881acf5038ebf58357278bd883e8052e466bb4b2b53c3622ffe2d1220` | historical_task_binding |
| E0017 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0017_reference_key_points.json) | `1a55e7aecec01f4fb5723d7c0ad490f6e0d98f39de77dba85831d21101d8c8b9` | historical_task_binding |
| E0018 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0018_reference_conclusions.json) | `99ce6763bf15cc2b5c3842744cd97fbf6955029bd2ccc544e19f4a84e6b3c981` | historical_task_binding |
| E0019 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0019_task.md) | `aea8e23c994df9425e839270cfb7c854f90f4a440c21970d56691bc0c302f019` | historical_task_binding |
| E0020 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0020_reference_key_points.json) | `1a55e7aecec01f4fb5723d7c0ad490f6e0d98f39de77dba85831d21101d8c8b9` | historical_task_binding |
| E0021 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0021_reference_conclusions.json) | `99ce6763bf15cc2b5c3842744cd97fbf6955029bd2ccc544e19f4a84e6b3c981` | historical_task_binding |
| E0022 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0e835b370ddd37b6/NATIVE_EVIDENCE_INDEX.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0e835b370ddd37b6/NATIVE_EVIDENCE_INDEX.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0022_NATIVE_EVIDENCE_INDEX.json) | `1c4cd200f7f6c95f9f578ae5a20c1e2cf4b7af013a70afbdf0e2d16fbfd89c2d` | evidence_or_analysis |
| E0023 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0e835b370ddd37b6/SOURCE_PAGES_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0e835b370ddd37b6/SOURCE_PAGES_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0023_SOURCE_PAGES_READBACK.json) | `c77897706ab27176603a9742cb13842b3a986d6e3ea85ca3999deb6160c3af39` | evidence_or_analysis |
| E0024 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0e835b370ddd37b6/COMPUTATION_INVENTORY.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_0e835b370ddd37b6/COMPUTATION_INVENTORY.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0024_COMPUTATION_INVENTORY.json) | `75b92497dda1f95078c94f31b89757d62d42543d5c023b663fe7239f8506e9e2` | evidence_or_analysis |
| E0025 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_0e835b370ddd37b6.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_0e835b370ddd37b6.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0025_paper_0e835b370ddd37b6.md) | `fec13e960aa64c0a39f13ec1aab0051d8b423bc111e59823cd26ceb586e6f2cd` | evidence_or_analysis |
| E0026 | [docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `242a4aec88efca037b3c1873d5596c3953b36c186d4289938d98bd2195d90a84` | historical_task_binding |
| E0027 | [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot](/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/legacy_v1_snapshot/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot.snapshot) | `242a4aec88efca037b3c1873d5596c3953b36c186d4289938d98bd2195d90a84` | historical_task_binding |
| E0028 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0028_native_excerpt.json) | `a36aa2c888fd4a936647553d07fd1b0eeef6feef9f13d1cdcac225db2580f4b6` | native_output |
| E0029 | [tasks/final_verified_paper_reproduction/paper_0e835b370ddd37b6/evaluation/verified_computation_reference.md](../../../final_verified_paper_reproduction/paper_0e835b370ddd37b6/evaluation/verified_computation_reference.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0029_verified_computation_reference.md) | `242a4aec88efca037b3c1873d5596c3953b36c186d4289938d98bd2195d90a84` | historical_task_binding |
| E0030 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0030_native_excerpt.json) | `059422d5ebef4429d897a6a8ba374a571933fc18395f37e96555dd2cfa451bfd` | native_output |
| E0031 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/1/frontier_projection.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/1/frontier_projection.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0031_frontier_projection.json) | `913204db30b81ecdb6bc147f2bd5485f15868df11a61e846f99d18db0fe0201d` | evidence_or_analysis |
| E0032 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0032_native_excerpt.json) | `4621d7292e22de3f148ec550182a50c3e8a57e2449eefba8ff26f2d57c15165a` | native_output |
| E0033 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/4/frontier_projection.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/4/frontier_projection.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0033_frontier_projection.json) | `0f2cf5fb79e7c1e07aa6545b7cc905316beff5a152753a071ac7b7219567bbab` | evidence_or_analysis |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0034_native_excerpt.json) | `3aea1cc0d1a74d199b47261394043401829ec730f3fbc3340baa9e5b50ea8892` | native_output |
| E0035 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/Vprime/frontier_projection.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/Vprime/frontier_projection.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0035_frontier_projection.json) | `9783aa6ce681e07b6d6e62c741f43750b42973cc2ddd93b7d6a18457d09ce98c` | evidence_or_analysis |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_TS_source_NBO_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_TS_source_NBO_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0036_native_excerpt.json) | `a629fa7c87168e5875fc057c6a22add3b502d60e3b1c557b32bdb386c2b51182` | native_output |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_TS_source_NBO_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_TS_source_NBO_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0037_native_excerpt.json) | `ded6569b4130a6e71a087faf5f585b518041ec1f547549e57cd3e1f1e601010e` | native_output |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_TS_source_NBO_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_TS_source_NBO_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0038_native_excerpt.json) | `0e56ba8ac2c220f1a7c6ff8091b503fc30d3b1af88a1f85e143281274f920338` | native_output |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene4_paired_stability_acceptance_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene4_paired_stability_acceptance_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0039_silylene4_paired_stability_acceptance_20260930.json) | `c78f15bf54b9f045081c3202005a3c9794c197dd8340f364c3a4f50f5d2761d9` | evidence_or_analysis |
| E0040 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/author_silylene_restarted_final_pair_20261004.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/author_silylene_restarted_final_pair_20261004.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0040_author_silylene_restarted_final_pair_20261004.json) | `695d95467e36d31661c6d5fd26171536a22c07d22d5be025887b8d3dd3fdc20d` | evidence_or_analysis |
| E0041 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/SILYLENE_WARNING_SCOPE_ACCEPTANCE_20261007.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/SILYLENE_WARNING_SCOPE_ACCEPTANCE_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0041_SILYLENE_WARNING_SCOPE_ACCEPTANCE_20261007.json) | `ea2d252de5a100065b841d9beaa1c10198c175bbe1fa670b0ba6c6f48bb43cbd` | evidence_or_analysis |
| E0042 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/author_silylene_trusted_stable_frontiers_20261002.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/author_silylene_trusted_stable_frontiers_20261002.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0042_author_silylene_trusted_stable_frontiers_20261002.json) | `25cb97efe46970249ac5f8dcbe5f34f245e9b7a19520d3d650556aea03caf4c5` | evidence_or_analysis |
| E0043 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0043_scoring_rules.json) | `d7df36622dfbc910acbb81d8fbfdc2f03e464215be5de593726b989734a9eae3` | historical_task_binding |
| E0044 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0044_scoring_rules.json) | `d7df36622dfbc910acbb81d8fbfdc2f03e464215be5de593726b989734a9eae3` | historical_task_binding |
| E0045 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/G1.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/deliveries/G1.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0045_G1.json) | `ccad79bf939c39a02d6d81ef6b33306a032329039eb7887cda053cf14d145f6b` | evidence_or_analysis |
| E0046 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_0e835b370ddd37b6_delivery_integrity.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/paper_0e835b370ddd37b6_delivery_integrity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0046_paper_0e835b370ddd37b6_delivery_integrity.json) | `754e30d00077a3458c6bba96e5503abc08335e8cf0982eca04d98b2b29408196` | evidence_or_analysis |
| E0047 | [docs/v2_verification/history/strict_author_route_validation_20261001/legacy_vs_v2_diagnosis_20261008/LEGACY_NUMERIC_CHECKS.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/legacy_vs_v2_diagnosis_20261008/LEGACY_NUMERIC_CHECKS.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0047_LEGACY_NUMERIC_CHECKS.json) | `412d3adaac47108c151d163d9e317702805e828567b40ddf8dfc0b30d5ea5378` | evidence_or_analysis |
| E0048 | [docs/v2_verification/history/strict_author_route_validation_20261001/legacy_vs_v2_diagnosis_20261008/SOURCE_PAGE_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/legacy_vs_v2_diagnosis_20261008/SOURCE_PAGE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0048_SOURCE_PAGE_READBACK.json) | `bd4590ede5bef400cd4a197a607c5d6ff21bd6fa704e3fc99d61188aea8f51d3` | evidence_or_analysis |
| E0049 | [docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/silylene_model4_native_readback.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/finish56_20261008T0810Z/coordinator_review/silylene_model4_native_readback.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0049_silylene_model4_native_readback.json) | `34e2bae5fd9b1ba4489b21e26d990b749d64ed3f53414e89551f7d3a53d3a470` | evidence_or_analysis |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene_cartesian_failure_path_audit_v2_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene_cartesian_failure_path_audit_v2_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0050_silylene_cartesian_failure_path_audit_v2_20260930.json) | `8780b586a2c1506015e4fa26f4edc7d0995edd11983a5fa79fd4a324f53ed9de` | evidence_or_analysis |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0051_execution.json) | `e04f379535d00aa905496fcb3e8cd98bf2574c19bbd43c4d8c4b98add9e823d9` | evidence_or_analysis |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_superfine_recalcfc_optfreq_a04/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_superfine_recalcfc_optfreq_a04/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0052_input.com) | `2566af1ee47128773d1d15bc683bc9dd29786d13f5bd109f4cbaf2ef7963e504` | input_or_analysis_code |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0053_native_excerpt.json) | `2da8d14145554df310a5e88ead6a80878315075a343f61b68037e1187578a4e4` | native_output |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_IRC_forward/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_IRC_forward/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0054_native_excerpt.json) | `0a597dfcd4a4bb8d22f8ace5748f6201a45d4650637a5ec6343371bc01b646dc` | native_output |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_IRC_reverse/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_IRC_reverse/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0055_native_excerpt.json) | `dcf6563f113a487ad83c52557710f4eaca193a4e1ada6a156c699ed8c5ddfb78` | native_output |
| E0056 | [.software_cache/installations/gaussian/g16/install/g16/g16](../../../../.software_cache/installations/gaussian/g16/install/g16/g16) | `384f3baca38297d3f11ed2168bb9be836778fa4c5f5d07cb38751e3ed1a66db5` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_IRC_forward_p43_optfreq_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_IRC_forward_p43_optfreq_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0057_input.com) | `3fde1c739a516227174dfa5f01b3fbe16ea3d61909708e36573a6e097abc835e` | input_or_analysis_code |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_IRC_forward_p43_optfreq_a01/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_IRC_forward_p43_optfreq_a01/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0058_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_IRC_forward_p43_optfreq_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_IRC_forward_p43_optfreq_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0059_native_excerpt.json) | `a257196a00faa7167a2030aab263828fb2c730ee409a359d62409a8a765a2f7c` | native_output |
| E0060 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/silylene_1_source_recalcfc_optfreq_exacthessian_20260922_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0060_input.com) | `2f3023adcf2877f5ba2c05dcfdbeabadf0f8d73c89023104795b2faa53007cb3` | input_or_analysis_code |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_source_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_source_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0061_input.com) | `240bca2d8be3b07b7c8ef5f989b2546f7e4390c2afe6eb4f91fe3a8fb72df014` | input_or_analysis_code |
| E0062 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/nacnacsi_vprime_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0062_input.com) | `639a157a49430b708d8ea3e2bfbdcbdb96d469921cdfe89a3a44824afe9a1714` | input_or_analysis_code |
| E0063 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/h2_full_si_pbe1pbe_optfreq_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0063_input.com) | `6952a2ca7d466f68ca6a905f8b5020fe4c5528d342651f546cf1c65c064ebe8a` | input_or_analysis_code |
| E0064 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0064_input.com) | `204c23fd49190171c10b3a8428f6973cf79b1d8ad310ac28849144f435a9a064` | input_or_analysis_code |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq_freq_recovery1/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq_freq_recovery1/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0065_input.com) | `9514fafcce876941acad1ce28436811806c40205c311c67b4d5d85c1dba7c87a` | input_or_analysis_code |
| E0066 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/vprime_h2_ts_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0066_input.com) | `7a70e9e574b9c09c31716899ab42682d0c299eaa3a61c2758002edf30fed9319` | input_or_analysis_code |
| E0067 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/provenance/local_stage_tests_20260914/silylene_1_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0067_input.com) | `0b3fc69f11e640d33ece5b5150a86b4e278cd85dc8f1db60f80e531e73a0ea58` | input_or_analysis_code |
| E0068 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_product_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_product_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0068_input.com) | `8c57727be8c4b9af1939aa5342c4ed3c0eba270f4e62016270069f72b2a9a57a` | input_or_analysis_code |
| E0069 | [docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_0e835b370ddd37b6/hpc_runs/vprime_h2_product_full_si_pbe1pbe_optfreq_internal_repair_20260918_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0069_input.com) | `9774f651a716e5b89899e15fff4eff776a907f26523a67f82dc02ddb708997d4` | input_or_analysis_code |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_reverse_recalcfc_optfreq_a03/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_reverse_recalcfc_optfreq_a03/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0070_native_excerpt.json) | `3267ad9313ef04fbdfdd676fa83894e38f1307ce9b442bdbf6488428a38144d3` | native_output |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0071_native_excerpt.json) | `283b9913c437d8fae325594ea0c067764989aa7d36a5f2ac3bff62a0a124254b` | native_output |
| E0072 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_optfreq_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_optfreq_20261002_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0072_native_excerpt.json) | `25bbb19d6d82ff2719cdb2ee2dace4d1befc6746d8e72c977078d23d5dfc2c1e` | native_output |
| E0073 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0073_native_excerpt.json) | `9b42da961282477ceebc4f25f8f77365a372ada25c5160230766cd4bb5e826ef` | native_output |
| E0074 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_20261002_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_20261002_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0074_native_excerpt.json) | `c63aaa203cde0c0fdb67c01de5b5085b1f330ca837da960ad1f28ef79ad3e3f0` | native_output |
| E0075 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silylene1_exactSI_NBO_20261004_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silylene1_exactSI_NBO_20261004_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0075_native_excerpt.json) | `54564b33270e3059b62181ab0e60bc434806a3026250996eb381061ad5bca609` | native_output |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silylene4_exactSI_NBO_20261004_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silylene4_exactSI_NBO_20261004_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0076_native_excerpt.json) | `2fac573d02fa496dbb1b69cfdb57bee3b6771d223e868d2239bc922abb7bda7e` | native_output |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silyleneVprime_exactSI_NBO_20261004_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silyleneVprime_exactSI_NBO_20261004_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0077_native_excerpt.json) | `cd52fca830f09dc5eaf3384ff3c123f675baec9b9471ac04b9174e720527166b` | native_output |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_exactSI_G09Defaults_NBO_20261005_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_exactSI_G09Defaults_NBO_20261005_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0078_native_excerpt.json) | `3f0a1420f7313439a994c283aba32393d1e8d7400fa55ae5018e48fd78dde35a` | native_output |
| E0079 | [papers/paper_0e835b370ddd37b6/documents/main.pdf](../../../../papers/paper_0e835b370ddd37b6/documents/main.pdf) | `4481b439479e8874cffa309e47cec459ec33ca4d18be30b921e08b43a3233971` | source_document |
| E0080 | [papers/paper_0e835b370ddd37b6/documents/supplementary_001.pdf](../../../../papers/paper_0e835b370ddd37b6/documents/supplementary_001.pdf) | `df2f9a3f458bd80190146adb77300f8cc65385fc12d2a5bba829e8d60a0e189c` | source_document |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/v2_strict_silylene_terminal_accept_20261002_a02_acceptance.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/v2_strict_silylene_terminal_accept_20261002_a02_acceptance.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0081_v2_strict_silylene_terminal_accept_20261002_a02_acceptance.json) | `0fbb79723357f87f52563a83b0dbff56b4f57628d168ac05b23716060611c268` | evidence_or_analysis |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0082_input.com) | `2566af1ee47128773d1d15bc683bc9dd29786d13f5bd109f4cbaf2ef7963e504` | input_or_analysis_code |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0083_input.com) | `121ea4e9dc17d9ade20ba3f1e46e369f8e663b32e24b42cc08234caf69da5fd4` | input_or_analysis_code |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0084_execution.json) | `c0c791ea2842cfa4de6d3082be0be2e1c4c614ce9bb13a9c66f49fcfac8f27b1` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene1_singlet_stable_check_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene1_singlet_stable_check_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0085_input.com) | `121ea4e9dc17d9ade20ba3f1e46e369f8e663b32e24b42cc08234caf69da5fd4` | input_or_analysis_code |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/checkpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_singlet_stable_check_a01/checkpoint.chk) | `bfbaba259ed1d6aab12520b4f9b27ecff1445a8b79b6d330c0a2be921e55bb12` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/1/wavefunction.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/1/wavefunction.fchk) | `1d448ce2a9198f3ecbbd2eac6f874609912ed2cc9d7752044a2817a1c4449e05` | evidence_or_analysis |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0088_input.com) | `121ea4e9dc17d9ade20ba3f1e46e369f8e663b32e24b42cc08234caf69da5fd4` | input_or_analysis_code |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0089_execution.json) | `df84983bba63a89fa406ba4b12f5f73c5d7f01557c32bc03b2cd6aba53b13125` | evidence_or_analysis |
| E0090 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_singlet_stable_check_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_singlet_stable_check_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0090_input.com) | `121ea4e9dc17d9ade20ba3f1e46e369f8e663b32e24b42cc08234caf69da5fd4` | input_or_analysis_code |
| E0091 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/checkpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_singlet_stable_check_a01/checkpoint.chk) | `6f76a34d23b7251f08215c0a993208acdf99806b3f193af3836936c191b8759d` | evidence_or_analysis |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/4/wavefunction.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/4/wavefunction.fchk) | `0d2e657535ef2a37884d93ee72950b746cac38672c5daddc1e018abf1d14e533` | evidence_or_analysis |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0093_input.com) | `121ea4e9dc17d9ade20ba3f1e46e369f8e663b32e24b42cc08234caf69da5fd4` | input_or_analysis_code |
| E0094 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0094_execution.json) | `0f54c1b7b29d5bd2486c6363c7a66848a334fcf0e1aa88c178e1c6ab32db3db8` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silyleneVprime_singlet_stable_check_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silyleneVprime_singlet_stable_check_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0095_input.com) | `121ea4e9dc17d9ade20ba3f1e46e369f8e663b32e24b42cc08234caf69da5fd4` | input_or_analysis_code |
| E0096 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/checkpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_singlet_stable_check_a01/checkpoint.chk) | `e2d38d30d7157be9529e32d2fbbc98a1a5cb1b59575272293b4a7604f6775047` | evidence_or_analysis |
| E0097 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/Vprime/wavefunction.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_frontier_trusted_stable_reuse_20261002_a01/Vprime/wavefunction.fchk) | `d42e654c621799f07221f51d1276d6052ef29a01c3ed5cbbe1656ce13248c47e` | evidence_or_analysis |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_TS_source_NBO_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_TS_source_NBO_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0098_input.com) | `779bfe4e55bcc184f464ee0f12b7c4f31f8ee0c9dbf5186d6223fe5457256727` | input_or_analysis_code |
| E0099 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_TS_source_NBO_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silyleneVprime_TS_source_NBO_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0099_input.com) | `b5343ff26c23d427f21c080934fa7a02434cb02f0e4d2a03352ff43e1099b79c` | input_or_analysis_code |
| E0100 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_TS_source_NBO_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_TS_source_NBO_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0100_input.com) | `5c01894a4b50d9b8e4c2f04dba9af61d205f19b6f7c1b6021b4ea024b590d833` | input_or_analysis_code |
| E0101 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_triplet_stable_check_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_triplet_stable_check_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0101_native_excerpt.json) | `80fdb04a6354ae476e2ce018d2d1ea2a5ecb3bd523581c676212083e8dd8a53f` | native_output |
| E0102 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_source_triplet_optfreq_a01/checkpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_source_triplet_optfreq_a01/checkpoint.chk) | `bfb914219a7ff8b12ebfcb1bba15bab7e3dc3857a3cf7ef3246fccd95af6d730` | evidence_or_analysis |
| E0103 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_source_triplet_optfreq_a01/gaussian.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_source_triplet_optfreq_a01/gaussian.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0103_native_excerpt.json) | `95464758e91dfa51f06c1b690ae0a62ab50baa82d0203c144f05206b6bc2bff8` | native_output |
| E0104 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene4_triplet_acceptance_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene4_triplet_acceptance_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0104_silylene4_triplet_acceptance_20260930.json) | `926b439455350b6d4479fd96f5ec3fa9ee563123931ca55959694304cf93550a` | evidence_or_analysis |
| E0105 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_triplet_stable_check_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_triplet_stable_check_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0105_input.com) | `620af11aa56486f37219be09cc4854413793a3e599496138b9040136f1dc3f01` | input_or_analysis_code |
| E0106 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_triplet_stable_check_a01/execution_worker.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_triplet_stable_check_a01/execution_worker.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0106_execution_worker.py) | `82e8071498a59695f1d8bebcefe318e389b0b16610951adf120841be2269bc3c` | input_or_analysis_code |
| E0107 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene4_singlet_stability_acceptance_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene4_singlet_stability_acceptance_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0107_silylene4_singlet_stability_acceptance_20260930.json) | `b35f078c9cd236d1e20b48d1a026c3da1617b87868450ce2939cc0ef98a8fc6c` | evidence_or_analysis |
| E0108 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0108_execution.json) | `5f22c9aa44d4be19509a6654a383a5bf040dea1cd9bb450c52470550bc72798d` | evidence_or_analysis |
| E0109 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0109_input.com) | `9accb837d67617b2ea555ebd9a53c2e5c357cb0858dd6bf6aef9fc12c15b57d5` | input_or_analysis_code |
| E0110 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0110_identity.json) | `36309e184ba7a67a6ef7c5a466121b9401f15ea7fcfa0b214bee6929efd3d6b8` | evidence_or_analysis |
| E0111 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/restart.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/restart.chk) | `b2c33f64eac5fbb5370626b0a175087f85ee1faefde26a8aee5ad9e171410b70` | evidence_or_analysis |
| E0112 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_restarted_pair_accept_20261003_a01/triplet/wavefunction.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_restarted_pair_accept_20261003_a01/triplet/wavefunction.fchk) | `f893b22bb2a1021392828498db01023b53ea9f39d2ac7219a9563cd34cc444f5` | evidence_or_analysis |
| E0113 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0113_execution.json) | `ed81999128eff569b1760bdb7a80c86f89886e2e85b7c872ce077e7078c08e63` | evidence_or_analysis |
| E0114 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0114_input.com) | `9157e3d93a3775acddf6d27585e5d2e6302366b76e2b3eecb683a2e5f211d5a6` | input_or_analysis_code |
| E0115 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0115_identity.json) | `b6d9c0c16acffa86d895aefbeff32bc3083e4c8edc7bf30baf68ea397591bf48` | evidence_or_analysis |
| E0116 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/checkpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/checkpoint.chk) | `19ee60111022afa19fa8348651ca5f2e850932f7d7aaad9075137ff176746b68` | evidence_or_analysis |
| E0117 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_restarted_pair_accept_20261003_a01/singlet_stability/wavefunction.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene_restarted_pair_accept_20261003_a01/singlet_stability/wavefunction.fchk) | `8065406063cad5f70875adfee5400e2e6709ea95978de70e5fef4d69a01cb7aa` | evidence_or_analysis |
| E0118 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/author_silylene_alt_minima_batch06_20261002.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/author_silylene_alt_minima_batch06_20261002.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0118_author_silylene_alt_minima_batch06_20261002.json) | `dc5aceacac0bdfa800809f26c8a5cd6c442dc6ad237d9ebb7d4ca03d2dbfce49` | evidence_or_analysis |
| E0119 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene_NBO_warning_scope_20261007.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene_NBO_warning_scope_20261007.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0119_silylene_NBO_warning_scope_20261007.json) | `ff1def4f666dacbe06e3fd1f237aa4a8bb345e2c4db2906f19d1a427e38962f6` | evidence_or_analysis |
| E0120 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene_NBO_warning_scope_20261007_a01/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene_NBO_warning_scope_20261007_a01/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0120_execution.json) | `e1e72667e905333201acf89b98c5780a781eb9ebfa09bf7a5795035650a9089f` | evidence_or_analysis |
| E0121 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene_NBO_warning_scope_20261007_a01/analysis_result.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene_NBO_warning_scope_20261007_a01/analysis_result.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0121_analysis_result.json) | `7bc3bc5bc78a2c03a360e4e5b6ebea2e611734f58c240bd0df46c592e32fa506` | evidence_or_analysis |
| E0122 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene_NBO_warning_scope_20261007_a01/analysis.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene_NBO_warning_scope_20261007_a01/analysis.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0122_analysis.json) | `50dddfe24b438c55c12df74469f2f4455c96b66717f99b0c9fc07ba1d01e45b1` | evidence_or_analysis |
| E0123 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/sources/software_defaults_20261005/nbo_faq.html](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group1/sources/software_defaults_20261005/nbo_faq.html) | `a8f5a8e0a5a7e4f0c2f4e58b9907d711faa759bd3e614e5143324d9bb742557c` | evidence_or_analysis |
| E0124 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene_author_route_synthesis_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/report/v2_execution_20260929/silylene_author_route_synthesis_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0124_silylene_author_route_synthesis_20260930.json) | `f9030788f914a7175301950f9984494ba016779aa9fa9abb5810d07da117311d` | evidence_or_analysis |
| E0125 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0125_critical_failures.json) | `adddec7c26e890731c33bd297bc90bed8b9d2c3d8ccbb23e2d364e8bf50c4aa2` | historical_task_binding |
| E0126 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/package_manifest.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_0e835b370ddd37b6/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0126_package_manifest.json) | `29417f250b9c6995ced9eef37630eb0bb318b07e6e83f29d2908a105bdf454d4` | historical_task_binding |
| E0127 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0127_critical_failures.json) | `adddec7c26e890731c33bd297bc90bed8b9d2c3d8ccbb23e2d364e8bf50c4aa2` | historical_task_binding |
| E0128 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/package_manifest.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_0e835b370ddd37b6/package_manifest.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0128_package_manifest.json) | `2234ec9a1a5308d1b9b91ca80c57d8a2c2b8fd4b94071121b6444a56b6037503` | historical_task_binding |
| E0129 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_TS_source_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0129_input.com) | `18abdf4db83741f20fa0cb3ced608496a057489527e3e67743b3cb1bd86b4edf` | input_or_analysis_code |
| E0130 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_IRC_forward/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_IRC_forward/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0130_input.com) | `26d176f1f0f1c593b0e08e1943d6f59e319bafbef7183e97a5c3e7813f5e87e4` | input_or_analysis_code |
| E0131 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_IRC_reverse/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/silylene4_H2_IRC_reverse/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0131_input.com) | `412a1ed25d5271c72d802909ad15f3a012412ad7fc030e6fb651e34a98824721` | input_or_analysis_code |
| E0132 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_IRC_forward_p43_optfreq_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_IRC_forward_p43_optfreq_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0132_input.com) | `3fde1c739a516227174dfa5f01b3fbe16ea3d61909708e36573a6e097abc835e` | input_or_analysis_code |
| E0133 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_reverse_recalcfc_optfreq_a03/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_reverse_recalcfc_optfreq_a03/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0133_input.com) | `613a3d98683087ac95c50b3dfe4e3a9d548206d431008b16def9d510345d6c08` | input_or_analysis_code |
| E0134 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_Hessian_RWF_restart_20261003_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0134_input.com) | `9accb837d67617b2ea555ebd9a53c2e5c357cb0858dd6bf6aef9fc12c15b57d5` | input_or_analysis_code |
| E0135 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_optfreq_20261002_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_triplet_optfreq_20261002_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0135_input.com) | `b953a29046a0fd70c1ed602c382d24acc754c355f8a303c7a4ae1e95fb8e7dc3` | input_or_analysis_code |
| E0136 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_restart_20261003_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0136_input.com) | `9157e3d93a3775acddf6d27585e5d2e6302366b76e2b3eecb683a2e5f211d5a6` | input_or_analysis_code |
| E0137 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_20261002_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_author_silylene1_wB97XD_singlet_Stable_20261002_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0137_input.com) | `713b0656613198af083ac8cd744ebd7cb8e8dd93bb0f0fbb1cc9e82037e32a23` | input_or_analysis_code |
| E0138 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silylene1_exactSI_NBO_20261004_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silylene1_exactSI_NBO_20261004_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0138_input.com) | `3a51bed9ea61865d2c643fcde5cc0809b5b9e882eb9bb2663cc8202071878cc6` | input_or_analysis_code |
| E0139 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silylene4_exactSI_NBO_20261004_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silylene4_exactSI_NBO_20261004_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0139_input.com) | `f105b58176c9038e47bd6a065b21470efc8e395a55ca0bda5ccfff3f84482a12` | input_or_analysis_code |
| E0140 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silyleneVprime_exactSI_NBO_20261004_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_reopen_silyleneVprime_exactSI_NBO_20261004_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0140_input.com) | `79dd487b40957c8fc2622df475fb60847417c339ea3c3c4b2b01d5e103ea48dc` | input_or_analysis_code |
| E0141 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_exactSI_G09Defaults_NBO_20261005_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene1_exactSI_G09Defaults_NBO_20261005_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0141_input.com) | `a5f999590a60708ce65fcb6f08997d5e19bfe6794dc74a5fd4d6f4d4119330c2` | input_or_analysis_code |
| E0142 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_superfine_recalcfc_optfreq_a04/identity.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_superfine_recalcfc_optfreq_a04/identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0142_identity.json) | `58c23bf6472508cc988399dd3dcd276e61984ab816e3d7164a4b9f3fcb33b8cd` | evidence_or_analysis |
| E0143 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_reverse_recalcfc_optfreq_a03/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/inputs/v2_silylene4_reverse_recalcfc_optfreq_a03/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0143_input.com) | `613a3d98683087ac95c50b3dfe4e3a9d548206d431008b16def9d510345d6c08` | input_or_analysis_code |
| E0144 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_reverse_recalcfc_optfreq_a03/execution.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_reverse_recalcfc_optfreq_a03/execution.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0144_execution.json) | `7d031b0ea143af0ae5883d7ef54e617ed4cc9d0d983f1746ae0d43f3f07c8599` | evidence_or_analysis |
| E0145 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_reverse_recalcfc_optfreq_a03/checkpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_reverse_recalcfc_optfreq_a03/checkpoint.chk) | `f6f8dd9b6ce67f60fe4ca18851e3d73eac596516466e22689802210209c8d691` | evidence_or_analysis |
| E0146 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/checkpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_superfine_recalcfc_optfreq_a04/checkpoint.chk) | `b00358c3fe2d647710047159430cb0c3584f7a218d3f97ebf4fa34d001da7a6c` | evidence_or_analysis |
| E0147 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_triplet_stable_check_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_triplet_stable_check_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0147_input.com) | `620af11aa56486f37219be09cc4854413793a3e599496138b9040136f1dc3f01` | input_or_analysis_code |
| E0148 | [docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_source_triplet_optfreq_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_1/papers/paper_0e835b370ddd37b6/outputs/v2_silylene4_source_triplet_optfreq_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_0e835b370ddd37b6/task_archives/paper_reproduction/evaluation/verified_computation/snapshots/E0148_input.com) | `d53f2803dcbb9e08fd0003c019f9cf903309f79f0cc972a9fc84e7e4bbf3566b` | input_or_analysis_code |
| N0149 | [tasks/v2_autonomous_research/paper_0e835b370ddd37b6/agent_input/task.md](../../../v2_autonomous_research/paper_0e835b370ddd37b6/agent_input/task.md) | `ef1854a881acf5038ebf58357278bd883e8052e466bb4b2b53c3622ffe2d1220` | latest_review_evidence |
| N0150 | [tasks/v2_autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_key_points.json](../../../v2_autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_key_points.json) | `1a55e7aecec01f4fb5723d7c0ad490f6e0d98f39de77dba85831d21101d8c8b9` | latest_review_evidence |
| N0151 | [tasks/v2_autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_conclusions.json](../../../v2_autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_conclusions.json) | `99ce6763bf15cc2b5c3842744cd97fbf6955029bd2ccc544e19f4a84e6b3c981` | latest_review_evidence |
| N0152 | [tasks/v2_autonomous_research/paper_0e835b370ddd37b6/evaluation/scoring_rules.json](../../../v2_autonomous_research/paper_0e835b370ddd37b6/evaluation/scoring_rules.json) | `d7df36622dfbc910acbb81d8fbfdc2f03e464215be5de593726b989734a9eae3` | latest_review_evidence |
| N0153 | [tasks/v2_autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_validation_plan.md](../../../v2_autonomous_research/paper_0e835b370ddd37b6/evaluation/reference_validation_plan.md) | `9848c1bd1a4240fb42e2df9a847cda2a94ad032154b0d2f25ef0e7ff11215bb0` | latest_review_evidence |
| N0154 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_0e835b370ddd37b6/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_0e835b370ddd37b6/verified_computation_reference.md) | `2c2fc4ac39a93165fd48aedb754a60858f2d8a20b1444db53bc2cf94d8a80fa3` | latest_review_evidence |
| N0155 | [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/agent_input/task.md](../agent_input/task.md) | `aea8e23c994df9425e839270cfb7c854f90f4a440c21970d56691bc0c302f019` | latest_review_evidence |
| N0156 | [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/reference_key_points.json](reference_key_points.json) | `1a55e7aecec01f4fb5723d7c0ad490f6e0d98f39de77dba85831d21101d8c8b9` | latest_review_evidence |
| N0157 | [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/reference_conclusions.json](reference_conclusions.json) | `99ce6763bf15cc2b5c3842744cd97fbf6955029bd2ccc544e19f4a84e6b3c981` | latest_review_evidence |
| N0158 | [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/scoring_rules.json](scoring_rules.json) | `d7df36622dfbc910acbb81d8fbfdc2f03e464215be5de593726b989734a9eae3` | latest_review_evidence |
| N0159 | [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `9848c1bd1a4240fb42e2df9a847cda2a94ad032154b0d2f25ef0e7ff11215bb0` | latest_review_evidence |
| N0160 | [docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_0e835b370ddd37b6/verified_computation_reference.md](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/paper_reproduction/paper_0e835b370ddd37b6/verified_computation_reference.md) | `5fc4d3d95f9081cdd055bc4d7a2d4fbd1aebed261186c3540a68e33c162432c8` | latest_review_evidence |
| N0161 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0162 | [docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/batch_a_results.json) | `6013c120f4dcc8b7f74d72b9d37c387ae48fc371f4b2c30a752db109007023b0` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/agent_input/task.md](../agent_input/task.md) | `aea8e23c994df9425e839270cfb7c854f90f4a440c21970d56691bc0c302f019` |
| [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/reference_key_points.json](reference_key_points.json) | `1a55e7aecec01f4fb5723d7c0ad490f6e0d98f39de77dba85831d21101d8c8b9` |
| [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/reference_conclusions.json](reference_conclusions.json) | `99ce6763bf15cc2b5c3842744cd97fbf6955029bd2ccc544e19f4a84e6b3c981` |
| [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/scoring_rules.json](scoring_rules.json) | `d7df36622dfbc910acbb81d8fbfdc2f03e464215be5de593726b989734a9eae3` |
| [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/critical_failures.json](critical_failures.json) | `adddec7c26e890731c33bd297bc90bed8b9d2c3d8ccbb23e2d364e8bf50c4aa2` |
| [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/evidence_map.json](evidence_map.json) | `cb089887bed2f7f7a86d754c8d165ed97fbf8515425c94373a23c72591681fd0` |
| [tasks/v2_paper_reproduction/paper_0e835b370ddd37b6/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `9848c1bd1a4240fb42e2df9a847cda2a94ad032154b0d2f25ef0e7ff11215bb0` |

## Current scoring policy — 2026-10-19

The active policy is paper_science_v2: independent intermediate scientific findings and final conclusions sum to 100; no process points, partial-credit discretion or multiplier applies. Active nodes, rules, PDF sources and fixed inclusive tolerances are in the synchronized JSON files. Historical evaluator IDs, weights, freezes and process language in the preceding archive are not current scoring instructions. The public task and PR author-route contract are unchanged. Existing PASS_STRICT_CURRENT_FROZEN_SCOPE acceptance and its scientific limitations remain; this migration runs no new chemistry calculations and does not certify publication readiness.

## Round 3 scoring-contract repair — 2026-10-19

No new paper-specific defect confirmed. Kept80/20 and all six original Gibbs targets; actual benzene298K1atm separated reactants remain essential. Public scoring policy repaired. Existing chemical acceptance and all archived measurements/results above are unchanged. This is a contract/rubric repair with no new quantum calculations or online Judge certification. See docs/final_verified_science_v2_migration_20261019/repair_round3/astra_science_01/REPORT.md.
