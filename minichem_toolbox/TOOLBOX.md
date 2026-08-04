# MiniChem Toolbox 结构与能力说明

## 1. 定位

MiniChem Toolbox 服务于以有机分子机理解释、反应路径、过渡态、构象、能量和选择性为核心的 Agent 评估任务。它不是完整材料模拟平台，也不覆盖周期材料、高通量固体计算、分子动力学或复杂多物理场工作流。

当前能力围绕以下主线组织：

```text
分子表示与三维结构
  -> 构象和质子化状态
  -> xTB 低成本预筛
  -> Gaussian 精细计算
  -> 过渡态与反应路径
  -> 振动、热化学和选择性
  -> cclib / Multiwfn / Python 结果分析
```

## 2. 三层接口

### 第一层：预定义 Action

Action 是稳定的结构化操作。Agent 先检索 Action，再读取输入契约，最后提交 JSON 请求。Action 负责参数校验、Backend 选择边界、执行记录和产物登记。

适合：常见且输入输出形式稳定的任务，例如生成三维结构、xTB 能量、构象搜索、热化学和反应路径分析。

### 第二层：原生软件调用

当 Action 无法表达完整软件输入时，Agent 可以自己编写 Gaussian、CREST、xTB 等输入文件，然后通过受审查的原生命令接口运行。工具箱只负责暴露明确可用的命令、隔离作业目录、限制资源、记录日志和收集产物，不替 Agent 决定科学方法。

### 第三层：Python 程序接口

Agent 可以编写 Python 程序，选择一个逻辑运行时，并通过 `researchchem_job.JobContext` 读取声明过的输入、写入声明过的输出。该层适合 cclib 解析、数值处理、结果汇总和自定义后处理。

三个逻辑层共享同一个物理 Conda 环境 `.envs/minichem`，逻辑运行时只用于表达依赖和 Backend 归属。

## 3. 目录职责

```text
config/
  mcp_profiles.yaml                  逻辑运行时、命令路径和环境变量
  native_software_guides.yaml        原生命令白名单与调用说明
  native_software_example_contracts.yaml
                                      原生作业请求示例
  software_capability_sources.yaml   软件别名

docs/software/                       Agent 可检索的软件使用文档
scripts/                             环境创建、MCP 启动和验证
src/minichem_toolbox/                Action、Backend、调度和产物核心
src/minichem_mcp_tools/              MCP 表面、软件检索和作业接口
tests/harnesses/                     三种 CLI 的隔离测试入口
```

## 4. 预定义 Action

工具箱当前保留 37 个 Action。

### 科学数据交换

- `normalize_qcschema_molecule`：规范化 QCSchema 分子记录；
- `validate_qcschema_record`：校验 QCSchema 记录；
- `parse_quantum_chemistry_output`：使用 cclib 解析量化输出。

### 结构与构象

- `standardize_structure`：规范化分子结构；
- `generate_3d_structure`：从分子表示生成三维结构；
- `generate_conformer_ensemble`：生成构象集合；
- `cluster_conformers`：构象聚类；
- `align_molecular_structures`：结构对齐；
- `rank_conformers_from_results`：根据计算结果排序构象；
- `enumerate_coordination_isomers`：枚举配位异构体；
- `assign_protonation_states`：生成或指定质子化状态。

### 化学信息学

- `assign_partial_charges`：分配部分电荷；
- `search_local_substructures`：局部子结构检索；
- `enumerate_tautomers`：枚举互变异构体；
- `enumerate_stereoisomers`：枚举立体异构体。

### 电子结构与性质

- `calculate_energy`：单点能；
- `calculate_forces`：力；
- `calculate_hessian`：Hessian；
- `optimize_geometry`：几何优化；
- `calculate_dipole_moment`：偶极矩；
- `calculate_atomic_charges`：原子电荷；
- `calculate_electron_isodensity_surface`：电子等密度面；
- `calculate_bond_orders`：键级。

### 振动与热化学

- `derive_vibrational_modes`：振动模式；
- `derive_ir_spectrum`：红外光谱；
- `derive_thermochemistry`：热化学量；
- `scan_thermochemistry_temperature`：温度扫描；
- `analyze_thermochemical_ensemble`：构象系综热化学；
- `validate_thermochemistry_inputs`：热化学输入检查；
- `analyze_thermochemical_selectivity`：选择性分析；
- `analyze_reaction_free_energy_profile`：反应自由能剖面。

### 过渡态与反应路径

- `locate_transition_state`：过渡态搜索；
- `search_reaction_path`：反应路径搜索；
- `scan_reaction_coordinates`：反应坐标扫描；
- `validate_reaction_path`：路径有效性检查；
- `analyze_reaction_coordinate`：反应坐标分析；
- `trace_intrinsic_reaction_coordinate`：IRC 跟踪。

## 5. Backend

工具箱保留 18 个 Backend：

| Backend | 主要职责 |
| --- | --- |
| `qcelemental` | QCSchema 规范化和校验 |
| `cclib` | Gaussian 等量化输出解析 |
| `rdkit` | 分子标准化和化学信息学 |
| `rdkit_etkdg` | 三维构象生成 |
| `rdkit_gasteiger` | Gasteiger 部分电荷 |
| `openbabel` | 格式转换和结构准备 |
| `xtb` | 低成本能量、力、优化和电荷 |
| `crest` | 构象和质子化状态搜索 |
| `gaussian` | 核心精细电子结构计算 |
| `sella` | 基于计算器的过渡态优化 |
| `pysisyphus` | 反应路径和过渡态工作流 |
| `goodvibes` | 热化学、系综和选择性分析 |
| `multiwfn` | 波函数和电子密度分析 |
| `internal_statistics` | 构象聚类和统计处理 |
| `internal_reaction_analysis` | 反应坐标和路径分析 |
| `internal_vibrations` | 振动模式处理 |
| `internal_spectroscopy` | 光谱整理 |
| `internal_thermochemistry` | 确定性热化学计算 |

Backend 不会自动替换失败的软件。请求指定的 Backend 不可用或执行失败时，结果会明确报错。

## 6. Action 检索流程

推荐的 MCP 调用顺序：

1. `list_action_domains`：查看能力域；
2. `search_actions`：按目标检索候选 Action；
3. `inspect_action`：读取一个 Action 的完整契约和可用 Backend；
4. 调用对应 Action 工具；
5. 检查返回状态、日志和 artifact 引用。

语义模型存在时可使用混合检索；否则使用 BM25 词法检索。检索只帮助发现工具，不自动替 Agent 选择方法或参数。

## 7. 原生软件调用流程

原生接口覆盖 Gaussian、CREST、xTB、Open Babel、pysisyphus、GoodVibes 和 Multiwfn。

推荐顺序：

1. `list_software`：缩小软件范围；
2. `inspect_software`：读取命令、路径、资源模板和文档索引；
3. `read_software_documentation` 或 `search_software_documentation`：读取具体用法；
4. `write_workspace_text`：写入输入文件；
5. `validate_native_job`：静态校验命令和输入；
6. `submit_native_job`：提交本地异步作业；
7. `get_execution_job`：轮询状态和日志；
8. `collect_execution_job`：收集并登记产物。

执行器不使用 shell 字符串，只运行审查后的 argv；每个作业有独立目录、临时目录、资源限制、stdout、stderr 和状态文件。Gaussian 的 `GAUSS_SCRDIR` 会重定向到该作业自己的临时目录。

## 8. Python 程序调用流程

推荐顺序：

1. `list_analysis_runtimes`：查看依赖和命令；
2. `write_workspace_text`：写入 Python 程序；
3. `validate_analysis_program`：检查导入、输入输出声明和明显路径问题；
4. `submit_analysis_program`：异步运行；
5. `get_execution_job`：轮询；
6. `collect_execution_job`：收集输出。

程序应使用：

```python
from researchchem_job import JobContext

ctx = JobContext.load()
source = ctx.input("gaussian_output")
ctx.write_json("parsed_result", {"source": source.name})
```

`JobContext` 是路径和审计辅助接口，不是操作系统级沙箱。Harness 通过独立工作目录和 CLI 权限配置提供外层隔离。

## 9. 典型 Case1 流程

一个常见的机理任务可以按以下方式完成：

1. 用 RDKit/Open Babel 从 SMILES 或正文结构生成三维几何；
2. 用 CREST 或 RDKit ETKDG 搜索构象；
3. 用 xTB 预优化和粗排；
4. Agent 编写 Gaussian 输入，进行 DFT 优化和频率计算；
5. 搜索过渡态并运行 IRC，验证反应物和产物连接关系；
6. 用 GoodVibes 整理热化学、构象系综和选择性；
7. 用 cclib、Multiwfn 或 Agent Python 程序提取和汇总结果。

核心难点仍是 Agent 是否能从论文中正确恢复分子、构象、计算层级、溶剂模型、约束、过渡态假设和结果判据；工具箱只提供可审计的执行能力。
