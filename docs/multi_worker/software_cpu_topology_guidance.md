# 化学工具箱软件的物理核与逻辑线程使用建议

## 1. 当前统一策略

当前分布式计算池不按软件分别配置 CPU 拓扑。worker inventory 更新程序自动读取
CPU affinity 和 `/sys/devices/system/cpu/*/topology`：

- 未检测到 SMT 时，配置的 `available_cpu_cores` 原值直接作为可调度物理核数；
- 检测到 SMT 时，将配置值除以可见的每核线程数；
- 每个可调度物理核只选择一个 logical CPU ID；
- SMT sibling 不进入科学计算池；
- Agent 看到的 `cpu_cores`、总池容量和单作业上限均表示物理核。

当前 SSH worker 的实测拓扑为 80 logical threads / 40 physical cores，配置值仍为
64，因此每个 worker 向 Agent 暴露 32 physical cores，四个 worker 共 128 cores。

这一策略优先保证 MPI/OpenMP 科学计算的稳定性、可重复性能和清晰资源语义。软件并不
“必须使用逻辑核”；逻辑线程只是 SMT 提供的额外执行上下文，适合部分轻量或等待型
负载。下表供未来确实需要按软件区分时参考。

## 2. 分类含义

| 分类 | 含义 | 当前建议 |
|---|---|---|
| 物理核优先 | MPI、OpenMP、BLAS、积分、FFT、网格或长时间数值计算 | 一进程/线程对应一个物理核，不使用 SMT sibling |
| 单核/吞吐型 | 解析、格式转换、图操作或短小独立任务 | 当前仍按物理核；未来可通过基准测试后允许 SMT |
| GPU 优先 | 主要计算在 GPU，CPU 用于数据准备和驱动 | GPU 作业分配少量物理核；CPU-only 模式仍按物理核 |
| 后端依赖 | 本身是编排器或优化器，主要资源需求由其调用的后端决定 | 继承实际电子结构、动力学或分析后端的策略 |
| 网络/数据服务 | 主要等待远程 API 或数据库 | 协调节点或少量 CPU 即可，不应占用大计算配额 |

## 3. 已注册 Backend 全表

### 3.1 数据处理、结构处理与轻量分析

| Backend | 主要类型 | SMT/CPU 建议 | 说明 |
|---|---|---|---|
| `qcelemental` | 单核/吞吐型 | 1 核；逻辑线程通常可接受 | 单位、分子模型和结果数据处理 |
| `cclib` | 单核/吞吐型 | 1 核；逻辑线程通常可接受 | 量化输出解析，常受文件 I/O 限制 |
| `rdkit` | 单核/吞吐型 | 独立任务并行；默认物理核 | 图、描述符、子结构等操作通常单线程 |
| `openbabel` | 单核/吞吐型 | 1 核；批量任务可并行 | 文件转换和基础结构处理 |
| `rdkit_etkdg` | 单核/吞吐型 | 多个 seed/process 分配不同物理核 | 单任务可较轻，适合任务级并行 |
| `internal_statistics` | 单核/吞吐型 | 1 核；大型 NumPy 运算按物理核 | 确定性统计分析 |
| `internal_reaction_analysis` | 单核/吞吐型 | 1 核 | 反应和配位结构分析 |
| `pdbfixer` | 单核/吞吐型 | 1 核 | PDB 修复和准备 |
| `pdb_tools` | 单核/吞吐型 | 1 核 | 文本型 PDB 操作 |
| `rdkit_gasteiger` | 单核/吞吐型 | 1 核；分子级并行 | Gasteiger 电荷 |
| `openff_am1bcc` | 单核/后端依赖 | 每个 `sqm` 作业优先一个物理核 | AM1-BCC 的量化步骤比普通格式处理更重 |
| `openff` | 单核/吞吐型 | 1 核 | 参数化和 Interchange 数据构建 |
| `openmm_builder` | 单核/吞吐型 | 1–2 核 | 系统构建，不是 MD 主计算 |
| `packmol` | 物理核优先 | 通常 1 个物理核 | 结构打包主要为单进程数值优化 |
| `spglib` | 单核/吞吐型 | 1 核 | 空间群和对称性分析 |
| `pymatgen` | 单核/吞吐型 | 1 核；批量结构可任务并行 | 材料结构和数据处理 |
| `ase_emt` | 单核/吞吐型 | 1 核；多结构任务级并行 | 轻量经验势 |
| `internal_vibrations` | 单核/吞吐型 | 1 核；大型矩阵用物理核 | Hessian 后处理和振动分析 |
| `internal_spectroscopy` | 单核/吞吐型 | 1 核 | 光谱展宽和数据生成 |
| `internal_thermochemistry` | 单核/吞吐型 | 1 核 | 统计热力学后处理 |
| `goodvibes` | 单核/吞吐型 | 1 核；多个文件集合可并行 | 解析频率输出并计算热化学 |
| `mdanalysis` | 单核/吞吐型 | 1–数个物理核 | 大轨迹可能受内存和 I/O 限制 |
| `mdtraj` | 单核/吞吐型 | 1–数个物理核 | 轨迹分析，部分操作可多线程 |
| `pymbar` | 物理核优先 | NumPy/BLAS 计算按物理核 | 大样本自由能统计可能为矩阵密集型 |
| `alchemlyb` | 单核/后端依赖 | 轻量整理 1 核；估计器继承 PyMBAR 策略 | 自由能数据整理与分析 |

### 3.2 分子电子结构、量子化学与量子后处理

| Backend | 主要类型 | SMT/CPU 建议 | 说明 |
|---|---|---|---|
| `crest` | 物理核优先 | OpenMP 线程对应不同物理核 | CREST 调用 xTB，适合构象或分子级并行 |
| `xtb` | 物理核优先 | OpenMP 线程对应不同物理核 | SMT 通常不能提供等比例加速 |
| `pyscf` | 物理核优先 | BLAS/OpenMP 使用物理核 | 常受矩阵运算和内存带宽限制 |
| `gpaw` | 物理核/GPU 优先 | CPU 模式按物理核；GPU 模式减少 CPU | 网格 DFT，可使用 MPI 和加速器 |
| `lobster` | 物理核优先 | 每个并行进程对应物理核 | 投影和键合分析可能占用大量内存 |
| `nwchem` | 物理核优先 | MPI rank/OpenMP thread 对应物理核 | 不默认把 SMT sibling 计作 MPI slot |
| `openmolcas` | 物理核优先 | MPI/OpenMP 对应物理核 | 多参考电子结构计算 |
| `multiwfn` | 物理核优先 | 重网格分析使用物理核 | 小型后处理可单核，大网格分析较重 |
| `critic2` | 物理核优先 | OpenMP/网格任务使用物理核 | 实空间拓扑分析 |
| `psi4` | 物理核优先 | OpenMP/BLAS 使用物理核 | 电子结构和积分计算 |
| `tblite` | 物理核优先 | OpenMP 使用物理核 | 半经验电子结构 |
| `orca` | 物理核优先 | 一个 MPI rank 对应一个物理核 | `%pal nprocs` 不应超过分配的物理核数 |
| `gaussian` | 物理核优先 | `%NProcShared` 按物理核 | SMT 通常收益很小，且会增加性能波动 |
| `gamess` | 物理核优先 | MPI/DDI 进程按物理核 | 避免 sibling 上放置多个重计算进程 |

### 3.3 机器学习势与可微分模型

| Backend | 主要类型 | SMT/CPU 建议 | 说明 |
|---|---|---|---|
| `mace` | GPU 优先 | GPU 推理配少量物理核；CPU 模式按物理核 | 批量大小和模型决定 CPU/GPU 比例 |
| `chgnet` | GPU 优先 | GPU 配少量物理核；CPU 模式按物理核 | 神经网络势推理和优化 |
| `deepmd` | GPU/物理核优先 | GPU 优先；CPU/MPI 模式按物理核 | DeePMD 推理和训练 |
| `nequip` | GPU 优先 | GPU 配少量物理核；CPU 模式按物理核 | 等变神经网络训练和推理 |
| `allegro` | GPU 优先 | GPU 配少量物理核；CPU 模式按物理核 | 与 NequIP 类似 |

### 3.4 优化、反应、动力学和统计计算

| Backend | 主要类型 | SMT/CPU 建议 | 说明 |
|---|---|---|---|
| `geometric` | 后端依赖 | 优化器本身轻量，继承 NWChem/量化后端资源 | 几何优化编排器 |
| `sella` | 后端依赖 | 优化器本身轻量，力和 Hessian 后端按物理核 | 极小值和鞍点优化 |
| `pysisyphus` | 后端依赖 | 编排部分 1 核，电子结构后端按物理核 | 反应路径和几何优化 |
| `cantera` | 物理核优先 | 大机理/批量积分按物理核 | 小型零维模型可单核 |
| `scipy` | 物理核优先 | BLAS/数值优化按物理核 | 单个轻量分析可只用 1 核 |
| `rmg` | 物理核优先 | 独立物种/反应任务级并行 | 机理生成含 Python 编排和量化估算 |
| `mess` | 物理核优先 | 每个主方程计算使用独立物理核 | 多个温压条件可任务并行 |
| `mesmer` | 物理核优先 | 数值求解使用物理核 | 主方程和动力学分析 |
| `catmap` | 单核/物理核 | 单模型通常 1 核；参数扫描任务级并行 | 微观动力学与描述符扫描 |

### 3.5 分子动力学与自由能

| Backend | 主要类型 | SMT/CPU 建议 | 说明 |
|---|---|---|---|
| `openmm` | GPU 优先 | GPU 配少量物理核；CPU platform 按物理核 | GPU 通常是主要计算资源 |
| `gromacs` | GPU/物理核优先 | MPI/OpenMP 按物理核，GPU 模式调低 CPU | 需要针对体系调优 rank/thread |
| `lammps` | GPU/物理核优先 | MPI/OpenMP 按物理核 | 加速包存在时可使用 GPU |
| `hoomd` | GPU 优先 | GPU 配少量物理核；CPU 模式按物理核 | 粒子模拟通常以 GPU 为主 |
| `namd` | GPU/物理核优先 | CPU worker/PE 按物理核 | NAMD 3 可使用 GPU resident 模式 |
| `amber_pmemd` | GPU/物理核优先 | `pmemd.MPI` 按物理核；GPU 版配少量 CPU | 不应把 SMT sibling 当作独立 MPI 核 |
| `charmm` | 物理核优先 | MPI/OpenMP 按物理核 | CPU 密集型分子模拟 |
| `plumed` | 后端依赖 | 继承 GROMACS/LAMMPS/OpenMM 的资源策略 | 增强采样插件本身不独立决定 CPU 拓扑 |

### 3.6 周期体系、声子和热输运

| Backend | 主要类型 | SMT/CPU 建议 | 说明 |
|---|---|---|---|
| `quantum_espresso` | 物理核优先 | MPI/OpenMP rank/thread 按物理核 | FFT、对角化和通信密集 |
| `cp2k` | 物理核优先 | MPI/OpenMP 混合并行按物理核 | 需要同时考虑内存和 NUMA |
| `siesta` | 物理核优先 | MPI rank 按物理核 | 周期 DFT |
| `dftbplus` | 物理核优先 | OpenMP/MPI 按物理核 | DFTB 计算 |
| `abinit` | 物理核优先 | MPI/OpenMP 按物理核 | 平面波 DFT |
| `vasp` | 物理核优先 | MPI/OpenMP 按物理核 | 需要结合 `NCORE`、`KPAR` 等调优 |
| `phonopy` | 单核/物理核 | 后处理 1 核；力计算继承量化后端 | 多位移力计算适合任务级并行 |
| `phono3py` | 物理核优先 | 大矩阵和多位移任务按物理核 | 三阶力常数和热输运前处理 |
| `shengbte` | 物理核优先 | MPI/OpenMP 按物理核 | 热导率求解 |

### 3.7 对接与外部数据服务

| Backend | 主要类型 | SMT/CPU 建议 | 说明 |
|---|---|---|---|
| `vina` | 物理核优先 | 搜索线程按物理核 | 多配体更适合任务级并行 |
| `gnina` | GPU 优先 | GPU 配少量物理核；CPU 模式按物理核 | CNN scoring 主要受 GPU 影响 |
| `pubchem` | 网络/数据服务 | 1 核 | 主要等待 HTTP API |
| `rcsb_pdb` | 网络/数据服务 | 1 核 | 主要等待远程数据服务 |
| `materials_project` | 网络/数据服务 | 1 核 | 主要等待 API |
| `catalysis_hub` | 网络/数据服务 | 1 核 | 主要等待 GraphQL 服务 |
| `nist_webbook` | 网络/数据服务 | 1 核 | 主要等待远程数据和解析 |

## 4. 未来若按软件配置时的最小规则

只有在真实基准测试证明 SMT 可以提高总吞吐量时，才建议增加按软件配置。最小配置可只
保留三类，不需要为 77 个 Backend 分别写调度代码：

```yaml
cpu_profile:
  physical:      # 默认：量化、MD、周期、数值计算
  throughput:    # 可选：解析、格式转换、轻量独立任务
  accelerator:   # GPU 为主，CPU 仅作驱动
```

当前实现统一采用 `physical`，因此不存在 ORCA 等软件专用分支，也不会随着软件数量增加
而扩大调度器复杂度。
