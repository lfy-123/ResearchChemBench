# MiniChem Toolbox

MiniChem 是面向 ARCHE Case1 类分子反应机理任务的小型计算化学工具箱。它以 Gaussian
为核心，保留构象搜索、低成本预筛选、过渡态与反应路径、频率与热化学、选择性分析、
量子化学输出解析和波函数分析能力，同时去掉材料模拟、分子动力学、对接和远程数据库等
与当前评估任务无关的部分。

MiniChem 与原来的 `chemistry_toolbox` 完全独立：它使用自己的 Conda 环境、软件缓存和
模型缓存，不会向 benchmark 主环境或原工具箱环境安装依赖。

详细的 Action、软件和三层接口说明见 [TOOLBOX.md](TOOLBOX.md)。

## 1. 目录结构

```text
minichem_toolbox/
├── .envs/
│   ├── environment.yml
│   ├── requirements-runtime.txt
│   ├── manifest.json
│   ├── minichem/                       # 专用 Conda 环境，Git 忽略
│   └── runtime_packs/minichem.tar.gz   # 可迁移环境包，Git 忽略
├── .mini_software_cache/
│   ├── gaussian/
│   ├── multiwfn/
│   └── manifest.json
├── .mini_model_cache/
│   ├── all-MiniLM-L6-v2/
│   └── manifest.json
├── config/                             # runtime、软件和 MCP 配置
├── mcp_tools/                          # 三层 MCP 接口的物理源码目录
├── native_software_docs/               # 原生软件本地使用文档
├── scripts/                            # 安装、启动、检查和打包脚本
├── src/minichem_toolbox/               # Action、backend 和执行核心
└── tests/harnesses/                    # Codex、Claude、OpenCode harness
```

其中只有一个物理 Conda 环境：

```text
.envs/minichem/
```

配置中的 `core`、`quantum`、`reaction`、`gaussian` 等名称只是逻辑 runtime 标签，全部
指向这个环境，不会重复安装八份依赖。

## 2. 环境要求

推荐运行平台：

- Linux x86-64；
- 可执行 `bash`；
- 有 runtime pack 时不要求预装 Conda；离线复用时需启用下述 pip 离线开关；
- 没有 runtime pack 时需要 `mamba`、`micromamba` 或 `conda`；
- Gaussian 需要合法许可证，MiniChem 不负责下载或分发 Gaussian。

## 3. 一键复现专用 Conda 环境

进入工具箱根目录：

```bash
cd minichem_toolbox
bash scripts/bootstrap.sh
```

脚本按以下顺序处理：

1. 如果 `.envs/minichem/bin/python` 已存在，直接复用；
2. 否则如果 `.envs/runtime_packs/minichem.tar.gz` 存在，解压并执行 `conda-unpack`；
3. 否则使用 `.envs/environment.yml` 创建 `.envs/minichem`；
4. 安装 `.envs/requirements-runtime.txt` 中的 pip 依赖；
5. 将当前 MiniChem 源码以 editable 方式安装进该环境；
6. 检查 37 个 Action 和 18 个 backend 的可用性。

默认 pip 索引为 PyPI。如需使用镜像：

```bash
export MINICHEM_PYPI_INDEX_URL=https://pypi.org/simple
bash scripts/bootstrap.sh
```

完整目录已包含 runtime pack，且目标机器不联网时：

```bash
export MINICHEM_PIP_OFFLINE=1
bash scripts/bootstrap.sh
```

离线模式使用环境中已有的软件包，不查询 pip 索引；如果 runtime pack 不完整，脚本会
明确失败，不会修改 benchmark 主环境。

也可以手工复现：

```bash
mamba env create -y -p .envs/minichem -f .envs/environment.yml
.envs/minichem/bin/python -m pip install \
  -r .envs/requirements-runtime.txt
.envs/minichem/bin/python -m pip install --no-build-isolation --no-deps -e .
.envs/minichem/bin/python scripts/verify_minichem.py
```

这个过程只写入 `.envs/minichem`，不会激活或修改 benchmark 主环境。

## 4. 环境验证与重新打包

检查 backend：

```bash
.envs/minichem/bin/python scripts/verify_minichem.py
```

检查 Action、runtime 和 MCP 配置：

```bash
.envs/minichem/bin/python -m minichem_mcp_tools.tool_manager validate
```

运行自动测试：

```bash
.envs/minichem/bin/python -m pytest tests -q
```

环境或缓存变化后重新生成清单：

```bash
.envs/minichem/bin/python scripts/generate_cache_manifests.py
```

重新生成可迁移环境包：

```bash
bash scripts/package_runtime.sh
```

生成结果为：

```text
.envs/runtime_packs/minichem.tar.gz
```

## 5. 软件与模型位置

Conda/Python 依赖位于：

```text
.envs/minichem/
```

不能通过 Conda 管理的原生软件位于：

```text
.mini_software_cache/gaussian/
.mini_software_cache/multiwfn/
```

可选语义检索模型为 `sentence-transformers/all-MiniLM-L6-v2`，来自 Hugging Face，位于：

```text
.mini_model_cache/all-MiniLM-L6-v2/
```

`deepseek-v4-flash` 等 Agent 模型通过 API 调用，不保存在工具箱中。

## 6. 启动 MCP 服务

stdio 模式：

```bash
bash scripts/start_mcp.sh \
  --transport stdio \
  --discovery-mode progressive
```

HTTP 模式：

```bash
bash scripts/start_mcp.sh \
  --transport streamable_http \
  --host 127.0.0.1 \
  --port 9010 \
  --discovery-mode progressive
```

默认工作目录是启动 MCP 的 Agent 项目目录。需要固定任务工作区时设置：

```bash
export MINICHEM_MCP_WORKSPACE=./agent_workspace
```

## 7. 接入 Codex

假设目标项目结构为：

```text
target_project/
└── minichem_toolbox/
```

在 `target_project` 下注册项目使用的 MCP：

```bash
codex mcp add minichem_toolbox -- \
  ./minichem_toolbox/scripts/start_mcp.sh \
  --transport stdio \
  --discovery-mode progressive
```

检查注册结果：

```bash
codex mcp list
```

也可以在 Codex 配置中手工添加：

```toml
[mcp_servers.minichem_toolbox]
command = "./minichem_toolbox/scripts/start_mcp.sh"
args = ["--transport", "stdio", "--discovery-mode", "progressive"]
startup_timeout_sec = 60
tool_timeout_sec = 3600
```

运行内置隔离测试：

```bash
cd minichem_toolbox
bash tests/harnesses/run_codex.sh
```

## 8. 接入 Claude Code

在目标项目根目录执行：

```bash
claude mcp add --scope project minichem_toolbox -- \
  ./minichem_toolbox/scripts/start_mcp.sh \
  --transport stdio \
  --discovery-mode progressive
```

检查 MCP：

```bash
claude mcp list
```

也可以在目标项目创建 `.mcp.json`：

```json
{
  "mcpServers": {
    "minichem_toolbox": {
      "type": "stdio",
      "command": "./minichem_toolbox/scripts/start_mcp.sh",
      "args": ["--transport", "stdio", "--discovery-mode", "progressive"],
      "env": {}
    }
  }
}
```

运行内置隔离测试：

```bash
cd minichem_toolbox
bash tests/harnesses/run_claude.sh
```

## 9. 接入 OpenCode

在目标项目的 `opencode.json` 中添加：

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "minichem_toolbox": {
      "type": "local",
      "command": [
        "./minichem_toolbox/scripts/start_mcp.sh",
        "--transport",
        "stdio",
        "--discovery-mode",
        "progressive"
      ],
      "environment": {},
      "timeout": 3600000,
      "enabled": true
    }
  }
}
```

运行内置 OpenCode 测试：

```bash
cd minichem_toolbox
export OPENAI_API_KEY=...
export MINICHEM_AGENT_MODEL=deepseek/deepseek-v4-flash
export MINICHEM_AGENT_BASE_URL=https://api.deepseek.com/v1
bash tests/harnesses/run_opencode.sh
```

## 10. Harness 隔离与聊天记录

三个 harness 每次都会创建独立目录：

```text
tests/results/<cli>/<UTC时间>_<进程号>/
```

其中保存：

- `INSTRUCTIONS.md`：测试 prompt；
- `_sessions/chat.jsonl`：聊天与工具事件流；
- `_sessions/*.stderr.log`：CLI 错误输出；
- `_sessions/*.db`：OpenCode 等 CLI 的会话状态；
- `_tool_trace.jsonl`：MCP 工具调用轨迹；
- `_tool_results/`：每次 MCP 调用的完整结果；
- `code/`：Agent 编写的 Gaussian 输入或 Python 程序；
- `outputs/`：Action、原生软件和 Python 作业结果；
- `report/`：Agent 最终报告。

不同 CLI、不同运行批次不会共享工作目录或聊天记录。

## 11. 迁移到其他项目

复制整个目录，不要只复制源码：

```bash
cp -a minichem_toolbox /path/to/target_project/
cd /path/to/target_project/minichem_toolbox
bash scripts/bootstrap.sh
```

需要一起迁移的关键目录为：

```text
.envs/
.mini_software_cache/
.mini_model_cache/
config/
mcp_tools/
src/
scripts/
native_software_docs/
```

Gaussian 的复制和使用必须符合许可证要求。对于不同操作系统或 CPU 架构，应使用
`.envs/environment.yml` 重新构建环境，而不是直接复用 Linux x86-64 runtime pack。
