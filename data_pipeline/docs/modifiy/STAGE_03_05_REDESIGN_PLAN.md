# 数据管线第三、四、五阶段重新设计方案

## 1. 文档目的

本文档定义 ResearchChemBench 数据管线第三、四、五阶段的新目标、判定规则、输入输出契约、外部服务依赖、配置方式、错误处理和代码迁移方案。

本次调整的核心原则是：每个阶段只回答一个明确问题，不再同时承担论文相关性、任务类型预测、工具可用性、数据可用性、Seed 覆盖和资源评估等多个职责。

重新设计后的三个阶段依次回答：

```text
Stage 03：论文实际使用的全部核心软件是否被工具箱直接覆盖？
Stage 04：论文是否包含可独立构建任务的完整计算化学过程？
Stage 05：论文明确记载的计算资源是否超过本地硬上限？
```

整体数据流：

```text
Stage 02 GROBID TEI
        |
        v
Stage 03 软件覆盖门控
  | direct_covered
  +---------------------> Stage 04
  | capability_equivalent
  +---------------------> 备选集合，暂不进入后续阶段
  | unsupported
  +---------------------> 淘汰
        |
        v
Stage 04 完整计算过程门控
  | complete
  +---------------------> Stage 05
  | incomplete/uncertain
  +---------------------> 淘汰
  | 模型未配置或调用失败
  +---------------------> 跳过并放行至 Stage 05
        |
        v
Stage 05 明确资源上限门控
  | within_limit / no_explicit_resource / ambiguous
  +---------------------> 后续阶段
  | exceeds_limit
  +---------------------> 淘汰
```

## 2. 总体设计原则

### 2.1 使用门控结果，不再使用混合评分

第三至第五阶段不再输出综合相关性分数或人为加权的任务可构建性分数。每个阶段输出有限状态和证据：

```text
pass
reject
candidate
skipped
error
```

### 2.2 所有决定必须可审计

每个通过或淘汰决定必须保存：

- 输入文档标识。
- 判定状态。
- 命中的规则或模型结论。
- 原始证据句或 TEI 段落。
- 规范化后的软件、能力或资源值。
- 服务版本和配置摘要。
- 失败原因。

### 2.3 基础设施失败不能伪装成论文判断

- Softcite 失败：流水线停止。
- GROBID Quantities 失败：流水线停止。
- 第四阶段本地通用模型未配置或调用失败：按需求跳过该阶段并放行，不执行回退判断。

### 2.4 后续阶段只消费明确允许的数据

- Stage 04 只消费 Stage 03 的 `direct_covered` 论文。
- Stage 03 的 `capability_equivalent` 只作为备选记录，不进入当前主数据流。
- Stage 05 只消费 Stage 04 的 `complete` 或 `skipped` 论文。
- Stage 06 及后续阶段只消费 Stage 05 未超限的论文。

## 3. Stage 03：核心软件覆盖门控

### 3.1 阶段目标

判断论文作者实际使用的全部核心计算软件是否都能由当前 ResearchChemBench 化学工具箱直接运行。

该阶段不再负责：

- 判断论文是否属于计算化学。
- 计算论文相关性分数。
- 预测 benchmark 任务类型。
- 检查数据、代码或补充材料是否可获得。
- 判断运行资源是否超限。

### 3.2 输入

每篇论文需要至少包含：

```text
document_id
paper_id
source_path
grobid_tei_path
title
abstract
section_headings
text_path
```

核心输入为 Stage 02 保存的 GROBID TEI XML。

### 3.3 Softcite 集成

使用官方项目：

- <https://github.com/softcite/software-mentions>

Softcite 提供 TEI 直接处理接口：

```text
POST /service/annotateSoftwareTEI
```

请求参数为 GROBID TEI 文件，输出为软件提及 JSON。优先使用以下字段：

```text
software-name.rawForm
software-name.normalizedForm
version
context
mentionContextAttributes.used
documentContextAttributes.used
created
shared
```

只保留作者实际使用的软件。判定顺序建议为：

1. `documentContextAttributes.used.value == true`。
2. 若文档级属性缺失，再使用 `mentionContextAttributes.used.value == true`。
3. 若属性缺失，不得仅因出现软件名称就认定为实际使用。

参考文献、背景介绍、软件比较或未来工作中的软件提及不进入核心软件集合。

### 3.4 核心软件与辅助软件

#### 核心软件

凡是直接产生论文核心科学结果的软件均视为核心软件，包括但不限于：

- 量子化学和电子结构计算引擎。
- 周期性材料计算引擎。
- 分子动力学引擎。
- 增强采样和自由能计算引擎。
- 反应路径、过渡态和微观动力学核心程序。
- 对论文核心结论不可替代的波函数、电子密度或轨迹分析程序。
- 机器学习势训练或推理引擎。
- 对核心任务不可替代的工作流执行系统。

例如 Gaussian、ORCA、VASP、CP2K、GROMACS、AMBER、LAMMPS、PLUMED 等，在其实际生成核心结果时应视为核心软件。

#### 辅助软件

以下软件在证据明确时可以忽略：

- 绘图和排版工具。
- 通用文本编辑器。
- 单纯格式转换工具。
- 可视化工具。
- 不影响科学结果的简单脚本或通用数据整理工具。

#### 保守原则

若某软件可能直接影响论文的数值结果，但无法明确判断是核心还是辅助，应按核心软件处理。只有明确属于展示、格式转换或非科学结果处理的软件才能归为辅助软件。

### 3.5 软件规范化

建立版本化的软件别名配置，例如：

```json
{
  "Gaussian 16": "gaussian",
  "Gaussian16": "gaussian",
  "G16": "gaussian",
  "Quantum ESPRESSO": "quantum_espresso",
  "PWscf": "quantum_espresso",
  "AMBER": "amber_pmemd",
  "GROMACS 2024": "gromacs"
}
```

建议新增：

```text
assets/software_aliases.json
assets/software_role_rules.json
assets/software_capability_map.json
```

软件规范化不得仅依赖大小写和标点删除，还需要显式别名表。所有自动规范化结果必须保留原始软件名。

### 3.6 工具箱直接覆盖

工具箱直接覆盖需要同时满足：

1. 软件规范名存在于工具箱 backend 或可用软件清单。
2. 软件没有被标记为 `unavailable`。
3. 工具箱对该软件至少有可运行或已验证的接口状态。

不能因为软件名称出现在文档、历史报告或 Action 名称中就认为已经直接覆盖。

当前 `assets/toolbox.json` 是面向数据管线的能力快照。实现时需要确保它能提供或关联以下结构：

```text
backend identifier
availability status
supported actions
functional validation level
aliases
```

如果当前快照不足，应从 ResearchChemBench 的规范工具箱目录生成新的结构化映射，而不是在 Stage 03 中硬编码全部 backend 能力。

### 3.7 能力等价映射

能力等价不是“都属于 DFT”这种宽泛匹配，而是实际使用目的与工具箱 Action 的映射。

映射结构建议如下：

```json
{
  "unsupported_software": "example_code",
  "usage_patterns": [
    "single-point energy",
    "geometry optimization"
  ],
  "required_actions": [
    "calculate_energy",
    "optimize_geometry"
  ],
  "equivalent_backends": [
    "orca",
    "psi4"
  ],
  "limitations": [
    "Only valid when no software-specific method is required"
  ]
}
```

判定能力等价需要：

1. 从 Softcite 上下文和 TEI 计算方法段落确认软件的实际用途。
2. 将用途映射为一个或多个工具箱 Action。
3. 确认这些 Action 有可用 backend。
4. 确认论文没有依赖原软件独有、不可替代的模型、功能或文件格式。

初始能力映射应采用小规模、人工审核的规则集。无法高置信映射时不能进入能力等价类。

### 3.8 三类判定

设论文核心软件集合为 `C`。

#### 第一类：`direct_covered`

满足：

```text
C 非空
且 C 中每一个核心软件都被工具箱直接支持
```

处理：进入 Stage 04。

#### 第二类：`capability_equivalent`

满足：

```text
C 非空
至少一个核心软件没有直接支持
所有未直接支持的核心软件都有可信能力等价映射
不存在完全无法覆盖的核心软件
```

处理：保存为备选，当前不进入 Stage 04。

混合情况“部分软件直接支持、部分软件能力等价”属于第二类。

#### 第三类：`unsupported`

满足任一条件：

- Softcite 正常完成，但没有识别到实际使用的软件。
- 只识别到辅助软件，没有核心软件。
- 至少一个核心软件既无直接支持，也无可信能力等价映射。
- 软件用途无法确认且按保守原则必须视为核心软件。

处理：淘汰。

### 3.9 Softcite 错误策略

以下情况必须使流水线失败并停止：

- Softcite 未安装或未配置。
- 服务无法启动。
- 健康检查失败。
- 请求超时且重试耗尽。
- 返回 400、500 或持续 503。
- 返回无法解析的 JSON。
- 返回结构不符合预期。

Softcite 服务失败不能转换为 `unsupported`，因为这属于基础设施错误，不是论文不合格。

### 3.10 Stage 03 输出

目录建议：

```text
stage_03_software_coverage/
  software_coverage_records.jsonl
  direct_covered_documents.jsonl
  capability_equivalent_candidates.jsonl
  unsupported_documents.jsonl
  selected_pdf_paths.jsonl
  softcite_raw/
    <document_id>.json
  summary.json
  softcite_service.log
```

单篇记录建议：

```json
{
  "paper_id": "doc_xxx",
  "decision": "direct_covered",
  "core_software": [
    {
      "raw_name": "Gaussian 16",
      "normalized_name": "gaussian",
      "version": "16",
      "role": "core",
      "used_score": 0.99,
      "evidence": "All calculations were performed using Gaussian 16.",
      "direct_support": {
        "supported": true,
        "backend": "gaussian",
        "validation_level": "functional"
      },
      "capability_equivalence": null
    }
  ],
  "auxiliary_software": [],
  "unsupported_core_software": [],
  "service_version": "pinned-version"
}
```

## 4. Stage 04：完整计算过程门控

### 4.1 阶段目标

判断论文是否包含一段能够独立构建为 benchmark 任务的完整计算化学过程。

该阶段不负责：

- 判断软件是否受工具箱支持。
- 判断资源是否超限。
- 预测四种 benchmark 任务类型。
- 下载数据或验证仓库。
- 使用规则分数替代模型判断。

### 4.2 输入范围

只处理 Stage 03 的 `direct_covered` 论文。

输入信息来自：

- GROBID 标题和摘要。
- TEI 正文段落及章节结构。
- 计算方法相关章节。
- Softcite 实际软件使用证据。
- 结果章节中的定量计算结果。
- 结论章节及结果与结论的关系。

### 4.3 紧凑证据文本构建

不直接把整篇论文提交给模型。先通过确定性规则从 TEI 中构建短文本。

建议结构：

```text
[TITLE]
...

[ABSTRACT]
...

[COMPUTATIONAL OBJECT OR INPUT]
...

[METHODS]
...

[SOFTWARE EVIDENCE]
...

[COMPUTATIONAL RESULTS]
...

[CONCLUSIONS]
...
```

章节召回关键词可包含：

```text
computational methods
computational details
theoretical methods
simulation methodology
DFT calculations
molecular dynamics
free energy calculations
results and discussion
conclusion
```

应保留 TEI 段落来源、章节标题和段落编号，以便模型证据可以回溯。

### 4.4 完整计算过程定义

模型需要判断是否形成以下完整链条：

```text
明确的计算对象、体系或输入
        +
明确的方法和核心软件
        +
实际执行的计算步骤
        +
计算产生的输出或定量结果
        +
结果支持的科学结论
```

不要求论文已经提供所有可复现输入文件，但必须存在能够独立抽象为任务的计算过程。

以下情况应判为不完整：

- 只在引言或背景中提到计算方法。
- 只引用其他论文的计算结果。
- 计算只是实验论文中的一句辅助说明，没有方法和结果链条。
- 只有软件名称，没有计算对象、过程或结果。
- 只有结果图或结论，没有足够信息确认结果来自本文计算。
- 只介绍平台、数据库或软件，没有执行具体科学计算。

### 4.5 本地模型接口

只保留一个 OpenAI-compatible Chat Completions 接口：

```text
POST <base_url>/chat/completions
```

配置建议：

```json
{
  "computation_completeness": {
    "enabled": true,
    "base_url": "http://127.0.0.1:8000/v1",
    "model_name": "local-general-model",
    "api_key_env": "COMPLETENESS_MODEL_API_KEY",
    "timeout_seconds": 300,
    "max_input_chars": 60000,
    "temperature": 0,
    "max_tokens": 2000
  }
}
```

数据管线不负责部署、启动或停止本地通用模型。

### 4.6 模型输出契约

模型必须返回 JSON：

```json
{
  "verdict": "complete",
  "has_computational_object": true,
  "has_method_and_software": true,
  "has_execution_process": true,
  "has_computational_results": true,
  "has_result_supported_conclusion": true,
  "evidence": [
    {
      "section": "Computational Methods",
      "statement": "..."
    }
  ],
  "reason": "The paper contains a complete calculation-to-conclusion chain."
}
```

`verdict` 只允许：

```text
complete
incomplete
uncertain
```

### 4.7 判定规则

| 模型状态 | 流水线状态 | 后续处理 |
|---|---|---|
| `complete` | `pass` | 进入 Stage 05 |
| `incomplete` | `reject` | 淘汰 |
| `uncertain` | `reject` | 淘汰 |
| 模型未配置或 `enabled=false` | `skipped` | 放行至 Stage 05 |
| API 超时、连接失败、服务错误 | `skipped_error` | 放行至 Stage 05 |
| 响应不是合法 JSON 或字段缺失 | `skipped_error` | 放行至 Stage 05 |

模型明确返回 `uncertain` 与 API 失败不同。前者是模型成功判断但证据不足，因此淘汰；后者属于该阶段无法执行，因此按照需求跳过并放行。

### 4.8 禁止回退

模型未配置或调用失败时：

- 不调用其他模型。
- 不使用旧第三阶段关键词评分。
- 不使用规则猜测完整性。
- 不因为 Softcite 识别到软件就自动判为完整。

### 4.9 审计与隐私

保存：

- 提交给模型的紧凑文本。
- Prompt 版本。
- 模型原始响应。
- 解析后的结构化结论。
- 请求时间、响应时间、模型名和错误。

不得保存 API Key。日志中也不得输出认证头。

### 4.10 Stage 04 输出

```text
stage_04_computation_completeness/
  completeness_records.jsonl
  passed_documents.jsonl
  rejected_documents.jsonl
  skipped_documents.jsonl
  selected_pdf_paths.jsonl
  model_inputs/
    <document_id>.txt
  model_responses/
    <document_id>.json
  summary.json
```

## 5. Stage 05：明确资源上限门控

### 5.1 阶段目标

筛除论文中明确记载的、超过本地配置上限的计算任务。

该阶段只比较论文明确给出的资源值，不负责估算真实计算成本。

### 5.2 输入范围

处理：

- Stage 04 `pass` 论文。
- Stage 04 因模型未配置或调用失败而产生的 `skipped`、`skipped_error` 论文。

不处理 Stage 04 的 `reject` 论文。

### 5.3 默认资源上限

```json
{
  "cpu_cores": 500,
  "gpu_count": 8,
  "walltime_hours": 12,
  "memory_gb": 1000
}
```

严格比较规则：

```text
提取值 > 上限  -> 超限
提取值 = 上限  -> 不超限
提取值 < 上限  -> 不超限
```

节点数可以记录，但当前不设置节点数上限，也不单独用于淘汰。

### 5.4 资源候选段落召回

首先从 GROBID TEI 段落中召回含资源关键词的句子或短段落。

#### CPU 关键词

```text
CPU
core
cores
processor
processors
thread
threads
MPI rank
```

#### GPU 关键词

```text
GPU
GPUs
graphics processing unit
CUDA device
accelerator
```

#### 时间关键词

```text
wall time
walltime
runtime
run time
elapsed time
CPU time
GPU time
took
completed in
ran for
hours
days
```

#### 内存关键词

```text
memory
RAM
GB
GiB
TB
TiB
MB
```

#### 平台上下文词

```text
node
nodes
cluster
supercomputer
HPC
SLURM
PBS
```

单独出现平台名称或集群名称不构成超限证据。

### 5.5 GROBID Quantities 集成

使用官方项目：

- <https://github.com/lfoppiano/grobid-quantities>
- <https://grobid-quantities.readthedocs.io/en/latest/restAPI/>

对召回的句子或短段落调用：

```text
POST /service/processQuantityText
```

不应把整篇论文作为一段发送。GROBID Quantities 面向段落级文本，输出数值、区间、单位及标准化结果。

主要使用：

```text
type
quantity / quantityLeast / quantityMost / quantities
rawValue
rawUnit
parsedValue.numeric
normalizedQuantity
normalizedUnit
offsetStart
offsetEnd
```

### 5.6 关键词和严格格式解析补充

GROBID Quantities 是通用物理量解析器，`core`、`GPU`、`node` 等 HPC 资源单位不一定都能稳定识别。因此必须增加局部、严格的关键词格式解析器作为补充。

示例模式：

```text
512 CPU cores
512 cores
64 processors
8 GPUs
GPU x 4
4 x A100 GPUs
1000 GB RAM
1.5 TB memory
12 hours walltime
ran for 24 h
completed in 720 minutes
```

补充解析器要求：

- 只处理资源召回段落。
- 数值必须与资源关键词处于同一句或受控窗口内。
- 不执行基于方法或体系规模的推断。
- 保存匹配表达式和字符偏移。
- 标记证据来源为 `grobid_quantities`、`keyword_parser` 或 `both`。

### 5.7 数值归一化

#### CPU

统一为：

```text
cpu_cores
```

`processor`、`CPU core` 和明确的计算核心数均按核数处理。线程数可以记录，但除非文本明确表示线程就是实际并行资源，否则不转换为 CPU 核数。

#### GPU

统一为：

```text
gpu_count
```

GPU 型号不影响数量比较。

#### 时间

统一为：

```text
walltime_hours
```

支持秒、分钟、小时和天的确定性换算。

必须排除分子动力学物理模拟时长，例如：

```text
100 ns trajectory
10 ps simulation
2 fs timestep
```

这些不是程序 walltime，不能与 12 小时上限比较。

#### 内存

统一为：

```text
memory_gb
```

支持 MB、GB、GiB、TB、TiB。实现中需要固定十进制或二进制换算规则，并在输出中记录原始单位和规范化单位。

### 5.8 区间和限定词

规则如下：

| 表达 | 比较方式 |
|---|---|
| `512 cores` | 使用 512 |
| `up to 1024 cores` | 使用 1024 |
| `512-1024 cores` | 使用上界 1024 |
| `at least 1024 cores` | 使用下界 1024 |
| `more than 500 cores` | 若下界明确大于 500，则超限 |
| `about 512 cores` | 使用 512，并标记 approximate |
| `several GPUs` | 无明确数值，放行 |
| `hundreds of cores` | 含糊，放行 |

同一段落中 GROBID Quantities 和关键词解析器产生冲突时：

1. 保留两者结果。
2. 优先使用单位与资源关键词绑定更明确的结果。
3. 无法确定时标记 `ambiguous` 并放行。
4. 不得为提高淘汰率而选择性使用更大的值。

### 5.9 不进行的计算

该阶段明确不做：

- CPU 核时计算。
- GPU 时计算。
- 多个独立任务的资源求和。
- 根据节点数猜测每节点核数。
- 根据体系规模估算内存。
- 根据 DFT、CCSD(T)、MD 等方法估算成本。
- 根据模拟物理时长估算 walltime。
- 判断论文资源是总项目消耗还是单次任务消耗。

只要抽取到明确资源数值，就按对应维度直接比较，不做总量或单次任务语义拆分。

### 5.10 实际计算上下文

资源值应来自描述本文实际计算的段落。以下信号可作为正向上下文：

```text
we used
calculations were performed with
simulations were run on
allocated
using N cores
completed in
required N GB
```

以下内容不能单独构成淘汰证据：

```text
平台最多支持多少资源
超算平台名称
其他论文使用的资源
未来计划
通用软件推荐配置
没有数值的资源描述
```

总计算与单次计算不再进一步区分，但仍需避免把明显不属于本文计算的资源值作为淘汰证据。

### 5.11 Stage 05 判定

#### `pass`

满足任一情况：

- 没有召回资源信息。
- 召回内容没有明确数值。
- 数值或单位含糊。
- 只有平台名称。
- 所有明确资源值都不超过上限。

#### `reject`

至少一个明确资源值超过对应上限：

```text
cpu_cores > 500
gpu_count > 8
walltime_hours > 12
memory_gb > 1000
```

### 5.12 GROBID Quantities 错误策略

GROBID Quantities 与关键词解析器是互补关系，关键词解析器不是服务故障回退。

以下情况流水线必须失败并停止：

- GROBID Quantities 未安装或未配置。
- 服务无法启动。
- 健康检查失败。
- 请求失败且重试耗尽。
- 返回无法解析的结构。

服务正常返回但某段没有识别到数量时，可以继续使用关键词解析结果。服务整体失败时不能仅依赖关键词解析器继续运行。

### 5.13 Stage 05 输出

```text
stage_05_resource_limits/
  resource_limit_records.jsonl
  passed_documents.jsonl
  rejected_documents.jsonl
  selected_pdf_paths.jsonl
  recalled_contexts/
    <document_id>.jsonl
  quantities_raw/
    <document_id>.json
  summary.json
  grobid_quantities_service.log
```

单篇记录建议：

```json
{
  "paper_id": "doc_xxx",
  "decision": "reject",
  "limits": {
    "cpu_cores": 500,
    "gpu_count": 8,
    "walltime_hours": 12,
    "memory_gb": 1000
  },
  "resource_mentions": [
    {
      "resource_type": "cpu_cores",
      "raw_value": "1024",
      "raw_unit": "CPU cores",
      "normalized_value": 1024,
      "normalized_unit": "cores",
      "evidence": "The production calculation used 1024 CPU cores.",
      "section": "Computational Methods",
      "source": "both",
      "exceeds_limit": true
    }
  ],
  "blocking_resources": ["cpu_cores"]
}
```

## 6. 服务部署与版本管理

### 6.1 服务隔离

三个 GROBID 相关组件应作为独立服务运行：

```text
Stage 02 GROBID Fulltext       127.0.0.1:8070
Stage 03 Softcite              127.0.0.1:8060
Stage 05 GROBID Quantities     127.0.0.1:8062
```

Softcite 和 GROBID Quantities 默认都可能使用 8060，因此必须显式配置不同端口。

### 6.2 第三方源码目录

建议：

```text
third_party/grobid/
third_party/software-mentions/
third_party/grobid-quantities/
```

第三方源码目录继续通过 `.gitignore` 排除，仓库只保存：

- 固定版本或 commit。
- bootstrap 脚本。
- 配置模板。
- 客户端代码。
- 服务健康检查和测试。

### 6.3 版本固定

不得长期使用浮动的 `master`。实施阶段需要：

1. 检查 Softcite 与当前 TEI 输出的兼容性。
2. 检查 GROBID Quantities 与当前 Java 环境的兼容性。
3. 选择通过真实论文测试的 tag 或 commit。
4. 在 bootstrap 脚本和 README 中固定版本。

Softcite 和 GROBID Quantities 不应未经验证直接合并到当前 GROBID 0.9.0 源码树。它们可以作为独立、版本自洽的服务读取 Stage 02 产物。

### 6.4 生命周期

建议沿用 Stage 02 的服务上下文管理：

```text
检查服务是否存活
如果不存在则自动启动
等待健康检查
执行当前阶段
如果服务由流水线启动，则阶段结束后自动停止
如果是外部服务，则复用且不停止
```

## 7. 配置设计

建议在 `config.json` 中新增：

```json
{
  "software_coverage": {
    "softcite": {
      "base_url": "http://127.0.0.1:8060",
      "working_directory": "third_party/software-mentions",
      "start_command": ["./gradlew", "--no-daemon", "run"],
      "auto_start": true,
      "startup_timeout_seconds": 600,
      "timeout_seconds": 300,
      "retries": 2
    },
    "aliases_file": "assets/software_aliases.json",
    "role_rules_file": "assets/software_role_rules.json",
    "capability_map_file": "assets/software_capability_map.json"
  },
  "computation_completeness": {
    "enabled": true,
    "base_url": "http://127.0.0.1:8000/v1",
    "model_name": "local-general-model",
    "api_key_env": "COMPLETENESS_MODEL_API_KEY",
    "timeout_seconds": 300,
    "max_input_chars": 60000,
    "temperature": 0,
    "max_tokens": 2000
  },
  "resource_limits": {
    "cpu_cores": 500,
    "gpu_count": 8,
    "walltime_hours": 12,
    "memory_gb": 1000,
    "grobid_quantities": {
      "base_url": "http://127.0.0.1:8062",
      "working_directory": "third_party/grobid-quantities",
      "start_command": ["./gradlew", "--no-daemon", "run"],
      "auto_start": true,
      "startup_timeout_seconds": 600,
      "timeout_seconds": 120,
      "retries": 2
    }
  }
}
```

## 8. 当前数据管线的代码调整方案

### 8.1 移除第三阶段旧职责

当前 `src/discovery/corpus_classify.py` 同时承担：

- 软件关键词识别。
- 方法和领域识别。
- 计算相关性评分。
- 文章类型判断。
- 四种任务可构建性评分。
- MinerU 深度解析决策。

这些职责不再属于新 Stage 03。实施时应停止在主数据流中调用 `classify_corpus_documents()`。

如后续模块仍需要方法或领域标签，应在后续专门阶段重新定义，不能继续依赖旧综合评分对象。

### 8.2 移除第四阶段旧低成本混合门控

当前 `stage_04_low_cost_screen` 同时检查：

- 文本质量。
- 计算化学中心性。
- 任务类型可抽取性。
- 工具箱覆盖。
- 数据、代码和 SI 线索。

新 Stage 04 只保留本地模型的完整计算过程判断。旧 `pre_screen_documents()` 不再用于第三至第五阶段主路径。

工具箱覆盖迁移到 Stage 03；数据和代码可用性应保留在后续资产发现或正式质量门控阶段，而不是在 Stage 04 初筛。

### 8.3 移除第五阶段 Seed 审计

当前 `stage_05_seed_audit` 不再占用 Stage 05。Seed 覆盖不属于论文可执行性硬门控。

如未来仍需要 Seed 分析，可：

- 移到后续独立报告阶段。
- 作为离线分析命令保留。
- 不影响论文是否进入 MinerU 和任务构建。

### 8.4 新增模块建议

```text
src/ingestion/softcite.py
  Softcite 客户端、服务生命周期、原始结果保存

src/screening/software_coverage.py
  软件规范化、核心/辅助分类、直接覆盖和能力等价判定

src/screening/computation_completeness.py
  TEI 紧凑证据构建、本地模型调用、响应验证

src/ingestion/grobid_quantities.py
  GROBID Quantities 客户端和服务生命周期

src/screening/resource_limits.py
  资源段落召回、关键词解析、归一化和硬上限比较
```

如项目不希望新增 `screening` 包，也可以放入 `src/curation/`，但三个阶段不应再次集中到一个大型混合模块中。

### 8.5 编排代码调整

`run_corpus_pipeline()` 中第三至第五阶段应改为：

```python
software_records = run_software_coverage(extracted_records, ...)
direct_records = select_direct_covered(software_records)

completeness_records = assess_computation_completeness(direct_records, ...)
complete_or_skipped = select_complete_or_skipped(completeness_records)

resource_records = assess_resource_limits(complete_or_skipped, ...)
selected_records = select_within_resource_limits(resource_records)
```

后续 Stage 06 MinerU 队列不再依赖旧的：

```text
corpus_classification.deep_parse_decision
pre_extraction_quality.decision
seed_guidance
```

Stage 06 应直接以 Stage 05 通过记录为候选输入。是否所有通过论文都进入 MinerU，可继续由 MinerU 的 `limit`、缓存和执行配置控制，但不能再使用已删除的相关性分数决定。

### 8.6 Stage 索引和目录名称

更新为：

```text
stage_03_software_coverage
stage_04_computation_completeness
stage_05_resource_limits
stage_06_mineru_queue
```

更新：

- `stage_index.json`
- `README.md`
- `DESIGN_PRINCIPLES.md`
- 日志阶段名称
- 运行报告
- 测试夹具
- 历史阶段说明文档

### 8.7 保留后期正式质量门控

新 Stage 03 至 Stage 05 是论文级早期筛选，不替代后期任务包质量检查。

后续仍应保留：

- 输入文件是否真实存在。
- 参考运行是否成功。
- 评分规则是否可执行。
- 工具调用是否在本地真实通过。
- 数据泄漏检查。
- 专家审核。

## 9. 输出状态与后续路由

建议使用统一路由字段：

```json
{
  "pipeline_routing": {
    "stage_03": "direct_covered",
    "stage_04": "complete",
    "stage_05": "pass",
    "continue": true,
    "stopped_at": null,
    "stop_reason": null
  }
}
```

淘汰示例：

```json
{
  "pipeline_routing": {
    "stage_03": "unsupported",
    "stage_04": "not_run",
    "stage_05": "not_run",
    "continue": false,
    "stopped_at": "stage_03_software_coverage",
    "stop_reason": "unsupported_core_software"
  }
}
```

## 10. 测试方案

### 10.1 Stage 03 单元测试

必须覆盖：

- 所有核心软件直接支持，判第一类。
- 一个直接支持、一个能力等价，判第二类。
- 一个直接支持、一个完全不支持，判第三类。
- 只有辅助软件，判第三类。
- Softcite 成功但没有软件，判第三类。
- 背景提及软件但 `used=false`，不计入使用集合。
- 软件别名和版本归一化。
- 模糊核心/辅助角色按核心处理。
- Softcite 服务失败导致阶段异常，而不是论文 reject。

### 10.2 Stage 04 单元测试

使用模拟 API 响应覆盖：

- `complete` 放行。
- `incomplete` 淘汰。
- `uncertain` 淘汰。
- `enabled=false` 跳过放行。
- 连接失败跳过放行。
- 超时跳过放行。
- 非 JSON 响应跳过放行。
- 缺少必要字段跳过放行。
- 输入紧凑文本包含方法、软件、结果和结论来源。

### 10.3 Stage 05 单元测试

必须覆盖：

```text
500 cores        -> pass
501 cores        -> reject
8 GPUs           -> pass
16 GPUs          -> reject
12 hours         -> pass
24 hours         -> reject
1000 GB          -> pass
1.5 TB           -> reject
720 minutes      -> pass
2 days           -> reject
100 ns trajectory -> 不作为 walltime
Summit supercomputer -> pass
several GPUs     -> pass
up to 1024 cores -> reject
512-1024 cores   -> reject
```

还需覆盖：

- GROBID Quantities 单独命中。
- 关键词解析器单独命中。
- 两者一致。
- 两者冲突且无法消解时标记含糊并放行。
- GROBID Quantities 服务失败导致流水线停止。

### 10.4 集成测试

- 使用小型 TEI fixture 运行 Softcite 客户端。
- 使用短资源段落运行 GROBID Quantities。
- 使用模拟本地模型运行 Stage 04。
- 验证三个服务日志和原始响应落盘。
- 验证 Stage 03 第二类不会进入 Stage 04。
- 验证 Stage 04 `skipped_error` 会进入 Stage 05。
- 验证 Stage 05 reject 不会进入 MinerU 队列。

### 10.5 真实论文回归测试

使用当前 17 篇去重正式论文运行：

1. 检查 Softcite 提取的软件及 `used` 证据。
2. 人工复核核心/辅助软件分类。
3. 人工复核三类工具箱覆盖结果。
4. 检查本地模型对完整计算过程的判断。
5. 检查资源召回是否把模拟物理时间误认为程序 walltime。
6. 统计每一阶段保留和淘汰数量。
7. 对所有淘汰论文保存可读证据。

## 11. 验收标准

### Stage 03

- 每个 Softcite 软件提及都保存上下文和 `used` 属性。
- 所有核心软件都必须参与覆盖判断。
- 第一类只包含全部核心软件直接支持的论文。
- 第二类不进入后续阶段。
- Softcite 故障会停止流水线。

### Stage 04

- 只调用一个本地模型 API。
- `complete` 才正常通过。
- `incomplete` 和 `uncertain` 淘汰。
- 未配置或调用失败跳过放行。
- 不存在规则或其他模型回退。

### Stage 05

- 同时使用 GROBID Quantities 和严格关键词解析器。
- 只比较 CPU、GPU、walltime 和内存硬上限。
- 不估算资源，不累计独立任务。
- 没有明确资源信息时放行。
- 明确超限时淘汰。
- GROBID Quantities 故障会停止流水线。

### 整体

- Stage 03 至 Stage 05 不再输出旧相关性和任务可构建性混合评分。
- 每个淘汰决定都有原始证据。
- 后续 MinerU 队列只包含 Stage 05 通过论文。
- 文档、配置、脚本和自动化测试同步更新。

## 12. 实施顺序

建议按以下顺序实施：

1. 固定并部署 Softcite，验证当前 GROBID TEI 输入。
2. 建立软件别名、核心/辅助角色和能力等价映射文件。
3. 实现并验证新 Stage 03。
4. 定义紧凑证据文本和本地模型 JSON 契约。
5. 实现并验证新 Stage 04。
6. 固定并部署 GROBID Quantities。
7. 实现资源召回、关键词解析和归一化。
8. 实现并验证新 Stage 05。
9. 调整 Stage 06 MinerU 队列输入。
10. 删除主路径对旧 Stage 03 至 Stage 05 逻辑的依赖。
11. 更新 README、设计原则和阶段报告。
12. 对 17 篇正式论文完成真实回归测试并人工审查淘汰结果。

## 13. 最终定义

重新设计后的第三至第五阶段不再试图通过一个综合分数预测论文“好不好”，而是形成三个清晰的事实门控：

```text
工具是否直接可用
计算过程是否完整
明确资源是否超限
```

只有全部核心软件直接受支持、论文具有完整计算过程且没有明确资源超限的论文，才进入当前 ResearchChemBench 数据管线的后续主流程。
