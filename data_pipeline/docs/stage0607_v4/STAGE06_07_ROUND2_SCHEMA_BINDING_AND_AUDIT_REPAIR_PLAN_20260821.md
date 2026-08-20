# Stage06/07 第2轮共性问题修改方案

日期：2026-08-21  
基线：`1ac85c6`  
依据：第1轮 DeepSeek 10篇测试 `runs/stage06-07-v4-round1-deepseek10-concurrency10-20260821`

## 发现与归因

第1轮 10篇中，9篇进入 Stage07；8篇科学审计通过，2篇机械通过并发布，6篇被机械阻断，1篇 Stage07 对 Stage06 的不可构建结果做了 workflow redesign。6个机械阻断中，大部分不是科学问题，而是验证层对既有合同表达的误读：

1. `ground_truth_common.json` 使用 `mode_submission_bindings`，而 gate 只读取 `submission_bindings_by_mode`，导致模式专用 binding 被忽略，错误回退到共同 binding。——代码缺陷。
2. `observed_fields: ["document"]` 是语义结论绑定，且同时声明 `report/report.md` 或 `report/results.json` artifact；gate 将 `document` 当作 JSONPath，错误阻断。——代码缺陷。
3. JSON Schema 的嵌套对象有 `required` 但没有 `properties`，表示字段集合由 evaluator/语义审计解释；gate 将其当成确定缺失字段。——代码缺陷。应降为 open diagnostic，不改变科学判断。
4. Stage07 对一个 `scientific_not_constructible` 输入执行了科学重设计并声称批准，但没有生成统一的 `hidden_reference/ground_truth_common.json`、完整 submission contract 和可加载任务树。——Stage07 Prompt/Agent执行缺陷，不由代码猜测科学内容；应在 Prompt中强调“重设计后必须按发布合同补齐全部文件并自检”，并让机械阻断原因显式记录。

## 修改边界

- 只修通用 binding/schema 运输语义和 Stage07 合同自检指令；不增加论文、分子、软件或固定关键词规则。
- 不把 mechanical gate 变成科学审计；不检查物质平衡、溶剂或结构科学正确性。
- 不修改 Ground Truth 数值、结论、排序、容差或 Agent 科学决定。
- 本轮暂不实现 Stage07B：先验证 gate 误报修复后，是否仍有稳定的可机械修复阻断。

## 代码修改计划

1. `_binding_for_mode()` 同时支持历史/当前合同键 `submission_bindings_by_mode` 与 `mode_submission_bindings`，并记录冲突诊断。
2. 对 binding `observed_fields` 中的 `document`/文档语义字段：当 `artifact_paths` 至少包含合法文档产物时，作为结构有效的 semantic binding；无合法 artifact 时才报 finding。
3. `_schema_path_status()` 遇到对象没有 `properties`、但有 `required` 或 `additionalProperties` 未显式为 false 时返回 `open`，不误报字段缺失。
4. 增加回归单测覆盖上述三类合同。
5. Stage07 Prompt增加重设计后合同闭合清单：统一 hidden ground truth 文件、两模式 required files、binding 与 results schema、真实 evaluator dry-run；不得仅凭 Agent 自报 passed。
6. 运行 Stage06/07 单测和全量测试，提交独立 Git 版本。

## 验收

- 第1轮中由上述三类误报造成的机械阻断不再出现；
- 真实缺文件/缺合同（如 3e 案）仍保持 blocked 并给出明确 `blocking_reasons`；
- 科学审计字段与机械状态继续分离；
- 如修复后仍有稳定的“Agent已批准且合同缺陷可确定修复”样本，再评估 Stage07B。
