# ResearchChemBench 化学工具箱能力扩展总结报告

> 日期：2026-07-20
> 基线提交：`fd01f226cd31b6c0bf9e2420aec160a2a7bc76e6`
> 基线测试：`71 passed`
> 目标：用一个 MCP Server 暴露完整原子工具目录，由 Agent 自主选择动作、软件、方法、参数、组件、顺序、分支和停止条件。

## 1. 最终结论

本轮已经把工具箱从“以软件入口为中心”扩展为“科学动作与软件 Backend 多对多映射”的统一 Catalog。公开接口中没有增加 `run_ase`、`run_sharc`、`run_autode` 等流程型或软件型总入口，也没有自动 Backend 选择、自动模型选择或失败后自动回退。

| 指标 | 基线 | 当前 | 变化 |
|---|---:|---:|---:|
| 公开 Action | 45 | 101 | +56 |
| Scientific Action | — | 91 | — |
| Data Action | — | 10 | — |
| BackendSpec | 55 | 76 | +21 |
| 隔离运行环境 | — | 35/35 就绪 | — |
| 注册科学资源 | — | 27/27 可用 | — |
| Pytest | 71 passed | 146 passed | +75 tests |
| 用户指定软件/接口清单 | — | 59 项全部有明确状态 | — |

当前 101 个 Action 按类别分布为：结构与体系 18、化学信息学 6、科学数据交换 3、分子电子结构 16、反应与动力学 8、分子动力学 23、周期与声子 16、对接 1、数据源 10。

## 2. 与 Benchmark 目标的对应关系

### 2.1 一个 Server，完整目录

- 每个任务都收到同一套 101 个 Action，而不是由系统按任务筛选候选工具。
- MCP 只负责公开动作和执行 Agent 的精确请求，不负责规划工作流。
- 35 个 Runtime 只隔离依赖，不拥有或过滤公开工具。

### 2.2 Agent 保留科学决策权

- 数值 Action 要求 Agent 明确提交 `backend_id`。
- geomeTRIC、Sella 等组合 Backend 还要求 Agent 提交 `component_backends.calculator`，并为计算器提供独立方法与设置。
- 模型、赝势、POTCAR、基组、泛函、力场、温度、收敛阈值、采样长度等均由 Backend 专属 Schema 显式表达。
- MESS、MESMER、ShengBTE 接收 Agent 明确提供的原生模型文件，不替 Agent 构造反应网络、主方程模型或声子散射模型。
- Dispatcher 不排序候选、不补齐 Backend、不使用 `auto`、不在失败后切换到其他软件。

### 2.3 不是每个动作都需要复杂软件

确定性处理和数据查询继续作为原子动作存在。例如 QCSchema 校验、cclib 输出解析、PDB 文本处理、统计推导、PubChem/NIST 查询不需要伪装成大型计算软件。实际实现及版本仍会写入 provenance。

## 3. 新增的 56 个 Action

| 类别 | 数量 | 新增 Action |
|---|---:|---|
| 科学数据交换 | 3 | `normalize_qcschema_molecule`、`validate_qcschema_record`、`parse_quantum_chemistry_output` |
| 结构与体系 | 9 | `cluster_conformers`、`align_molecular_structures`、`select_structure_subset`、`renumber_biomolecular_structure`、`normalize_pdb_records`、`analyze_crystal_symmetry`、`standardize_crystal_structure`、`build_supercell`、`enumerate_surface_slabs` |
| 化学信息学 | 6 | `calculate_molecular_descriptors`、`calculate_molecular_fingerprint`、`calculate_molecular_similarity`、`search_local_substructures`、`enumerate_tautomers`、`enumerate_stereoisomers` |
| 数据源 | 5 | `resolve_chemical_identity`、`retrieve_compound_properties`、`retrieve_compound_structure`、`search_similar_compounds`、`search_substructures` |
| 分子电子结构 | 6 | `calculate_bond_orders`、`calculate_excited_states`、`derive_uv_vis_spectrum`、`analyze_electron_density_topology`、`calculate_atomic_basin_properties`、`calculate_bader_charges` |
| 周期与声子 | 8 | `calculate_electronic_band_structure`、`calculate_density_of_states`、`calculate_projected_density_of_states`、`calculate_harmonic_thermodynamics`、`calculate_phonon_group_velocities`、`calculate_lattice_thermal_conductivity`、`analyze_periodic_bonding`、`calculate_charge_spilling` |
| 分子动力学与自由能 | 16 | `calculate_force_field_energy`、`calculate_force_field_forces`、`decompose_force_field_energy`、`calculate_contacts`、`calculate_hydrogen_bonds`、`calculate_solvent_accessible_surface`、`calculate_dihedral_distribution`、`assign_secondary_structure`、`calculate_principal_components`、`calculate_dynamic_cross_correlation`、`cluster_trajectory`、`parse_alchemical_energy_data`、`estimate_free_energy_difference`、`estimate_thermodynamic_expectations`、`calculate_potential_of_mean_force`、`analyze_free_energy_convergence` |
| 反应与动力学 | 3 | `calculate_rate_constants`、`calculate_tunneling_correction`、`solve_master_equation` |

## 4. 新接入的 21 个 BackendSpec

| Backend | 当前公开能力 |
|---|---|
| `qcelemental` | QCSchema Molecule 规范化、记录校验 |
| `cclib` | 已有量化化学输出的选择性解析 |
| `pdb_tools` | PDB 选择、重编号、规范化 |
| `pymatgen` | 对称性、标准晶胞、超胞、表面 slab |
| `spglib` | 对称性与标准化 |
| `mdtraj` | RMSD、回转半径、接触、SASA、二面角、二级结构、聚类 |
| `pymbar` | 自由能差、期望值、PMF、收敛分析 |
| `alchemlyb` | 显式解析炼金自由能输入数据 |
| `nwchem` | 能量、力、Hessian、偶极矩、原子电荷 |
| `gpaw` | 分子/周期能量与力、应力、弛豫、能带、DOS、PDOS |
| `hoomd` | 势能最小化、单段动力学、力场能量与力 |
| `geometric` | Agent 组合的几何优化 |
| `sella` | Agent 组合的极小值优化和一阶鞍点搜索 |
| `critic2` | 电子密度拓扑、原子盆积分、Bader 电荷 |
| `lobster` | 周期成键、PDOS、charge/total spilling |
| `shengbte` | Agent 提供模型的晶格热导率求解 |
| `rmg` | 显式速率模型求值与 Wigner/Eckart 隧穿修正 |
| `mess` | Agent 提供 MESS 模型的主方程求解 |
| `mesmer` | Agent 提供 MESMER XML 模型的主方程求解 |
| `openmolcas` | HF/DFT SCF 能量、偶极矩、Mulliken 电荷、轨道 |
| `multiwfn` | Mulliken/Lowdin 电荷和 Mayer/Wiberg-Lowdin/Mulliken 键级 |

## 5. 已有软件的能力扩展

本轮没有把“一种软件只能对应一个动作”固化到架构中。已有综合软件也按其科学特点扩展了多种独立动作：

| 软件 | 新增或扩展能力示例 |
|---|---|
| RDKit | 描述符、指纹、相似性、子结构、互变异构、立体异构、构象聚类、显式原子映射对齐 |
| PubChem | 身份解析、属性、2D/3D 结构、相似性与子结构检索 |
| xTB | 力、偶极矩、原子电荷、Wiberg 键级 |
| PySCF | 解析力、Hessian、激发态，并可把激发态结果交给独立光谱推导动作 |
| ORCA | 力、电荷、轨道、键级、激发态 |
| OpenMM | 力场能量、力、按 Force object 分解能量 |
| MDAnalysis | 氢键、PCA、动态交叉相关矩阵等轨迹分析 |
| Phonopy/Phono3py | 声子热力学、群速度和热输运 |

## 6. 真实验证证据

| 软件/链路 | 有界真实验证 |
|---|---|
| OpenMolcas 25.10 | H2/STO-3G SCF 能量 `-1.1167593075 hartree`，同时解析偶极、电荷和轨道 |
| Multiwfn 2026.7.15 | H2 formatted checkpoint：Mayer 与 Wiberg-Lowdin 键级约 `1.00000001`，Mulliken 键级约 `0.83866316` |
| ShengBTE | 官方 Test-RTA 模型在 300 K 解析得到 `25.662 W m^-1 K^-1` |
| MESS | HCO 示例完成主方程计算并解析温度/压力相关速率表 |
| MESMER | H2O 最小 XML 示例完成并解析 phenomenological rate |
| Sella + xTB | 显式 calculator component 的一阶鞍点搜索链路成功；最终科学 TS 仍要求 Agent 另行调用 Hessian/振动与 IRC 验证 |
| NWChem | 能量、力、Hessian、偶极和电荷均通过真实 QCEngine/NWChem 计算 |
| GPAW | 分子能量/力与周期能量真实计算通过 |
| Critic2/LOBSTER | 真实密度、成键与投影输出解析通过 |
| 完整测试 | `146 passed in 396.22s`，JUnit 位于 `config/pytest_status.xml` |
| 通用烟雾 | 7/7 Action 调用成功；Catalog、Runtime、Handler 覆盖与旧 runner 清理检查全部通过 |

35 个 MCP Runtime 当前全部通过依赖与 Backend 健康检查。Sella 已从 KinBot 环境拆分到独立 `.tool_envs/sella`；KinBot 环境固定为 NumPy 1.26.4、JAX/JAXlib 0.4.35，`pip check` 无冲突。RMG 的三个旧包平台标记通过精确正则登记为已知例外，其他任何依赖问题仍会导致检查失败。

## 7. 为什么仍有已安装软件不作为公共 Action

| 类型/软件 | 当前状态 | 原因 |
|---|---|---|
| QCEngine、AiiDA、atomate2、jobflow | runtime-only 基础设施 | 它们负责执行或工作流持久化，不直接产生一个边界明确的科学结果；伪装成 Action 会把 Agent 的编排权重新交给系统 |
| CENSO、autodE、AutoMeKin、KinBot | runtime-only 工作流软件 | 顶层入口会隐藏构象、搜索、电子结构软件和终止条件等多步科学决策 |
| Arkane | partial | 入口和数据库存在，但导入/示例超过有界时限；不能用无限等待或文件存在冒充完成 |
| Wannier90、Yambo | runtime-only | 需要 Agent 明确提供上游波函数/数据库及新的原子 Action 契约；尚无版本匹配的有界端到端样例 |
| SHARC、Newton-X | runtime-only | 非绝热动力学必须显式描述态、耦合、跳跃算法和电子结构接口，不能暴露一个总运行器 |
| TheoDORE 2.5.0 | runtime-only 候选 | CLI 可用，但当前官网是 3.x 文档；需要版本匹配的 transition-density 样例和稳定的类型化输出解析 |
| VMD、VESTA | runtime-only/GUI | 适合可视化，不应把交互式 GUI 启动等同于科学 Action |
| EasySpin | partial | 文件已缓存，但合法 MATLAB Runtime 尚未安装 |

## 8. 59 项用户指定软件/接口的最终状态

| 状态 | 数量 | 内容 |
|---|---:|---|
| `configured` | 46 | 已安装/配置并通过对应探测；其中只有具备完整契约和验证的能力进入公共 Catalog |
| `partial` | 2 | Arkane、EasySpin |
| `specification` | 1 | QCSchema；它是数据规范，不是可执行软件 |
| `manual_required` | 9 | Q-Chem、Molpro、TURBOMOLE、CASTEP、CRYSTAL、WIEN2k、MATLAB、OpenEye、Schrödinger |
| `manual_api_review` | 1 | NIST CCCBDB，不存在公开文档化 REST/JSON API，因此不暴露 |

其中 Q-Chem、Molpro、TURBOMOLE、CRYSTAL、WIEN2k、OpenEye 已按用户决定禁用。Schrödinger 下载目录中的包已确认是 Dirac 视频编解码器，而不是商业化学套件。MATLAB 只缓存了官方安装介质，未使用或处理任何破解内容。

NIST Chemistry WebBook 已通过官方参数化 CGI 接入受限的单物种查询；CCCBDB 不做脆弱网页爬取。

## 9. 软件资料缓存

`.software_cache/documentation/` 当前包含：

- 104 条软件、算法或数据源记录；
- 128 个官方资料入口；
- 122 个成功下载的有界 HTML/PDF 快照；
- 13/13 个已登记本地软件包手册及 SHA-256；
- 6 个下载失败记录，均保留原始 URL 和错误原因。

| 资料源 | 失败原因 |
|---|---|
| GAMESS 注册下载页 | 本机 CA 链无法验证 |
| LOBSTER 官网 | TLS 连接错误；本地 5.1.0 用户手册、FAQ、CHANGELOG 已登记 |
| MATLAB 产品页 | HTTP 403；官方安装介质已缓存 |
| MESS 官网与 PDF | HTTP 403；官方 URL 和本地示例手册已登记 |
| WIEN2k 官网 | 访问超时 |

这些错误只表示本地网页快照未保存，不改变软件安装或 Action 验证状态。

## 10. 联网数据源状态

最后一次有界联网测试为 3/5 成功：RCSB PDB、Materials Project、NIST WebBook 成功；PubChem PUG REST 与 Catalysis-Hub 当时均返回 HTTP 503。对应 Adapter 的结构化测试均通过，因此这是外部服务瞬时可用性，不是本地配置缺失。Agent 调用失败时会收到原始结构化错误，系统不会偷偷换数据源。

## 11. 用户还需要做什么

当前 101 个 Action 和 76 个 Backend 不要求继续下载软件即可使用。只有在希望扩展下列可选能力时需要额外处理：

1. 若要启用 EasySpin，请提供合法 MathWorks File Installation Key 与 license 文件或许可证服务器信息。
2. 若以后决定启用已禁用商业套件，请分别提供真实安装包和有效许可证；不需要时保持禁用即可。
3. PubChem 或 Catalysis-Hub 出现 503 时稍后重试，不需要重新安装本地环境。
4. CCCBDB 不需要继续寻找 REST API；在没有官方文档化接口前保持不公开是正确状态。
5. Arkane 的剩余工作是修复有界运行时，而不是继续下载文件；可在后续单独处理。

## 12. 关键文档与重放命令

- 完整 Action/Backend Schema：`evaluation/mcp_tools/TOOL_CATALOG.md`
- 工具、Backend、资源与环境矩阵：`docs/tools/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md`
- 软件能力与候选能力矩阵：`docs/tools/CHEMISTRY_TOOLBOX_SOFTWARE_CAPABILITY_MATRIX.md`
- 59 项需求状态：`docs/tools/CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md`
- Runtime 状态：`docs/MCP_PROFILE_STATUS.md`
- Toolbox 状态：`docs/TOOLBOX_STATUS.md`

```bash
.toolbox_env/bin/python -m evaluation.mcp_tools.tool_manager validate
.toolbox_env/bin/python scripts/check_mcp_profile_envs.py --timeout-seconds 180
.toolbox_env/bin/python scripts/audit_requested_software.py --timeout-seconds 30
.toolbox_env/bin/python scripts/verify_toolbox.py --smoke
.toolbox_env/bin/python -m pytest -q --junitxml=config/pytest_status.xml
```

用户自建的 `docs/tools/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX copy.md` 未被读取、修改或纳入提交。
