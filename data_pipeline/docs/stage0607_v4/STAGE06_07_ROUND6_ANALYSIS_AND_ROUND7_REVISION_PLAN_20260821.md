# Stage06/07 第六轮扩大测试分析与第七轮修改方案

日期：2026-08-21
基线提交：`b1fff7e`
测试目录：`runs/stage06-07-v4-round6-deepseek20-concurrency10-20260821`

## 1. 对照迭代目标

本轮重新对照 `STAGE06_07_ITERATION_OBJECTIVES_AND_ACCEPTANCE_CRITERIA_20260821.md`，重点检查：科学目标与范围、输入和评分闭合、双模式边界、机械误报、`task.md` 唯一指令源、代码/Prompt/模型能力归因，以及是否需要 Stage07B。

## 2. 测试配置与统计

- 模型：`deepseek-v4-pro-0813`
- Harness：Codex
- 并发数：10
- 样本数：20，抽样记录见 `STAGE06_07_ROUND6_TEST_SELECTION_20260821.md`
- CLI 完成：20/20，退出失败：0
- Stage06 constructed：20
- 进入 Stage07：20
- Stage07 科学批准：19
- Stage07 科学/客观失败：1
- 机械通过：18
- 机械阻断：1
- 实际发布：18

## 3. 逐篇结果

| 论文 | 任务方向 | Stage07/机械结果 | 质量结论 |
|---|---|---|---|
| `03455526` | 两条环加成分支自由能垒比较 | 批准/通过 | 目标聚焦，输入、分支比较和结论链完整。 |
| `09c8aaf1` | E/Z 异构化能量剖面与 TS | 批准/通过 | 气相/乙腈边界和 TS 验证明确。 |
| `0f779cb0` | 芳基自由基 VIE/EA/反应性与产率关联 | 批准/通过 | 指标链丰富；Stage07完成了交付和评分绑定修复。 |
| `108e6a1f` | Pd 氧化加成区域异构体与 UV-Vis | 批准/通过 | 热力学与光谱交叉验证合理。 |
| `23ab5e60` | 部花青前线轨道与吸收归属 | 批准/通过 | 存在方法自由与 PM6/COSMO 紧数值 GT 冲突；`task.md` 还引用 `task_spec.json`。 |
| `298959ea` | N2/N2H2/N2H4 键长、频率、Mayer 键级 | 批准/通过 | 方法约束型比较目标清楚。 |
| `3e2d7e83` | 硫氧亚胺酰氯反应综合 DFT 路线 | 批准/通过 | 完整核心路线，依赖和多个中间结论较完整。 |
| `4ee9947f` | ZnO 水层周期 DFT 与 NMR 指认 | 批准/通过 | 路线校准常数 `29.02 ppm` 可公开，不属于评分答案。 |
| `56da7f95` | 配体结构、振动、前线轨道与静电区域 | 批准/通过 | 可执行、目标闭合。 |
| `575b732f` | 两个 TS 候选的驻点、IRC、接触和路径偏好 | 批准/通过 | `task.md` 依赖 `task_spec.json` 且末尾约束重复，属于 Prompt 最终复核不足。 |
| `585288a5` | 三个 DFT 方法的 GED 几何比较 | 批准/通过 | 方法名是科学自变量，公开合理；但元数据仍写 `no_paper_method`，协议不诚实。 |
| `63c76161` | 反向顺反异构化势垒 | `objective_failure_retryable` | SI 坐标未进入源材料，`.sp` 是无坐标占位，外部 DOI 又因 DNS 失败；任务不可执行，阻断合理。 |
| `6b32cd68` | Ir(III) 配合物 DFT/TDDFT 激发态 | 批准/通过 | 完整核心工作流，目标和输入较充分。 |
| `72d95769` | CP2K/PLUMED 环起伏自由能面 | 批准/通过 | 增强采样任务具有完整过程和验证价值。 |
| `7574d997` | 主客体激发态发射与 NTO | 批准/机械阻断 | 科学任务可用；`observed_fields=report/report.md` 被代码误当 JSONPath，是运输兼容误报。 |
| `8f891f94` | 大环构象能量与 ECD | 批准/通过 | 构象筛选到光谱验证链条合理。 |
| `98b6f8a0` | 六个分子的 TDDFT 取代基趋势 | 批准/通过 | 多体系趋势任务闭合。 |
| `9bf81c34` | Li 吸附能、差分电荷与 DOS | 批准/通过 | 周期体系输入和多证据结论合理。 |
| `9d091f43` | 12 个构象体自由能与排序 | 批准/通过 | 参考态和构象排序定义清楚。 |
| `9e76a3b1` | O2/Ag(111) 吸附与自旋晶格模型 | 批准/通过 | 公开 `workflow_spec.json` 含约 `0.81` 的预期 suppression factor，可能是评分答案，Stage07 动态泄漏复核不足。 |

## 4. 问题归因与解决方案

### 4.1 代码问题：文档型 binding 的兼容语义过窄

**证据**：`paper_7574d99707125e60` 的 Acceptance Profile 同时把 `artifact_paths` 和 `observed_fields` 写成 `report/report.md`。文件路径安全且两者完全一致，但机械 gate 将后者送入 JSONPath 解析器，产生四条 `evaluator_binding_path_invalid`。

**解决方案**：若一个 `observed_fields` 值与同一 binding 中安全的文档 artifact path 完全相同，则按文档语义 binding 接受并记录 diagnostic。该规则只解释运输表示，不解释文档中的科学结论。统一把字符串或数组型 `artifact_paths` 规范为列表，避免逐字符校验。

### 4.2 代码/协议问题：autonomy scope 被强制写死且与 disclosure 冲突

**证据**：`_setup_converter_inputs()` 无条件写入 `fixed_input_method_constrained_workflow`；后续 canonicalizer 又无条件把 autonomous 写为 `no_paper_method`。`paper_585288...` 的科学目标本身要求比较 CAM-B3LYP、PBE0、mPW1PW91，却被标记为没有公开方法。`paper_23ab...` 则允许自由选方法，却继续用 PM6/COSMO 的 HOMO/LUMO 紧容差评分。

**解决方案**：

- Stage06A 必须选择并解释两种 scope 之一：
  - `fixed_input_method_constrained_workflow`：方法/方法集合是科学问题定义或严格数值口径的一部分，必须在 autonomous 公共任务中明确公开；
  - `fixed_input_method_discovery`：被评估 Agent 自选方法，GT 以排序、符号、趋势、方法稳健结论、过程证据或有科学依据的宽容差为主。
- 代码只保存 Agent 给出的 scope；缺失时使用与当前“自行选择方法”行为一致的 discovery 默认值，不再强制 constrained。
- `method_disclosure` 从 scope 派生：constrained 使用 `public_scientific_method_constraints`，discovery 使用 `no_paper_method`。
- Stage06B 从 conversion packet 读取并保留“问题定义型方法约束”，仍删除作者实现 route、步骤顺序和答案。
- Stage07 最终裁决 scope、公共方法信息和 GT 口径是否相容。

### 4.3 Prompt 问题：`task.md` 唯一指令源未被最终落实

**证据**：`paper_23ab...` 要求遵守 `task_spec.json` 中边界；`paper_575b...` 开头要求从 `task_spec.json` 确定结果。公开 JSON 因而成为第二套任务义务来源。

**解决方案**：Stage06A、Stage06B 和 Stage07 均增加最终自包含检查：`task.md` 必须完整陈述科学问题、边界和交付；不得让被评估 Agent 从 `task_spec.json`、`workflow_spec.json` 或其他 JSON/route 文件中发现额外义务。其他文件只能作为短元数据、数据或由 `task.md` 已经定义用途的路线证据。

### 4.4 Prompt 问题：公开答案扫描仍不完整

**证据**：`paper_9e76...` 的公开路线文件包含约 `0.81` suppression factor；与之相对，`paper_4ee...` 的 `29.02 ppm` 是方法校准常数，不应机械删除。

**解决方案**：Stage07 从本任务 hidden reference 动态建立目标数字、排序、趋势和结论命题清单，扫描两种模式的全部公共文件，并结合上下文判断其属于评分答案还是执行所需的路线常数/物理边界。该检查完全由 Agent 完成，不写固定数字、分子名或关键词规则。

### 4.5 模型执行问题：重复文本和漏做已声明检查

`paper_575b...` 的重复约束说明模型在长审计后的最终表面复核仍可能不完整。这不是代码科学缺陷；通过更短、更明确的最终检查清单改善。若后续仍是低频、无固定模式的语言编辑失误，则保留为模型能力限制，不增加代码文本裁决。

### 4.6 真实数据/环境问题：源资产缺失

`paper_63c...` 不可执行的根因是原子坐标未进入可访问源材料，且网络补取失败。Stage07 正确没有猜测结构。该问题不由机械 gate 放行，也不属于 Stage07B 可修复范围。

## 5. 第七轮代码修改计划

1. 为文档 artifact 同路径 binding 增加通用兼容和单元测试。
2. 让 `workflow_scope.autonomy_scope` 进入规范 scope 投影，移除 converter packet 的强制 constrained 覆盖。
3. 在 conversion packet 中增加可公开的问题定义型方法约束；Stage06B 根据 scope 保留或删除。
4. 让模式元数据从 autonomy scope 派生，避免 `公开方法 + no_paper_method` 的矛盾。
5. 强化 Stage06A/Stage06B/Stage07 prompt 的方法口径、`task.md` 自包含和动态泄漏扫描。
6. 增加 prompt/contract 单元测试，运行 Stage06/07 专项与全量测试。
7. 先回归 `7574d997`、`23ab5e60`、`585288a5`、`9e76a3b1` 和 `575b732f`；通过后再运行同一 20 篇并发回归。

## 6. Stage07B 决策

本轮不实现 Stage07B：

- 唯一机械阻断是 gate 的兼容误报，应直接修 gate；
- 方法 scope、GT 口径和答案泄漏属于 Stage07 的科学审计职责；
- 源坐标缺失无法由二次合同修复 Agent 合法补齐。

只有后续测试再次稳定出现“Stage07 已科学批准、信息完整、但存在可确定修复的路径/schema/目录/binding 表示错误”时，才重新评估 Stage07B。

## 7. 第七轮验收条件

- `7574d997` 不再被同路径文档 binding 误阻断；
- 新任务的 autonomy scope、公开方法边界和 `method_disclosure` 一致；
- discovery 任务不再用未公开论文方法的紧绝对值作为唯一硬评分；
- constrained 任务可以公开作为科学变量的必要方法，但不泄漏论文结果或实现 route；
- `task.md` 自包含，不把其他 JSON/route 文件变成第二指令源；
- Stage07 有动态公开答案复核证据；
- 不新增任何论文、分子、软件或固定答案特例规则。

## 8. 第七轮实施与回归结果

### Git版本

- 第七轮代码版本：`d6a8f1d`（文档和代码修改已提交）
- 本轮后续修正（scope 默认显式化、模式 binding matrix prompt）待下一提交。

### 代码验证

- Stage06/07 专项：136 passed
- 全量测试：523 passed
- 第6轮 `paper_7574d99707125e60` 机械回归：`mechanical_pre_publish_status=passed`、`schema_load_diagnostic=passed`；4 条 document-path compatibility diagnostic，无 finding。

### 第七轮十篇回归

目录：`runs/stage06-07-v4-round7-deepseek10-concurrency10-20260821`

- 模型：`deepseek-v4-pro-0813`，Codex，concurrency=10
- CLI：10/10 completed，`failed_count=0`
- Stage06 constructed：9；source-backed not-constructible：1（`paper_63c76161e5b55a6a`）
- Stage07 approved/approved_with_repairs：9；科学拒绝：1
- 机械通过：8；机械阻断：1（`paper_03455526ab937195`）
- 该机械阻断不是本轮代码误报：Stage07 将 reproduction-only `initial_addition_barrier` 和 `aromatization_barrier` 留在共享 top-level binding，而 autonomous `results_schema` 正确不包含它们。应由 Stage07 用 mode-specific binding matrix 修复，不能由 gate 猜测或放行。
- `paper_7574d99707125e60` 的同路径 document binding 已通过，说明第7轮代码修复有效。
- `paper_23ab5e60dd8e8983` 的方法自由/绝对值矛盾已由 Stage07 改为 method-robust acceptance；`paper_585288a5a5265d55` 保持方法选择型任务且未出现机械冲突；`paper_9e76a3b15026ccd8` 的 autonomous public method constraints 与 `method_disclosure=public_scientific_method_constraints` 一致。
- 若干 `task.md` 中出现“不要读取 task_spec.json”这类否定性句子，是为了明确唯一指令源，不属于把 JSON 设为第二指令；本轮不把它们误报为缺陷。

### 第八轮小修方向

1. 保留已验证的 document-path compatibility 代码。
2. 强化 Stage07 的 mode-specific binding matrix 终检，并要求在 shared binding 留存前证明两个 mode schema 都有该字段。
3. 保留 scope 显式默认和 method disclosure 派生修正；补跑 034/575/585/7574/9e76 代表性回归。
4. 若 mode-specific binding 问题不再出现，再重新跑 20 篇并发10扩大回归；若仍只剩模型偶发措辞/科学判断差异，不增加代码规则，也不实现 Stage07B。
