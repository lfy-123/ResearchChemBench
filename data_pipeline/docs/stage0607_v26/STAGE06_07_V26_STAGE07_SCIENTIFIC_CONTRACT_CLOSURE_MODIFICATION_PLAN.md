# Stage06/07 v26 Stage07 科学合同闭环审计增强方案

## 1. 版本目标

v26 在 v25 已完成的 feasibility-first、任务完整性、输入闭合、过程关键点、最终结论关键点和 Stage07
科学审计基础上，解决最终发布包中仍可能残留的细粒度不一致：

- 公开任务允许某种完成、部分完成或有证据失败结果，但 `submission_schema.json` 无法表达；
- evaluator 的字段路径虽然能够解析，却不能唯一识别被评价的体系或候选；
- 逐体系、逐候选的科学验证要求只绑定到一个全局文本字段；
- autonomous evaluator 继承了 reproduction 特有的作者解释或论文结论，形成隐藏评分要求；
- evaluator 使用论文内部 TS、构象、产物或立体化学标签，但公开任务没有答案中性的定义；
- Stage07 用一段概括性文字将 `instruction_completeness` 或 `evaluator_quality` 标记为通过，未实际完成
  `任务要求 → 提交字段 → 评估规则 → 科学对象` 的逐项闭环审计。

v26 的核心不是增加新的 Agent、扩大 Stage06 职责或把科学判断写进机械 Gate，而是把 Stage07 明确为
**最终科学质量与评估合同审计员**：它必须审计并修复 Stage06 已构建任务的指令、输入、提交合同和
evaluator 之间的完整闭环。批准意味着被评测 Agent 无需猜测任务或隐藏要求，并且每一种任务允许的合法结果
都能被提交和公平评价。

## 2. 已确认的设计边界

v26 保留以下既有边界：

1. Stage06 仍是最终任务构造者，负责冻结 scientific objective、闭合输入、构建可行模式、生成过程关键点、
   最终结论和初步 evaluator。
2. 不给 Stage06 增加新的独立阶段、额外 Agent 或新的输出文件；只精确化它已经承担的 schema/evaluator
   生成要求。
3. Stage07 只审计 Stage06 已存在的模式。它不能创建缺失模式、改变 scientific objective、换成弱代理问题
   或在缺乏来源证据时发明输入和参考答案。
4. Stage07 可以在 scientific objective 不变且来源证据充分时，大幅重写 `task.md`、输入说明、
   `submission_schema.json` 和 evaluator 文件。
5. 如果一个模式不可修复，可以只拒绝该模式并发布另一个已有模式；不要求完整 pair。
6. `paper_reproduction` 公开作者的定性假设、候选方向或机理路线；`autonomous_research` 不公开作者路线。
7. 两种模式都不能公开论文/SI、论文计算协议、参考数值、结果排序、获胜候选、结果结构、tolerance 或完整答案。
8. 每个模式必须有至少一个过程验证关键点和一个最终结论关键点；最终结论可以是数值、排序、结构、条件或
   文本语义。
9. 机械 Gate 只负责文件、JSON、schema、引用、required chain、显式答案字段和发布结构等通用合同，不判断
   科学中心性、机理合理性、模式公平性或 tolerance 是否最优。
10. 不新增论文级 ID。继续只使用 `paper_id`；保留 evaluator 内部的 `key_point_id`、`conclusion_id`、
    `rule_id`、`evidence_id`，以及任务结果内部真正需要的 `system_id` 或 `candidate_id`。
11. 不增加 `human_review_required` 等无意义生命周期标签；人工审查仍是所有 Stage07 发布结果的默认后续步骤。

## 3. v25 回归暴露的问题

本方案以
`runs/stage0607-v25-gpt-5.6-sol-20260827-five-rerun3` 的最终 release 为依据，只把 Stage07 审计后仍发布的
问题视为 v26 需要解决的问题。Stage07 已修复或拒绝的候选缺陷不计为最终发布缺陷。

### 3.1 `paper_611000e1de080f6f`：合法替代路径无法提交

任务允许：

- 使用频率以外的等价局部极小值验证；
- 在存在具体资源限制时，不完成第二套灵敏度计算，而是说明限制和不确定性。

但 schema 仍强制要求 `imaginary_modes` 整数和四个灵敏度数值。正常成功路径可提交，任务明确允许的替代路径
却无法被 schema 诚实表达。

### 3.2 `paper_a5564360a31f760b`：固定体系绑定不唯一

体系特定数值规则使用：

```text
$.systems[*].reorganization_energy_ev
$.systems[*].heavy_atom_rmsd_angstrom
```

`[*]` 会返回所有体系的值。规则只在自然语言 `comparison` 中说明选择 `system_id=p-2BN` 或
`system_id=m-2BN`。大模型裁判可能理解，但字段绑定本身不是唯一映射，对机械提取、数组换序、重复 ID 和后续
执行器不稳健。

### 3.3 `paper_a5564360a31f760b` autonomous：隐藏的论文特定解释

autonomous 公开任务要求独立比较重组能、RMSD、模式局域化并提出解释，但隐藏结论仍要求使用论文特定的
较窄发射和较小 Stokes shift 解释。公开任务没有给出这些待解释的实验现象，并将绝对光谱排除在 scored
physical boundary 之外。

该任务的 reproduction 与 autonomous `reference_key_points.json`、`reference_conclusions.json` 完全相同，
表明 autonomous evaluator 没有按其公开问题重新确定公平的结论边界。

### 3.4 `paper_76ae2dc25f0a5aeb`：候选身份与逐候选验证不闭合

隐藏 evaluator 使用 `TS2-R-S` 和 `TS2-S-R`，公开任务只要求比较两个相反立体化学结果，没有提供答案中性的
立体化学判定约定、相关原子映射或论文内部标签映射。被评测 Agent 可能找到科学上正确的两个 TS，却无法可靠
映射到隐藏 evaluator 的标签。

每个 candidate 已有虚频数和连接性检查字段，但过程规则绑定到全局 `validation` 文本，不能逐候选确认参与
比较的两个 TS 都完成了验证。

任务还允许搜索耗尽后有证据地报告只找到一个 family，但 schema 始终强制要求 `delta_delta_g_kcal_mol` 和
`ordering`，使合法失败路径无法提交。

### 3.5 Stage07 漏检的根因

当前 Stage07 角色已经包含 objective、inputs、instruction completeness、key points、conclusions、mode
separation、answer inversion 和 evaluator quality，但批准条件主要检查每个维度是否有非空 `finding` 和
`evidence`。Agent 可以用总体性描述宣布“evaluator is schema-bound”，却没有被明确要求逐规则核对：

```text
公开任务要求
  → 任务允许的结果状态
  → submission schema 中的 required 字段或合法分支
  → evaluator 的 reference item 和 scoring rule
  → 被评价体系、候选或结论的唯一身份
```

所以 v26 应强化审计方法，而不是继续增加审计维度。

## 4. Stage07 v26 角色定位

Stage07 Prompt 的开头应将角色明确为：

> You are the final scientific-quality and evaluation-contract auditor for completed
> computational-chemistry benchmark tasks. Approval means the public problem is self-contained,
> every allowed task outcome is representable by the submission contract, every hidden evaluation
> requirement is fair for that mode, and every scoring rule identifies its scientific object
> unambiguously. Repair source-determined defects without changing the Stage06 scientific objective;
> reject only when preserving that objective would require invented inputs, references or a new task.

同时保留：

- “You are not a fallback task builder”；
- 不创建缺失模式；
- 不改变 Stage06 scientific objective；
- 可以在目标不变时大幅修复已有模式；
- Stage07 后没有 Stage08，因此不能把明确发现的问题留给下一阶段。

角色强化的重点是“最终负责闭环”，而不是要求 Stage07 重新做 Stage06 的论文抽取和完整任务构建。

## 5. Stage07 v26 审计工作流

Stage07 继续只运行一次，但 Prompt 要求依次完成以下内部步骤。无需增加新的发布文件或新的 Agent-visible 字段。

### 5.1 接收并冻结审计边界

1. 复制 Stage06 候选到 `outputs/audited_task/`；
2. 读取 `workflow_review.json`、`paper_route.md`、全部已存在模式、全部 evaluator 和 immutable source；
3. 写清楚 Stage06 已冻结的 scientific objective 和现有模式列表；
4. 后续修复不得改变 objective 或创建缺失模式。

### 5.2 逐模式提取公开合同

对每个已有模式，从 `task.md` 和公开输入中提取：

- 研究对象与身份；
- 要求计算、搜索、比较或解释的结果；
- 过程验证要求；
- 完成条件；
- 停止条件；
- 允许的成功、部分完成或有证据失败结果；
- 被评测 Agent 必须提交的证据。

Stage07 不应只复述 task.md，而要以这些项目作为后续 schema 和 evaluator 审计的基准。

### 5.3 Task → Schema 合法结果审计

对每项公开要求检查其是否有对应的 required 提交字段。对每一种任务允许的结果状态检查 schema 是否可表达。

必须发现并修复：

- task 要求某个结果，但 schema 没有字段；
- evaluator 评价某字段，但该字段不在 required chain；
- task 允许替代验证，但 schema 只接受一种验证结果；
- task 允许 bounded failure，但 schema 仍强制要求只有成功时才存在的数值、排序或结构；
- schema 要求 task 从未要求且 Agent 没有理由生成的字段；
- `completion_status` 只是一个字符串标签，未真正控制成功和失败分支所需字段。

优先使用标准 JSON Schema 表达合法结果分支，例如 `oneOf`/`anyOf`、清晰的状态字段和分支内 required 字段。
不要求所有任务使用同一个固定 failure schema，也不为不同论文硬编码统一字段。

示意原则：

```json
{
  "oneOf": [
    {
      "properties": {"completion_status": {"const": "completed"}},
      "required": ["completion_status", "systems", "comparison"]
    },
    {
      "properties": {"completion_status": {"const": "bounded_failure"}},
      "required": ["completion_status", "failure_stage", "evidence", "limitations"]
    }
  ]
}
```

这里的 `const` 只区分合法提交状态，不编码科学答案。实际字段应由任务决定；该示例不是统一模板。

### 5.4 Schema → Evaluator 可追溯性审计

对 `reference_key_points.json` 和 `reference_conclusions.json` 中每个条目检查：

1. 是否有对应 `scoring_rules.json` rule；
2. rule binding 是否指向 schema 中真实存在的字段；
3. 字段是否在适用的成功或失败分支中 required；
4. expected 内容是否属于该模式公开要求的结果或必要过程验证；
5. binding 是否保留足够的科学对象身份；
6. key point、conclusion、rule 与 evidence 是否来自当前论文/SI。

不得用一个全局 `validation` 文本替代公开任务明确要求的多个逐候选验证结果。若过程关键点声明“两个 TS 分别
有一条虚频且连接正确”，rule 应绑定到参与比较的每个 candidate 的频率和连接性验证字段，或绑定到包含完整
候选身份和验证内容的候选对象。

### 5.5 科学对象唯一绑定审计

Stage07 必须判断 binding 是否唯一识别其目标，而不是机械禁止某种 JSONPath 语法。

#### 固定、已知的少量体系

对于任务开始前就固定的 p-2BN、m-2BN 或 rotamer 1、rotamer 2，优先使用显式对象键：

```json
{
  "systems": {
    "p_2bn": {"reorganization_energy_ev": 0.19},
    "m_2bn": {"reorganization_energy_ev": 0.45}
  }
}
```

对应规则绑定：

```text
$.systems.p_2bn.reorganization_energy_ev
$.systems.m_2bn.reorganization_energy_ev
```

也可以使用其他同样明确的结构，但不能让两个体系特定规则只绑定到相同的匿名值数组。

#### 数量不固定的开放候选

TS、构象、机理路径等开放候选继续使用数组。每个候选必须包含：

- 稳定的局部 `candidate_id` 或答案中性的结构身份；
- scientific assignment；
- 该候选自己的优化、频率、连接性或状态验证；
- 该候选自己的能量或比较量；
- 必要的证据路径。

`[*]` 可用于总体排序、完整集合比较或聚合审计；体系特定/候选特定规则必须同时保留能定位目标元素的身份
上下文。不要在 Gate 中简单加入“禁止 wildcard”的死规则。

### 5.6 论文内部标签与公开映射审计

对 evaluator 中的 TS、构象、产物、状态或立体化学标签逐一判断：

- 标签是否在 Agent-visible 输入中有答案中性的定义；
- 定义是否包含足够的原子映射、CIP 约定、结构关系或可操作判据；
- 定义是否会泄露获胜候选、结果排序或答案结构。

如果没有公开映射，Stage07 应：

1. 从现有输入和来源证据补充答案中性的判定约定；或
2. 将 evaluator 改为接受结构性描述和科学等价表达，不要求论文内部标签。

如果两种方式都需要猜测结构或改变 objective，则拒绝该模式。

### 5.7 模式特定 evaluator 公平性审计

Stage07 必须分别审计 reproduction 和 autonomous，不能因为来源相同就默认共享全部 evaluator 内容。

对每个隐藏 expected conclusion 执行反事实检查：

> 一个完成当前模式公开任务、但没有读过论文和 SI 的 Agent，是否知道自己需要研究或回答该结论？

如果答案是否定的：

- 若某个非答案实验现象属于科学问题定义，可以在不泄露计算答案时补充到公开任务；
- 否则应从该模式 evaluator 删除或改写超出公开任务边界的要求；
- 不得因为该结论存在于 reproduction evaluator 就自动复制到 autonomous evaluator。

共享的源支持数值、结构和过程参考可以保留，但作者特定解释、路线验证和论文结论必须按模式重新判断公平性。

### 5.8 双向反演审计

保留现有 answer-inversion audit，并增加反方向审计：

1. **答案泄露方向**：不做计算的 Agent 能否从公开面填写参考数值、排序、获胜候选、结果结构或主要结论；
2. **隐藏要求方向**：认真完成公开任务并严格遵守 schema 的 Agent，是否会因 evaluator 要求了公开任务从未
   要求的内容而失败。

任一方向失败都必须修复或拒绝，不能标记为 passed。

### 5.9 修复、复查和批准

Stage07 完成修复后必须重新阅读实际修改文件，而不是只依据 repair summary：

1. 重新核对 task、schema、evaluator 和对象身份链；
2. 更新 `workflow_review.json` 的 release modes 和质量记录；
3. 运行同一个 `phase_gate.py --phase audit`；
4. 修复机械阻断；
5. 再执行一次答案泄露和隐藏要求双向检查；
6. 最后写 `audit_receipt.json`。

批准的 `instruction_completeness` 和 `evaluator_quality` finding 必须分别覆盖每个保留模式，并引用具体
`task.md`、`submission_schema.json`、reference item 和 scoring rule。不能只写“all files are aligned”。

## 6. Stage06 的最小修改

Stage06 不增加新里程碑、新工具调用或新输出文件，只在现有 C 段构建要求和 evaluator 说明中增加以下约束。

### 6.1 合法结果必须可表示

在 `submission_schema.json` 说明后增加：

> Every outcome explicitly allowed by task.md must be representable without fabricated values.
> If the task permits bounded failure, partial discovery or an alternative validation method, the
> schema must provide a truthful branch for it rather than requiring success-only numeric,
> ordering or structure fields unconditionally.

### 6.2 对象绑定必须明确

增加：

> Bind each system-specific or candidate-specific rule to an unambiguous scientific object. For a
> fixed known set, prefer explicit named object fields or an equally unique selector. For an open
> candidate array, retain candidate identity and per-candidate validation context. Wildcards are
> valid for aggregate comparisons but must not erase object identity for item-specific targets.

### 6.3 evaluator 必须按模式重新确定

增加：

> Derive evaluator conclusions separately from each mode's public problem. Do not copy the
> reproduction evaluator into autonomous research unchanged. A shared source result may be reused,
> but an author-route interpretation is fair in autonomous research only when the autonomous public
> task independently asks for and supplies the problem-defining information needed to infer it.

这些要求属于 Stage06 已有的 schema/evaluator 生成职责，不要求它增加新的输入统一预处理、第二次科学审计或
更多工具调用。

## 7. Common Gate 的修改边界

### 7.1 保持不变的职责

Gate 继续检查：

- 必须目录和文件存在；
- task 四段结构、完成条件和停止条件存在；
- JSON 和 JSON Schema 可解析；
- `task_info`、deliverables 和 mode 声明一致；
- evaluator 五个文件存在、非空、ID 和 evidence 引用闭合；
- scoring binding 指向 schema 声明字段；
- numeric target 类型和 numeric leaf 基本一致；
- Agent-visible 输入中没有 PDF/SI、私有路线或明确答案字段；
- XYZ、manifest 和 release 结构满足基本机械合同。

### 7.2 v26 允许的唯一通用增强

为支持 Stage07 使用标准 JSON Schema 表达成功/失败分支，`src/stages/phase_gate.py` 的 selector 解析需要正确
理解字段位于 `oneOf`/`anyOf` 分支中的情况：

- selector 在至少一个合法分支中存在时，不能误报 `binding_field_not_in_schema`；
- selector 在其适用的成功分支 required 时，不能因为失败分支不需要该字段而误报 required-chain 错误；
- numeric selector 的合法分支中包含 number/integer leaf 时，可以识别为数值；
- 仍然阻断在所有分支都不存在、从未 required 或类型明确错误的 binding。

实现应集中在现有 schema selector helper，避免为某篇论文、某种化学任务或某个字段写特例。

### 7.3 明确不加入 Gate 的内容

不得在 Gate 中加入：

- 禁止 `[*]` 或要求固定 JSONPath 形式；
- p-2BN、m-2BN、TS2-R-S 等论文特例；
- 根据 `system_id`、candidate 数量或化学类别判断科学正确性；
- reproduction/autonomous evaluator 语义差异判断；
- tolerance、方法、搜索覆盖或结论合理性判断；
- 用关键词推断某个 hidden evaluator 是否公平。

上述内容仍由 Stage07 科学审计和人工后审完成。

## 8. 结构化 receipt 与 validation

v26 保留现有八个 `scientific_audit` 维度：

- `objective`；
- `inputs`；
- `instruction_completeness`；
- `process_keypoints`；
- `final_conclusions`；
- `mode_separation`；
- `answer_inversion`；
- `evaluator_quality`。

不新增顶层 `contract_traceability`、`human_review_required` 或额外发布标签，以免让代码和输出继续膨胀。

`src/agents/schemas.py` 原则上只需更新版本相关测试，不改变 receipt 形状。若实施中需要收紧 schema，只允许
加强现有 `AUDIT_ITEM` 的基本非空性，不新增论文或化学类型字段。

`src/stages/stage07_task_judge/validation.py` 继续负责：

- approved decision 的 modes、artifact、remaining issues 和八个维度完整；
- approved 状态不能包含 failed dimension；
- receipt modes 与 audited workflow review 一致。

不要尝试在 Python 中判断 finding 文本是否真正完成了科学审计。具体闭环质量由 Prompt、真实文件修复和回归
样本验证保证。

## 9. 代码修改范围

### 9.1 必须修改

#### `src/stages/stage07_task_judge/prompts.py`

- Prompt 版本升级为 v26；
- 强化最终科学质量与评估合同审计员角色；
- 加入逐模式公开合同提取；
- 加入 task → schema 合法结果审计；
- 加入 schema → evaluator 可追溯性审计；
- 加入固定体系和开放候选的对象身份原则；
- 加入论文内部标签公开映射检查；
- 加入模式特定 evaluator 公平性检查；
- 将 answer inversion 扩展为泄露和隐藏要求两个方向；
- 明确可修复范围和批准条件。

#### `src/stages/stage06_task_builder/prompts.py`

- Prompt 版本升级为 v26；
- 加入合法结果必须可表示；
- 加入对象绑定必须明确；
- 加入 evaluator 按模式分别确定；
- 不增加新的 Stage06 workflow、输出或 Gate 调用。

#### `src/stages/phase_gate.py`

- 在现有 `_schema_selector_target()` 附近集中实现 branch-aware schema traversal；
- 支持 selector 和 numeric leaf 位于 `oneOf`/`anyOf` 合法分支；
- 保持通用 required-chain、binding existence 和 numeric type 检查；
- 不添加科学语义、模式差异和 wildcard 禁止规则。

#### `src/stages/stage07_task_judge/stage.py`

- 仅更新 `STAGE07_IMPLEMENTATION_VERSION`；
- 保持一次审计、单模式保留、无 Stage07B、无 retry/resume 新逻辑和动态 release 装配流程。

### 9.2 预期无需修改

#### `src/agents/schemas.py`

- 保持现有 Stage07 receipt 形状和八个审计维度；
- 不新增 traceability 大对象或生命周期标签。

#### `src/stages/stage07_task_judge/validation.py`

- 现有批准条件已足以验证 receipt 的机械完整性；
- 不在这里解析科学 finding 或 evaluator 语义。

#### `src/stages/stage07_task_judge/package.py`

- release 文件布局、Agent/evaluator/metadata 隔离和 `paper_route.md` metadata 逻辑不变。

#### `src/stages/evaluator_reference.py`

- split evaluator 文件结构不变；
- 不增加执行器权重、阈值或兼容投影。

如果实际实施发现上述“无需修改”文件必须改变，应先确认变化是否仍属于 v26 目标，避免借 v26 引入无关兼容
代码。

## 10. 测试修改方案

### 10.1 Prompt 合同测试

新增 `tests/test_stage0607_v26_contract_closure.py`，检查 Stage06/07 Prompt 明确包含以下原则：

- every allowed outcome is representable；
- bounded failure/partial discovery 不得要求伪造成功数值；
- fixed systems 与 open candidate arrays 使用不同的身份策略；
- wildcard 可用于 aggregate，但不能丢失 item-specific identity；
- autonomous evaluator 不能无条件复制 reproduction evaluator；
- Stage07 执行 task → schema → evaluator → scientific object 闭环；
- 双向 answer inversion；
- Stage07 仍不能改变 objective 或创建 missing mode。

测试只检查通用原则，不绑定某篇论文或特定化学术语。

### 10.2 Common Gate 分支 schema 测试

构造通用 fixture，覆盖：

1. 成功分支要求 numeric result、失败分支要求 failure evidence，numeric binding 合法；
2. selector 只在成功 `oneOf` 分支存在且 required 时通过；
3. selector 在所有分支都不存在时阻断；
4. numeric selector 在所有合法分支都不是 number/integer 时阻断；
5. 没有任何分支 required 该字段时仍阻断；
6. 现有简单非分支 schema 行为不变。

### 10.3 既有回归测试

继续运行：

- `tests/test_stage0607_v19_contracts.py`；
- `tests/test_stage0607_v20_evidence_and_metadata.py`；
- `tests/test_stage0607_v22_dual_mode.py`；
- `tests/test_stage0607_v23_evaluator_and_finalization.py`；
- `tests/test_stage0607_v24_feasibility_and_release.py`；
- `tests/test_stage0607_v25_task_completeness.py`；
- package、release 和 benchmark task-loading 相关测试。

重点保证没有恢复 Stage07B、旧 ID、兼容投影、旧目录结构或额外 retry。

## 11. 真实回归验证方案

代码完成并与本方案逐条对照后，优先使用本轮暴露问题的三篇已发布论文回归：

1. `paper_611000e1de080f6f`；
2. `paper_76ae2dc25f0a5aeb`；
3. `paper_a5564360a31f760b`。

如需评估拒绝边界，再加入：

- `paper_9455a82229de2427`，确认明显答案泄露仍被修复或拒绝；
- `paper_2aca1dd116799b28`，确认输入不闭合仍不会被强行构建。

### 11.1 `paper_611...` 验收

- 两种模式仍保持相同 scientific objective 和正确路线披露差异；
- schema 能表达正常频率验证和科学等价验证；
- schema 能表达完成灵敏度计算和有证据资源限制；
- evaluator 不要求 Agent 为未执行计算伪造数值；
- 无新答案泄露。

### 11.2 `paper_a556...` 验收

- 固定 p-2BN、m-2BN 的数值规则有唯一体系绑定；
- 数组换序或重复匿名数值不会导致 evaluator 身份不明；
- CCDC 获取失败或端点失败有合法提交分支；
- reproduction 可以评价作者定性解释；
- autonomous evaluator 不再隐藏要求窄发射/Stokes shift，除非这些现象被作为非答案问题定义公开；
- autonomous 的过程关键点和最终结论与其公开任务一致。

### 11.3 `paper_76...` 验收

- 公开任务提供不泄露排序的立体化学判定约定，或 evaluator 接受结构性科学等价描述；
- 两个参与比较候选分别提交和评价优化、虚频和连接性验证；
- 有证据只找到一个 family 时可以合法提交 bounded failure；
- 成功找到两个 family 时仍能评价 ordering、ΔΔG 和机理解释；
- 不公开 TS 参考结构、获胜 family 或参考能量。

## 12. 方案一致性验收标准

代码实施完成后必须逐条确认：

1. Stage07 角色已经从宽泛科学审阅明确为最终科学质量与评估合同审计；
2. Stage07 对每个保留模式完成 task → schema → evaluator → object 的闭环；
3. 每个 task.md 允许的合法结果都能由 schema 诚实表达；
4. 固定体系特定结果有唯一绑定，开放候选保留身份和逐候选验证；
5. autonomous evaluator 没有未经公开问题支持的 reproduction 特有隐藏要求；
6. 论文内部标签具有答案中性的公开映射或被结构性评价替代；
7. Stage07 可以修复上述问题，但没有改变 scientific objective 或创建缺失模式；
8. Stage06 只增加三类生成约束，没有增加新的工作阶段或额外输出；
9. Common Gate 只增加标准 JSON Schema 分支解析，没有增加科学关键词和论文特例；
10. Stage07B、旧兼容投影、旧论文级 ID 和无意义标签没有恢复；
11. release 目录结构、Agent/evaluator 隔离、paper metadata 和 `paper_route.md` 隔离保持；
12. 所有定向测试、既有回归、编译检查和 `git diff --check` 通过。

## 13. 非目标

v26 不处理：

- evaluator 权重、总分、阈值和最终 benchmark 评分策略；
- tolerance 的最终人工校准；
- 计算成本和运行资源可达性判断；
- 被评测 Agent 的具体工具链；
- experiment_validation 数据管线；
- 论文之外的新科学真值；
- 用代码统一预处理所有化学输入；
- 为某种任务规定统一候选数量、统一 failure schema 或统一计算方法。

## 14. 预期效果与限制

v26 预期显著减少“任务科学上可做，但发布后才发现提交格式或 evaluator 不公平”的问题，并把 Stage07 的修复
能力用在真正需要的合同闭环上。它不能保证一次模型审计发现所有科学问题，也不能代替最终人工审查；但通过
明确逐项可追溯链、合法结果分支、对象身份和模式公平性，可以避免 Stage07 仅凭概括性描述批准任务。

最终职责划分保持简洁：

```text
Stage06：生成完整候选，尽量一次做好
Stage07：独立审计并修复已有候选，对最终科学合同负责
Gate：验证通用机械合同
人工：最终科学质量和评分规则校准
```
