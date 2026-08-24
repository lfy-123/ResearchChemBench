# Stage06/07 v9B 交接说明：当前进展、目标、边界与测试方法

给下一位 agent 的工作交接。本文只描述当前事实和可复现方法，不把单篇论文的科学失败硬编码成规则。

## 1. 当前代码和测试基线

- 工作目录：`/mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline`
- 本轮功能 commit：`15262cb feat(stage06): make autonomous converter gate external-only`
- 该 commit 之前的 Gate 设计 commit：`af6cad9 feat(stage0607): add agent self-check and external final gate`
- 工作区还有用户在 Stage00–05、chemistry toolbox 等目录中的既有修改；不要 reset、checkout 或提交这些无关修改。
- 定向回归：

  ```text
  PYTHONPATH=.:.. pytest -q \
    tests/test_stage0607_v9_self_check.py \
    tests/test_stage0607_v8_early_gate.py \
    tests/test_stage0607_v8_task_packages.py \
    tests/test_stage0607_v5_contracts.py
  39 passed
  ```

- 之前完整 Stage06/07 回归为 226 passed（当前修改没有已知回归）。
- 最近的 10 篇 GPT 测试已完成：
  [runs/stage06-07-v9b-gpt10-codex-20260824](/mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline/runs/stage06-07-v9b-gpt10-codex-20260824)

## 2. 已完成的功能目标

当前流程明确采用：

```text
Stage06A：Agent 生成 → Agent 在同一 workspace 自查 → 编排器外部只读 Gate
Stage06B：Agent 生成 autonomous 转换 → 编排器外部只读 Gate（不向 Agent 注入自查）
Stage07A：科学审计/合同审计 → Stage07B 仅做窄的 transport/合同修复 → 最终发布 Gate
```

`_run_phase()` 的 `phase_gate_mode` 有四种值：

- `agent_and_external`：Stage06A 使用；Agent 可运行工具并在同一上下文修复，编排器再独立检查。
- `external_only`：Stage06B 使用；不注入 Gate 命令，不因 finding 触发 resume/recovery，只做一次外部检查。
- `bounded_recovery`：仅为旧 fixture/旧调用兼容保留。
- `none`：关闭 Gate。

本批次证明 Stage06B external-only 已按预期工作：6 个构建任务中没有任何 `phase_gate.py --phase stage06b` Agent 调用，外部 Gate 仍运行一次并捕获了 `paper_8b...` 的 autonomous rubric/schema 错误。

## 3. 为什么 Stage06A 自查和最终检查不一样

这是当前最重要的实现问题。它不是“Agent 没按要求做”，而是代码中存在两套独立检查器：

### 3.1 Agent 自查使用的检查器

编排器会把独立脚本复制到 Agent workspace：

```text
inputs/tools/phase_gate.py
```

这个脚本是标准库自包含工具，主要检查：

- 必需文件是否存在、JSON 是否可读；
- `task_info/task_spec` 的模式和 ID 形状；
- `data/inputs` 中被 `task_spec` 引用的文件；
- required deliverables 与 submission contract 的路径一致性；
- receipt、handoff、hidden reference 的基本结构；
- autonomous 公开面是否出现内部协议/内部评分 ID。

它的设计目标是让 Agent 尽早修复运输层问题，且不需要导入 pipeline 私有模块。

### 3.2 编排器外部 Gate 使用的检查器

Stage06A 结束后，`src/stages/stage06_task_builder/stage.py` 的：

```python
_stage06a_phase_gate_findings(response, workspace)
```

会进一步调用 `validation.py` 中的 `_acceptance_profile_findings()`，检查：

- semantic profile 是否有 `required_propositions`；
- numeric profile 是否有 target、unit/tolerance；
- submission binding 是否存在；
- projection/comparison 是否完整；
- hidden truth 与 profile 的 evaluator 合同是否闭合。

这些检查在 Agent 自查脚本中没有完整实现。因此同一份产物可能出现：

```text
Agent 自查：passed
外部 Stage06A Gate：failed
semantic_acceptance_contract_missing:ap-1
numeric_acceptance_target_or_unit_missing:ap-2
acceptance_submission_projection_missing:ap-2
```

此外还有两个时点差异：

1. Agent 自查发生在 Agent 结束前，看到的是尚未完成编排器 canonical normalization 的文件；外部 Gate 在 normalization 后运行。
2. Agent 自查和外部 Gate 目前都写 `phase_gate_report.json`，后写入的外部报告覆盖了前一个报告。若不读取 `_agent_stdout.jsonl`，无法从报告文件单独判断 Agent 自查结果。

所以当前的“自查通过”只表示“通过 standalone 工具承诺的检查”，不表示“通过外部最终合同”。代码注释/文档曾把两者描述成同一套语义，这是需要修正的地方。

## 4. 最近 10 篇测试的客观结果

批次配置：`gpt-5.6-sol`、Codex、`high`、并发 10；10/10 worker 完成。

| 指标 | 数量 |
|---|---:|
| Stage06A constructed | 6/10 |
| Stage06A scientifically not constructible | 4/10 |
| constructed 中 Agent 自查最终通过 | 5/6 |
| constructed 中外部 Stage06A Gate 通过 | 1/6 |
| Stage06B Agent Gate 调用 | 0 |
| Stage06B 外部 Gate 通过 | 5/6 |
| constructed 中 Stage07 科学批准 | 6/6 |
| Stage07B repaired | 1/6 |
| 最终 publish-ready | 1/6 |

四篇 `provisional_not_constructible` 没有进入 Stage06B；这属于 Stage06A/Stage07 对论文输入闭合和可构建性的科学判断，不应统计为 Gate 代码误阻断。

逐篇详细分析在：

[STAGE06_07_V9B_GPT10_GATE_ANALYSIS_20260824.md](/mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline/docs/stage0607_v9/STAGE06_07_V9B_GPT10_GATE_ANALYSIS_20260824.md)

核心观察：自查对 receipt/handoff/坐标路径等早期问题确实有帮助，但目前不能证明它提高最终发布率；没有同样本、同模型、关闭自查的对照实验。

## 5. 目前问题的责任边界

### 5.1 代码问题（应优先修）

1. standalone self-check 与外部 Stage06A Gate 的通用合同检查不一致。
2. 两类报告写入同一个 `phase_gate_report.json`，审计轨迹不可直接区分。
3. 外部 Gate 运行在 canonicalization 之后，而 Agent 工具运行在之前；这本身可以是合理的两阶段设计，但必须显式记录前后快照和 normalization finding。

### 5.2 Prompt/Agent 输出问题

- semantic acceptance profile 为空命题；numeric profile 缺 target/unit/tolerance；binding 缺 projection/comparison；
- Stage06A 漏生成 receipt、handoff、final claim 或源坐标；
- Stage06B 生成非数组 `process_rubric` 或缺 results schema；
- Stage07A 同时输出 shared binding 和 mode matrix，或生成没有 comparison/projection 的 matrix。

这些不是代码替模型推导科学答案的问题。Prompt 应要求 Agent 使用工具检查并修复；代码只做通用结构检查。

### 5.3 论文/模型能力问题

四篇论文被科学判定为不可构建，原因是源材料无法闭合完整路线或核心子流程；这不是应该通过放宽 Gate 解决的代码问题。不能要求每篇论文都成功发布。

## 6. 交给下一位 agent 的优化总目标

在不引入论文特例规则、不把 Gate 变成科学裁判、不恢复 Stage06B Agent 自查循环的前提下，实现以下目标：

1. **同一合同语义**：Stage06A Agent 自查和外部 Gate 对同一份“通用 transport/evaluator 合同”给出一致结果；如果两者故意分层，必须在 schema、报告和文档中明确分层，不能让用户看到矛盾的 passed/failed。
2. **可追踪**：单独保存 Agent 自查报告和外部 Gate 报告，记录 authority、phase、attempt、输入快照 hash、normalization 记录和 findings。
3. **职责稳定**：
   - Stage06A 负责科学选题、完整 reproduction handoff 和基础 evaluator 草案；
   - Stage06B 负责 autonomous 公共表面转换，保持 external-only；
   - Stage07A 负责科学审计和 evaluator 语义决定；
   - Stage07B 只修可证明的合同/transport 问题，不能猜答案或补源坐标。
4. **失败可解释**：Gate finding 仍可 fail-open 传递给后续科学审计，但发布时必须有明确的 blocking reason；不能静默丢失。
5. **保持通用性**：只检查文件、schema、路径、安全、模式适用性和 binding 形状；不增加 paper ID、分子名、固定软件、固定数值或中心性关键词规则。

## 7. 建议的最小修改顺序

### Step A：先写合同测试（不要先改业务逻辑）

固定三个通用 fixture：

1. 合法 semantic profile（有 propositions + binding projection/comparison）；
2. 合法 numeric profile（有 target + unit + tolerance）；
3. 非法 profile（分别缺字段、重复 binding source、模式不适用）。

测试要求 Agent 工具和外部 Stage06A validator 对同一 snapshot 返回相同 findings 集合；如果有 normalization 前后差异，测试必须明确记录为 `pre_normalization`/`post_normalization`，而不是笼统 passed/failed。

### Step B：统一实现或明确分层

优先选择一个最小方案：把通用 typed-contract helper 提取到可被 standalone 工具使用的、无第三方依赖的模块，或者生成 standalone 工具时同步同一套规则。不要复制一套越来越长的手写逻辑。

### Step C：分离报告

建议文件：

```text
agent_self_check_report.json
external_phase_gate_report.json
```

保留兼容读取 `phase_gate_report.json`，但新代码不再让两种 authority 覆盖同一文件。

### Step D：回归和 A/B

先跑 fixture 与现有测试，再做同样本 A/B；不要直接扩大论文批量。

## 8. 可复现测试方法

### 8.1 单元/合同回归

```bash
cd /mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline
PYTHONPATH=.:.. pytest -q \
  tests/test_stage0607_v9_self_check.py \
  tests/test_stage0607_v8_early_gate.py \
  tests/test_stage0607_v8_task_packages.py \
  tests/test_stage0607_v5_contracts.py
```

验收：所有既有测试通过；新增 fixture 中 Agent/外部检查在同一 snapshot 的 findings 一致。

### 8.2 固定样本批量测试

不要把 API key 写进文档或命令历史。示例（凭据通过环境变量传入）：

```bash
export RCB_GPT_API_KEY='由运行环境安全注入'
python scripts/workflows/run_stage06_07_gpt_batch.py \
  --source-run runs/stage00-05-qualityfix-published-since-20260101-20260814T201641 \
  --output-root runs/stage06-07-v9b-replay-gpt10 \
  --config config.example.json \
  --limit 10 \
  --random-seed 20260824 \
  --max-parallel 10 \
  --harness codex \
  --model gpt-5.6-sol \
  --base-url http://127.0.0.1:50917/v1 \
  --reasoning-effort high \
  --api-key-env RCB_GPT_API_KEY
```

如果要 A/B，必须：

- 两次使用完全相同的 paper manifest、source run、模型、harness、reasoning、并发和 config；
- 只切换 Stage06A `phase_gate_mode`（`agent_and_external` 与关闭 Agent-facing self-check 的对照路径），外部 Gate 保留；
- 使用不同 output-root，禁止复用 checkpoint；
- 统计 `external Stage06A passed / constructed`、每篇自查 finding 数、修复命令数、Stage07 final publish-ready；
- 不把科学拒绝纳入 Gate 通过率分母，单独报告 `provisional_not_constructible`。

### 8.3 逐篇结果核对

每篇至少读取：

```text
papers/<paper>/historical_input_manifest.json
papers/<paper>/stage_06_task_construction/build_results.jsonl
papers/<paper>/stage_06_task_construction/stage_summary.json
papers/<paper>/stage_06_task_construction/workspaces/**/_agent_stdout.jsonl
papers/<paper>/stage_07_task_audit/audit_results.jsonl
papers/<paper>/stage_07_task_audit/stage_summary.json
```

在报告中分开写：

- Agent 自查最后一次结果（从 stdout 重建，直到报告分离修复）；
- 外部 Gate 结果；
- Stage07 科学决定；
- Stage07B status 和 `findings_before/findings_after`；
- 最终 package/publish 状态；
- 每个 finding 属于代码、prompt/Agent、论文输入或模型能力哪一类。

## 9. 不要做的事情

- 不要因为这 10 篇中只有 1 篇发布就放宽 Gate；
- 不要给某篇论文加关键词、固定资产名或固定数值规则；
- 不要把缺失源坐标交给 Stage07B 猜测或生成；
- 不要恢复 Stage06B Agent-facing Gate，除非出现跨论文、可重复且明确由 converter transport 造成的失败；
- 不要用 `git reset --hard`、`git checkout --` 清理工作区；
- 不要把 Stage00–05 或 chemistry toolbox 的既有修改纳入本轮提交。

## 10. 当前交接结论

Stage06B external-only 代码改动已经达到预期；Stage06A 自查机制“能运行、能促成早期修复”，但还没有达到“与最终 Gate 同语义、可作为可靠前置合同”的目标。下一位 agent 的首要任务是修复这两个 Gate 的通用合同对齐和报告可追踪性，然后用固定 fixture 与同样本 A/B 验证；在此之前，不应把当前 1/6 发布率解读为论文质量或模型能力的最终结论。

