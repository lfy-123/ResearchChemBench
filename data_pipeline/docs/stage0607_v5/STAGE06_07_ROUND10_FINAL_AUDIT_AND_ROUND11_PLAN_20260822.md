# Stage06/07 v5 Round 10 终态审查与 Round 11 修改计划

日期：2026-08-22  
代码基线：`0b0fd38`  
文档基线：`4467593`  
有效批次：`runs/stage06-07-v5-round10-deepseek10-concurrency10-20260822-final`

## 1. 运行终态

DeepSeek-v4-pro-0813、Codex harness、high、并发 10。10/10 worker 正常完成，
无 API、429、进程恢复或批处理终态错误。

## 2. 逐篇结论

| paper | Stage07 / 发布 | 对照论文后的判断 |
|---|---|---|
| `9774cf028b321785` | approved_with_repairs / published | 正确。五驻点工作流同时覆盖 Cu(II) Int-C 平衡、Curtin-Hammett 前提和决定对映选择性的两个 Cu(III) TS。 |
| `88939df8484e80c3` | rejected_scientific_unrepairable | 正确。Stage07 发现源坐标只有 338/363 原子，并发现不同组成物种的绝对总能排序没有平衡参考态。 |
| `56da7f9591ef00f2` | approved_with_repairs / published | 错误批准。标题、摘要和结论的最终主张是 drug-like/抗病毒潜力，直接计算证据是 docking 与 500 ns MD；静态 DFT/HOMO-LUMO 只能算支撑性电子结构。Stage06/07 还把缺少 Schrodinger/Desmond 写入范围降级理由，违反软件缺口非阻断原则。 |
| `733b1af3556e9046` | approved_with_repairs / published | 错误批准。任务要求从连接定义自行构建两个有机镍体系的中间体与两个 TS，再按紧势垒/NPA GT 评分；没有作者驻点坐标或确定性 TS 搜索输入，不能称为复现闭合。 |
| `c327fbf5709248aa` | approved_with_repairs / published | 错误批准。没有 MXene/PVA/砷酸根复合周期坐标和吸附位点，却允许从组成/距离配方任意搭建并用紧吸附能、Bader 电荷 GT 评分。Stage07 收据还缺少规定的科学审计表和代表性审计。 |
| `5be4368e659d4b40` | approved_with_repairs / published | 正确。三步 CO2RR 反应能比较是直接解释催化性能的核心子流程，范围声明诚实。 |
| `0b2ae2c005c15e30` | approved_with_repairs / published | 错误批准。完整 CCDC CIF 未随任务提供；fallback 仅靠组成、连接和少量实验键长/角度构建大型双核 Zn 配合物，不能支持源论文紧绝对 FMO/几何 GT。 |
| `d3b4575397179146` | approved_with_repairs / mechanical_blocked | 机械 gate 正确阻断。Agent 写出的 `archive_extractions` 缺少 evaluator 要求的 `source`/`destination`；属于 Stage07 漏修的简单运输合同问题，不是科学 gate 误报。 |
| `72c3e34e4e3814e2` | rejected_scientific_unrepairable | 正确。缺少周期坐标、晶格、Li 位点、NEB 端点/图像及参考能，没有降级成外围任务。 |
| `9ec32e81e2826041` | approved_with_repairs / published | 正确。构象、色散、TD-DFT、S1 和 Zn 4p 轨道组成形成直接支撑标题主张的完整核心子流程。 |

按“科学批准/拒绝是否合理，代码状态是否真实可见”严格统计，明确正确 6/10；错误批准
4/10。当前还没有达到 v5.2 的 80% 目标。失败集中在两类共性，而不是四篇互不相关的
论文特例。

## 3. 归因

### 3.1 Prompt/模型科学判断：最终主张依赖链不够强

`56da7f...` 中两个 Agent 都能填写 representativeness 表，却把直接决定论文最终主张的
docking/MD 重标为 secondary，把容易闭合的 DFT 描述标成 primary。现有 Prompt 要求核对
标题/摘要/结论，但没有要求把“论文最终宣传结论 → 必需计算证据 → 候选工作流”写成依赖链。

### 3.2 Prompt/模型科学判断：输入资产“可生成”与“可复现”混淆

`733b...`、`c327...`、`0b2...` 都把组成、连接、少量几何约束或模型配方当成了闭合坐标。
对于 TS、吸附位点、周期界面、金属配位和大型构象，这些信息只允许生成许多可能模型，
不能复现唯一源结果。`source_constrained_construction` 因而被过宽使用。

### 3.3 代码合同：批准收据证据不是必填

`STAGE07_AUDIT_SCHEMA` 只强制 `audit_decision`、`artifact_path`、`summary`。
`paper_c327...` 因此能在缺少 `representativeness_audit`、`scientific_audit_table`、
`selected_workflow_preserved`、repairs/remaining issues/resource 字段时发布。这是角色履职证据
合同 bug，不是让代码裁决科学。

### 3.4 Stage07B 尚未满足启用条件

只有 `d3b...` 一篇出现科学批准后的简单 schema 阻断，未达到单批至少 2 篇同类问题或连续
两批重复的阈值。Round 11 不启用 Stage07B。

## 4. Round 11 修改计划

1. Stage06A 要求写出 `ultimate_claim_dependency`：论文最终主张、直接计算证据、支持性证据及
   每个候选工作流在依赖链上的位置。数值/坐标易得不能改变中心性；软件缺口不得出现在
   `why_not_full_workflow` 或 `downgrade_reasons` 中。
2. Stage07 独立复核同一依赖链。若选定流程不直接支撑最终主张，必须 workflow redesign；
   真正核心流程无法闭合且没有同等级替代时科学拒绝。
3. 两个 Prompt 加入输入充分性矩阵：区分 identity、connectivity、initial geometry、
   unique/source stationary point、deterministic search protocol 和 target sensitivity。
   对几何敏感的紧绝对 GT，只有可生成任意结构不能记为 closed。
4. 收紧 approved Stage07 receipt 的结构合同，要求科学审计表、代表性审计、修复/遗留问题、
   toolbox/resource 和决策一致性字段；代码只验证存在性/形状，不评价化学内容。
5. 增加通用单测，不出现上述 paper ID、分子名、软件名或固定数值。
6. 运行全量测试后提交 Git，再用 GPT-5.6-sol/high、并发 10、随机 10 篇进行 Round 11。

## 5. 退出标准

Round 11 逐篇人工/Agent 对正文与 SI 复核。正确批准、正确科学拒绝和正确软件缺口登记均算
正确；目标至少 8/10，并且不能以代码科学规则、论文特例或强制提高拒绝率实现。
