# Stage06/07 Agent 重构后的 Resume 机制设计

日期：2026-08-13
状态：设计草案，等待 Stage06/07 重构方案确认后实施
依赖文档：`STAGE06_07_AGENT_REDESIGN_PLAN_20260813.md`
上游设计：`../resume/STAGE00_05_RESUME_DESIGN_20260813.md`

## 1. 文档目的

本文件完成两件事：

1. 如实记录当前 Stage06/07 代码已经具备和缺少的恢复能力；
2. 为 Agent 化重构后的 Stage06/07 定义候选级、子阶段级 resume 合同。

本轮只完成设计，不修改 Stage06/07 代码。Stage06/07 即将按独立方案重构，因此不建议先给当前
`direct_api` 实现增加一套很快会废弃的恢复逻辑。正式实现应在 Agent 工作区、输出 schema 和权限边界
冻结后进行。

## 2. 当前实现的真实恢复能力

### 2.1 Stage00-05 当前机制

当前 `src/pipeline.py` 对 Stage01-05 使用微批次级 `stage_cache.json`：

- 只有整个微批次被标记为 `completed` 且 stage hash 一致时才整批复用；
- 一个论文发生客观执行失败时，微批次通常成为 `completed_with_errors`，恢复时整批重跑；
- Stage05 Router 和 Auditor 没有独立 checkpoint；
- Stage04 还存在论文 `deep_parse_failed` 被当作普通完成结果缓存的语义风险；
- Stage00 的选样排除主要依赖批次 manifest，没有跨整个 run root 的永久选择账本。

这些问题由 `STAGE00_05_RESUME_DESIGN_20260813.md` 统一解决。Stage06/07 应复用其中的 attempt、lease、
artifact manifest 和 failure classification 基础设施，而不是另建不兼容的状态系统。

### 2.2 当前 Stage06

当前 `src/stages/stage06_task_builder/stage.py` 对每个 Stage05 candidate 依次执行三次模型调用：

```text
shared record -> autonomous task -> reproduction task -> deterministic audit
```

现有模型客户端只会缓存一次成功的 `call_json` 响应，cache key 包含请求内容。它能在完全相同请求下偶然
减少重复调用，但这不是完整的 Stage06 resume，原因如下：

- 没有持久化候选状态机和当前有效 attempt；
- 三个调用没有显式依赖图，也没有可查询的子阶段状态；
- 产物只在三个调用都结束后写入正式 candidate 目录；
- 进程在中途退出时，没有可靠记录候选进行到了哪里；
- 失败记录只在整批函数收尾时写入 `build_results.jsonl`；机器突然退出时该记录也可能不存在；
- 没有 lease，两个进程可能同时构建同一 candidate；
- `task_pair_id` 仍可能由模型提供，不能稳定标识恢复对象；
- 没有验证缓存响应所依赖的论文、SI、工具箱、prompt 和 schema 是否仍全部有效；
- Stage06 结果由本轮输入整体覆盖写出，不能可靠合并历史成功候选和本轮恢复候选。

因此，当前 Stage06 的真实语义是“整个 Stage06 再运行，模型请求可能命中底层成功响应缓存”，不是
“从候选的最后一个安全 checkpoint 继续”。

### 2.3 当前 Stage07

当前 `src/stages/stage07_task_judge/stage.py` 对所有 Stage06 pass 结果重新执行：

```text
deterministic audit -> Judge API -> optional Gold Run -> release decision
```

当前没有 Stage07 cache 或 candidate/pair 状态文件：

- `pipeline.py` 每次到达 Stage07 都会再次调用 `run_stage07`；
- Judge 成功响应可能命中模型客户端缓存，但 precheck、写盘和 Gold Run 仍可能重做；
- Gold Run 没有稳定 job identity，重启后可能重复提交；
- `release_decisions.jsonl` 和 summary 只在整阶段结束后统一写出；
- `revise` 没有版本化修订链；
- 无法区分科学 reject、合同 reject 和外部执行失败的恢复策略。

结论：当前 Stage06/07 没有可依赖的正式 resume 机制。用户要求的恢复能力应直接落在重构后的
`06A-06F / 07A-07C` 架构上。

## 3. 设计原则

### 3.1 恢复单位是 candidate/pair，不是 paper 或 batch

Stage05 一篇论文最多向 Stage06 释放一个首选 candidate，但状态键仍必须包含 `candidate_id`。Stage06C
冻结 Public Spec 后才产生稳定 `pair_id`，Stage07 以 `pair_id + revision` 为恢复单位。

```text
Stage06A-06B key: paper_id + candidate_id + generation
Stage06C-06F key: candidate_id + generation + revision
Stage07A-07C key: pair_id + generation + revision
```

batch 只用于调度和汇总，不是完成事实来源。一个 Agent 失败不能让同 batch 的其他 candidate 重跑。

### 3.2 Resume 只恢复客观中断，不改变科学结论

普通 resume 自动处理：

- 从未开始；
- 进程、机器或 harness 中断；
- API 连接、限流、5xx、超时；
- 合规输出未写完或产物损坏；
- 临时文件系统、沙箱或调度器故障。

普通 resume 不自动重跑：

- `workflow_incomplete`、`workflow_conflicting`、`workflow_unrecoverable`；
- Stage06F 发现的真实 schema、证据、可评分性或泄漏缺陷；
- Stage07 的科学 `reject`；
- 已经完成且输入指纹仍有效的 Agent session。

修改 prompt、schema、输入证据、工具箱能力或科学规则属于重新评估。必须显式 invalidation，并创建新的
generation/revision，不能以 resume 名义覆盖旧结论。

### 3.3 文件产物不能代替事务性状态

Agent 可能生成了一半文件，也可能已经返回成功但调度器尚未登记。SQLite 状态库是当前有效状态的事实
来源，文件由 artifact manifest 校验。恢复前必须 reconciliation，不能仅以“目录存在”判断成功。

### 3.4 Agent session ID 不能成为唯一 checkpoint

Codex、Claude、OpenCode 等 harness 对原生 session resume 的支持和语义不同。正式机制必须保存：

- 固定输入 manifest 和 hash；
- prompt、schema、harness、模型和权限签名；
- stdout/stderr、native trace、final message 和结构化输出；
- AgentRunResult 和 artifact manifest；
- 当前子阶段的 attempt 状态。

harness-native session ID 只作为诊断信息。默认恢复策略是从该子阶段的冻结输入重新启动一个 Agent，
并复用此前已验证通过的子阶段输出，而不是要求继续一段不透明的远端对话。

### 3.5 Public/Hidden 隔离优先于节省调用

Stage06C 的公共规范一旦冻结，Stage06D 才能看到隐藏结果。恢复时绝不能把 Stage06D 的上下文或输出交回
Stage06C。若 Public Spec 因显式修订发生变化，必须创建新 revision，并使 Hidden Reference、物化产物和
所有 Stage07 结果失效；不得原地修改旧 revision。

## 4. 统一持久化模型

Stage06/07 复用 Stage00-05 计划新增的 resume 核心表，并扩展候选字段。统一由
`src/core/resume.py` 访问同一个 `run_root/resume/resume_state.sqlite`。现有
`paper_screening_registry.sqlite` 仍是跨运行的筛选与资产审计库，不承担 candidate lease 或 Agent attempt
调度；每个子阶段事务提交后，再把当前有效投影同步给 screening registry。

### 4.1 Work item 主键

```text
(run_id, stage, phase, paper_id, candidate_id, pair_id, generation, revision)
```

其中尚未生成 `pair_id` 的 Stage06A-06B 使用空值；Stage06C 成功后由代码根据 candidate 和 public spec hash
生成 `pair_id`。

### 4.2 状态枚举

子阶段统一使用：

```text
pending
running
succeeded
terminal_reject
needs_revision
retryable_failed
terminal_failure
blocked_by_upstream
stale
not_applicable
```

`terminal_reject` 是正常科学或合同结论；`terminal_failure` 仅用于达到重试上限且必须人工处理的执行问题，
不能伪装成科学 reject。

### 4.3 不可变 attempt

每次子阶段执行都新增 attempt，不覆盖历史：

```json
{
  "attempt_id": "uuid",
  "paper_id": "paper-id",
  "candidate_id": "candidate-id",
  "pair_id": null,
  "stage": "stage06",
  "phase": "workflow_extraction",
  "generation": 1,
  "revision": 0,
  "status": "retryable_failed",
  "failure_class": "agent_timeout",
  "retryable": true,
  "lease_id": "uuid",
  "input_fingerprint": "sha256",
  "runtime_fingerprint": "sha256",
  "started_at": "...",
  "heartbeat_at": "...",
  "finished_at": "...",
  "artifact_manifest_path": "...",
  "error": {}
}
```

### 4.4 Candidate 当前状态投影

`candidate_state.json` 作为人可读投影，由数据库原子生成，不作为唯一事实来源：

```json
{
  "paper_id": "paper-id",
  "candidate_id": "candidate-id",
  "pair_id": "generated-pair-id",
  "generation": 1,
  "revision": 0,
  "state": "stage07_pending",
  "stage06": {
    "workspace": {"status": "succeeded", "attempts": 1},
    "extraction": {"status": "succeeded", "attempts": 1},
    "public_spec": {"status": "succeeded", "attempts": 1},
    "hidden_reference": {"status": "succeeded", "attempts": 1},
    "materialization": {"status": "succeeded", "attempts": 1},
    "validation": {"status": "succeeded", "attempts": 1}
  },
  "stage07": {
    "precheck": {"status": "pending", "attempts": 0},
    "audit": {"status": "blocked_by_upstream", "attempts": 0},
    "postcheck": {"status": "blocked_by_upstream", "attempts": 0}
  },
  "updated_at": "..."
}
```

### 4.5 Lease 与并发领取

每个 candidate phase 使用带心跳的 lease。领取必须使用数据库事务：

```text
pending/retryable_failed
  -> compare-and-swap running + lease_id
  -> Agent/代码执行
  -> 原子提交结果和 artifact manifest
```

lease 保存 hostname、PID、boot ID、进程启动 ticks、harness 子进程 PID 和 heartbeat。恢复时只有确认 lease
失效后才能把 `running` 改成 `retryable_failed/interrupted_external`。这允许多个 Stage06/07 worker 并行，
同时避免同一 candidate 被重复领取。

## 5. 输入指纹与失效传播

每个 phase 的 cache key 包含自身直接输入和所有科学语义依赖。推荐依赖图：

```text
Stage05 approved candidate + Stage04 docs + frozen facts
  -> 06A workspace
  -> 06B workflow extraction
  -> 06C public spec
  -> 06D hidden reference
  -> 06E materialization
  -> 06F validation
  -> 07A precheck
  -> 07B audit
  -> 07C postcheck/release
```

最低指纹字段：

- `paper_id`、`candidate_id` 和 Stage05 candidate hash；
- 正文与全部 SI 的 document ID、SHA256、解析器版本和内容 index hash；
- Stage03 工具箱事实、catalog hash 和能力 schema hash；
- Stage04 parse facts 和资源预算 hash；
- prompt/version、输出 schema、确定性校验器 implementation version；
- Agent key、harness 版本、实际 provider/model、权限 profile；
- 直接上游阶段输出 hash；
- Stage06D 及其下游必须包含 frozen public spec hash；
- Stage07 必须包含整个 task pair manifest hash。

失效规则：

| 变化 | 最早失效点 | 传播范围 |
|---|---|---|
| 论文/SI 或 evidence index 改变 | 06A | 06A-07C |
| Stage05 candidate 改变 | 06A | 06A-07C |
| extraction prompt/schema 改变 | 06B | 06B-07C |
| public spec prompt/schema 改变 | 06C | 06C-07C，新 revision |
| hidden reference prompt/schema 改变 | 06D | 06D-07C，新 revision |
| renderer 改变 | 06E | 06E-07C |
| deterministic validator 改变 | 06F | 06F-07C |
| Stage07 audit prompt/model改变 | 07B | 07B-07C |
| worker 数、超时或 API endpoint 改变 | 不失效成功结果 | 只改变 runtime fingerprint |

工具箱 catalog 改变不能由普通 resume 静默重审。用户显式 invalidation 后，从 06A 或由 planner 确定的最早
依赖点建立新 generation，历史结果继续保留。

## 6. Stage06 各子阶段的 Resume

### 6.1 Stage06A Evidence Workspace Builder

恢复单位：candidate。

成功条件：

- source、frozen、contracts、instructions manifest 全部存在；
- 每个文件的大小和 SHA256 与 manifest 一致；
- 所有论文和 SI 文档均能解析；
- read/write allowlist 已生成；
- 工作区不包含其他 candidate、正式任务或隐藏 Judge 凭证。

恢复行为：

- 完整且 hash 一致：复用；
- 构建到一半：将临时目录归档到当前 attempt，重新确定性构建；
- 上游必要文档缺失：`blocked_by_upstream`，不启动 Agent；
- 输入文档永久不存在或 evidence ID 无法解析：生成明确的 terminal reject，不以异常退出。

工作区使用 `candidate_id/generation/revision` 隔离，并通过临时目录加原子 rename 发布。

### 6.2 Stage06B Workflow Extraction Agent

恢复单位：candidate + extraction phase。

成功条件：

- AgentRunResult 为成功；
- structured output 通过 schema；
- evidence ID、工作流 DAG、输入、参数和 claim 的确定性校验通过；
- trace、prompt、输入和输出 hash 已归档。

正常 `workflow_incomplete/conflicting/unrecoverable` 是 terminal reject，普通 resume 不重跑。harness 异常、
API 故障、超时、输出截断或缺文件为 retryable。相同输入连续两次合同错误后标记 `terminal_failure` 并进入
人工队列，不能自动变成 `workflow_incomplete`。

### 6.3 Stage06C Public Task Spec Agent

恢复单位：candidate + public spec revision。

成功提交顺序必须是：

1. Agent 输出到 attempt 临时目录；
2. schema、公开字段和无答案检查通过；
3. 代码计算 `public_task_spec_hash` 和 `pair_id`；
4. 以只读权限冻结 Public Spec；
5. 数据库事务记录成功和 artifact manifest；
6. 才允许 Stage06D 入队。

若进程在步骤 3-5 中断，resume 通过 hash 和 manifest reconciliation 判断是否完成提交；不能再次让模型
随意生成另一份规范。若必须修改 Public Spec，则创建 `revision + 1`，旧 revision 永不覆盖。

### 6.4 Stage06D Hidden Reference Agent

恢复单位：pair + public spec hash + revision。

Agent 使用独立 session 和独立只读视图。恢复调用只能读取 frozen Public Spec、workflow extraction 和结果
证据，不能读取 Stage06C 的可写目录或复用其会话。成功后校验：

- 未修改 Public Spec hash；
- 所有 conclusion、expected value 和 tolerance 有合法 source evidence；
- rubric 权重和为 100；
- 输出没有要求反向改变输入、结构、参数或任务范围。

若返回 `hidden_reference_conflicts_with_public_spec`，candidate 在该 revision 下 terminal reject。只有人工确认
重新设计公共任务时才能创建新 revision，从 Stage06C 开始，不能把它当作 API 故障自动重试。

### 6.5 Stage06E Renderer 与 Asset Materializer

恢复单位：pair + revision。该阶段是确定性代码，不调用 Agent。

- 先写临时 pair 目录；
- 生成 common、autonomous、reproduction、private 和 trace 文件；
- 建立完整 artifact manifest；
- fsync 后原子 rename 到 revision 目录；
- 目录存在但 manifest 不完整时归档残留并重新物化；
- 输入资产 hash 一致时不重复复制，可使用只读 hardlink/reflink，但 manifest 必须记录实际策略。

正式发布目录不在此阶段写入，因此重复 materialization 不会覆盖已发布 benchmark。

### 6.6 Stage06F Deterministic Validation

恢复单位：pair + revision + validator version。

验证结果本身可缓存，但输入必须是 Stage06E 整体 manifest hash。通过或发现真实合同缺陷均是稳定结果；
I/O 中断、依赖工具临时不可用才是 retryable。

`task_pair_built` 只在 06A-06F 全部成功后产生。任一子阶段 terminal reject 时，其后子阶段全部
`not_applicable`，但已有 attempt 和证据保留。

## 7. Stage07 各子阶段的 Resume

### 7.1 Stage07A Deterministic Precheck

恢复单位：pair + revision + precheck implementation version。

必须重新校验 Stage06F、evaluation schema/load、dry-run workspace、公开文件 allowlist、工具箱 snapshot 和
task ID 冲突。真实 precheck 缺陷为 terminal reject；临时磁盘、依赖服务或加载器执行故障为 retryable。

### 7.2 Stage07B Independent Audit Agent

恢复单位：pair + revision + audit phase。

Stage07 使用独立于 Stage06 的 session 和只读工作区。成功缓存至少保存：

- Stage06 pair manifest hash；
- Stage07 prompt/schema/harness/model/permission 签名；
- Agent trace、structured audit、usage 和 output hash；
- findings 与 source evidence 映射。

`pass`、`revise`、`reject` 都是成功产生的科学审计结论。只有
`agent_processing_failed`、API/harness 故障、输出合同失败才进入 retryable。

### 7.3 Stage07C Postcheck 与发布聚合

恢复单位：pair + revision。由确定性代码执行：

```text
07A reject                         -> rejected
07A pass + 07B reject              -> rejected
07A pass + 07B revise              -> needs_revision
07A pass + 07B pass + 07C pass     -> approved
07B/07C 客观失败                   -> retryable_failure
```

`release_decisions.jsonl` 和 summary 必须从所有 candidate/pair 的当前有效状态重新生成，不能只包含本次恢复
处理的子集，也不能因为同一 candidate 有多个 revision 而重复计数。

## 8. `revise` 的恢复语义

第一版 Agent 重构按主方案保持 `max_revision_rounds=0`，即只记录 `required_revisions`，等待人工确认。未来
启用受约束 repair 时，`revise` 不能作为普通失败重试：

1. Stage07 finding 保存 `allowed_patch_fields`；
2. 人工或策略批准后创建 `revision + 1`；
3. 新 revision 只允许 Repair Agent 修改批准字段；
4. 若 Public Spec 任一字段变化，重新冻结 hash，并使 06D-07C 全部重新运行；
5. 即使只修改 renderer 输出，也至少重新执行 06F 和完整 Stage07；
6. 每轮保留父 revision、finding、patch、前后 hash 和批准者；
7. 达到最多两轮仍未通过则 terminal reject，不无限循环。

任何 repair 都不能用隐藏答案选择公共输入、构象、位点、方法或参数。恢复调度器只执行已经批准的 revision，
不会自行扩大 `allowed_patch_fields`。

## 9. Gold Run 的作业级 Resume

Gold Run 第一版默认关闭。未来启用时应作为 Stage07C 之后的独立 evaluator-side phase，而不是把命令退出码
嵌在 Judge attempt 中。

每个 Gold Run 生成稳定 `gold_job_id`：

```text
hash(pair_id, revision, task_manifest_hash, runner_config_hash)
```

状态至少包括：

```text
pending / submitted / running / collecting / passed / failed_task
failed_infrastructure / cancelled / stale
```

恢复时先查询调度平台的 job identity：仍运行则继续监控，明确失败则按 failure class 处理，找不到且 lease
过期才重新提交。不得仅因本地进程重启就重复提交昂贵计算。trace、deliverables、评分结果和资源统计必须
完整校验后才能 `passed`。

## 10. 独立恢复入口

重构后建议提供：

```bash
python scripts/workflows/run_stage06_07_resume.py \
  --run-root runs/stage00-05-api-batches-10000-20260813 \
  --start-phase stage06A \
  --stop-phase stage07C \
  --stage06-agent codex \
  --stage07-agent opencode \
  --stage06-workers 2 \
  --stage07-workers 2 \
  --dry-run
```

去掉 `--dry-run` 后执行。可选 `--watch` 监听同一 run root 中后续新增的 Stage05 approved candidates。

参数建议：

```text
--candidate-id ID             只恢复指定 candidate，可重复
--batch ID                    限制外层批次
--retry-only                  只处理 retryable failure
--pending-only                处理 retryable 和 never-started
--invalidate-phase PHASE      显式创建新 generation/revision
--max-attempts N              客观执行失败预算
--watch                       持续接收新 Stage05 candidate
--dry-run                     只 reconciliation 和输出计划
```

`--watch` 不持有整个 run root 的排他锁；它使用调度器 lease 和 candidate phase lease，从而允许 Stage05 继续
写入新候选。一个 candidate phase 仍只能被一个 worker 领取。

每次启动先生成：

```text
run_root/resume/stage06_07_plan.json
run_root/resume/stage06_07_summary.json
run_root/resume/stage06_07_unresolved.jsonl
```

计划必须列出 reuse、retry、pending、blocked、terminal、stale 和 needs_revision 数量，并且在申请 Agent
资源前完成 reconciliation。

## 11. 与 Stage00-05 增量扩容的衔接

Stage00 从 10,000 扩展到 20,000 后，Stage06/07 不需要重扫或重建既有任务：

1. Stage00-05 planner 为新论文建立 Batch0011-Batch0020；
2. 新论文按顺序进入 Stage01-05；
3. Stage05 每产生一个完整 approved candidate，就以事务方式发布候选事件；
4. Stage06/07 `--watch` 或下次 resume 只领取从未见过的新 candidate；
5. 已 approved/rejected 的历史 candidate 在指纹未改变时保持不动。

Stage05 candidate 只有在 Stage05 Router、Auditor、合同校验和所有引用产物都完整后才能发布。半成品或
客观失败不能进入 Stage06 pending 队列。

## 12. 资产保留与清理

按上游策略，只有 Stage00-03 终止性淘汰的论文允许删除远端复制资产。进入 Stage04/05 并被 Stage06/07
消费的正文、SI、解析文本和证据必须保留，至少直到 candidate terminal 且满足保留政策。

可以清理：

- retry attempt 的临时目录和重复 stdout/stderr，经压缩归档后删除；
- 已有完整 manifest 的重复 materialization 临时目录；
- 超过保留期的 harness 本地缓存，但不能删除当前有效输出和 provenance。

不能清理：

- frozen Public Spec 及其 hash；
- Hidden Reference、evidence map 和 task pair manifest；
- 当前有效和历史 revision 的结构化结论；
- Stage07 findings、release decision 和修订链；
- 用于证明无泄漏、输入一致性和模型来源的 trace manifest。

若因存储压力需要删除全文或原始 PDF，应先导出可恢复的远端 URI、SHA256 和对象版本，并把状态标记为
`archived_recoverable`；恢复时先重新物化证据工作区，再决定能否复用下游结果。

## 13. 旧 Stage06/07 结果迁移

当前 direct-API 产物与新 Agent schema、权限隔离和确定性验证不等价，不能导入为新 Stage06/07 的
`succeeded`。迁移器应：

1. 原样保留旧 `build_results.jsonl`、task pair 和 `release_decisions.jsonl`；
2. 写入 `legacy_direct_api` provenance 和旧文件 hash；
3. 可将旧结果登记为 `legacy_unverified`，用于对照和人工参考；
4. 对仍有效的 Stage05 candidate 建立新的 Stage06A pending；
5. 不把旧 Judge pass 当作新架构的 `approved`；
6. importer 重复执行必须幂等，不覆盖旧文件。

这会增加一次重构后的正式构建成本，但能避免把未做到全文主动检索、Public/Hidden 隔离和强验证的旧结果
错误视为 benchmark-ready。

## 14. 失败分类

建议共享 `src/core/failure_classification.py`，至少区分：

| failure class | 示例 | 默认处理 |
|---|---|---|
| `agent_transport` | API 断连、5xx、限流 | retry |
| `agent_timeout` | harness 超时 | retry |
| `agent_process_crash` | 非零退出、进程被回收 | retry |
| `agent_output_incomplete` | 无输出、JSON 截断 | retry，有限次数 |
| `artifact_io` | 临时磁盘/rename 失败 | retry |
| `contract_violation_repeat` | 相同输入连续合同错误 | terminal failure/人工 |
| `scientific_incomplete` | 流程或输入真实缺失 | terminal reject |
| `scientific_conflict` | 证据冲突不可消解 | terminal reject |
| `public_hidden_conflict` | 结果证据要求反改公共规范 | terminal reject/revision |
| `deterministic_validation` | schema、泄漏、parity 缺陷 | reject 或 revision |
| `audit_reject` | Stage07 独立科学否决 | terminal reject |
| `external_interruption` | 主机重启、lease 失效 | retry |

错误分类规则必须由异常类型、HTTP 状态、harness 结果和确定性 validator 输出决定，不能让模型自行声明一个
执行故障是否 retryable。

## 15. 聚合与审计输出

Stage06 `build_results.jsonl` 每个 candidate 只保留一条当前有效投影，并包含：

- generation/revision、pair/task IDs；
- 各子阶段状态和当前 attempt；
- decision、reject reasons 和 validation；
- public spec、input、pair manifest hash；
- Agent/harness/model provenance；
- cache hit、attempt、token、成本和时长。

Stage07 `release_decisions.jsonl` 每个 pair 当前 revision 一条，并包含：

- precheck、audit、postcheck 和可选 Gold Run 状态；
- findings、required revisions 和 release decision；
- `benchmark_ready`；
- 当前/父 revision 和全部关键 hash。

历史 attempts 与 revisions 保存在 SQLite 和 append-only JSONL 中。summary 从当前有效投影重建，并明确：

- completed、completed_with_errors、running；
- pending/retryable/blocked/stale；
- workflow reject、validation reject、audit revise/reject、approved；
- Agent 调用、cache hit、token、成本、延迟和 failure class 分布。

## 16. 实施顺序

Stage06/07 的 resume 不应早于核心重构。建议将原重构计划的 Phase 5 细化为：

1. 先冻结 06A-06F、07A-07C schema、目录、权限和输入 hash 合同；
2. 复用 Stage00-05 的 work item、attempt、artifact 和 lease 基础设施；
3. 实现 candidate/revision 状态投影和 reconciliation；
4. 给每个 Agent session 接入独立 checkpoint；
5. 给 renderer、validator、precheck/postcheck 接入确定性缓存；
6. 实现独立 `run_stage06_07_resume.py` 和 `--watch`；
7. 实现旧 direct-API 结果只读 importer；
8. 最后再考虑受限 repair 和 Gold Run job resume。

建议本地 Git 提交顺序：

```text
feat(agent-resume): add candidate phase state and leases
feat(stage06): checkpoint extraction public hidden and materialization
feat(stage07): checkpoint precheck audit and release aggregation
feat(agent-resume): add watch planner and legacy importer
test(agent-resume): cover interruption isolation revision and idempotency
```

在用户确认前不创建这些提交，也不修改运行代码。

## 17. 测试与验收

### 17.1 中断恢复测试

- 分别在 06A-06F、07A-07C 每个子阶段强制终止进程；
- 恢复后只重跑中断的 candidate phase；
- 已通过子阶段的模型调用次数不增加；
- 机器 boot ID 改变后陈旧 `running` 能被回收；
- 同时启动两个 worker 不会重复领取同一 candidate；
- 状态写入前后任意 crash point 都能通过 reconciliation 得到唯一结果。

### 17.2 隔离与失效测试

- Stage06D 永远不能修改或覆盖 Public Spec；
- Stage06C 新 revision 会使 06D-07C 旧 revision 失效，但保留历史；
- Hidden Agent trace 不会进入 Public Spec Agent workspace；
- autonomous/reproduction 输入 hash 保持一致；
- prompt/schema/toolbox/文档变化只从正确的最早依赖点失效；
- 只修改 workers、timeout 或 endpoint 不重跑成功科学结果。

### 17.3 结论与重试测试

- `workflow_incomplete` 普通 resume 不重跑；
- API 504、超时、非法 JSON 和 harness crash 会有限重试；
- 相同输入连续合同错误不会无限重试；
- Stage07 `pass/revise/reject` 均视为有效审计结果；
- `revise` 创建新 revision，不覆盖旧 task pair；
- 旧 direct-API pass 不会被错误迁移为新 `approved`；
- summary 同时包含历史完成结果和本轮恢复结果，且每个 current candidate 只计一次。

### 17.4 验收条件

1. 任意子阶段中断后无需删除目录即可继续；
2. 一名 candidate 失败不影响同 batch 的其他 candidate；
3. 恢复不会重复已完成 Agent 调用或 Gold Run 作业；
4. Public/Hidden 隔离在恢复和 revision 流程中仍严格成立；
5. 所有客观失败都有 failure class、attempt、lease 和下一步动作；
6. 所有正常 reject、revise 和 approved 都有完整证据与 provenance；
7. Stage00 扩容产生的新 Stage05 candidate 能被 `--watch` 增量消费，历史 task 不重建；
8. 正式发布仍是独立、显式、原子操作，不由 resume 自动覆盖 `ResearchChemBench/tasks`。

## 18. 最终边界

- Stage00-05 resume 负责论文、文档、筛选结果和 Stage05 candidate 的可靠增量生产；
- Stage06 resume 负责把每个 candidate 从证据工作区推进到经过确定性验证的 task pair；
- Stage07 resume 负责独立审计、修订状态和发布判定；
- evaluation 负责执行和评分正式任务；
- 普通 resume 只恢复执行，不改变已有科学结论；
- 显式 invalidation/revision 才能触发科学重新评估；
- Stage06/07 当前 direct-API 版本保持现状，等待 Agent 重构时一次性实现上述机制。

## 19. 编码前需要确认

除 Agent 重构主方案第 14 节的设计决策外，resume 还需要确认：

1. 不给当前 direct-API Stage06/07 单独补临时 resume，直接在 Agent 重构中实现。
2. 默认从冻结输入重新启动失败的 Agent 子阶段；harness-native session ID 只作诊断，不作唯一 checkpoint。
3. Stage06C Public Spec 成功后严格冻结；任何公共字段变化都创建新 revision，并重跑 06D-07C。
4. 第一版 Stage07 `revise` 只记录并等待人工处理，`max_revision_rounds=0`，不自动 repair。
5. 旧 direct-API Builder/Judge 结果保留为 `legacy_unverified`，不直接迁移成 approved。
6. Gold Run 第一版保持关闭；以后启用时采用稳定 job ID 和独立作业级 resume。
7. `--watch` 可以与 Stage00-05 同时运行，但通过 candidate phase lease 保证不重复消费。

确认这些边界后，应先完成 Stage06/07 Agent 重构 Phase 0-4，再实现本文件定义的 Phase 5 resume。
