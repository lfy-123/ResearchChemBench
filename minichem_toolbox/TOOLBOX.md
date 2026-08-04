# MiniChem Toolbox 结构与能力说明

本文档说明 MiniChem Toolbox 的设计边界、三层执行接口、预定义 Action、后端软件、
Action 检索方式和任务产物管理方式。环境复现及 Codex、Claude Code、OpenCode 的接入
命令见 [README.md](README.md)。

## 1. 工具箱定位

MiniChem 面向 ARCHE Case1 一类分子反应机理、选择性解释和小分子量子化学任务。核心
计算软件是 Gaussian，同时保留 xTB、CREST、pysisyphus、Sella、GoodVibes、Multiwfn、
RDKit、Open Babel 和 cclib 等准备、预筛选、路径搜索及结果分析能力。

它不以覆盖全部计算化学方向为目标。目前有意不包含周期性材料计算、分子动力学、蛋白
对接、大规模高通量材料筛选和远程化学数据库检索。这样可以缩小 Agent 的工具选择空间，
并让工具能力与 Case1 类评估任务保持一致。

## 2. 总体架构

```text
Agent（Codex / Claude Code / OpenCode）
                 |
                 | MCP（stdio 或 streamable HTTP）
                 v
┌─────────────────────────────────────────────────────┐
│ MiniChem MCP Server                                 │
│                                                     │
│  第一层：预定义 Scientific Actions                  │
│  第二层：原生软件调用                                │
│  第三层：Agent 自编 Python 分析程序                  │
└─────────────────────────────────────────────────────┘
                 |
                 v
        隔离工作区、作业记录和科学产物
```

三个执行层是并列能力，不是必须依次执行。Agent 应根据任务选择最简单且足够准确的一层：

- 常见且输入输出契约明确的操作，优先使用预定义 Action；
- Gaussian 自定义 route、过渡态、IRC 等 Action 未完整覆盖的计算，使用原生软件层；
- 数据整理、统计、绘图和组合分析，使用可编程 Python 层。

所有层共享统一的工作区、资源限制、作业状态和产物登记机制。工具箱不会自动替 Agent
选择计算方法，也不会在后端失败时偷偷换软件、方法或精度。

## 3. 目录与运行时组织

```text
minichem_toolbox/
├── .envs/                    # 专用 Conda 环境及可迁移 runtime pack
├── .mini_software_cache/     # Gaussian、Multiwfn 等非 Conda 软件
├── .mini_model_cache/        # 可选语义检索模型
├── config/                   # runtime、软件、MCP 和资源配置
├── mcp_tools/                # MCP server、三层工具与作业管理
├── native_software_docs/     # Agent 可检索的原生软件文档
├── scripts/                  # 环境安装、启动、验证、打包脚本
├── src/minichem_toolbox/     # Action catalog、backend 和执行逻辑
└── tests/harnesses/          # 三种 Agent CLI 的隔离测试入口
```

物理上只有一个 Conda 环境：

```text
.envs/minichem/
```

配置中的 `core`、`quantum`、`reaction`、`gaussian`、`goodvibes`、`multiwfn` 等是逻辑
runtime 标签。它们用于声明模块、命令、环境变量和 backend 归属，但都指向同一个物理
环境，不会重复安装依赖。

## 4. 第一层：预定义 Scientific Actions

Action 是具有固定输入、输出、参数约束和 provenance 的科学操作。渐进式 MCP 模式不会
一次向 Agent 暴露 37 个独立工具，而是通过检索工具找到 Action，再由统一的
`execute_action` 执行。

### 4.1 科学数据交换与结果解析

| Action | Backend | 目标 |
|---|---|---|
| `normalize_qcschema_molecule` | `qcelemental` | 将分子结构校验并标准化为 QCSchema Molecule。 |
| `validate_qcschema_record` | `qcelemental` | 校验明确类型的 QCSchema/QCArchive 记录。 |
| `parse_quantum_chemistry_output` | `cclib` | 解析已有量子化学输出，不重复运行计算。 |

### 4.2 结构、体系与构象

| Action | Backend | 目标 |
|---|---|---|
| `standardize_structure` | `rdkit` | 标准化分子表示，不生成三维结构。 |
| `generate_3d_structure` | `rdkit`, `openbabel` | 从二维表示生成一个三维初始结构。 |
| `generate_conformer_ensemble` | `rdkit_etkdg`, `crest` | 生成有界的构象集合。 |
| `cluster_conformers` | `rdkit` | 按显式 RMSD 阈值对已有构象聚类。 |
| `align_molecular_structures` | `rdkit` | 按显式原子映射刚性对齐两个结构。 |
| `rank_conformers_from_results` | `internal_statistics` | 根据 Agent 已提供的能量或自由能排序和计算权重。 |
| `enumerate_coordination_isomers` | `internal_reaction_analysis` | 对显式配位几何枚举对称不等价配位异构体。 |
| `assign_protonation_states` | `rdkit` | 按显式 pH 或规则分配质子化状态。 |
| `assign_partial_charges` | `rdkit_gasteiger` | 生成 Gasteiger 部分电荷。 |

### 4.3 化学信息学

| Action | Backend | 目标 |
|---|---|---|
| `search_local_substructures` | `rdkit` | 使用显式 SMARTS/SMILES 搜索局部子结构。 |
| `enumerate_tautomers` | `rdkit` | 在数量上限内枚举互变异构体。 |
| `enumerate_stereoisomers` | `rdkit` | 按显式规则枚举立体异构体。 |

### 4.4 电子结构、振动与热化学

| Action | Backend | 目标 |
|---|---|---|
| `calculate_energy` | `xtb`, `gaussian` | 使用 Agent 明确选择的方法计算单点能。 |
| `calculate_forces` | `xtb` | 计算非周期结构的原子力。 |
| `calculate_hessian` | `xtb`, `gaussian` | 计算 Hessian，不隐式推导频率和热化学。 |
| `optimize_geometry` | `xtb`, `gaussian`, `sella` | 优化分子几何结构。 |
| `calculate_dipole_moment` | `xtb`, `gaussian` | 计算分子偶极矩。 |
| `calculate_atomic_charges` | `xtb`, `multiwfn` | 计算电子结构布居电荷。 |
| `calculate_electron_isodensity_surface` | `multiwfn` | 从波函数或电子密度文件计算等密度面面积和体积。 |
| `calculate_bond_orders` | `xtb`, `multiwfn` | 计算原子对电子键级。 |
| `derive_vibrational_modes` | `internal_vibrations` | 从已有结构和 Hessian 推导频率与正规模式。 |
| `derive_ir_spectrum` | `internal_spectroscopy` | 从包含强度的振动结果构建 IR 光谱。 |
| `derive_thermochemistry` | `internal_thermochemistry`, `goodvibes` | 从已有能量、频率或量化输出推导热化学量。 |
| `scan_thermochemistry_temperature` | `goodvibes` | 在显式温度列表上评估热化学量。 |
| `analyze_thermochemical_ensemble` | `goodvibes` | 计算构象集合热化学和 Boltzmann 布居。 |
| `validate_thermochemistry_inputs` | `goodvibes` | 检查量化输出的一致性、频率问题和重复结构。 |

### 4.5 反应路径与选择性

| Action | Backend | 目标 |
|---|---|---|
| `locate_transition_state` | `pysisyphus`, `sella` | 从初猜定位候选过渡态，不隐式运行频率或 IRC。 |
| `search_reaction_path` | `pysisyphus` | 在反应物和产物之间执行双端链状态路径搜索。 |
| `scan_reaction_coordinates` | `pysisyphus` | 沿一个显式内坐标进行一维松弛扫描。 |
| `validate_reaction_path` | `internal_reaction_analysis` | 检查路径的原子、端点、连续性和可选键变化。 |
| `analyze_reaction_coordinate` | `internal_reaction_analysis` | 将路径图像和能量整理为相对能量剖面。 |
| `trace_intrinsic_reaction_coordinate` | `pysisyphus` | 从已有过渡态沿两个方向跟踪 IRC。 |
| `analyze_thermochemical_selectivity` | `goodvibes` | 从带标签的结构集合计算选择性和自由能差。 |
| `analyze_reaction_free_energy_profile` | `goodvibes` | 按显式路径定义生成反应自由能剖面。 |

## 5. 18 个 Backend 的职责

| Backend | 主要实现 | 职责 |
|---|---|---|
| `qcelemental` | QCElemental | QCSchema 结构和记录校验。 |
| `cclib` | cclib | Gaussian 等量子化学输出解析。 |
| `rdkit` | RDKit | 结构标准化、三维生成、构象处理和子结构操作。 |
| `openbabel` | Open Babel | 三维结构生成和格式转换。 |
| `rdkit_etkdg` | RDKit ETKDG | 快速构象集合生成。 |
| `crest` | CREST + xTB | 半经验级构象搜索。 |
| `internal_statistics` | 内部确定性代码 | 已有结果的排序、权重和统计。 |
| `internal_reaction_analysis` | 内部确定性代码 | 配位异构、反应路径校验和坐标分析。 |
| `rdkit_gasteiger` | RDKit | Gasteiger 部分电荷。 |
| `xtb` | xTB | 低成本能量、力、Hessian、优化和电性分析。 |
| `multiwfn` | Multiwfn | 波函数、电荷、键级和等密度面分析。 |
| `gaussian` | Gaussian 16 | 高精度分子能量、优化、Hessian 和偶极矩。 |
| `internal_vibrations` | ASE + NumPy | 从 Hessian 推导频率和模式。 |
| `internal_spectroscopy` | NumPy | 从振动结果构建 IR 光谱。 |
| `internal_thermochemistry` | ASE + NumPy | 基础热化学推导。 |
| `goodvibes` | GoodVibes | 准谐振热化学、集合、选择性和反应剖面。 |
| `sella` | Sella | 稳定点和一阶鞍点优化。 |
| `pysisyphus` | pysisyphus | 过渡态、路径、坐标扫描和 IRC 工作流。 |

## 6. Action 如何检索和执行

推荐使用 `progressive` discovery mode。标准流程如下：

1. `list_action_domains`：先查看工具箱支持的科学领域；
2. `browse_action_category`：浏览一个领域中的 Action；
3. `search_actions`：按任务描述、后端或输入输出需求检索；
4. `inspect_action`：读取 Action 的输入、方法参数、设置和输出契约；
5. `inspect_backend`：检查指定 backend 的能力、健康状态和资源要求；
6. `execute_action`：提交一个明确选择了 Action 和 backend 的请求；
7. 批量任务可使用 `submit_action_batch`，异步批量任务可使用
   `submit_action_batch_async` 和 `wait_execution_events`。

检索 xTB 能量计算的请求示例：

```json
{
  "request": {
    "query": "water xtb energy",
    "backend_id": "xtb",
    "detail_level": "summary",
    "limit": 10
  }
}
```

检查具体 Action 契约：

```json
{
  "request": {
    "action_id": "calculate_energy",
    "backend_id": "xtb",
    "detail_level": "contract"
  }
}
```

执行请求的结构示例：

```json
{
  "request": {
    "action_id": "calculate_energy",
    "backend_id": "xtb",
    "inputs": {
      "structure": {
        "symbols": ["O", "H", "H"],
        "geometry": [[0.0, 0.0, 0.0], [0.76, 0.58, 0.0], [-0.76, 0.58, 0.0]]
      }
    },
    "method_spec": {"method": "gfn2"},
    "action_settings": {},
    "resource_limits": {
      "cpu_cores": 2,
      "memory_mb": 2048,
      "gpu_count": 0
    }
  }
}
```

结构只是示意。Agent 应以 `inspect_action` 返回的当前契约为准，不应凭记忆猜测字段。
对于具有多个 backend 的 Action，必须显式选择 backend；工具箱不会自动从 Gaussian 降级到
xTB，也不会自动改方法、基组、温度或资源上限。

## 7. 第二层：原生软件调用

原生层允许 Agent 编写软件原生输入，并运行经过 allowlist 验证的命令。当前登记的软件为：

| software_id | 命令 | 典型用途 |
|---|---|---|
| `gaussian` | `g16`, `formchk` | 自定义 Gaussian route、单点、优化、频率、TS、IRC 和 checkpoint 转换。 |
| `crest` | `crest` | 构象搜索。 |
| `xtb` | `xtb` | 低成本量子化学计算和预筛选。 |
| `openbabel` | `obabel` | 分子格式转换和初始三维结构准备。 |
| `pysisyphus` | `pysis` | 反应路径、TS 和 IRC 工作流。 |
| `goodvibes` | `goodvibes` | Gaussian 输出的热化学和选择性分析。 |
| `multiwfn` | `Multiwfn_noGUI` | 波函数、电荷、键级和电子密度分析。 |

推荐调用顺序：

1. `list_software`：查看可用原生软件；
2. `inspect_software`：查看命令、运行时、输入文件和已知限制；
3. `search_software_documentation`：按关键词检索本地软件文档；
4. `read_software_documentation`：读取命中的具体章节；
5. `write_workspace_text`：把 `.gjf`、YAML、控制文件或脚本写入隔离工作区；
6. `validate_native_job`：在运行前校验命令、路径、文件和资源；
7. `submit_native_job`：提交作业；
8. `get_execution_job`：轮询至 `terminal=true`；
9. `collect_execution_job`：收集 stdout、stderr、输出文件和 provenance；
10. `declare_scientific_artifact`：为需要长期引用的结果登记科学含义。

Gaussian 的命令本身通常只是 `g16 input.gjf`，难点在于正确构造 `.gjf`：分子电荷和
多重度、坐标、方法、基组、溶剂、优化类型、频率、过渡态和 IRC 设置共同定义了计算
实验。因此原生层提供文档检索和提交校验，但科学设置仍由 Agent 根据论文证据明确决定。

## 8. 第三层：Agent 自编 Python 程序

可编程层用于 Action 没有覆盖的轻量分析，例如：

- 整理多个 Gaussian 输出；
- 计算相对能、能垒和单位换算；
- 组合 cclib、RDKit、ASE、NumPy、SciPy 或 pandas；
- 生成表格、JSON、CSV 和绘图数据；
- 对结果执行任务特定但可审计的确定性检查。

推荐调用顺序：

1. `list_analysis_runtimes`：查看可用逻辑 runtime 及包；
2. `inspect_analysis_inputs`：检查工作区中可供程序读取的文件；
3. `write_workspace_text`：写入 Python 程序；
4. `validate_analysis_program`：执行 AST、路径、导入和资源校验；
5. `submit_analysis_program`：提交程序；
6. `get_execution_job`：等待作业终止；
7. `collect_execution_job`：收集程序输出和生成文件；
8. `declare_scientific_artifact`：登记最终数据、表格或图形。

该层不是任意 shell。Agent 只能在隔离工作区和显式 runtime 中运行通过校验的程序，输出
会进入统一作业目录。所有逻辑 runtime 当前均使用 `.envs/minichem` 这一个 Conda 环境。

## 9. 作业状态、工作区与产物

MCP 调用返回的外层 `status=success` 只表示“工具调用成功”，不等于科学计算已经完成。
异步原生软件或 Python 作业必须检查：

- `terminal` 是否为 `true`；
- `job.status` 是否为成功终态；
- `return_code`、`stdout` 和 `stderr`；
- 声明的输出文件是否实际存在；
- 科学结果是否满足收敛、频率或路径等任务要求。

Harness 默认把每次运行隔离在：

```text
tests/results/<cli>/<UTC时间>_<进程号>/
```

其中 `code/` 保存 Agent 写入的输入和程序，`outputs/` 保存执行结果，`report/` 保存最终
报告，`_tool_trace.jsonl` 和 `_tool_results/` 保存工具调用，`_sessions/` 保存聊天与 CLI
会话。Agent 在其他项目接入时，也应为每个评估任务设置独立的
`MINICHEM_MCP_WORKSPACE`，防止任务之间读写彼此文件。

## 10. 典型 Case1 工作流

一个反应机理或选择性解释任务通常可以按以下路线完成，但具体步骤必须服从论文证据：

1. 用 RDKit/Open Babel 从论文给出的 SMILES 或结构信息准备三维结构；
2. 用 ETKDG 或 CREST 枚举关键反应物、络合物和过渡态初猜的构象；
3. 用 xTB 做低成本预优化和粗筛；
4. 用 Gaussian 对保留结构执行论文指定层级的优化、频率和单点能计算；
5. 检查稳定点无虚频、过渡态恰有一个目标虚频，必要时执行 IRC；
6. 用 cclib、GoodVibes 或 Python 程序整理能量、自由能、Boltzmann 权重和选择性；
7. 必要时用 Multiwfn 分析电荷、键级或电子密度；
8. 将输入、输出、计算设置、软件版本和分析结果登记为可追溯产物。

Action 层适合完成其中的标准步骤；Gaussian route 或论文特定流程超出 Action 契约时，
应切换到原生软件层；结果组合和任务特定统计则使用 Python 层。三层配合的目标是既让
Agent 有足够自由度复现论文，又保留明确的资源边界和完整审计记录。
