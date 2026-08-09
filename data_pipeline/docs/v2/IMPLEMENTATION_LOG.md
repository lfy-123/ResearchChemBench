# 数据管线 v2 实现记录

日期：2026-08-07；v2.1 阶段重排补录：2026-08-09

状态：代码基线、配置接口和自动测试已完成；v2.1 阶段重排与共享 GPU worker 切换已实现。

## 1. 实现策略

本次没有删除或改写旧 Stage 00-08。新实现放在 `data_pipeline/src/v2`，仅当配置包含：

```json
{"pipeline_contract": "researchchembench-data-pipeline/v2"}
```

时，`chem-pipeline run` 才进入 v2；旧配置继续调用原 `src.orchestration.pipeline`。这样旧运行目录、
旧缓存和已有批处理脚本不会因 v2 开发失效。

主要入口：

- `src/v2/pipeline.py`：Stage00-07 编排、微批次、服务生命周期和汇总；
- `src/v2/config.py`：v2 contract、路径和四类模型角色校验；
- `src/v2/model_client.py`：OpenAI-compatible JSON 调用、并发上限和审计缓存；
- `src/v2/runtime.py`：Stage03/04 共用 rlaunch screening worker；
- `src/v2/stages/stage00.py` 至 `stage07.py`：逐阶段实现；
- `config.v2.example.json`：完整配置样例；
- `scripts/workflows/run_pipeline_v2.sh`：一键运行入口。

## 2. 阶段实现

| 阶段 | 已实现行为 | 主要输出 |
| --- | --- | --- |
| Stage00 | 复用远端语料选择；正文和远端已有 SI 按 paper folder 落盘 | `stage_00_remote_corpus` |
| Stage01 | PDF hash、DOI/标题作者版本归一化、canonical 正文、正式 SI 清单和出版商补齐；下载失败不冒充无 SI | `papers.jsonl`、`documents.jsonl`、`duplicate_groups.jsonl`、acquisition audit |
| Stage02 | 正文和 PDF SI 统一 GROBID-first，错误或低质量时回退 `pdftotext`；不调用 MinerU；manifest 中的 docx/xlsx/zip/csv/txt/cif 等 SI 仍参与前筛 | coarse normalized Markdown、content blocks、parser attempts、quality reports |
| Stage03 | 对正文和全部 SI 做 evidence map/reduce；严格筛选纯计算原创论文，并隔离不完整解析和非原创文章；`uncertain` 独立复审一次 | chunk reviews、validated evidence、paper decision |
| Stage04 | 规则别名、可选 Softcite、共享 LLM 软件角色/资源审查；按原生 backend、已配置 Python 包和受限任务特定 Python 判定；通过后调用 MinerU | workflow inventory、software mappings、resource profile、deep normalization、decision |
| Stage05 | 独立强模型接口；按十方向检查三步科研闭环、验证门、公开输入/隐藏目标、机器评分、ground-truth 等级和科学意义；合同错误单独重试和记录 | 0-3 candidates、结构化 abstain 或 `contract_invalid` |
| Stage06 | 独立 Builder API；先生成私有 shared record，再用不含 hidden reference 的两个独立调用生成 autonomous/reproduction；执行泄漏和完整性校验 | task pair 目录、hidden reference、ground truth、rubric、builder audit |
| Stage07 | 独立 Judge API；确定性审计、证据对照、Judge 决策和可配置 Gold Run command | judge audit、gold manifest、release decision |

所有阶段将 `processing_status` 与科学 `decision` 分开。单篇网络、解析、模型或 schema 错误写入该论文记录，
不会抛出到整批并伪装成科学淘汰。

## 3. 模型接口

模型配置固定为四个角色：

| 配置键 | 使用阶段 | 默认密钥环境变量 | 是否共享 |
| --- | --- | --- | --- |
| `models.screening` | Stage03、Stage04 | `RCB_SCREENING_API_KEY` | 两阶段强制共享同一实例 |
| `models.suitability` | Stage05 | `RCB_SUITABILITY_API_KEY` | 独立 |
| `models.builder` | Stage06 | `RCB_BUILDER_API_KEY` | 独立 |
| `models.judge` | Stage07 | `RCB_JUDGE_API_KEY` | 独立 |

每个角色分别配置 `base_url`、`model`、`api_key_env`、`workers`、`timeout_seconds`、`retries`、
`max_tokens`、`thinking` 和 `cache`。也可以用 `RCB_<ROLE>_BASE_URL`、`RCB_<ROLE>_MODEL`
覆盖 endpoint 和模型名。

配置校验禁止 Stage03/04 改用非 screening 角色，也禁止 Stage05/06/07 互相串用。Stage03 map、
Stage03 reduce、Stage04 inventory 使用不同 prompt version 和缓存 namespace，即使共享 endpoint 也不会复用错误响应。

### Screening worker 生命周期

当 `models.screening.managed_rlaunch=true`：

1. 运行开始时与 OpenSandbox 申请并行调用 `scripts/stage03_llm/manage_rlaunch_worker.sh`；环境和模型只在联网开发机准备，GPU worker 直接读取共享存储；
2. 已有 state 先执行健康检查，健康则复用；不健康且无法安全清理时终止，不重复泄漏 GPU worker；
3. Stage03/04 全部微批次共用一个 Qwen3-30B-A3B-Instruct-2507 服务；
4. 本地通过持久 OpenSSH control socket 转发 worker gateway，避开需要浏览器会话的 Brain++ IAP 公网入口；
5. Stage04 完成后在 `finally` 中停止 worker 和 SSH 隧道；失败时保留可诊断 state，并可用同一 manager 精确清理；
6. 外部 API 模式只关闭 client，不停止外部服务。

## 4. 并发与沙箱

Stage00/01 是语料级步骤。通过 Stage01 的论文按 `microbatch.size` 分组，每组内部执行：

```text
Stage02 -> Stage03 -> Stage04 -> Stage05
```

不同组最多 `microbatch.concurrency` 个并行。某组完成当前阶段后立即进入下一阶段，不等待其他组。
每个模型角色还有独立全局 semaphore，防止“微批次数 × 阶段 workers”击穿单个 endpoint。
每个 batch 保存 `batch_result.json` 和 config hash，完全匹配时才 resume。
Stage04 的缓存键包含 MinerU 外部 JSON 配置文件的路径、大小和 SHA256；Stage02 缓存只依赖
GROBID/Poppler 路由与低成本质量策略。MinerU 配置变化只失效 Stage04 及其下游。

v2 复用现有 `SandboxPipelineRuntime`。使用 `--sandbox` 或 `execution.backend=sandbox` 时：

- 运行开始前创建/复用一个 OpenSandbox；
- MinerU、GROBID 和可选 Softcite 共用该沙箱；
- 服务在 run-level `ExitStack` 中只启动一次，不在 stage/batch 边界关闭；
- 全部阶段退出后才按 `cleanup=keep|stop|delete` 处理沙箱；
- CPU、memory、lifecycle、source、inventory、image 和 API key env 均可配置。

## 5. Stage04 确定性边界

LLM 只提取实际使用软件、角色、workflow、resource/complexity facts 和原文证据。最终判定不接受模型常识：

- backend 必须存在于本次冻结的 `toolbox_capabilities.json`；
- 被删除的软件不会因为模型声称“等价”而重新加入；
- 预设 Action 只作为便利层，不作为 Stage04 硬门；catalog 中的原生软件可由文档层直接调用；
- 环境 profile 已配置的 Python 包属于可用运行时能力；短小、确定性的 Python 分析可由第三层完成；
- 第三层不能替代论文未命名或工具箱未包含的核心量化、动力学、采样或专有软件；
- range 跨阈值、`greater_than` 下界未越界、未知单位/资源类型均为 `cost_unconfirmed`；
- physical experiment duration 不参与计算成本；
- aggregate study 超限进入 unconfirmed，不直接误杀可能可抽取的代表性子流程；
- 只有明确 single-job 最低成本已超限时作 `cost_exceeds_budget`。

## 6. Builder、Judge 与 Gold Run

Stage06 只接收 candidate 引用的原文 evidence blocks 和文档 hash/角色，不接收无界全文。生成 shared private
record 后，两个公开模式的请求体明确移除 `hidden_reference`。确定性校验会检查 task pair ID、必需文件、
模式、隐藏答案字符串泄漏和状态。

Stage07 使用独立模型配置和缓存；Judge 能读取 task pair、原文 evidence blocks 和 deterministic audit，
但不能读取 Builder 调用缓存或会话。`gold_run.enabled=false` 时，即使 Judge pass 也只记录
`benchmark_ready=false`；只有配置的 Gold Run command 返回 0 才能发布。

## 7. 运行方式

先从样例生成本地配置并填写实际 source、endpoint 和模型名。密钥只放环境变量或现有
`config.local.env`，不要写入 JSON。

```bash
cd /mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline

# 本地或外部服务模式
bash scripts/workflows/run_pipeline_v2.sh /path/to/config.v2.local.json

# 一个 128 CPU / 256 GiB 沙箱，共享到任务结束
python -m src.cli run \
  --config /path/to/config.v2.local.json \
  --sandbox \
  --sandbox-cpu 128 \
  --sandbox-memory 256Gi \
  --microbatch \
  --microbatch-size 10 \
  --microbatch-concurrency 5
```

可用 `stop_after=stage00` 至 `stage07` 做分阶段验收。正式批量运行前建议依次执行 10、100、500 篇
shadow run，并人工分层检查 Stage03/04/05 的 precision，而不是直接启动一万篇。

## 8. 自动验证

本次新增 `tests/test_v2_pipeline.py`，覆盖：

- Stage03/04 强制共享 screening role；
- LLM 响应缓存回放；
- Stage03 map quote 回映和 reduce 决策；
- Stage04 Softcite 输入、软件映射、action mismatch；
- resource range 跨阈值不放行；
- DOI 版本归一化和非 PDF SI inventory；
- 非 PDF SI 标准化；
- Builder 公开请求不包含 hidden reference。

验证结果：

```text
ruff check src tests: passed
pytest data_pipeline/tests: 173 passed, 8 subtests passed
config.v2.example.json: valid JSON
git diff --check: passed
```

## 9. 真实运行验收

已完成的基础设施验收：

1. OpenSandbox 以 128 CPU / 256 GiB 启动，GROBID `/api/isalive` 和单篇 MinerU 均通过；
2. Qwen3-30B-A3B-Instruct-2507 的 16 个权重分片已放在共享模型目录；ModelScope 下载可避开 Hugging Face Xet body 的网络限制；
3. 通用 rlaunch H200 worker 不要求指定镜像或 H200 tag；vLLM 使用 Triton MoE、原生 sampler，并关闭不适用于 runtime-only CUDA 容器的 FlashInfer/DeepGEMM JIT warm-up；
4. worker-local PID 目录避免共享存储 PID 复用误杀；本地 SSH 隧道上的真实 `/chat/completions` 返回 HTTP 200 和合法 JSON；
5. 500 篇测试 Stage00 已复制 500 篇；Stage01 已完成论文包和 SI 状态审计；该次运行最初按正文
   MinerU-first、SI GROBID-first 执行，随后已停止，并由第 20 项的新解析分层取代。

待本次 shadow run 完成后补录：Stage02-05 的通过数、决策分布、解析器回退率、模型错误率、耗时，
以及对 Stage03 计算化学相关性和 Stage04 工具箱/成本覆盖的分层人工抽查。Stage06/07 不在本次运行范围内。

## 11. 2026-08-09 Stage03-05 可靠性修复

2000 篇运行的逐记录审计发现三类合同问题：Stage03 的文章类型和实验执行者归属不稳，Stage04 会把
方法名/作者姓氏当软件且未完整表达三层工具箱，Stage05 混用了 GROBID 与 MinerU evidence namespace，
并将 schema 错误误记为科学 `abstain`。本轮已修复代码、prompt、能力快照和测试。

完整问题、修改项、历史回放结果和新数据流见
[STAGE03_05_RELIABILITY_FIX_LOG_20260809.md](STAGE03_05_RELIABILITY_FIX_LOG_20260809.md)。

## 10. 500 篇 shadow run 中的稳定性修正

2026-08-08 的真实运行没有把 `processing_failed` 当成正常淘汰，而是暂停汇总并逐项修复：

1. Qwen 服务最初的 8192 context 无法容纳 Stage03 map/reduce。worker 改为 16384 context 后，reduce
   仍会随分块数无界增长，因此 reduce packet 改为最多 12 条高置信证据、截断 quote 和仅含 ID/计数的
   chunk summary；完整 map 响应继续保存在 `chunk_reviews.jsonl` 和 LLM cache。
2. MinerU 可能产生一个超长 block，或产生数百个很短但 JSON metadata 很多的 block。Stage03 现在按
   序列化后的完整 JSON UTF-8 字节数（`chunk_payload_bytes`）封包，并能拆分单个超长 block；极端的
   963-block 论文真实重跑为 29 个 map 加一个 reduce，0 个处理错误。
3. 达到 token 上限的 JSON 可能缺少结束括号。通用 JSON repair 现在可修复这种截断对象；repair 后数组
   中偶发的 scalar fragment 会在 Stage03 evidence 校验时逐项忽略，不再使整篇失败。
4. Stage04 的输入改为高优先 evidence、紧凑规则/Softcite mention 和最小 capability prompt excerpt，
   evidence 使用 `max_evidence_payload_bytes` 限制。输出逐条验证 workflow step、software mention、
   resource/complexity fact 的 evidence ID 和原文 quote。错误事实被删除并写入
   `model_validation_warnings`，论文进入严格的确定性未覆盖/未确认决策，而不是 `processing_failed`。
5. Stage04 使用最多 3 workflows、12 steps、20 software mentions 等有界 schema，调用上限为 5120；
   该预算为 16384 context 保留输入余量。曾触发 context 400 的真实论文在相同 Qwen worker 上重跑完成，
   0 个处理错误。
6. GPFS 在 Python `Path.resolve()` 下可能暴露 `.snapshots/...` 物理路径，而 GPU worker 只挂载稳定的
   `/mnt/shared-storage-user/...`。v2 配置路径改为基于逻辑 `$PWD` 规范化且不解析快照映射，避免健康检查
   误停可用 rlaunch worker。修复后新 worker 在约 2 分钟内完成分配、SSH、vLLM 和隧道健康检查。
7. Stage04 不再把 resource budget 放入 LLM 输入，避免模型复制限额并冒充论文资源事实。每条资源事实
   必须由包含相应资源关键词和数字的原文 quote 支持，否则删除并记录审计告警。真实回归中模型生成的
   12 条无证据资源事实全部被确定性校验剔除。
8. 软件别名匹配不再自动使用内部 backend ID；存在显式别名时只匹配已审计别名，含大写的产品名使用
   大小写敏感匹配。由此消除普通形容词 `geometric` 对 geomeTRIC backend 的误命中。
9. MinerU 正文中可能含 XML 1.0 禁止的 NUL/控制字符。Softcite TEI 现在先做 XML 1.0 字符清洗；真实
   失败论文由 HTTP 400 修复为 HTTP 200，正文内容和 evidence ID 保持不变。
10. OpenSandbox 运行中曾从 `Running` 回退到 `Pending`。本地代理现在识别控制面“sandbox not running”
    响应，串行等待同一实例恢复，重建 worker RPC、刷新 client 并重启本次 run 已登记服务，然后只重放
    失败请求；停止和日志镜像仍为尽力而为，退出时不会为了清理反向等待资源。
11. 微批 `config_hash` 现在包含 Stage03 map/reduce、Stage04、Stage05 prompt version，杜绝代码 prompt
    升级后错误复用旧的 `completed` 批次。
12. 微批恢复由单个全流程 hash 拆为逐阶段依赖 hash。Stage04 的 prompt、工具箱快照或输出预算变化只
    失效 Stage04/05；当时 Stage02 还包含 PDF hash、解析配置和 MinerU 外部 JSON hash，Stage04 还包含
    capability/alias 文件 hash。该历史缓存结构已由第 20 项改成 Stage02 GROBID、Stage04 MinerU。
13. v2 Stage04 接入多 Softcite 实例池。本次配置为 5 个实例，按独立端口在任务开始前并行预热，再由
    线程安全队列做有界分发，避免 20 个 Stage04 worker 拥塞单实例产生 HTTP 504。真实沙箱验收中
    instance 0–4 均健康并返回 `0.9.0-SNAPSHOT`。
14. Softcite 原始 mention 含完整 paragraph 和多层属性，曾使一篇论文输入达到 11265 tokens。Stage04 r4
    只保留软件名、规范名、短 context 和 used/created/shared，并对完整用户包实施 18KB 硬预算；超限时
    优先移除冗余 Softcite/规则项。原失败论文真实重跑为 `cost_unconfirmed`，0 个处理错误。
15. 首批 50 篇人工抽查发现 Stage03 r2 将实验光谱/动力学拟合、XRD 精修、图像统计、LCA 和
    AlphaFold-only 工作误判为计算化学，根因是旧 prompt 明确允许“supporting computation”且 reduce
    看不到作者实验反证。Stage03 r3 改为严格纯计算门控：map 同时抽取可回映原文的分子/材料计算证据
    和作者实验反证；reduce 只有在原创研究、计算为 primary、研究为 pure_computational、无作者新实验、
    且模型—计算操作—化学输出工作流完整时才能确认。确定性后处理再次执行这些条件，并对方法/软件
    列表去重和限长；map 只接受 `attribution=this_paper` 的证据，任何已验证的作者实验反证都会阻止
    放行，即使 reduce 偶发忽略该证据。旧 Stage03/04/05 缓存因 prompt 版本依赖链自动失效，7 个
    当时的 Stage02 MinerU 缓存保留；第 20 项切换解析分层后不再作为新 Stage02 缓存复用。
16. 按存储空间要求清理了所有非当前正式运行的旧 `data_pipeline/runs/*` 筛选轨迹，只保留
    `v2_shadow_500_rlaunch_flash_20260807`；释放约 23 GB。当前正式目录中的 Stage00 论文包、Stage01
    审计、Stage02 缓存和资源状态均保留，旧 smoke 临时目录也已删除。
17. 全套测试发现 GitHub 更新后的 `chemistry_toolbox` 与数据管线生成能力快照哈希不一致。已运行
    `scripts/sync_toolbox_capabilities.py`，按当前源码重新生成 150 actions / 92 backends 的
    `toolbox.json` 和 `toolbox_capabilities.json`；Q-Chem、TURBOMOLE、TeraChem、Molpro、CASTEP 未出现在
    新快照中。Stage04/05 缓存通过 capability 文件哈希自动失效，Stage02/03 缓存继续复用。
18. 严格 Stage03 的首个纯计算候选人工核验正确，但 Stage04 将论文中的 `Gaussian filter` 和
    `Gaussian smearing` 误认成 Gaussian 程序。Stage04 r6 在规则提取和模型结果清洗两侧增加术语
    消歧：只有版本号、`using Gaussian`、`Gaussian was used`、`Gaussian calculations` 等明确执行语境
    才认可为软件；所有软件名还必须逐字出现在其 `exact_quote` 中，否则删除 mention。缺少软件使用证据
    的 workflow step 软件字段也会清空。该候选因自定义连续模型不在工具箱内仍会保守进入
    `software_inventory_unconfirmed`，不会因词义歧义通过。
19. Batch 6 一篇 70 分块长论文在 Stage03 reduce 时以 1 token 超出 Qwen 16,384 context。原因是
    `chunk_summaries` 重复携带数百个长 evidence ID；Stage03 reduce r5 改为只携带每块的验证证据计数，
    实际引用仍由有界 `validated_computational_evidence` / `validated_author_experiment_evidence` packet 提供，
    完整 ID 和响应保留在 `chunk_reviews.jsonl` 与 LLM cache。该批不缓存失败结果，恢复时自动重试。
20. 按 10 篇同源 PDF 的 MinerU/GROBID 对照调整解析成本分层：GROBID 10/10 成功，计算关键词按论文
    平均保留约 91%，Stage03 自然语言证据的有序词覆盖平均约 85%，但公式型证据平均仅约 16%。因此
    Stage02 改为全部 PDF 使用 GROBID，失败或低质量回退 `pdftotext`；MinerU 移入 Stage04，只处理
    软件覆盖和资源门控通过的论文。Stage04 新增 `deep_normalization/`，MinerU 失败记为
    `deep_parse_failed` 并阻止进入 Stage05。Stage05、Builder 和 Judge 已改读深解析文档；由于粗解析与
    深解析会产生不同 evidence IDs，Stage05 不复用 Stage04 的 GROBID block ID，只引用本次 MinerU packet
    中的新 evidence IDs。MinerU 沙箱运行参数和外部配置 hash 同步从 Stage02 迁移到 Stage04。

本轮新增的定向验证包括 reduce 边界、UTF-8/JSON metadata 分块、截断 JSON、repair scalar、Stage04
逐事实清洗、Softcite XML 清洗、Stage04 packet 预算、沙箱 Pending 恢复、逻辑共享路径，以及
Stage02 GROBID 路由/`pdftotext` 回退、Stage04 通过后 MinerU 调度/失败隔离和 Stage05 深文本路由。
全套测试为 `191 passed, 8 subtests passed`；最终阶段统计需在下一次新配置 shadow run 后更新。

## 11. Stage03 纯计算门控专项校准

2026-08-08 按要求停止 Stage02-05 全流程，单独校准并运行 Stage03。旧 r5 在同一批 300 篇中的结果为
`confirmed=1 / not_pure=297 / not_found=2`。审计发现旧 map 响应约 47.3% 因达到输出上限而截断，且会把
MD、DFT、声子、计算光谱以及外部 XFEL/PDB/实验数据库错误归为当前作者实验。

Stage03 r6/r7 完成以下修正：

1. map/reduce prompt 明确定义“当前作者实际实验”和“计算/外部实验数据”的边界，并加入 DFT、MD、
   声子、外部结构和实验合成/表征的正反例；map 输出数组和字符串均有界。
2. 达到 token 上限的响应不再接受修复后的不完整 JSON。依次执行 compact retry 和 essential retry，只有
   `finish_reason != length` 的完整响应才进入证据校验。
3. 作者实验必须同时通过原文 quote 回映和确定性实验语义检查；外部数据、计算光谱和模拟操作不能构成
   作者实验反证。模型声称有实验但没有验证证据时进入 `uncertain` 重审。
4. 原子坐标先在完整 block 层过滤，再在 UTF-8 分段后删除连续坐标序列并保留相邻自然语言。由此修复
   一篇 SI 混合超长说明和坐标、三次响应均截断的问题。
5. OpenLCA/Aspen 流程模拟、组学/序列分析，以及既有动物实验数据的数字化、因果推断和粒子群优化，
   在没有 DFT、MD、QM/MM 等目标计算证据时确定性归为 `computational_content_not_found`。

20 篇分层校准集在人工阅读 GROBID 正文/SI 后达到 20/20 一致：12 篇纯计算、3 篇作者同时做实验、
5 篇实验论文。随后对已有 Stage02 产物独立运行 350 篇，使用 5 个并行微批、每批 4 个 Stage03 worker，
共享 Qwen3-30B-A3B-Instruct-2507 H200 服务。最终结果为：

```text
computational_content_confirmed: 16 (4.57%)
not_pure_computational:          267 (76.29%)
computational_content_not_found:  66 (18.86%)
background_only:                   1 (0.29%)
processing_failed:                 0
```

267 篇 `not_pure` 全部包含通过原文回映和语义校验的作者实验引用；其中 212 篇的计算为 primary，55 篇为
supporting。16 篇通过项全部是 original research、primary computation、完整 workflow、高置信度且无作者
实验。逐篇人工核对通过集后，排除 1 篇仅对既有纳米毒性实验数据做机器学习/统计优化的误放行。

与旧 r5 的 300 篇重叠样本比较，新门控保留原有 1 篇，并恢复 14 篇被错误淘汰的纯计算论文；这些论文
涵盖 DFT/从头算/MD、NEO-DFT、VASP 声子与能带、QM/MM、MLIP-MD/NEB、metadynamics、ai-GCMC 等。
另有 55 篇从笼统的 `not_pure` 改为更准确的“无目标计算”。本轮 cache 共记录 4641 次首轮 map 调用，
其中 48 次（1.03%）截断且全部经重试或坐标过滤恢复；350 次 reduce 中 2 次截断，均在 compact retry
完成。专项测试为 `54 passed`，ruff 检查通过。结果位于
`runs/v2_stage03_r6_350_20260808/stage_03_computational_content/`，记录中的最终 run ID 为
`v2-stage03-r7-350-20260808`。Stage04/05 未运行，等待 Stage03 方案确认后再继续。

## 12. Stage02/03 完整论文包准入

2026-08-08 将 Stage02 对 `complete_with_si` 的论文级质量门从“至少一个 SI 解析成功”收紧为“所有
已知 canonical SI 均解析成功”。输出新增已知、成功和失败 SI 计数及失败 document IDs；任意 SI 失败
都会使整篇论文得到 `parse_failed`。Stage03 增加第二层准入校验，拒绝正文未成功、SI 未全部成功或
旧缓存中 `partial_si_parse=true` 的论文。Stage02 cache hash 新增实现版本，因此该规则变更会自动使
Stage02 及 Stage03-05 下游微批缓存失效。完整 prompt 和数据流说明见
`STAGE03_PROMPT_AND_DATA_FLOW.md`。

## 13. v2.1 阶段重排（2026-08-09）

当前运行入口已经采用 `stage_layout=v2.1-split-normalization`：旧 Stage01（论文包）与 Stage02（低成本
解析）合并为 Stage01，旧 Stage03 改为 Stage02，旧 Stage04 拆为 Stage03（软件/资源 gate）和 Stage04
（MinerU 深解析）。Stage02/03 共享 screening worker；当 Stage04 使用 managed GPU MinerU 时，Qwen
服务释放但 rlaunch worker 保留，随后同 worker 启动 MinerU API，run 结束统一关闭。完整修改和旧 2000
篇结果审计见 [STAGE_LAYOUT_AND_SHARED_GPU_REFACTOR_20260809.md](STAGE_LAYOUT_AND_SHARED_GPU_REFACTOR_20260809.md)。

## 13. Stage04 软件覆盖专项校准

2026-08-08 对 Stage03 r7 通过的 16 篇论文逐篇阅读正文和全部 SI，建立
`STAGE04_16_PAPER_GOLD_AUDIT_20260808.md` 人工金标。校准发现旧结果的聚合数碰巧接近金标，但逐篇
软件、能力和理由存在明显错配。Stage04 r9 完成以下调整：

1. 证据包优先保留别名命中、明确 software cue、Stage03 证据和方法段，每块独立限长；单个超长
   GROBID block 不再挤掉后续正文或 SI 的软件声明。
2. prompt 严格区分 executable 与 functional、basis、force field、algorithm、descriptor、hardware；
   要求逐项审查明确 executable cue，不能静默遗漏未覆盖扩展或自研代码。
3. 模型只能绑定能力快照中逐字存在的 action。确定性门控还会检查 VASP `xc_family` 等结构化约束，
   以及禁止 arbitrary route deck 时的 B3LYP* 等自定义设置。
4. 明确实际使用但不在 catalog 的软件优先判为 `core_software_uncovered`；其后才是
   `capability_constraints_unmet` 和 `software_inventory_unconfirmed`。该确定证据不会再被
   `inventory_complete=false` 或损坏的 workflow schema 覆盖。
5. 软件名称必须由 evidence 或已验证 mention 支持；Wannier interpolation、AutoNEB、HSE、PAW、
   ai-GCMC 等方法/算法不会被当成程序。明确的 VASPsol extension、Molpro、TURBOMOLE、PERTURBO、
   Tinker-HP 等仍会被提取，并因不在工具箱而淘汰。
6. 首次截断后执行 compact retry；再次截断则执行仅保留软件覆盖字段的 minimal retry。三次仍失败才
   记录单篇 `processing_failed`，不会拖垮批次。
7. 能力资产已同步到当前 150 actions / 92 backends，catalog hash 为
   `2f8e8e58b6d7054833558715dbf7bde374ddc860d4423a094a1fd45248ac0103`。Molpro、TURBOMOLE、
   TeraChem、Q-Chem、CASTEP 均不在 backend 或 aliases 中。

最终缓存回放完整执行当前 Stage04 清洗、映射和门控，得到 `10 core_software_uncovered / 3
capability_constraints_unmet / 3 software_inventory_unconfirmed / 0 passed / 0 processing_failed`，逐篇与
人工金标 16/16 一致。最终产物位于
`runs/v2_stage04_r9_gold_16_20260808_attempt5_final_replay/`。专项测试为 `84 passed`，ruff、能力资产
`--check` 和 `git diff --check` 均通过。

## 14. Stage04 三层工具箱覆盖口径修正

2026-08-08 进一步确认化学工具箱包含预设 Action、依据文档直接调用原生软件、任务特定 Python
处理三层。第 13 节的 r9 实现错误地把第一层 Action 和 adapter 参数范围当成整个工具箱能力边界。
r10 将 Stage04 收窄为必要软件存在性门控：

1. prompt 明确禁止因预设 Action、参数 schema 或 runtime 状态拒绝已在 catalog 的原生软件；
2. LLM 只抽取软件、角色、工作流和资源事实，候选 catalog 摘要不再包含 Action/方法约束；
3. 确定性门控只检查必要软件是否映射到活动 backend，以及软件清单是否完整；
4. 输出新增 `coverage_basis=native_software_catalog_presence` 和三层执行模式声明；
5. Molpro、TURBOMOLE、VASPsol、PERTURBO 等明确缺失软件仍为 `core_software_uncovered`；
6. VASP-HSE、CP2K AIMD/metadynamics、Gaussian 自定义 route 三篇由
   `capability_constraints_unmet` 修正为软件 `covered`。

复用已人工核验的真实 Qwen/Softcite 抽取结果执行确定性重算，软件覆盖分布为
`10 core_software_uncovered / 3 software_inventory_unconfirmed / 3 software_covered`。资源事实继续写入
`resource_profile` 供下游使用，但不再影响 Stage04 pass/reject。

验证结果：Stage04 专项文件 `86 passed`；完整 `data_pipeline/tests` 为 `237 passed, 8 subtests
passed`；ruff、能力 catalog `--check` 和 `git diff --check` 全部通过。

## 15. Stage04 部署 Qwen 真调用验证

2026-08-08 使用 rlaunch H200 部署 `Qwen3-30B-A3B-Instruct-2507`，对人工审查的 16 篇正文和 SI
执行 r10、r11 两轮全新模型调用。r11 的 16 个请求全部 `cache_hit=false`、`finish_reason=stop`，没有
截断重试或处理错误，结果为 `3 software_covered / 10 core_software_uncovered / 3
software_inventory_unconfirmed`，逐篇与修正后的人工金标 16/16 一致。

r11 删除发给模型的候选工具箱表，避免“不在候选表”影响软件清单抽取；资源和复杂度字段固定为空。
同时补齐 evidence 原文 quote 恢复、ASE 全名规范化、非软件方法过滤，以及从
`BackendSpec.executables` 生成原生软件别名。完整测试更新为 `241 passed, 8 subtests passed`；GPU
worker 已在验证后停止。详细报告见 `STAGE04_DEPLOYED_QWEN_VALIDATION_20260808.md`。

## 16. 数据管线统一运行环境

2026-08-09 将数据管线、Qwen/vLLM 和 MinerU 合并到唯一主 Python 环境
`data_pipeline/.envs/researchchem-data-pipeline`。两个 GPU 服务仍在同一个 rlaunch worker 上按
Qwen -> MinerU 的顺序切换，但不再切换 Python 环境。

统一 bootstrap 现在完成以下工作：

1. 安装 CUDA 12.8 构建的 PyTorch 2.11、torchvision 0.26 和 torchaudio 2.11；
2. 复用共享 vLLM 源码中已有的 CUDA 扩展，安装通用依赖和 `requirements/cuda.txt` 后端依赖；
3. 以 editable 方式安装 MinerU 3.4.4，并用 `onnxruntime-gpu` 提供 CUDA Provider；
4. 默认使用 PJLab PyPI 镜像和 uv 的 16 路并行下载，保留 wheel 缓存并跳过已安装的 editable vLLM；
5. 通过 `unified_runtime_constraints.txt` 固定 NumPy 1.26.4、Protobuf 4.25.9、Transformers 4.57.3
   和 OpenCV 4.11，避免破坏现有 TensorFlow/Softcite 路径。

旧 `mineru-gpu` 环境、旧 Qwen 环境链接和两个 incomplete 环境目录已删除；链接指向的外部 Conda
环境本体未删除。`.envs/tools` 只包含独立 OpenCode 可执行文件，不是 Python 环境，因此保留。
本地 CPU 节点已验证 CUDA PyTorch 构建、vLLM/MinerU import、MinerU CLI 和 ONNX Runtime
`CUDAExecutionProvider`；真实 GPU 服务生命周期仍需在 rlaunch worker 上验收。

统一环境有四项已知的发行包元数据冲突，不能通过盲目升级解决：当前 vLLM 声明需要
OpenCV-headless >=4.13 和 Protobuf >=5，而 TensorFlow 2.17/Softcite 路径需要 NumPy 1.26 与
Protobuf 4；Delft 声明固定 Transformers 4.48，而当前管线和 vLLM 使用 4.57；Magika 只识别
`onnxruntime` 发行包名，不识别提供相同 Python 模块的 `onnxruntime-gpu`。统一约束选择保护现有数据
管线的版本，`273 passed, 8 subtests passed`，且 `onnxruntime` 模块已确认暴露 CUDA Provider。
后续升级这些核心版本前必须同时回归 GROBID/Softcite、Qwen 和 MinerU，不能以 `pip check` 的自动升级
建议作为修改依据。

## 17. Stage05-07 远程 API 默认代理

2026-08-09 为 Stage05（`suitability`）、Stage06（`builder`）和 Stage07（`judge`）统一增加默认代理。
配置加载时这三个远程角色默认写入 `use_proxy=true` 和 `proxy_url_env=HTTPS_PROXY`；Stage02/03 共用的
本地 screening 服务默认 `use_proxy=false`，从而不会把本地 Qwen 请求错误送入外部代理。

`RoleModelClient` 对每次请求显式构造代理 opener，按以下顺序解析代理地址：指定环境变量、大小写
`HTTPS_PROXY`、大小写 `HTTP_PROXY`、配置中的 `proxy_url`，最后回退到 PJLab 内部代理
`http://httpproxy-headless.kubebrain.svc.pjlab.local:3128`。审计缓存只记录 `proxy_enabled` 布尔值，
不会保存可能含认证信息的代理 URL。对本地角色传入空代理表，确保即使父进程存在代理环境变量也直连。

工作流入口 `scripts/workflows/run_pipeline_v2.sh` 现在默认执行 PJLab 的代理初始化脚本；可通过
`RCB_SETUP_PROXY=0` 显式关闭。单个模型角色也可用 `use_proxy=false` 关闭。清空所有代理环境变量后，
使用实际 `RoleModelClient` 调用 `deepseek-v4-flash` 已返回 HTTP 成功结果，证明客户端自身的最终回退
代理有效，而不依赖 shell 中预先存在的代理变量。

历史 2000 篇运行的旧 Stage04 软件覆盖结果专项复核见
`STAGE04_2000_RESULT_AUDIT_20260809.md`。该目录使用旧编号；按 v2.1 当前布局解释时，其软件/资源部分
对应 Stage03，MinerU 深解析部分对应当前 Stage04。
