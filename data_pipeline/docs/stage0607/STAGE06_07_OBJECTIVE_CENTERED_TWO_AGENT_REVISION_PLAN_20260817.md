# Stage06/07 目标中心、双 Agent 任务构建修改方案

## 1. 文档目的

本文档针对当前 Stage06/07 实现制定代码修改方案。目标是把任务构建单位从“整篇论文的完整计算流程”调整为：

> 围绕一个明确科学目标，抽取一个输入闭合、过程可复现、具有中间关键结论和最终关键结论的计算化学过程，并构建论文复现与自主科研两种评估模式。

本方案只描述设计和验收方式，当前不修改业务代码。经用户确认后，按照本文档逐步实施。

## 2. 当前实现与目标的差异

当前 Stage06 的主要逻辑仍然以论文级 workflow 为中心，存在以下偏差：

1. `FULL-PAPER-FIRST` 容易把论文范围误认为任务范围，可能拒绝论文中具有明确科学目标但只覆盖一个完整子过程的任务。
2. 复杂度主要由计算步骤、分支和工具调用数量描述，不能充分表达竞争假设判别、负结果排除、描述符抽象等科研推理难度。
3. 论文复现任务复制为自主任务后，当前固定可编辑文件列表无法覆盖文件名、XYZ 注释、JSON 深层字段和输入资产标签等泄漏面。
4. Ground Truth 需要同时支持数值、结构、排序、趋势、中间结论和最终文字结论，但当前模式绑定和过程检查点的边界不够清晰。
5. Stage07 需要审计“目标中心的科学闭环”，而不只是检查论文流程字段是否齐全。
6. 编排器只能负责阶段编排、文件传递和结构完整性，不能根据固定规则代替 Agent 作科学裁决。

## 3. 总体架构

```text
Stage06A Scientific Task Builder
  ├─ 阅读论文、SI 和解析证据
  ├─ 识别科学目标候选
  ├─ 选择一个目标中心过程
  ├─ 生成 Objective Card
  ├─ 先生成论文复现任务
  └─ 生成共享 Key Points、Ground Truth 和 Acceptance Profile
                 |
                 | 复制文件夹和只读合同传递
                 v
Stage06B Autonomous Task Converter
  ├─ 复制论文复现任务
  ├─ 删除方法、路线和身份泄漏
  ├─ 保留同一科学目标、公共问题输入和结论目标
  ├─ 递归清理文件名、结构标签、JSON 和 XYZ 注释
  └─ 生成转换报告
                 |
                 v
Stage07 Audit-Repair Agent
  ├─ 优先审计并修复 Stage06A 选择的过程
  ├─ 审计科学目标、输入、Key Points、评分和泄漏
  ├─ 修复可修复问题
  ├─ 必要时重新设计另一个完整目标过程
  └─ 输出最终 Agent 决定
```

Stage06A 和 Stage06B 必须运行在不同的独立工作空间中。两者之间通过复制目录和生成的 JSON 合同传递信息，不共享可写目录。

Stage06B 是窄职责 Agent，不重新判断论文是否科学可构建，不修改 Ground Truth 的科学含义，不负责最终通过/拒绝。

## 4. Stage06A：科学目标与论文复现任务构建

### 4.1 Agent 职责

Stage06A 负责：

1. 阅读正文、SI、表格、坐标、布局文本和解析回退材料；
2. 盘点论文中作者实际执行的计算工作；
3. 识别一个或多个科学目标候选；
4. 选择一个证据闭合且具有科研价值的目标；
5. 抽取围绕该目标的完整计算过程；
6. 抽取中间科学判断和最终科学结论；
7. 生成论文复现任务和隐藏参考；
8. 记录选择范围、未选范围和选择原因。

“完整”定义为目标中心闭环，而不是覆盖论文所有计算：

```text
公共问题输入
  → 需要解决的科学未知量
  → 真实计算/分析步骤
  → 中间判别结论
  → 最终科学结论
```

### 4.2 目标选择原则

Prompt 应从 `full-paper-first` 改为 `objective-first`：

- 优先选择具有明确科学问题和可评分结论的目标；
- 整篇论文只有在其计算内容围绕一个连贯目标时才整体纳入；
- 如果论文包含多个互不相关研究，选择最大的完整目标中心过程；
- 允许选择论文中的完整子过程；
- 不要求固定的步骤数量；
- 不因上游 Stage02-05 的候选范围而机械拒绝；
- 不把文件转换、绘图、简单算术或报告写作当作科学计算步骤。

可支持的通用任务族包括但不限于：

- `mechanism_reconstruction`：恢复机理、过渡态家族或选择性来源；
- `hypothesis_discrimination`：比较竞争假设，利用计算和负结果排除路径；
- `descriptor_discovery`：从多个结构/电子特征中找出解释趋势的描述符；
- `selectivity_explanation`：解释构象、配体、取代基或条件导致的选择性；
- `state_or_pathway_validation`：验证电子态、反应路径或中间体关系。

任务族只是语义标签，不作为死规则。Agent 可以选择未列出的任务族，但必须说明目标和评分方式。

### 4.3 Objective Card

新增内部文件 `objective_card.json`，建议字段如下：

```json
{
  "objective_id": "objective-1",
  "task_family": "hypothesis_discrimination",
  "scientific_question": "...",
  "public_question": "...",
  "problem_inputs": [],
  "experimental_observations": [],
  "unknowns": [],
  "candidate_hypotheses": [],
  "selected_scope": {
    "kind": "objective_centered_workflow",
    "is_whole_paper": false,
    "included_workflows": [],
    "excluded_workflows": [],
    "selection_reason": ""
  },
  "workflow_steps": [],
  "key_points": [],
  "final_claim": {},
  "resource_profile": {},
  "evidence_ids": []
}
```

`objective_card.json` 是内部构建材料。自主任务只能得到经过公开面投影后的科学问题和问题输入，不能得到 `withheld_route_information` 等内部字段。

### 4.4 Workflow Step

工作流步骤保留现有结构化表达，但将步骤绑定到 Objective Card：

```json
{
  "step_id": "s1",
  "step_type": "core_computation",
  "scientific_purpose": "...",
  "inputs": [],
  "outputs": [],
  "depends_on": [],
  "software": [],
  "parameters": {},
  "branch": "hypothesis-a",
  "evidence_ids": []
}
```

最小科学合同只要求：

- 至少一个真实化学计算或有科学意义的计算分析；
- 至少一个有证据的中间或最终科学 Key Point；
- 输入、方法、输出和结论能够闭合；
- 不能依赖猜测补全缺失结构、参数或答案。

不设置固定“三步”或固定工具调用次数作为科学通过条件。

### 4.5 Key Point 与 Ground Truth

新增 `key_points.json`，每一个 Key Point 都必须对应一个可评分的科学判断：

```json
{
  "key_point_id": "kp-1",
  "stage": "intermediate",
  "kind": "hypothesis_rejection",
  "question": "该竞争路径是否可以被排除？",
  "expected_conclusion": "...",
  "ground_truth_type": "semantic_propositions",
  "acceptance_profile_id": "accept-kp-1",
  "evidence_ids": [],
  "applies_to_modes": [
    "paper_reproduction",
    "autonomous_research"
  ]
}
```

支持的 Ground Truth 类型至少包括：

- 数值或数值范围；
- 结构身份或几何关系；
- 排序；
- 趋势；
- 假设支持/排除；
- 机理命题；
- 中间文字结论；
- 最终文字结论；
- 必需计算产物。

两种模式共享科学结论和结论 Acceptance Profile。论文方法、执行顺序和作者特定中间检查点只进入论文复现模式的过程评分，不作为自主模式必须复制的路线答案。

### 4.6 复杂度

复杂度改为描述目标完成所需的科学推理，而不是单纯计算数量：

```json
{
  "complexity_profile": {
    "level": "medium",
    "core_calculations": 4,
    "scientific_branches": 2,
    "intermediate_decisions": 3,
    "validation_operations": 2,
    "systems_or_states": 5,
    "software_families": ["gaussian", "cclib"],
    "requires_hypothesis_revision": true,
    "reasoning_requirements": "..."
  }
}
```

该字段用于描述任务和排序，不作为“必须覆盖整篇论文”的替代死门槛。明显只有一次计算并直接读取答案的任务仍应由 Agent 标记为科研价值不足，但不通过固定步数代码判定。

## 5. 论文复现任务合同

Stage06A 只生成论文复现任务和隐藏参考，目录建议为：

```text
outputs/
  objective_card.json
  paper_reproduction/
    task.md
    task_info.json
    task_spec.json
    submission_contract.json
    process_rubric.json
    data/
      inputs/
    paper_route.md
    workflow_spec.json
    route_evidence_map.json
  hidden_reference/
    ground_truth_common.json
    key_points.json
    acceptance_profiles.json
    conclusion_rubric.json
    private_evidence_map.json
  conversion_manifest.json
```

论文复现模式可以公开作者的软件、方法、参数、路线顺序和验证流程，但不能公开目标值、关键排序、机理结论、Acceptance Profile 的具体答案或隐藏证据内容。

## 6. Stage06B：自主科研任务转换 Agent

### 6.1 职责边界

Stage06B 接收 Stage06A 已经生成的复现任务，通过复制目录生成自主任务。

它必须：

- 保留同一个 Objective Card 的科学目标；
- 保留相同的公共问题输入；
- 保留相同的最终结论 Key Point 和 Acceptance Profile；
- 删除论文方法、路线、候选排序和答案导向描述；
- 递归清理 Markdown、JSON、文件名、XYZ 注释和结构标签；
- 记录每个删除、重命名和改写动作。

它不能：

- 重新选择科学目标；
- 修改 Ground Truth 的科学含义；
- 修改论文复现任务；
- 修改化学工具箱；
- 返回最终科学通过或拒绝。

### 6.2 文件和资产分类

Stage06A 生成 `conversion_manifest.json`，把资产分为：

```text
common_problem_inputs
  反应物、产物、催化剂、实验条件、原始观测和答案无关的结构输入

reproduction_route_assets
  论文路线、作者方法、路线辅助结构、作者命名和特定执行模板

hidden_reference_assets
  目标数值、目标排序、关键结构、结论和证据映射
```

自主模式保留第一类，并根据科学问题保留必要的答案无关资产。若某个复现资产本身包含路线标签或目标结构身份，必须删除、重命名或改写，而不是原样复制。

### 6.3 不再使用固定四文件编辑白名单

当前固定四文件限制位于 [stage.py](/mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline/src/stages/stage06_task_builder/stage.py:1145)，需要取消。

Stage06B 允许递归编辑复制后的 `autonomous_research/`，但代码仍需强制：

- 不能写入 `paper_reproduction/`；
- 不能写入 `hidden_reference/`；
- 不能写入源论文或工具箱目录；
- 所有修改写入 `conversion_report.json`；
- 转换前后的公共科学字段必须保持一致；
- 自主目录不能包含隐藏目录或内部 source path。

建议输出：

```json
{
  "conversion_status": "converted",
  "source_mode": "paper_reproduction",
  "target_mode": "autonomous_research",
  "removed_files": [],
  "renamed_files": [],
  "rewritten_files": [],
  "preserved_common_assets": [],
  "remaining_disclosures": [],
  "unchanged_scientific_fields": [
    "objective_id",
    "scientific_question",
    "key_point_ids",
    "acceptance_profile_ids"
  ]
}
```

## 7. Stage07 目标中心审计与修复

### 7.1 审计顺序

Stage07 必须先审计和修复 Stage06A 选择的目标中心过程，只有在证明该过程科学上不可修复后，才考虑论文中的另一个目标。

审计顺序为：

1. 科学问题是否明确；
2. 公共输入是否足以提出问题；
3. 目标中心计算过程是否闭合；
4. 中间 Key Point 是否有论文证据；
5. 最终结论是否有论文证据；
6. 论文复现模式是否公开了足够路线；
7. 自主模式是否删除了路线和答案泄漏；
8. 两种模式是否共享同一个科学结论目标；
9. 工具箱和资源是否能够支持任务；
10. 评分规则是否能分别评价过程和结论。

### 7.2 可修复问题

Stage07 可以直接修复：

- 缺失的论文来源输入；
- 不完整的 task 指令；
- 中间或最终 Key Point 缺失；
- Acceptance Profile 绑定错误；
- 自主模式路线泄漏；
- 文件名、XYZ 注释或 JSON 字段泄漏；
- 软件缺失说明；
- 任务成本说明；
- 提交格式和报告路径错误。

Stage07 不应通过固定代码规则判定科学方法唯一正确，也不应因为自主模式没有复现论文路线而拒绝任务。

### 7.3 决策状态

保留 Agent 决策权，建议使用：

- `approved`：无需修复即可使用；
- `approved_with_repairs`：原目标保留并完成修复；
- `approved_after_workflow_redesign`：原目标不可用，另一个完整目标已实际重建；
- `rejected_scientific_unrepairable`：关键输入、过程或 Ground Truth 缺失且无法从来源恢复；
- `objective_failure_retryable`：API、Agent、文件系统或解析等客观失败，可重试；
- `needs_software`：科学任务可构建，但工具箱缺少软件；
- `missing_data`：任务仍缺关键数据；
- `high_cost`：目标中心过程在当前资源预算下难以执行。

工具箱缺失不能自动导致科学拒绝。Agent 应记录缺失软件，由后续流程决定是否安装和重跑。

## 8. 编排器边界

编排器只执行以下工作：

- 启动两个 Stage06 Agent 和一个 Stage07 Agent；
- 为每个 Agent 创建独立 workspace；
- 复制已完成的目录和只读输入；
- 检查 receipt、文件存在性、JSON 可解析性和 workspace 边界；
- 生成阶段状态和 resume 信息；
- 保存 Agent 原始输出与最终文件树。

编排器不得：

- 根据固定步骤数量判定任务是否有效；
- 根据软件 Action 名称判定软件是否缺失；
- 覆盖 Agent 的科学通过/拒绝；
- 自动把格式错误改写成科学拒绝；
- 自动选择另一个论文 workflow；
- 自动修改 Ground Truth 或结论。

## 9. 配置和运行方式

新增两个可配置 Agent：

```env
STAGE06_BUILDER_HARNESS=codex
STAGE06_BUILDER_MODEL=deepseek-v4-flash
STAGE06_BUILDER_MAX_TOOL_CALLS=120

STAGE06_CONVERTER_HARNESS=codex
STAGE06_CONVERTER_MODEL=deepseek-v4-flash
STAGE06_CONVERTER_MAX_TOOL_CALLS=60

STAGE07_AUDITOR_HARNESS=codex
STAGE07_AUDITOR_MODEL=deepseek-v4-flash
```

harness 支持 `codex`、`claude`、`opencode`，模型和 API 仍从配置读取，不写入业务逻辑。

每个阶段只保留一个小型 receipt 和必要的 Agent 轨迹，不再产生大量 `finished_at.txt`、`failed_count.txt` 等散落 sentinel 文件。

## 10. 正式发布隔离

内部构建目录可以保留完整 pair：

```text
internal_task_pair/
  paper_info.json
  objective_card.json
  paper_reproduction/
  autonomous_research/
  hidden_reference/
  conversion_report.json
  stage07_audit.json
```

最终发布必须拆分成两个互不相邻的任务目录：

```text
published_tasks/
  task_001_reproduction/
    task_info.json
    task.md
    data/

  task_001_autonomous/
    task_info.json
    task.md
    data/
```

评估 Agent 不得看到 sibling 模式、hidden reference、paper_info、原始论文路径、DOI、内部 evidence ID 或 Stage06/07 轨迹。

## 11. 代码修改清单

### Stage06

- 修改 `src/stages/stage06_task_builder/prompts.py`：改为 objective-first Prompt，增加 Objective Card、Key Point 和双 Agent 合同。
- 修改 `src/stages/stage06_task_builder/stage.py`：增加 Stage06B 转换阶段、独立 workspace、复制和恢复逻辑。
- 修改 `src/stages/stage06_task_builder/bootstrap_task_pair.py`：生成 Objective Card、Key Points 和 conversion manifest。
- 修改 `src/stages/stage06_task_builder/validation.py`：从 workflow 全覆盖检查改为目标闭环、证据绑定和目录边界检查。
- 更新相关 schema 和配置，使两个 Stage06 Agent 的 harness、模型、工具调用上限可配置。

### Stage07

- 修改 `src/stages/stage07_task_judge/prompts.py`：从论文级 workflow 审核改为目标中心审核，明确优先修复 Stage06A 目标。
- 修改 `src/stages/stage07_task_judge/stage.py`：接收 Objective Card、Key Points 和 Stage06B 转换报告，支持目标重设计状态。
- 修改 `src/stages/stage07_task_judge/validation.py`：只做结构和文件边界验证，不替 Agent 作科学裁决。

### 发布与评估

- 增加内部 pair 到两个独立 published task 的导出步骤。
- 检查评估 workspace 只能复制当前模式的 `data/`。
- 增加不依赖固定论文词表的公开面扫描。

## 12. 验收标准

### 结构验收

- Stage06A、Stage06B、Stage07 均在独立 workspace 运行；
- Stage06B 无法写入复现目录和 hidden reference；
- Stage07 不能修改工具箱；
- 最终两个 published task 互相不可见；
- resume 后不会重复生成已完成阶段。

### 科学合同验收

- 每个通过任务有一个明确 scientific objective；
- 目标中心过程的输入、计算、输出和结论闭合；
- 至少存在一个有证据的 Key Point；
- Ground Truth 同时支持数值、结构、趋势、排序和文字结论；
- 论文复现模式和自主模式共享结论目标；
- 两种模式可以使用不同过程 rubric；
- 不要求覆盖整篇论文或固定步骤数量。

### 泄漏验收

- 自主模式没有绝对路径、DOI、论文身份和 source evidence ID；
- 文件名、XYZ 注释、JSON 深层字段和 Markdown 不泄漏路线；
- 不出现 TS、INT、PRODUCT、major/minor 等会直接暴露答案的标签，除非它们是问题本身必需且答案无关；
- 自主模式不能通过输入目录排列顺序恢复作者路线；
- 公共输入仍足以让 Agent 理解并解决科学问题。

### 科学质量验收

- 至少使用一篇真实论文完成回归测试；
- 测试至少覆盖一个机理恢复或竞争假设任务；
- 记录 Stage06A、Stage06B、Stage07 的原始轨迹和最终产物；
- 检查 Stage07 是否真正修复泄漏、Key Point 或评分缺陷；
- 工具箱缺失只生成软件建议，不导致错误科学拒绝；
- 明确区分科学不可构建、软件暂缺、成本过高和客观运行失败。

## 13. 实施顺序

1. 新增并测试 Objective Card、Key Point、conversion manifest schema；
2. 重写 Stage06A Prompt 和输出合同；
3. 实现 Stage06B 独立 workspace、复制和递归转换；
4. 删除固定四文件编辑限制，增加转换报告；
5. 修改 Stage06 validator，去除整篇论文和固定步数导向；
6. 修改 Stage07 Prompt 和审计输入；
7. 实现两个模式的物理发布隔离；
8. 增加单篇论文回归测试和公开面泄漏测试；
9. 使用一篇真实论文运行完整 Stage06/07；
10. 通过后再运行多篇论文测试并记录迭代日志。

## 14. 非目标

本次修改不包括：

- 重新设计 Stage02-05；
- 自动安装或修改化学工具箱软件；
- 引入第四个科学裁判 Agent；
- 用代码规则替代 Stage06/07 Agent 的科学判断；
- 强制所有任务完全复制 ARCHE 的三个 Case；
- 以固定步数、固定软件数量或固定工具调用次数定义科研价值。

