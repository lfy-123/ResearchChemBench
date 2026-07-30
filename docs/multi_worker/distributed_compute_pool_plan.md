# ResearchChemBench 单任务多 Worker 计算资源池方案

状态：方案确认阶段，尚未修改执行代码
更新时间：2026-07-31

## 1. 目标与边界

本方案面向一个正在评估的 ResearchChemBench 任务。Agent、模型调用、MCP
服务和科学决策仍位于协调节点；工具箱把这个任务内部彼此独立的计算 Action、原生
软件作业和分析程序自动调度到多个 CPU worker。

明确边界如下：

- 不把不同 benchmark task 分发到不同 worker；
- 不让一个 ORCA、Gaussian、CP2K、xTB 等单次计算跨节点运行；
- 只并行分发彼此独立的计算；
- Agent 不选择 worker，不接触 SSH 地址，也不管理远端进程；
- 工具箱负责节点选择、资源预留、CPU 绑定、启动、查询、取消和故障隔离；
- 保留完全兼容的单节点模式。

```text
协调节点
Agent + MCP + 工具箱调度器
        │
        ├── Agent 同时提交独立计算及其 CPU/内存需求
        ▼
工具箱按 CPU 请求从大到小排序并自动放置
        ├── 64 CPU 计算 A ── worker 1
        ├── 32 CPU 计算 B ── worker 2
        ├── 16 CPU 计算 C ── worker 3
        └──  8 CPU 计算 D ── worker 4
```

## 2. 当前实测资源

2026-07-31 在 worker 以 `rlaunch --cpu=80 --memory=180000` 重新创建后，通过直接
SSH、`sched_getaffinity`、sysfs CPU topology 和 cgroup 获得以下资源。这里的“可用
CPU”是 cpuset 中的逻辑 CPU 数量。每台计算 worker 当前的 80 个逻辑 CPU 对应 40 个
物理核，每个物理核的两个 SMT 线程都在 cpuset 中。内存 cgroup 实测为 200000 MiB，
高于 rlaunch 请求的 180000 MiB。

| 节点 | 角色 | 可用 CPU | 物理核 | 内存 | CPU 型号 |
|---|---|---:|---:|---:|---|
| `guass-rkslq-310855-worker-0` | 当前协调节点 | 16 | 8 | 32000 MiB | 待运行时探测 |
| `guass-66bjc-338744-worker-0` | compute worker | 80 | 40 | 200000 MiB | Intel Xeon Gold 6530 |
| `guass-qh9l7-338862-worker-0` | compute worker | 80 | 40 | 200000 MiB | Intel Xeon Gold 6530 |
| `guass-zhh2n-338979-worker-0` | compute worker | 80 | 40 | 200000 MiB | Intel Xeon Gold 6530 |
| `guass-gwm6f-339153-worker-0` | compute worker | 80 | 40 | 200000 MiB | Intel Xeon Gold 6530 |

四台计算 worker 的实际资源总量为：

- 320 个逻辑 CPU，实际由 160 个物理核提供；
- 800000 MiB 内存。

不把全部实际资源承诺给计算进程。每台 worker 保留 16 个逻辑 CPU 和 72000 MiB
内存给系统、SSH、调度 supervisor、文件缓存和异常峰值，向 Agent 公布的计算资源为：

- 256 个可调度 CPU；
- 2000 MiB/逻辑 CPU 的参考内存比例；
- 512000 MiB 可调度内存；
- 单个计算最多 64 CPU；
- 单个计算最多 128000 MiB 内存，CPU 和内存独立计量；
- 每台 worker 的可调度上限为 64 CPU、128000 MiB。

当前协调节点只有 16 CPU 和 32000 MiB 内存，明确固定作为控制平面，不加入分布式
计算池。它的资源保留给 Agent、MCP、Judge、调度器、SSH 协调和轻量数据操作。
调度器不得把预定义计算 Action、native software job 或 analysis program 分配到该
节点。这样 Agent 看到的是同构的四节点计算资源池，也不会因为重型计算占满协调节点
而拖慢模型和工具调用。

## 3. Agent 的资源规划权与使用规则

工具箱应在初始任务指令、工具目录和 `get_execution_resources` 中向 Agent 提供一个
稳定的抽象资源合同，而不暴露节点名称、IP 或 SSH 信息。

建议显示：

```json
{
  "execution_mode": "distributed",
  "scheduling": "toolbox_managed",
  "healthy_compute_nodes": 4,
  "total_cpu_cores": 256,
  "cpu_unit": "logical_cpu",
  "physical_cpu_cores_backing_pool": 128,
  "reference_memory_mb_per_cpu_core": 2000,
  "total_schedulable_memory_mb": 512000,
  "maximum_cpu_cores_per_job": 64,
  "maximum_memory_mb_per_job": 128000,
  "single_job_cross_node_execution": false
}
```

Agent 可以决定同时提交哪些彼此独立的作业，以及每个作业申请多少 CPU 和内存；但
不能选择具体 worker。工具箱只负责机械资源验证、排序、放置、执行和状态回报，不替
Agent 判断科学任务应如何拆分。

写给 Agent 的规则应包含：

1. 整个计算池共有 256 个逻辑 CPU，由 128 个物理核提供；资源请求中的
   `cpu_cores` 表示可调度逻辑 CPU 数量。
2. 单个计算必须固定在一台节点，最多申请 64 CPU 和 128000 MiB 内存。
3. 2000 MiB/CPU 只是帮助规划的参考比例，不是硬性绑定。CPU 和内存分别申请、
   分别预留；只要目标 worker 同时有足够的剩余 CPU 和内存就可以运行。
4. Agent 应根据软件的实际并行效率申请核数，不应为了占用资源盲目申请 64 核。
5. 相互独立的分子、构象、反应路径、参数点或重复计算应使用
   `submit_action_batch`，或连续提交多个 `submit_native_job`。
6. 存在数据依赖的计算必须按顺序执行，例如优化完成后才能提交依赖该结构的频率计算。
7. 资源不足时工具箱负责排队；Agent 不需要降低资源、选择节点或重复提交。
8. Agent 通过统一 job ID 查询和取消作业，不需要知道实际执行位置。
9. Agent 应尽可能一次提交当前已经确定相互独立的作业，使调度器能够在同一队列中按
   CPU 请求从大到小安排，减少后续大作业因资源碎片而等待。
10. 当作业完成、启动失败或执行失败后，工具箱返回每个 worker 的最新可用 CPU 和
    内存；Agent 可以据此继续提交下一批科学任务。

Agent 负责声明科学依赖关系和资源需求。工具箱无法安全推断两个未来请求是否独立，
因此如果 Agent 始终逐个调用同步 `execute_action`，这些调用本身无法重叠。工具说明
应要求 Agent 将已经确认独立的工作放入异步批量接口。

Agent 可以看到匿名 worker 槽位的资源状态，但看不到真实节点名、IP 或 SSH 配置：

```json
{
  "workers": [
    {"worker_id": "compute-1", "available_cpu": 64, "available_memory_mb": 128000},
    {"worker_id": "compute-2", "available_cpu": 32, "available_memory_mb": 96000},
    {"worker_id": "compute-3", "available_cpu": 64, "available_memory_mb": 128000},
    {"worker_id": "compute-4", "available_cpu": 16, "available_memory_mb": 48000}
  ],
  "total_available_cpu": 176,
  "total_available_memory_mb": 400000
}
```

## 4. 四个 16 核任务放一台还是分散四台

### 4.1 实际拓扑带来的差异

两种方式都申请 64 个逻辑 CPU，但实际使用的物理核数量可能不同：

- 把 `4 × 16 CPU` 全装入一台 worker，最终会使用 32 个物理核的两个 SMT 线程；
- 四台 worker 各运行一个 16 CPU 作业时，如果优先分配每个物理核的第一线程，最多
  可以使用 64 个不同的物理核。

因此两种布局的速度不能假设接近。对于 SMT 扩展效率较低的量化化学、线性代数、
内存带宽或 scratch I/O 密集程序，完全分散可能明显更快；代价是四台 worker 都被
部分占用，暂时没有一台可立即容纳 64 CPU 作业。

### 4.2 修正后的默认策略：Agent 规划，调度器大作业优先

Agent 一次提交一组当前已知、彼此独立的作业，并为每个作业声明 CPU 和内存需求。
工具箱采用以下确定性规则：

1. 所有等待作业按 `cpu_cores` 从大到小排序；CPU 相同时按 `memory_mb` 从大到小，
   再按提交时间排序。
2. 依次处理排序后的作业，优先选择当前剩余 CPU 最多、且内存足够的 worker。
3. 同等条件下优先选择能让作业使用更多独立物理核第一线程的 worker。
4. 单个作业不能跨 worker；64 CPU 作业需要一台拥有 64 个可用逻辑 CPU 的 worker。
5. 当前没有任何 worker 能容纳的合法作业保留在队列中，不拆小、不降核，也不静默
   修改 Agent 的资源请求。
6. 已经开始运行的作业不因新到达的大作业被抢占。

如果 Agent 同时提交四个 16 CPU 作业，四台空闲 worker 的剩余 CPU 相同，因此默认
各放置一个作业，以获得更多独立物理核和节点级内存带宽：

```text
worker 1: 16 CPU
worker 2: 16 CPU
worker 3: 16 CPU
worker 4: 16 CPU
```

如果 Agent 在同一批中同时提交 `64、32、16、16` CPU 四个作业，64 CPU 作业会先
获得完整 worker，随后依次安排较小作业。这就是要求 Agent 尽可能一次提交当前已知
独立工作的原因：调度器能先看到大作业，避免资源被小作业切碎。

### 4.3 后续到达的 64 CPU 作业

不永久浪费一台 worker。如果一个 64 CPU 作业较晚进入队列且没有完整空闲 worker，
调度器选择剩余运行作业最少的一台 worker 标记为 `draining`，停止向它分配新的小
作业，等已有作业自然结束后启动 64 CPU 作业。

这就是“整机作业保护”：不是永远空置一台机器，而是在大作业真实出现时有计划地排空
一台机器。它不会抢占或杀死正在运行的作业。

### 4.4 建议的 rlaunch 资源规格

当前 worker 使用：

```bash
rlaunch --cpu=64 --memory=140000 \
  --charged-group=ai4chem_agent_cpu_task \
  --private-machine=group \
  --mount=gpfs://gpfs1/liyuqiang:/mnt/shared-storage-user/liyuqiang \
  -- bash
```

如果资源配额允许，且不会因此减少可同时获得的 worker 数量，建议改为：

```bash
rlaunch --cpu=80 --memory=180000 \
  --charged-group=ai4chem_agent_cpu_task \
  --private-machine=group \
  --mount=gpfs://gpfs1/liyuqiang:/mnt/shared-storage-user/liyuqiang \
  -- bash
```

工具箱仍只向 Agent 和普通计算 reservation 开放 64 个逻辑 CPU、128000 MiB 内存。
按当前 cgroup 实测值，额外 16 CPU 和 72000 MiB 内存属于不可调度的安全余量。

当前实测 80 个逻辑 CPU 对应 40 个物理核。推荐把其中 16 个逻辑 CPU（8 个完整物理
核）设为隐藏的 control/headroom cpuset，只用于：

- 远端 SSH 和启动器；
- job supervisor 与状态/心跳线程；
- 文件系统、日志压缩和结果整理；
- 软件产生但未计入主计算线程数的辅助进程；
- 作业接近满载时保持节点可登录、可取消、可回收。

对 Agent 的资源合同不变：每台最多 64 CPU、128000 MiB。隐藏的 16 CPU 不能被
普通计算 reservation 使用。必须按完整物理核隔离，不能简单保留任意 16 个 SMT
线程，否则控制进程仍可能与计算线程共享物理核。

扩大到 80 CPU 主要提高可管理性和抗卡顿能力，不代表单个 64 CPU 科学计算自动变快。
worker 内实测 200000 MiB 相对 128000 MiB 可调度上限提供 72000 MiB 余量，可覆盖
supervisor、文件缓存、辅助进程和短时内存峰值。防止节点失去响应还必须依赖
walltime、心跳、进程组取消和 scratch/I/O 限制。

新 worker 启动后必须重新探测 cpuset、物理核/SMT 映射、内存 cgroup 上限、IP 和 SSH
目标，并更新本地 worker inventory。若 80 CPU 不是按完整物理核分配，隐藏 CPU 的
具体选择必须根据实际拓扑重新计算。

## 5. 调度算法

每个请求包含规范化后的资源需求：

```text
cpu_cores
memory_mb
gpu_count
runtime/software capability
job kind
```

内部调度流程：

1. 筛选健康且安装了目标 runtime/软件的节点。
2. 排除 CPU、内存、GPU 或并发作业数不足的节点。
3. 排除处于 `draining`、`quarantined` 或维护状态的节点。
4. 等待队列按 CPU、内存、提交时间排序。
5. 选择剩余 CPU 最多且内存足够的节点，优先保证大作业获得完整节点容量。
6. 同分时优先使用更多独立物理核第一线程，再采用稳定轮换规则。
7. 分配互不重叠的 CPU ID，并保持完整物理核与 NUMA 拓扑可追踪。
8. 在共享存储中原子写入 reservation 后才启动远端作业。
9. 作业结束、取消或确认启动失败后释放 reservation。
10. 每次资源状态变化都生成新的匿名 worker resource snapshot。

调度器需要同时处理 CPU 和内存，不能只按照 CPU 装箱。例如一台节点即使还剩 16 个
CPU，如果剩余内存不足，也必须选择下一台 worker。

## 6. 工具接口与资源反馈

不向 Agent 增加节点选择字段。现有接口在分布模式下透明变化：

- `execute_action`：自动选择节点，同步返回格式保持不变；
- `submit_action_batch`：保留现有同步行为以兼容旧任务；
- `submit_action_batch_async`：提交独立 Action 队列，立即返回 job ID、初始状态和资源快照；
- `submit_native_job`：创建共享作业目录后在自动选择的 worker 启动 supervisor；
- `submit_analysis_program`：采用相同调度路径；
- `get_execution_job`：通过共享状态文件查询，不需要节点参数；
- `cancel_execution_job`：写入共享取消标记，由所在节点的 supervisor 终止进程组；
- `get_execution_resources`：返回抽象总资源、单作业上限和当前可用量，不返回 SSH 信息。
- `wait_execution_events`：等待任一关注作业完成、失败、启动失败或超时；状态变化后
  立即返回事件列表以及四台 worker 的最新剩余 CPU/内存。

MCP 工具无法在 Agent 没有发起调用时主动向其推送消息。因此推荐交互循环为：

```text
Agent 规划独立作业及 CPU/内存
        ↓
submit_action_batch_async / submit_native_job
        ↓
wait_execution_events
        ↓
返回已完成/失败作业 + 最新 worker 剩余资源
        ↓
Agent 分析结果并按需提交下一批
```

提交合法但暂时放不下的作业保留在队列中。启动参数无效、请求超过单节点上限、远端
环境缺失等提交失败会立即返回，并释放任何临时 reservation。运行中的科学计算失败也
会释放资源，并在下一次 `wait_execution_events` 中连同最新资源快照一起返回。

工具结果和 provenance 应记录实际节点、CPU ID、资源 reservation、调度策略和失败阶段，
用于复现与审计；这些字段不要求 Agent 做调度决策。

## 7. 单节点兼容模式

提交脚本增加：

```bash
--execution-mode local
--execution-mode distributed
```

- `local` 为默认值，保持现有本机 `invoke_worker`、资源预算和 supervisor 行为；
- `distributed` 启用节点注册表、共享 reservation 和 SSH executor；
- 两种模式使用相同的 Agent 请求 schema；
- 同一 benchmark task 不需要因为执行模式不同而修改提示词或科学输入。

## 8. Worker 配置与代理

worker 数量由配置决定，不在代码中写死。为避免每次 rlaunch 后手工修改大量环境
变量，正式实现增加 `scripts/update_worker_inventory.py`。用户维护一个不提交 Git 的
本地 YAML，例如 `config/workers.local.yaml`：

```yaml
workers:
  - ssh: "ssh -CAXY <gateway-target-1>"
    available_cpu_cores: 64
    available_memory_mb: 128000
  - ssh: "ssh -CAXY <gateway-target-2>"
    available_cpu_cores: 48
    available_memory_mb: 100000
```

每个 worker 必须显式给出对计算开放的 CPU 和内存，不能静默使用探测到的全部资源。
不同 worker 可以设置不同上限。`name` 是可选字段；如果未给出，脚本通过 SSH 自动
读取远端 hostname，并生成稳定的匿名调度 ID，例如 `compute-1`。因此用户只传 SSH
连接方式和资源上限即可。

更新命令设计为：

```bash
python scripts/update_worker_inventory.py \
  --input config/workers.local.yaml \
  --output config/worker_inventory.local.json
```

脚本并行完成：

- 解析完整 `ssh -CAXY ...` 命令或纯 SSH target；
- 通过网关发现 hostname、FQDN、IP、cpuset、物理核/SMT、NUMA 和 cgroup 内存；
- 验证实际资源不小于声明的可调度资源；
- 通过网关读取 SSH host key，并生成项目专用的 local known-hosts 文件；
- 验证 `liyuqiang@IP` 直连、共享项目写权限和 framework 环境；
- 原子生成不含 API 密钥的 worker inventory；
- 对单台失败给出明确诊断，不把失败 worker 标记为可调度。

`config.local.env` 只需保留 inventory 路径和全局策略：

```bash
RCB_DISTRIBUTED_WORKER_INVENTORY="config/worker_inventory.local.json"
RCB_DISTRIBUTED_SCHEDULING_POLICY="largest_cpu_first"
RCB_DISTRIBUTED_REMOTE_INIT_SCRIPT_URL="http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh"
```

生成的 JSON 内部仍可映射到以下字段，但不再要求用户逐项填写：

```bash
RCB_DISTRIBUTED_WORKER_COUNT=N
RCB_DISTRIBUTED_WORKER_1_ID=compute-1
RCB_DISTRIBUTED_WORKER_1_NAME=...
RCB_DISTRIBUTED_WORKER_1_EXECUTION_SSH_TARGET=...
RCB_DISTRIBUTED_WORKER_1_LOGICAL_CPUS=80
RCB_DISTRIBUTED_WORKER_1_MEMORY_MB=200000
RCB_DISTRIBUTED_WORKER_1_AVAILABLE_CPU_CORES=64
RCB_DISTRIBUTED_WORKER_1_AVAILABLE_MEMORY_MB=128000
```

远端启动使用配置的代理初始化脚本：

```bash
RCB_DISTRIBUTED_REMOTE_INIT_SCRIPT_URL="http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh"
```

远端科学计算进程只继承经过允许的代理、runtime、缓存、许可证和 workspace 环境变量，
不继承 OpenAI 或 Judge 密钥。

## 9. 性能基准与策略校准

在固定大作业优先、最大剩余资源优先策略后，应使用当前仓库实际会调用的软件比较
不同布局，为后续策略优化提供依据：

| 布局 | 测试方式 |
|---|---|
| `4 × 16` 位于一台 worker | packing |
| `2 × 16` 位于两台 worker | 中间布局 |
| `1 × 16` 位于四台 worker | spread |

至少选择：

- 一个 ORCA 或 Gaussian 代表计算；
- 一个 xTB/CREST 代表计算；
- 一个明显使用大量内存或 scratch 的代表计算。

记录：

- 四个作业全部完成的 makespan；
- 每个作业 wall time；
- CPU 利用率和 CPU time；
- 峰值 RSS；
- 本地与共享存储 I/O；
- NUMA remote-memory 比例（环境允许时）。

建议判据：默认保持 spread/最大剩余资源优先。如果某个 runtime 的 spread 相对
packing 的 makespan 改善不足 10%，可以为它启用更紧凑的 packing；如果改善超过
15%，明确保持 spread；10% 到 15% 之间结合整机作业等待时间决定。阈值是初始运维
策略，不是科学结果的一部分，可以根据实测调整。

## 10. 实施与 Git 提交计划

确认方案后创建 `feature/distributed-compute-pool` 分支，并分阶段提交：

1. 节点配置模型、健康检查、资源合同和调度算法；
2. 节点感知的共享 reservation、NUMA/CPU 分配和状态记录；
3. `execute_action`、`submit_action_batch_async` 和事件等待接口的远端 worker 执行；
4. native/analysis job 的远端 supervisor、取消与异常清理；
5. Agent 指令、CLI 参数、状态显示和文档；
6. 单节点回归测试、模拟 SSH 测试和四台真实 worker 的性能基准。

每次提交只暂存本功能涉及的文件，不提交现有环境安装改动、缓存或
`config.local.env` 中的本地密钥与 worker 地址。

## 11. 已确认事项与剩余选择

已经确认：

- 当前 16 CPU/32000 MiB 协调节点全部保留给控制平面；
- Agent 只看到四台 worker 的计算资源；
- 2000 MiB/CPU 只是参考比例，不是严格限制；
- CPU 和内存独立计量，只要单节点剩余资源足够即可调度；
- 不永久保留空 worker；64 CPU 作业进入队列后采用 draining 排空一台节点；
- Agent 负责规划同时提交的独立作业及资源需求，调度器按 CPU/内存降序并优先选择
  剩余资源最多的 worker；
- 软件级布局差异通过真实基准校准；
- reservation 默认实现为项目级共享资源池并带租约/心跳，从而即使同时启动多个
  benchmark 评估也不会相互超额占用 worker。

建议将四台 worker 的 rlaunch 规格从 64 CPU/140000 MiB 调整到 80 CPU/180000 MiB，
但资源合同仍保持每台 64 CPU/128000 MiB。额外资源只作为控制与安全余量。如果扩大
规格会导致无法同时获得四台 worker、排队时间明显增加或计费不可接受，则保持当前
规格并降低可调度上限，而不应在 64 CPU/140000 MiB 容器中把全部资源暴露给计算。
