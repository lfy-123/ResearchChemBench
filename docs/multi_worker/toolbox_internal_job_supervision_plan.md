# 工具箱内部作业监督与稳定窗口修改方案

状态：待用户确认，尚未修改功能代码

方案日期：2026-07-31

基线版本：第六版本（多机 CPU 初版代码）

## 1. 背景

当前分布式资源池已经能够把一个评估任务中的独立 Action、原生软件作业和分析程序
调度到任意数量的 CPU worker。单个计算不跨节点，协调节点只负责 Agent、MCP、Judge
和调度。

当前执行层的问题不在 worker 调度，而在 Agent 仍需主动监督异步作业：

- 反复调用 `get_execution_job`；
- 使用内置 shell 执行 `sleep` 后检查 Gaussian/ORCA 日志；
- 对已经进入终态的作业逐个调用 `collect_execution_job`；
- 在作业释放资源后重复查询 `get_execution_resources`。

最近一次端到端复杂任务共完成 258 个模型步骤，其中监督、查询、收集和取消相关步骤
约占总 token 的 50.7%；把重试和输入修复也计入后约占 59.9%。主要开销来自每个监督
步骤重新读取已经增长到约 90 万 token 的模型上下文。

本方案把机械性的等待、轮询、终态聚合、资源稳定确认和结果收集移到工具箱内部。Agent
只在出现需要科学决策的稳定状态更新时重新获得控制权。

## 2. 目标

1. 工具箱内部监督所有已经提交的 native/analysis 异步作业。
2. 正在运行的计算在工具返回期间继续运行，不暂停、不迁移、不取消。
3. 作业终态触发通知聚合；资源变化本身不单独唤醒 Agent。
4. 终态作业立即释放资源，排队作业立即自动补位，不等待 Agent。
5. 默认等待作业和调度状态连续 60 秒稳定，再一次性返回。
6. 返回时明确列出新终态、正在运行、排队和预留扩展的 held 作业。
7. 自动收集终态作业的机械结果和失败诊断，减少单独工具调用。
8. 保留当前 `local` 模式和 `distributed` 模式的执行语义。
9. 不替 Agent 修改科学参数、选择软件、自动重试或解释科学结论。

## 3. 非目标

本次修改不实现以下功能：

- 单个 Gaussian、ORCA、CP2K 等计算跨节点运行；
- Redis、Kafka、外部消息队列或独立回调服务；
- 自动修改结构、方法、基组、电荷、多重度或收敛参数；
- 单次失败后自动重新提交；
- 改变现有 worker inventory、SSH 连接、CPU 绑定和放置算法；
- 把协调节点资源加入科学计算池；
- 评估级 pause/resume。作业监督状态可以为以后实现 resume 提供基础，但不在本次范围。

## 4. 核心设计决定

### 4.1 返回边界

主要原则为：

> 作业终态负责触发 Agent 通知，资源状态作为通知内容返回；资源变化本身不唤醒 Agent。

具体事件规则如下。

| 事件 | 是否触发返回流程 | 行为 |
|---|---|---|
| `running -> success` | 是 | 进入状态聚合窗口 |
| `running -> failed` | 是 | 进入状态聚合窗口并生成失败诊断 |
| `running -> timeout` | 是 | 进入状态聚合窗口并生成超时诊断 |
| `running -> cancelled` | 是 | 进入状态聚合窗口 |
| `queued -> running` | 否，但会重置稳定计时 | 记录自动补位和 worker 分配 |
| 日志、SCF 或优化步变化 | 否 | 不影响稳定计时 |
| CPU/内存可用量变化 | 否，但会进入最终资源快照 | 不单独唤醒 Agent |
| 排队请求被调度 | 否，但会重置稳定计时 | 记录状态转换 |
| 连续一小时没有终态 | 是 | 返回紧凑 heartbeat |
| MCP 监督器或状态文件异常 | 是 | 立即返回监督错误 |
| 整个资源池不可用 | 是 | 立即返回基础设施错误 |

### 4.2 调度和通知解耦

作业进入终态后执行顺序必须是：

```text
作业进入 success/failed/timeout/cancelled
        │
        ├── 立即写入终态
        ├── 立即释放 CPU/内存 reservation
        ├── 调度器立即尝试运行排队作业
        ├── 工具箱继续观察状态变化
        └── 状态稳定后一次性通知 Agent
```

稳定窗口只延迟通知，不延迟资源回收和排队作业启动。不得为了等待 Agent 而人为保留
空闲 CPU。

### 4.3 正在运行的任务

`wait_execution_jobs` 是只读监督操作。调用期间：

- 已在 worker 上运行的 supervisor 和科学软件进程保持运行；
- SSH 连接、远端临时目录和 reservation 生命周期不改变；
- worker 绑定的 CPU ID 和内存请求不改变；
- 其他排队作业仍由现有 largest-CPU-first 调度器处理；
- 工具退出或返回不会向运行任务发送信号。

工具返回 Agent 时，仍在运行的任务继续运行。下一次等待应把返回的
`remaining_job_ids` 和 Agent 新提交的作业 ID 合并后传入。

## 5. 稳定窗口算法

### 5.1 评估器控制参数

新增以下配置，均由评估器控制，不允许被评估 Agent 在工具请求中缩短：

```yaml
job_event_settle_seconds: 60
job_event_max_batch_seconds: 300
job_wait_heartbeat_seconds: 3600
job_internal_poll_interval_seconds: 2
job_failure_tail_chars: 2000
```

- `job_event_settle_seconds`：连续无调度状态变化的时间，默认 60 秒；
- `job_event_max_batch_seconds`：从第一个终态事件开始的最大聚合时间，默认 300 秒；
- `job_wait_heartbeat_seconds`：没有终态事件时的最长静默等待，默认 3600 秒；
- `job_internal_poll_interval_seconds`：工具箱内部读取状态的间隔，默认 2 秒；
- `job_failure_tail_chars`：失败作业返回的 stdout/stderr 最大尾部字符数。

提交脚本公开 `--job-event-settle-seconds N`，高级参数可以保留在评估配置或环境变量中。
所有实际值写入运行 `_meta.json`，保证可审计。

### 5.2 状态签名

工具箱每次内部检查生成一个紧凑的调度状态签名，包括：

- 每个被监控作业的 `status`；
- `compute_worker_id`；
- reservation ID 和是否已经释放；
- 分布式队列请求状态和排队位置；
- worker 的 `scheduling_state`；
- active reservation 数量和 queued request 数量。

不把以下内容放入状态签名：

- stdout/stderr 内容；
- 日志文件大小；
- SCF 迭代、优化步、频率进度；
- CPU 使用率瞬时值；
- 运行时间增长。

这样正在正常计算的作业不会因为日志持续输出而永远无法达到稳定状态。

### 5.3 聚合流程

1. 工具开始等待并记录所有作业初始状态。
2. 没有终态事件时，工具持续内部检查，不返回 Agent。
3. 发现第一个新终态作业时，记录 `aggregation_started_at`，启动 60 秒稳定计时。
4. 稳定窗口内如果发生新的终态、`queued -> running`、worker 分配或 reservation
   释放，重置 60 秒稳定计时。
5. 日志和数值计算进度变化不重置稳定计时。
6. 连续 60 秒状态签名不再变化时返回。
7. 如果状态持续变化，达到 300 秒最大聚合时间后强制返回当前汇总，防止 Agent 长时间
   无法处理已经完成的结果。
8. 如果所有被监控作业都已经终止，且连续两次资源快照一致，可以提前返回，不必继续
   等待完整 60 秒。
9. 如果一小时内没有任何终态事件，返回一次 heartbeat。若没有 `suspected_stalled`
   或基础设施错误，Agent 必须直接再次等待。

### 5.4 资源稳定确认

终态事件后，工具箱最多等待 10 秒确认：

- 对应 reservation 已删除或标记释放；
- 排队任务已经完成可立即进行的补位；
- 连续两个资源快照一致。

若 10 秒后仍不一致，允许返回，但必须增加：

```json
{
  "resource_snapshot_stable": false,
  "resource_snapshot_warning": "terminal status is visible but reservation release is still converging"
}
```

不得把不稳定快照伪装成最终可用资源。

## 6. 排队任务自动补位

### 6.1 默认行为

已经成功提交并进入 distributed queue 的任务在资源释放后自动补位，继续使用现有规则：

1. CPU 请求从大到小；
2. 同 CPU 请求按内存从大到小；
3. 再按提交时间排序；
4. 优先填充能够容纳请求的 worker；
5. 保留当前 draining 机制，避免小作业永久碎片化 worker；
6. 不抢占运行中的作业；
7. 单个任务不跨节点。

失败、超时或取消不会暂停整个队列。单个作业终止后，其他合法排队作业应立即尝试运行。

### 6.2 无法自动补位的情况

- 后续任务尚未被 Agent 提交；
- 后续任务依赖刚完成的科学结果；
- 提交请求无效，因此从未进入队列；
- 当前任何 worker 的剩余资源都不足以放置排队请求；
- worker 不健康或不可调度。

这些情况在稳定返回中明确呈现，供 Agent 决定下一步。

### 6.3 相同失败的熔断

第一阶段不实现自动熔断，以保持修改简单并避免误停无关计算。接口中预留 `held_jobs`
字段，初始始终为空。

后续可以增加可选保护：同一软件、同一输入模板指纹在 60 秒内出现至少 3 次相同机械
错误时，仅暂停尚未运行的相同模板作业，并返回 Agent；其他软件和其他模板不受影响。
这一扩展必须单独评审，不能包含在首版实现中。

## 7. 新 MCP 工具

### 7.1 工具名称

新增：

```text
wait_execution_jobs
```

现有接口继续保留：

- `get_execution_job`：失败诊断或疑似卡死时查看一个作业；
- `collect_execution_job`：需要完整文件清单时显式调用；
- `cancel_execution_job`：取消一个具体作业；
- `get_execution_resources`：任务开始或显式重新规划时使用。

### 7.2 请求模型

首版保持简单，不增加消息队列或永久 watch 服务：

```json
{
  "job_ids": [
    "job_<32 lowercase hex>",
    "job_<32 lowercase hex>"
  ]
}
```

约束：

- 至少 1 个、最多 128 个 job ID；
- ID 必须唯一；
- 所有作业必须属于当前 workspace；
- Agent 不能覆盖 settle、heartbeat 或内部 polling 参数；
- 上一次返回的 `remaining_job_ids` 是下一次调用的基础；
- Agent 新提交作业后，将新 ID 与 remaining 列表合并。

### 7.3 返回模型

```json
{
  "status": "success",
  "return_reason": "settled_state_update",
  "settled_for_seconds": 60,
  "aggregation_duration_seconds": 108,
  "resource_snapshot_stable": true,
  "newly_terminal_jobs": [],
  "running_jobs": [],
  "queued_jobs": [],
  "held_jobs": [],
  "remaining_job_ids": [],
  "state_transitions": [],
  "summary": {},
  "resource_snapshot": {},
  "recommended_action": "process_terminal_results_then_wait_remaining"
}
```

`return_reason` 取值：

- `settled_state_update`；
- `all_terminal`；
- `aggregation_time_cap`；
- `heartbeat`；
- `monitor_error`；
- `resource_pool_unavailable`。

### 7.4 新终态作业

每个新终态作业返回：

```json
{
  "job_id": "job_...",
  "label": "P2_PyPy_TS",
  "status": "failed",
  "previous_status": "running",
  "worker_id": "compute-2",
  "resource_limits": {
    "cpu_cores": 16,
    "memory_mb": 32000,
    "gpu_count": 0
  },
  "scientific_validation_status": "not_reached",
  "failure_diagnostic": {},
  "collection_manifest": "outputs/execution_jobs/job_.../collection.json"
}
```

成功作业不返回大段 stdout。失败、超时作业只返回有限尾部和结构化诊断。完整内容仍保留
在 workspace。

### 7.5 正在运行的作业

返回所有仍运行作业的紧凑状态：

```json
{
  "job_id": "job_...",
  "label": "P1_frequency",
  "status": "running",
  "worker_id": "compute-3",
  "cpu_cores": 16,
  "memory_mb": 32000,
  "elapsed_seconds": 1540
}
```

不返回实时日志和迭代历史。

### 7.6 排队作业

```json
{
  "job_id": "job_...",
  "label": "DLPNO_P2_TS",
  "status": "queued",
  "queue_position": 1,
  "cpu_cores": 64,
  "memory_mb": 128000,
  "queue_reason": "no_worker_currently_has_64_free_cores"
}
```

### 7.7 状态转换

返回稳定窗口中的调度变化：

```json
{
  "job_id": "job_...",
  "from": "queued",
  "to": "running",
  "worker_id": "compute-2",
  "trigger": "resources_released"
}
```

不强制推断某个具体终态作业与补位作业的一一因果关系，除非 reservation/queue 记录能够
可靠提供该信息。

## 8. 自动收集

新工具对本轮新终态作业执行现有 collection 逻辑：

- 写入或更新 `collection.json`；
- 对 analysis program 生成 artifact manifest；
- 返回 collection manifest 路径、文件数量和机械验证状态；
- 不向模型返回完整文件列表；
- 不解释能量、频率、势垒或化学结论。

Agent 只有在确实需要完整输出清单时才单独调用 `collect_execution_job`。

## 9. Agent 使用规则修改

初始指令和工具描述增加以下强制规则：

1. 提交两个或以上异步作业后，调用 `wait_execution_jobs` 统一等待。
2. 当前已经确定且彼此独立的作业应全部提交；容量不足时由 distributed scheduler 排队。
3. 禁止用内置 shell 执行 `sleep`、循环 `grep` 或直接读取运行中日志进行监督。
4. 普通 heartbeat 且没有 stalled/error 时，直接再次等待，不逐个查询作业。
5. `get_execution_job` 只用于新失败作业的深入诊断，或工具明确标记的疑似卡死作业。
6. 使用等待结果中的资源快照，不在每次终态后重复调用 `get_execution_resources`。
7. 不直接读取 `_toolbox_catalog.json`；只使用渐进式发现工具。
8. 先处理 `newly_terminal_jobs`，提交由结果解锁的新任务，再将新 ID 和
   `remaining_job_ids` 合并等待。

## 10. 减少重复校验和输入修复

`submit_native_job` 和 `submit_analysis_program` 已经在内部调用对应 validator。修改工具
说明：

- 正常路径直接调用 `submit_*`；
- 提交前内部校验失败时不启动计算，返回结构化错误；
- `validate_*` 只用于主动 dry-run 或复杂错误排查。

增加两项静态校验：

1. 检测无效的 `ctx.output(name).register()` 调用，返回正确的
   `write_text` + `ctx.register_output(name)` 示例；
2. 在 JobContext 声明不匹配时，同时返回声明名称、代码使用名称和大小写差异。

工具箱不自动修改 Agent 代码，只返回精确、紧凑的修复建议。

## 11. 代码修改点

### 11.1 MCP 模型与实现

- `chemistry_toolbox/mcp/open_execution.py`
  - 增加内部等待循环、状态签名、稳定窗口和自动收集；
  - 复用 `_read_status`、`_execution_status_axes`、`_resource_availability` 和 collection
    逻辑；
  - 不创建新的作业 supervisor。
- `chemistry_toolbox/mcp/open_tools.py`
  - 注册 `wait_execution_jobs`；
  - 增加紧凑工具描述。
- 对应请求模型文件
  - 新增 `JobWaitRequest`；
  - 限制 job ID 数量、格式和唯一性。

### 11.2 配置传递

- `evaluation/config.py`
  - 新增 settle、max batch、heartbeat、poll interval 默认值。
- `evaluation/run_task.py`
  - 把评估器控制值传给 MCP 进程；
  - 写入 `_meta.json`。
- `scripts/submit_evaluation.sh`
  - 增加 `--job-event-settle-seconds`；
  - 生成 evaluation config。
- `scripts/submit_evaluation.md`
  - 补充参数和行为说明。

### 11.3 Agent 指令与目录

- `evaluation/instructions_tmpl.py`
  - 增加统一等待和禁止 shell 轮询规则。
- `chemistry_toolbox/src/researchchem_toolbox/catalog.py`
  - 把“显式轮询”说明替换为批量稳定等待。
- `chemistry_toolbox/mcp/software_catalog.py`
  - 更新 native execution prompt。
- native/analysis submission 的 `next_step`
  - 从 `get_execution_job` 改为 `wait_execution_jobs`。

### 11.4 轨迹与结果统计

- `evaluation/trace.py`
  - 把 `wait_execution_jobs` 计为监督工具；
  - 一次内部等待只记录一个 MCP 调用；
  - 记录等待时长、内部检查次数、聚合状态变化数量，但不为每次内部检查写独立工具事件。

## 12. 兼容性

### 12.1 分布模式

读取共享 reservation、queue 和 job status，能够返回匿名 worker 状态和全池资源快照。
不改变当前调度算法。

### 12.2 本地模式

读取相同的 job status，返回本地预算和 active job 状态。首版不为 local 模式增加新的
分布式队列语义，原有资源拒绝行为保持不变。

### 12.3 旧接口

所有旧工具继续存在，现有调用方不被破坏。新 Agent 指令优先使用新等待工具。

## 13. 测试方案

### 13.1 单元测试

1. 一个作业成功，其他作业继续运行，返回中正确分组；
2. 一个作业失败，自动生成诊断和 collection manifest；
3. 终态后排队作业自动进入 running，稳定计时被重置；
4. 状态连续 60 秒不变后返回；
5. 持续变化达到 300 秒后按 cap 返回；
6. 一小时无终态返回 heartbeat；
7. 所有作业终态且资源稳定时提前返回；
8. 日志变化不重置稳定计时；
9. 重复、非法、跨 workspace job ID 被拒绝；
10. 工具返回不影响运行 supervisor PID 和远端进程；
11. local/distributed 资源快照均正确；
12. 取消作业后排队补位和状态汇总正确。

测试中使用可注入时钟或较短参数，不能真实等待 60 秒或一小时。

### 13.2 集成测试

1. 四台 worker 提交多个短作业和长作业；
2. 人工让一个作业失败，确认其他运行作业不受影响；
3. 确认释放资源后排队作业自动补位；
4. 确认 Agent 只收到一次聚合返回；
5. 确认返回列出 running、queued 和 terminal 作业；
6. 取消一个分布式作业，确认远端进程、scratch 和 reservation 清理；
7. 停止整个评估，确认现有全局清理逻辑仍生效。

### 13.3 回归测试

- 现有 distributed pool 测试；
- open execution contract 测试；
- async Action batch 测试；
- submit evaluation 脚本测试；
- workspace stop/cleanup 测试；
- 单节点 runner 测试。

## 14. 验收标准

功能验收：

- 返回部分结果时，其他运行作业保持运行；
- 返回中完整列出 running 和 queued 作业；
- 终态后排队任务自动补位，不等待 Agent；
- 默认连续 60 秒稳定后聚合返回；
- 资源快照与 reservation 状态一致；
- 不改变现有单节点运行路径。

效率验收以最近复杂任务轨迹为参考：

- Agent shell `sleep` 轮询次数降为 0；
- 正常作业不再逐个调用 `get_execution_job`；
- 大部分终态作业无需单独 `collect_execution_job`；
- 监督相关模型步骤减少至少 60%；
- 总模型步骤预计从 258 降至 170 以下；
- 总缓存 token 预计降低 40% 以上；
- worker 利用率不因 60 秒通知稳定窗口降低。

## 15. 实施顺序

用户确认后按以下顺序修改，每个阶段独立提交 Git 版本：

1. 增加请求模型和 `wait_execution_jobs` 核心等待逻辑；
2. 增加稳定窗口、资源稳定确认和自动 collection；
3. 暴露评估配置和提交脚本参数；
4. 更新 Agent 指令、工具目录和 next-step 文本；
5. 增加 JobContext 静态修复诊断；
6. 完成单元和回归测试；
7. 在 local 模式执行短作业验证；
8. 在 distributed 模式执行多作业补位与聚合验证；
9. 使用一个较简单 benchmark 任务测试 Agent 轨迹；
10. 对比修改前后的工具调用、模型步骤和 token 指标；
11. 编写实现总结并提交最终版本。

## 16. 第六版本基线说明

第六版本保存当前“多机 CPU 初版代码”，包括：

- local/distributed 双执行模式；
- 任意数量 worker inventory；
- largest-CPU-first 资源调度和 draining；
- Action、native job、analysis program 远端执行；
- CPU 绑定、worker 本地 scratch、取消和资源回收；
- 异步 Action batch 和事件等待；
- 提交脚本分布模式参数与文档；
- 默认 Agent 最大步骤 600。

本文件描述的 native/analysis 作业内部稳定等待尚未包含在第六版本中。只有用户确认本
方案后才开始修改功能代码。
