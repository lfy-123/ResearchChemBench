# Stage06/07 下一轮实现记录

对应方案：[STAGE06_07_NEXT_ROUND_WHOLE_WORKFLOW_AND_ARCHE_CASE2_REVISION_PLAN_20260818.md](STAGE06_07_NEXT_ROUND_WHOLE_WORKFLOW_AND_ARCHE_CASE2_REVISION_PLAN_20260818.md)

## 本轮目标

落实整篇路线优先、重要核心子过程降级、ARCHE Case2 式自主模式边界，以及 Stage06/07 机械合同闭合。代码不替 Agent 作科学裁决。

## 已实现

### 1. 公共合同闭合

- 为两个模式统一生成基于 `task_pair_id` 的匿名稳定 `source_id`，避免 autonomous 公开 DOI/标题，同时满足 evaluator 的必填合同。
- 为 `submission_contract.json` 增加通用 `results_schema`；默认 schema 只声明结构化 JSON 对象，不发明论文特定结果字段。
- Stage07 机械门禁会对旧产物做一次 transport normalization，再执行 evaluator load 检查。

### 2. 模式差异与 rubric

- submission contract 的比较改为结果 schema 的类型/层级形状比较，不再比较 autonomous 中性化后的字段名。
- reproduction 缺失 `criterion_type=route_fidelity` 时，Stage06 增加独立的通用路线忠实度条目并重新配平分值，不覆写已有科学 rubric 条目的语义。
- Stage07 审计结果新增 `scientific_audit_passed`、`mechanical_contract_passed`、`publish_ready`，与 Agent 自报字段分离。

### 3. Prompt 与任务选择

- Stage06A 明确整篇 objective-centered route 为默认选择；只有成本、数据、软件家族或科学闭合性证据阻断时才降级。
- 要求记录降级原因、主张覆盖、被省略部分和核心性证据，禁止因任务较短或更省 token 而随意截取。
- Stage06B 明确保留溶剂/相态、温度、压力、波长/光子能量、电荷/自旋、化学计量和实验观察等定义问题所需事实，只隐藏作者实现 route。
- Stage07 增加整篇优先、参考态/守恒和物理边界审计提示。

### 4. 运行追踪

- 历史 late-stage run ID 增加微秒时间和输出路径哈希，降低并发模型运行冲突。
- Stage06/07 summary 增加 `paper_ids`；Stage07 summary 同时记录科学审计、机械合同和发布就绪计数。

## 验证结果

- `python -m pytest -q tests/test_stage0607_agents.py`：125 passed。
- `python -m pytest -q`：510 passed。
- `python -m compileall -q src/stages/stage06_task_builder src/stages/stage07_task_judge src/late_stage_runner.py`：通过。
- `git diff --check`：通过。

## 逻辑复核结论

- Stage06A 仍负责科学 workflow 选择和 reproduction/hidden draft；Stage06B 只负责按 handoff 分类转换 autonomous；Stage07 负责科学审计和小问题修复。
- 代码新增的逻辑均限于匿名 ID、schema、文件合同、状态记录和结果形状比较，没有新增论文关键词或科学结论判断。
- 最终 public mode 目录仍会清理 `conversion_contract.json`、`conversion_receipt.json`、`derived_from.json` 和 `conversion_manifest.json`；转换报告仅保留在外层审计 staging。

## 待测试

代码版本提交后，用同一篇历史论文分别提交 `deepseek-v4-pro-0813` 与 `gpt-5.6-sol` 测试。提交后不轮询，待用户后续要求时再分析运行轨迹。
