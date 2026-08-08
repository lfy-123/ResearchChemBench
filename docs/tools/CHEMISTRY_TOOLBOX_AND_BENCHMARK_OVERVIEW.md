# ResearchChemBench 化学工具箱与十方向建设总览

更新：2026-08-06

## 1. 核心结论

- 当前工具箱适合评估多阶段计算化学工作流，但“软件已注册”不等于“完成过科学计算验证”。
- 最适合建设 Benchmark 的十个方向见第 3 节；其中反应机理、构象、周期表面、电子密度最适合首批落地。
- 当前最重要的能力缺口是：晶体结构搜索、炼金自由能拓扑、有限温度非谐声子、符号描述符发现和反应后过渡态动力学。
- 先修复已有软件，再补开放软件；商业软件只在入选论文必须精确复现时接入。

## 2. 当前工具箱状态

### 2.1 能力规模

| 项目 | 数量 | 含义 |
|---|---:|---|
| Predefined Actions | 146 | 可组合的原子科研步骤 |
| BackendSpecs | 89 | Action 可调用的计算后端 |
| 原生软件指南 | 63 | 智能体可直接操作的软件入口 |
| Programmable runtimes | 47 | Python/R 等可编程分析环境 |

除既有核心链路外，本轮还完成了 RMG/Arkane、CENSO/ORCA、SHARC/ORCA、Newton-X/ORCA、QE/Wannier90、QE/Yambo、LOBSTER、Critic2 和 Multiwfn 的真实或有结果证据的 smoke。正式出题前仍应针对具体论文协议验证输入规模、数值收敛和评分容差。

### 2.2 当前运行边界

- 当前请求清单为 58 项：57 项 `configured`，QCSchema 作为规范记为 `specification`；没有 `partial` 或 `not_found` 项。
- 本轮新增 AIRSS、TDEP、ACPYPE、pmx、gmx_MMPBSA、SISSO、gplearn、PyFrag 和 BAGEL；VASPKIT 只允许本机非商业使用且禁止再分发。MultiWell、Progdyn 因无明确软件许可证未加入。
- MATLAB、EasySpin、Q-Chem、Molpro、TURBOMOLE、CASTEP、CRYSTAL、WIEN2k、OpenEye 和 Schrodinger Suite 已按要求从活动工具箱中移除，不再称为“当前不可用软件”。
- AiiDA 的同步本地执行可用；RabbitMQ/daemon 未启用，仅 daemon-backed `submit` 等后台工作流受限。
- VESTA 依赖已补齐并通过 Xvfb 有界启动；它是可视化工具，不是计算求解器，交互模式仍需要显示环境。
- CCCBDB 未接入；受控参考数据查询由 NIST WebBook Action 提供。新旧工具箱差异及迁移边界见 `docs/tools_v2/CHEMISTRY_TOOLBOX_V2_CHANGE_SUMMARY.md`。

## 3. 十个 Benchmark 方向

“当前覆盖率”是前期文献样本中软件实例的精确名称覆盖率，只用于判断缺口，不代表任务已经能够端到端完成。

| 顺序 | 方向 | 适合评估的计算链 | 当前主工具 | 当前覆盖率 | 最优先补充 |
|---:|---|---|---|---:|---|
| 1 | 反应机理、势能面与选择性 | 构象搜索 → DFT → TS → 频率/IRC → 自由能与选择性 | CREST/xTB、Gaussian/ORCA、pysisyphus、GoodVibes、Multiwfn | 17/30，57% | Progdyn、PyFrag |
| 2 | 构象系综、热化学与性质标定 | 构象搜索 → 聚类 → 优化/频率 → Boltzmann 加权 → 性质 | CREST、CENSO、xTB、Gaussian/ORCA、GoodVibes | 18/27，67% | 暂无阻断缺口；后补 NBO、CFOUR |
| 3 | 周期表面吸附、反应与成键 | slab/位点枚举 → 周期弛豫 → 吸附能 → DOS/成键 | VASP/QE/GPAW、ASE/pymatgen、LOBSTER、Critic2 | 10/11，91% | VASPKIT |
| 4 | 电子密度、QTAIM 与成键 | 波函数/密度 → 网格/QTAIM/COHP → 成键结论 | Gaussian/ORCA/VASP、Multiwfn、Critic2、LOBSTER | 20/24，83% | 先补科学 smoke；后补 NBO |
| 5 | 动力学、主方程与微观动力学 | 驻点/热化学 → 速率 → 主方程/微观动力学 → 分支比 | MESS、MESMER、CatMAP、Cantera、RMG/Arkane | 20/28，71% | MultiWell；补主方程科学 smoke |
| 6 | 激发态、光谱与光化学 | 激发态 → 交叉点/耦合 → 动力学或谱图 → 机理 | ORCA、OpenMolcas、SHARC、Newton-X、TheoDORE | 13/22，59% | 补 typed Actions；后补 BAGEL |
| 7 | 高压结构与多相稳定性 | 结构搜索 → 压力 DFT → 焓/声子 → 相图 | VASP/QE、Phonopy、LOBSTER、Critic2 | 22/30，73% | CALYPSO/USPEX/AIRSS、TDEP |
| 8 | 声子、非谐性与热输运 | 位移超胞 → 力 → 力常数 → 色散/热导率 | Phonopy/Phono3py、VASP/QE、ShengBTE | 26/33，79% | TDEP、thirdorder 工作流 |
| 9 | 分子动力学、增强采样与自由能 | 建模 → 平衡 → 采样/炼金变换 → 收敛与自由能 | GROMACS/LAMMPS/NAMD、PLUMED、PyMBAR、alchemlyb、Antechamber | 30/41，73% | pmx、ACPYPE、gmx_MMPBSA |
| 10 | 描述符发现与催化剂设计 | 数据/电子结构 → 特征 → 筛选/回归 → 外部验证 | VASP/QE、ASE/pymatgen、LOBSTER、scikit-learn | 18/23，78% | VASPKIT、SISSO、gplearn |

## 4. 软件补充顺序

### P0：完善现有软件的科学验证

1. RMG/Arkane、SHARC/Newton-X 等本轮故障已修复；继续补 MESS/MESMER、Phonopy/ShengBTE 和 GROMACS/PLUMED/PyMBAR 的端到端科学 smoke。
2. 把已验证的跨软件链路封装成边界清楚、参数显式且可评分的 typed Actions。

### P1：优先新增

| 顺序 | 软件 | 主要补齐能力 |
|---:|---|---|
| 1 | CALYPSO/USPEX，并评估 AIRSS | 未知晶体结构搜索 |
| 2 | pmx | 炼金自由能原子映射与混合拓扑 |
| 3 | ACPYPE | AmberTools/Antechamber 到 GROMACS 的拓扑转换 |
| 4 | gmx_MMPBSA | GROMACS 结合自由能与能量分解 |
| 5 | TDEP | 有限温度非谐声子 |
| 6 | MultiWell | 主方程求解路线扩展 |
| 7 | VASPKIT | 周期计算批处理与后处理 |
| 8 | SISSO | 稀疏符号描述符发现 |
| 9 | gplearn | 可比较的符号回归路线 |
| 10 | Progdyn | 后过渡态动力学和反应分岔 |
| 11 | PyFrag | Activation strain/EDA 分析 |

### P2：已有替代路线，按任务量补充

12. `BAGEL`
13. `NBO`
14. `ADF/AMS`
15. `FHI-aims`
16. `TURBOMOLE`
17. `Q-Chem`
18. `TeraChem`
19. `CFOUR`
20. `COSMOtherm`

`CASTEP`、`WIEN2k`、`DMol3`、`Molpro`、`CATKINAS`、`GENESIS`、`AIMAll`、`NCIPLOT`、`Desmond/FEP+` 只在最终论文池出现不可替代需求时接入。

## 5. 论文筛选标准

### 5.1 必须满足

- 论文和补充材料内包含可重建的输入结构、方法、关键参数、计算路线、中间结果和最终结论，不依赖未公开数据集。
- 至少包含 3 个相互依赖的计算阶段，或 2 类软件/Action family。
- 存在可评分的验证门或结果：虚频、IRC、收敛性、结构、相对能、自由能、速率、谱峰、热导率、相变压力等。
- 计算规模能在 Benchmark 预算内完成，或可构造不改变科学逻辑的缩小版本。
- 软件满足 `exact reproduction` 或 `method-equivalent reproduction`，且许可证允许自动执行。

### 5.2 优先排除

- 单软件、单结构、单点能等缺少编排价值的任务。
- 依赖未公开轨迹、模型、数据库或人工 GUI 操作的论文。
- 只能比较图片、缺少数值和结构化中间证据的论文。
- 主要贡献是新软件/新方法本身，无法由现有工具独立复现的论文。
- 计算量过大且不能合理缩小的高通量或长时间尺度任务。

## 6. 两种评估模式

| 模式 | 给智能体的信息 | 主要评分内容 |
|---|---|---|
| 论文路线复现 | 输入、论文方法、参数和路线 | 工具/后端选择、参数一致性、跨软件传递、必要验证、结果与论文误差 |
| 自主科研求解 | 科学问题、输入和起始观测；隐藏路线与结论 | 假设覆盖、实验/计算规划、失败识别、路线修正、证据充分性和最终发现可靠性 |

自主模式不要求复现作者的动作序列，应评分科学状态、必要证据和结论；复现模式才严格评分协议一致性。

每个任务记录三种软件可行性：

- `exact_reproduction_supported`：原软件可合法调用。
- `method_equivalent_supported`：软件不同，但方法和科学目标可等价复现。
- `blocked_by_unique_software`：缺少不可替代步骤，暂不纳入。

## 7. 建设顺序

1. Pilot：反应机理、构象、周期表面、电子密度，每方向先做双模式小样本。
2. 第一版：加入动力学、激发态、高压方向。
3. 第二版：加入声子、MD/自由能、描述符发现。
4. 最终论文池确定后，再根据真实频次处理商业软件许可证。
