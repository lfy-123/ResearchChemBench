# Stage03 Prompt 与数据流说明

更新时间：2026-08-08

本文描述当前代码的实际行为，主要对应 `src/v2/stages/stage02.py`、
`src/v2/stages/stage03.py` 和 `src/v2/prompts.py`。

## 1. Stage03 的准入条件

Stage03 只处理 Stage02 论文级记录满足以下全部条件的论文：

1. `decision == "pass"`；
2. canonical 正文解析成功，即 `main_parse_ok == true`；
3. 若 `package_status == "complete_with_si"`，全部已知、canonical SI 都解析成功，即
   `supplementary_parse_ok == true`；
4. `partial_si_parse == false`。

Stage02 会记录 `known_supplementary_documents`、`parsed_supplementary_documents` 和
`failed_supplementary_document_ids`。任意已知 SI 失败时，论文在 Stage02 得到 `parse_failed`，不调用
Stage03 模型。Stage03 还会重复检查这些字段，以防旧缓存中“至少一个 SI 成功就放行”的记录进入模型。
`complete_confirmed_no_si` 表示 Stage01 已确认没有 SI，这类论文只要求正文成功。

这里的“全部已知 SI”指 Stage00 已映射到该论文且去重后保留的 canonical 补充材料；同一文件的重复副本
不重复解析，也不构成额外失败条件。

## 2. 喂给模型的论文内容

Stage03 从每个合格论文包的 `document_ids` 读取：

- canonical 正文的 `content_blocks.jsonl`；
- 每一个已知且已成功解析的 SI 的 `content_blocks.jsonl`；
- PDF 经 GROBID 解析，GROBID 失败或质量不合格时使用 `pdftotext`；
- 可解析的非 PDF SI 使用相应资产解析器规范化后也进入同一数据流。

当前实现不只选择摘要或方法段，也不先按关键词丢弃章节。标题、摘要、正文、方法、结果、图表说明和
SI 中已经抽取成文本的块都会参与，以降低软件名称或计算细节仅出现在 SI 时的漏筛风险。每个输入块只
保留以下字段：

```json
{
  "evidence_id": "...",
  "document_id": "...",
  "page": 12,
  "section_path": ["Computational methods"],
  "block_type": "paragraph",
  "text": "..."
}
```

整块或长文本片段若主要是元素符号和三维坐标，会在调用模型前删除；相邻的自然语言说明尽量保留。
其余文本按 UTF-8 字节边界组成默认不超过 9000 bytes 的 chunk。正文与 SI 使用相同证据协议，
`document_id` 和 `evidence_id` 用来区分来源并回映原文。

Stage02 的 GROBID 文本足以用于“是否存在计算流程”的粗筛，但公式、复杂表格和版面信息并不完整。
Stage03 不据此构建最终任务；通过 Stage04 工具箱/成本门控后，Stage04 才用 MinerU 做高质量重解析。

## 3. Map prompt：逐块抽取证据

每个 chunk 使用同一个部署 screening LLM。system prompt 是固定、带版本的
`STAGE03_MAP_SYSTEM`；user message 是紧凑 JSON：

```json
{"paper_id": "...", "chunk_index": 0, "blocks": [/* 上述文本块 */]}
```

Map prompt 要求模型严格区分三类信息：

1. 当前论文作者实际执行的分子、原子、电子、反应或材料计算；
2. 当前作者对真实样品执行的合成、制备、测量、表征、光谱、衍射、电化学或 assay；
3. 论文只引用或使用的外部实验结构、数据库和历史测量值。

可接受的计算必须从模型或结构出发，执行实际计算/模拟，并产生结构、能量、电子性质、模拟光谱、轨迹、
自由能、反应路径、速率、声子或分子/材料预测等化学结果。DFT、从头算、MD、Monte Carlo、QM/MM、
声子、计算光谱和 ML 分子/材料筛选属于计算，不属于作者实验。

以下内容单独出现时不算目标计算化学：实验数据的常规拟合/统计、图像处理、绘图、单独 XRD/Rietveld
精修、仪器软件、LCA/流程/经济模型、数据库查询和 AlphaFold-only 工作。prompt 内含 DFT/MD、外部
XFEL/PDB、作者 NMR 和催化剂合成测试等正反例，以约束归因边界。

Map 返回紧凑 JSON：

```text
has_computational_evidence
evidence[]: evidence_id, exact_quote, method_family, model_system, action,
            computed_outputs, software_clues, attribution, confidence
author_experiment_evidence[]: evidence_id, exact_quote, experiment_type,
                              attribution, confidence
background_only_evidence[]
conflicts[]
```

每块最多返回 3 条计算证据、2 条作者实验反证和 2 条背景证据，默认输出上限为 2048 tokens。

## 4. Map 后的确定性校验

模型输出不会直接用于论文结论。程序逐条执行：

- `evidence_id` 必须来自本次 chunk；
- `exact_quote` 必须逐字存在于该 evidence block；
- 计算证据只保留 `attribution == "this_paper"`；
- 作者实验证据除归因外，还必须命中“作者执行动作 + 实验技术/对象”的确定性规则；
- `published`、`previously reported`、PDB、database 等外部数据语境不能作为作者实验；
- 计算、模拟、calculated spectrum 等语境不能因含有 spectrum 等词而误作实体实验。

模型响应若因 token 上限截断，会用更紧凑的 prompt 重试；连续截断才将该论文记为处理失败。完整 map
响应、通过校验的证据和模型审计写入 `chunk_reviews.jsonl`，不会只保留最终标签。

## 5. Reduce prompt：论文级严格判定

Reduce 仍使用同一个 screening LLM，但不重新发送全文。输入由全部正文/SI chunk 的校验证据组成：

- 最多 12 条、优先高置信度的计算证据；
- 最多 12 条作者实验反证；
- 每个 chunk 的计算/实验/背景/冲突证据计数；
- 每条证据包含原文 quote、方法、动作、软件或结果线索及 evidence ID。

Reduce prompt 要求同时满足以下条件才能输出 `computational_content_confirmed`：

1. `article_role == original_research`；
2. 当前作者确实执行目标计算；
3. 计算是论文的主要科学工作，而非少量辅助或背景；
4. 论文是 `pure_computational`，当前作者没有实体实验；
5. 存在“模型/结构 -> 计算或模拟 -> 化学结果”的完整工作流；
6. 存在通过原文校验的计算证据；
7. 置信度不低于默认阈值 0.75。

外部实验结构或已有实验数据库可作为输入/比较，不会因此淘汰纯计算论文；但当前作者同时合成、测量或
表征真实样品时，即使 DFT/MD 是主要部分，也输出 `not_pure_computational`。这正是当前“高精度、允许
漏筛”的严格策略。

Reduce 输出字段为：

```text
decision
article_role
performed_computation
computation_role
study_mode
author_performed_experiments
workflow_complete
method_families
computational_actions
software_clues
resource_clues
evidence_ids
experimental_evidence_ids
conflicting_evidence_ids
rationale
confidence
```

`decision` 可取：`computational_content_confirmed`、`not_pure_computational`、
`computational_content_not_found`、`background_only` 或 `uncertain`。`uncertain` 默认重审一次；模型声称
存在作者实验但没有通过校验的实验 quote 时，也会转为 `uncertain`，而不是直接淘汰。

## 6. 最终产物与边界

`decisions.jsonl` 保存论文级结论、完整 review、校验后的计算/实验依据、跳过的坐标块数、校验告警和
模型审计；`rejected.jsonl` 保存明确淘汰项，`held.jsonl` 保存不确定或处理失败项，
`stage_summary.json` 汇总输入、合格、不合格论文数和各 decision 数量。

Stage03 只决定“是否为具有完整主计算流程的纯计算化学原创论文”。它会输出软件和资源线索，但不声明
工具箱覆盖，也不做最终成本判定；这些由 Stage04 使用冻结能力快照和更深文本完成。
