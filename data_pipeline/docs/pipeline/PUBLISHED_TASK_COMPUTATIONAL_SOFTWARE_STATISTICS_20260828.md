# 批量合成已发布任务的计算软件统计

统计日期：2026-08-28（Asia/Hong_Kong）  
统计批次：`runs/stage0607-v28-gpt-5.6-sol-20260828-bulk582-p10`  
统计来源：`release/release_manifest.json` 与每个已发布任务私有的 `paper_route.md`

## 1. 统计范围

本次统计以该批次的 `release/release_manifest.json` 为准，而不是以 `papers/` 下的中间过程目录为准。当前发布快照包括：

- 258 篇唯一论文（按 `paper_id` 去重）；
- 497 个已发布任务模式，其中 `paper_reproduction` 255 个、`autonomous_research` 242 个；
- 每个任务目录下均有 `paper_route.md`，同一篇论文的两个模式共享同一条私有计算路线。

因此下面同时给出两种口径：

1. **按论文计数**：一篇论文只计一次，适合回答“有多少篇论文使用某软件”；
2. **按任务模式计数**：按 `task_type + paper_id` 计数，适合回答“有多少个发布任务使用某软件”。

一篇路线可能使用多个软件（例如 Gaussian 做几何优化、ORCA 做高层单点），所以各软件计数不能相加得到论文总数；它们是多标签统计。

## 2. 核心计算软件统计

这里的“核心计算软件”指在 `paper_route.md` 中承担电子结构计算、周期性 DFT、分子动力学或半经验量子化学计算的软件。软件只要在该路线中承担至少一个实质计算步骤，就计入；不要求它是路线中唯一的软件。

| 软件 | 唯一论文数 | 论文占比 | paper_reproduction 任务数 | autonomous_research 任务数 | 发布任务总数 | 任务占比 |
|---|---:|---:|---:|---:|---:|---:|
| Gaussian（含 Gaussian 09/16 等） | **191** | **74.0%** | **188** | **180** | **368** | **74.0%** |
| ORCA | 37 | 14.3% | 37 | 32 | 69 | 13.9% |
| VASP | 29 | 11.2% | 29 | 29 | 58 | 11.7% |
| xTB（含 GFN-xTB） | 10 | 3.9% | 10 | 10 | 20 | 4.0% |
| MOPAC | 3 | 1.2% | 2 | 3 | 5 | 1.0% |
| GROMACS | 4 | 1.6% | 4 | 4 | 8 | 1.6% |
| LAMMPS | 2 | 0.8% | 2 | 2 | 4 | 0.8% |
| CP2K | 2 | 0.8% | 2 | 2 | 4 | 0.8% |
| GAMESS | 1 | 0.4% | 1 | 1 | 2 | 0.4% |
| NAMD | 1 | 0.4% | 1 | 1 | 2 | 0.4% |
| Quantum ESPRESSO | 1 | 0.4% | 1 | 1 | 2 | 0.4% |
| ABINIT | 1 | 0.4% | 1 | 1 | 2 | 0.4% |
| CASTEP | 1 | 0.4% | 1 | 1 | 2 | 0.4% |
| ADF | 1 | 0.4% | 1 | 1 | 2 | 0.4% |
| Molcas/OpenMolcas | 1 | 0.4% | 1 | 1 | 2 | 0.4% |
| Psi4 | 1 | 0.4% | 1 | 1 | 2 | 0.4% |
| PySCF | 1 | 0.4% | 1 | 1 | 2 | 0.4% |

### Gaussian 的重点结论

- **按唯一论文计数：191/258 篇（74.0%）包含 Gaussian 核心计算。**
- **按发布任务模式计数：368/497 个任务（74.0%）包含 Gaussian 核心计算。**
- 其中 `paper_reproduction` 为 188/255，`autonomous_research` 为 180/242。两种模式的比例接近，说明模式转换没有改变论文路线的软件归属；任务模式数量略有差异是因为不是每篇论文都同时发布两个模式。
- 这 191 篇并不都“只使用 Gaussian”。其中一部分还结合 ORCA、xTB/CREST、Multiwfn、VMD 等工具；本统计回答的是“是否使用 Gaussian 作为核心计算软件”，不是“Gaussian 独占的任务数”。

## 3. 路线中出现的辅助/分析软件

下表不与上面的核心软件表相加。它们主要用于构象搜索、结构可视化、波函数/轨迹分析、后处理或建模；有些路线把它们作为计算工作流的重要组成部分，但它们不是本统计中“核心电子结构/MD 引擎”的主分类。

| 辅助或分析软件 | 唯一论文数 | 典型用途 |
|---|---:|---|
| Multiwfn | 35 | 波函数、轨道、QTAIM/NCI、空穴-电子分析等 |
| GaussView | 15 | Gaussian 输入/结构及轨道可视化 |
| VMD | 13 | 分子动力学轨迹和轨道/结构可视化 |
| CREST | 9 | 构象搜索和采样（通常与 xTB 联用） |
| NBO/NBO6 | 9 | NPA、键级、供受体相互作用分析 |
| GoodVibes | 5 | 准谐振热化学后处理 |
| Chemcraft | 3 | 结构建立和可视化 |
| Packmol | 3 | 溶剂/分子体系装箱 |
| PyMOL | 3 | 蛋白/分子结构建模和可视化 |
| Spartan | 3 | 分子力学或初始构象搜索 |
| ASE（Atomic Simulation Environment） | 2 | VASP 工作流编排和热力学后处理 |
| LOBSTER | 2 | 周期体系轨道/键合指标分析 |
| PLATON | 2 | 晶体几何参数分析 |
| Phonopy | 2 | 声子/有限位移分析 |
| Shermo | 2 | 热化学/振动后处理 |
| SpecDis | 2 | 光谱模拟与比较 |
| VESTA | 2 | 周期结构和晶体可视化 |
| AIMAll | 1 | QTAIM 分析 |
| AlphaFold2/ColabFold | 1 | 蛋白结构预测 |
| Amber/AmberTools | 1 | MD 参数化/分析生态（该路线的动力学主引擎另计 GROMACS） |
| AutoDock Vina | 1 | 分子对接 |
| Avogadro | 1 | 分子结构建立/初步建模 |
| BALLOON | 1 | 构象/分子力学建模 |
| CONFLEX | 1 | 构象搜索 |
| FCclasses3 | 1 | Franck–Condon/振动谱后处理 |
| KST48 | 1 | MECP/交叉点搜索（调用 Gaussian 计算） |
| MESS | 1 | 反应动力学主方程建模 |
| MSTor | 1 | 多参考/热化学后处理 |
| MaSK | 1 | 分子轨道/电荷可视化 |
| NCIPlot | 1 | 非共价相互作用分析 |
| Tinker | 1 | 分子力学构象扫描 |
| TDEP | 1 | 温度相关有效势/晶格动力学后处理 |
| VASPKIT | 1 | VASP 输出处理 |
| WebMO | 1 | Gaussian 计算的图形化入口 |
| py.Aroma | 1 | NMR/结构准备与分析 |
| sobEDA | 1 | 能量分解分析 |
| Chemkin-Pro | 1 | 反应机理/动力学模拟 |

注：力场、数值展宽、密度泛函名称不作为独立“计算软件”统计。例如 `AMBER14SB`、`GAFF`、`CHARMM36` 是力场，`Gaussian smearing`/`Gaussian broadening` 是数值展宽方法，不应被计为 Gaussian 软件。

## 4. 软件未识别情况

有 **1 篇论文**的 `paper_route.md` 没有写出具体软件名称：

- `paper_e8da3be56e9450b0`

该路线只说明了周期 BaTiO₃ 模型、独立弛豫和 Berry-phase 极化计算，没有公开具体软件。因此它被计入已发布论文总数，但不计入任何软件类别。这不是推断为“未使用软件”，而是“当前私有路线记录未给出软件名称”。

## 5. 识别规则与质量控制

统计脚本对每篇论文只读取一份 `paper_route.md`，避免两个任务模式导致重复计数。软件名称从路线中的 `Method/software` 字段及明确的计算步骤描述中识别。

Gaussian 使用了比简单关键词更严格的识别：

- 接受 `Gaussian 09`、`Gaussian 16`、`Gaussian09W`、`Gaussian DFT`、`Gaussian frequency`、`Gaussian single point`、`Gaussian ωB97X-D/...` 等明确计算语境；
- 排除 `Gaussian smearing`、`Gaussian broadening`、`Gaussian function/distribution`、`Gaussian width`、`Gaussian charges` 等非 Gaussian 软件语境；
- `GaussView` 单独统计为辅助软件，不会误计为 Gaussian 核心计算。

对于同时使用多个核心引擎的路线，各引擎均计 1 次。因此例如“Gaussian 优化 + ORCA 高层单点”的论文会同时出现在 Gaussian 和 ORCA 行中，这是有意保留的信息。

## 6. 统计局限性

1. 统计反映的是当前发布快照，不代表未来批量运行新增任务的最终软件分布。
2. 统计依赖 `paper_route.md` 的文字记录；如果路线文件没有写出软件名称，代码无法从任务指令或评估文件可靠反推，因此不会擅自猜测。
3. “核心软件”按路线中是否承担实质计算步骤判断；辅助工具和力场不与核心软件混为一谈。
4. 当前批次的 release 已完成，但批次包含少量失败论文；本统计只覆盖已经进入 `release/` 的已发布任务，不把未发布任务计入分母。

## 7. 一句话汇报版

在当前批量合成批次已发布的 258 篇论文、497 个任务模式中，Gaussian 是绝对主流：191 篇论文（74.0%）和 368 个任务模式（74.0%）将其作为至少一个核心计算步骤的软件；其次是 ORCA（37 篇）和 VASP（29 篇）。
