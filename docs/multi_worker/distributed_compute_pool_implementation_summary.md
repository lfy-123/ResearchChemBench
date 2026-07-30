# 分布式计算资源池实现总结

更新时间：2026-07-31

## 1. 实现结果

仓库现在同时支持两种执行方式：

- `local`：默认模式，保留原有单节点执行路径和资源预算行为；
- `distributed`：协调节点只运行 Agent、MCP、Judge 和调度器，科学计算自动发送到任意数量的已配置 worker。

单次科学计算不会跨节点。Agent 决定如何拆分彼此独立的科学工作以及每个作业申请的
CPU、内存；工具箱负责选择 worker、排队、预留、CPU 绑定、远端启动、状态查询、取消
和资源回收。Agent 看不到真实 hostname、IP 或 SSH target。

当前四台 worker 每台实际拥有 80 个逻辑 CPU 和约 200000 MiB 内存，仅暴露
64 个逻辑 CPU 和 128000 MiB 内存。Agent 可见的池总量是 256 CPU、512000 MiB，
单作业上限是 64 CPU、128000 MiB；2000 MiB/CPU 只是规划参考值。

## 2. 主要代码改动

### 2.1 Worker inventory

新增 `scripts/update_worker_inventory.py`：

- 输入任意数量的 SSH 连接和每台 worker 显式开放的 CPU/内存；
- 并行探测 hostname、直连 IP、cpuset、物理核/SMT、NUMA 和 cgroup 内存；
- 验证共享项目目录、framework Python 和直连 SSH；
- 生成项目专用 known-hosts 和原子更新的 inventory JSON；
- worker 名称可省略，调度只依赖自动生成的匿名 `compute-N` ID。

本地文件使用：

```text
.workers.local.yaml
.worker_inventory.local.json
.worker_known_hosts.local
config.local.env
```

前三个文件已加入 `.git/info/exclude`，`config.local.env` 包含 API 密钥和本地连接配置，
均不得提交 Git。

### 2.2 共享资源状态与调度

`researchchem_toolbox.distributed_pool` 在共享存储中维护：

- 全局 reservation；
- native/analysis 等待队列；
- reservation 和队列请求心跳；
- terminal/stale 状态清理；
- 匿名 worker 资源快照；
- 不重叠的 CPU ID 分配和 NUMA 均衡完整物理核选择。

等待作业按 CPU 降序、内存降序、提交时间排序。可立即运行的大作业不会被后提交的
小作业越过。如果大作业因已有作业造成的资源碎片暂时无法放入任何 worker，调度器会
选择一台当前运行作业较少、剩余资源较多的 worker 标记为 `draining`，停止向该节点
放置后续小作业；其他 worker 仍可继续运行能放下的任务。运行中的作业不抢占。

### 2.3 远端执行

预定义 Action、native software job 和 analysis program 都支持分布模式：

- 通过 SSH stdin 传递结构化启动 envelope，避免 shell 参数拼接；
- 远端使用与协调节点相同的共享项目路径和环境；
- 计算进程绑定 reservation 分配的精确 CPU ID；
- `memory_mb` 用于调度预留和软件自身内存参数；worker cgroup 是硬安全边界，不对
  分布式 Action 设置等于申请值的 `RLIMIT_AS`，避免 Gaussian、MPI 和数值库因额外
  虚拟地址空间需求在实际内存尚未超限时提前失败；
- 设置与申请 CPU 数一致的线程环境变量；
- 只传递允许的 runtime、缓存、许可证、workspace 和代理变量；
- 不向 worker 传递 OpenAI/Judge API 密钥；
- provenance 记录执行模式、匿名 worker ID、CPU ID、reservation 和资源请求；
- native/analysis supervisor 在 worker 上维护心跳、walltime、进程组取消和最终资源释放。

### 2.4 Agent 接口

新增异步 Action 接口：

- `submit_action_batch_async`：一次提交一批独立 Action，立即返回 batch ID；
- `wait_execution_events`：等待完成、失败、重排队等状态变化，并返回最新资源快照。

原有接口保持兼容：

- `execute_action` 在分布模式自动选择 worker；
- `submit_action_batch` 保留同步语义；
- `submit_native_job` 和 `submit_analysis_program` 返回 queued job；
- `get_execution_job`、`collect_execution_job` 和 `cancel_execution_job` 不需要节点参数；
- `get_execution_resources` 返回全池总量、单作业上限、实时可用量、队列数量和 draining 状态。

Agent 指令已区分本地与分布资源合同。分布模式明确说明全池 256 CPU，而不再错误地把
本地的 64 CPU 单作业上限描述为所有并发作业的总上限。

### 2.5 提交脚本

`scripts/submit_evaluation.sh` 和 `scripts/run_agent_eval.sh` 支持：

```bash
--execution-mode local
--execution-mode distributed
```

默认仍为 `local`。评估启动时会读取 `config.local.env`，并根据
`RESEARCHCHEMBENCH_PROXY_SETUP_URL` 或 `RCB_DISTRIBUTED_REMOTE_INIT_SCRIPT_URL`
自动加载代理脚本。

## 3. Git 版本

实现位于 `feature/distributed-compute-pool` 分支，按功能拆分提交：

```text
4976f2a docs: define distributed compute pool design
6a5c425 feat: add distributed worker inventory and reservations
9aba9e1 feat: execute predefined actions on compute workers
7614344 feat: add asynchronous distributed action batches
6d24d0c feat: dispatch native and analysis jobs to worker pool
dd50f77 feat: expose distributed execution mode to evaluations
dbb3189 test: include asynchronous execution tools
3878de5 fix: initialize proxy for evaluation launches
a1b99c3 feat: prioritize distributed native job queue
25ab859 fix: reject deterministic analysis script errors
440df25 fix: validate GoodVibes single-point suffixes
2c15f27 fix: require exact evaluation deliverable paths
8399b1b docs: summarize distributed compute pool implementation
a9925c3 fix: preserve workspace paths on compute workers
430c5d0 fix: expose analysis job directory aliases
fcad15f fix: stop queued evaluations after interrupt
935418d fix: treat distributed memory as a scheduler reservation
28838e6 docs: record distributed end-to-end fixes
88b5cac fix: use distributed pool capacity for sync batches
b83d730 fix: terminate remote process groups on cancellation
77ce79f docs: record distributed throughput and cancellation validation
b48a4be docs: sync GoodVibes suffix guidance
f873d59 fix: make long async batches cancellation safe
```

## 4. 已完成验证

真实 worker 验证包括：

- xTB 预定义 Action 在远端成功，H2 总能量为 `-0.981983694723 hartree`；
- 四个异步 xTB Action 自动分散到四台 worker，全部完成后资源恢复为 256 CPU；
- analysis program 在远端看到与 reservation 完全一致的 CPU affinity；
- native xTB job 在远端使用 4 CPU 成功完成，并得到相同 H2 总能量；
- 每次验证结束后 reservation 均归零。

最新相关定向测试通过 59 项；长异步等待、父进程退出和 reservation 回收修复又通过
15 项，CLI/MCP/runner 相关回归通过 25 项。按当前协调节点真实资源覆盖为 16 CPU、
32000 MiB 后，完整测试得到 `469 passed, 8 failed`。其中一个本功能引起的 GoodVibes
生成文档未同步问题已经修复并单独验证；两个失败只是该次资源覆盖与测试固定断言的
默认 48 CPU 合同不一致，去掉覆盖后均通过。其余失败来自仓库当前环境状态，包括历史
replay/smoke archive hash、缺失 LOBSTER 缓存文件，以及现有
`toolbox_resource_status.json` 中 ORCA OpenMPI 资源状态为 `fail`，不属于本次分布调度改动。

## 5. 使用方式

更新 worker：

```bash
.envs/researchchembench/bin/python scripts/update_worker_inventory.py \
  --input .workers.local.yaml \
  --output .worker_inventory.local.json \
  --known-hosts .worker_known_hosts.local
```

提交分布式评估：

```bash
bash scripts/submit_evaluation.sh submit \
  --execution-mode distributed \
  --session rcb_distributed_example \
  TASK_ID
```

查看评估状态：

```bash
bash scripts/submit_evaluation.sh status --run-root WORKSPACES_DIR
tmux attach -t rcb_distributed_example
```

单节点运行不需要改配置：省略 `--execution-mode`，或显式传入
`--execution-mode local`。

## 6. 端到端评估记录

简单任务使用 `PV_CC_CO_Pathway_Selectivity_Reproduction`，最终成功运行记录为：

```text
workspaces/distributed-simple-pv-cc-co-rerun3/
```

- 评估进程状态：`completed`；
- 时长：409.5 秒；
- Chemistry MCP 工具调用：19 次，失败 0 次；
- GoodVibes native job：`job_abefe9ab21a1469b9930f33b8e412d50`；
- 执行节点：`compute-4`；
- GoodVibes 处理 14 个结构，远端运行成功并生成结构化结果；
- 任务报告复现 C-C 势垒 13.86 kcal/mol，并与来源标注的 C-O 18.0 kcal/mol 比较；
- 运行结束后全池恢复为 256 CPU、512000 MiB，reservation 和等待队列均为 0。

测试过程中发现并修复了三类会造成无效远端作业的问题：

1. `JobContext.input(name).path`：`input` 已直接返回 `pathlib.Path`；
2. 把条件表达式写入 f-string format specifier，程序可编译但运行时必然抛出 `ValueError`；
3. GoodVibes `--spc _DLPNO` 会寻找双下划线文件，正确形式是
   `frequency_DLPNO.out` 配合 `--spc DLPNO`。

这些问题现在都在提交前预检或 Agent 指令阶段处理。该次 Agent 将四个任务专用证据表
写到了 `outputs/` 而不是要求的 `report/`；调度和科学软件执行成功，但这些路径不满足
benchmark 的精确 deliverable contract。后续 Agent 指令已明确要求终止前检查每个
required path，不能用 `outputs/` 中的同名文件替代 `report/` 路径。

三个复杂任务的最终运行记录在提交后继续补充。

复杂任务首次启动时又发现并修复了三项端到端问题：

1. 远端 Action envelope 遗漏 `RESEARCHCHEMBENCH_WORKSPACE`，导致 worker 无法解析
   workspace-relative XYZ 路径，并把路径字符串误当成 SMILES；修复后真实远端 xTB
   路径测试在 `compute-4` 得到 `-72.152552492371 hartree`。
2. 分析程序使用了直观但此前未提供的 `ctx.input_dir()` / `ctx.output_dir()`；现在
   `JobContext` 同时提供这些兼容方法和 `inputs_dir` / `outputs_dir` 属性。
3. `cli_eval` 原先一次性把全部任务 future 提交到线程池，中断当前任务后队列中的后续
   任务仍会启动；现在只维持最多 `max_concurrent_runs` 个已提交 future，收到 SIGINT
   后不再启动新任务，并在 batch report 中记录尚未启动项为 `cancelled`。

第二次复杂任务启动验证了内存语义修复：此前 Gaussian 的 `%Mem=8192MB` 与
`RLIMIT_AS=8192MB` 重叠，运行库开销使 9 个优化都在约 1 秒内报
`galloc: could not allocate memory`。取消分布模式的该虚拟地址空间硬限制后，真实
Gaussian HF/STO-3G 烟雾测试在 `compute-3` 使用 4 CPU、8192 MiB 请求成功得到
`-1.11675930751 hartree`。

后续吞吐和取消验证又发现并修复两项问题：

1. 同步 `submit_action_batch` 在分布模式仍按主节点的 48 CPU 本地预算限制并发；现在
   它根据实时 worker slot 做放置、等待和重排队，本地模式的原有预算路径不变。
2. 取消评估时，本地 SSH/MCP 结束后远端 Gaussian 进程组可能继续运行。远端启动器
   现在设置 Linux parent-death signal，并把 SIGINT/SIGTERM 逐层传播到 worker 和
   科学软件进程组；`run_external` 在中断异常下也会 TERM/KILL 整个进程组。真实取消
   烟雾测试中，reservation 立即释放，6 秒后 worker 上对应 launcher、Gaussian 和
   link 进程全部消失。

第三次复杂任务运行记录为：

```text
workspaces/distributed-complex-e2e-rerun3/
```

首个任务已经同时在四台 worker 上运行 9 个 Gaussian 几何优化，每个请求 16 CPU、
32000 MiB，总计 144 CPU、288000 MiB；四台 worker 分别放置 2、2、2、3 个作业。
所有 reservation 均正常心跳，checkpoint 持续更新。但长作业暴露出事件等待接口的
效率问题：`wait_execution_events` 最多只允许等待 60 秒，并在没有新事件时重复返回
全部 9 个 item。约 24 分钟内 Agent 已进行 46 次轮询、累计约 265 万计费 token；继续
运行可能在科学计算完成前耗尽 300 轮或上下文，因此按测试规则主动停止该次运行。

停止过程进一步验证并修复了两个生命周期边界：

1. 事件等待上限扩展为 600 秒；无事件超时只返回每种状态的数量，不再重复全部 item，
   Agent 指令和提交结果都明确要求长计算使用 600 秒等待。
2. 异步 Action batch supervisor 现在设置 Linux parent-death signal，MCP/evaluator
   退出后不会成为孤儿进程。没有持久化 job 状态且创建者 PID 已死亡的 Action
   reservation 会立即回收；native/analysis job 仍由远端状态文件和心跳保护。

停止后精确检查四台 worker，属于该 workspace 的 launcher、Gaussian 和 link 进程
均为 0；孤儿 supervisor 清理后资源池恢复为 256 CPU、512000 MiB、0 reservation。
真实 parent-death 回归测试验证 supervisor 会在拥有它的 MCP 父进程退出后自动结束。

修复后的正式复杂任务记录为：

```text
workspaces/distributed-complex-e2e-rerun4/
tmux: rcb_distributed_complex_e2e_rerun4
hourly monitor: rcb_monitor_distributed_complex_rerun4
```

三个任务仍按顺序运行，每小时监控一次。最终状态、科学产物和评分将在三个任务全部
结束后补充。
