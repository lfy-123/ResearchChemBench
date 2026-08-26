# Stage06/07 v18 代码清理与权威契约修改方案

## 1. 目标与范围

本方案针对 Stage06/07 当前实现中的旧路径、重复 Gate、兼容投影和多层 retry/resume
残留。目标不是放宽科学审查，而是让当前真正执行的流程只有一套清晰契约：

1. Stage06 负责一次性生成完整的双模式任务包，并在 Agent 内完成自查；代码只做一次
   外部只读 Gate 和确定性的文件装配。
2. Stage07 只负责审计 Stage06 产物、做有限的科学/评估文件修复，不能在 Stage06
   科学拒绝或不可修复时重新构建新任务。
3. split evaluator 文件是唯一权威参考；不再以旧的
   `ground_truth_common.json`/`evaluation/reference.json` 作为执行契约，也不再用
   有损兼容投影决定发布。
4. 一篇论文只使用一个规范身份 `paper_id`。模式由目录和 `task_mode` 表示；
   `key_point_id`、`conclusion_id`、`rule_id` 仍是评估文件内部实体 ID，不属于论文身份。
5. 技术失败、科学拒绝和成功发布必须是互斥且可解释的终态，不因旧批次缓存或兼容
   字段被误报为 retryable failure。

本轮只改 Stage06/07 及其直接契约、配置和测试；不修改 Stage00–05 的 resume、
API runner 或 chemistry toolbox。

## 2. 当前审查结论

### 2.1 Stage06 残留

当前入口 `run_stage06()` 实际调用 `_run_stage06_single_agent()`，但同一文件仍保留：

- `_run_stage06_legacy()` 完整旧 multi-phase builder；
- `deterministic_builder_audit()` 的旧三对象兼容调用；
- `_stage06a_legacy_phase_gate_findings()` 和旧 Gate recovery 分支；
- `resume`、`codex_native_resume`、`recovery_context`、`recovery_workspace`；
- Agent retry/backoff、失败 checkpoint 恢复和 `phase_gate_report.json` fallback；
- `single_agent`、`isolated_converter`、`legacy_multi_phase` 等已不应继续暴露的策略值。

这些代码会让同一份产物有多个判定来源，并且会把“文件不完整”重新包装成对话恢复或
retry，而不是一次清楚的终态。

### 2.2 Stage07 残留

当前入口调用 `_run_audit_repair_agent()`，但文件仍保留：

- 开头直接抛出异常、后面数百行不可达的 `_run_audit_agent()`；
- `_stage07a_legacy_phase_gate_findings()`；
- 明确 disabled 的 `deterministic_judge_audit()` 和旧 `run_gold()`；
- objective-audit retry/resume/recovery 实现；
- `legacy_reference_from_split()` 投影；
- Stage07B contract-repair Agent 及其配置、报告和二次组装路径。

不可达代码仍会被导入、测试和配置引用，导致维护者误以为它是有效流程；Stage07B
还会使“审计失败后再启动一个模型”看起来像隐式 retry，扩大科学改写边界。

### 2.3 evaluator 残留

当前 `evaluator_reference.py` 同时实现 split→legacy 和 legacy→split 两个方向。
典型 round-trip 损失包括 binding、字段 selector、`expected`/`reference_value`
和 `answer_items` 丢失，最终只能生成 answer-free compatibility stub，并留下
`split_reference_compatibility_projection_warning`。权威 split evaluator 已经足够
表达关键点、结论、规则、证据和关键失败条件，不应继续承担旧消费者适配职责。

### 2.4 批次状态残留

`_late_stage_pipeline_failure()` 已经能够识别 Stage06 科学拒绝，但旧运行生成的状态
不会被回写，仍可能留下 `FAILED/stage07_not_run`。需要定义新的终态并让批次汇总使用：

```json
{"state": "COMPLETED", "outcome": "scientific_rejection"}
```

只有技术不可用或契约无法装配才是 `FAILED`；科学拒绝不触发 retry，也不等待 Stage07。

## 3. 目标架构与数据流

### 3.1 Stage06

每篇论文执行以下固定流程，各 Agent invocation 最多一次：

1. 代码建立只读 source snapshot，并由 Stage06A Agent 检查科学目标所需输入是否
   存在、可读、相互闭合；输入不完整时写出科学不可构建 receipt。
2. Stage06A Agent 生成论文复现任务、autonomous 任务、split evaluator 五类文件和
   自查报告。Prompt 明确自查是完成任务的必需步骤，但编排器不解析 Agent 的自查文本
   来触发第二次对话。
3. 代码在 canonicalization 后运行同一份 `_stage06a_phase_gate_findings()`，只验证
   必需文件、路径、JSON、`paper_id`、关键点/结论/规则交叉引用、可执行 binding 和
   输入闭合。规则的科学 tolerance 选择不按固定数值阻断，但空模板、缺 expected、
   缺 comparison 或无法定位提交字段必须阻断。
4. Stage06B 只做一次 reproduction→autonomous 文件转换；不接受 `resume`、对话恢复或
   retry。转换失败即记录 `conversion_failed`/`conversion_uncertain`，由 Stage07 审计
   后拒绝或有限修复，不再由 Stage06B 自己重跑。
5. 每篇论文最终只输出一个 `paper_id`；若底层 Task Package v1 仍要求 `task_id` 或
   `task_family_id`，它们必须由代码写成同一个 `paper_id`，不得另行生成或接受 Agent
   提议的身份。

### 3.2 Stage07

Stage07A 是唯一模型审计入口，输入只包括：

- Stage06 handoff/task pair 的公开模式文件；
- split evaluator 文件（只读、不可把隐藏答案投影到 public mode）；
- Stage06 receipt、workflow review、manifest、toolbox/resource metadata；
- 必要的论文证据索引。

Stage07A 只能做三类决定：

- `approved` / `approved_with_repairs`：科学目标和评估文件完整，可发布；
- `rejected_scientific_unrepairable`：目标、输入闭合性或评估参考无法合理修复；
- `technical_blocked`：文件/装配/Schema/路径等技术问题无法确定性修复。

Stage07A 可以在同一次 Agent 调用中修改明确白名单内的任务指令、输入映射和 evaluator
文件，但不能改变论文的科学目标、凭空添加论文未支持的答案或重新选择一篇新任务。
Stage07 不因 Stage06 scientific rejection 重新构建任务。

Stage07B contract-repair Agent **删除**。所有 public/private 文件投影、manifest、
package schema 和路径规范化由代码一次完成；失败直接进入 `technical_blocked`，保留
明确 findings，避免第二个模型成为隐式 retry。若未来确需恢复，只能另起版本设计，
不能保留本方案中的旧入口。

### 3.3 权威 evaluator 契约

每个任务的 `evaluator_reference/` 只包含以下五个文件，均为必需文件：

- `reference_key_points.json`：计算过程关键节点及论文参考值/现象；
- `reference_conclusions.json`：最终科学结论及其支持的关键点；
- `scoring_rules.json`：针对 numeric、ordering、condition、semantic 的具体可执行
  初始规则（包括 target/expected、comparison、tolerance 或现象判定方式、submission
  binding）；
- `evidence_map.json`：参考结论到论文证据的映射；
- `critical_failures.json`：会使任务结论失效的关键失败条件。

Gate 检查文件存在、JSON 可读、条目非空、ID 唯一、引用闭合、规则类型受支持、规则有
明确 expected/target、comparison 和可定位 binding。Gate 不规定所有论文共用的 tolerance
数值、整数格式或某个固定科学方法；这些是 Agent 基于论文给出的初始规则，后续可人工
调整。旧 `ground_truth_common.json`、旧 `evaluation/reference.json` 不再作为必需输入，
也不再生成兼容 stub。

## 4. 代码修改清单

### 4.1 Stage06 文件

`src/stages/stage06_task_builder/stage.py`

- 保留 `_run_stage06_single_agent()`、一次性 `_run_phase()`、输入 snapshot、
  Stage06A/06B canonical Gate 和终态汇总；
- 删除 `_run_stage06_legacy()`、旧 multi-phase helper、旧 deterministic audit、旧
  Gate recovery context、Codex native resume 和 failure recovery workspace；
- `_run_phase()` 改为明确的单次调用：保留 checkpoint 作为可选的进程断点缓存时，只能
  复用已完成且 fingerprint 完全相同的产物，不复用失败对话、不读取 failure checkpoint；
  不再有 attempts/backoff/recovery 参数；
- 只读取 `external_phase_gate_report.json` 和 `agent_self_check_report.json`，删除
  `phase_gate_report.json` fallback；
- `mode_generation_strategy` 只接受 `two_agent_objective_centered`；删除 legacy aliases；
- 所有 transport identity 统一为 `paper_id`，评估内部 `key_point_id`/`conclusion_id`/
  `rule_id` 原样保留；
- 将 Stage06 scientific rejection 写成 terminal `decision`，不产生 retryable failure。

`src/stages/stage06_task_builder/validation.py` 与 `bootstrap_task_pair.py`

- 删除只服务旧 envelope/旧 ID/旧 acceptance profile alias 的 normalization 分支；
- 保留四种规则类型和跨文件引用、binding、输入闭合检查；
- 将 legacy 字段缺失从“兼容填充”改为明确 finding；不猜测科学含义；
- 更新测试 fixture 到 split canonical contract。

`src/stages/stage06_task_builder/prompts.py`

- 删除对旧阶段名、旧 recovery、旧 compatibility 文件的说明；
- 保留“完整合成任务 + 必须完成 Agent 自查”的单一任务描述；
- 明确规则必须具体可执行，但 tolerance 的科学选择由 Agent 根据论文确定，Gate 只
  检查完整性和可执行性。

### 4.2 Stage07 文件

`src/stages/stage07_task_judge/stage.py`

- 删除不可达 `_run_audit_agent()` 全部函数体、旧 Gate、`deterministic_judge_audit()`、
  `run_gold()` 和 objective-audit retry/resume/recovery；
- 只保留 `_run_audit_repair_agent()` 一次调用和科学审计结果归类；
- 删除 Stage07B 调用、二次组装和 `stage07b_*` 输出字段；
- Stage07A 修复后只运行一次代码 Gate 和一次 package assembly；失败分类为
  `rejected_scientific_unrepairable` 或 `technical_blocked`；
- audit 输入直接读取 split evaluator，不再调用 `legacy_reference_from_split()`；
- 汇总字段只保留 `paper_id`、科学决定、Gate/装配状态、findings、发布路径和 Agent
  运行记录。

`src/stages/stage07_task_judge/package.py`

- 删除 `legacy_reference_from_split`、`split_legacy_reference` import 和 stub；
- split evaluator 直接复制到 package 的 evaluation 目录；
- package validator 不要求旧 `evaluation/reference.json`；
- 若底层公共 schema 暂时仍有 `reference_schema` 字段，改成 split evaluator schema
  版本或固定为 metadata，不再验证旧 reference 内容；
- `task_id`/`task_family_id` 如无法立即从底层 schema 移除，统一写 `paper_id` 且增加
  测试保证三者永远相等，不接受 Agent 提供的其他值。

`src/stages/stage07_task_judge/validation.py`

- 删除 legacy hidden envelope 的 fallback 检查和 compatibility normalization；
- `minimal_evaluator_findings()` 成为 Stage06A 与 Stage07 共用的唯一 evaluator 完整性
  检查；
- split 文件缺失、空模板、交叉引用断裂、binding 无法映射、规则缺少比较方法属于
  blocking finding；tolerance 的具体科学数值不单独阻断；
- 将 warning 仅用于诊断，不生成 compatibility warning 伪失败。

`src/stages/evaluator_reference.py`

- 删除双向 legacy 投影函数及其专用辅助函数；
- 保留 split 文件常量、读取、最小完整性检查和必要的结构化 helper；
- 该模块不再生成隐藏 envelope 或 compatibility view。

`src/stages/stage07_contract_repair/`

- 从 Stage07 主流程和配置中移除；实现文件在确认无其他调用方后删除，或先保留为
  不可导入的历史迁移目录并在同一提交中清除测试/文档引用。优先直接删除，避免再次被
  误启用。

### 4.3 配置与批次脚本

`src/config.py`、`config.example.json`：

- Stage06/07 仅保留 `timeout_seconds`、`max_tool_calls`、`finalization_reserve`、
  `workers`、`checkpoint_cache_enabled`（若实现仍需要）及资源策略；
- 删除 late-stage 的 `max_attempts`、retry/backoff、resume、codex_native_resume、
  recovery、legacy strategy、objective_audit 和 Stage07B 配置；
- 配置校验只验证现行字段和 `two_agent_objective_centered`；
- 不改 Stage00–05 配置默认值。

`scripts/workflows/run_stage06_07_gpt_batch.py`：

- 将每篇 paper 的终态规范为 `completed/scientific_rejection`、
  `completed/published` 或 `failed/technical_blocked`；
- 旧批次状态只做读取诊断，不自动把科学拒绝重标为失败；新运行写入规范化状态文件；
- 不添加批次级 retry。

## 5. 测试与验收计划

### 5.1 先建立 canonical fixture

新增最小 fixture 覆盖：完整 numeric/ordering/condition/semantic 规则、缺文件、空
模板、缺 expected、缺 comparison、无效 binding、跨文件 ID 断裂、科学拒绝、技术装配
失败。fixture 只使用 `paper_id` 一个论文身份。

### 5.2 删除/迁移旧测试

删除或重写依赖以下旧行为的测试：`task_pair_id` 多重身份、legacy reference round-trip、
Stage07B、Agent retry/resume、`phase_gate_report.json` fallback、旧 Gate ID 优先级。
保留 Stage00–05 resume 测试，不把它们混入 Stage06/07 清理。

### 5.3 分层验证

1. 静态审查：`rg` 确认 Stage06/07 active code 不再出现旧入口、旧配置和兼容投影调用。
2. 单元测试：split evaluator、shared Gate、paper_id 唯一性、科学拒绝状态、技术阻断
   状态和 package assembly。
3. 定向回归：Stage0607 canonical tests 全部通过；旧契约测试必须被明确删除/迁移，不能
   通过兼容分支“伪修复”。
4. 同十篇论文 A/B 测试：先运行代码路径 dry-run，再提交模型任务；逐篇记录 Stage06A
   自查、Stage06B 转换、Stage07A 审计、Gate findings、最终发布/拒绝原因。
5. 质量验收重点：科学目标是否保持、输入是否闭合、关键点/结论是否具体、规则是否可
   执行、是否仍有 split compatibility warning、是否出现 Agent 通过但 Gate 阻断。

## 6. Git 实施顺序

1. 提交本方案和代码审查记录；不改实现。
2. 提交 evaluator canonical contract 与 shared Gate 清理。
3. 提交 Stage06 旧路径/重试/resume/ID 清理。
4. 提交 Stage07 旧审计路径、Stage07B 和 compatibility projection 清理。
5. 提交配置、批次状态和测试迁移。
6. 运行全量相关测试并提交测试报告。
7. 与本方案逐项对照；只有一致且回归通过后，才提交十篇论文的正式合成测试。

每个提交只涉及一个逻辑边界；不使用 destructive git 操作，不覆盖工作区中 Stage00–05
或 chemistry toolbox 的既有修改。

## 7. 明确不做的事情

- 不通过增加固定论文特例、固定 tolerance、固定数值或字符串黑名单来提高通过率；
- 不让 Stage07 在 Stage06 科学拒绝后生成新任务；
- 不把 Agent 自查报告变成编排器 retry 触发器；
- 不保留“为了旧 fixture 能过”而存在的兼容 wrapper；
- 不把 API 连通性问题扩大成 Stage06/07 业务逻辑改动。

## 8. 需要用户确认的决策

本方案默认删除 Stage07B 和所有 split→legacy evaluator 投影，并把底层仍要求的
`task_id`/`task_family_id`降为与 `paper_id` 相同的传输字段。如果你希望保留任一旧
公共文件或 Stage07B，需要在代码修改前明确指定其唯一用途和边界；否则按本方案执行。
