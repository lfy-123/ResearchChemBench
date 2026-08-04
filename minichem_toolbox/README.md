# MiniChem Toolbox

MiniChem Toolbox 是面向 ARCHE Case1 类分子机理任务的小型化学工具箱。它以 Gaussian 为核心电子结构软件，同时提供结构准备、构象搜索、低成本量化计算、热化学、反应路径和结果分析能力。

工具箱通过 MCP 暴露三层接口：预定义 Action、原生软件命令、Agent 编写的 Python 分析程序。详细能力见 [TOOLBOX.md](TOOLBOX.md)。

## 目录结构

```text
minichem_toolbox/
├── README.md
├── TOOLBOX.md
├── environment.yml                 # Conda 环境的可复现声明
├── requirements.txt                # Conda 创建后安装的 pip 依赖
├── pyproject.toml
├── config/                         # 运行时、软件命令和能力配置
├── docs/software/                  # Agent 可检索的本地软件文档
├── scripts/                        # 安装、启动、验证和清单更新脚本
├── src/
│   ├── minichem_toolbox/           # Action、Backend 和执行核心
│   └── minichem_mcp_tools/         # MCP 工具、作业管理和软件检索
├── tests/
│   ├── harnesses/                  # Codex、Claude、OpenCode 隔离测试入口
│   └── test_*.py                   # 自动化测试
├── .envs/minichem/                 # 本机 Conda 环境，Git 忽略
├── .mini_software_cache/           # 原生软件缓存，软件文件 Git 忽略
└── .mini_model_cache/              # 本地模型缓存，模型文件 Git 忽略
```

`environment.yml` 位于项目根目录，因为它是应纳入版本管理的环境声明；`.envs/` 只保存由该声明创建出的本机环境。工具箱不再维护重复的 runtime pack。

## 创建环境

要求主机已有 `mamba`、`micromamba` 或 `conda`。在工具箱根目录执行：

```bash
bash scripts/bootstrap.sh
```

脚本会：

1. 根据根目录 `environment.yml` 创建 `.envs/minichem`；
2. 安装 `requirements.txt`；
3. 以 editable 方式安装本工具箱；
4. 运行基础环境和缓存检查。

手动复现的等价命令：

```bash
mamba env create -y -p .envs/minichem -f environment.yml
.envs/minichem/bin/python -m pip install -r requirements.txt
.envs/minichem/bin/python -m pip install --no-build-isolation --no-deps -e .
.envs/minichem/bin/python scripts/verify_minichem.py
```

已有环境时，`bootstrap.sh` 会复用 `.envs/minichem`。设置 `MINICHEM_PIP_OFFLINE=1` 可禁止 pip 访问网络，但此时所需 wheel 必须已在本机 pip 缓存中。

## 软件缓存

所有工具箱专用软件放在相对路径 `.mini_software_cache/`：

```text
.mini_software_cache/
├── gaussian/g16/install/g16/
├── gaussian/g16/scratch/
└── multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI/
```

Conda 环境提供 RDKit、Open Babel、xTB、CREST、cclib、QCElemental 等开源依赖。Gaussian 16 是商业授权软件，必须从已有合法安装中复制，工具箱不会下载或重新分发。Multiwfn 应从其官方发布包获取。

更新软件和模型哈希清单：

```bash
.envs/minichem/bin/python scripts/update_manifests.py
```

## 模型缓存

语义检索模型来自 Hugging Face：

```text
sentence-transformers/all-MiniLM-L6-v2
```

模型文件放在：

```text
.mini_model_cache/all-MiniLM-L6-v2/
```

可选下载命令：

```bash
export HF_ENDPOINT=https://hf-mirror.com
huggingface-cli download sentence-transformers/all-MiniLM-L6-v2 \
  --local-dir .mini_model_cache/all-MiniLM-L6-v2
```

没有该模型时，Action 和软件文档仍可使用词法检索；仅混合语义召回不可用。

## 启动 MCP

```bash
bash scripts/start_mcp.sh --transport stdio --discovery-mode progressive
```

脚本始终使用 `.envs/minichem/bin/python`，并从相对路径 `src/` 加载两个 Python 包。

验证服务和测试：

```bash
.envs/minichem/bin/python -m pytest tests -q
.envs/minichem/bin/python scripts/verify_minichem.py
.envs/minichem/bin/python -m minichem_mcp_tools.tool_manager validate
```

## Agent 接入

### Codex

在目标项目的 Codex MCP 配置中注册工具箱启动脚本，或直接运行隔离 harness：

```bash
bash tests/harnesses/run_codex.sh
```

Harness 会为每次运行创建独立工作区，并通过 Codex 的 `mcp_servers.minichem_toolbox` 配置启动 MCP。

### Claude Code

```bash
bash tests/harnesses/run_claude.sh
```

Harness 会生成独立 `.mcp.json`，只向 Claude 开放工作区文件工具和 `mcp__minichem_toolbox__*`。

### OpenCode

OpenCode 使用 OpenAI 兼容接口。先在不纳入 Git 的 `config.local.env` 中配置：

```bash
export OPENAI_API_KEY=<api-key>
export MINICHEM_AGENT_BASE_URL=<openai-compatible-base-url>
export MINICHEM_AGENT_MODEL=deepseek/deepseek-v4-flash
```

然后执行：

```bash
bash tests/harnesses/run_opencode.sh
```

Harness 会生成独立 `opencode.json` 和 MCP 启动器。

## 工作区隔离与记录

每次 harness 运行默认写入：

```text
tests/results/<cli>/<timestamp_pid>/
```

其中保存：

- `_sessions/chat.jsonl`：CLI 对话和事件流；
- `_sessions/*.stderr.log`：CLI 错误输出；
- `_tool_results/`：MCP 工具结果；
- `_tool_artifacts/`：工具调用输入和产物索引；
- `code/`、`data/`、`outputs/`、`report/`：该次任务的隔离工作区。

`tests/results/` 是运行产物，已被 Git 忽略，可随时删除。

## 迁移

推荐迁移整个 `minichem_toolbox/`，但不要依赖复制已有 `.envs/minichem`，因为 Conda 前缀可能包含机器路径。目标机器上应重新运行 `scripts/bootstrap.sh`。

需要单独确认：

1. `.mini_software_cache/` 中的授权软件可在目标机器合法使用；
2. 目标机器架构与缓存二进制兼容；
3. `.mini_model_cache/` 已复制，或允许重新下载；
4. Codex、Claude、OpenCode CLI 已在目标机器安装并完成各自认证。
