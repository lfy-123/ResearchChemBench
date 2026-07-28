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
- **执行契约平面**：模板、预检、资源、结果校验、错误诊断和 provenance。

## 二、提高原生软件调用成功率

### 1. 更详细的使用文档是必要条件，但不能是唯一措施

当前有 56 个软件指南、69 个命令，但多数只说明 executable、synopsis、输入方式、必需文件和简单参数。历史上 Agent 很少主动搜索软件文档，而且 ORCA、Gaussian 等错误即使读过简略说明也很难完全避免。

因此建议采用四件套：

```text
详细文档 + 版本化模板 + 软件特定预检 + 结构化错误诊断
```

文档负责告诉 Agent 正确做法；模板降低从零编写输入的难度；预检阻止确定性错误进入计算；诊断帮助 Agent修复仍然发生的失败。

### 2. 每个软件统一使用 SoftwareGuideV2

每个软件和命令至少包含以下内容：

```yaml
software_id: orca
tested_versions: [6.1.1]
executables: [orca]
working_directory_contract: ...
staging_rules: ...
input_sections: ...
resource_mapping: ...
normal_termination_rules: ...
scientific_convergence_rules: ...
expected_outputs: ...
common_errors: ...
compatibility_requirements: ...
templates: ...
official_document_sections: ...
```

详细内容包括：

- 作业实际 cwd 和 staged target 规则；
- 输入文件中所有相对路径如何解析；
- 常见任务的完整最小输入；
- 并行、内存和作业资源的映射关系；
- 正常结束标志和科学收敛标志；
- 必需输出及其用途；
- 高频错误日志、原因和修改方式；
- 上下游文件兼容条件；
- 与当前安装版本对应的官方文档章节。

### 3. 模板不是静态示例，而是经过真实测试的版本化资产

建议为每个高频软件提供 `template_id`：

| 软件 | 第一批模板 |
|---|---|
| ORCA | 单点、优化、频率、DLPNO 单点、外部坐标文件 |
| Gaussian | 单点、优化、频率、TS、ModRedundant、Link1、GenECP |
| CREST | 普通构象搜索、约束搜索、protonation/deprotonation、QCG |
| VASP | 静态能、离子弛豫、体积点、DOS、LOBSTER 上游计算 |
| LOBSTER | COHP/COBI、DOS、投影基组显式配置 |

模板只能补全输入语法和文件结构，方法、泛函、基组、溶剂、收敛阈值等科学选择仍由 Agent 填写。每个模板必须：

- 绑定软件版本；
- 有独立文件和 SHA-256；
- 有真实最小 smoke；
- 记录最后验证时间；
- 在软件升级后自动重新测试。

### 4. 增加软件特定预检

统一接口：

```text
validate_native_job
  mechanical_validation
  syntax_validation
  compatibility_validation
  resource_reconciliation
  preflight_errors[]
  preflight_warnings[]
```

重点校验：

- ORCA：关键词、block/end、坐标、外部文件、charge/multiplicity、`%pal/%maxcore`。
- Gaussian：Link0、route、空行分段、坐标、GenECP、ModRedundant、Link1、checkpoint。
- CREST：当前版本支持的 flags、runtype、charge/UHF、线程数和输入格式。
- VASP：INCAR/POSCAR/KPOINTS/POTCAR、元素顺序、POTCAR 拼接、约束和输出开关。
- LOBSTER：WAVECAR/POSCAR/POTCAR/vasprun.xml 一致性、NBANDS、ISYM、LWAVE 和投影覆盖。

预检不自动修改输入，也不自动选择科学参数。它只拒绝确定不合法或确定不兼容的请求。

### 5. 将文档和模板嵌入调用流程

建议的原生调用顺序：

```text
search/list software
  -> inspect_software
  -> get_native_recipe(template_id 或 custom_input)
  -> write input
  -> validate_native_job
  -> submit_native_job
  -> assess_native_job
  -> collect outputs
```

`inspect_software` 首屏只返回简洁的调用检查表、模板列表和文档章节，不直接返回大段手册。Agent 选择模板或自定义输入后，再按需读取详细内容。

提交记录必须包含：

- `guide_version`；
- `template_id/template_version` 或 `custom_input`；
- preflight report；
- 输入文件哈希；
- 软件和 runtime 版本。

### 6. 实施顺序

不建议一开始平均投入 56 个软件。应按失败量和使用频率推进：

1. 第一批：ORCA、Gaussian、CREST、VASP、LOBSTER。
2. 第二批：xTB、GoodVibes、Multiwfn、Quantum ESPRESSO、CP2K、NWChem、GAMESS 等常用软件。
3. 第三批：其余低频软件完成统一文档 schema 和最小模板。

最终要求仍是 56/56 软件具备完整指南，但优先解决已被轨迹证明的主要失败源。

### 7. 验收指标

- 112 个历史原生失败形成固定回放集。
- 第一批软件的确定性输入错误执行前拦截率不低于 90%。
- 经过预检的作业，启动后 10 秒内输入失败率低于 5%。
- 第一批模板真实 smoke 成功率为 100%。
- 原生作业必须区分进程结束、软件正常结束和科学收敛。

## 三、提高 Action 搜索准确性

### 1. 几种方案的比较

| 方案 | 优点 | 风险 | 建议 |
|---|---|---|---|
| 当前英文词法 AND | 简单、稳定、可解释 | 中文和同义词为零召回，多词查询容易漏召回 | 必须替换 |
| 纯语义向量搜索 | 能处理自然语言、中文和同义表达 | 可能产生语义误召回，精确 ID 和专业术语不稳定 | 只作为补召回 |
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

即使分类器把 `single point energy` 只判断为 `molecular_electronic`，也没有问题；如果查询涉及“构象自由能与热布居”，全局语义检索仍可以补回 `structure_and_system` 和相关后处理 Action。

### 4. Action 元数据改造

为 ActionSpec 增加：

```text
aliases
zh_aliases
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
zh_aliases: 单点能, 电子能, 分子能量
tags: quantum chemistry, scalar energy, non-periodic
```

优先完成 aliases、中文别名和 tags，再引入向量检索。对于只有 114 个短文档的目录，优质元数据和 BM25 往往比直接增加 embedding 更稳定。

### 5. 搜索结果必须可解释

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

### 6. Action 搜索推荐流程

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

### 7. Action 搜索验收指标

构建中英双语查询集，覆盖同义词、缩写、任务表达和错误拼写。至少包含：

- `single point energy`；
- `conformer energy`；
- `电子能量`；
- `晶体对称性分析`；
- `过渡态频率验证`；
- `Boltzmann conformer population`。

目标：

- 200 条查询的 recall@5 不低于 95%；
- 精确 Action ID/alias top-1 为 100%；
- 中文核心能力 top-5 零召回率为 0；
- 搜索结果始终来自完整、任务无关的冻结目录。

## 四、提高其他搜索的准确性

其他搜索不应直接复制 Action 搜索算法。不同对象应该使用不同策略。

| 搜索对象 | 推荐策略 |
|---|---|
| DOI、CAS、InChIKey、Action ID、Backend ID、Artifact ID | 格式规范化后 exact match，精确结果绝对优先 |
| Backend | capability、支持的 Action、system type、runtime、资源和软件版本过滤 |
| 软件 | software ID、alias、executable、版本精确匹配，描述 BM25 补充 |
| 科学资源 | 元素覆盖、格式、版本、兼容 backend、模型类型等结构化过滤 |
| 软件文档 | 章节级 BM25 + 语义检索，返回章节、页码、版本和原文件 hash |
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

但每类对象使用自己的 index adapter。DOI/CAS 不需要 embedding；文档最适合语义检索；Artifact 最适合图查询。

### 2. 文档检索是语义检索最有价值的场景

软件手册通常很长，Agent 查询的是“ORCA 6.1 如何设置 DLPNO 内存”或“LOBSTER 要求 VASP 使用什么 ISYM”。这类查询比 Action 名称检索更需要章节级语义相似度。

缓存阶段应：

- 提取 PDF 文本；
- 按标题和章节切块；
- 保留页码；
- 建立 BM25 和本地 embedding；
- 返回原文件和 SHA-256；
- 严格按软件版本过滤。

### 3. 检索实施优先级

1. 精确 ID、aliases、中文别名和分类浏览。
2. BM25 与结构化过滤。
3. 文档章节 embedding。
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
    required: true
    schema: result_schema_v1
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
```

SDK 负责：

- 返回 job-local 绝对路径；
- 创建输出父目录；
- 阻止访问未声明的相对输入；
- 写入 JSON 时检查 NaN/Inf；
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

程序退出码 0 只代表 Python 正常退出。成功还需要：

- required outputs 存在；
- JSON/schema 合法；
- 数值无非预期 NaN/Inf；
- 单位和 shape 符合声明；
- Artifact lineage 完整；
- 必要时通过任务定义的科学 validator。

程序结果建议返回：

```text
preflight_status
execution_status
output_status
parse_status
scientific_validation_status
```

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

路径 SDK 和预检解决可靠性问题，但不能解决 ASE 启动外部 executable 的审计问题。runtime 还需要声明：

```text
execution_policy: in_process_only | declared_external
allowed_executables: []
```

- 普通分析 runtime 默认 `in_process_only`，允许 ASE 结构、优化器和注册的进程内 Calculator。
- 外部 ORCA/Gaussian/VASP/LOBSTER 默认走 Action 或原生接口。
- 第三层确需外部程序时，必须声明子调用，并为每次 exec 建立独立 provenance。

### 9. 编程接口验收指标

- 38 个历史失败形成固定回放集。
- 语法错误和声明 module 缺失在执行前拦截率为 100%。
- 路径/staging 类错误执行前拦截或 SDK 修复率不低于 90%。
- 经过预检的程序作业成功率目标不低于 85%。
- 所有成功作业都有输出 manifest、schema 校验和 Artifact lineage。

## 六、综合实施路线

### 第一阶段：先消除确定性失败

- 完成 ORCA、Gaussian、CREST、VASP、LOBSTER 的详细指南、模板和预检。
- 增加 `validate_analysis_program`、固定 job layout 和路径 SDK。
- 修复 runtime 依赖错误被记为 `invalid_request` 的分类问题。
- 为 Action 增加 aliases、中文别名和 `browse_action_domain`。

### 第二阶段：完善发现能力

- Action 使用分类浏览 + BM25 + 语义补召回。
- Backend、软件、资源使用结构化字段检索。
- PDF 文档建立章节级 BM25 和 embedding 索引。
- 建立中英查询回归集和搜索质量指标。

### 第三阶段：统一科学成功与审计

- 三层统一分层结果状态。
- ASE 外部子调用纳入 provenance。
- 程序输出 schema、NaN/Inf、单位和 lineage 验证。
- 原生软件正常结束、科学收敛和结果解析规则统一接入。

## 七、最终建议

三个方向的核心选择如下：

1. **原生软件**：详细文档必须做，但必须和版本化模板、提交前预检、结构化诊断一起实施，否则文档利用率低的问题仍会存在。
2. **Action 搜索**：优先建设分类浏览和高质量 aliases；使用 BM25 做主排序、语义相似度做跨分类补召回。不要只依赖 Agent 的一次分类，也不要只依赖 embedding。
3. **通用编程接口**：通过固定 job layout、路径 SDK、runtime 内预检和声明式输出契约消除主要失败，同时保留 Agent 编写任意科学程序的能力。

这套方案不改变三层架构，只让每一层更容易被发现、更难被错误调用，并让“运行成功”和“科学结果有效”能够被分别审计。
