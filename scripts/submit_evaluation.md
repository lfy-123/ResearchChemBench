# `submit_evaluation.sh` 使用说明

`scripts/submit_evaluation.sh` 用于提交一个或多个 ResearchChemBench 任务，支持前台运行或在 `tmux` 后台持续运行，并提供进度查看、日志跟踪、停止任务和结果汇总功能。

## 1. 超时机制

当前系统有三层超时。`submit_evaluation.sh` 只直接设置第一层，不会给每个化学 Action 写死同一个计算时限。

| 层级 | 控制对象 | 默认值 | 设置方式 |
|---|---|---:|---|
| 评测任务总超时 | 一个 Agent 完成一个任务的总运行时间 | 7200 秒 | `--timeout-seconds` |
| MCP 单次工具调用超时 | Agent 等待一次 MCP 工具调用返回的最长时间 | 7,500,000 毫秒，即 7500 秒 | 环境变量 `RESEARCHCHEMBENCH_MCP_TOOL_TIMEOUT_MS` |
| Action/后端计算超时 | ORCA、Gaussian、CREST、分析程序等单次科学计算的 walltime | 通常为 1800 秒；部分周期体系后端通常为 7200 秒 | Agent 调用 Action 时传入 `resource_limits.walltime_seconds` |

### 1.1 评测任务总超时

例如：

```bash
bash scripts/submit_evaluation.sh submit \
  --timeout-seconds 10800 \
  Electron_Isodensity_Reproduction_04_Blind_Prediction
```

这里的 `10800` 表示 Agent 最多可以为该任务运行 3 小时，包括推理、工具调用、读取结果和撰写答案的全部时间。

如果一次提交包含多个任务，`--timeout-seconds` 分别应用于每个任务，不是整个批次共用 10800 秒。

### 1.2 MCP 单次工具调用超时

所有 MCP 工具调用都有客户端等待上限，当前默认值为 7500 秒。这个值略大于工具箱中常见的 7200 秒同步计算上限，避免后端已经正常计算、客户端却提前断开。

脚本暂未提供单独的命令行参数；如需调整，可以在提交命令前设置环境变量：

```bash
RESEARCHCHEMBENCH_MCP_TOOL_TIMEOUT_MS=9000000 \
bash scripts/submit_evaluation.sh submit \
  --timeout-seconds 10800 \
  Task_A
```

也可以将其写入项目根目录的 `config.local.env`：

```dotenv
RESEARCHCHEMBENCH_MCP_TOOL_TIMEOUT_MS=9000000
```

该超时是 MCP 客户端的统一通信上限，不是不同化学 Action 的计算参数。

### 1.3 Action 和后端自身的计算超时

涉及真实科学计算的 Action 通常暴露：

```json
{
  "resource_limits": {
    "cpu_cores": 16,
    "memory_mb": 32000,
    "walltime_seconds": 3600
  }
}
```

其中 `walltime_seconds` 是该次后端计算的实际运行上限。通用默认值为 1800 秒，允许的全局模型范围为 1–172800 秒，但每个 backend 还可以设置更小的最大值；请求超过该 backend 的能力上限时，工具箱会拒绝请求并返回明确错误。

不同工具可能使用不同形式的超时：

- 电子结构、反应路径、构象搜索和原生程序作业：通常使用 `resource_limits.walltime_seconds`。
- 数据库或 HTTP 请求类 Action：通常使用 `action_settings.timeout_seconds`，常见默认值为 30 秒。
- 部分结构转换程序：使用自己的 `action_settings.timeout_seconds`，默认值可能为 600 秒。
- 查询目录、读取状态等快速 MCP 工具没有独立科学计算 walltime，但仍受 MCP 单次调用超时约束。

因此，“每个工具都有超时保护”，但不是由 `submit_evaluation.sh` 为所有工具统一设置。Agent 应根据 Action 目录暴露的参数和 backend 约束，为具体计算选择 walltime、CPU 和内存。

### 1.4 三层超时的优先关系

最先到达的超时会先终止对应工作：

1. Action walltime 到达：只终止该次化学计算，并把超时结果返回给 Agent；Agent仍可修改设置后重试。
2. MCP 调用超时到达：客户端停止等待该次工具调用。
3. 评测任务总超时到达：整个 Agent 任务终止；评测框架会清理该任务启动的后台化学作业。

建议满足：

```text
评测任务总超时 > 最大单次 Action walltime + Agent 分析和撰写答案所需时间
MCP 单次工具调用超时 > 最大同步 Action walltime
```

例如，计划执行最长 3600 秒的计算时，可将任务总超时设置为 5400–7200 秒。计划允许 7200 秒的周期体系计算时，任务总超时建议至少设置为 10800 秒。

## 2. 基本用法

在项目根目录执行：

```bash
bash scripts/submit_evaluation.sh submit [选项] TASK [TASK ...]
```

`TASK` 是 `tasks/` 下的任务目录名，目录中必须存在 `task_info.json`。

### 2.1 提交单个任务

```bash
bash scripts/submit_evaluation.sh submit \
  Electron_Isodensity_Reproduction_04_Blind_Prediction
```

默认行为：

- Agent 框架：`opencode`
- Agent 模型：`deepseek-v4-flash`
- Judge 模型：与 Agent 模型相同
- 单任务总超时：7200 秒
- 最大 Agent 轮数：200
- 并发任务数：1
- 每个任务重复次数：1
- 使用 `tmux` 后台运行
- 任务结束后自动评分

### 2.2 一次提交多个任务

```bash
bash scripts/submit_evaluation.sh submit \
  --model deepseek-v4-flash \
  --judge-model deepseek-v4-flash \
  --timeout-seconds 10800 \
  --max-turns 250 \
  Task_A Task_B Task_C
```

默认按 `--max-concurrent-runs 1` 逐个运行。对于可能占用较多 CPU 和内存的化学任务，建议保持串行，避免多个任务争用资源。

### 2.3 提交后立即查看进度

```bash
bash scripts/submit_evaluation.sh submit \
  --follow \
  Task_A Task_B
```

`--follow` 只是在当前终端展示状态；真正的评测仍运行在后台 `tmux` 中。退出状态查看不会停止任务。

### 2.4 前台运行

```bash
bash scripts/submit_evaluation.sh submit \
  --foreground \
  Task_A
```

适合调试。关闭终端或中断前台进程会停止评测，长任务建议使用默认的后台模式。

### 2.5 只检查配置，不实际运行

```bash
bash scripts/submit_evaluation.sh submit \
  --dry-run \
  Task_A Task_B
```

该命令会检查任务是否存在、生成提交配置并打印计划，但不会调用模型执行任务。

### 2.6 只执行 Agent，不调用 Judge

```bash
bash scripts/submit_evaluation.sh submit \
  --no-score \
  Task_A
```

适合只检查工具调用轨迹。之后如需得到分数，需要单独运行 Judge。

## 3. `submit` 参数

| 参数 | 默认值 | 作用 |
|---|---:|---|
| `--agent NAME` | `opencode` | Agent 框架预设名称 |
| `--model MODEL` | `deepseek-v4-flash` | 执行任务的 Agent 模型 |
| `--judge-model MODEL` | 与 `--model` 相同 | 评分模型 |
| `--timeout-seconds N` | `7200` | 每个任务的 Agent 总 walltime，单位为秒 |
| `--max-turns N` | `200` | 每个任务允许的最大 Agent 轮数 |
| `--max-concurrent-runs N` | `1` | 同时运行的任务数 |
| `--repeats N` | `1` | 每个任务重复运行次数 |
| `--workspaces-dir PATH` | `workspaces/submissions/<UTC>` | 本次提交的根目录 |
| `--session NAME` | 自动生成 | 后台运行使用的 `tmux` 会话名 |
| `--tool-discovery-mode progressive\|full` | `progressive` | 工具目录发现方式；渐进发现可减少上下文消耗 |
| `--progress-max-chars N` | `600` | 实时日志中每个字段最多保留的字符数 |
| `--progress-console` | 关闭 | 将详细实时进度同时写入 `launcher.log` |
| `--no-score` | 关闭 | 跳过 Judge 评分 |
| `--foreground` | 关闭 | 在当前终端运行，不创建 `tmux` 会话 |
| `--follow` | 关闭 | 后台提交后持续显示批次状态 |
| `--dry-run` | 关闭 | 只验证并打印执行计划 |

所有数值参数必须是正整数。

## 4. 查看和控制任务

提交成功后，终端会打印两个重要值：

```text
Submission root: /.../workspaces/submissions/20260727_120000
tmux session: rcb_20260727_120000
```

后续命令分别使用这两个值。

### 4.1 查看一次当前状态

```bash
bash scripts/submit_evaluation.sh status \
  --run-root workspaces/submissions/20260727_120000
```

状态表包括任务状态、运行时间、评分、工具调用次数、失败工具调用次数和总 token 数。

### 4.2 持续跟踪直到全部完成

```bash
bash scripts/submit_evaluation.sh follow \
  --run-root workspaces/submissions/20260727_120000 \
  --interval 30
```

`--interval` 的默认值为 10 秒。它只影响状态刷新频率，不影响 Agent 或工具调用。

### 4.3 进入后台终端

```bash
bash scripts/submit_evaluation.sh attach \
  --session rcb_20260727_120000
```

从 `tmux` 退出但保持任务运行：按 `Ctrl-b`，再按 `d`。

### 4.4 安全停止任务

```bash
bash scripts/submit_evaluation.sh stop \
  --session rcb_20260727_120000
```

脚本向评测进程发送 `SIGINT`，由评测框架停止当前 Agent、清理该任务启动的后台计算进程，并尽可能写入最终元数据。不要直接 `kill -9` 主评测进程，否则可能来不及执行清理和结果保存。

### 4.5 查看最终汇总

```bash
bash scripts/submit_evaluation.sh summary \
  --run-root workspaces/submissions/20260727_120000
```

任务全部结束后，该命令格式化输出批次级 `results.json`。如果尚未结束，会显示当前状态并返回非零退出码。

## 5. 输出文件

一次提交的主要目录结构如下：

```text
workspaces/submissions/<UTC>/
├── evaluation_config.yaml     # 本次评测配置
├── submission.json            # 提交参数和任务列表
├── launcher.log               # 启动器及可选实时进度日志
└── runs/
    └── cli_runs/
        └── batch_<...>/
            ├── results.json   # 整个批次的机器可读汇总
            └── <task_workspace>/
                ├── results.json
                ├── _meta.json
                ├── _score.json
                ├── _live_progress.log
                └── ...
```

批次和任务级 `results.json` 会保存可用的关键指标，包括：

- 总分和各评分维度；
- Agent 状态及运行时间；
- 工具调用次数和失败次数；
- 输入、输出、缓存及总 token；
- Agent 模型、Agent 框架和 Judge 模型；
- 任务目录、轨迹和评分文件位置。

## 6. 推荐配置

### 快速功能测试

```bash
bash scripts/submit_evaluation.sh submit \
  --timeout-seconds 600 \
  --max-turns 50 \
  --no-score \
  Task_A
```

### 常规化学评测

```bash
bash scripts/submit_evaluation.sh submit \
  --timeout-seconds 7200 \
  --max-turns 200 \
  --max-concurrent-runs 1 \
  Task_A Task_B
```

### 允许最长 7200 秒后端计算的复杂复现任务

```bash
bash scripts/submit_evaluation.sh submit \
  --timeout-seconds 10800 \
  --max-turns 300 \
  --max-concurrent-runs 1 \
  Task_A
```

如果确实需要让一次同步工具调用超过默认的 7500 秒，还必须同时增大 MCP 客户端超时：

```bash
RESEARCHCHEMBENCH_MCP_TOOL_TIMEOUT_MS=12600000 \
bash scripts/submit_evaluation.sh submit \
  --timeout-seconds 14400 \
  Task_A
```

## 7. 常见问题

### Agent 总超时已经调大，为什么某个计算仍在 1800 秒停止？

因为 `--timeout-seconds` 只控制整个 Agent 任务。该 Action 很可能仍使用默认的 `resource_limits.walltime_seconds=1800`。Agent 需要在工具请求中提高该值，同时遵守对应 backend 的最大 walltime。

### Action walltime 已调到 9000 秒，为什么工具调用仍会提前断开？

默认 MCP 客户端只等待 7500 秒。需要提高 `RESEARCHCHEMBENCH_MCP_TOOL_TIMEOUT_MS`，并确保评测任务总超时更长。

### 如何确认本次 OpenCode 工作区使用的 MCP 超时？

在任务工作区中检查生成的 `opencode.json`：

```bash
jq '.mcp | to_entries[] | {server: .key, timeout_ms: .value.timeout}' \
  /path/to/task_workspace/opencode.json
```

### 如何知道某个 Action 允许设置多长 walltime？

让 Agent 查询该 Action 的工具目录或调用 `inspect_action`，检查请求 schema 中的 `resource_limits`、`action_settings` 和 backend 的资源约束。不能假设所有后端都允许 172800 秒。

### 并发数越大越好吗？

不是。`--max-concurrent-runs` 控制同时运行多少个完整 Agent 任务；每个任务内部又可能启动多核化学软件。总 CPU 和总内存需求是所有并发任务的叠加。化学 benchmark 通常建议从 1 开始，确认单任务资源使用后再提高。

### 怎样查看脚本的简短帮助？

```bash
bash scripts/submit_evaluation.sh --help
```
