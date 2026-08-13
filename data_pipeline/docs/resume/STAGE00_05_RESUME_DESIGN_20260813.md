# Stage00-05 论文级 Resume 机制设计

日期：2026-08-13
状态：已确认并于 2026-08-13 完成 Stage00-05 首版实现
范围：`data_pipeline` Stage00-05、外层批次控制器、微批次调度器、筛选 registry 和 MinerU 沙箱池
明确不包含：Stage06 Task Builder 与 Stage07 Task Judge 的代码改造

Stage06/07 的后续恢复设计见
`../stage0607/STAGE06_07_RESUME_DESIGN_20260813.md`。

## 1. 目标

当前实现能够复用完整成功的微批次，但还不能可靠恢复一次因机器重启、API 故障、沙箱回收或 MinerU
失败而中断的长任务。本设计将 Stage00-05 的恢复单位从“整个微批次”下沉到“论文或文档”，达到：

1. 已成功完成的结果不重复调用模型、不重复解析 PDF；
2. 因客观原因失败的论文自动重新入队；
3. 尚未来得及处理的论文自动重新入队；
4. Stage04 只重跑 MinerU 失败或缺失的文档，成功的正文和 SI 继续复用；
5. 上游恢复后，原来被阻塞的下游论文自动继续处理；
6. 机器突然重启后能够识别陈旧的 `running` 状态；
7. 同一运行目录可以把累计采样目标从 10,000 扩展到 20,000 或更大，并且只复制从未选择过的论文；
8. 每次尝试、失败原因、结果来源和恢复代次均可审计；
9. 正常科学拒绝不会因 resume 被重新判断，除非用户显式要求失效某个阶段。

## 2. 核心语义

### 2.1 `--total` 是累计成功纳入筛选的唯一论文目标数

在同一个 `run_root` 下，`--total` 表示该运行目录计划成功物化并纳入筛选的累计唯一论文数，不是本次
新增数。实现上先建立稳定的 `target_slot_ordinal=1..total`；某个远端对象永久不可用时可以为原 slot 选择
替代对象，但该对象的历史选择身份仍永久保留并继续参与去重。

例如：

```text
第一次：--total 10000 --batch-size 1000
生成并处理 Batch0001-Batch0010，共 10,000 篇唯一论文。

第二次：--resume --total 20000 --batch-size 1000
冻结 Batch0001-Batch0010；追加 Batch0011-Batch0020；
只复制不在全局选择账本中的 10,000 篇新论文。
```

若 `--total` 等于已有累计目标，只恢复未完成和客观失败项；若大于已有目标，则先恢复旧任务，再按差额
追加新批次。若小于已有累计目标，默认拒绝执行，避免隐式截断历史；缩容必须使用单独的显式管理命令，
且不删除历史审计记录。

### 2.2 三种结果必须分开

| 类型 | 示例 | Resume 行为 |
|---|---|---|
| 终止性科学结论 | 无计算内容、软件不覆盖、Stage05 正常 reject | 直接复用，不重跑 |
| 可继续结论 | pass、needs_builder_review、software_coverage_probable | 直接复用，并释放下游 |
| 客观执行失败 | API 连接失败、HTTP 5xx、超时、沙箱回收、MinerU 无有效输出 | 自动重试 |

`uncertain` 是否重试由阶段合同明确规定，不能与 API 失败混为一类。模型正常返回的“不确定”是科学结果；
模型没有产生合规响应则是执行失败。

### 2.3 Resume 与重新评估不同

Resume 默认使用该批次创建时冻结的科学配置、prompt 版本、工具箱快照和输入 hash，只允许更新运行参数：

- API 地址、密钥和有序 fallback；
- worker 数和并发数；
- 超时、有限重试和退避参数；
- 沙箱 CPU、内存、生命周期和池大小；
- 日志级别。

模型、prompt、筛选阈值、工具箱能力快照或输入文档发生改变时，不能悄悄覆盖旧结论。用户必须显式执行：

```text
--invalidate-stage stage03
```

新结果写入新的 `resume_generation`，旧结果保留为历史尝试。

## 3. 持久化结构

### 3.1 全局选择账本

在 `run_root/resume/resume_state.sqlite` 的 `corpus_selections` 表中保存所有曾被 Stage00 选择过的论文，
即使论文随后被筛除并删除本地 PDF，选择记录仍永久保留。最低字段如下：

```text
dataset
source_main_uri                 PRIMARY identity component
normalized_doi
source_record_key
paper_id
source_sha256                   复制成功后写入
selection_id                    每次选中远端对象的全局唯一 ID
target_slot_ordinal             稳定目标槽位，决定批次归属
selection_event_ordinal         整个 run_root 内单调递增的选样事件序号
replaces_selection_id           永久失效对象被替换时记录
outer_batch_id
selected_at
copy_state
local_assets_state
```

唯一约束按以下优先级建立：

1. `(dataset, source_main_uri)`：远端对象的权威选择身份；
2. 有 DOI 时同时建立 `(dataset, normalized_doi)` 辅助唯一索引；
3. 复制完成后记录 SHA256，用于发现同一内容的不同远端路径，但不能在复制前依赖 SHA256。

如果 URI 与 DOI 的唯一约束发生冲突，记录为 `identity_conflict` 并进入人工审计，不覆盖已有论文。

### 3.2 论文/文档阶段状态

统一状态键：

```text
(outer_batch_id, stage, paper_id, document_id_or_empty, config_fingerprint)
```

状态枚举：

```text
pending
running
succeeded
terminal_reject
forwarded
retryable_failed
blocked_by_upstream
not_applicable
stale
```

Stage02、03、05 以论文为单位；Stage01 和 Stage04 同时保存文档状态与论文汇总状态；Stage00 同时保存
远端选择和文件复制状态。

每次执行另写一条不可变 attempt：

```json
{
  "attempt_id": "...",
  "resume_generation": 2,
  "stage": "stage04",
  "paper_id": "paper_...",
  "document_id": "doc_...",
  "status": "retryable_failed",
  "failure_class": "mineru_timeout",
  "started_at": "...",
  "finished_at": "...",
  "runtime_fingerprint": "...",
  "artifact_manifest": [],
  "error": {}
}
```

`run_root/resume/resume_state.sqlite` 是该运行目录选样、调度、attempt、artifact 和 lease 的事务性事实来源。
现有 `paper_screening_registry.sqlite` 继续保存跨运行的论文筛选事实和资产删除审计，但不负责并发任务领取；
resume 成功提交阶段结果时再把当前有效投影同步给 screening registry。两者都必须通过明确接口写入，业务
阶段不能自行解释或拼接状态。

`resume_state.sqlite` 建议增加以下表：

```text
corpus_selections
stage_work_items
stage_attempts
artifact_manifests
run_leases
resume_generations
```

### 3.3 文件仍是可读审计产物

SQLite 是事务性事实来源，同时原子导出：

```text
run_root/resume/resume_plan.json
run_root/resume/resume_summary.json
run_root/resume/attempts.jsonl
run_root/resume/unresolved.jsonl
run_root/resume/selection_ledger.jsonl
```

原有每阶段 `decisions.jsonl` 和 `stage_summary.json` 继续存在，但由最新有效论文状态重新聚合生成，不能使用
简单追加造成重复论文。

## 4. 启动与崩溃识别

批处理进程启动时创建 run lease：

```text
owner_pid
hostname
boot_id
process_start_ticks
heartbeat_at
command_hash
resume_generation
```

每 30 秒刷新一次。满足任一条件时，旧 `running` 自动归类为 `interrupted_external`：

- PID 不存在；
- PID 已被复用且进程启动时间不一致；
- 系统 `boot_id` 变化；
- 跨机器恢复且旧心跳超过阈值；
- 心跳超时且不存在有效锁持有者。

只以 PID 文件判断不够。进程正常退出时记录 `completed`、`failed` 或 `interrupted_signal`；机器重启等无法
执行 `finally` 的情况由下一次启动修复状态。

同一 `run_root` 同时只能有一个 Stage00-05 调度 lease。Stage04 沙箱池可以由该调度器拥有独立子 lease，
防止两个 resume 进程重复领取同一文档。

## 5. Resume 规划算法

启动后先执行只读 reconciliation，再提交任务：

1. 读取全局选择账本、批次配置快照、阶段状态和落盘产物；
2. 校验每个成功结果的输入 hash、配置 hash 和必需产物是否存在；
3. 将陈旧 `running` 改为 `retryable_failed/interrupted_external`；
4. 把有合规终止结论的论文标为可复用；
5. 把客观失败、产物缺失和从未出现的输入标为 pending；
6. 根据上游最新有效结果重建阶段依赖；
7. 若累计目标增大，追加 Stage00 新批次；
8. 输出 `resume_plan.json`，其中明确 reuse、retry、pending、blocked、new 五类数量；
9. 非 `--dry-run` 时领取任务并运行；每个任务完成后立即 checkpoint；
10. 每个阶段结束后按 `paper_id/document_id` 重建聚合文件和摘要。

微批次只是本次调度的临时分组。恢复时可把来自不同旧微批次的 pending 项重新组成 10 篇一组，不改变
论文身份和历史结果，也不要求重复运行同组内已成功论文。

## 6. Stage00 恢复与增量扩容

### 6.1 已有批次和目标槽位不可变，新增批次只追加

外层批次具有稳定编号和选区：

```text
Batch0001: target slot ordinal 1-1000
...
Batch0010: target slot ordinal 9001-10000
Batch0011: target slot ordinal 10001-11000
```

从 10,000 扩到 20,000 时，不重新生成前十个配置，不改变原有 `run_id`、论文归属和 Stage00 manifest；
只创建 Batch0011-Batch0020。新增批次配置应引用全局选择账本快照，而不是只串联前一个批次的 manifest。

### 6.2 去重不能依赖本地 PDF

Stage00-03 的终止性拒绝可能删除 `stage_00_remote_corpus/corpus/<paper_id>`，因此扩容时不能扫描现存目录
判断重复。选择前先查询永久账本：

```text
candidate remote URI
  -> 已在 corpus_selections：跳过
  -> DOI 与历史论文冲突：跳过并记录 alias/conflict
  -> 从未选择：事务性 reserve，再执行复制
```

`reserve` 必须先于远端复制，避免并发选择同一对象。复制失败保留 reservation 并标记
`copy_retryable_failed`；下次 resume 重试同一论文，不用另一篇替换它。只有明确的远端对象永久消失且达到
配置的放弃策略时，才把该 selection event 标记为 terminal，并为同一个 `target_slot_ordinal` 绑定一个新的
selection event。旧 URI/DOI 仍永久留在账本中并继续排除。这样一个批次始终表示 1000 个成功目标槽位，
不会因少数远端坏对象改变 Batch 编号或论文归属。

### 6.3 Stage00 论文级状态

- 主文和所有远端已知 SI 复制成功：`succeeded`；
- 已确认没有 SI：仍可 `succeeded`；
- 主文或已确认存在的 SI 复制失败：`retryable_failed`，占用原目标槽位并优先恢复；
- 只写了一部分文件或机器重启：检测 `.partial`，校验后续传或清理该论文 partial 再重试；
- 已有文件 hash 与账本一致：复用并把目标槽位记为 `materialized`；
- 文件已因正常淘汰删除：`local_assets_state=pruned_terminal`，选择身份仍保留，不重新复制；
- 文件意外丢失但后续仍需处理：`local_assets_state=missing_required`，重新复制该论文，而非选择新论文。

`remote_order` 使用持久化 cursor 加账本排除；cursor 只能作为加速提示，账本才是去重事实来源。
`seeded_sample` 不能继续按每次请求的 `N` 调用一次随机抽样，而应为每个远端对象计算稳定优先级：

```text
priority = sha256(dataset_snapshot_id + seed + normalized_source_identity)
```

Stage00 持久化远端候选目录的 snapshot ID、对象 identity 和 priority，按该稳定顺序填充目标槽位。扩容时
冻结已有槽位，只从账本未出现的对象中继续选择。远端后来新增的对象不会重排旧批次，只能参与新的目标
槽位；需要对新增对象重新构造完全可比的随机总体时，应建立新的 run root，而不是用 resume 改写历史样本。

## 7. Stage01 恢复

Stage01 包含论文包整理、补充材料补全和 GROBID/pdftotext 低成本解析。恢复单位为文档：

- 复用质量检查通过且输入 SHA256、parser 版本和配置 hash 一致的标准化文本；
- 网络补充材料获取失败、GROBID 连接失败、超时、沙箱回收为 `retryable_failed`；
- 确认无补充材料是正常结论，不重试；
- GROBID 失败但 pdftotext 成功且达到当前质量门时，是成功结果；
- 正文或任一已知 SI 最终未成功时，论文状态为 `retryable_failed`，不能进入 Stage02；
- 文档成功后重新计算论文包汇总，只有完整包才释放 Stage02。

现有 Stage01 通过论文删除策略保持不变，但客观失败论文不得删除源 PDF/SI。

## 8. Stage02 恢复

输入是 Stage01 完整论文包。按论文合并已有结果：

- `processing_status=completed` 且 decision 合法：复用，包括正常拒绝和 uncertain；
- `processing_failed`、无合规 JSON、所有模型不可达、HTTP 5xx、timeout：重新入队；
- 从未生成 Stage02 记录：重新入队；
- 上游文档后来发生变化：旧结果标记 `stale`，显式记录原因后重跑；
- 新结果成功后替换“当前有效指针”，不删除旧 attempt；
- 只有当前有效结果通过时才释放 Stage03。

对当前 Batch02，设计生效后的初始计划预计为：复用 420 篇 Stage02 成功结果，重试 165 篇 API 失败，
处理 412 篇尚未产生 Stage02 结果的论文。实际实现时由 planner 重新计算，不把这些数字写死在代码中。

## 9. Stage03 恢复

输入是 Stage02 当前有效的通过论文：

- 正常 `software_covered`、`software_coverage_probable`、正常拒绝或 hold 结论均复用；
- 模型、Softcite 服务或网关客观失败重新入队；
- 尚未处理的 Stage02 通过论文重新入队；
- 工具箱能力快照 hash 必须与原结果一致，否则旧结果标记 stale，但只有显式
  `--invalidate-stage stage03` 才开始重新评估；
- Stage03 恢复成功后，新增通过论文自动进入 Stage04 pending 队列。

当前 Batch02 可先复用 167 篇成功结果，重试 83 篇 API 失败，并处理当前至少 19 篇已经通过 Stage02 但
尚未进入 Stage03 的论文；Stage02 恢复后还可能增加 Stage03 输入。

## 10. Stage04 MinerU 恢复

### 10.1 文档级而不是微批次级

对每篇 Stage03 当前通过论文列出正文和所有已知 SI：

- MinerU 输出存在、质量门通过且输入 SHA256/config hash 一致：复用；
- `deep_parse_failed`、timeout、沙箱回收、服务错误、输出缺失或质量门失败：文档重新入队；
- 从未处理：文档重新入队；
- 只重跑失败文档，不重跑同一论文已经成功的正文/SI；
- 所有必需文档成功后，论文 Stage04 汇总转为 pass 并释放 Stage05。

必须修正当前语义：论文级 `deep_parse_failed` 不能继续记作普通 `processing_status=completed`。建议使用：

```json
{
  "processing_status": "retryable_failed",
  "decision": "deep_parse_failed",
  "passed": false
}
```

若需要保持旧 schema 兼容，可保留 `processing_status=failed` 并增加
`failure_disposition=retryable`，但不能让完整微批次缓存把它视为成功。

### 10.2 沙箱与重试

- planner 把 pending 文档交给沙箱池；每个文档任务使用 lease，超时可被其他健康实例重新领取；
- 同一次执行内仍可按现有规则等待 5 秒重试一次；
- 跨 resume 不因历史两次失败而永久淘汰，新的 resume generation 重新获得配置允许的尝试预算；
- 如果已有原始 MinerU 目录，通过完整性检查后复用；不完整目录移到 attempt 历史目录再重跑；
- supervisor 替换失效沙箱不会改变文档 attempt identity；
- 每篇/每文档写入真实 `duration_seconds`、sandbox ID、attempt 和错误类别。

当前 Batch01 的初始恢复计划应复用 102 篇深度解析成功论文，重试 5 篇 `deep_parse_failed`，继续处理尚未
完成 Stage04 的 Stage03 通过论文。最终数量以文档级 reconciliation 为准。

## 11. Stage05 恢复

Stage05 由 Router 与 Auditor 两个 API 子步骤组成，应分别 checkpoint：

```text
stage05_router
stage05_auditor
stage05_contract_validation
```

- Router 成功而 Auditor API 失败时，只重跑 Auditor；
- Router/Auditor 正常返回且得到正常 pass、needs_builder_review 或 reject：复用；
- API 失败、无效 JSON、响应截断后修复仍失败：重新入队；
- 纯确定性合同校验可从缓存模型响应重新执行，无需重新调用模型；
- prompt、证据包或 Stage04 文档 hash 变化时，结果 stale；
- 模型科学结论不因当前代码将其映射为 reject 而自动重跑，合同逻辑修复属于显式 Stage05 invalidation；
- Stage05 的论文与候选记录按 stable candidate ID 合并，避免 resume 产生重复候选。

当前已完成的 75 篇 Stage05 没有 API 级失败，默认复用。是否用新的 DeepSeek 模型和修订后的合同重新审查，
属于重新评估，不属于本次 resume。

## 12. 资产删除与恢复的关系

保持现有存储原则：只有 Stage00-03 得到终止性科学拒绝时，才允许删除对应 Stage00 论文目录；Stage04-05
拒绝不删除正文/SI。删除前必须完成：

1. 选择账本写入永久论文身份与远端 URI；
2. 阶段结果和证据写入 registry；
3. 结果状态为终止性而不是客观失败；
4. 删除动作写入 `asset_manifests`，状态为 `pruned_terminal`。

API 失败、MinerU 失败、pending、stale 和 blocked 论文一律不得删除原始资产。扩容 Stage00 时，已删除论文
仍通过账本排除，不会再次进入新批次。

## 13. 命令接口

统一增加入口：

```bash
bash scripts/resume_pipeline.sh \
  --run-root runs/stage00-05-api-batches-10000-20260813 \
  --total 10000 \
  --start-stage stage00 \
  --stop-stage stage05 \
  --dry-run
```

确认计划后去掉 `--dry-run`。扩容示例：

```bash
bash scripts/resume_pipeline.sh \
  --run-root runs/stage00-05-api-batches-10000-20260813 \
  --total 20000 --batch-size 1000 \
  --start-stage stage00 --stop-stage stage05
```

参数语义：

```text
--resume                         默认启用
--total N                        run_root 累计成功物化并纳入筛选的唯一论文目标
--batch-size N                   只用于新增外层批次；不得重切旧批次
--batch ID                       可限制恢复某个旧批次
--start-stage/--stop-stage       限制本次实际执行范围
--retry-only                     只执行客观失败，不执行 never-started
--pending-only                   执行失败和未开始项，不扩容
--invalidate-stage stageXX       显式重新评估该阶段及依赖下游
--resume-config original|current 默认 original
--dry-run                        只生成计划，不申请资源、不调用 API
```

`start-stage` 不能绕过依赖检查。例如指定 Stage04 时，只消费 Stage03 当前有效通过结果；缺失 Stage03 的论文
保持 blocked，而不是猜测输入。

## 14. 代码边界

建议新增：

```text
data_pipeline/src/core/resume.py
data_pipeline/src/core/failure_classification.py
data_pipeline/src/core/run_lease.py
data_pipeline/scripts/workflows/resume_pipeline.py
data_pipeline/scripts/resume_pipeline.sh
```

建议修改：

- `src/pipeline.py`：各阶段从 planner 领取论文/文档任务并增量合并；
- `src/stages/stage00_remote_corpus/remote.py`：全局 reservation、累计扩容、永久排除；
- Stage01-05：接受待处理子集并返回可合并的论文级结果；
- `src/integrations/mineru.py`：文档 attempt/lease 和失败目录隔离；
- registry：增加 selection、work item、attempt、artifact、lease 表；
- 两个批处理 workflow：不再以完整微批次 cache 作为唯一完成依据；
- `scripts/README.md`：统一恢复命令和扩容语义。

现有 `stage_cache.json` 保留为兼容层。迁移完成后，其 `completed` 仅表示该微批次当时没有 pending/retryable
项目；真实恢复判断必须查询论文级状态。

## 15. 对现有运行目录的迁移

第一次对旧 run_root 执行 resume 时，运行一次只读 importer：

1. 从所有 Stage00 `selected_papers.jsonl/source_manifest.jsonl` 建立全局选择账本；
2. 从阶段 decisions、documents、attempts 和 summaries 导入最新有效状态；
3. 以 `paper_id/document_id + created_at + artifact hash` 去重；
4. 将 `processing_failed` 导入为 retryable；
5. 将 Stage04 `deep_parse_failed` 特别迁移为 retryable；
6. 对没有记录但上游已释放的论文生成 pending；
7. 对状态写着 running、但 lease/PID/boot ID 无效的运行标记 `interrupted_external`；
8. 生成 migration report，用户确认后才允许写入和开始执行。

Importer 必须幂等。重复执行不能生成重复 attempt，也不能覆盖原始 JSONL。

## 16. 实施顺序与 Git 管理

建议分为六个本地提交，不上传 GitHub：

1. `feat(resume): add persistent work-item and run-lease contracts`
2. `feat(stage00): support cumulative unique corpus expansion`
3. `feat(resume): add paper-level recovery for stages 01-03`
4. `feat(stage04): resume failed MinerU documents independently`
5. `feat(stage05): checkpoint router and auditor independently`
6. `test(resume): cover crash recovery, expansion, retry and idempotency`

每个提交都应保持旧命令可用；最终再把统一入口设为推荐路径。

## 17. 测试与验收

### 17.1 必须测试

- Stage00 10 篇扩容到 20 篇，只新增 10 个唯一远端 URI；
- 已筛除且 PDF 已删除的历史论文不会被 Stage00 再选；
- Stage00 在复制正文后强制杀进程，resume 后不重复 target slot 或 selection event；
- Stage02 一个 10 篇微批次中 3 篇 API 失败，resume 只重跑这 3 篇；
- Stage03 同样验证模型 fallback 全失败后恢复；
- Stage04 正文成功、SI 失败，resume 只重跑失败 SI；
- Stage04 第一次 `deep_parse_failed`，第二次成功后正确释放 Stage05；
- Stage05 Router 成功、Auditor 失败，resume 不重复 Router；
- 正常 reject 永远不会被普通 resume 重跑；
- 修改运行并发不失效科学结果，修改 prompt/config 会要求显式 invalidation；
- 模拟 boot ID 变化后，陈旧 running 自动改为 `interrupted_external`；
- 同时启动两个 resume 进程，第二个不能重复领取任务；
- 重复执行 importer 和 resume，聚合 JSONL 中每篇只有一条当前有效记录；
- 扩容后 Batch0001-Batch0010 的 config hash 和论文归属保持不变。

### 17.2 验收条件

1. 对当前 Batch02 执行 dry-run 能准确列出 reuse、retry、pending 和 blocked 数量；
2. 恢复运行不重新调用 Batch02 已成功的 Stage02/03 模型结果；
3. Batch01 Stage04 的 5 篇失败论文会重新解析，102 篇成功论文不会重复解析；
4. 机器重启后无需删除任何阶段目录即可继续；
5. 从 10,000 扩到 20,000 时只追加 10 个批次和 10,000 篇新论文；
6. 所有删除过的历史论文仍可通过 registry 找到远端 URI、阶段结论和删除原因；
7. Stage00-05 每个客观失败都有可查询的 failure class、attempt 和下一步状态。

## 18. 本方案暂不实现的内容

- Stage06/07 候选级 Agent session 恢复；
- Gold Run 的作业级恢复；
- 自动把正常科学 uncertain 升级到更强模型；
- 因筛选规则变化自动重跑历史正常结论；
- 在没有稳定增量抽样排名的情况下原地扩容 `seeded_sample`。

Stage06/07 将按其 Agent 化重构方案另行设计 resume 合同，避免当前 direct API 结构反向约束未来实现。

## 19. 编码前需要确认

1. `--total` 按“成功物化并纳入筛选的累计唯一论文数”解释，永久复制失败对象由同一目标槽位的新对象替代。
2. 已选择但后来被筛除、且本地资产已删除的论文仍永久参与 Stage00 去重。
3. 旧批次、目标槽位和论文归属冻结；扩容只追加新槽位和新批次。
4. `remote_order` 与基于固定 seed/hash 的稳定顺序均支持增量；远端新增对象不回头重排旧批次。
5. 普通 resume 默认冻结原科学配置；prompt、模型语义、工具箱或规则变化必须显式 invalidation。
6. 正常 reject/uncertain 不自动重跑，只有客观执行失败和未开始任务自动入队。
7. API/MinerU 客观失败论文不删除资产；只有 Stage00-03 的终止性科学拒绝可以删除。
8. 使用 run-local `resume_state.sqlite` 调度，再把当前投影同步到现有 screening registry。

以上语义确认后再实施，不在本设计阶段修改生产代码或恢复正在运行的任务。
