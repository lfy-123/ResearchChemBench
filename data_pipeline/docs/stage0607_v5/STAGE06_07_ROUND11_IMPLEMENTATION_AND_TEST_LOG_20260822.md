# Stage06/07 v5 Round 11 实施、测试与审计记录

日期：2026-08-22

Round 11 基线提交：`874b548`

约束来源：`STAGE06_07_V5_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260821.md` v5.2

## 1. 本轮目标

Round 10 的严格判断正确率约为 6/10。Round 11 只处理三个共性问题：

1. 模型把容易闭合的支持性计算提升为论文主线；
2. 模型把 chemical identity/connectivity 或任意 buildable seed 当作可复现计算状态；
3. Stage07 批准收据缺少可以审计其职责是否完成的科学证据。

本轮没有要求所有论文批准或发布。正确识别不可构建论文并科学拒绝属于正确结果。

## 2. Round 11 实施内容

提交 `874b548 fix(stage06-07): audit claim dependency and input sufficiency` 完成：

1. Stage06A 增加论文最终宣传结论、直接计算证据、支持性证据和候选 workflow 位置的依赖链。
2. Stage06A/Stage07 明确区分 identity、connectivity、arbitrary seed、source computational state、
   deterministic conformer/site/TS search 和 target sensitivity。
3. 非唯一的 `source_constrained_construction` 不得支撑构象、吸附位点、TS 或周期界面敏感的紧绝对 Ground Truth。
4. 软件缺口只登记，不得作为缩小科学范围或科学拒绝的理由。
5. Stage07 批准收据必须包含代表性审计、最终主张依赖、六行科学审计表、workflow 保留/重构、
   修复和遗留问题以及资源/工具箱状态。代码只检查字段存在性和结构，不判断化学结论。
6. 未增加论文、分子、软件、数值或固定答案特例，未启用 Stage07B。

验证：

- 定向测试：159 passed；
- 全量测试：546 passed；
- 通用性扫描：Stage06/07 修改中没有测试论文 ID、分子名、固定软件或固定目标值。

## 3. GPT Round 11 批次

结果目录：

`runs/stage06-07-v5-round11-gpt56sol10-concurrency10-20260822-active`

配置：

- harness：Codex；
- model：`gpt-5.6-sol`；
- reasoning effort：`high`；
- 并发：10；
- seed：`20260829`；
- Stage05 source：`runs/stage00-05-qualityfix-published-since-20260101-20260814T201641`。

批次终态为 `COMPLETED_WITH_FAILURES`：10/10 worker 结束，9 个正常完成，1 个 Stage06B retryable failure。

## 4. 逐篇审查

| 论文 | 管线结果 | 独立判断 | 结论 |
|---|---|---|---|
| `paper_a79f...` | 科学拒绝 | 核心是双 Topo I-DNA/DDX5 docking→MD→MM-PBSA；prepared states、poses 和关键定义缺失，软件缺口单独登记 | 正确 |
| `paper_8e914...` | 科学拒绝 | 聚合物 MD/GCMC/DFT 主线缺 topology/reactive mapping、周期 host、GCMC 状态及 DFT 物种定义 | 正确 |
| `paper_1bcf...` | Stage06B retryable failure | Stage06A 已构建有精确坐标、两条竞争路径和完整热化学比较的高价值任务；converter 三次误判 shell 不可用 | 运行/Prompt 问题 |
| `paper_0e759...` | 科学拒绝 | PEG/PEGDME–EG/water 双侧比较缺具体低聚物和状态选择，未退化成 water-only baseline | 正确 |
| `paper_128335...` | 科学拒绝 | 双侧 S1 ESIPT 主线缺 source conformers、root following 和 scan definition，未退成静态描述符 | 正确 |
| `paper_3c89...` | 科学拒绝 | Au4 AIM/DI/NBO 是核心，但完整 Au4 坐标缺失且所有核心替代共同依赖该状态 | 正确 |
| `paper_0b113...` | 修复后批准并发布 | 两个 exact periodic models 的 PBE-D3 topology/planarity 比较直接支撑标题主张，双侧和输入闭合 | 正确且产物完整 |
| `paper_0c45...` | 科学拒绝 | 四体系 dipole 比较缺柔性酸/复合物构象和确定性搜索，未退成 connectivity-only 任务 | 正确 |
| `paper_15b84...` | redesign 批准，机械阻断 | 将不闭合 DFT 改为 NMR 浓度、FE 和选择性的实验表格算术；不是非平凡计算化学 workflow | 科学判断错误；机械阻断正确 |
| `paper_44f972...` | 修复后批准并发布 | 双结构 broken-symmetry DFT/UV–vis/Fe K pre-edge 比较是中心且输入齐全；但 autonomous `task.md` 残留私有 handoff JSON/错误 task-package deliverables，资源展开也需更严格审计 | 科学方向正确，公开产物不完全合格 |

## 5. 准确率口径

- 科学决策方向：8/10 正确。六个拒绝和两个批准方向合理；`paper_15b84...` 错误，`paper_1bcf...` 未形成科学终态。
- 端到端严格处理：7/10 完全正确。`paper_44f...` 虽科学方向正确，但公开任务仍含内部 handoff 文本，不能计为完全合格。
- 正确发布率不是目标；本轮六个科学拒绝是 Stage06/07 正常发挥作用的证据。

## 6. 问题归因

### 6.1 Prompt/角色边界

1. Stage07 对 `non-trivial workflow redesign` 的定义不足，允许实验数据简单算术挽救本应拒绝的论文。
2. Stage06B 未明确禁止把 `conversion_packet/deliverable_contract` 直接渲染到公开 `task.md`。
3. Stage06A、Stage07 prose 与收据 JSON 对最终主张依赖使用过多近义字段，导致 `paper_0b...` 和
   `paper_44f...` 分别发生额外重试。
4. 资源审计容易按“两个输入”估算，未展开数值频率、多个自旋态、TDDFT/XAS roots 等实际 job 数量。

### 6.2 模型/Harness 行为

`paper_1bcf...` 的 Stage06B shell 命令实际成功，但模型反复声称 workspace 不可用，并重复执行
`pwd`/`ls`。可选 code-mode host 不可用的提示可能诱发了错误归因。管线正确将其标为 retryable，
没有错误发布；问题主要是恢复指令和模型执行行为，而不是科学合同代码。

### 6.3 代码表现

本轮没有发现新的确定性科学规则代码 bug：

- Stage07 收据结构检查正确拦截了字段别名；
- mechanical gate 正确阻止了缺 route-fidelity evidence 的 `paper_15b84...`；
- 正确批准的两个任务最终均通过机械合同并进入 published tree；
- retryable converter failure 被显式记录，没有形成决策黑洞。

机械代码不应尝试判断表格算术是否具有科学价值，也不应通过论文关键词判断公开 handoff 语义；这些仍属于 Agent 审计职责。

## 7. Round 12 最小通用修改

1. Stage06A/Stage07 明确：简单算术、单位换算、重排表格、绘图和对已报告实验数据的描述统计，
   不能独立构成可挽救任务的计算化学 workflow。
2. Stage06A 与 Stage07 统一 `ultimate_claim_dependency` 为四个 canonical 字段，禁止继续写别名。
3. Stage06B 明确 private conversion packet 不得复制、引用或序列化进公开任务；公开 `task.md` 只能列
   evaluated submission artifacts，不能把 task-package 文件写成用户交付物。
4. Stage06B 完整文件已交付但仍有语义不确定时返回 `conversion_uncertain` 交 Stage07；只有真实
   filesystem/API/harness failure 才返回 `needs_conversion_retry`。
5. 通用恢复提示明确 optional code-mode host failure 不等于 shell failure，成功一次后禁止重复 access probe。
6. Stage07 资源审计展开所有 mandatory branches、spin states、displacements、replicas 和 roots，再判断是否符合 policy。
7. 不实现 Stage07B：当前问题分别属于 Stage07 科学误判和 Stage06B 转换，尚无重复的窄机械修复簇。

## 8. Round 12 停止/继续条件

完成代码测试和通用性审查后，使用新的随机 10 篇、`gpt-5.6-sol/high`、Codex harness、并发 10。
若严格正确处理达到至少 8/10 且没有稳定共性代码 bug，说明本轮目标达到；否则继续下一轮，最多迭代到 Round 20。
