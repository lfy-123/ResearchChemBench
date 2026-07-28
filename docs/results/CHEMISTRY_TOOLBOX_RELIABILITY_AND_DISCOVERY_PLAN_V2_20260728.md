# 化学工具箱可靠性与检索改进方案 V2

日期：2026-07-28

## 修改总结

本方案中的修改已全部完成，现有三层架构保持不变。主要结果如下：

- 工具箱第一方运行时文本、配置、脚本、测试和活动操作文档已统一为英文，并由自动检查阻止中文重新进入；历史中文材料保存在工具箱之外的归档目录。
- Action 发现新增分类浏览、英文 aliases、BM25 和本地量化 `all-MiniLM-L6-v2` 补召回。20 条固定查询的 lexical/hybrid Hit@1、Recall@5、MRR、nDCG@5 均为 1.00；60 次真实 hybrid 查询 p95 为 256.79 ms。
- 原生软件文档形成共享规则和 ORCA、Gaussian、CREST、VASP、LOBSTER 的 28 份主题化 Markdown，可按 software/topic/section 精确读取，也可执行章节级混合检索。
- 5 个高频原生软件均有独立示例和确定性 lint，真实 smoke 最终全部成功。测试过程实际发现并修复了 CREST 初始几何、LOBSTER 缺少上游文件、无效投影参数和 VASP 对称性设置问题。
- 通用编程接口新增语法/import/input/output 预检、固定 job layout、`JobContext`、声明式产物合同、JSON schema、NaN/Inf 检查和统一 artifact manifest；旧请求保持兼容。
- 三层状态语义已明确区分请求接受、进程结束、软件结束、科学收敛、产物有效和机械科学校验。真实 LOBSTER 退出码 0 但正文报错的轨迹会被判为 mechanically invalid。
- 第三层直接启动外部 executable 会被静态预检拦截并引导到原生作业接口；该检查与 `JobContext` 均明确不是 OS 安全边界。Supervisor 会清理遗留后台进程并记录原因。
- 最终英文检查、变更 Python 编译检查和完整测试套件均通过；完整结果为 308 passed，耗时 380.12 秒。

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
- 对传入 `ctx.input()` 和 `ctx.output()` 的逻辑名称执行声明校验，未知名称返回明确错误；
- 写入结构化数值结果时检查 NaN/Inf；
- 把输出登记到 manifest；
- 记录输入输出 lineage。

同时提供环境变量 `RESEARCHCHEM_JOB_ROOT/INPUTS/OUTPUTS/REPORT`，供不使用 SDK 的脚本使用。

`JobContext` 是路径辅助和执行契约 API，不是文件系统权限边界。普通 Python 程序仍然可以绕过 SDK，使用 `open()`、`pathlib`、绝对路径或第三方库访问进程权限允许读取的文件。SDK 不能拦截或阻止这些操作，也不能保证程序只读取已声明输入。

如果需要强制文件访问隔离，必须由作业运行器、容器、mount namespace 或操作系统权限实现。SDK 只能提高正确性和 provenance 完整性，不能替代系统级沙箱。

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
- 执行契约规定 Python/ASE 不应直接通过 `subprocess` 启动 ORCA、Gaussian、VASP、LOBSTER 等外部 executable；`JobContext` 本身无法强制执行该规定。
- 第三层确需外部程序时，调用已有原生作业提交接口，由其统一控制资源、超时、取消和进程终止。
- 每个原生子作业继续生成独立 tool trace 和 provenance，并与父程序作业关联。

若要强制禁止程序直接启动外部 executable，需要在作业运行器或操作系统隔离层限制可见 executable 和子进程权限；仅依赖 SDK、提示词或静态检查只能提供约束提示和审计，不能形成安全边界。

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

## 八、实施记录

实施开始日期：2026-07-28

本节在每项修改完成后记录实际改动、验证命令和结果。文档开头的修改总结将在全部任务完成后补充。

### 任务 1：基线审计与实施范围确认

状态：已完成。

基线结果：

- 当前目录包含 114 个 Action、9 个 Action domain、56 个原生软件指南和 69 个原生命令。
- `search_actions` 使用英文分词、简单词干和全部查询词 AND 匹配，结果按稳定 Action ID 排序，没有相关性分数。
- 原生接口具备 executable、路径、staging、stdin 和资源校验，但软件专属输入检查主要只有 pysisyphus。
- `submit_analysis_program` 检查 runtime、脚本路径、扩展名和资源，但没有 Python 语法预编译、import 可用性检查、声明式输出和通用产物 manifest。
- 第一方受版本控制文件中有 34 个文件包含中文，集中在软件清单、生成脚本和历史工具箱文档。
- 基线测试命令：`chemistry_toolbox/.venv/bin/pytest -q chemistry_toolbox/tests/test_progressive_discovery.py chemistry_toolbox/tests/test_open_execution_layers.py chemistry_toolbox/tests/test_progressive_program_runtime_discovery.py`。
- 基线测试结果：18 passed，耗时 4.13 秒。

### 任务 2：工具箱第一方文本统一为英文

状态：已完成。

修改内容：

- 将 `requested_software.yaml`、`requested_software_status.json`、相关清单测试以及软件审计、缓存、环境检查和能力矩阵脚本中的第一方中文界面文本改为英文。
- 将 23 份日期特定的中文工具箱历史文档移至 `docs/archive/chemistry_toolbox_legacy_cn/`，原路径保留英文归档说明，避免旧链接失效。
- 将 4 个仅生成历史中文报告的脚本源文件归档到上述目录，在原命令路径提供英文兼容入口；当前目录和参数合同继续由实时 Catalog 与测试套件校验。
- 新增 `scripts/check_english_only.py`，扫描活动工具箱中的代码、配置、测试、脚本和 Markdown，并排除第三方虚拟环境、缓存及不可修改的环境锁文件。
- 新增 `tests/test_english_only.py`，同时验证当前工具箱无 CJK 文本以及检查器能够报告文件和行号。

验证结果：

- `chemistry_toolbox/.venv/bin/python chemistry_toolbox/scripts/check_english_only.py`：通过，输出 `English-only check passed.`。
- `chemistry_toolbox/.venv/bin/pytest -q chemistry_toolbox/tests/test_english_only.py chemistry_toolbox/tests/test_requested_software_inventory.py`：9 passed，耗时 1.00 秒。

### 任务 3：Action 分类浏览与混合检索

状态：已完成。

修改内容：

- 新增 `browse_action_category` MCP 工具，可从 `list_action_domains` 返回的精确分类进入，并一次返回该类全部紧凑 Action 摘要。
- 新增 60 余组人工维护的英文 Action aliases，并为所有 Action 自动加入可读化 Action ID alias；结果中显式返回 aliases。
- 将 `search_actions` 从全部查询词 AND 过滤改为 OR 召回和 BM25 相关性排序，对精确 Action ID、完整 alias 和短语匹配进行透明加权。
- 新增本地语义检索模块，固定使用 `sentence-transformers/all-MiniLM-L6-v2` 的提交 `1110a243...` 和 8-bit AVX2 ONNX 模型；模型仅由显式缓存脚本下载，运行时不联网。
- 新增 `cache_minilm_model.py`，校验模型文件 SHA-256，并离线生成 114 个 Action 的 384 维向量缓存；查询阶段只编码一次 query，以 NumPy 余弦相似度补召回。
- 模型、ONNX runtime 或向量缓存不可用时，搜索结果显式报告原因并稳定降级到 BM25，不影响目录可用性。
- 新增 20 条版本化英文检索评估集和 `evaluate_action_search.py`，统计 Hit@1、Recall@5、Precision@5、MRR 和 nDCG@5，并加入质量下限测试。

验证结果：

- 已在工具箱 `.venv` 中安装 `onnxruntime 1.28.0` 和 `tokenizers 0.23.1`，成功缓存约 23 MB 的量化模型和 114 个 Action 向量。
- 真实查询 `single point energy`、`conformer energy`、`electron density surface` 和 `molecular energy` 均首位命中预期 Action，语义状态为 `available`。
- 20 条固定查询的 lexical 与 hybrid 结果均为 Hit@1=1.00、Recall@5=1.00、MRR=1.00、nDCG@5=1.00；Precision@5=0.22，原因是每条查询平均只有 1.1 个标注相关 Action，而固定返回前 5 项。
- `pytest -q test_action_search_evaluation.py test_search_index.py test_progressive_discovery.py`：12 passed，耗时 0.85 秒。

### 任务 4：原生软件文档组织与按需检索

状态：已完成。

修改内容：

- 新建 `chemistry_toolbox/native_software_docs/`，包含 4 份共享执行契约文档，以及 ORCA 6 份、Gaussian 5 份、CREST 4 份、VASP 5 份、LOBSTER 4 份主题文档。
- 所有文档使用统一英文 YAML front matter，记录 `software_id`、版本、topics、aliases 和示例路径；内容覆盖 cwd、staging、CPU/内存映射、正常结束、科学收敛、必要产物和高频故障修复。
- `inspect_software` 现在返回紧凑 `documentation_index` 和共享主题列表，不默认注入长文档正文。
- 新增 `read_software_documentation` MCP 工具，按 `software_id + topic + optional section` 精确读取有限正文；找不到精确主题时明确报错。
- 重写 `search_software_documentation`：Markdown 按标题切块，先应用 software/topic/section 精确过滤，再执行 BM25 和同一 MiniLM 模型的章节语义补召回；缓存官方 text/HTML 只作为后备，PDF/压缩包仍显式列为不可解析。
- `cache_minilm_model.py` 同时离线建立 5 个高频软件的章节向量索引；每个软件独立校验源文档 digest，文档变化后旧缓存会被标记为 stale。

验证结果：

- `inspect_software` 对 ORCA、Gaussian、CREST、VASP、LOBSTER 均返回预期索引，分别覆盖 6、5、4、5、4 个第一方文档路径（Gaussian 计入共享检索时显示 5 个索引项）。
- 精确读取 `gaussian + quickstart + required sections` 返回必需空行规则；`orca + single point` 返回对应独立文档。
- 真实 hybrid 查询能够将 ORCA memory、Gaussian blank-line EOF、CREST mutually-exclusive mode、VASP POTCAR order、LOBSTER charge spilling 的正确章节排在前两位，语义状态均为 `available`。
- `pytest -q test_native_software_documentation.py test_english_only.py`：6 passed，耗时 1.10 秒。

### 任务 5：原生软件示例与确定性 lint

状态：已完成。

修改内容：

- 新增独立最小示例：ORCA 单点和优化/频率、Gaussian 优化/频率和 Link1、CREST 构象搜索、VASP 基态输入集、LOBSTER COHP 输入；VASP POTCAR 继续从已注册许可资源显式选择，不进入 Git。
- `validate_native_job` 新增 5 个小型确定性 lint profile：ORCA 检查关键词行、block/坐标闭合和 CPU 映射；Gaussian 检查 route、必需空行、title、charge/multiplicity、Link1、CPU/内存映射；CREST 检查 XYZ、互斥模式和线程；VASP 检查固定文件、POSCAR 计数和 POTCAR dataset 数；LOBSTER 检查上游文件和非空输入。
- lint 错误使用稳定英文代码前缀，例如 `orca_unclosed_block`、`gaussian_route_separator`、`crest_conflicting_modes`、`vasp_missing_fixed_files` 和 `lobster_empty_fixed_files`，便于 Agent 定位故障章节。
- 根据真实 smoke 修正 CREST 初始几何；根据 LOBSTER 5.1.0 现场错误，将必需文件合同扩展为 `lobsterin/POSCAR/POTCAR/WAVECAR/CONTCAR/KPOINTS/OUTCAR/vasprun.xml`，并修正 `cohpGenerator` 与 VASP `ISYM=-1` 设置。
- 新增 `examples/native/smoke_manifest.json`，记录版本、输入 SHA-256、作业 ID、进程状态、软件终止、收敛证据、产物状态、耗时和失败修复历史。

真实 smoke 结果：

| 软件 | 版本 | 最终结果 | 关键科学证据 | 耗时 |
|---|---:|---|---|---:|
| ORCA | 6.1.1 | 成功 | `SCF CONVERGED`、`ORCA TERMINATED NORMALLY` | 0.709 s |
| Gaussian | 16 C.01 | 成功 | normal termination、优化/频率完成、`NImag=0` | 15.439 s |
| CREST | 3.0.2 | 成功 | normal termination、生成 3 个唯一构象 | 15.140 s |
| VASP | 6.3.2 | 成功 | 电子迭代达到 `EDIFF`、WAVECAR/vasprun.xml 等产物存在 | 1.914 s |
| LOBSTER | 5.1.0 | 成功 | projection 完成、COHP/COOP/COBI 产物存在、charge spilling 3.71% | 0.609 s |

发现并修复的关键问题：首次 LOBSTER 调用退出码为 0，但正文明确报告缺少上游文件；补齐文件后又发现无效 `type all` 参数导致 abort。该轨迹已保留为“进程成功不等于软件成功”的状态判定回归依据。

验证结果：`pytest -q test_native_input_lint.py test_native_software_documentation.py test_open_execution_layers.py`：21 passed，耗时 3.65 秒。

### 任务 6：通用编程接口执行契约

状态：已完成。

修改内容：

- `AnalysisJobRequest` 新增 `required_modules`、命名 `inputs`、声明式 `outputs`、JSON schema、semantic/media type、required 标志和 parent artifact lineage，同时保留旧 `staged_inputs` 兼容字段。
- 新增 `validate_analysis_program` MCP 工具；执行前检查 UTF-8、Python AST/compile、选定 runtime 中的 import、输入文件、目标路径、参数和资源，并返回包含 stage/code/file/line/evidence/candidate_fixes/retryable 的结构化诊断。
- 程序作业固定创建 `code/`、`inputs/`、`outputs/`、`report/`、`logs/`，默认脚本目标为 `code/agent_program.py`；任务 cwd 仍是作业根目录，并通过合同显式说明。
- 新增 `researchchem_job.JobContext`，允许脚本按声明名读取输入和获取输出路径。SDK 明确只提供可靠性和审计帮助，无法阻止普通 Python 使用 `open()`、绝对路径、subprocess 或其他库。
- 提交时生成 `analysis_contract.json`；收集时生成统一 `artifact_manifest.json`，记录 name/path/semantic type/media type/size/SHA-256/producer/parent/validation status。
- 输出校验支持 JSON parse、JSON schema、NaN/Inf 拒绝、CSV/TSV 非有限值检查、常见图像签名以及通用非空文件检查；非 JSON 的 cube、结构、轨迹和其他二进制产物可正常登记。
- 进程退出 0 但必需输出缺失、JSON 无效、schema 不匹配或含 NaN/Inf 时，`artifact_status` 为 `invalid`，不再把进程状态误当作产物有效。

验证结果：

- 语法错误和不存在的 import 均在创建作业前被拦截，并返回精确错误代码和修复建议。
- 使用 `JobContext` 的真实程序成功读取命名输入，生成 JSON/CSV 两类产物，schema 与 manifest 校验均为 `valid`。
- 另一个真实程序以退出码 0 写出含 `NaN` 的 JSON；收集结果正确保持 process success，同时将 `artifact_status` 标为 `invalid`。
- `pytest -q test_analysis_job_contract.py test_open_execution_layers.py test_progressive_program_runtime_discovery.py`：14 passed，耗时 3.27 秒。

### 任务 7：统一执行状态与外部程序审计边界

状态：已完成。

修改内容：

- `get_execution_job` 和 `collect_execution_job` 统一返回 `request_status`、`process_status`、`software_status`、`convergence_status`、`artifact_status`、`scientific_validation_status`，并附带每一轴的证据与 Judger 边界说明。
- 为 ORCA、Gaussian、CREST、VASP 和 LOBSTER 增加轻量结束/收敛/关键产物判定；未知软件保持 `not_checked`，不使用退出码伪造软件成功。
- LOBSTER 判定会拒绝正文中的 `ERROR:`，即使进程退出码为 0；同时提取 absolute charge spilling 作为可审计证据，但不在 Agent 未声明阈值时替 Agent 判断论文结论。
- 默认编程政策固定为 `in_process_only`，外部 executable 固定要求 `native_job_runner_only`。AST 预检拦截直接 `subprocess`/`os.system` 进程启动和常见 ASE 外部 Calculator 导入，并要求改用原生作业接口。
- 文档和返回值再次明确：静态检查、SDK 和提示不能构成安全边界；动态导入或其他规避只能由 OS/容器/调度器隔离强制限制。
- Native/Analysis 请求支持可选 `parent_job_id`；程序 hash、父作业、模块预检和外部执行发现写入 metadata，形成重试与跨层编排 provenance。
- Supervisor 在主进程结束后检查同一进程组，主动终止遗留后台进程，并记录 `background_process_cleanup`；取消、超时和非零退出继续保留明确原因。
- 作业状态同时返回总预算、当前占用和剩余 CPU/内存/GPU；现有文件锁 reservation 与 queued/running 状态共同执行并发预算。

验证结果：

- 复查真实 smoke 轨迹：ORCA、Gaussian、CREST、VASP、修正后的 LOBSTER 均为 process completed + software normal + convergence/projection complete + artifact valid + mechanically valid。
- 首次 LOBSTER 缺文件轨迹保持 process completed，但新判定正确返回 software failed、convergence failed、artifact invalid、mechanically invalid。
- 直接 `subprocess.run(['orca', ...])` 和 `ase.calculators.vasp.Vasp` 均在程序创建作业前被拦截；提示改用 `submit_native_job` 并关联 parent job。
- 后台 `sleep` 回归用例由 Supervisor 清理，状态记录 `terminated_remaining_process_group`；父作业 ID 正确保存在 metadata。
- `pytest -q test_analysis_job_contract.py test_execution_status_axes.py test_open_execution_layers.py test_resource_budget.py`：19 passed，耗时 13.09 秒。

### 任务 8：完整验证与总结

状态：已完成。

验证与收尾结果：

- 运行 `check_english_only.py`：通过；活动工具箱第一方文本无 CJK 字符。
- 对所有变更 Python 文件运行 `py_compile`：通过。
- Catalog 实时统计为 114 Actions、77 BackendSpecs、56 个原生软件指南；英文 `ACTION_BACKEND_COMPLETE_AUDIT_20260721.md` 已改为从实时 Catalog 自动生成，并由测试检查每个 Action/Backend ID。
- MiniLM 模型固定版本、量化 ONNX、SHA-256 校验、Action 向量和 5 个软件文档向量缓存均已真实构建；模型缓存受 `.gitignore` 管理，评估运行不依赖联网下载。
- 首次完整测试结果为 305 passed、3 failed。1 项失败暴露历史报告归档破坏了实时 Catalog 报告合同，已改成英文实时生成器；另 2 项为 `.venv` 缺少声明的 chemistry 可选依赖，补齐 ASE 和 pymatgen 后对应测试通过。
- 最终完整命令：`chemistry_toolbox/.venv/bin/pytest -q chemistry_toolbox/tests`。
- 最终完整结果：308 passed，耗时 380.12 秒。
- 本次只纳入化学工具箱实现、测试、文档、示例、英文历史归档和本实施文档；工作区中原有的评估输出、task 数据、core 文件和本地配置副本不属于本次修改。
