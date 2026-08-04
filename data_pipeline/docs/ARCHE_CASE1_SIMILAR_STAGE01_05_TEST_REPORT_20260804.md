# ARCHE Case1 相似论文 Stage 01-05 测试报告

## 1. 测试目标

本次测试不再使用材料计算或高通量工作流论文，而是围绕 ARCHE Case1 的研究形态选择
小分子反应机理、过渡态和立体选择性 DFT 论文，完整启用数据管线前五个阶段，重点检查：

1. Stage 03 能否保留工具箱支持的 Gaussian/CREST 论文并淘汰不支持的软件。
2. Stage 04 能否只对明确的 CPU、GPU、内存和运行时间证据进行资源审查。
3. Stage 05 能否发现、下载、溯源、展开并解析正式补充材料。
4. 对这类 Case1 风格论文，正文是否足以构造任务，补充材料实际包含什么。

正式输出目录：

```text
runs/arche_case1_similar_20260804/run_full_v4/outputs
```

测试论文目录：

```text
runs/arche_case1_similar_20260804/pdfs
```

## 2. 论文集

| 论文 | DOI | 选择原因 |
|---|---|---|
| Transition States of Vicinal Diamine-Catalyzed Aldol Reactions | `10.1021/jacs.5b12097` | ARCHE Case1 对应研究，Gaussian 09 过渡态与立体选择性分析 |
| Mechanism and Origins of Stereoselectivity of the Aldol-Tishchenko Reaction of Sulfinimines | `10.1021/acs.joc.0c02862` | Gaussian 16 + CREST，反应机理和立体选择性 |
| Two chiral catalysts in action | `10.1039/c8sc03078b` | Gaussian 09，双有机催化剂协同和立体控制 |
| DFT investigation of NHC-catalyzed asymmetric organosilane cycloaddition | `10.1039/d4ra03676j` | Gaussian 09，完整反应路径和选择性来源 |
| Proline-catalysed asymmetric aldol reaction of acetone and p-nitrobenzaldehyde | `10.1016/j.jare.2018.03.002` | 与 Case1 反应物高度相近，但核心软件为 Spartan 14，用作 Stage 03 负例 |

### 2.1 Case1 正文来源说明

ACS 出版社版本不是开放全文。本次没有使用来源不明的论文副本，而是下载 Adam Simon 的
UCLA 开放博士论文，并抽取其中完整 Chapter 1。该章明确说明是 Case1 论文的修改版本，
测试 PDF 前增加了一页来源说明，记录原论文 DOI 和开放来源。

因此 `arche_case1_vicinal_diamine_aldol.pdf` 在科学内容上覆盖 Case1 论文，但不是 ACS 排版的
四页 Version of Record。这个差异必须在后续数据溯源中保留。

## 3. 运行概况

正式运行从 2026-08-04 05:44:40 到 06:04:11，约 19 分 31 秒。

| 阶段 | 主要结果 | 约耗时 |
|---|---|---:|
| Stage 01 | 5 篇正文，0 重复，0 补充材料输入 | <1 秒 |
| Stage 02 | 5/5 GROBID 成功，无回退 | 50 秒 |
| Stage 03 | 4 篇直接覆盖，1 篇不支持 | 68 秒 |
| Stage 04 | 4 篇均无明确资源信息，全部放行 | 14 秒 |
| Stage 05 | 4 篇正文和 7 项补充资产全部解析成功 | 17 分 19 秒 |

Stage 05 的 7 项补充资产包括 3 个出版社补充 ZIP 和 ZIP 内的 4 个 SI PDF，不能理解为
7 份相互独立的补充文档。

## 4. Stage 01：论文清点与去重

### 目标

建立可靠入口，识别正文、补充材料和重复文件，只把去重后的正文送入后续阶段。

### 结果

- PDF 数：5
- canonical PDF：5
- duplicate PDF：0
- supplementary PDF：0
- 下游正文：5

本次语料已人工按测试目标整理，因此没有触发去重或正文/附件冲突。Stage 01 的输出符合预期。

## 5. Stage 02：GROBID 结构化解析

### 目标

从正文低成本提取标题、作者、DOI、章节和结构化文本，为 Stage 03、Stage 04 和 Stage 05
提供统一文档对象。

### 结果

5 篇均通过 GROBID，单篇 PDF 请求失败数为 0，没有触发 `pdftotext -layout` 回退。

| 论文 | DOI | 页数 | 提取字符数 | 评价 |
|---|---|---:|---:|---|
| Aldol-Tishchenko | `10.1021/acs.joc.0c02862` | 8 | 30,702 | 标题、作者、日期正确；章节偏向实验部分，但正文可读 |
| ARCHE Case1 | `10.1021/jacs.5b12097` | 14 | 10,968 | 标题、作者、DOI正确；日期缺失，因输入是论文改写章节 |
| NHC cycloaddition | `10.1039/d4ra03676j` | 15 | 41,954 | 方法、反应路径、选择性章节完整 |
| Spartan aldol | `10.1016/j.jare.2018.03.002` | 9 | 24,104 | 元数据和计算细节章节合理 |
| Two chiral catalysts | `10.1039/c8sc03078b` | 10 | 40,415 | 计算方法和分步反应章节完整 |

主要问题不是解析失败，而是 GROBID 对部分版面中的连字和特殊字体保留不理想，例如
`Nheterocyclic`、`rst`。这些噪声没有影响后续软件识别和 DOI 路由。

## 6. Stage 03：软件与工具箱覆盖

### 目标

识别作者实际使用的核心计算软件，并要求全部核心软件得到工具箱直接支持。可视化、晶体学
界面和后处理工具按辅助软件处理，不应阻断量子化学任务。

### 结果

| 论文 | 核心软件 | 辅助软件 | 决策 |
|---|---|---|---|
| Aldol-Tishchenko | Gaussian 16、CREST | ShelXT、Olex2 | `direct_covered` |
| ARCHE Case1 | Gaussian 09 | 无 | `direct_covered` |
| NHC cycloaddition | Gaussian 09 | 无 | `direct_covered` |
| Spartan aldol | Spartan 14 | 无 | `unsupported` |
| Two chiral catalysts | Gaussian 09 | CYLView | `direct_covered` |

结果与人工检查一致。Spartan 论文在化学主题上最接近 Case1，但工具箱没有 Spartan 后端，
因此在进入资源审查和资产下载前被淘汰。这说明 Stage 03 的门控关注点是“能否执行”，而不是
“研究方向是否相似”。

### 本次修复

首轮运行发现两类误判：

1. `Gaussian09`/`Gaussian16` 紧凑写法未被别名表覆盖。
2. ShelXT、ShelXL、Olex2、CYLView、GoodVibes 被误当成阻断性的核心计算后端。

修复后 4 篇应通过的论文全部通过，Spartan 负例仍正确拒绝。

## 7. Stage 04：资源上限审查

### 目标

只筛除论文明确记载且超过配置上限的计算：500 CPU 核、8 GPU、1000 GB 内存、12 小时
单次运行时间。没有资源信息或表达含糊时放行。

### 正式运行结果

4 篇均为 `no_explicit_resource`：

- CPU 核数：0 条
- GPU 数量：0 条
- 内存：0 条
- 运行时间：0 条
- 平台名称：0 条
- 超限记录：0 条

正式运行中 Two chiral catalysts 的一句 “tetracyclic core” 被旧规则中的裸 `core` 误召回。
`deepseek-v4-flash` 正确返回空结构，消耗 572 prompt tokens、44 completion tokens，共 616 tokens。

### 监督后的修复与复核

已将召回规则改为：

- 明确的 CPU/GPU/内存/节点/平台词可以召回。
- `32 cores`、`number of cores` 等带数量或 CPU 语境的 core 表达可以召回。
- `second step`、`tetracyclic core` 等化学语义不再召回。
- 时间必须是 `数字 + seconds/minutes/hours/days`，不能只靠单独时间单词。

对正式运行的 4 份 TEI 重新执行召回后，4 篇均为 0 条上下文。因此当前代码对这组语料不会
调用模型，理论 token 消耗为 0，最终决策仍是 4 篇全部放行。

### 评价

Stage 04 的判断是合理的，但筛选能力有限。这几篇论文详细报告了泛函、基组、溶剂模型、
频率计算和构象搜索，却没有报告 CPU、GPU、内存或 wall time。规则不能从“计算很多过渡态”
推断真实资源成本，也不应该这样估算。因此本阶段只能作为显式超限声明过滤器，不能替代后续
实际试运行或任务级资源估计。

## 8. Stage 05：资产发现、下载、溯源、展开和解析

### 8.1 本次新增能力

出版社页面对自动请求返回 403，首轮测试无法获取 ACS/RSC 附件。当前实现增加 Europe PMC
官方接口：

1. 按 DOI 查询 PMCID 和 `hasSuppl`。
2. 调用 `supplementaryFiles?includeInlineImage=false` 下载官方补充 ZIP。
3. 排除正文内嵌图片，只保留真正补充文件。
4. 修复 `Content-Disposition: filename = ...` 的文件名解析，确保 ZIP 后缀不丢失。
5. 安全解压、哈希去重、记录父子关系并解析 ZIP 内 PDF。

### 8.2 长 PDF 边界

真实补充材料达到 43、173、28 和 654 页。全部使用 MinerU 公式/表格解析会导致数小时运行。
新增 `mineru.max_pages`：本次阈值为 40 页。

- 不超过 40 页：MinerU 深度解析。
- 超过 40 页：保留原 PDF，使用 `pdftotext -layout` 生成 TXT/Markdown，并记录降级原因。

这不是丢弃文件，而是将昂贵版面解析变成有边界的增量策略。

### 8.3 各论文资产结果

#### ARCHE Case1

- 正文：开放博士论文 Chapter 1，MinerU 成功，16,872 字符。
- 自动下载的外部资产：0。
- 状态：`no_external_assets`。

该状态不能解释成“原论文没有补充材料”。ACS 官方页面明确列出
`ja5b12097_si_001.pdf`，约 579 KB，内容包括完整模型过渡态、能量、其他泛函结果、所有
驻点 Cartesian coordinates 和热力学参数。当前服务器访问 ACS 页面和旧附件 URL均为 403，
Europe PMC 又未收录该非开放论文全文，所以本次自动管线没有取得该 SI。

这是 Stage 05 当前最重要的剩余缺口：`no_external_assets` 实际表示“没有成功发现/下载”，
不等价于“论文不存在外部资产”。

#### Aldol-Tishchenko

- 正文：MinerU 成功，42,173 字符。
- 官方补充 ZIP：`PMC8279497_SupplementaryFiles_noInlineImages.zip`。
- SI：`jo0c02862_si_001.pdf`，43 页，使用长 PDF 回退，78,081 字符。
- 未解决线索：两个 CCDC 数据 DOI。
- 状态：`partial`。

SI 包含 Gaussian 16、CREST、Spartan、GaussView 等方法说明，以及构象、能量、频率和结构
信息。两个 CCDC DOI属于晶体结构实验数据，当前 DataCite 能发现标识符，但 CCDC 没有由
现有通用解析器暴露可直接下载的内容地址，所以保留为 unresolved。

#### NHC cycloaddition

- 正文：MinerU 成功，62,543 字符。
- 官方补充 ZIP：`PMC11538972_SupplementaryFiles_noInlineImages.zip`。
- SI：`RA-014-D4RA03676J-s001.pdf`，173 页，长 PDF 回退，220,397 字符。
- 状态：`complete`。

SI 明确包含各驻点的单点能、NIMAG 和 Cartesian coordinates。对精确重建计算任务而言，
这些信息明显比正文更接近可执行输入。

#### Two chiral catalysts

- 正文：MinerU 成功，54,772 字符。
- 官方补充 ZIP：`PMC6289169_SupplementaryFiles_noInlineImages.zip`。
- SI 1：`SC-009-C8SC03078B-s001.pdf`，28 页，MinerU 成功，88,957 字符。
- SI 2：`SC-009-C8SC03078B-s002.pdf`，654 页，长 PDF 回退，1,957,162 字符。
- 状态：`complete`。

28 页 SI 主要是自由能曲线、构象采样、过渡态比较和分析表；654 页文件是大规模优化结构
坐标集合。这篇论文最直接说明：正文足以理解科学问题，但不足以完整恢复作者枚举的大量结构。

### 8.4 Stage 05 总体评价

优点：

- 对三篇 Europe PMC 开放论文，补充材料发现和下载准确。
- 下载来源、哈希、父子关系、原始文件、结构化 JSON 和可读文本均被保存。
- ZIP 内没有混入正文插图，所有 11 项资产解析状态均为 success。
- 超长 SI 有明确、可配置的解析边界，不会无限占用 MinerU。

限制：

- ACS Cloudflare/权限策略仍可阻断公开 SI，Case1 即为实例。
- DataCite 能发现 CCDC DOI，但当前没有 CCDC 专用下载集成。
- `all` 模式会保留与论文有关但不一定是任务必需的实验数据线索，需要 Builder 再判断用途。
- `complete` 只表示当前已发现线索全部处理完，不证明互联网上不存在未发现资产。

## 9. 对 Case1 风格任务构建的结论

这组论文都适合构建“给定反应物/催化剂/计算方法，探索反应路径、过渡态或立体选择性”的
智能体任务，但输入来源应分层处理：

1. 正文通常足以确定研究问题、反应对象、核心软件、泛函/基组和主要结论。
2. 精确初始结构、全部构象、过渡态坐标、频率和绝对能量通常位于 SI，不应假设正文具备。
3. 若任务要求智能体从分子定义自行搜索过渡态，正文加少量结构描述可能足够。
4. 若任务要求复算论文中的特定驻点或数值，SI 坐标和热力学数据基本是必要输入。
5. 与 Case1 研究方向相似不代表工具箱可执行；Spartan 论文就是应由 Stage 03 淘汰的例子。

因此，优先收集反应机理和立体选择性论文是可行的，但 Stage 05 仍然重要。正确策略不是要求
“完全不需要外部数据”，而是优先选择“外部数据主要限于出版社 SI，并且 SI 中是有限数量的
结构、坐标和能量表”的论文，避开依赖大型专有数据库或复杂工作流状态的研究。

## 10. 修改和验证

本次修改包括：

- Stage 03：补充 Gaussian 紧凑版本别名，修正辅助软件角色。
- Stage 04：修正序数 second 和化学结构 core 的资源误召回。
- Stage 05：新增 Europe PMC 补充材料发现、正确文件名解析、排除内嵌图片。
- Stage 05：增加 `mineru.max_pages` 和超长 PDF 的可审计 `pdftotext` 回退。
- README：补充 Europe PMC 和长 PDF 策略说明。

验证结果：

```text
43 passed, 6 subtests passed
```

正式运行的全部原始日志、每阶段 JSONL、模型输入/响应、下载资产和解析文本均保存在
`run_full_v4/outputs` 中。
