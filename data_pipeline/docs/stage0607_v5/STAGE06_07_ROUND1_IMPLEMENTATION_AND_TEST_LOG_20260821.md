# Stage06/07 v5 第1轮实施与回归记录

日期：2026-08-21
基线：`6bf06ae`（v5 总目标/Stage07B 边界文档）
范围：仅 Stage06/07、相关回归测试和本目录文档；Stage00–05 未修改。

## 本轮目标

按照 v5 总目标先处理已确认的通用合同问题：mode applicability、mode-specific binding/scope、公共自主别名、route evidence 安全投影、评分策略不强制，以及机械归一化可追溯性。科学输入闭合、参考态、溶剂和化学结论仍由 Stage06A/Stage07 Agent 审计，不写成论文特例代码。

## 实施内容

### 1. evaluator 与 mode scope

- Stage07 dry-run 先按 `applies_to_modes` 过滤 profile；不适用 mode 不再误报缺 binding。
- 支持规范 `mode_submission_bindings`，兼容旧 `submission_bindings_by_mode` 和嵌套 mode map；显式 mode map 缺键时不回退到另一个 mode。
- private Ground Truth 投影按 truth/profile/rubric scope 过滤，并为当前 mode 选择单一 binding；`expected_result`/reference evidence 的按 ID 内容同步投影。
- Stage06 hidden validator 保留 shared、reproduction-only、autonomous-only scope，并检查 truth/profile scope 包含关系；不再无条件扩大为双模式。

### 2. 评分边界与 rubric

- 合成管线不再注入 `dual_axis_100`、`score_max=100` 或总分 100。
- 过程 rubric 和结论 rubric 只要求非空、唯一 ID、Key Point/证据字段；已有旧分数字段仍可读取。
- 修复 bootstrap、Stage06A 指令和 route-rubric 注入中残留的“总分 100”逻辑。新增 route Key Point 时保留 Agent 已给出的分数字段，不重配平、不发明权重。
- 两个 public mode 的 submission contract 不再由 Stage06 用 reproduction 副本覆盖 autonomous 副本；允许中性文件名/字段名和不同结果表示，分别规范化。

### 3. public surface 隔离

- 自主 mode 的 Ground Truth/claim 引用投影为 `kp_###` 中性 alias，移除 public metadata 中的 private acceptance profile IDs。
- 对 public `results_schema.properties`/`required` 中恰好匹配的 private key-point ID 做同样 alias 投影；不改科学结果字段的其他名称和值。
- `route_evidence_map.json` 只由安全索引投影生成（evidence ID、步骤索引、路线类别/角色等），Prompt 明确禁止目标值、排序、结论、DOI、源路径和答案段落。

### 4. provenance 与状态

- mechanical normalization 前后 SHA256、文件列表和 findings 写入 pair-level `orchestrator_normalizations.json`，不复制到 public mode。
- Stage07 audit response/summary 暴露 orchestrator normalization 记录；Agent 自报字段保持 `agent_observed_*` 语义。

## 验证结果

- `python -m compileall -q src/stages/stage06_task_builder src/stages/stage07_task_judge`：通过。
- `git diff --check`：通过。
- Stage06/07 定向测试：`159 passed`。
- 全量测试：`533 passed`。
- `ruff` 未安装，未执行。

## 本轮未做的事（有意保留）

- 未实现 Stage07B；按总目标，必须先观察修复通用 gate 后的批量证据，达到“10 篇中至少 2 篇同类简单合同阻断或连续两批重复”才启用。
- 未把化学计量、参考态、TS 动作、溶剂等变成代码规则；这些属于 Agent 科学审计和 Prompt 责任。
- 未要求任何统一评分模式、总分或权重。

## 待进行模型回归

提交本轮 Git 版本后，从 Stage05 通过集合中固定随机抽取 10 篇，使用 DeepSeek-v4-pro-0813、Codex harness、reasoning `high`、并发 10。逐篇记录：Stage06A 范围/闭合检查、Stage06B 脱敏、Stage07 科学决定、mode-aware binding、mechanical findings、发布树和任何共性代码/Prompt 问题。

## 风险观察

1. 实际 evaluator schema 包不在当前工作树中，真实 schema load 需在模型批量运行时确认。
2. 旧任务可能仍有历史分数字段；本轮只停止新任务强制生成，不破坏旧包读取兼容。
3. Stage07B 是否必要必须由批量统计决定，不能因单个科学失败或模型能力不足提前加入。

## 第一批运行中的问题归因（截至 8/10 进入 Stage07 终态）

批次目录：`runs/stage06-07-v5-round1-deepseek10-concurrency10-20260821-retry/`

- 模型与执行方式：DeepSeek-v4-pro-0813、Codex harness、reasoning `high`、并发 10。
- 已进入 Stage07 终态的 8 篇中，5 篇发布，1 篇科学拒绝，2 篇为“科学批准但机械阻断”。
- 已确认的科学拒绝来自源材料缺失/输入无法闭合，属于 Stage07 应报告的科学结果，不是代码 bug。
- `paper_aaa1ccd72d1c2b28` 的 4 条 `evaluator_binding_field_missing` 是通用代码 bug：binding 明确声明 `document_binding: true`，但 gate 仍把 JSONPath 形状的语义 selector 当作 `results_schema` 字段检查。
- `paper_7cfd59d5c7061c6b` 的 `evaluator_binding_path_invalid` 使用了以数字开头的对象键点式路径；该字符串不是当前支持的 JSONPath 子集。它暂归 Stage07 合同输出/Prompt 质量问题，不能用论文特例规则掩盖，待下一批观察是否重复。

## 第一轮收尾修补（提交 `9243218`）

- `_evaluator_dry_run()` 遇到显式 `document_binding: true` 时，只校验安全文档 artifact 路径，将 observed selector 记为 unchecked diagnostic，不再将其解释为结构化 JSONPath。
- 增加闭合结果 schema + `$.textual_*` 文档 selector 的回归用例；Stage06/07 测试文件当前 `147 passed`。
- 对 `paper_aaa1ccd72d1c2b28` 的最终 audited task tree 回放后，机械状态从 `failed` 变为 `passed`，除预期诊断外无 finding。
- 该修补不改变科学 truth、rubric 数量/评分模式或任何论文特例规则。

第一批剩余 2 篇仍在运行，最终统计在终态后补充；之后重新抽取 10 篇进行第 2 轮回归。Stage07B 目前不启用：已知的两类阻断并非同类，且其中一类已由通用 gate 修复。

## 第一批最终统计与归因

10 篇均已进入终态：

- Stage06A：10/10 `provisional_constructed`；Stage06B 均完成自主表面转换。
- Stage07：8 篇 `approved_with_repairs`，2 篇 `rejected_scientific_unrepairable`。
- 发布：6 篇；科学拒绝 2 篇；机械阻断 2 篇。
- 两篇科学拒绝分别因为源材料没有闭合的反应物/坐标/电子态，或无法区分所需的磁性参考态；Agent 给出了证据和不可修复结论，符合角色职责，不是代码失败。

机械问题分为三类，不能合并统计为一个 Stage07B 触发信号：

1. `paper_aaa1ccd72d1c2b28`：显式 `document_binding=true` 却被 gate 当成 JSONPath。已由提交 `9243218` 修复；对最终 audited tree 回放后状态为 `passed`，因此不再是当前阻断。
2. `paper_7cfd59d5c7061c6b`：Stage07 生成了 `$.relative_electronic_energies_kcal_mol.61TS2b` 形式的非法点式路径。对象键以数字开头时应使用 bracket-quoted JSONPath；已在 Stage06A/Stage07 Prompt 中补充通用规则（提交 `e3223bf`），本批旧运行不会反映该 Prompt 修复，待下一批验证。
3. 3 篇首次尝试出现 `hidden_ground_truth_task_pair_id_mismatch`，随后由确定性 canonicalization/Agent retry 修复并发布；这是模型初稿合同漂移，不是最终 gate 误报。

公共表面抽查：6 个已发布 pair 的结构检查全部通过；未发现 `gt_*`/`canonical_answer` 等 private 标记进入公共树。`route_evidence_map` 均为 evidence ID 索引；其中一篇使用了 `target_quantities` 作为类别键，内容仍只有 evidence IDs，但该键名会暗示答案语义，已通过 Prompt 增加中性类别白名单/禁用 `target|answer|preferred|conclusion` 键名（提交 `f58159f`），下一批继续观察。

第一批没有出现同一类、仍需 Stage07B 批量处理的简单合同阻断。按 v5 启用条件，Stage07B 暂不实现；第 2 轮重点验证 bracket selector 和 route-map 中性类别是否消除共性问题。
