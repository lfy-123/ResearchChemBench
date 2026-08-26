# Stage06/07 v20 代码修改计划与实施日志

## 1. 目标与边界

本轮实现以
`STAGE06_07_V20_MODEL_DRIVEN_INPUT_CLOSURE_AND_METADATA_PLAN.md` 为唯一设计基线。
目标是修复两类通用缺陷：

1. Stage06 只能依赖容易破坏表格列边界的 Markdown，无法可靠区分“解析损坏”和
   “原始证据缺失”；
2. 上游已有的标题、日期和作者没有形成唯一的 canonical paper metadata，release 中
   论文信息为空。

本轮不新增论文、论文类型、化合物或计算方法特例；不让代码选择科学目标、重建化学
输入或判断科学身份；不扩大 Gate 的科学判断职责。

## 2. 修改前基线

固定五篇论文：

- `paper_2aca1dd116799b28`
- `paper_611000e1de080f6f`
- `paper_76ae2dc25f0a5aeb`
- `paper_9455a82229de2427`
- `paper_a5564360a31f760b`

对照 run：

`runs/stage0607-v19.1-gpt-5.6-sol-20260826-reproduction-first-5-rerun3`

基线结果：两篇发布；`2aca` 因派生 Markdown 中坐标列粘连而误拒绝；`611` 因输入分子
身份与任务声明冲突被 Stage07 正确拒绝；`a556` 因原始证据不足以唯一确定模型而拒绝。

代码基线：

- Stage06 snapshot 包含 Markdown、content blocks 和 PDF，但没有布局保真文本与稳定查询
  工具；
- Stage06 `paper_info` 只从 Stage04 document 的少量顶层字段拼接；
- 历史加载器没有汇总 Stage01 paper/document metadata 或 GROBID TEI header；
- Stage06/07 Prompt 已采用 reproduction-first 和有限审计，但没有明确“拒绝前回查原始
  布局证据”和实际输入—任务—evaluator 的科学身份闭环。

## 3. 代码修改计划

### P1. canonical paper metadata

新增一个小型共享模块，输入为 paper-level 上游记录、文档记录和可选 GROBID TEI，输出
唯一对象：`paper_id/title/doi/journal/publication_date/publication_year/authors`。

- 标题、DOI、期刊优先使用 paper-level 结构化记录；
- 日期优先使用 normalized source date；
- 作者优先读取主文 GROBID TEI header；PDF Author 只作为明确可拆分的 fallback；
- 不从正文或参考文献猜作者；
- 历史加载器通用定位 Stage01 records 与主文 document 对应的 TEI，不修改历史 run；
- canonical metadata 显式传给 Stage06，并由 Stage06/Stage07/release 共用。

### P2. 通用 PDF layout 证据层

新增一个无化学语义的 PDF 访问模块：

- 使用 PyMuPDF 按页输出 `layout_blocks.jsonl`；
- 每条只记录 page、block_index、bbox、text；
- 在 Stage06 snapshot 构建时从已有 source PDF 生成；
- 提供只读 CLI，可列文档、按页读取、关键词查询并显示相邻块；
- 工具不重建坐标、不判断化合物、不给出可构建结论；
- 查询工具与共享 phase Gate 一起安装到 Agent workspace 后冻结。

### P3. Stage06 模型工作流

更新 Prompt 和版本号：

- 将 Agent 定位为最终合成者，不使用 Stage06/Stage07 流水线身份叙述；
- 科学拒绝前必须确认缺陷存在于原始/layout 证据，而非仅存在于 Markdown/OCR；
- 允许从唯一、清楚的原始证据无损转录，禁止在原始证据存在多解时猜测；
- 根据所选目标自行检查必要输入，不要求固定科学字段；
- 核对实际公开输入、任务声明、submission schema、evaluator 和论文对象；
- 保持先 reproduction、自查修复、再派生 autonomous、全对自查、最后 receipt；
- evaluator 继续要求完整、具体、可执行。

Stage06 实现接收 canonical metadata；snapshot hash 纳入 metadata 和 layout extractor 版本；
构建与科学拒绝均写入同一个 canonical `paper_info.json`。

### P4. Stage07 独立审计

更新 Prompt 和版本号：

- 检查 Stage06 是否将派生解析损坏误当作原始缺失；
- 独立核对实际输入—公开任务—schema—evaluator—论文证据的科学对象一致性；
- 检查 evaluator 是否覆盖关键过程节点与最终结论；
- 保持仅做有限、source-determined 修复；不得重建失败任务或更换目标。

Stage07 package 直接保留 canonical metadata，不再重新推断字段。

### P5. Gate 边界

不新增元素组成、结构、charge/spin、任务类型或 tolerance 科学规则。现有 Agent self-check
和 external Gate 继续调用同一 `src/stages/phase_gate.py`。`input_closure` 只由 Prompt 和
科学审计负责，本轮不增加编排器科学强制检查。

### P6. 测试

新增 v20 定向测试：

1. layout extraction 保留 page/text/bbox；
2. Markdown 字段粘连但 PDF layout 清晰时，可通过通用查询读取原始分列；
3. CLI 支持 pages/contains/context；
4. canonical title/date/year；
5. GROBID header authors 优先于不完整 PDF Author；
6. 无 TEI 时的可靠 PDF Author fallback；
7. release metadata 完整且不进入 `agent_input`；
8. Prompt 明确模型驱动输入闭合、原始证据回查和独立 Stage07 审计；
9. 生产代码不包含固定论文或化学特例；
10. v19 合同测试及相关 Stage06/07 测试全部通过。

### P7. 实施后审计与真实回归

- 逐条对照 v20 设计的 14 项验收标准；
- 用 `git diff` 检查冗余、兼容投影和范围外修改；
- 分阶段提交，仅提交本轮文件；
- 使用 `gpt-5.6-sol`、`high`、并发 5 跑固定五篇；
- 监督 batch 状态、Stage06/07 receipt、Gate report 和 Agent trace；
- 比较 v19.1 与 v20 的发布/拒绝归因、工具失败、重复调用、元数据和双模式任务质量。

## 4. 实施日志

| 步骤 | 状态 | 记录 |
|---|---|---|
| P1 canonical metadata | 完成 | 新增共享 metadata 模块；历史加载器读取 Stage01 source record 和 GROBID TEI；实时管线传递同一 canonical 对象。真实五篇验证补回标题、日期、年份和作者。另用“TEI 前缀与完整 PDF 作者序列一致”的通用规则清除 GROBID 误识别的机构片段。 |
| P2 layout 证据层 | 完成 | PyMuPDF 生成 1-based page、bbox、block text；安装通用只读查询 CLI。`2aca` SI 第 26 页成功恢复 `-2.783404   -1.943641` 的原始列边界。未恢复旧 parser JSON/图片投影。 |
| P3 Stage06 | 完成 | 接收 canonical metadata；snapshot 生成 layout blocks；Prompt 要求目标驱动输入闭合、拒绝前回查原始证据、对象一致性核对、reproduction-first 和完整 evaluator。 |
| P4 Stage07 | 完成 | 安装相同文档查询能力；Prompt 增加解析来源、实际输入身份和 evaluator 独立审计；仍只允许有限修复、不重建。 |
| P5 Gate 边界 | 完成 | 未加入科学输入规则。仅把旧 `closed` 枚举统一为 v20 `passed`，Agent self-check 与 external Gate 仍调用同一代码。 |
| P6 测试 | 完成 | 新增 10 项 v20 定向测试；v19/v20/late-stage 定向测试 22 passed；全量测试 409 passed。 |
| P7 一致性审计与五篇回归 | 完成 | 固定五篇以 `gpt-5.6-sol`、`high`、并发 5 完成：4 published、1 scientific rejection、0 technical/mechanical block。逐文件质量审查见 `STAGE06_07_V20_FIVE_PAPER_REGRESSION_AND_QUALITY_ANALYSIS.md`。核心证据恢复和 Gate 对齐目标达到；另发现 public schema 答案泄露、Stage07 repair receipt 不真实、部分 autonomous evaluator 与方法自由度不完全匹配等后续问题。 |

## 5. 变更与提交记录

本节随实施更新。任何提交都只包含本轮明确列出的文件，不纳入工作区已有的 Stage00–05、
chemistry toolbox 或其他文档修改。

- `b0bbf81 feat(stage0607): add model-driven evidence closure`：v20 代码、测试、设计与实施日志；
- 五篇真实回归 run：
  `runs/stage0607-v20-gpt-5.6-sol-20260827-model-driven-input-closure-5`；
- 回归和任务质量分析：
  `STAGE06_07_V20_FIVE_PAPER_REGRESSION_AND_QUALITY_ANALYSIS.md`。

## 6. 方案一致性审计

| v20 验收项 | 代码结果 |
|---|---|
| 1. 无测试论文/化学特例 | 通过。生产代码没有五篇 paper ID、DOI、化合物或数值。 |
| 2. 科学输入由 Stage06 判断 | 通过。代码只提取通用 PDF 文本块；Prompt 明确目标驱动检查。 |
| 3. 可区分解析损坏与原始缺失 | 通过。snapshot 同时提供 Markdown、content blocks、layout blocks 和 PDF。 |
| 4. 允许无损恢复、禁止猜测 | 通过。Stage06/07 Prompt 均明确该边界。 |
| 5. 格式可解析不等于科学身份正确 | 通过。两段 Prompt 均要求跨输入、任务、schema、evaluator、论文证据核对。 |
| 6. Stage07 独立审计且不重建 | 通过。职责和允许修复边界未扩张。 |
| 7. Gate 只做最小机械合同 | 通过。只统一 `input_closure.status=passed`；未加入化学判断。 |
| 8. evaluator 完整可执行 | 通过。既有最小 evaluator 合同和 Prompt 要求保留。 |
| 9. 标题和 normalized date 进入 release | 通过。真实五篇 metadata-only backfill 已验证。 |
| 10. authors 只来自可靠 header metadata | 通过。TEI 为主；完整 PDF 列表只在可交叉核对时清除 TEI 尾部污染。 |
| 11. metadata 不暴露给被评测 Agent | 通过。metadata 写在任务包根部；release runner 的 `agent_input/` 不含论文 metadata/PDF。 |
| 12. self/external Gate 语义一致 | 通过。两者继续使用共享 `phase_gate.py`。 |
| 13. 单元、定向、真实回归有报告 | 通过。单元与定向记录见下节；五篇真实回归和逐任务质量审查已有独立报告。 |
| 14. 完成后逐条回看方案 | 通过。代码边界与方案一致；真实运行另暴露了语义泄露审计和审计回执真实性问题，未把这些问题错误归入机械 Gate。 |

## 7. 验证记录

- `python -m pytest -q tests/test_stage0607_v20_evidence_and_metadata.py \
  tests/test_stage0607_v19_contracts.py tests/test_late_stage_runner.py`：22 passed；
- `python -m pytest -q`：409 passed；
- `git diff --check`：通过；
- 真实 SI layout smoke：`paper_2aca...` 共提取 2370 blocks、84 pages，第 25 页定位
  `R-EDY 15`，第 26 页保留原始分列坐标；
- 真实 metadata smoke：五篇均有 normalized publication date；此前为空的 `2aca` 标题已从
  GROBID header 补回；`76ae` 的 GROBID 机构污染由一致的完整 PDF 作者列表纠正。
- 五篇真实回归：4 published、1 scientific rejection、0 technical block、0 mechanical
  publish block；四篇发布任务的 Stage06 self-check 和 external Gate 一致通过；
- 回归质量结论：`2aca` 的解析误拒绝根因已经解决，`a556` 的科学拒绝合理，`9455` 的
  Stage07 evaluator 修复有效；`611` 改为 coordinate-defined model 后内部闭合，但需人工
  重点复核其代表性；另有 public schema 答案泄露、repair receipt 与真实 diff 不一致和
  metadata 字符归一化等非阻塞问题，详见独立报告。
