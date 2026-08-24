# Stage06/07 v9 实施计划与变更日志

关联方案：`STAGE06_07_V9_AGENT_SELF_CHECK_AND_EXTERNAL_GATE_PLAN_20260824.md`

## 代码修改计划

### Step 1：基线与工具骨架

- 记录当前 commit 和工作区状态，不覆盖用户已有的无关修改；
- 新增标准库依赖的 `phase_gate.py`；
- 定义统一的 JSON 输出和退出码；
- 为 Stage06A、Stage06B、Stage07A 提供最小通用检查 profile。

### Step 2：把工具放入 Agent 工作区

- 在各阶段 setup 中复制工具到只读 `inputs/tools/`；
- prompt 明确调用命令和“修复后再调用”的要求；
- 保证 Codex/Direct API/mock 三种 harness 都看到相同工具路径。

### Step 3：前置 canonicalization

- 在 Agent 自检和外部最终 Gate 前完成 mode/ID/兼容 alias normalization；
- 删除或禁用会把确定性 alias mismatch 反馈给 Agent 的重复检查；
- 保留原有规范化 provenance。

### Step 4：调整阶段运行器

- 阶段 Agent 结束后执行一次外部只读 Gate；
- 不再把 Gate finding 自动转换为多轮 Agent recovery；
- 仅保留 API/超时/无效 receipt 等执行失败重试；
- 保留 fail-open warning 和最终 publish blocking 语义。

### Step 5：调整 autonomous Prompt/投影

- 删除复制到 autonomous 的 reproduction route 文件；
- 缩短 task.md 为科学问题、边界、Key Points、实际交付物；
- 保留动态物理边界，隐藏默认方法和执行路线；
- 增加全树自检调用。

### Step 6：修共享合同检查与回归

- 修 `$ref`/数组 JSONPath resolver；
- 增加 deliverables 一致性检查；
- 增加自检工具、外部 Gate、autonomous 脱敏的通用测试；
- 运行既有 Stage06/07 测试集。

### Step 7：整体审查与 Git 记录

- 对照方案逐项检查代码调用顺序、prompt、文件权限和最终 Gate；
- 删除未使用 helper/import、重复 Gate 分支和临时调试代码；
- 只提交本轮目标文件，保留用户其他工作区修改。

### Step 8：20 篇 GPT 测试

- 固定 Stage05 来源和 20 篇清单；
- 使用 `gpt-5.6-sol` + Codex harness；
- 提交后记录 run 目录，不在本轮持续监督；
- 完成后分析 Agent 自检、外部 Gate、任务指令和发布结果。

## 变更日志

### v9-step-0：基线

- 基线 commit：`1ff5b14 docs(stage0607): record early gate implementation and replay`
- 工作区：存在 Stage00–05 与工具箱的用户既有修改；本轮只触碰 Stage06/07、共享合同、测试和 v9 文档。
- 基线测试：`PYTHONPATH=.:.. pytest -q tests/test_stage0607_v8_early_gate.py tests/test_stage0607_v8_task_packages.py tests/test_stage0607_v7_round04_contracts.py`，26 passed。

### v9-step-1：Agent 自检工具与 Prompt 接入

- 新增 `src/stages/phase_gate.py`。工具仅依赖标准库、只读、一次输出全部 finding，支持 `stage06a`、`stage06b`、`stage07a`，退出码 0/1/2 分别表示通过/合同 finding/工具错误。
- Stage06A、Stage06B、Stage07A 的 Agent workspace 均注入 `inputs/tools/phase_gate.py`；运行指令明确要求完成后调用、按需在同一 workspace 修复并再次调用，不要求固定修复轮数。
- Stage06A/06B 的旧 Gate finding 不再触发自动模型 recovery；编排器执行一次独立检查并将失败显式记录为 `phase_gate_status=failed`，继续把科学产物交给后续阶段/最终 Gate。
- Stage07A 默认启用 Agent 自检；旧两次 preflight recovery 仍可用 `stage07_agent_self_check=false` 显式兼容旧 fixture，但默认路径不再因 Gate finding 新建模型 attempt。
- 运行器在 Gate 前执行确定性的 mode/ID normalization；normalization 仍写入 provenance，外部 Gate 只读最终文件。
- 版本标记更新为 Stage06 `v19-agent-self-check-external-gate-20260824`、Stage07 `v18-agent-self-check-external-gate-20260824`。
- 回归：`PYTHONPATH=.:.. pytest -q tests/test_stage0607_v9_self_check.py tests/test_stage0607_v8_early_gate.py tests/test_stage0607_v8_task_packages.py tests/test_stage0607_v7_round04_contracts.py`，31 passed；`tests/test_stage0607_agents.py`，171 passed。

### v9-step-2：通用合同解析与交付闭合

- `researchchembench_contracts.task_package.schema_path_status` 增加本地 `$ref`（JSON Pointer）解析，并保留数组下标/嵌套对象支持；不抓取外部引用。
- Stage06A/Stage06B Gate 增加 `required_deliverables` 与 `submission_contract.required_files` 一致性检查。
- 新增通用 `$ref + array index` 回归 fixture 和自检工具多 finding/泄漏/外部 Gate 单次检查用例。
- 测试结果：上述 31 + Stage06 agent 171 全部通过。

### v9-step-3：整体对照与批量测试（已完成代码审查，测试已提交）

- 逐条核对方案：三阶段 workspace 均注入同一标准库自检工具；prompt 均要求在原 workspace
  自检、修复后再检；Agent Gate finding 不再自动创建模型 recovery；编排器在 canonical
  normalization 后执行一次独立只读最终 Gate；Stage07B 仍只处理 transport/合同字段。
- 核对结果：未发现本轮新增的论文特例规则、科学裁决硬编码、Gate finding 历史账本或重复
  recovery 分支；无关工作区修改未纳入本轮提交。`git diff --check` 通过。
- 回归结果：`tests/test_stage0607_v9_self_check.py` 与早期 Gate 回归共 13 passed；Task
  Package v1 回归通过；此前完整 Stage06/07 回归为 223 passed（其中 Stage06 Agent 171
  passed）。
- Stage05 来源共发现 582 篇通过候选。已固定 seed `20260824` 抽取 20 篇，使用
  `gpt-5.6-sol`、Codex harness、reasoning effort `high`、并发 20 提交测试。
- 测试输出目录：
  `runs/stage06-07-v9-gpt20-codex-20260824/`。提交时 `batch_status.json` 已写入
  `state=RUNNING`、20 篇清单、Stage06/Stage07 模型均为 `gpt-5.6-sol`、harness 为
  `codex`；后续结果分析待测试进程结束后进行。
