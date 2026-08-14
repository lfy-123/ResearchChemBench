# Stage02/03 筛选逻辑调整方案

日期：2026-08-14

状态：已确认并于 2026-08-14 完成实现与隔离回归；实施结果见
`STAGE02_03_SCREENING_REDESIGN_IMPLEMENTATION_REPORT_20260814.md`

## 1. 文档目的

本文档定义 Stage02 和 Stage03 的职责边界、模型配置、数据合同、确定性门控和回归方案。方案已在本地 `main` 实施并使用 Git 管理，未上传 GitHub；历史运行结果未被覆盖，回归输出写入独立评估目录。

本轮调整解决三个问题：

1. Stage02/03 的 API 模型在思考模式下容易耗尽输出 token，产生高延迟、截断和 fallback；
2. Stage02 与 Stage03 的职责存在重复，Stage03 不应再次判断计算化学流程是否完整；
3. Stage03 当前按论文全局收集未覆盖软件，导致已覆盖计算工作流被无关实验分析、可视化和辅助软件拖累。

本方案不改变 Stage00、Stage01、Stage04、Stage06 和 Stage07 的职责。Stage05 增加从 Stage03 迁入的资源审计职责。不在代码中加入 DOI、期刊、论文标题或单篇论文特例。

## 2. 修订后的职责边界

| 阶段 | 唯一核心问题 | 应完成 | 不应完成 |
|---|---|---|---|
| Stage02 | 论文是否包含作者实际完成、完整且非平凡的计算化学工作流？ | 判断计算内容、流程完整性、科学输出和实验/计算关系；输出经过验证的工作流 | 不判断工具箱覆盖，不判断输入资产是否齐全，不判断最终 benchmark 是否可构建 |
| Stage03 | 是否存在明确证据证明 Stage02 已确认的所有候选工作流都依赖工具箱未覆盖软件？ | 将冻结工作流步骤绑定到软件；规范化软件名称；查询冻结工具箱目录；只排除明确未覆盖的工作流 | 不要求论文必须报告软件，不把未知当作未覆盖，不重新发现科学工作流，不审查资源成本或科学意义 |

总体数据流为：

```text
Stage01 正文与全部已知 SI 文本
  -> Stage02 计算化学内容审查
       -> confirmed_workflows
  -> Stage03 软件覆盖负向排除门
       -> workflow_coverage_results
  -> Stage04 MinerU 高质量解析
  -> Stage05 Builder 前候选审计与资源审计
```

Stage03 仍需要工作流 ID 和步骤边界，因为软件排除不能按整篇论文全局判断；这些边界必须由 Stage02 冻结，Stage03 只能补充软件依赖，不能修改其科学定义。Stage03 的通过只表示“没有证据证明全部候选工作流明确不受工具箱覆盖”，不等于已经证明软件覆盖。

## 3. 已确认的现状问题

### 3.1 思考模式耗尽输出

第一批完整运行中，Stage03 的 96 篇论文有 68 次主调用在思考阶段耗尽 12,288 个输出 token，尚未返回完整 JSON；关闭思考后的同模型 fallback 可以完成结果。根因主要是未受限思考，而不是结构化结果需要超长输出。

Stage02、Stage03 中支持无思考开关的主模型和 fallback 均应关闭思考；没有专用开关的后级模型必须通过紧凑 JSON 和输出耗尽预检。提示词要求模型按固定检查表工作，但只输出每个检查项的结构化结论、证据 ID 和短理由，不要求展示自由形式思维链。

### 3.2 Stage02 输出不足以冻结多个工作流

当前 Stage02 能判断论文是否存在完整计算工作流，但主要输出一个概括性 workflow。若论文有多个相互独立的计算工作流，Stage03 可能只能围绕其中一个工作，或者被迫从全文重新恢复工作流，造成职责重复。

Stage02 应输出最多三个候选工作流，并经过第二次验证调用确认，最终形成 `confirmed_workflows`。Stage03 只处理这组冻结结果。

### 3.3 Stage03 的全局软件否决

当前 Stage03 虽然已有 `workflow_ids`，最终门控仍从整篇论文收集所有 `core_compute`、`required_preprocessing` 和 `required_analysis` 软件。只要其他位置存在未覆盖软件，就可能把已覆盖工作流改判为 `mixed_workflow_candidate`。

第一批结果中：

- 8 篇 `mixed_workflow_candidate` 都包含已覆盖的核心工作流；
- 58 篇 `core_software_uncovered` 中，至少 17 篇核心计算后端已覆盖，未覆盖项仅来自辅助分析或预处理；
- ImageJ、GraphPad Prism、FlowJo、TopSpin、SHELX、GaussView 等可能因为论文全局角色分类而错误阻断计算工作流；
- VASP、Gaussian、CP2K、Multiwfn 的版本、revision、括号缩写或重复写法可能造成映射失败或同一软件被重复计数。

### 3.4 资源审计迁移到 Stage05

第一批 96 篇 Stage03 输入全部得到 `cost_unconfirmed`，证明低质量文本和论文级软件清单不足以完成可靠成本估算。资源审计从 Stage03 完全移到 Stage05。Stage05 在 Stage04 MinerU 高质量文本、冻结工作流和候选任务范围基础上，统一抽取体系规模、方法、采样规模、job 数、CPU/GPU/内存和 wall time，并执行候选级成本判断。

## 4. API 模型与回退方案

### 4.1 配置原则

Stage02 和 Stage03 都是重要筛选阶段，不再默认依赖较小的本地部署模型。使用用户已经部署的 OpenAI-compatible API 模型，并为每个阶段维护独立、可配置的主备链。

模型名称和参数以 `data_pipeline/如何调用所有模型.md` 及运行时 `/models` 返回为准。业务代码只读取模型角色配置，不能硬编码模型名称。

### 4.2 已确认的默认模型链

Stage02 按以下顺序调用：

```text
DeepSeek-V4-Pro
  -> Nex-N2-Pro
  -> DeepSeek-V4-Flash
  -> Nex-N2-Pro-w8a8
  -> DeepSeek-V4-Flash-DSpark
  -> MiniMax-M2.7
  -> Mimo-V2.5-Pro
  -> Qwen3.6-27B
```

Stage03 按以下顺序调用：

```text
Nex-N2-Pro
  -> DeepSeek-V4-Pro
  -> DeepSeek-V4-Flash
  -> Nex-N2-Pro-w8a8
  -> DeepSeek-V4-Flash-DSpark
  -> MiniMax-M2.7
  -> Mimo-V2.5-Pro
  -> Qwen3.6-27B
```

`GLM-5.2` 和 `Kimi-K2.6` 不进入上述默认活动链，只作为排在 Qwen 之后的可选 emergency reserve；默认关闭，需要通过配置显式启用。

选择理由：

- Stage02 需要较强的论文语义分类和完整流程判断，优先使用 DeepSeek-V4-Pro；
- Stage03 需要稳定的实体、步骤和依赖关系结构化输出，优先使用 Nex-N2-Pro；
- 完整版 `Nex-N2-Pro` 始终排在量化版 `Nex-N2-Pro-w8a8` 之前；量化版仅作为后级 fallback，不能替代 Stage03 主模型；
- DeepSeek Pro、完整版 Nex 和 DeepSeek Flash 构成前三层高质量通道；
- DSpark、MiniMax、Mimo 和 Qwen 提供服务故障隔离；
- 没有专用无思考开关的模型仍保留在用户指定的 fallback 顺序中，但必须通过紧凑 JSON 和输出耗尽预检。

### 4.3 各模型的无思考参数

不同模型不能统一写同一个字段：

| 模型 | `chat_template_kwargs` |
|---|---|
| DeepSeek-V4-Pro / DeepSeek-V4-Flash / DeepSeek-V4-Flash-DSpark | `{"thinking": false}` |
| Nex-N2-Pro | `{"enable_thinking": false}` |
| Nex-N2-Pro-w8a8 | 无专用开关；省略 `chat_template_kwargs`，依赖预检和充足输出预算 |
| MiniMax-M2.7 | 无专用开关；省略 `chat_template_kwargs`，必须通过 JSON 预检 |
| Mimo-V2.5-Pro | 无专用开关；省略 `chat_template_kwargs`，保留内部推理所需输出预算 |
| Qwen3.6-27B | `{"enable_thinking": false}` |
| GLM-5.2 | `{"enable_thinking": false}` |
| Kimi-K2.6 | `{"thinking": false}` |

实现时由模型配置保存参数，Stage02/03 不自行猜测。启动批处理前为每个候选模型执行一次最小 JSON smoke test，确认：

1. 模型存在且有权限；
2. 对支持开关的模型，无思考参数生效；对不支持开关的模型，不在 JSON 前输出推理且不会频繁耗尽输出；
3. 可以返回单个合法 JSON 对象；
4. 不会把长推理文本放在 JSON 前；
5. 请求延迟和超时符合批处理要求。

### 4.4 Fallback 触发边界

只有以下执行失败可以切换 fallback：

- 连接失败、DNS、超时；
- HTTP 429、5xx 或服务端模型不可用；
- 空响应、非 JSON、JSON 合同无法修复；
- `finish_reason=length` 且一次紧凑重试仍失败；
- 模型在返回 JSON 前耗尽输出预算。

以下情况不能触发 fallback：

- 模型正常判定论文不通过；
- 软件明确不在工具箱；
- 正常返回 `uncertain` 或 `software_inventory_unconfirmed`。

否则 fallback 会演变成“不断换模型直到得到通过”，破坏筛选语义。

每次调用必须记录 `model_requested`、`model_returned`、fallback 序号、失败原因、参数、prompt 版本、原始响应哈希、token 用量和耗时。

### 4.5 Token 配置

首次实施只关闭思考，不同时缩小输出预算，以便单独评估影响：

- Stage02 candidate discovery/classification：12,288；
- Stage02 candidate verification：6,144；
- Stage03 software binding：12,288；
- 上下文窗口按模型实测配置，保留至少 2,048 token 安全余量。

回归后根据成功响应的 P95 输出长度再降低上限。提示词必须限制数组数量、字符串长度和 evidence ID 数量，不能依赖大 token 上限容纳重复叙述。

## 5. Stage02 调整方案

### 5.1 职责和通过标签

Stage02 负责计算化学内容、工作流完整性和论文中实验/计算关系。以下四类继续通过：

- `computational_content_confirmed`
- `computational_primary_mixed_confirmed`
- `computational_experimental_co_primary_confirmed`
- `experimental_primary_benchmarkable_computation`

每条通过工作流必须同时满足：

1. 有可识别的化学体系、结构、反应、材料、轨迹或模型；
2. 作者实际执行计算、模拟或电子结构操作；
3. 有明确的计算方法或操作；
4. 产生结构、能量、势垒、光谱、轨迹、速率或其他化学输出；
5. 该输出用于论文的科学结论、比较、预测、解释或设计；
6. 不是拟合、绘图、实验数据处理、仪器转换、简单公式代入或背景引用。

Stage02 不检查软件是否在工具箱中，不检查 SI 资产是否足以精确复现，不判断最终 benchmark ground truth。

### 5.2 输入

Stage02 只接收 Stage01 确认正文和全部已知 SI 都成功解析的论文。输入包括：

- 标题、摘要和文章类型线索；
- 正文与 SI 的计算关键词和方法段落；
- 计算输入、操作、结果和科学用途证据；
- 实验方法与实验贡献证据；
- 所有可引用的 evidence ID。

Stage01 的获取失败、正文失败或任一已知 SI 失败不能被 Stage02 当成“无计算内容”。这类论文保持上游 retryable/hold 状态。

### 5.3 调用 A：候选发现和论文分类

第一次调用按固定检查表判断论文，并输出最多三个彼此独立的 `workflow_candidates`。每个候选至少包含：

```json
{
  "workflow_id": "wf1",
  "chemical_system": "...",
  "scientific_output": "...",
  "scientific_use": "...",
  "steps": [
    {
      "step_id": "s1",
      "action": "geometry optimization",
      "generated_output": "optimized structure",
      "evidence_ids": ["ev1"]
    }
  ],
  "evidence_ids": ["ev1", "ev2"]
}
```

调用 A 同时输出论文角色标签，但不能输出软件覆盖结论。

### 5.4 调用 B：候选工作流验证

第二次调用接收原始证据包和调用 A 的最小候选骨架，但不接收第一次的最终 decision、confidence 或 rationale，以减少结论锚定。它逐候选验证：

- `author_performed_computation`
- `identifiable_chemical_system`
- `actual_chemical_calculation_or_simulation`
- `generated_chemical_output`
- `scientific_use_of_output`
- `nontrivial_workflow`
- evidence ID 是否支持对应步骤和输出。

一次调用验证全部候选，不按候选增加 API 次数。验证通过的候选进入 `confirmed_workflows`；未通过候选保留审计原因，但不传给 Stage03。

### 5.5 确定性裁决

代码执行以下检查：

- 至少一个候选的六个工作流轴全部为 `yes` 才可通过；
- 引用的 evidence ID 必须存在并支持相应字段；
- review、editorial、correction 不能作为原创研究通过；
- 调用 A 与 B 的论文角色不一致时，以工作流证据轴裁决，无法解决则 `uncertain`；
- API、JSON 和 token 失败写为 `processing_failed`/`retryable_failed`，不能转换为 `computational_content_not_found`。

### 5.6 Stage02 输出合同

保留现有字段，并新增：

```json
{
  "decision": "experimental_primary_benchmarkable_computation",
  "passed": true,
  "workflow_candidates": [],
  "confirmed_workflows": [],
  "workflow_verification": [],
  "model_audit": {}
}
```

`confirmed_workflows` 是 Stage03 唯一允许处理的科学工作流集合。每条工作流具有稳定 `workflow_id`、步骤、科学输出和 evidence ID。Stage02 prompt/schema 版本更新后必须进入缓存指纹。

## 6. Stage03 调整方案

### 6.1 职责

Stage03 只完成一项工作：为 Stage02 的 `confirmed_workflows` 尽可能绑定论文明确报告的软件，并只排除明确依赖工具箱未覆盖软件的工作流。论文未报告软件、软件绑定不完整或软件名称无法确认时，保持不确定状态并继续向后传递。

Stage03 不得：

- 新增或删除 Stage02 工作流；
- 改写工作流科学问题、步骤或输出；
- 判断工作流是否完整、非平凡或具有 benchmark 意义；
- 抽取或审计资源成本；
- 要求每条计算工作流必须具有明确软件名称；
- 将“未报告软件”“名称不确定”或“别名无法精确匹配”解释为工具箱未覆盖；
- 因为软件未命名而反向判定“没有计算化学流程”；
- 从论文其他位置构造一条更容易被工具箱覆盖的新流程。

如果 Stage02 的通过记录缺少 `confirmed_workflows`、步骤或 evidence ID，Stage03 返回 `upstream_contract_insufficient`，将其作为管线合同问题保留/重跑 Stage02，而不是科学拒绝论文。若 Stage02 合同完整，只是论文没有写明软件，则不是合同错误，而是正常的 `software_inventory_unconfirmed` Pass。

### 6.2 输入

每篇 Stage03 输入包括：

- Stage02 冻结的 `confirmed_workflows`；
- 每个步骤已引用的证据块；
- 这些证据块相邻的软件上下文；
- 正文与 SI 中规则识别的软件名称窗口；
- explicit executable cues 和可选 Softcite mentions；
- 冻结工具箱 capability snapshot 的路径和哈希，仅供确定性代码使用。

模型不接收“哪些软件在工具箱中”，避免根据希望通过的方向遗漏未覆盖软件。

### 6.3 单次软件绑定调用

Stage03 正常情况下只调用一次模型。模型对每条冻结工作流执行：

1. 检查每个 Stage02 步骤的证据和相邻上下文；
2. 提取论文明确用于该步骤的软件原始名称；
3. 判断软件是核心引擎、必要前后处理、透明 Python 后处理还是非阻断辅助工具；
4. 返回 `workflow_id`、`step_id`、software raw name 和 evidence ID；
5. 将无法绑定到冻结工作流的软件放入 `unscoped_software_mentions`。

模型不输出最终工具箱覆盖判断，也不判断工作流科学完整性。没有找到软件时必须如实返回未命名/未确认，不能猜测软件，也不能据此拒绝论文。

### 6.4 建议输出结构

```json
{
  "workflow_bindings": [
    {
      "workflow_id": "wf1",
      "software_inventory_complete": true,
      "step_bindings": [
        {
          "step_id": "s1",
          "software": "Gaussian 16 Revision C.01",
          "dependency_role": "core_compute",
          "required_for_execution": true,
          "evidence_ids": ["ev3"]
        }
      ]
    }
  ],
  "unscoped_software_mentions": [],
  "unresolved_software_bindings": []
}
```

这里的 `software_inventory_complete` 仅表示软件依赖清单是否完整，不表示计算化学流程完整；计算流程完整性已经由 Stage02 冻结。

### 6.5 通用软件名称规范化

确定性代码进行通用规范化，不为某篇论文或某个 DOI 添加规则：

1. 统一 Unicode、空白、大小写、连字符和标点；
2. 优先进行完整别名精确匹配；
3. 通用识别并剥离 `version`、`revision`、`release`、`build`、平台后缀和纯版本号；官方版本差异不改变软件覆盖；
4. 解析“软件全称（缩写和版本）”形式；
5. 若 raw name 中的多个别名都映射到同一 backend，则合并；
6. 若别名或带版本名称可以唯一映射到一个已覆盖 backend，则判为 covered；若基础软件唯一但修饰形式存在轻微歧义，则判为 probable 并允许通过；
7. 只有名称明确对应另一个不在目录中的独立软件，才能据此判为 uncovered；
8. plugin、extension、fork、patched copy 和 in-house modification 在确实构成独立执行依赖时保持独立实体；普通官方版本和 revision 不视为独立软件；
9. 编辑距离和模糊匹配不能直接判定 uncovered。它只能提供 canonical candidate；候选唯一且基础软件已覆盖时进入 probable，否则进入 inventory unconfirmed。

别名从当前 toolbox capability snapshot 动态同步。已经删除的软件不能出现在 covered capability 中；它们可以保留在 external aliases 中，以便识别明确未覆盖的软件。论文不能仅因别名未登记、大小写、括号缩写或官方版本不同而被直接淘汰。

### 6.6 阻断关系

软件阻断必须来自具体冻结工作流和步骤：

- `required_for_execution=true` 的命名软件不在冻结目录中，只阻断所属工作流；
- 实验仪器、实验图像处理、绘图、文件展示和其他未绑定到该工作流的软件不阻断；
- 可由第三层 task-specific Python 完成的短小透明变换可以不要求原辅助程序；
- Python 不能替代 DFT、MD、docking、kinetics、电子结构等核心科学引擎；
- 若某后处理软件产生 benchmark 的关键科学输出，它必须作为必要步骤检查覆盖；
- 角色名称本身不能决定阻断，最终依据是冻结步骤的执行依赖。

### 6.7 工作流级覆盖

确定性代码对每个 `confirmed_workflow` 生成：

| 状态 | 定义 |
|---|---|
| `workflow_covered` | 所有必要命名软件均存在于冻结工具箱目录；可唯一归一化的别名、官方版本和 revision 视为同一软件 |
| `workflow_coverage_probable` | 核心软件可唯一指向已覆盖 backend，但别名或版本修饰仍有轻微不确定性；该状态允许通过 |
| `workflow_uncovered` | 至少一个必要命名软件被明确识别为工具箱目录中不存在的独立软件；不能仅由别名或版本匹配失败产生 |
| `workflow_software_inventory_unconfirmed` | 必要软件未命名、归属不明或证据不足；该状态通过 Stage03，交给 Stage05 继续审查 |

`workflow_coverage_probable` 不能根据 DFT、MD 等方法名称猜测某个工具箱软件。它要求论文已经给出软件名称，并且该名称可以唯一指向一个已覆盖基础软件，只是别名、版本或 revision 未精确登记。

论文级汇总规则为：

```text
存在 workflow_covered
    -> software_covered

否则存在 workflow_coverage_probable
    -> software_coverage_probable

否则存在 workflow_software_inventory_unconfirmed
    -> software_inventory_unconfirmed

否则所有 confirmed_workflows 都有明确必要未覆盖的独立软件
    -> core_software_uncovered
```

`software_covered`、`software_coverage_probable` 和 `software_inventory_unconfirmed` 全部通过 Stage03。只有 `core_software_uncovered` 淘汰；该标签要求每一条 Stage02 冻结工作流都至少存在一个明确命名、执行所必需且确定不在工具箱目录中的独立软件。

因此：

- 一条工作流软件覆盖，其他工作流未覆盖：论文以 `software_covered` 通过；
- 一条工作流明确未覆盖，另一条工作流没有报告软件：论文以 `software_inventory_unconfirmed` 通过；
- 论文包含计算过程但没有报告任何软件：论文以 `software_inventory_unconfirmed` 通过；
- 所有冻结工作流都明确依赖工具箱不存在的软件：论文以 `core_software_uncovered` 淘汰。

`mixed_workflow_candidate` 降为 `other_workflow_constraints` 审计信息，不再作为论文级淘汰标签。Stage03 记录 `forwarded_for_later_review=true`，确保 Stage05 知道未确认通过并不等于软件覆盖证明。

### 6.8 资源审计迁移

Stage03 不再输出资源筛选结论，也不因资源未知或明确昂贵改变软件覆盖标签。资源审计全部由 Stage05 完成。Stage05 还必须对 Stage03 的 `software_inventory_unconfirmed` 候选使用 MinerU 高质量文本进行一次最终软件确认：

- 输入 Stage02 冻结工作流、Stage03 软件覆盖事实和 Stage04 MinerU 高质量正文/SI；
- 对 Stage03 未确认的软件重新定位方法段和 SI；能确认时更新候选软件事实，仍不能确认时由 Stage05 按 Builder 入口要求决定 review/reject；
- 提取方法级别、体系规模、采样长度、结构/路径数量、job 数和论文明确报告的 CPU/GPU/内存/wall time；
- 针对 Stage05 选定的有界候选任务估算资源，而不是估算整篇论文全部研究；
- 明确超限时拒绝，信息不足时进入 `needs_builder_review`，不能把未知资源视为已确认可控。

### 6.9 输出兼容性

保留现有下游字段：

- `decision`
- `passed`
- `coverage_decision`
- `workflow_inventory`
- `software_mentions`
- `software_mappings`
- `resource_profile`（迁移期仅为 `deferred_to_stage05` 占位）
- `toolbox_catalog_hash`
- `model_review`
- `model_audit`

新增：

- `workflow_coverage_results`
- `unscoped_software_mentions`
- `other_workflow_constraints`
- `upstream_contract_status`
- `forwarded_for_later_review`

兼容字段 `workflow_inventory` 由 Stage02 的冻结工作流和 Stage03 软件绑定组合生成，不再由 Stage03 模型重新定义科学流程。

若旧版 Stage05 仍读取 `resource_profile`，迁移期 Stage03 只写入固定的 `{"decision": "deferred_to_stage05"}` 兼容占位，不能包含筛选结论；Stage05 完成适配后停止依赖该字段。

## 7. 计划修改范围

用户确认后预计修改：

1. `data_pipeline/src/prompts.py`
   - Stage02 候选发现/验证 prompt；Stage03 仅软件绑定 prompt；
2. `data_pipeline/src/stages/stage02_computational_content/`
   - 多候选验证、`confirmed_workflows` 和确定性裁决；
3. `data_pipeline/src/stages/stage03_toolbox_resource_gate/stage.py`
   - 消费冻结工作流、通用软件规范化和工作流级负向排除；将 `software_inventory_unconfirmed` 纳入通过集合；停止资源筛选；
4. `data_pipeline/src/model_client.py` 与配置校验
   - 按模型写入正确无思考参数、预检和 fallback 审计；
5. `data_pipeline/config.example.json`、`config.local.env.example` 和本地配置映射
   - 独立 Stage02/03 主模型与 fallback 链；
6. `data_pipeline/src/stages/stage05_benchmark_suitability/`
   - 接收从 Stage03 迁移的候选级资源审计职责，并解析 Stage03 未确认的软件依赖；
7. Stage02/03/05 相关单元测试和批量回归测试；
8. 本文档追加实施记录、模型实测和改判分析。

不会修改 chemistry toolbox 能力范围，不增加特殊软件白名单，不修改正在运行任务的 frozen config。

## 8. 测试与验收

### 8.1 单元测试

Stage02 覆盖：

- 四类 Pass 均能输出至少一个 `confirmed_workflow`；
- 实验主导但具有完整计算子工作流可通过；
- 多工作流只把验证成功的候选传给 Stage03；
- 拟合、绘图、实验数据处理和公式代入不通过；
- API 失败保持 retryable；
- 主模型和 fallback 都使用正确无思考参数。

Stage03 覆盖：

- 不能新增、删除或改写 Stage02 工作流；
- 官方版本、revision 和括号缩写映射到正确 backend；
- 可唯一映射的别名或版本差异得到 covered/probable 并允许通过；
- 不得仅因别名表缺项、版本号或 revision 不同返回 uncovered；
- 插件、fork 和自定义版本不被错误合并；
- 已覆盖工作流不受其他工作流或实验软件影响；
- 关键后处理未覆盖时只阻断所属工作流；
- 核心软件未命名时返回 `software_inventory_unconfirmed` 且 `passed=true`；
- 一条工作流明确未覆盖、另一条工作流软件未报告时，论文继续通过；
- 只有所有冻结工作流均明确未覆盖时才 terminal reject；
- external alias 可识别未覆盖软件，但不能写入工具箱能力；
- Stage03 不执行资源筛选，仅写迁移兼容状态；
- Stage02 合同不足不能转化为科学拒绝。

### 8.2 Stage02 回归

复用已有 200 篇人工审查集，重新运行 Stage02，比较：

- 四类通过集合的 precision/recall；
- 完整计算工作流召回率；
- 多工作流识别和验证质量；
- `computational_workflow_not_benchmarkable` 与 `computational_content_not_found` 混淆；
- JSON 成功率、fallback 率、P50/P90 延迟和 token 用量。

### 8.3 Stage03 回归

复用第一批 96 篇 Stage02 通过结果，在隔离工作区重跑：

1. 原 22 篇通过论文；
2. 原 8 篇 `mixed_workflow_candidate`；
3. 17 篇“核心后端覆盖、只有辅助软件未覆盖”的高风险拒绝；
4. 所有因版本、revision、括号缩写、别名或重复 mention 改判的论文；
5. 所有新增通过和从通过变为拒绝的论文。

由于 Stage02 新增冻结工作流合同，完整回归还需要用新版 Stage02 对 200 篇和第一批论文生成 `confirmed_workflows`，不能长期依赖从旧 Stage03 结果反推工作流。

### 8.4 建议验收指标

- Stage02 通过集合 precision 不低于 90%；
- Stage02 完整计算工作流 recall 不低于 85%；
- Stage03 covered/probable 标签自身的 precision 不低于 90%；
- Stage03 `core_software_uncovered` 终止拒绝的 precision 不低于 95%；
- 不得出现仅因软件未报告、别名缺失、官方版本或 revision 差异产生的 terminal reject；
- 单独报告 `software_inventory_unconfirmed` 比例及其在 Stage05 的最终解析率；
- 正常调用不再出现思考耗尽输出 token；
- 执行失败和科学拒绝在 registry/resume 中保持可区分；
- 每个改判结果都有 workflow ID、step ID、软件原名、规范化结果和 evidence ID；
- 不通过 DOI、标题、期刊或特定论文硬编码提高指标。

## 9. 缓存、Resume 和当前任务

1. 当前运行任务继续使用其 frozen config、prompt 版本和缓存，不在中途切换；
2. 实施后同时提升 Stage02/03 prompt 和 schema 版本；
3. Stage02 改变时，其 Stage02-05 下游缓存失效；
4. 仅 Stage03 代码改变时，可复用满足新合同的 Stage02 结果；
5. 回归使用独立 run ID，不覆盖原 decisions、registry 或 resume state；
6. API/JSON/token 失败在 resume 时重试，terminal scientific reject 不自动重试；
7. 所有历史结果保留原模型、prompt、toolbox hash 和原始响应哈希。

## 10. Git 实施方式

确认后在本地 `main` 上实施，不新建分支、不上传 GitHub。工作区已有其他修改，只暂存本任务路径。

建议本地提交：

1. Stage02 冻结工作流合同和无思考模型链；
2. Stage03 软件绑定与工作流级覆盖；
3. Stage05 资源审计迁移；
4. 回归测试、改判审计和实施记录。

不能通过新增论文、DOI、期刊或特定软件硬编码修补回归样本。问题应在证据构建、工作流合同、通用规范化或门控语义层解决。

## 11. 主要风险

### 11.1 Stage02 候选遗漏

若 Stage02 只输出一个工作流，可能选中未覆盖流程并遗漏另一条已覆盖流程。因此允许最多三个候选，并在一次验证调用中统一确认；不让 Stage03 重新搜索新流程。

### 11.2 Stage02 错误拆分依赖工作流

若两个步骤共同生成一个科学结果，或一个流程依赖另一流程的关键中间产物，Stage02 必须用 `depends_on_workflow_ids` 表达依赖并在确认时作为整体检查，不能为了软件覆盖拆开。

### 11.3 Stage03 错误降级辅助软件

不是所有分析软件都可忽略。若它生成评分目标或不可透明重建的关键科学量，它仍是冻结工作流的必要依赖。判断依据是步骤和科学产物，不是软件类别名称。

### 11.4 别名过度匹配

精确别名、通用版本语法和同 backend 别名共识可直接判定 covered。名称可唯一指向已覆盖基础软件、但修饰形式未登记时判定 probable 并通过。模糊匹配不能把不同软件直接映射为 covered，也不能反过来仅因匹配不精确判定 uncovered。

### 11.5 未报告软件导致下游数量增加

`software_inventory_unconfirmed` 改为通过后，Stage04/05 输入会增加。这是高召回负向排除门的预期结果。Stage05 必须分别统计“高质量文本后确认覆盖、确认不覆盖、仍无法确认”的数量，避免把 Stage03 未确认候选误报为工具箱覆盖论文。

### 11.6 多模型漂移

不同 fallback 模型可能产生分布差异。运行记录必须保留实际模型，报告按模型分层统计 precision、recall 和通过率。fallback 只处理执行失败，不用于寻找更宽松结论。

## 12. 最终实施边界（已确认并实施）

以下边界汇总了既有确认和本次新增的 Stage03 负向排除语义：

1. Stage02 独占计算流程完整性判断，并输出最多三个经过验证的 `confirmed_workflows`；
2. Stage03 不重新发现或审查计算流程，只绑定软件并执行工具箱覆盖负向排除；
3. Stage02 保留四类 Pass，包括实验主导但具有完整、非平凡计算子工作流的论文；
4. Stage02 保留两次调用：候选发现/分类和一次统一候选验证；
5. Stage02 默认模型链为 DeepSeek-V4-Pro -> Nex-N2-Pro -> DeepSeek-V4-Flash -> Nex-N2-Pro-w8a8 -> DeepSeek-V4-Flash-DSpark -> MiniMax-M2.7 -> Mimo-V2.5-Pro -> Qwen3.6-27B；
6. Stage03 默认模型链为 Nex-N2-Pro -> DeepSeek-V4-Pro -> DeepSeek-V4-Flash -> Nex-N2-Pro-w8a8 -> DeepSeek-V4-Flash-DSpark -> MiniMax-M2.7 -> Mimo-V2.5-Pro -> Qwen3.6-27B；
7. GLM-5.2 和 Kimi-K2.6 只作为默认链之后、需显式启用的 emergency reserve；
8. 对支持无思考开关的模型必须关闭思考；无专用开关的后级模型必须通过预检并配置足够输出预算；
9. fallback 只响应执行失败，不能因正常拒绝、低通过率或不确定结论切换；
10. 任一 Stage02 冻结工作流的软件被工具箱覆盖，即可使论文得到 `software_covered`；
11. 可唯一归一化的别名、官方版本和 revision 差异判为 covered；基础软件唯一但修饰仍轻微不确定时判为 probable，两者都通过；
12. 只有明确识别为工具箱中不存在的独立必要软件，才能形成 `workflow_uncovered`；
13. 论文未报告软件、软件无法绑定或软件清单不完整时返回 `software_inventory_unconfirmed`，但仍通过 Stage03；
14. 只有所有 Stage02 冻结工作流都明确为 `workflow_uncovered` 时，论文才能以 `core_software_uncovered` 淘汰；
15. `mixed_workflow_candidate` 降为审计信息，不再论文级淘汰；
16. Stage03 完全停止资源筛选，资源审计迁移到 Stage05；Stage05 同时负责解析 Stage03 未确认的软件；
17. 当前运行任务不切换新逻辑，实施后先隔离回归，再决定是否 resume 重算。

本次需要确认的新增边界只有第 13、14 和 16 项：软件未报告也通过、仅在所有工作流都明确未覆盖时淘汰，以及 Stage05 接管未确认软件的最终审查。除此之外没有新的阻塞边界问题。确认后再修改代码。实现期间若模型 `/models` 不可用、某模型不接受文档规定的参数或无法稳定返回 JSON，按预检和 fallback 规则自动跳过该模型，不改变筛选语义。
