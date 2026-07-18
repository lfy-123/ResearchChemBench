# ResearchChem 化学工具箱重构实施报告

> 完成日期：2026-07-18  
> 目标：评估智能体自主选择、编排并调用多个化学工具完成科学任务的能力

## 1. 结论

本轮重构已经完成核心实现。公共工具面不再包含 `run_ase`、`run_xtb`、`run_cp2k`、`run_openmm` 等软件启动器，也没有预置的一键流程工具。现在统一公开：

- 40 个单一科学语义的 Scientific Actions；
- 4 个独立 Data Actions；
- 45 个可由智能体显式选择的 BackendSpecs；
- 一个对所有任务完全相同的 MCP 工具目录；
- 统一的 ActionRequest、ActionResult、ArtifactRef 和 provenance 协议。

智能体决定工具、调用顺序、分支、重复调用、软件、方法、关键参数、失败恢复和停止条件。系统只做确定性校验并执行精确选择，不做任务相关工具裁剪、候选排序、自动后端选择或自动回退。

## 2. Git 基线

重构前目录没有 Git 仓库。本轮先初始化 Git，并保存了完整旧实现：

- 基线 commit：`a3fcb45`
- 基线 tag：`pre-chemistry-toolbox-refactor-20260718`

因此，被删除的旧工具和测试仍可从该 tag 完整恢复和比较。

## 3. 已实施的架构

核心代码位于 `researchchem_toolbox/`：

- `models.py`：统一 ActionRequest、ActionResult、ArtifactRef 与规格模型；
- `specs.py`：44 个公共 Actions 和 45 个 BackendSpecs 的唯一事实源；
- `catalog.py`：完整目录、目录哈希、系统提示词摘要和 MCP 描述；
- `service.py`：显式后端校验、一次精确分派、结果封装；
- `runtime.py`：跨隔离环境探测和 worker 执行；
- `artifacts.py`：语义 Artifact、SHA-256、父子关系与 workspace 边界；
- `backends/`：结构、电子结构、反应、动力学、周期/声子、docking 和数据源适配器。

每次 Scientific Action 都要求 `backend_id`。`backend_id="auto"` 会被拒绝；后端失败后不会静默切换软件，provenance 中固定记录 `automatic_fallback_count: 0`。

## 4. 与 Benchmark 目标的配合

系统提示词现在先按七类汇总工具，再简要介绍每个 Action 及其可用后端状态：

1. 结构、构象与体系构建；
2. 分子电子结构与派生性质；
3. 反应路径、平衡与动力学；
4. 分子动力学与轨迹分析；
5. 周期电子结构与晶格动力学；
6. 分子 docking；
7. 外部化学数据源。

所有任务都得到同一份完整目录快照 `_toolbox_catalog.json`。提示词明确要求智能体自行规划，不注入 recipe、标准流程、任务相关工具子集或后端推荐。每个 MCP 工具描述列出输入语义、主输出、允许后端和后端所需字段。

## 5. 旧接口处理

- 删除了旧 `evaluation/mcp_tools/tools/` 下 41 个公共工具实现；
- 删除了对应的旧逐工具 wrapper 测试；
- 不提供 legacy `run_*` 公共兼容层，避免两套层级继续共存；
- profile 从“工具分组”改为“后端依赖运行时”；
- `--mcp-tools` 不再允许裁剪目录，评测入口始终暴露全部 44 个 Actions；
- 静态旧软件表改为由 BackendSpecs 动态生成的目录。

## 6. 最终真实验证

下载资源接入完成后，本轮最终验证结果为：

- 全量 Python 回归：`47 passed`；
- MCP 注册：44/44 工具，原子调用、Artifact 与 trace 重放成功；
- 运行环境：14/14 个 profile/support runtime 通过模块、命令、外部命令、`pip check` 和模型加载检查；
- BackendSpec：45/45 available，不再保留允许缺失项；
- 注册资源：9/9 通过归档/源码包/可执行文件校验、文件数和覆盖检查；两套 SSSP 共 206 个 UPF 文件逐文件 MD5 通过；
- 下载资源真实计算：18/18 通过，覆盖 QE/SIESTA/ABINIT/DFTB+ 的能量、力、应力或弛豫、GNINA CPU/CNN docking，以及 ORCA 的 PAL2 能量、Hessian、几何优化和偶极矩；
- 在线 Data Actions：PubChem、RCSB PDB、Materials Project、Catalysis-Hub 4/4 实时请求成功；
- OpenFF AM1-BCC、OpenFF Interchange、Packmol 和既有核心 smoke 全部成功。

过程中依据真实输出修复了 QE “Total force”误匹配、ABINIT 10 输出文件/力/应力单位解析、DFTB+ Parser 14 几何优化输入、GNINA 不支持 Vina `--energy_range`、ORCA 优化误读 `job_trj.xyz` 第一帧，以及 Materials Project/Catalysis-Hub 的有界在线请求问题。

简要状态见 [TOOLBOX_STATUS.md](../TOOLBOX_STATUS.md)。逐个 Action、Backend、runtime、资源、元素覆盖、SSSP cutoff 与 smoke 证据见 [CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md](CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md)。

## 7. 软件、模型与科学数据管理

- Conda/Pip 隔离环境继续位于 `.tool_envs/`；OpenFF 保持独立 Python 3.12 runtime；
- 手工下载或独立构建的大型软件统一放入 `.software_cache/`；GNINA 1.3.3、ORCA 6.1.1 和 ORCA 专用 OpenMPI 4.1.8 均使用版本化目录，runtime 只保留稳定链接或显式路径；
- 模型缓存位于 `.model_cache/`；模型名称/路径、device 和下载许可仍由 Agent 显式决定；
- 赝势与参数数据保留在被 Git 忽略的 `download/`，由 `config/toolbox_resources.json` 注册成只读 ResourceRef；
- `.tool_envs/abinit` 已补齐 NumPy、Pydantic、PyYAML 和 python-dotenv，使真实 worker 与健康探测均可启动；
- 当前需补装的 Conda/Pip 包为零。

Agent 可显式选择的科学数据包括：

- `qe_sssp_1_3_pbe_efficiency` 与 `qe_sssp_1_3_pbe_precision`；
- `siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml`；
- `abinit_pseudo_dojo_nc_sr_pbe_standard_psp8`；
- `dftb_3ob_3_1` 与 `dftb_matsci_0_3`。

元素文件使用 `resource://<resource_id>/<Element>`，参数集使用 `resource://<resource_id>`。系统不按元素、精度或任务自动选择资源，也不会把一个参数族替换为另一个参数族。

## 8. ORCA 6.1.1 完成项

用户提供的 `orca_6_1_1_linux_x86-64_shared_openmpi418_avx2.run` 已校验并安装到 `.software_cache/orca/6.1.1/`。匹配的 OpenMPI 4.1.8 从官方源码校验构建到 `.software_cache/openmpi/4.1.8/`，没有使用 Conda 中较旧的近似版本。

`quantum` runtime 通过完整路径设置 `CHEMGRAPH_ORCA_COMMAND`，并只向 `quantum`/`reaction` 注入 ORCA、OpenMPI 的 `PATH`/`LD_LIBRARY_PATH`。`.tool_envs/quantum/bin/orca` 与 `mpirun` 是稳定入口。Agent 仍需显式选择 `backend_id=orca`、方法、基组、Action 参数与 CPU 数；当 `resource_limits.cpu_cores>1` 时，适配器只做机械映射，生成相同数目的 `%pal nprocs`，不会替 Agent 选择方法或软件。

真实验证结果：energy（PAL2）、9×9 Hessian、收敛几何优化和 dipole 四条 Action 均为 `success`，并返回 `backend_version=6.1.1`。失败时仍不会自动改用 Psi4、PySCF、xTB 或其他后端。

## 9. 最终验收结论

当前 44 个公共工具、45 个 BackendSpecs、14 个运行环境、9 个注册资源和 4 个在线数据源均已完成配置审计。工具箱继续满足：公共工具同粒度、无笼统 runner、全目录可见、Agent 显式选择工具/软件/方法/资源、无自动回退、结果可组合、执行可追踪。
