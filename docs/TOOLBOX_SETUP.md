# ResearchChemBench 化学工具箱环境配置

## 当前环境结构

ResearchChemBench 使用两层环境：

- `.toolbox_env`：核心 RDKit/ASE/ChemGraph 兼容工具和 benchmark 控制程序；
- `.tool_envs/<profile>`：量化、周期、MD、服务、反应、MLIP、对接等隔离环境。

这样可以避免 NumPy、MPI、BLAS、CUDA/PyTorch 和 C++ 运行库冲突。详细分类和原理见
[MCP_PROFILE_ENVIRONMENTS.md](MCP_PROFILE_ENVIRONMENTS.md)。

## 从头安装

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench

# 核心环境
bash chemistry_toolbox/scripts/setup_toolbox_env.sh

# 所有隔离 profile 和 ABINIT 支撑环境
.toolbox_env/bin/python chemistry_toolbox/scripts/setup_mcp_profile_envs.py --continue-on-error
```

安装脚本会自动注册 `researchchem-core`、`researchchem-quantum`、`researchchem-md` 等
17 个 Conda 名称（包括独立的 NequIP/Allegro、DeePMD 模型推理和 VASP runtime）。现有前缀只需补注册/修复运行库时执行：

```bash
.toolbox_env/bin/python chemistry_toolbox/scripts/configure_mcp_conda_envs.py
conda env list | grep researchchem
```

按名称进入环境：

```bash
conda activate researchchem-quantum
python -c 'from mace.calculators import mace_mp; print("MACE import OK")'
conda deactivate
```

断点续装是安全的；脚本会跳过已有环境并重新检查声明的包。常用参数：

```bash
.toolbox_env/bin/python chemistry_toolbox/scripts/setup_mcp_profile_envs.py --help

# 只装 MD
.toolbox_env/bin/python chemistry_toolbox/scripts/setup_mcp_profile_envs.py --profiles md

# 重建一个环境
.toolbox_env/bin/python chemistry_toolbox/scripts/setup_mcp_profile_envs.py \
  --profiles psi4 --recreate

# 周期调度和 ABINIT 支撑环境
.toolbox_env/bin/python chemistry_toolbox/scripts/setup_mcp_profile_envs.py \
  --profiles periodic --support-environments abinit
```

## 凭据

```bash
cp config.local.env.example config.local.env
```

把 API key 和本地软件命令写入根目录 `config.local.env`。该文件不会被版本控制，
`run_agent_eval.sh` 自动加载它。不要把真实值写入示例文件或文档。

## 验证

```bash
.toolbox_env/bin/python chemistry_toolbox/scripts/configure_toolbox_resources.py
.toolbox_env/bin/python chemistry_toolbox/scripts/run_scientific_resource_smokes.py

.toolbox_env/bin/python chemistry_toolbox/scripts/check_mcp_profile_envs.py \
  --live-materials-project \
  --check-models

.toolbox_env/bin/python -m pytest -q

.toolbox_env/bin/python chemistry_toolbox/scripts/run_mcp_profile_tool_tests.py \
  --warnings-as-errors
```

状态见 [MCP_PROFILE_STATUS.md](../chemistry_toolbox/docs/MCP_PROFILE_STATUS.md)。

## 人工许可软件与独立二进制

当前工作区已经完成以下配置：

- ORCA 6.1.1：`.software_cache/orca/6.1.1/`；稳定入口 `.tool_envs/quantum/bin/orca`；
- ORCA 专用 OpenMPI 4.1.8：`.software_cache/openmpi/4.1.8/`；稳定入口 `.tool_envs/quantum/bin/mpirun`；
- VASP 6.3.2：`.software_cache/vasp/6.3.2/`；稳定入口 `.tool_envs/vasp/bin/vasp_std`；
- RMG-Py 4.0.0 源码与数据库：`.software_cache/rmg/`；
- EasySpin 6.0.12 工具箱：`.software_cache/easyspin/6.0.12/`（仍需 MATLAB）；
- NequIP/Allegro 与 DeePMD checkpoint：分别位于 `.model_cache/nequip/0.1/`、`.model_cache/deepmd/pretrained/`；
- GNINA 1.3.3：`.software_cache/gnina/1.3.3/`；
- 周期软件赝势与 DFTB+ 参数集：由 `config/toolbox_resources.json` 注册；
- 当前 BackendSpec 49/49 available，注册资源 22/22 通过校验，真实资源计算 23/23 通过。

这些软件、模型、数据和安装包均被 Git 忽略。迁移到新机器时需重新提供有权使用的 ORCA、VASP、GNINA 文件及科学资源，再运行 `chemistry_toolbox/scripts/configure_toolbox_resources.py`；不要提交或重新分发受许可约束的软件、POTCAR 或模型文件。

VASP 的本机 GCC/OpenMPI 构建参数另存为 `config/vasp_makefile.include.gcc_openmpi`。重新提供合法源码后，将其复制为源码根目录的 `makefile.include`，在 `.tool_envs/vasp` 的编译器/MPI 环境中串行执行 `make std`；生产计算还必须另行提供有权使用的 PAW POTCAR 库。
