# Stage06/07 第十轮：Evaluator 元数据类型闭合修复

## 1. 第九轮测试结论

测试运行目录：

`runs/stage06-07-ninth-round-paper6904-deepseek-v4-pro-0813-codex-20260820`

模型与 harness：`deepseek-v4-pro-0813` + Codex。

Stage06A 选择并构建了第一步 N–H tautomerization 核心子流程；Stage06B 完成了中性资产表面转换；Stage07 识别并修复了复现任务模板、Ground Truth 绑定以及 autonomous 路线/方法泄漏。科学审计结果为 `approved_with_repairs`，工具箱和资源判断为可用/可行。

但发布门禁报告：

`evaluator_load_failed: TaskInfo.scientific_requirements.* Input should be a valid string`

Stage07 Agent 在两个 `task_info.json` 中输出了对象数组（例如 `{id, requirement}`），而 evaluator 的 `TaskInfo.scientific_requirements` 合同是 `list[str]`。因此科学决策已通过，但机械发布被阻断；这是通用输出协议/代码问题，不是论文科学问题，也不是模型不会做科学审计。

## 2. 问题归因

| 层级 | 问题 | 归因 |
|---|---|---|
| 代码/协议 | Agent 可以写结构化 requirement records，而 evaluator 只接受字符串，Stage06/07 没有在模式合同归一化时投影类型 | 代码缺陷 |
| Prompt | Stage07 没有明确提醒 `scientific_requirements` 是 evaluator 的字符串元数据字段 | Prompt 约束不完整 |
| 模型能力 | 本轮模型选择对象记录表达需求本身合理；不构成科学能力缺陷 | 不归因于模型 |

## 3. 修改方案与边界

1. 在通用 `canonicalize_mode_task_contract()` 中增加 `normalize_scientific_requirements()`：字符串原样保留；对象优先取 `requirement`、其次 `description`/`text`；空项丢弃。该操作只做 evaluator 传输类型投影，不判断科学内容、不改写 rubric 或 Ground Truth。
2. 对 `task_info.json` 在机械模式归一化时应用该投影。`task_spec.json` 保留 Agent 的科学元数据结构，不把 evaluator schema 扩展成第二套科学协议。
3. 在 Stage07 Prompt 中明确要求最终 `task_info.json.scientific_requirements` 使用纯字符串列表；详细 ID 和 rubric 结构仍放在 rubric 中。
4. 增加回归单测，覆盖结构化记录、字符串记录和混合记录，并验证归一化后 evaluator 类型可加载。
5. 不新增论文关键词规则、不把科学闭合交给代码、不扩大编排器裁决权限。

## 4. 已完成的代码修改

- `src/stages/stage06_task_builder/validation.py`
  - 新增通用 `normalize_scientific_requirements()`。
  - 在模式合同归一化中将 `task_info.json` 的 requirement records 投影为字符串列表。
- `src/stages/stage07_task_judge/prompts.py`
  - 增加最终元数据类型提示。
- `tests/test_stage0607_agents.py`
  - 增加结构化 requirement records 的回归测试。

本地验证：`128 passed`。

## 5. 第十轮回归测试计划

使用 `deepseek-v4-pro-0813` + Codex，在同一篇 `paper_6904a9c8c09855cc` 上重新提交 Stage06/07。重点检查：

- Stage07 仍能发现并修复第九轮的科学/披露问题；
- mechanical pre-publish gate 是否通过；
- 两个 `task_info.json` 的 `scientific_requirements` 是否为字符串数组；
- evaluator dry-run、发布目录和 manifest 是否成功；
- 不因本修复引入新的科学裁决或答案泄漏。

若第十轮仅剩模型偶发的科学判断问题，则停止代码扩张，转为 Prompt/模型能力记录；若仍有新的通用代码合同问题，在五轮上限内继续下一轮。

## 6. 第十轮测试结果

测试路径：

`runs/stage06-07-tenth-round-paper6904-deepseek-v4-pro-0813-codex-20260820`

模型与执行方式：`deepseek-v4-pro-0813` + Codex harness。

结果：

- Stage06A：`provisional_constructed`，保留了第一步 N–H activation 的核心子流程。
- Stage06B：`converted`，删除路线/证据文件并将五个输入重命名为 `candidate_1…candidate_5`。
- Stage07：`approved_with_repairs`，保留原 workflow，并修复 autonomous 方法披露、Ground Truth JSONPath 绑定和证据 ID。
- `scientific_audit_passed=1`。
- `mechanical_contract_passed=1`，`schema_load_diagnostic=passed`。
- `publish_ready=1`，复现与 autonomous 两个 bundle 均发布成功；evaluator registry 两个投影均可由 `TaskInfo`/`GroundTruth` 加载。
- 两个已发布 `task_info.json` 的 `scientific_requirements` 均为字符串数组，验证了本轮代码修复。

主要轨迹统计（来自各 Agent 的 Codex usage）：

- Stage06A：约 3.85M 输入 token，约 50.9k 输出 token。
- Stage06B：约 0.68M 输入 token，约 23.3k 输出 token。
- Stage07：约 4.51M 输入 token，约 40.5k 输出 token。
- 合计约 9.04M 输入 token；Stage07 使用 54 个主要 Agent 项目，未发生重试。

Stage07 本轮实际发挥的作用：

1. 保留了 Stage06 选定的科学子流程，没有被编排器替换。
2. 发现并修复了 autonomous 中的作者方法关键词、隐藏评估元数据和不应公开的路线实现信息，同时保留 THF、温度/压力、闭壳层状态和 0.70 熵缩放等问题定义所需边界。
3. 修复了三个数值 acceptance profile 的提交字段绑定和不完整证据 ID。
4. 机械门禁只负责归一化 `scientific_requirements` 类型、schema 加载和发布树检查；科学审计结论仍来自 Stage07 Agent。

## 7. 第十轮结论与剩余观察

第九轮的阻断性代码问题已解决，且没有引入新的代码合同错误。发布目录只包含任务文件和输入资产，不含 `conversion_report.json`、路线文件或 hidden reference。

autonomous `task.md` 仍显式写出 G70% 公式和“intramolecular / ammonia-assisted”两个待比较假设。这是本任务目标和公开物理边界的一部分，Stage07 将其判定为不等同于作者路线泄漏；它没有公开泛函、基组、软件、SCRF 关键词、路线顺序、目标数值或 hidden key IDs。若后续希望进一步扩大自主性，应作为独立 Prompt 设计实验决定是否将熵缩放从公开边界改为 Agent 自主选择，不能由编排器关键词过滤。

本轮未发现需要继续修改的通用代码问题；按“最多五轮”约束，本轮可作为当前迭代的通过轮。后续若在不同论文上出现同类类型错配，应复用本轮通用投影，而不是增加论文特例规则。
