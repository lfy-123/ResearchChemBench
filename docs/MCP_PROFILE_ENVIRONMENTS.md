# ResearchChemBench MCP 工具发现与多环境设计

> 2026-07-18 更新：profile 现在只表示后端依赖运行时，不再筛选或拥有公共工具。所有任务始终连接一个暴露 44 个原子 Actions 的统一 MCP server；ORCA 6.1.1、OpenMPI 4.1.8 和 GNINA 1.3.3 已完成配置，当前 45/45 BackendSpecs 可用。当前事实以 `evaluation/mcp_tools/TOOL_CATALOG.md` 和 `docs/tools/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md` 为准；下文旧命令/工具名仅保留为历史迁移背景。

## 1. 智能体如何看到 MCP 工具

MCP server 不是智能体眼中的一个不透明“总工具”。连接建立后，Agent CLI 会向每个
MCP server 请求工具列表。每个工具都作为独立条目返回，至少包含：

- 工具名称；
- 功能说明；
- JSON Schema 参数定义；
- 可选的返回结构和行为提示。

因此，智能体能够区分 `query_pubchem`、`run_pyscf`、`run_openmm` 等具体工具，知道
它们分别做什么、需要哪些参数。多个 MCP server 同时连接时，Claude、Codex、OpenCode
通常会使用 server 名作为命名空间；概念上类似：

```text
researchchem_services/query_materials_project
researchchem_quantum/run_pyscf
researchchem_md/run_openmm
```

不同 CLI 的最终显示格式略有差异，但不会把一个 server 下的所有工具折叠成一个只能
传自然语言的模糊接口。

一次暴露 41 个工具虽然可行，但会增加小模型的工具选择负担。因此 benchmark 推荐按
任务只启动相关 profile，例如材料查询任务使用 `core,services`，量化任务使用
`core,quantum,psi4`。

## 2. 为什么拆成多个环境

化学软件的冲突主要不在 MCP，而在 NumPy/SciPy、MPI、BLAS、CUDA/PyTorch、C++
运行库和 Python 版本。实际安装中已经观察到：CP2K 和 DFTB+ 放进同一个环境时，
求解器会把 CP2K 2026.1 降级为旧的 Python 3.8 构建。因此当前设计采用“一个兼容类别
一个 MCP 环境”，必要时再把纯可执行程序放到支撑环境。

工具源码仍保持一工具一文件：

```text
evaluation/mcp_tools/tools/<tool_name>.py
```

环境拆分只发生在运行和安装层，不影响以后增加、删除或修改单个工具。

## 3. 当前 profile 分类

| Profile | Conda 名称 | 存储前缀 | 工具数 | 主要后端 |
|---|---|---|---:|---|
| `core` | `researchchem-core` | `.toolbox_env` | 12 | RDKit、ASE、cclib、NumExpr、ChemGraph core |
| `services` | `researchchem-services` | `.tool_envs/services` | 4 | PubChem、RCSB、Catalysis-Hub、Materials Project |
| `quantum` | `researchchem-quantum` | `.tool_envs/quantum` | 4 | ASE、xTB、PySCF、TBLite、MACE；ORCA 为人工后端 |
| `psi4` | `researchchem-psi4` | `.tool_envs/psi4` | 1 | Psi4 |
| `reaction` | `researchchem-reaction` | `.tool_envs/reaction` | 8 | CREST、CENSO、GoodVibes、pysisyphus、CatMAP、Cantera |
| `qe` | `researchchem-qe` | `.tool_envs/qe` | 1 | Quantum ESPRESSO |
| `cp2k` | `researchchem-cp2k` | `.tool_envs/cp2k` | 1 | CP2K |
| `periodic` | `researchchem-periodic` | `.tool_envs/periodic` | 1 | DFTB+、SIESTA，以及跨环境周期调度 |
| `phonons` | `researchchem-phonons` | `.tool_envs/phonons` | 1 | Phonopy、Phono3py |
| `md` | `researchchem-md` | `.tool_envs/md` | 6 | OpenMM、PDBFixer、MDAnalysis、GROMACS、LAMMPS、PLUMED |
| `openff` | `researchchem-openff` | `.tool_envs/openff` | 2 | OpenFF Toolkit、Interchange、AmberTools AM1-BCC |
| `mlip` | `researchchem-mlip` | `.tool_envs/mlip` | 1 | MACE、CHGNet |
| `docking` | `researchchem-docking` | `.tool_envs/docking` | 1 | AutoDock Vina；GNINA 为人工后端 |

额外的 `researchchem-abinit`（存储在 `.tool_envs/abinit`）是纯可执行程序支撑环境，不启动单独 MCP server。
`periodic` server 通过绝对命令路径调用它，从而避免 ABINIT 的 MPI 栈污染 DFTB+/SIESTA
环境。

## 4. 配置文件和关键代码

| 文件 | 作用 |
|---|---|
| `config/mcp_profiles.yaml` | profile、工具归属、conda/pip 依赖、命令映射和健康检查 |
| `evaluation/mcp_tools/profiles.py` | 加载配置、验证工具不重复、构建环境变量和 server 启动命令 |
| `evaluation/mcp_tools/server.py` | 只注册选中 profile 的工具 |
| `evaluation/config.py` | 为一次 benchmark 运行生成一个或多个 MCP server spec |
| `evaluation/run_task.py` | 写入 Claude/OpenCode 配置并构造 Codex MCP 参数 |
| `scripts/setup_mcp_profile_envs.py` | 创建、续装和记录所有隔离环境 |
| `scripts/configure_mcp_conda_envs.py` | 注册 `researchchem-*` 名称并安装运行库兼容 hook |
| `scripts/check_mcp_profile_envs.py` | 跨解释器检查并生成状态报告 |

### 模型权重与工具源码为什么分开放

`evaluation/mcp_tools/` 保存的是 MCP server、工具定义、参数 schema 和调用适配器，这些
源码应当体积小、可审查并提交到 Git。MACE 权重属于可重新下载的运行时资产，约几十到
数百 MB，不能和一工具一文件的源码一起打包，也不应跟随某个 Agent CLI 的全局缓存。

项目统一使用以下目录：

```text
ResearchChemBench/.model_cache/
└── mace/
    └── macempa0mediummodel
```

`.model_cache/` 已加入 `.gitignore`。`core`、`quantum`、`mlip` 三个 profile 启动时会
同时设置 `RESEARCHCHEMBENCH_MODEL_CACHE` 和 `XDG_CACHE_HOME`，因此 MCP subprocess、
`conda activate researchchem-*` 以及直接运行 `.tool_envs/.../bin/python` 都会复用同一份
模型。原先出现在 `.opencode/cache/mace` 是因为 MACE 继承了 OpenCode 进程的
`XDG_CACHE_HOME`，并不表示模型属于 OpenCode。

如需把大模型放到独立数据盘，可在被 Git 忽略的 `config.local.env` 中设置：

```bash
RESEARCHCHEMBENCH_MODEL_CACHE=/absolute/path/to/researchchem-model-cache
```

修改后重新执行 `scripts/configure_mcp_conda_envs.py`，使直接激活 Conda 环境的 hook 也
使用新位置。MACE 0.3.16 会在该根目录下自动创建 `mace/` 子目录。

## 5. 安装和复查

安装全部 profile 和支撑环境：

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench
.toolbox_env/bin/python scripts/setup_mcp_profile_envs.py --continue-on-error
```

只安装指定类别：

```bash
.toolbox_env/bin/python scripts/setup_mcp_profile_envs.py \
  --profiles services,quantum,psi4

.toolbox_env/bin/python scripts/setup_mcp_profile_envs.py \
  --profiles periodic,phonons \
  --support-environments abinit
```

安装器会合并并持续写入：

```text
config/mcp_profile_status.json
```

安装完成后可以按名称查看和激活：

```bash
conda env list | grep researchchem
conda activate researchchem-quantum
python -c 'from mace.calculators import mace_mp; print("MACE import OK")'
conda deactivate
```

Conda 的环境名称本质上是 `envs_dirs` 下的目录项。工具环境体积较大，因此本项目通过
`.conda_envs/researchchem-*` 注册稳定名称，实际数据仍保存在项目内原前缀，不复制也不
移动几十 GB 环境。名称丢失或换机器后可重新注册：

```bash
.toolbox_env/bin/python scripts/configure_mcp_conda_envs.py
```

检查所有环境并真实查询 Materials Project：

```bash
.toolbox_env/bin/python scripts/check_mcp_profile_envs.py \
  --live-materials-project \
  --check-models
```

结果写入：

```text
docs/MCP_PROFILE_STATUS.md
docs/MCP_PROFILE_STATUS.json
```

## 6. 本地 API key 和环境变量

项目根目录使用：

```text
config.local.env
```

该文件已加入 `.gitignore`，`scripts/run_agent_eval.sh` 会自动加载。发布项目时只保留：

```text
config.local.env.example
```

示例变量：

```bash
MP_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
JUDGE_API_KEY=
JUDGE_API_BASE=
JUDGE_MODEL_NAME=
CHEMGRAPH_ORCA_COMMAND=
CHEMGRAPH_CENSO_COMMAND=
CHEMGRAPH_GNINA_COMMAND=
```

不要把真实 key 写进 shell 脚本、任务 workspace、MCP JSON 配置或状态报告。

## 7. 运行不同任务

```bash
# 外部数据库查询
bash scripts/run_agent_eval.sh \
  --agent opencode \
  --task ChemGraph_003 \
  --mcp-profiles core,services \
  --no-score

# 分子量化计算
bash scripts/run_agent_eval.sh \
  --agent codex \
  --task ChemGraph_010 \
  --mcp-profiles core,quantum,psi4 \
  --timeout-seconds 3600 \
  --no-score

# 周期计算和声子任务
bash scripts/run_agent_eval.sh \
  --agent claude \
  --task ChemGraph_020 \
  --mcp-profiles core,qe,cp2k,periodic,phonons \
  --timeout-seconds 7200 \
  --no-score
```

`--mcp-profiles` 启用多环境模式；旧的 `--mcp-tools` 仍保留给单 server/兼容模式。

## 8. 尚需人工配置的后端

- ORCA：需要从官方渠道注册、下载并设置 `CHEMGRAPH_ORCA_COMMAND`；
- GNINA：需要下载官方 binary/container 并设置 `CHEMGRAPH_GNINA_COMMAND`；
- 周期程序还需要用户提供合法且匹配的赝势/参数文件；
- DFTB+ 需要 Slater-Koster 参数集；
- CatMAP、pysisyphus、CENSO 等真实任务仍需要合法模型/输入和量化后端配置；
  CENSO 2.1.2 已安装并修正为 `-i/--maxcores` 接口，但完整 DFT workflow 仍需
  ORCA 或 TURBOMOLE。

NequIP、DeepMD、FAIRChem、AIMNet2 没有被标为当前 `run_mlip` 的必需依赖，因为工具
尚未实现这些后端的模型加载、checkpoint 校验和安全下载策略。只安装 Python 包并不能
让它们正常执行；完成 adapter 后再建立独立环境更合理。

## 9. 当前验证结论

最新自动报告为 `docs/MCP_PROFILE_STATUS.md`。当前 12/12 profile 的必需模块、命令和
MCP 工具清单均通过，41 个工具全部被且只被一个 profile 管理；Materials Project live
smoke 已通过。2026-07-18 的最终回归结果如下：

- `evaluation/mcp_tools/test_tools/`：41 passed（每个公开工具一个测试文件）；
- `tests/`：77 passed；
- MACE `medium-mpa-0`：已下载并在 core、quantum、mlip 三个环境中完成 Si 能量计算，3/3 passed；
- 14 个 Conda 环境：`pip check` 全部通过；
- profile 归属测试：41 个工具在各自环境中全部通过，RuntimeWarning 按错误处理；
- 12-profile Codex dry-run：通过，能够为一次任务生成 12 个独立 MCP server 配置；
- 私钥扫描：真实 key 只存在于被忽略且权限为 `0600` 的 `config.local.env`。

ORCA 和 GNINA 仍明确标记为人工配置项。原 core 环境的 netCDF4/NumPy ABI warning
已通过改用 conda-forge netCDF4 消除；当前主测试剩余提示仅为 RDKit 兼容 API 的
deprecation warning，不影响当前结果。

### MACE C++ ABI 修复说明

PyPI PyTorch wheel 没有把 Conda 环境的 `libstdc++.so.6` 写入自己的 RPATH，直接执行
环境 Python 时可能先加载 Ubuntu 系统库，从而报 `CXXABI_1.3.15 not found`。配置脚本
会在 core、quantum、mlip 环境安装 `researchchem_runtime.pth`，在 Python 启动阶段预载
当前前缀的 C++ runtime；Conda 激活 hook 同时把 `$CONDA_PREFIX/lib` 放到动态库搜索路径
最前面。该修复适用于直接前缀 Python、`conda activate` 和 MCP subprocess 三种入口。

`cuequivariance ... is not available` 只表示 CUDA 加速扩展没有安装；CPU MACE 计算仍正常，
不应为了消除提示向 CPU 环境强装 CUDA 依赖。

三个 MACE 环境均固定使用 `mace-torch==0.3.16`。该版本遵循
`XDG_CACHE_HOME`；旧版 0.3.13 会把权重写死到 `~/.cache/mace`，因此不再使用。
