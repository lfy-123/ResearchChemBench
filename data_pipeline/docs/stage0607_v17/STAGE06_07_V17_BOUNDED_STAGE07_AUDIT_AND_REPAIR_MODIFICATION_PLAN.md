# Stage06/07 v17：有边界的 Stage07 科学审计与修复方案

## 1. 背景和问题

Stage06 已经调整为最终科学 benchmark task synthesizer：它选择一个闭合、重要且资源可行的计算化学目标，验证该目标需要的输入，并生成两种公开任务、私有参考答案和评分规则。

最新十篇论文测试证明 Stage06A 自查与外部 Gate 已经统一，最终也没有再次出现“科学批准后因两套 Gate 语义不同而被机械阻断”。但是 Stage07 仍存在职责边界问题：

1. Stage07 同时承担审计、修复、替换 workflow 和从 Stage06 失败产物重新构建任务，成为第二个 Builder。
2. `provisional_not_constructible` 会被编排器主动送入 Stage07，Stage07 prompt 也明确允许返回 `approved_after_workflow_redesign`。
3. Stage07 新建或重建的任务没有 Stage08 独立审计，发布质量只依赖同一个 Agent 的自我声明。
4. Stage07 evaluator 审计重视字段是否存在，却没有稳定检查 reference、rule、target、comparison 和 submission field 的值域与形状是否一致。
5. Stage07 输入审计没有稳定区分“文件存在”和“输入内容足以机器执行”。自然语言要求从论文图片转录 connectivity 的文件仍可能通过。
6. Stage06 的执行未完成可以被写成 `scientific_not_constructible`。`paper_9ec8c4761c4f171b` 已恢复 18 个 XYZ 并完成科学 scope，却因没有在工具预算内生成完整 task pair 而被错误归为科学不可构建，随后又由 Stage07 重建并发布。

本方案将 Stage06 固定为唯一构建者，将 Stage07 缩减为已有候选任务的独立审计者和有限修复者。

## 2. 核心目标

修改后必须满足：

- Stage06 是唯一能够选择、建立和交付科学任务的 Agent。
- Stage07 只审计已经成形的 Stage06 候选，不从拒绝或不完整产物重建任务。
- Stage07 可以在同一科学目标内修复 source-backed、局部且可复核的问题。
- Stage07 发现目标不合理、输入不闭合、参考答案不可恢复或 evaluator 无法成立时直接拒绝。
- 删除 `approved_after_workflow_redesign` 成功路径。
- Stage06 科学不可构建、构建执行失败和合同不完整在状态语义上保持可区分；三者都不允许由 Stage07 从零补建。
- evaluator Gate 阻断无争议的完整性和一致性错误，不判断 tolerance 的科学最优值、精度或文字风格。
- 不加入论文、分子、软件或固定数值特例。

## 3. 阶段职责边界

### 3.1 Stage06：唯一任务构建者

Stage06 负责：

- 阅读论文和 SI；
- 选择一个科学目标和 workflow；
- 验证目标需要的最小输入集合；
- 生成 reproduction 和 autonomous 两种公开任务；
- 生成 reference key points、reference conclusions 和 scoring rules；
- 运行自查并完成文件交付。

Stage06 的结果分为三类：

1. `provisional_constructed`：存在完整的候选任务树，可以进入 Stage07。
2. `provisional_not_constructible`：源材料无法支持一个闭合科学任务，直接作为科学拒绝结束，不进入 Stage07。
3. `artifact_delivery_failure_retryable` 或等价执行失败：API、harness、文件系统、工具预算或输出组织导致构建未完成，不进入 Stage07，也不得伪装成科学拒绝。

Stage06 返回 `constructed` 但仍有局部 Gate findings 时，只要基础候选树完整，可以进入 Stage07 做局部修复。没有两种模式、输入或 evaluator 核心文件的产物不属于可审计候选。

### 3.2 Stage07：独立审计和有限修复

Stage07 只负责：

1. 审查已选科学目标是否重要、诚实、可执行并与论文证据一致。
2. 审查公开输入是否真实存在、可解析并足以执行已选任务。
3. 审查 reference key points、conclusions、scoring rules 与 submission schema 的逐项一致性。
4. 审查 reproduction/autonomous 是否保持同一问题，同时正确处理路线披露和答案泄露。
5. 对同一科学目标内的局部问题进行 source-backed 修复。
6. 修复后重新读取最终文件、运行统一 Gate，并给出批准或拒绝。

Stage07 禁止：

- 选择另一条 workflow；
- 替换科学目标；
- 改变被评估的系统集合或比较对象；
- 从 `scientific_not_constructible` 或 artifact-incomplete 产物重新建任务；
- 从论文图片重新设计结构或生成任意 3D seed；
- 发明缺失数值、容差、结构、状态或科学结论；
- 用 `approved_with_repairs` 隐藏实际的 workflow redesign。

### 3.3 允许的局部修复

以下修复在不改变科学含义时允许：

- 澄清 task.md 中已有目标、边界和交付说明；
- 补入 Stage06 已选输入中、论文/SI 明确提供但复制遗漏的原始文件；
- 修复 evaluator-local ID、reference_id、supporting_key_point_ids；
- 将纯数值 reference 从错误的 semantic rule 改为 numeric rule；
- 将多个独立数值拆成逐项 target/tolerance，或补充已有科学定义明确要求的 aggregate projection；
- 修复 unit、comparison、binding 和 submission schema 对齐；
- 修复 reproduction/autonomous 披露差异和答案泄露；
- 修复 provenance、manifest 和路径等不改变科学内容的合同问题。

下列情况必须拒绝，而不是修复：

- 需要换目标或换 workflow 才能成立；
- 必需输入只能靠猜测或从不可见论文图片人工转录；
- 需要新建结构、反应路径、周期模型或 source 未提供的科学状态；
- 参考答案没有证据或无法与提交字段建立可执行映射；
- 已选目标只是论文外围描述而不能支持重要计算结论；
- 修复会改变系统集合、比较方向或最终科学结论。

## 4. Stage07 可见文件与权限

Stage07 workspace 维持三个明确区域：

```text
inputs/                    read-only
outputs/task_pair/         writable Stage06 candidate copy
outputs/stage07_audit.json writable terminal receipt
```

### 4.1 候选任务

`inputs/stage06_candidate/` 包含 Stage06 最终候选：

- `paper_info.json`
- `construction_receipt.json`
- `stage06_handoff.json`
- `objective_card.json`
- `workflow_review.json`
- `workflow_completeness_check.json`
- `source_manifest.json`
- `evidence_index.json`
- `public_to_private_asset_map.json`
- `paper_reproduction/**`
- `autonomous_research/**`
- `evaluator_reference/reference_key_points.json`
- `evaluator_reference/reference_conclusions.json`
- `evaluator_reference/scoring_rules.json`
- `evaluator_reference/evidence_map.json`
- `hidden_reference/**`

Stage07 必须看到完整 public/private task tree，才能检查任务、输入、参考答案和评分规则是否对应。

### 4.2 原始科学证据

`inputs/source_materials/` 保留：

- main paper 和 SI 的 normalized document；
- content blocks 和 evidence IDs；
- layout text；
- derived tables；
- source manifest；
- resource policy 和 toolbox snapshot。

这些材料只用于核实当前目标和修复当前候选，不得用于搜索或建立替代 workflow。

### 4.3 审计入口和工具

Stage07 还可见：

- `inputs/audit_index.json`：当前候选的重要文件、Stage06 findings 和审计入口；
- `inputs/stage06_record.json`：Stage06 最终状态；
- `inputs/input_manifest.json`：只读输入清单；
- `inputs/tools/phase_gate.py`；
- `inputs/tools/evaluator_reference.py`。

不向 Stage07 暴露其他论文、Stage06 对话历史、Codex session、bridge trace、旧版本任务或整个代码仓库。

## 5. Stage07 审计工作流

### 5.1 候选完整性确认

Stage07 开始时确认候选树已经存在。缺少整个模式、所有输入或 evaluator 核心文件，意味着 Stage06 没有交付可审计候选，应返回拒绝/执行失败记录，不得调用原始论文材料从头补建。

### 5.2 科学目标审计

只针对 Stage06 已选目标检查：

- 与论文重要计算结论的关系；
- workflow 是否能产生声明的关键点和结论；
- 公开边界、计算动作、验证与交付是否形成闭环；
- scope 是否诚实，不把外围 descriptor 冒充中心任务。

目标表述可以澄清，目标含义不能替换。

### 5.3 输入闭合审计

每个必需输入同时满足：

- 路径存在且非空；
- 声明格式可解析；
- 内容与任务所需科学角色一致；
- 坐标、connectivity、晶胞、TS、集合成员等关键内容确实机器可读；
- “从 Figure 转录”“按论文构建”“生成任意 seed”等文字不是可执行输入。

代码不尝试理解所有化学输入；Agent 使用论文证据和适用 parser 作科学判断。

### 5.4 evaluator crosswalk

对每个 key point 和 conclusion 建立：

```text
reference_id
  -> reference expected/value
  -> scoring rule type
  -> target/expected
  -> unit/tolerance or semantic criterion
  -> comparison/projection
  -> submission artifact and field
```

必须检查：

- 每个 reference 恰有可执行 rule；
- reference_id 存在且唯一；
- rule 类型和 reference 的数据形状一致；
- 纯数值 scalar/list/map 使用 numeric，而不是 semantic；
- 多个独立字段使用逐项 target/tolerance，或者具有明确 aggregate projection；
- scalar target 不能无 projection 地绑定多个独立字段；
- direct numeric target 与 reference expected 同域、同值；
- binding 字段存在于公开 submission schema；
- semantic rule 评价命题、分类或解释，而不是隐藏数值数组。

Gate 不判断 tolerance 是否科学最优、是否整数或小数位是否合适。

### 5.5 模式和泄露审计

- 两种模式保留同一目标、输入事实、参考答案和交付字段；
- reproduction 披露作者路线；
- autonomous 隐藏作者路线和答案，但保留问题定义；
- autonomous 公共文件、文件名和坐标注释不泄露角色、排序或结论。

### 5.6 终局复查

所有修复完成后重新读取：

- 两个 `task.md`；
- 两个 submission contract/schema；
- 三个 evaluator 核心文件；
- 所有必需输入；
- public/private 映射。

然后运行统一 Stage07 self-check。批准意味着最终文件而不是修复前审计对象已通过检查。

## 6. 决策和路由修改

### 6.1 Stage07 准入

Stage07 eligible decisions 仅保留：

- `provisional_constructed`
- `constructed`

移除 `provisional_not_constructible`。编排器也必须使用同一集合，避免 stage 内外路由漂移。

### 6.2 Stage07 决策

批准决策仅保留：

- `approved`
- `approved_with_repairs`

其他终局状态：

- `rejected_scientific_unrepairable`
- `objective_failure_retryable`

删除 `approved_after_workflow_redesign` 及相关 summary、receipt 和测试路径。为兼容已有历史记录而读取旧值不属于本轮目标；新运行不得产生该值。

### 6.3 Stage06 执行失败语义

当 Agent 自己声明 `execution_artifact_incomplete`，且详情明确科学目标和输入已闭合但文件未完成时，不得发布为 `provisional_not_constructible`。它应成为 `artifact_delivery_failure_retryable`，`handoff_ready=false`，不进入 Stage07。

科学拒绝仍要求 source-backed scientific failure code 和结构化 checked sources。执行失败与科学拒绝在汇总和测试报告中分别计数。

## 7. Gate 的通用一致性增强

在共享 `evaluator_reference.py` 中加入有限、通用且无论文特例的确定性检查：

- reference expected 为纯数值或纯数值集合时，semantic rule 产生阻断 finding；
- numeric reference map/list 必须由 numeric rule 表达；
- numeric rule 的 target 可以是 scalar、list 或 map，但形状必须与 reference expected 对应，除非 binding 明确给出 aggregate/projection；
- 多个 observed fields 对单一 scalar target 且无 projection 时阻断；
- direct identity numeric rule 的 target 与 reference expected 不一致时阻断；
- comparison/projection 必须能说明多值如何投影到 target。

只对无争议的结构/值域矛盾阻断。以下保持 diagnostic 或不检查：

- tolerance 数值是否科学最优；
- 精度和小数位；
- semantic 文字风格；
- 论文特定阈值。

Stage06 自查、Stage07 自查和外部 Gate 继续调用同一个共享 helper，确保语义一致。

## 8. Stage06 完成顺序优化

不扩大 Stage06 职责，只在 prompt 中强化完成顺序：

1. 批量读取目标相关证据和输入；
2. 确定目标并完成输入闭合；
3. 立即生成最小但完整的两种模式和 evaluator；
4. 运行 Gate 并修复；
5. 最后补充非必要的详细审计元数据。

避免：

- 一个工具调用处理一个输入文件；
- 在多个 JSON 中重复展开同一组大规模 asset 对象；
- 在 finalization reserve 中重复 `ls`、`find` 或重新阅读论文；
- 为了生成完整中间 review 而推迟 public task 和 evaluator。

`paper_9ec8c4761c4f171b` 的根因不是科学不可构建，而是 108 次工具调用中前期科学分析和 92 KB workflow review 占用过多，最终未生成任务树。本修改必须避免把类似情况交给 Stage07 重建。

## 9. 代码修改范围

预计修改：

- `src/late_stage_runner.py`
- `src/stages/stage06_task_builder/prompts.py`
- `src/stages/stage06_task_builder/stage.py`
- `src/stages/stage07_task_judge/prompts.py`
- `src/stages/stage07_task_judge/stage.py`
- `src/stages/evaluator_reference.py`
- 相关定向测试文件

不修改 Stage00-05、chemistry toolbox、论文特例或 evaluator 文件格式的大框架。

## 10. 测试和验收标准

### 10.1 单元和回归测试

至少覆盖：

1. `provisional_not_constructible` 不进入 Stage07。
2. `execution_artifact_incomplete` 不发布为科学拒绝，也不进入 Stage07。
3. Stage07 prompt 不包含 workflow replacement/redesign 授权。
4. Stage07 schema 不接受 `approved_after_workflow_redesign`。
5. Stage07 可以修复同一目标内 evaluator ID/binding/type 问题。
6. numeric map 被 semantic rule 承载时 Gate 阻断。
7. 多字段对 scalar target 且无 projection 时 Gate 阻断。
8. 有明确 aggregate projection 时允许 scalar target。
9. tolerance 科学取值和格式细节不会造成过度阻断。
10. Stage06、Stage07 self-check 与 external Gate 使用相同 findings。

### 10.2 同十篇论文实测

使用与 v16.2 相同的十篇论文、`gpt-5.6-sol` 和 high reasoning，并重点验证：

- Stage07 不再处理 Stage06 scientific rejection；
- Stage07 不再出现 `approved_after_workflow_redesign`；
- Stage06 artifact incomplete 不会被 Stage07 重建发布；
- 发布任务的输入均机器可执行；
- published evaluator 不再出现 numeric map/semantic 错配；
- published evaluator 不再出现无 projection 的多字段/scalar target；
- Stage07 对可修复 evaluator 问题有实际修改记录；
- 科学批准后机械 Gate 阻断仍保持为零或给出明确技术原因；
- 所有 published task 逐篇检查 task instruction、输入、reference、scoring rules 和两种模式转换。

## 11. 预期结果

该方案可能降低表面发布率，因为 Stage07 不再挽救 Stage06 未完成任务。但发布标签的含义更可靠：每个发布任务都来自 Stage06 完整构建，并经过另一个 Agent 对同一候选的独立审计。

对已知样本的预期：

- `paper_3590deded767345e` 应继续批准；
- `paper_9455a82229de2427` 的 schema/ordering 问题应被局部修复；
- `paper_9ec8c4761c4f171b` 若 Stage06 再次 artifact incomplete，不进入 Stage07，也不得发布；
- `paper_a5564360a31f760b` 的非机器可执行 connectivity 应被拒绝，除非 Stage06 已提供真实 source-backed connectivity/coordinates；
- `paper_2aca1dd116799b28` 若完整候选树存在，Stage07 可以修复 evaluator ID 对齐，但不能换 workflow。

成功标准不是发布数量最大，而是 Stage07 不再生成未经独立审计的新任务，并显著降低机械通过但科学/评分不可执行的 false negative。
