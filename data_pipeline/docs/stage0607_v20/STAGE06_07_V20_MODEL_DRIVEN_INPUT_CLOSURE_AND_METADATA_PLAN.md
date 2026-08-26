# Stage06/07 v20 模型驱动输入闭合、证据恢复与论文元数据方案

## 1. 文档状态

本文件是待确认的设计方案，不是已经完成的实现记录。本轮只确定设计边界，不修改
Stage06/07、Gate、Stage00–05 或 benchmark runtime 代码。用户确认本方案后，再单独制定
代码修改计划、测试计划和实施日志。

本方案承接 v19 的以下既定设计：

- Stage06 使用一次连续 Agent 调用，先完成 `paper_reproduction`，自查通过后再派生
  `autonomous_research`；
- Stage07 只负责独立科学审计和有限修复，不重新构建失败任务；
- 两种模式的被评测 Agent 都看不到论文正文和 SI；
- Gate 只阻断最低限度的任务文件和 evaluator 合同问题；
- release 使用 `paper_id + task_type` 管理任务，论文材料与任务包分离。

本方案解决新一轮测试暴露的两个通用问题：

1. 原始 PDF 中存在完整数据，但 Markdown/HTML 表格解析发生单元格粘连时，Stage06
   可能把“解析损坏”错误判定为“科学输入缺失”；
2. 标题、发布日期和作者在 Stage00–05 中已经存在或可以可靠提取，但没有通过统一的
   paper-level metadata 链路进入 Stage06 和 release。

## 2. 核心原则

### 2.1 科学输入由模型判断

代码不替模型决定一篇论文需要哪些科学输入，也不根据论文类别、任务方向或文件格式
强制套用固定检查清单。

Stage06 Agent 负责：

1. 选择一个核心、闭合、非平凡的科学目标；
2. 根据该目标判断需要哪些输入；
3. 检查输入是否存在、可恢复、无歧义并与论文中的科学对象一致；
4. 判断哪些内容可公开给被评测 Agent；
5. 完成任务、参考关键点、参考结论和可执行评分规则。

Stage07 Agent 独立复核 Stage06 的判断。代码和 Gate 不接管上述科学职责。

### 2.2 代码只提供可靠证据访问

代码只负责把已有原始证据以模型可访问、可追溯的方式交给 Stage06/07，包括原始 PDF、
normalized Markdown、content blocks 和必要的布局保真文本。

代码不得：

- 针对特定 `paper_id`、DOI、期刊、化合物或论文类型编写分支；
- 自动决定某一类论文必须提供 XYZ、CIF、SMILES 或某种固定输入；
- 自动重建分子结构、反应路径、晶胞、原子映射或计算参数；
- 自动替 Agent 修正科学身份或选择“正确”化合物；
- 因为某个文件可被 parser 读取，就宣称科学输入已经闭合；
- 因为 Markdown 表格损坏，就直接宣称原始论文缺少科学数据。

### 2.3 Gate 维持最小机械职责

Gate 只检查发布任务能否被稳定加载、执行和评分，不充当计算化学专家。

Gate 可以阻断：

- 必需文件或目录缺失；
- JSON 无法解析或最小字段缺失；
- `paper_id`、`task_type` 不一致；
- task instruction 为空；
- submission schema 无必交文件、主结果文件或结果 schema；
- evaluator 文件为空或引用关系断裂；
- scoring rule 缺少使其无法执行的基本字段；
- evaluator binding 指向不存在的提交文件或字段；
- 论文正文或 SI 被复制进公开 Agent 输入。

Gate 不判断：

- 分子式是否对应论文中的具体化合物；
- 结构是否具有正确化学身份；
- charge、multiplicity、态指认或模型化学是否科学合理；
- 某篇论文应当提供哪种输入；
- 某个 tolerance 是否是唯一正确的科学选择；
- 某一种计算路线是否优于另一种路线。

## 3. 问题归因与设计目标

### 3.1 解析损坏不等于原始数据缺失

当前 Stage06 snapshot 中虽然包含原始 PDF，但 Agent 运行环境不一定具有可用的 PDF
布局读取工具。Agent 往往主要依赖 normalized Markdown；当表格解析器把相邻坐标合并为
类似 `-2.783404-1.943641` 的文本时，模型可能无法验证原始表格，从而过度保守地拒绝
本来可以无损恢复的任务。

设计目标是让模型能够明确区分：

- **无损证据恢复**：原 PDF 中的字段清楚、唯一，只是解析产物破坏了列边界；
- **科学猜测**：原 PDF 本身缺字段、标签冲突或存在多个合理解释，需要人为选择。

前者允许继续构建，后者必须科学拒绝。

### 3.2 文件可解析不等于科学对象正确

一个 XYZ、CIF 或 JSON 能被 parser 读取，只能证明格式成立，不能证明它对应论文中声明的
化合物、构象、电子态或边界条件。

设计目标是要求 Stage06 Agent 根据具体任务完成“输入内容—公开任务声明—论文证据”的
科学交叉核对，并由 Stage07 独立复核；不把这种判断固化为代码规则。

### 3.3 论文元数据应由代码传递，而非模型填写

论文标题、DOI、期刊、发布日期、作者用于数据管理、展示和溯源，不属于任务的科学合成
结果。它们应从 Stage00–05 的结构化记录统一汇总，不能依赖 Stage06 Agent 从正文猜测，
也不能由两个任务模式分别填写。

## 4. 通用证据访问设计

### 4.1 Stage06 immutable snapshot

每个文档的 Stage06 输入快照建议包含：

```text
inputs/documents/<document_id>/
├── document.md
├── content_blocks.jsonl
├── layout_blocks.jsonl
└── source.pdf
```

各文件职责如下：

- `document.md`：适合模型快速阅读和全文检索；
- `content_blocks.jsonl`：保留 evidence ID、页码、章节和文本内容；
- `layout_blocks.jsonl`：保留 PDF 页码、文本块、行或词的顺序及边界框，用于核查表格列、
  坐标和页面布局；
- `source.pdf`：最终原始证据，用于必要时进行视觉确认。

`layout_blocks.jsonl` 是文档访问层，不是科学输入预处理层。它不得：

- 按化学术语重写内容；
- 推断表格语义；
- 自动拼接分子坐标；
- 判断哪组数据属于哪个科学对象；
- 生成被评测 Agent 的输入文件。

最小记录可采用：

```json
{
  "page": 25,
  "block_index": 12,
  "bbox": [102.3, 508.1, 492.8, 690.4],
  "text": "15  6  0  -2.783404  -1.943641  0.767615"
}
```

不默认为整篇论文批量生成页面图片，以避免大体积 SI 带来的存储和上下文开销。只有模型
确实需要视觉确认时，才通过通用方式读取指定 PDF 页面。

### 4.2 通用只读查询能力

Stage06 workspace 可以提供一个轻量、通用、只读的文档查询工具，用于：

- 按 `document_id` 和页码读取布局文本；
- 按关键词定位页码和文本块；
- 显示相邻文本块及其边界框；
- 必要时导出或查看指定 PDF 页面。

该工具不包含任何计算化学知识，不理解“反应物”“过渡态”“产物”等语义，也不输出
“可构建/不可构建”结论。是否能够无损恢复由 Agent 依据原始证据判断。

### 4.3 证据来源优先级不是固定科学规则

模型可按以下一般顺序核查，但可根据论文实际情况调整：

1. normalized Markdown 快速定位；
2. content blocks 确认 evidence ID 和上下文；
3. layout blocks 恢复列、行和页面顺序；
4. 原 PDF 页面视觉确认。

如果低层表示已经充分清晰，不要求模型机械调用所有层；但在因“输入缺失或歧义”准备
科学拒绝时，必须确认问题来自原始证据，而不只是某个派生解析文件。

## 5. Stage06 模型驱动输入闭合

### 5.1 工作顺序

Stage06 保持 reproduction-first 的单 Agent 设计，建议流程为：

1. 阅读上游候选和论文证据，选择科学目标；
2. 根据目标列出完成任务实际需要的公共输入和边界条件；
3. 对每项必要输入检查来源、完整性、标签和可恢复性；
4. 对可能的解析损坏回查 layout blocks 或原 PDF；
5. 检查输入与任务声明、论文科学对象是否一致；
6. 在 `workflow_review.json.input_closure` 中记录结论；
7. 若闭合，先完成完整 `paper_reproduction` 任务和 evaluator；
8. 运行 reproduction-only self-check，修复机械合同问题；
9. 复制稳定基线并语义派生 `autonomous_research`；
10. 审计两种模式的公开面和 evaluator；
11. 运行 full-pair self-check并修复；
12. 最后写 `construction_receipt.json`。

### 5.2 输入检查由科学目标决定

Prompt 不规定所有论文必须检查相同字段。模型应根据任务决定检查内容，例如：

- 分子电子结构任务可能需要结构、元素组成、charge、multiplicity；
- 过渡态任务可能需要反应物、产物、初始猜测、endpoint 或反应坐标边界；
- 周期体系可能需要晶胞、周期边界和组成；
- 激发态任务可能需要几何、电子态、溶剂或环境定义；
- 动力学任务可能需要初始构型、势能模型、温压或采样条件；
- 数据驱动任务可能需要样本、单位、特征定义和划分边界。

这些示例只用于说明“按目标判断”，不得变成代码分支或 Gate 强制字段。

### 5.3 模型可自行使用通用计算辅助核验

Agent 可以根据需要使用 shell、短 Python、文本查询或已有通用工具进行客观核验，例如：

- 统计 XYZ 元素组成；
- 比较声明原子数和实际记录数；
- 检查同一反应路径中结构的标签与组成；
- 比较论文表格与任务 evaluator 的数值、单位和顺序；
- 检查任务要求的交付字段是否都被评分。

这些操作由模型按任务需要主动选择，不新增一个由编排器强制运行的科学输入检查器，也
不新增 `inspect_assets.py` 之类的固定格式框架。

### 5.4 输入一致性审查

对任务所依赖的关键科学对象，Stage06 应核对：

```text
实际输入内容
↔ task.md / task_info 中的公开声明
↔ submission schema 中要求报告的对象
↔ evaluator reference 指向的对象
↔ 论文中的名称、标签、组成、状态或边界证据
```

如果发现冲突：

- 原证据能够唯一纠正：修正任务后重新检查；
- 原证据不能确认正确输入：科学拒绝；
- 不允许仅修改名称来掩盖结构不一致；
- 不允许仅因文件格式可解析就判定科学身份正确。

### 5.5 `input_closure` 的简约记录

`workflow_review.json` 保留通用、可扩展的输入闭合记录，不引入大量化学专用关键词。

通过示例：

```json
{
  "input_closure": {
    "status": "passed",
    "required_inputs": [
      {
        "name": "reactant geometry",
        "source": "SI coordinate table",
        "verification": "Complete coordinates were recovered and matched to the source label.",
        "status": "verified"
      }
    ],
    "unresolved_issues": [],
    "scientific_basis": "The supplied inputs uniquely define the requested calculation."
  }
}
```

拒绝示例：

```json
{
  "input_closure": {
    "status": "failed",
    "required_inputs": [
      {
        "name": "computational molecular model",
        "source": "SI model description",
        "verification": "The source describes a truncation but gives no unique connectivity or coordinates.",
        "status": "unresolved"
      }
    ],
    "unresolved_issues": [
      "Multiple chemically reasonable models satisfy the textual description."
    ],
    "scientific_basis": "Constructing the input would require an unsupported chemical choice."
  }
}
```

Gate 不强制所有记录具有同样的科学子字段，只检查 `input_closure` 的最小结构存在且状态
与 construction receipt 一致。

## 6. Stage06 Prompt 修改方向

Prompt 应明确以下规则：

1. 当前 Agent 是最终任务合成者，不暴露“Stage06”“后续 Stage07 会处理”等流水线角色；
2. 在生成任务前先完成输入闭合判断；
3. 上游 candidate 是线索，不是必须接受的目标；
4. Markdown/OCR/HTML 表格损坏不能单独作为科学拒绝理由；
5. 只要原 PDF 或布局证据能唯一恢复，允许进行无损转录；
6. 原证据缺失或存在多种合理解释时，禁止猜测；
7. 先完成、检查并修复 reproduction，再派生 autonomous；
8. evaluator 必须完整、具体、可执行，不能是空模板；
9. numeric rule 必须正常给出 target、unit、初始 tolerance 和 binding；
10. autonomous 必须隐藏作者路线、答案、排序、机制结论和 tolerance；
11. self-check 是合成任务必须完成的工作，但编排器不强制模型按固定科学检查器执行；
12. terminal receipt 只能最后写入。

Prompt 不应：

- 告诉模型 evaluator 可以随便写、后续人工会补；
- 要求模型机械检查与当前任务无关的固定输入字段；
- 通过关键词黑名单替代语义审查；
- 暗示为了提高通过率应放宽科学输入闭合标准。

## 7. Stage07 独立科学审计

### 7.1 职责

Stage07 只审计和有限修复已经构建的任务，不在 Stage06 科学拒绝时重新构建任务。

重点审计：

- 科学目标是否核心、明确且由论文证据支持；
- 输入是否足以定义任务；
- Stage06 是否把解析损坏误判为原始数据缺失；
- 输入内容、任务声明和论文对象是否一致；
- reproduction 路线是否由论文真实披露；
- autonomous 是否真正隐藏作者路线和答案；
- evaluator 是否覆盖要求提交的关键计算节点和最终结论；
- evaluator 的数值、单位、顺序、条件和语义参考是否有证据；
- 两种模式是否围绕同一科学核心，只在路线披露程度上不同。

### 7.2 有限修复边界

Stage07 可以修复：

- 小范围任务措辞不清；
- 个别引用或 binding 错误；
- 少量 evaluator 遗漏；
- autonomous 中残留的作者路线信息；
- 不改变科学对象的小型元数据漂移。

Stage07 必须拒绝：

- 核心输入指向错误分子或错误科学对象；
- 必要输入不存在或不能唯一恢复；
- 科学目标需要重新选择；
- evaluator 需要大规模重写才能覆盖任务；
- 修复等价于重新构建完整任务。

## 8. 论文元数据统一方案

### 8.1 唯一 canonical paper metadata

在进入 Stage06 前，由代码从 Stage00–05 记录生成唯一 paper-level metadata：

```json
{
  "paper_id": "paper_xxx",
  "title": "...",
  "doi": "...",
  "journal": "...",
  "publication_date": "2026-02-04",
  "publication_year": 2026,
  "authors": ["..."]
}
```

该对象由 Stage06、Stage07、release assembler 和 benchmark package 共用。两个任务模式
不得分别生成论文信息。

### 8.2 字段来源优先级

建议优先级如下：

`title`：

1. Stage01/Stage02 paper-level title；
2. 主文 PDF metadata title；
3. 无可靠值则为空，不让 Stage06 Agent猜测。

`doi` 和 `journal`：

1. Stage01/Stage02 paper-level record；
2. Stage04 canonical main document；
3. Stage00 paper manifest。

`publication_date`：

1. `source_record.publication_date_normalized`；
2. Stage00 `publication_date_normalized`；
3. 可稳定归一化的原始 publication date；
4. 无可靠值则为空。

`authors`：

1. Stage01 GROBID TEI header 的结构化作者列表；
2. 经过明确拆分的主文 PDF Author metadata；
3. 无法确认完整性时使用空数组，不把第一作者冒充完整作者列表。

作者只读取 TEI header 中的作者，不能把 bibliography 的参考文献作者混入论文作者列表。

### 8.3 历史 Stage00–05 run 的 metadata-only backfill

为复用现有 Stage00–05 结果，可以提供通用 metadata backfill：

- 遍历整个 source run，而不是针对五篇论文；
- 从 Stage01 papers、Stage00 manifest、Stage04 main document metadata 和保留的 GROBID
  TEI header 汇总字段；
- 输出 paper-level canonical metadata 索引；
- 不重新运行科学筛选；
- 不修改原始历史记录；
- 不让 Stage06 Agent承担论文目录信息提取工作。

### 8.4 元数据可见性

完整论文 metadata 用于 release 管理、人工审查和 benchmark 展示，不自动暴露给被评测
Agent。最终任务包仍按 v19 设计隔离：

```text
tasks/<task_type>/<paper_id>/
├── agent_input/
├── task_info.json
├── evaluation/
└── package_manifest.json
```

runner 只物化 `agent_input/`。`task_info.json` 中的论文信息不进入 Agent workspace，以免
模型利用题名、DOI 或作者搜索论文答案。

## 9. 不采用的方案

本版本明确不采用：

1. 代码自动生成 evaluator 骨架；
2. 代码按论文类型自动生成或修正科学输入；
3. 强制运行格式专用的 `inspect_assets.py`；
4. 编排器根据元素组成自动批准或拒绝任务；
5. 为某篇论文、某类化合物、某种计算方法添加特殊分支；
6. 放宽 Stage07 以恢复表面通过率；
7. 恢复独立 Stage06B converter、conversion retry 或旧 resume 逻辑；
8. 让 Stage07 在 Stage06 构建失败后重新构建；
9. 把论文 PDF/SI 复制到两种模式的 `agent_input/`；
10. 让 Agent填写本可由上游代码可靠传递的论文目录元数据。

## 10. 预期代码修改范围

用户确认后，详细代码计划预计覆盖：

- `src/stages/stage06_task_builder/stage.py`
  - 接收 canonical paper metadata；
  - 生成布局保真 snapshot；
  - 安装通用只读文档查询能力；
  - 不加入科学输入判断器。

- `src/stages/stage06_task_builder/prompts.py`
  - 增加无损恢复与科学猜测的边界；
  - 强调模型驱动输入闭合；
  - 保持 reproduction-first 和两次 self-check。

- `src/stages/stage07_task_judge/prompts.py`
  - 增加独立输入身份和解析来源审计；
  - 保持有限修复、不可重建边界。

- `src/stages/stage07_task_judge/package.py`
  - 直接使用 canonical paper metadata；
  - 不再从已经为空的 document projection 二次拼接。

- Stage01/Stage00–05 metadata 相关代码
  - 持久化 GROBID header authors 或提供通用 metadata-only backfill；
  - 统一标题、日期和作者来源。

- 通用文档访问模块和测试
  - PDF layout extraction；
  - 页码/关键词查询；
  - 不包含化学专用规则。

- Gate
  - 原则上不扩展科学判断；
  - 仅在必要时补充 `input_closure` 最小结构一致性检查；
  - 保持 Agent self-check 与外部 Gate 使用同一机械合同。

## 11. 测试方案

### 11.1 固定通用 fixtures

必须用通用合成 fixture 验证，不在生产代码中写入测试论文信息：

1. Markdown 表格字段粘连、layout blocks 完整：模型可回查并无损恢复；
2. Markdown 与 layout blocks 都缺字段、原 PDF 无法确定：允许科学拒绝；
3. 文件可解析但任务声明和源证据指向不同科学对象：Stage06 或 Stage07 应拒绝；
4. evaluator 文件完整但没有覆盖公开要求的关键结果：Stage07 应发现；
5. Stage02 有标题、Stage00 有 normalized date：release metadata 完整；
6. GROBID header 有完整作者、PDF metadata 只有第一作者：优先使用 GROBID；
7. GROBID 无可靠作者、PDF metadata 完整：允许使用可靠 fallback；
8. 两种任务包完整且 autonomous 不暴露论文路线：正常发布；
9. 论文 PDF/SI 出现在公开输入：Gate 阻断；
10. Agent self-check 与 external Gate 对同一文件树返回一致的机械结果。

### 11.2 五篇历史样本行为回归

固定 fixture 通过后，再使用同样五篇论文进行整体回归。测试目的不是强求固定通过数量，
而是核对拒绝理由是否来自真实科学问题。

根据当前证据，预期行为为：

- 两篇已经稳定发布的任务继续通过；
- 一篇因 Markdown 表格粘连而误拒绝的任务，应能通过原 PDF/布局证据重新完成输入闭合并
  进入 Stage07；
- 一篇存在分子身份冲突的任务不得因提高召回率而被放行；
- 一篇缺少唯一原子模型的任务，在原证据仍不足时继续科学拒绝。

以上预期只写入测试报告，不得转化为生产代码中的 paper ID 特例。

## 12. 验收标准

代码实施完成后必须同时满足：

1. 生产代码和 Prompt 中不存在针对测试论文的 paper ID、DOI、标题、期刊、化合物或数值
   特例；
2. 科学输入由 Stage06 Agent 根据目标判断，代码不自动决定输入方案；
3. Stage06 能访问足以区分解析损坏和原始缺失的证据表示；
4. 无损恢复允许继续，科学猜测仍被禁止；
5. 文件格式可解析不会被等同为科学身份正确；
6. Stage07 独立审计输入身份、科学目标和 evaluator，不重建任务；
7. Gate 只保留最小机械合同职责；
8. evaluator 仍必须完整、具体、可执行，不能是空模板；
9. 标题和 normalized publication date 能从 Stage00–05 正确进入 release；
10. authors 只来自可靠 paper header metadata，不混入参考文献作者；
11. 论文元数据不自动暴露给被评测 Agent；
12. Agent self-check 与 external Gate 的机械语义一致；
13. 单元测试、定向回归测试和五篇行为回归均有独立报告；
14. 完成代码后必须逐条回看本方案并记录一致性检查结果。

## 13. 确认后的实施顺序

本方案确认后，下一步再执行：

1. 编写详细代码修改计划；
2. 建立固定 fixtures 和当前行为基线；
3. 实现 canonical paper metadata；
4. 实现通用 PDF layout 证据访问；
5. 修改 Stage06 Prompt；
6. 修改 Stage07 Prompt；
7. 保持或最小调整共享 Gate；
8. 完成单元与定向回归；
9. 对照本方案做一致性审计；
10. 再提交五篇历史样本测试并形成科学质量分析报告。

在用户确认本文件前，不进入上述代码实施阶段。
