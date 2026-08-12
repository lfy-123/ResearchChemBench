# Stage05 单 API 回退与历史结果分析

日期：2026-08-12

## 回退边界

Stage05 已恢复到提交 `2f3cab8` 的单 API suitability gate。每篇论文读取 Stage04 MinerU 正文和全部
已知 SI 的结构化块，构造一个有界的跨文档 evidence packet，然后调用一次配置为 `suitability` 的
OpenAI-compatible 模型。只有模型响应违反 JSON/字段合约时，代码才用原始响应和验证错误做一次合同
修复；该修复不得改变科学结论，不构成第二轮独立审查。

未完成的 Flash 阅读 Agent、独立论文 workspace、Agent 评测入口及其依赖已经移除。Stage05 的默认
模型改为 `deepseek-v4-flash`，但可以通过 `RCB_SUITABILITY_*` 环境变量替换模型和 endpoint。

## 单 API 的输入和判定

单 API 输入包含：

- Stage04 通过论文的 MinerU 正文与全部 SI 证据块；
- Stage03 冻结的软件覆盖事实、工作流和资源预算；
- 十类 benchmark 任务 taxonomy；
- 最多一个候选、至少三个相互依赖科学步骤、隐藏目标和机器评分等合同要求。

代码在模型返回后确定性检查 taxonomy、工作流深度、输入/参数/ground truth、软件覆盖、成本、证据 ID
和输出合同。只有 `pass` 与 `needs_builder_review` 进入 Stage06；`reject`、`contract_invalid` 和处理
错误都不进入 Builder。

## 24 篇历史结果的可比范围

仓库中保留下来的单 API 完整实测是 DeepSeek V4 Pro，而不是 Flash。最终校准运行
`stage05-deepseek-v4-pro-eval-20260812-iteration3` 得到 2 `pass`、10 `needs_builder_review`、12
`reject`、0 处理错误；26 次调用约使用 1,031,404 tokens，8 并发墙钟约 335 秒。该提示词在这 24 篇
上反复开发，因此与人工最终标签 24/24 一致不能视为独立泛化准确率。

同一批论文的 GPT-5.6-sol + Codex 全文审查记录给出 2 `pass`、2 `needs_builder_review` 和 20
`reject`。与人工最终校准相比，三分类仅 11/24 一致；把 `pass` 和 `needs_builder_review` 都视为
“值得进入 Builder”时，仅 12/24 一致。13 个三分类分歧中，一个是 `pass`/`needs_builder_review`
的等级分歧；二元分歧包含 10 个 Codex 拒绝但人工认为应转交 Builder 的候选，以及 2 个 Codex 放行但
人工认为应拒绝的候选。

因此，这组结果不能支持“上下文越完整，结论自然越准确”。Codex 确实读取了全文和 SI，但采用了更
保守且不完全一致的可构建性边界，尤其容易把可由 Builder 确定性恢复的标准结构、输入或参数缺口直接
视为拒绝。相反，单 API Pro 与人工标签 24/24 一致，是在同一 24 篇上多轮修改 prompt 得到的校准
结果，也不能证明泛化能力。两者共同说明判定合同、`needs_builder_review` 边界和独立 holdout 比单纯
增加模型强度或全文上下文更重要。

## 对后续 Stage05 设计的结论

当前单 API 版本适合作为稳定、便宜、可审计的基线，但有两个已知限制：

1. Evidence packet 有界，可能遗漏分散在长 SI 后部的坐标、参数或结果表；更强模型不能恢复根本没进入
   上下文的信息。
2. 单次调用同时承担证据定位和候选裁决，模型可能在“找不到证据”和“证据确实不存在”之间混淆。

因此后续若重新设计 Stage05，应在新的独立 holdout 上分别测量最终放行 precision、false-negative
rate、每篇 token 和延迟。现阶段不应继续把这 24 篇校准集上的一致率作为选型依据，也不应在没有
Flash 新运行产物的情况下把 Pro 的历史结果归因给 Flash。
