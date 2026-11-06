# 2026-10-28 V3 最终命题与证据复用

31条改为18条最终命题/100分：四个绝热物性、九个垂直能级、电子解释、gap-only解释判断和三个供受体适用性结论。九个态字符与三个重元素人口节点退为非评分证据，原rubrene总括项并入三个逐供体结论去重。保持原能量硬窗，未以历史偏差接受替代严格数值判定。

13个最终能量均保留原目标/单位/容差：四个电子绝热T1为1.01993/1.01826/1.08974/0.99675 eV（IR780/Cy1/Cy2/rubrene），对目标1.02/1.02/1.09/1.00±0.01均在窗内。九个垂直能来自response_audit：IR780 S1/T1/T2=1.9389/0.9499/2.1355，Cy1=1.9038/0.9427/2.1011，Cy2=1.8909/1.0555/2.1220 eV；Cy1 S1/T2超原±0.005窗，其余七项在窗内。Cy1固定源几何控制=1.9040/0.9435/2.0995，S1/T2仍超窗，不以替换几何隐藏。T2−S1约0.1966/0.1973/0.2311 eV支持gap-only解释不足。完整XY同分区Mulliken的Cy1/Cy2成对空穴贡献S1=3.27756/15.45674%、T1=0.91660/10.52771%、T2=5.83567/15.19898%，仅作电子解释证据，不等于SOC或ISC速率。匹配电子能的供体减rubrene=+0.0231819/+0.0215130/+0.0929941 eV；一致加ZPVE后+0.0334678/+0.0294316/+0.0979738，支持有条件相容性及Cy2相对裕量。

限制：历史验收为USER_ACCEPTED_DEVIATION，非独立严格通过。Cy1固定源S1/T2残差−0.0112/−0.0196 eV不能通过原硬窗；人口分区和精确跃迁百分比未唯一恢复，不能按论文数字回填本地结果。电子绝热口径来自四物种一致性，原文未明说ZPE。没有分子SOC/ISC速率或唯一S1→T2认证；IR780/Cy1约0.02 eV裕量不证明真实转移自由能、跨方法稳健放能或UC效率。

本轮未运行新计算；下列历史正文逐字保留，旧 PASS/V2 评分不构成本版全面通过。

---

# V2 验证计算参考：Cyanine敏化

论文：`paper_e0791c047a731974`；模式：`autonomous_research`；整理日期：2026-10-15。

本文件位于私有 evaluation，用于维护者复核真实计算，不能作为被评估 agent 的公开输入。只整理已有已执行证据；本轮没有重算、改题、改规则或改容差。

**验收类型：历史用户明确接受数值偏差（USER_ACCEPTED_DEVIATION），不计入 30 篇无额外偏差授权的独立严格通过。** 下述科学计算已完成，但保留未解释的数值/定义差异。

当前验收依据：可维持用户明确接受偏差的当前范围验收；另列于无额外偏差授权的严格计数之外。不能说两篇被接受者的每个作者参数和人口百分比都已恢复。

当前裁定来自 [正式最新裁定](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) 和 [逐篇详细复审](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json)；这些裁定优先于归档中的历史 PASS、candidate 或 HOLD 字样。



## 1. 科学问题、模式范围与数据来源

IR780/Cy1/Cy2的三重态敏化电子特征及与rubrene的能量相容性。

冻结题面中的科学目标：

What molecular electronic evidence can explain differences in triplet sensitization among IR780, Cy1 and Cy2, and does it support their energetic compatibility with rubrene in chloroform?

自主科研模式向 agent 提供科学问题、物种/数据和边界，由其自主选择方法。以下作者路线是维护者验证采用的参考，不要求 agent 照抄该流程，也不是一次新的盲测自主发现记录。

原文/补充材料与本次冻结输入：

| 文件 | SHA-256 |
|---|---|
| [papers/paper_e0791c047a731974/documents/main.pdf](../../../../papers/paper_e0791c047a731974/documents/main.pdf) | `4d136fb1b060c26a81c3dacdb397eed6c4c913f61d95b8ada7262e801a1a91c1` |
| [papers/paper_e0791c047a731974/documents/supplementary_001.pdf](../../../../papers/paper_e0791c047a731974/documents/supplementary_001.pdf) | `06893f8d0c9056eba31a55a3c726a76bba621a0d20c80d6eb9fe11f9d35f1d02` |


任务、物种输入和评分绑定：[冻结题面](../agent_input/task.md)；[公开数据目录](../agent_input/data)。源页、图表和物种对应以以下比较与证据索引为准。

## 2. 作者路线、实际实现与计算依赖

B3LYP/SMD氯仿，I-SDD/Se-def2TZVP；四物种真实S0/UDFT三重态OptFreq、稳定性、TD、完整X/Y及两类人口分区控制。

1. 由正文 Fig.3 与 SI 核对 IR780/Cy1/Cy2 三个 +1 敏化剂及中性 rubrene，反离子排除。Gaussian16 B3LYP/6-31G(d,p)、SMD 氯仿，I 用 SDD ECP、Se 用全电子 def2TZVP，5D/7F 与电子计数保持。

2. 核收八个独立 S0/UDFT-T1 松弛端点与频率、六组垂直响应、九个 S1/T1/T2 电子-空穴分析及同定义四物种能量链；完整 required_calculations 清单共 24 项随附。旧 TD 优化 triplet 不冒充正文要求的 UDFT 绝热端点。

3. 逐一检查原 Opt 收敛、正曲率、自旋、分子身份、基组和溶剂；将后续 Freq 预测位移 NO 与原 Opt 接受分开。用 E(T1)−E(S0) 与含 ZPVE 两种口径分别计算，电子绝热 T1=1.01993/1.01826/1.08974/0.99675 eV 恢复源 1.02/1.02/1.09/1.00。

4. 核收完整 X/Y 导出修复、RPA 范数/序列化界、固定源 Cy1 几何响应及官方 Mulliken/Hirshfeld 两人口分析；主态身份和显著 Se>I 参与在已算定义下保持。Cy1 约 0.01–0.02 eV 和 I-T2 空穴 6.026536% 对源 5.52% 的差沿用用户接受，具体归一化/人口定义并未唯一恢复。

5. 以相同方法/介质比较 sensitizer/rubrene 近阈值能量相容性，保留 IR780/Cy1 约 +0.02 eV 的小余量边界。当前通过不认证每个精确人口百分比、唯一 S1→T2 ISC 途径、SOC/ISC 速率、跨方法真实放能转移或上转换效率。

### 已完成阶段的详细登记

详细冻结数据：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。每条含原路径、原记录及证据编号；可按 paper_id 分开的共享批次记录已筛选为本篇条目；少数联合运行记录保留原文，内含其他论文的信息不作为本篇结果，未展开为本篇证据文件。原作者/当前方法、模型、电荷自旋、温度介质及命令参数以实际输入文件和计算登记为准，未记录的选项不补造。

#### required_calculations（冻结记录 E0007）

```json
[
  {
    "id": "cy2_source_udft_t_optfreq_v2_a01",
    "purpose": "各物种S0/UDFT三重态的独立松弛端点、频率与同定义绝热能",
    "author_or_added": "author_plus_endpoint_validity",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy2",
      "charge": 1,
      "multiplicity": 3,
      "state": "UDFT triplet"
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; UDFT Opt/Freq",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "81ea7772ffcb1a07d0b4ba934ab717a0b397589c0c42eeab72fe3bee0bbd8fa1"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/input.com",
        "sha256": "04cdd3fc0dcaee588b7a98e02e92bd4ed4c2962af99809b7b3e148f931d9c67e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json",
        "sha256": "b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c"
      }
    ],
    "job_id": "hpc-job-e6041af1-f3b6-4063-9915-3f53ed6ea366",
    "native_validity": {
      "native_rc": 0,
      "full_identity_method_checks": {
        "native_rc0_normal": true,
        "normal_segments": true,
        "no_error": true,
        "atoms": true,
        "atom_order": true,
        "source_graph_exact": true,
        "charge_spin": true,
        "effective_electrons": true,
        "all_electron_count": true,
        "optimization_completed": true,
        "optimization_all_four": true,
        "final_force_pass": true,
        "full_curvature_count": true,
        "positive_curvature": true,
        "zpve_present": true,
        "method": true,
        "solvent": true,
        "angular_convention": true,
        "basis": true,
        "all_electron_Se": true,
        "triplet_spin_diagnostic": true
      },
      "positive_modes": 180,
      "minimum_cm1": 16.1161,
      "spin_before_after": [
        [
          2.0063,
          2.0
        ],
        [
          2.0063,
          2.0
        ],
        [
          2.0063,
          2.0
        ]
      ],
      "original_Opt_acceptance": [
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              0.0,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              4.4e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              1.2e-05,
              4e-05,
              "YES"
            ]
          ],
          "segment": 1
        }
      ],
      "later_Freq_prediction": [
        [
          "Maximum Force",
          0.0,
          1.5e-05,
          "YES"
        ],
        [
          "RMS     Force",
          0.0,
          1e-05,
          "YES"
        ],
        [
          "Maximum Displacement",
          6.1e-05,
          6e-05,
          "NO"
        ],
        [
          "RMS     Displacement",
          1.6e-05,
          4e-05,
          "YES"
        ]
      ],
      "convergence_caveat": "Final frequency-derived displacement criterion not all passed; retain native optimization criteria, tiny-force and local-curvature scope. No global-minimum or strict final four-criterion certification."
    },
    "actual_outputs": {
      "electronic_energy_Eh": -6109.28523636,
      "ZPVE_Eh": 0.502508
    },
    "new_compute_this_turn": false
  },
  {
    "id": "ir780_source_s0_optfreq_v2_a01",
    "purpose": "各物种S0/UDFT三重态的独立松弛端点、频率与同定义绝热能",
    "author_or_added": "author_plus_endpoint_validity",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "IR780",
      "charge": 1,
      "multiplicity": 1,
      "state": "S0"
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; restrictedDFT Opt/Freq",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/stdout.log",
        "sha256": "eb189981e13afdf94b3edde3a6521cbd283169793b37532decdfe7c26557399c"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/input.com",
        "sha256": "73164984762d082db2cc2164a8dfcd861dc3d3ba5c06193e46bdb614923c3cb1"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json",
        "sha256": "b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c"
      }
    ],
    "job_id": "hpc-job-47979736-3f88-4be2-8c8b-9001e5d7cdaf",
    "native_validity": {
      "native_rc": 0,
      "full_identity_method_checks": {
        "native_rc0_normal": true,
        "normal_segments": true,
        "no_error": true,
        "atoms": true,
        "atom_order": true,
        "source_graph_exact": true,
        "charge_spin": true,
        "effective_electrons": true,
        "all_electron_count": true,
        "optimization_completed": true,
        "optimization_all_four": true,
        "final_force_pass": true,
        "full_curvature_count": true,
        "positive_curvature": true,
        "zpve_present": true,
        "method": true,
        "solvent": true,
        "angular_convention": true,
        "basis": true,
        "no_ECP": true
      },
      "positive_modes": 243,
      "minimum_cm1": 10.5233,
      "spin_before_after": [],
      "original_Opt_acceptance": [
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              0.0,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              2.1e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              4e-06,
              4e-05,
              "YES"
            ]
          ],
          "segment": 1
        },
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              0.0,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              5.6e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              1.2e-05,
              4e-05,
              "YES"
            ]
          ],
          "segment": 2
        }
      ],
      "later_Freq_prediction": [
        [
          "Maximum Force",
          0.0,
          1.5e-05,
          "YES"
        ],
        [
          "RMS     Force",
          0.0,
          1e-05,
          "YES"
        ],
        [
          "Maximum Displacement",
          5.6e-05,
          6e-05,
          "YES"
        ],
        [
          "RMS     Displacement",
          1.2e-05,
          4e-05,
          "YES"
        ]
      ],
      "convergence_caveat": null
    },
    "actual_outputs": {
      "electronic_energy_Eh": -1967.96836245,
      "ZPVE_Eh": 0.720164
    },
    "new_compute_this_turn": false
  },
  {
    "id": "ir780_source_udft_t_optfreq_v2_a01",
    "purpose": "各物种S0/UDFT三重态的独立松弛端点、频率与同定义绝热能",
    "author_or_added": "author_plus_endpoint_validity",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "IR780",
      "charge": 1,
      "multiplicity": 3,
      "state": "UDFT triplet"
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; UDFT Opt/Freq",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "d8948b9025aef77ca59cc577cf79033a7bf190a8976b6a6e10512ba9831e34eb"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/input.com",
        "sha256": "44720be0dadb92c0fc950d20ac5148f1cd08c42f72459da8c96c24b47a00d75f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json",
        "sha256": "b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c"
      }
    ],
    "job_id": "hpc-job-f523ed6e-0883-4eae-b4d3-35d5ab94a9a7",
    "native_validity": {
      "native_rc": 0,
      "full_identity_method_checks": {
        "native_rc0_normal": true,
        "normal_segments": true,
        "no_error": true,
        "atoms": true,
        "atom_order": true,
        "source_graph_exact": true,
        "charge_spin": true,
        "effective_electrons": true,
        "all_electron_count": true,
        "optimization_completed": true,
        "optimization_all_four": true,
        "final_force_pass": true,
        "full_curvature_count": true,
        "positive_curvature": true,
        "zpve_present": true,
        "method": true,
        "solvent": true,
        "angular_convention": true,
        "basis": true,
        "no_ECP": true,
        "triplet_spin_diagnostic": true
      },
      "positive_modes": 243,
      "minimum_cm1": 12.2122,
      "spin_before_after": [
        [
          2.0089,
          2.0001
        ],
        [
          2.0089,
          2.0001
        ],
        [
          2.0089,
          2.0001
        ]
      ],
      "original_Opt_acceptance": [
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              1e-06,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              1.3e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              3e-06,
              4e-05,
              "YES"
            ]
          ],
          "segment": 1
        },
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              1e-06,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              1.5e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              4e-06,
              4e-05,
              "YES"
            ]
          ],
          "segment": 2
        }
      ],
      "later_Freq_prediction": [
        [
          "Maximum Force",
          1e-06,
          1.5e-05,
          "YES"
        ],
        [
          "RMS     Force",
          0.0,
          1e-05,
          "YES"
        ],
        [
          "Maximum Displacement",
          1.5e-05,
          6e-05,
          "YES"
        ],
        [
          "RMS     Displacement",
          4e-06,
          4e-05,
          "YES"
        ]
      ],
      "convergence_caveat": null
    },
    "actual_outputs": {
      "electronic_energy_Eh": -1967.9308808,
      "ZPVE_Eh": 0.718409
    },
    "new_compute_this_turn": false
  },
  {
    "id": "cy1_source_s0_optfreq_v2_a01",
    "purpose": "各物种S0/UDFT三重态的独立松弛端点、频率与同定义绝热能",
    "author_or_added": "author_plus_endpoint_validity",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy1",
      "charge": 1,
      "multiplicity": 1,
      "state": "S0"
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; restrictedDFT Opt/Freq",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/stdout.log",
        "sha256": "3a0a2fb4cd6a470f885015dea02c75e4905dd0d8eacd221764eda8fc56f467ce"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/input.com",
        "sha256": "21be808f1ed902616333d4124452449af62d48859b97447e507ba0eeab640f6f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json",
        "sha256": "b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c"
      }
    ],
    "job_id": "hpc-job-152cc037-ce33-45be-b7a6-718cda0b8bf2",
    "native_validity": {
      "native_rc": 0,
      "full_identity_method_checks": {
        "native_rc0_normal": true,
        "normal_segments": true,
        "no_error": true,
        "atoms": true,
        "atom_order": true,
        "source_graph_exact": true,
        "charge_spin": true,
        "effective_electrons": true,
        "all_electron_count": true,
        "optimization_completed": true,
        "optimization_all_four": true,
        "final_force_pass": true,
        "full_curvature_count": true,
        "positive_curvature": true,
        "zpve_present": true,
        "method": true,
        "solvent": true,
        "angular_convention": true,
        "basis": true,
        "iodine_ECP": true
      },
      "positive_modes": 225,
      "minimum_cm1": 7.8392,
      "spin_before_after": [],
      "original_Opt_acceptance": [
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              1e-06,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              5.1e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              9e-06,
              4e-05,
              "YES"
            ]
          ],
          "segment": 1
        }
      ],
      "later_Freq_prediction": [
        [
          "Maximum Force",
          1e-06,
          1.5e-05,
          "YES"
        ],
        [
          "RMS     Force",
          0.0,
          1e-05,
          "YES"
        ],
        [
          "Maximum Displacement",
          0.000108,
          6e-05,
          "NO"
        ],
        [
          "RMS     Displacement",
          2.2e-05,
          4e-05,
          "YES"
        ]
      ],
      "convergence_caveat": "Final frequency-derived displacement criterion not all passed; retain native optimization criteria, tiny-force and local-curvature scope. No global-minimum or strict final four-criterion certification."
    },
    "actual_outputs": {
      "electronic_energy_Eh": -1910.94630729,
      "ZPVE_Eh": 0.642065
    },
    "new_compute_this_turn": false
  },
  {
    "id": "cy1_source_udft_t_optfreq_v2_a01",
    "purpose": "各物种S0/UDFT三重态的独立松弛端点、频率与同定义绝热能",
    "author_or_added": "author_plus_endpoint_validity",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy1",
      "charge": 1,
      "multiplicity": 3,
      "state": "UDFT triplet"
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; UDFT Opt/Freq",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "82569e6406285efb534eb66a2bd0ce35f41b5215bdaaead543ee192f73ecae84"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/input.com",
        "sha256": "06bcb1e4ace63034a1663ab8695c7b019c2cc590d3945c686ae15eaf16d7ee2b"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json",
        "sha256": "b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c"
      }
    ],
    "job_id": "hpc-job-373cfe32-e1f0-48e0-b732-2b5dd836589a",
    "native_validity": {
      "native_rc": 0,
      "full_identity_method_checks": {
        "native_rc0_normal": true,
        "normal_segments": true,
        "no_error": true,
        "atoms": true,
        "atom_order": true,
        "source_graph_exact": true,
        "charge_spin": true,
        "effective_electrons": true,
        "all_electron_count": true,
        "optimization_completed": true,
        "optimization_all_four": true,
        "final_force_pass": true,
        "full_curvature_count": true,
        "positive_curvature": true,
        "zpve_present": true,
        "method": true,
        "solvent": true,
        "angular_convention": true,
        "basis": true,
        "iodine_ECP": true,
        "triplet_spin_diagnostic": true
      },
      "positive_modes": 225,
      "minimum_cm1": 11.9623,
      "spin_before_after": [
        [
          2.0089,
          2.0001
        ],
        [
          2.0089,
          2.0001
        ],
        [
          2.0089,
          2.0001
        ]
      ],
      "original_Opt_acceptance": [
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              0.0,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              3.6e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              7e-06,
              4e-05,
              "YES"
            ]
          ],
          "segment": 1
        },
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              0.0,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              1.1e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              3e-06,
              4e-05,
              "YES"
            ]
          ],
          "segment": 2
        }
      ],
      "later_Freq_prediction": [
        [
          "Maximum Force",
          0.0,
          1.5e-05,
          "YES"
        ],
        [
          "RMS     Force",
          0.0,
          1e-05,
          "YES"
        ],
        [
          "Maximum Displacement",
          1.1e-05,
          6e-05,
          "YES"
        ],
        [
          "RMS     Displacement",
          3e-06,
          4e-05,
          "YES"
        ]
      ],
      "convergence_caveat": null
    },
    "actual_outputs": {
      "electronic_energy_Eh": -1910.90888697,
      "ZPVE_Eh": 0.640223
    },
    "new_compute_this_turn": false
  },
  {
    "id": "rubrene_source_s0_optfreq_v2_a01",
    "purpose": "各物种S0/UDFT三重态的独立松弛端点、频率与同定义绝热能",
    "author_or_added": "author_plus_endpoint_validity",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "rubrene",
      "charge": 0,
      "multiplicity": 1,
      "state": "S0"
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; restrictedDFT Opt/Freq",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/stdout.log",
        "sha256": "fbc3136f51dc2c92c9dc838e43453860ce446eaf7b9f833c62c28027942f9e6c"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/input.com",
        "sha256": "385d3add4e1036fb3491557549b3ea584bfe132c8ead5dbb6faf1e954542dfe3"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json",
        "sha256": "b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c"
      }
    ],
    "job_id": "hpc-job-757331a0-7a17-4d37-a06e-e509e9ba4e38",
    "native_validity": {
      "native_rc": 0,
      "full_identity_method_checks": {
        "native_rc0_normal": true,
        "normal_segments": true,
        "no_error": true,
        "atoms": true,
        "atom_order": true,
        "source_graph_exact": true,
        "charge_spin": true,
        "effective_electrons": true,
        "all_electron_count": true,
        "optimization_completed": true,
        "optimization_all_four": true,
        "final_force_pass": true,
        "full_curvature_count": true,
        "positive_curvature": true,
        "zpve_present": true,
        "method": true,
        "solvent": true,
        "angular_convention": true,
        "basis": true,
        "no_ECP": true
      },
      "positive_modes": 204,
      "minimum_cm1": 24.1189,
      "spin_before_after": [],
      "original_Opt_acceptance": [
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              1e-06,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              4.6e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              1.1e-05,
              4e-05,
              "YES"
            ]
          ],
          "segment": 1
        },
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              1e-06,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              5.4e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              1.3e-05,
              4e-05,
              "YES"
            ]
          ],
          "segment": 2
        }
      ],
      "later_Freq_prediction": [
        [
          "Maximum Force",
          1e-06,
          1.5e-05,
          "YES"
        ],
        [
          "RMS     Force",
          0.0,
          1e-05,
          "YES"
        ],
        [
          "Maximum Displacement",
          5.4e-05,
          6e-05,
          "YES"
        ],
        [
          "RMS     Displacement",
          1.3e-05,
          4e-05,
          "YES"
        ]
      ],
      "convergence_caveat": null
    },
    "actual_outputs": {
      "electronic_energy_Eh": -1617.38568755,
      "ZPVE_Eh": 0.562669
    },
    "new_compute_this_turn": false
  },
  {
    "id": "rubrene_source_udft_t_optfreq_v2_a01",
    "purpose": "各物种S0/UDFT三重态的独立松弛端点、频率与同定义绝热能",
    "author_or_added": "author_plus_endpoint_validity",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "rubrene",
      "charge": 0,
      "multiplicity": 3,
      "state": "UDFT triplet"
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; UDFT Opt/Freq",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "a6154333d63a2123590305e002414971b80c78fdb9c89172fda65cea327456de"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/input.com",
        "sha256": "0d02360e455f1135a0c46cf6c7a2b7d12a7bf9d5b8a12372a05801025e1408f6"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json",
        "sha256": "b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c"
      }
    ],
    "job_id": "hpc-job-5e2ff286-e84b-47b8-a7da-9a3da5032a43",
    "native_validity": {
      "native_rc": 0,
      "full_identity_method_checks": {
        "native_rc0_normal": true,
        "normal_segments": true,
        "no_error": true,
        "atoms": true,
        "atom_order": true,
        "source_graph_exact": true,
        "charge_spin": true,
        "effective_electrons": true,
        "all_electron_count": true,
        "optimization_completed": true,
        "optimization_all_four": true,
        "final_force_pass": true,
        "full_curvature_count": true,
        "positive_curvature": true,
        "zpve_present": true,
        "method": true,
        "solvent": true,
        "angular_convention": true,
        "basis": true,
        "no_ECP": true,
        "triplet_spin_diagnostic": true
      },
      "positive_modes": 204,
      "minimum_cm1": 17.105,
      "spin_before_after": [
        [
          2.0289,
          2.0005
        ],
        [
          2.0289,
          2.0005
        ],
        [
          2.0289,
          2.0005
        ]
      ],
      "original_Opt_acceptance": [
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              0.0,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              3e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              6e-06,
              4e-05,
              "YES"
            ]
          ],
          "segment": 1
        },
        {
          "marker": "Optimization completed.",
          "criteria": [
            [
              "Maximum Force",
              0.0,
              1.5e-05,
              "YES"
            ],
            [
              "RMS     Force",
              0.0,
              1e-05,
              "YES"
            ],
            [
              "Maximum Displacement",
              3.3e-05,
              6e-05,
              "YES"
            ],
            [
              "RMS     Displacement",
              6e-06,
              4e-05,
              "YES"
            ]
          ],
          "segment": 2
        }
      ],
      "later_Freq_prediction": [
        [
          "Maximum Force",
          0.0,
          1.5e-05,
          "YES"
        ],
        [
          "RMS     Force",
          0.0,
          1e-05,
          "YES"
        ],
        [
          "Maximum Displacement",
          3.3e-05,
          6e-05,
          "YES"
        ],
        [
          "RMS     Displacement",
          6e-06,
          4e-05,
          "YES"
        ]
      ],
      "convergence_caveat": null
    },
    "actual_outputs": {
      "electronic_energy_Eh": -1617.34905782,
      "ZPVE_Eh": 0.560536
    },
    "new_compute_this_turn": false
  },
  {
    "id": "Cy2_S0_inherited_OptFreq",
    "purpose": "复用合法Cy2S0，禁止因升级重新优化",
    "author_or_added": "author_plus_endpoint_validity",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy2",
      "charge": 1,
      "multiplicity": 1,
      "atoms": 62
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stdout.log",
        "sha256": "d789107d6428836a2032ff8f198a1a48e32a1d33285778cbe7095ca2c39ae1be"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_native_reuse_audit_v2_a01/cy2_native_reuse_audit.json",
        "sha256": "51911a8a01d092f00f6195dad36ebf8675dc62e5912f3440e4db3532bc4fc793"
      }
    ],
    "job_id": null,
    "native_validity": {
      "normal": true,
      "positive_modes": 180,
      "minimum_cm1": 9.0747,
      "source_graph": true,
      "atom_order": true,
      "source_basis": true,
      "solvent": "SMD chloroform"
    },
    "actual_outputs": {
      "SCF_energy_Eh": -6109.32528356,
      "ZPVE_Eh": 0.504458
    },
    "new_compute_this_turn": false
  },
  {
    "id": "IR780_singlet_verticalTD",
    "purpose": "S0上垂直S1/T1/T2能量、f及同态响应",
    "author_or_added": "author",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "IR780",
      "charge": 1,
      "reference_multiplicity": 1,
      "spin_block": "singlet",
      "S0_geometry_difference_bohr": 0.0
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; fullTD",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/stdout.log",
        "sha256": "6d10ea193a4871fc13b657a5db5cb476b1f22c012e5b60ff6a3df32a95eb8c54"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/input.com",
        "sha256": "de7cfc12bd0be1c7a69d7dd7b9c6ae4f706de917d34c236bc07aa8bfe8bd5e69"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
        "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
      }
    ],
    "job_id": "hpc-job-a29aca78-a166-4ed9-9c56-0cf27a828682",
    "native_validity": {
      "normal": true,
      "response_converged": true,
      "state_identity_and_basis_checked": true,
      "printed_states": 6
    },
    "actual_outputs": [
      {
        "root": 1,
        "spin": "Singlet",
        "energy_eV": 1.9389,
        "wavelength_nm": 639.46,
        "f": 2.4673,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 145,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.70963,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 145,
            "to_mo": 146,
            "direction": "<-",
            "amplitude": -0.11165,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 2,
        "spin": "Singlet",
        "energy_eV": 2.9638,
        "wavelength_nm": 418.33,
        "f": 0.0024,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 144,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.68343,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 145,
            "to_mo": 147,
            "direction": "->",
            "amplitude": -0.17522,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 3,
        "spin": "Singlet",
        "energy_eV": 3.5025,
        "wavelength_nm": 353.99,
        "f": 0.0082,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 141,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.17694,
            "occupied_label": "HOMO-4",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.67367,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 4,
        "spin": "Singlet",
        "energy_eV": 3.5892,
        "wavelength_nm": 345.44,
        "f": 0.0935,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 142,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.52644,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 145,
            "to_mo": 147,
            "direction": "->",
            "amplitude": 0.44916,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 5,
        "spin": "Singlet",
        "energy_eV": 3.6188,
        "wavelength_nm": 342.61,
        "f": 0.0501,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 142,
            "to_mo": 146,
            "direction": "->",
            "amplitude": -0.45699,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 144,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.13984,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 145,
            "to_mo": 147,
            "direction": "->",
            "amplitude": 0.49182,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 6,
        "spin": "Singlet",
        "energy_eV": 3.6202,
        "wavelength_nm": 342.48,
        "f": 0.0074,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 141,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.66815,
            "occupied_label": "HOMO-4",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 146,
            "direction": "->",
            "amplitude": -0.17333,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      }
    ],
    "new_compute_this_turn": false
  },
  {
    "id": "IR780_triplet_verticalTD",
    "purpose": "S0上垂直S1/T1/T2能量、f及同态响应",
    "author_or_added": "author",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "IR780",
      "charge": 1,
      "reference_multiplicity": 1,
      "spin_block": "triplet",
      "S0_geometry_difference_bohr": 0.0
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; fullTD",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/stdout.log",
        "sha256": "960dbe5343d4613d879833fe8493aa38395c4e6eee040430e0c338ee95e15f23"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/input.com",
        "sha256": "ee6c1d95717c91ba676d0eccc1132990639e6f223a48706fa8cedba6259926e8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
        "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
      }
    ],
    "job_id": "hpc-job-7660116f-b4cb-47c8-8d15-db1f092f3678",
    "native_validity": {
      "normal": true,
      "response_converged": true,
      "state_identity_and_basis_checked": true,
      "printed_states": 6
    },
    "actual_outputs": [
      {
        "root": 1,
        "spin": "Triplet",
        "energy_eV": 0.9499,
        "wavelength_nm": 1305.24,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 145,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.71541,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 145,
            "to_mo": 146,
            "direction": "<-",
            "amplitude": 0.13831,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 2,
        "spin": "Triplet",
        "energy_eV": 2.1355,
        "wavelength_nm": 580.59,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 140,
            "to_mo": 146,
            "direction": "->",
            "amplitude": -0.11438,
            "occupied_label": "HOMO-5",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 144,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.68321,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 3,
        "spin": "Triplet",
        "energy_eV": 2.6049,
        "wavelength_nm": 475.96,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 143,
            "to_mo": 147,
            "direction": "->",
            "amplitude": 0.10007,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO+1"
          },
          {
            "from_mo": 145,
            "to_mo": 147,
            "direction": "->",
            "amplitude": 0.683,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 4,
        "spin": "Triplet",
        "energy_eV": 2.8427,
        "wavelength_nm": 436.14,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 138,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.11045,
            "occupied_label": "HOMO-7",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.64677,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 144,
            "to_mo": 147,
            "direction": "->",
            "amplitude": -0.18204,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 5,
        "spin": "Triplet",
        "energy_eV": 3.3594,
        "wavelength_nm": 369.06,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 140,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.60263,
            "occupied_label": "HOMO-5",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 142,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.14537,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 147,
            "direction": "->",
            "amplitude": -0.16692,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO+1"
          },
          {
            "from_mo": 144,
            "to_mo": 150,
            "direction": "->",
            "amplitude": -0.14586,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+4"
          },
          {
            "from_mo": 145,
            "to_mo": 151,
            "direction": "->",
            "amplitude": 0.12786,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+5"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 6,
        "spin": "Triplet",
        "energy_eV": 3.473,
        "wavelength_nm": 356.99,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 141,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.67326,
            "occupied_label": "HOMO-4",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.1072,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      }
    ],
    "new_compute_this_turn": false
  },
  {
    "id": "Cy1_singlet_verticalTD",
    "purpose": "S0上垂直S1/T1/T2能量、f及同态响应",
    "author_or_added": "author",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy1",
      "charge": 1,
      "reference_multiplicity": 1,
      "spin_block": "singlet",
      "S0_geometry_difference_bohr": 0.0
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; fullTD",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/stdout.log",
        "sha256": "e0c71b0adfa09fd0b6ab54e0cc603c6504cd15d35f8332c68bcd32aca8c588b8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/input.com",
        "sha256": "22c548e81e94dab7ae4b641c27c571dbab6d04e3417c6bb73686b1491437f69f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
        "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
      }
    ],
    "job_id": "hpc-job-2976a79f-8faf-4ade-a04b-694b986cc8e3",
    "native_validity": {
      "normal": true,
      "response_converged": true,
      "state_identity_and_basis_checked": true,
      "printed_states": 6
    },
    "actual_outputs": [
      {
        "root": 1,
        "spin": "Singlet",
        "energy_eV": 1.9038,
        "wavelength_nm": 651.24,
        "f": 2.614,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 143,
            "to_mo": 144,
            "direction": "->",
            "amplitude": 0.70798,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 144,
            "direction": "<-",
            "amplitude": -0.10726,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 2,
        "spin": "Singlet",
        "energy_eV": 2.8366,
        "wavelength_nm": 437.08,
        "f": 0.0159,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 142,
            "to_mo": 144,
            "direction": "->",
            "amplitude": 0.69397,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.12816,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 3,
        "spin": "Singlet",
        "energy_eV": 3.2394,
        "wavelength_nm": 382.74,
        "f": 0.0098,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 141,
            "to_mo": 144,
            "direction": "->",
            "amplitude": 0.69993,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 4,
        "spin": "Singlet",
        "energy_eV": 3.5191,
        "wavelength_nm": 352.31,
        "f": 0.1836,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 140,
            "to_mo": 144,
            "direction": "->",
            "amplitude": -0.28587,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 142,
            "to_mo": 144,
            "direction": "->",
            "amplitude": -0.10905,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.63236,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 5,
        "spin": "Singlet",
        "energy_eV": 3.6831,
        "wavelength_nm": 336.63,
        "f": 0.0,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 142,
            "to_mo": 147,
            "direction": "->",
            "amplitude": 0.14901,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+3"
          },
          {
            "from_mo": 143,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.68315,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+2"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 6,
        "spin": "Singlet",
        "energy_eV": 3.6832,
        "wavelength_nm": 336.62,
        "f": 0.0002,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 142,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.14906,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+2"
          },
          {
            "from_mo": 143,
            "to_mo": 147,
            "direction": "->",
            "amplitude": 0.68293,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+3"
          }
        ],
        "coefficient_list_complete": false
      }
    ],
    "new_compute_this_turn": false
  },
  {
    "id": "Cy1_triplet_verticalTD",
    "purpose": "S0上垂直S1/T1/T2能量、f及同态响应",
    "author_or_added": "author",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy1",
      "charge": 1,
      "reference_multiplicity": 1,
      "spin_block": "triplet",
      "S0_geometry_difference_bohr": 0.0
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; fullTD",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/stdout.log",
        "sha256": "ca88b415f17f996ceed76748fa62304eec85a4a97bfe028b554d37d6a618bd70"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/input.com",
        "sha256": "012fa1e19d74db54756de8975aecbad9b0797020cc759c9685ad42b94211bff4"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
        "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
      }
    ],
    "job_id": "hpc-job-d439bc06-0f6d-4449-a1c5-d05b9937c6dd",
    "native_validity": {
      "normal": true,
      "response_converged": true,
      "state_identity_and_basis_checked": true,
      "printed_states": 6
    },
    "actual_outputs": [
      {
        "root": 1,
        "spin": "Triplet",
        "energy_eV": 0.9427,
        "wavelength_nm": 1315.22,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 143,
            "to_mo": 144,
            "direction": "->",
            "amplitude": 0.71384,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 144,
            "direction": "<-",
            "amplitude": 0.13774,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 2,
        "spin": "Triplet",
        "energy_eV": 2.1011,
        "wavelength_nm": 590.09,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 140,
            "to_mo": 144,
            "direction": "->",
            "amplitude": -0.19298,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 142,
            "to_mo": 144,
            "direction": "->",
            "amplitude": 0.66464,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 3,
        "spin": "Triplet",
        "energy_eV": 2.5893,
        "wavelength_nm": 478.83,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 141,
            "to_mo": 145,
            "direction": "->",
            "amplitude": -0.10169,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO+1"
          },
          {
            "from_mo": 143,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.67903,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 4,
        "spin": "Triplet",
        "energy_eV": 2.7293,
        "wavelength_nm": 454.26,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 135,
            "to_mo": 144,
            "direction": "->",
            "amplitude": 0.19591,
            "occupied_label": "HOMO-8",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 141,
            "to_mo": 144,
            "direction": "->",
            "amplitude": 0.63686,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 142,
            "to_mo": 145,
            "direction": "->",
            "amplitude": -0.15893,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 5,
        "spin": "Triplet",
        "energy_eV": 3.2055,
        "wavelength_nm": 386.78,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 134,
            "to_mo": 144,
            "direction": "->",
            "amplitude": -0.23438,
            "occupied_label": "HOMO-9",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 138,
            "to_mo": 144,
            "direction": "->",
            "amplitude": -0.18515,
            "occupied_label": "HOMO-5",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 140,
            "to_mo": 144,
            "direction": "->",
            "amplitude": 0.55723,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 141,
            "to_mo": 145,
            "direction": "->",
            "amplitude": -0.12291,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO+1"
          },
          {
            "from_mo": 142,
            "to_mo": 144,
            "direction": "->",
            "amplitude": 0.15721,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 142,
            "to_mo": 150,
            "direction": "->",
            "amplitude": -0.1361,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+6"
          },
          {
            "from_mo": 143,
            "to_mo": 151,
            "direction": "->",
            "amplitude": 0.11423,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+7"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 6,
        "spin": "Triplet",
        "energy_eV": 3.5244,
        "wavelength_nm": 351.79,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 138,
            "to_mo": 149,
            "direction": "->",
            "amplitude": -0.11534,
            "occupied_label": "HOMO-5",
            "virtual_label": "LUMO+5"
          },
          {
            "from_mo": 139,
            "to_mo": 148,
            "direction": "->",
            "amplitude": -0.12772,
            "occupied_label": "HOMO-4",
            "virtual_label": "LUMO+4"
          },
          {
            "from_mo": 141,
            "to_mo": 144,
            "direction": "->",
            "amplitude": 0.13514,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 141,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.13127,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO+2"
          },
          {
            "from_mo": 142,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.1877,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+1"
          },
          {
            "from_mo": 142,
            "to_mo": 147,
            "direction": "->",
            "amplitude": 0.17544,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+3"
          },
          {
            "from_mo": 142,
            "to_mo": 151,
            "direction": "->",
            "amplitude": -0.11573,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+7"
          },
          {
            "from_mo": 143,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.42114,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+2"
          },
          {
            "from_mo": 143,
            "to_mo": 148,
            "direction": "->",
            "amplitude": -0.26357,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+4"
          },
          {
            "from_mo": 143,
            "to_mo": 150,
            "direction": "->",
            "amplitude": 0.2522,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+6"
          }
        ],
        "coefficient_list_complete": false
      }
    ],
    "new_compute_this_turn": false
  },
  {
    "id": "Cy2_singlet_verticalTD",
    "purpose": "S0上垂直S1/T1/T2能量、f及同态响应",
    "author_or_added": "author",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy2",
      "charge": 1,
      "reference_multiplicity": 1,
      "spin_block": "singlet",
      "S0_geometry_difference_bohr": 9.499999999995623e-07
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; fullTD",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stdout.log",
        "sha256": "3d11a8885822bfee61357107296ff4ec090ad3e9000243a959a237023aba20d2"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/input.com",
        "sha256": "7b5fadeceea4b5b6039b2de7c040e192efc779f15c5309c8e691bab47833b8d2"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
        "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
      }
    ],
    "job_id": null,
    "native_validity": {
      "normal": true,
      "response_converged": true,
      "state_identity_and_basis_checked": true,
      "printed_states": 6
    },
    "actual_outputs": [
      {
        "root": 1,
        "spin": "Singlet",
        "energy_eV": 1.8909,
        "wavelength_nm": 655.7,
        "f": 2.588,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 144,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.70699,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 2,
        "spin": "Singlet",
        "energy_eV": 2.7368,
        "wavelength_nm": 453.02,
        "f": 0.0317,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 143,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.69355,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 144,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.10043,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 3,
        "spin": "Singlet",
        "energy_eV": 3.0441,
        "wavelength_nm": 407.3,
        "f": 0.1944,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 142,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.6971,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 4,
        "spin": "Singlet",
        "energy_eV": 3.3767,
        "wavelength_nm": 367.18,
        "f": 0.075,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 141,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.53391,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 144,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.45712,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 5,
        "spin": "Singlet",
        "energy_eV": 3.6004,
        "wavelength_nm": 344.36,
        "f": 0.0371,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 141,
            "to_mo": 145,
            "direction": "->",
            "amplitude": -0.34371,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 144,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.38042,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          },
          {
            "from_mo": 144,
            "to_mo": 147,
            "direction": "->",
            "amplitude": -0.31088,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+2"
          },
          {
            "from_mo": 144,
            "to_mo": 148,
            "direction": "->",
            "amplitude": 0.32238,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+3"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 6,
        "spin": "Singlet",
        "energy_eV": 3.6141,
        "wavelength_nm": 343.06,
        "f": 0.0091,
        "S2": 0.0,
        "printed_transitions": [
          {
            "from_mo": 141,
            "to_mo": 145,
            "direction": "->",
            "amplitude": -0.14989,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 148,
            "direction": "->",
            "amplitude": -0.14008,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+3"
          },
          {
            "from_mo": 144,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.1775,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          },
          {
            "from_mo": 144,
            "to_mo": 147,
            "direction": "->",
            "amplitude": 0.61111,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+2"
          },
          {
            "from_mo": 144,
            "to_mo": 148,
            "direction": "->",
            "amplitude": 0.20647,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+3"
          }
        ],
        "coefficient_list_complete": false
      }
    ],
    "new_compute_this_turn": false
  },
  {
    "id": "Cy2_triplet_verticalTD",
    "purpose": "S0上垂直S1/T1/T2能量、f及同态响应",
    "author_or_added": "author",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy2",
      "charge": 1,
      "reference_multiplicity": 1,
      "spin_block": "triplet",
      "S0_geometry_difference_bohr": 9.499999999995623e-07
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; fullTD",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stdout.log",
        "sha256": "d255edb8b66d87556d3ccf100a14c3afaa92bee5d421f03a4d035261d2e6ff1c"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/input.com",
        "sha256": "790932d90471c3924bfbeb845ac5fbd951e79f762eb2a8920c1039bfd0e824e6"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
        "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
      }
    ],
    "job_id": null,
    "native_validity": {
      "normal": true,
      "response_converged": true,
      "state_identity_and_basis_checked": true,
      "printed_states": 6
    },
    "actual_outputs": [
      {
        "root": 1,
        "spin": "Triplet",
        "energy_eV": 1.0555,
        "wavelength_nm": 1174.61,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 144,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.70813,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 144,
            "to_mo": 145,
            "direction": "<-",
            "amplitude": 0.10537,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 2,
        "spin": "Triplet",
        "energy_eV": 2.122,
        "wavelength_nm": 584.27,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 139,
            "to_mo": 145,
            "direction": "->",
            "amplitude": -0.11888,
            "occupied_label": "HOMO-5",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 141,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.18477,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.65687,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 3,
        "spin": "Triplet",
        "energy_eV": 2.566,
        "wavelength_nm": 483.18,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 144,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.6765,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 4,
        "spin": "Triplet",
        "energy_eV": 2.6945,
        "wavelength_nm": 460.15,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 138,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.10403,
            "occupied_label": "HOMO-6",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 142,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.66767,
            "occupied_label": "HOMO-2",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 146,
            "direction": "->",
            "amplitude": -0.12822,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+1"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 5,
        "spin": "Triplet",
        "energy_eV": 2.9641,
        "wavelength_nm": 418.29,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 141,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.64125,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 143,
            "to_mo": 145,
            "direction": "->",
            "amplitude": -0.18724,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO"
          }
        ],
        "coefficient_list_complete": false
      },
      {
        "root": 6,
        "spin": "Triplet",
        "energy_eV": 3.212,
        "wavelength_nm": 386.0,
        "f": 0.0,
        "S2": 2.0,
        "printed_transitions": [
          {
            "from_mo": 140,
            "to_mo": 145,
            "direction": "->",
            "amplitude": 0.58709,
            "occupied_label": "HOMO-4",
            "virtual_label": "LUMO"
          },
          {
            "from_mo": 141,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.16607,
            "occupied_label": "HOMO-3",
            "virtual_label": "LUMO+1"
          },
          {
            "from_mo": 143,
            "to_mo": 146,
            "direction": "->",
            "amplitude": 0.12656,
            "occupied_label": "HOMO-1",
            "virtual_label": "LUMO+1"
          },
          {
            "from_mo": 144,
            "to_mo": 151,
            "direction": "->",
            "amplitude": 0.14292,
            "occupied_label": "HOMO",
            "virtual_label": "LUMO+6"
          }
        ],
        "coefficient_list_complete": false
      }
    ],
    "new_compute_this_turn": false
  },
  {
    "id": "IR780_S1_electron_hole",
    "purpose": "比较实际电子/空穴分布与标记C/I/Se原子对贡献",
    "author_or_added": "author_electron_hole_with_disclosed_partition",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "IR780",
      "state": "S1",
      "charge": 1,
      "same_saved_TD_parent": true
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; official native Multiwfn Hirshfeld; Mulliken controls retained separately",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/S1/multiwfn.log",
        "sha256": "21da9b750ea1f1b940f469a3d2050a480aaa4dfbfa7d3c438166b5e553b3d3dd"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/cyanine_ir780_hirshfeld_definition.json",
        "sha256": "e9043d77bc9363b098af5871abe2f66d9aa14aa87bae1a32ac50dde7db4fbe3e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      }
    ],
    "job_id": null,
    "native_validity": {
      "native_rc": 0,
      "wall_seconds": 47.58762784861028,
      "all_atom_partition_verified": true,
      "same_saved_TD_coefficients_and_NTO_subspace": true
    },
    "actual_outputs": {
      "pair_hole_percent": 1.06,
      "pair_electron_percent": 1.91,
      "all_atom_hole_sum_percent": 100.0
    },
    "new_compute_this_turn": false
  },
  {
    "id": "IR780_T1_electron_hole",
    "purpose": "比较实际电子/空穴分布与标记C/I/Se原子对贡献",
    "author_or_added": "author_electron_hole_with_disclosed_partition",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "IR780",
      "state": "T1",
      "charge": 1,
      "same_saved_TD_parent": true
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; official native Multiwfn Hirshfeld; Mulliken controls retained separately",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/T1/multiwfn.log",
        "sha256": "68f563018c00879a897d2a2f7c028d8caa14c0b35a2d475ef2677eda44da8141"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/cyanine_ir780_hirshfeld_definition.json",
        "sha256": "e9043d77bc9363b098af5871abe2f66d9aa14aa87bae1a32ac50dde7db4fbe3e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      }
    ],
    "job_id": null,
    "native_validity": {
      "native_rc": 0,
      "wall_seconds": 36.36677531339228,
      "all_atom_partition_verified": true,
      "same_saved_TD_coefficients_and_NTO_subspace": true
    },
    "actual_outputs": {
      "pair_hole_percent": 0.9,
      "pair_electron_percent": 1.73,
      "all_atom_hole_sum_percent": 100.0
    },
    "new_compute_this_turn": false
  },
  {
    "id": "IR780_T2_electron_hole",
    "purpose": "比较实际电子/空穴分布与标记C/I/Se原子对贡献",
    "author_or_added": "author_electron_hole_with_disclosed_partition",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "IR780",
      "state": "T2",
      "charge": 1,
      "same_saved_TD_parent": true
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; official native Multiwfn Hirshfeld; Mulliken controls retained separately",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/T2/multiwfn.log",
        "sha256": "45671daac32c08f9c94433131c114117d5eb2f6c946c206f3cde0817c214edc2"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/cyanine_ir780_hirshfeld_definition.json",
        "sha256": "e9043d77bc9363b098af5871abe2f66d9aa14aa87bae1a32ac50dde7db4fbe3e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      }
    ],
    "job_id": null,
    "native_validity": {
      "native_rc": 0,
      "wall_seconds": 324.67569154594094,
      "all_atom_partition_verified": true,
      "same_saved_TD_coefficients_and_NTO_subspace": true
    },
    "actual_outputs": {
      "pair_hole_percent": 0.75,
      "pair_electron_percent": 1.72,
      "all_atom_hole_sum_percent": 100.0
    },
    "new_compute_this_turn": false
  },
  {
    "id": "Cy1_S1_electron_hole",
    "purpose": "比较实际电子/空穴分布与标记C/I/Se原子对贡献",
    "author_or_added": "author_electron_hole_with_disclosed_partition",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy1",
      "state": "S1",
      "charge": 1,
      "same_saved_TD_parent": true
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; official native Multiwfn Hirshfeld; Mulliken controls retained separately",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_S1/multiwfn.log",
        "sha256": "f95ca2d220a2d3eea25915c6299017fe8b8d8bfcd7829c8e72ab6ed5bafccd37"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json",
        "sha256": "6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      }
    ],
    "job_id": null,
    "native_validity": {
      "native_rc": 0,
      "wall_seconds": 59.970576585270464,
      "all_atom_partition_verified": true,
      "same_saved_TD_coefficients_and_NTO_subspace": true
    },
    "actual_outputs": {
      "pair_hole_percent": 3.65,
      "pair_electron_percent": 0.79,
      "all_atom_hole_sum_percent": 100.0
    },
    "new_compute_this_turn": false
  },
  {
    "id": "Cy1_T1_electron_hole",
    "purpose": "比较实际电子/空穴分布与标记C/I/Se原子对贡献",
    "author_or_added": "author_electron_hole_with_disclosed_partition",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy1",
      "state": "T1",
      "charge": 1,
      "same_saved_TD_parent": true
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; official native Multiwfn Hirshfeld; Mulliken controls retained separately",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T1/multiwfn.log",
        "sha256": "40c190918b2411ca6f2e8f4278cc2552555bd2a56e257d005af298dba4f17e07"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json",
        "sha256": "6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      }
    ],
    "job_id": null,
    "native_validity": {
      "native_rc": 0,
      "wall_seconds": 47.25334851350635,
      "all_atom_partition_verified": true,
      "same_saved_TD_coefficients_and_NTO_subspace": true
    },
    "actual_outputs": {
      "pair_hole_percent": 1.16,
      "pair_electron_percent": 0.52,
      "all_atom_hole_sum_percent": 100.0
    },
    "new_compute_this_turn": false
  },
  {
    "id": "Cy1_T2_electron_hole",
    "purpose": "比较实际电子/空穴分布与标记C/I/Se原子对贡献",
    "author_or_added": "author_electron_hole_with_disclosed_partition",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy1",
      "state": "T2",
      "charge": 1,
      "same_saved_TD_parent": true
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; official native Multiwfn Hirshfeld; Mulliken controls retained separately",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T2/multiwfn.log",
        "sha256": "5e2d900c55db82125aa92d5891aa7aa709c7e31d0b86a1b9ffdc11a3b8dd847a"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json",
        "sha256": "6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      }
    ],
    "job_id": null,
    "native_validity": {
      "native_rc": 0,
      "wall_seconds": 298.1126522636041,
      "all_atom_partition_verified": true,
      "same_saved_TD_coefficients_and_NTO_subspace": true
    },
    "actual_outputs": {
      "pair_hole_percent": 6.27,
      "pair_electron_percent": 0.58,
      "all_atom_hole_sum_percent": 100.0
    },
    "new_compute_this_turn": false
  },
  {
    "id": "Cy2_S1_electron_hole",
    "purpose": "比较实际电子/空穴分布与标记C/I/Se原子对贡献",
    "author_or_added": "author_electron_hole_with_disclosed_partition",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy2",
      "state": "S1",
      "charge": 1,
      "same_saved_TD_parent": true
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; official native Multiwfn Hirshfeld; Mulliken controls retained separately",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_S1/multiwfn.log",
        "sha256": "e70d9156efadca56331813bd8fc65d44a6821e12ba6c5d0e7949d100e2e4a9ff"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json",
        "sha256": "6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      }
    ],
    "job_id": null,
    "native_validity": {
      "native_rc": 0,
      "wall_seconds": 127.4079091977328,
      "all_atom_partition_verified": true,
      "same_saved_TD_coefficients_and_NTO_subspace": true
    },
    "actual_outputs": {
      "pair_hole_percent": 14.84,
      "pair_electron_percent": 9.72,
      "all_atom_hole_sum_percent": 100.0
    },
    "new_compute_this_turn": false
  },
  {
    "id": "Cy2_T1_electron_hole",
    "purpose": "比较实际电子/空穴分布与标记C/I/Se原子对贡献",
    "author_or_added": "author_electron_hole_with_disclosed_partition",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy2",
      "state": "T1",
      "charge": 1,
      "same_saved_TD_parent": true
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; official native Multiwfn Hirshfeld; Mulliken controls retained separately",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T1/multiwfn.log",
        "sha256": "6bbc10058ce9c7dd8a9936947b0a5402aa99e3c79f100702fdfb73f50aadef84"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json",
        "sha256": "6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      }
    ],
    "job_id": null,
    "native_validity": {
      "native_rc": 0,
      "wall_seconds": 121.29329410474747,
      "all_atom_partition_verified": true,
      "same_saved_TD_coefficients_and_NTO_subspace": true
    },
    "actual_outputs": {
      "pair_hole_percent": 10.62,
      "pair_electron_percent": 9.59,
      "all_atom_hole_sum_percent": 100.0
    },
    "new_compute_this_turn": false
  },
  {
    "id": "Cy2_T2_electron_hole",
    "purpose": "比较实际电子/空穴分布与标记C/I/Se原子对贡献",
    "author_or_added": "author_electron_hole_with_disclosed_partition",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy2",
      "state": "T2",
      "charge": 1,
      "same_saved_TD_parent": true
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; official native Multiwfn Hirshfeld; Mulliken controls retained separately",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T2/multiwfn.log",
        "sha256": "fc01cb4e8f130bd20ad8d7831340bbab19dd6160459cc0205b7cd14e44d5c212"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json",
        "sha256": "6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      }
    ],
    "job_id": null,
    "native_validity": {
      "native_rc": 0,
      "wall_seconds": 268.45571678876877,
      "all_atom_partition_verified": true,
      "same_saved_TD_coefficients_and_NTO_subspace": true
    },
    "actual_outputs": {
      "pair_hole_percent": 14.88,
      "pair_electron_percent": 9.22,
      "all_atom_hole_sum_percent": 100.0
    },
    "new_compute_this_turn": false
  },
  {
    "id": "four_species_adiabatic_energy_and_validity_chain",
    "purpose": "同介质/同定义供体与rubrene能量差及各端点轨道稳定性",
    "author_or_added": "author_UDFT_energy_plus_validity_checks",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": [
        "IR780",
        "Cy1",
        "Cy2",
        "rubrene"
      ],
      "eight_own_endpoints": true,
      "S0_multiplicity": 1,
      "T1_multiplicity": 3
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; separate electronic and ZPVE corrected differences; no duplicated thermal term",
    "required_for_current_question": true,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_stability_audit_v2_a01/cyanine_stability_audit.json",
        "sha256": "27eadb3b33595dc6f8ec159e9916cdd7850b170e0e64f709da38774a640d4056"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json",
        "sha256": "b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_stability_acceptance_v2_a01/returned_acceptance_audit.json",
        "sha256": "91ce7ff219d72928e622d1b00fe0913099f2d815c6173128602f499abfac5193"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
        "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/stdout.log",
        "sha256": "e6372b6e83ceec1d5611b00ece94f1b5d29b40b24af9cf56f23e4b1fb167bf9d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stdout.log",
        "sha256": "a725df344a7a14e2ce905d586596c3ba811e0ef4b12aec986aae76517bcc5922"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stdout.log",
        "sha256": "697801651802143cfd356d9e32ccd961dd6667c2c17c92ca6ac6c05c63d2f632"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/stdout.log",
        "sha256": "4cf08d554cbc5a64f0e1a4c216cdab6391135b6c19b1a0dbbb775d98d4f1a911"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stdout.log",
        "sha256": "8f83323030cbb6a393c37a160c299756094d0f4c032c707043b583798d790248"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/stdout.log",
        "sha256": "e340b8224da03cd15ab767448be846bc75d5916c81f78c4d423da0608b32e2f2"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stdout.log",
        "sha256": "5bb8b847767968b5bdc59eff4babb1cc3f489d9934a20f1b9bf3836d6be06f39"
      }
    ],
    "job_id": null,
    "native_validity": {
      "seven_new_endpoints_plus_validated_Cy2_S0": true,
      "own_Hessians": true,
      "fixed_endpoint_stability_checks": 7,
      "Cy2_S0_stability_separate": true
    },
    "actual_outputs": {
      "adiabatic_gaps": [
        {
          "species": "IR780",
          "electronic_adiabatic_T_minus_S_eV": 1.0199276552874235,
          "ZPVE_corrected_adiabatic_T_minus_S_eV": 0.9721716724274861,
          "source_UDFT_adiabatic_eV": 1.02,
          "source_ZPVE_definition_unresolved": true,
          "electronic_residual_eV": -7.234471257655528e-05,
          "ZPVE_residual_eV": -0.04782832757251387,
          "source_printing_half_unit_eV": 0.005,
          "source_reproducibility_tolerance_eV": null,
          "source_calibration_pass": false,
          "own_stable_curvature_endpoints": true,
          "S_job": "hpc-job-e764c3bf-b686-4c21-806a-74ad33931983",
          "T_job": "hpc-job-e387c7fa-cc31-440e-8b4f-c8448a9995eb"
        },
        {
          "species": "Cy1",
          "electronic_adiabatic_T_minus_S_eV": 1.0182587809722115,
          "ZPVE_corrected_adiabatic_T_minus_S_eV": 0.9681354075099713,
          "source_UDFT_adiabatic_eV": 1.02,
          "source_ZPVE_definition_unresolved": true,
          "electronic_residual_eV": -0.0017412190277885653,
          "ZPVE_residual_eV": -0.05186459249002873,
          "source_printing_half_unit_eV": 0.005,
          "source_reproducibility_tolerance_eV": null,
          "source_calibration_pass": false,
          "own_stable_curvature_endpoints": true,
          "S_job": "hpc-job-a5142e9b-9462-4ed4-86c2-b28f8b136240",
          "T_job": "hpc-job-0abda2ca-e4e9-48f9-95a8-a8705f49b203"
        },
        {
          "species": "Cy2",
          "electronic_adiabatic_T_minus_S_eV": 1.089739827248774,
          "ZPVE_corrected_adiabatic_T_minus_S_eV": 1.0366776240576594,
          "source_UDFT_adiabatic_eV": 1.09,
          "source_ZPVE_definition_unresolved": true,
          "electronic_residual_eV": -0.0002601727512261398,
          "ZPVE_residual_eV": -0.05332237594234068,
          "source_printing_half_unit_eV": 0.005,
          "source_reproducibility_tolerance_eV": null,
          "source_calibration_pass": false,
          "own_stable_curvature_endpoints": true,
          "S_job": "hpc-job-e0fb966e-263e-4d3d-905f-a912e40bb51f",
          "T_job": "hpc-job-a7f8fedf-870e-4b74-a59f-7de73ac73e26"
        },
        {
          "species": "rubrene",
          "electronic_adiabatic_T_minus_S_eV": 0.9967457311151309,
          "ZPVE_corrected_adiabatic_T_minus_S_eV": 0.9387038442512529,
          "source_UDFT_adiabatic_eV": 1.0,
          "source_ZPVE_definition_unresolved": true,
          "electronic_residual_eV": -0.003254268884869127,
          "ZPVE_residual_eV": -0.06129615574874714,
          "source_printing_half_unit_eV": 0.005,
          "source_reproducibility_tolerance_eV": null,
          "source_calibration_pass": false,
          "own_stable_curvature_endpoints": true,
          "S_job": "hpc-job-ed3a58da-eb99-4309-a504-795f50d32aa4",
          "T_job": "hpc-job-e9e83d8f-c6ee-4ebf-abdd-07a3dff8f070"
        }
      ],
      "paired_energy_definition_sensitivity": [
        {
          "species": "IR780",
          "electronic_donor_minus_rubrene_eV": 0.02318192417229259,
          "ZPVE_donor_minus_rubrene_eV": 0.03346782817623328,
          "paired_definition_shift_eV": 0.010285904003940693,
          "both_nonnegative": true,
          "source_electronic_definition": "Inferred from disclosed UDFT method and four-member series; not explicitly quoted.",
          "boundary": "Energetic compatibility only; no transfer or ISC rate follows."
        },
        {
          "species": "Cy1",
          "electronic_donor_minus_rubrene_eV": 0.02151304985708058,
          "ZPVE_donor_minus_rubrene_eV": 0.02943156325871843,
          "paired_definition_shift_eV": 0.00791851340163785,
          "both_nonnegative": true,
          "source_electronic_definition": "Inferred from disclosed UDFT method and four-member series; not explicitly quoted.",
          "boundary": "Energetic compatibility only; no transfer or ISC rate follows."
        },
        {
          "species": "Cy2",
          "electronic_donor_minus_rubrene_eV": 0.09299409613364307,
          "ZPVE_donor_minus_rubrene_eV": 0.09797377980640654,
          "paired_definition_shift_eV": 0.004979683672763469,
          "both_nonnegative": true,
          "source_electronic_definition": "Inferred from disclosed UDFT method and four-member series; not explicitly quoted.",
          "boundary": "Energetic compatibility only; no transfer or ISC rate follows."
        }
      ]
    },
    "new_compute_this_turn": false
  }
]
```


#### completed_added_validation（冻结记录 E0007）

```json
[
  {
    "id": "Cy1_full_XY_export_and_screening_integrity",
    "purpose": "修复已发现CI接口错误，认证完整数组/导出/官方筛选不同层",
    "author_or_added": "necessary_technical_repair",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy1",
      "states": [
        "S1",
        "T1",
        "T2"
      ],
      "geometries_representations": [
        "SI_fixed_canonical",
        "relaxed_response_NTO"
      ]
    },
    "method": "Original full RPA1e-6 unchanged; independent1e-4 X/Y export tail accounting, 12-place serialization bounds; native population screening",
    "required_for_current_question": false,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_ci_export_integrity_repair_20261007_a01/output/results.json",
        "sha256": "0e76645e3513e359b1d17cc5b66f7cff4b1f7f87c7ea72abea62d3d7162265fd"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/ci_export_proof.py",
        "sha256": "95962a72eea7c13a34edadb442b38ce7980e93390bc563725f507e5a4fea7842"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      }
    ],
    "job_id": "hpc-job-c7082240-f333-4746-9bb4-c98f9a3a23d5",
    "native_validity": {
      "six_states_complete": true,
      "failed_checks": [],
      "no_rescaling_or_threshold_relaxation": true
    },
    "actual_outputs": [
      {
        "tag": "Cy1_SI_fixed_canonical_S1",
        "full_RPA_norm": 0.9999999996739736,
        "export_RPA_norm": 1.000000466814729,
        "full_unscreened_hole_percent": 3.266137471042145,
        "export_unscreened_hole_percent": 3.2661427665497853,
        "official_screened_hole_percent": 3.337224578468223
      },
      {
        "tag": "Cy1_SI_fixed_canonical_T1",
        "full_RPA_norm": 0.9999999998230007,
        "export_RPA_norm": 0.9999999842710463,
        "full_unscreened_hole_percent": 0.9115417823029933,
        "export_unscreened_hole_percent": 0.9115442290789887,
        "official_screened_hole_percent": 1.016699848115639
      },
      {
        "tag": "Cy1_SI_fixed_canonical_T2",
        "full_RPA_norm": 0.9999999993921314,
        "export_RPA_norm": 0.9999997821442619,
        "full_unscreened_hole_percent": 5.792755887381536,
        "export_unscreened_hole_percent": 5.7927383494230025,
        "official_screened_hole_percent": 6.026536439678824
      },
      {
        "tag": "Cy1_relaxed_response_NTO_S1",
        "full_RPA_norm": 0.9999999996616704,
        "export_RPA_norm": 1.0000418878858777,
        "full_unscreened_hole_percent": 3.277558980729342,
        "export_unscreened_hole_percent": 3.2768932626302734,
        "official_screened_hole_percent": 3.2084661423222416
      },
      {
        "tag": "Cy1_relaxed_response_NTO_T1",
        "full_RPA_norm": 0.9999999994013942,
        "export_RPA_norm": 1.0000122960239595,
        "full_unscreened_hole_percent": 0.9165961519084878,
        "export_unscreened_hole_percent": 0.916530592152197,
        "official_screened_hole_percent": 0.9013901882845605
      },
      {
        "tag": "Cy1_relaxed_response_NTO_T2",
        "full_RPA_norm": 1.0000000000459113,
        "export_RPA_norm": 0.9999912653009125,
        "full_unscreened_hole_percent": 5.8356682576182966,
        "export_unscreened_hole_percent": 5.835578531943382,
        "official_screened_hole_percent": 5.78310061214444
      }
    ],
    "new_compute_this_turn": false
  },
  {
    "id": "Cy1_literal_SI_S0_response_and_population",
    "purpose": "已完成源字面坐标单一诊断，保持与松弛端点区别",
    "author_or_added": "added_validation",
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.12 explicitly vertical Table S3, pp.22–24/Figs.S14–S17, pp.30–43 S0/T1 coordinate blocks",
    "identity": {
      "species": "Cy1",
      "charge": 1,
      "reference_multiplicity": 1,
      "geometry": "literalSI S0"
    },
    "method": "Gaussian16 B3LYP/6-31G(d,p), SMD chloroform; I:SDD ECP, Se:all-electron def2TZVP; native5D/7F; iodide counterion excluded; fixed-coordinate vertical response, no optimization",
    "required_for_current_question": false,
    "status": "COMPLETE",
    "reused_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_response_20261006_a01/output/application_status.json",
        "sha256": "517c5a85ceff2a2675fddcc1834b0b59cb18995589e4232802c5cc8323b1595a"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/Cy1_fixed_source_comparison.json",
        "sha256": "fbb20c0fd2cf63ba2bf9eefd54674a8fe64786e4c28f753f214e6c90f03790b2"
      }
    ],
    "job_id": "hpc-job-cce25d25-3c92-404f-9f48-12c8a191d93e",
    "native_validity": {
      "native_response_rc": 0,
      "six_singlet_six_triplet_roots": true,
      "native_population_rc": 0
    },
    "actual_outputs": null,
    "new_compute_this_turn": false
  }
]
```


#### reused_results（冻结记录 E0007）

```json
[
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/stdout.log",
    "sha256": "81ea7772ffcb1a07d0b4ba934ab717a0b397589c0c42eeab72fe3bee0bbd8fa1"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/input.com",
    "sha256": "04cdd3fc0dcaee588b7a98e02e92bd4ed4c2962af99809b7b3e148f931d9c67e"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json",
    "sha256": "b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/stdout.log",
    "sha256": "eb189981e13afdf94b3edde3a6521cbd283169793b37532decdfe7c26557399c"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/input.com",
    "sha256": "73164984762d082db2cc2164a8dfcd861dc3d3ba5c06193e46bdb614923c3cb1"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/stdout.log",
    "sha256": "d8948b9025aef77ca59cc577cf79033a7bf190a8976b6a6e10512ba9831e34eb"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/input.com",
    "sha256": "44720be0dadb92c0fc950d20ac5148f1cd08c42f72459da8c96c24b47a00d75f"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/stdout.log",
    "sha256": "3a0a2fb4cd6a470f885015dea02c75e4905dd0d8eacd221764eda8fc56f467ce"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/input.com",
    "sha256": "21be808f1ed902616333d4124452449af62d48859b97447e507ba0eeab640f6f"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/stdout.log",
    "sha256": "82569e6406285efb534eb66a2bd0ce35f41b5215bdaaead543ee192f73ecae84"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/input.com",
    "sha256": "06bcb1e4ace63034a1663ab8695c7b019c2cc590d3945c686ae15eaf16d7ee2b"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/stdout.log",
    "sha256": "fbc3136f51dc2c92c9dc838e43453860ce446eaf7b9f833c62c28027942f9e6c"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/input.com",
    "sha256": "385d3add4e1036fb3491557549b3ea584bfe132c8ead5dbb6faf1e954542dfe3"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/stdout.log",
    "sha256": "a6154333d63a2123590305e002414971b80c78fdb9c89172fda65cea327456de"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/input.com",
    "sha256": "0d02360e455f1135a0c46cf6c7a2b7d12a7bf9d5b8a12372a05801025e1408f6"
  },
  {
    "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stdout.log",
    "sha256": "d789107d6428836a2032ff8f198a1a48e32a1d33285778cbe7095ca2c39ae1be"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_native_reuse_audit_v2_a01/cy2_native_reuse_audit.json",
    "sha256": "51911a8a01d092f00f6195dad36ebf8675dc62e5912f3440e4db3532bc4fc793"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/stdout.log",
    "sha256": "6d10ea193a4871fc13b657a5db5cb476b1f22c012e5b60ff6a3df32a95eb8c54"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/input.com",
    "sha256": "de7cfc12bd0be1c7a69d7dd7b9c6ae4f706de917d34c236bc07aa8bfe8bd5e69"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
    "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/stdout.log",
    "sha256": "960dbe5343d4613d879833fe8493aa38395c4e6eee040430e0c338ee95e15f23"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/input.com",
    "sha256": "ee6c1d95717c91ba676d0eccc1132990639e6f223a48706fa8cedba6259926e8"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/stdout.log",
    "sha256": "e0c71b0adfa09fd0b6ab54e0cc603c6504cd15d35f8332c68bcd32aca8c588b8"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/input.com",
    "sha256": "22c548e81e94dab7ae4b641c27c571dbab6d04e3417c6bb73686b1491437f69f"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/stdout.log",
    "sha256": "ca88b415f17f996ceed76748fa62304eec85a4a97bfe028b554d37d6a618bd70"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/input.com",
    "sha256": "012fa1e19d74db54756de8975aecbad9b0797020cc759c9685ad42b94211bff4"
  },
  {
    "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stdout.log",
    "sha256": "3d11a8885822bfee61357107296ff4ec090ad3e9000243a959a237023aba20d2"
  },
  {
    "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/input.com",
    "sha256": "7b5fadeceea4b5b6039b2de7c040e192efc779f15c5309c8e691bab47833b8d2"
  },
  {
    "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stdout.log",
    "sha256": "d255edb8b66d87556d3ccf100a14c3afaa92bee5d421f03a4d035261d2e6ff1c"
  },
  {
    "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/input.com",
    "sha256": "790932d90471c3924bfbeb845ac5fbd951e79f762eb2a8920c1039bfd0e824e6"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/S1/multiwfn.log",
    "sha256": "21da9b750ea1f1b940f469a3d2050a480aaa4dfbfa7d3c438166b5e553b3d3dd"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/cyanine_ir780_hirshfeld_definition.json",
    "sha256": "e9043d77bc9363b098af5871abe2f66d9aa14aa87bae1a32ac50dde7db4fbe3e"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
    "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/T1/multiwfn.log",
    "sha256": "68f563018c00879a897d2a2f7c028d8caa14c0b35a2d475ef2677eda44da8141"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/T2/multiwfn.log",
    "sha256": "45671daac32c08f9c94433131c114117d5eb2f6c946c206f3cde0817c214edc2"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_S1/multiwfn.log",
    "sha256": "f95ca2d220a2d3eea25915c6299017fe8b8d8bfcd7829c8e72ab6ed5bafccd37"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json",
    "sha256": "6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T1/multiwfn.log",
    "sha256": "40c190918b2411ca6f2e8f4278cc2552555bd2a56e257d005af298dba4f17e07"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T2/multiwfn.log",
    "sha256": "5e2d900c55db82125aa92d5891aa7aa709c7e31d0b86a1b9ffdc11a3b8dd847a"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_S1/multiwfn.log",
    "sha256": "e70d9156efadca56331813bd8fc65d44a6821e12ba6c5d0e7949d100e2e4a9ff"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T1/multiwfn.log",
    "sha256": "6bbc10058ce9c7dd8a9936947b0a5402aa99e3c79f100702fdfb73f50aadef84"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T2/multiwfn.log",
    "sha256": "fc01cb4e8f130bd20ad8d7831340bbab19dd6160459cc0205b7cd14e44d5c212"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_stability_audit_v2_a01/cyanine_stability_audit.json",
    "sha256": "27eadb3b33595dc6f8ec159e9916cdd7850b170e0e64f709da38774a640d4056"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_stability_acceptance_v2_a01/returned_acceptance_audit.json",
    "sha256": "91ce7ff219d72928e622d1b00fe0913099f2d815c6173128602f499abfac5193"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/stdout.log",
    "sha256": "e6372b6e83ceec1d5611b00ece94f1b5d29b40b24af9cf56f23e4b1fb167bf9d"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stdout.log",
    "sha256": "a725df344a7a14e2ce905d586596c3ba811e0ef4b12aec986aae76517bcc5922"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stdout.log",
    "sha256": "697801651802143cfd356d9e32ccd961dd6667c2c17c92ca6ac6c05c63d2f632"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/stdout.log",
    "sha256": "4cf08d554cbc5a64f0e1a4c216cdab6391135b6c19b1a0dbbb775d98d4f1a911"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stdout.log",
    "sha256": "8f83323030cbb6a393c37a160c299756094d0f4c032c707043b583798d790248"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/stdout.log",
    "sha256": "e340b8224da03cd15ab767448be846bc75d5916c81f78c4d423da0608b32e2f2"
  },
  {
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stdout.log",
    "sha256": "5bb8b847767968b5bdc59eff4babb1cc3f489d9934a20f1b9bf3836d6be06f39"
  },
  {
    "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_ci_export_integrity_repair_20261007_a01/output/results.json",
    "sha256": "0e76645e3513e359b1d17cc5b66f7cff4b1f7f87c7ea72abea62d3d7162265fd"
  },
  {
    "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/ci_export_proof.py",
    "sha256": "95962a72eea7c13a34edadb442b38ce7980e93390bc563725f507e5a4fea7842"
  },
  {
    "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_response_20261006_a01/output/application_status.json",
    "sha256": "517c5a85ceff2a2675fddcc1834b0b59cb18995589e4232802c5cc8323b1595a"
  },
  {
    "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/Cy1_fixed_source_comparison.json",
    "sha256": "fbb20c0fd2cf63ba2bf9eefd54674a8fe64786e4c28f753f214e6c90f03790b2"
  }
]
```


#### protocol_variations（冻结记录 E0007）

```json
[
  "采用源披露的Gaussian16/B3LYP/SMD氯仿与I/Se基组；供体+1、rubrene中性；反离子排除。",
  "Main p6明确UDFT绝热T1。旧Cy2 TD优化triplet端点单独标记，不能充当UDFT；新的UDFT各端点已完成。",
  "源未明言电子绝热值是否含ZPVE，两套同定义四物种结果均保留；未知热项约定不是欠算。",
  "源人口分区未唯一指定；官方Mulliken/Hirshfeld均已处理，精确百分数比较仍需保留定义限定。"
]
```


#### considered_but_not_required（冻结记录 E0007）

```json
[
  "SI p8泛列S1/T1/T2几何优化；当前复现量Table S3明确是垂直激发，Fig3b/c与SI FigS14明确S0→S1/T1/T2且FigS15标S0。故不把每个S1/T2松弛端点加入当前必要矩阵；不冒称这些优化已做。能量转移节点需要的松弛三重端点已按Main p6 UDFT全部完成。",
  "当前只判断triplet donor/acceptor能量相容性和分子证据边界；不声称TTA反应速率、rubrene发光速率或自选完整动力学矩阵。",
  "Cy3/IR806及源实验薄膜效率不在当前三敏化剂任务对象内；没有将它们当遗漏的量化。"
]
```

## 3. 论文结果、实际结果与合理误差依据

本轮重算绝热T1=1.0199277/1.0182588/1.0897398/0.9967457 eV，对源1.02/1.02/1.09/1.00；Cy1源几何S1/T2差-0.0112/-0.0196 eV，I-T2空穴6.026536%对5.52%。

电子绝热T1实算[1.01993,1.01826,1.08974,0.99675] eV，对源[1.02,1.02,1.09,1.00]吻合；Cy1固定源S1/T2差−0.0112/−0.0196eV，I-T2空穴6.026536%对源5.52%。

## 4. 每个中间关键点与最终结论

ID 和要求直接取自本模式冻结 evaluator；逐项结果保留当前复审与已有原生证据。归档中仅有计划、失败或候选标签的内容不因此成为新的成功计算。

### kp_scope — Identity and scope

冻结要求：Declare state identity, geometry and energy reference for each excited-state quantity. For an energy-transfer claim, use compatible donor/acceptor definitions and state the sign of the driving energy. Explain heavy-element treatment and whether the evidence concerns a coupling, a transition probability or a kinetic rate.

当前复审：24项计算及主要态身份/Se>I参与已完成。不同实际人口定义均保留关键效应，为当前有限电子解释提供实证；不以某个未绑定作者百分比冒充精确复现。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

三个完整+1敏化剂和中性rubrene、反离子排除、SMD氯仿、I-SDD/Se-def2TZVP及电子/自旋库存有原生绑定；S0、垂直TD和UDFT绝热T1定义分开。

证据记录：`E0008`。

```json
[
  {
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.11 Tables S1/S2, p.12 Table S3, p.23 Fig.S16, pp.30–45 coordinates",
    "reason": "敏化剂+1/反离子排除，rubrene中性，SMD氯仿及I-SDD/Se-def2TZVP一致。八个端点各自正曲率/稳定性和原Opt完成已核，旧Cy2TD triplet与UDFT明确分开。"
  }
]
```


证据记录：`E0110`。

```json
[
  {
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.11 Tables S1/S2, p.12 Table S3, p.23 Fig.S16, pp.30–45 coordinates",
    "actual_result": "三个敏化剂+1、rubrene中性；反离子排除，SMD氯仿，I为SDD ECP、Se为全电子def2TZVP。S0垂直TD、UDFT绝热差、ZPVE差及实验量分别标记。八个端点各自曲率/态有证据；没有挪用旧Cy2 TD优化三重态作为UDFT最低点。",
    "reason": "七个新端点与已核Cy2S0共同闭合四物种S/T链；原Opt完成与Freq后预测位移NO分开。自旋污染、正曲率和轨道稳定性共同支持已述局部态。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "81ea7772ffcb1a07d0b4ba934ab717a0b397589c0c42eeab72fe3bee0bbd8fa1"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/stdout.log",
        "sha256": "eb189981e13afdf94b3edde3a6521cbd283169793b37532decdfe7c26557399c"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "d8948b9025aef77ca59cc577cf79033a7bf190a8976b6a6e10512ba9831e34eb"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/stdout.log",
        "sha256": "3a0a2fb4cd6a470f885015dea02c75e4905dd0d8eacd221764eda8fc56f467ce"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "82569e6406285efb534eb66a2bd0ce35f41b5215bdaaead543ee192f73ecae84"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/stdout.log",
        "sha256": "fbc3136f51dc2c92c9dc838e43453860ce446eaf7b9f833c62c28027942f9e6c"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "a6154333d63a2123590305e002414971b80c78fdb9c89172fda65cea327456de"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stdout.log",
        "sha256": "d789107d6428836a2032ff8f198a1a48e32a1d33285778cbe7095ca2c39ae1be"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json",
        "sha256": "b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_stability_audit_v2_a01/cyanine_stability_audit.json",
        "sha256": "27eadb3b33595dc6f8ec159e9916cdd7850b170e0e64f709da38774a640d4056"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

### kp_measure — Quantitative scientific results

冻结要求：Construct a quantitative molecular interpretation of the sensitizer differences using correctly identified states and evidence suited to the proposed explanation. Alternative valid characterization routes are accepted; source T2 or a fixed SOC matrix is not a required answer.

当前复审：24项计算及主要态身份/Se>I参与已完成。不同实际人口定义均保留关键效应，为当前有限电子解释提供实证；不以某个未绑定作者百分比冒充精确复现。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

24项必需计算已完成；四物种电子绝热T1=1.01993/1.01826/1.08974/0.99675eV，源1.02/1.02/1.09/1.00；各垂直态、ZPVE版本及电子-空穴结果均实际保存。

证据记录：`E0008`。

```json
[
  {
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.11 Tables S1/S2, p.12 Table S3, p.23 Fig.S16, pp.30–45 coordinates",
    "reason": "Cy2及IR780很多量接近，Cy1 literalSI坐标仍有E/f及多态I人口残差。仅canonicalS1 3.3372246%对3.34%不能替代T1/T2和松弛表示。"
  }
]
```


证据记录：`E0110`。

```json
[
  {
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.11 Tables S1/S2, p.12 Table S3, p.23 Fig.S16, pp.30–45 coordinates",
    "actual_result": "六组原生响应覆盖三物种S/T；垂直能量和f保持明确定义。Se空穴份额为约10.6–14.9%，明显超过I约1.2–6.3%及C约0.8–1.1%。Cy1固定源坐标S1/T1/T2为1.9040/0.9435/2.0995eV，f=2.6091，未替代松弛端点。",
    "reason": "使用同一人口定义作跨分子比较；没有挑选最接近源值的几何、根或表示。完整X/Y与原生波函数链接可重放。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/stdout.log",
        "sha256": "6d10ea193a4871fc13b657a5db5cb476b1f22c012e5b60ff6a3df32a95eb8c54"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/input.com",
        "sha256": "de7cfc12bd0be1c7a69d7dd7b9c6ae4f706de917d34c236bc07aa8bfe8bd5e69"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/stdout.log",
        "sha256": "960dbe5343d4613d879833fe8493aa38395c4e6eee040430e0c338ee95e15f23"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/input.com",
        "sha256": "ee6c1d95717c91ba676d0eccc1132990639e6f223a48706fa8cedba6259926e8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/stdout.log",
        "sha256": "e0c71b0adfa09fd0b6ab54e0cc603c6504cd15d35f8332c68bcd32aca8c588b8"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/input.com",
        "sha256": "22c548e81e94dab7ae4b641c27c571dbab6d04e3417c6bb73686b1491437f69f"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/stdout.log",
        "sha256": "ca88b415f17f996ceed76748fa62304eec85a4a97bfe028b554d37d6a618bd70"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/input.com",
        "sha256": "012fa1e19d74db54756de8975aecbad9b0797020cc759c9685ad42b94211bff4"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stdout.log",
        "sha256": "3d11a8885822bfee61357107296ff4ec090ad3e9000243a959a237023aba20d2"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/input.com",
        "sha256": "7b5fadeceea4b5b6039b2de7c040e192efc779f15c5309c8e691bab47833b8d2"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stdout.log",
        "sha256": "d255edb8b66d87556d3ccf100a14c3afaa92bee5d421f03a4d035261d2e6ff1c"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/input.com",
        "sha256": "790932d90471c3924bfbeb845ac5fbd951e79f762eb2a8920c1039bfd0e824e6"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
        "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_ci_export_integrity_repair_20261007_a01/output/results.json",
        "sha256": "0e76645e3513e359b1d17cc5b66f7cff4b1f7f87c7ea72abea62d3d7162265fd"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/cyanine_ir780_hirshfeld_definition.json",
        "sha256": "e9043d77bc9363b098af5871abe2f66d9aa14aa87bae1a32ac50dde7db4fbe3e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json",
        "sha256": "6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/cyanine_screening_control.json",
        "sha256": "5853d2500b06f49a43ed01fddaba7f9b6baf656fd848a643e66d3a971ad13412"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

### kp_explain — Evidence that distinguishes the claimed explanation

冻结要求：Assess rubrene energetic compatibility with coherent energy definitions, medium and structural reference. Distinguish vertical state separation, relaxed excitation energy and free-energy driving force as appropriate to the claim.

当前复审：24项计算及主要态身份/Se>I参与已完成。不同实际人口定义均保留关键效应，为当前有限电子解释提供实证；不以某个未绑定作者百分比冒充精确复现。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

修复后的完整X/Y、RPA范数与Mulliken/Hirshfeld控制保持主态身份及Se相对I显著更强参与；同方法同溶剂rubrene比较支持有限能量相容性。不能由此证明唯一ISC通道、SOC速率或实际转移效率。

证据记录：`E0008`。

```json
[
  {
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.11 Tables S1/S2, p.12 Table S3, p.23 Fig.S16, pp.30–45 coordinates",
    "reason": "四物种UDFT电子绝热值已按同一路线复现到源给出的有效位，配对ZPVE控制也支持方法内相容性。"
  }
]
```


证据记录：`E0110`。

```json
[
  {
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.11 Tables S1/S2, p.12 Table S3, p.23 Fig.S16, pp.30–45 coordinates",
    "actual_result": "电子绝热T1(IR780,Cy1,Cy2,rubrene)=1.0199276553/1.0182587810/1.0897398272/0.9967457311eV；供体减受体为正，配对ZPVE控制也为正。",
    "reason": "相同溶剂和各自最低点的同类电子能比较直接覆盖rubrene节点；不用垂直能与绝热值混减，不重复热项。近阈值支持方法内相容性，未证明自由能或动力学。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "81ea7772ffcb1a07d0b4ba934ab717a0b397589c0c42eeab72fe3bee0bbd8fa1"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/stdout.log",
        "sha256": "eb189981e13afdf94b3edde3a6521cbd283169793b37532decdfe7c26557399c"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "d8948b9025aef77ca59cc577cf79033a7bf190a8976b6a6e10512ba9831e34eb"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/stdout.log",
        "sha256": "3a0a2fb4cd6a470f885015dea02c75e4905dd0d8eacd221764eda8fc56f467ce"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "82569e6406285efb534eb66a2bd0ce35f41b5215bdaaead543ee192f73ecae84"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/stdout.log",
        "sha256": "fbc3136f51dc2c92c9dc838e43453860ce446eaf7b9f833c62c28027942f9e6c"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/stdout.log",
        "sha256": "a6154333d63a2123590305e002414971b80c78fdb9c89172fda65cea327456de"
      },
      {
        "path": "docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stdout.log",
        "sha256": "d789107d6428836a2032ff8f198a1a48e32a1d33285778cbe7095ca2c39ae1be"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_stability_audit_v2_a01/cyanine_stability_audit.json",
        "sha256": "27eadb3b33595dc6f8ec159e9916cdd7850b170e0e64f709da38774a640d4056"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
        "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

### kp_robust — Uncertainty and limits

冻结要求：Evaluate the uncertainty and confounding that govern the mechanism and energy-matching conclusions, especially unequal molecular scaffolds and heavy-element response. A bounded, evidenced non-resolution is acceptable without inventing a unique pathway.

当前复审：24项计算及主要态身份/Se>I参与已完成。不同实际人口定义均保留关键效应，为当前有限电子解释提供实证；不以某个未绑定作者百分比冒充精确复现。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

原Opt有效性、正曲率与Freq预测位移分开；源人口分区/归一化未唯一恢复，已算多定义支持核心结论。沿用用户接受的约0.01–0.02eV和I空穴约0.51百分点差；近阈值约+0.02eV余量不能外推为跨方法稳健放能。

证据记录：`E0008`。

```json
[
  {
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.11 Tables S1/S2, p.12 Table S3, p.23 Fig.S16, pp.30–45 coordinates",
    "reason": "c7082240六态保留fullRPA1e-6门，完整/导出/官方筛选三层已证。旧adf78断言失败是截断Y尾项问题，现已修复，不再作为当前阻碍。不同表示/分区没有共同消除所有I残差。"
  }
]
```


证据记录：`E0110`。

```json
[
  {
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.11 Tables S1/S2, p.12 Table S3, p.23 Fig.S16, pp.30–45 coordinates",
    "actual_result": "六态full RPA范数均过原1e-6门。旧失败的relaxed/NTO S1全范数0.9999999996616704；独立截断丢弃Y权重4.188822397e-5而X约2.304e-18，故导出范数1.0000418878858777合理。尾权重恒等残差2.327e-13落在序列化/浮点误差界内。源坐标canonical S1官方筛选后I空穴3.3372246%，T1/T2仍为1.01670/6.02654%。",
    "reason": "未改大阈值、未重标幅度；RPA度规、导出尾项和人口归一化分开。人口控制证实Se排序，不能把精确I残差隐藏；骨架、热项和窄能量裕量限制机制推断。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_ci_export_integrity_repair_20261007_a01/output/results.json",
        "sha256": "0e76645e3513e359b1d17cc5b66f7cff4b1f7f87c7ea72abea62d3d7162265fd"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json",
        "sha256": "4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/ci_export_proof.py",
        "sha256": "95962a72eea7c13a34edadb442b38ce7980e93390bc563725f507e5a4fea7842"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/METHOD_FINDINGS.json",
        "sha256": "5c41ce954d4163cddb8cf4731cf2dda40a41e2dcfe5504c63f2e9f057742689d"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/cyanine_ir780_hirshfeld_definition.json",
        "sha256": "e9043d77bc9363b098af5871abe2f66d9aa14aa87bae1a32ac50dde7db4fbe3e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json",
        "sha256": "6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/cyanine_screening_control.json",
        "sha256": "5853d2500b06f49a43ed01fddaba7f9b6baf656fd848a643e66d3a971ad13412"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

### con_answer — What molecular electronic evidence can explain differences in triplet sensitization among IR780, Cy1 and Cy2, and does it support their energetic compatibility with rubrene in chloroform?

冻结要求：Explain or delimit the molecular sensitization differences and rubrene compatibility with auditable quantitative evidence. Valid refutation or alternative mechanisms receive credit; reproducing a source triplet energy or claiming Se causes a higher rate from Z alone is insufficient.

当前复审：24项计算及主要态身份/Se>I参与已完成。不同实际人口定义均保留关键效应，为当前有限电子解释提供实证；不以某个未绑定作者百分比冒充精确复现。

此前已执行证据的详细展开（数值与原始记录保留；当前验收类型以上文为准）：

当前验收：在明确的科学范围和下述限制内已有实际证据。

三敏化剂的实际态/人口证据与四物种同定义UDFT端点链支持当前分子电子解释和有条件能量相容性，符合2026-10-11统一裁决。未认证每个源精确百分比、ISC/SOC速率或上转换效率。

证据记录：`E0008`。

```json
[
  {
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.11 Tables S1/S2, p.12 Table S3, p.23 Fig.S16, pp.30–45 coordinates",
    "reason": "计算完整，能量相容性子结论有实证，敏化剂排序的有限解释也成立；但所有当前必要分子态结果的严格源比较没有共同闭合。"
  }
]
```


证据记录：`E0110`。

```json
[
  {
    "source_locator": "Main pp.4–6/Fig.3; SI pp.7–8 methods, p.11 Tables S1/S2, p.12 Table S3, p.23 Fig.S16, pp.30–45 coordinates",
    "actual_result": "按作者B3LYP/SMD氯仿、I-SDD与Se-def2TZVP路线，IR780/Cy1/Cy2的S1为1.9389/1.9038/1.8909 eV，T1为0.9499/0.9427/1.0555 eV，T2为2.1355/2.1011/2.1220 eV。Cy2的S1最低、T2−S1却最大，因此小能隙本身不能解释其较快的实验ISC。相同Hirshfeld定义下，所标记原子对的S1/T1/T2空穴贡献分别为IR780 1.06/0.90/0.75%、Cy1 3.65/1.16/6.27%、Cy2 14.84/10.62/14.88%；Se参与显著更大且Mulliken控制保持该排序。这是重元素参与的分子证据，不是SOC矩阵或速率；三种骨架不完全相同，不能归因于单一原子替换。分别优化的单重/非限制三重最低点给出电子绝热T1能量1.01993/1.01826/1.08974 eV，rubrene为0.99675 eV，对应供体减受体+0.02318/+0.02151/+0.09299 eV；一致加入各自ZPVE后仍为+0.03347/+0.02943/+0.09797 eV。故支持该方法和溶剂内的近阈值能量相容性；未证明真实转移自由能或速率，特别IR780/Cy1的约0.02eV裕量不可当作跨方法可靠的放能保证。",
    "reason": "作者路线的三敏化剂垂直态、Se参与排序以及四物种同定义UDFT能量链已完整。电子绝热结果与源值最大差约0.0033 eV，没有为通过而扩大阈值；相同定义的供受体能量符号及Cy2较大裕量在已算ZPVE控制中保留。正文未明确是否加ZPVE，电子定义是公开方法和四物种结果支持的解释而非作者明言，因此两套结果并列。Cy1垂直谱残差最高约0.018eV、各态精确I贡献残差仍存在；它们不反转Se贡献远大于C/I及Cy2较大T2−S1间隔的核心判别。候选不声称所有人口数字、ISC率或真实能量转移速率复现；当前关键点允许且要求这种量化的因果边界。",
    "raw_evidence": [
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json",
        "sha256": "f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_stability_audit_v2_a01/cyanine_stability_audit.json",
        "sha256": "27eadb3b33595dc6f8ec159e9916cdd7850b170e0e64f709da38774a640d4056"
      },
      {
        "path": "docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_ci_export_integrity_repair_20261007_a01/output/results.json",
        "sha256": "0e76645e3513e359b1d17cc5b66f7cff4b1f7f87c7ea72abea62d3d7162265fd"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/cyanine_ir780_hirshfeld_definition.json",
        "sha256": "e9043d77bc9363b098af5871abe2f66d9aa14aa87bae1a32ac50dde7db4fbe3e"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json",
        "sha256": "6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031"
      },
      {
        "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/cyanine_screening_control.json",
        "sha256": "5853d2500b06f49a43ed01fddaba7f9b6baf656fd848a643e66d3a971ad13412"
      }
    ]
  }
]
```


涉及源辅助量与本题必要量的判定采用第 1 节最终裁决；以上旧记录不被解读为所有源输出均精确重现。

## 5. 实际计算时长与资源

已有逐日志核验的时长摘要：**正常结束阶段累计 12.26 小时；24 份计时日志/33 个计时段；部分覆盖**。

已记录资源：Gaussian 16 C.01；原生设置 20 线程/进程；Gaussian %Mem=24GB,80GB；回执请求 20 CPU/100 GiB。

CPU/内存为原生设置或明确提交请求，不是峰值实测用量；历史配置原样保留。CPU 时间与 elapsed 不相加，并行任务累计不能解释为日历时间。全流程壁钟、排队、未记录阶段与峰值内存均**未知**；未知不记为 0。

[逐原生日志计时机器记录](../../../../docs/v2_verification/history/v2_strict_update_20261013/RUNTIME_RESOURCE_LEDGER.json)。

| 原生记录／阶段 | 已记录 elapsed 秒 | 终止与计数说明 | CPU线程／内存设置 |
|---|---|---|---|
| [E0033 · outputs/cy2_source_udft_t_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/stdout.log) | Gaussian:1302.3；Gaussian:1025.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0034 · outputs/ir780_source_s0_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/stdout.log) | Gaussian:1340.3；Gaussian:1102.4 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0035 · outputs/ir780_source_udft_t_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/stdout.log) | Gaussian:1995.6；Gaussian:1864.6 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0036 · outputs/cy1_source_s0_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/stdout.log) | Gaussian:1576.1；Gaussian:1236.2 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0037 · outputs/cy1_source_udft_t_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/stdout.log) | Gaussian:2788.8；Gaussian:2281.8 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0038 · outputs/rubrene_source_s0_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/stdout.log) | Gaussian:2384.7；Gaussian:1316.5 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0039 · outputs/rubrene_source_udft_t_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/stdout.log) | Gaussian:3868.2；Gaussian:2343.1 | 正常；正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0040 · local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stdout.log) | Gaussian:1396；Gaussian:1166.9 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0041 · outputs/ir780_s0_singlet6_strict_v1_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/stdout.log) | Gaussian:260.4 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0042 · outputs/ir780_s0_triplet6_strict_v1_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/stdout.log) | Gaussian:296.2 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0043 · outputs/cy1_s0_singlet6_strict_v1_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/stdout.log) | Gaussian:243.4 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0044 · outputs/cy1_s0_triplet6_strict_v1_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/stdout.log) | Gaussian:364.3 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0045 · local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stdout.log) | Gaussian:447.5 | 正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0046 · local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stdout.log) | Gaussian:429.3 | 正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0047 · outputs/cy1_source_s0_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/stdout.log) | Gaussian:210.9 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0048 · outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stdout.log) | Gaussian:313.1 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0049 · outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stdout.log) | Gaussian:197.6 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0050 · outputs/ir780_source_s0_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/stdout.log) | Gaussian:217.5 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0051 · outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stdout.log) | Gaussian:298.3 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0052 · outputs/rubrene_source_s0_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/stdout.log) | Gaussian:278 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0053 · outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stdout.log) | Gaussian:409.3 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0092 · cyanine_ir780_hirshfeld_definition_20261002_a01/S1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/S1/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0095 · cyanine_ir780_hirshfeld_definition_20261002_a01/T1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/T1/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0096 · cyanine_ir780_hirshfeld_definition_20261002_a01/T2/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/T2/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0097 · cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_S1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_S1/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0099 · cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T1/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0100 · cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T2/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T2/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0101 · cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_S1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_S1/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0102 · cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T1/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0103 · cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T2/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T2/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0173 · local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/stdout.log) | Gaussian:5835.9；Gaussian:4883.3 | 正常；正常 | {"threads":[20],"Gaussian_mem":["24GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0321 · outputs/cy1_source_s0_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/stderr.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0328 · outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0335 · outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0341 · outputs/ir780_source_s0_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0348 · outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0355 · outputs/rubrene_source_s0_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0362 · outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0364 · outputs/cy2_source_s0_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/stdout.log) | Gaussian:146.7 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0366 · outputs/cy2_source_s0_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0371 · outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/stdout.log) | Gaussian:297.4 | 正常 | {"threads":[20],"Gaussian_mem":["80GB"],"ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0373 · outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/stderr.log) | 未知 | 无独立计时；此日志为同内容副本，已从累计排除 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0386 · output/S1/Mulliken.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/Mulliken.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0393 · output/T1/Mulliken.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/Mulliken.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0398 · output/T2/Mulliken.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/Mulliken.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0400 · cyanine_fragment_range_repair_20261002_a01/Cy1_S1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0403 · cyanine_fragment_range_repair_20261002_a01/Cy1_T1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |
| [E0406 · cyanine_fragment_range_repair_20261002_a01/Cy1_T2/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/multiwfn.log) | 未知 | 无独立计时 | {"threads":"未知","Gaussian_mem":"未知","ORCA_MaxCore_MB_per_process":"不适用/未知"} |

提交请求的记录（与原生软件设置分开）：
```json
[
  {
    "evidence_id": "E0318",
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/dispatch/submission_receipt.json",
    "requested": {
      "cpu": 20,
      "memory_gib": 100,
      "priority": 3
    }
  },
  {
    "evidence_id": "E0324",
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json",
    "requested": {
      "cpu": 20,
      "memory_gib": 100,
      "priority": 3
    }
  },
  {
    "evidence_id": "E0331",
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json",
    "requested": {
      "cpu": 20,
      "memory_gib": 100,
      "priority": 3
    }
  },
  {
    "evidence_id": "E0338",
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/dispatch/submission_receipt.json",
    "requested": {
      "cpu": 20,
      "memory_gib": 100,
      "priority": 3
    }
  },
  {
    "evidence_id": "E0344",
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json",
    "requested": {
      "cpu": 20,
      "memory_gib": 100,
      "priority": 3
    }
  },
  {
    "evidence_id": "E0351",
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/dispatch/submission_receipt.json",
    "requested": {
      "cpu": 20,
      "memory_gib": 100,
      "priority": 3
    }
  },
  {
    "evidence_id": "E0358",
    "path": "docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json",
    "requested": {
      "cpu": 20,
      "memory_gib": 100,
      "priority": 3
    }
  }
]
```

## 6. 已知偏差、失败分支和不能外推的结论

作者人口分区和跃迁百分比定义未唯一恢复；没有SOC矩阵或ISC速率，约0.02 eV近阈值余量不能泛化成跨方法保证放能。

24计算项完成，不是欠一个未投作业；不要求额外SOC矩阵。原Opt已完成且正曲率；个别Freq预测位移NO不能改写为原Opt失败。电子/ZPVE两套都已算。


```json
{
  "paper_id": "paper_e0791c047a731974",
  "initial_recommendation": "NOT_YET_STRICT_PROTOCOL_OR_EVIDENCE",
  "final_status": "STRICT_PASS",
  "basis": "24个计算项完成；四物种UDFT绝热T1 1.01993/1.01826/1.08974/0.99675eV复现源1.02/1.02/1.09/1.00。态身份和主导轨道组态一致，完整X/Y及实际Mulliken/Hirshfeld分析均保持Se相对I显著更强参与。人口分区与跃迁百分比归一化未唯一恢复，但不同已算定义不消除关键效应，也不改变主导组态；对当前电子性质及同方法同溶剂rubrene近阈值能量相容性，是有证据的解释而非缺核心节点。用户已明确接受约0.01–0.02eV和约0.51百分点I空穴偏差，计入通过。仍不认证作者每个精确百分比、唯一S1→T2机制、SOC/ISC速率、真实跨方法放能转移或上转换效率；IR780/Cy1约+0.02eV余量的限制必须保留。",
  "cross_review": "strict38_audit2 population-definition consistency review versus Ni; root source/native/current-contract review",
  "core_evidence_complete": true,
  "prior_user_accepted_numerical_deviation_applies": true,
  "brief": "4物种UDFT T1按源精度吻合，24计算项完成；完整XY与Mulliken/Hirshfeld控制保持显著Se>I参与，沿用已接受小差；精确人口定义及跨方法转移余量仍限定。",
  "source_detail_not_claimed_recovered": [
    "unique author population partition",
    "unique transition-percent normalization",
    "unreported author ZPVE convention; both versions computed"
  ]
}
```


科学参考验证完成不等于语义评审器已校准或运行时隔离已测试；旧 validation_plan 中的工程检查状态未在本次文档整理中冒称完成。

归档依据：[本篇最终严格复审](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/strict_verdict.json)。本轮仅移动未通过任务、汇总既有实际计算、补正文档并更新包哈希，没有改变题目或评分规则。

此处沿用用户既有明确授权，不能把未解释残差改称已恢复作者全部定义，也不能将该偏差接受方式推广到其他论文。V3 扩展任务的验收另行记录。

## 7. 可追溯输入、原始输出、分析与哈希索引

下列新地址用于本次整理后的访问；旧地址与原哈希同时保存在逐篇结构化提取 JSON。所有原生文件和旧快照字节保持不变。历史试算/失败分支可被索引，但只有上述具体采用结果属于本次验收；对同一个文件的多处引用不构成多次执行。

[逐篇结构化过程、原路径与新路径映射](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/staging/v2_extracted/autonomous_research/paper_e0791c047a731974.json)

整理前参考原文：[原字节快照](../../../../docs/v2_verification/maintenance/release_cleanup_20261015/source_snapshots/v2/autonomous_research/paper_e0791c047a731974/verified_computation_reference.md)；SHA-256 `d04c45ad91c586026c7ec7a79146f0647052479155984c285713a243b14e92cc`。

完整历史索引：[evidence_index.json](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/evidence_index.json)；冻结记录：[reviewed_records.json](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/reviewed_records.json)。历史 `full_original_in_zip` 是旧打包状态，本次迁至 docs 后不代表证据仍嵌在任务包中。

| 记录 | 原始文件／分析（整理后位置） | 原始 SHA-256 | 保存类型 |
|---|---|---|---|
| E0001 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e0791c047a731974/USER_ACCEPTANCE_20261009.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e0791c047a731974/USER_ACCEPTANCE_20261009.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0001_USER_ACCEPTANCE_20261009.json) | `fe5a5a0dde7f86d8419de66e5a422ab9a9516f880e61e6aa67e18a0bc12136b8` | evidence_or_analysis |
| E0002 | [tasks/v2_autonomous_research/paper_e0791c047a731974/agent_input/task.md](../agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0002_task.md) | `edcd22aa986f03f3e688ef7848f06d7895fdf9b0bf3a2ff36c5122605a4c5f83` | historical_task_binding |
| E0003 | [tasks/v2_paper_reproduction/paper_e0791c047a731974/agent_input/task.md](../../../v2_paper_reproduction/paper_e0791c047a731974/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0003_task.md) | `ce5b975cfb966aed6445f675fe86a5e809e3171cbb12323bd4935b7b026169e7` | historical_task_binding |
| E0004 | [docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/TWO_DEVIATION_PRIMARY_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/strict_reaudit/TWO_DEVIATION_PRIMARY_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0004_TWO_DEVIATION_PRIMARY_READBACK.json) | `b3b76c15c96f593e457d7ac95e98d4e4378f5e70e354803d22805ff9973ac4e3` | evidence_or_analysis |
| E0005 | [docs/v2_verification/history/v2_verified_task_export_20261011/TWO_USER_ACCEPTED_NATIVE_READBACK.json](../../../../docs/v2_verification/history/v2_verified_task_export_20261011/TWO_USER_ACCEPTED_NATIVE_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0005_TWO_USER_ACCEPTED_NATIVE_READBACK.json) | `2355a4f183bdce9fdb04456a0707cb8cde6d0263d22d829272e393c201658610` | evidence_or_analysis |
| E0006 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e0791c047a731974/NATIVE_VALIDITY_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e0791c047a731974/NATIVE_VALIDITY_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0006_NATIVE_VALIDITY_READBACK.json) | `4ac1d26e7b8a964a09a2b80d03add73e0d5f965b10829ee9e79c9b130a3abe43` | evidence_or_analysis |
| E0007 | [docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e0791c047a731974/COMPUTATION_STAGE.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/compute_first_20261009T035336Z/papers/paper_e0791c047a731974/COMPUTATION_STAGE.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0007_COMPUTATION_STAGE.json) | `ec5e83f1d45a03b2facbd2771eb403229ddb6fbbdb4ea87d82239afb6d31fe9f` | evidence_or_analysis |
| E0008 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e0791c047a731974/STRICT_REVIEW.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e0791c047a731974/STRICT_REVIEW.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0008_STRICT_REVIEW.json) | `0860038cc34430a7e1e10599495dd4b1357cbcfd9ce2b28898deb472e8dd3e8a` | evidence_or_analysis |
| E0009 | [docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_e0791c047a731974.md](../../../../docs/v2_verification/history/upgrade_tasks_verification/all_papers/paper_e0791c047a731974.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0009_paper_e0791c047a731974.md) | `60fe3f33e927032ec17b6911edb342266734276e1c4a0d17ae535e3a34581cdb` | evidence_or_analysis |
| E0010 | [docs/v2_verification/papers/paper_e0791c047a731974/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/paper_reproduction/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot) | `8ebf7fa07022c279da6a5fa1e548c92eeb2402a541b5921eae2e00ebab79174a` | historical_task_binding |
| E0011 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e0791c047a731974/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e0791c047a731974/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0011_task.md) | `edcd22aa986f03f3e688ef7848f06d7895fdf9b0bf3a2ff36c5122605a4c5f83` | historical_task_binding |
| E0012 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e0791c047a731974/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e0791c047a731974/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0012_reference_key_points.json) | `08d4634aa6ecf23b37f49f1f5ac9c5e35258cbe6af301a63625bea35bfa2e3e8` | historical_task_binding |
| E0013 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e0791c047a731974/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e0791c047a731974/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0013_reference_conclusions.json) | `21ff9fb7d3d239b44542bbd84222c0f1153e369de7f9705daf97134eca8f0eb5` | historical_task_binding |
| E0014 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/agent_input/task.md](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/agent_input/task.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0014_task.md) | `ce5b975cfb966aed6445f675fe86a5e809e3171cbb12323bd4935b7b026169e7` | historical_task_binding |
| E0015 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/evaluation/reference_key_points.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/evaluation/reference_key_points.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0015_reference_key_points.json) | `08d4634aa6ecf23b37f49f1f5ac9c5e35258cbe6af301a63625bea35bfa2e3e8` | historical_task_binding |
| E0016 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/evaluation/reference_conclusions.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/evaluation/reference_conclusions.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0016_reference_conclusions.json) | `21ff9fb7d3d239b44542bbd84222c0f1153e369de7f9705daf97134eca8f0eb5` | historical_task_binding |
| E0017 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e0791c047a731974/STRICT_REVIEW.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/papers/paper_e0791c047a731974/STRICT_REVIEW.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0017_STRICT_REVIEW.md) | `4c8728fd57002257b0a03ac8086e8ae71329365e76880331d8abac7e8af3902c` | evidence_or_analysis |
| E0018 | [papers/paper_e0791c047a731974/documents/main.pdf](../../../../papers/paper_e0791c047a731974/documents/main.pdf) | `4d136fb1b060c26a81c3dacdb397eed6c4c913f61d95b8ada7262e801a1a91c1` | source_document |
| E0019 | [papers/paper_e0791c047a731974/documents/supplementary_001.pdf](../../../../papers/paper_e0791c047a731974/documents/supplementary_001.pdf) | `06893f8d0c9056eba31a55a3c726a76bba621a0d20c80d6eb9fe11f9d35f1d02` | source_document |
| E0033 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0033_native_excerpt.json) | `81ea7772ffcb1a07d0b4ba934ab717a0b397589c0c42eeab72fe3bee0bbd8fa1` | native_output |
| E0034 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0034_native_excerpt.json) | `eb189981e13afdf94b3edde3a6521cbd283169793b37532decdfe7c26557399c` | native_output |
| E0035 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0035_native_excerpt.json) | `d8948b9025aef77ca59cc577cf79033a7bf190a8976b6a6e10512ba9831e34eb` | native_output |
| E0036 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0036_native_excerpt.json) | `3a0a2fb4cd6a470f885015dea02c75e4905dd0d8eacd221764eda8fc56f467ce` | native_output |
| E0037 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0037_native_excerpt.json) | `82569e6406285efb534eb66a2bd0ce35f41b5215bdaaead543ee192f73ecae84` | native_output |
| E0038 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0038_native_excerpt.json) | `fbc3136f51dc2c92c9dc838e43453860ce446eaf7b9f833c62c28027942f9e6c` | native_output |
| E0039 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0039_native_excerpt.json) | `a6154333d63a2123590305e002414971b80c78fdb9c89172fda65cea327456de` | native_output |
| E0040 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0040_native_excerpt.json) | `d789107d6428836a2032ff8f198a1a48e32a1d33285778cbe7095ca2c39ae1be` | native_output |
| E0041 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0041_native_excerpt.json) | `6d10ea193a4871fc13b657a5db5cb476b1f22c012e5b60ff6a3df32a95eb8c54` | native_output |
| E0042 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0042_native_excerpt.json) | `960dbe5343d4613d879833fe8493aa38395c4e6eee040430e0c338ee95e15f23` | native_output |
| E0043 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0043_native_excerpt.json) | `e0c71b0adfa09fd0b6ab54e0cc603c6504cd15d35f8332c68bcd32aca8c588b8` | native_output |
| E0044 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0044_native_excerpt.json) | `ca88b415f17f996ceed76748fa62304eec85a4a97bfe028b554d37d6a618bd70` | native_output |
| E0045 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0045_native_excerpt.json) | `3d11a8885822bfee61357107296ff4ec090ad3e9000243a959a237023aba20d2` | native_output |
| E0046 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0046_native_excerpt.json) | `d255edb8b66d87556d3ccf100a14c3afaa92bee5d421f03a4d035261d2e6ff1c` | native_output |
| E0047 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0047_native_excerpt.json) | `e6372b6e83ceec1d5611b00ece94f1b5d29b40b24af9cf56f23e4b1fb167bf9d` | native_output |
| E0048 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0048_native_excerpt.json) | `a725df344a7a14e2ce905d586596c3ba811e0ef4b12aec986aae76517bcc5922` | native_output |
| E0049 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0049_native_excerpt.json) | `697801651802143cfd356d9e32ccd961dd6667c2c17c92ca6ac6c05c63d2f632` | native_output |
| E0050 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0050_native_excerpt.json) | `4cf08d554cbc5a64f0e1a4c216cdab6391135b6c19b1a0dbbb775d98d4f1a911` | native_output |
| E0051 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0051_native_excerpt.json) | `8f83323030cbb6a393c37a160c299756094d0f4c032c707043b583798d790248` | native_output |
| E0052 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0052_native_excerpt.json) | `e340b8224da03cd15ab767448be846bc75d5916c81f78c4d423da0608b32e2f2` | native_output |
| E0053 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0053_native_excerpt.json) | `5bb8b847767968b5bdc59eff4babb1cc3f489d9934a20f1b9bf3836d6be06f39` | native_output |
| E0054 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0054_application_status.json) | `3bd3575e6a059e25d8b67a46479eac71fede96c4a13ac44e94ace075a80490b7` | evidence_or_analysis |
| E0055 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0055_application_status.json) | `1fd08da0999dfe900be019b50c1c051c9ef711dfa8b83cf4b7a59e730ff207a2` | evidence_or_analysis |
| E0056 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0056_application_status.json) | `b8b6c382db4d81cea8a4fc1b930775901dd0db33872fb763f63d50aa307f9f23` | evidence_or_analysis |
| E0057 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0057_application_status.json) | `b279a4251aa6849540e65a8c770fd9d5eff92f2527576e74f67b9d9953a747d6` | evidence_or_analysis |
| E0058 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0058_application_status.json) | `a5edacf2a7209c3866c9c658aa19dd43c9219690e61c1d5afb1ef95a4a0f126f` | evidence_or_analysis |
| E0059 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0059_application_status.json) | `a3c29445baa2c19450db6bd893521b858c38e5cdce6ff2d0676034bbe805c845` | evidence_or_analysis |
| E0060 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0060_application_status.json) | `57a86c05a11b0b816f742d428bdba44364afb4d622361748ea084a789e32cc06` | evidence_or_analysis |
| E0061 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0061_application_status.json) | `a87a92f415c509a5d650e3fc1f881ce7503d61ac97dfbc2d8134a672cfe975f3` | evidence_or_analysis |
| E0062 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0062_application_status.json) | `e24482727aa1bfb025d89ee5345e31f7355c6c5d4fb71e34ee12d10e82044159` | evidence_or_analysis |
| E0063 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0063_application_status.json) | `57a42f4b229978f4da856bf59caffbe92506021be1ea2f828222c1f7092119b2` | evidence_or_analysis |
| E0064 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0064_application_status.json) | `e301ced614bad948433d2750416a6946ada8309e054b44a42ddf5e56afc13183` | evidence_or_analysis |
| E0065 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0065_application_status.json) | `827a629d6f61e9726d1aacf73cab36d98a55dce7e2d3dd3277d91215ad1da42f` | evidence_or_analysis |
| E0066 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0066_application_status.json) | `3df945d2a90e19caf695af39387e36d8b7e9cd9e4c3da3e84f2fedb77747d458` | evidence_or_analysis |
| E0067 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0067_application_status.json) | `137696072eabaad82a566a8bb7d355a6261bd3e1934a160daaf5516f650b5373` | evidence_or_analysis |
| E0068 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0068_application_status.json) | `36b6113aa536383b8727ff12d08284fd52b325256f97e40f08d419626bc53a70` | evidence_or_analysis |
| E0069 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0069_application_status.json) | `056d5050d46a3efb8a86b338109276bfc88f6b24ee585017631b3ea030b5b09c` | evidence_or_analysis |
| E0070 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0070_application_status.json) | `e47f6ebd60bfae80c30023e7427ccfe1cd2c4c629e0320f80b56fc2613fe1ce2` | evidence_or_analysis |
| E0071 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0071_application_status.json) | `6b22d9b213eb4f29042b41c7dc9e678b4c72a3611983f03b85bff813a0cde2ee` | evidence_or_analysis |
| E0072 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e0791c047a731974/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e0791c047a731974/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0072_scoring_rules.json) | `f1e9ad47cbfdef7de1192fae4fedfced9e78cad0a845c8f6e812b0300f0bb61a` | historical_task_binding |
| E0073 | [tasks/upgrade_tasks/upgrade_version2/autonomous_research/paper_e0791c047a731974/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/autonomous_research/paper_e0791c047a731974/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0073_critical_failures.json) | `caa5c651b32eca1a18f49e9299ccc9c5f1e1dc9c96a2149e47290c1db2f3e70d` | historical_task_binding |
| E0074 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/evaluation/scoring_rules.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/evaluation/scoring_rules.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0074_scoring_rules.json) | `f1e9ad47cbfdef7de1192fae4fedfced9e78cad0a845c8f6e812b0300f0bb61a` | historical_task_binding |
| E0075 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/evaluation/critical_failures.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/evaluation/critical_failures.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0075_critical_failures.json) | `caa5c651b32eca1a18f49e9299ccc9c5f1e1dc9c96a2149e47290c1db2f3e70d` | historical_task_binding |
| E0076 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0076_input.com) | `04cdd3fc0dcaee588b7a98e02e92bd4ed4c2962af99809b7b3e148f931d9c67e` | input_or_analysis_code |
| E0077 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/endpoint_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0077_endpoint_audit.json) | `b9d299d9ff5270ca1a521051e82d0f49abf081410ba44fe7ad7a1868e7b8686c` | evidence_or_analysis |
| E0078 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0078_input.com) | `73164984762d082db2cc2164a8dfcd861dc3d3ba5c06193e46bdb614923c3cb1` | input_or_analysis_code |
| E0079 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0079_input.com) | `44720be0dadb92c0fc950d20ac5148f1cd08c42f72459da8c96c24b47a00d75f` | input_or_analysis_code |
| E0080 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0080_input.com) | `21be808f1ed902616333d4124452449af62d48859b97447e507ba0eeab640f6f` | input_or_analysis_code |
| E0081 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0081_input.com) | `06bcb1e4ace63034a1663ab8695c7b019c2cc590d3945c686ae15eaf16d7ee2b` | input_or_analysis_code |
| E0082 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0082_input.com) | `385d3add4e1036fb3491557549b3ea584bfe132c8ead5dbb6faf1e954542dfe3` | input_or_analysis_code |
| E0083 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0083_input.com) | `0d02360e455f1135a0c46cf6c7a2b7d12a7bf9d5b8a12372a05801025e1408f6` | input_or_analysis_code |
| E0084 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_native_reuse_audit_v2_a01/cy2_native_reuse_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_native_reuse_audit_v2_a01/cy2_native_reuse_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0084_cy2_native_reuse_audit.json) | `51911a8a01d092f00f6195dad36ebf8675dc62e5912f3440e4db3532bc4fc793` | evidence_or_analysis |
| E0085 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0085_input.com) | `de7cfc12bd0be1c7a69d7dd7b9c6ae4f706de917d34c236bc07aa8bfe8bd5e69` | input_or_analysis_code |
| E0086 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/cyanine_response_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0086_cyanine_response_audit.json) | `f39a879701f3e8ad5b5ce24071a27eb64b3173bff4b6898c5d03c6939ac9b090` | evidence_or_analysis |
| E0087 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0087_input.com) | `ee6c1d95717c91ba676d0eccc1132990639e6f223a48706fa8cedba6259926e8` | input_or_analysis_code |
| E0088 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0088_input.com) | `22c548e81e94dab7ae4b641c27c571dbab6d04e3417c6bb73686b1491437f69f` | input_or_analysis_code |
| E0089 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0089_input.com) | `012fa1e19d74db54756de8975aecbad9b0797020cc759c9685ad42b94211bff4` | input_or_analysis_code |
| E0090 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0090_input.com) | `7b5fadeceea4b5b6039b2de7c040e192efc779f15c5309c8e691bab47833b8d2` | input_or_analysis_code |
| E0091 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0091_input.com) | `790932d90471c3924bfbeb845ac5fbd951e79f762eb2a8920c1039bfd0e824e6` | input_or_analysis_code |
| E0092 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/S1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/S1/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0092_native_excerpt.json) | `21da9b750ea1f1b940f469a3d2050a480aaa4dfbfa7d3c438166b5e553b3d3dd` | native_output |
| E0093 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/cyanine_ir780_hirshfeld_definition.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/cyanine_ir780_hirshfeld_definition.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0093_cyanine_ir780_hirshfeld_definition.json) | `e9043d77bc9363b098af5871abe2f66d9aa14aa87bae1a32ac50dde7db4fbe3e` | evidence_or_analysis |
| E0094 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/cyanine_full_XY_closeout.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0094_cyanine_full_XY_closeout.json) | `4fe380af081aab1c9dedea712e53d93a9f614c7144300be77adad8824b8dacde` | evidence_or_analysis |
| E0095 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/T1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/T1/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0095_native_excerpt.json) | `68f563018c00879a897d2a2f7c028d8caa14c0b35a2d475ef2677eda44da8141` | native_output |
| E0096 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/T2/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_ir780_hirshfeld_definition_20261002_a01/T2/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0096_native_excerpt.json) | `45671daac32c08f9c94433131c114117d5eb2f6c946c206f3cde0817c214edc2` | native_output |
| E0097 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_S1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_S1/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0097_native_excerpt.json) | `f95ca2d220a2d3eea25915c6299017fe8b8d8bfcd7829c8e72ab6ed5bafccd37` | native_output |
| E0098 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/cyanine_companion_hirshfeld_definition.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0098_cyanine_companion_hirshfeld_definition.json) | `6f47eb9ab0eb1f7e631e4b13abb5e0166bc4b2ae03a8dac5e452494210357031` | evidence_or_analysis |
| E0099 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T1/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0099_native_excerpt.json) | `40c190918b2411ca6f2e8f4278cc2552555bd2a56e257d005af298dba4f17e07` | native_output |
| E0100 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T2/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy1_T2/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0100_native_excerpt.json) | `5e2d900c55db82125aa92d5891aa7aa709c7e31d0b86a1b9ffdc11a3b8dd847a` | native_output |
| E0101 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_S1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_S1/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0101_native_excerpt.json) | `e70d9156efadca56331813bd8fc65d44a6821e12ba6c5d0e7949d100e2e4a9ff` | native_output |
| E0102 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T1/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0102_native_excerpt.json) | `6bbc10058ce9c7dd8a9936947b0a5402aa99e3c79f100702fdfb73f50aadef84` | native_output |
| E0103 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T2/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_companion_hirshfeld_definition_20261002_a01/Cy2_T2/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0103_native_excerpt.json) | `fc01cb4e8f130bd20ad8d7831340bbab19dd6160459cc0205b7cd14e44d5c212` | native_output |
| E0104 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_stability_audit_v2_a01/cyanine_stability_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_stability_audit_v2_a01/cyanine_stability_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0104_cyanine_stability_audit.json) | `27eadb3b33595dc6f8ec159e9916cdd7850b170e0e64f709da38774a640d4056` | evidence_or_analysis |
| E0105 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_stability_acceptance_v2_a01/returned_acceptance_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_stability_acceptance_v2_a01/returned_acceptance_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0105_returned_acceptance_audit.json) | `91ce7ff219d72928e622d1b00fe0913099f2d815c6173128602f499abfac5193` | evidence_or_analysis |
| E0106 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_ci_export_integrity_repair_20261007_a01/output/results.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_ci_export_integrity_repair_20261007_a01/output/results.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0106_results.json) | `0e76645e3513e359b1d17cc5b66f7cff4b1f7f87c7ea72abea62d3d7162265fd` | evidence_or_analysis |
| E0107 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/ci_export_proof.py](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/ci_export_proof.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0107_ci_export_proof.py) | `95962a72eea7c13a34edadb442b38ce7980e93390bc563725f507e5a4fea7842` | input_or_analysis_code |
| E0108 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_response_20261006_a01/output/application_status.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_response_20261006_a01/output/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0108_application_status.json) | `517c5a85ceff2a2675fddcc1834b0b59cb18995589e4232802c5cc8323b1595a` | evidence_or_analysis |
| E0109 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/Cy1_fixed_source_comparison.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/Cy1_fixed_source_comparison.json) | `fbb20c0fd2cf63ba2bf9eefd54674a8fe64786e4c28f753f214e6c90f03790b2` | evidence_or_analysis |
| E0110 | [docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_e0791c047a731974/REVIEW.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/resume_remaining_20261009T020550Z/papers/paper_e0791c047a731974/REVIEW.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0110_REVIEW.json) | `83bd35a8870aa49f3aac881afb9dfc60fd1e65fdda1dffccd6db6953e5273430` | evidence_or_analysis |
| E0111 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/INSTRUCTIONS.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/INSTRUCTIONS.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0111_INSTRUCTIONS.md) | `6c9d5b9874acb6c9332f90553dcf828acc9b9c0bd3a8908b12b1a6e165a48571` | evidence_or_analysis |
| E0112 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/METHOD_FINDINGS.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/METHOD_FINDINGS.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0112_METHOD_FINDINGS.json) | `5c41ce954d4163cddb8cf4731cf2dda40a41e2dcfe5504c63f2e9f057742689d` | evidence_or_analysis |
| E0113 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/deliveries/W10_PUBLIC_RECHECK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/deliveries/W10_PUBLIC_RECHECK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0113_W10_PUBLIC_RECHECK.json) | `b1c5981248094ba4a4234e0bd29d847e341b5f4e40d4ec5e92beca33efa8a413` | evidence_or_analysis |
| E0114 | [docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/deliveries/W10_CROSSREF_RELATION_READBACK.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/continuous_forward_20261009T071333Z/deliveries/W10_CROSSREF_RELATION_READBACK.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0114_W10_CROSSREF_RELATION_READBACK.json) | `913747d2e1321189245b40e23d3b2cf20ee9466bf7c860e0b9fc101c8a49b2f9` | evidence_or_analysis |
| E0115 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/cyanine_screening_control.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/cyanine_screening_control.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0115_cyanine_screening_control.json) | `5853d2500b06f49a43ed01fddaba7f9b6baf656fd848a643e66d3a971ad13412` | evidence_or_analysis |
| E0143 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0143_input.com) | `16a5adb9b814e4cc38a0caf73bae74f2aabf4df70a216426be881de695c2a4cd` | input_or_analysis_code |
| E0144 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0144_input.com) | `3eab24660980be89176d780c79d0acf914f9bd95f750f2a7e0c6692dd36ddf7e` | input_or_analysis_code |
| E0145 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0145_input.com) | `93a2e153a68e831a9d67255f5988ecc938d7d3dbe89c3e233bacd328262ab33d` | input_or_analysis_code |
| E0146 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0146_input.com) | `234192ff2129f2f692e900d499cd5272d157fa53d5bc347dda13364b55181aae` | input_or_analysis_code |
| E0147 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0147_input.com) | `c44d05d27baa2a5e943f9ad1ac454b0822a39c16bb52d3941fde5b3f195d7c84` | input_or_analysis_code |
| E0148 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0148_input.com) | `f1ce5a662bc6c1260db0cd54132d57bcf51c51807259c73cfa23285ea839fa9e` | input_or_analysis_code |
| E0149 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0149_input.com) | `36aa61f82a55ac858db5dd1dbd23bad3bb8cc257075e6b3ec76b950e03df0918` | input_or_analysis_code |
| E0150 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0150_input.com) | `dd69c492376a75c830daf1fb55273e2e4acaf2886246119600f72d6a0ff591ca` | input_or_analysis_code |
| E0151 | [.software_cache/installations/gaussian/g16/install/g16/g16](../../../../.software_cache/installations/gaussian/g16/install/g16/g16) | `384f3baca38297d3f11ed2168bb9be836778fa4c5f5d07cb38751e3ed1a66db5` | evidence_or_analysis |
| E0152 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/v2_execution_20260929/audit_returned_20260930.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/v2_execution_20260929/audit_returned_20260930.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0152_audit_returned_20260930.py) | `d5e2c12c4c070b8ccfa20dc687f7903835d4eee00bd9ff1d3cdad77819065d79` | input_or_analysis_code |
| E0153 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/agent_input/data/inputs/Cy2_identity.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/agent_input/data/inputs/Cy2_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0153_Cy2_identity.json) | `39c76f934787f583843ce2ccc94d4e66b1fd5085ae549be6496f7ec9a0c1802c` | historical_task_binding |
| E0154 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy2_source_udft_t_optfreq_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy2_source_udft_t_optfreq_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0154_cy2_source_udft_t_optfreq_v2_a01.case.json) | `102f89dd72c674e5c6578c5736a4ce0f236f72f1e1bc0c962c6e1f399d49438b` | evidence_or_analysis |
| E0155 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/agent_input/data/inputs/IR780_identity.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/agent_input/data/inputs/IR780_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0155_IR780_identity.json) | `cc9ff6e1e549a00ca469ef26fb3b082fb715d25c676128b8df2583f92138703c` | historical_task_binding |
| E0156 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_s0_optfreq_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_s0_optfreq_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0156_ir780_source_s0_optfreq_v2_a01.case.json) | `83366adb529ef5bd02462b830a3110197847c51c374c6e4926b6e74c50c644d7` | evidence_or_analysis |
| E0157 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_udft_t_optfreq_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_udft_t_optfreq_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0157_ir780_source_udft_t_optfreq_v2_a01.case.json) | `76c9f5f12aa8db4419b44db957a3756866ae68f9c3c364236c6fbc68ff1ddf62` | evidence_or_analysis |
| E0158 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/agent_input/data/inputs/Cy1_identity.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/agent_input/data/inputs/Cy1_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0158_Cy1_identity.json) | `b0cd1a554a7e7f933552b26e265102c4d895691dee9181dfb473eca036eeac51` | historical_task_binding |
| E0159 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_s0_optfreq_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_s0_optfreq_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0159_cy1_source_s0_optfreq_v2_a01.case.json) | `3ee613e2452e7be81dae803545ab876dbe3f2975155f9a046684e7886cf5fcf5` | evidence_or_analysis |
| E0160 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_udft_t_optfreq_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_udft_t_optfreq_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0160_cy1_source_udft_t_optfreq_v2_a01.case.json) | `3f009dfe4fdc5a678d3d9c0b93fb3228f5c62710925d5eb4e435f77ed58e4035` | evidence_or_analysis |
| E0161 | [tasks/upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/agent_input/data/inputs/rubrene_identity.json](../../../upgrade_tasks/upgrade_version2/paper_reproduction/paper_e0791c047a731974/agent_input/data/inputs/rubrene_identity.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0161_rubrene_identity.json) | `11e0f8751c2d3d6dae6ffd96d988386723bba59a42cfff23eca86afdc4ec7bc2` | historical_task_binding |
| E0162 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_s0_optfreq_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_s0_optfreq_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0162_rubrene_source_s0_optfreq_v2_a01.case.json) | `1f5372a73e3f18742df3002ffccf1d98c9f6a2d9158eb418d81aaaace4b100c4` | evidence_or_analysis |
| E0163 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_udft_t_optfreq_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_udft_t_optfreq_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0163_rubrene_source_udft_t_optfreq_v2_a01.case.json) | `2e48b300bc605de66012c217bd4e2abffdbdb2e2f57a5023be2e0e9debe06142` | evidence_or_analysis |
| E0164 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/cy2_source_udft_t_optfreq_v2_a01_endpoint.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/cy2_source_udft_t_optfreq_v2_a01_endpoint.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0164_cy2_source_udft_t_optfreq_v2_a01_endpoint.xyz) | `a682e6e607e3da1b5747011828df84a735f1087703e64e2b62f70025202ce844` | input_or_analysis_code |
| E0165 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/ir780_source_s0_optfreq_v2_a01_endpoint.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/ir780_source_s0_optfreq_v2_a01_endpoint.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0165_ir780_source_s0_optfreq_v2_a01_endpoint.xyz) | `3248f07c0c121219d937fac1631cfc4066c39eab56982571da270f4a40a039ec` | input_or_analysis_code |
| E0166 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/ir780_source_udft_t_optfreq_v2_a01_endpoint.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/ir780_source_udft_t_optfreq_v2_a01_endpoint.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0166_ir780_source_udft_t_optfreq_v2_a01_endpoint.xyz) | `93605f59584b955b4de24530be25433f59bc9e068a2fbca86455a3a9d676913e` | input_or_analysis_code |
| E0167 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/cy1_source_s0_optfreq_v2_a01_endpoint.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/cy1_source_s0_optfreq_v2_a01_endpoint.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0167_cy1_source_s0_optfreq_v2_a01_endpoint.xyz) | `0382753146ca3e972f129e9643f287d8437d056138b68da7058e6e110d24fe74` | input_or_analysis_code |
| E0168 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/cy1_source_udft_t_optfreq_v2_a01_endpoint.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/cy1_source_udft_t_optfreq_v2_a01_endpoint.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0168_cy1_source_udft_t_optfreq_v2_a01_endpoint.xyz) | `8351b15c31f4f3d54234ceb7e84db514183bfe02778ab42209e3d19dfbd27b73` | input_or_analysis_code |
| E0169 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/rubrene_source_s0_optfreq_v2_a01_endpoint.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/rubrene_source_s0_optfreq_v2_a01_endpoint.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0169_rubrene_source_s0_optfreq_v2_a01_endpoint.xyz) | `d116d59d482694d9c306ccd5aeb15b3bfe65db32bcb117c344c1cbbe4e768799` | input_or_analysis_code |
| E0170 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/rubrene_source_udft_t_optfreq_v2_a01_endpoint.xyz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_seven_own_endpoints_audit_v2_a01/rubrene_source_udft_t_optfreq_v2_a01_endpoint.xyz)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0170_rubrene_source_udft_t_optfreq_v2_a01_endpoint.xyz) | `bef24d54b299af34a4f605e87aa124eec37067c85af1957fd5be7c1cccd3da1f` | input_or_analysis_code |
| E0171 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stability.json](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_s0_full_si_tdroute_20260915/stability.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0171_stability.json) | `a84b6af9f624a7461d6820529cee13adca24a41aa6f8ed06268d70795b318b1f` | evidence_or_analysis |
| E0172 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0172_input.com) | `a9308f3308aa5f20f206eb2780726f73697542ed0d3cc43e137112703904a519` | input_or_analysis_code |
| E0173 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/stdout.log](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0173_native_excerpt.json) | `4aa0f413693ad606244e62ce73c84d277b4d1005c64c6281cfc8ca2e6b60fcc5` | native_output |
| E0174 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/stability.json](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_source_internal_smallstep_optfreq_20260919/stability.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0174_stability.json) | `ae3cc83ef0973c6aeb176ad96a52ebdaeba75d2d6f1acbb485c835a962326434` | evidence_or_analysis |
| E0175 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stability.json](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_singlets_td6_20260915/stability.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0175_stability.json) | `c6f65e6fac5fcdf6d8d4521cafe5c9cfa3e45bdebda92e03d010c838434d367d` | evidence_or_analysis |
| E0176 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stability.json](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_computed_s0_triplets_td6_20260915/stability.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0176_stability.json) | `b2ed6fa175cb76ea5a68c14eecc2fb625fd3706b65848fe7e9f5b0343ba68457` | evidence_or_analysis |
| E0177 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/baseline_cy2_s0/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/baseline_cy2_s0/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0177_input.com) | `92d6b4f8da1a172698e02c7d1b394e9a9291ac63a371ef927ca554aaffdbe52b` | input_or_analysis_code |
| E0178 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/baseline_cy2_s0__resource_retry/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/baseline_cy2_s0__resource_retry/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0178_input.com) | `e82130f47828ab119c1ce633810cbfbb26da7fa9b40dc2555f200f7294b459c5` | input_or_analysis_code |
| E0179 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/coverage_cy2_s0/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/coverage_cy2_s0/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0179_input.com) | `5b9dff7033547ae77c5ba815005d26c9e8567436b9eb32e637ecffdb958dbb15` | input_or_analysis_code |
| E0180 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/coverage_cy2_s0__resource_retry/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/coverage_cy2_s0__resource_retry/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0180_input.com) | `409350f54824a46167190d07658a5006feaf37548db7897d62bb6e1e010d8159` | input_or_analysis_code |
| E0181 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_recovered_s0_optfreq/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_recovered_s0_optfreq/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0181_input.com) | `4b70a4dad382ee1ce5f4da888b171fbc62230badf556cff781dcc7a73ef9e1ef` | input_or_analysis_code |
| E0182 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_recovered_singlet_td3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_recovered_singlet_td3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0182_input.com) | `f7783221740e47e168c02012eecb364c3b5e087d93669d8373c31f802a2abd8a` | input_or_analysis_code |
| E0183 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_recovered_t1_opt/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_recovered_t1_opt/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0183_input.com) | `c4cc14e835e7ee821d07ad1d1f2964dbc2d1798b024d3b43de4ffdc6dd7b4d1a` | input_or_analysis_code |
| E0184 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_recovered_triplet_td3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_recovered_triplet_td3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0184_input.com) | `fa1170b8f3ddca59fe9fd00745127b591ac3c5dd26c64d205e9ab7fc73974b9d` | input_or_analysis_code |
| E0185 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_singlet_td3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_singlet_td3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0185_input.com) | `b653cb0b3f4f823681e04e2611aa96c89ba2f24197233be2ba53a046321d99f3` | input_or_analysis_code |
| E0186 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_singlet_td3__resource_retry/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_singlet_td3__resource_retry/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0186_input.com) | `239f126e8cc88e5c8c55fce7cd39946532db7f7dd80ff373a8a8d72701ac8be5` | input_or_analysis_code |
| E0187 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_t1_opt/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_t1_opt/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0187_input.com) | `ee8b1b361d2b8f16c34516b9aee68bde51b267bc05d47c9e0fc144fa893d9a87` | input_or_analysis_code |
| E0188 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_t1_opt__resource_retry/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_t1_opt__resource_retry/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0188_input.com) | `90ac850b1cab34925e3897563518593cbb0016b29f97fa48045c756c9a73d48d` | input_or_analysis_code |
| E0189 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_triplet_td3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_triplet_td3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0189_input.com) | `a54b7db0647debe7f1dd2d4de3d43e8e53f8059685ff869965334ab98dda97a8` | input_or_analysis_code |
| E0190 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_triplet_td3__resource_retry/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/artifacts/gaussian_batch/cy2_triplet_td3__resource_retry/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0190_input.com) | `ba5f8f910d5caadd0cfa476a5357fdd7f62522fc47f6f0336abbdaadb257156f` | input_or_analysis_code |
| E0191 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_631gdp_setz_optfreq__retry_001_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_631gdp_setz_optfreq__retry_001_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0191_input.com) | `5734ef20310939f478016bc67626193ceea0e8230a73bc7410b427bf5074bb30` | input_or_analysis_code |
| E0192 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_631gdp_setz_optfreq__retry_002_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_631gdp_setz_optfreq__retry_002_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0192_input.com) | `5734ef20310939f478016bc67626193ceea0e8230a73bc7410b427bf5074bb30` | input_or_analysis_code |
| E0193 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_631gdp_setz_optfreq_hpc20_p3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_631gdp_setz_optfreq_hpc20_p3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0193_input.com) | `5734ef20310939f478016bc67626193ceea0e8230a73bc7410b427bf5074bb30` | input_or_analysis_code |
| E0194 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_631gdp_setz_optfreq_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_631gdp_setz_optfreq_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0194_input.com) | `5734ef20310939f478016bc67626193ceea0e8230a73bc7410b427bf5074bb30` | input_or_analysis_code |
| E0195 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_631gdp_setz_optfreq_hpc20_p6__resubmit_001/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_631gdp_setz_optfreq_hpc20_p6__resubmit_001/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0195_input.com) | `5734ef20310939f478016bc67626193ceea0e8230a73bc7410b427bf5074bb30` | input_or_analysis_code |
| E0196 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_vertical_singlet_td3_hpc20_p3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_vertical_singlet_td3_hpc20_p3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0196_input.com) | `c539e0d671b2547e6786d664c6bb235a745d1d1c14c4582f4c0b9cc7a6a0721a` | input_or_analysis_code |
| E0197 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_vertical_singlet_td3_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_vertical_singlet_td3_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0197_input.com) | `c539e0d671b2547e6786d664c6bb235a745d1d1c14c4582f4c0b9cc7a6a0721a` | input_or_analysis_code |
| E0198 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_vertical_triplet_td3_hpc20_p3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_vertical_triplet_td3_hpc20_p3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0198_input.com) | `2d1588cd9cba9b0bdd055344dab3e6fedcc5f6071c944910966afd4a937b6569` | input_or_analysis_code |
| E0199 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_vertical_triplet_td3_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_s0_vertical_triplet_td3_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0199_input.com) | `2d1588cd9cba9b0bdd055344dab3e6fedcc5f6071c944910966afd4a937b6569` | input_or_analysis_code |
| E0200 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_t1_relaxed_triplet_optfreq_hpc20_p3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_t1_relaxed_triplet_optfreq_hpc20_p3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0200_input.com) | `6d883406e384f816d52aac02e5d3441ea440b3d55a7eb7456b37b5af220c18be` | input_or_analysis_code |
| E0201 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_t1_relaxed_triplet_optfreq_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_author_t1_relaxed_triplet_optfreq_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0201_input.com) | `6d883406e384f816d52aac02e5d3441ea440b3d55a7eb7456b37b5af220c18be` | input_or_analysis_code |
| E0202 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_si62_author_s0_optfreq_corrected_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_si62_author_s0_optfreq_corrected_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0202_input.com) | `2eaf300e0d3f69ce59cd93a5bc9437a36698394e27f3c765d26162b36e7e14f4` | input_or_analysis_code |
| E0203 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_t1_full_si_tdroute_20260915_hpc20_p6/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/hpc_runs/cy2_t1_full_si_tdroute_20260915_hpc20_p6/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0203_input.com) | `4c16278c3d82df126343c5883713072c871c7d47a65a063eba162b4be3a72776` | input_or_analysis_code |
| E0204 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/baseline_cy2_s0.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/baseline_cy2_s0.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0204_baseline_cy2_s0.com) | `92d6b4f8da1a172698e02c7d1b394e9a9291ac63a371ef927ca554aaffdbe52b` | input_or_analysis_code |
| E0205 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/baseline_cy2_s0__resource_retry.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/baseline_cy2_s0__resource_retry.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0205_baseline_cy2_s0__resource_retry.com) | `e82130f47828ab119c1ce633810cbfbb26da7fa9b40dc2555f200f7294b459c5` | input_or_analysis_code |
| E0206 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/coverage_cy2_s0.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/coverage_cy2_s0.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0206_coverage_cy2_s0.com) | `5b9dff7033547ae77c5ba815005d26c9e8567436b9eb32e637ecffdb958dbb15` | input_or_analysis_code |
| E0207 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/coverage_cy2_s0__resource_retry.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/coverage_cy2_s0__resource_retry.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0207_coverage_cy2_s0__resource_retry.com) | `409350f54824a46167190d07658a5006feaf37548db7897d62bb6e1e010d8159` | input_or_analysis_code |
| E0208 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_s0_optfreq.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_s0_optfreq.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0208_cy2_recovered_s0_optfreq.com) | `4b70a4dad382ee1ce5f4da888b171fbc62230badf556cff781dcc7a73ef9e1ef` | input_or_analysis_code |
| E0209 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_s0_optfreq__segfault_retry1.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_s0_optfreq__segfault_retry1.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0209_cy2_recovered_s0_optfreq__segfault_retry1.com) | `4b70a4dad382ee1ce5f4da888b171fbc62230badf556cff781dcc7a73ef9e1ef` | input_or_analysis_code |
| E0210 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_singlet_td3.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_singlet_td3.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0210_cy2_recovered_singlet_td3.com) | `f7783221740e47e168c02012eecb364c3b5e087d93669d8373c31f802a2abd8a` | input_or_analysis_code |
| E0211 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_t1_opt.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_t1_opt.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0211_cy2_recovered_t1_opt.com) | `c4cc14e835e7ee821d07ad1d1f2964dbc2d1798b024d3b43de4ffdc6dd7b4d1a` | input_or_analysis_code |
| E0212 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_t1_opt__segfault_retry1.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_t1_opt__segfault_retry1.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0212_cy2_recovered_t1_opt__segfault_retry1.com) | `c4cc14e835e7ee821d07ad1d1f2964dbc2d1798b024d3b43de4ffdc6dd7b4d1a` | input_or_analysis_code |
| E0213 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_triplet_td3.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_triplet_td3.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0213_cy2_recovered_triplet_td3.com) | `fa1170b8f3ddca59fe9fd00745127b591ac3c5dd26c64d205e9ab7fc73974b9d` | input_or_analysis_code |
| E0214 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_triplet_td3__segfault_retry1.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_recovered_triplet_td3__segfault_retry1.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0214_cy2_recovered_triplet_td3__segfault_retry1.com) | `fa1170b8f3ddca59fe9fd00745127b591ac3c5dd26c64d205e9ab7fc73974b9d` | input_or_analysis_code |
| E0215 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_singlet_td3.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_singlet_td3.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0215_cy2_singlet_td3.com) | `b653cb0b3f4f823681e04e2611aa96c89ba2f24197233be2ba53a046321d99f3` | input_or_analysis_code |
| E0216 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_singlet_td3__resource_retry.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_singlet_td3__resource_retry.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0216_cy2_singlet_td3__resource_retry.com) | `239f126e8cc88e5c8c55fce7cd39946532db7f7dd80ff373a8a8d72701ac8be5` | input_or_analysis_code |
| E0217 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_t1_opt.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_t1_opt.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0217_cy2_t1_opt.com) | `ee8b1b361d2b8f16c34516b9aee68bde51b267bc05d47c9e0fc144fa893d9a87` | input_or_analysis_code |
| E0218 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_t1_opt__resource_retry.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_t1_opt__resource_retry.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0218_cy2_t1_opt__resource_retry.com) | `90ac850b1cab34925e3897563518593cbb0016b29f97fa48045c756c9a73d48d` | input_or_analysis_code |
| E0219 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_triplet_td3.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_triplet_td3.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0219_cy2_triplet_td3.com) | `a54b7db0647debe7f1dd2d4de3d43e8e53f8059685ff869965334ab98dda97a8` | input_or_analysis_code |
| E0220 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_triplet_td3__resource_retry.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/code/cy2_triplet_td3__resource_retry.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0220_cy2_triplet_td3__resource_retry.com) | `ba5f8f910d5caadd0cfa476a5357fdd7f62522fc47f6f0336abbdaadb257156f` | input_or_analysis_code |
| E0221 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_0a88b9dff8a348d9b03c743f97820163/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_0a88b9dff8a348d9b03c743f97820163/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0221_input.com) | `409350f54824a46167190d07658a5006feaf37548db7897d62bb6e1e010d8159` | input_or_analysis_code |
| E0222 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_31e4b0c1b9fc4025b335506ddc5835b7/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_31e4b0c1b9fc4025b335506ddc5835b7/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0222_input.com) | `ee8b1b361d2b8f16c34516b9aee68bde51b267bc05d47c9e0fc144fa893d9a87` | input_or_analysis_code |
| E0223 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_34b46f915740420eb75686c10521c6e2/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_34b46f915740420eb75686c10521c6e2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0223_input.com) | `c4cc14e835e7ee821d07ad1d1f2964dbc2d1798b024d3b43de4ffdc6dd7b4d1a` | input_or_analysis_code |
| E0224 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_545a1a2e660f4ab5972d893fa7d47f74/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_545a1a2e660f4ab5972d893fa7d47f74/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0224_input.com) | `a54b7db0647debe7f1dd2d4de3d43e8e53f8059685ff869965334ab98dda97a8` | input_or_analysis_code |
| E0225 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_5760e55f2ee24987b57d6463cb4c2af3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_5760e55f2ee24987b57d6463cb4c2af3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0225_input.com) | `b653cb0b3f4f823681e04e2611aa96c89ba2f24197233be2ba53a046321d99f3` | input_or_analysis_code |
| E0226 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_8a0631180d6340d9ad36c86057b26c75/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_8a0631180d6340d9ad36c86057b26c75/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0226_input.com) | `ba5f8f910d5caadd0cfa476a5357fdd7f62522fc47f6f0336abbdaadb257156f` | input_or_analysis_code |
| E0227 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_a3e9cff944384264a8ff68fdd4f773de/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_a3e9cff944384264a8ff68fdd4f773de/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0227_input.com) | `239f126e8cc88e5c8c55fce7cd39946532db7f7dd80ff373a8a8d72701ac8be5` | input_or_analysis_code |
| E0228 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_b0e1ca866495409f95a978a5e30cadb3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_b0e1ca866495409f95a978a5e30cadb3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0228_input.com) | `f7783221740e47e168c02012eecb364c3b5e087d93669d8373c31f802a2abd8a` | input_or_analysis_code |
| E0229 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_b1165855533748e6ae4fe1ff6de1f7d4/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_b1165855533748e6ae4fe1ff6de1f7d4/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0229_input.com) | `4b70a4dad382ee1ce5f4da888b171fbc62230badf556cff781dcc7a73ef9e1ef` | input_or_analysis_code |
| E0230 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_bab0411aa3864f7c8ae5ba1e7818d3f8/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_bab0411aa3864f7c8ae5ba1e7818d3f8/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0230_input.com) | `fa1170b8f3ddca59fe9fd00745127b591ac3c5dd26c64d205e9ab7fc73974b9d` | input_or_analysis_code |
| E0231 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_bd8a6c6cfd934f638495ce87ba626a70/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_bd8a6c6cfd934f638495ce87ba626a70/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0231_input.com) | `92d6b4f8da1a172698e02c7d1b394e9a9291ac63a371ef927ca554aaffdbe52b` | input_or_analysis_code |
| E0232 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_c2341fbdd5ca458784fd059c806dc7db/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_c2341fbdd5ca458784fd059c806dc7db/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0232_input.com) | `e82130f47828ab119c1ce633810cbfbb26da7fa9b40dc2555f200f7294b459c5` | input_or_analysis_code |
| E0233 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_cc9ce92ebb7d41b197a3e8912b14ba2a/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_cc9ce92ebb7d41b197a3e8912b14ba2a/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0233_input.com) | `90ac850b1cab34925e3897563518593cbb0016b29f97fa48045c756c9a73d48d` | input_or_analysis_code |
| E0234 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_e6d94d595482437d81beb6841bbd170d/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_e6d94d595482437d81beb6841bbd170d/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0234_input.com) | `4b70a4dad382ee1ce5f4da888b171fbc62230badf556cff781dcc7a73ef9e1ef` | input_or_analysis_code |
| E0235 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_ea467a010a4d42d3bf462ade9d882c1b/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/native_workspace_batch/outputs/execution_jobs/job_ea467a010a4d42d3bf462ade9d882c1b/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0235_input.com) | `5b9dff7033547ae77c5ba815005d26c9e8567436b9eb32e637ecffdb958dbb15` | input_or_analysis_code |
| E0236 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_failure_tests_20260909/e079_si62_author_route/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_failure_tests_20260909/e079_si62_author_route/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0236_input.com) | `bfe3bee1c75f389b562b1a9c26b4ac69c13a5d9e8a1bb2f867aef7056dbd6924` | input_or_analysis_code |
| E0237 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_failure_tests_20260909/e079_si62_author_route_gen_v2/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_failure_tests_20260909/e079_si62_author_route_gen_v2/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0237_input.com) | `448a61cc0ba0a894577784bc3fbe70aa4ee84700f9bfc1b1fadbd42fc717caa8` | input_or_analysis_code |
| E0238 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_failure_tests_20260909/e079_si62_author_route_gen_v3/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_failure_tests_20260909/e079_si62_author_route_gen_v3/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0238_input.com) | `527e88b461e061419d87e6389c0181be99c7f55e13df764befb3c9c9e0c5f8f8` | input_or_analysis_code |
| E0239 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_full_si_tdroute_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/local_stage_tests_20260914/cy2_t1_full_si_tdroute_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0239_input.com) | `83bf1a41f365ec3d755d398da8521e2007e9f866273b73cffcafee69e96a847a` | input_or_analysis_code |
| E0240 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/recovery27_20260915/cy2_computed_s0_singlets_td6_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/recovery27_20260915/cy2_computed_s0_singlets_td6_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0240_input.com) | `1c3f21c61bebbb4c06610d0d5e3220b31fb733cdbb9b09ca2a1b808e439a1745` | input_or_analysis_code |
| E0241 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/recovery27_20260915/cy2_computed_s0_triplets_td6_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/recovery27_20260915/cy2_computed_s0_triplets_td6_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0241_input.com) | `067f6848ce88be24468415f5a51e350f84d22e70938061f8b7e2a61c5faf43b4` | input_or_analysis_code |
| E0242 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/recovery27_20260915/cy2_s0_full_si_tdroute_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/recovery27_20260915/cy2_s0_full_si_tdroute_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0242_input.com) | `c8c28fa46877b450b4e60cd0869ffd26ec0dcfe962c07e06d00140a3e8bdccd2` | input_or_analysis_code |
| E0243 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/recovery27_20260915/cy2_t1_full_si_tdroute_20260915/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/recovery27_20260915/cy2_t1_full_si_tdroute_20260915/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0243_input.com) | `4c16278c3d82df126343c5883713072c871c7d47a65a063eba162b4be3a72776` | input_or_analysis_code |
| E0244 | [docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/recovery27_20260915/cy2_t1_source_internal_smallstep_optfreq_20260919/input.com](../../../../docs/v2_verification/history/verification/group_4/paper_e0791c047a731974/provenance/recovery27_20260915/cy2_t1_source_internal_smallstep_optfreq_20260919/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0244_input.com) | `cdbea778133d3fdbff051e7adb6b8236bf644f17a5917afea3f76d5390feac51` | input_or_analysis_code |
| E0245 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/stable.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/stable.chk) | `b3f806df43e559b788e1b34a90ed944381e19b7c1cabe79868858c578154c1f8` | evidence_or_analysis |
| E0246 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/response.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_singlet6_strict_v1_a01/response.chk) | `42f25e6467b949bf1f940786b65a45442097fa7e0f6b6045917bf623e4f80af9` | evidence_or_analysis |
| E0247 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/response.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_s0_triplet6_strict_v1_a01/response.chk) | `e82d8dab521b57a6755acc8540053c0f7395268f4637c76ee2074955df182ac6` | evidence_or_analysis |
| E0248 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/stable.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/stable.chk) | `ff2b2627c429a7e0bf9bd5a4df2e522629324c22aacb05ef3cf6a0c84ac30596` | evidence_or_analysis |
| E0249 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/response.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_singlet6_strict_v1_a01/response.chk) | `293ca2b2e1f08e80ad0f2dec27238f8ee5a38525c5675c86b2f674d0c9c0ed4d` | evidence_or_analysis |
| E0250 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/response.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_s0_triplet6_strict_v1_a01/response.chk) | `56b396afd8ff2107885d0acb33e9fc6f03b01e2565ddc8edc240d6a0a7bc75d6` | evidence_or_analysis |
| E0251 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_remaining_source_models_audit_v2_a01/remaining_models_audit.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_remaining_source_models_audit_v2_a01/remaining_models_audit.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0251_remaining_models_audit.json) | `9ddf25e9e52f6bfdd087be399bc6c02784fdc1afccc9f7413fe94b2e0c52cb98` | evidence_or_analysis |
| E0252 | [docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_e0791c047a731974.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/coordinator_reviews/paper_e0791c047a731974.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0252_paper_e0791c047a731974.json) | `2ed20a57f176689f9099f2fef2abae4a1289319c91bff9ea098147bfcea32ee9` | evidence_or_analysis |
| E0253 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group5/source_checks_0750Z/official_2.html](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group5/source_checks_0750Z/official_2.html) | `2ed92bf4dd0b78009d03f0437f5fc04b4698edd17380875f03ecb4f271151cdb` | evidence_or_analysis |
| E0254 | [docs/v2_verification/history/strict_author_route_validation_20261001/groups/group5/source_checks_0750Z/official_3.html](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/groups/group5/source_checks_0750Z/official_3.html) | `cabb2f46c1d91f0c75902db7b000429bb3ce393dc51779cae547920f4c0ddb2e` | evidence_or_analysis |
| E0255 | [.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/Multiwfn_noGUI](../../../../.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/Multiwfn_noGUI) | `d7d2539dae7b8d2faf03ca473d856cf1936a7b8ca4fdcfbb3e1cfa5f45184030` | evidence_or_analysis |
| E0256 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_S1/orbitals.fch](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_S1/orbitals.fch) | `a9ff9f2bd95758a899034e9dc67888a1820c87ad072bff08616e4d73e6337249` | evidence_or_analysis |
| E0257 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_S1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_S1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0257_coefficients.txt) | `ffaf28d958c0019c5bfbd44b422ca6a5772944629043979370fde8ac0012fe4e` | evidence_or_analysis |
| E0258 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_S1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_S1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0258_fragments.txt) | `278a52d3a2dca67d7fa5e12bcd939e0ab564f8bdb2a77b5f09b571fc00148b29` | evidence_or_analysis |
| E0259 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_S1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_S1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0259_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0260 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_S1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_S1/settings.ini) | `6d389712144c2f00bcc5f8a4823065b1037c5c0d0e18cc71190b12e9aeb09b79` | evidence_or_analysis |
| E0261 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T1/orbitals.fch](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T1/orbitals.fch) | `26e6fa8721a4bd5783323e77986398c1a3eb8ee98b1044aa1a7378ba68cce2be` | evidence_or_analysis |
| E0262 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0262_coefficients.txt) | `7886216a100ecd33351476a74b426832f5031a060c0ae5bd5221db82433131a3` | evidence_or_analysis |
| E0263 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0263_fragments.txt) | `278a52d3a2dca67d7fa5e12bcd939e0ab564f8bdb2a77b5f09b571fc00148b29` | evidence_or_analysis |
| E0264 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0264_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0265 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T1/settings.ini) | `6d389712144c2f00bcc5f8a4823065b1037c5c0d0e18cc71190b12e9aeb09b79` | evidence_or_analysis |
| E0266 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T2/orbitals.fch](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T2/orbitals.fch) | `26e6fa8721a4bd5783323e77986398c1a3eb8ee98b1044aa1a7378ba68cce2be` | evidence_or_analysis |
| E0267 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T2/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T2/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0267_coefficients.txt) | `f4239ca553d12c1ca5ae8ff168e16684bc3a76ce810e0a7f0caa831be4b1ce12` | evidence_or_analysis |
| E0268 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T2/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T2/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0268_fragments.txt) | `278a52d3a2dca67d7fa5e12bcd939e0ab564f8bdb2a77b5f09b571fc00148b29` | evidence_or_analysis |
| E0269 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T2/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T2/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0269_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0270 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T2/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/IR780_T2/settings.ini) | `6d389712144c2f00bcc5f8a4823065b1037c5c0d0e18cc71190b12e9aeb09b79` | evidence_or_analysis |
| E0271 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/IR780/singlet/data.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/IR780/singlet/data.fchk) | `a9ff9f2bd95758a899034e9dc67888a1820c87ad072bff08616e4d73e6337249` | evidence_or_analysis |
| E0272 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/IR780/triplet/data.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/IR780/triplet/data.fchk) | `26e6fa8721a4bd5783323e77986398c1a3eb8ee98b1044aa1a7378ba68cce2be` | evidence_or_analysis |
| E0273 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy1/singlet/data.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy1/singlet/data.fchk) | `442ffcf4797a0ea956680e48105ab80e5e7832ce8c2e9fe7df1e1bf35dc7656f` | evidence_or_analysis |
| E0274 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy1/triplet/data.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy1/triplet/data.fchk) | `af8a0856f077b2975c3dc8cacccf88714e3533dc92608b2e425668b8b72e37e0` | evidence_or_analysis |
| E0275 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy2/singlet/data.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy2/singlet/data.fchk) | `8619cb912e8681568faa339ae25e2a313043cb4fe07193e9f9ee1e6d8aa4f4d6` | evidence_or_analysis |
| E0276 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy2/triplet/data.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy2/triplet/data.fchk) | `b1d1f5f040bed7279792dc8ffa19a69e3f824ccd4284fe91ce763017a80c164e` | evidence_or_analysis |
| E0277 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0277_application_status.json) | `552e38a80fb12a8189be4962bf3a9be4d017fd7bf74cedf8bc1ed4109ad4eb64` | evidence_or_analysis |
| E0278 | [.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/settings.ini](../../../../.software_cache/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/settings.ini) | `e5f700c4d34c143b0266f48fe049f45c21f73afe9e5a68e5acccd008cfbd5c7c` | evidence_or_analysis |
| E0279 | [docs/v2_verification/history/verification/group_3/postprocess_b5_saved_states_reaudit_20260918.py](../../../../docs/v2_verification/history/verification/group_3/postprocess_b5_saved_states_reaudit_20260918.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0279_postprocess_b5_saved_states_reaudit_20260918.py) | `8ae6de3214e6ec17ca17b89be6157b6f96ef077fb883215b34e7416b19e8fc3d` | input_or_analysis_code |
| E0280 | [docs/v2_verification/history/verification/group_3/postprocess_b5_official_multiwfn_20260918.py](../../../../docs/v2_verification/history/verification/group_3/postprocess_b5_official_multiwfn_20260918.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0280_postprocess_b5_official_multiwfn_20260918.py) | `e3d1ef592fda4776d8463ed879c26dc7dce8379cb77a53a9114e93ec13b11b8f` | input_or_analysis_code |
| E0281 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/IR780/canonical/data.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/IR780/canonical/data.fchk) | `c3749d66d2753f4d80aceb7faa085b8755b530286012d16f7798563cd0cf84f6` | evidence_or_analysis |
| E0282 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy1/canonical/data.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy1/canonical/data.fchk) | `87facc63d4d9a7add30470dab7a2b9e665f57c5e531ea1234eff3845fc1796e1` | evidence_or_analysis |
| E0283 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy2/canonical/data.fchk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_six_response_readback_strict_v1_a01/Cy2/canonical/data.fchk) | `4ace1e80525e106a24883fb2859727ba0ee065c596a8a181e4a52cd03dbe1030` | evidence_or_analysis |
| E0284 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/cyanine_full_XY_closeout.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/cyanine_full_XY_closeout.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0284_cyanine_full_XY_closeout.json) | `c5c8d6df87d09f24b5157edf5b2ee48a37d6f2d91a53e369ec6650a04b410610` | evidence_or_analysis |
| E0285 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/orbitals.fch](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/orbitals.fch) | `442ffcf4797a0ea956680e48105ab80e5e7832ce8c2e9fe7df1e1bf35dc7656f` | evidence_or_analysis |
| E0286 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0286_coefficients.txt) | `7706b75878d6850e5db9f581d8edb859596fc73542225e7d8a46471e80320a1a` | evidence_or_analysis |
| E0287 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0287_fragments.txt) | `6d6a13dc15b9d6d848b94b8f5082cfc2187eb44373f9ba1ae3b9d2051cd5faba` | evidence_or_analysis |
| E0288 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0288_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0289 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/settings.ini) | `6d389712144c2f00bcc5f8a4823065b1037c5c0d0e18cc71190b12e9aeb09b79` | evidence_or_analysis |
| E0290 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/orbitals.fch](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/orbitals.fch) | `af8a0856f077b2975c3dc8cacccf88714e3533dc92608b2e425668b8b72e37e0` | evidence_or_analysis |
| E0291 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0291_coefficients.txt) | `87341a445e567f8e9d6785fc988309189e977b5bbad81960869e1c0da7bb9672` | evidence_or_analysis |
| E0292 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0292_fragments.txt) | `6d6a13dc15b9d6d848b94b8f5082cfc2187eb44373f9ba1ae3b9d2051cd5faba` | evidence_or_analysis |
| E0293 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0293_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0294 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/settings.ini) | `6d389712144c2f00bcc5f8a4823065b1037c5c0d0e18cc71190b12e9aeb09b79` | evidence_or_analysis |
| E0295 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/orbitals.fch](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/orbitals.fch) | `af8a0856f077b2975c3dc8cacccf88714e3533dc92608b2e425668b8b72e37e0` | evidence_or_analysis |
| E0296 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0296_coefficients.txt) | `53297b9f2df3fe4831bdd1175cc87a44a4facda43c21dd99b51af6ccb8f8572c` | evidence_or_analysis |
| E0297 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0297_fragments.txt) | `6d6a13dc15b9d6d848b94b8f5082cfc2187eb44373f9ba1ae3b9d2051cd5faba` | evidence_or_analysis |
| E0298 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0298_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0299 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/settings.ini) | `6d389712144c2f00bcc5f8a4823065b1037c5c0d0e18cc71190b12e9aeb09b79` | evidence_or_analysis |
| E0300 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_S1/orbitals.fch](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_S1/orbitals.fch) | `8619cb912e8681568faa339ae25e2a313043cb4fe07193e9f9ee1e6d8aa4f4d6` | evidence_or_analysis |
| E0301 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_S1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_S1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0301_coefficients.txt) | `8676f90191891c73cc2504149b6558b15bea7823aa12747dc2dbe03e84c3f24c` | evidence_or_analysis |
| E0302 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_S1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_S1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0302_fragments.txt) | `1a0661498f318ebeba7034ba808c6c3febd257868a46cf2457c310a819386345` | evidence_or_analysis |
| E0303 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_S1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_S1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0303_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0304 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_S1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_S1/settings.ini) | `6d389712144c2f00bcc5f8a4823065b1037c5c0d0e18cc71190b12e9aeb09b79` | evidence_or_analysis |
| E0305 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T1/orbitals.fch](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T1/orbitals.fch) | `b1d1f5f040bed7279792dc8ffa19a69e3f824ccd4284fe91ce763017a80c164e` | evidence_or_analysis |
| E0306 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0306_coefficients.txt) | `be2f240f70fe5256781a6d94e1788711da0b8ae645b85a2b906cd50ea5458751` | evidence_or_analysis |
| E0307 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0307_fragments.txt) | `1a0661498f318ebeba7034ba808c6c3febd257868a46cf2457c310a819386345` | evidence_or_analysis |
| E0308 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0308_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0309 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T1/settings.ini) | `6d389712144c2f00bcc5f8a4823065b1037c5c0d0e18cc71190b12e9aeb09b79` | evidence_or_analysis |
| E0310 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T2/orbitals.fch](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T2/orbitals.fch) | `b1d1f5f040bed7279792dc8ffa19a69e3f824ccd4284fe91ce763017a80c164e` | evidence_or_analysis |
| E0311 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T2/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T2/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0311_coefficients.txt) | `5f73ac90e8e2d23fd79c488f893331ed748dba020fe39cac503d604cbe2a1733` | evidence_or_analysis |
| E0312 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T2/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T2/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0312_fragments.txt) | `1a0661498f318ebeba7034ba808c6c3febd257868a46cf2457c310a819386345` | evidence_or_analysis |
| E0313 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T2/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T2/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0313_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0314 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T2/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy2_T2/settings.ini) | `6d389712144c2f00bcc5f8a4823065b1037c5c0d0e18cc71190b12e9aeb09b79` | evidence_or_analysis |
| E0315 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/report/cy2_native_reuse_acceptance_20260930.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/report/cy2_native_reuse_acceptance_20260930.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0315_cy2_native_reuse_acceptance_20260930.json) | `6b21f5ff3041dac3a579629ac7cfd89749b93ccc2c6fa0389bdf737a537d7d2e` | evidence_or_analysis |
| E0316 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/report/cy2_source_stability_acceptance_v2_a01_acceptance.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/report/cy2_source_stability_acceptance_v2_a01_acceptance.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0316_cy2_source_stability_acceptance_v2_a01_acceptance.json) | `2e798b38e03aa1843603cf27a22fdc76166dc5c29fa12191c9cd18db0a48eb49` | evidence_or_analysis |
| E0317 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_s0_endpoint_stability_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_s0_endpoint_stability_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0317_cy1_source_s0_endpoint_stability_v2_a01.case.json) | `afa790df87813191dc013b713dfdeeb682282ed256b36b5042dc4a3c22ebf356` | evidence_or_analysis |
| E0318 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/dispatch/submission_receipt.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/dispatch/submission_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0318_submission_receipt.json) | `901a2c7dea72b6fca869c915fd7094d8f54189303825570401a243ea82426156` | evidence_or_analysis |
| E0319 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_s0_endpoint_stability_v2_a01.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_s0_endpoint_stability_v2_a01.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0319_cy1_source_s0_endpoint_stability_v2_a01.com) | `3eab24660980be89176d780c79d0acf914f9bd95f750f2a7e0c6692dd36ddf7e` | input_or_analysis_code |
| E0320 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/endpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_optfreq_v2_a01/endpoint.chk) | `1cf95d4a8377ed4a445df49f349775085d205a8be033991efe6760630307a659` | evidence_or_analysis |
| E0321 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0321_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0322 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/parent.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_s0_endpoint_stability_v2_a01/parent.chk) | `1cf95d4a8377ed4a445df49f349775085d205a8be033991efe6760630307a659` | evidence_or_analysis |
| E0323 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_udft_t_endpoint_stability_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_udft_t_endpoint_stability_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0323_cy1_source_udft_t_endpoint_stability_v2_a01.case.json) | `5002f5329d205655caf086e019d94a5da8147b416d44fc90479d1a82e270bb2d` | evidence_or_analysis |
| E0324 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0324_submission_receipt.json) | `56a823556f5fcde32bdf0506c2fdd0f874902fa4461bbae7998b1ab98eeea5ab` | evidence_or_analysis |
| E0325 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_udft_t_endpoint_stability_v2_a01.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy1_source_udft_t_endpoint_stability_v2_a01.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0325_cy1_source_udft_t_endpoint_stability_v2_a01.com) | `93a2e153a68e831a9d67255f5988ecc938d7d3dbe89c3e233bacd328262ab33d` | input_or_analysis_code |
| E0326 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/endpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_optfreq_v2_a01/endpoint.chk) | `10abedd09382f3d70441cb0b61e30ee7076149afc44d037600f97163bfa11eed` | evidence_or_analysis |
| E0327 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stable.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stable.chk) | `e08a0b32183c8e19a5090370b6950122f5e0b568705746b6f80b5394c095ce42` | evidence_or_analysis |
| E0328 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0328_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0329 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/parent.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy1_source_udft_t_endpoint_stability_v2_a01/parent.chk) | `10abedd09382f3d70441cb0b61e30ee7076149afc44d037600f97163bfa11eed` | evidence_or_analysis |
| E0330 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy2_source_udft_t_endpoint_stability_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy2_source_udft_t_endpoint_stability_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0330_cy2_source_udft_t_endpoint_stability_v2_a01.case.json) | `978dd6c4a7c5fa884eb38a87c765c84705a9172ad2c85d66ef9877cc73e7bf83` | evidence_or_analysis |
| E0331 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0331_submission_receipt.json) | `556f5f567acb014262c00e7d1517c24c0e9c8ad984864fbe343092d88063da8c` | evidence_or_analysis |
| E0332 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy2_source_udft_t_endpoint_stability_v2_a01.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy2_source_udft_t_endpoint_stability_v2_a01.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0332_cy2_source_udft_t_endpoint_stability_v2_a01.com) | `234192ff2129f2f692e900d499cd5272d157fa53d5bc347dda13364b55181aae` | input_or_analysis_code |
| E0333 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/endpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_optfreq_v2_a01/endpoint.chk) | `eb7936dda63702e34979ace4d6221d02b6b0fea04205bf93bc6f5a228ee92bb0` | evidence_or_analysis |
| E0334 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stable.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stable.chk) | `4405be417557d33816fb31424cdc8997dd6f1d1e4c64b20fd2fa7525f51031d4` | evidence_or_analysis |
| E0335 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0335_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0336 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/parent.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_endpoint_stability_v2_a01/parent.chk) | `eb7936dda63702e34979ace4d6221d02b6b0fea04205bf93bc6f5a228ee92bb0` | evidence_or_analysis |
| E0337 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_s0_endpoint_stability_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_s0_endpoint_stability_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0337_ir780_source_s0_endpoint_stability_v2_a01.case.json) | `853ae96f0c231f579fce3459c74e53fbd705ca1b935ee16835eecba227ef71e4` | evidence_or_analysis |
| E0338 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/dispatch/submission_receipt.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/dispatch/submission_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0338_submission_receipt.json) | `e8735270740722127e76ead68ee2419667f082182bfe45063113bf0178a32906` | evidence_or_analysis |
| E0339 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_s0_endpoint_stability_v2_a01.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_s0_endpoint_stability_v2_a01.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0339_ir780_source_s0_endpoint_stability_v2_a01.com) | `c44d05d27baa2a5e943f9ad1ac454b0822a39c16bb52d3941fde5b3f195d7c84` | input_or_analysis_code |
| E0340 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/endpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_optfreq_v2_a01/endpoint.chk) | `5dc43d1bb9c5ef6d805c5d5c0fbbcdba0d024a6f5c66936fd1b9e9e551590a1a` | evidence_or_analysis |
| E0341 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0341_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0342 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/parent.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_s0_endpoint_stability_v2_a01/parent.chk) | `5dc43d1bb9c5ef6d805c5d5c0fbbcdba0d024a6f5c66936fd1b9e9e551590a1a` | evidence_or_analysis |
| E0343 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_udft_t_endpoint_stability_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_udft_t_endpoint_stability_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0343_ir780_source_udft_t_endpoint_stability_v2_a01.case.json) | `b7bbe0398ab69342d65e7f6dae4a38fb84035e13d273fb2efd7b0f89172695fb` | evidence_or_analysis |
| E0344 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0344_submission_receipt.json) | `7c95915bcaf80ad09b11b0ba344a36cd0500a94484e47f11d49af81f6adbfe03` | evidence_or_analysis |
| E0345 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_udft_t_endpoint_stability_v2_a01.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/ir780_source_udft_t_endpoint_stability_v2_a01.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0345_ir780_source_udft_t_endpoint_stability_v2_a01.com) | `f1ce5a662bc6c1260db0cd54132d57bcf51c51807259c73cfa23285ea839fa9e` | input_or_analysis_code |
| E0346 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/endpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_optfreq_v2_a01/endpoint.chk) | `e8057068056e0a447cf89bbd377afa4945cdb97cfd2524217819a80174744760` | evidence_or_analysis |
| E0347 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stable.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stable.chk) | `17c90c6f0a6b116d93e5cd61e83e65f833e901861a985ba0e566964a43f46423` | evidence_or_analysis |
| E0348 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0348_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0349 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/parent.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/ir780_source_udft_t_endpoint_stability_v2_a01/parent.chk) | `e8057068056e0a447cf89bbd377afa4945cdb97cfd2524217819a80174744760` | evidence_or_analysis |
| E0350 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_s0_endpoint_stability_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_s0_endpoint_stability_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0350_rubrene_source_s0_endpoint_stability_v2_a01.case.json) | `50b12fd9023e8db35ed3ccd54df86dd245ea57c81a231d2e341b8d747fb41152` | evidence_or_analysis |
| E0351 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/dispatch/submission_receipt.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/dispatch/submission_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0351_submission_receipt.json) | `74ea64a5e2fb265ac8e36e11362fe5987e37423d957bffdd0821dd94b3c7571c` | evidence_or_analysis |
| E0352 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_s0_endpoint_stability_v2_a01.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_s0_endpoint_stability_v2_a01.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0352_rubrene_source_s0_endpoint_stability_v2_a01.com) | `36aa61f82a55ac858db5dd1dbd23bad3bb8cc257075e6b3ec76b950e03df0918` | input_or_analysis_code |
| E0353 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/endpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_optfreq_v2_a01/endpoint.chk) | `e301169fb6e43df181606aca674ff7bcd340017322474917f9a0f0ccd8cae397` | evidence_or_analysis |
| E0354 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/stable.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/stable.chk) | `b51b56cf4daa3c2bc55ceac726d57beeeb0ee6fa2a7aa4c7ec044f66f805379e` | evidence_or_analysis |
| E0355 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0355_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0356 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/parent.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_s0_endpoint_stability_v2_a01/parent.chk) | `e301169fb6e43df181606aca674ff7bcd340017322474917f9a0f0ccd8cae397` | evidence_or_analysis |
| E0357 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_udft_t_endpoint_stability_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_udft_t_endpoint_stability_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0357_rubrene_source_udft_t_endpoint_stability_v2_a01.case.json) | `2bc598ffa2acf08d33431b8fcfae7eecff23bf9323c4893a4aaaf1b34b92e230` | evidence_or_analysis |
| E0358 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/dispatch/submission_receipt.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0358_submission_receipt.json) | `9e16ea6cc168f5e1d4b97daa771316cca33da16ba0a1ed9c169aadc7bade95f8` | evidence_or_analysis |
| E0359 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_udft_t_endpoint_stability_v2_a01.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/rubrene_source_udft_t_endpoint_stability_v2_a01.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0359_rubrene_source_udft_t_endpoint_stability_v2_a01.com) | `dd69c492376a75c830daf1fb55273e2e4acaf2886246119600f72d6a0ff591ca` | input_or_analysis_code |
| E0360 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/endpoint.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_optfreq_v2_a01/endpoint.chk) | `1577378e3845386836a91f344ad66336dbf863a02db6aa67f27d2331f9b3e11e` | evidence_or_analysis |
| E0361 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stable.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stable.chk) | `3327c2b6ac053dcfc45a79c52fa2c0a95b1ae9fb65816dc125aae14f82843ff0` | evidence_or_analysis |
| E0362 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0362_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0363 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/parent.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/rubrene_source_udft_t_endpoint_stability_v2_a01/parent.chk) | `1577378e3845386836a91f344ad66336dbf863a02db6aa67f27d2331f9b3e11e` | evidence_or_analysis |
| E0364 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0364_native_excerpt.json) | `5e372c4aa43bf2a9ab36e405c07e0212e2178412fd2319d00f9509f434443496` | native_output |
| E0365 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/stable.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/stable.chk) | `f9c56ed32cd691ef2b5f9b474575e3b0d7117106cfdd40e1747b428d83fb9837` | evidence_or_analysis |
| E0366 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0366_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0367 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/parent.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/parent.chk) | `33ef12842921a83f40487186337d1c0f97a96d57fe3df449c367c269b9e56acb` | evidence_or_analysis |
| E0368 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0368_input.com) | `3526fc84d7ab208083e36877a1de0adb47d1c9f47b0e327fba0c79d24986633e` | input_or_analysis_code |
| E0369 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy2_source_s0_stability_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy2_source_s0_stability_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0369_cy2_source_s0_stability_v2_a01.case.json) | `208933cab5d98571d89addb94b74b77ea61672ccad5c0d379b4829a8dcb6295d` | evidence_or_analysis |
| E0370 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_s0_stability_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0370_application_status.json) | `d192b951b0f7cbcf0638f50273be3316282e204d938f8c1a5e17483a5ea0568a` | evidence_or_analysis |
| E0371 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/stdout.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/stdout.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0371_native_excerpt.json) | `b15c905060e1a7e85cf1d8830e461899fe094d0635e6c7c3c29221d513c45c94` | native_output |
| E0372 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/stable.chk](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/stable.chk) | `54ebc564d5912c6bf0ef2dc529edfb50a8a5bc9989d2a4628287ff98ad48cc36` | evidence_or_analysis |
| E0373 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/stderr.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/stderr.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0373_native_excerpt.json) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | native_output |
| E0374 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/input.com](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/input.com)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0374_input.com) | `3940c450f220b85ee24d28e63851350e682e8c49a28d411518c5bb68803e2894` | input_or_analysis_code |
| E0375 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01.case.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/inputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01.case.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0375_cy2_source_udft_t_at_tdgeom_stability_v2_a01.case.json) | `56115f1476bf20dcbf90d46d8bb7b7967c3059496e5b05d566809c6219aab8ff` | evidence_or_analysis |
| E0376 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/application_status.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cy2_source_udft_t_at_tdgeom_stability_v2_a01/application_status.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0376_application_status.json) | `90d733026af3fb51755f5525d03e2ee31afde9dd569e67e97c0da2dc8a02d025` | evidence_or_analysis |
| E0378 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/v2_execution_20260929/code/cyanine_full_xy_response_basis_20261002.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/v2_execution_20260929/code/cyanine_full_xy_response_basis_20261002.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0378_cyanine_full_xy_response_basis_20261002.py) | `3ab02f657cc8bd7f9cea1717a5d1922510b62cd872fc00ecd221886c58833fcc` | input_or_analysis_code |
| E0379 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/v2_execution_20260929/code/cyanine_fragment_range_repair_20261002.py](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/v2_execution_20260929/code/cyanine_fragment_range_repair_20261002.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0379_cyanine_fragment_range_repair_20261002.py) | `ec1b64c919095824a2e7cfe1e193cd21920f0595a8c0d6313f9049497cd6a56b` | input_or_analysis_code |
| E0382 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/coefficients.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0382_coefficients.txt) | `70ae135c9dafb30444e7b01389aa3deeecfe483027d22cce2b13e028ae2dc7a3` | evidence_or_analysis |
| E0383 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_response_20261006_a01/output/singlet/response.fchk](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_response_20261006_a01/output/singlet/response.fchk) | `727baab5c4a7e9abcb5bf0996b828412488d6449bfb43881e6f3fbc94a3631c0` | evidence_or_analysis |
| E0384 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/fragments.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0384_fragments.txt) | `6d6a13dc15b9d6d848b94b8f5082cfc2187eb44373f9ba1ae3b9d2051cd5faba` | evidence_or_analysis |
| E0385 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/settings.ini](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/settings.ini) | `72a5732d23d7066048e373c3df25615b114b7518fab80d2190651b35ec088663` | evidence_or_analysis |
| E0386 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/Mulliken.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/Mulliken.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0386_native_excerpt.json) | `c065dfaec3871d1969d2216dafdf847d9c9e0881aec16011be957a5fe9d70dc4` | native_output |
| E0387 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/full_XY.npz](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/S1/full_XY.npz) | `1e759ae35c3ee4e36b9072675f4ecedea16d44072d1e9ce862f35eca6cf5cca9` | evidence_or_analysis |
| E0388 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/analyze_cy1_source.py](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/analyze_cy1_source.py)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0388_analyze_cy1_source.py) | `009e298964fecfce7015625e289ddb6547c95303a724c925b5bc8c3a9573de53` | input_or_analysis_code |
| E0389 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/coefficients.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0389_coefficients.txt) | `affd39ed188b17b6d2102b787d6d51351705e7ec654ff4a135ed6bb43f2fc864` | evidence_or_analysis |
| E0390 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_response_20261006_a01/output/triplet/response.fchk](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_response_20261006_a01/output/triplet/response.fchk) | `b67cbaa723db464eec73a59a98079032fe69ed15ccddd4827386884c19d3b517` | evidence_or_analysis |
| E0391 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/fragments.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0391_fragments.txt) | `6d6a13dc15b9d6d848b94b8f5082cfc2187eb44373f9ba1ae3b9d2051cd5faba` | evidence_or_analysis |
| E0392 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/settings.ini](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/settings.ini) | `72a5732d23d7066048e373c3df25615b114b7518fab80d2190651b35ec088663` | evidence_or_analysis |
| E0393 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/Mulliken.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/Mulliken.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0393_native_excerpt.json) | `3fbd40b59b98f57df7ba82ac2bbf7c016e0cb0d16b22914f9a9a495b07a26f6a` | native_output |
| E0394 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/full_XY.npz](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T1/full_XY.npz) | `fafbed35e824241883607731c62b9194676e2ee7afead5a2aa1a5ba3adf0c5b5` | evidence_or_analysis |
| E0395 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/coefficients.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0395_coefficients.txt) | `b12b6716b0acda4df350ec9c84c1dbfde08d2221092b8a68847584aff549c6dc` | evidence_or_analysis |
| E0396 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/fragments.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0396_fragments.txt) | `6d6a13dc15b9d6d848b94b8f5082cfc2187eb44373f9ba1ae3b9d2051cd5faba` | evidence_or_analysis |
| E0397 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/settings.ini](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/settings.ini) | `72a5732d23d7066048e373c3df25615b114b7518fab80d2190651b35ec088663` | evidence_or_analysis |
| E0398 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/Mulliken.log](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/Mulliken.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0398_native_excerpt.json) | `9562cdb9b755511935c96af50ca64b7f1c59ed5e6e127cb5e88ebc38a3a1e250` | native_output |
| E0399 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/full_XY.npz](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/papers/paper_e0791c047a731974/cases/cy1_si_s0_fixed_analysis_20261006_a01/output/T2/full_XY.npz) | `b300dce4760826a38c5e6f6a22c02e660693c497e6a5a17e15ec5729c7fcfa4e` | evidence_or_analysis |
| E0400 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_S1/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0400_native_excerpt.json) | `ae85ce6d0d3c59fe225a4d6de6d88a9b48c6dfe4cba316636968d94dfca8ea16` | native_output |
| E0401 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/full_XY.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/full_XY.npz) | `6ff1f6c6a0b3b0b0a766a1142c291ce4287bdf0978bee7b08045373e75e46a6d` | evidence_or_analysis |
| E0402 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/evidence.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/evidence.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0402_evidence.json) | `b5ed0dc52c6b4d6d60fca9f900ac7b71131aa19d9c925a6d20b95721bbdebb37` | evidence_or_analysis |
| E0403 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T1/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0403_native_excerpt.json) | `5edf5476d65fb12dccbe653bf02d7fb9d6bef8576cc92870db2257e3192689c8` | native_output |
| E0404 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/full_XY.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/full_XY.npz) | `8aac28badc16d58ce1c947f9d9dc4282bdf44fb955acfb28c7955e1907162c12` | evidence_or_analysis |
| E0405 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/evidence.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/evidence.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0405_evidence.json) | `2f26131e70429b27c6200dce405b54dedc4012a99fc483bf4a5dd3252b436aab` | evidence_or_analysis |
| E0406 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/multiwfn.log](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_fragment_range_repair_20261002_a01/Cy1_T2/multiwfn.log)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0406_native_excerpt.json) | `40fbf8c26209abb9402a4f492de872657bd13ad1a6b764447957777edd1b1c28` | native_output |
| E0407 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/full_XY.npz](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/full_XY.npz) | `cacd3dd06b2b5dbdcb4da6760a11c39c13656f8ee02b77199b34c4c621446031` | evidence_or_analysis |
| E0408 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/evidence.json](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/evidence.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0408_evidence.json) | `ac73792094e09fa7948aa8a171694902ba6d4fe108a4c26b2bf1123e19ebbf77` | evidence_or_analysis |
| E0409 | [docs/v2_verification/history/strict_author_route_validation_20261001/user_resolution_20261009T1305Z/INSTRUCTIONS.md](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/user_resolution_20261009T1305Z/INSTRUCTIONS.md)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0409_INSTRUCTIONS.md) | `72c994b53c1d7f7874500b5f6415a3d8ce502ef13f981340aadc8f39204425b9` | evidence_or_analysis |
| E0410 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/gaussian_gen.html](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/gaussian_gen.html) | `d694ce54fd27a764d11965aea5306fac87e9b90ef50f742e4fb23c23ed1ca73b` | evidence_or_analysis |
| E0411 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/gaussian_basis.html](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/gaussian_basis.html) | `937403a38bfdf2c314e5f275442beab67a94457fe1b141e7e8ea9f4f97243bc0` | evidence_or_analysis |
| E0412 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/multiwfn_download.html](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/multiwfn_download.html) | `748d0560fea9d37f7e1d5c40b4a217fa3f07a47ce996336d47b34c28aadeed97` | evidence_or_analysis |
| E0413 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/manual_3_8.pdf](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/manual_3_8.pdf) | `c3e0a5e3cc4a9baa277af05e2ac4d5e01257b2ebe3e07d80be39fca11f3e5cb2` | source_document |
| E0414 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/source_3_8.zip](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/source_3_8.zip) | `61a0e7701b98afd3c750c6a3a28454881480559d4e0b89d45ae4f0772eea6648` | evidence_or_analysis |
| E0415 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/source_current.zip](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/source_current.zip) | `f41d4023e08405fbd89f849e3fd4b40767e0de2583e291dcfc6797e45f3438e4` | evidence_or_analysis |
| E0416 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/gaussian_gen.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/gaussian_gen.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0416_gaussian_gen.txt) | `869620c5f1fe38650f20ed624d0b7d6a73f40d670cf5eae7abc3317dc2667f07` | evidence_or_analysis |
| E0417 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/gaussian_basis.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/gaussian_basis.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0417_gaussian_basis.txt) | `79eb0607a2ea8993950711dba5166f5e989354cfdd3e96c371ed8884b16cd49a` | evidence_or_analysis |
| E0418 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/source_3_8_selected/excittrans.f90](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/source_3_8_selected/excittrans.f90) | `40a1514f5111df8d17ae385bcb50f5497c053644c2337cb3cd92435bf4aa877e` | evidence_or_analysis |
| E0419 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/manual_3_8_relevant_pages.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/manual_3_8_relevant_pages.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0419_manual_3_8_relevant_pages.txt) | `a177e4e175f8a0d29b8cfcc9fcb137b910ecb29158c2f097a98f47c24f97c369` | evidence_or_analysis |
| E0420 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/source_3_8_selected_atmcontri_holeele_Mulliken.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/source_3_8_selected_atmcontri_holeele_Mulliken.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0420_source_3_8_selected_atmcontri_holeele_Mulliken.txt) | `cdda7603c5791d5f819f6728e0024a4c19fc5d623a4e41dfbb74256166d09cd4` | evidence_or_analysis |
| E0421 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/source_3_8_selected_atmcontri_holeele_Hirshfeld.txt](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/source_3_8_selected_atmcontri_holeele_Hirshfeld.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0421_source_3_8_selected_atmcontri_holeele_Hirshfeld.txt) | `e49bc23ab3f2edd865155d9003b30b52e352d393b3e0ed310de7d59a17f7ac00` | evidence_or_analysis |
| E0422 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/routine_comparison.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/routine_comparison.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0422_routine_comparison.json) | `d2762bafe41f3d15979e6c4d66bd90f4dab7c6c9454f5ba37ffc4a59e40a3abd` | evidence_or_analysis |
| E0423 | [docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/publication_metadata_recheck.json](../../../../docs/v2_verification/history/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W10/public_methods_20261007/publication_metadata_recheck.json)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0423_publication_metadata_recheck.json) | `6c5576e8c13f9100093b9b690b9c8c7fc656892e7a6f94e446e29f824480cd92` | evidence_or_analysis |
| E0424 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_S1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_S1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0424_coefficients.txt) | `ffaf28d958c0019c5bfbd44b422ca6a5772944629043979370fde8ac0012fe4e` | evidence_or_analysis |
| E0425 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_S1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_S1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0425_fragments.txt) | `c74ed06b28eed3f39482373ca9fd7bd5a88710dad5915ee6766faedc4019562f` | evidence_or_analysis |
| E0426 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_S1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_S1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0426_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0427 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_S1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_S1/settings.ini) | `60f96bbe29b9b8c791901b09bc66e205fe8eaf674bba73ff144b1c018b412a47` | evidence_or_analysis |
| E0428 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0428_coefficients.txt) | `7886216a100ecd33351476a74b426832f5031a060c0ae5bd5221db82433131a3` | evidence_or_analysis |
| E0429 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0429_fragments.txt) | `c74ed06b28eed3f39482373ca9fd7bd5a88710dad5915ee6766faedc4019562f` | evidence_or_analysis |
| E0430 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0430_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0431 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T1/settings.ini) | `60f96bbe29b9b8c791901b09bc66e205fe8eaf674bba73ff144b1c018b412a47` | evidence_or_analysis |
| E0432 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T2/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T2/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0432_coefficients.txt) | `f4239ca553d12c1ca5ae8ff168e16684bc3a76ce810e0a7f0caa831be4b1ce12` | evidence_or_analysis |
| E0433 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T2/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T2/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0433_fragments.txt) | `c74ed06b28eed3f39482373ca9fd7bd5a88710dad5915ee6766faedc4019562f` | evidence_or_analysis |
| E0434 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T2/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T2/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0434_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0435 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T2/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/IR780_T2/settings.ini) | `60f96bbe29b9b8c791901b09bc66e205fe8eaf674bba73ff144b1c018b412a47` | evidence_or_analysis |
| E0436 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0436_coefficients.txt) | `7706b75878d6850e5db9f581d8edb859596fc73542225e7d8a46471e80320a1a` | evidence_or_analysis |
| E0437 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0437_fragments.txt) | `2592a61af399e3dabf9c3cdab0cca4fcfc802e9255d7c0a74dba2d1e07a3dc46` | evidence_or_analysis |
| E0438 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0438_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0439 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_S1/settings.ini) | `60f96bbe29b9b8c791901b09bc66e205fe8eaf674bba73ff144b1c018b412a47` | evidence_or_analysis |
| E0440 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0440_coefficients.txt) | `87341a445e567f8e9d6785fc988309189e977b5bbad81960869e1c0da7bb9672` | evidence_or_analysis |
| E0441 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0441_fragments.txt) | `2592a61af399e3dabf9c3cdab0cca4fcfc802e9255d7c0a74dba2d1e07a3dc46` | evidence_or_analysis |
| E0442 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0442_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0443 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T1/settings.ini) | `60f96bbe29b9b8c791901b09bc66e205fe8eaf674bba73ff144b1c018b412a47` | evidence_or_analysis |
| E0444 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0444_coefficients.txt) | `53297b9f2df3fe4831bdd1175cc87a44a4facda43c21dd99b51af6ccb8f8572c` | evidence_or_analysis |
| E0445 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0445_fragments.txt) | `2592a61af399e3dabf9c3cdab0cca4fcfc802e9255d7c0a74dba2d1e07a3dc46` | evidence_or_analysis |
| E0446 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0446_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0447 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_response_basis_xy_repair_20261002_a01/Cy1_T2/settings.ini) | `60f96bbe29b9b8c791901b09bc66e205fe8eaf674bba73ff144b1c018b412a47` | evidence_or_analysis |
| E0448 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_S1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_S1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0448_coefficients.txt) | `8676f90191891c73cc2504149b6558b15bea7823aa12747dc2dbe03e84c3f24c` | evidence_or_analysis |
| E0449 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_S1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_S1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0449_fragments.txt) | `c18c550f248552f0238a33791bb70a615aee514474dffdbfa106a893cbd29899` | evidence_or_analysis |
| E0450 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_S1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_S1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0450_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0451 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_S1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_S1/settings.ini) | `60f96bbe29b9b8c791901b09bc66e205fe8eaf674bba73ff144b1c018b412a47` | evidence_or_analysis |
| E0452 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T1/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T1/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0452_coefficients.txt) | `be2f240f70fe5256781a6d94e1788711da0b8ae645b85a2b906cd50ea5458751` | evidence_or_analysis |
| E0453 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T1/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T1/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0453_fragments.txt) | `c18c550f248552f0238a33791bb70a615aee514474dffdbfa106a893cbd29899` | evidence_or_analysis |
| E0454 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T1/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T1/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0454_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0455 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T1/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T1/settings.ini) | `60f96bbe29b9b8c791901b09bc66e205fe8eaf674bba73ff144b1c018b412a47` | evidence_or_analysis |
| E0456 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T2/coefficients.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T2/coefficients.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0456_coefficients.txt) | `5f73ac90e8e2d23fd79c488f893331ed748dba020fe39cac503d604cbe2a1733` | evidence_or_analysis |
| E0457 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T2/fragments.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T2/fragments.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0457_fragments.txt) | `c18c550f248552f0238a33791bb70a615aee514474dffdbfa106a893cbd29899` | evidence_or_analysis |
| E0458 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T2/commands.txt](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T2/commands.txt)；[冻结副本](../../../../docs/v2_verification/papers/paper_e0791c047a731974/task_archives/autonomous_research/evaluation/verified_computation/snapshots/E0458_commands.txt) | `173a845a3c4b41ccdd1887dc4a626323b28ec37f2855e7294775602dc195672a` | evidence_or_analysis |
| E0459 | [docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T2/settings.ini](../../../../docs/v2_verification/history/upgrade_tasks_verification/group_5/papers/paper_e0791c047a731974/v2_execution_20260929/outputs/cyanine_full_xy_closeout_strict_v1_a01/Cy2_T2/settings.ini) | `60f96bbe29b9b8c791901b09bc66e205fe8eaf674bba73ff144b1c018b412a47` | evidence_or_analysis |
| N0417 | [tasks/v2_autonomous_research/paper_e0791c047a731974/evaluation/reference_key_points.json](reference_key_points.json) | `08d4634aa6ecf23b37f49f1f5ac9c5e35258cbe6af301a63625bea35bfa2e3e8` | latest_review_evidence |
| N0418 | [tasks/v2_autonomous_research/paper_e0791c047a731974/evaluation/reference_conclusions.json](reference_conclusions.json) | `21ff9fb7d3d239b44542bbd84222c0f1153e369de7f9705daf97134eca8f0eb5` | latest_review_evidence |
| N0419 | [tasks/v2_autonomous_research/paper_e0791c047a731974/evaluation/scoring_rules.json](scoring_rules.json) | `f1e9ad47cbfdef7de1192fae4fedfced9e78cad0a845c8f6e812b0300f0bb61a` | latest_review_evidence |
| N0420 | [tasks/v2_paper_reproduction/paper_e0791c047a731974/evaluation/reference_key_points.json](../../../v2_paper_reproduction/paper_e0791c047a731974/evaluation/reference_key_points.json) | `08d4634aa6ecf23b37f49f1f5ac9c5e35258cbe6af301a63625bea35bfa2e3e8` | latest_review_evidence |
| N0421 | [tasks/v2_paper_reproduction/paper_e0791c047a731974/evaluation/reference_conclusions.json](../../../v2_paper_reproduction/paper_e0791c047a731974/evaluation/reference_conclusions.json) | `21ff9fb7d3d239b44542bbd84222c0f1153e369de7f9705daf97134eca8f0eb5` | latest_review_evidence |
| N0422 | [tasks/v2_paper_reproduction/paper_e0791c047a731974/evaluation/scoring_rules.json](../../../v2_paper_reproduction/paper_e0791c047a731974/evaluation/scoring_rules.json) | `f1e9ad47cbfdef7de1192fae4fedfced9e78cad0a845c8f6e812b0300f0bb61a` | latest_review_evidence |
| N0423 | [docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/FINAL_VERDICTS.json) | `edd5067778bac91f780a18cb6f05836866847226282c1bb1419d08679c1a9269` | authoritative_current_review |
| N0424 | [docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json](../../../../docs/v2_verification/history/v2_strict_reaudit_20261014/root_results.json) | `3045e1e783ab41ea75b761599ea05ea0e0df1f8a9a6c1d65c3ca10bdd6daea91` | authoritative_current_review |

## 8. 本次整理的边界与冻结绑定

本轮只从已经完成的计算与正式复审提取过程，未提交计算、未删除结果、未更改公开任务及 evaluator。软件版本允许按已有政策使用本地版本，但所有已知残差保留。未记录的实际耗时、资源或作者私有参数写为未知，不自行补齐。

| 冻结文件 | SHA-256（整理前） |
|---|---|
| [tasks/v2_autonomous_research/paper_e0791c047a731974/agent_input/task.md](../agent_input/task.md) | `edcd22aa986f03f3e688ef7848f06d7895fdf9b0bf3a2ff36c5122605a4c5f83` |
| [tasks/v2_autonomous_research/paper_e0791c047a731974/evaluation/reference_key_points.json](reference_key_points.json) | `08d4634aa6ecf23b37f49f1f5ac9c5e35258cbe6af301a63625bea35bfa2e3e8` |
| [tasks/v2_autonomous_research/paper_e0791c047a731974/evaluation/reference_conclusions.json](reference_conclusions.json) | `21ff9fb7d3d239b44542bbd84222c0f1153e369de7f9705daf97134eca8f0eb5` |
| [tasks/v2_autonomous_research/paper_e0791c047a731974/evaluation/scoring_rules.json](scoring_rules.json) | `f1e9ad47cbfdef7de1192fae4fedfced9e78cad0a845c8f6e812b0300f0bb61a` |
| [tasks/v2_autonomous_research/paper_e0791c047a731974/evaluation/critical_failures.json](critical_failures.json) | `caa5c651b32eca1a18f49e9299ccc9c5f1e1dc9c96a2149e47290c1db2f3e70d` |
| [tasks/v2_autonomous_research/paper_e0791c047a731974/evaluation/evidence_map.json](evidence_map.json) | `2e20f8ca59b8674f4e0c43e1e922077946c8a36fecc2ac44cd5c3f35fa2530b1` |
| [tasks/v2_autonomous_research/paper_e0791c047a731974/evaluation/reference_validation_plan.md](reference_validation_plan.md) | `5fa774c073a34b74844f702cb1942d4fef3b25d2ed11a4cd007c85b223025040` |

## 2026-10-19 active paper_science_v2 scoring migration

The active private rubric assigns 100 points only to independent intermediate findings and final scientific conclusions, using binary leaves and no process score or multiplier. Historical criteria/weights above are archival, not active scoring. Public inputs and author-route contract remain byte-identical. Existing acceptance remains USER_ACCEPTED_DEVIATION; this migration is not new chemical validation. User-accepted residuals remain unresolved and do not become an independent strict pass. Fixed windows and retained boundaries are in scoring_rules.json and reference_qualification.json.


## 2026-10-19 Round3 scoring-contract repair

Historical verification statements above are preserved verbatim. Current mode-specific scientific rules supersede earlier scoring-policy wording; this append does not change the chemistry acceptance class.

- Removed B3LYP-only wording from three donor/rubrene sign leaves (13 points) and clarified actual method-equivalence criteria.
- No numeric targets or tolerances were widened. Historical Cy1 residual/user acceptance remains qualification metadata, not a submitter obligation.
- Audited every existing leaf for scientific role, source/verification support and physical definitions; retained unproven narrow-window risks as explicit provisional calibration limits rather than inventing wider tolerances.
