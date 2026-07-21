# ResearchChemBench 化学工具箱详细审计与汇报报告

> 审计日期：`2026-07-20 UTC`；报告生成时间：`2026-07-20T18:02:15.472734+00:00`。
> 本报告统计的是当前工作区实际 Catalog、隔离运行环境、逐 Action 调用记录、真实后端 smoke、在线数据源现场状态和全量回归测试。

## 1. 执行结论

### 1.1 最重要的数字

| 指标 | 结果 | 解释 |
|---|---|---|
| 公开 Actions | **101** | 91 个 Scientific Actions + 10 个 Data Actions |
| 本轮逐 Action 已触发 | **101/101** | 每个公开 Action 至少进入过真实统一分发器一次 |
| 当前现场端到端成功 | **94/101** | 91 个本地 Scientific Actions + 3 个在线 Data Actions |
| 当前受外部服务影响 | **7** | 全部是在线数据源；本地 Scientific Action 为 0 个失败 |
| 至少存在一次成功证据 | **95** | 包含单元/契约测试与真实 smoke；`search_compounds` 契约测试成功但当前 PubChem 现场失败 |
| 完全没有成功证据 | **6** | 5 个扩展 PubChem Action + Catalysis-Hub |
| 注册 BackendSpecs | **76** | 71 个本地执行提供者 + 5 个在线数据服务 |
| 后端健康检查可用 | **76/76** | 加载 `config.local.env` 后模块、命令、模型与凭据检查均可用 |
| 有成功调用证据的后端 | **75/76** | 仅 Catalysis-Hub 本轮没有成功证据 |
| 当前现场成功的后端 | **74/76** | 全部 71 个本地后端 + RCSB PDB、Materials Project、NIST WebBook；PubChem/Catalysis-Hub 当前降级 |
| Action–Backend 候选组合 | **233** | Catalog 中声明的全部组合 |
| 已成功实测组合 | **165** | 至少一次成功/部分成功 |
| 仅有失败证据的组合 | **6** | 5 个扩展 PubChem 组合 + 1 个 Catalysis-Hub 组合；`search_compounds` 另有契约成功证据但当前在线失败 |
| 尚未逐组合实测 | **62** | 多数是同一 Action 的替代软件后端；不能宣称 233 个组合全部通过 |
| 全量回归 | **146/146 passed** | 用时 381.825 秒；failures+errors=0 |
| MCP 隔离运行环境 | **35/35 ready** | 每个后端按 runtime profile 隔离依赖 |
| 注册科学资源 | **27/27** | 赝势、基组、模型等资源校验 |
| 用户要求的软件清单 | **59 项** | configured=46；partial=2；manual/review=10；specification=1 |

### 1.2 能否说“所有工具都正常运行”

不能不加限定地这样说。准确表述是：

- **本地 Scientific Actions：91/91 至少有一个代表性后端成功执行。**
- **本地 BackendSpecs：71/71 至少有一个真实 Action 成功执行。**
- **在线 Data Actions：3/10 当前现场成功，7/10 受服务端 503 或超时影响。**
- **所有 101 个 Action 都已触发和记录状态，但不是所有 233 个 Action–Backend 组合都逐一运行。** 当前还有 62 个替代后端组合没有本轮运行证据。
- 当前 smoke 证明的是接口、调度、输入生成、程序执行和主要输出解析链路可工作；它**不是**对所有方法、元素、体系尺度、收敛参数和科学精度的穷尽验证。

## 2. 测试方法与证据层级

本次采用四层证据，避免把“命令存在”与“科学 Action 可用”混为一谈：

1. **Catalog/契约层**：校验 ActionSpec、BackendSpec、必填输入、方法字段、设置字段、禁止 `auto` 和禁止自动 fallback。
2. **分发层**：所有记录均经过 `researchchem_toolbox.service.execute_action`，验证智能体的选择被原样执行。
3. **真实后端 smoke 层**：运行量化程序、MD 引擎、材料程序、机器学习势、反应动力学软件和数据接口，并检查主要结果或产物文件。
4. **全量回归层**：`pytest` 共 146 项全部通过，覆盖契约、适配器、安全约束、资源注册与部分真实/模拟输出解析。

| 证据文件 | 结果 | 作用 |
|---|---|---|
| `config/action_test_coverage.json` | 95 success-evidence / 6 failure-only | 汇总逐 Action 与 Action–Backend 组合 |
| `config/action_gap_smoke_status.json` | 19/25 passed | 补齐 IRC、CatMAP、PLUMED、MDAnalysis、Phonopy、Cantera 等 Action；另做在线复测 |
| `config/backend_gap_smoke_status.json` | 18/18 passed | 补齐 17 个此前仅健康检查的本地后端，并追加 PySCF 单点能组合复核 |
| `config/scientific_resource_smoke_status.json` | 24/24 passed | 真实赝势、基组、模型、周期程序和 GNINA/ORCA 等资源 smoke |
| `config/data_source_smoke_status.json` | 3/5 passed | 在线数据源现场状态 |
| `config/pytest_status.xml` | 146/146 passed | 最终全量回归，381.825 秒 |

### 2.1 本轮真实补测的软件后端

以下 18 个补缺用例在本轮全部通过统一 MCP Action 分发链路：

`amber_pmemd`, `charmm`, `chgnet`, `cp2k`, `crest`, `gamess`, `gaussian`, `goodvibes`, `gromacs`, `lammps`, `mace`, `namd`, `openbabel`, `psi4`, `pyscf`, `rdkit_gasteiger`, `tblite`, `vina`

此外，CatMAP 0.3.1 和 Pysisyphus IRC 在补测过程中发现并修复了真实适配问题：

- Pysisyphus 现在分别适配 XTB 与 PySCF：`gfn2` 等方法会正确映射为 XTB 的 `gfn` 参数，HF/DFT/MP2 会按 PySCF 的 method/xc/basis 语义生成输入；两条链路都以 HCN 异构化过渡态成功生成 IRC 路径。反应运行环境已固定加入 `pyscf==2.13.1`。
- CatMAP 不再直接使用未初始化的 `ReactionModel()`；现在由类型化字段生成受控 `.mkm` setup 文件，再调用官方 `ReactionModel(setup_file=...)`，CO 氧化微观动力学模型成功返回 rate/coverage/production-rate maps。
- PLUMED driver 现在支持显式 `box_angstrom`、`timestep_ps` 和 `trajectory_stride`，真实集体变量计算通过。

## 3. 工具箱如何工作：Action 流程与智能体自由度

```text
科学任务
  ↓ 智能体自行判断当前需要的原子科学动作
选择 Action
  ↓ 智能体显式选择 backend_id / source_id / component_backends
填写 inputs + method_spec + action_settings + resource_limits
  ↓ 统一分发器做契约、必填字段、兼容性和健康检查
隔离 runtime worker
  ↓ 仅执行智能体所选的软件与参数；automatic_fallback_count = 0
类型化 ActionResult
  ├─ result：主要科学结果
  ├─ output_artifacts：可传给后续 Action 的文件/对象
  ├─ provenance：Action、后端、方法、设置、资源、命令和 Catalog hash
  └─ warnings/error：结构化状态
  ↓
智能体读取结果后，自主决定下一次调用哪个 Action/软件
```

关键设计原则：

- 不公开 `run_ase`、`run_orca`、`run_workflow` 这类笼统流程工具。
- Scientific Action 默认要求智能体明确给出 `backend_id`；禁止 `backend_id=auto`。
- 组合动作要求智能体明确选择组件后端，例如优化器与能量/梯度计算器。
- 系统不替智能体选择理论方法、基组、泛函、力场、赝势、模型权重或流程顺序。
- 运行时只负责机械隔离、资源限制与精确执行，不进行科学 fallback。

### 3.1 典型但非固定的智能体编排示例

这些只是可能的调用图，不是工具箱内置流程：

- 分子热化学：`standardize_structure → generate_3d_structure → generate_conformer_ensemble → optimize_geometry → calculate_energy → calculate_hessian → derive_vibrational_modes → derive_thermochemistry`。每一步的软件和是否继续均由智能体决定。
- 反应速率：`locate_transition_state → calculate_hessian → derive_vibrational_modes → trace_intrinsic_reaction_coordinate → calculate_tunneling_correction → calculate_rate_constants`。
- 分子动力学：`assign_protonation_states → assign_partial_charges → assign_force_field_parameters → solvate_molecular_system → minimize_system_energy → propagate_dynamics → trajectory/free-energy Actions`。
- 周期材料：`standardize_crystal_structure → relax_periodic_structure → electronic structure Actions`，或 `generate_displaced_supercells → 外部力计算 → assemble_force_constants → phonon/thermal Actions`。
- 对接：智能体先自行准备受体/配体与搜索盒，再调用 `dock_ligand`，之后自行选择结构或轨迹分析工具。

## 4. 化学领域覆盖情况

| 领域 | Action 数 | 当前现场成功 | 当前降级 | 覆盖评价 |
|---|---:|---:|---:|---|
| 科学数据与格式互操作 | 3 | 3 | 0 | QCSchema 规范化/验证与主流量化输出解析，适合作为跨软件数据桥。 |
| 结构与体系准备 | 18 | 18 | 0 | 分子、蛋白 PDB、晶体、超胞、表面、质子化、电荷、力场和溶剂化准备较完整。 |
| 化学信息学 | 6 | 6 | 0 | 描述符、指纹、相似性、子结构、互变异构和立体异构覆盖常用基础操作。 |
| 分子电子结构与派生性质 | 16 | 16 | 0 | 基态能量/力/Hessian/优化及部分电荷、轨道、键级、激发态、电子密度和光谱派生，基础骨架较强。 |
| 反应路径、热力学与动力学 | 8 | 8 | 0 | TS、IRC、平衡、网络积分、速率、隧穿、主方程和微观动力学均有原子 Action。 |
| 分子动力学、轨迹与自由能 | 23 | 23 | 0 | 体系执行、轨迹分析、集体变量、MBAR/PMF 与炼金数据解析覆盖广，但高级采样生成仍不足。 |
| 周期材料、电子结构、声子与热输运 | 16 | 16 | 0 | 周期能量/力/应力/弛豫、能带/DOS、LOBSTER、声子和晶格热导形成完整基础链。 |
| 分子对接 | 1 | 1 | 0 | 具备 Vina/GNINA 对接核心动作，但受体/配体专用准备和高级重打分尚不完整。 |
| 外部化学数据源 | 10 | 3 | 7 | PubChem、RCSB、Materials Project、Catalysis-Hub、NIST WebBook；当前 PubChem/Catalysis-Hub 现场降级。 |

### 4.1 当前尚未或覆盖较弱的方向

| 方向 | 当前缺口 | 建议新增的原子 Action 方向 |
|---|---|---|
| 多参考与高阶相关电子结构 | 缺少 CASSCF/CASPT2/NEVPT2、CC/EOM-CC 等统一类型化动作 | `calculate_multireference_states`、`calculate_correlated_energy`、`calculate_eom_excited_states` |
| 非绝热动力学与光化学 | SHARC、Newton-X 已安装但仍是 runtime-only；缺少态耦合、初态采样、surface hopping | `sample_excited_state_initial_conditions`、`calculate_nonadiabatic_couplings`、`propagate_nonadiabatic_dynamics` |
| 光谱广度 | 已有 IR/UV-Vis；缺 Raman、NMR、EPR、XAS/XES、圆二色等 | 独立性质计算与独立谱线构造 Actions |
| QM/MM 与嵌入 | 尚无显式 QM 区/MM 区、边界、嵌入电荷和耦合设置 | `build_qmmm_partition`、`calculate_qmmm_energy_forces`、`propagate_qmmm_dynamics` |
| 高级自由能与增强采样 | 有 CV 评估、MBAR/PMF；没有 metadynamics、umbrella window 执行、重加权和采样收敛执行动作 | `propagate_enhanced_sampling`、`run_umbrella_sampling_window`、`reweight_biased_trajectory` |
| 自动反应发现 | AutoMeKin、KinBot、autodE、CENSO 等部分已安装但没有作为单一粗粒度 workflow 暴露 | 应拆成候选生成、路径搜索、过滤、精修、网络扩展等原子 Actions |
| 电化学/电催化 | 缺恒电位、溶剂/电极界面、CHE、电荷补偿和电势扫描 | 显式电极模型、potential/charge scan、表面反应自由能 Actions |
| 周期多体与拓扑材料 | Yambo、Wannier90 已安装但 runtime-only；缺 GW/BSE、激子、Wannier、Berry/拓扑性质 | `calculate_quasiparticle_energies`、`calculate_exciton_properties`、`construct_wannier_functions`、`calculate_berry_phase_properties` |
| 缺陷、相图、吸附与催化结构搜索 | 目前只有晶体/超胞/slab；缺点缺陷枚举、相稳定性、吸附位点和吸附能专门动作 | `generate_defect_structures`、`calculate_phase_diagram`、`identify_adsorption_sites`、`calculate_adsorption_energy` |
| 动力学网络生成与 KMC | 可积分已有网络，但不生成网络，也没有 KMC | `generate_reaction_candidates`、`expand_reaction_network`、`run_kinetic_monte_carlo` |
| 聚合物、粗粒化和介观模拟 | 仅通用 MD 基础，无聚合物构建、粗粒化映射和 dissipative/mesoscale 动作 | 体系构建、映射、粗粒化参数化与传播 Actions |
| 不确定度与可重复比较 | 有 provenance，但缺模型不确定度、方法集成、跨后端一致性和参考数据比较 | `estimate_model_uncertainty`、`compare_backend_results`、`validate_against_reference` |
| HPC/调度与分布式执行 | runtime 隔离已完成，但没有把 Slurm/队列、批量任务依赖作为科学 Action | 保持与科学 Action 解耦，未来增加机械执行/作业管理层 |

### 4.2 是否满足“绝大多数计算化学需求”

结论取决于“需求”的边界：

- 对**计算化学 benchmark 的基础与中等难度任务**，当前 101 个 Actions 已经形成很强的通用骨架：结构准备、基态量化、周期 DFT、声子、经典 MD、轨迹分析、自由能估计、反应速率/主方程、数据检索和对接都能由智能体自由组合。
- 对**整个计算化学领域的生产级全部需求**，答案仍然是否定的。高级多参考/非绝热、QM/MM、增强采样执行、电化学、GW/BSE/Wannier、KMC、缺陷/相图、聚合物/粗粒化和广谱学仍明显不足。
- 因此更准确的汇报措辞是：**当前工具箱能覆盖大量常见计算化学任务和多软件编排能力，但还不能代表整个计算化学领域的全面生产工具链。**

## 5. 逐 Action 详细清单

状态说明：`✅` 表示当前代表性端到端成功；`⚠️` 表示代码/契约存在，但当前官方在线服务失败。候选后端中列出的“曾失败后已成功”表示早期/不同输入尝试失败、但该组合后来已有成功证据；“仅有失败记录”才计入 7 个失败组合；“未逐组合验证”不等于不可用，只表示本轮没有为该 Action–Backend 组合留下成功记录。

| # | Action | 领域 | 功能 | 输入 → 主要输出 | 智能体选择权 | 候选后端与实测 | 当前状态 |
|---:|---|---|---|---|---|---|---|
| 1 | `normalize_qcschema_molecule` | 科学数据与格式互操作 | 把一个分子结构验证并规范化为 QCSchema Molecule；不启动量化计算。<br>Catalog 原文：Validate and normalize one supplied molecular structure into a QCSchema Molecule record without launching a calculation. | required: structure; optional: 无<br>→ `QCSchemaMolecule` | 固定确定性内部实现 | 成功: `qcelemental` | ✅ 代表性端到端通过 |
| 2 | `validate_qcschema_record` | 科学数据与格式互操作 | 验证指定类型的 QCSchema/QCArchive 记录并返回规范化记录或结构化错误。<br>Catalog 原文：Validate one explicit QCSchema/QCArchive record type and return a normalized record or structured validation errors without executing it. | required: record; optional: 无<br>→ `QCSchemaValidationResult` | 固定确定性内部实现 | 成功: `qcelemental` | ✅ 代表性端到端通过 |
| 3 | `parse_quantum_chemistry_output` | 科学数据与格式互操作 | 从已有量化输出文件中解析智能体明确选择的性质，不重新计算。<br>Catalog 原文：Parse explicitly selected properties from one existing quantum-chemistry output file without rerunning the calculation. | required: output_file; optional: 无<br>→ `ParsedQuantumChemistryResult` | 固定确定性内部实现 | 成功: `cclib` | ✅ 代表性端到端通过 |
| 4 | `standardize_structure` | 结构与体系准备 | 清洗和标准化分子表示，不生成三维坐标，也不优化几何。<br>Catalog 原文：Standardize one molecular representation without generating 3D coordinates or optimizing geometry. | required: structure; optional: 无<br>→ `AtomicStructure` | 智能体必须显式选择 `backend_id` | 成功: `rdkit` | ✅ 代表性端到端通过 |
| 5 | `generate_3d_structure` | 结构与体系准备 | 由二维分子表示生成一个明确的三维结构。<br>Catalog 原文：Generate one explicit three-dimensional structure from a two-dimensional molecular representation. | required: molecule; optional: 无<br>→ `AtomicStructure` | 智能体必须显式选择 `backend_id` | 成功: `openbabel`, `rdkit` | ✅ 代表性端到端通过 |
| 6 | `generate_conformer_ensemble` | 结构与体系准备 | 生成构象集合；量化精修、排序和加权仍由后续独立 Action 完成。<br>Catalog 原文：Generate a conformer ensemble; it does not perform the later quantum refinement or final ranking workflow. | required: molecule; optional: initial_structure<br>→ `ConformerEnsemble` | 智能体必须显式选择 `backend_id` | 成功: `crest`, `rdkit_etkdg` | ✅ 代表性端到端通过 |
| 7 | `cluster_conformers` | 结构与体系准备 | 按明确 RMSD 阈值对已有构象集合聚类。<br>Catalog 原文：Cluster an already supplied conformer ensemble by an explicit heavy/all-atom RMSD cutoff without generating or ranking conformers. | required: ensemble; optional: 无<br>→ `ConformerClusterResult` | 智能体必须显式选择 `backend_id` | 成功: `rdkit` | ✅ 代表性端到端通过 |
| 8 | `align_molecular_structures` | 结构与体系准备 | 按显式原子映射把探针三维结构刚性对齐到参考结构。<br>Catalog 原文：Rigidly align one supplied 3D probe structure to a reference using an explicit atom-to-atom map. | required: reference, probe, atom_map; optional: 无<br>→ `StructureAlignmentResult` | 智能体必须显式选择 `backend_id` | 成功: `rdkit` | ✅ 代表性端到端通过 |
| 9 | `rank_conformers_from_results` | 结构与体系准备 | 根据智能体已提供的能量或自由能结果排序构象并计算 Boltzmann 权重。<br>Catalog 原文：Rank and weight conformers only from aligned energies or free energies already supplied by the agent. | required: ensemble, scores; optional: 无<br>→ `ConformerEnsemble` | 固定确定性内部实现 | 成功: `internal_statistics` | ✅ 代表性端到端通过 |
| 10 | `repair_biomolecular_structure` | 结构与体系准备 | 修复生物分子结构中缺失的残基或原子，不隐藏质子化、参数化或溶剂化。<br>Catalog 原文：Repair missing biomolecular residues or atoms without choosing protonation, force field, solvent, or dynamics settings. | required: structure; optional: 无<br>→ `AtomicStructure` | 智能体必须显式选择 `backend_id` | 成功: `pdbfixer` | ✅ 代表性端到端通过 |
| 11 | `select_structure_subset` | 结构与体系准备 | 从 PDB 中按链、模型和异原子保留策略选择结构子集。<br>Catalog 原文：Select explicit chains and/or models from one PDB structure, with an explicit choice about retaining heteroatom records. | required: structure; optional: 无<br>→ `AtomicStructure` | 固定确定性内部实现 | 成功: `pdb_tools` | ✅ 代表性端到端通过 |
| 12 | `renumber_biomolecular_structure` | 结构与体系准备 | 按显式起始编号重排 PDB 原子和残基编号，不改变化学与坐标。<br>Catalog 原文：Renumber PDB atom serials and residue identifiers from explicit starting values without changing coordinates or chemistry. | required: structure; optional: 无<br>→ `AtomicStructure` | 固定确定性内部实现 | 成功: `pdb_tools` | ✅ 代表性端到端通过 |
| 13 | `normalize_pdb_records` | 结构与体系准备 | 整理、排序并规范化 PDB 记录。<br>Catalog 原文：Sort and format one PDB record stream under explicit ordering, chain-break, and hybrid-36 choices. | required: structure; optional: 无<br>→ `AtomicStructure` | 固定确定性内部实现 | 成功: `pdb_tools` | ✅ 代表性端到端通过 |
| 14 | `assign_protonation_states` | 结构与体系准备 | 按智能体选择的规则或后端为固定结构添加/调整质子化状态。<br>Catalog 原文：Assign explicit protonation states using the agent-selected backend and pH/rule settings. | required: structure; optional: 无<br>→ `AtomicStructure` | 智能体必须显式选择 `backend_id` | 成功: `pdbfixer`, `rdkit` | ✅ 代表性端到端通过 |
| 15 | `assign_partial_charges` | 结构与体系准备 | 在不自动参数化或溶剂化的前提下计算并附加部分电荷。<br>Catalog 原文：Assign named force-field or docking partial charges without parameterizing or solvating the system. | required: structure; optional: 无<br>→ `ChargedStructure` | 智能体必须显式选择 `backend_id` | 成功: `openff_am1bcc`, `rdkit_gasteiger` | ✅ 代表性端到端通过 |
| 16 | `assign_force_field_parameters` | 结构与体系准备 | 用明确选择的力场为已有结构建立参数化体系。<br>Catalog 原文：Assign an explicitly selected force field to an already prepared molecular system. | required: structure; optional: charges<br>→ `ParameterizedSystem` | 智能体必须显式选择 `backend_id` | 成功: `openff`, `openmm_builder` | ✅ 代表性端到端通过 |
| 17 | `solvate_molecular_system` | 结构与体系准备 | 按明确盒形、尺寸、溶剂模型与组成对参数化体系溶剂化。<br>Catalog 原文：Build the explicitly requested solvent/ion environment without minimizing or propagating dynamics. | required: system; optional: 无<br>→ `ParameterizedSystem` | 智能体必须显式选择 `backend_id` | 成功: `packmol`<br>未逐组合验证: `openmm_builder` | ✅ 代表性端到端通过 |
| 18 | `analyze_crystal_symmetry` | 结构与体系准备 | 分析周期晶体的空间群、对称操作与等价位置。<br>Catalog 原文：Determine the crystallographic space group and symmetry-equivalent sites for one supplied periodic structure. | required: structure; optional: 无<br>→ `CrystalSymmetryResult` | 智能体必须显式选择 `backend_id` | 成功: `pymatgen`, `spglib` | ✅ 代表性端到端通过 |
| 19 | `standardize_crystal_structure` | 结构与体系准备 | 按原胞或常规胞约定标准化晶体结构。<br>Catalog 原文：Standardize one periodic structure in an explicitly selected primitive or conventional crystallographic setting. | required: structure; optional: 无<br>→ `AtomicStructure` | 智能体必须显式选择 `backend_id` | 成功: `pymatgen`, `spglib` | ✅ 代表性端到端通过 |
| 20 | `build_supercell` | 结构与体系准备 | 根据显式超胞矩阵扩展周期结构。<br>Catalog 原文：Apply one explicit integer supercell transformation to a periodic structure. | required: structure; optional: 无<br>→ `AtomicStructure` | 智能体必须显式选择 `backend_id` | 成功: `pymatgen` | ✅ 代表性端到端通过 |
| 21 | `enumerate_surface_slabs` | 结构与体系准备 | 根据 Miller 指数、厚度和真空层枚举表面 slab。<br>Catalog 原文：Enumerate a bounded set of symmetry-distinct slabs for one explicit Miller index and slab/vacuum geometry. | required: structure; optional: 无<br>→ `StructureCollection` | 智能体必须显式选择 `backend_id` | 成功: `pymatgen` | ✅ 代表性端到端通过 |
| 22 | `calculate_molecular_descriptors` | 化学信息学 | 计算一组明确选择的分子描述符。<br>Catalog 原文：Calculate an explicitly selected set of graph-based molecular descriptors without generating coordinates or running electronic structure. | required: molecule; optional: 无<br>→ `MolecularDescriptorResult` | 智能体必须显式选择 `backend_id` | 成功: `rdkit` | ✅ 代表性端到端通过 |
| 23 | `calculate_molecular_fingerprint` | 化学信息学 | 生成指定类型和参数的分子指纹。<br>Catalog 原文：Calculate one explicitly selected molecular fingerprint representation. | required: molecule; optional: 无<br>→ `MolecularFingerprint` | 智能体必须显式选择 `backend_id` | 成功: `rdkit` | ✅ 代表性端到端通过 |
| 24 | `calculate_molecular_similarity` | 化学信息学 | 用明确指纹和相似性度量比较分子。<br>Catalog 原文：Calculate one similarity value between two molecules using an explicit fingerprint and metric. | required: molecule_a, molecule_b; optional: 无<br>→ `MolecularSimilarityResult` | 智能体必须显式选择 `backend_id` | 成功: `rdkit` | ✅ 代表性端到端通过 |
| 25 | `search_local_substructures` | 化学信息学 | 在本地分子集合中执行 SMARTS/子结构匹配。<br>Catalog 原文：Find atom-index matches for an explicit SMARTS or SMILES query in one supplied molecule. | required: molecule, query; optional: 无<br>→ `SubstructureMatchResult` | 智能体必须显式选择 `backend_id` | 成功: `rdkit` | ✅ 代表性端到端通过 |
| 26 | `enumerate_tautomers` | 化学信息学 | 按明确规则枚举互变异构体。<br>Catalog 原文：Enumerate bounded tautomeric forms without selecting a preferred tautomer for the agent. | required: molecule; optional: 无<br>→ `MoleculeCollection` | 智能体必须显式选择 `backend_id` | 成功: `rdkit` | ✅ 代表性端到端通过 |
| 27 | `enumerate_stereoisomers` | 化学信息学 | 枚举未指定或目标立体中心的立体异构体。<br>Catalog 原文：Enumerate bounded stereoisomers under explicit uniqueness and assignment rules. | required: molecule; optional: 无<br>→ `MoleculeCollection` | 智能体必须显式选择 `backend_id` | 成功: `rdkit` | ✅ 代表性端到端通过 |
| 28 | `calculate_energy` | 分子电子结构与派生性质 | 用智能体明确选择的软件和理论方法计算一个分子或非周期体系的标量能量。<br>Catalog 原文：Calculate one molecular or non-periodic scalar energy with the exact software and method selected by the agent. | required: structure; optional: 无<br>→ `EnergyResult` | 智能体必须显式选择 `backend_id` | 成功: `ase_emt`, `chgnet`, `deepmd`, `gamess`, `gpaw`, `mace`, `nwchem`, `openmolcas`, `orca`, `psi4`, `pyscf`, `tblite`, `xtb`<br>曾失败后已成功: `openmolcas`, `orca`, `pyscf`<br>未逐组合验证: `gaussian` | ✅ 代表性端到端通过 |
| 29 | `calculate_forces` | 分子电子结构与派生性质 | 计算一个结构或同质结构批次的原子力。<br>Catalog 原文：Calculate atomic forces for one non-periodic structure or an aligned batch. | required: structure; optional: 无<br>→ `ForceResult` | 智能体必须显式选择 `backend_id` | 成功: `gpaw`, `nwchem`, `orca`, `pyscf`, `xtb`<br>未逐组合验证: `ase_emt`, `chgnet`, `deepmd`, `mace`, `tblite` | ✅ 代表性端到端通过 |
| 30 | `calculate_hessian` | 分子电子结构与派生性质 | 计算或数值构造 Hessian；振动分析仍是独立 Action。<br>Catalog 原文：Calculate one molecular Hessian without deriving modes, spectra, or thermochemistry. | required: structure; optional: 无<br>→ `Hessian` | 智能体必须显式选择 `backend_id` | 成功: `gaussian`, `nwchem`, `orca`, `pyscf`<br>未逐组合验证: `ase_emt`, `psi4`, `tblite`, `xtb` | ✅ 代表性端到端通过 |
| 31 | `optimize_geometry` | 分子电子结构与派生性质 | 按显式收敛阈值优化一个结构，只把优化结构作为主要科学结果。<br>Catalog 原文：Optimize one non-periodic geometry and return the optimized structure only as the primary result. | required: structure; optional: constraints<br>→ `AtomicStructure` | 智能体必须显式选择 `backend_id` | 成功: `geometric`, `gpaw`, `orca`, `sella`<br>未逐组合验证: `ase_emt`, `chgnet`, `deepmd`, `gamess`, `gaussian`, `mace`, `tblite`, `xtb` | ✅ 代表性端到端通过 |
| 32 | `calculate_dipole_moment` | 分子电子结构与派生性质 | 计算分子偶极矩。<br>Catalog 原文：Calculate one molecular dipole moment with an explicitly chosen electronic method. | required: structure; optional: 无<br>→ `DipoleResult` | 智能体必须显式选择 `backend_id` | 成功: `nwchem`, `openmolcas`, `orca`, `xtb`<br>未逐组合验证: `gamess`, `gaussian`, `psi4`, `pyscf`, `tblite` | ✅ 代表性端到端通过 |
| 33 | `calculate_atomic_charges` | 分子电子结构与派生性质 | 用明确人口分析/电荷方案计算原子电荷。<br>Catalog 原文：Calculate electronic-structure population-analysis charges without attaching force-field parameters. | required: structure; optional: 无<br>→ `AtomicChargeResult` | 智能体必须显式选择 `backend_id` | 成功: `multiwfn`, `nwchem`, `openmolcas`, `orca`, `xtb`<br>未逐组合验证: `psi4`, `pyscf` | ✅ 代表性端到端通过 |
| 34 | `calculate_orbitals` | 分子电子结构与派生性质 | 提取轨道能量、占据数、系数或相关轨道信息。<br>Catalog 原文：Calculate orbital energies, occupations, and optional coefficient artifacts. | required: structure; optional: 无<br>→ `OrbitalResult` | 智能体必须显式选择 `backend_id` | 成功: `openmolcas`, `orca`<br>未逐组合验证: `psi4`, `pyscf` | ✅ 代表性端到端通过 |
| 35 | `calculate_bond_orders` | 分子电子结构与派生性质 | 用明确方案计算原子对键级。<br>Catalog 原文：Calculate atom-pair electronic bond-order indices using one explicitly selected population-analysis backend. | required: structure; optional: 无<br>→ `BondOrderResult` | 智能体必须显式选择 `backend_id` | 成功: `multiwfn`, `orca`, `xtb` | ✅ 代表性端到端通过 |
| 36 | `calculate_excited_states` | 分子电子结构与派生性质 | 用明确的激发态方法和状态数计算电子激发态。<br>Catalog 原文：Calculate a bounded set of vertical electronic excited states without constructing a broadened spectrum or propagating dynamics. | required: structure; optional: 无<br>→ `ExcitedStateResult` | 智能体必须显式选择 `backend_id` | 成功: `orca`, `pyscf` | ✅ 代表性端到端通过 |
| 37 | `analyze_electron_density_topology` | 分子电子结构与派生性质 | 对已有波函数或电子密度执行临界点/拓扑分析。<br>Catalog 原文：Locate and characterize critical points in one supplied molecular or periodic electron-density field without generating that field or integrating atomic basins. | required: density_file; optional: structure_file<br>→ `ElectronDensityTopologyResult` | 智能体必须显式选择 `backend_id` | 成功: `critic2` | ✅ 代表性端到端通过 |
| 38 | `calculate_atomic_basin_properties` | 分子电子结构与派生性质 | 对电子密度原子盆进行积分并返回盆性质。<br>Catalog 原文：Integrate population, Laplacian, and available volume properties over atomic or attractor basins in one supplied scalar-field grid using an explicitly selected partition algorithm. | required: density_file; optional: structure_file<br>→ `AtomicBasinPropertyResult` | 智能体必须显式选择 `backend_id` | 成功: `critic2` | ✅ 代表性端到端通过 |
| 39 | `calculate_bader_charges` | 分子电子结构与派生性质 | 从周期电子密度计算 Bader 电荷。<br>Catalog 原文：Calculate atomic Bader charges from one supplied electron-density grid using an explicitly selected Yu-Trinkle or Henkelman grid partition. | required: density_file; optional: structure_file<br>→ `AtomicChargeResult` | 智能体必须显式选择 `backend_id` | 成功: `critic2` | ✅ 代表性端到端通过 |
| 40 | `derive_vibrational_modes` | 分子电子结构与派生性质 | 由已有 Hessian 与结构导出频率和正常模式，不隐藏 Hessian 计算。<br>Catalog 原文：Derive frequencies and normal modes from an existing Hessian and structure. | required: hessian, structure; optional: 无<br>→ `FrequencyResult` | 固定确定性内部实现 | 成功: `internal_vibrations` | ✅ 代表性端到端通过 |
| 41 | `derive_ir_spectrum` | 分子电子结构与派生性质 | 由已有振动频率与强度构建展宽后的红外光谱。<br>Catalog 原文：Construct an IR spectrum from vibration results that already contain intensities. | required: vibrations; optional: 无<br>→ `SpectrumResult` | 固定确定性内部实现 | 成功: `internal_spectroscopy` | ✅ 代表性端到端通过 |
| 42 | `derive_uv_vis_spectrum` | 分子电子结构与派生性质 | 由已有跃迁能和振子强度构建展宽后的 UV/Vis 光谱。<br>Catalog 原文：Construct a deterministic broadened UV/visible spectrum from supplied transition energies and oscillator strengths. | required: excited_states; optional: 无<br>→ `SpectrumResult` | 固定确定性内部实现 | 成功: `internal_spectroscopy` | ✅ 代表性端到端通过 |
| 43 | `derive_thermochemistry` | 分子电子结构与派生性质 | 由电子能和频率推导指定温压下的热化学量。<br>Catalog 原文：Derive thermochemical quantities from supplied electronic energy and frequencies; no optimization or Hessian is hidden. | required: energy, frequencies; optional: 无<br>→ `ThermochemistryResult` | 智能体必须显式选择 `backend_id` | 成功: `goodvibes`, `internal_thermochemistry` | ✅ 代表性端到端通过 |
| 44 | `locate_transition_state` | 反应路径、热力学与动力学 | 从给定初猜定位一个候选过渡态；频率和 IRC 验证保持独立。<br>Catalog 原文：Locate one candidate transition-state structure without automatically running frequencies or IRC. | required: initial_guess; optional: reactant, product<br>→ `AtomicStructure` | 智能体必须显式选择 `backend_id` | 成功: `sella`<br>未逐组合验证: `pysisyphus` | ✅ 代表性端到端通过 |
| 45 | `trace_intrinsic_reaction_coordinate` | 反应路径、热力学与动力学 | 从已给定的过渡态结构沿一个或两个方向追踪 IRC。<br>Catalog 原文：Trace an IRC from an already supplied transition-state structure. | required: transition_state; optional: 无<br>→ `ReactionPath` | 智能体必须显式选择 `backend_id` | 成功: `pysisyphus` | ✅ 代表性端到端通过 |
| 46 | `calculate_chemical_equilibrium` | 反应路径、热力学与动力学 | 对显式机理、组成和热力学条件计算平衡状态。<br>Catalog 原文：Calculate an equilibrium composition/state for an explicitly supplied mechanism and thermodynamic condition. | required: composition; optional: mechanism<br>→ `EquilibriumResult` | 智能体必须显式选择 `backend_id` | 成功: `cantera` | ✅ 代表性端到端通过 |
| 47 | `integrate_reaction_network` | 反应路径、热力学与动力学 | 对显式反应网络与初始状态进行时间积分。<br>Catalog 原文：Integrate one explicitly specified reaction network over time. | required: network, initial_state; optional: 无<br>→ `KineticsTrajectory` | 智能体必须显式选择 `backend_id` | 成功: `scipy`<br>未逐组合验证: `cantera` | ✅ 代表性端到端通过 |
| 48 | `calculate_rate_constants` | 反应路径、热力学与动力学 | 在指定温压点计算 Arrhenius、多 Arrhenius、PDep 或 Chebyshev 速率常数。<br>Catalog 原文：Evaluate an explicitly supplied Arrhenius, multi-Arrhenius, pressure-dependent Arrhenius, or Chebyshev kinetics model on explicit temperature/pressure points. | required: kinetics_model, temperatures_kelvin; optional: pressures_pa<br>→ `RateConstantResult` | 智能体必须显式选择 `backend_id` | 成功: `rmg` | ✅ 代表性端到端通过 |
| 49 | `calculate_tunneling_correction` | 反应路径、热力学与动力学 | 按 Wigner 或 Eckart 模型计算隧穿修正。<br>Catalog 原文：Calculate Wigner or Eckart transition-state tunneling correction factors at explicit temperatures. | required: temperatures_kelvin, imaginary_frequency_cm1; optional: reactant_energy_kj_mol, transition_state_energy_kj_mol, product_energy_kj_mol<br>→ `TunnelingCorrectionResult` | 智能体必须显式选择 `backend_id` | 成功: `rmg` | ✅ 代表性端到端通过 |
| 50 | `solve_master_equation` | 反应路径、热力学与动力学 | 对智能体提供的 MESS/MESMER 主方程模型求解并提取唯象速率。<br>Catalog 原文：Solve an explicitly supplied gas-phase chemical master-equation model and extract pressure/temperature-dependent phenomenological rate coefficients without constructing or modifying the reaction model. | required: model_file; optional: companion_files, model_relative_path<br>→ `MasterEquationResult` | 智能体必须显式选择 `backend_id` | 成功: `mesmer`, `mess` | ✅ 代表性端到端通过 |
| 51 | `solve_microkinetic_model` | 反应路径、热力学与动力学 | 求解智能体完整指定的 CatMAP 微观动力学模型，不替智能体构造反应网络。<br>Catalog 原文：Solve one explicitly supplied microkinetic model without constructing the reaction model for the agent. | required: model; optional: 无<br>→ `MicrokineticResult` | 智能体必须显式选择 `backend_id` | 成功: `catmap` | ✅ 代表性端到端通过 |
| 52 | `minimize_system_energy` | 分子动力学、轨迹与自由能 | 对已参数化体系执行一次能量最小化，不自动平衡或继续动力学。<br>Catalog 原文：Minimize an already parameterized system without automatically equilibrating or propagating dynamics. | required: system; optional: 无<br>→ `ParameterizedSystem` | 智能体必须显式选择 `backend_id` | 成功: `amber_pmemd`, `charmm`, `gromacs`, `hoomd`, `lammps`, `namd`<br>未逐组合验证: `openmm` | ✅ 代表性端到端通过 |
| 53 | `calculate_force_field_energy` | 分子动力学、轨迹与自由能 | 对已参数化体系计算力场势能。<br>Catalog 原文：Evaluate the total potential energy of an already parameterized system at explicitly selected stored coordinates/state without minimizing or propagating it. | required: system; optional: 无<br>→ `ForceFieldEnergyResult` | 智能体必须显式选择 `backend_id` | 成功: `hoomd`, `openmm` | ✅ 代表性端到端通过 |
| 54 | `calculate_force_field_forces` | 分子动力学、轨迹与自由能 | 对已参数化体系计算力场原子力。<br>Catalog 原文：Evaluate atomic force-field forces for an already parameterized system at explicitly selected stored coordinates/state. | required: system; optional: 无<br>→ `ForceResult` | 智能体必须显式选择 `backend_id` | 成功: `hoomd`, `openmm` | ✅ 代表性端到端通过 |
| 55 | `decompose_force_field_energy` | 分子动力学、轨迹与自由能 | 把力场势能按已有 Force 对象分解，不重新定义力场。<br>Catalog 原文：Decompose one OpenMM potential energy evaluation by the explicitly present Force objects without changing parameters or running dynamics. | required: system; optional: 无<br>→ `ForceFieldEnergyDecompositionResult` | 智能体必须显式选择 `backend_id` | 成功: `openmm` | ✅ 代表性端到端通过 |
| 56 | `propagate_dynamics` | 分子动力学、轨迹与自由能 | 执行一个由智能体定义的动力学片段并返回轨迹和最终状态。<br>Catalog 原文：Propagate exactly one agent-defined dynamics segment and return its trajectory and final state. | required: system; optional: 无<br>→ `Trajectory` | 智能体必须显式选择 `backend_id` | 成功: `hoomd`<br>未逐组合验证: `amber_pmemd`, `charmm`, `gromacs`, `lammps`, `namd`, `openmm` | ✅ 代表性端到端通过 |
| 57 | `calculate_trajectory_rmsd` | 分子动力学、轨迹与自由能 | 计算轨迹相对参考结构的 RMSD。<br>Catalog 原文：Calculate an RMSD time series for an explicitly selected trajectory atom group and reference. | required: trajectory, topology; optional: reference<br>→ `TimeSeries` | 智能体必须显式选择 `backend_id` | 成功: `mdtraj`<br>未逐组合验证: `mdanalysis` | ✅ 代表性端到端通过 |
| 58 | `calculate_radius_of_gyration` | 分子动力学、轨迹与自由能 | 计算轨迹随时间变化的回转半径。<br>Catalog 原文：Calculate the radius-of-gyration time series for an explicitly selected atom group. | required: trajectory, topology; optional: 无<br>→ `TimeSeries` | 智能体必须显式选择 `backend_id` | 成功: `mdtraj`<br>未逐组合验证: `mdanalysis` | ✅ 代表性端到端通过 |
| 59 | `calculate_radial_distribution` | 分子动力学、轨迹与自由能 | 计算两组原子选择之间的径向分布函数。<br>Catalog 原文：Calculate one radial distribution function for two explicitly selected atom groups. | required: trajectory, topology; optional: 无<br>→ `DistributionResult` | 智能体必须显式选择 `backend_id` | 成功: `mdanalysis` | ✅ 代表性端到端通过 |
| 60 | `calculate_mean_squared_displacement` | 分子动力学、轨迹与自由能 | 计算选定原子的均方位移。<br>Catalog 原文：Calculate one mean-squared-displacement time series for an explicitly selected atom group. | required: trajectory, topology; optional: 无<br>→ `TimeSeries` | 智能体必须显式选择 `backend_id` | 成功: `mdanalysis` | ✅ 代表性端到端通过 |
| 61 | `calculate_contacts` | 分子动力学、轨迹与自由能 | 统计轨迹中的原子/残基接触。<br>Catalog 原文：Calculate inter-residue contact distances for an explicitly supplied residue-pair set and contact definition. | required: trajectory, topology, residue_pairs; optional: 无<br>→ `ContactTimeSeries` | 智能体必须显式选择 `backend_id` | 成功: `mdtraj` | ✅ 代表性端到端通过 |
| 62 | `calculate_solvent_accessible_surface` | 分子动力学、轨迹与自由能 | 计算溶剂可及表面积。<br>Catalog 原文：Calculate solvent-accessible surface area per atom or residue for an existing trajectory. | required: trajectory, topology; optional: 无<br>→ `SurfaceAreaTimeSeries` | 智能体必须显式选择 `backend_id` | 成功: `mdtraj` | ✅ 代表性端到端通过 |
| 63 | `calculate_dihedral_distribution` | 分子动力学、轨迹与自由能 | 计算显式二面角集合的时间序列或分布。<br>Catalog 原文：Calculate dihedral-angle time series for explicitly supplied atom-index quartets. | required: trajectory, topology, atom_quartets; optional: 无<br>→ `DihedralTimeSeries` | 智能体必须显式选择 `backend_id` | 成功: `mdtraj`<br>未逐组合验证: `mdanalysis` | ✅ 代表性端到端通过 |
| 64 | `calculate_hydrogen_bonds` | 分子动力学、轨迹与自由能 | 按明确几何标准分析氢键。<br>Catalog 原文：Identify hydrogen-bond events in an existing trajectory using explicit donor, hydrogen, acceptor, distance, and angle definitions. | required: trajectory, topology; optional: between_selections<br>→ `HydrogenBondResult` | 智能体必须显式选择 `backend_id` | 成功: `mdanalysis` | ✅ 代表性端到端通过 |
| 65 | `calculate_principal_components` | 分子动力学、轨迹与自由能 | 对对齐后的轨迹执行主成分分析。<br>Catalog 原文：Calculate coordinate principal components and frame projections for an explicitly selected trajectory atom group. | required: trajectory, topology; optional: 无<br>→ `PrincipalComponentResult` | 智能体必须显式选择 `backend_id` | 成功: `mdanalysis` | ✅ 代表性端到端通过 |
| 66 | `calculate_dynamic_cross_correlation` | 分子动力学、轨迹与自由能 | 计算原子运动的动态交叉相关矩阵。<br>Catalog 原文：Calculate an atom-wise dynamic cross-correlation matrix from explicitly selected and optionally aligned trajectory coordinates. | required: trajectory, topology; optional: 无<br>→ `DynamicCrossCorrelationResult` | 智能体必须显式选择 `backend_id` | 成功: `mdanalysis` | ✅ 代表性端到端通过 |
| 67 | `assign_secondary_structure` | 分子动力学、轨迹与自由能 | 为蛋白轨迹分配二级结构。<br>Catalog 原文：Assign per-residue secondary-structure labels for every frame of an existing protein trajectory. | required: trajectory, topology; optional: 无<br>→ `SecondaryStructureTimeSeries` | 智能体必须显式选择 `backend_id` | 成功: `mdtraj` | ✅ 代表性端到端通过 |
| 68 | `cluster_trajectory` | 分子动力学、轨迹与自由能 | 按明确特征和聚类参数对轨迹帧聚类。<br>Catalog 原文：Cluster explicitly selected trajectory frames by RMSD using a deterministic cutoff-based leader assignment. | required: trajectory, topology; optional: 无<br>→ `TrajectoryClusterResult` | 智能体必须显式选择 `backend_id` | 成功: `mdtraj` | ✅ 代表性端到端通过 |
| 69 | `evaluate_collective_variables` | 分子动力学、轨迹与自由能 | 用 PLUMED 对已有轨迹计算智能体指定的集体变量。<br>Catalog 原文：Evaluate explicitly defined collective variables on an existing trajectory. | required: trajectory, topology, collective_variables; optional: 无<br>→ `TimeSeries` | 智能体必须显式选择 `backend_id` | 成功: `plumed` | ✅ 代表性端到端通过 |
| 70 | `estimate_free_energy_difference` | 分子动力学、轨迹与自由能 | 用 MBAR 对明确给定的约化势数据估计态间自由能差。<br>Catalog 原文：Estimate dimensionless pairwise free-energy differences from an explicitly supplied reduced-potential matrix and sample counts. | required: reduced_potentials, samples_per_state; optional: 无<br>→ `FreeEnergyDifferenceResult` | 智能体必须显式选择 `backend_id` | 成功: `pymbar` | ✅ 代表性端到端通过 |
| 71 | `estimate_thermodynamic_expectations` | 分子动力学、轨迹与自由能 | 用 MBAR 估计热力学期望值及不确定度。<br>Catalog 原文：Estimate state-resolved observable expectations from explicitly supplied samples and a reduced-potential matrix. | required: reduced_potentials, samples_per_state, observables; optional: 无<br>→ `ThermodynamicExpectationResult` | 智能体必须显式选择 `backend_id` | 成功: `pymbar` | ✅ 代表性端到端通过 |
| 72 | `calculate_potential_of_mean_force` | 分子动力学、轨迹与自由能 | 由采样数据计算一维或离散自由能面/PMF。<br>Catalog 原文：Estimate a one-dimensional histogram free-energy profile from supplied uncorrelated samples; this does not integrate a mean-force trajectory or choose bins for the agent. | required: reduced_potentials, samples_per_state, target_reduced_potential, collective_variable; optional: 无<br>→ `FreeEnergyProfileResult` | 智能体必须显式选择 `backend_id` | 成功: `pymbar` | ✅ 代表性端到端通过 |
| 73 | `analyze_free_energy_convergence` | 分子动力学、轨迹与自由能 | 分析自由能估计随样本量或时间的收敛。<br>Catalog 原文：Re-estimate one explicitly selected pairwise free-energy difference over supplied sample fractions without generating or decorrelating samples. | required: reduced_potentials, samples_per_state; optional: 无<br>→ `FreeEnergyConvergenceResult` | 智能体必须显式选择 `backend_id` | 成功: `pymbar` | ✅ 代表性端到端通过 |
| 74 | `parse_alchemical_energy_data` | 分子动力学、轨迹与自由能 | 从 GROMACS、Amber 或 NAMD 输出解析炼金自由能数据。<br>Catalog 原文：Parse one or more explicitly identified engine output files into a normalized alchemical reduced-potential or derivative table. | required: files; optional: 无<br>→ `AlchemicalEnergyData` | 智能体必须显式选择 `backend_id` | 成功: `alchemlyb` | ✅ 代表性端到端通过 |
| 75 | `calculate_periodic_energy` | 周期材料、电子结构、声子与热输运 | 用明确周期电子结构后端计算总能。<br>Catalog 原文：Calculate one periodic-system energy with the explicitly selected electronic-structure backend. | required: structure; optional: 无<br>→ `EnergyResult` | 智能体必须显式选择 `backend_id` | 成功: `abinit`, `allegro`, `cp2k`, `dftbplus`, `gpaw`, `quantum_espresso`, `siesta`, `vasp`<br>未逐组合验证: `deepmd`, `nequip` | ✅ 代表性端到端通过 |
| 76 | `calculate_periodic_forces` | 周期材料、电子结构、声子与热输运 | 计算周期体系原子力。<br>Catalog 原文：Calculate periodic atomic forces for one structure or aligned displaced-structure batch. | required: structure; optional: 无<br>→ `ForceResult` | 智能体必须显式选择 `backend_id` | 成功: `abinit`, `dftbplus`, `gpaw`, `nequip`, `quantum_espresso`, `siesta`<br>未逐组合验证: `allegro`, `cp2k`, `deepmd`, `vasp` | ✅ 代表性端到端通过 |
| 77 | `calculate_periodic_stress` | 周期材料、电子结构、声子与热输运 | 计算周期体系应力张量。<br>Catalog 原文：Calculate one periodic stress tensor without relaxing the structure. | required: structure; optional: 无<br>→ `StressResult` | 智能体必须显式选择 `backend_id` | 成功: `abinit`, `deepmd`, `gpaw`, `quantum_espresso`<br>未逐组合验证: `allegro`, `cp2k`, `nequip`, `vasp` | ✅ 代表性端到端通过 |
| 78 | `relax_periodic_structure` | 周期材料、电子结构、声子与热输运 | 按显式阈值弛豫周期原子位置，并可选择是否弛豫晶胞。<br>Catalog 原文：Relax a periodic structure under explicit atomic/cell constraints. | required: structure; optional: 无<br>→ `AtomicStructure` | 智能体必须显式选择 `backend_id` | 成功: `dftbplus`, `gpaw`<br>未逐组合验证: `abinit`, `allegro`, `cp2k`, `deepmd`, `nequip`, `quantum_espresso`, `siesta`, `vasp` | ✅ 代表性端到端通过 |
| 79 | `calculate_electronic_band_structure` | 周期材料、电子结构、声子与热输运 | 沿智能体给定的 k 路径计算电子能带。<br>Catalog 原文：Calculate electronic eigenvalue bands along one explicit reciprocal-space path from an existing converged periodic ground-state restart. | required: ground_state; optional: 无<br>→ `ElectronicBandStructureResult` | 智能体必须显式选择 `backend_id` | 成功: `gpaw` | ✅ 代表性端到端通过 |
| 80 | `calculate_density_of_states` | 周期材料、电子结构、声子与热输运 | 计算总电子态密度。<br>Catalog 原文：Calculate a total electronic density of states on an explicit energy grid from an existing converged periodic ground-state restart. | required: ground_state; optional: 无<br>→ `DensityOfStatesResult` | 智能体必须显式选择 `backend_id` | 成功: `gpaw` | ✅ 代表性端到端通过 |
| 81 | `calculate_projected_density_of_states` | 周期材料、电子结构、声子与热输运 | 计算按原子/轨道投影的电子态密度。<br>Catalog 原文：Calculate or extract explicitly requested atom/orbital projected electronic densities of states from an existing compatible periodic electronic-state artifact. | required: projections; optional: ground_state, dos_file, structure_file<br>→ `ProjectedDensityOfStatesResult` | 智能体必须显式选择 `backend_id` | 成功: `gpaw`, `lobster` | ✅ 代表性端到端通过 |
| 82 | `analyze_periodic_bonding` | 周期材料、电子结构、声子与热输运 | 从已有周期波函数输出执行 COHP/COOP/COBI 等成键分析。<br>Catalog 原文：Extract explicitly selected integrated and optional energy-resolved COHP, COOP, or COBI bonding information from existing LOBSTER outputs. | required: integrated_bond_list; optional: bond_curve_file<br>→ `PeriodicBondingResult` | 智能体必须显式选择 `backend_id` | 成功: `lobster` | ✅ 代表性端到端通过 |
| 83 | `calculate_charge_spilling` | 周期材料、电子结构、声子与热输运 | 评估 LOBSTER 投影质量和电荷泄漏。<br>Catalog 原文：Assess LOBSTER wavefunction-projection charge/total spilling against explicit acceptance thresholds from an existing lobsterout file. | required: lobster_output; optional: 无<br>→ `ProjectionQualityResult` | 智能体必须显式选择 `backend_id` | 成功: `lobster` | ✅ 代表性端到端通过 |
| 84 | `generate_displaced_supercells` | 周期材料、电子结构、声子与热输运 | 按超胞和位移幅度生成有限位移结构。<br>Catalog 原文：Generate a displacement set from an explicit supercell matrix and displacement amplitude. | required: structure; optional: 无<br>→ `DisplacementSet` | 智能体必须显式选择 `backend_id` | 成功: `phonopy`<br>未逐组合验证: `phono3py` | ✅ 代表性端到端通过 |
| 85 | `assemble_force_constants` | 周期材料、电子结构、声子与热输运 | 由位移集合与对应力组装二阶力常数。<br>Catalog 原文：Assemble force constants only from a supplied displacement set and aligned forces. | required: displacement_set, force_set; optional: 无<br>→ `ForceConstants` | 智能体必须显式选择 `backend_id` | 成功: `phonopy`<br>未逐组合验证: `phono3py` | ✅ 代表性端到端通过 |
| 86 | `calculate_phonon_dispersion` | 周期材料、电子结构、声子与热输运 | 由二阶力常数沿给定 q 路径计算声子色散。<br>Catalog 原文：Calculate a phonon dispersion from existing force constants and an explicit q-point path. | required: force_constants, structure; optional: 无<br>→ `PhononDispersion` | 智能体必须显式选择 `backend_id` | 成功: `phonopy`<br>未逐组合验证: `phono3py` | ✅ 代表性端到端通过 |
| 87 | `calculate_phonon_density_of_states` | 周期材料、电子结构、声子与热输运 | 由二阶力常数和 q 网格计算声子态密度。<br>Catalog 原文：Calculate a phonon density of states from existing force constants and an explicit q mesh. | required: force_constants, structure; optional: 无<br>→ `PhononDensityOfStates` | 智能体必须显式选择 `backend_id` | 成功: `phonopy`<br>未逐组合验证: `phono3py` | ✅ 代表性端到端通过 |
| 88 | `calculate_harmonic_thermodynamics` | 周期材料、电子结构、声子与热输运 | 从声子谱计算谐振近似热力学量。<br>Catalog 原文：Calculate harmonic free energy, entropy, and constant-volume heat capacity at explicitly supplied temperatures. | required: force_constants, structure; optional: 无<br>→ `HarmonicThermodynamicsResult` | 智能体必须显式选择 `backend_id` | 成功: `phono3py`, `phonopy` | ✅ 代表性端到端通过 |
| 89 | `calculate_phonon_group_velocities` | 周期材料、电子结构、声子与热输运 | 计算声子群速度。<br>Catalog 原文：Calculate mode-resolved phonon group-velocity vectors along an explicitly supplied q-point path. | required: force_constants, structure; optional: 无<br>→ `PhononGroupVelocityResult` | 智能体必须显式选择 `backend_id` | 成功: `phono3py`, `phonopy` | ✅ 代表性端到端通过 |
| 90 | `calculate_lattice_thermal_conductivity` | 周期材料、电子结构、声子与热输运 | 由显式二阶/三阶力常数和求解设置计算晶格热导率。<br>Catalog 原文：Calculate the lattice thermal-conductivity tensor from explicit second-/third-order force constants or a complete native BTE model under Agent-selected solution and scattering settings. | required: 无; optional: second_order_force_constants, third_order_force_constants, structure, control_file, second_order_force_constants_file, third_order_force_constants_file, born_file, companion_files<br>→ `LatticeThermalConductivityResult` | 智能体必须显式选择 `backend_id` | 成功: `phono3py`, `shengbte` | ✅ 代表性端到端通过 |
| 91 | `dock_ligand` | 分子对接 | 把已准备好的配体对接到已准备好的受体，并使用显式搜索盒。<br>Catalog 原文：Dock an already prepared ligand into an already prepared receptor using an explicit search space. | required: receptor, ligand, search_space; optional: charges<br>→ `DockingResult` | 智能体必须显式选择 `backend_id` | 成功: `gnina`, `vina` | ✅ 代表性端到端通过 |
| 92 | `search_compounds` | 外部化学数据源 | 通过 PubChem 执行受限化合物检索。<br>Catalog 原文：Search PubChem compound records by an explicit identifier and namespace. | required: query; optional: 无<br>→ `CompoundRecords` | 固定官方数据源 | 成功: `pubchem`<br>曾失败后已成功: `pubchem` | ⚠️ 当前在线失败；契约/模拟曾成功<br>ServerBusyError: PubChem HTTP Error 503 PUGREST.ServerBusy: Too many requests or server too busy |
| 93 | `resolve_chemical_identity` | 外部化学数据源 | 把名称、CID、CAS、SMILES 等标识解析为统一化学身份。<br>Catalog 原文：Resolve one explicit compound identifier to a bounded ChemicalIdentity record through PubChem. | required: query; optional: 无<br>→ `ChemicalIdentity` | 固定官方数据源 | 成功: —<br>仅有失败记录: `pubchem` | ⚠️ 当前在线失败<br>ServerBusyError: PubChem HTTP Error 503 PUGREST.ServerBusy: Too many requests or server too busy |
| 94 | `retrieve_compound_properties` | 外部化学数据源 | 从 PubChem 获取智能体指定的单分子性质字段。<br>Catalog 原文：Retrieve an explicitly selected bounded property set for matching PubChem compounds. | required: query; optional: 无<br>→ `CompoundPropertyRecords` | 固定官方数据源 | 成功: —<br>仅有失败记录: `pubchem` | ⚠️ 当前在线失败<br>ServerBusyError: PubChem HTTP Error 503 PUGREST.ServerBusy: Too many requests or server too busy |
| 95 | `retrieve_compound_structure` | 外部化学数据源 | 从 PubChem 获取指定二维/三维结构记录。<br>Catalog 原文：Retrieve bounded PubChem 2D or 3D coordinate records while leaving coordinate dimensionality and explicit-hydrogen handling to the agent. | required: query; optional: 无<br>→ `StructureCollection` | 固定官方数据源 | 成功: —<br>仅有失败记录: `pubchem` | ⚠️ 当前在线失败<br>ServerBusyError: PubChem HTTP Error 503 PUGREST.ServerBusy: Too many requests or server too busy |
| 96 | `search_similar_compounds` | 外部化学数据源 | 通过 PubChem 相似性服务检索相似化合物。<br>Catalog 原文：Run one bounded PubChem 2D similarity search from an explicit structure identifier. | required: query; optional: 无<br>→ `CompoundRecords` | 固定官方数据源 | 成功: —<br>仅有失败记录: `pubchem` | ⚠️ 当前在线失败<br>HTTPStatusError: Server error '503 PUGREST.ServerBusy' for url 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsimilarity_2d/smiles/CCO/cids/JSON?MaxRecords=1&MaxSeconds=30&Threshold=99'<br>For more information check: https://developer.mozilla.org/en-US/d |
| 97 | `search_substructures` | 外部化学数据源 | 通过 PubChem 子结构服务检索匹配化合物。<br>Catalog 原文：Run one bounded PubChem substructure search from an explicit SMILES, SMARTS, InChI, or CID query. | required: query; optional: 无<br>→ `CompoundRecords` | 固定官方数据源 | 成功: —<br>仅有失败记录: `pubchem` | ⚠️ 当前在线失败<br>HTTPStatusError: Server error '503 PUGREST.ServerBusy' for url 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastsubstructure/smarts/O/cids/JSON?MaxRecords=1&MaxSeconds=30&Stereo=ignore&MatchCharges=false&MatchIsotopes=false'<br>For more information check:  |
| 98 | `search_protein_structures` | 外部化学数据源 | 通过 RCSB PDB Data API 检索蛋白/大分子结构。<br>Catalog 原文：Search or retrieve RCSB PDB structure records using explicit identifiers or query terms. | required: query; optional: 无<br>→ `ProteinStructureRecords` | 固定官方数据源 | 成功: `rcsb_pdb` | ✅ 在线实测通过 |
| 99 | `search_materials` | 外部化学数据源 | 通过 Materials Project API 检索材料记录。<br>Catalog 原文：Search Materials Project records by material id, formula, or explicit query fields. | required: query; optional: 无<br>→ `MaterialRecords` | 固定官方数据源 | 成功: `materials_project` | ✅ 在线实测通过 |
| 100 | `search_catalysis_records` | 外部化学数据源 | 通过 Catalysis-Hub GraphQL 检索催化反应记录。<br>Catalog 原文：Search Catalysis-Hub reaction records using explicit reactant/product filters. | required: query; optional: 无<br>→ `CatalysisRecords` | 固定官方数据源 | 成功: —<br>仅有失败记录: `catalysis_hub` | ⚠️ 当前在线失败<br>ReadTimeout: The read operation timed out |
| 101 | `lookup_nist_webbook_species` | 外部化学数据源 | 使用 NIST WebBook 官方 CGI 对一个物种做受限精确查询。<br>Catalog 原文：Look up one bounded NIST Chemistry WebBook species query by explicit CAS number, exact name, or exact formula through the official CGI interface. | required: query; optional: 无<br>→ `NISTWebBookSpeciesRecords` | 固定官方数据源 | 成功: `nist_webbook` | ✅ 在线实测通过 |

## 6. Backend 详细状态

### 6.1 后端统计口径

- Catalog 共 **76** 个 BackendSpecs，其中 **71** 个本地执行后端、**5** 个在线数据服务。
- 加载本地配置后健康检查：**76/76 available**。
- 至少一次成功 Action 证据：**75/76**。
- 当前现场端到端成功：**74/76**；当前降级的是 `pubchem` 与 `catalysis_hub`。
- `available` 只代表运行环境、模块、命令、模型或凭据准备好；报告同时列出真实成功 Action，防止误读。

### 6.2 Backend 状态与能力

| Backend | Runtime | 能力 Actions | 健康 | 已成功 Actions | 尚未逐 Action 组合实测 | 当前备注 |
|---|---|---|---|---|---|---|
| `qcelemental`<br>QCElemental | `workflows` | `normalize_qcschema_molecule`, `validate_qcschema_record` | ✅ available | `normalize_qcschema_molecule`, `validate_qcschema_record` | — | ✅ 本地真实 Action 至少一次成功。 |
| `cclib`<br>cclib | `workflows` | `parse_quantum_chemistry_output` | ✅ available | `parse_quantum_chemistry_output` | — | ✅ 本地真实 Action 至少一次成功。 |
| `rdkit`<br>RDKit | `core` | `standardize_structure`, `generate_3d_structure`, `assign_protonation_states`, `cluster_conformers`, `align_molecular_structures`, `calculate_molecular_descriptors`, `calculate_molecular_fingerprint`, `calculate_molecular_similarity`, `search_local_substructures`, `enumerate_tautomers`, `enumerate_stereoisomers` | ✅ available | `align_molecular_structures`, `assign_protonation_states`, `calculate_molecular_descriptors`, `calculate_molecular_fingerprint`, `calculate_molecular_similarity`, `cluster_conformers`, `enumerate_stereoisomers`, `enumerate_tautomers`, `generate_3d_structure`, `search_local_substructures`, `standardize_structure` | — | ✅ 本地真实 Action 至少一次成功。 |
| `openbabel`<br>Open Babel | `quantum` | `generate_3d_structure` | ✅ available | `generate_3d_structure` | — | ✅ 本地真实 Action 至少一次成功。 |
| `rdkit_etkdg`<br>RDKit ETKDG | `core` | `generate_conformer_ensemble` | ✅ available | `generate_conformer_ensemble` | — | ✅ 本地真实 Action 至少一次成功。 |
| `crest`<br>CREST | `reaction` | `generate_conformer_ensemble` | ✅ available | `generate_conformer_ensemble` | — | ✅ 本地真实 Action 至少一次成功。 |
| `internal_statistics`<br>ResearchChem deterministic statistics | `core` | `rank_conformers_from_results` | ✅ available | `rank_conformers_from_results` | — | ✅ 本地真实 Action 至少一次成功。 |
| `pdbfixer`<br>PDBFixer | `md` | `repair_biomolecular_structure`, `assign_protonation_states` | ✅ available | `assign_protonation_states`, `repair_biomolecular_structure` | — | ✅ 本地真实 Action 至少一次成功。 |
| `pdb_tools`<br>pdb-tools | `core` | `select_structure_subset`, `renumber_biomolecular_structure`, `normalize_pdb_records` | ✅ available | `normalize_pdb_records`, `renumber_biomolecular_structure`, `select_structure_subset` | — | ✅ 本地真实 Action 至少一次成功。 |
| `rdkit_gasteiger`<br>RDKit Gasteiger charges | `core` | `assign_partial_charges` | ✅ available | `assign_partial_charges` | — | ✅ 本地真实 Action 至少一次成功。 |
| `openff_am1bcc`<br>OpenFF AM1-BCC | `openff` | `assign_partial_charges` | ✅ available | `assign_partial_charges` | — | ✅ 本地真实 Action 至少一次成功。 |
| `openff`<br>OpenFF Toolkit/Interchange | `openff` | `assign_force_field_parameters` | ✅ available | `assign_force_field_parameters` | — | ✅ 本地真实 Action 至少一次成功。 |
| `openmm_builder`<br>OpenMM system builder | `md` | `assign_force_field_parameters`, `solvate_molecular_system` | ✅ available | `assign_force_field_parameters` | `solvate_molecular_system` | ✅ 本地真实 Action 至少一次成功。 |
| `packmol`<br>Packmol | `md` | `solvate_molecular_system` | ✅ available | `solvate_molecular_system` | — | ✅ 本地真实 Action 至少一次成功。 |
| `spglib`<br>spglib | `workflows` | `analyze_crystal_symmetry`, `standardize_crystal_structure` | ✅ available | `analyze_crystal_symmetry`, `standardize_crystal_structure` | — | ✅ 本地真实 Action 至少一次成功。 |
| `pymatgen`<br>pymatgen | `workflows` | `analyze_crystal_symmetry`, `standardize_crystal_structure`, `build_supercell`, `enumerate_surface_slabs` | ✅ available | `analyze_crystal_symmetry`, `build_supercell`, `enumerate_surface_slabs`, `standardize_crystal_structure` | — | ✅ 本地真实 Action 至少一次成功。 |
| `xtb`<br>xTB | `quantum` | `calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry`, `calculate_dipole_moment`, `calculate_atomic_charges`, `calculate_bond_orders` | ✅ available | `calculate_atomic_charges`, `calculate_bond_orders`, `calculate_dipole_moment`, `calculate_energy`, `calculate_forces` | `calculate_hessian`, `optimize_geometry` | ✅ 本地真实 Action 至少一次成功。 |
| `pyscf`<br>PySCF | `quantum` | `calculate_energy`, `calculate_forces`, `calculate_hessian`, `calculate_dipole_moment`, `calculate_atomic_charges`, `calculate_orbitals`, `calculate_excited_states` | ✅ available | `calculate_energy`, `calculate_excited_states`, `calculate_forces`, `calculate_hessian` | `calculate_atomic_charges`, `calculate_dipole_moment`, `calculate_orbitals` | ✅ 本地真实 Action 至少一次成功。 |
| `gpaw`<br>GPAW | `gpaw` | `calculate_energy`, `calculate_forces`, `optimize_geometry`, `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure`, `calculate_electronic_band_structure`, `calculate_density_of_states`, `calculate_projected_density_of_states` | ✅ available | `calculate_density_of_states`, `calculate_electronic_band_structure`, `calculate_energy`, `calculate_forces`, `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `calculate_projected_density_of_states`, `optimize_geometry`, `relax_periodic_structure` | — | ✅ 本地真实 Action 至少一次成功。 |
| `lobster`<br>LOBSTER | `lobster` | `analyze_periodic_bonding`, `calculate_projected_density_of_states`, `calculate_charge_spilling` | ✅ available | `analyze_periodic_bonding`, `calculate_charge_spilling`, `calculate_projected_density_of_states` | — | ✅ 本地真实 Action 至少一次成功。 |
| `nwchem`<br>NWChem | `nwchem` | `calculate_energy`, `calculate_forces`, `calculate_hessian`, `calculate_dipole_moment`, `calculate_atomic_charges` | ✅ available | `calculate_atomic_charges`, `calculate_dipole_moment`, `calculate_energy`, `calculate_forces`, `calculate_hessian` | — | ✅ 本地真实 Action 至少一次成功。 |
| `openmolcas`<br>OpenMolcas | `openmolcas` | `calculate_energy`, `calculate_dipole_moment`, `calculate_atomic_charges`, `calculate_orbitals` | ✅ available | `calculate_atomic_charges`, `calculate_dipole_moment`, `calculate_energy`, `calculate_orbitals` | — | ✅ 本地真实 Action 至少一次成功。 |
| `multiwfn`<br>Multiwfn | `multiwfn` | `calculate_atomic_charges`, `calculate_bond_orders` | ✅ available | `calculate_atomic_charges`, `calculate_bond_orders` | — | ✅ 本地真实 Action 至少一次成功。 |
| `critic2`<br>Critic2 | `critic2` | `analyze_electron_density_topology`, `calculate_atomic_basin_properties`, `calculate_bader_charges` | ✅ available | `analyze_electron_density_topology`, `calculate_atomic_basin_properties`, `calculate_bader_charges` | — | ✅ 本地真实 Action 至少一次成功。 |
| `psi4`<br>Psi4 | `psi4` | `calculate_energy`, `calculate_hessian`, `calculate_dipole_moment`, `calculate_atomic_charges`, `calculate_orbitals` | ✅ available | `calculate_energy` | `calculate_atomic_charges`, `calculate_dipole_moment`, `calculate_hessian`, `calculate_orbitals` | ✅ 本地真实 Action 至少一次成功。 |
| `tblite`<br>TBLite | `quantum` | `calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry`, `calculate_dipole_moment` | ✅ available | `calculate_energy` | `calculate_dipole_moment`, `calculate_forces`, `calculate_hessian`, `optimize_geometry` | ✅ 本地真实 Action 至少一次成功。 |
| `mace`<br>MACE | `mlip` | `calculate_energy`, `calculate_forces`, `optimize_geometry` | ✅ available | `calculate_energy` | `calculate_forces`, `optimize_geometry` | ✅ 本地真实 Action 至少一次成功。 |
| `chgnet`<br>CHGNet | `mlip` | `calculate_energy`, `calculate_forces`, `optimize_geometry` | ✅ available | `calculate_energy` | `calculate_forces`, `optimize_geometry` | ✅ 本地真实 Action 至少一次成功。 |
| `deepmd`<br>DeePMD-kit | `deepmd` | `calculate_energy`, `calculate_forces`, `optimize_geometry`, `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ available | `calculate_energy`, `calculate_periodic_stress` | `calculate_forces`, `calculate_periodic_energy`, `calculate_periodic_forces`, `optimize_geometry`, `relax_periodic_structure` | ✅ 本地真实 Action 至少一次成功。 |
| `nequip`<br>NequIP | `nequip` | `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ available | `calculate_periodic_forces` | `calculate_periodic_energy`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ 本地真实 Action 至少一次成功。 |
| `allegro`<br>Allegro | `nequip` | `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ available | `calculate_periodic_energy` | `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ 本地真实 Action 至少一次成功。 |
| `orca`<br>ORCA | `quantum` | `calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry`, `calculate_dipole_moment`, `calculate_atomic_charges`, `calculate_orbitals`, `calculate_bond_orders`, `calculate_excited_states` | ✅ available | `calculate_atomic_charges`, `calculate_bond_orders`, `calculate_dipole_moment`, `calculate_energy`, `calculate_excited_states`, `calculate_forces`, `calculate_hessian`, `calculate_orbitals`, `optimize_geometry` | — | ✅ 本地真实 Action 至少一次成功。 |
| `gaussian`<br>Gaussian 16 | `gaussian` | `calculate_energy`, `calculate_hessian`, `optimize_geometry`, `calculate_dipole_moment` | ✅ available | `calculate_hessian` | `calculate_dipole_moment`, `calculate_energy`, `optimize_geometry` | ✅ 本地真实 Action 至少一次成功。 |
| `gamess`<br>GAMESS | `gamess` | `calculate_energy`, `optimize_geometry`, `calculate_dipole_moment` | ✅ available | `calculate_energy` | `calculate_dipole_moment`, `optimize_geometry` | ✅ 本地真实 Action 至少一次成功。 |
| `ase_emt`<br>ASE EMT | `core` | `calculate_energy`, `calculate_forces`, `calculate_hessian`, `optimize_geometry` | ✅ available | `calculate_energy` | `calculate_forces`, `calculate_hessian`, `optimize_geometry` | ✅ 本地真实 Action 至少一次成功。 |
| `internal_vibrations`<br>ResearchChem vibrational analysis | `core` | `derive_vibrational_modes` | ✅ available | `derive_vibrational_modes` | — | ✅ 本地真实 Action 至少一次成功。 |
| `internal_spectroscopy`<br>ResearchChem spectrum builder | `core` | `derive_ir_spectrum`, `derive_uv_vis_spectrum` | ✅ available | `derive_ir_spectrum`, `derive_uv_vis_spectrum` | — | ✅ 本地真实 Action 至少一次成功。 |
| `internal_thermochemistry`<br>ResearchChem statistical thermochemistry | `core` | `derive_thermochemistry` | ✅ available | `derive_thermochemistry` | — | ✅ 本地真实 Action 至少一次成功。 |
| `goodvibes`<br>GoodVibes | `reaction` | `derive_thermochemistry` | ✅ available | `derive_thermochemistry` | — | ✅ 本地真实 Action 至少一次成功。 |
| `geometric`<br>geomeTRIC | `nwchem` | `optimize_geometry` | ✅ available | `optimize_geometry` | — | ✅ 本地真实 Action 至少一次成功。 |
| `sella`<br>Sella | `sella` | `optimize_geometry`, `locate_transition_state` | ✅ available | `locate_transition_state`, `optimize_geometry` | — | ✅ 本地真实 Action 至少一次成功。 |
| `pysisyphus`<br>pysisyphus | `reaction` | `locate_transition_state`, `trace_intrinsic_reaction_coordinate` | ✅ available | `trace_intrinsic_reaction_coordinate` | `locate_transition_state` | ✅ 本地真实 Action 至少一次成功。 |
| `cantera`<br>Cantera | `reaction` | `calculate_chemical_equilibrium`, `integrate_reaction_network` | ✅ available | `calculate_chemical_equilibrium` | `integrate_reaction_network` | ✅ 本地真实 Action 至少一次成功。 |
| `scipy`<br>SciPy | `reaction` | `integrate_reaction_network` | ✅ available | `integrate_reaction_network` | — | ✅ 本地真实 Action 至少一次成功。 |
| `rmg`<br>RMG-Py | `rmg` | `calculate_rate_constants`, `calculate_tunneling_correction` | ✅ available | `calculate_rate_constants`, `calculate_tunneling_correction` | — | ✅ 本地真实 Action 至少一次成功。 |
| `mess`<br>MESS | `mess` | `solve_master_equation` | ✅ available | `solve_master_equation` | — | ✅ 本地真实 Action 至少一次成功。 |
| `mesmer`<br>MESMER | `mesmer` | `solve_master_equation` | ✅ available | `solve_master_equation` | — | ✅ 本地真实 Action 至少一次成功。 |
| `catmap`<br>CatMAP | `reaction` | `solve_microkinetic_model` | ✅ available | `solve_microkinetic_model` | — | ✅ 本地真实 Action 至少一次成功。 |
| `openmm`<br>OpenMM | `md` | `minimize_system_energy`, `propagate_dynamics`, `calculate_force_field_energy`, `calculate_force_field_forces`, `decompose_force_field_energy` | ✅ available | `calculate_force_field_energy`, `calculate_force_field_forces`, `decompose_force_field_energy` | `minimize_system_energy`, `propagate_dynamics` | ✅ 本地真实 Action 至少一次成功。 |
| `gromacs`<br>GROMACS | `md` | `minimize_system_energy`, `propagate_dynamics` | ✅ available | `minimize_system_energy` | `propagate_dynamics` | ✅ 本地真实 Action 至少一次成功。 |
| `lammps`<br>LAMMPS | `md` | `minimize_system_energy`, `propagate_dynamics` | ✅ available | `minimize_system_energy` | `propagate_dynamics` | ✅ 本地真实 Action 至少一次成功。 |
| `hoomd`<br>HOOMD-blue | `free_energy` | `minimize_system_energy`, `propagate_dynamics`, `calculate_force_field_energy`, `calculate_force_field_forces` | ✅ available | `calculate_force_field_energy`, `calculate_force_field_forces`, `minimize_system_energy`, `propagate_dynamics` | — | ✅ 本地真实 Action 至少一次成功。 |
| `namd`<br>NAMD 3 | `namd` | `minimize_system_energy`, `propagate_dynamics` | ✅ available | `minimize_system_energy` | `propagate_dynamics` | ✅ 本地真实 Action 至少一次成功。 |
| `amber_pmemd`<br>Amber 26 PMEMD | `amber` | `minimize_system_energy`, `propagate_dynamics` | ✅ available | `minimize_system_energy` | `propagate_dynamics` | ✅ 本地真实 Action 至少一次成功。 |
| `charmm`<br>CHARMM c50b2 | `charmm` | `minimize_system_energy`, `propagate_dynamics` | ✅ available | `minimize_system_energy` | `propagate_dynamics` | ✅ 本地真实 Action 至少一次成功。 |
| `mdanalysis`<br>MDAnalysis | `md` | `calculate_trajectory_rmsd`, `calculate_radius_of_gyration`, `calculate_radial_distribution`, `calculate_mean_squared_displacement`, `calculate_dihedral_distribution`, `calculate_hydrogen_bonds`, `calculate_principal_components`, `calculate_dynamic_cross_correlation` | ✅ available | `calculate_dynamic_cross_correlation`, `calculate_hydrogen_bonds`, `calculate_mean_squared_displacement`, `calculate_principal_components`, `calculate_radial_distribution` | `calculate_dihedral_distribution`, `calculate_radius_of_gyration`, `calculate_trajectory_rmsd` | ✅ 本地真实 Action 至少一次成功。 |
| `mdtraj`<br>MDTraj | `workflows` | `calculate_trajectory_rmsd`, `calculate_radius_of_gyration`, `calculate_contacts`, `calculate_solvent_accessible_surface`, `calculate_dihedral_distribution`, `assign_secondary_structure`, `cluster_trajectory` | ✅ available | `assign_secondary_structure`, `calculate_contacts`, `calculate_dihedral_distribution`, `calculate_radius_of_gyration`, `calculate_solvent_accessible_surface`, `calculate_trajectory_rmsd`, `cluster_trajectory` | — | ✅ 本地真实 Action 至少一次成功。 |
| `plumed`<br>PLUMED | `md` | `evaluate_collective_variables` | ✅ available | `evaluate_collective_variables` | — | ✅ 本地真实 Action 至少一次成功。 |
| `pymbar`<br>PyMBAR | `free_energy` | `estimate_free_energy_difference`, `estimate_thermodynamic_expectations`, `calculate_potential_of_mean_force`, `analyze_free_energy_convergence` | ✅ available | `analyze_free_energy_convergence`, `calculate_potential_of_mean_force`, `estimate_free_energy_difference`, `estimate_thermodynamic_expectations` | — | ✅ 本地真实 Action 至少一次成功。 |
| `alchemlyb`<br>alchemlyb | `free_energy` | `parse_alchemical_energy_data` | ✅ available | `parse_alchemical_energy_data` | — | ✅ 本地真实 Action 至少一次成功。 |
| `quantum_espresso`<br>Quantum ESPRESSO | `qe` | `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ available | `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress` | `relax_periodic_structure` | ✅ 本地真实 Action 至少一次成功。 |
| `cp2k`<br>CP2K | `cp2k` | `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ available | `calculate_periodic_energy` | `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ 本地真实 Action 至少一次成功。 |
| `siesta`<br>SIESTA | `periodic` | `calculate_periodic_energy`, `calculate_periodic_forces`, `relax_periodic_structure` | ✅ available | `calculate_periodic_energy`, `calculate_periodic_forces` | `relax_periodic_structure` | ✅ 本地真实 Action 至少一次成功。 |
| `dftbplus`<br>DFTB+ | `periodic` | `calculate_periodic_energy`, `calculate_periodic_forces`, `relax_periodic_structure` | ✅ available | `calculate_periodic_energy`, `calculate_periodic_forces`, `relax_periodic_structure` | — | ✅ 本地真实 Action 至少一次成功。 |
| `abinit`<br>ABINIT | `abinit` | `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ available | `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress` | `relax_periodic_structure` | ✅ 本地真实 Action 至少一次成功。 |
| `vasp`<br>VASP | `vasp` | `calculate_periodic_energy`, `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ available | `calculate_periodic_energy` | `calculate_periodic_forces`, `calculate_periodic_stress`, `relax_periodic_structure` | ✅ 本地真实 Action 至少一次成功。 |
| `phonopy`<br>Phonopy | `phonons` | `generate_displaced_supercells`, `assemble_force_constants`, `calculate_phonon_dispersion`, `calculate_phonon_density_of_states`, `calculate_harmonic_thermodynamics`, `calculate_phonon_group_velocities` | ✅ available | `assemble_force_constants`, `calculate_harmonic_thermodynamics`, `calculate_phonon_density_of_states`, `calculate_phonon_dispersion`, `calculate_phonon_group_velocities`, `generate_displaced_supercells` | — | ✅ 本地真实 Action 至少一次成功。 |
| `phono3py`<br>Phono3py | `phonons` | `generate_displaced_supercells`, `assemble_force_constants`, `calculate_phonon_dispersion`, `calculate_phonon_density_of_states`, `calculate_harmonic_thermodynamics`, `calculate_phonon_group_velocities`, `calculate_lattice_thermal_conductivity` | ✅ available | `calculate_harmonic_thermodynamics`, `calculate_lattice_thermal_conductivity`, `calculate_phonon_group_velocities` | `assemble_force_constants`, `calculate_phonon_density_of_states`, `calculate_phonon_dispersion`, `generate_displaced_supercells` | ✅ 本地真实 Action 至少一次成功。 |
| `shengbte`<br>ShengBTE | `shengbte` | `calculate_lattice_thermal_conductivity` | ✅ available | `calculate_lattice_thermal_conductivity` | — | ✅ 本地真实 Action 至少一次成功。 |
| `vina`<br>AutoDock Vina | `docking` | `dock_ligand` | ✅ available | `dock_ligand` | — | ✅ 本地真实 Action 至少一次成功。 |
| `gnina`<br>GNINA | `docking` | `dock_ligand` | ✅ available | `dock_ligand` | — | ✅ 本地真实 Action 至少一次成功。 |
| `pubchem`<br>PubChem PUG REST | `services` | `search_compounds`, `resolve_chemical_identity`, `retrieve_compound_properties`, `retrieve_compound_structure`, `search_similar_compounds`, `search_substructures` | ✅ available | `search_compounds` | `resolve_chemical_identity`, `retrieve_compound_properties`, `retrieve_compound_structure`, `search_similar_compounds`, `search_substructures` | ⚠️ 安装与契约测试正常；当前官方 PUG REST 对本机返回 503 ServerBusy。 |
| `rcsb_pdb`<br>RCSB PDB Data API | `services` | `search_protein_structures` | ✅ available | `search_protein_structures` | — | ✅ 当前在线实测成功。 |
| `materials_project`<br>Materials Project | `services` | `search_materials` | ✅ available | `search_materials` | — | ✅ 当前在线实测成功。 |
| `catalysis_hub`<br>Catalysis-Hub GraphQL | `services` | `search_catalysis_records` | ✅ available | — | `search_catalysis_records` | ⚠️ 当前 GraphQL 端点 503/ReadTimeout，本轮没有成功调用。 |
| `nist_webbook`<br>NIST Chemistry WebBook SRD 69 CGI | `services` | `lookup_nist_webbook_species` | ✅ available | `lookup_nist_webbook_species` | — | ✅ 当前在线实测成功。 |

### 6.3 Backend 环境与资源要求

| Backend | Python 模块 | 命令/可执行文件 | Conda/Pip | 环境变量 | 科学数据/模型资源 | License |
|---|---|---|---|---|---|---|
| `qcelemental` | qcelemental=0.50.4 | — | conda:qcelemental=0.50.4 | — | — | `open_source` |
| `cclib` | cclib=0.0.0 | — | conda:cclib=1.8.1 | — | — | `open_source` |
| `rdkit` | rdkit=2025.3.3 | — | conda:rdkit | — | — | `open_source` |
| `openbabel` | openbabel=OK | obabel=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/quantum/bin/obabel | conda:openbabel | — | — | `open_source` |
| `rdkit_etkdg` | rdkit=2025.3.3 | — | conda:rdkit | — | — | `open_source` |
| `crest` | — | crest=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/reaction/bin/crest | conda:crest<br>conda:xtb | CHEMGRAPH_CREST_COMMAND=set | — | `open_source` |
| `internal_statistics` | — | — | — | — | — | `open_source` |
| `pdbfixer` | pdbfixer=1.12.0<br>openmm=8.5.2 | — | conda:pdbfixer<br>conda:openmm | — | — | `open_source` |
| `pdb_tools` | pdbtools=OK | pdb_selchain=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.toolbox_env/bin/pdb_selchain<br>pdb_reres=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.toolbox_env/bin/pdb_reres<br>pdb_tidy=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.toolbox_env/bin/pdb_tidy | pip:pdb-tools==2.7.0 | — | — | `open_source` |
| `rdkit_gasteiger` | rdkit=2025.3.3 | — | conda:rdkit | — | — | `open_source` |
| `openff_am1bcc` | openff.toolkit=0.18.1 | antechamber=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/openff/bin/antechamber<br>sqm=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/openff/bin/sqm | conda:openff-toolkit<br>conda:ambertools | — | — | `open_source` |
| `openff` | openff.toolkit=0.18.1<br>openff.interchange=0.5.3 | — | conda:openff-toolkit<br>conda:openff-interchange | — | — | `open_source` |
| `openmm_builder` | openmm=8.5.2 | — | conda:openmm | — | — | `open_source` |
| `packmol` | — | packmol=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/md/bin/packmol | conda:packmol | — | — | `open_source` |
| `spglib` | spglib=2.7.0<br>numpy=2.4.6 | — | conda:spglib<br>conda:numpy | — | — | `open_source` |
| `pymatgen` | pymatgen=2026.5.4<br>numpy=2.4.6 | — | conda:pymatgen<br>conda:numpy | — | — | `open_source` |
| `xtb` | — | xtb=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/quantum/bin/xtb | conda:xtb | CHEMGRAPH_XTB_COMMAND=set | — | `open_source` |
| `pyscf` | pyscf=2.13.1 | — | pip:pyscf | — | — | `open_source` |
| `gpaw` | gpaw=25.7.0<br>ase=3.29.0<br>numpy=2.4.6 | gpaw=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/gpaw/bin/gpaw | conda:gpaw=25.7.0<br>conda:ase<br>conda:numpy | — | `GPAW PAW setup datasets under .software_cache/gpaw/setups` | `open_source` |
| `lobster` | pymatgen=2026.5.4<br>numpy=2.4.6 | lobster-5.1.0=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/lobster/5.1.0/package/lobster-5.1.0 | conda:pymatgen | CHEMGRAPH_LOBSTER_COMMAND=set | — | `academic_license` |
| `nwchem` | qcengine=0.50.0<br>qcelemental=0.50.4<br>numpy=2.4.6 | nwchem=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/nwchem/bin/nwchem | conda:nwchem=7.3.1<br>conda:qcengine=0.50.0<br>conda:qcelemental=0.50.4<br>conda:cclib | NWCHEM_BASIS_LIBRARY=set | `NWChem basis libraries under .software_cache/nwchem/source/src/basis/libraries` | `open_source` |
| `openmolcas` | — | pymolcas=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/openmolcas/25.10/pymolcas | — | CHEMGRAPH_OPENMOLCAS_COMMAND=set | `OpenMolcas v25.10 basis_library managed under .software_cache/openmolcas/25.10` | `open_source` |
| `multiwfn` | — | Multiwfn_noGUI=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/Multiwfn_noGUI | — | CHEMGRAPH_MULTIWFN_COMMAND=set | `Agent-supplied fch/fchk/wfn/wfx/mwfn/Molden/47 wavefunction file; both required Multiwfn citations are returned in provenance` | `custom_open_source_citation_required` |
| `critic2` | — | critic2=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/critic2/install-conda/bin/critic2 | — | CHEMGRAPH_CRITIC2_COMMAND=set | `Agent-supplied electron-density grid or compatible wavefunction file; an explicit separate structure file is required when the density file does not contain geometry` | `open_source` |
| `psi4` | psi4=OK | psi4=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/psi4/bin/psi4 | conda:psi4 | — | — | `open_source` |
| `tblite` | tblite=0.4.0<br>ase=3.29.0 | — | pip:tblite==0.4.0 | — | — | `open_source` |
| `mace` | mace.calculators=OK<br>ase=3.29.0 | — | pip:mace-torch==0.3.16 | — | — | `open_source` |
| `chgnet` | chgnet=0.4.2<br>ase=3.29.0 | — | pip:chgnet | — | — | `open_source` |
| `deepmd` | deepmd=OK<br>ase=3.29.0 | dp=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/deepmd_models/bin/dp | pip:deepmd-kit==3.2.0b0<br>pip:ase<br>pip:e3nn | — | `Explicit resource:// DeePMD model checkpoint; multitask checkpoints require a named model_branch and single-task checkpoints require model_branch=single_task` | `open_source` |
| `nequip` | nequip=0.19.0<br>torch=2.10.0<br>e3nn=0.6.0<br>ase=3.29.0 | nequip-train=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/nequip/bin/nequip-train | pip:nequip==0.19.0 | — | `Explicit resource:// NequIP checkpoint or workspace model ArtifactRef` | `open_source` |
| `allegro` | allegro=OK<br>nequip=0.19.0<br>torch=2.10.0<br>e3nn=0.6.0<br>ase=3.29.0 | — | pip:nequip-allegro==0.8.3<br>pip:nequip==0.19.0 | — | `Explicit resource:// Allegro checkpoint or workspace model ArtifactRef` | `open_source` |
| `orca` | — | orca=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/orca/6.1.1/orca | — | CHEMGRAPH_ORCA_COMMAND=set | — | `manual_license` |
| `gaussian` | — | g16=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/gaussian/g16/install/g16/g16<br>formchk=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/gaussian/g16/install/g16/formchk | — | CHEMGRAPH_GAUSSIAN_COMMAND=set<br>CHEMGRAPH_GAUSSIAN_FORMCHK_COMMAND=set | — | `commercial_license` |
| `gamess` | — | rungms=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/gamess/2024-r2-p1/source/rungms | — | CHEMGRAPH_GAMESS_COMMAND=set | — | `registration_license` |
| `ase_emt` | ase.calculators.emt=3.29.0 | — | pip:ase | — | — | `open_source` |
| `internal_vibrations` | numpy=1.26.4 | — | pip:numpy | — | — | `open_source` |
| `internal_spectroscopy` | numpy=1.26.4 | — | pip:numpy | — | — | `open_source` |
| `internal_thermochemistry` | ase=3.29.0<br>numpy=1.26.4 | — | pip:ase<br>pip:numpy | — | — | `open_source` |
| `goodvibes` | goodvibes=3.2 | goodvibes=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/reaction/bin/goodvibes | conda:goodvibes | — | — | `open_source` |
| `geometric` | geometric=1.1.1<br>numpy=2.4.6 | — | pip:geometric==1.1.1 | — | — | `open_source` |
| `sella` | sella=2.5.0<br>ase=3.29.0<br>numpy=2.4.6 | — | pip:sella==2.5.0 | — | — | `open_source` |
| `pysisyphus` | pysisyphus=1.0.0 | pysis=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/reaction/bin/pysis | pip:pysisyphus==1.0.0 | — | — | `open_source` |
| `cantera` | cantera=3.2.0 | — | conda:cantera | — | — | `open_source` |
| `scipy` | scipy=1.15.2 | — | pip:scipy | — | — | `open_source` |
| `rmg` | rmgpy=OK | rmg.py=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/rmg/bin/rmg.py | conda:rmg=4.0.0 | — | — | `open_source` |
| `mess` | — | mess=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/mess/2020.1.24/build/mess | — | CHEMGRAPH_MESS_COMMAND=set | — | `open_source` |
| `mesmer` | — | mesmer=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/mesmer/7.1/bin/mesmer | — | CHEMGRAPH_MESMER_COMMAND=set | — | `open_source` |
| `catmap` | catmap=OK | — | pip:git+https://github.com/SUNCAT-Center/catmap.git | — | — | `open_source` |
| `openmm` | openmm=8.5.2 | — | conda:openmm | — | — | `open_source` |
| `gromacs` | — | gmx=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/md/bin/gmx | conda:gromacs | CHEMGRAPH_GROMACS_COMMAND=set | — | `open_source` |
| `lammps` | lammps=2025.7.22 | lmp=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/md/bin/lmp | conda:lammps | CHEMGRAPH_LAMMPS_COMMAND=set | — | `open_source` |
| `hoomd` | hoomd=OK<br>numpy=2.4.6 | — | conda:hoomd=7.1.0<br>conda:numpy | — | — | `open_source` |
| `namd` | — | namd3=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/namd/3.0.2/multicore-avx512/namd3 | — | CHEMGRAPH_NAMD_COMMAND=set | — | `academic_registration` |
| `amber_pmemd` | — | pmemd=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/amber/26/install/bin/pmemd<br>pmemd.MPI=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/amber/26/install/bin/pmemd.MPI<br>mpirun=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/amber/bin/mpirun | — | CHEMGRAPH_AMBER_COMMAND=set<br>CHEMGRAPH_AMBER_MPI_COMMAND=set<br>CHEMGRAPH_AMBER_MPIRUN_COMMAND=set<br>CHEMGRAPH_AMBER_MPI_EXECUTABLE=set | — | `academic_registration` |
| `charmm` | — | charmm=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/charmm/50b2/install/bin/charmm | — | CHEMGRAPH_CHARMM_COMMAND=set | — | `academic_registration` |
| `mdanalysis` | MDAnalysis=2.9.0 | — | pip:MDAnalysis | — | — | `open_source` |
| `mdtraj` | mdtraj=1.11.1<br>numpy=2.4.6 | — | conda:mdtraj<br>conda:numpy | — | — | `open_source` |
| `plumed` | — | plumed=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/md/bin/plumed | conda:plumed | CHEMGRAPH_PLUMED_COMMAND=set | — | `open_source` |
| `pymbar` | pymbar=4.2.0<br>numpy=2.4.6 | — | conda:pymbar<br>conda:numpy | — | — | `open_source` |
| `alchemlyb` | alchemlyb=0.0.0<br>pandas=2.3.3<br>numpy=2.4.6 | — | conda:alchemlyb=2.5.0<br>conda:pandas<br>conda:numpy | — | — | `open_source` |
| `quantum_espresso` | — | pw.x=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/qe/bin/pw.x | conda:qe | CHEMGRAPH_QE_COMMAND=set | `Explicit ResourceRefs from qe_sssp_1_3_pbe_efficiency or qe_sssp_1_3_pbe_precision, one per element; workspace ArtifactRefs remain accepted` | `open_source` |
| `cp2k` | — | cp2k=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/cp2k/bin/cp2k.psmp | conda:cp2k | CHEMGRAPH_CP2K_COMMAND=set | — | `open_source` |
| `siesta` | — | siesta=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/periodic/bin/siesta | conda:siesta | CHEMGRAPH_SIESTA_COMMAND=set | `Explicit ResourceRefs from siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml, one per element; workspace ArtifactRefs remain accepted` | `open_source` |
| `dftbplus` | — | dftb+=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/periodic/bin/dftb+ | conda:dftbplus | CHEMGRAPH_DFTBPLUS_COMMAND=set | `Explicit ResourceRef to dftb_3ob_3_1 or dftb_matsci_0_3 with all required directed element-pair SKF files; workspace directory ArtifactRefs remain accepted` | `open_source` |
| `abinit` | numpy=2.2.6<br>pydantic=2.13.4<br>yaml=OK | abinit=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/abinit/bin/abinit | conda:abinit | CHEMGRAPH_ABINIT_COMMAND=missing | `Explicit ResourceRefs from abinit_pseudo_dojo_nc_sr_pbe_standard_psp8, one per element; workspace ArtifactRefs remain accepted` | `open_source` |
| `vasp` | — | vasp_std=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/vasp/6.3.2/bin/vasp_std | — | CHEMGRAPH_VASP_COMMAND=set | `One explicit POTCAR ResourceRef or workspace ArtifactRef per element; five operator-supplied production families expose exact directory-name variants and no family or variant is selected automatically` | `commercial_license` |
| `phonopy` | phonopy=4.3.1 | phonopy=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/phonons/bin/phonopy | conda:phonopy | — | — | `open_source` |
| `phono3py` | phono3py=4.3.3 | phono3py=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/phonons/bin/phono3py | conda:phono3py | — | — | `open_source` |
| `shengbte` | — | ShengBTE=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/shengbte/source/ShengBTE | — | CHEMGRAPH_SHENGBTE_COMMAND=set | — | `open_source` |
| `vina` | vina=1.2.7 | vina=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.tool_envs/docking/bin/vina | conda:vina | CHEMGRAPH_VINA_COMMAND=set | — | `open_source` |
| `gnina` | — | gnina=/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.software_cache/gnina/1.3.3/gnina.cuda12.8.static | — | CHEMGRAPH_GNINA_COMMAND=set | — | `open_source` |
| `pubchem` | pubchempy=1.0.5 | — | pip:pubchempy==1.0.5 | — | — | `open_source` |
| `rcsb_pdb` | httpx=0.28.1 | — | pip:httpx>=0.28 | — | — | `open_source` |
| `materials_project` | httpx=0.28.1<br>mp_api=0.45.13 | — | conda:mp-api | MP_API_KEY=set | — | `open_source` |
| `catalysis_hub` | httpx=0.28.1 | — | pip:httpx>=0.28 | — | — | `open_source` |
| `nist_webbook` | httpx=0.28.1 | — | pip:httpx>=0.28 | — | `NIST Chemistry WebBook SRD 69 official CGI and its SRD copyright/licensing terms` | `nist_srd_terms` |

## 7. 用户要求的软件/工具清单状态

当前受管理清单共 59 项：

- `configured`: **46**
- `partial`: **2**
- `manual_required`: **9**
- `manual_api_review`: **1**
- `specification`: **1**（QCSchema 不是独立软件）

### 7.1 已安装但不直接作为公共 Action 暴露的软件

这些组件可以提供底层能力或未来扩展，但直接暴露一个固定工作流会削弱 benchmark 对智能体编排能力的评估。

| 软件 | Runtime | 作用/当前处理 |
|---|---|---|
| `QCEngine` | `workflows` | Execution substrate rather than a separate scientific result; NWChem public actions use its exact QCSchema harness, but no generic QCEngine workflow runner is exposed. |
| `AiiDA` | `workflows` | Profile researchchembench is initialized with SQLite under .software_cache/aiida; it remains infrastructure because exposing a fixed AiiDA workflow would hide the Agent's tool ordering and backend choices. |
| `atomate2` | `workflows` | Installed as a library only; no fixed workflow is exposed as a public Action. |
| `jobflow` | `workflows` | A minimal add(2,3) local flow passed; Agent still chooses job ordering and inputs. |
| `CENSO` | `reaction` | CENSO is available in the reaction runtime; complete runs still require explicit CREST/ORCA/TURBOMOLE choices and inputs. |
| `autodE` | `nwchem` | Library installed with NWChem support dependencies; no monolithic workflow Action is exposed. |
| `Wannier90` | `qe` | Existing Quantum ESPRESSO runtime already provides wannier90.x. |
| `Yambo` | `yambo` | Yambo 5.3.0 binary is installed; no upstream wavefunction database or fixed input is generated. |
| `AutoMeKin` | `automekin` | Official source was built in an isolated conda environment with the bundled MOPAC engine; a real water PM7 single-point job ended normally. Gaussian is configured independently, but AutoMeKin-to-Gaussian/Qcore coupling is not prewired or selected implicitly. |
| `KinBot` | `kinbot` | KinBot 2.2.2 and dependencies import successfully in a repaired NumPy 1.26 / JAX 0.4.35 runtime with no pip dependency conflicts; real PES execution requires explicit input and remains a workflow-level capability rather than a public monolithic runner. |
| `SHARC` | `sharc` | SHARC4 core binaries and wfoverlap_ascii were compiled; PySHARC/NetCDF and full trajectories still require explicit electronic-structure interfaces and task inputs. |
| `Newton-X` | `newtonx` | Newton-X New Series 3.5.3 is installed and the bundled analytical avoided-crossing test passed. It remains runtime-only until a typed nonadiabatic Action can expose states, couplings, hopping controls and an explicit electronic-structure interface without becoming a monolithic workflow runner. |
| `TheoDORE` | `theodore` | TheoDORE 2.5.0 imports and CLI starts; optional Orbkit/OpenBabel extensions are not installed. |
| `VMD` | `vmd` | VMD 1.9.3 text-mode startup passed; GUI operation depends on DISPLAY/OpenGL. |
| `VESTA` | `vesta` | Official VESTA 3.90.5a GTK3 x86_64 package is installed with locally extracted Ubuntu runtime libraries; an Xvfb headless launch remained healthy until the bounded smoke timeout. Interactive GUI use still requires DISPLAY/OpenGL, and redistribution is prohibited by the VESTA license. |

### 7.2 尚未完成或需要人工决策的软件

| 软件 | 状态 | 原因 | 需要用户做什么 |
|---|---|---|---|
| `Q-Chem` | **manual_required** | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog; do not install or expose it unless the operator later reverses this decision and supplies a valid license. | 若未来启用，提供合法许可证和官方安装包；当前按用户决定保持屏蔽。 |
| `Molpro` | **manual_required** | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog; re-enable only after a deliberate operator decision and valid license/site installation. | 若未来启用，提供合法许可证和官方安装包；当前保持屏蔽。 |
| `TURBOMOLE` | **manual_required** | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog; CENSO must not select it implicitly. | 若未来启用，提供合法许可证和官方安装；当前不得由 CENSO 隐式选择。 |
| `CASTEP` | **manual_required** | Requires STFC academic/commercial license and a site build. | 如需启用，取得 STFC/商业许可并提供站点安装包或可用二进制。 |
| `CRYSTAL` | **manual_required** | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog. | 若未来启用，提供许可证和官方安装；当前保持屏蔽。 |
| `WIEN2k` | **manual_required** | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog. | 若未来启用，提供许可证和站点安装；当前保持屏蔽。 |
| `Arkane` | **partial** | Shipped with RMG-Py, Arkane.py and the official database are present. Top-level import remains pathologically slow and a bundled H thermochemistry example exceeded a 300-second bound, so this stays partial until the runtime is repaired or a bounded real calculation passes. | 无需额外下载；需要后续定位导入/示例运行超过 300 秒的问题并做更小的类型化 Action。 |
| `EasySpin` | **partial** | EasySpin 6.0.12 toolbox files are staged and structurally validated. Official MATLAB R2018a installation media are now cached, but no licensed MATLAB executable exists yet; executable EasySpin validation remains blocked on a legitimate File Installation Key/license file or license server. | EasySpin 文件已缓存；需先有合法 MATLAB 可执行环境，再做真实 EPR smoke。 |
| `MATLAB` | **manual_required** | Both official MATLAB R2018a Linux ISO images are staged in .software_cache (DVD1 SHA-256 780717eeeaf11855a119ffe5e3e8be3443df4b1b79a2dcb04feb4c3ea7eb693e; DVD2 485467b9662b7d2f6bbf92b84b18b95fed93a9d6fc6ead4c806b1b67e9296997). The separately downloaded crack archive was deliberately not copied, opened or used. Installation and EasySpin execution require a legitimate MathWorks File Installation Key plus license file/server information. | 安装介质已缓存，但仍需合法许可证和可执行安装；只有需要 EasySpin 执行时才必须处理。 |
| `OpenEye` | **manual_required** | Explicitly disabled by the operator because it is not needed and no license is available. It is absent from BackendSpecs and the MCP catalog; a conda package alone would not authorize use without a valid OpenEye license. | Conda 包不能替代许可证；当前按用户决定保持屏蔽。 |
| `Schrödinger` | **manual_required** | The supplied schroedinger-1.0.11-7 Arch package was identified from .PKGINFO as an ANSI C implementation of the Dirac video codec, not the commercial Schrödinger chemistry suite. It is retained only under .software_cache/schrodinger/rejected with SHA-256 41906fcce0eeb74edcaf50ee46635c2f336703692d956782dba7dd1f419187b7 and is not installed or exposed. A genuine Schrödinger Suite installer and site license are still required if this backend is wanted. | 当前文件是同名 Dirac 视频编解码包，不是化学套件；若启用需提供商业 Schrödinger 官方安装包与许可证。 |
| `NIST CCCBDB 接口` | **manual_api_review** | CCCBDB has no public documented REST/JSON API and is suitable only for limited interactive single-molecule webpage use. It remains outside BackendSpecs and is not exposed through MCP; no brittle page scraping or bulk crawler is added. | 官方无公开文档化 REST/JSON API；建议继续不做脆弱网页抓取，除非定义极受限的人工维护查询。 |

## 8. 当前问题清单

### 8.1 当前运行问题

1. **PubChem PUG REST**：本机连续收到 `503 PUGREST.ServerBusy`。这影响 `search_compounds`、`resolve_chemical_identity`、`retrieve_compound_properties`、`retrieve_compound_structure`、`search_similar_compounds` 和 `search_substructures`。适配器契约测试仍通过，问题属于当前官方服务/共享出口限流。
2. **Catalysis-Hub GraphQL**：当前出现 `503 Service Unavailable` 和 `ReadTimeout`，影响 `search_catalysis_records`。
3. **Materials Project 凭据**：Backend 健康依赖 `MP_API_KEY`；当前 `config.local.env` 已配置且现场查询通过。部署到新节点时必须同步安全配置。

### 8.2 非当前故障但仍需说明的限制

- 62 个替代 Action–Backend 组合尚未逐组合运行，例如一个 Action 的所有量化软件、所有 MD 引擎和所有 ML 势都没有对该 Action 全覆盖。
- GPU 路径未系统验证；当前 smoke 以 CPU 为主，NAMD CUDA、PMEMD CUDA、GNINA GPU 等没有被自动选择。
- 大体系、长轨迹、并行扩展、队列调度、断点恢复和生产级收敛尚未在本报告中验证。
- 商业/注册软件的可用性依赖现有站点许可证和文件，不代表可以复制到任意服务器。
- 在线数据源状态会随时间变化；报告中的 503/timeout 是 2026-07-20 的现场结果。

## 9. 汇报建议

建议在正式汇报中使用下面这段结论：

> ResearchChemBench 当前公开 101 个原子化化学 Actions 和 76 个明确可选 BackendSpecs。智能体必须自行选择 Action、软件后端、方法和调用顺序，系统不进行科学自动 fallback。91 个本地 Scientific Actions 均已有代表性端到端成功记录，71 个本地后端均至少真实执行过一个 Action；全量回归 146/146 通过。当前主要运行问题集中在在线数据服务：PubChem 和 Catalysis-Hub 在审计时出现 503/超时，因此当前现场可用 Action 为 94/101。工具箱已较好覆盖结构准备、化学信息学、分子基态电子结构、经典 MD 与轨迹/自由能分析、反应动力学、周期 DFT、声子/热输运、对接和数据接口，但高级多参考/非绝热、QM/MM、增强采样执行、电化学、GW/BSE/Wannier、KMC、缺陷/相图及更广光谱仍是后续重点。

## 10. 关联文档与可复现命令

关联文档：

- `docs/tools/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md`：完整 Action/Backend/runtime/resource 参数矩阵。
- `docs/tools/CHEMISTRY_TOOLBOX_SOFTWARE_CAPABILITY_MATRIX.md`：软件版本、官方资料缓存和候选能力。
- `docs/tools/CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md`：59 项用户软件清单。
- `.software_cache/documentation/catmap/0.3.1/`：本次 CatMAP 官方教程、代码概览和仓库页面缓存。

复现命令：

```bash
.toolbox_env/bin/python -m pytest -q --junitxml=config/pytest_status.xml
.toolbox_env/bin/python scripts/run_action_gap_smokes.py
.toolbox_env/bin/python scripts/run_action_gap_smokes.py --include-network
.toolbox_env/bin/python scripts/run_backend_gap_smokes.py
.toolbox_env/bin/python scripts/run_scientific_resource_smokes.py
.toolbox_env/bin/python scripts/run_data_source_smokes.py
.toolbox_env/bin/python scripts/audit_action_test_coverage.py
.toolbox_env/bin/python scripts/generate_detailed_toolbox_audit_report.py
```

## 11. 官方资料

- CatMAP 微观动力学模型要求显式反应表达式、表面/描述符、物种定义和能量输入；本工具箱现在按其官方 setup-file API 生成受控模型：[CatMAP 创建微观动力学模型教程](https://catmap.readthedocs.io/en/latest/tutorials/creating_a_microkinetic_model.html)。
- CatMAP 的 parser/scaler/solver/mapper 架构说明：[CatMAP Code Overview](https://catmap.readthedocs.io/en/latest/topics/code_overview.html)。
- PubChem PUG REST 官方接口说明：[PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)。
