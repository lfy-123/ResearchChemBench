# v17 工程问题与已通过任务质量分析

## 1. 结论摘要

Stage07 职责收缩后，已经有效改善了两个关键问题：

1. 它不再把科学上不可修复的候选重新构建成另一个任务；
2. 它能在同一科学目标内修复 evaluator 绑定、规则类型、结论覆盖和公开面泄露问题。

十篇测试中，`paper_3590deded767345e` 被明确科学拒绝，说明 Stage07 没有为了提高通过率而替换错误的 scored quantity；`paper_76ae2dc25f0a5aeb` 和 `paper_9455a82229de2427` 的 evaluator 缺陷被有限修复；`paper_611000e1de080f6f` 的剩余阻断则定位为包边界实现问题而不是科学质量问题。

因此，Stage07 新职责对“科学目标是否仍然合理”和“评估文件是否可执行”是有效的。但它不能替代 Stage06 的科学构建：输入缺失、电子态不闭合或论文本身没有可复现的 TS，仍应在 Stage06 终止。

## 2. 工程问题一：科学拒绝被显示为 `FAILED stage07_not_run`

### 2.1 实际原因

旧批次 `runs/stage0607-v17-gpt-5.6-sol-20260826` 启动时使用的 batch helper 仍把“Stage06 科学不可构建、因此 Stage07 按设计不运行”映射为：

```text
state = FAILED
failure_class = stage07_not_run
```

这造成了表面上的失败，但论文目录中的 `late_stage_run_summary.json` 实际已经记录了：

```text
stage06.provisional_not_constructible = 1
stage07.status = not_run
```

当前 `scripts/workflows/run_stage06_07_gpt_batch.py` 的 `_late_stage_pipeline_failure()` 已包含科学拒绝分支：当 `provisional_not_constructible > 0` 且 Stage07 为 `not_run` 时返回 `None`。对应回归测试也已通过：

```text
test_late_stage_batch_treats_scientific_rejection_as_terminal_success
```

所以 v17 代码已经修复了判断逻辑；旧批次状态文件不会自动回写，必须重新执行批次 helper 或进行一次只读状态重算。

### 2.2 建议的最终状态设计

当前返回 `None` 会让批次层把它显示为普通 `COMPLETED`，虽然不再误报失败，但科学拒绝和正常发布仍然不够区分。建议在 batch 层增加一个非失败的明确终态：

```text
state: COMPLETED
outcome: scientific_rejection
failure_class: null
```

或者使用：

```text
state: COMPLETED_SCIENTIFIC_REJECTION
```

推荐第一种，因为不需要让上层重新解释 `state=FAILED`，也不把科学拒绝混入 infrastructure failure。`late_stage_run_summary.json` 继续作为科学事实来源，`run_status.json` 只负责传达终态类别。

### 2.3 不应采用的方案

- 不要把科学拒绝改成 `FAILED` 以触发 retry；
- 不要为了让统计“成功率”更高而把不可构建任务标记为 published；
- 不要让 Stage07 接收 `provisional_not_constructible` 并重新构建。

## 3. 工程问题二：`split_reference_compatibility_projection_warning`

### 3.1 现象

已通过的任务中，package report 经常出现：

```text
compatibility_reference_split_authoritative
split_reference_compatibility_projection_warning:ValidationError
```

这不是 split evaluator Gate 失败。`minimal_evaluator_findings()` 对四篇已通过任务均返回空列表，`reference_key_points.json`、`reference_conclusions.json`、`scoring_rules.json`、binding 和 submission schema 都已经通过权威检查。发布包也都成功。

### 3.2 根本原因

包组装同时维护两个视图：

- v13 的 split evaluator 文件：权威、可人工编辑；
- Task Package v1 的旧 `evaluation/reference.json`：兼容视图。

当前流程先把 split 文件通过 `legacy_reference_from_split()` 转成旧 hidden envelope，再调用 `project_computational_reference()`。这个转换是有损的，至少丢失了以下信息：

1. scoring rule 的 `type` 没有稳定保留到 legacy profile；
2. split rule 的 `binding` 没有映射为旧接口使用的 `submission_binding`；
3. key point 只有 `expected` 时，legacy truth 只读取 `reference_value`，导致 numeric answer 为空；
4. 因而兼容投影产生空 `artifact_paths` 或空 `answer_items`，被 `ComputationalScienceReferenceV1` 拒绝；
5. assembler 捕获该异常，生成 answer-free compatibility stub，并把异常作为 diagnostic 返回。

这解释了为什么 split Gate 通过但每个包仍带 warning：不是模型生成质量差，而是兼容视图的 round-trip adapter 不完整。

### 3.3 推荐解决方案

不要放宽 Gate，也不要删除 split 文件。应修复唯一的 transport adapter：

- `legacy_reference_from_split()` 保留 `rule.type`、`rule.reference_id`、`rule.binding`，并把 `binding` 映射到 legacy 使用的 `submission_binding`；
- key point 的 canonical value 使用 `reference_value`，若不存在则回退到 `expected`；
- 保留 numeric target/unit/tolerance 和 semantic expected/propositions；
- 增加一个 round-trip fixture：split → legacy → `project_computational_reference()` 必须成功，且 binding、rule type、target shape 与 split 输入一致；
- 如果兼容投影仍失败，应该返回明确的 `compatibility_view_unavailable` diagnostic，但不改变 split Gate 的通过/阻断语义。

这是通用字段映射修复，不是针对某篇论文写特例。修复完成后，正常 split evaluator 不应再出现 ValidationError warning。

## 4. 已通过任务的科学目标质量

### `paper_2aca1dd116799b28`

科学目标是三套匹配 triazolyl enediyne 的 Bergman 环化势垒比较，包含九个 XYZ、反应物/TS/产物角色、频率和双向 IRC 验证，最终比较三个 activation barrier。Stage07 确认输入闭合、目标直接支持论文计算结论，并仅移除 autonomous 中作者特定 B3LYP/QST3 路线。

该任务的 autonomous 仍保留“三个连续几何三元组对应 A/B/C”的中性分组，因为这是定义比较对象所必需的，不是答案排序泄露。科学目标质量高，且 reproduction/autonomous 仍是同一个问题。

需要注意一个 contract 一致性问题：Stage06B 的私有 `conversion_contract.json` 曾把 B3LYP/6-31G(d,p) 和 QST3 列入 `preserve_method_constraints`，但最终 autonomous public task 被 Stage07 改成“选择合适方法”。这两者不能同时作为规范。若该方法只是作者实现细节，Stage06B 就不应把它列为 preserve constraint；若它决定 evaluator 数值的可比性，就必须保留。当前样本没有因此被 Gate 阻断，但说明“问题定义方法约束”和“作者路线细节”的分类还不够明确。

### `paper_76ae2dc25f0a5aeb`

目标是两个 CPA annulation 过渡态的相对自由能差，包含两份 130 原子 XYZ、优化/频率、溶剂单点、ΔΔG 和较低势垒判断。Stage07 修复了真实 evaluator 缺陷：frequency numeric map 的规则类型，以及缺失的 `con_ddg` 规则；没有改变目标或方法。

该任务 autonomous 仍公开 B3LYP-D3(BJ)、基组、SMD(toluene) 和热力学边界。这是当前 conversion contract 标记的 problem-defining method constraint，因此不是 Stage07 漏删作者路线；但它意味着该 autonomous 任务更接近“方法受限的自主复现”，不是完全开放方法发现。若 benchmark 需要完全开放方法，应在 Stage06 conversion contract 中取消该约束，而不是在 Stage07 通过死规则删除。

### `paper_9455a82229de2427`

目标是四个结构的 CBS-QB3 0 K 能量、平衡氢损失反应能和 P1/P2 稳定性排序。四份 XYZ、SiN 双重态/其余单重态、反应式和结果字段都闭合。Stage07 修复了四个独立能量的逐物种 binding、具体的 `P1 lower than P2` proposition 和 submission schema。

该任务的 scoring rules 现在可执行，但 Hartree 容差 `1e-6` 是非常严格的科学选择。Gate 只需确认它是非空、数值可用并与 reference 形状一致；具体容差是否合理应留给人工科学审查，不应重新引入机械阻断。

### `paper_611000e1de080f6f`

目标是两个 coumarin 4a rotamer 的 S1 emission energy 和 oscillator strength，输入是两份 31 原子 XYZ，workflow 明确包含 S0/S1 优化、TD-DFT 和状态/收敛检查。四条 numeric key-point 规则都具备 target、unit、tolerance、comparison 和结果字段 binding；Stage07 科学审计通过。

该任务 evaluator 主要评分四个数值，没有额外评分 TICT 机制解释。这与当前选定的“发射性质复现”目标一致，不是缺失规则。如果 benchmark 以后要评分 TICT 解释，应新增独立 semantic conclusion，而不是把现有 numeric 规则改复杂。

## 5. Stage07 改造是否缓解合成质量问题

答案是肯定的，但作用边界需要明确：

| 质量维度 | v17 证据 | 评价 |
|---|---|---|
| 科学目标不被错误替换 | `paper_3590...` 被拒绝且没有重建 | 明显改善，避免“为了发布而换题” |
| 输入/物理边界闭合 | 通过任务的 audit table 均为 `closed` | Stage07 能发现缺失或错配，但不能补造科学输入 |
| evaluator 完整可执行 | `paper_76...`、`paper_9455...` 被有限修复；其余通过 | 明显改善，规则与 reference/binding/submission schema 对齐 |
| reproduction→autonomous | 通过任务保留同一目标和输入，去除答案泄露 | 转换总体正确；部分任务是方法受限自主模式 |
| 机械发布稳定性 | `paper_611...` 的边界过滤修复后重组通过 | 已解决一个真实 package boundary 阻断 |
| 论文全部主张覆盖 | 不保证 | Stage07 只审计选定目标，不会自动扩展到论文所有结论 |

最重要的质量提升不是“通过率变高”，而是通过与拒绝的归因变得正确：能修的 evaluator 合同被修，不能修的科学错配被拒，不能把科学缺失伪装成格式修复。

## 6. 建议优先级

1. **优先修复 split→legacy round-trip adapter**，消除非阻断但重复出现的兼容 warning；增加通用 fixture，不加论文特例。
2. **更新 batch 状态枚举/汇总**，将 Stage06 scientific rejection 显式标为正常终态；不触发 retry。
3. 保持 Stage07 当前单次审计和 bounded repair 边界，不恢复 workflow redesign 或自动重建。
4. 对 autonomous 的方法约束采用显式 contract policy：方法是科学问题约束就保留，否则由 Stage06 conversion 删除；不要在 Gate 中用关键词黑名单判断。
5. 对 tolerance、ordering comparison 等仅做非阻断质量诊断，继续允许人工修改，不因格式或具体科学取值阻断发布。

## 7. 证据与回归

- v17 定向回归：`72 passed`；新增 v17 测试：`22 passed`。
- `minimal_evaluator_findings()` 对四篇通过/重组任务均为空。
- `paper_611...` 使用当前 assembler 无模型重组：paper reproduction 和 autonomous research 均 `passed`。
- 旧批次中的 `FAILED stage07_not_run` 是修复前状态文件，不能代表当前 helper 的判断逻辑。
