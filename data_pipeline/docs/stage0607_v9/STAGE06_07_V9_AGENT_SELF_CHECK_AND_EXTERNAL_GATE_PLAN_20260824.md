# Stage06/07 v9：Agent 自检工具 + 外部最终 Gate 修改方案

日期：2026-08-24
状态：已实施（代码与回归测试完成，批量测试待提交）
适用范围：Stage06A、Stage06B、Stage07A、Stage07B 及其任务合同/发布检查代码

## 1. 目标

本轮的唯一工程目标是让阶段 Agent 在同一个工作区内完成“生成 → 自检 → 修复 → 再自检”，并由编排器在 Agent 结束后用独立的只读 Gate 做最终兜底。

需要同时满足：

1. Gate 的完整检查结果一次性呈现给 Agent，Agent 可以在同一上下文中一次修复所有可修复问题。
2. 编排器不再依靠固定的“失败后新建 workspace、恢复一次、再失败放行”作为主要修复机制。
3. 最终发布判断仍以外部确定性 Gate 为准，不能信任 Agent 自报的 `passed`。
4. 代码和 prompt 保持通用，不添加论文名称、分子名称、特定数字或特例关键词规则。
5. autonomous 任务只公开科学问题、必要输入和物理边界，默认不公开论文执行路线或机器执行协议。

本轮不要求每篇论文都构建成功；科学不可闭合仍由 Stage06/07 Agent 判断。代码只处理确定性的文件、JSON、路径、模式和公开隔离合同。

## 2. 非目标与边界

本轮不做以下事情：

- 不建立大型 `CanonicalTask` 对象或重写三种任务类型的整体目录架构；
- 不把科学代表性、中心性、答案数值、容差或机制正确性硬编码到 gate；
- 不为某篇测试论文添加规则；
- 不保存复杂的 finding 历史、修复分类账或长期反馈数据库；
- 不取消最终发布 Gate；
- 不因为工具箱缺少软件而把科学任务改成拒绝。

Agent 的总 tool-call 和 timeout 上限仍然保留，这是防止无限执行的安全上限，不是 Gate 修复轮数限制。

## 3. 目标流程

```text
阶段 Agent 生成文件
        ↓
Agent 调用 inputs/tools/phase_gate.py --phase <阶段> --root <输出根>
        ↓
一次性返回全部 finding
        ↓
Agent 在同一工作区修改并再次调用工具（可按需要重复）
        ↓
Agent 提交 receipt
        ↓
编排器先做确定性 canonicalization
        ↓
编排器调用同一类外部只读 Gate
        ├─ 通过：进入下一阶段/组装发布包
        └─ 失败：保留 warning 或按最终发布规则阻断
```

“Agent 自检”与“外部最终 Gate”必须使用同一套通用检查语义，但运行位置不同：

- 自检工具运行在 Agent 工作区，读取 `outputs/`，不修改文件；
- 外部 Gate 运行在编排器控制的副本/最终包上，读取最终文件，不接受 Agent 的自报结果；
- 自检工具输出不进入发布任务目录，只作为当前会话的临时终端输出。

## 4. 自检工具设计

### 4.1 入口与返回格式

新增一个通用命令：

```bash
python inputs/tools/phase_gate.py --phase stage06a --root outputs
python inputs/tools/phase_gate.py --phase stage06b --root outputs
python inputs/tools/phase_gate.py --phase stage07a --root outputs
```

约定：

- 退出码 `0`：检查通过；
- 退出码 `1`：发现合同/结构/公开隔离问题；
- 退出码 `2`：参数或工具自身错误；
- stdout 输出一个简短 JSON 对象，包含 `status`、`phase`、`findings`；
- `findings` 一次包含当前检查能发现的全部问题；
- finding 必须包含文件相对路径、字段/结构位置和明确修复建议，但不写入任务包。

工具只依赖 Python 标准库，避免 Agent 工作区必须访问项目源代码。代码侧的最终 Gate 继续使用已有共享 validator；自检工具与最终 Gate 的检查项通过少量通用 helper 保持一致，不能各自发展出论文特例规则。

### 4.2 Stage06A 检查范围

只检查 Stage06A 已经负责交付的 reproduction/handoff：

- `construction_receipt.json`、`workflow_review.json` 的存在和 JSON 结构；
- reproduction 必需文件、相对输入路径和实际输入文件；
- `hidden_reference/ground_truth_common.json` 的 ready 状态、item/profile 引用闭合和至少一个 `claim_role=final`；
- `workflow_completeness_check.json`、`public_to_private_asset_map.json`、`toolbox_requirements.json` 的存在和可读性；
- `task_info.required_deliverables` 与 `submission_contract.required_files` 的一致性；
- rubric 非空且没有因包装归一化而丢失内容。

不检查 autonomous 目录、不判断论文科学代表性、不判断答案数值。

### 4.3 Stage06B 检查范围

只检查 autonomous public surface：

- 五个核心文件、输入目录和声明路径；
- autonomous mode metadata 的确定性 canonical 形式；
- 不出现 reproduction route 文件、conversion packet、hidden reference 或内部 handoff；
- `task.md` 非空且包含科学问题、必要边界和实际评估交付物；
- `task_info.required_deliverables` 与 `submission_contract.required_files` 一致；
- 动态公开泄漏检查：扫描 Markdown、JSON、文件名、XYZ 注释和 manifest，过滤本任务动态提取的答案值、容差、排序/趋势、内部 ID 和路线实现信息。

代码只发现通用泄漏类别，不使用固定论文关键词；科学上必须公开的物理边界由 Agent 的转换 packet 标记并保留。

### 4.4 Stage07A 检查范围

只检查 Agent 已批准任务的发布合同：

- 两个 mode 的必需文件和公开输入；
- hidden reference 的 profile、mode scope 和 binding 合同；
- 不允许同一 profile 同时保留 shared binding 和 mode matrix，除非它们在代码中已被确定性投影为单一来源；
- binding 指向的字段在对应 schema 中可解析；
- required deliverables、submission contract 和 `task.md` 的交付声明一致；
- public surface 的动态答案/路线泄漏检查。

该工具不重新做 Stage07 科学审计，不修改 hidden answer、容差、claim role、workflow scope 或输入结构。

## 5. Agent Prompt 修改

### 5.1 共同规则

在 Stage06A、Stage06B、Stage07A prompt 中加入同一段短指令：

1. 完成文件后必须调用对应 `phase_gate.py`；
2. 若返回 findings，必须在当前 workspace 一次修复所有可修复项，再调用一次或多次直到通过或确认工具自身问题；
3. 不得通过删除科学内容、答案、输入或必需交付物来“让 Gate 通过”；
4. 最终 receipt 必须反映当前文件，而不是早期草稿。

不要求 Agent 维护额外的 gate 日志，也不要求把工具输出复制进公共任务。

### 5.2 autonomous 指令收缩

Stage06B 的 `task.md` 生成规则改为最小充分内容：

保留：

- 一个中心科学问题；
- 匿名输入资产；
- 溶剂/介质、温度、压力、电荷、多重度、自旋、波长、周期性、固定几何等必要物理边界；
- 要回答的过程 Key Points 和最终结论（疑问式、答案中性）；
- 实际需要提交的报告、结果和计算证据。

默认移除：

- 论文软件名称、泛函、基组、力场和 route keyword；
- 作者的步骤顺序、精确扫描路线和验证路线；
- TS、产物、最低态、中间体、优选通道等答案性路线标签；
- 目标值、容差、排序、趋势、机制结论、`gt_*`/内部 profile ID；
- 完整 JSON 示例、固定 research plan、固定 process trace 文件要求。

只有当方法本身是科学比较变量或评分明确锚定该方法时，才保留最小的 method constraint，并将任务语义标为 `fixed_input_method_constrained_workflow`；否则使用 `fixed_input_method_discovery`。不能一边隐藏方法一边在 task 文本中规定完整执行协议。

`paper_route.md`、`workflow_spec.json`、`route_evidence_map.json` 只属于论文复现模式；autonomous 模式不复制它们。

## 6. 编排器与最终 Gate 修改

### 6.1 normalization 时序

把确定性的 mode、task ID、兼容 alias 和 schema wrapper normalization 放在外部 Gate 之前。Agent 自检工具看到的文件也应尽量是 canonical 形式，不能把本应由代码完成的 alias mismatch 反馈给 Agent。

### 6.2 删除主要恢复循环

现有 `_run_phase`/Stage07A 的“Gate finding → 新 attempt → native resume → 第二次 fail-open”不再作为主要修复路径。阶段调用改为：

- Agent 自己负责调用 Gate 并修复；
- 编排器在 Agent 结束后执行一次外部只读检查；
- 外部失败时保留现有 warning/technical-blocked 规则；
- 不自动新建多轮恢复 workspace。

保留最小的执行失败重试（API、超时、结构化 receipt 无效），但不把外部 Gate finding 再转成模型恢复循环。

### 6.3 外部 Gate 必须只读

`stage07_mechanical_pre_publish_check()` 不再在检查过程中写回任务合同。所有 normalization 先在独立步骤完成，并将既有 `orchestrator_normalizations.json` 作为 provenance。最终 Gate 只读最终副本并返回 findings。

### 6.4 Stage07B 边界

Stage07B 继续保留为一次窄合同修复，但不是 Agent 自检的替代品：

- 只处理可以确定性证明为 transport 的字段；
- 不处理科学答案、输入、claim role、路线中心性或方法选择；
- 修复后由外部 Gate 再检查一次；
- 不增加循环或复杂 finding 历史。

## 7. 回归测试要求

新增/更新通用 fixture，至少覆盖：

1. Agent 在同一 workspace 调用自检工具并修复后通过；
2. 自检工具一次返回多个 finding；
3. mode normalization 在 Gate 前完成，合法输出不再报告 alias mismatch；
4. `required_deliverables` 与 `required_files` 不一致时能被 Stage06A/Stage07A 发现；
5. autonomous 中 reproduction route 文件和执行协议被发现；
6. 物理边界（溶剂、温度、电荷/自旋、波长）不会被泄漏扫描误删；
7. `$ref` + 数组下标 resolver 回归；
8. 外部最终 Gate 对 Agent 自报 `passed` 不信任；
9. Stage07B 仍不能修改科学文件。

测试不得绑定论文 ID、分子名称或特定数字。

## 8. 验收标准

代码完成后必须满足：

- 每个阶段 prompt 都明确要求调用对应自检工具；
- 工具实际存在于 Agent 工作区并可执行；
- Agent 自检通过后，外部 Gate 对同一输出再次通过；
- 外部 Gate 失败不会被 Agent receipt 静默覆盖；
- autonomous task 不含 reproduction route 文件或完整执行协议，但保留必要物理边界；
- 现有 Stage07B 和双模式发布合同回归测试继续通过；
- 代码中没有新增论文特例规则、无用的 finding 历史或重复恢复分支。

## 9. 测试计划

单元/回归测试通过后，使用 `gpt-5.6-sol`、Codex harness、当前配置，从 Stage05 通过集合中固定抽取 20 篇，提交 Stage06/07 合成测试。测试只验证角色、合同、脱敏和外部 Gate 闭环，不要求 20 篇全部科学批准或发布。

测试结束后逐篇统计：

- Agent 自检工具调用和最终状态；
- 外部 Gate 状态；
- 科学构建/拒绝；
- 合同阻断；
- autonomous 指令是否残留路线/执行协议；
- 代码错误、prompt 执行问题和论文输入/模型能力问题。
