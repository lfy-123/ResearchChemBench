# Second expert review — 2026-10-28

The withdrawing-substitution conclusion now explicitly covers the already-public compound 2 versus 3 comparison, using assigned optical shifts and electronic reordering. No new molecule, numerical target, tolerance or separate ranking score is introduced. Source prose/SI conflicts and the small 1-to-4 baseline split remain documented. No new scientific calculations were run.

# V3 final-result evidence reuse — 2026-10-28

Same four complete neutral-singlet B2N6 derivatives and DCM absorption explanation, with identical AR/PR final quantities and weights. Experimental absorption is already disclosed; the scored new results are physical transition assignments and computed substitution explanations.

r_bright_character_c1/c2/c3/c4 reuse the native configuration/spatial join: C1 3.1216 eV/f0.3326, C4 3.1242/f0.5044, C3 3.4533/f0.3831 and C2 3.8445/f0.4733 with N6-localized transitions. r_methyl_toly_substitution reuses unequal orbital responses and a 0.0026 eV baseline shift; r_withdrawing_substitution reuses the N6 occupied-state reordering and C3/C2 higher-energy bright transitions. Original active V2 had no numeric windows; V3 does not introduce or restore historical windows. Supplied experimental ordering is context within the explanation, not an independent prediction score.

Limitations: Historical acceptance is ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION under the prior authorization, not exact quantitative reproduction. C1 differs from SI by +0.1097 eV and C4−C1 is 0.0026 versus 0.1101 eV. Main prose 3.52/3.97/4.33 eV conflicts with SI 3.0119/3.4440/3.8436 eV. Optional no-D3 and broadening diagnostics can reverse/merge the small C1/C4 separation; this does not establish a robust resolved experimental splitting or full solvent speciation.

The current policy is paper_science_v3 / final_results_100. The text below is an unchanged historical record; its old policies, scores and PASS labels are not current V3 certification. No new calculation was run.

---

# 当前计算验证与科学分V2参考 — 2026-10-20

验收类型：**ACCEPTED_QUALITATIVE_WITH_NUMERICAL_DEVIATION**。当前冻结任务范围的必要定性节点、重要披露方法与有效计算已获协调确认；formal_scoring_permitted=true。当前评分为paper_science_v2，二元叶子总分100，无过程分。此验收不声称原数值容差已通过，不承诺全部源表或整篇实验精确复现。出版/专家复核与运行评分资格分开。

## 当前科学范围与对象

Four source molecular identities, absorption ordering and N6 electronic-structure interpretation in DCM; source assigned transitions rather than arbitrary first roots or added broadening conventions.

- source: Gaussian16C.01; B3LYP-D3BJ/6-31+G(d), SMD DCM; source nominated bright statesC1S1,C4S1,C3S5,C2S5.
- native: Same program revision and disclosed functional,dispersion,basis,solvent; full neutral structures including four covalent OTf groups in compound2; six baseline endpoints valid.
- version: Gaussian16C.01 matches source; no version substitution needed.
- source_conflict: Main prose energies3.52/3.97/4.33eV conflict with SI tabulated transitions; both retained and no root renaming used.

## 实际计算验证过程与关键节点

1. Validate all four complete neutral singlets; compound2 includes four covalent triflate groups.
2. Perform B3LYP-D3BJ/6-31+G(d), SMD DCM geometry/baseline response calculations in Gaussian16C.01; six accepted baseline endpoints include compound2 basin alternatives.
3. Read complete printed configurations and spatial N6 partitions. Source-relevant C1S1/C4S1/C3S5/C2S5 are chosen by physical character, not source-number closeness.
4. Compare energies, oscillator strengths and source assignments. Retain SI tabulated values as the explicit stick-spectrum definition while recording incompatible main prose.
5. Keep optional noD3 and added broadening/basin controls separate. They bound robustness but do not replace the disclosed baseline.

所有以下记录复用真实既有计算；本次迁移不启动量子化学/HPC任务，不拟合参考值或容差。版本差异依既有授权，不自动视为误差来源或数值准确度证据。

## 论文值、实际值与偏差

差值定义为native−source；绝对偏差另列。表中为实数减法汇总，无新科学模拟。相对误差对近零能隙、位移或不同实验/理论口径可能误导，未机械计算。无数值评分叶子，表值不形成隐藏容差门。

| 量 | 论文值 | 实算值 | 有符号差 | 绝对差 | 单位 / 定义 |
|---|---:|---:|---:|---:|---|
| C1 nominated bright E | 3.0119 | 3.1216 | 0.1097 | 0.1097 | eV / C1/C4:S1;C3/C2:S5 physical transition |
| C1 nominated bright f | 0.3456 | 0.3326 | -0.0130 | 0.0130 | dimensionless / Same physical transition |
| C4 nominated bright E | 3.122 | 3.1242 | 0.0022 | 0.0022 | eV / C1/C4:S1;C3/C2:S5 physical transition |
| C4 nominated bright f | 0.5223 | 0.5044 | -0.0179 | 0.0179 | dimensionless / Same physical transition |
| C3 nominated bright E | 3.444 | 3.4533 | 0.0093 | 0.0093 | eV / C1/C4:S1;C3/C2:S5 physical transition |
| C3 nominated bright f | 0.387 | 0.3831 | -0.0039 | 0.0039 | dimensionless / Same physical transition |
| C2 nominated bright E | 3.8436 | 3.8445 | 0.0009 | 0.0009 | eV / C1/C4:S1;C3/C2:S5 physical transition |
| C2 nominated bright f | 0.4243 | 0.4733 | 0.0490 | 0.0490 | dimensionless / Same physical transition |
| C4−C1 bright energy gap | 0.1101 | 0.0026 | -0.1075 | 0.1075 | eV / Direction retained; no minimum required separation |

## 额外实际结果与未复现项

- Bright-state energies C1,C4,C3,C2：source=[3.0119, 3.122, 3.444, 3.8436]；native=[3.1216, 3.1242, 3.4533, 3.8445]；Source-nominated roots S1,S1,S5,S5
- Bright-state oscillator strengths C1,C4,C3,C2：source=[0.3456, 0.5223, 0.387, 0.4243]；native=[0.3326, 0.5044, 0.3831, 0.4733]；Same source-nominated bright-state comparison
- Compound2 other source basins：source="Same compound2 identity"；native={"E": [3.8138, 3.8208], "f": [0.4255, 0.4292]}；Basin variation retains ordering relative to C3
- 1→4 bright-state gap：source=0.1101；native=0.0026；Same direction with smaller magnitude; no-D3 diagnostic gap−0.0032eV is separately labeled

## 定性关键节点与仍有边界

- Full identity and chemical state：SUPPORTED: four neutral singlets; compound2 is not modeled as an incomplete bare ion.
- Absorption ordering and substitution response：SUPPORTED on disclosed baseline: E1<E4<E3<E2; all three compound2 basins remain above compound3.
- Compound1→4 blue shift：SUPPORTED in sign: source0.1101eV versus native0.0026eV. Magnitude mismatch retained; no robustness claim beyond baseline.
- Transition mechanism and spatial orbital assignment：SUPPORTED:1/4 H→L and2/3 H−4→L; configuration/spatial N6 evidence aligns with source explanation.
- Calculation validity and correspondence：SUPPORTED: baseline endpoints complete with actual native route readback; source nominated physical states retained, not selected by numeric proximity.
- Source inconsistency and diagnostic sensitivity：BOUNDED: SI/prose discrepancy, basin dependence and broadened1/4 near-overlap are disclosed; optional diagnostic reversals do not change the nominated baseline result.
- Main prose3.52/3.97/4.33eV differs from SI tabulated3.0119/3.4440/3.8436eV. The SI includes explicit states and f/configuration definitions, so those define the table comparison.
- Source1→4 gap .1101eV becomes .0026eV but does not reverse on the disclosed baseline.
- Added broadenedC1/C4 maxima overlap or interchange; no-D3 gap−.0032eV is a separate diagnostic, not the author baseline.
- Computed broadenedC1 maxima396.6225–397.1307nm andC4 approximately396.8764nm may overlap or interchange for added kernels. Acceptance is not a claim that every chosen broadened maximum preserves a resolvable1/4 split.
- Experimental maxima C1/C2/C3/C4=418/354/379/409nm are not relabeled as calculated sticks.
- No unreported ordinary Gaussian default or optional noD3 control is made a new rejection requirement.

## 原生输入/输出与验证分析位置

以下路径为仓库/服务器真实文件，hash为2026-10-20独立重读值。正常终止只作为执行证据；对象、状态、频率/曲率、响应定义仍是科学资格前提。

- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_46f6118697c6397c/cases/reopen20261011_B2_remaining_budget_repair03/compound4/noD3_TD12.com`；SHA256 `f775cf5862a95d253e4b413d983565efcb3042b88a497a447cfc0124afb9c822`；input；normal_marker=None
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_46f6118697c6397c/cases/reopen20261011_B2_remaining_budget_repair03/compound4/noD3_TD12.log`；SHA256 `61bfd7404998ef854d15ec1df1d24a76e5b3d2dade6f3321ffe5acae7ebd952e`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_46f6118697c6397c/outputs/v2_compound1_source_basin1_TD30/attempt_001/input.com`；SHA256 `23ee82e4a87565a8b48eec24a8394183a68465c2b6ea837a0c1ac442fbf6895f`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_46f6118697c6397c/outputs/v2_compound1_source_basin1_TD30/attempt_001/stdout.log`；SHA256 `87db0085223b7da058fe6e6b8b34e9646f116f8a3c17beef4be05945377a48e7`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_46f6118697c6397c/outputs/v2_compound3_source_basin1_TD30/attempt_001/input.com`；SHA256 `a3bcff83a4ecf4624e2551522adeefab71897bee46a328729b06f2adabad24b3`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_46f6118697c6397c/outputs/v2_compound3_source_basin1_TD30/attempt_001/stdout.log`；SHA256 `82b8b45dd06b2abf0f6becb045cc831451b7c08b6d3d32d810164b39eb93bf98`；native_output；normal_marker=True
- `docs/upgrade_tasks_verification/group_2/papers/paper_46f6118697c6397c/outputs/v2_compound4_source_basin1_TD30/attempt_001/input.com`；SHA256 `87c02f012d7f3f557b148867b17da4cc74bbea44081aa5dc36192fb0f7fa6a86`；input；normal_marker=None
- `docs/upgrade_tasks_verification/group_2/papers/paper_46f6118697c6397c/outputs/v2_compound4_source_basin1_TD30/attempt_001/stdout.log`；SHA256 `b5db0db21c29565c2f206b8cfda70ee5d8890bb64b5954cd3801fce17a74339b`；native_output；normal_marker=True
- `docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B1_op2_td50_20260912T064210Z/input.com`；SHA256 `b26ba7c7a408209578c02b1d1ee0b164070de394ba7cd38a9b25dea6a2953b42`；input；normal_marker=None
- `docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B1_op2_td50_20260912T064210Z/stdout.log`；SHA256 `48465beb01f3aa0b36fd2364cca277f2f35936850d928382cb4293bf4300125f`；native_output；normal_marker=True
- `docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_A_op5_td50_hpc20_20260910T022113Z/input.com`；SHA256 `66bef65d89881941ed5af6264b773e4387cd1edce20e51a4c5049c88a4239a97`；input；normal_marker=None
- `docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_A_op5_td50_hpc20_20260910T022113Z/stdout.log`；SHA256 `8f0d1b32a6b6ad6e219281b1a6a5e75fcc44b20f251a84338a8fa4552151343d`；native_output；normal_marker=True
- `docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_B_op5_td50_hpc20_20260910T022118Z/input.com`；SHA256 `064f1af69b36c3a4d9c60c156c3f745ea19542ab20e1fd987efc74d3ff9001a5`；input；normal_marker=None
- `docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_B_op5_td50_hpc20_20260910T022118Z/stdout.log`；SHA256 `78411c72bd5af31ba9702a019fb69aa2ac3423de6e970731a0cf0432270acde7`；native_output；normal_marker=True

验证汇总/实际源页与分析：

- `docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_46f6118697c6397c/ROUTE_ALIGNMENT.json`；SHA256 `02e3a7a3ec1c569c97747d45e32633da5fba0a81867797bedf8add96cb4c876b`
- `docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_46f6118697c6397c/ACTUAL_INPUT_READBACK.json`；SHA256 `c3c0956d0d752fa06472a7277320f0059f2cb57af0118db4db41462cdaff8541`
- `docs/strict_author_route_validation_20261001/parallel_blockers_20261005T090259Z/workers/W02/papers/paper_46f6118697c6397c/SOURCE_NATIVE_JUDGMENT.json`；SHA256 `b74ace8cf980eb95681600091bb973d9a25a441f911598d8b555d5d3cdf18dc7`
- `docs/upgrade_tasks_verification/group_2/v2_execution_20260929/native_acceptance/b2_all12_configuration_spatial_join.json`；SHA256 `556f2889de6c694ff72ea86b16f1f64807ca18d534c2e84d798f47e72c43ade0`
- source_orbitals：{"path": "papers/paper_46f6118697c6397c/documents/main.pdf", "sha256": "4633e67606dc23badd9f553b89ec95d96540bd4fa637876897ae830a4e31901c", "pdf_pages_1based": [3, 4], "locator": "Fig4 and N6/substituent orbital interpretation"}
- source_c1：{"path": "papers/paper_46f6118697c6397c/documents/supplementary_001.pdf", "sha256": "d25723e53953f2a507b014af89f62abe1f1c229886d0090fd80943b24dd21cfa", "pdf_pages_1based": [16, 17], "locator": "Computational methods, FigS20, TableS2"}
- source_c2：{"path": "papers/paper_46f6118697c6397c/documents/supplementary_001.pdf", "sha256": "d25723e53953f2a507b014af89f62abe1f1c229886d0090fd80943b24dd21cfa", "pdf_pages_1based": [18, 19, 20], "locator": "FigS22, TableS3 and compound2 spectrum"}
- source_c3：{"path": "papers/paper_46f6118697c6397c/documents/supplementary_001.pdf", "sha256": "d25723e53953f2a507b014af89f62abe1f1c229886d0090fd80943b24dd21cfa", "pdf_pages_1based": [21, 22], "locator": "FigS24, TableS4"}
- source_c4：{"path": "papers/paper_46f6118697c6397c/documents/supplementary_001.pdf", "sha256": "d25723e53953f2a507b014af89f62abe1f1c229886d0090fd80943b24dd21cfa", "pdf_pages_1based": [23, 24], "locator": "FigS26, TableS5"}

## 时间与资源记录

本次迁移新增科学计算数0、HPC作业数0。历史输出中记录的逐作业资源可按原生/执行记录核查；没有统一完整的四篇总walltime、CPU-hour或费用记录，本报告不从核数或日志数量推算。失败、历史固定几何及控制计算不混入成功基线。

## 当前评分边界

中间科学结果70分；最终综合推断30分；全部定性叶子，满分或0。无精度充分校准的通用吸收/位移/结合能窗口，本轮不以最大残差拟合容差。身份、状态和证据是各项前提，不单独奖励。AR/PR具有相同物理判分清单；PR复现合同及合理替代义务仍由原题面约束，AR不被要求采用验证软件或固定搜索轨迹。

## 逐项科学规则—实际证据对应

下表明确本次验证对各项的支持，不使未来Agent自动获分。未来提交仍须独立有效证据。

| Rule / role / score | 实算支持 | 定位 |
|---|---|---|
| r_bright_character_c1 / intermediate / 10 | C1: E=3.1216eV,f=0.3326, H→L; printed configuration joined to spatial N6 occupied/virtual partitions. | b2_all12_configuration_spatial_join.json/rows |
| r_bright_character_c2 / intermediate / 10 | C2: E=3.8445eV,f=0.4733, H−4→L; printed configuration joined to spatial N6 occupied/virtual partitions. | b2_all12_configuration_spatial_join.json/rows |
| r_bright_character_c3 / intermediate / 10 | C3: E=3.4533eV,f=0.3831, H−4→L; printed configuration joined to spatial N6 occupied/virtual partitions. | b2_all12_configuration_spatial_join.json/rows |
| r_bright_character_c4 / intermediate / 10 | C4: E=3.1242eV,f=0.5044, H→L; printed configuration joined to spatial N6 occupied/virtual partitions. | b2_all12_configuration_spatial_join.json/rows |
| r_energy_c1_below_c4 / intermediate / 10 | 3.1216<3.1242eV for physical nominated bright transitions. | SOURCE_NATIVE_JUDGMENT.json; b2_all12_configuration_spatial_join.json |
| r_energy_c4_below_c3 / intermediate / 10 | 3.1242<3.4533eV for physical nominated bright transitions. | SOURCE_NATIVE_JUDGMENT.json; b2_all12_configuration_spatial_join.json |
| r_energy_c3_below_c2 / intermediate / 10 | 3.4533<3.8445eV for physical nominated bright transitions. | SOURCE_NATIVE_JUDGMENT.json; b2_all12_configuration_spatial_join.json |
| r_methyl_toly_substitution / conclusion / 15 | N6-localized physical orbitals/configurations plus C4−C1=.0026eV support baseline direction; optional noD3−.0032 and overlapping broadened maxima bound robustness. | SOURCE_NATIVE_JUDGMENT.json; b2_all12_configuration_spatial_join.json |
| r_withdrawing_substitution / conclusion / 15 | C3/C2 N6 bright channels are H−4→L with benzyl-localizedHOMO alternative; spatial/configuration evidence and E3<E2 support substituent-dependent reordering. | b2_all12_configuration_spatial_join.json; SOURCE_NATIVE_JUDGMENT.json |

## 历史验证原文（保留；非当前验收/评分状态）

### 历史文件 docs/final_verified_science_v2_additions_20261020/astra_science_02/archive/paper_reproduction/paper_46f6118697c6397c/evaluation/legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot

# 已验证成功计算链：compound 2 三分支 TD50

- 论文 ID：`paper_46f6118697c6397c`
- 本任务模式：`paper_reproduction`（论文复现模式）
- 论文 DOI：`10.1039/d5dt02896e`
- 归档日期：2026-09-16（历史验证完成日期以原始记录为准）
- 验证来源：[group_2](../../../../docs/verification/group_2/paper_46f6118697c6397c)；[本组通过清单](../../../../docs/verification/all_verified_tasks/group_2.md)
- 最新已归档科学状态：作者路线完成，三条 CIF 派生分支及 evaluator 数值/跃迁指认审计通过。
- 2026-09-17 最终包审查通过；当前目录/审批状态：已按负责人授权迁入 `final_verified_paper_reproduction`。该状态适用于本包声明的科学范围；部署访问隔离仍需单独确认。

## 1. 本文件用途与任务版本

本文件记录已经真实完成、被最新作者路线审计采纳的计算步骤和结果，不是新增计算，也不是评估评分规则。评分仍由本目录下 `critical_failures.json`、`evidence_map.json`、`reference_conclusions.json`、`reference_key_points.json`、`scoring_rules.json` 决定。本文件及其链接中的作者结构、数值答案均属于 evaluator 侧资料，不能作为 agent 输入。

本任务的入库基线已保存于 Git `e67441a9`；格式整理检查点为 `42970e03`。来源为 [canonical 源任务](../../../paper_reproduction/paper_46f6118697c6397c)，后续维护只调整本副本，不覆盖原始验证记录。本文件归档历史真实计算；包的现行指令、输入和 evaluator 应按维护后的版本核对，不能把“入库时原样复制”理解成此后从未修改。

验证者允许知道正文/SI 的作者路线，并可用作者结构作为验证起点。验证的含义是：相应科学子问题已有真实计算支持；不是要求当时验证过程模拟待评 agent 的信息受限探索，也不是将私有作者 endpoint 重新提供给 agent 的授权。本模式记录作者子路线的科学可计算性；不把它扩大为整篇论文复现或自主 agent 盲测通过。

## 2. 真实有效的计算流程

1. 从 CCDC 2512981 的 compound 2 CIF 出发，按预处理档案执行对称性展开（含 2_655/5 对称操作）并分别处理无序，得到 B1_op2、B2_A_op5、B2_B_op5 三条分支；补氢后各为完整 68 原子 C18H14B2F12N6O12S4、中性单重态，保留四个 triflate 配体，不能将无序分支错误拼接或删去配体。

2. 使用 Gaussian 16 C.01，在 B3LYP-D3(BJ)/6-31+G(d)、SMD 二氯甲烷下分别执行三分支 Opt/Freq。三条均正常终止，各有 198 实频、0 虚频。

3. 将每条真实优化末态逐一用于同方法/溶剂的 TD-DFT 50 singlets 计算，保留所有状态的能量、振子强度和主要轨道展开。

4. 三分支最大振子强度均位于第 5 单重激发态。历史报告在三条分支中选择第 5 态能量最低的 B2_A_op5 作代表；这是当时的报告选择，不是当前 task 强制的筛选规则。三分支的该态能量和强度均在现行容差内，也不意味着 B2_A_op5 的基态电子能全局最低。

5. 读取所选第 5 态的 217→222 主贡献（系数 0.70257，当前编号对应 HOMO−4→LUMO），结合归档轨道分析给出 N6 相关近紫外跃迁指认，逐项对照参考能量/强度、关键点和结论。

## 3. 实际结果与支持的结论

| 分支 | 第 5 态能量 / eV | 振子强度 f |
|---|---:|---:|
| B1_op2 | 3.8445 | 0.4733 |
| B2_A_op5（代表） | 3.8138 | 0.4255 |
| B2_B_op5 | 3.8208 | 0.4292 |
| evaluator 参考 | 3.8436 ± 0.15 | 0.4243 ± 0.05 |

代表分支误差为 0.0298 eV、0.0012；支持任务所需 compound 2 主导近紫外激发及其跃迁指认；第 5 态是本方法三分支中实际得到的编号，不是对任意程序/方法强加的固定序号。

## 4. 原始输入与输出索引

下表按有效链列出原始输入/命令及日志。多个 `Normal termination` 通常对应组合输入中的多个计算段，不等于多个独立体系。正常终止标记只是执行证据，科学判断同时依赖上文频率、身份、数值及下文专门审计。成功重提作业可作为证据；失败尝试不列为有效步骤。

| 阶段 | 原始输入/命令/波函数 | 原始输出 | 执行证据与限定 |
|---|---|---|---|
| compound2_B1_op2_optfreq | [input.com](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/compound2_B1_op2_optfreq_local_migration_20260904T155532Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/compound2_B1_op2_optfreq_local_migration_20260904T155532Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| author_compound2_B2_A_op5_b3lyp_d3bj_631pgd_optfreq | [input.com](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_A_op5_b3lyp_d3bj_631pgd_optfreq_local_migration_20260905T022637Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_A_op5_b3lyp_d3bj_631pgd_optfreq_local_migration_20260905T022637Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| author_compound2_B2_B_op5_b3lyp_d3bj_631pgd_optfreq | [input.com](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_B_op5_b3lyp_d3bj_631pgd_optfreq_local_migration_20260904T223914Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_B_op5_b3lyp_d3bj_631pgd_optfreq_local_migration_20260904T223914Z/stdout.log) | Gaussian 正常终止标记 2 处；有优化收敛标记 |
| author_compound2_B1_op2_td50 | [input.com (1)](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B1_op2_td50_20260912T064210Z/input.com)<br>[source_input.com (2)](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B1_op2_td50_20260912T064210Z/source_input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B1_op2_td50_20260912T064210Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| author_compound2_B2_A_op5_td50 | [input.com](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_A_op5_td50_hpc20_20260910T022113Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_A_op5_td50_hpc20_20260910T022113Z/stdout.log) | Gaussian 正常终止标记 1 处 |
| author_compound2_B2_B_op5_td50 | [input.com](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_B_op5_td50_hpc20_20260910T022118Z/input.com) | [stdout.log](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/qzcli_hpc/author_compound2_B2_B_op5_td50_hpc20_20260910T022118Z/stdout.log) | Gaussian 正常终止标记 1 处 |

## 5. 后处理、结果与逐项核验依据

- [provenance/author_route_evaluation_audit.json](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/author_route_evaluation_audit.json)
- [provenance/compound2_cif_preprocessing.json](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/compound2_cif_preprocessing.json)
- [report/results.json](../../../../docs/verification/group_2/paper_46f6118697c6397c/report/results.json)
- [verification_report.md](../../../../docs/verification/group_2/paper_46f6118697c6397c/verification_report.md)
- [provenance/prepare_compound2_from_cif.py](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/prepare_compound2_from_cif.py)
- [provenance/advance_46_tddft.py](../../../../docs/verification/group_2/paper_46f6118697c6397c/provenance/advance_46_tddft.py)

以上脚本/输入仅作为历史流程索引，不要求本次重新运行。总报告可能保留早期失败或旧状态；应以本文件明确选定的原始成功输出、最新专门审计和正式结果为准，不将旧尝试混入成功链。

## 6. 保留的科学与记录边界

- CIF 对称展开和无序处理是验证流程的必要步骤，不能把晶体中不完整 asymmetric unit 直接当作完整计算分子。
- 基态局部极小值、有限三分支与溶液连续介质模型不等于晶体堆积/全构象空间验证。
- 轨道绝对编号随程序/模型变化，评价应保留轨道性质与 HOMO−4→LUMO 映射，不把 217/222 当通用常数。

## 7. 成功阶段计时

六条成功 Opt/Freq/TD 作业的逐项时间可在原始日志及 HPC 摘要中查询；不把平台汇总时间直接称作应用 CPU 时间。

本次归档没有提交、重启或停止任何计算作业。

## Evidence scope review (2026-09-19)

The recorded excitation energy, oscillator strength and configurations support the scalar results. Complete coverage of the N6-localization assertion additionally requires retrievable same-state spatial/population evidence. An MO number is not such evidence. This revision does not certify that missing assertion or rerun TD calculations.

