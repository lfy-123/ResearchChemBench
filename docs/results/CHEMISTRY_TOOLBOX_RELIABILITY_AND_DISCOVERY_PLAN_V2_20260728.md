# 化学工具箱可靠性与检索改进方案 V2

日期：2026-07-28

本方案结合已有代码和轨迹核查结果，重点解决三个问题：原生软件调用成功率、Action 及其他目录的检索准确性、第三层通用编程接口的失败率。现有三层架构保持不变。

## 一、总体设计

三层执行能力继续保留：

1. 预设 Action：稳定、结构化、可组合，优先承载重复出现的原子科研操作。
2. 原生软件接口：承载特殊输入、版本特定功能和 Action 尚未覆盖的原生流程。
3. 通用编程接口：承载论文特定分析、数据转换和自定义算法。

改造重点是在三层之上补充两个公共平面：

- **发现平面**：分类浏览、混合检索、文档检索和可解释排序。
- **执行契约平面**：结构化操作文档、最小机械校验、资源、结果校验、错误诊断和 provenance。

### 复杂度控制原则

方案只增加能够直接解决现有失败、且不会明显扩大架构复杂度的机制。不建设复杂模板服务、完整软件语法解析器、独立向量数据库、新的外部软件代理或多 embedding 模型系统。

### 工具箱统一使用英文

`chemistry_toolbox` 中由项目维护的运行时代码、配置、Action 与 Backend 元数据、软件目录、MCP 描述、错误消息、脚本输出、测试和操作文档统一使用英文。现有中文内容应转换为英文，新代码不得再增加中文运行时文本。

实施时使用 `rg '[一-龥]' chemistry_toolbox` 审计第一方受版本控制的文本文件，并增加自动检查阻止中文重新进入工具箱。第三方环境、软件缓存和外部原始手册不进行改写，也不进入工具箱自建检索索引。位于项目级 `docs/results` 下的中文分析报告不属于工具箱运行时接口，可以继续使用中文。

## 二、提高原生软件调用成功率

### 1. 采用轻量的 Markdown 文档驱动方案

当前代码已经提供 `inspect_software` 和 `search_software_documentation`，具备按需读取软件调用信息的基础，无需为 56 个软件建设完整的专属语法解析器和预检框架。

推荐方案调整为：

```text
结构化 Markdown 操作手册
  + 按功能和章节检索
  + 独立且经过测试的最小输入示例
  + 通用机械校验
  + 失败后按需读取故障章节
```

文档负责输入语法、任务流程、收敛判断和故障修复；现有 `validate_native_job` 只保留路径、命令、staging 和资源等低成本硬约束。只有轨迹证明文档仍无法消除某类高频错误时，才为个别软件增加针对性检查。

### 2. 文档按共享规则、软件和功能三级组织

建议目录如下：

```text
native_software_docs/
├── _shared/
│   ├── EXECUTION_CONTRACT.md
│   ├── STAGING_AND_PATHS.md
│   ├── RESOURCE_GUIDE.md
│   └── SUCCESS_AND_CONVERGENCE.md
├── orca/
│   ├── INDEX.md
│   ├── QUICKSTART.md
│   ├── SINGLE_POINT.md
│   ├── OPTIMIZATION_AND_FREQUENCY.md
│   ├── EXCITED_STATES.md
│   └── TROUBLESHOOTING.md
├── gaussian/
│   ├── INDEX.md
│   ├── QUICKSTART.md
│   ├── OPTIMIZATION_AND_FREQUENCY.md
│   ├── LINK1.md
│   └── TROUBLESHOOTING.md
└── lobster/
    ├── INDEX.md
    ├── VASP_REQUIREMENTS.md
    ├── PROJECTION_SETUP.md
    └── TROUBLESHOOTING.md
```

共享文档只维护一次，用于解释所有原生作业共同遵守的 cwd、staging、资源和成功状态。每个软件的 `INDEX.md` 是短导航页，只返回任务意图、对应文档和主要输出，不包含完整手册。

### 3. 功能文档采用统一格式

每个功能文档包含：

1. 适用软件版本和 executable。
2. 使用场景和输入前提。
3. 完整且真实测试过的最小输入文件引用。
4. staged target、stdin 和工作目录规则。
5. CPU、内存和并行参数映射。
6. 预期输出文件。
7. 软件正常结束标志。
8. 科学收敛标志。
9. 高频错误、原因和修复方法。
10. 提交前自检清单。

测试输入保存在独立文件中，例如：

```text
chemistry_toolbox/examples/native/orca/single_point/input.inp
chemistry_toolbox/examples/native/gaussian/optimization/input.gjf
chemistry_toolbox/examples/native/crest/conformer_search/input.xyz
```

独立文件是唯一真实来源，并由 smoke test 直接执行。Markdown 只记录示例路径、适用版本、输入说明、预期输出和最后测试状态，避免文档代码块与真实测试输入逐渐不一致。不另外建设模板渲染服务；方法、泛函、基组、溶剂和收敛阈值等科学选择仍由 Agent 根据任务决定。

每个文档使用统一 front matter，支持精确过滤和索引：

```yaml
---
software_id: orca
versions: ["6.1.1"]
topics: [optimization, frequency, thermochemistry]
aliases: [geometry optimization, frequency calculation, opt, freq]
inputs: [orca_input, xyz]
outputs: [orca_output, hessian]
example_path: examples/native/orca/optimization_frequency/input.inp
last_smoke_tested: 2026-07-28
---
```

### 4. 按需读取以减少上下文消耗

原生调用顺序简化为：

```text
确定软件
  -> inspect_software 返回软件索引和可用主题
  -> 读取 INDEX.md
  -> 按任务读取一个功能文档或其中一个章节
  -> 读取一个已测试示例文件并生成任务输入
  -> validate_native_job 执行通用机械校验
  -> submit_native_job
  -> 按收敛章节判断结果
  -> 失败时只检索 TROUBLESHOOTING 对应章节
```

正常调用通常只读取几百 token 的索引和一个功能章节，不把完整官方手册放入上下文。推荐为文档读取接口增加 `software_id + topic + section` 精确入口；只有无法确定章节时才执行 BM25 和语义检索。

### 5. 保留最小机械校验，不建设全面专属预检

以下检查属于安全和执行契约，必须保留：

- executable 是否在白名单；
- staged source 是否存在；
- target path 是否安全；
- stdin 文件是否已经 staged；
- arguments、工作目录和输入模式是否一致；
- CPU、内存和时间是否超过预算。

不建设完整 ORCA、Gaussian、VASP 或 LOBSTER 语法解析器。路径和资源错误继续由通用校验器处理；同时只增加少量高频、确定性的 lint 规则，例如 Gaussian 缺少必要空行、ORCA block 未闭合、CREST 参数与模式明显冲突或 LOBSTER 上游文件缺失。

### 6. 具体修改

- 建立 `_shared` 文档和统一 front matter。
- 为 ORCA、Gaussian、CREST、VASP、LOBSTER 建立索引、常用功能文档和故障文档，并按使用频率覆盖其余软件。
- 将 `inspect_software` 改为返回主题索引，不默认返回长文本。
- 增加独立 smoke 示例文件和少量高频确定性 lint。
- 将文档切分到标题和子标题级，建立精确 topic、BM25 和向量索引。

### 7. 验收指标

- 高频软件所有常用任务都能通过 `software_id + topic` 精确找到一个操作章节。
- 独立最小输入示例真实 smoke 成功率为 100%，并记录软件版本与文件 hash。
- 正常一次调用只读取索引和一个任务章节，记录实际检索 token 数。
- 112 个历史失败形成回放集，统计文档方案实施后的即时失败率变化。
- 路径、staging、白名单和资源越界仍在执行前 100% 拦截。
- 原生作业继续区分进程结束、软件正常结束和科学收敛。

## 三、提高 Action 搜索准确性

### 1. 几种方案的比较

| 方案 | 优点 | 风险 | 建议 |
|---|---|---|---|
| 当前英文词法 AND | 简单、稳定、可解释 | 同义词容易零召回，多词查询容易漏召回 | 必须替换 |
| 纯语义向量搜索 | 能处理自然语言和同义表达 | 可能产生语义误召回，精确 ID 和专业术语不稳定 | 只作为补召回 |
| 先分类，再返回该类全部 Action | 高召回、容易浏览、当前每类最多 23 个 Action | 一旦分类错会漏掉跨类 Action；完整 schema 全返回会占用大量上下文 | 适合作为主要浏览入口 |
| 分类浏览 + 词法/语义混合搜索 | 同时保证可浏览性、精确匹配和跨类补召回 | 实现稍复杂 | 推荐方案 |

### 2. 推荐方案：分类浏览为主，混合检索补召回

当前 114 个 Action 分为 9 类，每类规模如下：

| 分类 | Action 数 |
|---|---:|
| `scientific_data_interchange` | 3 |
| `structure_and_system` | 19 |
| `cheminformatics` | 6 |
| `molecular_electronic` | 22 |
| `molecular_dynamics` | 23 |
| `reaction_and_kinetics` | 14 |
| `periodic_and_phonons` | 16 |
| `docking` | 1 |
| `data_sources` | 10 |

每类最多 23 个，因此向 Agent 返回某类全部 Action 的**紧凑摘要**是可行的。摘要包含：

```text
action_id
一句话能力描述
输入语义
主要输出
可用 backend ids
关键标签
```

不应一次返回该类所有 Action 的完整 provider contract、参数说明和资源 schema。Agent 选出候选后，再调用 `inspect_action` 获取完整信息。

### 3. 不让一次分类成为不可恢复的决定

不建议强制 Agent 先选且只能选一个分类。推荐两种并行入口：

```text
browse_action_domain(category)
search_actions_v2(query)
```

`search_actions_v2` 内部执行：

1. Action ID/alias 精确匹配；
2. 判断 top 2-3 可能分类；
3. 将这些分类内全部 Action 加入候选集；
4. 从全目录执行 BM25 和语义相似度补召回；
5. 使用 reciprocal rank fusion 或加权分数合并；
6. 按分类展示结果，并解释命中原因。

即使分类器把 `single point energy` 只判断为 `molecular_electronic`，也没有问题；如果查询涉及 `conformer free energy and thermal populations`，全局语义检索仍可以补回 `structure_and_system` 和相关后处理 Action。

### 4. Action 元数据改造

为 ActionSpec 增加：

```text
aliases
keywords
capability_tags
scientific_entities
task_verbs
input_semantic_types
output_semantic_types
```

例如：

```text
calculate_energy
aliases: single point energy, electronic energy, molecular energy
tags: quantum chemistry, scalar energy, non-periodic
```

优先完成英文 aliases 和 tags，再引入向量检索。对于只有 114 个短文档的目录，优质元数据和 BM25 往往比直接增加 embedding 更稳定。

### 5. 小型 embedding 模型和运行方式

语义相似度检索需要把查询和目录文本编码为向量，因此需要 embedding 模型。该模型只负责候选召回，不负责选择科学方法，也不替代精确匹配、分类浏览和 BM25。

首选本地英文模型：

```text
sentence-transformers/all-MiniLM-L6-v2
参数量：约 22.7M
向量维度：384
默认最大长度：256 word pieces
运行位置：本地 CPU
```

选择该模型的原因：

- 模型较小，适合英文短查询和低延迟 CPU 推理；
- 当前 Action 索引文本平均约 39 个英文词，最大约 61 个词；现有软件指南平均约 56 个词，适合该模型的短句和短段落检索范围；
- 工具箱目录、aliases、操作文档和检索查询统一使用英文，不需要多语言模型；
- 114 个 Action 和有限数量的文档章节不需要大型向量数据库或大型 embedding 服务。

模型信息以官方模型卡为准：`https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2`。使用官方 ONNX 导出在 CPU 上执行，避免为检索功能引入完整 PyTorch 服务。模型固定为一个，不增加多模型路由和 fallback。

#### 5.1 离线生成目录向量

Action 向量不应在每次查询时重新生成。索引构建时，将下列字段拼接后一次性编码：

```text
action_id
category
description
aliases
keywords
capability_tags
input_semantic_types
output_semantic_types
```

软件文档按照 Markdown 标题和子标题切分，每个章节单独编码。章节控制在 200 word pieces 左右，超过该长度时再拆分，以避免超过模型的 256 word-piece 上限。只有源文件 hash 或 embedding 模型版本发生变化时才重新生成对应向量。

索引 manifest 至少记录：

```text
model_id
model_revision
embedding_dimension
normalization
source_file_hash
chunk_id
index_built_at
```

#### 5.2 查询时只编码一次

每次搜索只对用户查询生成一个向量，再与已经缓存的目录向量计算余弦相似度。当前数据规模很小，可以直接使用 NumPy 矩阵点积，不必引入独立向量数据库或 FAISS 服务。

模型在 MCP 服务启动时加载一次并保持驻留。模型文件缓存在本地，正式评估期间使用离线模式，避免网络下载和外部 API 波动。

#### 5.3 向量结果只做补召回

推荐排序顺序：

1. 精确 ID 和 alias 命中始终最高优先级。
2. 分类候选和结构化 capability 命中进入主候选集。
3. BM25 负责专业关键词和缩写匹配。
4. embedding 补充英文同义改写和跨分类结果。
5. 使用 reciprocal rank fusion 合并 BM25 和向量结果，避免不同分数尺度难以校准。

向量相似度较低或各结果分数接近时，不应强行返回一个 Action；应返回 top 分类及其紧凑 Action 列表，让 Agent 继续选择。

#### 5.4 性能和质量验收

- 模型预热后，短查询在当前 CPU 上的 embedding 加检索 p95 目标低于 300 ms。
- Action 目录常驻内存，向量矩阵检索本身目标低于 10 ms。
- 更新一个 Action 或一个 Markdown 章节时只增量重建对应向量。
- 使用覆盖英文同义词、缩写、任务表达和相似 Action 的固定查询集评估语义补召回。
- 同时报告 `BM25` 与混合检索的质量指标，确认语义补召回没有造成不可接受的误召回。

### 6. 搜索结果必须可解释

每个结果返回：

```text
score
matched_fields
exact_matches
expanded_terms
predicted_categories
ranking_reason
```

这样 Agent 可以判断结果是因为精确 alias、分类命中、backend capability，还是仅仅语义相似。

### 7. Action 搜索推荐流程

```text
Agent 有明确分类
  -> browse_action_domain
  -> 查看该类所有紧凑 Action
  -> inspect_action

Agent 只有自然语言需求
  -> search_actions_v2
  -> 查看 top 分类和跨分类候选
  -> 必要时 browse_action_domain
  -> inspect_action
```

### 8. Action 搜索验收指标

构建英文查询集，覆盖同义词、缩写、任务表达、错误拼写和容易混淆的相似 Action。至少包含：

- `single point energy`；
- `conformer energy`；
- `electronic energy`；
- `crystal symmetry analysis`；
- `transition-state frequency validation`；
- `Boltzmann conformer population`。

目标：

- recall@5 不低于 95%；
- 报告 precision@5、top-1 accuracy 和 MRR@5；
- 精确 Action ID/alias top-1 为 100%；
- 单独统计相似 Action 对的误召回率；
- 搜索结果始终来自完整、任务无关的冻结目录。

## 四、提高其他搜索的准确性

其他搜索不应直接复制 Action 搜索算法。不同对象应该使用不同策略。

| 搜索对象 | 推荐策略 |
|---|---|
| DOI、CAS、InChIKey、Action ID、Backend ID、Artifact ID | 格式规范化后 exact match，精确结果绝对优先 |
| Backend | capability、支持的 Action、system type、runtime、资源和软件版本过滤 |
| 软件 | software ID、alias、executable、版本精确匹配，描述 BM25 补充 |
| 科学资源 | 元素覆盖、格式、版本、兼容 backend、模型类型等结构化过滤 |
| 软件文档 | 优先按 `software_id + topic + section` 精确读取；未知章节时使用 BM25 + 小型 embedding 补召回 |
| Artifact | semantic type、producer、parent/child lineage 和依赖图查询 |
| Python runtime | module、版本、backend、executable 和 capability 过滤 |

### 1. 统一接口，不统一算法

建立公共结果格式：

```text
object_type
object_id
score
exact_match
matched_fields
source_version
```

但每类对象使用自己的 index adapter。DOI/CAS 不需要 embedding；结构化 Markdown 文档适合 topic 精确读取和章节级语义补召回；Artifact 最适合图查询。

### 2. 软件文档先精确路由，再使用语义检索

自行维护的原生软件操作文档已经按软件、任务和章节组织，因此大部分查询不需要向量检索。例如几何优化可以直接读取 `orca/OPTIMIZATION_AND_FREQUENCY.md`，只在 Agent 不知道主题名称或提出开放式故障问题时使用语义召回。

文档索引顺序为：

1. `software_id` 和版本硬过滤。
2. topic、section、aliases 精确匹配。
3. 标题和正文 BM25。
4. `sentence-transformers/all-MiniLM-L6-v2` 章节向量补召回。
5. 本地结构化文档没有答案时，才检索缓存的官方 HTML/PDF 手册。

缓存官方文档时应提取文本、按标题切块、保留页码和源文件 SHA-256。最终只返回命中的少量章节，而不是返回整份手册。

### 3. 检索实施优先级

1. 精确 ID、英文 aliases 和分类浏览。
2. BM25 与结构化过滤。
3. 使用同一个小型本地模型建立文档章节 embedding。
4. Action embedding 作为补召回。
5. Artifact lineage 图查询。

## 五、降低第三层通用编程接口失败率

### 1. 当前主要失败不是 Python 本身，而是执行契约不清晰

101 个程序作业中只有 54 个成功。典型失败集中在：

- Agent 以为 cwd 是任务 workspace；
- 输入文件没有 staging；
- 脚本写入不存在的 `outputs/` 或 `report/`；
- runtime 没有所需 module；
- API 或版本不匹配；
- Python 语法和数据解析错误；
- 输出没有统一格式和校验。

因此核心方向不是限制 Agent 编程，而是让脚本运行环境和输入输出契约显式化。

### 2. 引入 AnalysisJobContract

建议请求结构：

```yaml
runtime: workflows
script_path: code/analyze.py
required_modules:
  - numpy
  - pymatgen
inputs:
  - name: structure
    source_path: data/input.vasp
    semantic_type: AtomicStructure
outputs:
  - name: result
    path: outputs/result.json
    semantic_type: AnalysisResult
    media_type: application/json
    required: true
    schema: result_schema_v1
  - name: density
    path: outputs/density.cube
    semantic_type: ElectronDensityGrid
    media_type: chemical/x-gaussian-cube
    required: false
resource_limits:
  cpu_cores: 2
  memory_mb: 4096
```

作业目录固定为：

```text
job_root/
  code/agent_program.py
  inputs/
  outputs/
  report/
  logs/
  manifest.json
```

这些目录在执行前由框架创建。

### 3. 提供路径 SDK，避免 Agent 手写 cwd 逻辑

```python
from researchchem_job import JobContext

ctx = JobContext.load()
structure = ctx.input("structure")
result_path = ctx.output("result")
ctx.write_json("result", payload)
ctx.register_output("density", "outputs/density.cube")
```

SDK 负责：

- 返回 job-local 绝对路径；
- 创建输出父目录；
- 阻止访问未声明的相对输入；
- 写入结构化数值结果时检查 NaN/Inf；
- 把输出登记到 manifest；
- 记录输入输出 lineage。

同时提供环境变量 `RESEARCHCHEM_JOB_ROOT/INPUTS/OUTPUTS/REPORT`，供不使用 SDK 的脚本使用。

### 4. 提交前强制预检

新增 `validate_analysis_program`，并让提交工具自动调用：

1. `py_compile` 检查语法；
2. AST 提取 imports；
3. 在选定 runtime 内验证 module 和版本；
4. 检查所有声明输入存在且成功 staging；
5. 检查输出路径合法、无冲突；
6. 检查参数和编码声明；
7. 返回可操作的错误字段和修复建议。

预检应能在实际运行前发现历史中的语法错误、缺 module 和大部分路径错误。

### 5. 提供通用程序模板

至少提供：

- JSON/CSV 数据分析；
- cclib/正则量化输出解析；
- ASE 结构读写和进程内 Calculator；
- pymatgen 周期结构分析；
- NumPy/SciPy 拟合与不确定性；
- Matplotlib 图表生成；
- 批量文件处理；
- 结果 schema 和 report 生成。

模板绑定 runtime 和经过验证的 API 版本，减少 Agent 根据旧 API 编写代码。

### 6. 结果输出必须声明和验证

程序输出不限于 JSON，可以是 JSON、CSV、CIF、XYZ、SDF、cube、轨迹、检查点、文本报告、PNG 或其他科研文件。JSON 只作为统一 `manifest.json` 的格式，不要求所有科学产物转换为 JSON。

manifest 中每个产物至少记录：

```text
name
path
semantic_type
media_type
size_bytes
sha256
producer
parent_artifacts
validation_status
```

程序退出码 0 只代表 Python 正常退出。作业状态统一分为：

1. `request_status`：工具是否接受请求。
2. `process_status`：进程是否正常结束。
3. `software_status`：若存在原生子作业，软件是否正常结束。
4. `convergence_status`：科学计算是否达到声明的收敛条件。
5. `artifact_status`：必需产物是否存在、可解析且通过类型相关校验。
6. `scientific_validation_status`：结果是否满足工具箱能够机械判断的科学约束。

产物校验按类型执行：JSON 可以使用 schema，数值表检查 NaN/Inf、单位和 shape，结构和轨迹检查格式可读性，图像检查文件有效性，所有产物检查 hash 和 lineage。

工具箱不负责判断 Agent 的最终论文解释或科学结论是否正确。最终结论正确性和证据是否充分仍由评估任务的 Judger 判断。

### 7. 失败后的修复流程

失败诊断应结构化返回：

```text
stage: preflight | import | input | execution | output | parse
code
file
line
evidence
likely_cause
candidate_fixes
retryable
```

系统不自动修改 Agent 程序，但 Agent 可以根据诊断重新提交。每次重试保留 parent job id 和 diff hash，形成完整修复轨迹。

### 8. 第三层权限边界

路径 SDK 和预检解决可靠性问题，但不能解决 ASE 启动外部 executable 的审计问题。为避免增加新的代理子系统，第三层直接复用现有原生作业执行器：

```text
execution_policy: in_process_only
external_execution: native_job_runner_only
```

- 普通分析 runtime 默认 `in_process_only`，允许 ASE 结构、优化器和注册的进程内 Calculator。
- Python/ASE 不允许直接通过 `subprocess` 启动 ORCA、Gaussian、VASP、LOBSTER 等外部 executable。
- 第三层确需外部程序时，调用已有原生作业提交接口，由其统一控制资源、超时、取消和进程终止。
- 每个原生子作业继续生成独立 tool trace 和 provenance，并与父程序作业关联。

### 9. 编程接口验收指标

- 38 个历史失败形成固定回放集。
- 语法错误和声明 module 缺失在执行前拦截率为 100%。
- 路径/staging 类错误执行前拦截或 SDK 修复率不低于 90%。
- 经过预检的程序作业成功率目标不低于 85%。
- 所有成功作业都有输出 manifest、适用的类型校验和 Artifact lineage。

## 六、综合修改内容

- 将 `chemistry_toolbox` 第一方代码、配置、运行时元数据、消息、脚本输出、测试和操作文档统一为英文，并增加自动语言检查。
- 为原生软件建立共享规则、软件导航页、功能文档、故障文档和独立 smoke 示例文件。
- 保留原生作业白名单、路径、staging 和资源校验，只增加少量高频确定性 lint，不建设完整软件语法解析器。
- Action 使用分类浏览、英文 aliases、BM25 和 `all-MiniLM-L6-v2` 语义补召回。
- embedding 使用 ONNX CPU 推理、离线缓存目录向量和 NumPy 相似度计算，不增加向量数据库或多模型路由。
- Backend、软件和科学资源继续使用精确字段与结构化过滤；软件文档优先精确 topic 路由，语义检索只用于未知章节。
- 通用编程接口增加固定 job layout、路径 SDK、runtime 预检和声明式输入输出契约。
- Python/ASE 的外部软件调用统一复用现有原生作业执行器，不新增代理系统。
- 科研程序允许生成 JSON、CSV、结构、cube、轨迹、图像等产物，并统一写入 artifact manifest。
- 三层统一区分请求接受、进程结束、软件结束、科学收敛、产物有效和机械科学校验；最终科学结论由 Judger 评价。

## 七、最终建议

三个方向的核心选择如下：

1. **原生软件**：采用共享规则、软件导航页、按功能拆分的 Markdown 文档和独立真实测试示例；按需读取章节并保留通用机械校验，只增加少量高频确定性 lint。
2. **Action 搜索**：优先建设分类浏览和高质量英文 aliases；使用 BM25 做主排序，`all-MiniLM-L6-v2` 做跨分类补召回。目录向量离线缓存，查询时只编码一次，不依赖外部 embedding API。
3. **通用编程接口**：通过固定 job layout、路径 SDK、runtime 内预检、声明式输出契约和通用 artifact manifest 消除主要失败，同时保留 Agent 编写任意科学程序的能力。
4. **语言规范**：工具箱第一方实现统一使用英文，中文仅保留在工具箱之外的项目级分析报告中。

这套方案不改变三层架构，只让每一层更容易被发现、更难被错误调用，并让“运行成功”和“科学结果有效”能够被分别审计。
