# Heterobiaryl P(V) 双轨任务、工具箱修复与可行性实施报告

> 日期：2026-07-23
>
> 项目：ResearchChemBench
>
> 范围：六个开放探索任务、六个论文复现任务、相关 Chemistry Toolbox 能力和真实软件调用

## 1. 最终判断

本轮已经完成任务设计和工具箱修复，但**没有把工具 smoke、低层路径测试或论文参考值伪装成 P(V) 论文级复现结果**。

当前结论如下：

1. 原六个 `Heterobiaryl_PV_01...06` 已保留为开放探索轨：只提供任务、必要原始种子和实验观察，不公开论文方法或候选路线。
2. 新增六个 `Heterobiaryl_PV_Reproduction_01...06` 作为引导复现轨：公开论文重建的方法层级、候选成键/断键定义和验证要求，但不公开作者驻点、IRC、能量、势垒、路线排序或答案。
3. 修复后，Gaussian、ORCA、GoodVibes、pysisyphus、xTB 和直接编程入口能够覆盖论文复现所需的主要软件类型。此前“没有预设 Action”已不再是根本阻塞。
4. 六个任务当前都按真实证据标为 `partially_solvable`：工具能力已有实测，但尚未完成整个 P(V) 驻点网络、频率、双向连通性、DLPNO 外推和统一热化学计算，因此不能声称已复现论文主要数值结论。
5. Q5 还存在独立于软件的输入证据缺口：没有原始时间分辨动力学曲线、原始 NMR FID，也没有完整定义所有候选决速步骤（尤其醇加成）的反应体系和端点。它可以复现论文的“实验观察 + 下游偶联计算”论证，但不能从当前公开数据独立重做完整动力学鉴定。

## 2. Git 管理

本轮使用以下检查点和提交：

| Git 对象 | 用途 |
|---|---|
| `9a7046a` / tag `before-heterobiaryl-feasibility-audit-20260723` | 最初可行性审计前检查点 |
| `c4b66e1` / tag `before-heterobiaryl-dual-track-20260723` | 数据清理和第一版可行性审计完成 |
| `b876a8c` | 新增开放探索/论文复现双轨任务 |
| `a4496bf` | 修复反应工具、增加 Actions、保存真实运行证据并写入复现基线 |

未修改用户原有的无关未跟踪文件、压缩包和 core dump。

## 3. 双轨任务设计

### 3.1 开放探索轨

保留目录：

- `tasks/Heterobiaryl_PV_01_Protonation`
- `tasks/Heterobiaryl_PV_02_CC_Selectivity`
- `tasks/Heterobiaryl_PV_03_CC_vs_CO`
- `tasks/Heterobiaryl_PV_04_Coupling_Mechanism`
- `tasks/Heterobiaryl_PV_05_Rate_Determining_Step`
- `tasks/Heterobiaryl_PV_06_End_to_End`

统一元数据：

- `benchmark_family = heterobiaryl_pv`
- `task_mode = open_discovery`
- `method_disclosure = none`
- `pathway_disclosure = none`

该轨用于评估智能体能否在不知道论文方法和路线的情况下，自主提出假设、选择工具、生成路径、排错和验证结论。自动测试会检查公开文本及输入中没有 Gaussian、ORCA、GoodVibes、ωB97XD、DLPNO、论文 DOI、作者中间体/过渡态标签等路线泄漏。

### 3.2 引导复现轨

新增目录：

- `tasks/Heterobiaryl_PV_Reproduction_01_Protonation`
- `tasks/Heterobiaryl_PV_Reproduction_02_CC_Selectivity`
- `tasks/Heterobiaryl_PV_Reproduction_03_CC_vs_CO`
- `tasks/Heterobiaryl_PV_Reproduction_04_Coupling_Mechanism`
- `tasks/Heterobiaryl_PV_Reproduction_05_Rate_Determining_Step`
- `tasks/Heterobiaryl_PV_Reproduction_06_End_to_End`

每个复现任务在对应开放任务原始数据的基础上增加：

- `computational_protocol.json`：论文重建的方法和后处理层级；
- `reaction_definitions.json`：零基原子映射、候选成键/断键和对照路线；
- `workflow_requirements.json`：驻点、Hessian、连通性、统一热化学和失败保留要求。

公开的方法层级为：

- Gaussian：ωB97XD/6-31+G(d)，SMD ethanol，优化与频率；
- Gaussian 大基组检查：ωB97XD/def2-QZVPP，SMD ethanol；
- ORCA 参考路线：SMD-DLPNO-CCSD(T)，`Extrapolate(2/3,cc)`，cc-pVDZ/cc-pVTZ 外推，RIJCOSX、GRIDX5、TightSCF、KDIIS；
- GoodVibes：353.15 K、1 M、ethanol、100 cm⁻¹ Grimme 准谐处理、`--invertifreq -5`、匹配 `DLPNO` 单点；
- NBO 不设为必需，允许用键长、Wiberg/Mayer 键级、原子电荷和可选密度分析建立等价但边界清楚的证据。

复现轨仍然不包含：

- 作者优化结构或过渡态；
- 作者 IRC；
- 作者 Gaussian/ORCA 输出；
- 发表势垒、能量或路线排序；
- 参考答案。

## 4. 六个开放任务整理后的输入

所有数据均为正常可读取文件，不再依赖 ZIP 或符号链接。公共数据没有无差别复制到每个任务；每个任务只保留自身需要的状态和观察。

| 任务 | 结构输入 | 实验输入 | 顶层输入文件 |
|---|---|---|---|
| Q1 Protonation | P0/P1/P2 各 3 个未优化 ETKDG XYZ，共 9 个 | 无 | `README.md`、`conditions.json`、`molecular_systems.json`、`input_manifest.json`、`initial_structures/` |
| Q2 C–C Selectivity | P0/P1/P2 各 3 个未优化 XYZ，共 9 个 | 无 | 同 Q1 |
| Q3 C–C vs C–O | P2 的 3 个未优化 XYZ | E02、E10、E11、E12 | 上述公共文件，加 `experimental_measurements/measurements.json` |
| Q4 Coupling Mechanism | P0/P1/P2 各 3 个未优化 XYZ，共 9 个 | 无 | 同 Q1 |
| Q5 Rate-Determining Step | P2 的 3 个未优化 XYZ | E01、E02、E04–E12，共 11 条 | 上述公共文件，加筛选后的 `measurements.json` |
| Q6 End-to-End | P0/P1/P2 各 3 个未优化 XYZ，共 9 个 | 与 Q5 相同的 11 条 | Q1–Q5 所需输入的非重复并集 |

结构审计结果：

| 状态 | 分子式 | 原子数 | 电荷 | 多重度 | 质子化 N（零基） |
|---|---|---:|---:|---:|---|
| P0 | C23H21N2OP | 48 | 0 | 1 | 无 |
| P1 | C23H22N2OP | 49 | +1 | 1 | 18 |
| P2 | C23H23N2OP | 50 | +2 | 1 | 18、24 |

这些坐标是未优化起始种子，不应被称为最低能构象、驻点或作者结构。输入中没有显式酸、抗衡离子或溶剂分子；`conditions.json` 明确记录了这一点。

## 5. 新增 Action 和 backend 能力

| Action | backend | 作用 | 科学边界 |
|---|---|---|---|
| `search_reaction_path` | `pysisyphus` | NEB、Growing String、Freezing String 双端路径搜索 | 路径最高图像不是自动验证的过渡态 |
| `scan_reaction_coordinates` | `pysisyphus` | 单个键长/键角/二面角的松弛一维扫描 | 当前一次调用只扫描一个坐标 |
| `validate_reaction_path` | `internal_reaction_analysis` | 检查原子/电荷/自旋、端点、图像连续性和指定键变化 | 不代替 Hessian 或 IRC |
| `analyze_reaction_coordinate` | `internal_reaction_analysis` | 对齐路径图像和能量，给出相对能与最高图像候选 | 明确不自动宣称 TS 已验证 |
| `enumerate_coordination_isomers` | `internal_reaction_analysis` | 枚举 TBP、方锥和八面体中对称不等价的配体位点分配 | 不生成坐标，不虚构能量排序 |

同时修正了 `locate_transition_state` 的输入契约：单端 TS 定位不再虚假声明会消费反应物和产物双端点。

## 6. 已修复的问题

### 6.1 ORCA SMD

原实现生成的 ORCA 6 SMD 溶剂字段不正确，导致任务失败。已改为 ORCA 6.1.1 可接受的 `SMDsolvent "Ethanol"` 形式，并通过真实 ORCA 计算验证。

### 6.2 CPU 和同步运行上限

- ORCA 最大 `cpu_cores` 从原较小上限提高到 48；
- 同步 `walltime_seconds` 上限提高到 7200 秒；
- 54 核服务器上保留至少 6 核给系统、监控和并发调度。

真实 P2 HF/STO-3G 测试表明 2、4、8、16、32、48 核均正常且能量一致；该小任务中 32 核为 5.873 s，48 核为 6.052 s。因此“核数越多越快”不能作为固定规则，DLPNO 和大基组任务应先做 24–32 核的小规模扩展测试，再决定是否升到 48 核。

### 6.3 pysisyphus 双端路径

已修复或规避：

- 反应物和产物端点没有被真正消费；
- xTB、PySCF、ORCA calculator 构造不完整；
- CPU `pal` 与溶剂参数未传递；
- 多 XYZ 能量注释解析错误；
- Growing String 搭配 QuickMin 时节点增长导致历史数组维度错误，现要求 `optimizer=string`；
- pysisyphus 1.0.0 Freezing String CLI 向类构造器传入无效 `fix_first/fix_last`，现使用该版本实际类接口的受控驱动器；
- Freezing String 完全生长但力未收敛时返回明确的继续精修警告，不冒充已验证 TS。

### 6.4 审计配置

- 新 backend 已登记到 core runtime；
- Action–backend 覆盖清单更新为 111 Actions、77 Backends、246 个组合；
- 修复覆盖审计重复运行时会丢失历史真实 smoke 证据的问题；
- 当前为 241 个成功组合、5 个既有远端数据服务失败组合、0 个未观察组合。

## 7. 真实工具和软件调用

完整摘要：`docs/check/heterobiaryl_toolbox_repair/REAL_BACKEND_RUN_SUMMARY.json`。原始输入、stdout/stderr、生成配置、轨迹和 ORCA 输出保存在 `docs/check/heterobiaryl_toolbox_repair/outputs/`。

### 7.1 ORCA

| 输入/方法 | 核数 | 结果 |
|---|---:|---|
| 水，HF/STO-3G，SMD ethanol | 1 | 正常终止，E = -74.970047221478 Eh |
| 50 原子 P2 种子，+2/单重态，HF/STO-3G | 2/4/8/16/32/48 | 全部正常终止，能量在数值精度内一致；32 核为该 smoke 最快 |

该结果证明 SMD 语法和几十核调用可工作，但不证明 ωB97XD 或 DLPNO 的 P(V) 论文势垒已经得到。

### 7.2 pysisyphus/xTB

| Action | 方法 | 结果 |
|---|---|---|
| `search_reaction_path` | 5 图像 NEB，GFN2-xTB，ALPB ethanol，2 核 | 成功，双端点被消费并保存完整路径 |
| `search_reaction_path` | Growing String，GFN2-xTB，2 核 | 在修复优化器兼容性后成功，6 图像 |
| `search_reaction_path` | Freezing String，GFN2-xTB，2 核 | 路径完全生长；末端力未达到目标，正确标为需继续 TS 精修 |
| `scan_reaction_coordinates` | O–H 0.95→1.05 Å 松弛扫描，GFN2-xTB | 两点均收敛，结构与能量对齐保存 |

这些是小分子后端验证，不是 P(V) 路线的替代结果。

### 7.3 确定性分析 Action

- `enumerate_coordination_isomers`：对 OMe/Ph/Ph/PyH/PyH 的 TBP 配体标签得到 5 个对称不等价位点分配；
- `validate_reaction_path`：真实服务调用检查了三图像测试路径的端点和连续性；
- `analyze_reaction_coordinate`：从对齐能量识别最高能图像，同时保持 `transition_state_validated = false`。

### 7.4 GoodVibes

现有 GoodVibes 4.3 真实软件 smoke 为 7/7 通过，覆盖热化学、构象集合、选择性和反应剖面能力。本轮没有用作者输出给 P(V) 任务“回放答案”，也没有把 GoodVibes 后端可用等同于 P(V) 热化学已完成。

## 8. 六个科学问题的可行性和差距

### Q1：质子化效应

- 论文主要结论：P0/P1/P2 的 BiPy 势垒约 30/20/14 kcal mol⁻¹，逐次质子化降低势垒。
- 当前能做：筛选构象、生成三条映射路线、路径搜索、Gaussian TS/频率/IRC、ORCA SMD-DLPNO 单点、GoodVibes 353.15 K/1 M 后处理。
- 当前不能宣称复现的原因：没有完成三个电荷态的论文层级反应物/TS 优化、频率、双向连通性和匹配的 DLPNO 外推。
- 分类：`partially_solvable`。
- 需要补充：不是必需新增软件；需要执行完整长计算和驻点验证。若追求逐位小数与论文完全一致，还需锁定 ORCA 4.0.1.2、GoodVibes 2.0.1 及论文未完全公开的频率缩放/构象处理细节。

### Q2：Py–Py 与 Ph–Py 选择性

- 论文主要结论：P0/P1/P2 都动力学偏好 BiPy；P2 中 PhPy 产品更稳定也不能解释选择性。
- 当前能做：七个公开候选路线/对照方向、配位异构枚举、双端路径、驻点验证、反应物/产物/TS 统一热化学。
- 当前不能宣称复现的原因：尚未生成并验证全部 P0/P1/P2 的 PyPy、PhPy 反应物、TS 和产品集合；供体方向与构象分支仍有组合爆炸。
- 分类：`partially_solvable`。
- 需要补充：主要是作业编排、检查点恢复和长计算资源，而不是新的量化软件。产品端点生成 Action 会显著降低智能体直接写程序的负担。

### Q3：C–C 与 C–O 竞争

- 论文主要结论：P2 C–C/C–O 势垒约 14/18 kcal mol⁻¹，C–C 动力学更有利。
- 当前能做：输入公开了正确的 O–C 形成/P–O 断裂映射；可运行路径、扫描、TS/IRC、高层能量和热化学。
- 当前不能宣称复现的原因：没有作者产品/TS 坐标是有意设计；当前审计尚未从 bond edit 生成并验证 P2 C–O 产品端点和一阶鞍点，也没有形成同条件的两条自由能势垒。
- 分类：`partially_solvable`。
- 需要补充：新增“按原子映射和 bond edit 构造化学合理端点/复合物”的 typed Action 最有价值；直接编程目前可以完成，但需要智能体自己维护价态、质子和构象。

### Q4：偶联机理

- 论文主要结论：stepwise、asynchronous、apical-to-equatorial；形成 C–C 的同时主要削弱一条轴向 P–C，并形成 dearomatized 中间体。
- 当前能做：已新增路径搜索、坐标扫描、路径验证、键级/电荷/几何分析；Gaussian 可执行 Hessian 和 IRC。NBO 不是必需。
- 当前不能宣称复现的原因：尚无 P(V) 候选被精修为只有一个目标虚频并完成双向连接；concerted control 和 dearomatized minimum 也未得到论文级验证。
- 分类：`partially_solvable`。
- 需要补充：实际 P(V) 计算和多坐标路径编排。若只要求论文的定性氧参与结论，不需要新增 NBO；若要求精确 NBO 占据数，则必须另接 NBO 授权程序。

### Q5：决速步骤

- 论文主要结论：醇/烷氧负离子向 phosphonium P 加成为主要决速步骤；P(V) 内配体偶联决定选择性；后续塌陷强放能、近不可逆。
- 当前能做：处理相对速率 OMe 0.16、Me 0.37、H 1.00、Cl 1.89，计算下游 P2 偶联，并与 NMR 非检出、产物和 EtONa 观察分层整合。
- 当前不能宣称完整复现的原因：没有原始时间序列、FID 和测量不确定度；也没有完整的醇加成反应体系、抗衡离子/酸模型及所有候选决速步骤端点；本轮也未完成 P2 论文层级偶联势垒。
- 分类：`partially_solvable`。
- 需要补充：若目标只是复现论文论证，当前公开观察可用；若目标是独立动力学机制鉴定，需要原始动力学/NMR 数据和完整加成步骤结构定义。增加 CPU 不能补足这些数据。

### Q6：完整端到端

- 论文主要结论：汇总 Q1–Q5 的质子化、选择性、竞争路线、stepwise/asynchronous 机理和动力学角色分离。
- 当前能做：引导复现轨已经给出九条候选路线和完整方法层级，工具覆盖所有组成步骤。
- 当前不能宣称复现的原因：完整驻点网络、统一自由能面和 Q5 的数据受限部分尚未完成；一个成功路径不足以代表端到端结果。
- 分类：`partially_solvable`。
- 需要补充：长作业调度/恢复、产品端点生成、多坐标扫描和 CBS/热化学组合便利 Action；Q5 的原始实验数据仍是独立缺口。

## 9. 直接写程序调用软件能解决什么

直接编程入口足以绕过“预设 Action 没覆盖所有关键词或流程”的问题，例如：

- 写 Gaussian TS、IRC 或约束扫描输入；
- 写 ORCA 4/6 版本兼容的 `Extrapolate(2/3,cc)` 输入；
- 解析输出并做 cc-pV(DT)Z/CBS 组合；
- 组合 GoodVibes 或自定义热化学校正；
- 构造产品、插值路径或多坐标扫描。

但它不能自动解决：

- 缺失的反应物/产品化学定义；
- 不正确的电荷、质子、构象或原子映射；
- 没有收敛的一阶鞍点、错误虚频或错误 IRC 端点；
- 缺失的原始实验数据；
- 计算时间、内存和磁盘预算；
- 软件版本差异和结果 provenance。

因此本轮新增 Action 的目标不是否定直接编程，而是把高频、可验证的操作变成统一输入/输出和可审计失败语义；特殊路线仍允许智能体直接调用原生软件。

## 10. 后续建议的工具箱能力

这些能力会提高成功率，但在允许直接编程的前提下，大多不是绝对软件阻塞：

1. `build_reaction_endpoint`：按原子映射、成键/断键和质子变化生成受控端点，进行价态/电荷检查。
2. 多坐标 `scan_reaction_coordinates`：支持二维或耦合的成键/断键扫描，并输出可继续优化的候选。
3. 长作业 `submit/status/collect/resume`：支持超过当前 7200 s 同步上限的 Gaussian/ORCA 计算和失败恢复。
4. typed ORCA CBS：显式表达 SMD、DLPNO-CCSD(T)、`Extrapolate(2/3,cc)`、SCF/PNO 设置并解析外推分量。
5. 复现级能量组合：把驻点、频率热修正、高层单点、1 M 修正和构象集合按唯一 ID 组合，拒绝错配物种。
6. 反应网络完整性检查：确保所有被比较路径具有同口径反应物、TS、产品和失败记录。

## 11. 还需要用户准备什么

当前代码和任务结构不要求用户再提供软件安装；Gaussian 16、ORCA 6.1.1、GoodVibes 4.3、pysisyphus 和 xTB 已存在。

如要继续做完整论文级数值复现，需要用户确认或准备：

1. 允许长时间批处理的总计算预算、磁盘预算和失败重试策略；54 核可用，但建议以多个 24–32 核任务并行和单任务 32/48 核扩展测试相结合。
2. 是否接受 ORCA 6.1.1/GoodVibes 4.3 的版本兼容复现；若要求与 2018 年输出尽可能逐数值一致，需要保留 ORCA 4.0.1.2、GoodVibes 2.0.1 和当年的精确后处理设置。
3. 若 Q5 的目标升级为“从原始数据独立鉴定决速步骤”，需要原始动力学时间序列、测量误差、原始 NMR FID/检测限，以及醇加成步骤的完整反应物、质子/抗衡离子和产物定义。
4. 不建议把作者优化结构或计算输出加入开放探索轨；若它们只用于评分或离线校准，应继续保留在 hidden reference 中。

## 12. 验证状态

- 双轨任务结构测试：4/4 通过；
- 新反应路径 Action 专项测试：5/5 通过；
- Action/backend、MCP runtime 和新增 Action 联合回归：17/17 通过；
- Chemistry Toolbox 与任务结构全量回归：247/247 通过，耗时 344.73 s；
- Catalog 审计：111 Actions、77 Backends、246 pairs，241 success、5 远端失败、0 unobserved。

## 13. 相关文件

- 原六任务第一版审计：`docs/check/HETEROBIARYL_TASK_FEASIBILITY_AUDIT.md`
- 真实运行摘要：`docs/check/heterobiaryl_toolbox_repair/REAL_BACKEND_RUN_SUMMARY.json`
- 原始真实软件产物：`docs/check/heterobiaryl_toolbox_repair/outputs/`
- Action/backend 总审计：`chemistry_toolbox/docs/ACTION_BACKEND_COMPLETE_AUDIT_20260721.md`
- 工具/资源矩阵：`chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md`
- 双轨构建器：`scripts/build_heterobiaryl_pv_dual_track_tasks.py`
