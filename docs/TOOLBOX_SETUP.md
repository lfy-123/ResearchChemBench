# ResearchChemBench 环境重建

## 环境结构

项目只使用仓库根目录 `.envs/` 下的七个环境：

- `researchchembench`：评估框架、Agent 编排、测试和管理脚本；
- `general-modern-openmpi5`：通用化学、量化、材料分析和 MCP 服务；
- `molecular-simulation-openff`：OpenFF、OpenMM、GROMACS 和自由能分析；
- `kinetics-legacy`：RMG、Arkane、KinBot、Sella、ABINIT 和 LAMMPS；
- `equivariant-ml`：DeePMD、NequIP、Allegro 和 e3nn；
- `periodic-mpich`：CP2K 与独立 MPICH 运行栈；
- `yambo-openmpi4`：CatMAP、ASE 3.17 和 Yambo。

代码不支持 `.toolbox_env`、`.tool_envs`、`.tool_envs_merged` 或
`.conda_envs` 回退。

## Linux x86-64 精确重建

```bash
git clone git@github.com:lfy-123/ResearchChemBench.git
cd ResearchChemBench

export RCB_PIP_INDEX_URL=https://pypi.org/simple
export RCB_PIP_TRUSTED_HOST=pypi.org

bash chemistry_toolbox/scripts/setup_toolbox_env.sh \
  --from-lock --skip-verify
bash chemistry_toolbox/scripts/build_environments.sh \
  --from-lock all
```

主环境和六个工具环境分别使用已提交的显式 Conda 锁。pip 直接依赖和
VCS 依赖也在环境目录中固定版本。非 Linux x86-64 平台应去掉
`--from-lock`，使用维护的规格重新求解。

标准 `.envs/` 路径不需要环境变量。只有整体迁移七个环境时才设置：

```bash
export RESEARCHCHEMBENCH_ENV_ROOT=/data/ResearchChemBench-envs
```

## 凭据与外部资源

编辑占位符版本的 `config.local.env`，不要提交真实密钥：

```bash
chmod 600 config.local.env
${EDITOR:-vi} config.local.env
```

模型、赝势、原生软件和许可软件不进入 Git。迁移现有部署时，将
`.model_cache/` 和 `.software_cache/` 复制到仓库根目录，然后执行：

```bash
.envs/researchchembench/bin/python \
  chemistry_toolbox/scripts/configure_toolbox_resources.py --quick
```

## 验证

```bash
.envs/general-modern-openmpi5/bin/python \
  -m chemistry_toolbox.mcp.tool_manager validate
.envs/general-modern-openmpi5/bin/python \
  chemistry_toolbox/scripts/check_mcp_tools.py --smoke
.envs/researchchembench/bin/python -m pytest -q chemistry_toolbox/tests
bash scripts/run_agent_eval.sh --agent mock \
  --task Electron_Isodensity_Reproduction_01_Method_Selection --no-score
```

`kinetics-legacy` 的三个旧包平台元数据警告以及 `yambo-openmpi4` 的
ASE 3.17 元数据警告由构建脚本白名单处理；其他依赖错误会导致构建失败。
