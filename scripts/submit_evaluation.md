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
- MCP timeout必须大于计算Action timeout和作业等待心跳时间。

10800秒只是计算类默认值，不是硬上限。人工可以通过脚本增大或减小它；相应地必须把MCP和Agent总timeout设置得更长。

### native/analysis作业的稳定等待

原生软件作业和Agent编写的analysis program使用 `wait_execution_jobs` 批量监督。工具箱在一次MCP调用内部检查作业状态；Agent不需要使用shell `sleep`、循环、`grep`、重复的 `get_execution_job` 或重复的 `get_execution_resources` 进行轮询。

异步Action batch使用`wait_execution_events`执行相同的稳定监督。首个item进入成功、失败、超时或取消等终态后，工具箱默认继续等待60秒调度状态稳定；期间运行任务继续运行，资源释放后排队item自动补位。返回值一次给出新终态结果和artifact、仍在运行/排队的item、剩余batch ID、cursor及worker资源快照。请求中的旧`timeout_seconds`仅作兼容解析，不能缩短评估器控制的稳定窗口。

默认策略如下：

| 参数 | 默认值 | 配置方式 | 含义 |
|---|---:|---|---|
| 稳定窗口 | 60秒 | `--job-event-settle-seconds N` | 首个终态出现后，连续无重要状态变化多久才聚合返回 |
| 单批聚合上限 | 300秒 | `RESEARCHCHEMBENCH_JOB_EVENT_MAX_BATCH_SECONDS` | 状态持续变化时最迟多久返回一次 |
| 无事件心跳 | 3600秒 | `RESEARCHCHEMBENCH_JOB_WAIT_HEARTBEAT_SECONDS` | 没有终态事件时多久返回一次心跳 |
| 内部检查间隔 | 2秒 | `RESEARCHCHEMBENCH_JOB_INTERNAL_POLL_INTERVAL_SECONDS` | 工具箱内部读取持久状态的频率 |
| 失败日志尾部 | 2000字符 | `RESEARCHCHEMBENCH_JOB_FAILURE_TAIL_CHARS` | 失败/超时作业随聚合结果返回的日志上限 |

除稳定窗口外，其余参数是高级评测策略，通常只在 `config.local.env` 中设置。它们不会进入Agent可填写的工具请求，因此被评估智能体不能缩短稳定窗口或提高轮询频率。
若人工把 MCP timeout 设得短于默认心跳且没有显式设置心跳，提交器会把有效心跳自动收窄为 `MCP timeout - 1秒`；显式设置的心跳必须仍小于 MCP timeout。

终态、排队转运行、worker分配和reservation释放会重置稳定窗口；stdout/stderr增长、SCF迭代和优化步增长不会重置。作业一旦终态，调度器立即释放资源并让合法排队作业自动补位，60秒只用于合并通知，不会让worker空等。返回部分结果时，其他运行作业继续运行，返回中会同时列出 `running_jobs`、`queued_jobs` 和下一次等待使用的 `remaining_job_ids`。

示例：

```bash
bash scripts/submit_evaluation.sh submit \
  --job-event-settle-seconds 90 \
  --mcp-tool-timeout-seconds 14000 \
  Task_A
```

## 2. CPU、内存和GPU资源预算

### 2.1 单节点模式

单节点模式由评测者在提交任务时设置资源总量，并作为每个任务的固定环境条件告诉智能体：

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

### 2.2 分布式worker模式

分布式模式下，主节点只运行Agent、MCP服务和调度逻辑，化学计算作业由worker池执行。每个作业只能使用一台worker，不会跨节点并行；同一评估任务可以同时向多台worker提交多个独立计算作业。

此模式的资源上限来自 `RCB_DISTRIBUTED_WORKER_INVENTORY` 指向的worker inventory，而不是 `--available-cpu-cores`、`--available-memory-mb` 和 `--available-gpu-count`。智能体会看到整个资源池的总容量，以及单个作业在一台worker上最多能申请的资源。

在 `config.local.env` 中至少设置：

```bash
RCB_DISTRIBUTED_WORKER_INVENTORY=".worker_inventory.local.json"
```

如果远端worker启动计算前需要初始化代理，还可以设置：

```bash
RCB_DISTRIBUTED_REMOTE_INIT_SCRIPT_URL="http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh"
```

#### 更新worker inventory

`.workers.local.yaml` 是人工维护的源配置，例如：

```yaml
workers:
  - ssh: "ssh -CAXY <worker-ssh-target>"
    available_cpu_cores: 64
    available_memory_mb: 128000
    enabled: true
```

其中 `enabled` 是可选字段：

- 省略 `enabled` 与写入 `enabled: true` 完全相同，表示该worker参与调度；
- `enabled: false` 表示生成的inventory保留这台worker的信息，但调度器不加载它；
- inventory更新脚本当前仍会探测 `enabled: false` 的条目。如果worker已经离线，应先从源YAML中删除或注释该条目，否则探测会失败。

生成或刷新运行清单：

```bash
.envs/researchchembench/bin/python scripts/update_worker_inventory.py \
  --input .workers.local.yaml \
  --output .worker_inventory.local.json \
  --known-hosts .worker_known_hosts.local
```

该命令会并行连接所有源配置中的worker，探测CPU拓扑、cgroup内存、直连地址和SSH主机密钥，并生成 `.worker_inventory.local.json`。

#### 使用 OpenSandbox worker 池

Sandbox 与 SSH worker 使用同一套调度、reservation、排队、超时和核心执行逻辑。SSH 仍是默认传输；只有显式选择 `sandbox` 时才进入 OpenSandbox HTTP/RPC 传输层。

本地源配置为 `.sandboxes.local.yaml`，生成 inventory：

也可以自动创建指定规模的 Sandbox 池并生成这两个文件：

```bash
bash scripts/create_sandbox_pool.sh \
  --count 4 \
  --cpu 20 \
  --memory 48Gi \
  --available-memory-mb 45000 \
  --lifecycle-minutes 1440 \
  --replace
```

该脚本创建成功后会把 Environment ID 和每个 Sandbox ID 自动写回 `.sandboxes.local.yaml`，并生成 `.sandbox_inventory.local.json`。`--replace` 会备份现有本地配置，但不会停止旧的远端实例。使用 `--help` 查看镜像、端口、挂载、名称和调度资源等完整参数。

手工刷新已有配置对应的 inventory：

```bash
.envs/researchchembench/bin/python scripts/update_sandbox_inventory.py \
  --input .sandboxes.local.yaml \
  --output .sandbox_inventory.local.json
```

源 YAML 中每个条目只需要维护 Sandbox ID 和希望暴露给调度器的资源。若环境和实例使用 `create_if_missing: true` 且 ID 为 `null`，脚本也可以自动创建并把生成的 ID 写回 YAML。API Key 从 `config.local.env` 的 `RCB_SANDBOX_API_KEY` 读取，不写入 inventory。

提交 Sandbox 分布式任务：

```bash
bash scripts/submit_evaluation.sh submit \
  --execution-mode distributed \
  --distributed-transport sandbox \
  --distributed-inventory .sandbox_inventory.local.json \
  Task_A
```

切回原有 SSH worker：

```bash
bash scripts/submit_evaluation.sh submit \
  --execution-mode distributed \
  --distributed-transport ssh \
  --distributed-inventory .worker_inventory.local.json \
  Task_A
```

Sandbox 的共享 GPFS 挂载为只读。框架会自动把 Action 引用的 workspace 文件上传到实例本地目录；native/analysis 作业会整体 stage 到 `/tmp`，完成后再把状态、日志和产物同步回主节点。因此不要把 Sandbox proxy URL 填入 `execution_ssh_target`。

#### 控制本次运行使用多少台worker

`submit_evaluation.sh` 当前没有 `--worker-count N` 参数。实际使用的worker集合由inventory中 `enabled` 为真的条目决定。推荐为不同规模的运行准备不同的源YAML和inventory，例如：

```bash
.envs/researchchembench/bin/python scripts/update_worker_inventory.py \
  --input .workers.two.yaml \
  --output .worker_inventory.two.json \
  --known-hosts .worker_known_hosts.two

RCB_DISTRIBUTED_WORKER_INVENTORY=.worker_inventory.two.json \
  bash scripts/submit_evaluation.sh submit \
    --execution-mode distributed \
    Task_A
```

不要在仍有分布式作业运行时原地修改该运行正在使用的inventory。需要改变worker数量时，应生成新的inventory文件，并让下一次提交指向新文件。

#### `.worker_inventory.local.json` 字段说明

顶层字段：

| 字段 | 含义 |
|---|---|
| `schema_version` | inventory数据结构版本 |
| `generated_at` | inventory生成时间，UTC |
| `project_path` | 生成时确认worker可以访问的共享项目路径 |
| `scheduling_policy` | 记录的调度策略；当前为 `largest_cpu_first`，优先处理CPU请求较大的作业 |
| `workers` | worker记录列表 |

每个worker的主要字段：

| 字段 | 含义 |
|---|---|
| `worker_id` | 调度器使用的唯一逻辑ID，例如 `compute-1` |
| `name`、`hostname`、`fqdn` | 远端探测到的主机名和完整域名 |
| `gateway_ssh_target` | 用户提供的rlaunch网关SSH目标，主要用于发现和探测worker |
| `gateway_ssh_options` | 网关连接参数，例如 `-CAXY` |
| `execution_ssh_target` | 实际计算作业使用的worker直连SSH目标 |
| `direct_ip` | worker的内部直连IP |
| `logical_cpus` | worker进程所在cpuset中可见的逻辑CPU数量 |
| `physical_cores` | 上述逻辑CPU对应的物理核心数量 |
| `memory_mb` | 在worker cgroup中实际探测到的内存容量，单位MiB |
| `available_cpu_cores` | 暴露给调度器、允许计算作业申请的逻辑CPU总数 |
| `available_memory_mb` | 暴露给调度器、允许计算作业申请的内存总量 |
| `reserved_cpu_cores` | `logical_cpus - available_cpu_cores`，静态留给系统和控制进程的CPU余量 |
| `reserved_memory_mb` | `memory_mb - available_memory_mb`，静态保留的内存余量 |
| `gpu_count` | 暴露给调度器的GPU数量 |
| `compute_cpu_ids` | 调度器可以分配给计算作业的Linux逻辑CPU编号列表 |
| `compute_core_groups` | 按物理核心分组的可调度逻辑CPU；同组SMT sibling不会分给不同作业 |
| `all_cpu_ids` | worker当前cpuset中全部可见的Linux逻辑CPU编号 |
| `known_hosts_file` | 直连worker时使用的固定SSH主机密钥文件 |
| `ssh_host_key_fingerprint` | 已验证的SSH主机公钥指纹 |
| `enabled` | 是否将该worker加载进调度池；缺省为 `true` |
| `connectivity_status` | inventory生成时的连通性结果，不是持续更新的实时心跳 |

`compute_cpu_ids` 不是“CPU数量”，而是一组Linux CPU编号。生成脚本根据worker的CPU亲和性、物理核心、SMT线程和NUMA拓扑，从 `all_cpu_ids` 中选择完整物理核心并尽量在NUMA节点间均衡。例如worker可见80个逻辑CPU、只暴露64个时，该列表包含选中的64个逻辑CPU，其他16个逻辑CPU作为静态余量保留。

`compute_core_groups`保存上述CPU对应的物理核心关系，例如`[6, 70]`表示两个逻辑CPU属于同一物理核心。调度器允许一个作业使用整组，但不会把两个sibling拆给两个不同作业；奇数CPU请求只向作业暴露所需数量，同时临时阻塞同组剩余sibling，作业结束后一起释放。旧inventory没有该字段时仍可读取，但会退化为逻辑CPU粒度，因此更新代码后应重新运行inventory生成脚本。

这些编号不必从0开始，也不必连续；rlaunch/cgroup分配出的cpuset本来就可能是不连续的。每个作业获得其中一部分编号，远端启动器通过CPU affinity以及OpenMP、MKL、OpenBLAS和MPI相关环境变量将进程限制到这部分CPU，避免不同作业重叠使用同一逻辑核。

注意，inventory中的 `reserved_cpu_cores` 是生成inventory时确定的静态安全余量；运行状态快照中worker的 `reserved.cpu_cores` 则是当前活跃作业动态占用的资源，两者不是同一个概念。

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

不传 `--execution-mode` 时默认使用原有单节点模式；也可以显式写出：

```bash
bash scripts/submit_evaluation.sh submit \
  --execution-mode local \
  Task_A
```

使用worker池时：

```bash
bash scripts/submit_evaluation.sh submit \
  --execution-mode distributed \
  --workspaces-dir workspaces/distributed-example \
  --session rcb_distributed_example \
  Task_A
```

使用 Sandbox 池时：

```bash
bash scripts/submit_evaluation.sh submit \
  --execution-mode distributed \
  --distributed-transport sandbox \
  --distributed-inventory .sandbox_inventory.local.json \
  --workspaces-dir workspaces/sandbox-example \
  --session rcb_sandbox_example \
  Task_A
```

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

默认 `--max-concurrent-runs 1`，即逐个运行完整评估任务。分布式模式下，即使该值为1，一个评估任务内的Agent仍可同时提交多个独立化学计算作业，由worker池调度；该参数控制的是完整Agent任务的并发数，不是worker计算作业数。

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
| `--max-turns N` | `600` | 每个任务最大Agent轮数 |
| `--max-concurrent-runs N` | `1` | 同时运行的完整任务数 |
| `--repeats N` | `1` | 每个任务重复次数 |
| `--workspaces-dir PATH` | `workspaces/submissions/<UTC>` | 本次提交根目录 |
| `--session NAME` | 自动生成 | `tmux`会话名 |
| `--tool-discovery-mode progressive\|full` | `progressive` | 工具目录发现方式 |
| `--execution-mode local\|distributed` | `local` | 选择原有单节点执行或分布式worker池执行 |
| `--distributed-transport ssh\|sandbox` | `ssh` | 分布式模式使用原有SSH worker或OpenSandbox实例 |
| `--distributed-inventory PATH` | 按传输类型从本地配置读取 | 显式指定本次运行使用的worker inventory |
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

`submission.json`、批次配置、任务 `_meta.json` 和 `results.json` 会记录本次使用的四层timeout策略、执行模式和资源预算。分布式计算作业的结果还会记录实际分配的 `worker_id`、CPU编号和其他资源信息。

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

执行模式可使用：

```bash
jq '.execution_mode // .run.execution_mode' /path/to/task_workspace/{_meta.json,results.json}
```

### 为什么 `.workers.local.yaml` 中没有 `enabled: true`？

因为它是可选开关，缺省值就是 `true`。当前四个worker即使未显式写出该字段，也都会被生成到inventory并参与调度。只有需要临时排除一台仍然可连通的worker时，才需要显式写 `enabled: false` 并重新生成inventory。

### 为什么 `compute_cpu_ids` 看起来不连续？

它记录的是worker cgroup实际允许使用的Linux逻辑CPU编号，而不是从0开始重新编号后的序号。cgroup cpuset、NUMA拓扑和SMT线程布局都可能令编号不连续，这是正常现象；不要手工把它改成 `0..N-1`。

### 分布式模式下如何查看当前资源池？

智能体可以通过工具箱资源状态接口取得worker容量、当前活跃reservation、排队请求和剩余资源。评测者也可以在项目环境中读取同一个快照：

```bash
set -a
source config.local.env
set +a
RESEARCHCHEMBENCH_EXECUTION_MODE=distributed \
  .envs/researchchembench/bin/python - <<'PY'
from pprint import pprint
from researchchem_toolbox.distributed_pool import pool_snapshot

pprint(pool_snapshot(include_internal=True))
PY
```

### 查看脚本帮助

```bash
bash scripts/submit_evaluation.sh --help
```
