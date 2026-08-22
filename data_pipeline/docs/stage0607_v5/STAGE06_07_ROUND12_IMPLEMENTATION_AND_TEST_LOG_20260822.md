# Stage06/07 v5 Round 12 实施与测试记录

日期：2026-08-22

代码基线：`874b548`

总目标：`STAGE06_07_V5_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260821.md` v5.2

## 1. 输入问题

Round 11 的科学决策方向达到 8/10，但严格端到端处理为 7/10。需要修复的通用问题是：

1. Stage07 将已报告 NMR 实验数据的简单算术误认为可挽救任务的替代计算 workflow；
2. Stage06B 将 private conversion handoff 的 method/deliverable JSON 直接附加到公开 `task.md`；
3. Stage06A/Stage07 使用多个最终主张依赖字段别名，导致批准收据无价值重试；
4. Stage06B 将 optional Codex code-mode host warning 错当成 shell failure；
5. 资源评估没有展开 numerical frequency、spin states、response roots 等实际计算分支。

## 2. 修改计划和实际修改

### Stage06A

- 要求选中流程产生新的非平凡计算证据；简单算术、单位换算、重排表格、绘图或对已报告实验值的
  描述统计不能独立构成计算化学任务。
- `ultimate_claim_dependency` 统一为：
  `advertised_conclusion`、`direct_computational_evidence`、`supporting_only_evidence`、
  `selected_workflow_position`。

### Stage06B

- 明确 conversion packet 是 private handoff，禁止复制、引用或序列化到任何公开文件。
- method constraints 必须翻译成正常科学任务文字；evaluated deliverables 必须来自公开
  `submission_contract.json`，不能把 task-package 文件写成提交物。
- 完整任务树已交付但仍有语义疑问时使用 `conversion_uncertain` 交 Stage07；只有真实文件/API/harness
  阻断才使用 `needs_conversion_retry`。
- optional code-mode host 不可用不等于 shell 不可用；shell 成功一次后不得重复 access probe。

### Stage07

- workflow redesign 只能选择非平凡、作者执行的计算化学/分子模拟/科学建模流程；实验 bookkeeping
  不能挽救任务。
- 最终公开面必须移除 conversion packet、deliverable contract、preservation flags 和 task-package manifests。
- 批准收据只使用 canonical claim-dependency 字段。
- 资源审计必须展开自旋态、构象/位点、数值频率位移、轨迹重复、response roots 和验证重跑后再判断。

### 通用恢复提示

- Codex optional code-mode warning 与普通 shell/filesystem 可用性明确分离；成功访问后不重复 `pwd`/`ls`。

没有增加任何论文、分子、软件、数值或固定答案特例；没有新增机械科学裁决规则；没有启用 Stage07B。

## 3. 验证

- 新增 Prompt/恢复合同测试 3 项；
- Stage06/07 定向回归：162 passed；
- 全量回归：549 passed；
- 直接不带 `PYTHONPATH=.` 执行 `test_stage0607_agents.py` 会因测试模块自身未注入仓库根目录而 import
  失败；按项目运行环境使用 `PYTHONPATH=.` 后全部通过。这是测试调用环境，不是 Stage06/07 回归。

## 4. 通用性与职责审查

- “非平凡 workflow”按操作类型和新计算证据定义，不绑定论文领域或计算软件；
- handoff 隔离按 private/public artifact 类型定义，不扫描具体化学关键词；
- 资源展开覆盖量化计算、MD、周期计算和谱学响应等通用分支；
- Stage06A 仍负责构建，Stage06B 仍只负责公开面转换，Stage07 仍负责科学审计和修复；
- 代码仍只负责 transport、schema、artifact 和运行状态，不判断科学中心性或计算价值。

## 5. Round 12 批次

结果目录：

`runs/stage06-07-v5-round12-gpt56sol10-concurrency10-20260822-active`

配置：Codex harness、`gpt-5.6-sol`、reasoning effort `high`、并发 10、seed `20260830`。
该 seed 与 Round 11 的 10 篇没有重叠。随机样本：

- `paper_1257710b003be407`
- `paper_5d94285cfbd51973`
- `paper_c56ec62e92dbdfbc`
- `paper_2a758cc748cc0828`
- `paper_0bea8aa6bfd57e65`
- `paper_ec61d902ec1e111d`
- `paper_7565fae875ec11ed`
- `paper_eda20ed4eb2044e2`
- `paper_83cdd9460eb100d6`
- `paper_0b2ae2c005c15e30`

第一次 `nohup` 提交未进入 Python 主流程，没有 `batch_status.json` 或 worker，不计为测试。随后通过
持久执行会话提交成功：`batch_status.json` 记录正确模型/推理强度，10/10 worker 为 RUNNING，启动阶段
没有 401、429、连接失败或 invalid-agent-configuration。

批次完成后补充逐篇正文/SI 对照、严格正确率、运行轨迹问题和 Round 13 是否必要。
