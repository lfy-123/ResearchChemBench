# ResearchChemBench 数据管线当前进度与阶段设计

更新时间：2026-08-03

## 当前进度

数据管线已收敛为 7 个阶段。Stage 01-04 核心筛选逻辑保持不变，旧的冗余后续阶段已删除并替换为新的 Stage 05-07。

当前状态：

- Stage 05 有边界资产发现、下载、溯源、安全展开和增量解析已完成真实测试。
- Stage 06 Builder Agent 已支持 `codex`、`claude`、`opencode`，并通过 OpenCode + `deepseek-v4-flash` 真实测试。
- Stage 07 Judge Agent 使用独立工作区和会话，已正确拒绝一个能通过基础校验但实际不可执行的候选任务。
- Builder/Judge 的 prompt、Schema、CLI 事件、聊天记录、stdout/stderr、token 和运行元数据均会保存。
- 自动化测试：29 passed，另有 6 个 subtests passed；Ruff、Vulture 和 `git diff --check` 通过。
- 当前只保存到本地 Git，不推送 GitHub。

## 七阶段设计

### Stage 01：论文清点与去重

扫描 PDF，计算哈希并结合 DOI、标题和文件角色去重。重复正文和被排除的补充材料不进入后续阶段。

### Stage 02：GROBID 结构化解析

提取标题、摘要、作者、DOI、章节、正文、参考文献、TEI XML 和纯文本。

### Stage 03：软件与工具箱覆盖

使用 Softcite 识别实际使用的核心软件，并与 ResearchChemBench 工具箱匹配。主流程仅保留 `direct_covered` 论文。

### Stage 04：资源上限审查

通过关键词、GROBID Quantities 和模型结构化资源记录，再由 Python 与 CPU、GPU、内存和运行时间上限比较。仅明确超限时淘汰。

### Stage 05：有边界的资产发现、下载与增量解析

以 DOI、Availability 文本、仓库和数据标识符为线索，查询 Crossref、DataCite、OpenAlex、GitHub、Zenodo、OSF 和 Materials Cloud。最多三轮，无新资产时提前结束。

每项资产保留原始文件、SHA-256、来源、版本、父子关系、结构化 JSON 和 Agent 可读 Markdown/TXT。新 PDF 立即使用 MinerU；压缩包安全展开并公平分配资产预算。

### Stage 06：Builder Agent

Builder 在隔离只读输入快照中构建一个候选计算化学智能体任务，输出公开输入、隐藏参考、评分规则和证据映射；证据不足时返回 `abstain`。

### Stage 07：Judge Agent

Judge 在新的独立 workspace、HOME 和会话中审查候选，不读取 Builder 聊天。审计论文忠实性、数据充分性、工具箱支持、答案泄漏、评分和资源可行性，输出 `pass`、`revise` 或 `reject`。

当前版本到 Stage 07 结束，不包含人工发布，也不实现 Builder-Judge 自动循环修订。

## 最新测试输出

```text
Stage 05:
data_pipeline/runs/stage05_network_mbpt_20260803_v8/outputs/stage_05_asset_collection/

Stage 06:
data_pipeline/runs/stage06_07_opencode_mbpt_20260803_v5/outputs/stage_06_builder/

Stage 07 负例审计:
data_pipeline/runs/stage06_07_opencode_mbpt_20260803_v6/outputs/stage_07_judge/
```

完整分析见 `docs/STAGE_05_07_IMPLEMENTATION_AND_TEST_REPORT_20260803.md`。
