# Stage06/07 批量运行共性问题与修复方案

日期：2026-08-20  
分析对象：

`runs/stage06-07-gpt-5.6-sol-stage05-passed-concurrency8-20260820T033608Z`

## 1. 运行快照

本批次由 `gpt-5.6-sol + Codex harness` 执行，并发上限为 8。用户要求停止时，批次状态已标记为 `STOPPED_BY_USER`。

停止时的文件系统快照为：

| 指标 | 数量 | 含义 |
|---|---:|---|
| 计划提交论文 | 529 | `batch_status.json` 中的固定输入集合 |
| 已创建论文目录 | 374 | 已启动过 Stage06/07 单论文流程 |
| 已形成 Stage07 审计结果 | 284 | 有 `stage_07_task_audit/audit_results.jsonl` |
| Stage07 科学审计通过 | 97 | `scientific_audit_passed=true` |
| Stage07 科学拒绝 | 186 | `rejected_scientific_unrepairable` |
| Stage07 机械通过并可发布 | 30 | `publish_ready=true` |
| 科学批准但机械阻断 | 67 | `mechanical_approved_but_unpublished=true` |
| 仍处于未完成/未形成完整审计的目录 | 90 左右 | 批次被停止时尚未闭合，不能当作失败或通过 |

由于批次被中途停止，`374` 个目录不能等价为 `374` 个完成任务。单篇 `run_status.json`、Stage06 receipt、Stage07 receipt 可能处于不同终态，后续统计必须以各阶段的实际 receipt 为准。

## 2. 总体判断

Stage06/07 已经能完成“科学目标选择 → 复现任务构建 → 自主表面转换 → Stage07 科学审计/修复 → 机械发布检查”的基本链路，但目前仍有三个断点：

1. Stage06/07 Agent 的科学决策与发布合同没有稳定闭合。
2. 机械 gate 把一部分正确的自主脱敏误判为模式不一致，同时又无法发现一部分真实的 evaluator binding 错误。
3. 批量停止和失败状态的记录不够统一，导致“已创建、Stage06完成、Stage07完成、可发布”容易被混为一谈。

这不是单一模型能力问题。科学任务选择和部分审计遗漏主要属于 Prompt 执行/模型能力；合同字段、gate 比较语义、状态落盘和 evaluator dry-run 的边界则是代码/协议问题，应分别处理。

## 3. 共性问题、归因和方案

### P0-1：Stage07 科学批准不等于可发布，合同修复没有形成闭环

**实测现象**

67 个任务的 Stage07 decision 为 `approved` 或 `approved_with_repairs`，但机械状态为 blocked。常见 finding 包括：

- `process_rubric_not_array`；
- `submission_required_files_missing`；
- `hidden_ground_truth_common_missing`；
- `evaluator_load_failed`（例如 `task_info.category` 缺失）；
- 公开模式中残留 `hidden_reference`。

**归因**

- `Stage07 Agent`：没有在最终文件上逐项验证它声称修复的合同，属于 Prompt 执行不完整和模型审计能力不足。
- `代码/协议`：Stage07 receipt 与机械事实虽然已经分字段记录，但当前流程仍允许“Agent approved + 实际不可发布”长时间停留在中间状态，且没有统一的后续处理终态。

**方案**

1. 保留科学 decision 和机械 publication status 两条独立轴。
2. 科学批准后必须经过一次发布前机械检查；失败后进入明确的 `mechanical_publish_blocked` 终态，而不是继续显示为普通 approved。
3. 仅将科学批准且机械阻断的任务送入一次窄职责合同修复流程（详见 Stage07B 文档）。
4. 修复后仍失败时写入 `mechanical_blocked_unresolved`、finding 列表和 `publish_ready=false`，不自动改变科学 decision。

### P0-2：机械 gate 对安全脱敏过于严格，产生系统性误报

**实测现象**

批次中出现大量：

- `mode_pair_input_assets_mismatch`；
- `mode_pair_submission_contract_mismatch`。

抽查此前固定的20篇发现，至少7篇的差异仅来自自主模式的中性文件名、JSON manifest 匿名化或交付字段改名，科学输入和评分语义仍然对应。

当前 gate 的两个具体问题：

- `required_files` 仍包含文件名的逐字比较；
- 输入资产除 XYZ 第二行注释外，JSON、SMILES、manifest 等按原始字节哈希比较。

**归因**

这是代码侧比较语义错误，不是模型能力问题。自主模式本来就需要中性化名称和部分元数据。

**方案**

1. `submission_contract` 比较交付角色、文件类型、路径安全、结果结构和 Ground Truth binding，不比较答案相关的字面名称。
2. 输入资产按 `asset_id → 类型 → 规范化科学内容` 比较：
   - XYZ 去除注释行；
   - JSON 只忽略明确声明的展示标签/来源标签，保留数值、结构、边界条件和关系；
   - SMILES、坐标、实验观测等科学载荷不可删除或改变。
3. Stage06B 输出一份私有的等价映射/转换记录供 Stage07B 使用，但不复制到公开任务。
4. 不用论文名、分子名或固定关键词建立特例规则。

### P0-3：evaluator dry-run 检查过弱，真实 binding 错误被放行

**实测现象**

此前已发布任务中发现：

- `results_schema` 为空，但 acceptance profile 绑定到未定义字段；
- 真实字段是 `delta_g_B_minus_A_kcal_mol`，绑定却写成 `$.value`；
- 某些模式字段同时混在共同 `observed_fields` 中，存在绑定歧义。

当前 `_evaluator_dry_run()` 主要验证 Pydantic schema 能否加载、路径是否安全和 observed_fields 是否非空，并没有确认 JSONPath 在 `results_schema` 中真实可落地。

**归因**

- 绑定内容错误主要是 Stage06/Stage07 Prompt 执行和模型审计遗漏。
- 代码侧的问题是 dry-run 观察能力不足，不能把明显的结构错绑反馈给 Agent。

**方案**

1. Stage07 Prompt 要求每个 Ground Truth item 只有一个明确的 mode-specific binding，并列出 artifact、field、类型和证据。
2. Stage07B 对 binding 做结构化检查：解析受支持的 JSONPath，确认顶层字段/嵌套字段在对应 `results_schema` 中存在且类型兼容。
3. 代码只报告 binding observation，不依据科学数值作裁决；无法解析的绑定交给 Agent 修复。
4. 没有真实可绑定字段时阻止发布，并给出具体字段路径，不接受 Agent 的 `contract_status=passed` 自报作为替代。

### P0-4：Stage06 输出协议与 evaluator 合同仍有漂移

**实测现象**

批量任务中重复出现：

- `task_info.category` 缺失；
- `process_rubric.json` 使用对象包装而不是顶层数组；
- `required_file`、`primary_file`、`required_artifacts` 等非标准字段；
- `scientific_requirements` 偶尔为对象数组而非字符串列表。

**归因**

这是 Prompt、模板和协议三者没有共享唯一最终 schema 的问题。不能归因于某一篇论文。

**方案**

1. 生成阶段使用唯一的发布合同示例和字段表；Stage06A/06B 只生成科学内容和必要草稿，Stage07/Stage07B 按同一合同投影。
2. `task.md` 是唯一任务指令；JSON 只保存短索引元数据，不复制第二套操作指令。
3. 对运输字段使用一次确定性的 normalizer，避免多处 alias/canonicalize 互相覆盖。
4. 删除已废弃的 legacy alias 和无调用的重复 bootstrap/gate 路径；保留最小兼容层时必须有明确迁移期限。

### P1-1：Stage06A 的输入/工作流完整性仍依赖模型自检，且失败反馈没有闭环

**实测现象**

Stage06A 能构造不少科学目标，但个别任务声明了输入或参考态，却没有在 `data/inputs` 和 workflow steps 中完整提供；阶段最终仍可能返回 provisional constructed。

**归因**

主要是 Stage06A Prompt 执行和模型能力问题。代码不应把化学计量、物理边界或“什么是核心子流程”写成论文特例硬规则。

**方案**

1. Stage06A 的 `workflow_completeness_check` 必须列出每个输入、参考态、中间产物和最终产物，并给出 evidence ID。
2. 代码只做非阻断的引用图观察：声明资产是否存在、workflow input/output 是否有悬空引用；把 finding 喂回 Stage06A 或 Stage07。
3. Stage07 继续读取正文/SI和私有资产映射，负责科学判断输入是否完整、参考态是否守恒、计算动作与验证是否匹配。
4. 只有源材料本身无法补救时才科学拒绝；不要用代码猜测缺失结构或补充 Ground Truth 数值。

### P1-2：自主模式的公开边界和严格数值 GT 存在张力

**实测现象**

很多任务允许自主选择方法，却仍然用论文特定方法产生的很窄绝对数值容差评分。这会把合理的方法选择误判为失败。

**归因**

这是任务设计和 Prompt 语义问题，不是机械 gate 问题。

**方案**

每个任务明确选择一种模式：

- 方法受约束的自主 workflow：公开必要溶剂、温度、压力、体系和方法边界，保留严格数值评分；
- 方法发现型自主 workflow：放宽绝对数值，重点评分排序、符号、趋势、过程证据和解释。

不要用“完全自主”措辞描述实际上固定方法边界的任务。

### P1-3：批量停止后的状态不可直接用于质量统计

**实测现象**

用户停止批次后，一些目录的 `run_status.json`、Stage06 summary 和 Stage07 audit receipt 不同步；“进程退出”不代表 Stage07完成。

**归因**

这是运行器状态机和停止处理的问题。

**方案**

1. 区分 `submitted`、`stage06_completed`、`stage07_completed`、`mechanical_checked`、`published`。
2. 收到停止信号时，未形成终态 receipt 的任务统一写 `stopped_incomplete`，不要伪造 completed。
3. 汇总脚本只统计对应阶段有权威 receipt 的任务；批次中途停止时输出 `incomplete_count`。
4. 不删除 Stage00–05 输入或筛选结果；Stage06/07运行目录应有独立前缀和清理清单。

### P1-4：token和工具调用成本仍被合同返工放大

**实测现象**

任务在 Stage07 科学批准后因合同格式失败，仍需要完整 Agent 审计或人工复核；重复读取大文件、重复生成同一文件会放大输入 token。

**归因**

主要是流程设计和 Prompt 预算约束问题，部分是模型没有按批量读取指令执行。

**方案**

1. Stage07 首次读取使用 `audit_index.json` 和分组脚本，只读取一次核心文件。
2. 先执行确定性运输归一化和最小 gate，再决定是否需要 Agent 修复。
3. Stage07B最多一次合同修复尝试；不要因为机械 finding 重跑完整科学审计。
4. 所有 Agent 共享统一的“已检查文件列表”和剩余问题列表，禁止重复生成 process trace。

## 4. Stage06/07实际发挥情况

### 已发挥作用

- Stage06A能从论文中选择整篇核心路线或重要核心子流程；
- Stage06B多数任务完成了自主模式中性化；
- Stage07对部分任务做了科学修复、披露清理和 workflow redesign；
- 机械 gate确实拦截了缺少 category、hidden GT、错误 rubric 类型和公开 hidden_reference 等硬错误。

### 尚未达到预期

- Stage07科学批准后仍有较多任务合同不可加载；
- gate无法区分安全脱敏和真正输入删除；
- evaluator binding观察不够强；
- 中途停止时统计状态不闭合；
- “可发布任务数量”不能直接代表“高质量科学任务数量”。

## 5. 推荐实施顺序

1. 先修正批次状态机和机械 gate 的比较语义，加入 binding 结构观察，但不加入化学特例规则。
2. 收紧 Stage06A/Stage07 Prompt 的合同闭合表和最终文件复核要求。
3. 增加窄职责 Stage07B，处理科学批准后的剩余合同阻断。
4. 用本批次固定 fixture 回归：真实合同错误必须阻断，安全脱敏不得误报，真实输入删除必须阻断，错误 binding 必须被发现。
5. 再用不同计算方向的论文验证通用性。

