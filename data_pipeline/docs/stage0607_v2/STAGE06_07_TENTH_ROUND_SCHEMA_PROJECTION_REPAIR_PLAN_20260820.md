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

## 6. 结果记录（待第十轮任务完成后补充）

- 测试路径：待补充
- Stage06/07 决策：待补充
- 机械发布状态：待补充
- 轨迹与 token：待补充
- 新问题与后续方案：待补充
