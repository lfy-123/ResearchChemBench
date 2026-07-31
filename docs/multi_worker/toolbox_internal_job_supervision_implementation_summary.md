# 工具箱内部作业监督第二版实现总结

> 2026-08-01 后续修正：ORCA 4/8 核真实复测发现，第二版最初的完整 SMT sibling
> 分配会让多个 MPI rank 共享物理核。当前 inventory 更新逻辑已改为自动检测 SMT，
> 配置 64 logical CPU 时向 Agent 暴露 32 physical cores，并只选择每个物理核的一条
> 线程。软件分类和未来扩展建议见 `software_cpu_topology_guidance.md`。

## 1. 完成范围

本次按照 `toolbox_internal_job_supervision_plan.md` 第二版逐项完成以下修改：

1. 把 evaluator-controlled 稳定监督从 native/analysis 的 `wait_execution_jobs` 扩展到
   Action batch 的 `wait_execution_events`；
2. 修复同一物理核心的 SMT sibling 被两个分布式作业同时占用的问题；
3. 强化 Agent 的计划优先、完整批次一次提交、pilot 复用和禁止主动轮询规则；
4. 补齐 analysis program 的 JobContext `.path`、运行时 API 属性、目录输出预检；
5. 更新轨迹统计、inventory 生成脚本和使用文档。

保留原有 local、distributed SSH 和 distributed Sandbox 三条路径。没有增加 ORCA 或其他
软件专用并发上限，没有替 Agent 选择科学参数、自动重试、自动修改输入或跨节点运行单个作业。

## 2. 实施过程与 Git 记录

实现过程中反复对照方案的目标、非目标和验收条款，分两个阶段保存 Git：

- `97cee26 fix: isolate distributed jobs by physical CPU core`
  - 更新方案为第二版实施基线；
  - inventory 新增 `compute_core_groups`；
  - reservation 按物理核心组隔离 SMT sibling；
  - 奇数 logical CPU 请求阻塞同组未使用 sibling；
  - SSH/Sandbox inventory 生成脚本同步支持新字段。
- `8a00e05 feat: stabilize asynchronous toolbox supervision`
  - Action 稳定等待、紧凑结果和 artifact handoff；
  - evaluator-controlled 公共监督策略；
  - Agent 完整批次与分层计划指令；
  - Action 监督轨迹指标；
  - analysis API/JobContext/目录输出预检；
  - 对应测试与提交文档。

用户已有的环境 requirements、缓存状态、worker/sandbox 本地配置和 `config.local.env` 修改均未
纳入这两个提交。

## 3. SMT 物理核心隔离

### 3.1 inventory

`compute_cpu_ids` 继续表示可向作业暴露的 logical CPU。新增的
`compute_core_groups` 保存它们的物理核心关系，例如：

```json
{
  "compute_cpu_ids": [6, 70, 32, 96],
  "compute_core_groups": [[6, 70], [32, 96]]
}
```

旧 inventory 没有该字段时退化为原有 logical CPU 粒度，保持兼容。更新脚本生成的新
inventory 会显式保存核心组。

### 3.2 reservation

- 调度器只从完全空闲的物理核心组分配 CPU；
- 一个作业可使用同组的全部 SMT threads；
- 同组 sibling 不会分配给另一个作业；
- 奇数请求只把所需 CPU ID 传给作业，同时在 reservation 中记录并阻塞剩余 sibling；
- allocation 新增 `reserved_cpu_ids`、`physical_core_groups` 和
  `blocked_sibling_cpu_ids`；
- 作业结束后整组释放。

该修改保留 arbitrary CPU request、largest-CPU-first、fill/draining 和单作业不跨节点语义。

## 4. Action 稳定监督

`wait_execution_events` 现在与 `wait_execution_jobs` 共用以下评测者控制参数：

| 参数 | 默认值 |
|---|---:|
| settle | 60 秒 |
| maximum batch | 300 秒 |
| heartbeat | 3600 秒 |
| internal poll | 2 秒 |

请求中的旧 `timeout_seconds` 仅作兼容解析，不能缩短稳定窗口。

具体返回边界为：

1. item 的成功、失败、超时或取消启动聚合；
2. 新终态、queued-to-running、worker 分配和 reservation/资源状态变化重置稳定计时；
3. 资源变化本身不会在首个终态前唤醒 Agent；
4. 排队 item 在资源释放后立即自动补位，不等待稳定窗口结束；
5. 所有 batch 终态且资源连续两个快照稳定时提前返回；
6. 其他情况在稳定 60 秒、达到 300 秒上限、heartbeat 或监督错误时返回。

工具返回时，未完成进程继续运行。返回值包含：

- `newly_terminal_items`：紧凑 ActionResult、错误、worker、结果和 output artifacts；
- `running_items`、`queued_items`；
- `remaining_batch_ids`、`next_sequences`；
- `state_transitions`、资源快照、内部检查次数和等待时长。

因此 Agent 不再需要直接读取 `outputs/action_batches/*/status.json` 才能取得结果或 artifact。

## 5. Agent 编排规则

统一指令现在明确要求：

- 计算前先形成依赖有序的简洁计划，区分 screening、refinement、validation 和 final analysis；
- 识别独立作业和由结果解锁的后续阶段；
- 同一独立 Action 阶段先生成完整且唯一的 item 列表，再一次提交一个 async batch；
- 不通过拆分重叠 batch 制造并发，容量不足由全局队列处理；
- pilot 结果必须复用，最终批次排除已完成输入；
- 使用稳定等待工具，禁止 shell sleep、循环 grep、重复资源查询和直接状态文件监督。

提交时会对完全相同的 item inputs 生成非阻断 warning，保留 Agent 最终判断权。

## 6. Analysis program 失败预防

### 6.1 JobContext

提交前会拦截：

- `ctx.input(...).path`；
- `ctx.output(...).path`；
- `ctx.output(...).register()`；
- 文件/目录输出 helper 与声明类型不匹配。

目录输出新增明确契约：

```python
bundle = ctx.output_directory("bundle")
# write files under bundle
ctx.register_output("bundle")
```

请求中对应声明使用 `kind="directory"`。注册和 collection 会记录目录文件数、总字节数、
确定性 tree hash，并拒绝空 required directory 或 symlink。

### 6.2 自动 API 属性探测

preflight 从 AST 提取可静态解析的 import alias 和属性链，例如：

```python
from rdkit.Chem import AllChem
AllChem.SomeFunction(...)
```

`AllChem.SomeFunction` 会在所选 runtime 中自动探测，无需完全依赖 Agent 手写
`required_symbols`。显式声明和自动发现会合并后验证，不存在的 API 在 reservation 和程序
启动前返回 `runtime_symbols_missing`。

### 6.3 结果交接

`wait_execution_jobs` 的新终态 analysis 结果现在附带紧凑 `declared_outputs`，包括名称、
workspace path、semantic/media type、file/directory kind、大小、hash 和验证状态，减少额外
collection 和手工复制步骤。

## 7. 轨迹指标

`evaluation/trace.py` 新增：

- `action_batch_wait_call_count`；
- `action_batch_wait_seconds`；
- `action_batch_wait_internal_check_count`；
- `action_batch_wait_transition_count`；
- `action_batch_wait_terminal_count`；
- native/analysis 与 Action 合并后的 `managed_supervision_*` 指标。

工具箱内部每次 poll 不写独立 MCP 事件，因此不会直接增加模型轮次或上下文 token。

## 8. 验证结果

### 8.1 定向测试

- distributed pool：14 项通过；
- Action/native/analysis supervision、JobContext 和 trace：61 项通过；
- 跨模块回归（调度、提交脚本、SSH/Sandbox、workspace）：通过；
- Python compileall 和 `git diff --check`：通过。

### 8.2 真实 SSH inventory 与 reservation

重新并行探测四台 worker 后，每台为：

- 80 logical CPU 可见；
- 64 logical CPU 对 Agent 可调度；
- 32 个双线程 `compute_core_groups`；
- 128000 MiB 可调度内存。

真实 reservation 测试提交了多个 1-CPU 请求。同一 worker 上相邻请求分别获得不同物理
核心；每个请求只暴露一个 logical CPU，同时正确阻塞 sibling。释放后资源池恢复为
256 logical CPU、0 active reservation。

### 8.3 真实 SSH Action 集成

在 SSH pool 提交两个独立 `calculate_energy/ase_emt` item：

- 两个 item 分别运行于 `compute-3` 和 `compute-4`；
- 两者均成功并返回数值结果与 output artifact；
- `wait_execution_events` 一次返回两个终态；
- 返回后资源池恢复为 256/256 logical CPU，0 active reservation。

集成证据保存在：

```text
workspaces/toolbox_supervision_integration_v2/
```

### 8.4 完整测试套件

第一次按当前进程实际 16 核亲和性运行得到 510 passed、7 failed。两个失败仅因测试固定断言
默认 48 核预算，而本次运行临时覆盖为 16；恢复 48 核预算单独复跑后通过。因此功能有效结果为
512 项通过，剩余 5 项均来自本次修改前已有的外部状态：

- LOBSTER smoke cache 缺少 `ICOHPLIST.lobster` 和 `DOSCAR.lobster`；
- `toolbox_resource_status.json` 中 ORCA OpenMPI runtime 当前为 `fail`；
- execution failure replay 与 native smoke 两组历史 evidence 的归档文件和 manifest 不一致。

本次未修改或伪造上述缓存、资源状态和历史证据。

## 9. 后续端到端验证

代码完成后将重新提交以下两个曾用于观察监督行为的 SSH 任务：

1. `Heterobiaryl_PV_Reproduction_01_Protonation`；
2. `GEOM_Hierarchical_Conformer_Reranking_Reproduction`。

两项任务完成后，需要继续对照方案分析真实轨迹中的 Action 批次完整性、wait 调用次数、
内部 poll、SMT allocation、worker 利用率、重复计算、输入修复和科学工具客观失败。该结果将在
独立轨迹分析报告中记录，不把尚未产生的端到端结论提前写入本实现总结。
