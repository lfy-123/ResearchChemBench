# 暂缓任务与按 group 分配的补充验证指令

更新：2026-09-15。本文及所链接的 evaluator、reference、计算证据均为维护者私有资料，不得作为被评估 agent 的输入。

补充状态（2026-09-20）：group_6 的 `paper_b815e2622b0d6085` 已完成第二网格补算的独立复核，并将有效证据同步到两份 HOLD 包的私有 reference 和 `evaluation/verification_supplement.json`。原态身份/稳定性缺口已关闭，当前范围无需再计算；科学目标、公开输入及评分容差未改。下述第 4 节保留原交接问题及计算边界，当前状态以两包新补充记录为准。本次验证修复没有将任务移回 final。

## 1. 本次迁移范围

用户已要求将明确暂缓的三篇论文移出 final。此次只迁移完整任务目录，**不改变任何任务正文、输入、科学对象、evaluator、容差或包内 reference**，不启动计算，不修改 `docs/verification`。

| paper_id | 历史验证组 | 自主科研任务 | 论文复现任务 | 剩余问题 |
|---|---|---|---|---|
| paper_6492e1e5d38d23ae | group_5 | [AR](hold_verified_autonomous_research/paper_6492e1e5d38d23ae) | [PR](hold_verified_paper_reproduction/paper_6492e1e5d38d23ae) | 表面模型/终止方式与定量评分边界；先核查，不直接下达重算 |
| paper_8b7bf002cc6a4ba9 | group_5 | [AR](hold_verified_autonomous_research/paper_8b7bf002cc6a4ba9) | [PR](hold_verified_paper_reproduction/paper_8b7bf002cc6a4ba9) | 显式水优化未收敛、终态身份错误，不能支撑优选构象与偶极的完整结论 |
| paper_b815e2622b0d6085 | group_6 | [AR](hold_verified_autonomous_research/paper_b815e2622b0d6085) | [PR](hold_verified_paper_reproduction/paper_b815e2622b0d6085) | 2026-09-20 验证修复完成：第二网格独立态身份/稳定性已支持，仍 HOLD 等待独立发布决定 |

迁移后 final 为 **53 篇、105 个任务：AR 52、PR 53**；hold 为 **3 篇、6 个任务：AR 3、PR 3**，合计仍为原来的 56 篇、111 个任务。`paper_84efbea3ab8e6e20` 两模式继续留在 final，发布时保留“支持有证据的替代解释，未复现作者特定 CZ2B/T4-HLCT 解释”的限定；本次不为它分配补算。

这些数字是目录状态，不是重新进行全量科学验证的声明。历史报告中的原 final 路径对上述三篇应定位到对应 hold 目录；包内相对论文/验证链接因目录深度未变而继续有效。源 `tasks/autonomous_research`、`tasks/paper_reproduction` 和历史验证档案未移动，**正式发布清单不得因此重新包含源目录中的这三篇**。

## 2. 所有接手 agent 必须遵守的边界

1. 这是**作者路线验证**，不是让验证 agent 扮演盲测被评估 agent。可以读取正文、SI、作者最终结构/TS及私有结果作为验证起点；不要求从当前 public starter 自主重新发现答案。同一条有效科学验证链可服务 AR、PR，不要为两个模式重复跑相同计算。
2. 科学对象、物理量定义和作者方法优先以正文/SI为依据；是否已经成功计算必须看真实应用输出、结构/态身份及对应数值，不能只看任务状态、包装器返回码或旧 PASS 标签。reference 只是索引和过程记录，不是替代 evaluator 的评分工具。
3. 先查已有有效证据，再对**仍缺失的最小环节**补算。不能通过改变目标、放宽容差、换质子化态、挑选更接近答案的模型、隐去失败对象或强行匹配编号来获得 PASS。遇到原文不足以确定且会影响科学结论的边界，先向用户说明并确认。
4. `docs/verification/group_5`、`group_6` 以及其他 `docs/verification` 文件保持只读，不覆盖历史文件。新计算建议使用独立私有目录 `runs/hold_verification/group_5/<paper_id>/<run_id>/` 或 `runs/hold_verification/group_6/<paper_id>/<run_id>/`，其中保留真实输入、完整输出、终态/波函数/后处理证据、运行记录和报告。不要把新证据放进任何 `agent_input`。
5. 每篇交付 `report/supplementary_verification.md` 和 `report/results.json`：列出原缺口、原有有效步骤、此次新增步骤、完整成功链、每个 evaluator 关键点对应的原始证据和结论，以及仍未解决的问题。失败/重试日志另存，不作为有效计算步骤；成功重试按实际有效输出记录。报告明确哪些条目是方法假设，哪些有论文依据。
6. 接手本指令不等于获准改任务或自动移回 final。先交付证据和逐项判定，经发布维护复核后再决定恢复。涉及 HPC 时先阅读**当时最新的 `qzcli-hpc` skill**，按用户授权和当前资源规则运行，不取消其他正在运行的作业。

## 3. 交给 group_5 agent 的指令

请在遵守第 2 节边界的前提下，分别处理以下两篇。可以顺序处理；两篇的模型决策和结果不能互相替代。

### 3.1 paper_6492e1e5d38d23ae：先确定模型/评分边界，再判断是否需要补算

**目标**：确定已有 TiO2 功函数计算在物理模型和物理量上是否对应当前任务；只在选定、可解释的模型确有计算缺口时补充对应计算。不要为了约 0.001 eV 的过线差距直接重跑整条流程。

**必读资料**：

- [正文](../papers/paper_6492e1e5d38d23ae/documents/main.pdf)，PDF pp.5–6，Fig.5/讨论。
- [SI 原文件](../docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/source_additions_20260915/1-s2.0-S1001841725006084-mmc1.docx)，TextS5。
- [历史结果](../docs/verification/group_5/paper_6492e1e5d38d23ae/report/results.json)、[终态计算对账](../docs/verification/group_5/paper_6492e1e5d38d23ae/provenance/endpoint_reconciliation_20260914.json)及其真实输入/输出。
- [AR reference](hold_verified_autonomous_research/paper_6492e1e5d38d23ae/evaluation/verified_computation_reference.md)、[PR reference](hold_verified_paper_reproduction/paper_6492e1e5d38d23ae/evaluation/verified_computation_reference.md)，以及两个 hold 包的 `agent_input/task.md`、`data/inputs/slab_protocol.json`、`evaluation/reference_key_points.json` 和 `scoring_rules.json`。

**已知事实，不要重复误判**：

- SI 指定 VASP/PBE、400 eV、力阈值 0.03 eV/Å；没有唯一披露 termination、层数、真空、k 网格。六层/18 Å 是公开 benchmark 约定，不是作者唯一模型。
- 现有主分支 W(anatase)=6.36999978845305 eV、W(rutile)=7.189349995247433 eV。按当前定义 W(rutile)−W(anatase)=+0.8193502067943825 eV；历史负号已经在当前任务/reference 解释中纠正。
- evaluator 两个功函数目标分别为 6.871、7.009 eV，容差均 ±0.5 eV。主锐钛矿结果低于下界 6.371 eV 约 0.00100021155 eV。另一个锐钛矿终止分支为 7.173123045896127 eV。
- 两模式的 key point 还写了差值接近 +0.138 eV，而 scoring rule 主要检查方向/符号，没有单独的差值数值容差。不能自行选宽松的一处宣布完全通过。

**执行步骤**：

1. 对照正文/SI、公开 bulk/POSCAR 与历史 POSCAR/CONTCAR，逐分支核对化学计量、晶面、两面终止、切割位置/暴露层、层数定义、晶胞与放松约束、势函数及真空/费米参考。区分作者原文、benchmark 约定和实现选择。
2. 在不以接近 gold 为选择标准的前提下，说明哪一物理构造最符合当前公开边界。若原文和公开约定仍允许影响结果的多个不等价分支，提交具体分支差异和建议，先请用户决定模型边界；不要事后挑更容易过线的分支。同步报告差值 key point 与 scoring rule 的粒度差异，评分修改需单独批准。
3. 对选定分支先复核已有真实放松和静态输出，从每侧真空平台及费米能重新提取 W，保留平台区间、左右差异、采样、收敛和单位。已有结果若覆盖该分支，不需重算。
4. **只有模型边界已确定且该分支证据缺失或确有数值疑点时**，补做相应放松/功函数静态或必要的单项数值敏感性；保持论文规定的方法及批准边界，不扩大到异相界面、掺杂或其他晶面。完整保存输入、实际收敛证据、可提取真空电势的输出和费米能来源。
5. 分别报告“计算收敛”“两个 W 的数值规则”“顺序”“差值幅度”“clean-facet 范围内的解释”是否支持。未通过的真实结果照实保留；不要用四舍五入、修改容差或无限调模型追逐目标。

**预期交付/退出条件**：优先给出模型对照表与逐评分项结果。若只是任务/评分口径需决策，明确标记，不把它转化为无边界补算。如果批准模型的有效既有或补充计算仍不满足现行定量要求，报告差距并继续 hold，不自动改答案。

### 3.2 paper_8b7bf002cc6a4ba9：补足有效显式水构象链，而非失败结构上的单点

**目标**：验证水中优选 AL/AB 构象及所选构象的分子偶极是否支持 evaluator。保留当前对象和目标，不能拿破碎、质子化态不同或仅文件名为 extended 的终态作为成功构象。

**必读资料**：

- [正文](../papers/paper_8b7bf002cc6a4ba9/documents/main.pdf)，PDF p.3 结论、p.10 “Theoretical Calculation”；[SI](../papers/paper_8b7bf002cc6a4ba9/documents/supplementary_001.pdf)，Fig.S5/S7。
- [现有逐结构/单点审计](../docs/verification/group_5/paper_8b7bf002cc6a4ba9/artifacts/alab_author_sp_audit_20260915.json)。该文件明确 `all_eight_single_points_complete=true` 但 `verification_passed=false`；其中链接到四份原始 xTB 输出和八个单点。
- [AR reference](hold_verified_autonomous_research/paper_8b7bf002cc6a4ba9/evaluation/verified_computation_reference.md)、[PR reference](hold_verified_paper_reproduction/paper_8b7bf002cc6a4ba9/evaluation/verified_computation_reference.md)，及两包任务、`molecular_system.json`、evaluator。

**已有可复用部分和实际缺口**：

- 四个 ORCA B3LYP-D4/def2-TZVP/CPCM(water) Opt/Freq 极小值有效，不是气相。其有效排序偏好 folded AL 和 folded AB；AB_extended 比 AB_folded 的电子能高约 7.9061 kcal/mol，未支持目标中的 extended AB 优选。
- 四个旧 xTB 显式水优化均明确未收敛。AL_extended 断键；另外三份为 NH2/COOH 而非当前任务的 NH3+/COO−。旧 AB_extended 的终态也不是伸展构象。
- 后续八个 ORCA SP 成功不修复上述前驱。作者能量定义为 `E(complex) − E(corresponding water network)`，不是整簇总能量。
- 旧偶极字段把 a.u. 标成 Debye；有效隐式水 AL_folded/AL_extended/AB_folded/AB_extended 的 Debye 为 14.620695228/21.369550129/14.886720073/26.981347392。50 水簇整体偶极不是分子偶极。

**执行步骤**：

1. 先核定正文/SI 对连通性、质子化态、能量和分子偶极的定义，与当前明确两性离子输入逐项对照。作者路线为 MMFF94/Avogadro → B3LYP-D4/def2-TZVP/CPCM(water) 优化 → Packmol 加 50 水 → GFN2-xTB 优化 → ORCA 单点。末段未单独重述最终单点全部参数，偶极取法也须明确；有影响科学结论的未披露选项，先报告方案并请用户确认，不能把实现假设写成论文事实。
2. 查是否另有**已经收敛、连通性/质子化态正确、终态构象可确认**的显式水候选及对应单点。找到则先复用。没有则复用已有效的前段结构或合法的作者私有起点，只补缺少的显式水构建/优化及后续步骤，不为 AR/PR 各跑一遍。
3. 对需要补充的候选，覆盖足以区分各分子 compact/open 的有效结构。SI 的三 AL/四 AB 构象可作私有验证参照，但不能擅自增加“公开任务必须恰好搜索七个”的要求。水分子数、构建/采样选择和候选去重需记录，不能只保留碰巧满足答案的一次。
4. 严格检查应用层几何收敛及驻点质量；根据终态结构核对 N/O 上的 H、重原子连通、N···O 距离/骨架构象、溶质与水的原子映射。xTB 的 SCC 迭代设置不能当成几何优化循环设置；按实际版本确认优化控制项。发生断键、质子转移或构象合并时按真实终态记录，不继续沿用原文件名宣称成功，也不未经批准加约束强行得到指定构象。
5. 仅对有效终态进行一致的 ORCA 配对单点，按已确认的作者式定义处理复合物与其对应水网络，保留水网络的几何来源和是否另作处理的约定。旧失败结构上的单点能量不能嫁接到新终态。只在同一分子内形成相对能量和优选构象，不比较 AL/AB 绝对能量。
6. 对能量所选的有效构象计算/提取**分子**偶极，写清所对应的几何、溶剂近似、单位和电荷定义。若能量用显式簇而偶极采用溶质单独计算，必须明确几何映射、是否改变几何及不同计算阶段；不能把整簇偶极或未核对的前驱偶极当成同一终态分子偶极。直接核对输出打印的 Debye。
7. 分别检验“AL 优选 folded”“AB 优选 extended”“优选 AB 分子偶极 > 优选 AL”。先按有效能量选构象，再比较偶极；禁止先选目标构象再声称它最低。若一致、有效的方案仍得到 folded AB 或其他不符结果，照实报告，不改变 evaluator 或自动转入无限重试。

**预期交付/退出条件**：每候选的真实最终身份、收敛/驻点证据、复合物/水网络成对能量、相对能、构象描述符和分子偶极；逐项说明三条目标结论得到支持还是仍不支持。没有有效、身份一致的前驱链时，即使下游单点全成功也不能宣布关闭缺口。

## 4. 交给 group_6 agent 的指令

请遵守第 2 节，仅处理 `paper_b815e2622b0d6085` 的第二网格电子态身份/稳定性缺口。`paper_84efbea3ab8e6e20` 不在本次补算任务中。

### 4.1 目标与边界

三种 300 K 实验母体晶体，Cl/Br/I 分别为 CCDC 2499860/2499862/2499861。保持当前批准的固定母体几何、HSE06（25% exact exchange，screening 0.2 Å−1）、scalar-relativistic/no-SOC 主协议。原有主网格结果已支持三个框架能隙目标：4.664272/4.660486/4.460078 eV 对应 4.63/4.64/4.44 eV（±0.15）。不是重做晶体、优化结构或再找一个更接近答案的能带。

**必读资料**：

- [正文](../papers/paper_b815e2622b0d6085/documents/main.pdf)，PDF p.2 方法、p.4 对低有机导带与 Pb 相关导带的区分；[SI](../papers/paper_b815e2622b0d6085/documents/supplementary_001.pdf)。
- [AR reference](hold_verified_autonomous_research/paper_b815e2622b0d6085/evaluation/verified_computation_reference.md)、[PR reference](hold_verified_paper_reproduction/paper_b815e2622b0d6085/evaluation/verified_computation_reference.md)。
- [当前物理量定义](hold_verified_autonomous_research/paper_b815e2622b0d6085/agent_input/data/inputs/electronic_observables.json)、[已整理主网格证据](hold_verified_autonomous_research/paper_b815e2622b0d6085/evaluation/boundary_repair_evidence.json)，重点看 `release_reconciliation`，以及两模式 task/evaluator。
- 历史文件根：`docs/verification/group_6/paper_b815e2622b0d6085/provenance/qzcli_hpc/`。三个第二网格目录分别为 `Cl_parent_HSE06_kmesh3x3_analysis/1_20260903T220321Z_266`、`Br_parent_HSE06_kmesh3x3_analysis/1_20260903T220351Z_422`、`I_parent_HSE06_kmesh3x3_analysis/1_20260903T220327Z_345`；主网格/投影目录的精确链接见 reference。

### 4.2 执行步骤

1. 核实已有 2×2×1 主网格的完整本征值、投影、母体结构、占据、自旋、计算参数及较低候选态。已确认主候选为按成分识别的 Pb-p-leading 框架态，不是按固定编号或 gold 能量选出来的；保留这部分成果。
2. 查找第二个 3×3×1 网格是否在其他既有归档、原工作区或输出收集处留有对应投影/可用波函数。当前列出的三个目录有本征值，但没有 PROCAR，vasprun 无 projected 段，WAVECAR 均为零字节。先确认找到的文件确实属于同一结构、方法、网格和有效运行，不可借用主网格投影冒充第二网格投影。
3. 若找到有效波函数/投影，则用可验证的后处理恢复态字符，优先避免新 SCF。若没有，**只补三种晶体的 3×3×1 HSE06 定几何静态/投影计算**，保持原有一致方法、势函数、自旋和收敛设置，正确启用并保存投影输出（例如原主网投影使用的 LORBIT=11）。保存完整 INCAR/POSCAR/KPOINTS、势函数身份、OUTCAR、EIGENVAL、PROCAR、vasprun 和可用波函数。重启数据只有在实际兼容时才复用；不能用另一个低级别方法或未经核实的非自洽近似代替该 HSE06 分支。
4. 在第二网格独立检查**所有较低未占据候选**及有机/无机组分。依公开定义，以 Pb-p 为领先的 component/element/angular-momentum 组识别最低可跟踪框架导带，并结合成分和连续性核对跨网格物理身份。保留每个 k/自旋的候选投影、归一化和原子归属。不能直接取 band 133；I 的混合态也不能被额外的“每个 k 都需 >50% 无机权重”规则排除。
5. 分别提取 fundamental edge gap、fundamental minimum same-k gap、framework edge gap、framework minimum same-k gap；保存相关能带、自旋、占据、简并边缘 k 集合和采样范围内的直接/间接判定。对每个量给出相对主网格的带符号变化及非负绝对变化。
6. 明确是否真的比较了同一物理定义的框架态。混合、换序或无法唯一跟踪时报告证据和歧义，不强行凑原编号。小的同编号能量差本身不能关闭身份缺口。
7. 逐条对齐当前 evaluator：主目标值、成分身份、低导带保留、两类 gap、同 k 点量、数值稳定性和有限采样解释。不要增加 SOC、光学矩阵元、母体重优化或完整布里渊区极值证明等当前非必评工作；光学 allowedness 继续与单纯电子能隙分开。

### 4.3 预期交付/退出条件

交付三晶体两网格的量值/变化对照表、独立投影和跨网格身份依据、所有必要原始路径及逐关键点判定。如果三个第二网格均完成且物理态身份可确认，就可提交“原稳定性缺口已补足”的证据供复核；如果有对象仍含糊，点名对象和量，不能通过删除必评要求宣布通过。

## 5. 回到 final 的条件

接手 agent 先交报告，不自行恢复。维护者需核对：现有/补充计算真实有效；对象和定义对应当前任务；所有保留的必评点有证据；公开输入没有加入答案/终态；任何科学边界调整已获用户确认。然后同步 AR/PR 的私有 reference（只记录真实有效链）、相关元数据和必要 manifest，检查包与链接，再成对移回 final 并更新发布统计。不能只依据 PASS 字段或“程序完成”恢复。

## 6. 本次迁移验收（不等于补充科学验证）

- 六个迁移包共 88 个文件，与迁移前 Git 版本逐字节比较全部相同；final 中不再留副本。
- 105 个 final 包和 6 个 hold 包直接结构/manifest 校验均无 findings；迁移包 reference、当前汇总和交接文档的本地链接均可定位。
- 路径校验器仅增加 hold 存储别名，不将 hold 纳入任务发现；回归测试继续覆盖 hold 包，未靠移出目录跳过其科学边界检查。
- 相关回归：`tests/test_final_release_remediation.py`、`test_three_boundary_repairs.py`、`test_remaining_final_task_repairs.py`、`test_agent_geometry_audit.py`、`test_task_package_v19.py`，合计 **98 passed**。这些是软件/结构和既有输出检查，不是新量化计算或运行时隔离证明。
- 没有修改 `docs/verification`，没有提交或取消任何计算作业。源任务仍保留，实际发布必须明确只选 final，不能从 canonical 源目录重新选入暂缓论文。
