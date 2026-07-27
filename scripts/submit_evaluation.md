# `submit_evaluation.sh` 使用说明

`scripts/submit_evaluation.sh` 用于提交一个或多个 ResearchChemBench 任务，支持 `tmux` 后台运行、状态查看、安全停止和结果汇总。

## 1. 默认 timeout 策略

timeout 是评测环境统一规定的资源预算，不再由智能体设置。

| 层级 | 默认值 | 脚本参数 | 智能体能否修改 |
|---|---:|---|---|
| 快速/数据 Action | 240秒 | `--fast-action-timeout-seconds` | 否 |
| 计算 Action、native job、analysis program | 10800秒 | `--compute-action-timeout-seconds` | 否 |
| MCP单次工具调用 | 14000秒 | `--mcp-tool-timeout-seconds` | 否 |
| 单个Agent任务总时间 | 14400秒 | `--timeout-seconds` | 否 |

计算类包括ORCA、Gaussian、CREST、xTB、VASP、QE、GPAW、结构优化、频率、TS、IRC、反应路径、电子密度、热化学、native software job和Agent编写的analysis program。

快速类包括PubChem、Materials Project等数据Action。工具发现、软件检查和作业状态查询本身也不接受智能体提供的timeout。

### timeout关系

推荐保持：

```text
快速Action timeout < 计算Action timeout < MCP timeout < Agent任务总timeout
```

默认关系为：

```text
240 < 10800 < 14000 < 14400
```

`submit_evaluation.sh` 会检查：

- 快速Action timeout不能超过计算Action timeout；
- MCP timeout必须大于计算Action timeout。

10800秒只是计算类默认值，不是硬上限。人工可以通过脚本增大或减小它；相应地必须把MCP和Agent总timeout设置得更长。

## 2. CPU、内存和GPU资源预算

资源总量由评测者在提交任务时设置，并作为每个任务的固定环境条件告诉智能体：

| 参数 | 默认值 | 含义 |
|---|---:|---|
| `--available-cpu-cores N` | `48` | 单个任务可使用的逻辑CPU核数上限 |
| `--available-memory-mb N` | `204800` | 单个任务可使用的内存上限，单位MiB |
| `--available-gpu-count N` | `0` | 单个任务可使用的GPU数量上限 |

这些默认值依据当前服务器的实际进程约束设置：64个在线且位于当前CPU
亲和性集合中的物理核、300 GiB cgroup内存上限、无swap。默认保留16个CPU核和约
100 GiB cgroup内存给评测服务、操作系统及其他进程；不会根据提交瞬间的系统负载
动态变化，以保持不同评测运行之间的资源条件可复现。

示例：

```bash
bash scripts/submit_evaluation.sh submit \
  --available-cpu-cores 48 \
  --available-memory-mb 204800 \
  --available-gpu-count 0 \
  Task_A
```

智能体不能修改这三个环境上限，但可以为每次计算选择不超过上限的资源：

智能体仍然可以在backend允许范围内选择：

```json
{
  "resource_limits": {
    "cpu_cores": 16,
    "memory_mb": 32000,
    "gpu_count": 0
  }
}
```

工具箱同时检查两层约束：

- 单次Action或作业的CPU、内存、GPU请求不得超过任务预算；
- 同一任务内所有并发排队或运行的托管计算，资源请求总和不得超过任务预算。

超额请求会返回结构化的 `resource_budget_exceeded` 或
`aggregate_resource_budget_exceeded` 错误，不会静默缩小。CPU通过进程亲和性和线程环境变量约束，内存通过进程地址空间上限约束，GPU通过可见设备列表约束。

默认 `--max-concurrent-runs 1`。如果并行执行多个完整任务，每个任务均拥有上述独立预算，因此评测者应确保“单任务预算 × 并发任务数”不超过服务器实际资源。

资源预算会写入：

- 智能体初始任务指令；
- Action和原生软件工具目录；
- `evaluation_config.yaml`、`submission.json`；
- 每个任务的 `_meta.json`、`_toolbox_catalog.json` 和 `results.json`。

### timeout仍不可由智能体控制

公开Action请求中不再包含：

```json
{
  "walltime_seconds": 1800
}
```

如果智能体猜测并提交 `resource_limits.walltime_seconds` 或 `action_settings.timeout_seconds`，工具箱会拒绝请求并说明timeout由评测策略控制。

## 3. 基本用法

在项目根目录执行：

```bash
bash scripts/submit_evaluation.sh submit [OPTIONS] TASK [TASK ...]
```

`TASK` 是 `tasks/` 下的目录名，目录中必须存在 `task_info.json`。

### 提交单个任务

```bash
bash scripts/submit_evaluation.sh submit \
  Electron_Isodensity_Reproduction_04_Blind_Prediction
```

### 提交多个任务

```bash
bash scripts/submit_evaluation.sh submit \
  Task_A Task_B Task_C
```

默认 `--max-concurrent-runs 1`，即逐个运行。多核化学任务建议先保持串行，避免多个任务争用CPU和内存。

### 显式设置全部 timeout

```bash
bash scripts/submit_evaluation.sh submit \
  --fast-action-timeout-seconds 60 \
  --compute-action-timeout-seconds 10800 \
  --mcp-tool-timeout-seconds 14000 \
  --timeout-seconds 14400 \
  Task_A
```

### 使用Flash执行和评分

```bash
bash scripts/submit_evaluation.sh submit \
  --model deepseek-v4-flash \
  --judge-model deepseek-v4-flash \
  Task_A Task_B
```

### 提交后持续查看状态

```bash
bash scripts/submit_evaluation.sh submit \
  --follow \
  Task_A Task_B
```

任务仍在后台 `tmux` 中运行；退出状态显示不会停止任务。

### 前台调试

```bash
bash scripts/submit_evaluation.sh submit \
  --foreground \
  Task_A
```

长任务建议使用默认后台模式。

### 只检查配置

```bash
bash scripts/submit_evaluation.sh submit \
  --dry-run \
  Task_A Task_B
```

该命令会验证参数和任务目录、生成配置并打印计划，但不调用模型。

### 不调用Judge

```bash
bash scripts/submit_evaluation.sh submit \
  --no-score \
  Task_A
```

## 4. `submit` 参数

| 参数 | 默认值 | 作用 |
|---|---:|---|
| `--agent NAME` | `opencode` | Agent框架预设 |
| `--model MODEL` | `deepseek-v4-flash` | 执行任务的模型 |
| `--judge-model MODEL` | 与Agent模型相同 | Judge模型 |
| `--timeout-seconds N` | `14400` | 每个Agent任务的总walltime |
| `--compute-action-timeout-seconds N` | `10800` | 所有计算Action和计算作业的固定timeout |
| `--fast-action-timeout-seconds N` | `240` | 所有快速/数据Action的固定timeout |
| `--mcp-tool-timeout-seconds N` | `14000` | MCP客户端等待单次工具调用的最长时间 |
| `--available-cpu-cores N` | `48` | 每个任务的CPU核数预算 |
| `--available-memory-mb N` | `204800` | 每个任务的内存预算，单位MiB |
| `--available-gpu-count N` | `0` | 每个任务的GPU数量预算 |
| `--max-turns N` | `200` | 每个任务最大Agent轮数 |
| `--max-concurrent-runs N` | `1` | 同时运行的完整任务数 |
| `--repeats N` | `1` | 每个任务重复次数 |
| `--workspaces-dir PATH` | `workspaces/submissions/<UTC>` | 本次提交根目录 |
| `--session NAME` | 自动生成 | `tmux`会话名 |
| `--tool-discovery-mode progressive\|full` | `progressive` | 工具目录发现方式 |
| `--progress-max-chars N` | `600` | 实时日志每个字段的显示上限 |
| `--progress-console` | 关闭 | 把详细进度同时写入启动器终端日志 |
| `--no-score` | 关闭 | 跳过Judge评分 |
| `--foreground` | 关闭 | 在当前终端执行 |
| `--follow` | 关闭 | 后台提交后持续显示状态 |
| `--dry-run` | 关闭 | 只验证并打印计划 |

## 5. 查看和控制任务

提交后会打印：

```text
Submission root: /.../workspaces/submissions/20260727_120000
tmux session: rcb_20260727_120000
```

### 查看当前状态

```bash
bash scripts/submit_evaluation.sh status \
  --run-root workspaces/submissions/20260727_120000
```

状态表包含任务状态、运行时间、评分、工具调用次数、失败次数和token消耗。

### 持续跟踪

```bash
bash scripts/submit_evaluation.sh follow \
  --run-root workspaces/submissions/20260727_120000 \
  --interval 30
```

`--interval` 只控制刷新频率，不影响评测或工具timeout。

### 进入后台终端

```bash
bash scripts/submit_evaluation.sh attach \
  --session rcb_20260727_120000
```

按 `Ctrl-b`，再按 `d`，可退出 `tmux` 但保持任务运行。

### 安全停止

```bash
bash scripts/submit_evaluation.sh stop \
  --session rcb_20260727_120000
```

评测框架会停止Agent并清理该任务启动的后台化学作业。不要直接对主评测进程使用 `kill -9`。

### 查看最终汇总

```bash
bash scripts/submit_evaluation.sh summary \
  --run-root workspaces/submissions/20260727_120000
```

## 6. 输出文件

```text
workspaces/submissions/<UTC>/
├── evaluation_config.yaml
├── submission.json
├── launcher.log
└── runs/
    └── cli_runs/
        └── batch_<...>/
            ├── results.json
            └── <task_workspace>/
                ├── results.json
                ├── _meta.json
                ├── _score.json
                ├── _tool_trace.jsonl
                └── _live_progress.log
```

`submission.json`、批次配置、任务 `_meta.json` 和 `results.json` 会记录本次使用的四层timeout策略和资源预算。

## 7. 常见问题

### timeout设置为10800秒，简单Action会等待10800秒吗？

不会。timeout是上限，不是固定执行时间。10秒完成的Action仍会在10秒左右返回。

### 为什么不允许智能体修改timeout？

timeout属于benchmark资源预算。统一设置可以保证不同模型处在相同环境中，并避免模型误把昂贵计算设置成过短时间。

### 设置较大timeout能保证计算成功吗？

不能。错误输入、SCF不收敛、错误方法或软件故障仍可能失败。较大timeout只避免正常长计算被过早终止。

### 为什么数据Action不也设置为7200秒？

正常数据请求不会因为60秒上限而变慢；如果远程服务卡死，短timeout可以避免一次网络请求占据整个评测任务。

### 如何查看某次运行实际使用的策略？

查看任务工作区的 `_meta.json` 或 `results.json`：

```bash
jq '.timeout_policy // .run.timeout_policy' /path/to/task_workspace/{_meta.json,results.json}
```

资源预算可使用：

```bash
jq '.resource_budget // .run.resource_budget' /path/to/task_workspace/{_meta.json,results.json}
```

### 查看脚本帮助

```bash
bash scripts/submit_evaluation.sh --help
```
