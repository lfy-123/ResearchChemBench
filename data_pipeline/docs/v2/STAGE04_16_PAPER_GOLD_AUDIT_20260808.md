# Stage04 16 篇论文人工金标审查

更新时间：2026-08-08

本审查逐篇阅读 Stage02 的正文与 SI 文本，核对论文实际执行的软件、核心工作流和当前
`toolbox_capabilities.json`。2026-08-08 根据工具箱三层结构修正金标：Stage04 只判断必要命名软件
是否存在于活动 backend catalog，不以预设 Action、adapter 参数或 runtime 验证状态作为覆盖边界。
资源是否可确认是独立维度。

判定语义：

- `core_software_uncovered`：已明确命名的必要程序、库、服务或扩展不在工具箱；
- `software_inventory_unconfirmed`：论文存在必要计算步骤，但没有说明其实现程序或代码；
- `covered`：所有必要命名软件均存在于当前工具箱；缺少预设 Action 时可由后续 Agent 阅读软件文档
  直接调用原生软件，或编写 Python 完成辅助处理。

| paper_id | 人工判定 | 实际软件和依据摘要 |
|---|---|---|
| `paper_03db136b9dfeeae1` | `software_inventory_unconfirmed` | 使用低能动量空间 continuum model 和 MHC rate model，但正文/SI 未命名实现程序。Fourier transform、Fermi function、voltage 均不是软件。 |
| `paper_1027f6b6495227bb` | `core_software_uncovered` | 反应路径和 RPA 明确使用 TURBOMOLE 7.5.1，另有 ORCA 5.0；TURBOMOLE 已从工具箱删除。 |
| `paper_229398bc7d4dd935` | `core_software_uncovered` | Gaussian16、CREST 可覆盖，但核心 NEO-DFT 使用 Molpro 2024.2；Molpro 已从工具箱删除。 |
| `paper_2d5323da0eb4aeee` | `covered` | Materials Project、VASP、TDEP 均在工具箱；HSE 和 Fourier interpolation 是方法/设置，不是缺失软件。预设 Action 是否覆盖 HSE 不属于 Stage04 判据。 |
| `paper_3d1ec7be672a5bac` | `core_software_uncovered` | NAMD、ORCA、xTB/Gaussian 可映射；QM/MM 必需 ChemShell、TURBOMOLE、DL_POLY，极化 MD 还使用 Tinker-HP，均未覆盖。 |
| `paper_4b4df409feb16caa` | `core_software_uncovered` | AMBER/Vina 可映射；核心 QM/MM 反应路径依赖 ChemShell、DL_POLY 和 TURBOMOLE，未覆盖。AmberFF19SB 和 MMPBSA/MMGBSA 是力场/方法，不是软件。 |
| `paper_576b22eb9fbcfdef` | `core_software_uncovered` | VASP 和 Allegro 可映射；增强采样 MD 明确依赖通用 ASE 与 PySAGES，当前仅有 `ase_emt`，无 PySAGES。AutoNEB/NEB 是算法。 |
| `paper_5b16a392cdac5456` | `software_inventory_unconfirmed` | DFT 数据由 VASP 生成，但论文核心线性/正则化回归模型没有命名实现库或代码。PAW 是方法。 |
| `paper_6797331f736c6743` | `covered` | 实际程序为 CP2K，已在工具箱；AIMD/metadynamics 可通过原生 CP2K 调用实现，缺少预设 Action 不构成 Stage04 拒绝。1D-MTD、Gaussian hills、revPBE 不是额外软件。 |
| `paper_67a927de6363bbb5` | `covered` | Gaussian 16 和 Multiwfn 均在工具箱；自定义 B3LYP*、TS/STQN、IRC 可在后续阶段通过原生软件接口评估，不属于 Stage04 软件缺失。 |
| `paper_70fb431035f2bf9a` | `software_inventory_unconfirmed` | DFT 明确使用 Quantum ESPRESSO；核心 ai-GCMC 表面生成算法未说明实现程序或代码，不能仅凭 QE 推断可执行。 |
| `paper_71e1f79eeb72bc40` | `core_software_uncovered` | AMBER、CP2K、Gaussian 可映射；核心 QM/MM 还依赖 ChemShell、TURBOMOLE、DL_POLY，未覆盖。QUICKSTEP/FIST 是 CP2K 模块。 |
| `paper_804bc3f1be133124` | `core_software_uncovered` | VASP、Phonopy、LOBSTER、VASPKIT、Materials Project 可映射；隐式溶剂核心计算明确依赖未提供的 VASPsol 扩展。 |
| `paper_921f3425c5e8797d` | `core_software_uncovered` | VASP 和 Phonopy 可映射；载流子输运/超快动力学核心步骤使用未覆盖的 PERTURBO。HSE/GW/BSE 是方法设置，不是额外软件。 |
| `paper_96a0a765d1651f87` | `core_software_uncovered` | VASP、Open Babel、RDKit 可映射；完整 CrystalDFT workflow 依赖通用 ASE、自研代码和 CrystalExplorer，未覆盖。 |
| `paper_b2ba8ce344632b5d` | `core_software_uncovered` | Quantum ESPRESSO 可映射；核心 WWL-GPR/EDT 和调参使用 Scikit-learn、Scikit-optimize 及自定义图核/微动力学实现，工具箱未覆盖。SOAP 是 descriptor。 |

人工金标汇总：

```text
core_software_uncovered:       10
software_inventory_unconfirmed: 3
covered:                        3
```

旧 Stage04 曾将 HSE、PAW、AutoNEB、Fourier transform 和 applied voltage 当成软件，又漏掉了
TURBOMOLE、Molpro、PERTURBO 等明确程序。r9 虽修复了软件实体识别，却错误地把预设 Action/adapter
约束当成整个三层工具箱的能力上限，因此又将 3 篇软件齐全论文误判为能力不足。r10 修正了该口径。

## 工具箱范围复核

Stage04 最终使用当前 `chemistry_toolbox` 生成的 150 actions / 92 backends 能力快照：

```text
profile_id:   researchchembench-toolbox-20260807-v2
catalog_hash: 2f8e8e58b6d7054833558715dbf7bde374ddc860d4423a094a1fd45248ac0103
```

Molpro、TURBOMOLE、TeraChem、Q-Chem 和 CASTEP 均不在 active backend 或 aliases 中；同步脚本还通过
`EXCLUDED_SOFTWARE` 强制排除这些名称。源码和第三方文档中出现这些名称，仅表示可读取对应输出格式、
历史移除记录或上游程序帮助文本，不构成可执行能力。运行
`scripts/sync_toolbox_capabilities.py --check` 已通过。

## 校准过程和最终结果

第一轮真实 r7 运行暴露了证据包、截断和软件/方法混淆问题，得到 `5 core uncovered / 1 capability /
9 inventory unconfirmed / 1 covered`。第二轮真实 r9 运行使用同一批 16 篇正文和 16 份 SI、Qwen3
30B-A3B、5 个 Softcite 实例及当前工具箱快照，0 篇发生服务错误，但有 1 篇双重截断、2 篇错误放行。
第三次只为截断论文执行极简模型重试，其余响应从审计 cache 回放。r9 当时按错误的 Action 边界得到：

```text
core_software_uncovered:       10
capability_constraints_unmet:   3
software_inventory_unconfirmed: 3
covered/passed:                 0
processing_failed:              0
按当时错误口径的人工标签一致率: 16/16
```

最终可审计产物位于：

`runs/v2_stage04_r9_gold_16_20260808_attempt5_final_replay/stage_04_toolbox_resource_gate/`

其中 `decisions.jsonl` 保留逐篇 workflow、软件证据、toolbox mapping 和模型审计信息；
`stage_summary.json` 记录上述最终汇总。`attempt5_final_replay` 明确表示复用已保存的真实 Qwen/Softcite
响应，仅重放当前清洗、映射和确定性决策代码，不代表重新调用了模型。

在确认三层工具箱语义后，r10 复用上述已人工核验的真实 Qwen/Softcite 软件抽取结果，只重放新的确定性
软件门控，得到：

```text
Stage04 软件覆盖维度：
core_software_uncovered:       10
software_inventory_unconfirmed: 3
covered:                        3

Stage04 最终 decision：
core_software_uncovered:       10
software_inventory_unconfirmed: 3
software_covered:               3
```

3 篇从 `capability_constraints_unmet` 修正为软件 `covered`：VASP-HSE、CP2K-AIMD/metadynamics 和
Gaussian 自定义 route 都可通过第二层原生软件调用，不应由 Stage04 淘汰。资源状态只保留为下游元数据，
不再改变 Stage04 的 pass/reject。r10 删除 exact Action、method constraint、runtime verification 和
资源门控，保留软件实体清洗、明确 executable cue、缺失软件优先、清单完整性和单篇失败隔离。

随后已使用 rlaunch H200 部署的 `Qwen3-30B-A3B-Instruct-2507` 对 16 篇执行 r10、r11 两轮全新调用。
r11 结果为 `3 software_covered / 10 core_software_uncovered / 3 software_inventory_unconfirmed`，逐篇
16/16 匹配本页修正后的人工金标；16 次请求均非 cache replay。完整设置和问题分析见
`STAGE04_DEPLOYED_QWEN_VALIDATION_20260808.md`。
