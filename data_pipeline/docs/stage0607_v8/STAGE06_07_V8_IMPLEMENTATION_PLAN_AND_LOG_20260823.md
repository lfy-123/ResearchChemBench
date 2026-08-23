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

- [ ] `answer_items[*].canonical_answer` 成为最终包唯一手工答案源；
- [ ] acceptance profile 只引用 answer item，不重复 target；
- [ ] 只输出一套 canonical submission binding；
- [ ] process Key Points 与 final conclusions 进入 `evaluation/reference.json`；
- [ ] reproduction/autonomous 各自产生 mode-specific reference；
- [ ] expected result 和旧 evaluator projection 不进入最终包；
- [ ] validator 检查 answer/profile/binding/conclusion 引用闭合；
- [ ] 保持 Stage06/07 现有科学 Agent 所有权，不用代码发明答案。

预计修改：

- `src/stages/stage06_task_builder/stage.py`
- `src/stages/stage06_task_builder/validation.py`
- Stage07 assembler/validator
- hidden reference tests

兼容策略：Stage06 内部 audited master 可暂时保留旧 envelope；只在明确的 package projection 边界转换为 v1 reference，避免一次性重写长 Prompt 和全部 Agent schema。验证稳定后再删除确认无调用者的 legacy projection 代码。

### Phase 3：Benchmark Repository/Runner v2

计划：

- [ ] 递归发现三个 `task_type` 的 Task Package v1；
- [ ] 全局 task ID 冲突显式失败；
- [ ] 支持 type/readiness/capability/runnable 筛选；
- [ ] 返回统一 TaskPackage 描述，而不是通过 `TASKS_DIR / task_id` 猜路径；
- [ ] 分离 public task、submission schema 和 private reference 加载；
- [ ] runner 只按 manifest allowlist 物化公开工作区；
- [ ] `evaluation/` 和 hidden assets 不进入 Agent workspace；
- [ ] unknown adapter/reference schema 显式不可运行；
- [ ] 保留隔离的 legacy loader，不污染 v1 输出；
- [ ] `experiment_validation` 可被 catalog，但 adapter 未注册时不可评分。

预计修改：

- `evaluation/repository.py`
- `evaluation/settings.py`
- `evaluation/schemas/`
- `evaluation/execution/runner.py`
- `evaluation/execution/workspace.py`
- repository/runner/security tests

### Phase 4：Benchmark dual-axis adapter 与结果结构

计划：

- [ ] 新增 computational-science reference adapter；
- [ ] benchmark policy 提供过程轴 rubric、结论轴权重和组合公式；
- [ ] task-specific process Key Points 作为 judge 证据检查表；
- [ ] final conclusions 确定性映射到结论轴；
- [ ] scorer 从 adapter 取得运行时 Ground Truth，不要求 pipeline 写评分字段；
- [ ] unsupported/invalid reference 禁止静默 binary fallback；
- [ ] score/result 记录 task type、package hash、adapter ID 和 policy ID；
- [ ] task definition 与 run result 分离；
- [ ] 完成一个 reproduction 和一个 autonomous 的真实 scoring smoke。

预计修改：

- 新增 `evaluation/scoring/adapters.py` 或小型 adapter package
- `evaluation/scoring/service.py`
- `evaluation/scoring/dual_axis.py`
- `evaluation/provenance/results.py`
- evaluator schema/scoring tests

### Phase 5：窄 Stage07B

启用依据：既定 20 篇旧回归中，科学批准后存在多篇重复 binding/schema/path 技术阻断，满足 v8 触发条件。

计划：

- [ ] 定义 allowlisted technical findings；
- [ ] Stage07A 科学批准且无 unresolved science 才能进入；
- [ ] 计算 science hash；
- [ ] Stage07B 只接收 audit、exact findings、合同文件和映射；
- [ ] 最多一次 Agent repair；
- [ ] 修复后运行完整机械复检和 package assembler；
- [ ] science hash 变化立即失败；
- [ ] unresolved 明确记录为 `technical_blocked`；
- [ ] 不提供重新解释科学所需的正文/SI。

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
- hidden projection 删除 `evaluation_mode`、`score_max`、`expected_result`、profile target/canonical value 和 binding canonical projection；
- mode-specific truth/profile/binding 在投影时按适用 scope 选择；
- 只将 `claim_role=final` 的答案纳入 final conclusions，中间结果继续作为 answer/process evidence；
- 新增 readiness 状态 `approved_ready`、`approved_needs_software` 和 `technical_blocked`；
- 对旧 20 篇中的真实 approved pair `paper_ba22b36578408587` 做只读组装 smoke，两个 mode 均形成完整包；
- 测试：共享合同 `5 passed`（增加显式 schema negative case 后）；Stage06/07 v8 package tests `3 passed`；Stage06/07 相关全集 `201 passed`。

## 7. 测试与提交记录

待每个 Phase 完成后追加，至少记录：

- commit hash；
- 修改文件；
- 测试命令与结果；
- 与主方案对应条目；
- 尚未解决的问题；
- 是否改变科学语义（正常应为否，Prompt 修改需单独说明）。

## 8. 最终对照审查

尚未开始。代码完成后逐条对照主方案第 20 节 Ready 验收标准，并在此记录 passed/failed/evidence。

## 9. 20 篇模型回归结果

尚未提交。必须在代码、测试和最终对照审查完成后执行。
