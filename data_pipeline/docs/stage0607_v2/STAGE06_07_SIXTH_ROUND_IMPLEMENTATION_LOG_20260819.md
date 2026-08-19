# Stage06/07 第六轮实施日志（2026-08-19）

## 基线

- 方案：[STAGE06_07_SIXTH_ROUND_MINIMAL_BOUNDARY_AND_MODE_ALIGNMENT_PLAN_20260819.md](./STAGE06_07_SIXTH_ROUND_MINIMAL_BOUNDARY_AND_MODE_ALIGNMENT_PLAN_20260819.md)
- 起始 commit：`726bb67 fix(stage06-07): close next-round contracts and autonomous boundaries`
- 本轮明确变更：任务指令只保留在 `task.md`，不再保留 `task_info.task` 兼容字段。
- 工作区中有大量与 Stage06/07 无关的既有修改，本轮不覆盖、不回滚。

## 计划

1. 更新 TaskInfo/schema、Stage06 bootstrap/validator、Stage07 读取路径，移除 `task_info.task`。
2. 统一新任务 pair ID、mode 投影和 hidden common 来源。
3. 加入 Stage06A workflow completeness / 私有 asset map 合同，保持 Stage06B 答案盲。
4. 修复 Stage07 mechanical blocked 的可见状态，清理 rubric 覆写和重复/死逻辑。
5. 简化 complexity profile 与 Prompt，运行测试并检查整体逻辑。
6. 使用 DeepSeek 与 GPT 对同一论文提交测试任务；提交后不主动监督。

## 修改记录

| 时间 | 版本/文件 | 修改内容 | 验证结果 | 遗留问题 |
|---|---|---|---|---|
| 2026-08-19 | 基线 | 尚未修改代码 | 待运行 | 待记录 |
| 2026-08-19 | 第一阶段 | `task.md` 成为唯一任务指令来源；Evaluator 运行时从 `task.md` 读取文本；生产代码不再写入 `task_info.task`。 | `compileall` 通过 | 旧 fixture 中仍有多余 `task` 字段，Pydantic 会忽略；依赖缺失导致 pytest 尚未运行 |
| 2026-08-19 | 第二阶段 | hidden reference 收敛到 `hidden_reference/ground_truth_common.json`；Stage06A 增加 workflow completeness/map 私有交接；pair ID 由 paper ID 确定性派生；complexity 收敛为 `complexity_profile`；Stage07 mechanical blocked 显式写入 record/summary。 | `compileall` 通过 | 待完成完整可用 Python 环境验证 |
| 2026-08-19 | 第三阶段 | 清理 receipt/record 中 `complexity_level` 双写；统一 `schema_load_diagnostic` 命名；Evaluator binding 的科学完整性继续由 Stage07 Agent 负责，机械层只做 schema/path 诊断，不以 artifact 是否出现在任务静态文件列表中裁决。 | `compileall` 通过；导入 smoke test 受 `json_repair` 依赖缺失阻断 | 需要在运行环境恢复依赖后执行 pytest；不影响代码语法检查 |
| 2026-08-19 | 第四阶段 | 修复 Prompt JSON 示例的 f-string 转义、确定性 pair ID 在 Stage06 全路径生效、route rubric ID 冲突、隐藏 common 投影加载，以及 Stage07 schema/path 诊断边界。 | `tests/test_stage0607_agents.py`: **125 passed**；`compileall`: 通过；最小 Stage07 mechanical smoke: passed/passed | 其他全量 pipeline 测试受环境依赖（如 `dotenv`）影响，未纳入本轮 Stage06/07 验收 |

## 测试记录

尚未开始。

## 本轮回看结论

- 生产路径不再生成 `task_info.task`，发布任务只要求 `task.md` 与元数据 JSON。
- 新任务的 `task_pair_id` 不接受 Agent 自拟值；Agent 提议值仅作为非权威审计元数据保留。
- `mode` 是内部模式来源，`scientific_mode`、`task_mode`、披露字段由编排器派生以满足当前 Evaluator 枚举兼容。
- Stage07 的机械检查不承担科学 workflow 完整性或 evaluator binding 语义裁决；它只报告可解析性、安全路径和 schema load 结果，binding 缺陷作为诊断交给 Stage07 Agent/审计报告。
- 未发现 Stage06B 读取正文/SI、hidden reference 或私有 asset map 的路径；答案盲边界保持不变。
