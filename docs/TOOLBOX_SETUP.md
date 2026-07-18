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
bash scripts/setup_toolbox_env.sh

# 所有隔离 profile 和 ABINIT 支撑环境
.toolbox_env/bin/python scripts/setup_mcp_profile_envs.py --continue-on-error
```

安装脚本会自动注册 `researchchem-core`、`researchchem-quantum`、`researchchem-md` 等
14 个 Conda 名称。现有前缀只需补注册/修复运行库时执行：

```bash
.toolbox_env/bin/python scripts/configure_mcp_conda_envs.py
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
.toolbox_env/bin/python scripts/setup_mcp_profile_envs.py --help

# 只装 MD
.toolbox_env/bin/python scripts/setup_mcp_profile_envs.py --profiles md

# 重建一个环境
.toolbox_env/bin/python scripts/setup_mcp_profile_envs.py \
  --profiles psi4 --recreate

# 周期调度和 ABINIT 支撑环境
.toolbox_env/bin/python scripts/setup_mcp_profile_envs.py \
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
.toolbox_env/bin/python scripts/check_mcp_profile_envs.py \
  --live-materials-project \
  --check-models

.toolbox_env/bin/python -m pytest -q

.toolbox_env/bin/python scripts/run_mcp_profile_tool_tests.py \
  --warnings-as-errors
```

状态见 [MCP_PROFILE_STATUS.md](MCP_PROFILE_STATUS.md)。

## 人工软件

当前自动环境覆盖所有已实现且可自动安装的必需后端。仍需人工处理：

- ORCA：注册/许可下载；
- GNINA：官方 binary 或 container；
- 各周期软件所需赝势与 DFTB+ 参数集；
- 任务特定模型、checkpoint、输入模板和集群 MPI 配置。
