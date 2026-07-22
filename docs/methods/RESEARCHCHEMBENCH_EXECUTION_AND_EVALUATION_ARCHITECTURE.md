# ResearchChemBench 代码运行机制、智能体调用、化学工具箱与评估方法详解

> 代码快照日期：2026-07-21  
> 分析对象：当前工作区中的 ResearchChemBench 代码，而不是某个历史发布版本  
> 重点范围：智能体调用方式、化学工具箱构建与执行方式、评估与评分方式  
> 说明：工作区存在未提交修改，因此本文记录的是阅读时的实际代码状态。若后续继续增删 Action、Backend 或运行环境，文中的数量应以运行时 catalog 为准。

## 目录

1. [核心结论](#1-核心结论)
2. [阅读范围与事实来源](#2-阅读范围与事实来源)
3. [系统总体架构](#3-系统总体架构)
4. [项目目录和模块职责](#4-项目目录和模块职责)
5. [配置加载与程序入口](#5-配置加载与程序入口)
6. [任务数据模型与 40 个 ChemGraph 任务](#6-任务数据模型与-40-个-chemgraph-任务)
7. [一次评测运行的完整生命周期](#7-一次评测运行的完整生命周期)
8. [四种智能体的具体调用方式](#8-四种智能体的具体调用方式)
9. [化学工具箱的总体设计原则](#9-化学工具箱的总体设计原则)
10. [Action、Backend 与 Catalog 的构建方式](#10-actionbackend-与-catalog-的构建方式)
11. [MCP 服务注册与工具调用协议](#11-mcp-服务注册与工具调用协议)
12. [一次化学 Action 的内部执行链](#12-一次化学-action-的内部执行链)
13. [后端运行时、Worker 与环境隔离](#13-后端运行时worker-与环境隔离)
14. [Artifact、科学资源和追踪系统](#14-artifact科学资源和追踪系统)
15. [外部数据源与 PubChem 网络调用](#15-外部数据源与-pubchem-网络调用)
16. [工具箱安装、锁定、迁移与验证](#16-工具箱安装锁定迁移与验证)
17. [评分与裁判机制](#17-评分与裁判机制)
18. [批量评测与 Web UI](#18-批量评测与-web-ui)
19. [测试体系与自动检查](#19-测试体系与自动检查)
20. [端到端示例](#20-端到端示例)
21. [关键问题、偏差与风险](#21-关键问题偏差与风险)
22. [推荐的运行和排障流程](#22-推荐的运行和排障流程)
23. [如何扩展项目](#23-如何扩展项目)
24. [附录 A：101 个公开 Action](#附录-a101-个公开-action)
25. [附录 B：76 个 Backend 的运行时分布](#附录-b76-个-backend-的运行时分布)
26. [附录 C：关键代码索引](#附录-c关键代码索引)

---

## 1. 核心结论

ResearchChemBench 不是一个把固定化学工作流包装成单个工具的基准，而是一个测试智能体能否自主组合原子化化学能力的运行框架。当前代码的主链可以概括为：

~~~text
公开任务描述
  → 为一次运行创建独立 workspace
  → 冻结当前完整工具 catalog 和后端健康状态
  → 启动 Codex / Claude / OpenCode / Mock 子进程
  → 向智能体暴露同一个完整 Chemistry MCP 服务
  → 智能体自主选择 Action、Backend、方法、参数和调用顺序
  → MCP 记录每次调用、结果、Artifact 和文件变化
  → 智能体写出 report/report.md
  → LLM judge 对比隐藏 ground truth、成功工具调用和最终报告
  → 输出二元分数 0/1 或裁判错误 None
~~~

当前代码最重要的事实如下。

| 项目 | 当前代码事实 |
|---|---:|
| 公开任务数 | 40 |
| 公开 MCP Action 数 | 101 |
| Scientific Action | 91 |
| Data Action | 10 |
| BackendSpec 数 | 76 |
| Action–Backend 组合数 | 236 |
| 公开 MCP 服务数 | 每次运行 1 个 |
| 依赖型运行时 profile | 25 |
| executable-only support environment | 10 |
| 注册科学资源 | 27 |
| Agent preset | mock、codex、claude、opencode |
| 评分 | LLM judge 二元 0/1 |
| 自动后端选择 | 禁止 |
| 自动 fallback | 禁止 |
| 按任务过滤工具 | 禁止；所有任务看到相同完整 catalog |

理解项目时应牢牢记住以下三个边界。

第一，智能体负责科学决策。框架不会替智能体挑选计算软件、理论方法、模型、势函数、温度、收敛阈值或替代后端。

第二，MCP Action 是科学语义接口，不是软件 runner。公开工具名是 <code>calculate_energy</code>、<code>optimize_geometry</code>、<code>derive_thermochemistry</code> 等，而不是旧 ChemGraph 中的 <code>run_ase</code> 或 <code>run_xtb</code>。

第三，运行完成、工具成功和评测通过是三种不同状态：

- Agent 进程退出码为 0 且生成非空报告，运行状态才是 completed。
- 某个 Action 返回 success 或 partial_success，才被视为成功工具调用。
- LLM judge 返回 score=1，才表示该任务评测通过。

这三个状态可以互相不一致。例如，Agent 可以成功退出并写报告，但报告答案错误，最终 score=0；也可以运行 completed，但 judge API 失败，score=None。

---

## 2. 阅读范围与事实来源

本文以可执行代码为第一事实来源，优先级如下：

1. Python、Shell、JSON、YAML 中的当前实现。
2. 当前静态 ActionSpec、BackendSpec、资源配置和 runtime 配置。
3. 测试代码对不变量的约束。
4. README 和 docs 中的文字说明。

项目内部分文档保留了旧架构信息，例如“5 个工具”“41 个工具”“40 Scientific + 5 Data”“按任务筛选工具”“多个 profile 分别提供不同 MCP 工具”等。这些说法与当前实现不一致。当前实现明确采用：

- 101 个公开原子 Action；
- 1 个完整 MCP server；
- profile 只做后端依赖隔离；
- 所有任务看到同一工具集合；
- 运行时不允许自动 fallback。

因此，本文凡涉及计数、调用链和配置语义，均以当前代码实测结果为准。主要事实来源包括：

- [evaluation/run_task.py](../../evaluation/run_task.py)
- [evaluation/score.py](../../evaluation/score.py)
- [evaluation/cli_eval.py](../../evaluation/cli_eval.py)
- [chemistry_toolbox/src/researchchem_toolbox/catalog.py](../../chemistry_toolbox/src/researchchem_toolbox/catalog.py)
- [chemistry_toolbox/src/researchchem_toolbox/service.py](../../chemistry_toolbox/src/researchchem_toolbox/service.py)
- [chemistry_toolbox/src/researchchem_toolbox/runtime.py](../../chemistry_toolbox/src/researchchem_toolbox/runtime.py)
- [chemistry_toolbox/mcp/registry.py](../../chemistry_toolbox/mcp/registry.py)
- [chemistry_toolbox/config/mcp_profiles.yaml](../../chemistry_toolbox/config/mcp_profiles.yaml)

---

## 3. 系统总体架构

### 3.1 分层视图

~~~text
┌──────────────────────────────────────────────────────────────────┐
│ 任务层                                                           │
│ tasks/ChemGraph_xxx/task_info.json                               │
│ tasks/ChemGraph_xxx/target_study/ground_truth.json               │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Benchmark Harness                                                │
│ evaluation/config.py                                             │
│ evaluation/run_task.py                                           │
│ evaluation/cli_eval.py / evaluation/server.py                    │
└──────────────────────────────┬───────────────────────────────────┘
                               │ 创建 workspace、prompt、MCP 配置
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ 外部 Agent CLI                                                   │
│ Codex / Claude Code / OpenCode / Mock                            │
│ 负责推理、选择工具、恢复失败、生成最终报告                       │
└──────────────────────────────┬───────────────────────────────────┘
                               │ stdio MCP
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ 统一 Chemistry MCP Server                                        │
│ chemistry_toolbox/mcp/server.py                                  │
│ 动态注册完整 101 Action                                           │
└──────────────────────────────┬───────────────────────────────────┘
                               │ ActionRequest
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Protocol-independent Toolbox Core                                │
│ ActionSpec + BackendSpec + service.execute_action                │
│ 参数校验、后端校验、Artifact 校验、健康检查                      │
└──────────────────────────────┬───────────────────────────────────┘
                               │ 精确选择一个 runtime
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Dependency-isolated Worker                                      │
│ runtime Python -m researchchem_toolbox.worker                    │
│ backends/<domain>.py 执行具体库或外部程序                        │
└──────────────────────────────┬───────────────────────────────────┘
                               │ ActionResult + files
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ 可审计运行产物                                                   │
│ _tool_trace.jsonl / _tool_results / _tool_artifacts              │
│ report/report.md / _meta.json                                    │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌──────────────────────────────────────────────────────────────────┐
│ Evaluation                                                       │
│ 隐藏 ground truth + 成功工具调用 + 最终报告 → LLM judge          │
│ _score.json / batch eval_report                                  │
└──────────────────────────────────────────────────────────────────┘
~~~

### 3.2 控制面与数据面

可以把项目拆成两个平面。

控制面负责：

- 发现任务；
- 生成运行目录；
- 构造智能体命令行；
- 配置 MCP server；
- 设置超时和停止信号；
- 管理批量并发；
- 调用裁判；
- 汇总结果。

主要代码在 evaluation 目录。

数据面负责：

- 暴露 101 个化学 Action；
- 校验 ActionRequest；
- 检查明确选择的 Backend；
- 在正确的隔离环境中运行科学代码；
- 传递 Artifact；
- 保存结构化结果和 provenance；
- 记录每次 MCP 调用。

主要代码在 chemistry_toolbox 目录。

---

## 4. 项目目录和模块职责

### 4.1 顶层目录

| 路径 | 作用 |
|---|---|
| evaluation/ | Benchmark harness、Agent adapter、评分、Web API |
| tasks/ | 40 个公开任务和隐藏 ground truth |
| eval_configs/ | 单次或批量评测 YAML |
| chemistry_toolbox/ | 完整化学工具箱源码、MCP transport、配置、测试和部署脚本 |
| scripts/ | 顶层评测启动和 ChemGraph 任务导入 |
| tests/ | Benchmark harness 的单元测试 |
| docs/ | 项目级说明 |
| workspaces/ | 运行时生成；单次和批量运行结果 |
| .toolbox_env/ | 核心开发、MCP server 与审计环境 |
| .tool_envs/ | 各科学后端隔离环境 |
| .software_cache/ | 外部程序、授权程序和本地软件资产 |
| .model_cache/ | MLIP 等模型权重 |
| download/ | 下载包、伪势、参数集等可迁移资产 |

### 4.2 evaluation 目录

| 文件 | 职责 |
|---|---|
| config.py | 路径、环境变量、Agent preset、judge 配置、统一 MCP server spec |
| task_schema.py | TaskInfo、GroundTruth 的 Pydantic schema |
| utils.py | 任务发现、ground truth 读取、run 发现、安全路径和文件树 |
| instructions_tmpl.py | 所有 Agent 共用的自主化学 prompt |
| run_task.py | workspace 构建、Agent 命令行、子进程、流式日志、完成判定 |
| cli_eval.py | 单任务和批量评测、并发、信号处理、结果汇总 |
| score.py | LLM judge prompt、调用、解析和 _score.json |
| trace.py | MCP trace 读取、成功调用归一化、过程指标 |
| server.py | Flask Web UI/API |
| mock_agent.py | 不调用 API 的 harness smoke agent |
| agents.json | mock、codex、claude、opencode preset |

### 4.3 chemistry_toolbox 目录

| 路径 | 职责 |
|---|---|
| src/researchchem_toolbox/actions/ | 按科学领域组织的静态 ActionSpec |
| src/researchchem_toolbox/backend_specs.py | 76 个 BackendSpec |
| src/researchchem_toolbox/models.py | ActionRequest、ActionResult、ArtifactRef 等公共契约 |
| src/researchchem_toolbox/catalog.py | catalog 校验、快照、hash、Agent 工具概览 |
| src/researchchem_toolbox/service.py | 单个 Action 的选择校验与 dispatch |
| src/researchchem_toolbox/runtime.py | runtime 健康探测和 Worker 子进程启动 |
| src/researchchem_toolbox/worker.py | 后端环境内 JSON stdin/stdout 边界 |
| src/researchchem_toolbox/backends/ | 各科学领域的具体实现 |
| src/researchchem_toolbox/artifacts.py | 语义 ArtifactRef 存储 |
| src/researchchem_toolbox/resources.py | 显式科学资源注册与解析 |
| src/researchchem_toolbox/proxy.py | PubChem 代理环境配置 |
| mcp/server.py | FastMCP server |
| mcp/registry.py | 将全部 ActionSpec 动态注册为 MCP tools |
| mcp/tracing.py | MCP 调用结果、trace、文件变化快照 |
| mcp/workspace.py | MCP 文件路径约束 |
| mcp/profiles.py | profile 配置读取和统一 server spec |
| config/mcp_profiles.yaml | 25+10 个后端 runtime 声明 |
| config/toolbox_resources.json | 27 个科学资源 |
| scripts/ | 安装、验证、probe、smoke、锁文件和迁移脚本 |
| tests/ | 工具箱契约、后端、资源、MCP、环境和回归测试 |

### 4.4 两个 Python 打包表面

项目顶层 [pyproject.toml](../../pyproject.toml) 是 Benchmark 的主要安装入口，提供：

- researchchembench → Web server；
- researchchembench-eval → CLI evaluator；
- researchchem-mcp-server → chemistry_toolbox.mcp.server。

chemistry_toolbox 目录还包含独立的 [chemistry_toolbox/pyproject.toml](../../chemistry_toolbox/pyproject.toml)，用于把工具箱作为独立 transport 包安装，并将 mcp 目录映射为 researchchem_mcp_tools 命名空间。

正常 benchmark run 使用顶层包和 <code>chemistry_toolbox.mcp.server</code>。独立 installer 使用的是另一个包命名空间。维护时需要同时验证这两个打包入口，避免一个入口更新而另一个入口滞后。

---

## 5. 配置加载与程序入口

### 5.1 环境变量加载顺序

[evaluation/config.py](../../evaluation/config.py) 在 import 时执行：

1. 定位 PROJECT_ROOT；
2. 用 python-dotenv 加载根目录 <code>config.local.env</code>，且 override=False；
3. 为兼容旧项目，再加载 <code>evaluation/.env</code>；
4. 读取环境变量覆盖任务目录、workspace 目录、ChemGraph 路径、超时、turn 数和模型配置；
5. 加载 <code>evaluation/agents.json</code>。

因为 override=False，已在 shell 中导出的变量优先于文件内容。

顶层 Shell 启动器 [scripts/run_agent_eval.sh](../../scripts/run_agent_eval.sh) 还会使用 shell 的 <code>source</code> 加载 <code>config.local.env</code>。这意味着该文件不仅是 dotenv 键值文件，也会按 Bash 脚本执行。它适合受信任的本地配置，不应加载来源不明的文件。

### 5.2 关键环境变量

| 变量 | 作用 |
|---|---|
| RESEARCHCHEMBENCH_TASKS_DIR | 覆盖 tasks 目录 |
| RESEARCHCHEMBENCH_WORKSPACES_DIR | 覆盖 run 输出根目录 |
| CHEMGRAPH_ROOT | sibling ChemGraph checkout |
| CHEMGRAPH_PYTHON | 历史兼容变量；当前统一 server spec 实际选择 core profile Python |
| RESEARCHCHEMBENCH_AGENT_TIMEOUT_SECONDS | Agent 进程总超时，默认 7200 秒 |
| RESEARCHCHEMBENCH_MAX_TURNS | 默认 200；当前主要传给 Claude adapter |
| RESEARCHCHEMBENCH_OPENCODE_MODEL | 默认 deepseek/deepseek-v4-flash |
| RESEARCHCHEMBENCH_OPENCODE_BASE_URL | OpenCode provider base URL |
| JUDGE_API_KEY / BASE / MODEL_NAME | LLM judge |
| OPENAI_API_KEY | OpenCode/OpenAI-compatible Agent credential |
| ANTHROPIC_API_KEY | Claude credential |
| RESEARCHCHEMBENCH_MCP_PROFILES | 仅验证安装/probe profile 名称，不改变公开工具 |
| RESEARCHCHEMBENCH_WORKSPACE | 每次运行传给 MCP 和 Worker 的 workspace |
| RESEARCHCHEMBENCH_RUN_ID | trace 中的运行 ID |

### 5.3 入口

| 命令 | 实际入口 |
|---|---|
| python -m evaluation | evaluation.server.main |
| researchchembench | evaluation.server.main |
| researchchembench-eval | evaluation.cli_eval.main |
| ./rchem-eval | evaluation.cli_eval.main |
| bash scripts/run_agent_eval.sh | 参数处理后 exec python -m evaluation.cli_eval |
| researchchem-mcp-server | chemistry_toolbox.mcp.server.main |

---

## 6. 任务数据模型与 40 个 ChemGraph 任务

### 6.1 任务目录结构

每个任务目录的设计是：

~~~text
tasks/ChemGraph_001/
├── task_info.json
├── data/
│   └── .gitkeep
└── target_study/
    └── ground_truth.json
~~~

公开给 Agent 的是 task_info 和复制到 workspace 的 data。target_study 不会被复制。

### 6.2 TaskInfo schema

TaskInfo 包含：

| 字段 | 含义 |
|---|---|
| task_id | ResearchChemBench 任务 ID |
| source_id | 原 ChemGraph 条目 ID |
| category | 任务类别 |
| task | 自然语言问题 |
| data | DataFile 列表 |

DataFile 包含 name、path、type、description。

当前 40 个任务的 data 均为空，因此当前评测主要是纯文本化学问题，没有额外输入文件。

### 6.3 GroundTruth schema

隐藏 ground truth 包含：

| 字段 | 含义 | 当前是否用于评分 |
|---|---|---|
| expected_tool_calls | 原 ChemGraph 预期调用链 | 是 |
| expected_result | 预期答案或结果对象 | 是 |
| expected_structured_output | 结构化目标字段 | 否 |

<code>expected_structured_output</code> 虽然被 schema 读取，但 [evaluation/score.py](../../evaluation/score.py) 没有把它放进 judge prompt，也没有做确定性比较。这是当前评分链的重要缺口。

### 6.4 任务导入

[scripts/import_chemgraph_tasks.py](../../scripts/import_chemgraph_tasks.py) 从 sibling ChemGraph 的 ground_truth.json 导入 list-format 数据，按原顺序生成 ChemGraph_001 到 ChemGraph_040。

导入逻辑：

1. 读取原列表；
2. 为每个条目创建 data 和 target_study；
3. query 写入 task_info.task；
4. answer.tool_calls 写入 expected_tool_calls；
5. answer.result 写入 expected_result；
6. answer.structured_output 写入 expected_structured_output；
7. 默认拒绝覆盖已有任务，只有 --force 会先删除重建。

### 6.5 当前 40 个任务的类别分布

| 类别 | 数量 | Task ID |
|---|---:|---|
| smiles_lookup | 4 | 001–004 |
| optimization_from_name | 4 | 005、010、016、019 |
| vibrations_from_name | 2 | 006、011 |
| thermochemistry_from_name | 4 | 007、012、017、020 |
| dipole_from_name | 2 | 008、013 |
| energy_from_name | 4 | 009、014、015、018 |
| optimization_from_smiles | 2 | 021、028 |
| vibrations_from_smiles | 2 | 022、029 |
| thermochemistry_from_smiles | 2 | 023、030 |
| dipole_from_smiles | 2 | 024、027 |
| energy_from_smiles | 2 | 025、026 |
| reaction_energy | 10 | 031–040 |

这些任务实际上形成三组能力测试：

1. 名称解析和 SMILES 查询；
2. 单分子结构生成与能量、优化、振动、热化学、偶极性质；
3. 多物种重复计算和反应计量算术。

### 6.6 隐藏参考与当前工具的代际差异

ground truth 是从旧 ChemGraph 工具链导入的。40 个任务中的旧调用名累计为：

| 旧工具名 | 出现次数 |
|---|---:|
| smiles_to_coordinate_file | 60 |
| run_ase | 60 |
| molecule_name_to_smiles | 54 |
| calculator | 10 |
| extract_output_json | 9 |

而当前 Agent 实际看到的是新原子 Action，例如：

- molecule_name_to_smiles 的语义通常由 resolve_chemical_identity 或 search_compounds 完成；
- smiles_to_coordinate_file 的语义通常由 generate_3d_structure 完成；
- run_ase 被拆分成 calculate_energy、optimize_geometry、calculate_hessian、derive_thermochemistry 等；
- calculator 没有对应公开算术工具，Agent 可以在推理或报告中完成算术；
- extract_output_json 通常不再需要，因为 ActionResult 已是结构化 JSON。

因此，当前 judge 必须做“旧工具链到新 Action 语义”的自然语言映射，而不是精确工具名匹配。这是整个评测最显著的兼容性风险，详见第 21 节。

---

## 7. 一次评测运行的完整生命周期

核心实现位于 [evaluation/run_task.py](../../evaluation/run_task.py) 的 TaskRunner。

### 7.1 创建 TaskRunner

构造参数包括：

- task_id；
- agent_key；
- 可选 workspace_root；
- timeout_seconds；
- max_turns。

run_id 的格式为：

~~~text
<task_id>_<agent_key>_<UTC年月日_时分秒>_<6位随机十六进制>
~~~

单次运行默认写入：

~~~text
workspaces/<run_id>/
~~~

批量运行写入：

~~~text
workspaces/cli_runs/<batch_id>/<run_id>/
~~~

### 7.2 构建 workspace

setup_workspace 执行：

1. 检查任务目录存在；
2. 使用 exist_ok=False 创建全新 workspace；
3. 只复制任务的 data，不复制 target_study；
4. 创建 code、outputs、report、report/images、tool_logs；
5. 创建 _tool_results 和 _tool_artifacts；
6. 将 data 中普通文件 chmod 为 0444；
7. 生成完整 catalog 健康快照；
8. 写 INSTRUCTIONS.md；
9. 写 Claude 的 .mcp.json；
10. 写 OpenCode 的 opencode.json；
11. 写状态为 ready 的 _meta.json。

workspace 的标准形态：

~~~text
<run_id>/
├── INSTRUCTIONS.md
├── .mcp.json
├── opencode.json
├── data/
├── code/
├── outputs/
├── report/
│   ├── report.md
│   └── images/
├── tool_logs/
├── _toolbox_catalog.json
├── _tool_results/
├── _tool_artifacts/
├── _agent_output.jsonl
├── _final_message.txt
├── _tool_trace.jsonl
├── _meta.json
└── _score.json
~~~

后五项并非每次都必然存在。例如没有评分时没有 _score.json；Agent 没有调用 MCP 时可能没有 _tool_trace.jsonl。

### 7.3 冻结 catalog

workspace 创建阶段调用：

~~~text
catalog_snapshot(include_health=True)
~~~

它会：

- 校验 Action/Backend 双向映射；
- probe 76 个 backend；
- 读取 27 个科学资源状态；
- 写出 actions、backends、health、resources；
- 计算 catalog_hash；
- 保存为 _toolbox_catalog.json。

随后 prompt 使用这个快照生成工具概览。MCP server 内部的 active_catalog_snapshot 也优先读取该文件，因此同一次运行的 provenance 使用冻结的 catalog，而不是执行中途重新生成另一套 catalog。

注意：hash 包含健康状态和资源状态，所以代码不变但本机环境变化时，catalog_hash 也可能变化。

### 7.4 构造统一 Prompt

[evaluation/instructions_tmpl.py](../../evaluation/instructions_tmpl.py) 对所有 Agent 使用同一模板。主要要求：

- Agent 是自主计算化学智能体；
- 不允许等待人类确认；
- 所有任务获得完整原子工具 catalog；
- Agent 自己决定调用顺序、分支、重复调用和停止条件；
- Scientific Action 必须显式 backend_id；
- composite backend 必须显式 component_backends；
- 方法、模型、温度、收敛和采样参数需按 schema 提供；
- 使用 ArtifactRef 串联步骤；
- 不得编造工具应返回的值；
- 失败后由 Agent 自己决定修参、换后端、换 Action 或停止；
- 不得访问隐藏 ground truth；
- 不得修改 data；
- 必须创建非空 report/report.md。

最终报告至少应写：

1. 直接答案和单位；
2. Action 顺序、Backend、方法和关键参数；
3. 中间结果；
4. 相关文件路径；
5. 反应任务的计量表达式和算术。

### 7.5 配置 MCP 环境

每个 server spec 会合并以下 per-run 环境：

| 变量 | 值 |
|---|---|
| RESEARCHCHEMBENCH_WORKSPACE | 当前 workspace 绝对路径 |
| RESEARCHCHEMBENCH_RUN_ID | 当前 run_id |
| PYTHONPATH | 项目根、ChemGraph src 和已有 PYTHONPATH |
| CHEMGRAPH_LOG_DIR | workspace/tool_logs |

公开 server spec 来自 chemistry_toolbox.mcp.profiles.public_server_spec。当前只返回一个 server，名称通常为 researchchem_toolbox，Python 来自 core profile，也就是 .toolbox_env/bin/python。

### 7.6 启动 Agent 子进程

运行前：

- build_agent_argv 生成参数数组；
- command_preview 把完整 prompt 替换成占位符，避免在 _meta.json 中重复记录超长 prompt；
- _meta.json 状态改为 running；
- 复制父进程环境；
- 删除 JUDGE_API_KEY；
- 加入 workspace/MCP 环境；
- 设置 PYTHONUNBUFFERED=1。

然后通过 subprocess.Popen 启动：

~~~text
stdin  = DEVNULL
stdout = PIPE
stderr = STDOUT
cwd    = workspace
shell  = False
~~~

shell=False 和参数数组避免了通过 shell 字符串拼接执行内置 adapter。

### 7.7 流式日志和超时

单独的 daemon reader thread 持续读取 Agent stdout，并放入 Queue。主线程每 0.2 秒：

- 从 Queue 取一行；
- 追加到 _agent_output.jsonl；
- 检查总运行时间；
- 检查进程是否结束。

如果超过 timeout_seconds：

1. termination 设为 timeout；
2. 调用 terminate；
3. 最多等 10 秒；
4. 仍未退出则 kill。

用户停止时 request_stop 同样调用 terminate，并把 termination 标记为 stopped。

### 7.8 完成判定

只有同时满足以下条件，run 才是 completed：

1. Agent 退出码为 0；
2. report/report.md 存在；
3. report/report.md 非空；
4. termination 等于 process_exit。

工具调用次数、工具调用是否成功、答案是否正确，都不参与这个 completed 判定。

结束后 _meta.json 记录：

- exit_code；
- termination；
- duration_seconds；
- 检测到的 model；
- report_exists；
- tool_call_count；
- successful_tool_calls；
- failed_tool_calls；
- tool_runtime_seconds；
- tools_used。

### 7.9 运行状态机

~~~text
不存在
  │ setup_workspace
  ▼
ready
  │ Popen
  ▼
running
  ├── exit=0 + 非空报告 + 正常退出 ──→ completed
  ├── timeout / stopped                ──→ failed
  ├── 非零退出                         ──→ failed
  ├── 无报告                           ──→ failed
  └── runner exception                 ──→ failed

completed
  │ 可选 score_workspace
  ├── judge score=1  → 评测通过
  ├── judge score=0  → 评测未通过
  └── judge error    → score=None
~~~

---

## 8. 四种智能体的具体调用方式

Agent preset 来自 [evaluation/agents.json](../../evaluation/agents.json)。

### 8.1 Mock

Mock 用当前 Python 运行：

~~~text
python -m evaluation.mock_agent
  --workspace <workspace>
  --prompt-file <INSTRUCTIONS.md>
~~~

它只用于验证 harness：

- 读取 prompt；
- 输出几个 JSON event；
- 写一份固定的 mock report；
- 不调用化学 MCP；
- 不验证科学正确性。

因此 quick_mock 只能说明 workspace、进程和报告链正常，不能说明工具箱后端或评分有效。

### 8.2 Codex CLI

Codex 命令的核心参数：

~~~text
codex exec
  --ignore-user-config
  --skip-git-repo-check
  -C <workspace>
  --sandbox workspace-write
  --json
  --output-last-message <_final_message.txt>
  ...MCP -c 配置...
  <完整 prompt>
~~~

对每个 MCP server，代码动态注入：

- command；
- args；
- required=true；
- startup_timeout_sec=60；
- tool_timeout_sec=3600；
- 全部 server environment。

特点：

- 忽略用户 Codex 配置，降低本机配置污染；
- workspace-write sandbox；
- 允许 Codex 自己使用其内置文件和 shell 能力；
- 没有把 max_turns 传给 Codex；
- 总体停止依赖外层 Agent process timeout。

### 8.3 Claude Code

Claude 命令：

~~~text
claude -p
  --strict-mcp-config
  --mcp-config <workspace/.mcp.json>
  --output-format stream-json
  --verbose
  --max-turns <N>
  --tools Read,Write,Edit
  --allowedTools Read,Write,Edit,mcp__researchchem_toolbox__*
  --permission-mode dontAsk
  --disable-slash-commands
  --no-session-persistence
  <完整 prompt>
~~~

特点：

- 使用 run-local 严格 MCP 配置；
- 明确只开放 Read、Write、Edit 和 chemistry MCP；
- 不开放 Bash 工具；
- max_turns 在四个 adapter 中只有这里真正作为 CLI 参数使用；
- 不持久化 session；
- dontAsk 符合无人值守评测。

### 8.4 OpenCode

OpenCode 命令：

~~~text
opencode run
  --pure
  --dir <workspace>
  --model <provider/model>
  --format json
  --dangerously-skip-permissions
  <完整 prompt>
~~~

workspace 内的 opencode.json 定义：

- provider 使用 @ai-sdk/openai-compatible；
- baseURL 来自环境配置；
- model 和 small_model；
- 本地 MCP server command；
- MCP environment；
- enabled=true。

配置文件不会写 API key。credential 通过进程环境传入。

特点：

- --pure 减少用户配置影响；
- 没有显式 turn cap；
- 使用 dangerously-skip-permissions，隔离强度低于理想容器；
- 总体依赖外层 timeout。

### 8.5 Adapter 差异对公平性的影响

| 维度 | Codex | Claude | OpenCode | Mock |
|---|---|---|---|---|
| MCP | 动态 CLI config | .mcp.json | opencode.json | 无 |
| 文件能力 | Agent 内置 | Read/Write/Edit | Agent 内置 | 固定脚本 |
| Shell | 有可能使用 | 未开放 Bash | 有可能使用 | 无 |
| 明确 turn cap | 无 | 有 | 无 | 不适用 |
| 进程总超时 | 有 | 有 | 有 | 有 |
| 用户配置隔离 | ignore-user-config | strict config | pure | 不适用 |
| 权限策略 | workspace-write | dontAsk | skip permissions | 不适用 |

因此，项目是 agent-agnostic adapter 框架，但当前各 Agent 的可用能力并不完全同构。尤其是：

- Claude 不开放 shell；
- Codex 和 OpenCode 可能用非 MCP 方法解决任务；
- max_turns 仅对 Claude 生效；
- OpenCode 权限最宽松。

如果目标是严格比较“化学 MCP 使用能力”，后续需要用统一容器、统一文件/网络策略和统一非 MCP 工具白名单进一步约束。

---

## 9. 化学工具箱的总体设计原则

### 9.1 原子 Action，而不是预制 Workflow

工具箱的公开接口按科学操作命名。一个 Action 应产生一个主要科学结果，例如：

- calculate_energy；
- calculate_forces；
- optimize_geometry；
- derive_vibrational_modes；
- derive_thermochemistry；
- calculate_rate_constants；
- calculate_periodic_stress。

系统刻意不公开：

- run_ase；
- run_xtb；
- run_cp2k；
- 自动执行整条任务的 workflow 工具；
- 根据任务类别自动选软件的 router。

这样，Agent 的能力体现在可观察的决策链上，而不是调用一个已经把答案流程编码好的工具。

### 9.2 科学语义与软件实现分离

ActionSpec 描述“要做什么”，BackendSpec 描述“由谁做、需要什么”。

例如 optimize_geometry 是一个科学 Action，可由多个 Backend 提供。Agent 必须：

1. 选择 optimize_geometry；
2. 选择明确 backend_id；
3. 若选 geometric 或 sella，再选择 calculator component；
4. 填写该 backend 需要的方法和收敛设置。

公开 Action 名不会因为底层从 XTB 换成 ORCA、MACE 或 PySCF 而改变。

### 9.3 Agent 显式选择、系统不兜底

Catalog 全局声明：

- 默认 exposure_policy = progressive_discovery；
- catalog_visibility_policy = complete_task_independent；
- full 兼容模式 exposure_policy = atomic_all；
- backend_selection_policy = per_action_explicit；
- scientific_resource_selection_policy = agent_explicit_no_default；
- automatic_fallback = false。

这意味着：

- Agent 选错 backend，返回 invalid 或 unsupported；
- Agent 选中未安装 backend，返回 unavailable；
- backend 执行失败，返回 failed；
- 系统不会静默换到另一个 backend；
- 系统不会替 Agent 选择伪势、参数集或模型 checkpoint。

### 9.4 不隐藏不可用后端

不可用 Backend 仍保留在同一完整 Catalog 中，并可通过 search_actions、inspect_action 和 inspect_backend 发现。渐进模式不再把全部 unavailable Backend 文本预先塞入 Agent prompt，但不会按任务或健康状态隐藏它们；只有 Agent 明确设置 available_only=true 时，才应用这个显式过滤条件。

优点是可审计；缺点是 Agent 可能浪费调用去尝试明确不可用的软件。项目把这种选择也视为待评估的智能体决策。

---

## 10. Action、Backend 与 Catalog 的构建方式

### 10.1 ActionSpec 的静态来源

ActionSpec 按九个科学领域拆分：

| 类别 | Action 数 | Action–Backend 对 | 不同 Backend 数 |
|---|---:|---:|---:|
| scientific_data_interchange | 3 | 3 | 2 |
| structure_and_system | 18 | 26 | 14 |
| cheminformatics | 6 | 6 | 1 |
| molecular_electronic | 16 | 80 | 22 |
| reaction_and_kinetics | 8 | 11 | 8 |
| molecular_dynamics | 23 | 40 | 12 |
| periodic_and_phonons | 16 | 58 | 14 |
| docking | 1 | 2 | 2 |
| data_sources | 10 | 10 | 5 |
| 合计 | 101 | 236 | 76 个全局 BackendSpec |

这些 tuple 在 [chemistry_toolbox/src/researchchem_toolbox/actions](../../chemistry_toolbox/src/researchchem_toolbox/actions) 中声明，并由 actions/__init__.py 拼接为单一 ACTION_SPECS。

ActionSpec 主要字段：

| 字段 | 作用 |
|---|---|
| id | MCP tool 名，必须 lower_snake_case |
| category | 后端 handler 模块路由依据 |
| description | Agent 可见说明 |
| primary_output | 主要结果的语义类型 |
| backend_ids | 可选 provider |
| required_inputs | Action 级必需输入键 |
| optional_inputs | 可选输入键 |
| input_description | 更详细的输入约定 |
| version | Action 版本 |
| data_action | 是否为外部数据 Action |
| requires_network | 是否需要网络 |
| selection_policy | provider 选择策略 |

ActionSpec.validate 强制：

- ID 合法；
- 公开 Action 不能以 run_ 开头；
- 至少一个 backend；
- data Action 必须使用 data-source policy；
- Scientific Action 不能使用 data-source policy；
- fixed/internal provider 只能有一个；
- 不得出现 auto；
- required/optional 输入不得重复。

### 10.2 当前 provider policy 分布

| Policy | 数量 | 语义 |
|---|---:|---|
| agent_backend_required | 81 | Agent 必须给 backend_id |
| fixed_source | 10 | Data Action 固定到命名数据源 |
| internal_deterministic | 10 | 固定确定性内部 provider |
| agent_components_required | 0 | 类型被模型支持，但当前没有 ActionSpec 直接使用 |
| agent_source_required | 0 | 类型被模型支持，但当前没有 ActionSpec 使用 |

需要注意，当前 composite 选择并不靠 ActionSpec 的 agent_components_required policy，而是靠具体 BackendSpec 的 required_component_roles。service.py 检测到所选 Backend 有 component 角色后，会把 selection_source 改为 agent_components。

### 10.3 10 个固定数据源 Action

所有 Data Action 都是 fixed_source：

| Action | 固定 source |
|---|---|
| search_compounds | pubchem |
| resolve_chemical_identity | pubchem |
| retrieve_compound_properties | pubchem |
| retrieve_compound_structure | pubchem |
| search_similar_compounds | pubchem |
| search_substructures | pubchem |
| search_protein_structures | rcsb_pdb |
| search_materials | materials_project |
| search_catalysis_records | catalysis_hub |
| lookup_nist_webbook_species | nist_webbook |

调用这些 Action 时不需要伪造 backend_id 或 source_id。若请求显式提供与固定 source 不一致的值，service 会返回 invalid_request。

### 10.4 10 个确定性内部 Action

当前 internal_deterministic Action：

- normalize_qcschema_molecule；
- validate_qcschema_record；
- parse_quantum_chemistry_output；
- rank_conformers_from_results；
- select_structure_subset；
- renumber_biomolecular_structure；
- normalize_pdb_records；
- derive_vibrational_modes；
- derive_ir_spectrum；
- derive_uv_vis_spectrum。

它们虽然仍有一个实现 BackendSpec，但 Agent 不需要提交 fake backend。若提交了不同 backend，同样会被拒绝。

### 10.5 BackendSpec

BackendSpec 主要描述：

- id、display_name、runtime；
- capabilities；
- Python modules；
- executables；
- 必需环境变量和 credential；
- Conda/Pip 安装信息；
- 外部科学数据；
- license class；
- method schema；
- 每个 Action 的 backend-specific required inputs；
- required method fields；
- required action settings；
- 枚举型 allowed values；
- composite component roles 和候选；
- 支持的 system type；
- validation level。

ActionSpec 与 BackendSpec 必须双向一致：

- Action 宣称支持 backend B，则 B.capabilities 必须包含该 Action；
- Backend 宣称支持 Action A，则 A.backend_ids 必须包含该 Backend。

catalog.validate_catalog 会在 server 注册和快照生成前检查该不变量。

### 10.6 Composite backend

当前有三种 backend/action 组合要求 calculator component：

| Action | 主 Backend | 必需角色 |
|---|---|---|
| optimize_geometry | geometric | calculator |
| optimize_geometry | sella | calculator |
| locate_transition_state | sella | calculator |

calculator 候选为：

- xtb；
- pyscf；
- tblite；
- gpaw；
- nwchem；
- orca；
- mace；
- chgnet；
- deepmd；
- ase_emt。

请求示意：

~~~json
{
  "backend_id": "geometric",
  "component_backends": {
    "calculator": "xtb"
  },
  "inputs": {
    "structure": {
      "artifact_id": "art_..."
    }
  },
  "method_spec": {
    "method": "gfn2-xtb"
  },
  "action_settings": {
    "max_steps": 200,
    "force_threshold_ev_per_angstrom": 0.02
  }
}
~~~

主 Backend 和 component 都会单独健康检查；任一不可用都会返回结构化 unavailable，不会自动换 calculator。

### 10.7 Catalog 快照

catalog_snapshot 的 schema_version 当前为 4，包含：

- 全局策略；
- 全部 ActionSpec；
- 全部 BackendSpec；
- 每个 Backend 的健康状态；
- 全部资源状态；
- canonical JSON 的 SHA-256 catalog_hash。

Catalog 的作用有三层：

1. 给 Agent 展示同一完整工具空间；
2. 给 MCP resource <code>researchchem://catalog</code> 提供机器可读信息；
3. 在每个 ActionResult provenance 中记录运行所依据的 catalog_hash。

### 10.8 Agent 工具概览

agent_toolbox_overview 生成长文本，内容包括：

- 完整工具策略；
- ActionRequest 公共字段；
- AtomicStructure 基本格式；
- ResourceRef 语法；
- 按类别列出的全部 Action；
- 每个 Action 的 provider 和 health；
- 注册资源及可用性；
- “不可用仍可见、失败后由 Agent 决策”的规则。

它刻意不包含：

- 任务类别到工具链的 recipe；
- 后端推荐排序；
- 自动 workflow；
- 隐藏 ground truth。

---

## 11. MCP 服务注册与工具调用协议

### 11.1 一个完整 server

[chemistry_toolbox/mcp/profiles.py](../../chemistry_toolbox/mcp/profiles.py) 的 public_server_spec 返回：

- server name；
- core runtime；
- .toolbox_env/bin/python；
- <code>python -m chemistry_toolbox.mcp.server --transport stdio</code>；
- core runtime environment；
- 默认的渐进发现/显式执行工具名；full 兼容模式则为排序后的全部 Action 名。

evaluation.config.chemistry_server_specs 始终返回只包含这个 spec 的列表。

RESEARCHCHEMBENCH_MCP_PROFILES 如果存在，只会调用 selected_profile_names 验证名称，既不会减少 server 数，也不会改变 Action 列表。

### 11.2 两种等价 Catalog 可见性的 MCP 表面

[chemistry_toolbox/mcp/registry.py](../../chemistry_toolbox/mcp/registry.py) 支持两种表面，但底层 ActionSpec 集合完全相同：

1. 默认 progressive：注册 list_action_domains、search_actions、inspect_action、inspect_backend、search_resources、inspect_resource 和 execute_action；
2. execute_action 接收显式 action_id 与原有 ActionRequest 字段；
3. 执行仍进入 execute_traced，并用真实 Action ID 写轨迹；
4. full 兼容模式仍为每个 ActionSpec 动态创建独立 MCP tool；
5. 两种模式最终都调用同一个 service.execute_action，不改变验证、Backend 选择或 provenance。

渐进搜索按稳定 ID 顺序返回 Catalog 事实，不做相关性排名、任务分类或候选推荐。

### 11.3 tool_config 的硬性策略

[chemistry_toolbox/mcp/tool_config.json](../../chemistry_toolbox/mcp/tool_config.json) 声明：

~~~json
{
  "schema_version": 4,
  "exposure_policy": "progressive_discovery",
  "full_catalog_compatibility_mode": true,
  "backend_selection_policy": "per_action_explicit",
  "automatic_fallback": false,
  "catalog_resource": "researchchem://catalog"
}
~~~

registry.configuration_errors 会拒绝：

- 非 progressive_discovery/atomic_all；
- 非 per_action_explicit；
- automatic_fallback=true；
- enabled_tools；
- disabled_tools。

这从配置层阻止重新引入按任务过滤工具。

### 11.4 FastMCP server 行为

[chemistry_toolbox/mcp/server.py](../../chemistry_toolbox/mcp/server.py)：

- progressive 默认使用仅含领域索引和发现协议的精简 instructions；
- progressive 注册目录发现、显式 Action 执行和原生/可编程执行原语；
- full 兼容模式使用 agent_toolbox_overview 并注册全部独立 Action；
- 注册 catalog resource；
- 默认 stdio transport；
- 可选 streamable_http；
- 启动时把 cwd 切到 workspace；
- 默认把 CHEMGRAPH_LOG_DIR 设为 workspace/tool_logs。

Benchmark Agent adapter 使用 stdio。streamable_http 是独立部署能力，不参与正常评分 run。

### 11.5 ActionRequest 公共协议

所有工具使用同一 Pydantic 请求 envelope：

| 字段 | 类型 | 含义 |
|---|---|---|
| backend_id | string/null | Scientific Action 的明确 backend |
| component_backends | object | composite role → backend |
| source_id | string/null | 多源 Data Action 的 source；当前无此类 Action |
| inputs | object | 结构、数值、网络查询、ArtifactRef 等 |
| method_spec | object | 理论、基组、模型、力场、charge model 等 |
| action_settings | object | 本 Action 的收敛、约束、温度、采样等 |
| resource_limits | object | walltime、memory、CPU、GPU 数 |

公共 ResourceLimits：

- walltime_seconds：1 到 172800，默认 1800；
- memory_mb：如提供，至少 128；
- cpu_cores：如提供，至少 1；
- gpu_count：如提供，至少 0。

目前 runtime.py 会把 cpu_cores 映射为多个线程环境变量；memory_mb 和 gpu_count 主要作为契约/provenance，并未形成通用 OS 级强制资源限制。

### 11.6 ActionResult 公共协议

状态枚举：

- success；
- partial_success；
- invalid_request；
- unsupported；
- unavailable；
- failed；
- timeout；
- cancelled。

返回 envelope 还包括：

- action 和 action_version；
- requested_backend 和实际 backend；
- backend_version；
- selection_source；
- result；
- input_artifacts；
- output_artifacts；
- warnings；
- provenance；
- error；
- retryable。

这种统一 envelope 让 Agent 可以通过状态和 error.code 决定下一步，而无需解析每个库完全不同的异常文本。

---

## 12. 一次化学 Action 的内部执行链

核心入口是 [chemistry_toolbox/src/researchchem_toolbox/service.py](../../chemistry_toolbox/src/researchchem_toolbox/service.py)。

### 12.1 完整顺序

~~~text
MCP tool invoke
  → tracing.execute_traced
  → service.execute_action
  → ActionRequest Pydantic 校验
  → provider policy 校验
  → Action/Backend 支持关系校验
  → Action required_inputs 校验
  → Backend required inputs/method/settings 校验
  → 枚举取值校验
  → component role 校验
  → ArtifactRef 规范化与校验
  → ResourceRef 收集
  → 主 Backend 和 component health probe
  → runtime.invoke_worker
  → worker.execute_local
  → domain backend module
  → ActionResult + semantic ArtifactRef
  → trace/result/file snapshot 持久化
  → MCP 返回 Agent
~~~

### 12.2 Provider policy 校验

service 首先根据 ActionSpec.selection_policy 决定 backend_id：

- fixed_source：强制使用唯一固定 source；
- internal_deterministic：强制唯一内部 provider；
- agent_source_required：要求 source_id；
- agent_backend_required：要求 backend_id；
- agent_components_required：要求 backend_id，并将 selection_source 标为 agent_components。

任何 backend_id=auto 会在 ActionRequest schema 阶段直接失败。

### 12.3 Action 级和 Backend 级校验

校验分两层是重要设计：

Action 级回答“这个科学操作通常需要什么”，例如结构输入。

Backend 级回答“这个实现额外要求什么”，例如：

- ORCA 需要 method、basis、charge、multiplicity；
- periodic backend 需要 k-point、cutoff、伪势；
- thermochemistry backend 需要温度、压力或频率数据；
- trajectory backend 需要 topology 与 trajectory；
- composite optimizer 需要 calculator role。

required fields 缺失时，Worker 不会被启动，避免昂贵后端在明显无效的请求上运行。

### 12.4 Allowed value 校验

BackendSpec 可以为 method_spec 或 action_settings 声明精确枚举。例如 fingerprint type、optimizer、record type 等。

service 使用 casefold 比较，但不替 Agent 自动纠正或挑选值。非法值返回 invalid_request。

### 12.5 ArtifactRef 规范化

inputs 中允许三种显式 Artifact 形式：

1. 完整 ArtifactRef；
2. 只有 artifact_id 的对象；
3. 形如 art_加32位十六进制的字符串。

service 在 Worker 启动前：

- 从 index 查找 compact ID；
- 展开为完整 immutable reference；
- 验证格式；
- 不自动读取并替换成另一个科学对象；
- 不做模糊匹配。

未知 Artifact 会以 invalid_artifact_reference 返回，且不会启动 backend。

### 12.6 健康检查

probe_all_backends 对主 Backend 和 component 执行：

- runtime Python 是否存在；
- Python module 是否可 import；
- executable 是否可解析；
- 必需环境变量是否存在；
- 以 _KEY 结尾的 credential 是否存在。

如果 component 不可用，返回 component_backend_unavailable。

如果主 Backend 不可用，返回 backend_unavailable，并在 error.health 中带诊断。

两种情况 automatic_fallback_count 都是 0。

### 12.7 Worker dispatch

只有通过全部前置校验，service 才构造：

~~~json
{
  "action_id": "...",
  "backend_id": "...",
  "request": {
    "...": "规范化后的 ActionRequest"
  }
}
~~~

然后把 payload 交给 runtime.invoke_worker。

### 12.8 成功后的 Artifact 注册

若 Worker 返回 success 或 partial_success：

1. 将 result 写为 JSON semantic Artifact；
2. semantic_type 使用 ActionSpec.primary_output；
3. parent_artifact_ids 来自输入 Artifact；
4. 注册 Worker 返回的 artifact_files；
5. 文件注册失败不会抹掉主结果，而是写 warning。

### 12.9 Provenance

最终 provenance 至少包含：

- catalog_hash；
- agent_selected_action；
- agent_selected_backend；
- agent_selected_method_spec；
- agent_selected_action_settings；
- agent_selected_resource_refs；
- agent_selected_component_backends；
- agent_selected_source_id；
- runtime_profile；
- dispatcher_executed_backend；
- automatic_fallback_count=0；
- Worker 追加的程序、命令、输入或解析信息。

---

## 13. 后端运行时、Worker 与环境隔离

### 13.1 为什么使用多环境

计算化学依赖存在大量冲突：

- Python 版本不同；
- NumPy、PyTorch、CUDA ABI 不同；
- Conda 与系统二进制混合；
- MPI 和 BLAS 版本不同；
- 授权软件需要独立路径；
- 模型框架依赖互斥。

因此，完整 MCP server 在 core 环境运行，但实际计算通过子进程转发到 BackendSpec.runtime 对应的 Python。

### 13.2 25 个 profile 与 10 个 support environment

配置位于 [chemistry_toolbox/config/mcp_profiles.yaml](../../chemistry_toolbox/config/mcp_profiles.yaml)。

profile：

- 包含 MCP/Worker Python 和科学依赖；
- 一般位于 .toolbox_env 或 .tool_envs；
- public_server.runtime 指向 core。

support_environment：

- 主要是 executable-only 或授权软件；
- 安装时不要求完整 MCP runtime layer；
- 仍必须覆盖其 BackendSpec；
- 运行时依然通过统一 Worker 边界调用。

profiles.py 强制：

- 每个 BackendSpec 恰好分配一次；
- runtime 名与 BackendSpec.runtime 完全一致；
- conda_name 唯一；
- public_server.runtime 必须是 profile；
- default_profiles 必须合法。

### 13.3 Runtime 环境构造

runtime_environment 为一个后端运行时设置：

- PATH：runtime/bin + 配置 path_entries + 原 PATH；
- LD_LIBRARY_PATH：runtime/lib + 配置项 + 原值；
- PYTHONPATH：工具箱 source + 项目根 + 原值；
- RESEARCHCHEM_BACKEND_RUNTIME；
- environment_variables；
- command_variables；
- 可选 XDG_CACHE_HOME 和项目 model cache。

相对路径会解析为项目根下的绝对路径。

### 13.4 Worker 子进程

invoke_worker 运行：

~~~text
<runtime_python> -m researchchem_toolbox.worker
~~~

协议：

- JSON 通过 stdin；
- JSON 通过 stdout 最后一行返回；
- cwd 固定为 PROJECT_ROOT；
- timeout 来自 ActionRequest.resource_limits.walltime_seconds；
- shell=False。

若 cpu_cores 存在，会同时设置：

- OMP_NUM_THREADS；
- MKL_NUM_THREADS；
- OPENBLAS_NUM_THREADS；
- NUMEXPR_NUM_THREADS；
- VECLIB_MAXIMUM_THREADS。

### 13.5 Worker 边界

worker.py：

1. 读取 stdin JSON；
2. 捕获 backend 代码写到 stdout/stderr 的文本；
3. 调用 backends.execute_local；
4. 捕获文本最多保留尾部到 provenance；
5. 任意未捕获异常转换为 structured failed；
6. traceback 截断到最后 8000 字符；
7. stdout 最终只打印一个 JSON 对象。

这一边界避免科学库的普通 print 污染 MCP transport。

### 13.6 领域 handler 路由

backends/__init__.py 用 Action category 路由：

| Category | Handler 模块 |
|---|---|
| scientific_data_interchange | interchange.py |
| structure_and_system | structure.py |
| cheminformatics | cheminformatics.py |
| molecular_electronic | electronic.py |
| reaction_and_kinetics | reaction.py |
| molecular_dynamics | dynamics.py |
| periodic_and_phonons | periodic.py |
| docking | docking.py |
| data_sources | data.py |

每个模块声明 ACTIONS 集合和 execute 函数。若 category 有模块但 Action 不在模块 ACTIONS 中，则返回 unsupported/handler_missing。

### 13.7 后端模块职责概览

| 模块 | 主要实现 |
|---|---|
| interchange.py | QCElemental normalize/validate、cclib 输出解析 |
| structure.py | RDKit/OpenBabel 3D、构象、PDB、晶体、溶剂化、参数化 |
| cheminformatics.py | descriptor、fingerprint、similarity、substructure、tautomer、stereo |
| electronic.py | ASE calculator、XTB、PySCF、NWChem、ORCA、Psi4、GPAW、振动/光谱/热化学等 |
| reaction.py | TS/IRC、Cantera、SciPy、CatMAP、RMG、MESS、MESMER |
| dynamics.py | OpenMM、GROMACS、LAMMPS、HOOMD、MDAnalysis、MDTraj、PLUMED、PyMBAR、alchemlyb |
| periodic.py | QE、CP2K、DFTB+、SIESTA、ABINIT、VASP、MLIP periodic、Phonopy、Phono3py、LOBSTER、ShengBTE |
| docking.py | Vina、GNINA |
| data.py | PubChem、RCSB、Materials Project、Catalysis-Hub、NIST WebBook |

模块中还存在 composite.py、quantum_legacy.py、licensed_md.py、mlip.py 等辅助实现，用于共享渲染、解析和外部程序调用逻辑。

### 13.8 无 fallback 的具体保证

系统中不存在“失败后循环其他 Backend”的 dispatcher。execute_action 只调用一次：

~~~text
invoke_worker(runtime=所选 Backend.runtime, payload=所选 Backend)
~~~

Agent 若要换 backend，必须再次发起新的 MCP 调用。新选择会形成新的 trace event，因此恢复策略是可观察、可评分的。

---

## 14. Artifact、科学资源和追踪系统

这里有两类容易混淆的 Artifact。

### 14.1 语义 ArtifactRef

[chemistry_toolbox/src/researchchem_toolbox/artifacts.py](../../chemistry_toolbox/src/researchchem_toolbox/artifacts.py) 管理 Action 之间传递的 typed reference。

ArtifactRef 字段：

| 字段 | 含义 |
|---|---|
| artifact_id | art_加 UUID hex |
| semantic_type | Structure、EnergyResult 等语义类型 |
| media_type | application/json 或文件类型 |
| sha256 | 内容 hash |
| path | workspace 相对路径 |
| producer_action | 生成它的 Action |
| producer_backend | 生成它的 Backend |
| parent_artifact_ids | 上游依赖 |

JSON result 保存到：

~~~text
_tool_artifacts/objects/art_<id>.json
~~~

索引追加到：

~~~text
_tool_artifacts/index.jsonl
~~~

加载 Artifact 时会重新计算 SHA-256，hash 不一致则拒绝。

### 14.2 Trace 文件变化快照

[chemistry_toolbox/mcp/tracing.py](../../chemistry_toolbox/mcp/tracing.py) 还会比较调用前后的 workspace 文件快照，把变化文件复制到：

~~~text
_tool_artifacts/<四位调用序号>/<原相对路径>
~~~

这类记录用于审计和重放，不是 Action 之间的语义输入。

两者区别：

| 维度 | Semantic ArtifactRef | Trace snapshot |
|---|---|---|
| 目的 | Action 链接 | 审计文件变化 |
| ID | art_xxx | 调用序号 |
| 有 semantic_type | 是 | 否 |
| 可作为下一 Action 输入 | 是 | 通常否 |
| 有 parent lineage | 是 | 否 |
| 目录 | _tool_artifacts/objects | _tool_artifacts/0001 等 |

### 14.3 MCP result 与 trace

每次调用会预留不重复的 sequence，并写：

~~~text
_tool_results/0001_<tool>.json
~~~

其中包含：

- Action status；
- MCP transport status；
- 完整 result；
- error。

同时向 _tool_trace.jsonl 追加：

- sequence；
- run_id；
- tool；
- arguments；
- Action status；
- transport_status；
- started_at；
- duration_seconds；
- result_path；
- 最长 2000 字符 result_preview；
- error；
- changed-file artifacts。

Action 返回 invalid/unavailable/failed 时，MCP transport 本身仍可能是 success。tracing 会把 recorded_status 改成 ActionResult.status，使评估能区分“传输正常但科学调用失败”。

### 14.4 Sequence 的持久性

sequence 使用 _tool_results/.sequence-XXXX 文件以 O_EXCL 原子创建。即使 MCP server 重启，也不会覆盖已有序号和结果文件。

### 14.5 文件快照限制

默认：

- 每次最多 1000 个变化文件；
- 单文件最多复制 100 MiB。

超过单文件大小时只记录原路径、大小和 hash，不复制内容。

可用环境变量调整：

- RESEARCHCHEM_MCP_MAX_ARTIFACT_FILES；
- RESEARCHCHEM_MCP_MAX_ARTIFACT_BYTES。

### 14.6 Workspace 路径约束

mcp/workspace.py 对 MCP 工具路径提供较强约束：

- 相对或绝对路径最终必须在 workspace 内；
- 路径链中不允许 symlink；
- 输出只允许写到 outputs、code、report、tool_logs；
- 保护 INSTRUCTIONS.md、_meta.json、_score.json、trace、MCP 配置等保留文件。

但这只约束 MCP 工具实现。Agent 自身的 Read/Write/Shell 能力是否受相同限制，取决于对应 Agent CLI 的 sandbox，因此项目整体仍不是 hardened sandbox。

### 14.7 显式科学资源

[chemistry_toolbox/config/toolbox_resources.json](../../chemistry_toolbox/config/toolbox_resources.json) 当前注册 27 个资源：

| Kind | 数量 |
|---|---:|
| model_checkpoint | 12 |
| variant_file_collection | 5 |
| element_file_collection | 4 |
| backend_executable | 3 |
| slater_koster_parameter_set | 2 |
| single_file_resource | 1 |

典型资源：

- QE SSSP efficiency/precision；
- SIESTA PseudoDojo PSML；
- ABINIT PSP8；
- DFTB 3ob 和 matsci；
- VASP POTCAR 变体集合；
- NequIP、Allegro、DeePMD checkpoint；
- ORCA、OpenMPI、GNINA runtime asset。

### 14.8 ResourceRef 语法

| Resource kind | 语法 |
|---|---|
| element_file_collection | resource://resource_id/Element |
| variant_file_collection | resource://resource_id/Variant |
| parameter set | resource://resource_id |
| model checkpoint | resource://resource_id |
| single file | resource://resource_id |

资源解析器只允许配置中登记的路径，不搜索 host、不选择默认 family、不替换缺失资源。

例如 VASP POTCAR 需要 Agent 明确选择每个元素的 variant；DeePMD 多任务模型还要求显式选择 branch。资源选择会进入 provenance。

---

## 15. 外部数据源与 PubChem 网络调用

### 15.1 网络 Action

10 个 Data Action 全部 requires_network=true。依赖：

- PubChem；
- RCSB PDB；
- Materials Project；
- Catalysis-Hub；
- NIST Chemistry WebBook。

Materials Project 还要求 MP_API_KEY。

### 15.2 通用重试策略

data.py 将以下状态视为 transient：

- 408；
- 425；
- 429；
- 500；
- 502；
- 503；
- 504。

同时重试 httpx timeout、transport error、TimeoutError、ConnectionError。

Action settings 可控制：

- max_retries：0 到 4；
- retry_backoff_seconds：0 到 30；
- timeout_seconds；
- 各接口的 max_records。

若响应有 Retry-After，优先使用，并限制到 0–60 秒；否则指数退避。

重试耗尽会返回：

- status=failed；
- code=remote_service_unavailable；
- retryable=true；
- attempts；
- status_code、Retry-After、x-throttling-control 等 diagnostics。

### 15.3 PubChem 速率控制

PubChem 默认最小请求间隔为 0.25 秒，低于官方 5 request/s 限制。

多个 Worker 通过一个 state 文件和 fcntl 锁协调请求时间。若受限环境无法写 state 文件，代码会跳过共享限速，但保留重试层。

### 15.4 PubChem 代理加载

[chemistry_toolbox/src/researchchem_toolbox/proxy.py](../../chemistry_toolbox/src/researchchem_toolbox/proxy.py) 在每个 PubChem backend dispatch 前执行。

优先级：

1. 当前进程已存在 HTTP_PROXY、HTTPS_PROXY、ALL_PROXY 或小写版本；
2. RESEARCHCHEMBENCH_PUBCHEM_PROXY_URL；
3. config.local.env 中的 RESEARCHCHEMBENCH_PUBCHEM_PROXY_URL；
4. 只有显式传入 config_path 的测试/调用场景才从文件读取通用代理变量。

已有 shell 代理环境始终优先，因此执行 proxy_on 后启动 benchmark 会自然继承代理。

可用变量：

- RESEARCHCHEMBENCH_PUBCHEM_PROXY_URL；
- RESEARCHCHEMBENCH_PUBCHEM_NO_PROXY；
- RESEARCHCHEMBENCH_PUBCHEM_PROXY_MODE。

MODE 为 0、false、no、off、disabled 时禁用本地自动加载。

函数只返回：

- enabled；
- source；
- 变量名列表。

它不会把代理 URL 放入诊断或 provenance，避免泄漏 credential。

### 15.5 PubChem 查询实现

当前实现不完全依赖 PubChemPy 默认的 urllib 行为。完整 compound JSON 使用 httpx 直接请求 PUG REST，以保留响应 header 和 Retry-After。

支持：

- name、CID、SMILES、InChI、InChIKey、formula 查询；
- identity resolution；
- 属性字段白名单；
- 2D/3D 结构；
- explicit/omit hydrogen policy；
- similarity；
- substructure。

所有记录数量均有上限，防止 Agent 发起无界下载。

### 15.6 连通性诊断脚本

[chemistry_toolbox/scripts/check_pubchem_connectivity.py](../../chemistry_toolbox/scripts/check_pubchem_connectivity.py) 分别测试：

1. DNS；
2. HTTPS homepage；
3. 直接 PUG REST GET；
4. PubChemPy name lookup。

输出还记录代理是否启用、来源和代理变量名，但不记录 URL。

---

## 16. 工具箱安装、锁定、迁移与验证

### 16.1 滚动安装路径

[chemistry_toolbox/scripts/setup_toolbox_env.sh](../../chemistry_toolbox/scripts/setup_toolbox_env.sh) 用于创建 .toolbox_env：

1. 查找 mamba 或 conda；
2. 根据 toolbox-conda.txt 建环境；
3. 安装 pip、setuptools、wheel；
4. 按 constraints 和 toolbox-pip.txt 安装依赖；
5. editable 安装项目和 test extra；
6. 配置 Conda 环境注册；
7. 运行核心测试；
8. 运行 MCP smoke；
9. 运行 verify_toolbox。

这个路径适合开发，但依赖 specification 可能随 channel 更新，不保证跨时间字节级复现。

### 16.2 分 profile 安装

[chemistry_toolbox/scripts/setup_mcp_profile_envs.py](../../chemistry_toolbox/scripts/setup_mcp_profile_envs.py)：

- 按 mcp_profiles.yaml 创建各 runtime；
- 逐个安装 conda_packages；
- profile 安装 common MCP pip layer；
- support environment 不安装完整 MCP layer；
- 逐个安装 pip_packages；
- 持续写 mcp_profile_status.json；
- 可 --continue-on-error；
- 最后运行 configure_mcp_conda_envs.py。

逐包安装便于定位失败，但也不是严格锁定安装。

### 16.3 平台锁文件

chemistry_toolbox/environment/locks/linux-64 下为每个环境保存：

- conda-explicit.txt；
- pip-requirements.txt；
- pip-lock.json；
- 顶层 manifest.json。

这些文件记录 exact Conda artifact、版本、build/hash、pip 分发和本地 editable 信息。

### 16.4 锁文件捕获

[chemistry_toolbox/scripts/capture_portable_toolbox_lock.py](../../chemistry_toolbox/scripts/capture_portable_toolbox_lock.py)：

- 合并 profiles、support environments 和 auxiliary environments；
- 去重共享 prefix；
- 捕获 Conda explicit lock；
- 只捕获实际由 pip 安装的 distribution；
- 识别本地 editable、file URL、direct URL；
- 标记不可迁移的本地 source；
- 记录资源与关键外部资产 checksum；
- 不把 credential、软件、模型或 license 文件复制进源码树。

### 16.5 可迁移 bootstrap

[chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.py](../../chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.py) 只依赖 Python 标准库，可在项目环境尚不存在时运行。

主要流程：

1. 选择当前 Conda subdir 对应 manifest；
2. 验证 lock 文件 SHA-256；
3. 验证平台和 CPU compatibility；
4. 可复制、链接或跳过 software/model/download asset roots；
5. 按 exact Conda lock 创建环境；
6. 安装 pip layer；
7. 验证 Conda exact inventory；
8. 验证 pip package version 和 pip check；
9. 运行资源与环境 post-configure；
10. 运行 catalog、toolbox 和可选 full smoke；
11. 写 bootstrap report。

它只允许管理 .toolbox_env 和 .tool_envs 前缀，避免误删其他路径。

### 16.6 外部与授权资产

以下内容不会由普通开源安装自动获得：

- Gaussian、ORCA、VASP 等授权或受限软件；
- 某些 MPI/runtime bundle；
- 大模型 checkpoint；
- 伪势和参数集合；
- Materials Project API key；
- 其他 license/account-gated 程序。

配置可以注册这些 Backend，但健康检查会在缺失时返回 unavailable。注册能力不等于本机可执行能力。

### 16.7 验证层级

项目提供多层验证：

| 层级 | 工具 |
|---|---|
| 静态 catalog | tool_manager validate、validate_catalog |
| MCP 注册 | check_mcp_tools.py |
| 无网络 smoke | check_mcp_tools.py --smoke |
| Toolbox 结构/安装 | verify_toolbox.py |
| Runtime 环境 | check_mcp_profile_envs.py |
| PubChem 网络 | check_pubchem_connectivity.py |
| Unit/regression | pytest |
| 完整后端矩阵 | action/backend audit 与 smoke scripts |

check_mcp_tools.py --smoke 会通过内存 FastMCP client 验证：

- 工具集合与 action_specs 完全相等；
- 若干原子调用可成功；
- trace 顺序正确；
- semantic Artifact index 被创建。

---

## 17. 评分与裁判机制

### 17.1 评分入口

评分由 [evaluation/score.py](../../evaluation/score.py) 的 score_workspace 完成。

输入 workspace 后依次检查：

1. _meta.json 存在；
2. meta 中有 task_id；
3. report/report.md 存在且非空；
4. 从 tasks/<task>/target_study/ground_truth.json 读取隐藏参考；
5. 读取 _tool_trace.jsonl；
6. 归一化成功工具调用；
7. 构造 judge prompt；
8. 调用 OpenAI-compatible chat completions；
9. 写 _score.json。

### 17.2 Judge 实际看到什么

Judge prompt 包含：

- Query；
- Expected tool calls；
- Expected result；
- Agent tool calls；
- Agent final report。

Judge 看不到：

- expected_structured_output；
- 完整 _agent_output.jsonl；
- 失败工具调用；
- _tool_results 中的完整结果；
- semantic Artifact 内容；
- changed-file snapshots；
- report 引用文件的真实内容；
- Backend health；
- 完整 provenance。

### 17.3 工具调用归一化

[evaluation/trace.py](../../evaluation/trace.py) 默认只保留 status 为：

- success；
- partial_success。

每个调用转换为：

~~~json
{
  "action_name": {
    "request": {
      "...": "参数"
    }
  }
}
~~~

invalid_request、unsupported、unavailable、failed、timeout、cancelled 都不会进入 actual_tool_calls，但仍计入 process_metrics.failed_tool_calls。

这意味着 judge 不知道 Agent 在成功前尝试过多少错误 Backend，也无法直接惩罚高成本失败链，只能从最终成功链和报告判断。

### 17.4 Judge 规则

系统 prompt 要求：

- 关键化学结果正确；
- 逻辑依赖链基本正确；
- 数值默认 5% 相对容差；
- 单位、calculator、模型/方法、driver、温度、分子、SMILES、计量数关键；
- 默认参数、额外无害调用、文件名和格式差异可接受；
- 若答案和可观察依赖链正确，可接受缺少某个调用；
- 错误结果、编造值、错误 calculator/driver/identity 或无意义失败应判 0。

裁判只能返回：

~~~json
{
  "score": 0,
  "rationale": "..."
}
~~~

或 score=1。

### 17.5 Judge API

要求：

- JUDGE_API_KEY；
- JUDGE_API_BASE；
- JUDGE_MODEL_NAME。

使用 OpenAI Python client：

- base_url 可配置；
- chat.completions.create；
- temperature=0；
- system + user 两条消息。

Agent 子进程环境会删除 JUDGE_API_KEY，从而避免 Agent 直接使用裁判 credential。JUDGE_API_BASE 和 JUDGE_MODEL_NAME 没有被删除，但没有 key 时通常不能调用 judge。

### 17.6 JSON 解析

_parse_judge_json：

- 去掉可选 Markdown fence；
- 先尝试完整 JSON；
- 失败时提取第一个大括号对象；
- 只有整数 1 被映射为 1，其他值均映射为 0；
- rationale 转为字符串。

### 17.7 Judge 失败

如果缺 credential、网络失败、API 错误或 JSON 无法解析：

- score=None；
- rationale 写 Judge evaluation failed；
- parse_error 记录异常类型；
- _score.json 仍会写入；
- result 同时带 error。

Judge 失败不会自动把任务判 0，这对区分“Agent 错误”和“评估基础设施错误”是合理的，但统计时必须单独报告未评分数。

### 17.8 _score.json 内容

包括：

- run_id；
- task_id；
- agent_key/name；
- query；
- expected_tool_calls；
- actual_tool_calls；
- expected_result；
- score；
- rationale；
- parse_error；
- process_metrics。

### 17.9 当前评分的三个层次

| 层次 | 判定位置 | 判定标准 |
|---|---|---|
| 进程完成 | run_task.py | exit 0 + 非空报告 |
| Action 成功 | trace.py | success 或 partial_success |
| 任务通过 | score.py | LLM judge score=1 |

批量分析时不应只看 completed 数，也不应只看 score 均值。建议同时报告：

- completed rate；
- judge coverage；
- pass rate among scored runs；
- tool failure rate；
- 平均成功/失败调用数；
- 平均工具运行时间；
- judge error rate。

---

## 18. 批量评测与 Web UI

### 18.1 YAML 配置

示例：

~~~yaml
name: full_chemgraph_40
agents:
  - codex
tasks: all
repeats: 1
max_concurrent_runs: 1
timeout_seconds: 7200
max_turns: 200
judge:
  enabled: true
~~~

resolve_specs 生成 tasks × agents × repeats 的笛卡尔积。

校验：

- Agent 必须在 agents.json；
- tasks=all 或合法任务列表；
- repeats 至少 1；
- max_concurrent_runs 至少 1。

### 18.2 批量目录

~~~text
workspaces/cli_runs/
└── batch_<UTC>_<6hex>/
    ├── <run_1>/
    ├── <run_2>/
    ├── eval_report.json
    └── eval_report.md
~~~

### 18.3 并发

cli_eval 使用 ThreadPoolExecutor。每个线程运行一个 TaskRunner，而真正的 Agent 和 chemistry Worker 都是子进程。

SIGINT handler 会对 active runner 调用 request_stop。

潜在共享资源：

- .model_cache；
- .software_cache；
- PubChem rate state；
- license server；
- GPU；
- 外部数据库限流；
- 系统 CPU/内存。

workspace 本身隔离，但这些全局资源不是按 run 隔离的。提高 max_concurrent_runs 前应检查软件许可、显存和外部 API 限额。

### 18.4 评分触发

只有：

- meta.status=completed；
- 未传 --no-score；
- judge.enabled=true；

才会自动评分。

如果 score_workspace 返回 error，batch row 中 score=None、score_error 有值。

### 18.5 Batch report

eval_report.json 保存：

- 原 config；
- summary；
- 每个 run row。

eval_report.md 保存简表。

summary 中：

- runs；
- completed；
- failed；
- scored；
- mean_score；
- pass_rate。

由于 score 是二元值，mean_score 与 pass_rate 当前数值相同。

CLI 最终退出码只取决于所有 run 是否 completed：

- 全部 completed → 0；
- 任一 run failed → 1。

它不要求所有 score=1，也不要求 judge 全部成功。因此自动化流水线若要以科学通过率作为 gate，需要另外读取 eval_report.json。

### 18.6 Dry run

--dry-run：

- 验证 YAML；
- 解析全部 RunSpec；
- 打印计划；
- 不创建 batch workspace；
- 不启动 Agent；
- 不评分。

### 18.7 Web UI

evaluation.server 是 Flask + CORS 的轻量 UI。

主要 API：

| Endpoint | 功能 |
|---|---|
| GET /api/config | Agent preset |
| GET /api/tasks | 按 category 列任务 |
| GET /api/tasks/<id>/info | 任务描述 |
| GET /api/tasks/<id>/files | 输入文件树 |
| GET /api/tasks/<id>/file | 输入文件 |
| GET /api/runs | 历史 run |
| POST /api/runs | 启动异步 run |
| POST /api/runs/<id>/stop | 停止 |
| GET /api/runs/<id>/meta | 状态 |
| GET /api/runs/<id>/output | Agent 输出 |
| GET /api/runs/<id>/trace | 工具 trace |
| GET /api/runs/<id>/stream | SSE 双流 |
| GET /api/runs/<id>/files | workspace 文件树 |
| GET /api/runs/<id>/file | 读取文件 |
| POST /api/runs/<id>/score | 手动评分 |
| DELETE /api/runs/<id> | 删除 run |

SSE 每 0.5 秒检查 Agent output、tool trace 和 meta。约每 20 秒发送 keepalive。

前端 app.js：

- 加载任务和 Agent；
- 启动/停止 run；
- 分栏显示 Agent stream 与 tool trace；
- 显示 workspace 文件；
- 手动调用 score；
- 显示最近 50 个 run。

### 18.8 Web UI 安全边界

server 默认：

- host=0.0.0.0；
- port=5000；
- CORS 全局启用；
- 无认证；
- 支持启动、停止、评分和删除 run。

因此它适合受信任内网或本机，不应未经反向代理认证直接暴露到公网。

---

## 19. 测试体系与自动检查

阅读时项目包含：

- 45 个 test_*.py 文件；
- 160 个以 test_ 开头的测试函数；
- 参数化测试会产生更多实际 case。

### 19.1 Harness 测试

顶层 tests 重点覆盖：

- 40 个任务 schema 与 ground truth；
- workspace 不复制 hidden target_study；
- Mock Agent 端到端；
- Codex/Claude/OpenCode argv；
- MCP 配置；
- Judge key 不暴露给 Agent；
- batch config、dry-run 和报告；
- judge 成功、失败和 score=None；
- run discovery 和安全路径。

### 19.2 Toolbox 契约测试

主要覆盖：

- 完整 catalog 数量和无 runner；
- Action/Backend 双向映射；
- 不允许 auto 和 fallback；
- 固定数据源；
- internal deterministic；
- composite component；
- compact ArtifactRef；
- workspace path 和 trace；
- MCP 注册完整性；
- profile 覆盖每个 Backend 一次；
- 资源显式选择；
- backend-specific method/settings 校验。

### 19.3 科学后端测试

测试覆盖 RDKit、XTB、PySCF、ORCA、GPAW、NWChem、OpenMolcas、Multiwfn、Critic2、OpenMM、MDAnalysis、MDTraj、PyMBAR、Phonopy、Phono3py、LOBSTER、RMG、MESS、MESMER、PubChem 等。

其中很多测试使用：

- 小型真实输入；
- monkeypatch 模拟外部程序输出；
- parser/renderer 回归；
- 未安装时的 structured unavailable；
- 请求无效时不启动 Worker。

### 19.4 CI

.github/workflows/tests.yml 在 Python 3.11：

1. pip install -e .[test]；
2. pytest -q。

CI 的普通 GitHub runner 不具备全部科学软件，因此 CI 更偏向 catalog、mock、纯 Python 和隔离测试，不等价于完整 76 Backend 实机验收。

### 19.5 审计状态文件

chemistry_toolbox/config 中存在 action/backend matrix、coverage、gap smoke、connectivity 等状态 JSON。这些是某次运行产物或审计快照，不应替代当前代码和重新执行验证。

特别是文档和审计文件中的 233 对组合，当前代码实测为 236 对，说明仓库正在继续演进。

---

## 20. 端到端示例

### 20.1 名称到 SMILES：ChemGraph_001

任务要求 sulfur dioxide 的 SMILES。

旧 ground truth：

~~~text
molecule_name_to_smiles("sulfur dioxide")
→ O=S=O
~~~

当前工具链更可能是：

~~~text
resolve_chemical_identity
  fixed source: pubchem
  query.identifier: sulfur dioxide
  query.namespace: name
  require_unique: true
→ ChemicalIdentity ArtifactRef
→ Agent 从 result 读取 canonical/isomeric SMILES
→ 写 report/report.md
~~~

这里不需要 backend_id，因为 PubChem Action 是 fixed_source。

### 20.2 名称到几何优化：ChemGraph_005

旧 ground truth：

~~~text
molecule_name_to_smiles
→ smiles_to_coordinate_file
→ run_ase(driver=opt, calculator=mace_mp, model=medium-mpa-0)
→ energy approximately -16.8158 eV
~~~

当前语义链可能是：

~~~text
resolve_chemical_identity
→ generate_3d_structure backend_id=rdkit
→ optimize_geometry backend_id=mace
→ 读取优化结构与最终能量
→ report
~~~

如果 Agent 选择 geometric：

~~~text
optimize_geometry
  backend_id=geometric
  component_backends.calculator=mace
~~~

这种链与旧 run_ase 的参数层级不同，因此 judge 需要理解方法和结果语义，而不能按 JSON 精确匹配。

### 20.3 热化学：ChemGraph_007

旧任务要求 carbon dioxide 在 800 K、GFN2-xTB 下的 Gibbs free energy。

合理的当前原子链可能是：

~~~text
resolve_chemical_identity
→ generate_3d_structure
→ optimize_geometry backend_id=tblite 或 xtb
→ calculate_hessian backend_id=tblite 或 xtb
→ derive_vibrational_modes
→ derive_thermochemistry backend_id=internal_thermochemistry 或 goodvibes
→ report Gibbs free energy、温度、单位和中间值
~~~

当前工具箱把旧 run_ase thermo 拆成多个可审计步骤，这更能评估 Agent 是否理解 Hessian、频率和热化学之间的依赖。

### 20.4 反应自由能：ChemGraph_031

旧 ground truth 对 CH4、O2、CO2、H2O 分别做 thermo，然后计算：

~~~text
G_rxn = G_CO2 + 2 G_H2O - G_CH4 - 2 G_O2
~~~

当前 Agent 应：

1. 对每个物种建立独立 Artifact 链；
2. 使用一致 Backend、模型和温度；
3. 避免覆盖同名输出文件；
4. 从每个 ActionResult 读取 Gibbs free energy；
5. 在 report 中明确写计量式和数值代入；
6. 给出最终单位。

框架没有公开 calculator Action，因此算术可以由 Agent 自己完成。Judge 依赖报告判断计量和 arithmetic 是否正确。

---

## 21. 关键问题、偏差与风险

### 21.1 旧 ground truth 与新 Action catalog 不同代

这是最大的问题。

Expected tool calls 使用旧的 molecule_name_to_smiles、run_ase 等；actual calls 使用 101 个新 Action，并且参数包在 request 下。

后果：

- Judge 必须做语义映射；
- 同一科学流程有多种合理原子分解；
- 合理的新链可能因模型不理解而被误判；
- 错误链也可能因最终答案接近而被放过；
- 无法做精确 deterministic call matching。

推荐：

1. 为 40 个任务重新制作 current_catalog_expected_plan；
2. 用“允许的语义依赖图”代替单一线性调用列表；
3. 同时保留 legacy ground truth 作为来源；
4. 明确每个任务允许的 Backend/方法替代范围。

### 21.2 expected_structured_output 未参与评分

GroundTruth 已提供 SMILES、scalar_answer、dipole、vibrational_answer 等结构字段，但 scorer 完全忽略。

推荐：

- 先做确定性结构字段提取与单位归一化；
- 对数值、SMILES、向量、频率列表、原子结构分别评分；
- LLM 仅评估过程合理性和无法结构化的解释。

### 21.3 Judge 看不到失败调用

normalized_tool_calls 默认 successful_only=True。

后果：

- 连续选错 Backend 后最终成功，与一次成功在 judge 中可能相同；
- 无法评价恢复效率；
- failed computation 的成本只能从 process_metrics 看，不能影响 score。

推荐增加 process score：

- invalid/unavailable/failed 次数；
- 重复调用；
- 工具运行时间；
- timeout；
- 网络重试；
- 是否读取中间 Artifact。

### 21.4 partial_success 被当作成功

trace.py 将 partial_success 和 success 等价纳入 actual calls。

但 partial_success 的定义是主要科学结果不完整。Judge 可能只看到调用存在，而未检查其 result 是否完整。

推荐：

- actual call 中保留 status；
- 将 result 的关键字段或 error/warnings 摘要交给 judge；
- 对依赖 partial result 得到的最终答案做额外验证。

### 21.5 Judge 不读取真实结果文件

Agent 可在报告中声称某个值来自 outputs 文件，但 judge 不检查该文件。

风险：

- 报告和 Artifact 不一致；
- 路径不存在；
- 数值被手工修改；
- 结构/单位丢失。

推荐：

- 从 semantic Artifact index 自动收集最终候选结果；
- 验证 report 中引用路径存在；
- 对关键 JSON/结构文件做 hash 和 schema 校验；
- 把可控摘要交给 judge。

### 21.6 二元评分过粗

当前只有 0/1：

- 无法区分答案正确但过程弱；
- 无法区分工具链正确但数值略超容差；
- 无法区分 identity、method、unit、result 各维度。

建议拆为：

- answer correctness；
- chemistry method correctness；
- dependency-chain correctness；
- parameter completeness；
- provenance/artifact integrity；
- efficiency；
- final report quality。

最终可再定义严格 pass gate。

### 21.7 5% 相对容差缺少单位系统

Judge prompt 只用自然语言说明 5%，没有 deterministic unit conversion，也没有 absolute tolerance。

问题：

- 接近 0 的量不稳定；
- eV、kJ/mol、kcal/mol 需模型自行转换；
- 向量、光谱和结构无法用单一相对容差；
- 不同软件/模型理论值不应一概使用 5%。

### 21.8 Agent completed 不代表科学有效

run_task 只检查退出码和报告。即使：

- 零次 MCP 调用；
- 所有工具都失败；
- 报告是编造的；

只要 Agent 退出 0 且报告非空，仍是 completed。

这适合作为基础设施状态，但 UI 和 batch report 应明确标注 completed 不是 passed。

### 21.9 Batch 退出码不以 score 为 gate

全任务 completed 即退出 0，即使全部 score=0 或 score=None。

CI/排行榜脚本若只看 shell exit code，会误认为评测成功。

### 21.10 Agent 权限与工具不对齐

- Codex 可能使用 shell；
- OpenCode 使用 skip permissions；
- Claude 不开放 Bash；
- Prompt 禁止访问 ground truth，但不是所有 Agent 都有同等硬隔离；
- data chmod 0444 不是同用户下不可逆的安全边界；
- target_study 未复制，但 host 路径仍存在。

项目 README 已说明它不是 hardened container sandbox。严格 benchmark 应在一次性容器中只挂载 workspace。

### 21.11 Catalog health 带来运行环境依赖

每次 setup 都 probe 全部 Backend 并把 health 写入 hash。

优点：

- 可重现本次选择空间；
- Agent 知道什么可用；
- provenance 明确。

问题：

- workspace setup 可能较慢；
- server 创建时还会生成自身 instructions 并再次 probe；
- 临时 credential、网络挂载或 executable 状态会改变 hash；
- 同一代码在不同机器不是同一 catalog hash。

如果想把“语义 catalog 版本”和“环境健康快照”分开比较，建议分别计算 schema_hash 与 health_snapshot_hash。

### 21.12 Profile 选项容易被误解

--mcp-profiles 的名字暗示它会改变公开工具，但当前只做名称验证。

帮助文本中也仍有“all 40 Scientific and 5 Data Actions”的旧计数，实际是 91+10。

推荐：

- 将参数重命名为 --validate-runtime-profiles；
- 或真正实现 preflight，并在 run 前失败；
- 修正所有旧计数；
- 删除无效兼容变量。

### 21.13 CHEMGRAPH_PYTHON 的当前语义弱化

Shell 支持 --chemgraph-python 并导出 CHEMGRAPH_PYTHON，但统一 MCP server spec 从 core profile 选择 Python，没有使用该变量启动 server。

保留该选项可能让使用者误以为它能控制当前 MCP Python。

### 21.14 文档漂移

项目中同时存在：

- 当前 README 的 1-server/atomic-all 架构；
- 旧 docs 中的 5/41 工具；
- Shell help 的 40+5；
- 旧 audit 的 233 pairs；
- 当前代码的 101 Action、236 pairs。

建议生成式文档全部由 catalog_snapshot 派生，人工文档只解释概念，不重复硬编码数量。

### 21.15 外部服务与授权软件的不确定性

评测结果可能受：

- PubChem 503/429；
- 代理；
- Materials Project key；
- license server；
- 软件版本；
- 模型下载；
- GPU/CUDA；
- MPI；
- 远端数据库更新；
- 本地资源缺失。

这类失败应和 Agent reasoning failure 分开统计。

### 21.16 并发资源冲突

多 run 虽有独立 workspace，但共享：

- GPU；
- CPU；
- 内存；
- model cache；
- software cache；
- 外部限流；
- license；
- 某些程序的全局 scratch/env。

大规模评测需要调度层按 BackendSpec 资源需求限流，而不是仅设置 ThreadPoolExecutor 数量。

### 21.17 Web UI 无认证

0.0.0.0 + CORS + 删除接口不适合公网。还应限制：

- 可运行 Agent；
- 可读文件；
- 单用户并发；
- workspace 总量；
- run 删除权限；
- score API 消耗。

### 21.18 config.local.env 被 shell source

便于 proxy_on、PATH 和复杂 shell 环境，但也意味着配置文件可执行任意 shell。复制模板后应限制文件权限，避免把未知内容放入该文件。

---

## 22. 推荐的运行和排障流程

### 22.1 第一次安装

开发安装：

~~~bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench
bash chemistry_toolbox/scripts/setup_toolbox_env.sh
.toolbox_env/bin/python chemistry_toolbox/scripts/setup_mcp_profile_envs.py --continue-on-error
cp config.local.env.example config.local.env
~~~

严格复现：

~~~bash
bash chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.sh +  --asset-source /path/to/existing/ResearchChemBench
~~~

### 22.2 先做结构验证

~~~bash
.toolbox_env/bin/python -m chemistry_toolbox.mcp.tool_manager validate
.toolbox_env/bin/python chemistry_toolbox/scripts/check_mcp_tools.py
.toolbox_env/bin/python chemistry_toolbox/scripts/verify_toolbox.py --no-write
~~~

### 22.3 再做本地 MCP smoke

~~~bash
.toolbox_env/bin/python chemistry_toolbox/scripts/check_mcp_tools.py --smoke
~~~

这一步失败时先不要启动真实 Agent。

### 22.4 检查运行时

~~~bash
.toolbox_env/bin/python chemistry_toolbox/scripts/check_mcp_profile_envs.py +  --no-write +  --timeout-seconds 600
~~~

若只需某些 runtime：

~~~bash
.toolbox_env/bin/python chemistry_toolbox/scripts/check_mcp_profile_envs.py +  --profiles core,services,quantum,mlip +  --no-write
~~~

### 22.5 检查 PubChem

若终端 proxy_on 后可用，可直接在同一 shell 运行：

~~~bash
proxy_on
.tool_envs/services/bin/python chemistry_toolbox/scripts/check_pubchem_connectivity.py +  --name water +  --cid 962 +  --timeout 20 +  --output chemistry_toolbox/config/pubchem_connectivity_status.json
~~~

也可在 config.local.env 设置专用变量：

~~~text
RESEARCHCHEMBENCH_PUBCHEM_PROXY_URL=http://127.0.0.1:PORT
RESEARCHCHEMBENCH_PUBCHEM_NO_PROXY=localhost,127.0.0.1
~~~

不要把带 credential 的代理 URL 写入受版本控制文件。

### 22.6 Harness smoke

~~~bash
bash scripts/run_agent_eval.sh +  --agent mock +  --task ChemGraph_001 +  --no-score
~~~

检查：

- workspace 被创建；
- _meta.json 最终 completed；
- report/report.md 非空；
- _agent_output.jsonl 有内容。

Mock 没有 tool trace 是正常的。

### 22.7 真实 Agent 无评分运行

~~~bash
bash scripts/run_agent_eval.sh +  --agent codex +  --task ChemGraph_001 +  --timeout-seconds 1800 +  --no-score
~~~

先无评分运行便于把 Agent/MCP 问题和 judge 问题分开。

### 22.8 评分

配置：

~~~text
JUDGE_API_KEY=...
JUDGE_API_BASE=...
JUDGE_MODEL_NAME=...
~~~

然后不传 --no-score。

已有 run 也可通过 Web API 手动 score，或在 Python 中调用 evaluation.score.score_workspace。

### 22.9 Batch dry-run

~~~bash
bash scripts/run_agent_eval.sh +  --config eval_configs/full.yaml +  --dry-run +  --no-score
~~~

### 22.10 小规模真实批量

先跑：

~~~bash
bash scripts/run_agent_eval.sh +  --config eval_configs/quick_codex.yaml
~~~

再扩展到 full.yaml。

### 22.11 一次失败 run 的检查顺序

1. _meta.json：看 termination、exit_code、report_exists；
2. _agent_output.jsonl：看 Agent CLI 错误；
3. _tool_trace.jsonl：看 Action status；
4. _tool_results/NNNN_tool.json：看完整 ActionResult；
5. error.health：看 runtime/module/executable/credential；
6. _toolbox_catalog.json：确认本次 frozen health；
7. _tool_artifacts/index.jsonl：确认 Artifact 链；
8. report/report.md：确认 Agent 最终使用了什么值；
9. _score.json：区分 score=0 与 judge error。

### 22.12 常见故障定位

| 现象 | 优先检查 |
|---|---|
| Agent 起不来 | agents.json executable、PATH、_agent_output |
| MCP server 起不来 | .toolbox_env、server command、startup timeout |
| Tool 显示 unavailable | Backend health、runtime Python、module/executable/key |
| invalid_request | BackendSpec required fields、Action description |
| Artifact 找不到 | _tool_artifacts/index.jsonl、artifact_id、hash |
| Tool timeout | resource_limits.walltime_seconds、外部程序日志 |
| Run failed 但工具成功 | Agent exit、report 是否生成 |
| Run completed 但 score 0 | ground truth、报告、成功调用链 |
| Run completed 但 score None | judge credential/API/JSON |
| PubChem 503 | proxy、Retry-After、rate state、connectivity probe |

---

## 23. 如何扩展项目

### 23.1 新增 Action

推荐流程：

1. 在对应 actions/<category>.py 添加 ActionSpec；
2. 选择明确 primary_output；
3. 定义 required/optional inputs；
4. 决定 selection policy；
5. 在至少一个 BackendSpec.capabilities 中加入；
6. 在 Action.backend_ids 中加入相同 Backend；
7. 在对应 backends/<domain>.py 的 ACTIONS 和 execute 中实现；
8. 返回 common.success/partial_success/failed 等结构；
9. 为 backend-specific 字段更新 BackendSpec；
10. 添加契约和真实/模拟后端测试；
11. 运行 validate_catalog 和 MCP smoke；
12. 重新生成 TOOL_CATALOG 和审计计数。

不得新增一个直接完成整个 benchmark task 的 workflow Action，否则会破坏评测目标。

### 23.2 新增 Backend

1. 在 backend_specs.py 新增 BackendSpec；
2. 添加到相应 Action.backend_ids；
3. 在 mcp_profiles.yaml 中恰好分配一个 runtime；
4. 声明 module、executable、env、credential 和 license；
5. 声明 method/input/settings contract；
6. 在 backend handler 实现；
7. 必要时注册科学资源；
8. 添加 health probe、parser/renderer 和 no-fallback 测试；
9. 更新 lock、asset manifest 和安装文档。

### 23.3 新增 Runtime

1. 在 mcp_profiles.yaml 的 profiles 或 support_environments 添加；
2. conda_name 必须唯一；
3. environment 路径应在受管理目录；
4. backends 必须非空；
5. BackendSpec.runtime 必须完全匹配；
6. 添加 conda/pip package、path、library、command variable；
7. 运行 profile coverage 测试；
8. 捕获 portable lock。

### 23.4 新增 Agent adapter

不要添加可执行 shell 字符串模板。推荐：

1. agents.json 添加结构化 preset；
2. run_task.build_agent_argv 增加明确 kind 分支；
3. 使用 argv 数组和 shell=False；
4. 创建 run-local MCP 配置；
5. 删除 judge credential；
6. 统一 cwd、workspace 和 stdout 格式；
7. 定义 turn/permission/sandbox；
8. 添加 argv、credential 和 end-to-end mock 测试。

### 23.5 新增任务

1. 创建 task_info.json；
2. 输入文件放 data；
3. ground truth 放 target_study；
4. 确保 task_id 与目录一致；
5. 使用当前 101 Action 语义定义 expected plan；
6. 尽量给出结构化目标；
7. 添加确定性 scorer；
8. 验证 Agent workspace 不包含 hidden reference。

### 23.6 改进评分的推荐架构

建议把 scorer 分成：

~~~text
Trace validator
  + Artifact/result extractor
  + Unit-aware deterministic answer scorer
  + Semantic dependency graph scorer
  + LLM report/process reviewer
  → 分项得分和最终 gate
~~~

这样 LLM 不再独自承担数值、单位、工具映射和过程判断。

---

## 附录 A：101 个公开 Action

### A.1 scientific_data_interchange，3

- normalize_qcschema_molecule
- validate_qcschema_record
- parse_quantum_chemistry_output

### A.2 structure_and_system，18

- standardize_structure
- generate_3d_structure
- generate_conformer_ensemble
- cluster_conformers
- align_molecular_structures
- repair_biomolecular_structure
- assign_protonation_states
- assign_partial_charges
- assign_force_field_parameters
- solvate_molecular_system
- analyze_crystal_symmetry
- standardize_crystal_structure
- build_supercell
- enumerate_surface_slabs
- rank_conformers_from_results
- select_structure_subset
- renumber_biomolecular_structure
- normalize_pdb_records

### A.3 cheminformatics，6

- calculate_molecular_descriptors
- calculate_molecular_fingerprint
- calculate_molecular_similarity
- search_local_substructures
- enumerate_tautomers
- enumerate_stereoisomers

### A.4 molecular_electronic，16

- calculate_energy
- calculate_forces
- calculate_hessian
- optimize_geometry
- calculate_dipole_moment
- calculate_atomic_charges
- calculate_orbitals
- calculate_bond_orders
- calculate_excited_states
- analyze_electron_density_topology
- calculate_atomic_basin_properties
- calculate_bader_charges
- derive_vibrational_modes
- derive_ir_spectrum
- derive_uv_vis_spectrum
- derive_thermochemistry

### A.5 reaction_and_kinetics，8

- locate_transition_state
- trace_intrinsic_reaction_coordinate
- calculate_chemical_equilibrium
- integrate_reaction_network
- calculate_rate_constants
- calculate_tunneling_correction
- solve_master_equation
- solve_microkinetic_model

### A.6 molecular_dynamics，23

- minimize_system_energy
- calculate_force_field_energy
- calculate_force_field_forces
- decompose_force_field_energy
- propagate_dynamics
- calculate_trajectory_rmsd
- calculate_radius_of_gyration
- calculate_radial_distribution
- calculate_mean_squared_displacement
- calculate_contacts
- calculate_solvent_accessible_surface
- calculate_dihedral_distribution
- calculate_hydrogen_bonds
- calculate_principal_components
- calculate_dynamic_cross_correlation
- assign_secondary_structure
- cluster_trajectory
- evaluate_collective_variables
- estimate_free_energy_difference
- estimate_thermodynamic_expectations
- calculate_potential_of_mean_force
- analyze_free_energy_convergence
- parse_alchemical_energy_data

### A.7 periodic_and_phonons，16

- calculate_periodic_energy
- calculate_periodic_forces
- calculate_periodic_stress
- relax_periodic_structure
- calculate_electronic_band_structure
- calculate_density_of_states
- calculate_projected_density_of_states
- analyze_periodic_bonding
- calculate_charge_spilling
- generate_displaced_supercells
- assemble_force_constants
- calculate_phonon_dispersion
- calculate_phonon_density_of_states
- calculate_harmonic_thermodynamics
- calculate_phonon_group_velocities
- calculate_lattice_thermal_conductivity

### A.8 docking，1

- dock_ligand

### A.9 data_sources，10

- search_compounds
- resolve_chemical_identity
- retrieve_compound_properties
- retrieve_compound_structure
- search_similar_compounds
- search_substructures
- search_protein_structures
- search_materials
- search_catalysis_records
- lookup_nist_webbook_species

---

## 附录 B：76 个 Backend 的运行时分布

### B.1 Profiles

| Runtime | 环境 | Backend |
|---|---|---|
| core | .toolbox_env | rdkit、rdkit_etkdg、rdkit_gasteiger、internal_statistics、ase_emt、internal_vibrations、internal_spectroscopy、internal_thermochemistry、pdb_tools |
| services | .tool_envs/services | pubchem、rcsb_pdb、materials_project、catalysis_hub、nist_webbook |
| workflows | .tool_envs/workflows | qcelemental、cclib、pymatgen、spglib、mdtraj |
| free_energy | .tool_envs/free_energy | pymbar、alchemlyb、hoomd |
| quantum | .tool_envs/quantum | openbabel、xtb、pyscf、tblite、orca |
| gpaw | .tool_envs/gpaw | gpaw |
| critic2 | .tool_envs/deepmd | critic2 |
| lobster | .tool_envs/lobster | lobster |
| shengbte | .tool_envs/deepmd | shengbte |
| openmolcas | .tool_envs/deepmd | openmolcas |
| multiwfn | .tool_envs/multiwfn | multiwfn |
| nwchem | .tool_envs/nwchem | nwchem、geometric |
| psi4 | .tool_envs/psi4 | psi4 |
| reaction | .tool_envs/reaction | crest、goodvibes、pysisyphus、cantera、scipy、catmap |
| qe | .tool_envs/qe | quantum_espresso |
| cp2k | .tool_envs/cp2k | cp2k |
| periodic | .tool_envs/periodic | dftbplus、siesta |
| phonons | .tool_envs/phonons | phonopy、phono3py |
| md | .tool_envs/md | pdbfixer、openmm_builder、packmol、openmm、gromacs、lammps、mdanalysis、plumed |
| openff | .tool_envs/openff | openff_am1bcc、openff |
| mlip | .tool_envs/mlip | mace、chgnet |
| nequip | .tool_envs/nequip | nequip、allegro |
| deepmd | .tool_envs/deepmd_models | deepmd |
| vasp | .tool_envs/vasp | vasp |
| docking | .tool_envs/docking | vina、gnina |

### B.2 Support environments

| Runtime | 环境 | Backend |
|---|---|---|
| abinit | .tool_envs/abinit | abinit |
| gaussian | .tool_envs/gaussian | gaussian |
| gamess | .tool_envs/gamess | gamess |
| rmg | .tool_envs/rmg | rmg |
| mess | .tool_envs/mess | mess |
| mesmer | .tool_envs/mesmer | mesmer |
| sella | .tool_envs/sella | sella |
| namd | .tool_envs/namd | namd |
| amber | .tool_envs/amber | amber_pmemd |
| charmm | .tool_envs/charmm | charmm |

### B.3 值得注意的共享环境

runtime 名和实际 prefix 不一定一一对应。例如 critic2、shengbte、openmolcas 当前都可指向 .tool_envs/deepmd。profile loader 按 runtime 语义验证 Backend 分配，但 portable lock capture 会按真实 prefix 去重。

---

## 附录 C：关键代码索引

### C.1 Benchmark harness

- [evaluation/config.py](../../evaluation/config.py)：路径与全局配置
- [evaluation/task_schema.py](../../evaluation/task_schema.py)：任务 schema
- [evaluation/utils.py](../../evaluation/utils.py)：任务/run 发现
- [evaluation/instructions_tmpl.py](../../evaluation/instructions_tmpl.py)：Agent prompt
- [evaluation/run_task.py](../../evaluation/run_task.py)：单 run 主链
- [evaluation/cli_eval.py](../../evaluation/cli_eval.py)：批量评测
- [evaluation/trace.py](../../evaluation/trace.py)：trace 归一化
- [evaluation/score.py](../../evaluation/score.py)：LLM judge
- [evaluation/server.py](../../evaluation/server.py)：Web API
- [scripts/run_agent_eval.sh](../../scripts/run_agent_eval.sh)：Shell 启动器
- [scripts/import_chemgraph_tasks.py](../../scripts/import_chemgraph_tasks.py)：任务导入

### C.2 Toolbox contracts and catalog

- [chemistry_toolbox/src/researchchem_toolbox/models.py](../../chemistry_toolbox/src/researchchem_toolbox/models.py)
- [chemistry_toolbox/src/researchchem_toolbox/actions](../../chemistry_toolbox/src/researchchem_toolbox/actions)
- [chemistry_toolbox/src/researchchem_toolbox/backend_specs.py](../../chemistry_toolbox/src/researchchem_toolbox/backend_specs.py)
- [chemistry_toolbox/src/researchchem_toolbox/catalog.py](../../chemistry_toolbox/src/researchchem_toolbox/catalog.py)
- [chemistry_toolbox/src/researchchem_toolbox/service.py](../../chemistry_toolbox/src/researchchem_toolbox/service.py)

### C.3 Execution

- [chemistry_toolbox/src/researchchem_toolbox/runtime.py](../../chemistry_toolbox/src/researchchem_toolbox/runtime.py)
- [chemistry_toolbox/src/researchchem_toolbox/worker.py](../../chemistry_toolbox/src/researchchem_toolbox/worker.py)
- [chemistry_toolbox/src/researchchem_toolbox/backends](../../chemistry_toolbox/src/researchchem_toolbox/backends)

### C.4 MCP and observability

- [chemistry_toolbox/mcp/server.py](../../chemistry_toolbox/mcp/server.py)
- [chemistry_toolbox/mcp/registry.py](../../chemistry_toolbox/mcp/registry.py)
- [chemistry_toolbox/mcp/profiles.py](../../chemistry_toolbox/mcp/profiles.py)
- [chemistry_toolbox/mcp/tracing.py](../../chemistry_toolbox/mcp/tracing.py)
- [chemistry_toolbox/mcp/workspace.py](../../chemistry_toolbox/mcp/workspace.py)
- [chemistry_toolbox/src/researchchem_toolbox/artifacts.py](../../chemistry_toolbox/src/researchchem_toolbox/artifacts.py)
- [chemistry_toolbox/src/researchchem_toolbox/resources.py](../../chemistry_toolbox/src/researchchem_toolbox/resources.py)

### C.5 Environment and reproducibility

- [chemistry_toolbox/config/mcp_profiles.yaml](../../chemistry_toolbox/config/mcp_profiles.yaml)
- [chemistry_toolbox/config/toolbox_resources.json](../../chemistry_toolbox/config/toolbox_resources.json)
- [chemistry_toolbox/scripts/setup_toolbox_env.sh](../../chemistry_toolbox/scripts/setup_toolbox_env.sh)
- [chemistry_toolbox/scripts/setup_mcp_profile_envs.py](../../chemistry_toolbox/scripts/setup_mcp_profile_envs.py)
- [chemistry_toolbox/scripts/capture_portable_toolbox_lock.py](../../chemistry_toolbox/scripts/capture_portable_toolbox_lock.py)
- [chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.py](../../chemistry_toolbox/scripts/bootstrap_chemistry_toolbox.py)
- [chemistry_toolbox/scripts/check_mcp_tools.py](../../chemistry_toolbox/scripts/check_mcp_tools.py)
- [chemistry_toolbox/scripts/check_mcp_profile_envs.py](../../chemistry_toolbox/scripts/check_mcp_profile_envs.py)
- [chemistry_toolbox/scripts/check_pubchem_connectivity.py](../../chemistry_toolbox/scripts/check_pubchem_connectivity.py)

---

## 总结

ResearchChemBench 当前已经形成了一个结构清晰的“Agent 决策层—统一 MCP 协议层—显式 Backend 执行层—可审计 Artifact/Trace 层—LLM Judge 层”体系。

其最强的设计点是：

- 所有任务共享完整工具空间；
- 科学 Action 与软件 Backend 解耦；
- 所有重要科学选择由 Agent 显式做出；
- 无自动 fallback；
- 多环境隔离复杂科学依赖；
- 每次运行冻结 catalog；
- 工具结果、文件和 provenance 可追踪。

当前最需要优先改进的不是工具箱执行链，而是评估层：

1. 将旧 ChemGraph ground truth 迁移到当前原子 Action 语义；
2. 使用 expected_structured_output；
3. 引入确定性、单位感知的答案评分；
4. 将失败调用、Artifact 和真实结果纳入过程评分；
5. 统一不同 Agent 的权限与资源边界；
6. 消除文档中的旧工具数量和旧架构描述。

完成这些改进后，该项目才能更可靠地区分“Agent 真的理解并正确组合了计算化学工具”与“Agent 只是在报告中给出了看似正确的最终答案”。
