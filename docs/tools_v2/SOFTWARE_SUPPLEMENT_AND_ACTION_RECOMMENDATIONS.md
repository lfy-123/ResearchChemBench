# Software Supplement and Action Recommendations

> 本文是软件扩展前的规划记录，不代表当前安装状态。已经实施的变化以
> [`CHEMISTRY_TOOLBOX_V2_CHANGE_SUMMARY.md`](CHEMISTRY_TOOLBOX_V2_CHANGE_SUMMARY.md) 为准。

更新时间：2026-08-05

## 推荐顺序

这里的“补充”要求同时满足：有明显 Benchmark 能力增量、能合法自动部署、能够设计成边界清晰且可评分的 Action。不是论文里常见的软件都必须加入。

| 顺序 | 软件 | 获取与许可 | 结论 |
|---:|---|---|---|
| 1 | AIRSS | [GPL-2.0，源码可直接下载](https://airss-docs.github.io/getting-started/installation/) | **优先加入**。先建立开源晶体结构搜索基线；CALYPSO/USPEX 不应先于它。 |
| 2 | TDEP | [MIT，源码可直接下载](https://github.com/tdep-developers/tdep) | **优先加入**。补齐有限温度有效力常数、非谐谱和热输运。 |
| 3 | ACPYPE | [GPL-3.0，conda/PyPI/GitHub 可下载](https://github.com/alanwilter/acpype) | **优先加入**。现有 AmberTools、OpenBabel、GROMACS 可直接形成可验证链路。 |
| 4 | pmx | [LGPL-3.0，源码可直接下载](https://degrootlab.github.io/pmx/) | **优先加入**。补齐炼金变换映射和 hybrid topology。 |
| 5 | gmx_MMPBSA | [GPL-3.0，源码可直接下载](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA) | **优先加入**。依赖现有 GROMACS 和 AmberTools；必须同时提供收敛/分解校验。 |
| 6 | SISSO | [Apache-2.0，源码可直接下载](https://github.com/rouyang2017/SISSO) | **加入**。适合检验特征构造、筛选、稀疏模型和外部验证的编排。 |
| 7 | gplearn | [BSD-3-Clause，PyPI/GitHub 可下载](https://github.com/trevorstephens/gplearn) | **加入作对照**。用同一数据划分与 SISSO 比较，不单独形成方向。 |
| 8 | MultiWell | [源码和实例可直接下载](https://multiwell.engin.umich.edu/downloads/) | **条件加入**。先核对分发条款，再补主方程 Action；当前 MESS/MESMER 已覆盖基础需求。 |
| 9 | VASPKIT | [免费非商业二进制](https://vaspkit.com/installation.html) | **低优先级**。大量功能依赖 VASP/POTCAR；当前 QE、ASE、pymatgen 已能覆盖多数公开 Benchmark。 |
| 10 | PyFrag 2019 | [开源代码与文档](https://pyfragdocument.readthedocs.io/) | **条件加入**。ORCA/Gaussian 路径可做 activation strain；高价值 ADF-EDA 受商业 AMS 限制。 |
| 11 | Progdyn | [公开 GitHub 源码](https://github.com/DanielSingleton/Progdyn) | **条件加入**。脚本式、主要绑定 Gaussian；先验证能否稳定改接现有 ORCA，再决定接入。 |
| 12 | BAGEL | [GPL-3.0+，源码可直接下载](https://github.com/qsimulate-open/bagel) | **按论文需求加入**。激发态已有 ORCA/OpenMolcas，只有多参考梯度/耦合任务足够多时才有增量。 |
| 13 | CALYPSO | [学术非商业免费，但需注册申请](https://iccms-calypso.github.io/CALYPSO-Fortran/_licence.html) | **只标记，不自动下载/分发**。取得授权后再配置。 |
| 14 | USPEX | [个人注册下载、禁止再分发](https://uspex-team.org/ru/uspex/downloads) | **只标记，不自动下载/分发**。取得授权后再配置。 |
| 15 | CFOUR | [非商业免费，但必须签许可协议](https://cfour.uni-mainz.de/) | **只标记**。现有 ORCA/Psi4 已覆盖常规任务；高精度 CC benchmark 出现后再申请。 |
| 16 | FHI-aims | [需签学术许可；官方列出自愿费用](https://fhi-aims.org/get-the-code-menu/license-academia) | **只标记**。不能作为可自由再分发依赖。 |
| 17 | NBO 7 | [购买许可证后下载](https://nbo7.chem.wisc.edu/) | **收费，不添加**。先使用 Multiwfn、IAO/IBO、Mayer/Wiberg 等现有开放分析。 |
| 18 | AMS/ADF | [商业许可与公开价格](https://www.scm.com/pricing-and-licensing/) | **收费，不添加**。PyFrag 的 ADF-EDA 路线随之不纳入默认工具链。 |
| 19 | TURBOMOLE | [商业学术许可证](https://store.turbomole.org/product/turbomole-8-0-academic/) | **收费，不添加**。CENSO 已改为 ORCA backend。 |
| 20 | Q-Chem | [商业许可证与公开价格](https://www.q-chem.com/purchase/pricing/) | **收费，不添加**。 |
| 21 | TeraChem | 专有商业软件 | **收费，不添加**；GPU 量化能力已有可替代路线。 |
| 22 | COSMOtherm | [BIOVIA 商业产品](https://www.3ds.com/products/biovia/cosmo-rs/cosmotherm) | **收费，不添加**。 |

结论：下一轮真正值得实施的是 `AIRSS -> TDEP -> ACPYPE -> pmx -> gmx_MMPBSA -> SISSO/gplearn`。其余软件先由论文池中不可替代任务的数量触发，不应为了扩大软件数量而加入。

## 建议新增 Actions

Action 应是可组合的科学原子操作，输入、输出、质量指标明确；完整论文路线由 Agent 编排，不做一个覆盖整篇论文的巨型 Action。

| 优先级 | Action | 后端 | 关键输入 | 可评分输出与质量门槛 |
|---:|---|---|---|---|
| P0 | `generate_crystal_structure_candidates` | AIRSS | composition、cell/volume constraints、symmetry、seed、candidate count | 去重结构、enthalpy/rank、失败率、随机种子与 provenance |
| P0 | `fit_temperature_dependent_force_constants` | TDEP | snapshots、forces、temperature、cutoff/order | force constants、fit error、held-out error、对称性检查 |
| P0 | `analyze_finite_temperature_phonons` | TDEP | force constants、q path/mesh、temperature | dispersion/DOS/linewidth/thermal data、虚频和收敛标志 |
| P0 | `convert_amber_topology_to_gromacs` | ACPYPE | prmtop/inpcrd 或 molecule、charge method、GAFF version | `.top/.gro`、原子映射、电荷和拓扑一致性、GROMACS `grompp` 验证 |
| P0 | `build_alchemical_hybrid_topology` | pmx | state A/B、mapping、force field、mutation type | hybrid structure/topology、映射、未参数化项、端点能量一致性 |
| P0 | `analyze_mmgbsa_binding_energy` | gmx_MMPBSA | topology、trajectory、frame selection、GB/PB model | 总能与分项、逐残基分解、block/bootstrap uncertainty、帧数 |
| P1 | `discover_sparse_symbolic_descriptor` | SISSO | features、target、units、train/validation split、operator set | 方程、维度、CV/holdout metrics、复杂度和稳定性 |
| P1 | `fit_symbolic_regression_baseline` | gplearn | 与 SISSO 相同的数据划分、operators、seed | 方程、holdout metrics、复杂度、跨 seed 方差 |
| P1 | `solve_multichannel_master_equation` | MultiWell | wells/channels、DOS、microcanonical rates、energy transfer、T/P grid | phenomenological rates、branching、mass balance、T/P sensitivity |
| P1 | `run_post_transition_state_trajectory_ensemble` | Progdyn 或替代实现 | TS Hessian、temperature、sampling、step、stop criteria、seed set | trajectory ensemble、recrossing、product assignment、branching CI |
| P1 | `analyze_activation_strain_profile` | PyFrag/开放解析器 | reaction path、fragment definitions、single-point results | strain/interaction profiles、fragment consistency、路径覆盖 |
| P1 | `prepare_nonadiabatic_dynamics_ensemble` | SHARC/Newton-X | states、initial-condition sampling、electronic backend、seed set | 可执行 ensemble、状态/耦合检查、完整 provenance |
| P1 | `analyze_nonadiabatic_trajectory_ensemble` | SHARC/Newton-X | trajectories、state mapping、time window | populations、hop statistics、lifetimes、失败轨迹与不确定度 |

## 不建议设计的 Actions

- 不提供任意 shell/input runner；原生软件作业仍由受限 native-job 接口承载。
- 不提供 `reproduce_paper`、`run_full_reaction_study` 之类巨型 Action；它们会吞掉需要评估的规划与纠错能力。
- 不把“程序正常退出”当科学成功。结构搜索要去重和收敛，声子要检查虚频，MD/自由能要报告不确定度，主方程要检查守恒与参数敏感性。
- 不实现 CCCBDB scraper。若任务需要某个参考量，应优先从论文/SI、NIST WebBook 或题目随附数据获得，并记录来源。
