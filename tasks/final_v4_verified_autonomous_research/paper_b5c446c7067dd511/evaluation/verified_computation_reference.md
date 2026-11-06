# Second audit — native job segments

Second audit, direct native log check: An-mP main optimization completed with all four YES (maximum/RMS forces 0.000003/0.000001; maximum/RMS displacements 0.001223/0.000248). The later frequency-related segment prints negligible-force completion and displacement NO (0.100183/0.008294); it is not evidence that the main optimization failed. The linked parent has 210 positive modes, minimum 7.4015 cm^-1. Na main optimization instead genuinely uses negligible-force completion (maximum displacement 0.001832 versus 0.001800). T_edge equals Ph/Na T4 and An/Py T3 in both source Table S1 and existing native responses; universal cross-method state correspondence and numeric-window fairness remain unresolved.

# V3 scope and evidence reuse — 2026-10-28

Same four full emitters and molecular electronic relaxation/substituent question. Final spectroscopic quantities, state character and molecular inferences are explicit; source targets/windows unchanged and no new kinetic or device scope.

All 12 final vertical energies and four oscillator strengths reuse the four baselines in NATIVE_READBACK.json; unchanged ±0.05 eV and ±0.03 dimensionless windows apply. Maximum relevant energy deviation is0.0186 eV; actual f=0.8089/0.7133/0.2203/0.6775. The eight state-character outcomes reuse the corresponding native IFCT and full-response records; Na-T4 CT=9.522% versus source22.25% remains a substantive unresolved quantitative discrepancy, not a tolerated percentage target. Four molecule-specific route inferences reuse the matched energy gaps plus spatial evidence; proximity is supporting evidence only. The cross-molecule outcome concerns nonmonotonic substitution, not duplicated state labels. Exact CT/NTO percentages, all80 roots, cross-functional near-degeneracy and real RISC/device rates remain unverified; no new calculations or V3 whole-case PASS.

Final rules: r_Ph_S1_energy, r_Ph_T1_energy, r_Ph_T4_energy, r_Ph_S1_strength, r_Ph_S1_mixed, r_Ph_T4_character, r_Ph_high_triplet_electronic_route, r_Na_S1_energy, r_Na_T1_energy, r_Na_T4_energy, r_Na_S1_strength, r_Na_S1_mixed, r_Na_T4_character, r_Na_high_triplet_electronic_route, r_An_S1_energy, r_An_T1_energy, r_An_T3_energy, r_An_S1_strength, r_An_S1_mixed, r_An_T3_character, r_An_high_triplet_electronic_route, r_Py_S1_energy, r_Py_T1_energy, r_Py_T3_energy, r_Py_S1_strength, r_Py_S1_mixed, r_Py_T3_character, r_Py_high_triplet_electronic_route, r_substituent_spatial_explanation.

The following text is unchanged historical verification, including its old policy/status wording. It is not a declaration of a new V3 PASS. No new calculations were performed.

State correspondence correction: For the isolated-molecule comparison at a common neutral S0 equilibrium geometry, use S1 and T1 for the lowest singlet and triplet excitations. Define T_edge as the upper boundary of the triplet manifold below S1: the highest-energy triplet below S1, excluding T1. Establish that boundary from the neighboring response states, without assuming a root index or a local/charge-transfer assignment. If no such state exists, or state crossing changes its identity, report that result explicitly. This is a spectroscopic comparison state; its definition does not establish a relaxation pathway. When comparing geometries or methods, distinguish a change of energy ordering from physical state correspondence using transition-density/NTO or equivalent response evidence. Do not replace a tracked state with a different state just because its energy is closer.

Expert attention: the neutral T_edge definition selects the original Ph/Na T4 and An/Py T3 at the source baseline (SI Table S1), but a different model can change that ordering or mix/cross states. Existing evidence does not provide a universal cross-method state correspondence. Never apply a reference window or character target to an unrelated proposed route state, nor silently rematch by root number or nearest target energy. Numeric leaves remain binary with unchanged windows; an unestablished match has no numeric pass, and a demonstrated change of T_edge identity is a reference-applicability issue to record for expert review, not proof that the alternative physical result is wrong. Semantic pathway findings are assessed independently. No claim that AR cross-method fairness or this state-selection ambiguity is fully resolved.

---

# V2 验证计算参考：HLCT four-emitter molecular electronic evidence

论文：`paper_b5c446c7067dd511`；模式：`autonomous_research`；发布整理：2026-10-17。

**验收：当前冻结 V2 完整任务范围内独立严格通过。** 不依赖用户接受数值偏差；不代表论文全文或补充材料全部数值均已复现。

本文件仅供私有 evaluator / 维护者使用，不得放入被测 agent 的公开输入。

## 发布与验收绑定

- 科学题面、公开输入、关键点、结论、评分及容差逐文件从已复审的 `upgrade_version2` 复制，评分策略保持 `dual_axis_100.scientific_results.v1`。
- 历史开发快照和计算缓存未复制进发布包，原件仍在源目录与 docs 中。
- [独立验收裁定](../../../../docs/strict_author_route_validation_20261001/supervised_continue_20261011T0932Z/COORDINATOR_REVIEW/paper_b5c446c7067dd511_20261015T2030Z/DECISION.json)；[原始复审全文](../../../../docs/strict_author_route_validation_20261001/supervised_continue_20261011T0932Z/COORDINATOR_REVIEW/paper_b5c446c7067dd511_20261015T2030Z/REVIEW.md)；[原生证据解析](../../../../docs/strict_author_route_validation_20261001/supervised_continue_20261011T0932Z/COORDINATOR_REVIEW/paper_b5c446c7067dd511_20261015T2030Z/NATIVE_READBACK.json)。
- [本包证据和资源索引](verification_evidence_index.json)记录原生文件路径、哈希、处理器、内存和程序打印时长。

## 计算过程及结果对照

以下为独立复审报告原文。报告中“未导出”指独立裁定当时的历史状态；本次已根据用户授权复制至 V2 发布目录。没有重新计算或修改原裁定。

# HLCT 四分子任务：主协调独立复审

论文：`paper_b5c446c7067dd511`，*Study on optical properties of phenanthroimidazole-based HLCT emitters with extended conjugation*。本次事件：`COORDINATOR_cbcf6eff352204e1.json`。日期：2026-10-15 UTC。

**裁决：PASS_STRICT_CURRENT_FROZEN_V2_TASK。** 这是一项针对现行 AR、PR 两种任务全部必要节点的独立裁决。允许验收的结果是：作者气相 B3LYP 模型下，四个分子的 S1 与指定高三重态在能量上接近，而 S1 与 T1 相隔明显更远；八个相关态的空间分布支持四个 S1 的混合特征，并重现 Na-T4 比 Ph-T4、An-T3、Py-T3 更局域的取代效应。现有证据也能够明确指出这些结果不能确定真实 RISC 速率或通道的动力学主导地位。

**精确 CT/NTO 百分比、完整 SI 激发态表以及高效 RISC/器件效率没有因此验收。** 特别是 Na-T4 的 CT 数字明显不一致，本报告没有把该差异认定为合理的数值误差。其不阻断本次验收的理由是下述冻结任务所要求的物理区分已被多项实际结果验证，且上述精确比例和细微排序并非独立的必要验收靶。不能把本裁决引用成“所有作者数字均已重现”。

## 1. 验收对象在计算结果之外预先固定

验收绑定 `tasks/upgrade_tasks/upgrade_version2/{autonomous_research,paper_reproduction}/paper_b5c446c7067dd511`，不是外层较早的固定矩阵设计，也不是发布目录。48 个任务、输入及评估文件的 hash 与候选提交时一致，见 `CONTRACT_CHECK.json`。正文、SI、候选、中央状态及关键任务文件另存于 `before/`；索引见 `FROZEN_INPUTS.json`。

两模式的科学问题均为：四个给定发光分子的分子电子证据支持哪些激发态弛豫通道，芳香取代如何影响这个判断。PR 另外要求执行或有据替代作者气相 TD-B3LYP/6-31G(d,p)、NTO/IFCT 基线；AR 不向被测 agent 提供作者答案。私有验证材料不应作为 AR 输入。

2026-09-28 的现行版本已经明确：根数按科学结论选择；不强制旧的 SOC/45°/固定控制矩阵；允许有充分证据的机制界定；近能量或混合标签不能证明速率。这些规定早于本次候选，并非为迁就此次残差新增。此次没有更改科学问题、评分、参考值或容差。

本次没有仅凭“允许负答案”放行：需要实际重现的能量层级与空间分布区分有正面证据，所有四个分子都被覆盖；动力学不可识别性只是这些证据能够支持的边界。

## 2. 主协调亲自检查的来源与原生证据

- 直接重新读取主文第 2、3、4、10 页；查看第 4 页 Fig.3 的 NTO 空间分布、状态标号和构象示意；读取 SI 第 2–7 页，尤其 S6 的 Table S1、S7 的 Table S2。页面摘录在 `SOURCE_EXCERPTS.txt`，图像在 `main_p4.png`、`supplementary_001_p3.png`。
- 独立解析四份匹配父结构的 Gaussian Opt/Freq 日志和八份 singlet/triplet TD 日志。没有用正常退出码代替频率、电子数、物理态和几何核查。脚本 `read_native.py` 与输出 `NATIVE_READBACK.json` 可复查。
- 独立读取十份相关官方 Multiwfn IFCT 日志，包括 Na 的 Mulliken/Hirshfeld 两种布居，核查实际 CT、LE、片段贡献及负贡献警告。
- 独立读取八份完整 X/Y 数组，保持原 1e-6 RPA 范数门；再与原 Gaussian 日志中的 29,009 个已打印系数逐项核对，最大误差约 5e-6，与原日志五位小数精度相符。结果在 `FULL_RESPONSE_NORMS.json`。这验证已保存数组与实际响应的联系，不把导出归一化当作来源证明。
- 核对已存 same-state 分析、原始 fchk 文件 hash、原计算/后处理实现及附加模型控制。保留源数据不可恢复的部分；没有声称取回了作者私有波函数或逐坐标完全相同的优化端点。

## 3. 原生有效性与作者路线

| 分子 | 原子/电子数 | 正频率数 | 最低频率 cm⁻¹ | 原 Opt 的终止依据 |
|---|---:|---:|---:|---|
| Ph-mP | 60 / 242 | 174 | 18.7995 | 四项标准全部 YES |
| Na-mP | 66 / 268 | 192 | 11.9426 | Gaussian negligible forces；最大位移 0.001829 略高于 0.001800 |
| An-mP | 72 / 294 | 210 | 7.4015 | Gaussian negligible forces；最大位移 0.100183、RMS 位移 0.008294 保留为例外 |
| Py-mP | 74 / 306 | 216 | 8.7695 | 四项标准全部 YES |

所有对象均为中性闭壳层 S0 参考；triplet 是该参考上的 TD triplet 响应，不能误标成以三重态基态几何计算。四个父 Hessian 均为 3N−6 个正模。An 的最大/RMS 力为 0.000003/0.000001，程序据可忽略的力接受端点；没有宣称其位移门全部通过。频率阶段的后续预测位移不代替原 Opt 终止判据。

本次特别更正 An 的证据血缘：与 TD 对应的是 memory1g 父的 7.4015 cm⁻¹，不是另一父的 7.3798。Py 也核对了实际 memory1g 父。独立比较父与 TD 的原子顺序及全距离矩阵，Ph 最大差约 1e-6 Å，其余三者为原日志精度下的 0；未借用其他构象的频率。

作者披露的是气相 B3LYP/6-31G(d,p) 优化和 TD，加三片段 Multiwfn 分析，当前实现遵循该物理模型。Gaussian16 C.01 替代 Gaussian09W 符合用户允许的软件版本例外。公开资料没有唯一披露优化坐标、全部积分默认值、Multiwfn 版本及响应导出约定。现有较细网格、Na 的 G09Defaults/FineGrid 控制属于已执行的数值检查；不能由版本不同推断所有差异均由版本造成。适用等价性是本任务所需的能量层级和局域/混合区分，不是所有高根或精确布居比例的等价性。

## 4. 必要能量结果与合理误差的判定

Tn 依据作者先验选择：Ph/Na 为 T4，An/Py 为 T3；没有事后选择更接近论文的根。单位均为 eV。

| 分子 | 实算 S1 / T1 / Tn | 论文 S1 / T1 / Tn | 实算 / 论文 S1−T1 | 实算 / 论文 S1−Tn |
|---|---|---|---|---|
| Ph | 3.5185 / 2.6345 / 3.4249 | 3.518 / 2.635 / 3.424 | 0.8840 / 0.883 | 0.0936 / 0.094 |
| Na | 3.4524 / 2.5661 / 3.3367 | 3.463 / 2.572 / 3.336 | 0.8863 / 0.891 | 0.1157 / 0.127 |
| An | 3.1095 / 1.7610 / 3.0753 | 3.104 / 1.761 / 3.083 | 1.3485 / 1.343 | 0.0342 / 0.021 |
| Py | 3.1274 / 2.0370 / 3.0153 | 3.146 / 2.041 / 3.027 | 1.0904 / 1.105 | 0.1121 / 0.119 |

12 个相关端点最大绝对差为 0.0186 eV，两个必要能隙的最大差分别为 0.0146、0.0132 eV。这里判断误差适用性的依据是实际结论的尺度：所有指定 Tn−S1 接近程度均远小于 T1−S1 间隔，排序未逆转；每个分子两类间隔之间还有至少约 0.77 eV 的区分。上述残差足以支持这一能量层级区别，不能支持 An 的精确热激活概率或 RISC 速率，也不意味着以后所有量都可采用 0.02 eV 统一容差。

四个实算 S1 振子强度为 0.8089、0.7133、0.2203、0.6775；Fig.3 的对应标注为约 0.80、0.71、0.23、0.69。光学允许性及 An 较弱的区别保持。振子强度不是 ISC/RISC 耦合。

全部 80 根已经计算，完整源表并未复现。例如新 Na S10=4.4673，而 SI 为 4.146 eV。该项不能被本裁决作为准确参考；冻结任务不要求逐根全表匹配。

## 5. CT/NTO 残差为何必须保留，及其对必要结论的影响

| 态 | SI CT % | 官方 Mulliken CT % | 完整未筛选 CT % | 独立布居对照 CT % |
|---|---:|---:|---:|---:|
| Ph S1 | 59.10 | 56.745 | 56.7992 | 56.7268 |
| Na S1 | 66.49 | 62.474 | 62.3892 | 62.6230 |
| An S1 | 37.73 | 39.467 | 39.2318 | 39.2742 |
| Py S1 | 54.23 | 60.208 | 60.0063 | 60.0272 |
| Ph T4 | 47.58 | 48.385 | 48.6851 | 48.7492 |
| Na T4 | 22.25 | 9.522 | 9.7273 | 11.0300 |
| An T3 | 50.99 | 46.645 | 47.0798 | 47.0102 |
| Py T3 | 44.41 | 42.409 | 43.4167 | 43.3463 |

独立布居对照中 Na 为 Hirshfeld，其他为完整 Lowdin；它们不能混称同定义百分比。NTO raw 本征值和按 sumX² 归一化权重也始终分开。

**Na-T4 的 −12.728 个百分点不是小误差，也未找到能够唯一解释它的作者输入。** 源 NTO 权重 80.94% 与实算 raw 91.2065%、归一化 90.6297% 也未一致。不将这些残差归咎于版本、四舍五入、1e-4 导出尾项或已证明的作者笔误。源百分比为参考观察，不能成为本次认可的数值靶或容差。

但任务所需的三项空间区别有独立的、定量的保真证据：

1. 四个 S1 均有显著局域与跨片段分量；An-S1 的局域占比更大，其他三者的 CT 占比更大。该区别同时出现在源值、完整响应及替代布居中。
2. Na-T4 的 CT 比其他三个指定 Tn 明显低：源中低至少 22.16 个百分点；本次不同已测表示中，Na 最大 11.030%，其他态最小 42.409%。同时 Na 完整 hole/electron 在核心的贡献为约 92.69/97.35%，Hirshfeld 为 91.66/96.99%。这既有组间分离，也有实际空间分布证据，与 Fig.3 的 Na-T4 核心局域图及正文解释相符。
3. 芳环增加没有产生简单单调的 CT 趋势。源与当前数值均如此。Ph 与 Py 的精细先后次序、An-T3 是否稍微 CT 多数则不稳健，不作为已验证结论。没有通过事后重排分子或选指标掩盖这些变化。

冻结 KP 接受有据的态性质判据，并未要求固定百分比或作者全表。因此，必要的定量能量区分和空间态区分可成立，同时具体 CT/NTO 数值仍未复现。这是本次判定可以通过完整冻结任务、但不能验证精确百分比的依据。

另一个实际数据问题：旧 Py-T3 官方日志给出 CT/LE=42.409/57.624，和为 100.033。日志明确警告将负片段电子贡献截成零，旧 `normalization_deviation=0` 汇总不正确。完整响应 43.416734/56.583266 及 Lowdin 43.346283/56.653717 闭合；它们用于该态的规范化解释，原异常日志保留。源主文 Py-S1=57.23/45.77、An-T3=50.09/49.01 也不闭合；SI 的 54.23/45.77、50.99/49.01 单独列出，不暗改正文。

IFCT 实现疑点已核查：用原生日志的片段 hole/electron 贡献重构乘积矩阵，非对角和及对角和能复现打印 CT/LE，最大差约 0.0104 个百分点，来自片段贡献仅打印两位小数。没有发现 worker 使用了与这些实际 Multiwfn 输出不符的乘积公式。原响应数组、筛选导出、默认 0.1 截断日志则是不同表示，不能因为后者较接近源就择优替换。

## 6. 逐必要节点独立裁定

| 冻结节点 | 独立裁定 | 验收依据和保留边界 |
|---|---|---|
| kp_scope | 通过 | 四对象、原子/电子/电荷与三片段有据；实际父与响应几何相连；八个态的完整响应与原日志系数一致；物理态、气相、B3LYP及指标定义明确。源精确端点未知不是假称坐标相同的理由。 |
| kp_measure | 通过 | 80 根实际输出及必要 12 端点直接回读；能隙尺度与论文一致，四个 S1 的光学允许性有原生振子强度；完整 IFCT/空间分布提供定量态图景。未认可未复现的高根表及精确 CT/NTO 数值。 |
| kp_explain | 通过 | 能量接近性、光学跃迁、三片段分布、NTO及 Na 局域例外联合区分分子解释。没有由近能量直接推出速率。已有 5D 模型 SOC 只能说明该附加模型中存在有限耦合。 |
| kp_robust | 通过 | 原始 RPA、导出截断、布居归一化、负值处理及替代布居的影响有已执行证据；组间区别保持，细微 CT 排序不保持。CAM 同态对照否定跨泛函普遍近简并的说法，明确模型适用边界。 |
| con_answer | 通过 | 四分子的作者模型电子候选通道与取代依赖得到验证：高 Tn 相对 T1 在垂直能量上更接近 S1，Na-T4 更核心局域，其余三个 Tn 更混合。不能确定实际 RISC 竞争胜出、速率或器件表现。完整回答了当前分子电子证据问题。 |
| PR 额外过程要求 | 通过，带明示偏离记录 | 披露的气相 B3LYP/6-31G(d,p) 优化/TD 和三片段 NTO/IFCT 已执行；当前软件版本已授权；用已算结果证明必要物理区别适用，而不是声称私有原始文件或所有默认参数完全相同。 |

附加控制必须准确使用：ORCA 5D 模型的 SOC 约 0.18/0.11/0.24/0.15 cm⁻¹，不能当成作者 Gaussian6D 的耦合。Ph/An 同 5D 的跨实现能量差不超过 0.0006 eV、重叠大于 0.9998，只验证所测条件。Ph/An 同态 CAM 间隔增至约 0.589/0.461 eV，不能宣称作者近简并跨泛函稳健；An45 的同根号也不能冒充同态对应。

## 7. 后继、登记与发布边界

本次没有可据此定义的必要遗漏计算，也没有为重复取得已成功结果再投 HPC。精确源百分比若未来成为新任务硬靶，需要先获取作者实际几何/响应导出及布居协议，或者提出可判别这些原因的新证据；盲目增加泛函、构象或重投同计算不会自动解决该问题。

中央验收和逐篇状态记录本次独立结果。原 worker 候选交付保持原样作为历史证据；本报告及 `DECISION.json` 是协调裁决。当前发布目录和 ZIP 均不自动修改；本篇登记为已严格验收、尚未导出。

监督回执有一项状态机修复：允许以 hash 认证的协调回执关闭 `START_CONFIRMED` 等已派发状态，保持幂等，且不赋予科学 PASS。定向核查结果见 `SUPERVISOR_ACK_CHECK.json`。使用现有同一监督目录和锁完成受控重载；不并行启动第二个监督器，也不打断 HPC 或验证会话。最终健康和回执消费记录另存本目录。


## 原生计算时长与资源

每条时长均照录原日志中的阶段记录；CPU time 与 wall/Elapsed time 不混用。缺失字段标为未记录，不推测总耗时，也不把多作业 CPU 时长当日历时长。完整索引另见 verification_evidence_index.json。

| 原生文件 | 日志处理器/内存设置 | 原生日志时长 |
|---|---|---|
| [docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Ph_mP_b3lyp_631gdp_opt_freq_hpc20_p3_p3_auto_retry3_p3/stdout.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Ph_mP_b3lyp_631gdp_opt_freq_hpc20_p3_p3_auto_retry3_p3/stdout.log) | CPU=20; mem=100GB | Job cpu time:       0 days  2 hours 45 minutes  8.4 seconds.<br>Elapsed time:       0 days  0 hours  8 minutes 22.8 seconds.<br>Job cpu time:       0 days  3 hours 28 minutes 51.9 seconds.<br>Elapsed time:       0 days  0 hours 10 minutes 32.1 seconds. |
| [docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Ph_mP_b3lyp_631gdp_opt_freq_hpc20_p3_td10/stdout.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Ph_mP_b3lyp_631gdp_opt_freq_hpc20_p3_td10/stdout.log) | CPU=8; mem=64000MB | Job cpu time:       0 days  2 hours 56 minutes 26.5 seconds.<br>Elapsed time:       0 days  2 hours 14 minutes 18.0 seconds. |
| [docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Ph_mP_b3lyp_631gdp_opt_freq_hpc20_p3_triplet_td10/stdout.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Ph_mP_b3lyp_631gdp_opt_freq_hpc20_p3_triplet_td10/stdout.log) | CPU=8; mem=64000MB | Job cpu time:       0 days  2 hours 26 minutes 55.4 seconds.<br>Elapsed time:       0 days  1 hours 48 minutes 35.3 seconds. |
| [docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/optfreq/stdout.log](../../../../docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/optfreq/stdout.log) | CPU=20; mem=80GB | Job cpu time:       0 days  3 hours 16 minutes 17.6 seconds.<br>Elapsed time:       0 days  0 hours  9 minutes 51.7 seconds.<br>Job cpu time:       0 days  3 hours 21 minutes 49.3 seconds.<br>Elapsed time:       0 days  0 hours 10 minutes  8.1 seconds. |
| [docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/singlet/stdout.log](../../../../docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/singlet/stdout.log) | CPU=20; mem=80GB | Job cpu time:       0 days  2 hours 10 minutes 27.5 seconds.<br>Elapsed time:       0 days  0 hours  6 minutes 35.9 seconds. |
| [docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/triplet/stdout.log](../../../../docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/triplet/stdout.log) | CPU=20; mem=80GB | Job cpu time:       0 days  2 hours 14 minutes 56.3 seconds.<br>Elapsed time:       0 days  0 hours  6 minutes 53.0 seconds. |
| [docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/An_mP_b3lyp_memory1g_p3_r1_auto_retry1_p3/stdout.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/An_mP_b3lyp_memory1g_p3_r1_auto_retry1_p3/stdout.log) | CPU=20; mem=100GB | Job cpu time:       0 days 12 hours 20 minutes 12.6 seconds.<br>Elapsed time:       0 days  0 hours 37 minutes 37.7 seconds.<br>Job cpu time:       0 days  5 hours 38 minutes 24.1 seconds.<br>Elapsed time:       0 days  0 hours 17 minutes  3.3 seconds. |
| [docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/An_mP_b3lyp_631gdp_opt_freq_hpc20_p3_td10/stdout.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/An_mP_b3lyp_631gdp_opt_freq_hpc20_p3_td10/stdout.log) | CPU=8; mem=64000MB | Job cpu time:       0 days  4 hours  9 minutes 20.3 seconds.<br>Elapsed time:       0 days  4 hours 17 minutes 20.6 seconds. |
| [docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/An_mP_b3lyp_631gdp_opt_freq_hpc20_p3_triplet_td10/stdout.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/An_mP_b3lyp_631gdp_opt_freq_hpc20_p3_triplet_td10/stdout.log) | CPU=8; mem=64000MB | Job cpu time:       0 days  3 hours 38 minutes 16.1 seconds.<br>Elapsed time:       0 days  3 hours 34 minutes 25.7 seconds. |
| [docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Py_mP_b3lyp_memory1g_p3_r1_auto_retry1_p3/stdout.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Py_mP_b3lyp_memory1g_p3_r1_auto_retry1_p3/stdout.log) | CPU=20; mem=100GB | Job cpu time:       0 days  7 hours 33 minutes 21.8 seconds.<br>Elapsed time:       0 days  0 hours 23 minutes  3.4 seconds.<br>Job cpu time:       0 days  5 hours 49 minutes 36.2 seconds.<br>Elapsed time:       0 days  0 hours 17 minutes 37.0 seconds. |
| [docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Py_mP_b3lyp_631gdp_opt_freq_hpc20_p3_td10/stdout.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Py_mP_b3lyp_631gdp_opt_freq_hpc20_p3_td10/stdout.log) | CPU=8; mem=64000MB | Job cpu time:       0 days  2 hours 42 minutes 10.1 seconds.<br>Elapsed time:       0 days  2 hours 24 minutes 12.9 seconds. |
| [docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Py_mP_b3lyp_631gdp_opt_freq_hpc20_p3_triplet_td10/stdout.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/artifacts/gaussian/Py_mP_b3lyp_631gdp_opt_freq_hpc20_p3_triplet_td10/stdout.log) | CPU=8; mem=64000MB | Job cpu time:       0 days  5 hours 39 minutes 22.8 seconds.<br>Elapsed time:       0 days  5 hours 48 minutes 23.8 seconds. |
| [docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/Ph_S1/multiwfn.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/Ph_S1/multiwfn.log) | CPU=未记录; mem=未记录 | 原日志未记录 |
| [docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/Ph_T4/multiwfn.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/Ph_T4/multiwfn.log) | CPU=未记录; mem=未记录 | 原日志未记录 |
| [docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/An_S1/multiwfn.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/An_S1/multiwfn.log) | CPU=未记录; mem=未记录 | 原日志未记录 |
| [docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/An_T3/multiwfn.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/An_T3/multiwfn.log) | CPU=未记录; mem=未记录 | 原日志未记录 |
| [docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/Py_S1/multiwfn.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/Py_S1/multiwfn.log) | CPU=未记录; mem=未记录 | 原日志未记录 |
| [docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/Py_T3/multiwfn.log](../../../../docs/verification/group_3/paper_b5c446c7067dd511/provenance/priority_repair_20260918/official_multiwfn/Py_T3/multiwfn.log) | CPU=未记录; mem=未记录 | 原日志未记录 |
| [docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/analysis/Na_S1/IFCT_Mulliken_GENERAL/multiwfn.log](../../../../docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/analysis/Na_S1/IFCT_Mulliken_GENERAL/multiwfn.log) | CPU=未记录; mem=未记录 | 原日志未记录 |
| [docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/analysis/Na_S1/IFCT_Hirshfeld_GENERAL/multiwfn.log](../../../../docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/analysis/Na_S1/IFCT_Hirshfeld_GENERAL/multiwfn.log) | CPU=未记录; mem=未记录 | 原日志未记录 |
| [docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/analysis/Na_T4/IFCT_Mulliken_GENERAL/multiwfn.log](../../../../docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/analysis/Na_T4/IFCT_Mulliken_GENERAL/multiwfn.log) | CPU=未记录; mem=未记录 | 原日志未记录 |
| [docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/analysis/Na_T4/IFCT_Hirshfeld_GENERAL/multiwfn.log](../../../../docs/strict_author_route_validation_20261001/align_current_library_20261012T0330Z/papers/paper_b5c446c7067dd511/cases/na_g09defaults_remaining_defaults_20261012_a01/output/analysis/Na_T4/IFCT_Hirshfeld_GENERAL/multiwfn.log) | CPU=未记录; mem=未记录 | 原日志未记录 |

## 2026-10-19 active paper_science_v2 scoring migration

The active private rubric assigns 100 points only to independent intermediate findings and final scientific conclusions, using binary leaves and no process score or multiplier. Historical criteria/weights above are archival, not active scoring. Public inputs and author-route contract remain byte-identical. Existing acceptance remains PASS_STRICT_CURRENT_FROZEN_SCOPE; this migration is not new chemical validation. Fixed windows and retained boundaries are in scoring_rules.json and reference_qualification.json.


## 2026-10-19 Round3 scoring-contract repair

Historical verification statements above are preserved verbatim. Current mode-specific scientific rules supersede earlier scoring-policy wording; this append does not change the chemistry acceptance class.

- Split independent molecule-specific electronic-route final10 into Ph3/Na3/An2/Py2; retained the genuinely relational four-molecule substitution conclusion10. Scientific conclusion total20 unchanged.
- Audited every existing leaf for scientific role, source/verification support and physical definitions; retained unproven narrow-window risks as explicit provisional calibration limits rather than inventing wider tolerances.
