# Stage06/07 第八轮 Token 与合同一致性修复方案（2026-08-20）

## 1. 第七轮回归结论

测试运行：

`runs/stage06-07-seventh-round-paper6904-deepseek-v4-pro-0813-codex-20260819`

Stage06A/06B 均完成，Stage07 返回 `approved_with_repairs`，最终 `mechanical_pre_publish_status=passed`、两个模式的 evaluator projection 均通过，两个任务已发布。Stage07 的科学审计表明确检查了参考态、自由 NH3、动作/验证和提交绑定，说明第七轮的核心科学审计 Prompt 已发挥作用。

## 2. 仍存在的问题及归因

### C1/P1：自主转换器的交付物指令与提交合同不一致

Stage06B Prompt 仍要求“research plan”和 task-specific numerical/structural results，但实际 `submission_contract.json` 只声明 `report/results.json` 与 `report/report.md`。这会让 Agent 额外创建无评分文件，或误以为合同缺字段，属于 Prompt/合同设计问题，不是模型科学能力问题。

方案：Prompt 以当前 `submission_contract.json` 为唯一交付物来源；只要求合同声明的文件。研究计划、过程轨迹和中间证据只在合同明确要求时写入报告，不创建未声明的固定文件。

### C2/P1：模式字段存在别名，但没有明确谁负责派生

发布包同时出现 `mode`、`scientific_mode`、`task_mode`、`method_disclosure`、`pathway_disclosure`。这是为了兼容 evaluator 的运输字段，但当前 Prompt 仍让 Agent 直接生成/修改这些字段，造成多套枚举和重复推理。属于代码合同与 Prompt 边界问题。

方案：保留 evaluator 需要的字段，明确 `mode` 是科学模式的唯一语义源；`task_mode`、`scientific_mode`、披露字段是编排器在运输阶段确定性派生的兼容字段。Stage06B/Stage07 Agent 不再自行设计别名，只验证科学内容和公开/隐藏边界。

### C3/P1：科学问题在 task.md、task_info、task_spec 中重复

`task.md` 是评估 Agent 唯一的任务指令；JSON 中的 `scientific_question`/`target_definition` 仅是加载和索引元数据，当前 Prompt 没有明确这一点，容易导致 Agent 重复编辑或产生漂移。该问题是 Prompt 边界问题；为了向后兼容，本轮不删除 evaluator 读取的元数据字段。

方案：在 Stage06B/Stage07 Prompt 明确 task.md 为唯一操作指令，JSON 字段只做同一问题的短摘要，不复制额外要求；代码继续将运输字段确定性归一化。

### P2：Stage07 重复读取大文件并使用不可用工具

第七轮 Stage07 约 57 次 workspace 命令，反复读取 workflow_review、task_spec、Ground Truth 和自主任务，累计约 4.2M prompt token；其中一次 `jq` 因环境未安装失败。重复读取属于 Prompt/运行协议问题，不是科学判断问题。

方案：增加只含路径、大小、顶层键和模式计数的 `inputs/audit_index.json`，要求 Agent 首次用一个 `/usr/bin/python3` 批处理读取 index 与必要字段，后续只读取尚未核查的局部文件；明确禁止 `jq`、禁止重复 cat 同一大文件、禁止为审计生成完整重复 trace。该 index 不包含答案、科学结论或新的规则。

### P3：固定“最多三个 Ground Truth”与实际中间/最终 Key Point 需求冲突

第七轮产物包含 10 个紧凑的中间/最终 key point，覆盖整条核心路线；这比强行压成三个条目更适合评估过程。现有 Prompt 的固定上限会诱导 Agent 删除关键中间结论，属于 Prompt 设计问题。

方案：改为“保持紧凑、按同一科学量聚合，禁止逐原子/逐坐标拆分；不设固定数量上限，覆盖核心过程所需的中间和最终结论”。不增加论文特例规则。

## 3. 代码与 Prompt 修改计划

1. 新增 Stage07 `audit_index.json` 生成函数，仅记录运输层文件索引和非科学计数信息。
2. 在 Stage07 Prompt 中把 index 设为首个读取入口，加入批量读取、无 `jq`、不重复读取约束。
3. 修改 Stage06B Prompt，使交付物严格从 `submission_contract.json` 派生，并说明 task.md/JSON 的职责边界。
4. 修改 Stage07 Prompt，明确模式语义源与兼容字段派生关系，并把 task.md 设为唯一评估指令。
5. 删除固定 Ground Truth 数量上限措辞，改成紧凑聚合原则。
6. 运行 `tests/test_stage0607_agents.py` 及相关静态检查；只提交 Stage06/07 相关文件，保留工作区其他既有修改。
7. 用 DeepSeek-v4-pro-0813 + Codex 对 paper 6904 重新回归；完成后检查完整轨迹、科学审计表、机械报告和发布树。

## 4. 验收标准

- Stage07 首次可从 `audit_index.json` 获得审计所需文件导航，Prompt 不再要求 `jq` 或重复 dump 大文件；
- Stage06B 不再要求合同未声明的固定文件；
- Agent 不再被要求自行决定模式别名，task.md 被明确为唯一任务指令；
- 不新增科学死规则，不由代码判断元素守恒、溶剂、势垒、路线或科学结论；
- 单元测试通过，且回归任务仍能由 Stage07 Agent 做科学审计并发布两个模式。

## 5. 迭代记录

本节在代码修改、回归运行和轨迹分析完成后追加。最多五轮；若后续只剩模型能力问题，则停止扩展代码。
