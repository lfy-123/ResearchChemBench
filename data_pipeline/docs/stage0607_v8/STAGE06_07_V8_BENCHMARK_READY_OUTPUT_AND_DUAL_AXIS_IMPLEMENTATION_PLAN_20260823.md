# Stage06/07 v8：最终任务包、三类任务管理、Benchmark 适配与 Stage07B 实施方案

版本：v8.1 修订方案稿

日期：2026-08-23

状态：待用户确认后实施
范围：Stage06A、Stage06B、Stage07A、可选 Stage07B、Stage07 最终任务整理，以及 ResearchChemBench 对三类任务的新加载与评估接口。

## 0. 本次更正

v8.0 把“兼容当前旧 benchmark 目录”和“迁移以前的测试结果”放得过重。根据用户反馈，本版明确撤回这一前提。

本轮真正要完成的是：

1. 整理和优化 Stage07 最终通过任务的文件；
2. 合成记录、模型轨迹、审计记录和内部映射继续留在 `runs/`，不进入最终任务包；
3. 将科学参考、接受条件、过程 Key Points 和最终结论整理成单一、清楚的隐藏评估参考；
4. 允许修改已经长期未更新的 benchmark repository、runner 和 evaluator，使它们适配新的数据管线输出；
5. 合理管理以下三类任务：
   - `paper_reproduction`：论文复现；
   - `autonomous_research`：自主科研；
   - `experiment_validation`：实验验证；
6. `experiment_validation` 由尚未定型的 `data_pipeline_experiment_validation` 生成，本轮不查看或修改该管线，只为它预留稳定、最小的接入接口；
7. 以前的 Stage06/07 测试批次只作为回归样本，不批量转换、不改写，也不作为最终数据直接安装；
8. 当前 `ResearchChemBench/tasks/` 中的旧任务不需要先被迁移，benchmark 可以在过渡期保留 legacy loader。

因此，本方案中的 ready 不再表示“可以原样复制进旧的扁平 `tasks/<task_id>/` 结构”，而是表示“Stage07 能生成符合新 `Task Package v1` 合同的干净任务包，改造后的 benchmark 能安全发现、执行和评估它”。

## 1. 总目标与边界

### 1.1 总目标

Stage06/07 应达到以下状态：

1. Stage06A 正确选择全文计算主线；若不可行，才退到最重要的核心子流程；完整主线和核心子流程均不可构建时，允许科学拒绝；
2. Stage06B 正确生成自主科研任务的公开表面，不泄漏论文路线和隐藏答案；
3. Stage07A 对科学代表性、输入闭合、物理量定义、模式口径、答案证据和公开/隐藏边界作最终科学审计；
4. Stage07 对每个最终通过的任务类型实例原子生成一个精简、无构建垃圾的任务包；
5. 缺少当前工具箱软件时登记 `needs_software`，不能仅因此科学拒绝；
6. Stage07B 仅在科学批准后处理重复、窄、可机械描述的合同修复；
7. benchmark 负责选择具体评分策略，例如 `dual_axis_100`，数据管线不决定分值、权重或评分公式；
8. 三类任务使用共同的发现、身份、安全隔离和结果归档机制，但允许使用不同的科学参考 schema 和 evaluator adapter；
9. 不增加论文、分子、固定数值或特定软件的特例规则。

### 1.2 正确终态

以下都可能是正确结果：

- `approved_ready`：科学和合同均通过，当前工具箱可运行；
- `approved_needs_software`：科学和合同均通过，但等待工具能力补齐；
- `scientifically_rejected`：源材料、代表性或科学闭合不满足；
- `technical_blocked`：科学批准，但安全合同修复仍未完成；
- `retryable_agent_failure`：模型/执行交付失败，不冒充科学拒绝。

目标不是让所有论文发布，而是让每个 Agent 角色正确发挥作用、代码无 bug、终态分类真实可解释。

### 1.3 明确不做

- 不把历史测试结果转成正式任务；
- 不为了迁就旧 evaluator 保留错误或重复字段；
- 不让代码做化学计量、参考态、量子态、溶剂或机理科学裁决；
- 不让 Stage07B 改科学问题、答案、容差、输入或 workflow；
- 不要求实验验证任务复用计算化学任务的内部 schema；
- 不在本轮查看尚未定型的 `data_pipeline_experiment_validation` 代码；
- 不把构建记录、论文全文、SI、prompt 或 Agent trace 放入最终任务包；
- 不在任务定义目录中存放某次 benchmark run 的模型提交和评分结果。

## 2. 当前 Stage06/07 运行目录分别有什么作用

以下说明保留现有运行轨迹的价值，同时明确哪些文件不能进入最终任务。

### 2.1 批次根目录

典型结构：

```text
runs/<batch_run>/
├── batch_status.json
└── papers/
    └── <paper_id>/
        ├── llm_cache/
        ├── late_stage_run_summary.json
        ├── stage_06_task_construction/
        └── stage_07_task_audit/
```

- `batch_status.json`：批次模型、并发、开始/结束时间和逐论文终态；
- `llm_cache/`：prompt、模型响应和调用缓存；
- `late_stage_run_summary.json`：提前失败或阶段未运行时的诊断摘要。

这些都是运行记录，不属于任何 benchmark task。

### 2.2 Stage06 根目录

```text
stage_06_task_construction/
├── input_snapshots/
├── workspaces/
├── checkpoints/
├── staging/
├── provisional_tasks/
├── build_results.jsonl
└── stage_summary.json
```

- `input_snapshots/`：正文、SI、Stage04/05 记录、证据索引、工具箱和资源快照；
- `workspaces/`：Stage06A/06B 的实际 Agent 工作区和 trace；
- `checkpoints/`：恢复、缓存和输入 fingerprint；
- `staging/`：原子提交前的临时树；
- `provisional_tasks/`：交给 Stage07 的双模式候选任务及 hidden reference；
- `build_results.jsonl`、`stage_summary.json`：逐论文和阶段汇总。

这些目录都不能直接作为最终任务包。

### 2.3 Stage06 候选任务对

当前 `provisional_tasks/<paper_id>/` 常见内容：

```text
provisional_tasks/<paper_id>/
├── autonomous_research/
├── paper_reproduction/
├── hidden_reference/
├── objective_card.json
├── workflow_review.json
├── key_points.json
├── toolbox_requirements.json
├── evidence_index.json
├── source_manifest.json
├── paper_info.json
├── construction_record.json
├── construction_receipt.json
├── conversion_manifest.json
├── conversion_report.json
├── stage06_handoff.json
└── task_pair_manifest.json
```

主要职责：

- `objective_card.json`：目标和范围选择；
- `workflow_review.json`：全文 workflow inventory、代表性、输入/动作/产物闭合、资源和软件审查；
- `key_points.json`：过程 Key Points 与最终结论草案；
- `toolbox_requirements.json`：所需软件/能力及缺口；
- `evidence_index.json`、`source_manifest.json`：来源证据和 hash；
- `conversion_*`：Stage06B 的脱敏合同和转换记录；
- `construction_*`、`stage06_handoff.json`：构建轨迹和正式交接；
- `task_pair_manifest.json`：候选任务对完整性。

这些文件对 Stage07 审计很重要，但绝大多数不应进入最终 task package。

### 2.4 当前 mode 目录

当前公开 mode 目录可能包括：

```text
<mode>/
├── task.md
├── task_info.json
├── task_spec.json
├── submission_contract.json
├── process_rubric.json
├── public_manifest.json
├── data/inputs/
├── paper_route.md                 # reproduction
├── workflow_spec.json             # reproduction
└── route_evidence_map.json        # reproduction
```

当前职责：

- `task.md`：唯一面向被评估 Agent 的任务指令；
- `task_info.json`：运行和分类 metadata；
- `task_spec.json`：Stage06/07 科学审计合同；
- `submission_contract.json`：交付文件、结果 schema 和 binding；
- `process_rubric.json`：任务特定过程 Key Points；
- `data/inputs/`：公开输入；
- reproduction 的路线文件：作者方法和 workflow 的结构化表达；
- `route_evidence_map.json`：来源证据映射。

其中只有部分内容属于最终 runtime。最终整理方案见第 6 节。

### 2.5 当前 hidden reference

```text
hidden_reference/
├── ground_truth_common.json
├── private_evidence_map.json
├── disclosure_contract.json
├── process_rubric_autonomous.json
└── process_rubric_reproduction.json
```

- `ground_truth_common.json`：科学真值、acceptance profile、最终结论和关键失败；
- `private_evidence_map.json`：论文证据和 public/private 资产映射；
- `disclosure_contract.json`：两个 mode 的公开边界；
- 两份 process rubric：当前 mode-specific 隐藏投影。

目前最大问题是同一答案、Key Point 和 mode projection 容易在多处重复。最终包中应收敛成一份隐藏科学参考。

### 2.6 当前 Stage07 根目录

```text
stage_07_task_audit/
├── workspaces/
├── checkpoints/
├── audited_tasks/
├── published_tasks/
├── evaluator_registry/
├── rejected_tasks/
├── audit_results.jsonl
└── stage_summary.json
```

- `workspaces/`、`checkpoints/`：Stage07 Agent 轨迹和恢复信息；
- `audited_tasks/`：含双 mode、hidden truth、审计报告的私有审计 master；
- `published_tasks/`：当前仅包含公开任务表面；
- `evaluator_registry/`：当前仅包含 evaluator 侧投影；
- `rejected_tasks/`：科学拒绝记录；
- `audit_results.jsonl`、`stage_summary.json`：逐论文和阶段汇总。

当前 `published_tasks/` 与 `evaluator_registry/` 是两棵需要人工拼接的半成品树。v8 应取消这种最终输出形式，由 Stage07 一次性组装完整任务包。

## 3. 当前产物的主要问题

### 3.1 构建记录与 runtime 文件边界不清

`task_spec.json`、路线证据、转换记录、audit manifest 和模型轨迹服务于构建/审计，不应跟随最终任务进入 benchmark。把它们混在 task 根目录会增加泄漏面、加载复杂度和维护成本。

### 3.2 公共任务与隐藏评估被拆成两个半包

当前 public bundle 缺隐藏参考，evaluator registry 缺任务指令和数据。两者都不是完整、可独立验证的任务定义。

### 3.3 旧 benchmark schema 不应反向决定新管线

当前 evaluator 依赖旧的 `TaskInfo` 和 `GroundTruth` 字段，并可能把新字段丢弃或默认成 binary。这说明 evaluator 应升级，不代表 Stage06/07 应将自己的科学合同扭曲成旧 schema。

### 3.4 三类任务没有统一身份和路由

如果继续使用扁平目录和混乱的 `task_mode`、`scientific_mode`、`evaluation_profile`，未来实验验证任务接入后会继续增加别名和 canonicalize 逻辑。

正确做法是只使用一个一等分类字段 `task_type`，其余运行和评分差异交给 adapter。

### 3.5 任务定义与运行结果容易混淆

task package 是不可变的 benchmark 输入；Agent submission、trace 和 score 是某一次 run 的输出。二者必须分开存储，不能把“评估结果”写回 task 目录。

## 4. 三类任务的统一管理模型

### 4.1 唯一一等分类字段

新任务只保留：

```text
task_type = paper_reproduction | autonomous_research | experiment_validation
```

不再为新任务同时写出：

- `task_mode`；
- `scientific_mode`；
- `mode`；
- `pathway_disclosure`；
- 由 mode 可直接推导的重复枚举。

旧任务的这些字段只由 legacy adapter 读取，不继续写进新包。

### 4.2 三类任务的关系

| task_type | 当前生产者 | 公开任务特征 | 隐藏参考特征 | benchmark adapter |
|---|---|---|---|---|
| `paper_reproduction` | Stage06A + Stage07 | 公开论文复现方法、边界和路线 | 作者结果、容差、关键结论和复现证据 | computational-science adapter，reproduction profile |
| `autonomous_research` | Stage06A + Stage06B + Stage07 | 不公开作者答案性路线；明确 autonomy scope 和必要公共边界 | 方法稳健或受约束的结果、趋势、结论和接受条件 | computational-science adapter，autonomous profile |
| `experiment_validation` | 未来的 experiment-validation 管线 | 由该管线定义实验输入、执行和报告义务 | 由该管线定义观测、接受标准和实验参考 | 独立 adapter，待该管线定型后实现 |

三类任务共享包壳和安全规则，不要求共享完全相同的科学 payload。

### 4.3 family 与 variant

同一论文科学目标产生的 reproduction/autonomous 两个任务通过稳定 ID 关联：

```json
{
  "task_id": "globally_unique_task_id",
  "task_family_id": "shared_scientific_objective_id",
  "task_type": "paper_reproduction",
  "related_task_ids": ["paired_autonomous_task_id"]
}
```

规则：

- `task_id` 全局唯一，由编排器确定性生成；
- `task_family_id` 表示共同的来源和科学目标；
- `task_type` 表示实际任务类型；
- 实验验证任务可以独立成 family，也可以在未来通过 `related_task_ids` 与计算任务关联；
- evaluator registry 路径不依赖 Agent 自拟 ID。

### 4.4 软件状态与科学决定分离

每个任务 metadata 明确：

```json
{
  "runtime_readiness": "ready | needs_software",
  "required_capabilities": [
    {"capability": "...", "preferred_software": ["..."], "required": true}
  ]
}
```

- `needs_software` 不等于 rejected；
- repository 可以发现这类任务；
- 默认调度器只运行 `ready`；
- 工具箱能力补齐后重新做 capability check，无需重建科学任务；
- 不允许因为缺软件偷偷换成外围、容易执行但不代表论文主线的任务。

## 5. Task Package v1

### 5.1 推荐目录

每个最终通过任务使用同一包壳：

```text
<task_id>/
├── task.md
├── task_info.json
├── submission_schema.json
├── data/
│   └── ... public inputs ...
├── evaluation/
│   ├── reference.json
│   └── hidden_assets/              # 可选
└── package_manifest.json
```

这是完整 task definition，但不是 evaluated Agent 的工作区。runner 必须基于公开 allowlist 物化工作区，不能把包根目录直接暴露给 Agent。

### 5.2 `task.md`

唯一的人类可读任务指令，必须完整说明：

- 科学问题；
- 可见输入；
- 模式边界与方法自由度；
- 计算/实验动作和验证义务；
- 交付文件、字段、单位和符号约定；
- 必要的停止条件或不可接受替代。

`task_info.json` 不再保存第二份任务正文。

### 5.3 `task_info.json`

只保存最小 runtime 和管理 metadata：

```json
{
  "schema_version": "researchchembench.task-info.v1",
  "task_id": "...",
  "task_family_id": "...",
  "task_type": "paper_reproduction",
  "source_id": "...",
  "title": "...",
  "category": "...",
  "tags": [],
  "runtime_readiness": "ready",
  "required_capabilities": [],
  "data": [],
  "required_deliverables": [],
  "related_task_ids": [],
  "reference_schema": "computational-science-reference.v1"
}
```

不保存：

- task 正文；
- canonical answer；
- hidden profile ID；
- prompt、模型、token 或 repair 轨迹；
- paper excerpt；
- 多套 mode 别名；
- dual-axis 权重和公式。

### 5.4 `submission_schema.json`

这是唯一机器可读的提交合同，保存：

- required files；
- structured result schema；
- 文件/字段路径；
- 单位和基础类型；
- 可公开的字段说明。

它不是第二份科学任务说明。`task.md` 负责语义，`submission_schema.json` 负责精确机器形状。Stage07 必须检查二者一致。

### 5.5 `data/`

只保存 evaluated Agent 可见的输入：

- 起始结构；
- 实验或计算输入表；
- 必要协议附件；
- 公开辅助数据。

不能包含：

- 正文/SI 全文，除非任务本身明确以该文档为公开输入且不构成答案泄漏；
- hidden truth；
- private evidence map；
- Agent prompt/response；
- Stage06/07 audit；
- 带答案性 comment 或文件名的资产。

### 5.6 `evaluation/reference.json`

它是隐藏科学评估参考的唯一 runtime 来源。对于当前两类计算任务，建议使用：

```json
{
  "schema_version": "computational-science-reference.v1",
  "task_id": "...",
  "task_type": "autonomous_research",
  "answer_items": [],
  "acceptance_profiles": [],
  "submission_bindings": [],
  "process_key_points": [],
  "final_conclusions": [],
  "critical_failures": [],
  "private_evidence": {}
}
```

职责：

- `answer_items[*].canonical_answer` 是唯一手工答案源；
- `acceptance_profiles` 引用 answer item，不重复目标答案；
- `submission_bindings` 绑定当前任务提交字段；
- `process_key_points` 是该任务特有的过程检查点；
- `final_conclusions` 是需要评价的最终科学结论；
- `private_evidence` 保存 evaluator 需要但 Agent 不可见的证据引用。

它不保存：

- `evaluation_mode`；
- `score_max`；
- 每项 `max_score`；
- dual-axis 公式；
- benchmark judge prompt。

这些都属于 benchmark policy，不属于数据合成。

### 5.7 `evaluation/hidden_assets/`

仅在评分确实需要二进制或大型隐藏参考时使用，例如隐藏谱图、参考结构或实验标准。所有文件必须被 `reference.json` 引用并进入 manifest；不允许成为无引用的垃圾目录。

### 5.8 `package_manifest.json`

由代码确定性生成，至少包含：

- package/schema 版本；
- task ID/type/family；
- 每个文件的路径、hash、大小和 visibility；
- `public_to_agent` allowlist；
- reference schema；
- assembler 版本；
- package content hash。

它可以保存最小生产版本，但不能保存完整模型轨迹。manifest 是完整性合同，不是构建日志。

## 6. 最终任务包应该保留和删除哪些当前文件

| 当前文件 | 最终处理 | 原因 |
|---|---|---|
| `task.md` | 保留并最终审计 | 唯一任务指令 |
| `task_info.json` | 精简后保留 | 统一身份、类型和 runtime metadata |
| `submission_contract.json` | 规范化为 `submission_schema.json` | 保留必要 runtime 合同，删除审计冗余 |
| `data/inputs/*` | 复制为 `data/*` | Agent 可见输入 |
| `process_rubric.json` | 不单独保留；投影到隐藏 `process_key_points` | 避免多份真源和公开 rubric 泄漏 |
| `task_spec.json` | 留在 audit master | 它是构建/科学审计合同，不是 runtime 必需 |
| `paper_route.md` | 内容并入 `task.md` 或公开 `data/protocol/` | reproduction 必须可执行，但避免重复说明 |
| `workflow_spec.json` | 默认留在 audit master | 除非它本身是 Agent 必须消费的公开机器输入 |
| `route_evidence_map.json` | 留在 audit master | 来源证据映射不属于 runtime；公开路线由白名单投影到 task.md |
| `public_manifest.json` | 删除，重新生成 package manifest | 旧 manifest 覆盖范围不完整 |
| `ground_truth_common.json` | 规范化为 `evaluation/reference.json` | 单一隐藏科学参考 |
| `private_evidence_map.json` | 必要子集进入 `reference.json.private_evidence` | 只保留 evaluator 真正需要的内容 |
| `disclosure_contract.json` | 留在 audit master | 它用于构建和审计，不用于 benchmark runtime |
| `process_rubric_*` | 删除重复投影 | 由 reference 中 Key Points 和 benchmark adapter 生成 |
| `objective_card.json`、`workflow_review.json` | 留在 audit master | 科学选择和审计 provenance |
| `construction_*`、`conversion_*` | 留在 runs | 合成记录，不进入任务 |
| `stage06_handoff.json`、`stage07_audit.json` | 留在 runs | 阶段治理和复核 |
| prompt、response、cache、checkpoint、trace | 留在 runs | 调试/复现，不进入任务 |

最终任务包应只有第 5.1 节列出的六个顶层条目，不再把“可能有用”的审计文件全部带入。

## 7. Stage07 新的最终输出

### 7.1 推荐结构

```text
stage_07_task_audit/
├── audit_records/
│   └── <paper_id>/
│       ├── audited_task_pair/
│       ├── stage07_audit.json
│       ├── mechanical_report.json
│       └── stage07b_report.json          # 可选
├── final_tasks/
│   ├── paper_reproduction/
│   │   └── <task_id>/
│   └── autonomous_research/
│       └── <task_id>/
├── rejected_tasks/
├── technical_blocked_tasks/
├── audit_results.jsonl
└── stage_summary.json
```

变化：

- `audited_tasks` 的概念保留，但统一进入 `audit_records`；
- 取消作为最终接口的 `published_tasks/` + `evaluator_registry/` 双树；
- 新增完整 `final_tasks/<task_type>/<task_id>/`；
- 科学拒绝与技术阻断分开；
- `needs_software` 任务可以进入 `final_tasks`，但 metadata 标记不可调度。

### 7.2 原子组装

Stage07 finalizer 必须：

1. 从 audited master 读取公开 mode 和唯一 hidden reference；
2. 在临时目录组装 Task Package v1；
3. 删除不在 allowlist 中的文件；
4. 生成精简 task info、submission schema、evaluation reference 和 manifest；
5. 运行 package validation；
6. 验证通过后原子 rename 到 `final_tasks`；
7. 失败则进入 `technical_blocked_tasks`，不能留下半包。

### 7.3 不回写历史运行结果

v8 代码只对新运行使用新 finalizer。以前的批次：

- 保持原样；
- 可作为 regression fixture 读取；
- 不批量补文件；
- 不重新声称为正式任务；
- 若某篇以后需要正式纳入，应在新代码上重新运行或经过独立人工策展流程。

## 8. Benchmark 的新任务仓库设计

### 8.1 目录管理

ResearchChemBench 建议使用：

```text
ResearchChemBench/tasks/
├── paper_reproduction/
│   └── <task_id>/
├── autonomous_research/
│   └── <task_id>/
├── experiment_validation/
│   └── <task_id>/
└── legacy/                          # 可选、过渡期
```

这三个一级目录是管理分类，不要求 task ID 含类型名称。`task_info.task_type` 必须与所在目录一致。

### 8.2 Repository v2

新 repository 应：

1. 递归发现 `task_info.json`；
2. 验证 package manifest 和目录身份；
3. 以 `task_id` 建全局唯一索引；
4. 支持按 `task_type`、category、tag、readiness 和 capability 筛选；
5. 返回统一 `TaskPackage` 对象，而不是散落的文件 dict；
6. 明确区分：
   - `load_public_task()`；
   - `load_submission_schema()`；
   - `load_private_reference()`；
7. 对无 adapter 或缺软件的任务返回显式不可运行原因，不静默忽略；
8. 禁止未知 reference schema 自动回退为 binary。

建议接口：

```python
list_tasks(task_type=None, readiness=None, runnable_only=False)
load_task_package(task_id)
load_public_task(task_id)
load_private_reference(task_id, evaluator_context=True)
resolve_evaluator_adapter(task_id)
```

### 8.3 Legacy 兼容

当前旧任务可以通过独立 `LegacyTaskAdapter` 暂时加载：

- 不要求本轮先迁移旧任务；
- legacy 逻辑不能污染 Task Package v1 schema；
- 新任务永远只写 v1；
- 待旧任务另行迁移后删除 legacy adapter。

### 8.4 多任务根目录

为了让不同数据管线独立生产、统一消费，repository 可支持只读 task roots：

```text
RESEARCHCHEMBENCH_TASK_ROOTS=
  /curated/tasks,
  /paper_pipeline/releases,
  /experiment_pipeline/releases
```

加载时统一建立索引并检查全局 task ID 冲突。生产环境仍建议通过 curator/installer 将已确认任务固化到主 `tasks/`；多 root 主要用于测试和审阅，不允许后加载者静默覆盖先加载者。

## 9. 公开/隐藏隔离与 runner

### 9.1 Agent 可见内容

runner 只能根据 manifest 的 `public_to_agent` allowlist 物化：

```text
workspace/
├── task.md 或生成后的 INSTRUCTIONS.md
├── data/
└── submission_schema.json          # 若选择公开给 Agent
```

`evaluation/`、`package_manifest.json` 的 private 条目和 audit records 绝不能复制进 workspace。

### 9.2 不依赖“Agent 不会去看”

安全边界必须由 runner 的文件复制策略和执行隔离保证，不能仅依赖 prompt 告诉 Agent 不要读取 Ground Truth。测试必须扫描实际 workspace，确认没有：

- `evaluation/`；
- `ground_truth`/`reference`；
- hidden assets；
- private evidence；
- Stage06/07 audit；
- source paper/SI 的答案性副本。

### 9.3 任务包不可变

benchmark run 不得回写 task package。每次执行记录 package content hash，保证评分对应固定任务版本。

## 10. 科学参考与 dual-axis 的职责划分

### 10.1 数据管线负责什么

Stage06/07 负责：

- 过程 Key Points 的内容和证据要求；
- 最终科学结论及其 canonical answer；
- 数值/排序/趋势/语义接受条件；
- submission binding；
- critical failures；
- mode/autonomy 对科学真值口径的影响。

Stage06/07 不负责：

- 采用 binary、rubric 还是 dual axis；
- 总分；
- 每项权重；
- 过程轴固定 rubric；
- 两轴组合公式；
- judge 调用和评分输出格式。

### 10.2 Benchmark 负责什么

benchmark evaluator adapter 负责：

- 选择 `dual_axis_100`；
- 加载标准研究过程 rubric；
- 将任务特定 `process_key_points` 作为证据检查清单；
- 将 `final_conclusions` 转为结论轴项目；
- 确定权重；
- 应用 evidence gates 和 critical failures；
- 生成 itemized score 和总分；
- 保存评分 provenance。

这样以后改变评分政策不需要重新合成科学任务。

### 10.3 Adapter registry

不把所有任务强塞进一个巨大 GroundTruth schema。使用 adapter registry：

```text
(task_type, reference_schema) -> evaluator adapter
```

第一阶段注册：

```text
paper_reproduction + computational-science-reference.v1
    -> ComputationalScienceDualAxisAdapter(reproduction=True)

autonomous_research + computational-science-reference.v1
    -> ComputationalScienceDualAxisAdapter(reproduction=False)
```

未来注册：

```text
experiment_validation + <future experiment reference schema>
    -> ExperimentValidationAdapter
```

若 adapter 不存在：

- 任务仍可被 catalog 发现；
- 标记 `evaluation_ready=false`；
- 禁止执行正式评分；
- 不回退成 binary；
- 不要求实验验证管线提前模仿计算任务 payload。

### 10.4 Dual-axis 转换

对于当前两个计算任务类型，benchmark adapter 可继续使用标准过程轴，并对 `final_conclusions` 做确定性权重分配。具体公式和权重由 benchmark 的版本化 policy 管理，例如：

```text
policy_id = dual_axis_100.v1
```

该 `policy_id` 写入 run/evaluation result，不写回任务科学参考。

### 10.5 禁止默认退化

以下情况必须显式失败：

- reference schema 未注册；
- final conclusions 为空；
- acceptance profile 无 binding；
- numeric binding 指向未声明字段；
- adapter 无法构造两个评分轴；
- policy 版本不存在。

不能再因为字段缺失而默认 `evaluation_mode=binary, score_max=1`。

## 11. Benchmark 运行结果如何整理

任务定义与运行结果完全分开：

```text
ResearchChemBench/results/<run_id>/
├── run.json
└── tasks/
    └── <task_id>/
        ├── run_metadata.json
        ├── submission/
        │   └── ... Agent deliverables ...
        ├── evaluation/
        │   ├── result.json
        │   └── judge_artifacts/          # 可选
        └── trace/
            └── ... execution provenance ...
```

### 11.1 `run.json`

批次级信息：模型、Agent、工具箱版本、任务筛选条件、开始/结束时间和汇总。

### 11.2 `run_metadata.json`

任务级执行信息：

- task ID/type/family；
- package hash；
- evaluator adapter 和 policy 版本；
- runtime status；
- resource/token/time 统计；
- objective infrastructure failure 分类。

### 11.3 `submission/`

Agent 的原始提交副本。评分器只读，不修改。

### 11.4 `evaluation/result.json`

统一外层，内部允许 adapter-specific details：

```json
{
  "task_id": "...",
  "task_type": "paper_reproduction",
  "status": "scored",
  "adapter_id": "computational_science_dual_axis.v1",
  "policy_id": "dual_axis_100.v1",
  "final_score": 0,
  "axes": {
    "research_process": {},
    "scientific_conclusion": {}
  },
  "gates": [],
  "diagnostics": []
}
```

实验验证 adapter 将来可以在 `axes` 或 `details` 中提供自己的项目，但必须保留统一外层的 task identity、status、score 和 provenance。

### 11.5 `trace/`

保存工具调用、托管计算和 judge provenance。是否长期保留大型 workspace 由结果保留策略决定，但不得写进 task package。

## 12. Hidden scientific truth 的简化

不引入覆盖整个 Stage06/07 的大型 `CanonicalTask`。只对隐藏科学参考建立小型单一真源：

```text
answer_items[*].canonical_answer
          │
          ├── acceptance profile 引用 answer_item_id
          ├── final conclusion 引用 answer/profile
          └── benchmark adapter 读取并生成评分上下文
```

规则：

1. acceptance profile 不重复 target value；
2. final conclusion 不另存一份 canonical answer；
3. 只写 `submission_bindings` 一套 canonical 字段；
4. mode-specific 差异在各自 task 的 reference 中显式表达，不用共享 profile 回退；
5. `expected_result` 若 scorer 需要，只在内存中由 adapter 生成；
6. Stage07A/07B 后重新验证 answer/profile/binding/conclusion 引用闭合；
7. 科学证据仍由 Agent 判断，代码只验证引用、类型、路径和 schema 事实。

## 13. Stage07A 的职责与最小 Prompt 修改

Stage07A 仍是最终科学 Judge，重点保持以下 grouped checklist：

1. **代表性**：是否优先覆盖全文计算主线；若降级，是否确为最重要核心子流程；外围但容易执行的流程不能替代论文核心问题；
2. **科学闭合**：输入、参考态、边界、计算动作、输出物理量和最终结论是否闭合；
3. **mode/GT 口径**：method-constrained 才能使用固定方法紧数值；method-discovery 使用方法稳健的排序、符号、趋势或区间；
4. **证据与绑定**：每个 answer、profile、binding 和 final conclusion 是否可由源材料支持并可从提交中判定；
5. **公开边界**：自主任务不泄漏作者路线/答案；复现任务公开足够路线但不公开目标值和结论；
6. **软件处理**：缺软件登记，不因工具箱缺口改变科学问题或直接拒绝；
7. **最终包可表达性**：科学内容是否能映射到 Task Package v1，而无需保留构建记录。

代码不新增化学死规则，只将结构/路径/schema finding 作为 observation 提供给 Agent。

## 14. Stage07B 设计

### 14.1 启用条件

只有当 Stage07A 已科学批准、没有 unresolved scientific issue，并且机械检查只剩重复的 allowlisted 技术合同问题时触发。

如果批量测试表明 Stage07A 后只有极少数偶发技术问题，Stage07B 可以不启用；如果科学批准后仍有较高比例任务只需简单结构修复即可完成 final package，则启用窄 Stage07B。

### 14.2 输入

- immutable Stage07A audit；
- audited task pair；
- exact mechanical findings；
- canonical hidden scientific reference；
- public/private asset map；
- disclosure contract；
- Task Package v1 schema。

默认不重新提供正文/SI。需要重新解释科学内容时必须停止并退回 Stage07A。

### 14.3 允许修改

- JSON 容器和基础类型；
- submission schema properties/required；
- binding JSONPath；
- comparison/projection 缺失；
- 公开 alias 和既有映射一致性；
- 相对路径和资产声明；
- 不改变语义的 reference/package 字段形状。

### 14.4 禁止修改

- 科学问题、代表性和范围；
- workflow；
- 输入文件内容；
- canonical answer、单位、容差或命题；
- evidence IDs；
- 电荷、多重度、溶剂、参考态等科学边界；
- autonomy scope；
- task type；
- answer/profile 的适用科学语义；
- 过程 Key Point 和最终结论的增删。

### 14.5 代码负责而不是 Stage07B 负责

- authoritative task ID；
- package 目录组装；
- manifest；
- route evidence 白名单投影；
- answer/profile 的确定性 runtime projection；
- benchmark dual-axis 权重和公式；
- 最终 allowlist 和 workspace 隔离。

### 14.6 science freeze

Stage07B 前后计算：

```text
objective + workflow + input hashes + boundaries +
canonical answers + tolerances + propositions + task type/autonomy scope
```

hash 变化即 repair 失败。Stage07B 最多执行一次 repair 和一次完整复检，未解决则终态为 `technical_blocked`。

## 15. 实验验证任务的接入方案

### 15.1 当前只定义接口，不定义科学 payload

由于 `data_pipeline_experiment_validation` 尚未定型，本轮不应猜测它一定具有：

- 计算化学 workflow；
- mode pair；
- numerical acceptance profile；
- 与论文任务相同的 process Key Points；
- 相同的 dual-axis 过程 rubric。

强行提前统一会让两个管线相互绑死。

### 15.2 它必须遵守的最小公共合同

未来 experiment-validation 管线只需输出同一包壳：

- `task.md`；
- 精简 `task_info.json`，其中 `task_type=experiment_validation`；
- `submission_schema.json`；
- 公开 `data/`；
- `evaluation/reference.json`，声明自己的 `schema_version`；
- `package_manifest.json`；
- 相同的 public/private visibility 规则；
- 全局唯一 task ID 和明确 runtime readiness。

### 15.3 保留扩展而不污染公共 schema

实验专有字段放入其自己的 reference schema，例如未来可能是：

```text
experiment-validation-reference.v1
```

benchmark 通过 adapter registry 加载。不要把实验字段不断塞进计算任务的 `computational-science-reference.v1`。

### 15.4 接入门槛

在实验验证管线定型后，单独完成：

1. 它的 reference schema；
2. package validator；
3. workspace materialization 测试；
4. evaluator adapter；
5. 与 benchmark policy 的映射；
6. 至少一个端到端 fixture。

在这之前，repository 可以 catalog 这类包，但应显示 `evaluation_adapter_unavailable`，不能错误评分。

## 16. 发布前确定性检查

这些检查只处理可确定的运输/合同事实，不作科学裁决。

### 16.1 身份与类型

- 目录名等于 task ID；
- task ID 全局唯一；
- task type 是三个正式枚举之一；
- 所在一级目录与 task type 一致；
- family/related task 引用存在或显式 external；
- schema version 受支持。

### 16.2 最终文件 allowlist

- 顶层只允许 Task Package v1 文件；
- 不存在 prompt、response、checkpoint、audit、source paper、SI 或 conversion record；
- 所有实际文件进入 manifest；
- manifest 中不存在悬空条目。

### 16.3 公开输入

- metadata 声明的数据路径存在；
- manifest/hash 一致；
- 相对路径安全；
- task.md 明确引用的输入存在；
- runner 物化后 public workspace 与 allowlist 完全一致。

代码只验证声明与文件关系，不判断这些资产是否在科学上足够。

### 16.4 提交合同与 binding

- required deliverables 与 submission schema 一致；
- numeric/ranking/structured binding 指向显式声明字段；
- JSONPath 可解析；
- comparison/projection 类型完整；
- 每个 acceptance profile 有合法 answer 和 binding；
- 每个 final conclusion 引用存在项；
- 不从错误 task type/mode 回退 binding。

### 16.5 隐藏与泄漏

- Agent workspace 不含 `evaluation/`；
- public 文件不出现 canonical answer、容差、GT/profile 内部 ID 或答案性 route evidence；
- reproduction 路线只公开可执行方法，不公开被评分目标；
- autonomous 公开边界与 autonomy scope 一致；
- hidden assets 只被 evaluator 读取。

### 16.6 Readiness

- `ready` 任务的 required capabilities 均可满足；
- `needs_software` 任务仍需通过其余 package checks；
- scheduler 默认跳过 `needs_software`，但 repository 和 curator UI 可显示它；
- 缺 evaluator adapter 与缺软件使用不同状态。

## 17. 代码修改计划

### Phase 0：冻结合同与基线

1. 记录当前 Git HEAD 和 dirty files；
2. 将本文件作为 v8 实施纲领；
3. 定义 `Task Package v1`、`task_info.v1` 和 `computational-science-reference.v1` schema；
4. 不修改历史 runs；
5. 不迁移旧 benchmark tasks；
6. 建立少量正/负 fixture。

### Phase 1：Stage07 final package assembler

主要范围：

- Stage07 finalization；
- package schema/validator；
- manifest builder；
- final status/summary。

修改：

1. 新增 `final_tasks/<task_type>/<task_id>`；
2. 原子组装 5 部分最终包；
3. 建立严格文件 allowlist；
4. 将 audit/provenance 留在 `audit_records`；
5. 取消新流程对 `published_tasks` + `evaluator_registry` 双树的依赖；
6. 显式区分 ready、needs software、rejected、technical blocked。

### Phase 2：隐藏科学参考收敛

1. `canonical_answer` 只保留一份；
2. acceptance profile 改为引用 answer item；
3. binding 只写一套 canonical 表示；
4. process Key Points 和 final conclusions 进入单一 reference；
5. mode-specific task 各自生成 reference，不共享错误回退；
6. 删除最终包中的重复 rubric/expected-result 投影。

### Phase 3：Benchmark Repository/Runner v2

此阶段修改 `ResearchChemBench/evaluation`，而不是继续让数据管线迁就旧代码：

1. 递归发现三类 Task Package v1；
2. 实现 `TaskPackage` 加载对象；
3. 支持 type/readiness/capability 过滤；
4. 实现 public workspace allowlist materialization；
5. 从 evaluator context 单独读取 private reference；
6. 未注册 schema 禁止运行；
7. 保留独立 legacy adapter，不污染 v1。

### Phase 4：Benchmark dual-axis adapter

1. 实现 `ComputationalScienceDualAxisAdapter`；
2. 从 process Key Points/final conclusions 生成评分上下文；
3. 由 benchmark policy 决定两轴 rubric、权重和公式；
4. 不回写 task package；
5. 统一输出第 11 节的 evaluation result；
6. 删除缺字段自动 binary fallback；
7. 完成真实 scorer smoke test。

### Phase 5：Stage07B

1. allowlisted finding router；
2. science hash/freeze；
3. 一次结构化 repair；
4. provenance diff；
5. 完整复检；
6. unresolved 显式 technical blocked。

### Phase 6：实验验证接入占位

本轮只实现：

- `experiment_validation` task type；
- adapter registry 的未注册状态；
- catalog/filter/UI 展示；
- 通用包壳 validator。

不实现实验 reference schema 和 evaluator adapter，等该数据管线定型后单独设计。

## 18. 测试计划

### 18.1 Stage07 包测试

- final package 顶层 allowlist；
- 构建记录不进入 package；
- task.md 是唯一任务正文；
- task identity/type/family 一致；
- manifest/hash 一致；
- ready/needs software 正确区分；
- 半包不会进入 final tasks；
- 历史 runs 未被改写。

### 18.2 Reference 合同测试

- answer 单一真源；
- profile 不重复 target；
- binding/schema/path 闭合；
- process Key Points 和 final conclusions 非空且引用有效；
- reproduction/autonomous 不互相错误套用 profile；
- adapter round-trip 不丢字段。

### 18.3 Benchmark 安全测试

- repository 发现三类目录；
- task ID 冲突阻断；
- runner workspace 只有 public allowlist；
- private reference 和 hidden assets 不可见；
- run 不修改 task package；
- unknown adapter 不回退 binary；
- `needs_software` 默认不调度；
- legacy loader 与 v1 loader 隔离。

### 18.4 Dual-axis 端到端测试

至少选择一个 reproduction 和一个 autonomous fixture：

1. repository load；
2. runner 物化 workspace；
3. mock Agent 生成 submission；
4. submission schema validate；
5. adapter 构造 process/conclusion 两轴；
6. scorer 输出 itemized axes 和 final score；
7. result 记录 adapter/policy/package hash；
8. 断言没有 binary fallback。

### 18.5 真实模型测试

代码与单测通过后，继续采用已验证较好的组合：

- Stage06A/06B：`deepseek-v4-pro-0813`；
- Stage07A：`gpt-5.6-sol`；
- Stage07B：若启用，先使用 `gpt-5.6-sol`；
- high reasoning；
- Codex harness；
- 随机 10 篇，并发 10。

重点检查：

- 该拒绝的是否正确拒绝；
- 通过任务是否真正代表全文主线或最核心子过程；
- `needs_software` 是否只登记不拒绝；
- final task 是否无构建垃圾和答案泄漏；
- reference 是否能判定 submission；
- Stage07B 是否只修技术合同；
- benchmark 能否真实运行并输出 dual-axis 结果。

## 19. Git 与实施记录

当前工作树可能包含用户其他修改。实施时：

1. 记录 baseline HEAD；
2. 不 reset、覆盖或提交无关 dirty changes；
3. 每个 Phase 使用独立小提交；
4. 每次提交只审查本 Phase 文件；
5. 在 `docs/stage0607_v8/` 记录 commit、测试、问题和剩余风险；
6. schema 变更和 migration 分开提交；
7. 旧任务 legacy 支持与新 v1 代码分开测试。

建议提交序列：

```text
v8-01 define task-package-v1 contracts
v8-02 assemble clean stage07 final tasks
v8-03 consolidate computational scientific reference
v8-04 add benchmark repository and runner v2
v8-05 add benchmark dual-axis adapter and result layout
v8-06 add bounded stage07b contract repair
v8-07 regression and 10-paper integration report
```

## 20. Ready 验收标准

只有同时满足以下条件，才宣布 Stage06/07 与 benchmark 接口 ready：

1. Stage07 final task 只有 Task Package v1 允许的文件；
2. 合成、转换、审计、prompt、response 和 source records 全部留在 runs；
3. `task.md` 是唯一任务指令；
4. task ID/type/family 可确定、无别名漂移；
5. reproduction/autonomous 两类 reference 可以完整表达过程 Key Points、答案、接受条件、binding 和最终结论；
6. canonical answer 没有多份手工副本；
7. ready 与 needs software 分离，缺软件不导致科学拒绝；
8. package manifest 和公开/隐藏分类通过；
9. runner 实际 workspace 不含任何隐藏参考；
10. benchmark repository 能按三类 task type 管理和筛选；
11. 实验验证类型可以被 catalog，但在 adapter 未实现时不会被错误运行；
12. computational adapter 能将任务参考转换成 dual-axis 评分上下文；
13. 评分策略、权重和公式只存在于 benchmark policy；
14. scorer 不再静默回退 binary；
15. 运行结果存放在 results，不回写 tasks；
16. Stage07B 若启用，不改变 science hash；
17. scientific reject、technical blocked、needs software 和 retryable failure 都可观察；
18. 没有论文、分子、固定数值或软件特例；
19. 历史测试结果和 Stage00–05 数据未被改写；
20. 随机模型回归中没有重复的共性代码 bug 或合同设计错误。

## 21. 最终实施建议

推荐顺序不是“先迁移旧 benchmark”，而是：

1. 先冻结 Task Package v1 和 computational scientific reference；
2. 让 Stage07 只输出干净完整的 final task；
3. 收敛隐藏科学参考，修掉多份答案和 mode binding 漂移；
4. 改 benchmark repository/runner，使其消费新包并严格隔离 hidden files；
5. 在 benchmark 侧实现 dual-axis adapter 和统一结果目录；
6. 视批量技术阻断比例启用窄 Stage07B；
7. 对 experiment validation 只保留 task type、包壳和 adapter 插槽，等其管线定型后再实现专属 schema。

这一方案的核心是“任务定义优先、评估器适配、构建记录隔离、三类任务共壳但不强行同构”。它比把所有产物拼进旧 `tasks/` 更干净，也避免为了尚未定型的实验验证模式提前引入错误抽象。
