# Stage06/07 通用代码缺陷修复方案（2026-08-17，修订版）

## 目标与边界

本轮只修复妨碍 Agent 发挥作用的编排、数据归一化、交付、预算和可观测性问题，不针对六篇测试论文写特例，也不让代码替代 Agent 做科学裁决。

- Stage06 Agent 依据正文、SI、PDF 和解析证据选择完整、可复现且尽可能复杂的计算工作流，并构建两个任务模式。
- Stage07 Agent 负责科学审计、修复、必要时重设计或拒绝。
- 代码只验证运行/交付事实和 receipt 自洽性，不根据固定 schema、复杂度、Ground Truth 内容或路线泄漏规则改判科学结论。
- 两阶段只读取已安装软件清单，不读取 preset Action。软件版本完全不参与可用性判断；同一软件家族的不同 release/version 不产生软件缺口。

## 基线回归确认的问题

### P0：Stage07 事后门禁覆盖 Agent 科学结论

旧实现会在 Agent 完成审计和修复之后执行 `deterministic_stage07_audit()`，并把固定 validator 的 findings 直接合并为 blocking scientific findings。实际回归中，Agent 明确认为工作流科学完整、可复现并返回 `approved_with_repairs`，代码却在 Agent 不可见的事后阶段统一改成 `rejected_scientific_unrepairable`。

修复：Stage07 最终编排不再运行任务科学有效性 validator，不再由代码检查工作流完整性、复杂度、Ground Truth 质量、模式泄漏或 evidence 语义并据此改判。科学拒绝只能来自 Stage07 Agent。

### P0：批准 receipt 自相矛盾时没有回到 Agent

部分 Agent receipt 同时返回 approved 和高严重度关键数据缺失。这不是代码可以替 Agent 裁决的科学问题，但 receipt 本身不自洽。

修复：只做最小状态合同检查。若 approved receipt 同时声明非软件 blocking/critical/high 问题、`resource_status=infeasible`、空 final task ID，或 redesign 状态互相冲突，则标记 `invalid_phase_contract` 并触发同一 Stage07 Agent 的 recovery。代码不得把它改写成科学拒绝。

### P0：Stage06 `input_assets` 表达漂移导致元数据物化中断

Agent 可能把 `public_task_basis.input_assets` 输出为 list，也可能输出为以资产名为 key 的 map。旧代码假设一定为 list[dict]，对字符串调用 `.get()`，导致 `metadata_materialization_deferred:AttributeError`，并跳过部分 handoff 元数据。

修复：

1. 对 list/map 两类资产声明做语法归一化；
2. 若非标准声明无法恢复可信资产，无条件回退到已生成 reproduction/autonomous `task_spec.input_assets`；
3. 所有 scaffold/projection 迭代只处理 dict row；
4. 不凭描述生成结构、坐标或其他科学数据。

### P1：代码侧 public-surface guard 修改任务科学内容

旧 guard 会重命名两个模式的 XYZ、改写 comment 和正文/JSON 引用，并删除固定文件名。它既改变论文复现模式的路线表达，也把科学泄漏审核责任从 Agent 转移到代码。

修复：删除代码侧文件重命名、comment 改写、文本替换和路线文件删除。Stage07 Agent 自己审核并修复 autonomous public surface。代码只刷新已有 copy-provenance hash、两个 mode manifest 和 task-pair manifest，不修改任务科学内容。

### P1：原生 Responses 路径 token 统计为零

Codex 原生 Responses 输出在 `_agent_stdout.jsonl` 的 `turn.completed.usage` 中包含真实 token，但 bridge 没有 usage record，旧代码仍写入全零。

修复：增加通用 Codex stdout usage parser。当 bridge totals 为零时，从最后一个 `turn.completed` 回填 input、cached input、cache miss、output、reasoning output 和 total token；保留统计来源，避免与 provider-request count 混淆。

### P1：Stage07 工具调用预算偏紧

基线 Stage07 已达到 88、94、95/96 次调用，Agent 在最终验证阶段没有余量。

修复：Stage07 primary 从 96 调整为 120，recovery 从 128 调整为 160，finalization reserve 至少 16。更高预算是上限，不要求 Agent 用满；同时移除重复 prompt 和事后复杂门禁，降低无效调用。

### P1：软件版本与可用性边界需要统一

Prompt 和代码均必须遵循：只按 software family、canonical ID、display name 和 alias 与已安装清单匹配；完全忽略版本字符串。Gaussian 09/16、G09/G16 等均视为同一 Gaussian 软件家族。不存在 preset Action 不是软件缺失，软件暂缺也不导致科学拒绝。

## 具体代码修改

1. `stage06_task_builder/stage.py`
   - 增加资产声明语法归一化；
   - 修复 task-spec fallback；
   - scaffold/projection 防御非 dict row。
2. `stage07_task_judge/stage.py`
   - 最终步骤只对账安装软件、刷新 manifests/provenance；
   - 删除 post-Agent scientific gate 和 deterministic content guard；
   - 增加 approved receipt 最小一致性检查并通过 recovery 修复。
3. `stage07_task_judge/prompts.py`
   - 明确 Agent 自己负责 autonomous public-surface 审核和修复；
   - 删除 orchestrator 会自动修改任务内容的错误承诺和重复句；
   - 强调软件版本完全忽略。
4. `agents/harness.py`
   - 从 Codex stdout 回填原生 Responses usage。
5. `config.py`、`config.example.json`
   - Stage07 预算改为 120/160，finalization reserve 改为 16。
6. `tests/test_stage0607_agents.py`
   - 增加 map/list 资产恢复、manifest-only guard、Agent 决策不被 validator 覆盖、receipt 冲突触发 recovery、stdout usage 和版本无关软件匹配测试。

## 验收标准

1. Agent 的 approved/rejected 科学结论不再被代码 validator 改判。
2. approved receipt 自相矛盾时触发 Agent recovery，而不是代码生成科学拒绝。
3. map 形态 `input_assets` 不再产生 AttributeError，且不制造科学输入。
4. 发布后的机械步骤不重命名、删除或重写任务科学内容，只刷新 manifest/provenance。
5. Stage07 原生 Responses token 不再记录为零。
6. 两阶段 prompt 和软件对账都完全忽略版本，不使用 preset Action 判断。
7. 不添加论文、分子、软件或路线特例；核心代码复杂度较旧 final-gate 版本下降。
8. 定向测试、全项目测试、ruff 和 py_compile 通过后，以新 Git 提交重跑六篇，并在迭代日志记录每轮真实效果。
