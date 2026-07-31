# 工具箱内部作业监督实现总结

## 1. 实现状态

已按照 `toolbox_internal_job_supervision_plan.md` 完成 native software job 和
programmable analysis job 的工具箱内部监督。新增公开 MCP 工具：

```text
wait_execution_jobs
```

Action batch 继续使用原有 `wait_execution_events`，没有把两套状态模型混在一起。
原有 `get_execution_job`、`collect_execution_job`、`cancel_execution_job` 和
`get_execution_resources` 均保留兼容。

## 2. 核心行为

- 一次等待可接收 1 到 128 个唯一 job ID，Agent 不能传入等待时间参数。
- 工具箱默认每 2 秒读取持久状态；内部检查不产生额外 MCP 调用或模型步骤。
- 首个 `success`、`failed`、`timeout` 或 `cancelled` 终态启动通知聚合。
- 默认稳定窗口为 60 秒，持续变化时最多聚合 300 秒，无终态时 3600 秒返回心跳。
- 新终态、排队转运行、worker 分配、reservation 释放和调度资源状态变化会重置稳定窗口。
- stdout/stderr 增长以及软件内部 SCF、优化或采样进度不会重置稳定窗口。
- 全部监控作业终态且资源连续两个快照稳定时可提前返回。
- 终态可见后最多等待 10 秒确认 reservation 释放；仍未稳定时返回明确 warning。

通知等待与计算调度完全解耦。部分结果返回时，其他运行作业不会暂停、取消或迁移；
终态作业的资源立即由原调度路径释放，分布式队列仍按 largest-CPU-first 和 draining
规则自动补位，不等待 Agent 再次调用工具。

## 3. 返回与自动收集

稳定返回包含：

- `newly_terminal_jobs`：本次观察到的新终态、机械科学状态、collection 路径；
- `running_jobs`：worker、CPU、内存和已运行时间，不含实时日志；
- `queued_jobs`：队列位置、资源请求和等待原因；
- `remaining_job_ids`：下一次批量等待的基础；
- `state_transitions`：稳定窗口内的关键状态和调度变化；
- `resource_snapshot`：返回时的本地预算或完整分布式资源池快照；
- `internal_check_count`、`wait_duration_seconds` 和聚合时长；
- `held_jobs`：首版固定为空，不实现未经评审的自动熔断。

终态作业在返回前自动生成 `collection.json`；analysis job 同时生成或更新
`artifact_manifest.json`。成功作业不返回大段 stdout。失败和超时作业只返回评测者控制的
日志尾部（默认 2000 字符）以及已有结构化诊断，完整日志和文件仍保存在 workspace。

## 4. 配置与提交入口

评测者控制以下参数：

| 配置 | 默认值 |
|---|---:|
| `job_event_settle_seconds` | 60 |
| `job_event_max_batch_seconds` | 300 |
| `job_wait_heartbeat_seconds` | 3600 |
| `job_internal_poll_interval_seconds` | 2 |
| `job_failure_tail_chars` | 2000 |

`scripts/submit_evaluation.sh` 新增公开参数
`--job-event-settle-seconds N`。其余高级参数可由对应的
`RESEARCHCHEMBENCH_JOB_*` 环境变量设置。有效策略写入 evaluation config、
`submission.json` 和每个任务的 `_meta.json`，并传给 MCP 子进程，不进入 Agent 的工具请求。

为兼容原有短时测试和人工配置，未显式设置心跳且 MCP timeout 小于 3600 秒时，有效心跳
自动收窄为 `MCP timeout - 1 秒`；显式值仍须小于 MCP timeout 且不小于聚合上限。

## 5. Agent 规则与降开销效果

初始指令、工具描述、软件目录、native quickstart 和提交返回的 `next_step` 已统一为：

1. 先提交当前已知的独立 native/analysis 作业；
2. 把所有 job ID 一次传给 `wait_execution_jobs`；
3. 部分返回后处理终态结果，再用 `remaining_job_ids` 加新 job ID 继续等待；
4. heartbeat 后直接继续等待；
5. 仅在失败深查或疑似卡死时调用单作业 `get_execution_job`；
6. 仅在需要完整清单时显式调用 `collect_execution_job`；
7. 禁止 shell sleep/循环/grep 轮询和重复资源查询。

trace 将一次内部等待记为一次监督工具调用，并额外汇总等待时长、内部检查次数、状态转换数
和终态数。内部轮询不会扩张 Agent 轨迹或消耗模型 token。

## 6. 静态失败预防

analysis preflight 新增两类确定性诊断：

- 拒绝无效的 `ctx.output(name).register()`，提示先写入 `ctx.output(name)`，再调用
  `ctx.register_output(name)`；JSON 可直接使用 `ctx.write_json(name, payload)`。
- JobContext 声明不匹配会同时返回声明名称、代码使用名称、大小写差异和可直接执行的精确修复。

这些检查发生在资源 reservation 和程序执行之前，用于减少失败后的日志检查、修复和重提轮次。

## 7. 执行模式兼容性

- local：沿用原有单任务资源预算和拒绝语义，只增加只读监督与批量通知。
- distributed SSH：读取共享 queue、reservation 和 status，不修改现有调度算法或远端进程。
- distributed Sandbox：只观察已同步到主节点的本地终态；远端 artifact 同步完成前仍不会暴露终态。
- coordinator：不增加主节点科学计算资源，主节点继续只运行 Agent、MCP 和调度服务。

## 8. 代码与 Git 记录

- `237606d`：请求模型、评测配置和分布式只读调度快照。
- `86084fa`：内部等待状态机、自动收集、MCP 工具和 JobContext 诊断。
- `75bfdeb`：Agent 指令、提交入口、工具目录、trace 指标和使用文档。

实现复用了现有 status、queue、reservation、resource snapshot 和 collection 接口，没有增加
常驻 watch 服务、消息队列或第二套调度器。核心状态字段集中定义，资源稳定和状态变化共用一套
快照签名，避免重复监督逻辑。

## 9. 验证结果

已验证：

- fake clock 覆盖部分终态、失败收集、日志增长、稳定窗口重置、聚合上限和 heartbeat；
- 真实 local analysis supervisor 提交、运行、终态和自动 collection；
- SSH 与 Sandbox 持久状态使用相同等待语义；
- distributed queue/reservation 只读快照和原调度回归；
- MCP 工具注册、runner 环境、提交脚本、trace 指标和 JobContext preflight；
- 相关回归 60 项通过；
- 完整测试运行结果为 503 项通过、7 项失败，其中 2 项是测试时临时 CPU 预算为 16 而用例固定
  断言默认 48，恢复默认后单独复跑通过。

剩余 5 项失败与本次修改无关，均来自当前工作区已有外部状态：

- LOBSTER smoke cache 缺少 `ICOHPLIST.lobster` 和 `DOSCAR.lobster`；
- ORCA OpenMPI 资源状态文件当前记录为 `fail`；
- 两组历史 evidence 的归档哈希与 manifest 不一致。

本次实现未修改或覆盖这些用户本地缓存、资源状态和历史证据文件。
