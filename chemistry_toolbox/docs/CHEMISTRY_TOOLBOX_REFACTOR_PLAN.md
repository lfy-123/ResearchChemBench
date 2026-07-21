# ResearchChem 化学工具箱重新整合方案（Benchmark 自主编排版，已实施）

> 文档状态：已确认并完成第一阶段实施；实施结果见 `CHEMISTRY_TOOLBOX_REFACTOR_REPORT.md`
> 更新日期：2026-07-18
> 适用仓库：ResearchChemBench
> 实施范围：核心工具箱、MCP 暴露、后端运行时、Artifact/trace、系统提示词、配置、测试与文档

## 1. 这次重构的明确结论

本次不再把现有 41 个工具视为需要保留的公共 API，也不做简单重命名、重新分组或在外面增加一层门面。

目标是重新构造一套真正同层次的化学工具箱：

- 公共工具只表达一个边界明确、可独立验证的科学操作；
- 每个工具只有一种主要科学结果；
- 软件名、运行框架、文件操作和系统管理不出现在公共工具名中；
- `run_ase` 必须删除，不能改名后继续作为多任务入口；
- `run_xtb`、`run_pyscf`、`run_cp2k` 等软件启动器也不再作为公共工具；
- ASE、xTB、PySCF、Psi4、CP2K、OpenMM 等全部成为内部后端；
- 多步骤任务由智能体显式组合原子工具，不包装成默认流程工具；
- Benchmark 默认向智能体完整暴露全部原子计算行动、数据行动和后端能力目录，不按任务检索、裁剪、排序或预选候选范围；
- 智能体在每次计算调用中显式选择 `backend_id` 以及会影响科学结果的方法、基组、模型、力场和关键设置；系统不替智能体选择计算软件；
- 系统只校验并执行智能体提交的精确选择，不自动切换后端、方法或工具；失败后的重试、改参、换软件和改变调用顺序均由智能体决定；
- recipe、参考流程和标准答案只供维护者、测试与评测器使用，不注入正在接受评测的智能体上下文；
- 当前工具可以删除、合并、拆分或重写，不以兼容旧 41 个接口为约束；
- MCP 只是可选的暴露方式，核心工具箱与 MCP 解耦。

最终形态不是“41 个旧工具 + 一层新名称”，而是：

> 一套统一化学对象协议 + 同粒度原子科学行动 + 可替换后端 + Artifact 链 + 独立数据源 + 多种传输绑定。

## 2. 当前实现基线与上一版不足

### 2.1 当前事实基线

2026-07-18 的真实测试结果为：

| 检查项 | 结果 |
|---|---:|
| 公开工具 | 41 |
| 隔离 profile | 12 |
| 模块导入和 MCP 注册 | 41/41 通过 |
| 仓库逐工具回归 | 41/41 通过 |
| 真实任务完全可用 | 32/41 |
| 部分模式/后端可用 | 6/41 |
| 当前不可用 | 3/41 |

这里必须区分“wrapper 能返回结构化 unavailable/error”和“软件真正完成了科学计算”。现有部分测试会把预期的 unavailable/error 视为通过，因此旧测试可以作为迁移证据，但不能直接作为新工具可用性的质量门。

### 2.2 应保留的工程能力

以下实现应抽取并继续使用：

- 12 个依赖隔离 profile；
- workspace 路径边界；
- shell=False、参数数组、超时和日志截断；
- trace、结果和 Artifact 快照；
- 一文件一测试的可追踪性；
- 软件注册表中许可证、安装方式和人工动作信息；
- 真实 smoke 与网络服务验证方法。

这些能力应迁移到 Runtime、Artifact、BackendSpec 和 conformance test 层，而不是继续绑定到旧工具名。

### 2.3 当前已知缺陷在新架构中的处理

| 当前问题 | 新架构处理 |
|---|---|
| `run_ase` 同时包含 energy/dipole/opt/vib/ir/thermo | 完全删除并拆到独立行动；ASE 仅作框架 |
| `run_ase` thermo 缺 pymatgen，部分文件可能写出 workspace | 不修补旧公共入口；在统一 Runtime/Artifact 层解决 |
| Vina 可用、GNINA 未安装 | Catalog 如实标记 Vina available、GNINA unavailable；Agent 仍显式选择，指定 GNINA 时返回 unavailable 而不自动换 Vina |
| DFTB+ 与 ABINIT 调用方式错误 | 分别修复独立 backend adapter，不保留 dispatcher |
| Phonopy displacement 缺 supercell 参数，Phono3py 参数不兼容 | 拆分位移、力常数和声子结果行动后逐项修复 |
| backend availability 只能检查当前 profile | 由统一控制面跨 worker 探测 |
| 静态 toolbox registry 状态滞后 | 声明元数据与机器健康状态分离；健康状态由 probe/smoke 生成 |
| CENSO 当前崩溃且默认依赖未安装 Turbomole | CENSO 是多步骤构象工作流，不作为原子行动后端；只抽取可证明为单一语义的底层能力 |
| CatMAP CLI 调用错误 | 改用受控 Python API 和类型化 MicrokineticModel |
| ORCA 未安装 | 作为 manual/license backend 保留，不能注册软件工具 |

### 2.4 为什么上一版方案仍然不够彻底

上一版方案已经提出拆分 `run_ase`，但仍存在四个问题：

1. 把保留 41 个旧工具和兼容 wrapper 当成实施约束，会长期维持两套概念体系。
2. `simulate_molecular_dynamics`、`prepare_simulation_system`、`calculate_thermochemistry` 等候选接口仍可能隐藏多个独立步骤。
3. 把预置 Workflow 暴露给默认 Agent，会再次出现“一个调用完成完整流程”和原子工具并存的层级混乱。
4. `expert/legacy` 中长期保留 `run_*`，会继续让软件启动器被误认为化学能力。

新版方案取消这些约束。旧实现只作为迁移时可复用的代码来源，不作为目标架构的一部分。同时，Benchmark 不引入任务相关工具检索、后端自动选择或自动回退，以免系统替代智能体完成本应被评估的规划决策。

## 3. 公共工具的统一粒度

### 3.1 一个公共工具必须同时满足的条件

每个公共工具必须满足以下全部规则：

1. 名称是“动词 + 科学对象或科学结果”，不含软件名。
2. 完成一个科学操作，而不是执行一个软件、脚本、输入文件或流程。
3. 只有一种主要输出类型；辅助日志和原始文件不改变工具语义。
4. 不使用 `driver`、`task`、`mode`、`operation` 等参数切换到另一种科学任务。
5. `backend_id` 由智能体显式指定；不同后端只能实现同一行动语义，不能改变主要输出或任务边界。
6. 输入是标准化化学对象或 Artifact，而不是软件专属文件。
7. 输出能直接成为其他原子工具的输入。
8. 能为该操作定义独立的科学正确性测试。
9. 工具不能在内部静默执行另一个具有独立科学含义的公共操作。
10. 如果一次调用包含两个可以分别验证、分别失败或被别的任务复用的科学步骤，就必须拆成两个工具。

### 3.2 判定示例

| 候选接口 | 判定 | 原因 |
|---|---|---|
| `run_ase(driver=energy/opt/vib)` | 禁止 | 通过参数切换多个不同科学任务 |
| `calculate_energy(backend_id=xtb/pyscf)` | 合格 | Agent 可选择不同软件，但结果始终是能量 |
| `simulate_molecular_dynamics` | 禁止作为单一工具 | 体系参数化、最小化、平衡、生产模拟是不同操作 |
| `propagate_dynamics` | 合格 | 输入已参数化状态，输出轨迹与最终状态 |
| `calculate_thermochemistry` 并自动优化和算频率 | 禁止 | 隐藏了优化和 Hessian/频率计算 |
| `derive_thermochemistry` | 合格 | 只从已验证频率与电子能量推导热化学量 |
| `calculate_phonons` 并自动生成位移、算力、组装 | 禁止 | 包含三个独立科学/计算步骤 |
| `generate_displaced_supercells` | 合格 | 只生成位移结构集合 |
| `assemble_force_constants` | 合格 | 只由位移-力数据组装力常数 |

### 3.3 允许的内部机械步骤

原子工具可以隐藏不值得单独评测的机械细节，例如：

- 内存中的格式转换；
- 软件输入文件渲染；
- 单位转换；
- 临时目录创建；
- 命令启动与输出解析；
- 结果 schema 序列化；
- 确定性的字段校验。

它不能隐藏具有独立科学决策的步骤，例如构象搜索、几何优化、力场参数化、频率计算、平衡模拟或需要科学判断的结果验收。字段、单位、有限值和 Artifact 完整性等确定性校验仍由每个行动自动执行。

### 3.4 原子操作不等于一次软件调用

“原子”描述的是科学语义，而不是进程数或迭代次数。几何优化、过渡态搜索、构象枚举和动力学传播可以内部进行多次能量/力评估，因为它们仍只产生一种主要结果。

判断边界的方法是：

- 内部步骤是否只是完成当前结果所必需的算法迭代；
- 中间结果是否值得被其他任务独立复用；
- 中间步骤是否需要独立参数、独立失败处理或独立科学判断。

如果后两项成立，就应拆成显式行动。

## 4. 目标架构

~~~text
Agent / Python / CLI / MCP / HTTP
                 │
                 ▼
  完整 Action / Data / Backend Catalog
    对评测智能体全量可见，不做任务裁剪
                 │
                 ▼
       智能体提交原子 ActionRequest
 action + backend_id + method/model/settings
                 │
                 ▼
        确定性校验与后端分派器
 只验证并执行精确选择，不选择、不排序、不回退
                 │
                 ▼
          后端适配器目录
 RDKit / ASE / xTB / PySCF / Psi4 / ...
                 │
                 ▼
        隔离 Runtime Provider
 Python / Process / Conda / Container / Slurm
                 │
                 ▼
      Artifact Store + Provenance
~~~

架构中故意没有默认 Workflow Tool 层，也没有替 Agent 选择候选工具或计算软件的 Router。任务分解、行动顺序、后端、方法以及失败恢复都由 Agent 完成，这正是 ResearchChemBench 希望评估的能力。

可以维护工作流示例、模板和教学 recipe，但它们只能作为维护者文档、隐藏测试 fixture 或评测器参考，不能自动注册为公共工具，也不能注入被评测 Agent 的 prompt、检索结果或工具描述。

## 5. 四类资源必须分开

### 5.1 Scientific Action

普通 Agent 可调用的原子科学操作，例如：

- `calculate_energy`
- `optimize_geometry`
- `calculate_hessian`
- `propagate_dynamics`

### 5.2 Backend

实现一个或多个行动的软件、库、模型或服务，例如：

- ASE 是结构/优化/振动算法框架和 calculator 适配生态；
- xTB、PySCF、Psi4、ORCA 是电子结构后端；
- MACE、CHGNet 是势能/力后端；
- OpenMM、GROMACS、LAMMPS 是动力学后端；
- Phonopy、Phono3py 是晶格动力学后端。

Backend 永远不直接注册成 `run_software` 式普通工具，但其完整 `BackendSpec` 必须对 Agent 可见。Agent 通过原子行动的 `backend_id` 显式选择软件；分派器不得把这个选择权收回系统内部。

### 5.3 Data Source

PubChem、RCSB PDB、Materials Project、Catalysis-Hub 独立管理。数据查询不是计算行动，通过独立的 `researchchem.data` 工具面在主 Benchmark 中全量暴露。

### 5.4 Runtime / Admin

环境探测、Artifact 查看、安装和许可证管理属于管理 API，不进入科学工具目录，也不参与 Agent 科学任务评分。为了让 Agent 能自主选择，Benchmark 启动时仍需把完整后端清单、声明能力、版本、许可证类别和当前可用状态作为只读 Catalog 快照提供给 Agent；这不是任务相关候选筛选。

## 6. 统一输入对象

公共工具不再接受任意软件 input deck。第一版建立以下标准对象：

| 对象 | 核心内容 |
|---|---|
| `ChemicalIdentity` | 名称、SMILES、InChI、InChIKey、数据库 ID |
| `AtomicStructure` | 元素、坐标、单位、电荷、多重度、晶胞、PBC |
| `ChargedStructure` | 结构、逐原子部分电荷、charge model、参数和来源 |
| `ConformerEnsemble` | 多个结构、相对能量、权重、来源 |
| `ParameterizedSystem` | 结构、拓扑、已分配参数和力场元数据；可记录是否已构建溶剂/离子环境 |
| `ElectronicState` | 方法、基组/模型、电荷、自旋及电子结果引用 |
| `FrequencyResult` | 频率、正规模式、强度、质量和温度约定 |
| `ReactionDefinition` | 反应物、产物、计量关系和条件 |
| `ReactionNetwork` | 物种、反应、速率常数和初始状态 |
| `Trajectory` | 拓扑引用、帧、时间步、单位和周期信息 |
| `DisplacementSet` | 原始晶体、超胞、位移结构和位移向量 |
| `ForceSet` | 与位移结构逐一对应的力 |
| `ForceConstants` | 二阶/三阶力常数及生成条件 |
| `DockingSystem` | receptor、ligand、搜索空间和质子化状态 |
| `ArtifactRef` | artifact id、语义类型、哈希和相对位置 |

输入对象允许从结构化 JSON、内存对象或已登记 Artifact 构造。传输层可以提供上传文件，但文件进入核心前必须解析和登记，不能把任意路径当成公共协议。

所有计算行动共享以下 Benchmark 控制字段：

- `backend_id`：必填，由 Agent 从完整 `BackendSpec` Catalog 中显式选择；不允许 `auto`；
- `method_spec`：显式记录理论方法、泛函、基组、模型、力场、charge model 等会改变科学含义的设置；
- `action_settings`：当前行动自身的收敛阈值、约束、采样长度、温压条件、搜索空间等参数；
- `resource_limits`：可选的时间、内存、CPU/GPU 上限，只约束执行资源，不改变科学任务；
- `inputs`：标准对象或 `ArtifactRef`。

不存在由系统补齐的科学性 `default_backend`。当某个行动只有一个实现时，Agent 仍需提交该 `backend_id`，以便 trace 明确证明计算软件是 Agent 的选择。只允许对日志级别、临时目录等不改变科学结果的机械参数使用系统默认值。

## 7. 统一结果外壳

所有行动使用相同结果外壳，主要 payload 由行动定义：

~~~json
{
  "status": "success",
  "action": "calculate_energy",
  "action_version": "1.0.0",
  "requested_backend": "xtb",
  "backend": "xtb",
  "backend_version": "6.x",
  "selection_source": "agent",
  "result": {
    "energy": -5.123,
    "unit": "hartree"
  },
  "input_artifacts": [],
  "output_artifacts": [],
  "warnings": [],
  "provenance": {},
  "error": null,
  "retryable": false
}
~~~

统一状态：

- `success`
- `partial_success`
- `invalid_request`
- `unsupported`
- `unavailable`
- `failed`
- `timeout`
- `cancelled`

公共结果不能只是 stdout、return code 或输出目录。

## 8. 新的公共科学行动目录

下面 40 个行动构成目标公共计算工具面。数量不是优化目标；粒度一致、边界清楚和可组合才是目标。新增行动必须通过第 3 节的粒度审查。

### 8.1 结构、构象与体系构建：9 个

| Action | 单一主要结果 | 第一版 BackendSpec（非默认） | 输入要求 |
|---|---|---|---|
| `standardize_structure` | 标准化结构 | RDKit | `ChemicalIdentity` 或 `AtomicStructure` |
| `generate_3d_structure` | 一个三维结构 | RDKit、Open Babel | 二维分子表示 |
| `generate_conformer_ensemble` | 初始构象集合 | RDKit、CREST | 标准化分子图；CREST 还要求初始 3D Artifact |
| `rank_conformers_from_results` | 带排序和权重的构象集合 | 内部确定性统计分析 | `ConformerEnsemble` + 对齐的逐构象能量/自由能结果 + 显式温度与权重规则 |
| `repair_biomolecular_structure` | 修复后的生物分子结构 | PDBFixer | 蛋白/核酸结构 |
| `assign_protonation_states` | 带显式质子化状态的结构 | RDKit、PDBFixer，后续专用后端 | 标准化结构 + pH/规则 |
| `assign_partial_charges` | `ChargedStructure` | RDKit Gasteiger、OpenFF AM1-BCC；后续其他单一语义 adapter | 已确定质子化状态的结构 + Agent 显式选择的 charge model |
| `assign_force_field_parameters` | `ParameterizedSystem` | OpenFF/OpenMM adapter，后续 GROMACS 等 | 已修复、质子化且按所选力场要求带电荷的结构 + Agent 显式选择的 force field |
| `solvate_molecular_system` | 加入显式环境后的 `ParameterizedSystem` | OpenMM/OpenFF/Packmol adapter | 已参数化体系 + Agent 显式指定的盒型、尺寸/边距、溶剂/水模型、离子和浓度 |

说明：

- `generate_3d_structure` 只生成一个结构，不自动进行量子几何优化。
- `generate_conformer_ensemble` 只负责搜索/生成；每个构象是否优化、使用哪个软件算能量/自由能、保留哪些构象，均由 Agent 通过后续原子行动决定。
- `rank_conformers_from_results` 只对 Agent 已经提供的逐构象结果做排序、简并处理和权重计算，不运行几何优化、能量、频率或溶剂计算。CENSO 的完整 refine 工作流不得作为该行动的 backend。
- PDB 修复、质子化、部分电荷、力场参数分配和溶剂/离子环境构建是显式分离的行动；任何一个行动都不得自动补跑前一步或后一步。
- `calculate_atomic_charges` 返回电子结构/布居分析结果；`assign_partial_charges` 为力场或 docking 构造带命名模型的部分电荷。两者语义不同，均不得在内部隐式调用对方。
- `assign_force_field_parameters` 不添加溶剂或离子；`solvate_molecular_system` 不进行最小化、平衡或动力学传播。
- 文件格式转换由 Artifact import/export 和后端 adapter 内部完成，不作为公共科学行动。

### 8.2 分子/非周期原子计算：10 个

| Action | 单一主要结果 | 第一版 BackendSpec（非默认） | 输入要求 |
|---|---|---|---|
| `calculate_energy` | 标量能量 | xTB、PySCF、Psi4、TBLite、MACE、CHGNet；未来 ORCA/Gaussian | `AtomicStructure` |
| `calculate_forces` | 每个原子的力 | TBLite、MACE、CHGNet；后续量化后端 | `AtomicStructure` 或同构结构批次 |
| `calculate_hessian` | Hessian 矩阵 | TBLite/EMT/MACE 等经 ASE finite difference、Psi4；后续 ORCA/Gaussian | `AtomicStructure` |
| `optimize_geometry` | 优化后的结构 | xTB、TBLite、MACE、CHGNet；ASE optimizer 仅为算法框架 | `AtomicStructure` + 约束 |
| `calculate_dipole_moment` | 偶极矩 | TBLite、PySCF、Psi4；ASE 仅为执行框架 | `AtomicStructure` + 电子方法 |
| `calculate_atomic_charges` | 原子电荷 | PySCF、Psi4；外部结果由 cclib parser 导入 | `AtomicStructure` 或标准电子态 Artifact |
| `calculate_orbitals` | 轨道能级/占据和可选系数 Artifact | PySCF、Psi4；外部结果由 cclib parser 导入 | `AtomicStructure` 或标准电子态 Artifact |
| `derive_vibrational_modes` | 频率和正规模式 | 内部数值分析/ASE vibration analysis | `Hessian` + 结构 |
| `derive_ir_spectrum` | 红外光谱 | 内部光谱构建/ASE IR 数据 | 带强度的振动结果 |
| `derive_thermochemistry` | 热化学量 | GoodVibes/内部统计热力学 | 电子能量 + `FrequencyResult` |

这里有意把 Hessian、振动模式和热化学拆开：

~~~text
optimize_geometry
→ calculate_hessian
→ derive_vibrational_modes
→ derive_ir_spectrum（仅在需要光谱时）
→ derive_thermochemistry
~~~

Agent 必须根据任务决定调用哪些步骤，不能通过一个 `run_ase(driver=thermo)` 隐藏整个链条。

### 8.3 反应与动力学：5 个

| Action | 单一主要结果 | 第一版 BackendSpec（非默认） |
|---|---|---|
| `locate_transition_state` | 一个候选过渡态结构 | pysisyphus，后续 Sella/autodE |
| `trace_intrinsic_reaction_coordinate` | IRC 路径 | pysisyphus |
| `calculate_chemical_equilibrium` | 平衡组成/状态 | Cantera |
| `integrate_reaction_network` | 浓度随时间轨迹 | SciPy、Cantera |
| `solve_microkinetic_model` | 表面覆盖度/速率稳态结果 | CatMAP |

`locate_transition_state` 不自动做 IRC；`trace_intrinsic_reaction_coordinate` 不自动寻找过渡态；过渡态验证由 Agent 读取 `derive_vibrational_modes` 结果完成。

### 8.4 动力学与轨迹：7 个

| Action | 单一主要结果 | 第一版 BackendSpec（非默认） |
|---|---|---|
| `minimize_system_energy` | 最小化后的系统状态 | OpenMM、GROMACS、LAMMPS |
| `propagate_dynamics` | 一个动力学时间段的轨迹与最终状态 | OpenMM、GROMACS、LAMMPS |
| `calculate_trajectory_rmsd` | RMSD 时间序列 | MDAnalysis |
| `calculate_radius_of_gyration` | 回转半径时间序列 | MDAnalysis |
| `calculate_radial_distribution` | RDF | MDAnalysis |
| `calculate_mean_squared_displacement` | MSD | MDAnalysis |
| `evaluate_collective_variables` | CV 时间序列 | PLUMED |

不存在 `simulate_molecular_dynamics` 或 `equilibrate_system` 大工具。平衡过程通过多次、条件不同的 `propagate_dynamics` 显式表示：

~~~text
repair_biomolecular_structure
→ assign_protonation_states
→ assign_partial_charges（所选力场需要时）
→ assign_force_field_parameters
→ solvate_molecular_system（任务需要显式溶剂时）
→ minimize_system_energy
→ propagate_dynamics（NVT 段）
→ propagate_dynamics（NPT 段）
→ propagate_dynamics（生产段）
→ 选择具体轨迹分析行动
~~~

### 8.5 周期体系与晶格动力学：8 个

| Action | 单一主要结果 | 第一版 BackendSpec（非默认） | 输入要求 |
|---|---|---|---|
| `calculate_periodic_energy` | 周期体系能量 | QE、CP2K、SIESTA、DFTB+、ABINIT；未来 VASP | 带晶胞/PBC 的 `AtomicStructure` |
| `calculate_periodic_forces` | 周期体系原子力 | QE、CP2K、SIESTA、DFTB+、ABINIT | 周期结构或同构结构批次 |
| `calculate_periodic_stress` | 应力张量 | QE、CP2K 等 | 周期结构 |
| `relax_periodic_structure` | 松弛后的晶体结构 | QE、CP2K、SIESTA、DFTB+ | 周期结构 + 原子/晶胞约束 |
| `generate_displaced_supercells` | `DisplacementSet` | Phonopy、Phono3py | 周期结构 + 超胞矩阵 |
| `assemble_force_constants` | `ForceConstants` | Phonopy、Phono3py | `DisplacementSet` + `ForceSet` |
| `calculate_phonon_dispersion` | 声子色散 | Phonopy、Phono3py | `ForceConstants` + 晶体 + q 路径 |
| `calculate_phonon_density_of_states` | 声子态密度 | Phonopy、Phono3py | `ForceConstants` + 晶体 + q 网格 |

不存在 `run_periodic_calculation` 或 `calculate_phonons` 大工具。以声子为例，Agent 应调用：

~~~text
generate_displaced_supercells
→ 对每个位移结构调用 calculate_periodic_forces
→ assemble_force_constants
→ calculate_phonon_dispersion 和/或 calculate_phonon_density_of_states
~~~

### 8.6 对接：1 个

| Action | 单一主要结果 | 第一版 BackendSpec（非默认） |
|---|---|---|
| `dock_ligand` | poses 与 scores | AutoDock Vina；后续 GNINA |

`dock_ligand` 接收已由 Agent 明确准备的 receptor、ligand/ligand ensemble、可选 `ChargedStructure` Artifact，以及 Agent 显式给出的搜索空间和 docking 参数。后端 adapter 只能完成 PDBQT 等软件必需的机械序列化与原子类型映射，不得自动修复 receptor、选择质子化状态、生成 ligand 构象、分配部分电荷或推断 docking box。上述科学选择必须由 Agent 先调用相应原子行动或直接提交明确参数。

## 9. 独立数据访问工具面：4 个

数据工具与计算工具使用相同的 schema/trace 基础，但在目录和 Agent 暴露上分开：

| Data Action | 输出 | 数据源 |
|---|---|---|
| `search_compounds` | 化合物记录 | PubChem |
| `search_protein_structures` | 蛋白结构记录 | RCSB PDB |
| `search_materials` | 材料记录 | Materials Project |
| `search_catalysis_records` | 催化反应记录 | Catalysis-Hub |

名称到 SMILES 的解析是 `search_compounds` 的一种查询，不再单独保留 `molecule_name_to_smiles`。

## 10. 明确禁止进入公共目录的接口

以下类别一律不注册为普通 Agent 科学工具：

### 10.1 软件启动器

- `run_ase`
- `run_xtb`
- `run_pyscf`
- `run_psi4`
- `run_orca`
- `run_cp2k`
- `run_quantum_espresso`
- `run_gromacs`
- `run_lammps`
- `run_openmm`
- `run_phonopy`
- `run_plumed`
- 任何未来的 `run_gaussian`、`run_vasp` 等

### 10.2 文件和结果 I/O

- `extract_output_json`
- 任意 `read_*_file`、`write_*_input`、`convert_*_file` 型内部操作

Artifact Store 和 transport 负责这些工作。

### 10.3 管理工具

- `check_backend_availability`
- `list_toolbox_capabilities`
- `validate_computation`
- 安装、启停、环境和许可证检查

这些可调用管理操作只属于 CLI/Admin API。第 19.3 节的完整只读 Catalog Resource 是例外：它对 Agent 可见，但不是科学工具，也不能按任务返回裁剪后的候选集。

### 10.4 多步骤流程工具

- `run_ase`
- `simulate_molecular_dynamics`
- `calculate_phonons`
- `conformer_thermochemistry`
- `reaction_profile`
- `transition_state_validation`
- 任何默认自动完成多个独立科学步骤的 Workflow Tool

工作流可以存在于示例文档中，但不能与原子工具一同注册。

## 11. 后端不是工具：ASE 的准确位置

ASE 在新架构中拆成三种内部角色：

1. `ASEStructureAdapter`：读写和转换 `AtomicStructure`；
2. `ASEAlgorithmAdapter`：优化器、有限差分、振动模式分析等算法；
3. `ASECalculatorBridge`：把 TBLite、EMT、MACE、ORCA 等 calculator 接到能量/力接口。

ASE 不能作为 `backend_id="ase"` 的模糊选择。Agent 请求和执行记录必须写明真正决定科学结果的计算后端，例如：

~~~json
{
  "action": "optimize_geometry",
  "backend": "tblite_gfn2_xtb",
  "execution_framework": "ase",
  "optimizer": "bfgs"
}
~~~

这样不会把执行框架与理论方法混为一谈。

## 12. Benchmark 中的后端自主选择与确定性分派

本项目当前不是生产自动化平台，而是评估 Agent 是否会自主编排化学工具的 Benchmark。因此本阶段不实现会替 Agent 搜索、过滤、排序或选择计算软件的能力 Router。

### 12.1 Agent 决策与系统职责

~~~text
完整 Action / Data / Backend Catalog 快照
→ Agent 选择下一项原子行动
→ Agent 选择 backend_id
→ Agent 选择 method / basis / model / force field / 关键设置
→ Agent 提交精确 ActionRequest
→ 系统校验 schema、后端存在性、声明支持范围和当前可用状态
→ 系统把请求原样分派给被指定的 backend
→ 执行、解析并验证本行动
→ 成功结果或结构化失败返回 Agent
→ Agent 自主决定继续、检查、改参、重试、换 backend 或改走其他行动
~~~

校验器可以拒绝不存在、不支持或当前不可用的精确组合，但不得在提交前替 Agent 缩小候选范围，也不得在拒绝后自动替换选择。Agent 始终可以查看同一份完整 Catalog，并自行作出下一次调用。

### 12.2 Benchmark 分派硬规则

1. 所有计算行动的 `backend_id` 必填，禁止 `auto`、空值和“推荐后端”占位符。
2. 会改变科学含义的 method、basis、functional、model、force field、charge model、ensemble、温压条件和搜索空间必须由 Agent 或题目显式给出，不能由系统按启发式补齐。
3. 分派器只能执行请求中的精确 backend；不得按可用性、成本、速度或精度改选软件。
4. 后端失败、超时或 unavailable 时直接返回统一错误；不得自动 fallback，哪怕另一后端语义等价。错误只解释被请求组合的失败原因，不附带系统生成的推荐或排序候选。
5. Runtime 可以把同一 backend 作业发送到匹配的本地 profile、容器或集群节点，因为这是基础设施分派；它不能把作业换成另一计算软件或理论方法。
6. Backend adapter 只负责该软件的输入渲染、执行和解析；不得借机调用其他 Scientific Action 补齐前处理或后处理。
7. 若未来需要生产环境自动路由，应另建不参与 ResearchChemBench 主评测面的 orchestration/service 层；不在本轮工具箱实现范围内。

### 12.3 选择与执行必须显式记录

每次结果必须记录：

- 本轮完整 Catalog 快照版本与哈希；
- Agent 选择的 action、backend id 和软件版本；
- Agent 或题目指定的方法、基组、泛函、模型、力场和关键设置；
- execution framework 与 runtime profile；
- 分派器是否逐字执行了请求中的 backend id；
- validator 的接受/拒绝理由；
- 若前一次调用失败，本次改参、重试或换 backend 是否来自 Agent 的新调用。

主 Benchmark 中 `selection_source` 必须为 `agent` 或 `task_constraint`，不能为 `router`。系统自动回退计数必须恒为零；任何 backend 或方法变化都必须表现为 Agent 发起的一次新工具调用。

## 13. 后端适配器协议

~~~python
class BackendAdapter(Protocol):
    spec: BackendSpec

    def probe(self) -> BackendHealth: ...
    def supports(self, request: ActionRequest) -> SupportDecision: ...
    def prepare(self, request: ActionRequest, context: ExecutionContext) -> PreparedJob: ...
    def parse(self, completed: CompletedJob, context: ExecutionContext) -> ActionPayload: ...
    def validate(self, payload: ActionPayload) -> ValidationReport: ...
~~~

适配器不得注册公共工具。新增 Gaussian 时，实现能量、力、Hessian、优化等 capability adapter 即可，公共行动名称不增加。

运行环境单独实现：

~~~python
class RuntimeProvider(Protocol):
    def submit(self, job: PreparedJob) -> JobHandle: ...
    def poll(self, handle: JobHandle) -> JobState: ...
    def cancel(self, handle: JobHandle) -> None: ...
    def collect(self, handle: JobHandle) -> CompletedJob: ...
~~~

第一版复用现有 12 个隔离 profile，把它们从“各自拥有一组 MCP 工具”改成“供统一核心调度的 worker runtime”。

## 14. Artifact 链取代路径和流程隐藏

每个行动的主要输出写入 Artifact Store，并返回 `ArtifactRef`。下一步工具只接收语义化 Artifact 或结构化对象。

示例：

~~~text
artifact:molecule-raw
  └─ standardize_structure
       → artifact:molecule-standard
           └─ generate_3d_structure
                → artifact:structure-3d
                    └─ optimize_geometry
                         → artifact:structure-optimized
                             ├─ calculate_energy
                             └─ calculate_hessian
~~~

Artifact 至少记录：

- `artifact_id`
- `semantic_type`
- `media_type`
- SHA256
- 生产 action/backend
- 输入父项
- 单位和对象 schema 版本
- 相对路径或 URI
- 创建时间

文件格式转换仍可由系统自动处理，但 Artifact 的科学类型不能因格式变化而改变。

## 15. 推荐代码结构

~~~text
chemistry_toolbox/src/researchchem_toolbox/
├── api.py
├── schemas/
│   ├── structures.py
│   ├── ensembles.py
│   ├── dynamics.py
│   ├── electronic.py
│   ├── reactions.py
│   ├── periodic.py
│   ├── artifacts.py
│   └── results.py
├── actions/
│   ├── structure/
│   ├── electronic/
│   ├── reaction/
│   ├── dynamics/
│   ├── periodic/
│   └── docking/
├── datasources/
├── backends/
│   ├── rdkit/
│   ├── ase/
│   ├── xtb/
│   ├── pyscf/
│   ├── psi4/
│   ├── orca/
│   ├── cp2k/
│   ├── quantum_espresso/
│   ├── openmm/
│   └── ...
├── dispatch/
├── runtimes/
├── artifacts/
├── provenance/
├── validation/
└── transports/
    ├── python.py
    ├── mcp.py
    ├── cli.py
    └── http.py
~~~

现有 `chemistry_toolbox/mcp` 在迁移完成后不再保存 41 个工具实现，只保留薄的 MCP binding 或整体被 `chemistry_toolbox/src/researchchem_toolbox/transports/mcp.py` 取代。

## 16. 当前 41 个工具的最终处理方式

下表是最终去向，不是长期兼容策略。`删除` 表示从公共注册、活动工具代码和 profile 工具清单中移除；可复用实现先抽到相应 adapter/service。

| 当前工具 | 操作 | 新位置或替代行动 |
|---|---|---|
| `analyze_md_trajectory` | 拆分后删除 | RMSD、回转半径、RDF、MSD 等独立轨迹行动 |
| `analyze_wavefunction` | 拆分后删除 | `calculate_atomic_charges`、`calculate_orbitals`；解析器进入后端层 |
| `calculator` | 从化学工具箱删除 | 通用数学能力，不属于化学工具箱 |
| `check_backend_availability` | 从公共工具删除 | Runtime probe；结果写入对 Agent 全量可见的 Benchmark Catalog 快照 |
| `compute_thermochemistry` | 重写后删除旧名 | `derive_thermochemistry`，只接收能量与频率结果 |
| `convert_structure` | 从公共工具删除 | Artifact import/export 与后端内部结构序列化 |
| `extract_output_json` | 删除 | Artifact Store/API |
| `find_transition_state` | 重写后删除旧名 | `locate_transition_state`，不接受任意 pysisyphus 输入文件 |
| `generate_3d_structure` | 保留名称、重写协议 | `generate_3d_structure` |
| `generate_conformers_crest` | 合并后删除 | CREST backend → `generate_conformer_ensemble` |
| `generate_conformers_rdkit` | 合并后删除 | RDKit backend → `generate_conformer_ensemble` |
| `list_toolbox_capabilities` | 删除旧实现 | 由不可按任务裁剪的只读 Action/Data/Backend Catalog Resource 取代 |
| `molecule_name_to_smiles` | 合并后删除 | `search_compounds` |
| `prepare_md_system` | 拆分后删除 | `repair_biomolecular_structure`、`assign_protonation_states`、`assign_partial_charges`、`assign_force_field_parameters`、`solvate_molecular_system` |
| `query_catalysis_hub` | 重命名重写 | `search_catalysis_records` |
| `query_materials_project` | 重命名重写 | `search_materials` |
| `query_pubchem` | 重命名重写 | `search_compounds` |
| `query_rcsb_pdb` | 重命名重写 | `search_protein_structures` |
| `refine_ensemble_censo` | 完全拆分并删除 | CENSO 的工作流编排不进入 backend；Agent 显式完成优化/能量/频率等步骤后，可调用 `rank_conformers_from_results` 做确定性汇总 |
| `run_ase` | 完全拆分并删除 | 后端/框架代码分别进入能量、力、Hessian、优化、偶极、振动、IR、热化学等 adapter |
| `run_cantera` | 拆分后删除 | `calculate_chemical_equilibrium` 或 `integrate_reaction_network` |
| `run_catmap` | 重写后删除 | `solve_microkinetic_model`；不再执行任意模型脚本 |
| `run_cp2k` | 删除公共入口 | CP2K backend → 周期能量/力/应力/松弛等行动 |
| `run_docking` | 完全拆分并删除旧名 | 复用结构修复、质子化、3D/构象和部分电荷行动；最终仅调用 `dock_ligand`，搜索空间由 Agent 显式给出 |
| `run_gromacs` | 完全拆分并删除 | GROMACS backend → 最小化和单段动力学传播行动 |
| `run_irc` | 重写后删除旧名 | `trace_intrinsic_reaction_coordinate` |
| `run_lammps` | 完全拆分并删除 | LAMMPS backend → 最小化和单段动力学传播行动 |
| `run_mlip` | 完全拆分并删除 | Agent 根据对象与目标选择分子或周期能量、力、结构优化行动，并显式指定 MACE/CHGNet backend |
| `run_openmm` | 完全拆分并删除 | OpenMM backend → 最小化和单段动力学传播行动 |
| `run_orca` | 删除公共入口 | ORCA backend → 能量/力/Hessian/优化等行动；未安装时对 Agent 可见为 unavailable，系统不自动换软件 |
| `run_periodic_calculation` | 完全删除 | 被原子周期行动与按 Agent 指定 `backend_id` 的确定性分派取代 |
| `run_phonopy` | 完全拆分并删除 | 位移超胞、力常数、声子色散、声子态密度行动 |
| `run_plumed` | 重写后删除旧名 | `evaluate_collective_variables` |
| `run_psi4` | 删除公共入口 | Psi4 backend → 能量/偶极/Hessian 等行动 |
| `run_pyscf` | 删除公共入口 | PySCF backend → 能量/偶极/电荷/轨道等行动 |
| `run_quantum_espresso` | 删除公共入口 | QE backend → 周期能量/力/应力/松弛等行动 |
| `run_reaction_kinetics` | 重写后删除旧名 | `integrate_reaction_network` |
| `run_xtb` | 删除公共入口 | xTB backend → 能量/优化/Hessian 等行动 |
| `smiles_to_coordinate_file` | 合并后删除 | `generate_3d_structure` + Artifact export |
| `standardize_molecule` | 重命名重写 | `standardize_structure` |
| `validate_computation` | 从公共工具删除 | 每个行动的内置 validator + Admin report |

处理原则：

- 不建立永久 `legacy_tools/`；
- 不把旧 `run_*` 移到另一个普通 MCP server；
- 如 benchmark 迁移需要，可在单独冻结分支、版本标签或测试 fixture 中保存旧行为；
- 主分支目标状态只保留新行动体系。

## 17. 工作流参考如何隔离

仓库可以为维护者、集成测试和隐藏评测器保留以下可能的分解示例，但它们不是工具，也不是唯一正确流程。主 Benchmark 运行时不得把这些内容提供给被评测 Agent，评测器也不能因为 Agent 采用另一条科学上有效的行动链而扣分。

### 17.1 构象热化学 recipe

~~~text
standardize_structure
→ generate_3d_structure
→ generate_conformer_ensemble
→ Agent 决定对哪些构象调用 optimize_geometry
→ Agent 为各构象选择 backend/method 并调用 calculate_energy
→ 需要自由能时再逐构象调用 calculate_hessian 与 derive_vibrational_modes
→ rank_conformers_from_results
→ 任务需要时对选定结果调用 derive_thermochemistry
~~~

### 17.2 过渡态验证 recipe

~~~text
locate_transition_state
→ calculate_hessian
→ derive_vibrational_modes
→ 检查恰有一个目标虚频
→ trace_intrinsic_reaction_coordinate
~~~

### 17.3 MD recipe

~~~text
repair_biomolecular_structure
→ assign_protonation_states
→ assign_partial_charges（所选力场需要时）
→ assign_force_field_parameters
→ solvate_molecular_system（显式溶剂任务）
→ minimize_system_energy
→ propagate_dynamics（NVT 段）
→ propagate_dynamics（NPT 段）
→ propagate_dynamics（生产段）
→ calculate_trajectory_rmsd / calculate_radius_of_gyration / 其他所需分析
~~~

### 17.4 声子 recipe

~~~text
generate_displaced_supercells
→ calculate_periodic_forces × N
→ assemble_force_constants
→ calculate_phonon_dispersion 和/或 calculate_phonon_density_of_states
~~~

这些 recipe 只用于维护者理解依赖关系、构造测试数据和检查 Artifact 契约，不用于工具检索、Agent 提示、few-shot 示例或固定答案匹配。未来如果另做面向生产用户的一键自动化产品，也应放在独立的 workflow service，不能混入 ResearchChemBench 的原子工具评测面。

## 18. Agent 暴露与评测

### 18.1 主 Benchmark 采用全量原子工具面

每个任务默认向 Agent 暴露同一份、完整且带版本哈希的能力快照：

- 第 8 节全部 40 个原子 Scientific Actions；
- 第 9 节全部 4 个 Data Actions；
- 每个行动的完整输入/输出 schema；
- 全部 BackendSpec，包括支持能力、可用状态、版本、许可证类别、方法/模型范围和资源要求；
- Artifact 类型与可连接关系。

主评测禁止 task-aware retrieval、top-k 工具召回、领域分类后裁剪、后端预过滤、推荐排序和动态隐藏。即使某个工具或 backend 对当前任务显然无关或 unavailable，也通过 Catalog 如实可见，由 Agent 自己排除。Workflow、raw runner、Admin、文件 I/O 和第 17 节 recipe 仍不暴露，因为它们不是待选择的原子科学能力或会泄露流程答案。

### 18.2 Agent 拥有的决策权

评测中的 Agent 自主决定：

- 是否先查询数据，以及调用哪个数据源；
- 使用哪些预处理、结构构建和科学计算行动；
- 行动的先后顺序、分支、循环和可并行部分；
- 每次行动使用哪个 `backend_id`；
- 方法、基组、泛函、模型、力场、charge model、约束、温压、采样长度和搜索空间等科学参数；
- 是否以及如何检查中间结果；
- 失败后重试、修改参数、更换软件、回到前一步或选择另一条行动链；
- 何时已有足够证据停止调用并形成答案。

系统只拥有机械执行权：schema 校验、精确 backend 分派、运行环境投递、格式序列化、单位统一、输出解析、确定性结果校验和 Artifact 持久化。系统不能代替 Agent 作上述科学或流程决策。

### 18.3 需要评估的能力

- 是否从完整工具集中选择了必要且合适的原子行动；
- 是否把复杂任务拆成科学上合理的步骤并自主安排顺序；
- 是否正确传递和复用 Artifact；
- 是否为每一步选择合适且受支持的计算软件与方法；
- 是否避免无意义、重复或与目标无关的调用；
- 是否读取并判断中间结果后再推进；
- 后端失败后是否由 Agent 做出合理恢复决策；
- 是否识别停止条件；
- 最终答案是否由真实工具结果和完整 provenance 支撑。

评分不能要求复现某一条隐藏 recipe；应根据任务约束、结果正确性、关键依赖是否满足、选择理由和调用效率判断，多条科学上有效的行动链都应得分。

### 18.4 Trace 必须区分

- `agent_selected_action`；
- `agent_selected_backend`；
- `agent_selected_method_spec` 与 `agent_selected_action_settings`；
- `task_constraints` 中题目明确锁定的选择；
- 系统自动完成的机械转换；
- Runtime 执行行为；
- validator 的判定；
- Agent 在失败后发起的新调用及其与失败调用的因果链接。

主 Benchmark trace 中不得出现系统生成的候选排序、`router_selected_backend` 或自动 fallback。系统不能把内部机械步骤计成 Agent 的规划成绩，也不能把 Agent 的显式软件选择归因于系统。

## 19. 元数据与插件机制

### 19.1 ActionSpec

至少包含：

- `id`、`version`、`description`；
- 唯一主要输出类型；
- 输入/输出 schema；
- required capability；
- 允许的对象类型；
- 单位约定；
- 科学参数语义、允许范围以及哪些字段必须由 Agent 显式给出；
- 与各 `backend_id` 的公开兼容契约；
- 中立的能力关键词，仅用于 Agent 阅读，不用于系统按任务召回或排序；
- conformance test 标识。

ActionSpec 校验器必须拒绝通过 `mode/driver/task` 切换主要结果的定义，也必须拒绝会静默选择 backend 或补齐科学性默认值的定义。

### 19.2 BackendSpec

至少包含：

- capability 集合；
- 支持的系统、元素、PBC、电荷和自旋；
- method/model/force-field；
- fidelity 和 cost tier；
- runtime profile；
- license class；
- availability 和真实 smoke；
- action-specific method/settings schema；
- adapter entry point。

BackendSpec 在 Benchmark 中不得包含供系统使用的推荐分数、默认优先级或 task-specific rank。描述可以客观列出能力、限制、成本和精度层级，由 Agent 自行权衡。

### 19.3 Catalog 契约

- Benchmark 开始前生成完整 Action/Data/Backend Catalog 快照并计算哈希；
- 同一评测运行内所有任务使用同一快照，不按题目改变可见范围；
- Catalog 同时呈现 available、unavailable、manual/license-required 状态，不静默删除条目；
- 每次 ActionResult 记录快照哈希，确保可以还原 Agent 当时拥有的全部选择；
- Catalog 可以通过 MCP Resource、静态上下文或等价只读接口提供，但读取它不算科学工具调用；
- 如果上下文长度成为未来问题，应单独研究公平的目录浏览机制，不能在当前主 Benchmark 中以隐藏候选集代替。

### 19.4 插件发现

建议 entry points：

- `researchchem.actions`
- `researchchem.backends`
- `researchchem.datasources`
- `researchchem.runtimes`

不提供 `researchchem.workflows` 公共工具插件组；recipe 作为文档/数据资源管理。

## 20. 测试与质量门

### 20.1 粒度一致性测试

每个 Action 必须自动检查：

- 名称不含软件名或 `run_`；
- schema 不含切换主要任务的 `driver/task/operation`；
- `mode` 只能表达同一结果的数值/算法设置，不能改变结果类型；
- 只有一个声明的 primary output type；
- 至少一个后端通过真实 smoke；
- 所有计算行动要求显式 `backend_id`，且拒绝 `auto`；
- 会改变科学含义的设置没有隐式默认值；
- 行动实现不在内部调用另一个公共 Scientific Action；
- 不接受任意软件 input deck 或 shell command。

### 20.2 后端一致性测试

同一行动的所有后端必须通过同一个 conformance suite。例如 `calculate_energy`：

- 接受相同 `AtomicStructure`；
- 返回统一能量字段和单位；
- 记录方法和收敛状态；
- 不把优化后的结构偷偷作为主要结果；
- 后端不可用时返回统一状态。

### 20.3 Benchmark 自主权回归测试

必须用可观测的测试证明选择权确实属于 Agent：

- 任意两个任务收到的 Action/Data/Backend Catalog 条目集合与哈希相同；
- 指定 backend A 的请求只会进入 backend A adapter，其他 adapter 调用次数为零；
- backend A 返回 unavailable/failed/timeout 时，不调用 backend B，结果直接返回 Agent；
- 缺少 `backend_id` 或提交 `backend_id="auto"` 时返回 `invalid_request`；
- 缺少必需的 method/force-field/charge-model/search-space 等科学设置时返回可解释错误，不静默填默认值；
- unavailable 和 manual/license backend 在 Catalog 中仍然可见；
- Agent prompt、工具描述和运行期资源中不包含第 17 节 recipe 或隐藏标准调用序列；
- trace 中 action/backend/method 选择来源为 Agent 或显式 task constraint，`automatic_fallback_count == 0`；
- 原子行动内部没有嵌套调用其他公共行动的 trace。

### 20.4 科学验证

- 能量、力、Hessian 为有限值且维度正确；
- 优化结构满足收敛阈值；
- 振动模式数与体系自由度一致；
- 过渡态虚频和 IRC 可分别验证；
- 参数化体系包含完整拓扑和参数；
- 轨迹时间、帧和拓扑一致；
- 周期结构、应力和力单位正确；
- 位移结构、力集合和力常数索引一一对应；
- docking pose 与 score 一一对应；
- Artifact 可读取、哈希稳定且父子链完整。

### 20.5 测试矩阵

1. schema/registry 测试；
2. 粒度规则测试；
3. adapter 单元测试；
4. backend conformance 测试；
5. 精确 dispatch 与 no-fallback 测试；
6. runtime/profile 测试；
7. Artifact/provenance 测试；
8. Python/MCP/CLI parity 测试；
9. 真实最小计算 smoke；
10. 全量 Catalog 暴露公平性测试；
11. Agent 多步骤组合、软件选择与失败恢复评测。

旧 41 个工具测试只用于迁移期间核对可复用实现；它们不是目标质量门，旧工具删除后应由新行动测试取代。

## 21. 实施步骤

### 阶段 0：确认目录与冻结事实基线

- 确认第 8 节的 40 个计算行动和第 9 节的 4 个数据行动；
- 保存当前真实 smoke 状态和可复用后端清单；
- 给当前版本打迁移前标签或生成归档清单；
- 明确主分支不承诺旧公共 API 兼容。
- 冻结“全量 Catalog、Agent 显式 backend、无自动路由、无自动回退、recipe 隔离”的 Benchmark 自主权契约。

验收：只冻结事实，不修改运行行为。

### 阶段 1：建立核心 schema、Action Registry 和 Artifact Store

- 创建协议无关 `researchchem_toolbox` 包；
- 实现标准对象、ActionResult、ArtifactRef；
- 实现 ActionSpec 粒度校验；
- 实现完整 Action/Data/Backend Catalog 快照与哈希；
- 实现只执行 Agent 精确选择的 validator/dispatcher，并禁止 `backend_id="auto"`；
- 实现 Artifact/trace/provenance 基础；
- 调整根 `pyproject.toml` 包发现。

验收：可注册空行动和生成全量 catalog；粒度违规、缺少显式 backend、科学设置不完整和自动 fallback 配置都会被拒绝。

### 阶段 2：抽取后端并实现第一批原子行动

优先实现最能替代 `run_ase` 和软件启动器的核心：

- `standardize_structure`
- `generate_3d_structure`
- `generate_conformer_ensemble`
- `rank_conformers_from_results`
- `calculate_energy`
- `calculate_forces`
- `calculate_hessian`
- `optimize_geometry`
- `calculate_dipole_moment`
- `calculate_atomic_charges`
- `calculate_orbitals`
- `derive_vibrational_modes`
- `derive_ir_spectrum`
- `derive_thermochemistry`

抽取 RDKit、ASE、xTB、TBLite、PySCF、Psi4、MACE、CHGNet、GoodVibes adapter，并把 cclib 限定为标准结果导入/解析器。

验收：`run_ase` 的每项有效能力都被独立行动覆盖；Agent 指定哪个 backend 就只执行哪个 backend；新行动通过真实 smoke。

### 阶段 3：删除第一批旧入口

删除公共注册和活动实现中的：

- `run_ase`
- `run_xtb`
- `run_pyscf`
- `run_psi4`
- `run_mlip`
- `compute_thermochemistry`
- 重叠的结构/构象旧工具

同步重写 profile 配置，使 profile 承载后端 worker，不再拥有这些公开工具。

验收：公共 catalog 中无 `run_ase`、无软件名工具；核心分子计算任务只使用原子行动。

### 阶段 4：重构体系构建、MD、反应、周期、声子和 docking

- 将结构修复、质子化、部分电荷、力场参数分配和溶剂/离子构建拆为独立行动；
- 将 OpenMM/GROMACS/LAMMPS 拆到最小化和单段动力学传播；平衡由 Agent 发起的多次显式传播组成；
- 将 pysisyphus 拆到 TS 与 IRC；
- 重写 CatMAP adapter；
- 将 QE/CP2K/dispatcher 拆到周期能量、力、应力、松弛；
- 将 Phonopy 拆成位移、力常数、声子色散和声子态密度；
- 删除 docking 专属 preparation 大工具；复用通用结构/质子化/3D/构象/部分电荷行动，`dock_ligand` 只执行 Agent 给定搜索空间上的 docking。

每个领域完成后立即删除相应旧入口，不等待全项目完成才清理。

### 阶段 5：数据源、传输层和全量 Agent 暴露

- 实现 4 个 Data Actions；
- 从同一 ActionSpec 生成 Python、MCP、CLI/HTTP binding；
- 向每个主 Benchmark 任务暴露相同的完整 Action/Data/Backend Catalog；
- 加入 Catalog 快照哈希、选择来源和 no-fallback trace；
- 验证没有 task-aware retrieval、候选排序、动态裁剪或 backend 自动选择；
- 默认不暴露 Admin、raw runner 和 recipe。

### 阶段 6：删除剩余旧体系并升级评测

- 删除旧 `tools/*.py`、旧 ToolSpec 和按工具归属的 profile 注册逻辑；
- 删除所有已被替代的旧测试；
- 以 action/backend conformance 测试替代；
- 更新 benchmark 任务与评分，重点评估工具分解、调用顺序、软件/方法选择、Artifact 传递、结果检查和 Agent 主导的失败恢复；
- 增加自主权回归测试，保证系统不会替 Agent 选工具、backend 或 fallback；
- 生成最终 Action/Backend/DataSource catalog。

## 22. 关键验收标准

重构完成必须同时满足：

1. 公共科学工具名中没有 `run_` 和软件名称。
2. `run_ase`、`run_periodic_calculation` 等多任务/dispatcher 入口不存在。
3. 每个公共工具只有一种主要结果类型。
4. 不存在通过 `driver/task/operation` 切换科学任务的参数。
5. 后端选择不改变行动语义。
6. 主 Benchmark 的每个任务看到同一份完整的 40 个计算行动、4 个数据行动和全部 BackendSpec，不存在任务相关检索、裁剪、排序或隐藏。
7. 每个计算调用都要求 Agent 显式指定 `backend_id`，并按需显式指定方法、基组、模型、力场和关键科学设置。
8. 系统只校验并执行 Agent 指定的 backend；不存在 Router 选软件、默认 backend 或自动 fallback。
9. backend 失败后的重试、改参、换软件和改变流程都表现为 Agent 的新调用。
10. 默认 Agent 看不到 raw input runner、Admin、文件 I/O、Workflow Tool 和隐藏 recipe。
11. 复杂任务必须通过多个行动和 Artifact 链完成。
12. CENSO 等多步骤工作流软件不能伪装成单个原子行动 backend。
13. 力场参数化不隐藏修复、质子化、部分电荷或溶剂构建；docking 不隐藏 receptor/ligand 准备和搜索空间选择。
14. 新增 Gaussian、VASP 或新 MLIP 时不新增公共软件工具，但其 BackendSpec 和支持行动对 Agent 全量可见。
15. 每个可用 backend/action 组合都经过真实 smoke 和统一 conformance test。
16. 12 个隔离环境的价值被保留，但它们成为运行时，不再决定公共工具分组。
17. workspace、无 shell 注入、超时、许可证和模型下载边界不退化。
18. 主分支不再携带未使用的永久 legacy 工具面。

## 23. 需要确认的决策

按当前目标，建议确认以下默认决策：

1. 接受破坏性 API 重构，不以兼容现有 41 个工具为目标。
2. 公共面采用第 8 节 40 个原子计算行动，第 9 节 4 个独立数据行动。
3. 完全删除 `run_ase`，不在 legacy/expert MCP 中保留。
4. 所有软件专属 `run_*` 从公共工具箱删除。
5. 不把预置工作流注册成工具，也不向被评测 Agent 提供 recipe；由 Agent 自行组合。
6. 主 Benchmark 全量暴露所有 Action、Data Action 和 BackendSpec，不做任务相关候选范围决定。
7. 每个计算行动由 Agent 显式选择 `backend_id` 和关键科学设置；系统没有默认 backend。
8. 不实现 backend 自动选择、候选排序或自动 fallback；失败恢复由 Agent 新调用完成。
9. CENSO 不作为 `rank_conformers_from_results` 的 backend；排名行动只汇总预计算结果。
10. MD 体系构建拆分为修复、质子化、部分电荷、力场参数分配和溶剂/离子构建。
11. docking 不保留两个 preparation 大工具；通用前处理由 Agent 显式调用，搜索空间由 Agent 指定。
12. 保留现有多 profile 环境，但改造成后端 worker runtime。
13. 使用 ArtifactRef 显式连接步骤。
14. 每完成一组新行动就删除对应旧入口，而不是长期双轨运行。
15. 商业软件仅作为用户提供安装的 backend，不新增软件工具，但状态仍在完整 Catalog 中可见。
16. 本文档确认后，从阶段 0—2 开始实施，并在第一批新行动通过后删除 `run_ase` 相关旧入口。

## 24. 本文档确认后的第一批代码工作

确认后建议一次完成以下闭环，而不是只创建空架构：

1. 固化迁移前状态；
2. 创建核心 schema、Action Registry、Artifact Store 和完整 Catalog 快照；
3. 抽取 RDKit/ASE/xTB/TBLite/PySCF/Psi4/MACE/CHGNet adapter；
4. 实现第一批分子结构、能量、力、Hessian、优化、偶极、振动和热化学行动；
5. 增加 conformance/live smoke、精确 dispatch、全量暴露和 no-fallback 测试；
6. 修改 MCP binding 和 profile runtime；
7. 删除 `run_ase` 及已被完全替代的分子计算旧入口；
8. 返回代码差异、工具目录、后端矩阵和测试结果供审阅。

在用户确认前，不执行上述代码修改。

## 25. 参考基线

- 当前工具目录：[TOOL_CATALOG.md](../mcp/TOOL_CATALOG.md)
- 当前工具元数据：[models.py](../mcp/models.py)
- 当前 profile 配置：[mcp_profiles.yaml](../config/mcp_profiles.yaml)
- 当前软件注册表：[toolbox_registry.yaml](../config/toolbox_registry.yaml)
- Biomni 论文：https://biomni.stanford.edu/paper.pdf
- Biomni 代码：https://github.com/snap-stanford/Biomni
