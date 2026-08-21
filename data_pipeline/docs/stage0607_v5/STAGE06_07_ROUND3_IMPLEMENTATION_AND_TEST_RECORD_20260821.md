# Stage06/07 v5 Round 3：代表性审计与批处理终态修复

日期：2026-08-21  
基线：`e9bfc7f`（v5 round2 结果分析后的 `main`）

## 本轮目标

在不加入论文、分子、固定数值或软件特例规则的前提下，把“完整计算路线优先、核心子过程兜底、外围流程不得凑数”落实到两个 Agent 的通用审计职责；同时修复上一轮发现的批处理孤儿 `RUNNING` 状态。软件不在当前 toolbox 时只登记缺口，不改变科学范围或科学决定。

## 实际修改

1. Stage06A prompt 版本升级为 `v10-stage06-representativeness-and-toolbox-policy-20260821`：
   - 要求比较论文标题/摘要/主图或主表/结论中的计算主张与候选 workflow；
   - 完整路线只能因成本、关键输入缺失或科学闭合失败降级；工具箱缺口不是降级理由；
   - 增加 `representativeness_review`、输入 provenance 状态和非阻断 `execution_readiness` 说明。
2. Stage07 prompt 版本升级为 `v17-stage07-representativeness-and-toolbox-policy-20260821`：
   - 独立复核 Stage06A 的候选流程比较，发现外围流程时重选或科学拒绝；
   - 要求在新批准收据中写 `representativeness_audit`；
   - 明确缺失软件只进入 `required_additions`/`execution_readiness`，不能导致科学拒绝。
3. Schema/验证增加代表性审计字段的结构支持。验证器只检查容器、ID、覆盖字段和 evidence ID 形状，不计算科学中心性；旧科学拒绝/批准收据仍可读取。
4. `run_stage06_07_gpt_batch.py`：worker 在进程创建、日志或子命令异常时写 `FAILED`；父级捕获异常 future，持续写入完成计数和结果，避免单篇失败导致永久 `RUNNING`。
5. Stage07 summary 增加 `execution_readiness` 分布，便于区分科学决定与后续软件准备度。

## 回归检查

- `PYTHONPATH=. pytest -q tests/test_stage0607_agents.py tests/test_stage0607_v5_contracts.py`：152 passed。
- `PYTHONPATH=. pytest -q tests/test_batch_workflow.py tests/test_stage_layout.py tests/test_pipeline.py`：259 passed。
- `python -m compileall -q`：Stage06/07 源码、批处理脚本和新增测试通过。

## 兼容性判断

本轮没有把 `representativeness_review`/`representativeness_audit` 设成历史产物的硬发布门槛：新 prompt 要求 Agent 提供，代码在字段出现时做通用形状检查；旧收据缺字段仍能运输。这样既能观察角色是否执行了新职责，也不会把历史科学拒绝或旧批准结果误改写成代码失败。

## 下一步

提交本轮精确 Git 版本后，从 Stage05 通过论文中随机抽取 10 篇，用 `codex` harness、DeepSeek-v4-pro-0813、推理强度 high、并发 10 测试。提交后等待约 30 分钟，再逐篇核对代表性、软件登记、输入闭合、科学决定与运行终态；个别论文失败不自动视为代码问题。
