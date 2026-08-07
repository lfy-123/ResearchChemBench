# 纯计算工具箱筛选：新 500 篇 Flash 测试报告

日期：2026-08-07

## 1. 结论

本次从远端数据集重新抽取了 500 篇论文，并明确排除了上一轮 500 篇的选择清单。
新旧两批的 `paper_id` 和正文 `remote_uri` 交集均为 0。Stage 00-06 全部完成，
50/50 个微批次成功，0 个批次失败。

严格漏斗为：500 篇输入 -> Stage 03 保留 14 篇纯计算候选 -> Stage 05 保留 1 篇
工具箱完整覆盖候选 -> Stage 06 成功处理 1 篇。最终保留率为 0.2%。这 1 篇仍只是
Builder 候选，不等于已经具备输入、隐藏答案、评分指标和资源可行性的 benchmark-ready
任务。

## 2. 测试配置

- 代码版本：`909fd28 fix(data-pipeline): reuse pending managed sandbox`；
- 数据集：`en-paper-hzzj`，seeded sample 500 篇，seed `20260808`；
- 排除清单：上一批
  `runs/redesigned_stage00_06_500_strict_flash_20260807/stage_00_remote_corpus/selected_papers.jsonl`；
- Stage 03 模型：`deepseek-v4-flash`，未启动本地 Qwen/rlaunch 服务；
- Stage 03 completion 上限：2048 tokens；Flash API 并发 16；
- 筛选策略：`strict`，只接受纯计算、primary、作者实际执行且软件清单完整的研究；
- Stage 02-06：每批 10 篇、最多 5 个微批次并发；同一微批次内按阶段串行；
- 沙箱：64 CPU、128 GiB，一个沙箱贯穿 Stage 02-06，结束后统一停止；
- 总墙钟时间：648.622 秒，即 10 分 49 秒；
- 运行目录大小：5.1 GiB，共 4026 个文件。

## 3. 阶段结果

| 阶段 | 输入 | 主要结果 | 继续 |
| --- | ---: | --- | ---: |
| Stage 00 | 500 篇 | 500 正文、426 份 SI；417 篇有 SI、83 篇无 SI；0 复制失败 | 500 |
| Stage 01 | 926 PDF | 926 canonical、0 duplicate；正文和 SI 均参与后续解析 | 500 篇 |
| Stage 02 | 926 PDF | GROBID 922；`pdftotext` 回退 4；0 最终失败 | 500 篇 |
| Stage 03 | 500 篇 | pure candidate 14、not pure 275、not computational 208、unconfirmed 3 | 14 |
| Stage 04 | 14 篇 | 已有 SI 13；另 1 篇下载 3 份 PDF，因视频附件未取记为 partial | 14 |
| Stage 05 | 14 篇 | workflow uncovered 11、method incomplete 2、direct candidate 1 | 1 |
| Stage 06 | 1 篇 | 复用 Stage 02 的 1 份 SI 文本；0 错误 | 1 |

## 4. Stage 02 解析

4 个 GROBID 请求因单文件 `HTTP 504 stream timeout` 回退 `pdftotext`，包括 2 篇正文和
2 份 SI。回退全部成功，文本质量分分别为 94.8、95.1、68.7 和 83.4，没有空文本。
500 篇正文的平均质量分为 96.53，426 份 SI 的平均质量分为 77.09。

启动阶段日志曾出现并发请求返回 503，但内置重试随后成功；最终汇总中的 GROBID 失败
仅为上述 4 个 504，失败比例 0.432%，且均已降级隔离。

## 5. Stage 03 结果与抽查

规则层得到 214 strong、97 weak、189 not computational；前两类共 311 篇调用 Flash。
311 次调用无 API、JSON、schema 或截断错误，模型返回名均为 `deepseek-v4-flash`，最大
completion 为 1500 tokens。累计模型耗时 1314.712 秒，单次平均 4.227 秒；由于 16 路
API 和 5 路微批次并发，这些耗时不是串行叠加到墙钟时间。

模型把 272 篇判为混合计算/实验、8 篇实验为主且计算辅助、15 篇纯计算、15 篇非计算、
1 篇不确定。严格条件最终只放行 14 篇；3 个 `llm_unconfirmed` 均 fail closed，没有进入
Stage 04。

对 14 个放行候选逐篇做关键词和上下文抽查后，发现 1 个明确假阳性：
`10.1039/d3sc02954a`（*Towards routine organic structure determination using Raman
microscopy*）的正文和 SI 均包含作者 Raman 测量及测量参数，Flash 却判为纯计算。
该论文随后因依赖未覆盖的 SARA 软件被 Stage 05 淘汰，所以没有污染最终候选。这说明
Stage 03 的严格通过集仍不是 100% 精确，后续本地模型测试应重点比较实验方法段召回。

其余 13 个 Stage 03 候选未在本次快速审计中发现作者实验，主要是 DFT、AIMD、QM/MM、
微观动力学和理论模型研究。该结论是运行后抽查，不是人工金标准 precision 评估。

## 6. Stage 04 补充材料

14 篇候选中 13 篇在 Stage 00 已带 SI，Stage 04 不访问官网。唯一缺 SI 的论文为
`10.1016/j.checat.2025.101394`：Stage 04 从 Elsevier 找到附件并成功下载 3 份 PDF；
另有 6 个 MP4 视频不在当前允许格式内，因此状态为 `partial`。论文仍进入 Stage 05，
之后因需要未收录的自定义 Python/Julia 代码而淘汰。

本轮没有出现“有 SI 但网站阻断导致淘汰”的样本，也没有把未知状态误当成无 SI。

## 7. Stage 05 工具箱覆盖

14 篇纯计算候选中：

- 11 篇存在至少一个未完整覆盖的工作流软件，例如 CP2K、Multiwfn、Quantum ESPRESSO、
  Q-Chem、CatMAP、ChemShell、Turbomole、CPMD、SIESTA 或论文自定义代码；
- 2 篇虽然核心软件为功能验证过的 Gaussian/VASP，但方法族仍有未覆盖项，因此按
  `method_coverage_incomplete` 淘汰；
- 1 篇满足完整软件清单、功能验证和方法覆盖，成为 `direct_candidate`。

本轮 Stage 05 有明显的精度优先取舍：interface、catalogued、needs-complete-input 和
未知能力均不当作完整覆盖。它可能漏掉可通过等价工具重建的任务，但符合当前“误筛掉一些
可用论文可以接受，筛出来必须符合要求”的口径。

## 8. 最终候选与 Stage 06

最终候选：

- `paper_id`：`paper_7ef0eff1e6ca2dd9`；
- DOI：`10.1039/d4sc01507j`；
- 题目：*Radical ligand transfer: mechanism and reactivity governed by three-component
  thermodynamics*；
- 研究类型：纯计算、计算为 primary；
- 核心软件：Gaussian 16，工具箱 validation level 为 functional；
- 方法覆盖：无未覆盖方法族；
- SI：本地已有，Stage 06 复用 Stage 02 GROBID 文本，质量分 74.1，0 错误；
- 快速人工复核：未发现作者执行实验；正文提到的实验研究是背景引用，SI 为计算热力学、
  反应势垒、结构和电荷结果。

正文和 SI 分别保存在：

- `stage_00_remote_corpus/corpus/paper_7ef0eff1e6ca2dd9/main/10.1039_d4sc01507j.pdf`；
- `stage_00_remote_corpus/corpus/paper_7ef0eff1e6ca2dd9/supplementary/10.1039_d4sc01507j_sup_0.pdf`。

## 9. 并发与资源释放

50 个微批次均按 Stage 02 -> 03 -> 04 -> 05 -> 06 顺序运行，不同微批次最多 5 路并发。
GROBID、Softcite 池和沙箱在整个任务期间只启动一次，没有在每个阶段反复开关。本次没有
上一轮 79 分钟的异常长尾，500 篇从沙箱申请到全部汇总约 10 分 49 秒。

运行后通过沙箱控制面复核：`sbx-8d68d44e-8ef` 状态为 `Terminated`，环境资源使用为 0。
本次未占用 GPU，也未启动 Qwen3-30B-A3B-Instruct-2507。

## 10. 产物

- 完整运行目录：`data_pipeline/runs/redesigned_stage00_06_500_pure_flash_seed20260808/`；
- 汇总：`run/outputs/run_summary.json`；
- Stage 03 判定和 Flash 缓存：`run/outputs/stage_03_computation_relevance/`；
- Stage 05 能力判定：`run/outputs/stage_05_preliminary_coverage/decisions.jsonl`；
- 最终候选及 SI 证据：
  `run/outputs/stage_06_supplementary_extraction/supplementary_evidence_bundles.jsonl`；
- 本报告只记录运行和审计结果，没有因测试结果继续修改筛选代码。
