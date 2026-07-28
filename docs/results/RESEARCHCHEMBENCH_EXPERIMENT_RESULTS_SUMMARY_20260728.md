# ResearchChemBench 实验结果总览

截至日期：2026-07-28

本汇总整理 `docs/results` 中已有的 7 份实验报告。重复覆盖同一运行时，以最新的 `dual_axis_100` 人工轨迹审查为最终评分口径；早期试运行和旧评分只用于展示评分演进。所有正式运行的 Agent 与 Judge 均为 `deepseek-v4-flash`。

## 一、总体结论

- 共整理 **14 个正式 Agent 运行**：7 个自主科研任务、7 个论文复现任务。
- 人工双轴最终平均分为 **38.94/100**；Flash Judge 平均分为 **49.34/100**，平均高估约 **10.4 分**。
- 自主科研任务人工平均分为 **27.32**，论文复现任务为 **50.56**。模型在公开方法和路径明确时表现明显更好。
- 最佳运行是 `Electron_Isodensity_Reproduction_04_Blind_Prediction`（91.00）和 `BaO_Phase_Crossover_And_5d_Bonding_Reproduction`（90.00）。
- `Heterobiaryl_PV_02_CC_Selectivity` 自主与复现均为 0 分，核心原因是错误解释作者文件标签并且没有验证反应路径连通性。
- 14 个运行累计耗时 **10,730.8 秒**，共调用工具 **571 次**、失败 **24 次**，Agent Token 合计 **79,610,417**。

最终分数均按下式计算：

```text
最终分数 = 科学结论分 × 科研过程分 ÷ 100
```

## 二、14 个正式运行的最终结果

| 任务 | 模式 | Judge 结论/过程/最终 | 人工结论/过程/最终 | 时长（秒） | 工具调用（失败） | Agent Token | 主要结果 |
|---|---|---:|---:|---:|---:|---:|---|
| `GEOM_Hierarchical_Conformer_Reranking` | 自主 | 55 / 88 / 48.40 | 53 / 79 / **41.87** | 995.7 | 46（0） | 3,292,540 | 证明低成本与 DFT 电子能排序明显不同，但没有频率和自由能，未完成热布居结论。 |
| `GEOM_Hierarchical_Conformer_Reranking_Reproduction` | 复现 | 80 / 77 / 61.60 | 58 / 67 / **38.86** | 2,162.1 | 70（2） | 10,160,512 | 完成 CREST、ORCA 和 GoodVibes，但缺少可靠的构象盆地对齐，lineage 记录错误。 |
| `Electron_Flexible_Ensemble_Surface` | 自主 | 80 / 89 / 71.20 | 69 / 76 / **52.44** | 304.9 | 41（1） | 2,817,549 | 四构象表面积差异显著，但采样不足、权重仅基于电子能，169.19 Å² 偏离论文尺度。 |
| `Electron_Flexible_Ensemble_Surface_Reproduction` | 复现 | 90 / 87 / 78.30 | 95 / 81 / **76.95** | 1,427.6 | 97（5） | 6,294,960 | 五构象热集合得到 159.09 Å²，与论文 157.1994 Å² 相差约 1.2%，主要结论成功复现。 |
| `Electron_Isodensity_04_Blind_Prediction` | 自主 | 100 / 84 / 84.00 | 64 / 63 / **40.32** | 617.3 | 53（0） | 3,877,008 | 预测 110.81 Å²，数值准确；但先计算 M4、后写 calibration lock 和研究计划，不构成严格盲测。 |
| `Electron_Isodensity_Reproduction_04_Blind_Prediction` | 复现 | 100 / 94 / 94.00 | 100 / 91 / **91.00** | 395.8 | 21（0） | 1,714,453 | 计算 110.05219 Å²，相对论文值误差 0.0505%、相对实验误差 0.44%，完整复现。 |
| `PV_Protonation_Barrier_Trend` | 自主 | 0 / 66 / 0 | 18 / 57 / **10.26** | 468.3 | 18（0） | 7,549,989 | P0>P1>P2 仅名义成立，P1/P2 未分辨，路径和热化学处理不足。 |
| `PV_Protonation_Barrier_Trend_Reproduction` | 复现 | 80 / 81 / 64.80 | 52 / 73 / **37.96** | 462.3 | 28（0） | 得到强放热轮廓，但没有复现第二次质子化的进一步显著降垒。 |
| `BaO_Phase_Crossover_And_5d_Bonding` | 自主 | 100 / 71 / 71.00 | 60 / 63 / **37.80** | 1,019.0 | 38（9） | 底层 VASP 数据支持正确相序，但最终报告的 3.1、17.65 GPa 与自身焓表矛盾。 |
| `BaO_Phase_Crossover_And_5d_Bonding_Reproduction` | 复现 | 100 / 91 / 91.00 | 100 / 90 / **90.00** | 583.7 | 59（5） | 成功复现 B1→B8→dB2 及 6.09、29.0 GPa 两个转变压力。 |
| `Heterobiaryl_PV_02_CC_Selectivity` | 自主 | 0 / 77 / 0 | 0 / 57 / **0.00** | 412.9 | 14（0） | 把没有字面 Py-Py 文件名误判为没有该路径，得到相反的 Ph-Py 优先结论。 |
| `Heterobiaryl_PV_Reproduction_02_CC_Selectivity` | 复现 | 0 / 53 / 0 | 0 / 41 / **0.00** | 609.3 | 27（0） | 同一 TS 同时用于 Py-Py 和 Ph-Py，未验证成键坐标、虚频模式或 IRC。 |
| `Heterobiaryl_PV_05_Rate_Determining_Step` | 自主 | 0 / 78 / 0 | 13 / 66 / **8.58** | 383.4 | 14（0） | 重建部分下游轮廓，但把下游重排/偶联错误地作为全反应决速步骤。 |
| `Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step` | 复现 | 40 / 66 / 26.40 | 33 / 58 / **19.14** | 888.6 | 45（2） | 部分支持选择性和后续不可逆性，但误判总决速步骤，并以 298 K 代替 353.15 K 热校正。 |

## 三、可靠的论文复算与数值基准

这些结果来自作者原始输出重分析或真实软件计算，用于验证任务是否存在可达的正确答案，不是 Agent 得分。

| 科学体系 | 已验证结果 | 证据与边界 |
|---|---|---|
| P(V) Py-Py 质子化趋势 | P0/P1/P2 势垒分别为 **30.9134、19.8135、14.3004 kcal/mol** | 作者 Gaussian 频率与 ORCA DLPNO 输出，经 GoodVibes 353.15 K、1 M、乙醇准谐分析。 |
| P(V) Py-Py 与 Ph-Py | Ph-Py 势垒为 **37.3192、26.8607、25.5695 kcal/mol**；三种状态均为 Py-Py 动力学优先 | P2 完整 Py-Py 路径为 `0, 14.2937, -19.2054, -10.3901, -31.3526` kcal/mol。 |
| P(V) C-C 与 C-O | C-C 可重算为约 **14.30 kcal/mol**；论文 C-O 为约 **18 kcal/mol** | 公开归档没有 C-O TS 频率、IRC 和匹配 DLPNO 文件，C-O 只能作为明确标注的论文证据。 |
| BaO 高压相变 | B1→B8 为 **6.023 GPa**，B8→dB2 为 **28.909 GPa** | 15 个真实 VASP 相-体积点、10 个内部弛豫和 Birch-Murnaghan EOS 拟合。 |
| BaO 5d 成键 | 标准 LOBSTER 基组无法复现论文的 Ba 5d 自定义投影消融 | 论文所需 La-5d-on-Ba 自定义基组未公开；标准运行实际仍只建立 Ba 5s/6s/5p。 |
| NHC/PdCu(111) | NHC1/NHC4 的 Pd-C 距离为 **2.0570/2.0430 Å**；结合能差 **-1.1 kcal/mol** | 坐标与论文表格可复算；完整 VASP-to-LOBSTER 原始链不可用，因此未进入快速双轨发布。 |
| Electron Flexible Ensemble | 五构象集成面积 **159.0863 Å²**，论文完整集合约 **157.1994 Å²** | 受控 5 构象复现，支持构象依赖和热集合结论，但不是完整 25 构象复制。 |
| Electron Isodensity Q4 | 复现值 **110.05219 Å²**；论文值 **109.9966 Å²**；实验值 **110.538 Å²** | ORCA relaxed-MP2 density → 波函数导出 → Multiwfn 的真实软件链完整。 |

对于异联芳基 Q5，需要区分两个层级：作者归档中的 TS-I 是**已给定下游 P(V) 轮廓内**的最高前向势垒；最终任务要求的**全反应总体决速步骤**则是实验支持的上游醇加成。下游轮廓本身不能单独证明总体决速步骤。

## 四、评分口径演进

早期报告主要采用单轴量表或较宽松的语义门槛，后续统一改为结论轴与过程轴相乘。下表展示重复实验为什么出现不同分数。

| 任务 | 早期 Judge / 人工 | 严格或双轴 Judge | 最终双轴人工 | 变化原因 |
|---|---:|---:|---:|---|
| `GEOM_Hierarchical_Conformer_Reranking` | 85 / 79 | 48.40 | **41.87** | 未完成 DFT 几何、频率和热自由能，电子能重排不能等同热布居。 |
| `GEOM_Hierarchical_Conformer_Reranking_Reproduction` | 92 / 88 | 61.60 | **38.86** | 缺少优化前后构象盆地对齐，lineage 错误使覆盖和重排序证据失效。 |
| `Electron_Flexible_Ensemble_Surface` | 93 / 85；严格复评 95 / 57 | 71.20 | **52.44** | 四构象电子能集合缺少采样收敛、热自由能和密度方法敏感性。 |
| `Electron_Flexible_Ensemble_Surface_Reproduction` | 100 / 96 | 78.30 | **76.95** | 双轴评分保留高结论分，同时扣除验证、失败记录和并行效率问题。 |
| `Electron_Isodensity_04_Blind_Prediction` | 70 / 60 | 84.00 | **40.32** | 数值命中，但 calibration lock 和研究计划晚于目标分子计算，报告时序不真实。 |
| `Electron_Isodensity_Reproduction_04_Blind_Prediction` | 93 / 98 | 94.00 | **91.00** | 真实复现仍保持高分；后续仅增加网格/不确定性和溯源方面的严格扣分。 |

## 五、跨实验观察

### 模型能力

1. Flash 能编排 RDKit、CREST/xTB、ORCA、Gaussian、GoodVibes、VASP 和 Multiwfn 等多软件链。
2. 给定明确协议时，模型可以完成高质量复现；Q4、BaO 和 Flexible Ensemble 复现是主要正例。
3. 自主科研的主要短板不是工具调用，而是研究设计和证据门槛：缺少热化学、采样收敛、路径连通性、方法比较及真正的预注册。
4. 模型容易相信文件名和自身生成的标签，而不是检查结构、成键坐标、虚频模式和 IRC。
5. 模型可能先完成计算，再补写研究计划、calibration lock、tool trace 或 failure log，因此必须检查系统轨迹时间顺序。

### Judge 可靠性

1. 14 个任务中，Flash Judge 平均比人工轨迹审查高约 10.4 分。
2. 当报告、轨迹和证据一致时，Judge 与人工较接近，例如 Q4、Flexible 和 BaO 复现。
3. 最大风险是 Judge 过度相信 Agent 报告，没有核验原始时间顺序、构象 lineage、实际调用的软件参数和最终结论与底层数据是否矛盾。
4. 评分前应增加确定性检查：计划/锁定时间、调用与失败计数、结构对齐、频率/IRC 是否执行、数值误差和量表公式。

### 工具箱状态

实验期间已修复 CREST 工件传递、ORCA/OpenMPI、ORCA 深路径 Hessian、方法名兼容、GoodVibes 乙醇介质、VASP POTCAR 拼接和 VASP 结构解析等问题。修复后的正式运行没有因缺少关键后端而客观不可评分；主要差异来自 Agent 的科研决策和验证质量。

## 六、源报告索引

| 报告 | 内容 | 在本汇总中的口径 |
|---|---|---|
| [ELECTRON_ISODENSITY_Q4_DUAL_MODE_FLASH_EVALUATION_REPORT.md](./ELECTRON_ISODENSITY_Q4_DUAL_MODE_FLASH_EVALUATION_REPORT.md) | Q4 双模式早期专项分析 | 保留任务说明和数值；最终分采用后续六任务双轴审查。 |
| [MULTISOFTWARE_PILOT_FLASH_EVALUATION_20260726.md](./MULTISOFTWARE_PILOT_FLASH_EVALUATION_20260726.md) | GEOM/Flexible 四任务试运行与工具修复 | 保留真实流程、数值和资源信息；早期分数已被双轴评分替代。 |
| [AUTONOMOUS_STRICT_RESCORE_GEOM_ELECTRON_20260726.md](./AUTONOMOUS_STRICT_RESCORE_GEOM_ELECTRON_20260726.md) | 两个自主任务严格单轴复评 | 作为评分器演进证据，不作为最终统一分数。 |
| [SIX_DUAL_AXIS_TASKS_FLASH_REJUDGING_AND_EXPERT_AUDIT_20260726.md](./SIX_DUAL_AXIS_TASKS_FLASH_REJUDGING_AND_EXPERT_AUDIT_20260726.md) | GEOM、Flexible、Q4 六任务双轴重判 | 六个任务的最终人工评分来源。 |
| [PAPER_REPRODUCTION_TASK_REPAIR_AND_VALIDATION_20260727.md](./PAPER_REPRODUCTION_TASK_REPAIR_AND_VALIDATION_20260727.md) | P(V)、BaO、NHC 真实复算与任务修复 | 数值基准和可复现边界来源。 |
| [PAPER_REPRODUCTION_DUAL_TRACK_RELEASE_20260728.md](./PAPER_REPRODUCTION_DUAL_TRACK_RELEASE_20260728.md) | 四组论文任务双轨发布决策 | 发布范围、共享数据和排除项来源。 |
| [PAPER_DUAL_TRACK_MANUAL_RESCORING_20260728.md](./PAPER_DUAL_TRACK_MANUAL_RESCORING_20260728.md) | 八个论文双轨运行的人工轨迹审查 | 八个任务的最终人工评分来源。 |
