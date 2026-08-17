# Stage06/07 修订与同论文对照测试报告

日期：2026-08-17  
论文：`paper_6904a9c8c09855cc`，DOI `10.1002/anie.202525581`

## 本轮修订

本轮只做通用合同和运行兼容修复，没有针对论文内容增加规则：

1. Stage06B 的转换报告统一归一化到任务对根目录的 `conversion_report.json`。来源可以是
   Agent 写出的顶层文件、误写到 autonomous 子目录的文件，或最终响应中的
   `conversion_report` 对象。代码只负责搬运/校验文件，不判断科学内容。
2. 删除任务目录内的 `conversion_contract.json`、`derived_from.json`、
   `conversion_receipt.json`、`conversion_manifest.json`。这些是内部来源合同或运行元数据，
   不属于评估 Agent 的输入。
3. Stage07 发布包只保留：`task.md`、`task_info.json`、`task_spec.json`、
   `submission_contract.json`、`process_rubric.json` 和 `data/inputs/`。
4. 本地 loopback API 自动禁用外部代理；兼容 API 拒绝宽松 JSON Schema 时，终端请求回退为
   `json_object`，不改变工具探索协议。
5. Stage06 对 Agent 的 `scientific_not_constructible` receipt 允许无 workflow review 的
   合法科学终止，不再被代码误报为文件系统失败。

## 验证

- `PYTHONPATH=. pytest -q tests/test_stage0607_agents.py`：118 passed。
- `PYTHONPATH=. pytest -q tests/test_pipeline.py tests/test_batch_workflow.py tests/test_resume.py`：268 passed。
- 修复桥接兼容后，`tests/test_stage0607_agents.py tests/test_pipeline.py`：358 passed。
- `python -m compileall -q src`：通过。

## 三模型轨迹对照

| 模型 | Stage06 | Stage06B | Stage07 | 工具调用特征 | 结论 |
|---|---|---|---|---|---|
| `deepseek-v4-flash`（既有测试） | constructed | 53 次；成功 | `approved_with_repairs` | Builder 65 次；Stage07 多轮，曾有一次 invalid output recovery | 能完成流程，但任务抽取和语义 rubric 质量较弱；旧发布包有 manifest 元数据 |
| `deepseek-v4-pro`（本轮） | constructed | 53 次；成功，报告归一化无重试 | `approved_with_repairs`，保留原 workflow | Builder 45 次；Converter 53 次；Stage07 71 次 | 科学抽取和结构恢复最好；本轮验证了报告位置不一致不再导致 `invalid_phase_contract` |
| `gpt-5.6-sol`（本地 `127.0.0.1:50917/v1`） | `provisional_not_constructible` | 未进入 | `objective_failure_retryable` | Stage06/07 工具调用均为 0；API 最终只返回协议恢复 JSON | API 本身可连通，但当前中转/模型适配没有执行 Codex workspace 工具调用，属于 Agent 能力/协议兼容问题，不是科学判定或代码侧任务拒绝 |

Pro 本轮最终发布目录实测只包含：

```text
task.md
task_info.json
task_spec.json
submission_contract.json
process_rubric.json
data/inputs/*
```

其中 `conversion_report.json` 只保存在 Stage07 审计根目录，未复制到任一评估任务目录。

## 问题归因

### 已确认的代码问题（已修复）

- Agent 把转换报告放在响应或 nested path 时，旧代码只检查顶层文件，错误触发
  `autonomous_converter_conversion_report_missing`。现在统一恢复。
- 公开任务目录混入来源合同和 manifest，存在来源信息泄漏。现在在 materialize 和发布阶段
  都清理/隔离。
- 单 Agent 明确科学拒绝但不写成功 review 时，旧代码先读 review，造成
  `FileNotFoundError`。现在科学拒绝先分支处理。
- 本地 API 被共享远程代理配置劫持；现在 loopback 自动禁用代理。
- 部分兼容 API 的严格 schema 要求与宽松 benchmark schema 不一致；现在只在明确的 schema
  错误上降级到 JSON object。

### 非代码问题

- GPT 对照测试的核心限制是工具调用为零。即使 `/v1/models`、`/v1/responses` 和
  `/v1/chat/completions` 的 ping 均返回 200，模型在 Codex 的 tool-capable 请求中没有发出
  `exec_command`，只在协议恢复阶段返回终止 JSON。因此不能据此判断论文不可构建，也不能
  用代码替它执行文件读取或生成任务。
- Flash 的空 acceptance semantic propositions、Pro 与 Flash 任务范围差异，属于模型的
  科学抽取/判断能力差异，不应增加论文特例或代码死规则；应通过 holdout、提示词和模型选择
  评估。

## 后续建议

1. 将 GPT API 作为“Codex 工具调用兼容性”单独做小型 smoke test；若仍为 0 tool calls，标记
   该模型/中转不适合作为 Stage06/07 harness，而不是把任务代码改成无工具静态生成。
2. 保留 Pro 作为当前主力构建模型，继续用 Flash 做成本/召回对照。
3. 继续把科学决定留给 Agent；代码只做路径、文件、manifest、恢复和发布边界管理。
4. 对最终发布包做通用文件白名单测试，防止后续 prompt 或模型重新写入来源合同。
