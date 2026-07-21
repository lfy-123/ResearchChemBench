# MCP 工具逐项测试与未配置软件手动配置指南

> 2026-07-18 更新：本文主体记录旧 41 工具基线，下面的 `run_orca`/`run_gnina` 内容只作历史参考。ORCA 6.1.1、OpenMPI 4.1.8 和 GNINA 1.3.3 已配置完成；当前原子工具与资源状态请使用 `chemistry_toolbox/docs/TOOLBOX_STATUS.md` 和 `chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md`。

> 本文前半部分记录 2026-07-17 单一 `.toolbox_env` 下的逐工具测试。后续已经建立
> 多 profile 环境并补装 Psi4、QE、CP2K、DFTB+、SIESTA、ABINIT、GROMACS、LAMMPS、
> PLUMED、CENSO、GoodVibes、pysisyphus、CatMAP、Vina 等后端。当前状态请看
> [MCP_PROFILE_STATUS.md](../chemistry_toolbox/docs/MCP_PROFILE_STATUS.md)，环境设计请看
> [MCP_PROFILE_ENVIRONMENTS.md](MCP_PROFILE_ENVIRONMENTS.md)。下面的人工安装说明仍可作为
> ORCA、GNINA 和许可证软件的参考。

## 1. 本次测试结论

测试目录：

```text
chemistry_toolbox/mcp/test_tools/
```

公开工具文件与测试文件严格一一对应：

- MCP 工具文件：41
- `test_<tool_name>.py`：41
- 缺失测试：0
- 多余测试：0

执行结果：

```text
默认可重复模式：41 passed
真实网络服务模式：5 passed
完整项目回归：70 passed
```

首轮测试发现 `test_run_ase.py` 在执行前没有生成 `data/water.xyz`，导致
`FileNotFoundError`。这是新测试夹具的问题，不是 `run_ase` 实现问题；补写 XYZ
输入后，41 个测试全部通过。

当前没有无法修复的工具代码失败。仍存在两类非失败提示：

1. RDKit `MolStandardize` 使用了上游标记为 deprecated 的兼容入口；
2. PubChemPy 的 `canonical_smiles/isomeric_smiles` 属性有弃用警告。

它们不影响当前返回结果，后续升级 RDKit/PubChemPy 时应迁移到新版属性并重新锁定版本。

## 2. 如何运行测试

先激活环境：

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench
source chemistry_toolbox/scripts/activate_toolbox_env.sh
```

运行全部 41 个逐工具测试：

```bash
bash chemistry_toolbox/mcp/test_tools/run_tests.sh
```

真实访问 PubChem、RCSB PDB、Catalysis-Hub：

```bash
bash chemistry_toolbox/mcp/test_tools/run_tests.sh --live-network
```

测试后刷新真实软件状态报告：

```bash
bash chemistry_toolbox/mcp/test_tools/run_tests.sh --live-network --status-report
```

单独复测一个工具：

```bash
python -m pytest -q   chemistry_toolbox/mcp/test_tools/test_run_cp2k.py
```

## 3. 41 个工具的测试状态

| Tool | 测试方式 | 当前结果 |
|---|---|---|
| `analyze_md_trajectory` | 真实 MDAnalysis/PDB | 通过 |
| `analyze_wavefunction` | 真实 xTB 输出→cclib | 通过 |
| `calculator` | 真实 NumExpr | 通过 |
| `check_backend_availability` | 真实模块/命令探测 | 通过 |
| `compute_thermochemistry` | GoodVibes 缺失状态 | 通过，返回 unavailable |
| `convert_structure` | 真实 ASE XYZ 转换 | 通过 |
| `extract_output_json` | 真实 ChemGraph JSON core | 通过 |
| `find_transition_state` | pysisyphus 缺失状态 | 通过，返回 unavailable |
| `generate_3d_structure` | 真实 RDKit 3D | 通过 |
| `generate_conformers_crest` | 真实 CREST/xTB | 通过 |
| `generate_conformers_rdkit` | 真实 RDKit ETKDG/MMFF | 通过 |
| `list_toolbox_capabilities` | 读取 99 项软件注册表 | 通过 |
| `molecule_name_to_smiles` | mock 与真实 PubChem 两种模式 | 通过 |
| `prepare_md_system` | 真实 PDBFixer/OpenMM | 通过 |
| `query_catalysis_hub` | mock 与真实 GraphQL 两种模式 | 通过 |
| `query_materials_project` | 无 key 状态 | 通过，返回 unavailable |
| `query_pubchem` | mock 与真实 PUG-REST 两种模式 | 通过 |
| `query_rcsb_pdb` | mock 与真实 RCSB API 两种模式 | 通过 |
| `refine_ensemble_censo` | CENSO 缺失状态 | 通过，返回 unavailable |
| `run_ase` | 真实 ChemGraph ASE/EMT | 通过 |
| `run_cantera` | 真实 Cantera 平衡计算 | 通过 |
| `run_catmap` | CatMAP 缺失状态 | 通过，返回 unavailable |
| `run_cp2k` | CP2K 缺失状态 | 通过，返回 unavailable |
| `run_docking` | Vina/GNINA CLI 缺失状态 | 通过，返回 unavailable |
| `run_gromacs` | GROMACS 缺失状态 | 通过，返回 unavailable |
| `run_irc` | pysisyphus 缺失状态 | 通过，返回 unavailable |
| `run_lammps` | LAMMPS 缺失状态 | 通过，返回 unavailable |
| `run_mlip` | 真实 CHGNet/Si | 通过 |
| `run_openmm` | 真实 OpenMM 水分子 | 通过 |
| `run_orca` | ORCA 未挂载状态 | 通过，返回 unavailable |
| `run_periodic_calculation` | 周期后端缺失状态 | 通过，返回 unavailable |
| `run_phonopy` | 真实 Phonopy 4 `phonopy-init` | 通过 |
| `run_plumed` | PLUMED 缺失状态 | 通过，返回 unavailable |
| `run_psi4` | Psi4 缺失状态 | 通过，返回 unavailable |
| `run_pyscf` | 真实 PySCF H₂ 单点 | 通过 |
| `run_quantum_espresso` | `pw.x` 缺失状态 | 通过，返回 unavailable |
| `run_reaction_kinetics` | 真实 SciPy ODE | 通过 |
| `run_xtb` | 真实 xTB 水分子 | 通过 |
| `smiles_to_coordinate_file` | 真实 ChemGraph/RDKit/ASE | 通过 |
| `standardize_molecule` | 真实 RDKit MolStandardize | 通过 |
| `validate_computation` | 真实 JSON/有限数检查 | 通过 |

## 4. 现有 wrapper 对应后端的手动配置

以下软件配置完成后无需修改 MCP tool 文件，重启 Agent/MCP server 即可被现有 wrapper
发现。推荐把命令变量写入启动 benchmark 的 shell 或安全环境文件，不要写入任务 workspace。

### 4.1 GoodVibes：`compute_thermochemistry`

```bash
source chemistry_toolbox/scripts/activate_toolbox_env.sh
python -m pip install goodvibes
export CHEMGRAPH_GOODVIBES_COMMAND="$(command -v goodvibes)"
goodvibes --help
```

若 PyPI 包与官方版本不一致，应按
[GoodVibes 官方仓库](https://github.com/patonlab/GoodVibes) 安装。真实输入必须是
GoodVibes 支持的 Gaussian/ORCA 等频率输出，普通文本不能作为功能 smoke。

### 4.2 pysisyphus：`find_transition_state`、`run_irc`

建议单独创建兼容环境，按
[pysisyphus 官方文档](https://pysisyphus.readthedocs.io/) 安装，并确认 `pysis`：

```bash
export CHEMGRAPH_PYSIS_COMMAND=/absolute/path/to/pysis
"$CHEMGRAPH_PYSIS_COMMAND" --help
```

工具输入是已经准备好的 pysisyphus YAML；同时需要在 YAML 中配置可用的量化后端。

### 4.3 Materials Project API：`query_materials_project`

```bash
source chemistry_toolbox/scripts/activate_toolbox_env.sh
python -m pip install mp-api
export MP_API_KEY='your-materials-project-key'
python -c 'from mp_api.client import MPRester; print("mp-api import OK")'
```

API key 从 [Materials Project](https://materialsproject.org/) 账户获取。不要把 key 提交到仓库。

### 4.4 CENSO：`refine_ensemble_censo`

xTB 和 CREST 已配置。继续按照
[CENSO 官方说明](https://xtb-docs.readthedocs.io/en/latest/CENSO_docs/censo.html)
安装 CENSO，然后：

```bash
export CHEMGRAPH_CENSO_COMMAND=/absolute/path/to/censo
"$CHEMGRAPH_CENSO_COMMAND" --help
```

CENSO 还可能需要 ORCA/TURBOMOLE 等量化后端；这类后端必须单独获得许可。

### 4.5 CatMAP：`run_catmap`

```bash
source chemistry_toolbox/scripts/activate_toolbox_env.sh
python -m pip install catmap
export CHEMGRAPH_CATMAP_COMMAND="$(command -v catmap)"
catmap --help
```

如果 PyPI 安装不可用，按 [CatMAP 官方文档](https://catmap.readthedocs.io/)
从源码安装。工具接受已经准备好的 CatMAP model 文件。

### 4.6 CP2K：`run_cp2k`、`run_periodic_calculation`

建议独立 conda 环境，避免当前 OpenFF/AmberTools 栈的求解冲突：

```bash
mamba create -n rchem-cp2k -c conda-forge cp2k
export CHEMGRAPH_CP2K_COMMAND=/path/to/rchem-cp2k/bin/cp2k
"$CHEMGRAPH_CP2K_COMMAND" --version
```

如果命令实际为 `cp2k.psmp`，变量可以直接指向该绝对路径。

### 4.7 AutoDock Vina/GNINA：`run_docking`

当前已安装 Vina Python 包，但没有 `vina` CLI。安装命令行程序：

```bash
mamba install -p .toolbox_env -c conda-forge vina
export CHEMGRAPH_VINA_COMMAND=/absolute/path/to/vina
vina --help
```

GNINA 使用官方 release/container：

```bash
export CHEMGRAPH_GNINA_COMMAND=/absolute/path/to/gnina
gnina --help
```

复测需要真实 receptor/ligand PDBQT，不能用普通 PDB 代替。

### 4.8 GROMACS：`run_gromacs`

```bash
mamba create -n rchem-gromacs -c conda-forge gromacs
export CHEMGRAPH_GROMACS_COMMAND=/path/to/rchem-gromacs/bin/gmx
"$CHEMGRAPH_GROMACS_COMMAND" --version
```

`run_gromacs` 接受已经由 `grompp` 生成的 TPR；系统构建和参数化需预先完成。

### 4.9 LAMMPS：`run_lammps`

```bash
mamba create -n rchem-lammps -c conda-forge lammps
export CHEMGRAPH_LAMMPS_COMMAND=/path/to/rchem-lammps/bin/lmp
"$CHEMGRAPH_LAMMPS_COMMAND" -help
```

需要确保安装版本包含输入脚本所需的 package（KSPACE、MOLECULE、ML-IAP 等）。

### 4.10 ORCA：`run_orca`

从 [ORCA 官方网站](https://www.faccts.de/orca/) 注册并人工下载，不要把安装包或许可证
加入仓库：

```bash
export CHEMGRAPH_ORCA_COMMAND=/opt/orca/orca
export PATH=/opt/orca:$PATH
"$CHEMGRAPH_ORCA_COMMAND" --version
```

集群上还要匹配 ORCA 要求的 OpenMPI 版本。测试时提供真实 `.inp` 文件。

### 4.11 Quantum ESPRESSO：`run_quantum_espresso`、`run_periodic_calculation`

```bash
mamba create -n rchem-qe -c conda-forge quantum-espresso
export CHEMGRAPH_QE_COMMAND=/path/to/rchem-qe/bin/pw.x
"$CHEMGRAPH_QE_COMMAND" -help
```

还需准备与输入一致的赝势目录；赝势文件放在任务 workspace 或管理员批准的共享目录。

### 4.12 DFTB+、SIESTA、ABINIT：`run_periodic_calculation`

```bash
export CHEMGRAPH_DFTBPLUS_COMMAND=/absolute/path/to/dftb+
export CHEMGRAPH_SIESTA_COMMAND=/absolute/path/to/siesta
export CHEMGRAPH_ABINIT_COMMAND=/absolute/path/to/abinit
```

分别验证：

```bash
"$CHEMGRAPH_DFTBPLUS_COMMAND" --version
"$CHEMGRAPH_SIESTA_COMMAND" --version
"$CHEMGRAPH_ABINIT_COMMAND" --version
```

DFTB+ 还需要 Slater–Koster 参数集；SIESTA/ABINIT 需要匹配元素和泛函的赝势。

### 4.13 PLUMED：`run_plumed`

```bash
mamba create -n rchem-plumed -c conda-forge plumed
export CHEMGRAPH_PLUMED_COMMAND=/path/to/rchem-plumed/bin/plumed
"$CHEMGRAPH_PLUMED_COMMAND" info
```

`run_plumed` 使用 `plumed driver`，需要合法的 PLUMED 输入和可读取轨迹。

### 4.14 Psi4：`run_psi4`

当前综合环境中 conda 求解未完成，建议使用独立环境：

```bash
mamba create -n rchem-psi4 -c conda-forge psi4 python=3.10
/path/to/rchem-psi4/bin/python -c 'import psi4; print(psi4.__version__)'
```

当前 `run_psi4` 是 Python API wrapper，因此 MCP server 解释器必须能 import Psi4。最稳妥
方案是为 Psi4 单独启动一个 MCP server，或者把兼容 Psi4 安装到 `.toolbox_env`。

## 5. 其他未配置开源/人工软件

这些条目已登记在 `config/toolbox_registry.yaml`，但当前没有独立的、完成真实 smoke 的
公开 wrapper。安装后还需要补充或扩展 adapter，不能仅凭“命令存在”宣称集成完成。

| 软件 | 建议手动配置 |
|---|---|
| AiiDA | `pip install aiida-core`，运行 `verdi presto`/官方 profile 配置，再为 AiiDA daemon/provenance 增加专用 adapter。 |
| jobflow | `pip install jobflow`，按官方文档配置本地或 MongoDB JobStore。 |
| atomate2 | `pip install atomate2`，配置 jobflow store、计算机资源、赝势和所需 DFT 程序。 |
| NWChem | 在独立 conda 环境安装 `nwchem`，把命令加入 PATH；ChemGraph ASE backend 会从 PATH 查找。 |
| autodE | `pip install autode`，在 Python 中配置 `autode.Config` 的 ORCA/xTB 等后端；之后增加专用 wrapper。 |
| geomeTRIC | 已安装；若用于新工作流，确认 `geometric-optimize --help` 并为目标计算器增加 adapter。 |
| Sella | 已安装；需要选择 ASE calculator 后再增加真实 TS 输入和 wrapper。 |
| Critic2 | 从 conda-forge 或官方源码安装 `critic2`，准备电荷密度/波函数文件，再扩展 `analyze_wavefunction`。 |
| Multiwfn | 审阅官方获取/再分发条款后手动下载，设置 `CHEMGRAPH_MULTIWFN_COMMAND=/path/Multiwfn`；仍需增加非交互输入 adapter。 |
| GAMESS | 在官网注册、接受条款并安装，配置 `rungms` 及 scratch；再增加 GAMESS adapter。 |
| GPAW | 建议独立 conda 环境安装 GPAW/ASE/MPI，运行 `gpaw info`；并配置 PAW datasets。 |
| Wannier90 | 安装 `wannier90.x`/postw90，确认与 QE/DFT 接口一致，再增加输运 wrapper。 |
| Yambo | 安装 Yambo，并准备兼容 QE save database；增加独立 excited-state wrapper。 |
| ShengBTE | 从官方源码编译 MPI 版本，准备二/三阶力常数文件，再增加热输运 wrapper。 |
| HOOMD-blue | 按 CPU/GPU 和 CUDA 版本安装 `hoomd`，验证 Python import 后增加 MD wrapper。 |
| RMG-Py | 使用官方专用 conda 环境安装 RMG-Py/database；数据库路径和 solver 通过管理员配置。 |
| Arkane | 随 RMG-Py 安装，配置 ESS 输出和数据库；增加 Arkane thermochemistry wrapper。 |
| AutoMeKin | 从官方源码安装，配置依赖的量化程序和运行脚本；建议容器化。 |
| KinBot | 按官方仓库安装并配置 Gaussian/ORCA 等后端；增加 reaction-network adapter。 |
| MESMER | 从官方源码构建，验证 MESMER XML 样例后增加 master-equation wrapper。 |
| MESS | 审阅分发条件后从官方渠道获取，配置命令和输入模板；不要自动再分发。 |
| OpenMolcas | 从官方 GitLab 构建，设置 `MOLCAS`/scratch，跑官方最小样例后增加 wrapper。 |
| TheoDORE | 按官方文档安装 Python 包及依赖，准备受支持量化输出后增加分析 wrapper。 |
| SHARC | 注册并人工安装，设置 SHARC 路径及电子结构接口；不要自动下载。 |
| Newton-X | 从官方分发安装，配置量化接口与 scratch，再增加 surface-hopping wrapper。 |
| GNINA | 下载官方 binary 或使用官方容器，设置 `CHEMGRAPH_GNINA_COMMAND`。 |
| NequIP | `pip install nequip`，提供经过审查的模型 checkpoint；当前 `run_mlip` 仍需补模型加载 adapter。 |
| DeePMD-kit | 安装匹配 CPU/CUDA 的 `deepmd-kit`，提供冻结模型；再补 `run_mlip` adapter。 |
| FAIRChem/UMA | 安装 `fairchem-core`，确认模型条款并准备 checkpoint；避免工具调用时隐式下载。 |
| AIMNet2 | 按官方 AIMNet2 calculator 仓库安装，固定模型文件和校验和，再增加 adapter。 |
| NIST Chemistry WebBook/CCCBDB | 当前没有选择稳定且条款允许的通用 API；不要用脆弱网页抓取。 |
| gRASPA | 从官方 RASPA3/gRASPA 源码构建 `graspa`，配置 force-field 数据，再增加 GCMC wrapper。 |
| FDMNES/XANES | 从官方渠道人工安装 `fdmnes`，确认使用条款，准备最小 XANES 输入后增加 wrapper。 |
| Parsl | `pip install parsl`，配置本地/Slurm provider 和 executor；再连接 benchmark 调度层。 |

## 6. 许可证/商业软件的手动挂载

以下软件不会由项目自动下载。即使安装完成，也必须确保用户/机构拥有有效许可。

| 软件 | 手动配置要点 |
|---|---|
| Gaussian | 安装授权版本，设置 Gaussian profile/scratch；已有探测变量 `CHEMGRAPH_GAUSSIAN_COMMAND`，正式计算还需专用 wrapper。 |
| VASP | 挂载授权二进制和赝势，设置 `CHEMGRAPH_VASP_COMMAND=/path/vasp_std`；不要提交 POTCAR。 |
| Q-Chem | 安装授权版本并 source 官方环境，设置 `CHEMGRAPH_QCHEM_COMMAND=/path/qchem`。 |
| Molpro | 安装授权版本/许可证服务，设置 `CHEMGRAPH_MOLPRO_COMMAND=/path/molpro`。 |
| TURBOMOLE | 安装授权版本，配置 `TURBODIR`、`PATH`、许可证；当前需新增 adapter。 |
| AMBER 正式版 | AmberTools 已随环境依赖部分存在，但正式 AMBER/CUDA 需授权安装并配置 `AMBERHOME`。 |
| CHARMM | 安装授权 binary，配置拓扑/参数库和命令路径；需新增 adapter。 |
| AMS/ADF | 使用 SCM 官方安装器，配置许可证与 `AMSBIN`；需新增 adapter。 |
| CASTEP | 安装授权 binary、许可证和赝势库；需新增 periodic adapter。 |
| CRYSTAL | 安装授权版本、scratch 和 launcher；需新增 periodic adapter。 |
| WIEN2k | 安装授权版本，设置 `WIENROOT` 并运行 `siteconfig`；需新增 adapter。 |
| Schrödinger | 安装授权 suite，设置 `SCHRODINGER` 和许可证服务；只允许从管理员环境调用。 |
| OpenEye | 安装授权 toolkit，配置 `OE_LICENSE`；增加 Python adapter 前先确认许可证允许部署方式。 |
| EasySpin/Matlab | 安装 MATLAB 与 EasySpin，配置 MATLAB license 和 `MATLAB_ROOT`；需独立进程 adapter。 |
| LOBSTER | 从官方渠道获取并接受条款，配置 binary、basis 数据和许可证；需新增分析 wrapper。 |

## 7. 手动配置后的统一复测流程

以 CP2K 为例：

```bash
source chemistry_toolbox/scripts/activate_toolbox_env.sh
export CHEMGRAPH_CP2K_COMMAND=/absolute/path/to/cp2k

python - <<'PY'
from evaluation.mcp_tools.tools.check_backend_availability import (
    check_backend_availability_core,
)
print(check_backend_availability_core("CP2K"))
PY

python -m pytest -q   chemistry_toolbox/mcp/test_tools/test_run_cp2k.py
```

然后必须使用一个真实、最小、可收敛输入调用相应 core/MCP 工具，并确认：

1. 返回 `status=success`；
2. return code 为 0；
3. `stdout.log`/`stderr.log` 可审计；
4. 预期输出文件存在；
5. `_tool_trace.jsonl` 和 `_tool_results/` 已记录；
6. 再运行 `python chemistry_toolbox/scripts/verify_toolbox.py` 刷新状态文档。

如果软件只能在另一个 conda/module 环境运行，可以让 `CHEMGRAPH_*_COMMAND` 指向一个由
管理员编写的固定 wrapper 脚本。该脚本应只负责激活环境并 exec 固定程序，不能拼接或
eval Agent 提供的任意 shell 文本。
