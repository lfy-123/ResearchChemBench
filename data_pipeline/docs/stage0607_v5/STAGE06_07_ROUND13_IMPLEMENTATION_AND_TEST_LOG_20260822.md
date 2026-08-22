# Stage06/07 v5 Round 13 实施与测试记录

日期：2026-08-22

代码基线：`5dbccc6`

总目标：`STAGE06_07_V5_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260821.md` v5.2

## 1. 本轮问题来源

Round 12 的 10 篇测试中，Stage06A 的科学方向约 9/10，但有 3 篇在 Stage06B 因同一种工作区运输问题失败：

- 普通 shell 已成功，Agent 却被 optional code-mode host 的错误事件干扰并误判 shell 不可用；
- Agent 或恢复过程把整个 `paper_reproduction/` wrapper 嵌套复制到 autonomous 输出根目录；
- 顶层任务文件缺失，Stage06B semantic validator 正确拒绝了不完整输出。

另有一个 Prompt 边界问题：闭合候选中相对最中心的流程，如果仍然只是论文最终主张的辅助证据，不能替代不闭合的直接核心流程。

## 2. 实施内容

### 2.1 Stage06B 运输职责前置

- `_setup_converter_inputs()` 将 reproduction 公开树的**内容**直接预置到可写的
  `outputs/autonomous_research/`；Stage06B 只编辑正确根目录中的现成任务。
- 新增 `_ensure_converter_output_scaffold()`，在恢复合并后：
  - 提升并移除确定错误的嵌套 `paper_reproduction/` wrapper；
  - 保留已经存在的顶层语义编辑；
  - 只补齐缺失的必需公开文件和缺失的输入树。
- converter validator 显式拒绝 `paper_reproduction/` 和 `conversion_packet/` wrapper 残留。

这部分只处理目录运输和必需文件存在性，不执行科学脱敏、任务选择或答案判断。

### 2.2 Codex 工具面降噪

- Codex harness 新增可配置的 `codex_disable_code_mode`。
- Stage06/07 默认显式传入 `--disable code_mode --disable code_mode_host`。
- 普通 shell 和文件系统工具不受影响。

### 2.3 Prompt 对齐

- Stage06B 明确输出树已经预置，禁止再次复制整个输入树或创建嵌套 wrapper。
- Stage06A/Stage07 使用一致的通用中心性边界：仅仅是“所有闭合候选中最中心”仍不够；若所选流程对最高中心性论文主张只是 supporting-only evidence，而直接流程不闭合，应拒绝该论文而不是包装外围片段。

## 3. 代码审查与回归

- 新增/更新测试覆盖：预置输出根、嵌套 wrapper 恢复、wrapper validator、Codex feature 参数及 Prompt 合同。
- Stage06/07 定向回归：`165 passed`。
- 全量回归：`552 passed`。
- `git diff --check`：通过。
- 通用性检查：代码和 Prompt 没有论文 ID、特定分子、特定软件或固定科学答案规则。

## 4. 职责边界复核

- Stage06A：仍负责科学范围选择、闭合论证和任务构建；
- Stage06B：仍只负责从 reproduction 公开面转换 autonomous 公开面；
- Stage07：仍负责独立科学审计、必要修复和批准/拒绝；
- 代码：只负责确定性的工作区运输、恢复、结构验证和工具配置。

本轮不启用 Stage07B，因为 Round 12 的稳定失败簇发生在 Stage06B 交付之前，并非 Stage07 审计后仍需简单合同修复的任务。

## 5. Round 13 批次

结果目录：

`runs/stage06-07-v5-round13-gpt56sol10-concurrency10-20260822`

配置：`gpt-5.6-sol`、high、Codex harness、并发 10、seed `20260848`。样本与此前 v5 批次的 108 篇均不重叠。10/10 worker 正常到达终态，无 API、harness 或 Stage06B retryable failure。

终态分布：

- Stage06A：3 篇 provisional constructed，7 篇 provisional not constructible；
- Stage07：2 篇批准并发布，1 篇科学批准但机械阻断，7 篇科学拒绝；
- mechanical gate：无误阻断；唯一阻断真实对应 evaluator schema/route-fidelity evidence 缺陷。

## 6. 逐篇审查

| paper | 管线结果 | 正文/SI 与最终产物审查 | 判定 |
|---|---|---|---|
| `1f75d49fd0794b70` | 科学拒绝 | 中心 DFT/TDDFT/SOC、S0/T1 relaxation 和 cyclized/un-cyclized 对照都缺少源驻点/完整 SI 数值；没有用实验值重排挽救 | 正确 |
| `25cf900788ed833f` | 科学拒绝 | 光物理/铜传感路线缺少 CIF/坐标、Table S3 和 Cu(II) complex state；外围 descriptor 不能替代 | 正确 |
| `46f6118697c6397c` | 科学拒绝 | 四个取代物的 DFT/TDDFT 路线仅指向外部 CCDC，无内部几何；拒绝有依据 | 科学正确，但 toolbox receipt 自相矛盾：把已匹配安装的 Gaussian 同时记为 `needs_software` |
| `5abe7bbb49ae38e5` | 批准并发布 | Stage07 从 9306 行伪结构中恢复 3-2/TS23/3-1*，但漏检 TS12 为 345 原子而路径端点均为 373 原子，仍要求 IRC；五个大型 opt/freq 和两个 IRC 的 24 h 可行性也只有断言；未重新计算的 2/4-proton 结论仍进入 final GT | 不正确，科学审计漏检 |
| `6e09640463562644` | 批准并发布 | BaOH n=1–5 静态 QC/TS/IRC 是直接支撑 headline threshold 的核心流程；Stage07 正确拆成六个 XYZ frame 并补 observed bands。但公开定义 `ΔG(3A−3B)=G(3A)−G(3B)`，同时 hidden 以 `+1.69` 表示“3A 低 1.69”，符号矛盾 | 范围正确，合同科学符号不正确 |
| `7a1d5d7c60a0ae04` | 科学批准、机械阻断 | 氧鎓还原 cis/trans barrier/NCI 是直接核心子流程；Stage07 正确恢复八个 source frame 并登记 NCIPLOT/Chemcraft 缺口。但两个 hidden policy 对象被写成字符串，route-fidelity criterion 缺证据 | 科学方向正确，Stage07 合同交付失败；gate 正确 |
| `880da984c53ecf48` | 科学拒绝 | host 1/3 与 PQT2+ AIMD 机制缺复合物初态、原子映射和轨迹起点；Pearson/RDF-only 属 supporting-only | 正确 |
| `8dfe68f29439e76d` | 科学拒绝 | 1HBT–4HBT 绝对 excited-state/dipole/SOC 主线依赖缺失的 source/crystal structures；没有改选容易的实验或 descriptor 片段 | 正确 |
| `ae62f86035f43274` | 科学拒绝 | Cu-In-Te neutral/anion isomer ranking 缺完整结构和确定性搜索，n=2 的少量距离不能闭合绝对能量/ADE/VDE | 正确 |
| `e0a13f62f9e90fbb` | 科学拒绝 | cocrystal 路线从 X-ray geometry 开始，但 SI 只有 checkCIF 元数据、无 atom-site loop；FMO/QTAIM/IGMH 均依赖同一缺失几何 | 正确 |

## 7. 正确率与角色表现

- 科学范围/拒绝方向约 `9/10`：除 `5abe...` 的最终批准外，中心性选择方向有依据；`6e096...` 和 `7a1d...` 都选到了直接核心流程。
- 严格端到端正确为 `6/10`：`5abe...`、`6e096...`、`7a1d...` 分别存在科学闭合、符号、Stage07 合同交付问题；`46f...` 的软件状态记录不符合角色要求。
- Stage06B：3/3 正常完成，Round 12 的 wrapper/shell 共性故障消失。
- Stage07：能从源材料修复复杂坐标边界，说明源材料访问和修复职责有效；但最终复核没有逐 frame 验证路径组成、代入检查差值符号，也没有完成严格合同自检。
- 代码：没有 worker 状态黑洞、schema load 隐藏失败、机械误阻断或批准后静默不发布；机械 gate 对 `7a1d...` 的阻断正确且理由可见。

## 8. Round 14 决定

进入 Round 14，采用 Prompt-only 最小修复：

1. Stage06A 明确多 frame XYZ 边界与 IRC 元素组成/映射检查；
2. Stage07 修复后必须重新解析 frame，并执行差值公式/数值/自然语言/per-mode binding 的符号闭环；
3. 资源可行性必须有展开分支与有依据的 walltime/memory 观察；
4. 最终合同清单固定 policy object、route-fidelity evidence 和 toolbox 状态一致性；
5. 未重新计算的对照分支只能作为 unscored context。

不新增代码侧科学 gate，不启用 Stage07B。Round 13 只有 1/10 出现简单机械阻断，未达到总目标定义的启用阈值。
