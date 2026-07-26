# 多软件新任务 Flash 试运行与工具箱可行性报告

日期：2026-07-26  
Agent：`deepseek-v4-flash`  
Judger：`deepseek-v4-flash`

## 1. 结论摘要

本轮选择了两个任务对，共运行四个任务，且没有重复此前的 `Electron_Isodensity_*_04_Blind_Prediction`：

| 模式 | 任务 | Flash/Judger | 独立审计 | 结论 |
|---|---|---:|---:|---|
| 论文复现 | `GEOM_Hierarchical_Conformer_Reranking_Reproduction` | 92 | 88 | 客观可完成；成功复现“低成本搜索可覆盖构象，但量子精修会显著重排能量与布居”的论文结论 |
| 论文复现 | `Electron_Flexible_Ensemble_Surface_Reproduction` | 100 | 96 | 修复工具箱后客观可完成；真实获得构象依赖表面积及热力学集成结果 |
| 自主科研 | `GEOM_Hierarchical_Conformer_Reranking` | 85 | 79 | 有效评估了自主路线设计能力；结论有计算支持，但缺少 DFT 几何优化和频率/自由能修正 |
| 自主科研 | `Electron_Flexible_Ensemble_Surface` | 93 | 85 | 有效评估了自主采样、密度和数值敏感性分析能力；仅 4 个构象且使用电子能权重，Judger 偏宽松 |

四项任务均存在从当前输入和工具箱得到有效科学结论的客观路径。修复后的正式运行中，没有发现仍会阻止任务完成的工具箱缺陷。

Judger 平均分为 **92.5**，独立审计平均分为 **87.0**。主要差异不是工具是否真实运行，而是 Flash Judger 对采样覆盖、自由能严谨性、并行效率和证据充分性的扣分偏少。

## 2. 本轮修复内容

### 2.1 任务和评分边界

提交 `2043bca`：

- 复现任务将论文主要结论置于高权重评分项，避免只完成流程却没有得到论文结论仍获高分。
- 自主科研任务使用独立的 `autonomous_discovery` 评分维度，不要求命中隐藏论文数值。
- GEOM 复现按结构盆地而非文件序号比较构象。
- Electron 复现明确为 4–6 构象的受控复现，不要求复制论文完整 25 构象总平均。
- Electron 自主任务不向 Agent 泄露论文 TE 数值或固定论文答案。

### 2.2 CREST 和构象工件互操作

提交 `4a3e5f4`：

- 修复 CREST 构象集合、能量和单构象结构的解析与工件传递。
- 允许后续 ORCA/分析步骤直接消费 CREST 结果，避免手工转录结构。
- 增加相关回归测试。

### 2.3 ORCA MPI 与资源运行时

提交 `2391057`：

- 修复 ORCA 6.1.1 与匹配 OpenMPI 4.1.8 的大分子并行运行环境。
- 校正 ORCA、`mpirun`、PATH 和动态库路径，避免大体系并行作业因运行时不匹配失败。

### 2.4 嵌套并行和轨迹快照

提交 `1626f7e`：

- CREST 的主 OpenMP 线程数使用 Agent 选择的 CPU 数，但 OpenBLAS/NumExpr 固定为 1，避免嵌套并行和警告洪泛。
- 原生软件层同样限制 BLAS 嵌套线程。
- 轨迹系统不再实时复制 `outputs/execution_jobs/**` 中仍在变化的 ORCA 大型临时文件，消除了轮询期间的文件竞争和大量重复数据；最终科学输出仍由 collect/结果工件完整保留。

### 2.5 ORCA Hessian 深层路径崩溃

提交 `3320011`：

- 通用 ORCA Action 原先向 ORCA 传入工作区深层绝对输入路径。
- ORCA 的 property/frequency 模块会将该路径传播到内部 basename，可能在性质积分阶段无诊断退出。
- 现改为在计算目录中传入 `./job.inp`。
- 真实回归：水分子 `r2SCAN-3c` Hessian、4 CPU，约 3 秒成功，得到 9×9 Hessian。

### 2.6 ORCA 文献方法名兼容

提交 `6981bf3`：

- 论文常将方法写成 `DSD-PBEP86-D3BJ`，ORCA 简单输入实际要求 `DSD-PBEP86 D3BJ` 两个关键词。
- Action 原样拼接时会报 `UNRECOGNIZED ... DSD-PBEP86-D3BJ`。
- 新增通用方法/色散别名规范化，并对显式冲突进行拒绝，不静默替换 Agent 参数。
- 真实回归：ORCA 6.1.1 水分子 relaxed-MP2 密度成功，产出密度与波函数工件。

## 3. 正式运行结果

### 3.1 GEOM 论文复现

运行目录：

`workspaces/multisoftware_pilot/agent_deepseek-v4-flash__judge_deepseek-v4-flash/cli_runs/batch_20260726_090315_682c08/GEOM_Hierarchical_Conformer_Reranking_Reproduction_opencode_20260726_090315_8d11a2`

实际流程：

1. RDKit 生成初始三维结构和 ETKDG/MMFF 构象。
2. CREST `GFN2-xTB + ALPB(water)` 搜索，得到 25 个候选构象。
3. 选择 8 个构象，用 ORCA `r2SCAN-3c/CPCM(water)` 优化和频率计算。
4. GoodVibes 在 298.15 K 做准谐振自由能和布居分析。
5. 对齐相同构象盆地，比较 xTB、SCF 能量和准谐振 Gibbs 排名。

主要结果：

- xTB 与量子电子能 Spearman `rho = 0.40`。
- xTB 与准谐振 Gibbs 排名 Spearman `rho = 0.50`。
- Top-3 仅重合 2/3，部分低成本高排名构象在精修后明显下降。
- 8/25 精修预算的未覆盖布居代理估计约 9.7%。
- 支持论文结论：低成本方法适合提供覆盖，但不能直接代替量子自由能排序。

独立审计扣分点：

- Flash 多次编写错误 ORCA 原生输入后才恢复，管理型科学尝试中记录了较多失败/未完成分支。
- 只精修 8/25，遗漏布居依赖 xTB 能量代理，不是严格量子上界。
- 部分分析脚本曾通过普通 shell 运行，科学主计算仍为可审计的 managed calls。
- 作业调度存在一次长时间无效等待，并行利用不够稳定。

### 3.2 Electron Flexible Ensemble 论文复现

运行目录：

`workspaces/multisoftware_pilot/agent_deepseek-v4-flash__judge_deepseek-v4-flash/cli_runs/batch_20260726_101013_f288f5/Electron_Flexible_Ensemble_Surface_Reproduction_opencode_20260726_101013_2c9b71`

实际流程：

1. 对论文提供的 25 个 ISO-M6 构象逐个运行 GFN2-xTB 能量筛选。
2. 使用能量和重原子 RMSD 选择 5 个构象。
3. ORCA `r2SCAN-3c` 优化、Hessian、振动和 298.15 K 热化学。
4. ORCA `DSD-PBEP86-D3BJ/def2-QZVPD` relaxed-MP2 密度。
5. ORCA 导出 WFX，Multiwfn 在锁定 cutoff `0.0016 a.u.`、网格 `0.08 bohr` 下计算表面积和体积。
6. 用计算得到的热力学权重构造 5 构象集成。

主要结果：

| 构象 | 表面积 / Å² | Boltzmann 权重 |
|---|---:|---:|
| 1475-1 | 161.1810 | 0.3263 |
| 1475-2 | 159.2367 | 0.1049 |
| 1475-3 | 158.7151 | 0.2510 |
| 1475-4 | 155.9028 | 0.1936 |
| 1475-5 | 159.1694 | 0.1241 |

- 集成表面积：`159.0863 Å²`。
- 最低自由能单构象：`161.1810 Å²`。
- 集成与单构象差：`-2.0947 Å² (-1.3%)`。
- 构象范围：`155.9028–161.1810 Å²`，跨度 `5.2783 Å²`。
- leave-one-out 最大偏差：`1.0147 Å² (0.64%)`。
- 论文完整 25 构象值约 `157.1994 Å²`；本受控 5 构象结果高约 `1.89 Å² (1.2%)`，方向和主要结论一致，不应宣称完整数值复现。

独立审计扣分点：

- `conformer_selection.csv` 没有保存逐对 RMSD 或 cluster id，虽然脚本确实计算了 RMSD，报告的“多样性”证据仍不够直观。
- 独立构象计算通过同步 Action 串行执行，未充分利用 54 核服务器。
- Flash 最初遗漏 `linearity` 参数，连续产生 5 次无效振动分析请求后才通过 schema 修正。
- 因为任务明确是 4–6 构象受控复现，以上问题不改变“客观可复现”的结论，但 100 分略显宽松。

### 3.3 GEOM 自主科研

运行目录：

`workspaces/multisoftware_pilot/agent_deepseek-v4-flash__judge_deepseek-v4-flash/cli_runs/batch_20260726_103452_e4131f/GEOM_Hierarchical_Conformer_Reranking_opencode_20260726_103452_37b4ec`

Flash 自主选择的流程：

1. 从 SMILES 生成三维结构。
2. CREST `GFN2-xTB + ALPB(water)` 搜索出 27 个构象。
3. 选择 12 个构象，用 ORCA `B3LYP/def2-SVP + SMD(water)` 单点精修。
4. 对 7 个构象增加 `PBE0/def2-SVP + SMD(water)` 方法扰动。
5. 比较排名、电子能 Boltzmann 布居和 Top-3 重合度。

主要结果：

- GFN2 与 B3LYP：`rho = 0.4336`。
- B3LYP 与 PBE0：`rho = 0.6071`。
- GFN2 主导构象为 Conf 1，约 38.1%；B3LYP 主导构象为 Conf 7，约 44.6%。
- GFN2 Top-3 为 1/2/3；B3LYP Top-3 为 7/6/1，仅重合 1 个。
- 结论：GFN2 搜索可用于构象生成，但其能量排序不能直接作为热布居预测。

独立审计认为 85 分偏高：

- DFT 只做了 GFN2 几何上的单点，没有 DFT 几何优化。
- 没有频率、零点能或热/熵修正，因此所谓 298.15 K “Boltzmann population”实际基于电子能，不是自由能布居。
- 没测试 CREST 能量窗口或采样重复的收敛性。
- `rho = 0.607` 只能说明 B3LYP/PBE0 中等一致，报告称“DFT internal consistency”略偏强。

尽管如此，该任务确实测到了自主规划、软件选择、方法扰动和证据约束结论的能力，没有被工具箱客观限制。

### 3.4 Electron Flexible Ensemble 自主科研

运行目录：

`workspaces/multisoftware_pilot/agent_deepseek-v4-flash__judge_deepseek-v4-flash/cli_runs/batch_20260726_105217_d362e0/Electron_Flexible_Ensemble_Surface_opencode_20260726_105217_64d3fa`

Flash 自主选择的流程：

1. RDKit ETKDG 生成构象，最终得到 4 个不同结构。
2. GFN2-xTB 优化。
3. ORCA `B3LYP/def2-SVP` SCF 密度。
4. ORCA WFN 导出，Multiwfn 计算 `0.001` 和 `0.002 a.u.` 两个等密度面。
5. 比较 `0.15` 与 `0.08 bohr` 网格，并分析 Top-1/2/3 截断。
6. 用 GFN2 电子能权重构造集成。

主要结果：

- `0.001 a.u.` 集成表面积：`169.19 ± 2.91 Å²`。
- 单个最低能构象：`170.3506 Å²`；与集成差 0.69%。
- 四构象表面积范围为 11.66 Å²，约 6.89%。
- `0.15` 与 `0.08 bohr` 网格差 0.019%，数值离散误差约 0.032 Å²。
- 构象 0 权重约 86.3%，因此集成和单构象接近，但集成仍更可辩护。

独立审计认为 93 分偏高：

- 仅得到 4 个构象，且缺少生成后聚类覆盖或重复采样验证。
- 权重仅基于 GFN2 电子能，没有自由能或低频熵敏感性。
- 密度使用 B3LYP/def2-SVP，未做基组或密度方法扰动。
- 自主选择 `0.001 a.u.` 是合理探索值，但没有实验/物理校准，因此该数值只能解释为该定义下的盲预测，不能与论文的 `0.0016 a.u.` 数值直接比较。

该任务仍然有效评估了自主路线设计、失败后切换后端、跨软件工件传递、cutoff 与网格敏感性以及不确定性表达。

## 4. 资源消耗

Agent token 为逐模型步骤统计；`cache` 是缓存读取量，不等同于未缓存输入计费。Judger token 单独列出。

| 任务 | 墙钟时间 | 模型步骤 | 工具调用（成功/失败） | Agent input | Agent cache read | Agent output | Judger prompt/output |
|---|---:|---:|---:|---:|---:|---:|---:|
| GEOM 复现 | 2162.1 s（36:02） | 87 | 70（68/2） | 151,742 | 9,962,752 | 34,674 | 184,369 / 3,883 |
| Electron 复现 | 1427.6 s（23:48） | 45 | 97（92/5） | 218,194 | 6,044,032 | 26,722 | 130,797 / 2,634 |
| GEOM 自主 | 995.7 s（16:36） | 36 | 46（46/0） | 121,552 | 3,145,472 | 18,847 | 103,253 / 2,264 |
| Electron 自主 | 304.9 s（05:05） | 32 | 41（40/1） | 115,468 | 2,674,688 | 21,781 | 84,914 / 3,004 |
| 合计 | 4890.2 s（81:30） | 200 | 254（246/8） | 606,956 | 21,826,944 | 102,024 | 503,333 / 11,785 |

耗时最大的单阶段：

- GEOM CREST：复现约 8.6 分钟，自主约 8.3 分钟。
- Electron 复现 5 个 DSD-PBEP86 密度：每个约 151–155 秒，串行总计约 12.8 分钟。
- Electron 复现 5 个 Multiwfn 表面：每个约 33–36 秒。

## 5. 是否真正评估了模型能力

### 复现模式

修复后，两个复现任务的所有关键阶段都有真实软件输出，且工具箱能够产出目标结论。最终差异主要来自 Agent 的：

- 参数填写与原生输入正确性；
- 构象选择和覆盖策略；
- 是否按协议完成所有阶段；
- 是否正确解释受控子集与完整论文值的差别；
- 是否充分并行和减少无效重试。

因此这两个正式结果可以用于评价 Flash 的论文复现能力。Electron 复现的 100 分应下调至约 96，主要是证据记录和效率问题，而不是结论错误。

### 自主科研模式

两个自主任务未泄露论文路线，Flash 自主选择了与复现路线不同的方法：

- GEOM 自主使用 B3LYP/PBE0 单点扰动，而非复现任务的 r2SCAN-3c + GoodVibes。
- Electron 自主使用 4 个自生成构象、B3LYP/def2-SVP SCF 密度和自主 cutoff，而非论文的 25 个构象、DSD-PBEP86 密度和 0.0016 cutoff。

这表明任务确实在测试自主科研决策，而不是照抄论文流程。当前评分标准的主要改进方向是进一步提高以下内容的扣分力度：

- 将电子能布居写成热力学布居；
- 构象数量过少或缺乏采样收敛；
- 没有几何/频率验证却给出过强结论；
- 方法扰动只有中等一致却称为充分验证；
- 串行调用大量独立计算，忽略服务器并行资源。

## 6. 最终判断

1. 这四个任务在修复后的当前化学工具箱上均可客观完成。
2. 两个复现任务能够得到论文主要结论；Electron 为受控 5 构象复现，不是完整 25 构象数值复制。
3. 两个自主科研任务没有受到关键工具缺失限制，结果主要反映 Flash 的科研方案质量。
4. 当前最需要继续改进的不是新增任务专用 Action，而是评分器对“自由能严谨性、采样收敛、方法验证和资源效率”的识别与扣分。
5. ORCA/CREST/Multiwfn 的关键客观故障均已修复并通过正式任务验证。

