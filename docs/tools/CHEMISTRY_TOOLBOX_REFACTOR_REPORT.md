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

## 6. 已完成的真实验证

本轮已验证：

- 全量 Python 回归：`36 passed`；
- MCP 注册：44/44 工具；
- MCP 原子链：结构标准化、3D 生成、能量计算、构象结果排序、Artifact 和 trace；
- wheel 构建：根包与独立 MCP 包均成功；
- 实际计算 smoke：RDKit、Open Babel、ASE/EMT、xTB、PySCF、Psi4、TBLite、Cantera、SciPy、PDBFixer、OpenMM、MDAnalysis、Phonopy、Phono3py、Vina、CP2K；
- CP2K PBE 周期能量计算成功返回 `-3.714233601738498 hartree`；
- Phono3py 二阶/三阶位移生成和力常数组装均通过当前安装版本验证；
- 结构检查、运行时覆盖、handler 覆盖和旧公共工具移除检查全部通过。

状态报告见 [TOOLBOX_STATUS.md](../TOOLBOX_STATUS.md)，完整 Action/Backend 目录见 [TOOL_CATALOG.md](../../evaluation/mcp_tools/TOOL_CATALOG.md)。

## 7. 需要用户准备的软件与数据

当前缺少的 Conda 软件包：

- `openff-toolkit`
- `openff-interchange`
- `packmol`

需要人工下载或许可的软件：

- ORCA：从官方入口下载，并配置 `CHEMGRAPH_ORCA_COMMAND`；
- GNINA：下载发布版二进制，并配置 `CHEMGRAPH_GNINA_COMMAND`。

周期软件还需要实际科学数据，而不只是程序本身：

- Quantum ESPRESSO：覆盖任务元素的 UPF 赝势，例如 SSSP/PseudoDojo；
- SIESTA：对应元素的 PSF/兼容赝势；
- DFTB+：覆盖全部元素对的 Slater–Koster 参数集，例如 3ob/matsci；
- ABINIT：对应元素的 ABINIT 兼容赝势。

Materials Project 在新环境中还需要 `MP_API_KEY`。这些资源都应作为 workspace Artifact 显式传给 Action，系统不会替智能体暗中选择赝势或参数集。

## 8. 安装后的下一阶段调试

按用户要求，本轮不继续猜测尚未安装软件的具体版本行为。相关 BackendSpec、输入渲染、命令隔离、结果协议和 unavailable 处理已经建立；软件/数据就绪后需要执行真实 conformance：

1. 固定实际版本与可执行文件路径；
2. 用最小可靠体系完成能量/力/优化或 docking smoke；
3. 对照原始输出校准解析器和单位；
4. 将通过结果写入 BackendSpec 状态和回归测试；
5. 对 ORCA、GNINA、OpenFF、Packmol 及带外部赝势/参数集的周期计算逐项验收。

在这些后端完成真实 smoke 前，目录仍会完整展示它们，但健康状态为 unavailable，或在缺少必需 Artifact 时返回结构化错误；系统不会替换成其他软件。

## 9. 最终验收标准

本轮已经满足工具箱层面的关键目标：公共工具同粒度、无笼统软件 runner、全目录可见、Agent 显式选择、无自动回退、结果可组合、执行可追踪。后续工作的边界是“补齐外部软件并做版本级真实调试”，而不是再次改变公共工具架构。
