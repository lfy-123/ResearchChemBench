# Stage06/07 v19 代码修改计划与实施记录

日期：2026-08-26  
依据：`STAGE06_07_V19_RELEASE_AND_TASK_PACKAGE_FILE_MANAGEMENT_PLAN.md`  
范围：`autonomous_research` 与 `paper_reproduction`；不设计或修改
`data_pipeline_experiment_validation` 的科学 reference。

## 1. 实施目标

1. Stage06 使用一次连续 Agent 调用：先从共同科学核心生成并自查 reproduction，再在
   同一上下文中派生并完整审查 autonomous；不保留独立 converter Agent、转换状态或
   兼容投影。
2. Stage06 Agent 自查与外部 Gate 调用同一个 v19 合同检查实现，分别写入不同报告。
3. Stage07 只审计和有限修复完整候选；不从失败候选重建任务。
4. 生成 `runs/<run_id>/release/papers/` 与
   `runs/<run_id>/release/tasks/<task_type>/<paper_id>/`。
5. benchmark runtime 以 `(task_type, paper_id)` 定位任务，只向 Agent 物化
   `agent_input/`。
6. 删除旧 Task Package、旧 ID、旧任务目录和 v19 执行路径上的兼容代码。

## 2. 修改前基线

### 2.1 五篇同样本

- `paper_2aca1dd116799b28`
- `paper_611000e1de080f6f`
- `paper_76ae2dc25f0a5aeb`
- `paper_9455a82229de2427`
- `paper_a5564360a31f760b`

历史输入继续来自既有 Stage00-05 通过样本，不修改低成本筛选阶段。

### 2.2 测试基线

修改前运行 Stage06/07 v14-v18 定向测试与 benchmark Task Package 测试：

- Stage06/07 定向能力：40 项通过；
- 旧 `test_task_package_v1.py`：13 项失败；
- 失败根因是旧测试仍生成聚合 `evaluation/reference.json`，而当前合同代码已只允许五个
  拆分 evaluator 文件，说明旧合同、测试和现行输出已经发生漂移。

因此 v19 不修补旧 v1，而是建立单一新合同并删除旧兼容路径。

### 2.3 工作区保护

工作区包含 Stage00-05、chemistry toolbox 和本地配置的既有修改。实施期间不还原、不
覆盖、不提交这些内容；每次 Git 提交只暂存 v19 明确涉及的文件。

## 3. 分步代码修改计划

### 步骤 A：建立 v19 Task Package 合同

文件范围：

- `evaluation/contracts/task_package.py`
- `evaluation/contracts/__init__.py`
- `evaluation/repository.py`
- `evaluation/execution/{workspace,runner,lifecycle}.py`
- `evaluation/scoring/{adapters,service}.py`
- CLI、Web、provenance 和 schema 中的任务选择字段
- benchmark 对应测试

实施内容：

1. 合同固定为 `agent_input/ + task_info.json + evaluation/ + package_manifest.json`。
2. 身份只使用 `paper_id` 和 `task_type`；repository 索引为 Python tuple。
3. runner 只复制 `agent_input/` 内容，不读取 manifest 来扩大公开面。
4. scorer 从同一任务包的五个 evaluation 文件加载私有参考。
5. 删除 `researchchembench_contracts/` 及 pyproject package include。
6. 删除现有旧格式 `tasks/`，不迁移、不兼容。

验收：合同、repository、runner 隔离、scoring、CLI/Web 双字段测试通过。

### 步骤 B：Stage06 直接双模式合成

文件范围：

- `src/stages/stage06_task_builder/{prompts,stage,validation}.py`
- `src/config.py`、`config.example.json`
- `src/late_stage_runner.py`

实施内容：

1. prompt 将 Agent 定义为最终任务合成者，不出现阶段编号或后续 Agent 分工。
2. 工作流固定为：科学目标 → task kind → 输入闭合 → 共同科学核心 → paper route →
   reproduction 任务/evaluator → reproduction 自查修复 → 同 Agent 派生 autonomous →
   autonomous 全公开面/evaluator 审查 → 双模式最终自查。
3. autonomous 可以复制 reproduction 的稳定科学核心和合理公开输入，但必须同步重写
   task、task_info、submission schema、文件表面和 evaluator；禁止只改 task.md 或做
   关键词 redaction。
4. 删除 converter prompt、harness、配置、receipt、retry/uncertain/audit 和调用分支。
5. 删除机械 evaluator/task 骨架；Agent 直接写完整科学内容。
6. Stage06 只输出一次 synthesis 结果和一次最终合同状态。

验收：源代码不存在独立 converter 执行路径和 conversion 状态；一次 synthesis 调用中
可以看到 reproduction 单模式自查和双模式最终自查，完整候选才能交给 Stage07。

### 步骤 C：统一 Gate

文件范围：

- `src/stages/phase_gate.py`
- `src/stages/evaluator_reference.py`
- Stage06/07 validation 与 workspace helper

实施内容：

1. 用一个 v19 validator 检查两个模式的任务文件、五个 evaluator 文件、JSON、路径、
   ID、binding、deliverable 和公开/私有目录边界。
2. `agent_self_check_report.json` 与 `external_phase_gate_report.json` 分离。
3. tolerance 科学宽严、整数/小数形式和等价单位表达只进入 diagnostics。
4. 删除 acceptance profile、mode alias、旧目录探测和旧 evaluator 投影。
5. 不使用方法关键词黑名单代替科学泄漏审计。

验收：self-check 与 external Gate 对同一 snapshot 给出相同 blocking findings。

### 步骤 D：Stage07 审计、有限修复和 release

文件范围：

- `src/stages/stage07_task_judge/{prompts,stage,validation,package}.py`
- `src/late_stage_runner.py`

实施内容：

1. Stage07 只接收 Stage06 完整候选。
2. 审计科学目标、task kind、输入角色、两模式一致性、autonomous 泄漏、reproduction
   路线完整、自包含和 evaluator/schema 对齐。
3. 仅允许来源明确且不改变科学目标的局部修复；否则拒绝。
4. 统一 Gate 通过后，把真实 audited snapshot 原子组装为 release pair。
5. 论文正文/SI 每篇只复制一次到 `release/papers/<paper_id>/`；两种任务的
   `agent_input/` 均不得包含 PDF/SI。
6. assembler 只生成 metadata、manifest 和 hash，不推断或改写科学内容。

验收：不产生半个 pair；release 不含 workspace、checkpoint、Gate 报告或构建脚本。

### 步骤 E：测试、方案审计和同样本运行

1. 新增 v19 task semantics、unified Gate、release 和 benchmark runtime fixture。
2. 运行 Stage06/07 定向测试与 benchmark runtime 测试。
3. 用 `rg` 和逐文件检查确认没有 converter、旧 ID、mode alias 或旧 package 兼容路径。
4. 按主方案第 17 节逐条填写一致性审计。
5. 使用 `gpt-5.6-sol`、reasoning `high`、并发 5 运行五篇同样本。
6. 持续检查 batch status、每篇 Stage06/07 轨迹、self/external Gate、audited snapshot、
   release pair 和科学内容。
7. 输出逐篇结果与跨样本问题归因报告。

## 4. Git 管理策略

计划拆分为以下提交，实际可在模块耦合要求下合并相邻提交：

1. `refactor(evaluation): adopt paper-scoped v19 task packages`
2. `refactor(stage06): synthesize both task modes directly`
3. `refactor(stage0607): unify gates and bounded audit`
4. `feat(stage0607): assemble isolated v19 releases`
5. `test(stage0607): verify v19 contracts and release flow`

提交前均检查 staged diff，确保没有纳入无关脏工作区内容。

## 5. 实施记录

| 项目 | 状态 | 结果 |
|---|---|---|
| 基线与方案读取 | 完成 | 五篇样本与 40 passed / 13 legacy failures 已记录 |
| v19 公共合同/runtime | 完成 | 合同迁入 `evaluation/contracts`；repository、runner、scoring、CLI/Web 改用 `paper_id + task_type`；runner 只物化 `agent_input/` |
| Stage06 直接双模式合成 | 完成 | 单次 synthesis；reproduction 先完成并单模式自查；同一 Agent 再派生 autonomous；删除 builder/converter 旧实现和旧 schema |
| 统一 Gate | 完成 | Agent 工具和 orchestrator 直接使用 `phase_gate.py` 同一实现；两种报告分离；tolerance 科学选择只诊断 |
| Stage07/release | 完成 | Stage07 仅审计和有限修复；不能重建；release 生成 paper 和两个隔离任务包；batch 汇总根 release |
| 定向测试 | 完成 | 最终组合回归 35 项通过；其中核心 Stage06/07 + late runner + Task Package 组合 28 项通过 |
| 方案一致性复核 | 完成 | 见第 6 节；没有发现需要恢复旧 converter、旧 ID 或旧 package 投影的缺口 |
| 五篇并发测试 | 待实施 | |
| 最终分析报告 | 待实施 | |

### 5.1 reproduction-first 首轮真实轨迹修正

首轮修复 workspace 权限后的五篇运行已证明主流程能够先写 reproduction，但同时暴露出
终止合同缺口：Stage06 把 `outputs/construction_receipt.json` 作为结构化终止 artifact，
而 prompt 没有明确其 schema。科学拒绝样本写出的 receipt 缺少必填 `summary`，因此
`gpt-5.6-sol` 的 `required_until_artifact` 协议持续要求 shell 工具调用，模型反复执行
`find`/`json.tool` 而不能自然结束。该现象不是 Stage06 retry、resume 或 converter。

修正保持单 Agent 架构不变：

1. 明确先完整 reproduction、自查修复，再派生完整 autonomous，最后 pair self-check；
2. 明确 receipt 只能作为最后文件写入，禁止进度占位；
3. 在 prompt 中给出 constructed 与 scientific rejection 两种精确 receipt 结构；
4. receipt 必须包含 schema 要求的 `decision`、`paper_id`、`artifact_path`、`summary`；
5. 不为此恢复 Stage06B、retry 或新的编排器修复循环。

## 6. 方案一致性复核

### 6.1 Stage06

- `final_task_synthesis_instructions` 明确按 input closure → scientific core/paper route →
  完整 reproduction → reproduction Gate → 同 Agent 全公开面派生 autonomous → pair Gate
  的顺序工作。
- Stage06 只有一次 Agent 调用和一次 external Gate；不存在独立 converter harness、
  conversion receipt、conversion retry 或 uncertain 状态。
- `bootstrap_task_pair.py` 和旧 `validation.py` 已删除，代码不再生成科学模板骨架或旧
  mode/ID 投影。

### 6.2 Gate

- `phase_gate.py --mode paper_reproduction` 可在 autonomous 尚未生成时验证稳定基线；无
  `--mode` 时验证完整 pair。
- Stage06、Stage07 Agent workspace 安装的是该文件本身，external Gate 导入其
  `run()`，不存在第二套 evaluator 合同。
- 必须字段、跨文件引用、deliverable/binding/schema 和 public/private 边界会阻断；
  authored tolerance 的科学最优性只写 diagnostics。
- TaskInfo 允许字段和 release runtime 的严格结构一致，避免 self-check 通过后再因旧字段
  被 package validator 阻断。

### 6.3 Stage07 与 release

- Stage07 只接收 `handoff_ready` 的完整 Stage06 pair，并同时读取候选和不可变来源
  snapshot；没有失败候选 fallback。
- prompt 和 receipt validator 限制批准 artifact 为原候选副本上的有限修复；改变目标、
  workflow、必需输入或大规模 evaluator 重写时必须拒绝。
- assembler 只复制 audited task/schema/data/evaluator，并投影共享论文 metadata、生成
  manifest/hash；不修改科学目标或 evaluator 内容。
- PDF/SI 每篇只进入 `release/papers/<paper_id>/documents/`，两个模式的
  `agent_input/` 均禁止 PDF；任一任务包无效时 pair 不发布。

### 6.4 Benchmark runtime

- 顶层 `researchchembench_contracts` 已移除，单一合同位于 `evaluation/contracts`。
- repository 使用 `(task_type, paper_id)` tuple；TaskRunner、scoring、CLI、Web 和运行
  provenance 均显式携带两个字段，没有持久化复合 task ID。
- 旧格式 `tasks/` 已按已确认决定清空；依赖旧静态任务和旧 ground-truth 结构的测试已
  删除，由 v19 package/runtime/scoring fixture 取代。
- `run_agent_eval.sh` 和 `submit_evaluation.sh` 使用显式双字段或
  `TASK_TYPE/PAPER_ID`，不再解析旧全局 task ID。

### 6.5 尚待真实样本验证的风险

- 同一次长调用中，模型是否确实把主要精力先用于 reproduction，而不是同时铺模板；
- autonomous 的 schema、输入注释和 evaluator 是否都完成语义派生，未残留论文路线；
- Stage07 是否能发现科学目标、task kind 和 evaluator 的实质问题，而不只修机械合同；
- 五篇任务的 token/tool-call 预算是否足够完成两次自查。

这些问题无法由机械 fixture 证明，将在五篇同样本运行中通过 Agent 轨迹和逐文件科学
审计验证，并与 v18 同论文输出逐篇比较。

## 7. Git 实施记录

- `da7d260 docs(stage0607): finalize v19 synthesis and release plan`
- `5e9286d refactor(evaluation): adopt paper-scoped v19 task packages`
- `d070108 refactor(stage0607): synthesize reproduction-first v19 releases`
- experiment-validation 独立仓库参考文档：
  `8b2affc docs(reference): capture computational v19 stage design`

三个主仓库提交均使用显式路径暂存，未纳入 Stage00-05、chemistry toolbox、本地配置和
其他既有工作区修改。

## 8. 五篇运行前工程烟测

首次五并发启动在 Agent 调用前约 25 秒统一停止。五篇均为同一工程错误：不可变 Stage06
snapshot 复制后仍保留只读权限，workspace setup 随后尝试创建 `inputs/tools/`，因此触发
`PermissionError`。这批运行没有调用合成 Agent，不属于模型或新逻辑质量结果。

修复方式不是增加重试或错误标签，而是纠正 workspace 构造顺序：复制 snapshot → 仅将
workspace 副本临时改为可写 → 安装共享 Gate → 再冻结完整 inputs。新增不可变 snapshot
fixture 后，Stage06/07 + late runner + Task Package 组合 29 项通过。修复后使用新 run
目录重新提交五篇，旧失败 run 保留为工程诊断证据但不参与科学对比。
