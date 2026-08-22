# Stage06/07 v5 Round 19 实施与结果分析

日期：2026-08-22

总目标：`STAGE06_07_V5_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260821.md` v5.2

## 1. 运行信息

- 有效结果目录：`runs/stage06-07-v5-round19-deepseek10-concurrency10-20260822-retry`
- 无效首批目录：`runs/stage06-07-v5-round19-deepseek10-concurrency10-20260822`。该批为配置指向错误 endpoint 后产生的 401，不进入科学或代码统计。
- 模型：DeepSeek-v4-pro-0813
- Harness：Codex
- 推理强度：high
- 并发：10
- 抽样 seed：`20260860`
- 运行状态：10/10 worker 完成，均为进程退出码 0。

`paper_308bbee002d4560c` 的第一次 Stage07 调用没有产生最终消息，编排器按既有恢复合同完成第二次调用并发布；恢复流程本身正常。

## 2. 逐篇审查

| paper | 管线结果 | 独立判断 | 归因 |
|---|---|---|---|
| `paper_543899da7526ed9b` | 科学拒绝 | 正确。NiTe2/Co/vacancy 周期模型缺少晶格、原子位置、缺陷/吸附位点及关键周期设置；VASP 已安装，未因软件拒绝。 | 源材料不闭合，角色履职正确 |
| `paper_1d110039f3d1af1d` | 科学拒绝 | 正确。COF/CNF fragment identity、坐标、长度、电荷/多重度和复合物组成不足。 | 源材料不闭合，角色履职正确 |
| `paper_97df74aff9225c95` | 科学拒绝 | 正确。原文指向独立 POSCAR/CONTCAR 压缩包，但当前快照没有该资产，形成能参考结构也不闭合。 | 源材料不闭合，角色履职正确 |
| `paper_c625cba3ce868eb1` | 批准并发布 | 基本正确。两个 hydroperoxide/analogue 的 MEP/ESP 电荷对比覆盖完整计算分支，输入和目标闭合。原子索引 `[1,3]`、`[7,9]` 未声明零基/一基，存在 evaluator 歧义；根级旧审计记录还保留 `[0,1]`，不影响发布树但说明索引合同不够明确。 | 可用任务；通用 Prompt 小缺口 |
| `paper_308bbee002d4560c` | 修复后批准并发布 | 正确。完整机理约 29 个驻点，所选 IM7/cis-TS6/trans-TS6/cis-4a/trans-4a 子流程是正文明确称为整个过程关键步骤的最终成环，直接覆盖动力学和热力学 trans 选择性。五个 XYZ 可解析；IM7 与两条 TS 组成一致，两个产物组成一致。 | 最高中心性闭合子流程，角色履职正确 |
| `paper_5d08b6b80b3941dc` | 科学批准，机械阻断 | 科学判断基本正确：完整 Bi(V) 路线不闭合，HSO4 radical + CH4 的 HAT 是中央传播步骤且小体系身份、路线与能量表可恢复。机械阻断来自 `task_info.data[0].name` 缺失，evaluator schema 报错真实，但该字段可由已声明 path 确定性派生。 | 确定的运输层代码 bug |
| `paper_2be7143d125be4af` | 修复后批准并发布 | 范围基本正确：五个身份明确的 para-substituted Azo-R 覆盖核心 charge/BDE 机制，排除三个身份不闭合变体合理，BDE 参考态守恒。问题是自主模式允许方法选择却要求五物种严格全序；例如 Br/H 电荷差约 0.002 e，未证明排序对方法稳健。 | Stage07 方法稳健性审计偏弱 |
| `paper_cb289b1dcc8f0d7c` | 修复后批准并发布；登记 FCclasses3 缺口 | 范围可接受但批准偏乐观。Headline BQ7 dimer QM/MM 路线缺晶体原子坐标和 MM embedding，选择七个 monomer 的重原子 photophysics 是仍具中心性的最大闭合子流程；软件缺口仅登记，行为正确。但输入只给 formula/substitution pattern，phenyl rotamer 不唯一；hidden acceptance 仍对多个近简并量使用完整全序。21 个激发态优化/Hessian/SOC/rate 分支估计 600–1000 core-hours，虽可在 48 核约 12.5–20.8 h 完成，但余量很小。 | Stage07 方法/构象稳健性和成本余量判断偏强 |
| `paper_b111d57313b312c5` | 修复后批准并发布 | 不应按当前范围批准。任务只选择 guest-free 1a–c/2 FMO 红移；SI 实际还包含 `1a·(orcinol)2` 坐标、自由/扭曲模型和 host–guest Kohn–Sham orbitals，这些计算直接解释 guest-induced pi-conjugation cleavage 与 quenching。Stage07 错误声称 host–guest 输入缺失，未恢复到更中心路线。现有 Prompt 已要求标题/摘要/结论依赖审计并提供 PDF/layout/坐标回退。 | DeepSeek 未执行已有中心性/源材料审计要求，不是代码 bug |
| `paper_499cdd89b60e365c` | 修复后批准并发布 | 发布任务不可用。除 clean Cu slab 外，多数所谓 POSCAR 的头部语法错位：有的把元素行放在 scale 位置，有的缺 comment 行。Stage07 只核对坐标行数，没有用完整格式解析器验证资产，却声称输入闭合；同时对 13 个周期 DFT 分支的 24 h 可行性论证不足。 | Stage07 结构资产真实性与资源审计失败 |

## 3. 统计与边界判断

- 完全正确：5/10（3 个正确科学拒绝，2 个正确批准/发布）。
- 范围可接受但 acceptance 过强：2/10（`2be...`、`cb289...`）。
- 科学任务有效但被运输 bug 阻断：1/10（`5d08...`）。
- Stage07 科学审计失败并误发布：2/10（`b111...`、`499...`）。

不能把 10/10 进程完成或 6 个 published 解释为任务质量通过。Round 19 暴露了一个通用代码 bug、两个可收敛的 Prompt 边界，以及 DeepSeek 在已有长审计要求下仍可能漏查中心性证据的能力限制。

## 4. 本轮修改

### 4.1 运输层修复

在 `canonicalize_mode_task_contract()` 中增加 `normalize_task_data_files()`：当 `TaskInfo.data` 项已经声明 `path`、但缺 evaluator 必填展示字段 `name` 时，从 path basename 确定性派生名称。该操作不新增、删除或解释科学输入，属于允许的 transport normalization，并由已有文件哈希 normalization 记录体现。

### 4.2 最小 Prompt 修复

Stage06A 与 Stage07 增加三条格式无关要求：

1. 每个结构化科学资产必须由适用的完整格式 parser/schema 实际解析，并记录 parser/tool 和结果；文件后缀、行数或局部坐标检查不能证明完整 grammar 有效。
2. 使用原子、位点、bead、residue 等整数索引时必须声明零基/一基，公共任务、结果字段和 private binding 保持一致。
3. strict ranking 必须审计源精度、未决构象/构建自由度和方法自由；近简并或方法敏感量使用 tie group、partial order、端点/分组趋势或 mode-specific acceptance，不能仅因源表数值可排序就强制全序。

这些要求不包含 POSCAR、特定软件、论文、分子或固定数值规则。代码没有新增结构格式科学 gate，也没有用机械规则替代 Stage07 判断。

### 4.3 版本与目标文档

- Stage06 implementation：`v14-task-data-transport-normalization-20260822`
- Stage06A Prompt：`v15-stage06-asset-and-ranking-closure-20260822`
- Stage07 Prompt：`v23-stage07-asset-and-ranking-closure-20260822`
- 修正总目标中的测试模型描述，使其与用户当前指定的 DeepSeek-v4-pro-0813 一致。

## 5. 验证

- 定向测试：5 passed。
- 全量测试：`PYTHONPATH=. pytest -q` -> 559 passed。
- `git diff --check`：通过。

## 6. Stage07B 决策

本轮不启用 Stage07B。

唯一简单合同阻断是 `TaskInfo.data.name`，可由 path 确定性修复，已经由代码解决；没有达到“至少 2/10 同类简单 Agent 修复”条件。中心性重选、近简并 acceptance、完整结构语法真实性和资源可行性都是科学审计，交给 Stage07B 会越过既定边界。

## 7. 下一轮

Round 19 尚未达到总目标中的至少 80% 正确处理要求。使用剩余一轮预算执行 Round 20：DeepSeek-v4-pro-0813、Codex harness、high、随机 10 篇、并发 10。重点检查：

1. 是否仍因 `TaskInfo.data.name` 出现机械阻断；
2. structured asset 的 parser/tool 证据是否真实，而非 Agent 自报；
3. 自主 acceptance 是否对近简并量使用稳健投影；
4. 是否继续出现“可执行但不够中心”的误发布；
5. 软件缺口是否只登记、不改变范围或科学决定。

Round 20 后即使模型仍有个体科学误判，也不得继续加入论文特例或扩大机械 gate；应把剩余问题明确归为 Prompt 可改进空间或模型能力边界。
