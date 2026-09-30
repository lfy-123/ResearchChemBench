# Audited expanded computation reference — 2026-09-28

All artifact paths in the report below resolve relative to `docs/upgrade_tasks_verification/group_2/papers/paper_3e4cad1d1d650d0c/`. This is an author-informed reference audit, not a blind AR run or a remotely scored submission. Numerical values are evidence, not fixed acceptance targets. The score must continue to judge supported, refuted and indistinguishable outcomes symmetrically. Total electrochemical error is not calibrated.

# 芴阴离子光还原能力：第一版实际计算验收

## 范围、版本与结论

本报告为作者知情的参考计算验证，兼核 AR/PR 同一科学端点；不是一次盲测自主发现。当前包已在 `task_snapshot/phase1_takeover_20260928/` 按官方内容哈希冻结。所有原始计算和可执行分析在本论文目录内，`analysis/recompute.py` 从原生日志重算本报告结果。

结论是有边界的否定：HOMO 排序不足以解释完整光还原行为。统一 DMSO 氧化循环支持 1a 比 1e 具有更负的名义激发态氧化电位；其数值接近受体阈值，不能消除溶剂、电极、不可逆还原及近似方法的不确定性。强度明显淬灭而寿命近乎不变，反对把强度 Stern–Volmer 斜率解释为纯动态淬灭。静态预缔合与此相容，但尚非唯一解释；不推断 C–Cl 断裂速率或收率。

## 原文路线及新增计算

正文 PDF 第4页 Table1 提供吸收/发射交点 517、511 nm 和印刷 SCE 氧化电位；第5页提供 4-chloroanisole 及 Figure3 淬灭图。SI 第23页给 Ag/AgCl→SCE 的本文条件转换；正文参比文字不一致，不能将该转换通用于其他条件。SI 第57–58页计算部分采用 CAM-B3LYP/6-311G(d)、CPCM DMSO。作者阴离子轨道比较仅作为基线。

复用两个历史阴离子的完整 Gaussian16 C.01 优化/频率日志；新增中性双重态自由基优化/频率。这是源方法下新增的氧化循环。另对四个源几何真实执行 CAM-B3LYP/6-311+G(d)、CPCM DMSO、Stable=Opt 单点，检验弥散基组与电子稳定性；这是复合单点敏感性，不伪称更大基组重新优化/频率。熵处理比较 RRHO 与熵插值 qRRHO 50/100 cm⁻¹，两种转子惯量约定均留存。

## 原始端点与质量

| 端点 | E / Eh | 原生 G(RRHO,1 atm) / Eh | 最低频率 / cm⁻¹ | 原始证据 |
|---|---:|---:|---:|---|
| 1a 阴离子 | -731.699962923 | -731.482427 | 65.2426 | outputs/legacy_reused/1a_anion/stdout.log |
| 1a 自由基 | -731.569932260 | -731.351981 | 62.9116 | outputs/1a_radical_source_optfreq/attempt_002/stdout.log |
| 1e 阴离子 | -1068.773222930 | -1068.557595 | 11.2594 | outputs/legacy_reused/1e_anion/stdout.log |
| 1e 自由基 | -1068.637745400 | -1068.421789 | 14.2140 | outputs/1e_radical_source_optfreq/attempt_001/stdout.log |

四者均与映射图完整显式氢元素/邻接同构、电荷和多重度一致；输出中方法与介质正确，Hessian 模式数均为 3N−6，无虚频。此几何邻接检查不将距离推断冒充完整共振键级识别。所有原子映射和最终坐标见 `structures/`。

前三者 Tight 优化四项准则均 YES。1e 自由基由 Gaussian 的 negligible-forces 分支正常收敛，最大位移 0.000067 略高于 Tight 0.000060，其他准则通过，力接近打印零且完整 Hessian 正定。据力及正定 Hessian 接受为局部极小点，同时明确它不满足“四个打印准则全 YES”。不存在把一次 SCF 能或进程成功当极小点的判定。两个自由基 S² 湮灭前约 0.797，之后约 0.752，相对理想 0.75 的偏离留作方法限制；四个弥散单点通过所测试扰动下的波函数稳定性检查。

未执行穷尽构象搜索，不宣称全局最低点。源芴刚性骨架和源苯基构型经自由基优化，CF₃ 软模的影响用 qRRHO 检查。这里的任务要求四个最低点及敏感性，未把额外全系综工作暗作已完成。

## 重算公式与实际结果

对每个溶质以相同 RT ln(24.4654) 从原生 1 atm 热化学转为 1 M；`results.json` 报告转换后的 G，原生绝对值保留在审核记录。修正对每个氧化差及相对循环均抵消。1 Eh=27.211386245988 eV；n=1；固定 Eox(1a)=−0.61 V vs SCE，不拟合 1e。

ΔΔGox=[G(rad1e)−G(an1e)]−[G(rad1a)−G(an1a)]。
Eox(1e)=−0.61+ΔΔGox/e；E00=1239.841984/λ(nm)；Eox*=Eox−E00；ΔGET/e=Eox*−Ered，受体 Ered=−2.91 V vs SCE。

| 量 | 1a | 1e |
|---|---:|---:|
| Eox / V vs SCE | -0.610000 | -0.464147 |
| E00 / eV | 2.398147 | 2.426305 |
| Eox* / V vs SCE | -3.008147 | -2.890452 |
| ΔGET / eV | -0.098147 | +0.019548 |
| 源阴离子 HOMO / eV | -4.923356 | -5.071658 |

RRHO ΔΔGox=0.145853 eV，qRRHO50/100（分子平均惯量）为 0.145108/0.144332 eV；弥散单点+源热修正为 0.150802 eV。电子能差单独对照为 0.148217 eV，但不当作自由能。名义排序在这些有限对照下不变，不代表总误差小于 0.007 eV。

源 Table1 的 1e Eox 为 −0.32 V，而此模型给 −0.464147 V，残差 −0.144147 V。它远大于这些有限数值控制的漂移；我们既没有调整电极常数，也没有拿该残差定义一个迎合答案的接受区间。参比标签歧义、不可逆/解离型受体还原、连续溶剂及所选电子结构近似限制了绝对定量比较。1a 名义负驱动力和 1e 名义小正驱动力不能当成稳健平衡判决。

## 独立淬灭挑战

`analysis/redox_cycle_prechallenge_freeze.json` 固定于 2026-09-27 15:14:20 UTC，早于图像的定量检查。本文方法、原文数值及私有信息已知，不能把此顺序夸大为完整盲测。两种可证伪解释与其推翻条件已写入结果。

纯动态 Stern–Volmer 模型要求 I₀/I=τ₀/τ=1+K[Q]。K=86540 M⁻¹ 在 10 μM 预测寿命比 1.8654；Figure3 红色寿命标记在此域及至约49 μM 都接近1。原图纵轴标定为 ratio1 对应 y=289.5 px、ratio2 对应 y=42 px；5 px 包络给寿命比偏差 0.020202，转换为相对寿命偏差保守上界约0.02062，向上报告0.021。3/5/7 px敏感性均不改变纯动态反例。原始逐点寿命及仪器误差不可得，故 `lifetime_change_fraction=null`，这个上界仅是图像分辨率估计，不是置信区间或仪器精度。图像原件、标定与像素计数可重查。

静态暗缔合物或 sphere-of-action 模型可同时解释强度降低及剩余发光组分寿命不变；光学伪影或异质发光群体同样可能，需要额外独立观测才能唯一归因。这不影响对纯动态解释的当前反证。

## evaluator 逐项核查

`evaluator_mapping.json` 对 AR/PR 分别绑定当前哈希、全部5个 key point、6条评分规则、最终结论及8条 critical failure。身份、氧化循环、实测E00/统一受体、淬灭挑战及数值敏感性均有原始证据；所选结论不要求作者解释获胜。合成格式回归与本真实结果的格式/路径检查单独记录，绝不作为科学成功的替代。没有启动远程 LLM judge，语义审查是本次逐项人工式计算审查。

## 复用、成本与失败

两个阴离子原计算共 146135.285 秒作业时间，6核分配折合243.558809核时，均直接复用，未重新优化。该数是省去的原历史重算工作量，不预测今日HPC会花同样时间。

本轮7次平台尝试中有1次在 Gaussian 启动前因 `/usr/bin/time` 缺失失败，完整保留。成功6次实际Gaussian启动（两个opt/freq+四个稳定单点），累计应用墙钟4244.331秒，实测user+system CPU=22.153906核时，20核分配时间=23.579617核时。墙钟为并行作业时长之和，不是日历历时。峰值内存未测，报告null；80GB输入限额和100GiB预约不当成实际使用量。原失败/重试、平台ID、资源释放与日志哈希见 `analysis/resource_accounting.json` 和原attempt记录。

## 剩余范围

公开第一版核心矩阵已有实际证据；不需要也未完成全催化循环、所有收率、C–Cl势垒或动力学。科学完成为“有边界的模型比较与纯动态反证”，而不是所有假设均成立。最终发布处置还需当前第一阶段包版本/审核交接一致；不得用旧ready文件或旧PASS代替此报告。
