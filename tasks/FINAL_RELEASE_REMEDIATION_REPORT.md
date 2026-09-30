# Final 任务发布修复汇总

更新：2026-09-15。审计总范围仍为 56 篇论文、111 个任务（AR 55，PR 56）；按用户要求迁移后，**final 为 53 篇、105 包（AR 52，PR 53），hold 为 3 篇、6 包（各模式 3）**。

三篇的完整任务目录已原样移入 `tasks/hold_verified_autonomous_research`、`tasks/hold_verified_paper_reproduction`，没有改变包内科学内容或 evaluator。按 group 的核查/最小补算交接指令见 [HOLD_VERIFICATION_HANDOFF.md](HOLD_VERIFICATION_HANDOFF.md)。`84ef` 仍在 final，保持下述发布主张限制。本次只迁移与维护入口/校验，不发起验证计算。

本报告是本轮发布修复的集中入口，位于 `tasks/`，不写入验证资料目录。执行依据仍为 [批准方案](../docs/verification/final_verified_tasks/final_release_remediation_plan.md)，但其中允许同步 group/维护文档的旧条款已被用户后续“不要修改 docs/verification”指令覆盖。**本轮没有修改该目录，没有提交/取消 HPC 作业，没有新科学计算，也没有实际对外发布。**

## 1. 目前可以得出的结论

不能把全部 111 包宣布为“无条件、全关键点验证通过”。

- **3 篇 / 6 包仍有明确发布缺口，已移出 final 到 hold**：`paper_6492e1e5d38d23ae`、`paper_8b7bf002cc6a4ba9`、`paper_b815e2622b0d6085`，均涉及 AR、PR。具体缺口及处理建议见第 3 节；补充验证按交接文档执行，当前没有因迁移而宣布这些缺口解决。
- **1 篇 / 2 包需要准确限定发布主张**：`paper_84efbea3ab8e6e20`。有真实 SOC/三重态后处理，可支持当前 evaluator 已允许的“有证据的替代解释”；不能宣传为论文 CZ2B/T4-HLCT 解释已被复现。
- 其余 **52 篇 / 103 包** 本次没有新增上述发布阻塞，继续沿用已有逐篇审计和各包批准范围。此计数不是本轮重新逐篇全文审读的声明，更不是全方法、全构象空间或全部论文结论的复现证书。
- 六篇 / 十二包的 public starter 与历史作者 endpoint 不同，**不因此否定作者路线验证，也不要求重算**。只是不能声称已经从当前公开 starter 盲自主复现作者结构。
- 实际运行时的文件系统/网络隔离必须由发布运行环境保证。包校验及“只复制 agent_input”的代码检查不能证明一个可访问整个仓库的 agent 不会读到答案。

`reference` 仍只记录计算过程和证据；评分仍使用 evaluator 的中间关键点与结论。档案中的旧 HOLD/PARTIAL、字段名差异或历史失败标签不等于当前任务失败。

## 2. 已落实的修复

### 2.1 已批准的四项任务契约调整

| 决策 | 论文，两种模式 | 已落实内容 | 没有取消的要求 |
|---|---|---|---|
| D2 | 08c040bf4e456891 | 两条合理、连续、有效验证的解离路径；不强制完整多维 MEP 证明 | 三项能量、两通道、端点身份、路径有效性 |
| D3 | 5286f393dfa5a49a | 固定输入几何；wB97M-V/def2-TZVP/SMD(DCM) 主比较；其他方法/优化单列敏感性 | 现有对象、主排序目标、容差 |
| D4 | 84efbea3ab8e6e20 | 实验寿命隐藏，由 evaluator 对照；agent 报计算比较与限制 | 全部三分子、选态、SOC、态字符 |
| D6 | 9d091f4337662e78 | 按最终构象身份匹配，区分 initial_id/endpoint，重复终态只计一次 | 三种不同构象及三成员归一化；不足三种不能交完整布居 |

### 2.2 现有真实输出的整理

- **534ae3b6e2fb695f**：全局亲核性、两个 N 的局部量、环面角、键连扭转分开；从真实输出补齐原子映射、几何、平面残差和 CDFT 探针来源。固定 TCE 标尺是批准的 benchmark 约定，未冒充论文唯一披露方法。
- **1b285cf9f763f2cf**：每状态完整 24 中心、128 壳层键、288 无序配对角；改正组成解释，不使用 nearest-target 选角。等距离邻居增加稳定排序，避免不同数值环境导致归档不一致。
- **b815e2622b0d6085**：先按归一化轨道成分确定候选，再分别提取 fundamental/framework 和 minimum same-k gaps；保留所有较低候选和态身份。第二网格身份不足仍明确保留。
- **08c / 0dc855 / 5286 / 6e096 / f9 / 4e977**：已完成的扫描、热化学、敏感性或性质结果不再被旧未完成状态遮蔽。电子能、ZPE、Gibbs、不同计算模型没有混为同一量。
- **2f0a**：统一使用已公开实验 X-ray/IR 观测的指令，不能一处说 supplied、一处又要求比较未提供的 hidden 数据。
- **0de37 / 221 / 3a22 / 430**：保留已修复的身份、输入与作者路线证据边界；未因本轮而无意义地重写已正确任务或恢复作者 endpoint。
- **98b6f8a0352f72c2**：只从 reference 的成功链摘除调度恢复块，其中含被取消的旧运行；两套有效 Opt/Freq 和两套后续 TDDFT/NTO 保留，原始历史未删。

### 2.3 本次续做中纠正的两处错误“闭合”表述

**8b7：此前 reference 的完整成功结论不成立，已撤回。**

亲自核对正文 PDF p.10、SI Fig. S5/S7，以及四套 ORCA/xTB 的原始输出后：

1. 四套 ORCA 是 CPCM(Water)，不是 gas phase。
2. 原来标作 5.752107 / 8.407257 / 5.856768 / 10.615064 D 的值实际上是 a.u.。输出明确打印的 Debye 为 **14.620695228 / 21.369550129 / 14.886720073 / 26.981347392**。
3. 四份 xTB stdout 均有 `FAILED TO CONVERGE GEOMETRY OPTIMIZATION`。正常包装器终止和 `xtbopt.xyz` 不能证明优化成功。
4. AL_extended 有断键；另三份显式簇的溶质变为 NH2/COOH，AB_extended 文件的终态其实 compact，不能按初始文件名宣布为 extended zwitterion。
5. 后来的八个 ORCA SP 确实成功；但它们是在上述未验证几何上的单点，不能把失败前驱变成有效极小值。整水簇偶极也不是 Fig. S7 的分子偶极。

两个 reference 已改为简明有效链：真实隐式水 Opt/Freq 与性质 → 分开的下游诊断/排除原因 → 尚未支持的 evaluator 结论。没有把失败条目伪装为成功，也没有改动 group 的原始记录。

**84ef：有真实三重态结果，但原来的相对 Bpin 解释写反了，已纠正。**

- 最大 SOC 根是 CZ1B/T3、CZ2B/T4、CZ4B/T3；真实自旋/能量及 X/Y 后处理证据完整保留。
- 同一 state-weighted Löwdin 定义的 Bpin particle fractions 分别为 **0.089721184 / 0.035307522 / 0.077837085**，不能据此说 CZ2B 比另外两者“更多”。
- 正文 p.3/SI S21–S23 的 T1 电荷重排与正文 p.4 的 SOC 相关 T3/T4-HLCT 是不同问题；T1 定性相符不能代替 T4-HLCT 验证。
- 两个 reference 已记录全部五个近 S1 的 SOC 配对、所有对应三重态、有效后处理及定义差异，剔除 cancelled 调度条目。保留“有证据的替代解释”和“作者特定解释未复现”的区别，不擅自修改 evaluator。

## 3. 仍需处理的问题和建议

### 3.1 paper_6492e1e5d38d23ae — group_5 — D1 未定

**已经确认：**

- 正文 Fig.5/讨论的目标为 anatase 6.871 eV、rutile 7.009 eV。
- 已阅读 group 中保留的出版社 SI DOCX，TextS5 规定 VASP/PBE、400 eV、0.03 eV/Å 力阈值及 relaxed lattice，没有唯一 termination、层数、真空或 k 网格。因此不能把公开的六层/18 Å 约定冒充唯一作者模型。
- 主分支为 anatase **6.36999978845305**、rutile **7.189349995247433 eV**。anatase 低于现行下界 6.371 eV 约 **0.00100021155 eV**，不能靠四舍五入宣布通过。
- 历史结果 `difference_eV=-0.8193502067943825` 使用了反向定义。task、schema、规则现已明确 **W(rutile)−W(anatase)**；reference 列出正确派生值 **+0.8193502067943825 eV**，保留原历史快照。只支持方向；该差值幅度不是论文的 0.138 eV。
- 另一 anatase termination 为 **7.173123045896127 eV**，不能因为它更接近 gold 而事后换主分支。

**建议和待确认：**目前保留原科学目标与容差，暂不把两个模式列为“全数值验证通过”。如要继续修定义，应先依据物理构造固定切割/终止规则、两面身份和放松约定，再匹配已有计算；若仍不满足数值规则，再单独讨论评分合理性。**我未选择 termination，也未扩大容差。** 单独修符号已经完成，不依赖 D1。

### 3.2 paper_8b7bf002cc6a4ba9 — group_5 — D5 未定

**当前差距：**有效隐式水计算偏好 AL_folded 和 AB_folded（AB 的裸电子能差约 7.9061 kcal/mol），并未再现 evaluator 的 AB_extended 最稳。作者定义是每个候选 `E(complex)−E(对应水网络)`；旧整簇 xTB 能量比较不是同一量。现有配对 SP 也不能补救未收敛/身份错误的结构。

**建议和待确认：**

1. 保留“水中 AL/AB 构象稳定性及分子偶极”的科学目标，不改成整簇总能量、不中途更换期望排序。
2. 建议明确以作者复合物减水网络的定义作为主比较依据，并为分子偶极注明所对应的溶质结构、溶剂近似和单位。AR 只提供定义/测量边界，不给作者优胜构象；PR 可增加路线。具体主模型/偶极取法仍需确认，不能从当前已算结果倒推。
3. 对其他 agent 如能提供的**已经存在**的收敛、身份保持的水簇和对应 SP，逐条核对。当前检查到的四套旧显式链不能当作这些有效证据。
4. 若没有这样的现成证据，继续暂缓两个模式作为已验证任务发布。此建议不等于发起重算；本轮未提交或要求自动补算。

### 3.3 paper_b815e2622b0d6085 — group_6 — 第二网格态身份不足

**已支持：**三晶体的主网格 HSE06 收敛、完整低导带候选、Pb-p-leading 成分判别、两种 gap 及 same-k gap，主 framework 数值在原容差内。fundamental 趋势与 framework 趋势没有混用。

**尚缺：**3×3×1 网格没有 PROCAR、vasprun 的 projected 内容或可用 WAVECAR。相同 band ordinal 的能量变化只说明谱值敏感性，不能证明比较的是同一个物理 framework manifold。当前指令明确要求每个已报告量的数值稳定性，故该必评证据不能被省略。

**建议：**优先找是否有另存的现成投影/波函数；没有则暂缓完整已验证发布。若希望把“主网格身份成立 + 第二网格谱值敏感性”作为接受标准，那是必评证据要求的调整，必须由用户另行批准。我没有降为 optional，也没有提出必须增加 SOC 或光学计算。

### 3.4 paper_84efbea3ab8e6e20 — group_6 — 发布主张需限定

现有 task/evaluator 已允许明确有证据的 alternative，且未要求精确 HLCT 分区百分比或 PVA 因果模型。因此不能因为尚未复现作者特定 HLCT 解释，就说所有分子计算都不可行；也不能反过来宣称作者解释已被证明。

建议继续保留现有科学目标、SOC/态字符必评和 alternative 条款。如果发布，说明“已验证分子计算与态字符分析的可行性，允许有证据的不同解释”；**不标注为论文 T4-HLCT 结论已完整复现**。如果发布政策要求每篇必须复现作者特定解释，则应将它一并暂缓，而不是删除证据要求。

## 4. 输入和验证口径

以下六篇均有 AR、PR，十二个 public starter 包继续保留：

- `paper_0dc85595cab7bc0a`、`paper_221aafe4bd916a11`：历史确定性位移 starter。
- `paper_0de37d01e35c27df`、`paper_3a22e838133b906d`、`paper_430b9cbe83c2c203`、`paper_9d091f4337662e78`：独立 topology-preserving starter。

这些记录区分了几何来源；不是声称所有 starter 的生成方法都相同。作者 endpoint/TS 可作为后台验证输入；当前公开 starter 未独立复跑不构成需要补算的理由。小位移或文件注释本身也不是“绝对无泄露”的证明，仍须依据具体任务的求解对象及真实可见边界判断。

固定结构性质任务允许给定该结构作为研究对象；结构/TS 搜索任务不应公开待求 endpoint。PR 可获得作者假设/路线，AR 不可；两者均不能拿到隐藏数值答案、结论或待求几何。

## 5. 检查和版本

### 实际检查结果

| 检查 | 结果 | 不能据此宣称的内容 |
|---|---|---|
| 全部 111 包直接 `validate_task_package` | 0 findings；manifest 均一致 | 科学目标自动通过 |
| task 标题/模式分区与公开输入声明 | 0 指令格式 findings，0 缺失路径，0 task 私有绝对路径引用 | 所有语义歧义均由格式测试排除 |
| 公开 JSON/XYZ 及元素行检查 | 0 解析错误、0 非法元素行 | 任何起点都一定收敛到同一终态 |
| 几何文件名/头部标记 | 0 高风险 endpoint/TS 标记；30 个 SI 来源标记需按固定性质/求解对象解释 | “零关键词命中”证明绝对无泄露 |
| 本次重写/补充的三个 reference 的本地链接 | 130 个链接均存在 | 路径存在本身即科学有效 |
| 成功链 JSON 的失败/取消/运行条目复查 | 111 包中未再检出上述负状态执行对象 | 只有状态检查即可替代应用日志审读 |
| 最后一次修复及相关回归（没有排除测试） | **94 passed**，36.97 s | 整个运行平台已端到端验收 |

执行命令：`.envs/researchchembench/bin/python -m pytest -q tests/test_final_release_remediation.py tests/test_three_boundary_repairs.py tests/test_remaining_final_task_repairs.py tests/test_agent_geometry_audit.py tests/test_task_package_v19.py`。这些是软件/mock 测试、原始文本核对和既有数据的算术/几何提取，不运行新的量子化学作业。

测试过程中的并行改动已单独区分：早先测试曾遇到 `runner.py` 缺少 `os` 导入，以及旧恢复测试未启用 `recovery_enabled` 却要求恢复（`legacy_run_not_resumable`）。并行维护工作随后补全导入，并把恢复测试调整为显式启用恢复、真实 mock 中断/继续的持久化链；最后完整重跑 **94 项全部通过**，没有靠 deselect 隐藏失败。我没有修改或提交这些并行运行器/恢复测试内容；自己的目录别名测试放在独立 `test_final_release_remediation.py` 中。该结果基于当时的共享工作区，运行器维护者仍需保存其对应版本；这些软件问题不算新增“验证论文失败”。

### 工具与版本边界

- 审计器增加应用层几何失败过滤；明确 xTB 优化失败不能被 return_code=0 遮蔽；成功 retry 仍保留。该过滤器是负证据检查，不是假装通用收敛判据。
- 审计器移除“本次实施了固定清单修复”的硬编码宣称；不把旧 public-starter replay 要求恢复成发布门槛。
- 新回归覆盖四项批准契约、失败记录过滤、6492 符号/不放宽容差、8b7 Debye/未收敛前驱、84ef 真实自旋与不过度结论，以及两个 final 目录别名。
- 六个既有边界包（534、1b285、b815 各两模式）的 `release_reconciliation` 与只读重提取结果比较；几何邻居排序已消除数值环境微小误差引发的记录抖动。
- 包内复制路径只包含 `agent_input`；真实运行时的读权限、挂载、软链接、网络访问仍由部署端检查。评估索引只选 final roots，避免同时索引源 tasks 产生重复 `paper_id/task_type`。

版本基线：`40a6cb60`（批准实施前）；上一批修复：`0a870315`。相对基线，当前累积实际修改 **15 篇 / 30 包**；其余重点论文核对正确则不重复改文件。此次续做修改 **4 篇 / 8 包**，其中只有 6492 的两包涉及公开定义/规则措辞，其余是 reference 更正；本轮没有修改 gold 数值、容差或新增科学边界。原始历史及旧 reference 可从 Git 取回，没有删除原始计算文件。

## 6. 逐论文入口

AR/PR 是两个实际模式包的参考计算链接，不是两个独立盲测通过标签。“沿用”表示本轮未引入科学变更，需保留该 reference 中的原有模型/证据限制。下列清单不把自动档案状态重新命名为科学 PASS。

| paper_id | 模式/计算记录 | 本轮结论 |
|---|---|---|
| `paper_08c040bf4e456891` | [AR](final_verified_autonomous_research/paper_08c040bf4e456891/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_08c040bf4e456891/evaluation/verified_computation_reference.md) | D2 已落实；两通道与三能量保留 |
| `paper_0a62b797f51de2c0` | [AR](final_verified_autonomous_research/paper_0a62b797f51de2c0/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_0a62b797f51de2c0/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_0dc85595cab7bc0a` | [AR](final_verified_autonomous_research/paper_0dc85595cab7bc0a/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_0dc85595cab7bc0a/evaluation/verified_computation_reference.md) | 作者路线证据保留；不同 starter 不要求重算 |
| `paper_0dcba54d6a1436bd` | [AR](final_verified_autonomous_research/paper_0dcba54d6a1436bd/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_0dcba54d6a1436bd/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_0de37d01e35c27df` | [AR](final_verified_autonomous_research/paper_0de37d01e35c27df/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_0de37d01e35c27df/evaluation/verified_computation_reference.md) | C10H14S2 身份保留；不同 starter 不要求重算 |
| `paper_1b285cf9f763f2cf` | [AR](final_verified_autonomous_research/paper_1b285cf9f763f2cf/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_1b285cf9f763f2cf/evaluation/verified_computation_reference.md) | 全壳层与组成已对齐；限批准 56 原子模型 |
| `paper_221aafe4bd916a11` | [AR](final_verified_autonomous_research/paper_221aafe4bd916a11/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_221aafe4bd916a11/evaluation/verified_computation_reference.md) | TS/IRC 作者路线证据保留；TS 私有 |
| `paper_2c439196c2f349c9` | [AR](final_verified_autonomous_research/paper_2c439196c2f349c9/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_2c439196c2f349c9/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_2f0a4f80a37fbccd` | [AR](final_verified_autonomous_research/paper_2f0a4f80a37fbccd/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_2f0a4f80a37fbccd/evaluation/verified_computation_reference.md) | 实验边界 supplied/hidden 指令已统一 |
| `paper_2f2aa11ea61a32bb` | [AR](final_verified_autonomous_research/paper_2f2aa11ea61a32bb/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_2f2aa11ea61a32bb/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_2f302589e5e9e420` | [AR](final_verified_autonomous_research/paper_2f302589e5e9e420/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_2f302589e5e9e420/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_3235db287859287e` | [AR](final_verified_autonomous_research/paper_3235db287859287e/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_3235db287859287e/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_3316e45a74258fb7` | [AR](final_verified_autonomous_research/paper_3316e45a74258fb7/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_3316e45a74258fb7/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_36722b90a0c12825` | [AR](final_verified_autonomous_research/paper_36722b90a0c12825/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_36722b90a0c12825/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_3a22e838133b906d` | [AR](final_verified_autonomous_research/paper_3a22e838133b906d/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_3a22e838133b906d/evaluation/verified_computation_reference.md) | 中性/阴离子性质与映射；不同 starter 不要求重算 |
| `paper_3c058fa17fa7c54e` | [AR](final_verified_autonomous_research/paper_3c058fa17fa7c54e/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_3c058fa17fa7c54e/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_3e4cad1d1d650d0c` | [AR](final_verified_autonomous_research/paper_3e4cad1d1d650d0c/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_3e4cad1d1d650d0c/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_430b9cbe83c2c203` | [AR](final_verified_autonomous_research/paper_430b9cbe83c2c203/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_430b9cbe83c2c203/evaluation/verified_computation_reference.md) | 独立 cis/trans starter；按真实终态处理身份 |
| `paper_4e9774f4128551d3` | [AR](final_verified_autonomous_research/paper_4e9774f4128551d3/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_4e9774f4128551d3/evaluation/verified_computation_reference.md) | 正确 50/S20 链及 ΔG≈2.641225；旧失败不覆盖成功 |
| `paper_4fa592965be9841e` | [AR](final_verified_autonomous_research/paper_4fa592965be9841e/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_4fa592965be9841e/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_51a03695e1ccb105` | [AR](final_verified_autonomous_research/paper_51a03695e1ccb105/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_51a03695e1ccb105/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_5286f393dfa5a49a` | [AR](final_verified_autonomous_research/paper_5286f393dfa5a49a/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_5286f393dfa5a49a/evaluation/verified_computation_reference.md) | D3 已落实；固定几何主协议，敏感性分开 |
| `paper_534ae3b6e2fb695f` | [AR](final_verified_autonomous_research/paper_534ae3b6e2fb695f/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_534ae3b6e2fb695f/evaluation/verified_computation_reference.md) | 描述符/原子映射/角度/残差完整；保留批准标尺 |
| `paper_60f4c45810428116` | [AR](final_verified_autonomous_research/paper_60f4c45810428116/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_60f4c45810428116/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_63a9254b8e68a23c` | [AR](final_verified_autonomous_research/paper_63a9254b8e68a23c/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_63a9254b8e68a23c/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_641a923cbe5bbc48` | [AR](final_verified_autonomous_research/paper_641a923cbe5bbc48/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_641a923cbe5bbc48/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_6492e1e5d38d23ae` | [AR hold](hold_verified_autonomous_research/paper_6492e1e5d38d23ae/evaluation/verified_computation_reference.md) / [PR hold](hold_verified_paper_reproduction/paper_6492e1e5d38d23ae/evaluation/verified_computation_reference.md) | 已移至 hold：termination / 数值容差；符号已修 |
| `paper_6943bfe5eeaa42b8` | [PR](final_verified_paper_reproduction/paper_6943bfe5eeaa42b8/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_6e09640463562644` | [AR](final_verified_autonomous_research/paper_6e09640463562644/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_6e09640463562644/evaluation/verified_computation_reference.md) | 九候选能量类型分开；谱学证据与有限覆盖 |
| `paper_72f60526b64ce1b6` | [AR](final_verified_autonomous_research/paper_72f60526b64ce1b6/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_72f60526b64ce1b6/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_84efbea3ab8e6e20` | [AR](final_verified_autonomous_research/paper_84efbea3ab8e6e20/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_84efbea3ab8e6e20/evaluation/verified_computation_reference.md) | 限定：可支持有证据的 alternative，不声称原 HLCT 已复现 |
| `paper_86a0b654270a8ce7` | [AR](final_verified_autonomous_research/paper_86a0b654270a8ce7/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_86a0b654270a8ce7/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_8b7bf002cc6a4ba9` | [AR hold](hold_verified_autonomous_research/paper_8b7bf002cc6a4ba9/evaluation/verified_computation_reference.md) / [PR hold](hold_verified_paper_reproduction/paper_8b7bf002cc6a4ba9/evaluation/verified_computation_reference.md) | 已移至 hold：显式水前驱失效、主能量/偶极定义未定 |
| `paper_94b0a8ae694590ea` | [AR](final_verified_autonomous_research/paper_94b0a8ae694590ea/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_94b0a8ae694590ea/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_94e7481ded3b6a75` | [AR](final_verified_autonomous_research/paper_94e7481ded3b6a75/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_94e7481ded3b6a75/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_988bc12ae3768679` | [AR](final_verified_autonomous_research/paper_988bc12ae3768679/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_988bc12ae3768679/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_98b6f8a0352f72c2` | [AR](final_verified_autonomous_research/paper_98b6f8a0352f72c2/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_98b6f8a0352f72c2/evaluation/verified_computation_reference.md) | 有效四步链保留；取消调度记录移出主链 |
| `paper_9a58a1fa6ed7d780` | [AR](final_verified_autonomous_research/paper_9a58a1fa6ed7d780/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_9a58a1fa6ed7d780/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_9aa6d5655edfeb52` | [AR](final_verified_autonomous_research/paper_9aa6d5655edfeb52/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_9aa6d5655edfeb52/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_9d091f4337662e78` | [AR](final_verified_autonomous_research/paper_9d091f4337662e78/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_9d091f4337662e78/evaluation/verified_computation_reference.md) | D6 已落实；终态身份与去重；不要求 starter replay |
| `paper_9ec8c4761c4f171b` | [AR](final_verified_autonomous_research/paper_9ec8c4761c4f171b/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_9ec8c4761c4f171b/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_9f4c259696ad2f87` | [AR](final_verified_autonomous_research/paper_9f4c259696ad2f87/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_9f4c259696ad2f87/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_a6e8c57709329bdb` | [AR](final_verified_autonomous_research/paper_a6e8c57709329bdb/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_a6e8c57709329bdb/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_b1467cd61ca8022d` | [AR](final_verified_autonomous_research/paper_b1467cd61ca8022d/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_b1467cd61ca8022d/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_b276b18215cba283` | [AR](final_verified_autonomous_research/paper_b276b18215cba283/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_b276b18215cba283/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_b5c446c7067dd511` | [AR](final_verified_autonomous_research/paper_b5c446c7067dd511/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_b5c446c7067dd511/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_b815e2622b0d6085` | [AR hold](hold_verified_autonomous_research/paper_b815e2622b0d6085/evaluation/verified_computation_reference.md) / [PR hold](hold_verified_paper_reproduction/paper_b815e2622b0d6085/evaluation/verified_computation_reference.md) | 已移至 hold：framework 第二网格身份/稳定性证据 |
| `paper_c625cba3ce868eb1` | [AR](final_verified_autonomous_research/paper_c625cba3ce868eb1/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_c625cba3ce868eb1/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_d3b4575397179146` | [AR](final_verified_autonomous_research/paper_d3b4575397179146/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_d3b4575397179146/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_d91572979a89303a` | [AR](final_verified_autonomous_research/paper_d91572979a89303a/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_d91572979a89303a/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_db6c4e0558113873` | [AR](final_verified_autonomous_research/paper_db6c4e0558113873/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_db6c4e0558113873/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_e2d9397dff2a3f0f` | [AR](final_verified_autonomous_research/paper_e2d9397dff2a3f0f/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_e2d9397dff2a3f0f/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_eda19e7c8edd4b39` | [AR](final_verified_autonomous_research/paper_eda19e7c8edd4b39/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_eda19e7c8edd4b39/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_f9d09d28c7d9adaa` | [AR](final_verified_autonomous_research/paper_f9d09d28c7d9adaa/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_f9d09d28c7d9adaa/evaluation/verified_computation_reference.md) | CF3 optional；保留扭转和轨道必评 |
| `paper_fcc3c7f2c46a0fbe` | [AR](final_verified_autonomous_research/paper_fcc3c7f2c46a0fbe/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_fcc3c7f2c46a0fbe/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
| `paper_fda8b9b53f8276db` | [AR](final_verified_autonomous_research/paper_fda8b9b53f8276db/evaluation/verified_computation_reference.md) / [PR](final_verified_paper_reproduction/paper_fda8b9b53f8276db/evaluation/verified_computation_reference.md) | 沿用既有逐篇审计及已声明范围；本轮无科学改动 |
