# V2 流水线调度与软件门控修复记录（2026-08-10）

## 目标

- 保持严格筛选语义，不针对单篇论文添加特例。
- 消除 Stage01 被下游 Qwen 审查占用同一微批次线程所造成的背压。
- 让软件覆盖结论可以由结构化工作流和原文证据审计。
- 为后续调优提供阶段级真实性能统计。

## 运行中 2000 篇任务的性能基线

本节来自 `runs/v2_screening_2000_fresh_20260810` 的旧调度代码。任务未因本次修改而停止。

- Stage00 远端选择与复制约 7 分 44 秒。
- Stage01 补充材料整理约 9 分 14 秒。
- GROBID 首批 80 篇约 6 分 38 秒；当前累计解析中 GROBID 1300 次成功、
  `pdftotext` 10 次成功，其中 4 次是 GROBID 回退。
- Stage02 每个 10 篇微批次平均 14.68 分钟，中位 13.15 分钟，P90 21.80 分钟，
  最大 43.78 分钟。
- Stage02 已记录 7501 次 map 调用，单次平均 12.55 秒；每篇约 13 次 map 调用，
  是当前主要瓶颈。
- Qwen 服务观测为 16 个运行请求、0 个等待请求、KV cache 使用约 9.1%。
  客户端并发限制先于 H200 容量成为瓶颈。
- Stage03 只处理 Stage02 严格通过的少量论文，模型调用平均约 41.64 秒；它不是总体吞吐瓶颈。
- 活跃运行目录约 24 GiB；文件系统使用 447/500 GiB，剩余约 54 GiB。

## 调度修改

新增有序、有限缓冲的多阶段调度器 `ordered_pipeline_map`：

1. Stage01、Stage02、Stage03 分别使用独立线程池。
2. 微批次完成 Stage01 后立即进入 Stage02；Stage01 线程可继续处理下一批。
3. 每个阶段仍按 `microbatch.stage_concurrency` 单独限流。
4. 阶段边界由 `microbatch.buffer_size` 限制排队数量，避免上游无限占用内存和存储 I/O。
5. 输出仍按输入微批次顺序聚合，缓存和断点恢复契约不变。
6. 所有 Stage03 审查完成后，才将共享 GPU worker 从 Qwen 切换到 MinerU。
7. Stage04 MinerU 与 Stage05 外部 API 也使用独立线程池；一个批次完成 MinerU 后可立即进入 Stage05。

阶段汇总新增 `performance`，包含微批次数、缓存命中数、批次 P50/P90/最大耗时、
累计 worker 时间、墙钟时间和每分钟论文数。

示例配置调整为：

- Qwen 客户端并发 32；vLLM 仍由服务端 `max-num-seqs=64` 限制。
- Stage02 文本块从 9000 字节增至 18000 字节，以减少重复输出和请求数，同时保持在
  16384 token 上下文预算内。
- Stage01/02/03/05 阶段池分别为 2/8/8/8；GROBID 单批工作线程为 4。
- 这些值只影响后续新任务，不修改正在运行任务的快照。

## 软件门控修改

Stage03 软件/资源审查新增结构化 `execution_layer`：

- `named_software`：核心计算引擎和需要明确软件身份的步骤，必须填写 `software`。
- `task_specific_python`：仅允许短小、透明、可由 Python 重写的输出后处理，允许
  `software=null`。

确定性校验不再允许 `inventory_complete=true` 掩盖未命名的核心步骤。目录别名恢复遵循：

1. 软件名称必须来自冻结的 toolbox alias snapshot。
2. 原文局部上下文必须包含实际使用动词。
3. 多词正式产品名不区分大小写；单词缩写继续区分大小写，避免普通词误命中。
4. 自动绑定工作流步骤时，证据 ID、workflow ID 和步骤动作关键词都必须一致。
5. 无法唯一绑定时保持 `software_inventory_unconfirmed`，不由规则猜测软件。

对运行中任务的旧规则通过项进行了部署 Qwen 回归。最终 R18 样本随原任务推进扩展到 6 篇：
5 篇 `software_covered`，1 篇因关键超胞构建步骤未明确绑定实现而进入
`software_inventory_unconfirmed`，无处理错误。人工逐篇核对确认通过项的必要命名软件均在当前
toolbox snapshot 中：Gaussian 16、ORCA、CP2K、VASP、VASPKIT、LAMMPS、Pymatgen 和
Materials Project。OVITO 仅作为非必要可视化软件出现且不参与覆盖通过。

R18 prompt 增加了独立后处理边界，避免将一个段落中的核心引擎自动转移给另一个分析方法。
Qwen 对多数步骤已遵守该边界，但仍将一篇论文的 Bader 分析归给 VASP；这是当前小模型的残余
语义误差。生产代码没有为该论文或 Bader 添加特例规则。该步骤需要后续 Builder/Judge 强模型
再次核验，或者在具备通用软件-动作证据契约后再提升为确定性门控。

## 验证

- Ruff：通过。
- Python compileall：通过。
- `PYTHONPATH="$PWD:$PWD/data_pipeline" ... pytest -q data_pipeline/tests`：
  `337 passed, 8 subtests passed`。
- 新增测试覆盖独立阶段调度、顺序稳定、异常传播、长软件名大小写恢复、背景软件排除、
  证据局部绑定、Python 后处理边界和未命名核心引擎拦截。
