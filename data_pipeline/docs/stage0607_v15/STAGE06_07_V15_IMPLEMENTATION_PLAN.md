# Stage06/07 v15 代码实现计划

状态：已根据 `STAGE06_07_V15_MINIMAL_EVALUATOR_AND_GATE_MODIFICATION_PLAN.md` 制定，作为本轮代码修改的执行清单。

## 1. 实现边界

本轮只修改 Stage06/07 evaluator 合同、Gate 共享检查、Stage06A prompt 和相关回归测试。不会恢复第一层 resume，不会新增 replay/retry，不会自动猜测或生成科学答案，不会改动 chemistry toolbox、Stage00–05 或无关的工作区修改。

v15 的职责分工固定为：

```text
Stage06A Agent  -> 生成完整 evaluator 并主动运行自查
共享 evaluator helper -> 只判断文件、引用、规则是否完整且可执行
Stage06A self-check / Stage07 external Gate -> 调用同一 helper
人工 -> 后续调整具体科学答案和 tolerance
```

## 2. 文件和函数级修改

### 2.1 `src/stages/evaluator_reference.py`

新增唯一的最小 evaluator 合同检查入口：

```python
minimal_evaluator_findings(root: Path) -> list[str]
```

该入口负责读取 `evaluator_reference/` 下五个 split 文件，并返回稳定排序的 blocking findings。它只检查：

- 三个主文件和两个辅助文件可读取且为对象；
- key point/conclusion 非空，ID 唯一，`statement`/`expected` 非空；
- 数值 key point 若声明 `unit` 则值可读；
- conclusion 的 `supporting_key_point_ids` 和 evidence ID 闭合；
- scoring rule 的 `rule_id`、`reference_id`、`type`、`binding` 完整；
- rule 覆盖全部 key point/conclusion；
- 四种 rule type 的必需字段：
  - `numeric`: `target`、`unit`、`tolerance`；
  - `ordering`、`condition`、`semantic`: `expected`；
- binding 的 artifact path 安全且属于对应 mode 的公开 `required_files`，字段选择器非空；
- 明显占位 statement/rule 文本被阻断。

共享 helper 不判断 tolerance 的数值是否科学最佳，不要求整数，不检查关键词数量，不使用 `keywords` 作为必需字段。

保留 `evaluator_reference_findings()` 作为已有 transport 调用的兼容包装，但其 evaluator policy 结果改由最小 helper 产生；旧 `acceptance_profile`/旧 evaluator type 不再作为 v15 生产格式扩展入口。

### 2.2 `src/stages/phase_gate.py`

- 将 `GATE_CHECKER_VERSION` 更新为 v15；
- 删除独立实现中的旧 `ACCEPTANCE_TYPES` policy 检查分支；
- `_v13_evaluator_reference_findings()` 改为调用 `minimal_evaluator_findings()`，只保留 self-check 所需的独立 JSON/路径检查；
- 把 helper 返回的 evaluator 完整性 findings 视为 blocking；科学容差选择和文字风格不生成 blocking finding；
- 保留 `scoring_rule_*` 前缀仅用于历史报告读取，不再用它把 v15 必需字段降级成 warning；
- 保留 snapshot、report 分离和 Stage06B external-only 行为。

### 2.3 `src/stages/stage07_task_judge/validation.py`

- `stage07_mechanical_pre_publish_check()` 直接调用 `minimal_evaluator_findings()`；
- 删除“split evaluator policy warning-only”的过滤前缀；
- 只把 helper 明确标为 completeness/transport 的 findings 加入 Gate blocking；
- 兼容 `reference.json` projection 仍然只作 transport 视图，不反向覆盖 split 文件；
- 既有 mode、公开提交文件、paper_id 和输入闭合检查保持不变。

### 2.4 `src/stages/stage06_task_builder/prompts.py`

在 Stage06A 合成 prompt 中明确：

- 五个 evaluator 文件是任务合成必需交付物；
- 逐个 key point/conclusion 生成具体参考结果和可执行评分规则；
- numeric 必须填写 `target`、`unit`、`tolerance`；其他三类必须填写具体 `expected`；
- 规则必须绑定到公开 submission schema；
- 禁止空数组、占位句、只有 ID/关键词或“报告该结果”式规则；
- 完成 canonical 输出后必须运行 `inputs/tools/phase_gate.py --phase stage06a`，修复所有 blocking findings；
- 不再要求或暗示 `keywords`、旧 acceptance profile 类型或人工检查标签。

Stage06B prompt 保持 external-only 和自主科研模式的隔离要求，不引入新的自查/retry流程。

### 2.5 `src/stages/stage07_task_judge/package.py`

- 确认五个 split 文件原样写入发布包；
- compatibility `reference.json` 只由 split projection 生成，不自动补造 target、expected、tolerance 或 binding；
- 不新增 evaluator 字段，不改变公开 submission schema。

## 3. 测试与 fixture 计划

新增 `tests/test_stage0607_v15_minimal_evaluator.py`，使用最小临时 package 覆盖：

1. 完整 numeric、ordering、condition、semantic 规则通过；
2. numeric 缺 target/unit/tolerance 分别阻断；
3. 非整数、小数或科学上未优化的 tolerance 仍通过；
4. ordering/condition/semantic 缺 expected 阻断；
5. 规则缺 binding、binding 指向非 required 文件阻断；
6. key point/conclusion 缺 statement/expected、引用不闭合或占位语句阻断；
7. 任一 key point/conclusion 没有 rule 阻断；
8. Stage06A `run()` 与 Stage07 `stage07_mechanical_pre_publish_check()` 对同一 fixture 的阻断集合一致；
9. `keywords` 缺失不再产生 Gate 阻断；
10. 旧 compatibility reference 不会重新制造 split evaluator 阻断。

更新 v13/v14 旧测试中与“scoring rule warning-only”相冲突的断言，使它们明确区分 v15 blocking completeness 和非阻断科学 diagnostics。

## 4. 执行顺序

1. 提交本计划文档；
2. 新增 v15 fixture 和失败优先测试；
3. 在 `evaluator_reference.py` 实现共享 helper；
4. 接入 `phase_gate.py` 和 Stage07 validation；
5. 收敛 Stage06A prompt，检查 package assembly；
6. 运行 v15 + v13/v14/v9 定向回归，再运行相关 Stage06/07 全量测试；
7. 生成方案一致性审计文档，逐项核对本计划与 v15 方案；
8. 只提交本轮涉及文件的 scoped Git commits；
9. 代码和回归测试确认无误后，使用同一批十篇论文提交 `gpt-5.6-sol`、`reasoning_effort=high` 合成测试；
10. 检查十篇任务的 evaluator 完整性、Stage06A self-check 与 Stage07 external Gate 一致性、科学批准和最终发布状态。

## 5. Git 管理

工作树包含大量既有修改。禁止 `git reset --hard`、`git checkout --` 或全量提交。每阶段仅对本轮文件执行 `git add -- <paths>`，建议提交：

- `docs(stage0607): add v15 implementation plan`；
- `test(stage0607): add v15 minimal evaluator fixtures`；
- `feat(stage0607): share minimal evaluator gate contract`；
- `feat(stage0607): align self-check, external gate, and prompt`；
- `docs(stage0607): record v15 consistency audit`。

如果某目标文件含有用户未提交的既有改动，先用 diff 定位交集，只提交本轮新增/修改的行。

## 6. 验收标准

- 五个 split evaluator 文件仍是唯一权威来源；
- 规则类型只有 numeric、ordering、condition、semantic；
- Agent 必须产出完整、具体、可执行规则；
- Gate 对必需字段和可执行 binding 阻断；
- Gate 不因 tolerance 格式/具体科学选择、关键词或文字风格阻断；
- Stage06A self-check 和 Stage07 external Gate 使用同一最小合同语义；
- 不新增 resume/retry/replay，不引入科学答案自动修复；
- 回归测试通过后再提交十篇论文测试。
