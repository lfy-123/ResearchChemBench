# Stage 03-04 重构实施记录（2026-08-03）

## 目标

本次修改将筛选流程收敛为两个职责明确的阶段：

1. Stage 03 只抽取作者实际使用的核心软件，并要求全部核心软件被工具箱直接覆盖。
2. 删除旧 Stage 04“计算化学完整性判断”。
3. 将旧 Stage 05 重构为新 Stage 04：候选资源句召回、模型结构化、Python 校验和硬上限比较。
4. 原 Stage 06-18 全部前移一位，最终流水线为 Stage 01-17。

## Stage 03 修改

- 修复 `_direct_support()` 只检查 `backends` 的错误。
- 软件只要位于 `available_identifiers` 且不在 `unavailable` 中，即视为工具箱支持。
- `scientific_smoke`、`interface_smoke` 和 `needs_complete_input` 只决定验证等级。
- Yambo 从错误的 `unsupported` 修正为 `direct_covered`，验证等级为 `interface`。
- 未识别到核心软件时使用独立状态 `software_not_identified`。
- `capability_equivalent` 继续只作为备选，不进入主流程。
- AMBER/GAFF/GAFF2 力场和参数不作为 Amber 引擎。
- Gaussian 只有在版本号、software/package/program/code 或明确计算执行语境中才作为软件。

## 删除旧 Stage 04

删除了 `src/screening/computation_completeness.py`、旧模型 prompt、配置、输出、
路由字段、测试和下游记录字段。Stage 03 的 `direct_covered` 论文现在直接进入
新 Stage 04。

## 新 Stage 04 实现

新阶段采用四步结构：

1. 使用关键词从 GROBID TEI 召回 CPU、GPU、内存、wall time、core-hours 和平台句子。
2. GROBID Quantities 为候选句提供数值与单位提示。
3. OpenAI 兼容模型按固定 JSON 结构整理资源，不负责最终筛选。
4. Python 校验证据、数值、单位、scope 和 relation，再与配置上限比较。

Python 只比较 `cpu_cores`、`gpus`、`memory_gb` 和 `runtime_hours`，并且只比较
`actual_computation=true`、`scope=single_job` 的记录。CPU/core/GPU-hours、平台
名称、物理模拟时长和不确定表达只记录。

模型输出校验包括：

- evidence 必须完整对应候选原文句；
- CPU 核数必须来自明确的 core 表达；
- CPU 型号中的数字不能作为核数；
- 内存和时间必须能够从原文确定性换算；
- `1 day and 4 hours` 可验证为 28 小时；
- 带逗号或 million/thousand 的 aggregate 数值可验证；
- `finish_reason=length` 视为无效响应；
- 非法结构自动重试一次，仍失败则写入 `.error.json` 并停止流水线。

## 阶段重编号

旧 Stage 05-18 依次改为新 Stage 04-17。同步修改了主流水线、summary、MinerU、
ScientificRecord、任务选择、包生成、数据集构建、cache/output 路径和
`stage_index.json`。独立脚本由 `run_stage03_05.py/.sh` 替换为
`run_stage03_04.py/.sh`。

## 调试中发现并修复的问题

1. Yambo 已在工具箱中，但旧代码只检查 backend，导致误判。
2. `Xeon Gold 6230 CPU` 被旧正则识别为 6230 核；新实现识别为 40 核。
3. `89.1 core hours` 曾被当成 89.1 核；新实现作为 aggregate 记录。
4. `1 day and 4 hours` 曾拆成 24 和 4 小时；新实现归一化为 28 小时。
5. 1800 completion tokens 导致 GEOM 响应截断；上限调整为 3000，并拒绝 length finish。
6. 初版数值校验没有覆盖 `0.04 wall hours` 和 `core count was 12.0`，已补充。
7. flash 对 platform/unresolved 输出对象，现统一归一化为带 evidence 的对象。
8. Gaussian 偏置势存在多种表达，最终改为软件执行语境白名单。

## 验证

- Ruff 检查和格式检查通过。
- 最终全仓 54 个单元测试全部通过。
- 新增 Stage 03/04 回归测试，覆盖 Yambo、AMBER/GAFF、Gaussian 歧义、CPU 型号、
  复合时间、aggregate 资源、非法 evidence 重试和 API 失败停止。
- 使用 flash 模型完成两篇定向回归和 17 篇正式论文全量测试。

本次修改只保存在本地 Git，不推送 GitHub。
