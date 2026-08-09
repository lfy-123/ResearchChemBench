# ResearchChemBench 数据管线 v2 设计包

状态：v2.1 阶段重排和统一 GPU 运行环境已实现，已通过本地回归测试；真实 GPU 服务切换仍需在
rlaunch worker 上执行集成验收（2026-08-09）。

本目录定义下一版 ResearchChemBench 数据管线。它以
[ResearchChemBench Benchmark 设计与数据管线简介](../../../docs/RESEARCHCHEMBENCH_BENCHMARK_DESIGN_AND_DATA_PIPELINE.md)
的 Benchmark 目标为上游约束，
并吸收当前 Stage 00-08 实现、500 篇 shadow run 和人工审查中暴露的问题。

v2 的核心顺序是：

```text
先闭合论文包，再解析和筛选；
先确认计算化学内容，再检查软件与成本；
最后才判断能否构造科研任务、生成任务并独立审核。
```

## 文档索引

| 文档 | 内容 |
| --- | --- |
| [DATA_PIPELINE_V2_DESIGN.md](DATA_PIPELINE_V2_DESIGN.md) | 总体架构、逐阶段输入输出、路由、文本抽取、并发、缓存和验收标准 |
| [LLM_PROMPTS_AND_SCHEMAS.md](LLM_PROMPTS_AND_SCHEMAS.md) | Stage 03/04 共用模型、Stage 05 强模型、Builder 和 Judge 的 prompt 与结构化 schema |
| [V1_TO_V2_MIGRATION.md](V1_TO_V2_MIGRATION.md) | 旧阶段到新阶段的代码、配置、缓存、运行产物和测试迁移方案 |
| [IMPLEMENTATION_LOG.md](IMPLEMENTATION_LOG.md) | v2 实现范围、代码入口、模型参数、验证结果和运行前提 |
| [STAGE_LAYOUT_AND_SHARED_GPU_REFACTOR_20260809.md](STAGE_LAYOUT_AND_SHARED_GPU_REFACTOR_20260809.md) | v2.1 阶段重排、Qwen/MinerU 同 worker 切换、旧 2000 篇结果审计 |
| [STAGE03_05_RELIABILITY_FIX_LOG_20260809.md](STAGE03_05_RELIABILITY_FIX_LOG_20260809.md) | 2000 篇运行审计后对 Stage03-05 的可靠性修复、历史回放和新流程 |

## v2 阶段

| 阶段 | 名称 | 核心问题 |
| --- | --- | --- |
| Stage 00 | 远端语料选择 | 本轮处理哪些论文？原始来源和选择过程能否复现？ |
| Stage 01 | 论文包闭合 + 低成本标准化 | 正文/SI 是否已闭合，且 GROBID 或 `pdftotext` 文本质量足以前筛？ |
| Stage 02 | 计算化学内容筛选 | 论文包中是否存在可信、原创、以计算为主的计算化学内容？ |
| Stage 03 | 软件覆盖与资源预筛 | 论文实际使用的软件是否在三层工具箱能力快照中，且明确成本未超预算？ |
| Stage 04 | MinerU 深度标准化 | 仅对 Stage 03 通过者重新生成高质量正文/SI 证据；失败者不进入 Stage 05。 |
| Stage 05 | Benchmark 适用性筛选 | 是否存在符合十个方向、具有完整科研闭环的候选任务？ |
| Stage 06 | 双模式任务构建 | 能否构造共享科学对象的自主科研和论文复现任务？ |
| Stage 07 | 独立审核与 Gold Run | 任务是否忠实、完整、不泄漏、可评分且实际可运行？ |

## 已确认的设计决定

1. Stage 01 在任何语义筛选之前完成正式 SI 的发现、下载和论文绑定，并在同一阶段完成低成本解析。
2. Stage 01 的全部 PDF 使用 GROBID 做低成本正文抽取；请求失败或结果未通过质量门时回退
   `pdftotext -layout`。Stage 02 不调用 MinerU。
3. Stage 02 按当前严格策略筛选原创、主流程完整且无当前作者实体实验的纯计算化学论文；更正、综述、
   观点和评论类文章先由元数据/正文首页规则隔离，实验归属再由 LLM 证据和确定性校验共同确认。
4. Stage 02 和 Stage 03 共用一个运行期部署的 OpenAI-compatible LLM 服务，但使用独立
   prompt、schema、缓存命名空间和并发限制。
5. Stage 03 允许规则、Softcite 与 LLM 协同提取软件；LLM 只负责证据化清单，确定性代码使用
   冻结的原生 backend 和已配置 Python 包快照判定覆盖。预设 Action 缺失本身不淘汰论文。
6. Stage 03 的软件和资源门控结束后，只对通过论文的正文及 PDF SI 调用 MinerU（Stage 04）；深解析失败的论文
   记录为 `deep_parse_failed`，不进入 Stage 05。Stage 05、Stage 06 和 Gold Run 使用这份深解析证据。
7. Stage 05 使用强推理模型判断十个方向、完整科研流程和成对任务可行性，不直接生成正式任务。
8. Stage 06 和 Stage 07 使用最强可用模型；Builder 与 Judge 必须隔离会话、工作区和缓存。
9. 处理错误与科学淘汰严格分开。网络、解析、模型和 schema 错误可重试，不得伪装成论文不合格。
10. 旧运行目录保持只读，v2 不原地改写历史结果。

## 实现边界

- v2 位于独立的 `src/v2` 命名空间，通过配置中的
  `pipeline_contract=researchchembench-data-pipeline/v2` 显式启用；
- 旧 Stage 00-08 实现、旧配置和历史缓存没有被删除或原地改写；
- `config.v2.example.json` 是新配置样例，现有 `config.json` 仍保持旧入口；
- 本次已完成静态、合同和回归测试，尚未启动新的大规模论文 shadow run；
- 正式发布仍要求真实 MinerU、GROBID、Softcite、四类模型 endpoint 和 Gold Run 验收。
