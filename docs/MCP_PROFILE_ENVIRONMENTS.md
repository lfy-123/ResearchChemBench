# MCP 运行时与环境布局

ResearchChemBench 对所有任务只暴露一个完整 MCP server。运行时 profile 只负责依赖和命令隔离，不过滤 Action，也不代表科研工作流。

## 配置来源

| 文件 | 作用 |
|---|---|
| `chemistry_toolbox/config/mcp_profiles.yaml` | 50 个拥有 BackendSpec 的正式运行时 |
| `chemistry_toolbox/config/auxiliary_environments.yaml` | 7 个仅供原生命令或可编程层使用的辅助运行时 |
| `chemistry_toolbox/environment/environments.yaml` | 57 个运行时到 7 个 Conda 前缀的唯一映射 |
| `chemistry_toolbox/environment/*` | 可重建环境规格与 `linux-64` 精确锁 |

七个化学环境为：

```text
.envs/general-modern-openmpi5
.envs/molecular-simulation-openff
.envs/kinetics-legacy
.envs/equivariant-ml
.envs/periodic-mpich
.envs/yambo-openmpi4
.envs/gmx-mmpbsa
```

框架和评测入口使用 `.envs/researchchembench`。旧目录 `.toolbox_env`、`.tool_envs`、`.tool_envs_merged` 和 `.conda_envs` 不属于当前布局。

## 重建

在仓库根目录执行：

```bash
bash chemistry_toolbox/scripts/setup_toolbox_env.sh \
  --env-dir "$PWD/.envs/researchchembench" --from-lock --skip-verify

bash chemistry_toolbox/scripts/build_environments.sh --from-lock all
```

非 `linux-64` 平台去掉 `--from-lock`，从维护的 YAML 重新求解。KinBot 会固定到 2.2.2 的官方提交并自动应用仓库内补丁；`gmx_MMPBSA` 使用独立的 Python 3.11/AmberTools 23.6 环境。

需要整体迁移环境根目录时设置：

```bash
export RESEARCHCHEMBENCH_ENV_ROOT=/path/to/researchchem-envs
```

该变量对全部 57 个运行时生效。`.software_cache` 与 `.model_cache` 仍位于仓库根目录，分别保存原生软件/测试资产和模型权重；它们不能替代 `.envs`。

## 本地配置

```bash
cp config.local.env.example config.local.env
chmod 600 config.local.env
```

`config.local.env` 被 Git 忽略。Materials Project 和 Catalysis Hub 分别使用 `MP_API_KEY`、`CATALYSIS_HUB_API_KEY`；真实凭据不得写入 YAML、状态报告或提交记录。

## 验证

```bash
.envs/researchchembench/bin/python \
  chemistry_toolbox/scripts/check_mcp_profile_envs.py --check-models

.envs/general-modern-openmpi5/bin/python \
  chemistry_toolbox/scripts/check_mcp_tools.py --smoke

.envs/general-modern-openmpi5/bin/python \
  chemistry_toolbox/scripts/verify_toolbox.py --smoke
```

状态输出统一位于：

```text
chemistry_toolbox/docs/MCP_PROFILE_STATUS.md
chemistry_toolbox/docs/MCP_PROFILE_STATUS.json
chemistry_toolbox/docs/TOOLBOX_STATUS.md
chemistry_toolbox/docs/TOOLBOX_STATUS.json
```

持久化报告会把仓库绝对路径转成相对路径，避免携带生成服务器信息。
