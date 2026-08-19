# Stage06/07 第七轮代码与 Prompt 修复方案（2026-08-19）

## 1. 本轮依据

本轮依据第六轮同一篇论文的 DeepSeek-v4-pro-0813 与 GPT-5.6-sol 测试结果制定。两次运行暴露的问题必须分成三类处理：

1. 运输层/文件合同代码问题：可以由代码确定性修复，不涉及科学裁决；
2. Agent 职责与 Prompt 问题：通过更明确的审计工作表和模式边界修复；
3. 模型科学能力问题：不能用针对论文的死规则替代，只能让 Agent 有更清晰的证据要求，并在测试报告中单独记录。

## 2. 发现的问题与本轮处理边界

### 2.1 代码问题

#### C1：Stage06B rubric 对象/列表结构不兼容

DeepSeek Converter 输出 `process_rubric.json` 为 `{schema_version, items}` 对象，而 Stage06 主路径把它当成列表传给 `_ensure_reproduction_route_rubric()`，遍历对象键后调用 `row.get()`，导致成功的 Stage06A/06B 产物以 `AttributeError` 失败，Stage07 未运行。

处理：在 Stage06 运输边界统一 rubric 形状；支持列表、`items`、`criteria` 三种已有传输形式，输出 evaluator 使用的列表。不得根据 rubric 内容作科学判断。

#### C2：canonical pair ID 与 hidden Ground Truth ID 不同步

编排器将 Agent 自拟 ID 规范成 `<paper_id>_task_pair`，但 `hidden_reference/ground_truth_common.json` 和 evaluator registry 中仍残留 Stage06A 的旧 ID。

处理：Stage07 发布前只对 hidden/reference 的运输身份字段做确定性同步，并在机械报告中检查 mode task_info、hidden Ground Truth、registry projection 的 pair ID 一致性。该检查只报告文件合同，不判定科学有效性。

#### C3：机械合同没有覆盖 hidden identity linkage

处理：增加通用的 hidden identity linkage finding；不得增加元素、溶剂、势垒等论文特定科学规则。

### 2.2 Prompt/职责问题

#### P1：Stage07 虽要求科学闭合，但没有强制证据化闭合表

GPT 将缺少自由 NH3 参考态、缺 TS-1a、TS 优化动作矛盾的任务错误标成 `closed`。

处理：Stage07 Prompt 增加一张最小科学闭合表要求：

- 每个差值量：左侧/右侧参考态、对应输入 asset、元素/物种是否闭合、公式和单位；
- 每个候选 TS/驻点：起始结构、计算动作、输出产物、频率/IRC 等验证条件；
- 每个 key point：所需输入、workflow step、提交字段、hidden profile 的一一映射；
- 无法从来源闭合时，必须 `repairable` 补齐来源资产，或 `unrepairable` 拒绝，不能仅凭一句总结写 `closed`。

这些是通用审计问题，不写论文、分子或关键词规则。

#### P2：复现模式答案泄漏边界仍不够醒目

Stage06A Prompt 已写“复现模式不公开 target values”，但 GPT 仍把 19.2/24.3 和答案性 `supported_primary_claims` 放进复现公共 metadata。

处理：在 Stage07 Prompt 中明确：复现模式可公开作者路线、软件和参数，但 `task_info/task_spec/workflow_scope` 不得包含数值答案、排序、优选路线、最终结论或容差；只能保留 claim ID/任务目标。需要修复时同时扫描 JSON、Markdown、文件名，而不是只改 `task.md`。

#### P3：全流程优先与子流程降级证据不足

处理：Stage06A Prompt 强调子流程必须给出成本、数据或软件阻断证据；仅仅“更容易包装”不是降级理由。Stage07 复核 scope 时要求确认该证据，但不由代码自动裁决。

#### P4：Autonomous 方法披露与 Ground Truth 口径可能矛盾

本轮不加入死规则。Prompt 仅要求 Stage07 明确记录任务属于 method-constrained 还是 method-discovery，并确认 public boundary、允许的方法自由度和 hidden acceptance 的数值口径一致；若不一致，由 Agent 修复任务定义或拒绝。

## 3. 代码修改计划

1. 修改 Stage06 rubric 运输归一化，覆盖 converter 产物在主路径和恢复路径的对象/列表差异。
2. 新增 Stage07 hidden identity 同步函数，在 canonical pair ID 确定后更新 pair-level hidden Ground Truth 的身份字段。
3. 在 `stage07_mechanical_pre_publish_check()` 增加 hidden identity linkage 的机械 finding，并补充单元测试。
4. 不新增任何化学、元素、溶剂、势垒或论文关键词的代码侧规则。
5. 更新 Stage06A/Stage07 Prompt，加入证据化科学闭合表和复现泄漏边界。
6. 运行 Stage06/07 相关单元测试与静态检查。
7. 使用 DeepSeek-v4-pro-0813 + Codex harness 对 paper 6904 重新提交单篇回归测试。

## 4. 验收标准

### 代码层

- DeepSeek Converter 的 `{items: [...]}` rubric 不再触发 `AttributeError`；
- Stage07 发布后的 public task、hidden GT、evaluator registry 使用同一 canonical pair ID；
- mechanical report 能报告 identity linkage 错误；
- 代码不执行科学输入闭合、元素守恒、势垒正确性或方法选择裁决。

### Prompt/Agent 层

- Stage07 输出的科学审计表中，参考态、输入资产、动作/验证、GT binding 均有具体证据；
- 复现公共 metadata 不再包含目标数值和答案性结论；
- 子流程选择包含可解释的完整路线降级依据；
- autonomous 的方法自由度与评分口径被明确说明。

### 回归报告

记录 Builder、Converter、Stage07 的工具调用/token、最终决策、发布树、审计表和剩余问题，并继续区分代码、Prompt、模型能力。

## 5. 迭代规则

最多进行五轮：每轮先检查上一轮运行轨迹，再只修复可归因于代码或 Prompt 的问题；若剩余问题仅属于模型科学能力，则停止代码扩张并在总结报告中说明。

## 6. 修改过程记录

本节在每次代码修改、测试提交和结果分析后追加，包含代码版本、测试路径、发现的问题、归因和下一轮动作。

### 2026-08-19：代码与 Prompt 第一轮修改

- 修改 `stage06_task_builder/stage.py`：`_ensure_reproduction_route_rubric()` 现在接受裸列表以及 `items`/`criteria` 包装对象，统一为列表后再注入 route-fidelity criterion。
- 修改 `stage07_task_judge/stage.py`：Stage07 通过机械门禁前同步 hidden Ground Truth 的 canonical `task_pair_id`；该函数只改运输身份，不改科学字段。
- 修改 `stage07_task_judge/validation.py`：机械门禁在显式传入 canonical pair ID 时检查 hidden Ground Truth 身份链接。
- 修改 Stage06A/Stage07 Prompt：增加参考态/资产/公式/动作/验证/提交字段闭合表要求，并明确 reproduction 模式禁止公开目标数值、排序、偏好路线和结论。
- 新增两个回归测试：`items` 包装 rubric 兼容、hidden pair identity mismatch 可被机械门禁报告。
- 验证：`127 passed`（`tests/test_stage0607_agents.py`）。

下一步：提交 DeepSeek-v4-pro-0813 的单篇 Codex 回归任务；完成后检查 Stage06B 是否进入 Stage07，以及科学闭合表和复现泄漏边界是否真正由 Agent 执行。
