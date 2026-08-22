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

## 6. Round 12 终态

批次于 `2026-08-22T05:13:54Z` 结束，状态为 `COMPLETED_WITH_FAILURES`：

- 10/10 worker 到达终态；
- 7 篇正常完成；
- 3 篇为 `stage06_retryable_failure`；
- 5 篇得到有依据的科学拒绝；
- 2 篇经 Stage07 实质修复后批准并通过机械发布；
- 没有机械误阻断、schema load failure 或 approved-but-unpublished 黑洞。

### 6.1 逐篇判定

| paper | 管线终态 | 独立审查 | 结论 |
|---|---|---|---|
| `1257710b003be407` | 科学拒绝 | 中心有机铜机理路线虽有坐标和方法，但缺少决定性的 charge/multiplicity 与 spin-surface 定义；外围 BDE/descriptor 不能替代直接机理 | 正确 |
| `5d94285cfbd51973` | Stage06B retryable | Stage06A 构建了 AZ9 静态 DFT descriptor 任务；它可执行，但相对论文的抗菌/对接主张更像 supporting-only 分支，且 Stage06B 未完成转换 | 严格不正确；另有中心性疑问 |
| `c56ec62e92dbdfbc` | 批准并发布 | 完整 CREST/多路径路线不闭合且超预算；双 TS 自由能差是直接支撑 ee 的最高中心性闭合子流程。Stage07 正确删除了“仅凭双 TS 即证明决定步骤”的过度结论 | 正确且质量较高 |
| `2a758cc748cc0828` | Stage06B retryable | Stage06A 选择了具有精确 SI 坐标和闭合参考态的后光还原自由基羰基化主链，科学选择合理；转换树被错误嵌套 | 严格不正确，科学草稿合理 |
| `0bea8aa6bfd57e65` | 科学拒绝 | QC 和 MD 两条中心路线都缺少确定构象/复合物、质子化/电荷、拓扑/力场与完整 MD 控制 | 正确 |
| `ec61d902ec1e111d` | Stage06B retryable | 七构象 TDDFT-ECD 是论文唯一完整的作者计算链，直接支撑新天然产物的绝对构型；Stage06A 选择合理，Stage06B 未交付 | 严格不正确，科学草稿合理 |
| `7565fae875ec11ed` | 批准并发布 | 三种 Sc2C termination 的结构→HSE06→真空能级→pH/STH 链直接覆盖论文计算主张；Stage07 修正了无界 Cartesian seed/spin 展开、Janus 双面真空参考及 STH 分段公式 | 正确；构造搜索仍需后续跨样本关注 |
| `eda20ed4eb2044e2` | 科学拒绝 | DFT、MD 和有限元三条中心路线分别缺少有限分子模型、周期体系/力场及材料/边界参数 | 正确 |
| `83cdd9460eb100d6` | 科学拒绝 | CoPc/CoFPc ET/PT/CPET 热力学循环缺少六个几何/电子态与 charge/multiplicity；解析模型只是 supporting illustration | 正确 |
| `0b2ae2c005c15e30` | 科学拒绝 | 全部非平凡 DFT/Hirshfeld 分支依赖缺失的 CCDC 2361759 结构；晶胞常数和局部键长不能重建约百原子状态 | 正确 |

### 6.2 两种正确率口径

- 科学方向：Stage06A 的范围选择/拒绝方向约 `9/10`；唯一明显疑问是
  `5d942...` 把 supporting-only 静态 descriptor 当作无法复现 docking 的替代核心流程。
- 严格端到端：`7/10`。三篇 Stage06B retryable 均未得到最终 Stage07 科学裁决，不能计为完成。

这两个口径都不等于发布率。五篇正确科学拒绝属于成功结果。

## 7. 已确认的共性问题

### 7.1 Stage06B 的工作树运输边界不稳定

三个失败具有同一轨迹：

1. Codex 事件先出现 optional code-mode host 不可用；
2. 普通 shell 命令实际 `exit=0` 并返回文件，但模型仍反复声称 shell 未执行；
3. 恢复脚本从 `inputs/task_pair/` 而不是
   `inputs/task_pair/paper_reproduction/` 复制，形成
   `outputs/autonomous_research/paper_reproduction/...`；
4. 顶层 `task.md`/contract 缺失，semantic validator 正确拒绝交付。

这是通用的运输/工作树初始化问题，不是论文科学问题。当前 Prompt 要 Stage06B 自己完成“找到源目录、复制、
展平、再脱敏”，把无科学价值的目录搬运也交给了模型。

### 7.2 supporting-only 替代路线边界仍可能被误读

`5d942...` 的 Stage06A 明知 docking 是更直接的计算证据但不闭合，仍选择单分子 frontier-orbital/global-
descriptor 分支。现有 Prompt 同时写了“不能用 supporting descriptor 替代核心路线”和“先找 closed
electronic-property workflow”，存在可被模型解释为“最中心的可执行分支即可”的张力。

## 8. Round 13 最小修复决定

1. 编排器把 `paper_reproduction/` 的内容预置到可写的
   `outputs/autonomous_research/` 根目录；Stage06B 只做语义脱敏和重写，不再负责复制/展平目录。
2. recovery 后只补齐缺失的预置文件，并清除确定错误的嵌套 transport wrapper；不替 Agent 做方法/答案
   脱敏。
3. Codex harness 对 Stage06/07 显式关闭不可用的 code-mode/code-mode-host feature，保留普通 shell。
4. Prompt 明确输出树已经预置，禁止再次复制 `inputs/task_pair` 或创建嵌套
   `paper_reproduction/`。
5. 统一中心性规则：一个 workflow 仅仅是“所有闭合候选中最中心”还不够；若它对 advertised conclusion
   仍只是 supporting-only，且直接核心路线不闭合，应科学拒绝。
6. 不增加科学机械 gate，不启用 Stage07B。Round 12 的阻塞发生在 Stage06B，且不是 Stage07 批准后的
   简单合同修复簇。
