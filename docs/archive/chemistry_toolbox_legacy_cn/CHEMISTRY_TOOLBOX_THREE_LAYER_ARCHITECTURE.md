# ResearchChem 三层化学工具箱架构

## 1. 为什么采用三层结构

开放式科研 benchmark 不能要求每篇论文先拥有一组完全匹配的预定义 Action。否则评估会退化为“开发者是否提前复现了论文流程”，而不是“智能体能否阅读任务、设计计算、选择软件、编写输入、执行和解释结果”。

另一方面，删除已有 Action 也会丢失稳定的输入校验、跨软件统一结果、轻量操作和已有测试。因此工具箱把三种能力作为并列入口：

| 层级 | 面向的任务 | 智能体负责 | 框架负责 |
|---|---|---|---|
| 1. 预定义 Action | 常见、稳定、值得统一的科学操作 | Action、backend、组件、数据源、方法、参数和调用顺序 | 契约校验、精确分派、统一结果和 Artifact |
| 2. 软件原生执行 | 软件已有能力但当前没有合适 Action | 软件、原生输入文件、命令、参数、文件映射、资源和结果解释 | 提供明确调用手册、白名单命令、隔离作业目录、执行状态和日志 |
| 3. 可编程分析 | 自定义预/后处理、论文特定算法、库组合和新分析 | 完整程序、运行环境、输入、资源、算法和解释 | 固定解释器、文件暂存、资源上限、异步运行、日志和产物哈希 |

三层不是固定流水线。智能体可以只用一层，也可以按任务需要任意交错。例如，先用 Data Action 获取记录，再写代码筛选，随后生成原生 CP2K 输入，最后用另一个 Action 解析通用结果。框架不会替智能体安排这个顺序。

## 2. 当前暴露规模

| 项目 | 数量 | 说明 |
|---|---:|---|
| 预定义 Actions | 101 | 91 个 Scientific Actions，10 个 Data Actions，全部保留 |
| BackendSpecs | 76 | Action 可选择的计算、程序库、内部算法或数据后端 |
| 开放执行 MCP 工具 | 13 | 软件发现、文件、原生作业、脚本作业、状态、收集、取消和 Artifact |
| 原生软件调用指南 | 56 | 覆盖 40 个声明 executable 的 BackendSpec，并纳入 16 个此前 runtime-only 的软件入口 |
| 原生命令说明 | 69 | 68 个策略允许；当前 66 个实际可执行；通用 `mpirun` 仅记录、不直接暴露 |
| 可编程 Python 运行环境 | 45 | 41 个当前具有 Python；每个环境列出模块、版本、命令和关联 backends |

软件清单还包含没有 BackendSpec 的已安装程序库或已记录软件。AiiDA/QCEngine、CENSO、Wannier90、Arkane、AutoMeKin、KinBot、SHARC、Newton-X、TheoDORE、Yambo、VMD 和 VESTA 等可以直接使用原生入口；atomate2、jobflow 等程序库可以通过 `workflows` Python 环境由智能体程序使用。它们都不需要为每个论文工作流预定义 Action。

## 3. MCP 工具分类

### 第一层：预定义 Action

101 个工具继续使用统一 `ActionRequest`：

- `backend_id`：智能体明确选择的主 backend；
- `component_backends`：复合计算中每个角色的明确 backend；
- `source_id`：多数据源 Action 的明确来源；
- `inputs`、`method_spec`、`action_settings`：科学输入、理论/模型和操作参数；
- `resource_limits`：机械资源边界。

Action 分派器只执行所提交的选择，不自动替换 backend 或参数。

### 第二层：软件发现与原生执行

| MCP 工具 | 作用 |
|---|---|
| `list_software` | 按名称、能力和可用性过滤完整软件/库/文档清单，不排序推荐 |
| `inspect_software` | 返回一个软件的版本、runtime、健康状态、Action 覆盖、模块、原生命令、调用格式、输入模式、文件、输出、本地文档和请求模板 |
| `search_software_documentation` | 在 `.software_cache/documentation` 的缓存文本和 HTML 中搜索版本相关说明 |
| `write_workspace_text` | 把智能体编写的输入 deck、配置或程序保存到 `code/` 或 `outputs/` |
| `read_workspace_text` | 读取指定 UTF-8 文件并返回哈希，支持检查输入和输出 |
| `validate_native_job` | 只检查命令白名单、路径、文件映射、stdin 和资源，不执行、不补科学参数 |
| `submit_native_job` | 使用精确 argv、`shell=false` 和独立目录提交后台作业 |
| `get_execution_job` | 查询状态及 stdout/stderr 尾部 |
| `collect_execution_job` | 终态后列出日志和输出的路径、大小和 SHA-256 |
| `cancel_execution_job` | 取消指定作业，不启动替代作业 |

机器可读调用手册位于 `chemistry_toolbox/config/native_software_guides.yaml`。命令必须由 `BackendSpec.executables` 或 `requested_software.yaml` 的 runtime/command 清单明确登记，否则 MCP 校验失败。它记录调用机制而不是论文流程。

一次 ORCA 原生调用的机械结构如下。输入文件内容完全由智能体根据任务和 ORCA 文档决定：

```json
{
  "request": {
    "software_id": "orca",
    "executable": "orca",
    "arguments": ["input.inp"],
    "staged_inputs": [
      {"source_path": "code/input.inp", "target_path": "input.inp"}
    ],
    "stdin_target": null,
    "resource_limits": {
      "walltime_seconds": 7200,
      "memory_mb": 8192,
      "cpu_cores": 8,
      "gpu_count": 0
    },
    "label": "agent-selected calculation"
  }
}
```

执行器不会检查或补写 ORCA 的泛函、基组、电荷、多重度、收敛或任务关键字。它只保证调用的是本地登记的 ORCA，而不是任意 shell 命令。

### 第三层：可编程科学分析

| MCP 工具 | 作用 |
|---|---|
| `list_analysis_runtimes` | 列出每个固定 Python、已探测模块/版本、命令和关联 backend |
| `submit_analysis_program` | 在智能体明确选择的 runtime 中运行一个已保存的 `.py` 文件 |
| `declare_scientific_artifact` | 为输出文件声明语义、媒体类型、生产者和父 Artifact，生成不可变 ArtifactRef |

脚本不能以内联 `python -c` 或 shell 字符串提交。完整代码必须先写入 workspace，因此 benchmark 可以检查代码本身、运行环境、参数、日志和输出。

```json
{
  "request": {
    "runtime": "workflows",
    "script_path": "code/analyze.py",
    "script_target": "analyze.py",
    "arguments": ["trajectory.xtc", "topology.pdb"],
    "staged_inputs": [
      {"source_path": "outputs/md/trajectory.xtc", "target_path": "trajectory.xtc"},
      {"source_path": "inputs/topology.pdb", "target_path": "topology.pdb"}
    ],
    "resource_limits": {
      "walltime_seconds": 1800,
      "memory_mb": 4096,
      "cpu_cores": 2,
      "gpu_count": 0
    }
  }
}
```

## 4. 作业状态与目录

每个原生或程序作业得到 `job_<uuid>`，并存放在：

```text
outputs/execution_jobs/<job_id>/
├── request.json          # 精确命令、runtime、资源和输入文件哈希
├── supervisor_spec.json  # 受信任监督器的机械执行记录
├── status.json           # queued/running/success/failed/timeout/cancelled
├── stdout.log
├── stderr.log
├── collection.json       # 收集后的输出清单
├── <staged inputs>
└── <program outputs>
```

作业由独立 supervisor 继续运行，MCP 提交调用可以很快返回。因此 OpenCode/MCP 的网络超时只需覆盖“提交/查询”，不需要设置成一小时。科学计算时长由 `resource_limits.walltime_seconds` 单独控制。

## 5. 自主性与约束边界

框架明确不做以下事情：

- 不根据任务检索或隐藏 Action；
- 不推荐或自动选择 software/backend/runtime；
- 不生成论文工作流；
- 不补方法、基组、势函数、温度、时间步长等科学参数；
- 不在失败后换软件、改参数或调用默认 callback；
- 不把第二层包装成软件特定的固定流程。

框架只实施可审计的机械边界：

- executable 必须同时存在于 BackendSpec 和调用手册；
- 原生程序使用 argv 且 `shell=false`；
- 工作文件必须显式映射，不允许 `..`、绝对 host 路径或 symlink 逃逸；
- CPU 线程、CPU affinity、walltime 和可选内存上限由 supervisor 实施；
- Agent 程序不会继承 MCP 进程的 API key、认证 token 或 SSH 环境；只保留 runtime 明确配置和有限的调度/设备/许可证变量；
- 已提交作业目录不能通过公开文本写入工具改写，防止命令、状态和 provenance 被覆盖；
- 运行命令、输入哈希、状态、日志、返回码、资源使用和输出哈希持久化；
- 无自动 fallback。

可编程层允许智能体编写通用代码，这本质上比结构化 Action 拥有更大权限。当前执行器提供进程、路径约定和资源限制，但不能作为恶意代码的完整安全边界。正式 benchmark 部署应把整个 MCP server 放在无特权容器、受限用户或批处理作业沙箱中，并按任务控制网络、挂载和 GPU。

## 6. 如何扩充工具箱

以后遇到论文中新操作时，不需要立即增加 Action：

1. 如果已有软件支持，智能体通过 `inspect_software` 获取准确调用方式，然后写原生输入并提交。
2. 如果是自定义分析或库组合，智能体在合适 runtime 写程序。
3. 只有当一种操作跨任务反复出现、输入输出语义稳定、值得统一校验和跨 backend 比较时，才把它提升为新的 Action。
4. 新安装一个命令行软件时，需要增加 runtime/BackendSpec executable 和原生调用指南；这扩充“可执行软件”，但不强制新增 Action。
5. 新增 Python 库时，只需把其固定版本加入适当 runtime 并刷新状态/锁；智能体即可在第三层调用。

这种演进方式让 Action catalog 保持清晰，同时不把开放科研能力限制在预定义动作集合内。

## 7. Benchmark 可评分信息

三层统一 trace 可以支持至少以下过程评分：

- 是否选择了与任务相符的 Action、软件和 runtime；
- 工具调用顺序和步骤依赖是否合理；
- 原生输入或程序是否包含关键科学参数；
- 是否检查程序状态和错误输出；
- 是否保留中间数据、命令、版本、资源和随机种子；
- Artifact 父子关系是否与实际计算依赖一致；
- 是否得到可复现的数值、结构、轨迹、谱图或结论；
- 是否出现无依据的 fallback、遗漏或结果误读。

评估器可以读取 `_tool_trace.jsonl`、`_tool_results/`、`outputs/execution_jobs/` 和 `_tool_artifacts/index.jsonl`，不需要依赖智能体在最终回答中自述过程。
