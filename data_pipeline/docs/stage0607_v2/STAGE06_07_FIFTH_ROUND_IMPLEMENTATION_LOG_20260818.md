# Stage06/07 第五轮实现记录（2026-08-18）

## 本轮目标

本轮按 `STAGE06_07_FIFTH_ROUND_SCIENTIFIC_CLOSURE_AND_EVALUATOR_ALIGNMENT_PLAN_20260818.md` 执行，重点区分确定性代码缺陷、Prompt 合同问题和模型科学能力问题。编排器只负责文件、模式隔离、机械合同和加载诊断，不替 Agent 做科学裁决。

## 修改内容

### 代码合同与发布路径

- `canonicalize_complexity_profile()` 增加 `core_operation_count` 兼容别名，避免同时产生互相矛盾的复杂度字段。
- route fidelity 只按结构化 `criterion_type=route_fidelity` 识别；缺失时形成 finding，不再把第一条科学 rubric 改写成 route rubric。
- reproduction patch helper 同样要求显式 route criterion，避免隐式覆盖其他评分项。
- Stage07 机械门禁在检查前执行一次 mode/ID/枚举/复杂度传输归一化；这类修复不会重新调用科学 Agent。
- 两模式 submission contract 比较改为模式中性的结构比较，允许 autonomous 对答案相关键名做中性化；输入资产按内容指纹比较。
- public 目录扫描不再排除 `workspace`、`source_materials` 等目录名，但只扫描两个最终 public mode tree，避免把 pair-level 内部工作区误报为泄漏。
- 增加最终 `published_tasks` bundle 的 JSON、隐藏目录和必需文件检查，并将结果写入 stage07 记录。
- mechanical failure 不再触发完整 Stage07 Agent 重跑；机械问题阻塞发布并记录 finding，科学 decision 保持 Agent 原值。
- `audit_results.jsonl` 和 `stage_summary.json` 分开记录 `agent_observed_*` 与 `orchestrator_*` 状态。
- Stage06/07 GroundTruth 生成中将 shared conclusion evidence policy 与 mode-specific route policy 分层：autonomous 为 Agent 自选路线，reproduction 为遵循公开路线。
- submission contract 不再要求 Agent 额外生成完整 `report/process_trace.jsonl`；过程权威证据由 evaluator harness 的 canonical trace 提供。

### Prompt 合同

- Stage06A 增加简短 closure checklist：输入状态、物理边界、参考态/化学计量、动作-产物-验证、Ground Truth binding、scope 限制。
- Stage06B 明确 preserve/remove/uncertain 三类编辑；未分类内容默认保留并上报 Stage07，不静默删除。
- Stage07 增加六行科学审计表，要求逐项给出 closed/repairable/unrepairable、证据和实际改动；不由代码填写科学值。
- Stage06 autonomous Prompt 明确不要求重复写完整过程 trace，节省 token。
- Prompt/implementation version 已提升到第五轮版本，避免复用旧缓存。

## 验证结果

### 单元测试

```text
PYTHONPATH=. pytest -q tests/test_stage0607_agents.py tests/test_pipeline.py tests/test_batch_workflow.py
369 passed
```

### Round4 回放

对 `runs/stage06-07-round4-20260818-paper6904-pro0813/stage_07_task_audit/audited_tasks/paper_6904a9c8c09855cc` 执行机械回放：

- `mechanical_pre_publish_status=passed`
- `schema_load_status=passed`
- `evaluator_dry_run_status=not_run`（明确表示尚未执行真实 submission scoring）
- 两个 published mode bundle 的目录/JSON 检查均为 `passed`

旧产物中的 `core_operation_count` 在回放时被一次性归一化，不再触发整轮 Agent 审计重跑。

## 尚未由代码解决的事项

charge/multiplicity、TS action 与虚频验证、物理溶剂边界、GT binding 是否科学对应、scope 是否夸大等仍由 Stage06A/Stage06B/Stage07 Agent 根据全文证据判断。本轮没有加入 Gaussian、论文 6904 或具体分子关键词的死规则。后续用同一论文分别运行 DeepSeek Pro 0814 与 GPT-5.6-sol，对比 closure checklist 的实际召回率。

## 下一步测试

使用同一历史 Stage00-05 输入论文 `paper_6904a9c8c09855cc`，分别提交：

- `deepseek-v4-pro-0814`
- `gpt-5.6-sol`

两个任务使用 Codex harness，独立输出目录，完成后比较 Stage06A、Stage06B、Stage07 轨迹及最终双模式任务质量。

## 模型测试提交结果

两个任务均已真实提交，但当前 `config.local.env` 所指向的中转站令牌没有相应模型权限：

- DeepSeek：run id `stage06-07-history-paper_6904a9c8c09855cc-20260818T085007Z`，上游对 `deepseek-v4-pro-0814` 返回 HTTP 403；三次 harness attempt 均为 0 tool calls、0 tokens，Stage06 记录为 `objective_failure_retryable`，Stage07 未运行。
- GPT：run id `stage06-07-history-paper_6904a9c8c09855cc-20260818T085029Z`，上游对 `gpt-5.6-sol` 返回 HTTP 403；三次 harness attempt 均为 0 tool calls、0 tokens，Stage06 记录为 `objective_failure_retryable`，Stage07 未运行。

这两项是中转站访问权限失败，不是 Stage06/07 代码、Prompt 或科学判断失败。对应运行目录分别为：

- `runs/stage06-07-fifth-round-20260818-paper6904-pro0814`
- `runs/stage06-07-fifth-round-20260818-paper6904-gpt56sol`

获得允许访问上述模型的 URL/API key 后可以直接重新提交；不要把本次失败产物用于模型质量对比。
