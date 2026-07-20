# ResearchChemBench 化学工具箱能力扩展实施计划

> 状态：本轮实施完成；候选能力按验证门槛持续扩展
> 基线提交：`fd01f226cd31b6c0bf9e2420aec160a2a7bc76e6`
> 基线测试：`71 passed`
> 原则：科学动作优先、Agent 显式选择、无自动回退、软件能力多对多映射

## 1. 目标

本轮不以“每个软件增加一个工具”为目标，而是建立完整的多对多能力图：

- 一个科学动作可以由多个软件实现；
- 一个综合软件可以实现多个科学动作；
- 专用软件只暴露其边界明确的能力，不强行增加无意义动作；
- 数据查询、确定性推导和格式转换不强制 Agent 选择计算软件；
- 组合型计算要求 Agent 显式选择所有组件软件；
- 只有通过类型化适配和真实验证的 Action–Backend 组合才进入公开 MCP Catalog。

## 2. 四级能力状态

| 状态 | 含义 | 是否公开给 Agent |
|---|---|---:|
| `documented` | 对应版本的官方资料声明支持 | 否 |
| `installed` | 本机安装、构建或数据资源具备该能力 | 否 |
| `adapted` | 已实现类型化输入、执行、解析和 Artifact | 否 |
| `validated` | 已通过真实科学计算与 MCP 端到端测试 | 是 |

禁止仅凭软件手册把能力标记为可用；也禁止仅凭命令能够启动就把能力公开为 MCP Action。

## 3. Provider 类型

现有 Scientific/Data 二分法扩展为：

| Provider 策略 | 用途 | Agent 是否选择 |
|---|---|---:|
| `agent_backend_required` | 数值计算软件或算法会影响科学结果 | 是 |
| `agent_components_required` | 优化器、动力学驱动和电子结构等组合计算 | 是，选择全部组件 |
| `agent_source_required` | 同一数据动作存在多个数据源 | 是 |
| `fixed_source` | 动作已经明确绑定一个数据源 | 否 |
| `internal_deterministic` | 单位转换、确定性统计和结构化推导 | 否 |

内部始终记录实际执行实现及版本，但不要求 Agent 为没有真实选择空间的动作提交伪 `backend_id`。

## 4. 分阶段实施

### 阶段 A：资料与能力审计

1. 建立 `config/software_capability_sources.yaml`。
2. 从当前 BackendSpec、软件清单、运行环境状态和官方资料生成能力目录。
3. 将官方资料索引、本机版本、当前 Action 和候选 Action 写入：
   `.software_cache/documentation/<software>/<version>/`。
4. 对可下载的官方 PDF、HTML 手册保存本地副本；记录 URL、获取日期和 SHA-256。

### 阶段 B：协议升级

1. 为 ActionSpec 增加 `selection_policy` 和 Provider 语义。
2. 为 ActionRequest 增加 `component_backends` 与可选 `source_id`。
3. 为每个 Action–Backend 组合声明：
   - 支持的体系类型；
   - 输入与输出语义类型；
   - 方法和设置 Schema；
   - 所需组件 Backend；
   - 所需软件、模型和数据资源；
   - 能力验证级别。
4. Dispatcher 只执行 Agent 的精确选择，不排序、不补全、不回退。

### 阶段 C：扩展已公开软件

优先扩展当前已经在公共 Runtime 中的软件：

- RDKit / PubChem：标识符、描述符、指纹、相似性、子结构和枚举；
- xTB / tblite / PySCF / Psi4：力、电荷、轨道、键级、响应和激发态；
- ORCA / Gaussian / GAMESS：力、波函数性质、TS/IRC、激发态和光谱；
- MACE / CHGNet / DeePMD / NequIP / Allegro：按模型适用域扩展分子、周期、优化和动力学；
- OpenMM / GROMACS / LAMMPS / NAMD / Amber / CHARMM：力场能量、增强采样和分析；
- QE / CP2K / SIESTA / DFTB+ / ABINIT / VASP：能带、DOS、密度、介电、NEB、AIMD；
- Phonopy / Phono3py：热力学、声子寿命和热输运；
- Vina / GNINA：打分、精修和重打分。

### 阶段 D：接入 runtime-only 软件

第一批直接接入：NWChem、GPAW、HOOMD-blue、MDTraj、pymatgen、spglib。

第二批新增分析和输运 Action：Multiwfn、Critic2、LOBSTER、pymbar、alchemlyb、Wannier90、Yambo、ShengBTE、TheoDORE。

第三批反应和激发态 Action：Arkane、MESS、MESMER、OpenMolcas。

### 阶段 E：组合型软件

在 `component_backends` 完成后接入：

- geomeTRIC / Sella + Agent 选择的能量梯度后端；
- SHARC / Newton-X + Agent 选择的激发态电子结构后端；
- CENSO / autodE / AutoMeKin / KinBot / RMG-Py 的可分解原子能力。

不暴露 `run_censo`、`run_sharc`、`run_autode` 等隐藏科学决策的流程入口。

## 5. Action 设计门槛

新增 Action 必须满足：

1. 名称描述科学结果而不是软件；
2. 只有一个主要科学输出；
3. 不通过 `mode` 或 `driver` 切换到不同科学任务；
4. 软件专属输入被转换为类型化字段；
5. 输出可作为其他 Action 的 Artifact 输入；
6. 有独立科学正确性测试；
7. 不隐藏可独立失败、复用或需要 Agent 判断的步骤。

## 6. 验证要求

每个公开 Action–Backend 组合至少具备：

- Schema 拒绝缺失和未知科学参数；
- 环境和资源健康检查；
- 一个最小真实科学计算；
- 结构化结果数值和单位检查；
- Artifact 哈希和父子关系检查；
- MCP 调用回归；
- 无自动 fallback 的 trace 断言。

## 7. 文档与缓存约定

- `.software_cache/documentation/`：官方资料、本机帮助输出、版本探测、下载校验；
- `config/software_capability_sources.yaml`：受 Git 管理的官方来源和候选能力声明；
- `docs/tools/CHEMISTRY_TOOLBOX_SOFTWARE_CAPABILITY_MATRIX.md`：可审查能力矩阵；
- `CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md`：只记录最终公开且验证通过的能力。

## 8. 本轮实施结果

- Catalog 从基线的 45 个 Action / 55 个 BackendSpec 扩展到 101 个 Action / 76 个 BackendSpec；原有 Action 和 Backend 均未删除。
- 已落地 Provider 选择协议、`component_backends`、Backend 专属 Schema、严格未知字段拒绝、无自动选择和无自动回退。
- 已新增 56 个原子 Action，并将 21 个此前未公开的 Backend 接入类型化执行链。
- geomeTRIC 与 Sella 只负责优化算法；计算器、方法和参数仍由 Agent 通过 `component_backends.calculator` 显式指定。
- MESS、MESMER、ShengBTE 等只接受 Agent 明确提供的原生科学模型/输入文件，不替 Agent 构造或修改反应网络、散射模型或计算流程。
- 官方资料与本地手册统一登记到 `.software_cache/documentation/`；资料存在不等于能力已公开。
- TheoDORE、Wannier90、Yambo、SHARC、Newton-X、Arkane 等仍保持候选或 runtime-only 状态，直到能够定义边界清晰的原子 Action、取得版本匹配输入样例并通过有界真实计算。不会为了提高工具数量而暴露软件级流程入口。
- AiiDA、atomate2、jobflow、QCEngine 等执行/工作流基础设施继续作为运行底座，不伪装成独立科学 Action。

详细结果、验证证据和剩余事项见 `CHEMISTRY_TOOLBOX_CAPABILITY_EXPANSION_REPORT_20260720.md`。
