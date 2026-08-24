# Stage06/07 v8：Stage06A 早期合同预检与批量运行可靠性修复方案

日期：2026-08-24
状态：用户已确认；代码、通用回归与历史阻断样本副本回放均已完成
适用范围：`data_pipeline` 的 Stage06A、Stage06B、Stage07A、Stage07B 及其合同检查/批量编排代码

## 1. 方案结论

在 Stage06A 产物交给 Stage06B 之前增加一个 Gate 是合理的，但它不能是现有的发布前 Gate 的原样复制。应当实现为一个“阶段化合同预检（Stage06A preflight）”，使用少量可复用的只读检查内核，检查 Stage06A 当前阶段已经有权交付的内容；原有 Stage07 发布 Gate 保留，继续作为双模式最终防线。

目标流程如下：

```text
Stage06A task-pair builder
        │
        ├─ Stage06A preflight 失败
        │       └─ 精确 findings → Stage06A recovery attempt → 第二次 preflight
        │                       ├─ 通过 → Stage06B
        │                       └─ 仍失败 → gate_bypassed_with_warnings → Stage06B
        │
        ├─ scientific_not_constructible
        │       └─ 只检查负向 receipt 合同，不强行要求任务目录；保留科学拒绝
        │
        └─ Stage06A preflight 通过
                └─ Stage06B autonomous conversion
                        └─ Stage06B conversion preflight
                        └─ Stage07A scientific audit
                                └─ Stage07A preflight（最多两次，第二次失败也带警告放行）
                                        └─ final publish Gate
                                                ├─ safe transport findings → Stage07B 一次窄修复
                                                └─ unresolved → visible mechanical/technical blocked
```

每个阶段的 Gate 最多执行两次：第一次失败后反馈 findings 并恢复 Agent，第二次仍失败则设置 `gate_bypassed_with_warnings=true`，继续进入下一个阶段；Gate 不直接给出科学拒绝。放行的是流程控制权，不是最终发布许可，下游 Gate 和 Stage07 科学审计仍可阻断发布。

“resume 之前的对话”目前实现为可审计的文件级恢复：Codex harness 使用 `--ephemeral`，现有 `_run_phase` 会复制上一次的 outputs、生成 `RECOVERY_CONTEXT.md` 并把精确 findings 传给新的隔离尝试。这个选择不是因为 Codex 永远不能 resume，而是当前编排器主动关闭了 session 持久化。当前安装的 `codex-cli 0.147.0` 已提供 `codex exec resume [SESSION_ID] [PROMPT]`，因此本方案增加“原生 session resume 优先、文件恢复兜底”的实现路线；在并发、隔离和自定义 Responses bridge 下完成 smoke test 前，不直接切换生产批量任务。

## 2. 约束与非目标

### 2.1 必须保持的边界

代码只负责确定性的运输/合同闭合，不负责替 Agent 做科学裁决。具体包括：

- 代码可以判断文件是否存在、JSON 是否可读、路径是否安全、字段/绑定是否闭合、rubric 是否因归一化而丢失。
- 代码可以要求下游包合同所必需的结构存在，例如至少一个 `claim_role=final`；但不能自行把某个 intermediate 改成 final。
- 代码不能判断所选子流程是否代表论文主线、哪个结论更重要、数值是否科学正确、溶剂/泛函选择是否合理。这些继续由 Stage06A/Stage07A prompt 和 Agent 负责。
- 缺少当前工具箱的软件只登记为 `needs_software`/toolbox gap，不因此阻断任务。

### 2.2 Stage06A preflight 明确不检查的内容

- autonomous 目录、两模式一致性、最终发布 manifest；这些属于 Stage06B/Stage07。
- 真实评分或 evaluator 运行；没有 submission 时只做无答案的 schema/binding 诊断。
- 论文科学代表性、路线中心性、答案数值、容差和机制解释。
- 从 `scientific_not_constructible` 结果凭空重建完整任务。

### 2.3 不引入的复杂架构

本轮不引入大型 `CanonicalTask` 对象、不重写三种任务模式的 benchmark 总架构、不把所有投影文件合并为新目录。只增加阶段 profile、复用已有合同函数，并修正已确认的数据丢失/误报。

### 2.4 原生 Codex session resume 的可行性与边界

本地检查得到的事实：

- `src/agents/harness.py` 的 Codex 命令固定包含 `codex exec --ephemeral`，所以当前每次 Agent attempt 都不会在 Codex 本地保存可供 `resume` 查找的 session。
- 每次 `_run_phase` recovery 都新建 `attempt-*` workspace；prompt 也明确写着 “fresh isolated session”。这解释了当前为什么只能通过 `RECOVERY_CONTEXT.md` 做文件级恢复。
- 本机 CLI 同时支持 `codex exec resume <SESSION_ID> <PROMPT>`，但 resume 命令不提供与首次调用完全相同的 `-C` 参数；它依赖原 session 的工作目录/配置。因此不能只删除 `--ephemeral` 就认为恢复已经正确。

推荐的实现顺序：

1. 对 Stage06A、Stage06B、Stage07A 各增加 `native_resume` 配置开关，默认先关闭。
2. 首次 Codex 调用不使用 `--ephemeral`，从 JSONL 的 `thread.started` 事件提取 session/thread ID，写入阶段审计文件；绝不使用 `--last`，每篇论文每个 phase 始终使用显式 ID。
3. recovery 复用同一个 phase workspace（保留输入和已有 outputs），调用 `codex exec resume <id> <recovery prompt>`；每次尝试仍单独归档 before/after manifest，保证审计可追溯。
4. 验证模型、provider、Responses bridge、output schema、隐藏材料权限和工具调用限制在 resume 后保持一致。Responses API 本身支持用 conversation 或 previous response 建立多轮状态，但自定义 bridge 是否完整保留 Codex CLI 的本地 session 语义必须通过实际 smoke test 确认。[官方 Responses API 文档](https://developers.openai.com/api/reference/cli/resources/responses/methods/create)说明了 `conversation` 与 `previous_response_id` 的多轮状态机制。
5. 若 session ID 丢失、resume 返回不兼容、workspace 不可恢复或 bridge 不支持，则自动退回现有文件级 recovery，不把基础设施问题转成科学拒绝。
6. 原生 session 会把 prompt/工具轨迹持久化到本地，可能包含 hidden reference；必须为每个 pipeline run 使用隔离的 Codex session storage、限制权限、记录保留期限，并在 batch 完成后按策略清理。

因此，原生 resume 是可实现的增强项，但需要先做单篇、双阶段、并发三项验证；在验证前继续使用现有文件恢复不会丢失科学内容，只是模型看不到原始对话上下文。

实施结果（2026-08-24）：当前 Codex CLI `0.147.0` 已通过显式 UUID 命令解析、`thread.started` 提取、假 CLI 首次调用→resume smoke 和 resume 失败→文件恢复回退测试。Stage06A、Stage06B、Stage07A 的 Codex Gate recovery 默认启用显式 session resume，可通过配置关闭；并发路径不使用 `--last`，会话目录按 paper/phase 隔离。

## 3. 批量运行证据与问题归因

当前批次 `runs/stage06-07-bulk-gpt-gpt582-concurrency20-20260824` 的目录仍显示 `state=RUNNING`，但结果文件只记录到 152 篇（124 completed、28 failed），因此不能把它当作 582 篇完整批次。已处理结果中：

- Stage06：30 个 provisional constructed、102 个 provisional not constructible、20 个 retryable failure。
- Stage07：24 个 scientific audit passed，7 个 publish-ready，17 个科学批准后未发布（10 个 prepublish mechanical、6 个 task-package、1 个 Stage07B 阶段阻断）。
- 另有 8 个 Stage07 objective failure retryable；这些首先是 Agent/harness 运行失败，不应被误报成科学拒绝。

17 个阻断的谱系不是同一类：

| 类别 | 数量 | 根因归属 | 处理原则 |
|---|---:|---|---|
| `patternProperties` schema walker 误报 | 1 | 代码 | 修复两个 schema walker 并加回归测试 |
| Stage07 同时保留 shared binding 与 mode matrix | 6 | Stage07 prompt/Agent，代码合同正确阻断 | 明确 prompt；允许 Stage07B 只做可证明安全的冗余清理 |
| Stage06A 没有任何 `final` claim | 6 | Stage06A prompt/模型未执行合同，代码只检查了枚举 | Stage06A preflight 反馈并重试；不由代码升级 claim |
| Stage07 从 `scientific_not_constructible`/空树恢复不完整 | 3 | Stage07 prompt/职责边界 | 禁止普通批准路径从零猜建；需完整合同后才可继续 |
| rubric 归一化把 `key_points` 丢成空列表 | 1 | 明确代码 bug | 实现无损统一 normalizer，未知非空包装不得静默变空 |

另外，批次中的 `agent_process_failed`、`agent_timeout`、`stage07_objective_failure_retryable` 需要单独归为 harness/网关/模型运行可靠性问题；它们不能通过增加科学规则解决。批次状态残留 `RUNNING` 则是编排状态持久化问题。

当前 checkout 中 `_evaluator_dry_run` 已有 `applies_to_modes` 过滤，Stage06 hidden-reference 归一化也已尝试保留显式 mode scope。因此历史批次中关于“所有 profile 都被两个 mode 检查”的结论必须用当前代码回放确认，不能直接重复实现；本轮只补回归测试，防止回退。

## 4. 具体修改方案

### P0-A：新增 Stage06A 合同预检并接入 recovery

#### 代码位置

- 在 `src/stages/stage06_task_builder/validation.py` 增加 `stage06a_preflight(...)`。
- 在 `src/stages/stage06_task_builder/stage.py` 的 `task_pair_builder` `_run_phase` 中，把现有窄运输检查与 Stage06A preflight 组合；或由一个小的组合函数调用两者。
- 将结果写入 Stage06A handoff 的 `stage06a_preflight.json`，并在构建记录中保存 `attempt`、`findings`、输入 fingerprint 和产物 manifest。

#### 通过条件

仅针对 `candidate_ready/constructed`：

1. `workflow_review.json`、`construction_receipt.json`、`hidden_reference/ground_truth_common.json` 和 `paper_reproduction/` 的阶段必需文件存在且可读。
2. reproduction 的 `task.md`、`task_info.json`、`task_spec.json`、`submission_contract.json`、`process_rubric.json`、`workflow_spec.json` 存在；`data/inputs` 中实际文件与公开资产声明连通，路径相对且无目录穿越。
3. hidden reference 为 `ready`，ground-truth item/profile ID 唯一；每个 item 有且只有一个 profile；profile 类型、证据引用和 reproduction binding 合法。
4. `applies_to_modes` 显式值被保留并按适用 mode 检查；缺失字段只按已有 legacy 规则视为 shared，不能覆盖显式的 mode-specific scope。
5. 至少一个过程 Key Point；至少一个 `claim_role=final`。这是下游 Task Package 的结构要求，不代表代码选择科学结论；若没有 final，只报告 finding，让 Agent 根据源材料修复或拒绝。
6. reproduction rubric 是非空列表，所有 Agent 给出的 criteria/key points 均被无损保留；route-fidelity criterion 的证据路径在声明中存在时必须可解析。
7. `public_to_private_asset_map.json`、`workflow_completeness_check.json`、toolbox requirements 等 handoff 元数据可读；缺失只在确实需要该元数据时报告，不能把空的可选 telemetry 当作科学失败。

#### 失败处理

- 第一次 Gate findings 作为 `invalid_phase_contract` 进入现有 `_run_phase` recovery；`RECOVERY_CONTEXT.md` 明确列出文件、JSON path、期望和当前值。
- 第二次 Gate 仍有 findings 时，不把论文改写为科学拒绝，也不直接终止管线；写入 `stage06a_gate_bypassed`、`gate_attempts=2`、`gate_findings` 和 `gate_warning=true`，将当前可用 handoff 继续交给 Stage06B。
- Gate 放行不代表产物合同已经正确。Stage06B 必须读取并记录该 warning；若缺少它所需的输入，Stage06B 可以返回 `conversion_uncertain` 或自身的 gate warning，但不能伪造文件。
- 只有 Agent/harness 无法启动、输入 snapshot 不存在等执行级错误才走既有 retryable failure；Gate finding 本身不产生不可恢复的 scientific reject。
- 对 `scientific_not_constructible` 只验证负向 receipt（decision、reason、milestones、无半成品 task tree）；不因缺少 reproduction 文件而回环，也不为了 fail-open 凭空创建任务目录。

### P0-A.1：Stage06B conversion preflight

Stage06B 完成 autonomous conversion 后增加同样的两次检查：

1. 第一次检查 autonomous 必需文件、公开输入资产、脱敏字段、边界条件、mode metadata 和 conversion report 的结构闭合；不检查隐藏答案科学正确性。
2. 失败时将精确 findings 反馈给 Stage06B Agent（原生 resume 优先，文件恢复兜底），只允许一次修复。
3. 第二次仍失败则写入 `stage06b_gate_bypassed` 并进入 Stage07A；Stage07A 输入中必须显式带 warning 和 findings，不能把它当作 clean candidate。

Stage06B Gate 不检查 reproduction 的科学内容，也不要求两个 mode 的最终 binding 一致；这些留给 Stage07A/最终 Gate。

### P0-A.2：Stage07A audit preflight

Stage07A Agent 返回科学审计结果和候选修复后，在执行最终发布 Gate 前增加一个阶段预检：

1. 第一次检查 Stage07A 的审计结果、repair patch、双模式目录、hidden reference 投影、binding/rubric/schema 引用是否闭合。
2. 失败时把 findings 反馈给同一个 Stage07A Agent，最多恢复一次；这一步可以使用原生 Codex session resume，也可以退回当前文件级恢复。
3. 第二次仍失败则写入 `stage07a_gate_bypassed` 并继续进入现有最终发布 Gate。最终 Gate 仍可阻断发布，但不能把“预检二次失败”直接记为科学拒绝。

Stage07A preflight 不替代 Stage07 的科学审计，也不把 Stage07B 变成第三次科学重试。Stage07B 仍只处理最终 Gate 明确 allowlist 的运输问题。

### P0-B：修复已确认的代码数据丢失与 schema 误报

#### 1. 支持 `patternProperties`

目前 `src/stages/stage07_task_judge/validation.py` 和 `researchchembench_contracts/task_package.py` 各有一份 schema path walker，均未完整处理 `patternProperties`，导致合法的 `asset_01` 等字段被判定缺失。

实施方式：

- 提取一个小型、无科学语义的 JSON Schema path resolver，或让两处共享同一实现。
- 对对象字段依次支持 `properties`、`patternProperties`、`additionalProperties`；匹配到 pattern 时返回其子 schema。
- 保留 `open`/`present`/`missing` 三态，不把开放 schema 自动当作显式字段存在。
- 增加 patternProperties、additionalProperties、数组通配符、缺失字段四组单元测试，并回放 `paper_084ee9610f1503dd`。

#### 2. rubric 无损归一化

当前 `_normalize_process_rubric()` 只读取 `criteria`，遇到 `{"key_points": [...]}` 会返回空数组；另一个 normalizer 只支持 `criteria/items/rubric`。修改为一个统一 helper，支持：

- 直接 list；
- `criteria`、`items`、`rubric`、`key_points` 包装；
- 每一行保留原字段，只补充稳定 `id`/`description`/`max_score` 别名，不删除科学内容；
- 多个包装同时存在时合并并去重，而不是任意覆盖；
- 非空但未知的 wrapper 返回明确 finding，绝不能静默变成 `[]`。

同时统一 `required_artifact` 与 `evidence_artifacts` 的只读别名投影。投影必须写入 provenance，且不能改变 profile 的答案、容差或 claim role。回放 `paper_2add3fc3e8afd205`，确认原始三项 rubric 在 Stage06A、Stage07 和最终 package 中数量与内容一致。

### P0-C：保持最终 Gate，但改为真正的只读防线

现有 `stage07_mechanical_pre_publish_check()` 会在检查过程中写回多个 task 文件。后续调整为：

- 规范化在进入 Gate 前的独立 transport-normalization 步骤完成；或在临时副本上计算；
- Gate 本身只读并返回 findings；
- 每次确定性投影记录到 `orchestrator_normalizations.json`（文件、JSON path、前后 hash、规则版本）；
- Agent 原始输出、Stage07 repair patch、orchestrator normalization 三者在审计记录中分开。

这项修改不改变 Gate 的科学边界，只避免“检查顺手改文件后无法追溯”。

### P0-D：修复 Stage07B 路由，但限制权限

Stage07B 仍只在 Stage07 scientific approval 之后运行一次，不能变成第二个科学审计 Agent。允许的 finding 必须是可证明的运输修复，例如：

- 缺少安全的 required file/schema 元数据；
- legacy binding 字段别名；
- shared binding 与完整、等价的 mode matrix 同时存在时，删除冗余 shared binding；
- manifest/hash 或 public metadata 的机械投影。

新增 `acceptance_submission_binding_ambiguous` 的路由前缀时必须加保护：只有 mode matrix 覆盖所有适用 mode、每行 binding 可加载且科学字段 hash 不变，才允许删除 shared binding；否则交回 Stage07A 或保持 blocked。

Stage07B 明确禁止处理：缺 final conclusion、缺源资产、科学答案/容差、路线中心性、机制判断、从空任务树重建任务、软件选择。修复后只允许一次机械复检；失败输出 `mechanical_blocked_unresolved`，不可静默放行。

### P0-E：限制 Stage07 从科学拒绝恢复的范围

Stage07 收到 `scientific_not_constructible` 且没有 provisional task tree 时，不应按普通 approved candidate 从零构造并直接进入发布 Gate。默认行为：

- 保留 Stage06 科学拒绝及其理由，Stage07 只做拒绝记录完整性检查；
- 只有在显式配置的“科学恢复”路径下才允许 Stage07 尝试重建；
- 恢复产物必须先通过完整 Stage07 scientific audit 和全量合同 Gate，不能因为目录非空而批准；
- 恢复失败归为 `scientific_recovery_incomplete`，不交给 Stage07B。

### P1：prompt 与 Agent 职责修订

#### Stage06A prompt

在现有科学选择要求后加入短的结构化交付表：

- `workflow_completeness_check`：输入、参考态、中间产物、输出、软件逐项列出；
- `claim_role`：明确哪些是 intermediate、哪些是 final；至少一个 final，但由 Agent 根据论文证据决定；
- `public_to_private_asset_map`：只记录 ID 映射，不暴露答案；
- `toolbox_requirements`：列出当前工具箱之外的软件，不因缺软件拒绝；
- `scope_selection_record`：说明选择全文路线、核心子流程或拒绝，以及证据和降级原因。

恢复 prompt 只要求修复 Gate findings，不增加新的科学主张，不把代码 finding解释为论文科学错误。

#### Stage06B prompt

保持答案盲，不增加正文/SI 的答案访问权。它只接收 Stage06A 的公开转换包、ID 映射、preserve/remove 白名单和必要的边界条件；完成脱敏和自主表面转换后输出自身合同。缺失科学输入由 Stage06A 修复，不由 Stage06B 猜测。

#### Stage07A prompt

将审计与修复明确分成两个输出：先 immutable scientific audit，再输出结构化 repair patch。补充一条通用规则：同一 profile 要么使用 shared binding，要么使用覆盖适用 mode 的 matrix，不得两者并存。对于 Stage06 scientific rejection，不得把从零重建视为普通合同修复。

同时明确文件职责：`task.md` 是唯一的科学任务指令来源；`task_info.json`、`task_spec.json` 和 `workflow_spec.json` 只保存结构化元数据/机器合同，不得各自携带一份可与 `task.md` 漂移的任务指令。发布时可以保留兼容字段，但由 `task.md` 派生或校验，不能把它们当作第二个科学任务文本。

`route_evidence_map.json` 采用白名单投影：公开面只保留 software、method、basis、solvent、路线顺序、验证操作和输入事实；target values、target ordering、机制结论、preferred route 和 acceptance tolerance 继续留在 private evidence。该边界适用于 reproduction 和 autonomous 的相应公开表面，不为单篇论文添加关键词规则。

#### Stage07B prompt

只接受 allowlisted transport findings，输出 changed files、before/after findings、science hash before/after 和 unresolved 状态；不能编辑 hidden answer、claim role、容差、workflow scope 或 input assets。

### P1：批量编排与可观测性修复

- 将批次状态明确区分 `RUNNING`、`PAUSED`、`COMPLETED`、`FAILED`；停止/暂停时原子写入状态和原因，启动时根据子任务状态修复陈旧 `RUNNING`。
- 在批次汇总中分开记录：Agent execution failure、Stage06A contract blocked、scientific rejection、Stage07 mechanical blocked、Stage07B unresolved、published。
- 对 `agent_process_failed`、429、超时等可重试基础设施故障使用有限退避；不要重复调用 Stage07B或增加科学规则。
- 每篇论文保留阶段 fingerprint、attempt、输入/输出 hash、Gate findings 和恢复上下文路径，支持历史产物回放。

## 5. 实施顺序与提交边界

按以下小步提交，每步都可单独回滚：

1. 建立当前代码基线 tag/commit，并添加本方案对应的变更日志。
2. 先修 patternProperties resolver 和 rubric 无损 normalizer；只加单元/fixture 测试，不改变 Agent prompt。
3. 实现 Stage06A preflight、两次 Gate/fail-open 状态和 `_run_phase` recovery 接入；添加 candidate-ready、缺 final、缺资产、scientific rejection 五类测试。
4. 为 Stage06B 和 Stage07A 增加各自的两次 preflight；第二次失败只写 warning 并进入下一个阶段，不直接拒绝。
5. 将 Stage07 Gate 的 normalization 前置并记录 provenance，确保最终 Gate 只读。
6. 修 Stage07B allowlist/安全判定和 Stage07 空树恢复路由。
7. 在隔离测试目录实现 Codex native resume smoke test；通过后再开放配置开关，失败自动回退文件级恢复。
8. 精简并统一 Stage06A/Stage07A/Stage07B prompt，更新 schema 版本/实现版本。
9. 修批量状态和审计摘要，增加 `gate_attempts`、`gate_bypassed`、`gate_findings`、`resume_mode` 和 `session_id`（脱敏/摘要）字段。
10. 回放历史 17 个阻断样本及 20 个 Stage06 retryable/8 个 Stage07 objective failure；确认问题分类没有互相转移。
11. 通过回放后再用新目录提交小批量（建议 10 篇、并发 10），观察三个阶段的 Gate recovery/fail-open；再扩大到 20 篇。不得在旧暂停目录上续跑，避免混入旧代码产物。

## 6. 回归测试清单

### 单元测试

- `patternProperties` 对象字段可解析；不存在字段仍被阻断。
- `key_points` rubric 包装无损转换；未知非空 wrapper 报错而不变空。
- `required_artifact`/`evidence_artifacts` 等价读取。
- profile `applies_to_modes`：reproduction-only、autonomous-only、shared 三种情况；不适用 profile 不参与 evaluator dry run。
- shared binding 与完整 mode matrix 的安全冗余清理；不完整 matrix 不可自动修复。
- Stage06A preflight 不检查尚未生成的 autonomous 目录。
- 三个阶段均只执行最多两次 Gate；第二次失败会带 warning 进入下一阶段，不产生自动科学拒绝。
- native resume 成功时同一 session/thread ID 被显式使用；resume 失败时可审计地回退到文件恢复。
- Gate 检查不会修改输入文件；normalization provenance 可重放。

### 历史回放验收

| 样本 | 预期 |
|---|---|
| `paper_084ee9610f1503dd` | 不再因 `patternProperties` 产生 32 个字段缺失；继续真实合同检查 |
| 6 个 shared/matrix 冲突样本 | Stage07A/Stage07B按安全条件修复或明确阻断，不误报为科学失败 |
| 6 个无 final 样本 | Stage06A preflight 早发现并反馈；不得由后续代码静默升级 |
| 3 个空树恢复样本 | 不得从不完整重建直接发布；保留科学恢复未完成状态 |
| `paper_2add3fc3e8afd205` | rubric 三项内容全程保留，evaluator schema 可加载 |
| 20 个 Agent/harness 失败样本 | 状态归类为可重试运行失败，不生成虚假的科学结论 |

## 7. 完成标准

本轮不以“所有论文都发布”为目标，而以以下工程和角色边界为完成标准：

- Stage06A 能在 Stage06B 前捕获并反馈确定性的缺文件/合同闭合问题；最多恢复一次，第二次仍失败也能带警告进入 Stage06B，恢复上下文可追溯。
- Stage06B 和 Stage07A 具有同样的两次检查/一次恢复/fail-open 行为，且下游能看见上游 Gate warning。
- Codex native resume 在隔离 smoke test 中可用；不可用时文件级 recovery 仍然可靠。
- Stage06B 不获得隐藏答案访问权，且只负责自主表面转换。
- Stage07A 负责科学审计，Stage07B 只处理有限运输合同问题；科学拒绝、科学不确定和机械阻断不被混淆。
- 最终 Gate 对合法 schema/profile/binding 不误报，且不修改未经记录的文件。
- rubric、hidden reference、mode scope 和公开资产不因代码归一化丢失。
- 批次状态、失败类别和发布阻断原因可从 summary 直接解释；不存在 `approved` 但静默未发布的状态。
- 历史回放和至少一轮新小批量测试通过后，才进入更大规模批量合成。

## 8. 暂不处理的事项

- 不为个别论文添加特殊规则或关键词。
- 不要求每篇论文都能构造任务；源材料不足时允许科学拒绝。
- 不把软件不在工具箱中变成拒绝条件。
- 不在本轮重写 benchmark 的评分政策；Stage06/07 只提供过程 Key Point、最终结论和可绑定答案，评分适配层另行维护。

## 9. 实施与验证索引

具体修改过程、测试命令、历史回放样本和最终审查清单见：

[Stage06/07 v8 早期 Gate 实施日志](STAGE06_07_V8_EARLY_GATE_IMPLEMENTATION_LOG_20260824.md)

本轮按用户要求只使用历史被阻断任务的临时副本回放，没有覆盖旧批次，也没有启动新的模型批次。历史回放用于验证 Gate 路由、误报修复和 science freeze；论文是否科学可构建仍由 Stage06A/Stage07A 判断。
