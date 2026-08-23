# Stage06/07 v8 实施计划与变更日志

日期：2026-08-23

状态：实施中

方案基准：`STAGE06_07_V8_BENCHMARK_READY_OUTPUT_AND_DUAL_AXIS_IMPLEMENTATION_PLAN_20260823.md`
Git baseline：`c86de51c3a4b3ac8a83a73f4cf26af96b41d8b15`

## 1. 实施目标

本轮只围绕 v8 总方案推进：

1. Stage07 为科学批准且合同有效的任务生成精简、完整、原子的 Task Package v1；
2. 构建、转换、审计、模型调用和 source evidence 留在 `runs/`，不进入最终任务包；
3. 当前两个计算任务类型使用一份规范化隐藏科学参考；
4. ResearchChemBench repository、runner 和 evaluator 适配新包，不让数据管线迁就旧 schema；
5. 论文复现、自主科研和实验验证使用统一任务身份/发现/安全外壳，但不强制使用相同科学 payload；
6. dual-axis 的公式、权重和 judge policy 由 benchmark adapter 管理；
7. 科学批准后仍存在重复技术合同阻断时，使用一次、窄权限的 Stage07B；
8. 完成静态复审、单元测试、集成测试后，再用既定 20 篇论文执行 DeepSeek Stage06 → GPT Stage07 回归。

## 2. 不越过的边界

- 不改写历史 Stage06/07 runs；
- 不修改 Stage00–05 结果；
- 不为单篇论文增加特殊规则或 Prompt；
- 不用代码判断化学计量、参考态、量子态、溶剂或机理是否正确；
- 不让 Stage07B 改科学目标、workflow、输入、答案、容差或最终结论；
- 不读取或修改尚未定型的 `data_pipeline_experiment_validation`；
- 不提交仓库中用户已有的无关 dirty changes；
- 不把旧 benchmark task migration 设为本轮前置条件。

## 3. 基线状态

### 3.1 Git

- Repository root：`/mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench`
- Baseline commit：`c86de51c3a4b3ac8a83a73f4cf26af96b41d8b15`
- Stage06/07 源码和 `evaluation/` 在开始时无未提交修改；
- 仓库其他目录存在大量用户已有修改和未跟踪文件，本轮不触碰、不纳入提交。

### 3.2 当前实现事实

- Stage07 最终仍分别写 `published_tasks/` 和 `evaluator_registry/`；
- public bundle 与 evaluator projection 都不是独立完整任务包；
- Stage07 mechanical gate 仍包含 normalization 写回；
- benchmark repository 只发现旧扁平目录；
- runner 通过 `TASKS_DIR / task_id` 定位任务；
- scorer 直接读取旧 `GroundTruth`，字段缺失时可能进入 binary 默认值；
- 当前 batch runner 已支持 Stage06 与 Stage07 使用不同模型；
- 本轮 20 篇对照样本来自：
  `runs/stage06-07-v7-round6-deepseek-gpt20-concurrency10-20260823`。

## 4. 分阶段代码计划

### Phase 0：基线与合同

计划：

- [x] 冻结 Git baseline；
- [x] 明确 dirty worktree 边界；
- [x] 确认既定 20 篇 paper IDs 与模型组合；
- [x] 运行 Stage06/07 和 evaluator 基线测试；
- [x] 定义 Task Package v1、TaskInfo v1、SubmissionSchema v1、ComputationalScienceReference v1；
- [x] 建立不含化学特例的正/负 fixture。

预计修改：

- 新增共享 package/reference schema 模块；
- 新增本日志中的合同字段表和测试记录。

### Phase 1：Stage07 clean final task assembler

计划：

- [x] 新增 `final_tasks/<task_type>/<task_id>/`；
- [x] 从 audited pair 原子组装 `task.md`、`task_info.json`、`submission_schema.json`、`data/`、`evaluation/reference.json`、`package_manifest.json`；
- [x] 使用严格 allowlist，不复制 task spec、route evidence、audit、conversion、prompt 或 trace；
- [x] 目录名、task ID、task type、family ID 由编排器确定；
- [x] manifest 记录 hash、size、visibility 和 public workspace allowlist；
- [x] 明确 `approved_ready`、`approved_needs_software`、`technical_blocked`；
- [x] 新流程不再依赖 `published_tasks/` + `evaluator_registry/` 双树；
- [x] 组装失败不留下半包。

预计修改：

- `src/stages/stage07_task_judge/stage.py`
- `src/stages/stage07_task_judge/validation.py`
- 新增 Stage07 task package assembler/validator 模块
- Stage07 tests

### Phase 2：隐藏科学参考收敛

计划：

- [x] `answer_items[*].canonical_answer` 成为最终包唯一手工答案源；
- [x] acceptance profile 只引用 answer item，不重复 target；
- [x] 只输出一套 canonical submission binding；
- [x] process Key Points 与 final conclusions 进入 `evaluation/reference.json`；
- [x] reproduction/autonomous 各自产生 mode-specific reference；
- [x] expected result 和旧 evaluator projection 不进入最终包；
- [x] validator 检查 answer/profile/binding/conclusion 引用闭合；
- [ ] 保持 Stage06/07 现有科学 Agent 所有权，不用代码发明答案。

预计修改：

- `src/stages/stage06_task_builder/stage.py`
- `src/stages/stage06_task_builder/validation.py`
- Stage07 assembler/validator
- hidden reference tests

兼容策略：Stage06 内部 audited master 可暂时保留旧 envelope；只在明确的 package projection 边界转换为 v1 reference，避免一次性重写长 Prompt 和全部 Agent schema。验证稳定后再删除确认无调用者的 legacy projection 代码。

### Phase 3：Benchmark Repository/Runner v2

计划：

- [x] 递归发现三个 `task_type` 的 Task Package v1；
- [x] 全局 task ID 冲突显式失败；
- [x] 支持 type/readiness/capability/runnable 筛选；
- [x] 返回统一 TaskPackage 描述，而不是通过 `TASKS_DIR / task_id` 猜路径；
- [x] 分离 public task、submission schema 和 private reference 加载；
- [x] runner 只按 manifest allowlist 物化公开工作区；
- [x] `evaluation/` 和 hidden assets 不进入 Agent workspace；
- [x] unknown adapter/reference schema 显式不可运行；
- [x] 保留隔离的 legacy loader，不污染 v1 输出；
- [x] `experiment_validation` 可被 catalog，但 adapter 未注册时不可评分。

预计修改：

- `evaluation/repository.py`
- `evaluation/settings.py`
- `evaluation/schemas/`
- `evaluation/execution/runner.py`
- `evaluation/execution/workspace.py`
- repository/runner/security tests

### Phase 4：Benchmark dual-axis adapter 与结果结构

计划：

- [x] 新增 computational-science reference adapter；
- [x] benchmark policy 提供过程轴 rubric、结论轴权重和组合公式；
- [x] task-specific process Key Points 作为 judge 证据检查表；
- [x] final conclusions 确定性映射到结论轴；
- [x] scorer 从 adapter 取得运行时 Ground Truth，不要求 pipeline 写评分字段；
- [x] unsupported/invalid reference 禁止静默 binary fallback；
- [x] score/result 记录 task type、package hash、adapter ID 和 policy ID；
- [x] task definition 与 run result 分离；
- [x] 完成一个 reproduction 和一个 autonomous 的真实 scoring smoke。

预计修改：

- 新增 `evaluation/scoring/adapters.py` 或小型 adapter package
- `evaluation/scoring/service.py`
- `evaluation/scoring/dual_axis.py`
- `evaluation/provenance/results.py`
- evaluator schema/scoring tests

### Phase 5：窄 Stage07B

启用依据：既定 20 篇旧回归中，科学批准后存在多篇重复 binding/schema/path 技术阻断，满足 v8 触发条件。

计划：

- [x] 定义 allowlisted technical findings；
- [x] Stage07A 科学批准且无 unresolved science 才能进入；
- [x] 计算 science hash；
- [x] Stage07B 只接收 audit、exact findings、合同文件和映射；
- [x] 最多一次 Agent repair；
- [x] 修复后运行完整机械复检和 package assembler；
- [x] science hash 变化立即失败；
- [x] unresolved 明确记录为 `technical_blocked`；
- [x] 不提供重新解释科学所需的正文/SI。

预计修改：

- 新增 `src/stages/stage07_contract_repair/`
- `src/stages/stage07_task_judge/stage.py`
- config/model routing 和 Stage07B tests

### Phase 6：复审、清理与模型回归

计划：

- [ ] 对照 v8 主方案逐条验收；
- [ ] 搜索并删除新流程中已无调用者的双树发布/旧 projection 死代码；
- [ ] 检查 Prompt 与代码字段、终态和职责一致；
- [ ] 运行 data_pipeline 全部相关测试；
- [ ] 运行 benchmark repository/runner/scorer 测试；
- [ ] 记录每个 commit、测试和剩余风险；
- [ ] 用完全相同的 20 篇 paper IDs 提交 DeepSeek Stage06 → GPT Stage07，Codex harness，high reasoning，并发 10；
- [ ] 等待完成后逐篇检查 Stage06、Stage07、Stage07B、final task package 和终态；
- [ ] 输出最终批量 readiness 报告。

## 5. 既定 20 篇回归集合

来源批次：`stage06-07-v7-round6-deepseek-gpt20-concurrency10-20260823`

```text
paper_ba22b36578408587
paper_d489c3dc19dc32a9
paper_2aca1dd116799b28
paper_c34c2c307d7178ce
paper_3590deded767345e
paper_d82912082c8ff147
paper_9ec8c4761c4f171b
paper_8b7bf002cc6a4ba9
paper_4ee9947f568c29ba
paper_30cec9ecf4782412
paper_308bbee002d4560c
paper_76ae2dc25f0a5aeb
paper_611000e1de080f6f
paper_4cb3b70046e9cd5e
paper_a5564360a31f760b
paper_7ba8eb4d40542a94
paper_8e4994cea4744520
paper_bc9ad5e42ff1b269
paper_4f2c83d206477579
paper_9455a82229de2427
```

模型与运行约束：

- Stage06A/06B：`deepseek-v4-pro-0813`；
- Stage07A：`gpt-5.6-sol`；
- Stage07B：`gpt-5.6-sol`（若触发）；
- harness：Codex；
- reasoning effort：high；
- papers concurrency：10；
- 不把科学拒绝统计为代码失败；
- 不以发布率作为唯一成功指标。

## 6. 变更日志

### 2026-08-23：实施启动

- 冻结 baseline `c86de51c3a4b3ac8a83a73f4cf26af96b41d8b15`；
- 确认 Stage06/07 与 benchmark evaluator 起始代码无本轮未提交修改；
- 确认仓库存在大量无关 dirty changes，本轮采用逐文件 staging；
- 确认旧 Stage07 双树发布、旧 repository 定位和 binary fallback 是本轮主要工程接口问题；
- 确认 20 篇固定回归集合及 DeepSeek→GPT 模型路由。

### 2026-08-23：基线测试

- Data pipeline 命令：
  `pytest -q tests/test_stage0607_v5_contracts.py tests/test_stage0607_v7_round04_contracts.py tests/test_stage0607_v7_round05_contracts.py`
- 结果：`31 passed`；
- Benchmark 命令：
  `pytest -q tests/test_tasks.py tests/test_workspace_and_runner.py tests/test_score.py tests/test_results.py`
- 结果：`4 passed, 33 failed`；
- 33 个失败的共同前置原因是当前 34 个旧任务没有 `task.md`，旧 repository 因而发现 0 个任务，runner 随后在旧扁平路径读取 `task.md` 失败；
- 该失败在本轮开始前已经存在，不通过迁移旧任务修复。v8 将为 Task Package v1 建立独立 fixture 和 loader；legacy loader 作为隔离兼容层处理旧任务，不把旧字段带入 v1。

### 2026-08-23：Phase 0/1——Task Package v1 与 Stage07 assembler

- 新增仓库级共享合同包 `researchchembench_contracts`，供数据生产管线和 benchmark runtime 共同使用；
- 新增严格的 TaskInfo、SubmissionSchema、ComputationalScienceReference 和 PackageManifest v1 模型；
- package validator 检查身份、路径、hash、visibility、answer/profile/binding/conclusion 引用和 structured binding 的显式 JSON schema；
- package manifest 明确自排除 `package_manifest.json`，避免自哈希循环，content hash 覆盖其余全部 payload；
- Stage07 新增 clean assembler，原子写入 `final_tasks/<task_type>/<task_id>`；
- Stage07 主路径不再调用 public/evaluator 双树发布函数；
- final task 只保留 task instruction、精简 metadata、submission schema、public data、private reference 和 manifest；
- hidden projection 删除 `evaluation_mode`、`score_max`、`expected_result`、profile target/canonical value；binding 的
  `canonical_projection` 仅保留在 private `evaluation/reference.json`，不进入 public schema 或 Agent workspace，
  以便 runtime adapter 能将公开字段映射回唯一隐藏答案；
- mode-specific truth/profile/binding 在投影时按适用 scope 选择；
- 只将 `claim_role=final` 的答案纳入 final conclusions，中间结果继续作为 answer/process evidence；
- 新增 readiness 状态 `approved_ready`、`approved_needs_software` 和 `technical_blocked`；
- 对旧 20 篇中的真实 approved pair `paper_ba22b36578408587` 做过只读组装 smoke；后续
  严格启用 structured-binding schema 校验后，该 pair 暴露出 open-schema 合同缺口，
  已在 Phase 6 preflight 中记录并作为 Stage07B 回归样本，不能把旧 smoke 结果当作
  v8 package 已通过的证据；
- 测试：共享合同 `5 passed`（增加显式 schema negative case 后）；Stage06/07 v8 package tests `3 passed`；Stage06/07 相关全集 `201 passed`。

### 2026-08-23：Phase 2/3——隐藏参考投影与 Repository/Runner v2

- 新增 `evaluation/repository.py` 的 `TaskRepository` 和 `TaskPackage` 索引：递归发现 v1 包、按 `task_type`/readiness/capability/runnable 筛选、全局 task ID 冲突显式失败，并返回真实目录而不是拼接 `TASKS_DIR / task_id`。
- 新增 `RESEARCHCHEMBENCH_TASK_ROOTS` 多根配置；保留 `RESEARCHCHEMBENCH_TASKS_DIR` 作为单根兼容入口。
- v1 任务通过 `validate_task_package()` 后才能进入索引；legacy 任务只在边缘 adapter 中读取内嵌 `task_info.task` 作为 `task.md` 缺失时的回退，不会写入 v1。
- `TaskRunner` 改为使用 package descriptor，并按 `package_manifest.public_to_agent` 只物化 `task.md`、`submission_schema.json` 和 public data；`evaluation/`、manifest、task metadata 和 hidden assets 不进入 Agent workspace。
- Web API 改用 repository 的真实路径解析；不可运行任务显式返回原因。
- 运行元数据和结果摘要新增 task type、package format/content hash、reference schema 字段，任务定义与 run result 保持分离。

### 2026-08-23：Phase 4——Benchmark computational-science dual-axis adapter

- 新增 `evaluation/scoring/adapters.py`，注册 `(paper_reproduction|autonomous_research, computational-science-reference.v1)` 两个 adapter。
- adapter 将 pipeline 提供的 answer/profile/binding、process Key Points 和 final conclusions 投影为 benchmark 运行时 `dual_axis_100` GroundTruth；过程 rubric、结论权重、乘法公式由 `dual_axis_100.v1` benchmark policy 提供，不回写任务包。
- 未注册的 `experiment_validation` reference 仍可 catalog，但 `evaluation_ready=false`、禁止 Runner 执行和正式评分，不回退为 binary。
- score/result 写入 adapter ID、policy ID、task type 和 package hash；v1 score 不再把 `expected_result` 复制到公开运行结果。

### 2026-08-23：Phase 5——窄 Stage07B contract repair

- 新增 `src/stages/stage07_contract_repair/`，只接受显式 allowlist 的 evaluator/binding/path/manifest 等技术 findings；科学 finding 或未知 finding 不触发。
- Stage07A 科学批准后，机械 gate 或 package validator 仅剩 allowlisted 技术 finding
  时才尝试一次 Stage07B；Agent 无正文/SI/source packet，只能编辑合同文件，不能改
  `task.md`、data、hidden reference 科学字段、workflow、答案、容差或 mode scope。
- 以 pair science fingerprint 守护前后科学内容；非法文件改动、指纹变化、复检仍失败或 Agent 未完成均保持 `technical_blocked`，不会覆写原 audited tree。
- Stage07 summary/record 新增 `stage07b_status`、invoked/repaired/blocked 计数；Stage07 prompt 明确 Stage07B 是后续窄合同修复，不应通过科学内容迁就机械 gate。
- 测试：`PYTHONPATH=data_pipeline pytest -q data_pipeline/tests/test_stage07b_contract_repair.py` → `6 passed`；v8 package + v7 contract 回归持续通过。

### 2026-08-24：历史技术阻断回放修复（不调用模型）

本次只修改通用 transport/evaluator contract，不改 Stage00–05、不改历史 runs，也没有为任何论文加入特例规则。

- `researchchembench_contracts/task_package.py`：
  - private reference binding 增加 evaluator-only `canonical_projection`；
  - 统一有限 JSONPath filter 语法、文档 selector、legacy `observed_fields`/`target_fields` 投影和 open-schema 路径 materialization；
  - 混合 report + structured binding 只跳过文档 selector，仍检查结构化 selector；非法 filter 和 closed-schema 缺失路径继续阻断。
- `src/stages/stage07_task_judge/package.py`：
  - 旧 `workspace_artifact` 类型只在明确 package projection 边界移除并记录 diagnostic；
  - package assembly 先生成 private reference，再按已审计 binding materialize open result schema；
  - 不把 `canonical_projection` 或 audit/build 文件写入 public package。
- `src/stages/stage07_task_judge/validation.py`：
  - mechanical evaluator dry-run 与 package validator 使用同一 selector/filter 规则；
  - 修复 evaluator import path 的初始化顺序；
  - `published_bundle_mechanical_check()` 对 v1 package 改用 canonical package validator，不再要求已淘汰的 `task_spec.json` / `submission_contract.json`。
- `src/stages/stage07_task_judge/prompts.py`：明确新版 deliverable 和 structured/document binding 输出合同，禁止再生成 `type: workspace_artifact`。
- `src/stages/stage07_contract_repair/stage.py`：非法 JSONPath/filter 被标记为不支持 Stage07B 的 finding，避免窄 Agent 擅自改写科学字段映射。
- 新增/更新 v8、shared package、Stage07B 回归 fixture，覆盖 bounded/invalid filter、open schema、mixed document binding、private projection 和 v1 final bundle。

#### 六个历史技术阻断 pair 的临时目录回放

来源：`runs/stage06-07-v8-deepseek-gpt20-concurrency20-20260823`；原目录未写回。

| pair | mechanical gate | package assembly | 结论 |
|---|---|---|---|
| `paper_30cec9ecf4782412` | passed | 两种 mode 均 passed | 旧 deliverable 类型是可确定的 transport 投影，恢复可发布 |
| `paper_611000e1de080f6f` | passed | 两种 mode 均 passed | 受限 filter 记 diagnostic，不再被 package validator 误阻断 |
| `paper_76ae2dc25f0a5aeb` | passed | 两种 mode 均 passed | legacy target/selector 投影后保留 report 文档证据 |
| `paper_8b7bf002cc6a4ba9` | failed | 未组装 | shared/mode binding 歧义和 comparison 缺失，继续正确阻断 |
| `paper_9455a82229de2427` | failed | 未组装 | projection/binding 缺失且存在歧义，继续正确阻断 |
| `paper_9ec8c4761c4f171b` | failed | 未组装 | 多个适用 profile 没有 binding，Stage07B 不猜测，继续阻断 |

回放期望与实际 gate 结果 `6/6` 一致；前三个 pair 的两个 package 均通过。所有变更均为确定性运输投影或验证边界，不改变答案、容差、命题、证据或科学结论。

定向测试：

- `data_pipeline/tests/test_stage0607_v8_task_packages.py` + Stage07B/v7 contract：`29 passed`；
- `data_pipeline/tests/test_stage0607_agents.py`：`165 passed, 2 failed`。两个失败是仓库基线中缺失的 `src/stages/stage06_task_builder/bootstrap_task_pair.py`，与本轮改动无关；文档 binding 相关测试全部通过；
- `tests/test_task_package_v1.py -k 'not v1_runner'`：`12 passed`；runtime adapter smoke 已分别执行，未发现本轮合同回归。

### 2026-08-23：Phase 3/4 legacy regression

- Benchmark 回归：`pytest -q tests/test_workspace_and_runner.py tests/test_score.py tests/test_results.py tests/test_tasks.py` → `37 passed`（约 12 分钟）。
- 新 package/adapter 回归：`pytest -q tests/test_task_package_v1.py` → `12 passed`。
- 未修改 Stage00–05 代码或结果；实验验证管线目录未读取、未改写。

### 2026-08-23：Phase 6 preflight——真实 audited pair 的 package 合同闭合

对历史 approved pair
`paper_ba22b36578408587/stage_07_task_audit/audited_tasks/paper_ba22b36578408587`
做只读 Task Package v1 smoke 时发现：两个 mode 的结构化 binding 都引用
`$.energies.s1_vertical_eV`、`$.energies.t1_vertical_eV`、`$.energies.s1_emission_nm`
和 `$.energies.t1_emission_nm`，但旧 `results_schema` 只声明了 `energies` 为
`additionalProperties: true` 的开放对象。Stage07 evaluator dry-run 将其记录为
diagnostic，而新的 package validator 正确按 v8 §16.4 报告四个
`binding_schema_path_open:*` 阻断；这不是科学拒绝，也不是允许把 open schema
放行的理由。

本次代码修复：

1. 将 `binding_schema_path_open:` 纳入 Stage07B 的通用技术 finding allowlist，并在
   Stage07B prompt 中明确：只能把已有 binding 路径投影为显式 JSON Schema 属性，不能
   发明结果字段、目标值、容差或科学语义。
2. Stage07 编排器现在按以下闭环运行：
   `Stage07A → mechanical gate → package assembler →（仅 allowlisted package finding）Stage07B → mechanical gate → package assembler`。
   Stage07B 每个 pair 最多调用一次；未知 finding、修复失败或重检仍失败均保持
   `technical_blocked`，不会重启 Stage07A。
3. package 尝试在 `stage_07_task_audit/package_staging/` 私有目录完成；两个 mode
   全部验证通过后才分别原子提交到 `final_tasks/<task_type>/<task_id>/`，失败不会留下
   本次尝试的半包。
4. Stage07B 修复后再次运行 package validator，而不是只依据 evaluator dry-run 的
   `passed`；因此 open schema 这类旧合同不会被静默发布。

文件布局说明：`researchchembench_contracts/` 保持在仓库根部，作为 benchmark runtime
与 data pipeline 共用的纯合同库；`tasks/` 和 `final_tasks/` 只存任务数据包，不承载
Python 实现。把合同代码放进任务目录会让运行时依赖数据目录并破坏任务包的可移植性，
因此本轮不做那种移动。

静态检查：`git diff --check` 通过；`PYTHONPATH=. pytest -q tests/test_stage0607*.py`
为 `202 passed`；v8 package 与 Stage07B 定向测试为 `10 passed`。下一步需用真实
Stage07B harness 对上述 smoke 和固定 20 篇回归验证模型是否能完成允许的 schema
投影，然后再宣布 v8 ready。

补充回归：`pytest -q tests/test_task_package_v1.py` 为 `12 passed`；
`pytest -q tests/test_workspace_and_runner.py tests/test_score.py tests/test_results.py tests/test_tasks.py`
为 `37 passed`。一次真实 GPT Stage07B smoke 使用 Codex/Responses bridge 时遇到
本地 bridge 的连续 `502 Bad Gateway`，未修改 audited pair；该次是模型端点可用性
失败，不改变代码合同结论，批量回归仍按用户指定的 Codex harness 单独记录。

## 7. 测试与提交记录

### 2026-08-24：历史 Stage07B 产物回放更正与回归修复

上一节的六篇回放表是在完成 Stage07B artifact-row 归一化之前记录的，其中
`paper_9ec8c4761c4f171b` 被误记为“继续阻断”。本次在临时副本中重新回放，未写回
历史 runs：

- 修复 `normalize_binding_contract()` 中 artifact-row 派生分支引用未定义局部函数
  `values` 的纯代码错误；该错误只会在 reproduction/结构化 binding 触发，属于本轮
  新增回归，已加入 fixture 回归覆盖。
- 随后新增的 artifact-row 回归又发现 selector 提取顺序问题：先把
  `{path,json_path}` 压成字符串会丢失 JSONPath，可能把混合 binding 错降为
  report-only。现已改为先从原始 rows 提取 selector、再归一化 artifact path；回放中
  `paper_9ec8.../ap_definition` 的 6 个结构化 selector 和 `report/report.md` 均保留。
- Stage07B 历史产物中的
  `artifacts/artifact_paths: [{"path": ..., "json_path": ...}]` 被统一投影为合法
  `artifact_paths` + JSONPath `observed_fields`；缺失的 comparison/projection 只从
  同一 acceptance profile/answer 的既有语义复制，不生成新科学内容。
- 重新回放结果：`paper_30cec9ecf4782412`、`paper_611000e1de080f6f`、
  `paper_76ae2dc25f0a5aeb` 的 gate 和两个 mode package 均 passed；
  `paper_8b7bf002cc6a4ba9`、`paper_9455a82229de2427` 仍因 binding 歧义/缺失而
  blocked；`paper_9ec8c4761c4f171b` 的原始 audited tree 仍 blocked，但其历史
  Stage07B candidate 经归一化后 gate 与两个 mode package 均 passed。
- `canonical_projection` 只写入 private `evaluation/reference.json`，最终 public
  `submission_schema.json` 未出现该字段；非法 filter、closed-schema 缺失路径和
  多候选歧义仍保持阻断。

定向回归：v8 package + Stage07B + shared contract（排除需要外部 runner 的
`v1_runner` smoke）为 `24 passed, 3 deselected`；完整 Stage06/07 agent 集合仍有
2 个基线失败，原因是仓库缺失
`src/stages/stage06_task_builder/bootstrap_task_pair.py`，与本轮无关）。

待每个 Phase 完成后追加，至少记录：

- commit hash；
- 修改文件；
- 测试命令与结果；
- 与主方案对应条目；
- 尚未解决的问题；
- 是否改变科学语义（正常应为否，Prompt 修改需单独说明）。

### 2026-08-24：后续静态审查补丁（commit `7eca759`）

又发现并修复两处通用运输健壮性问题：

- shared `submission_binding` 使用 `artifacts`/`target_fields` 时，package assembler
  不再把 binding 误识别为空；
- `published_bundle_mechanical_check()` 被单独导入时也会显式准备 repository
  import path，不依赖 `package.py` 的导入副作用。

新增回归为 `25 passed, 3 deselected`（排除需要外部 runner 的 `v1_runner` smoke），
并完成 standalone published-bundle 调用 smoke；没有改变科学字段、答案、容差或
Stage00–05 文件。

补充：此前记录的 `165 passed, 2 failed` 来自仓库根目录执行
`data_pipeline/tests/test_stage0607_agents.py`，其中两个测试的相对脚本路径被解析
到错误的根目录。按项目约定在 `data_pipeline/` 下以 `PYTHONPATH=.` 重新执行，结果为
`167 passed`；因此这两项不属于基线代码失败。

最后一次回归发现纯 document binding 缺少结构化映射被过度放行的边界问题：只有在
binding 已经提供明确 JSONPath/`target_fields` 结构化 selector 时，才允许从同一
profile/answer 补齐 transport comparison/projection；report-only binding 缺少映射
继续阻断。修复后 Stage06/07 相关集合为 `211 passed`，六个历史 pair 的回放边界
保持不变（3 个恢复、2 个合理阻断、1 个 Stage07B candidate 通过）。

### 2026-08-24：最终 binding Prompt 合同对齐

最终静态审查发现 Stage06 Prompt 仍允许 `TSV key/column mappings`，而 Task Package v1
运行时合同只实现结构化 JSONPath selector 和显式 document binding。为避免 Agent 生成
无法执行的第三种评分绑定，本次收窄 Prompt：CSV/TSV 仍可作为辅助提交产物，但被评分的
目标必须投影到结构化 JSON 结果或明确的评分报告中。本次不新增 tabular binding schema，
不改变任何科学目标、答案、容差、模式范围或任务资产。

修改后完整 Stage06/07 回归为 `211 passed`；该修复仅消除 Prompt 对运行时不存在能力的
承诺，并保持任务输出合同精简。

## 8. 最终对照审查

代码侧已完成一次静态对照：Task Package v1 顶层 allowlist、task.md 唯一指令、
mode/type 身份、hidden reference 投影、public allowlist、runner 隔离、adapter
路由、`needs_software` 分类、Stage07B science hash 和技术阻断可见性均有对应实现
与测试。剩余待在固定 20 篇模型回归中验证的是模型实际产物，不把科学拒绝率当作代码
通过率。

## 9. 20 篇模型回归结果

已提交运行（代码 commit `082d116`）：

```text
runs/stage06-07-v8-deepseek-gpt20-concurrency20-20260823
```

模型组合为 Stage06A/06B=`deepseek-v4-pro-0813`、Stage07A/Stage07B=`gpt-5.6-sol`，
Codex harness、high reasoning、论文并发 `20`。批次于 `2026-08-23T15:29:10Z`
写入 `batch_status.json`，20 个 paper worker 均已建立；结果目录和每篇
`papers/<paper_id>/run_status.json` 由批处理器维护。首次尝试中的 paper ID 拼写错误
在参数校验阶段退出，没有生成或修改任何论文结果，随后已用上一批次 manifest 的合法
20 个 ID 重新提交。
