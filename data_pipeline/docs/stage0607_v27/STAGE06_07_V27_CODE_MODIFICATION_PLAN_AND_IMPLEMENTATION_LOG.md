# Stage06/07 v27 代码修改计划与实施记录

## 1. 实施边界

本轮严格按 v27 方案实施：

- `feasibility`、`task_quality` 由 Stage06/Stage07 Agent 生成和审计；
- Stage06/Stage07 Agent 负责科学可行性和科学拒绝；
- Common Gate 不根据 feasibility/task_quality 作科学拒绝；
- Common Gate 只负责机械文件、JSON/schema、路径、安全隔离和 runtime 合同；
- 不开放 Agent 的 `rm -rf` 权限；
- 不增加 Stage08，不恢复 Stage07B、旧 ID 或兼容投影。

## 2. 代码修改步骤

### 步骤 1：Stage06 终态协议

修改 `src/stages/stage06_task_builder/prompts.py` 和 `stage.py`：

1. 明确 constructed 与 scientific_not_constructible 两个分支都必须写 `outputs/construction_receipt.json`；
2. 拒绝分支 receipt 必须与 Agent 返回对象完全一致；
3. 合法 scientific_not_constructible receipt 直接映射为 `scientific_rejection`；
4. 不要求科学拒绝分支创建普通任务/evaluator 目录；
5. Stage06 implementation version 更新为 v27。

### 步骤 2：workflow_review 状态协议

修改 Stage06/Stage07 Prompt 和 schema 校验：

1. `workflow_review.decision` 只允许 `candidate_ready` 或 `scientific_not_constructible`；
2. Stage07 不写 `audited_with_repairs` 等新 decision；
3. Stage07 修复状态只写 `audit_receipt.audit_decision`；
4. approved/approved_with_repairs 时 workflow_review 保持 `candidate_ready`；
5. receipt、workflow_review、release_modes 不一致时作为 artifact consistency technical error。

### 步骤 3：Stage07 安全修复

修改 `src/stages/stage07_task_judge/stage.py`、workspace helper 或相关工具：

1. Agent 启动前由编排器创建隔离 audited 输出目录；
2. Agent 不需要执行 `rm -rf`；
3. 提供安全 JSON 重写/增量编辑路径，减少脆弱文本 patch；
4. 修复后由 Agent 重新读取实际文件并运行 self-check；
5. 编排器重新读取 artifact，校验实际 workflow_review、audit_receipt 和 release modes；
6. 修复失败应给出明确的 `technical_blocked`，不得伪装成科学拒绝。

### 步骤 4：Common Gate 机械化

修改 `src/stages/phase_gate.py` 和 `stage07_task_judge/validation.py`：

1. 保留必须文件、目录、JSON、schema、路径和安全隔离检查；
2. 保留 evaluator 最小结构可解析性和 binding 路径存在性检查；
3. 保留 Agent-visible PDF/SI/evaluator/paper route 泄露检查；
4. 移除或降级 `feasibility_*_not_passed` 对机械 Gate 的阻断；
5. 移除或降级 `workflow_review_task_quality_not_passed:*` 对机械 Gate 的阻断；
6. workflow_review 的科学字段作为 diagnostics/审计证据保留，不由 Common Gate 重新裁决；
7. scientific_not_constructible 的拒绝包不进入普通任务 Gate。

### 步骤 5：批处理状态和并发测试

检查 `scripts/workflows/run_stage06_07_gpt_batch.py`：

1. 保持每篇论文内部 Stage06→Stage07 顺序；
2. 保持 ThreadPoolExecutor 的滚动槽位语义；
3. 某篇任务结束后立即补充等待队列中的下一篇；
4. 最终汇总仍等待所有 future 进入终态；
5. 不增加盲目 retry/resume。

## 3. 定向测试计划

新增或更新 `tests/test_stage0607_v27_terminal_gate.py`，至少覆盖：

1. scientific_not_constructible 必须有 construction receipt；
2. 合法科学拒绝不要求 task/evaluator 目录；
3. scientific rejection 被编排器正确分类；
4. Stage07 approved_with_repairs 保持 workflow_review.decision 为 candidate_ready；
5. `audited_with_repairs` 被拒绝为非法 workflow decision；
6. receipt/workflow/release_modes 不一致时技术阻断；
7. Common Gate 不因 feasibility/task_quality 科学标签失败而阻断结构完整包；
8. Common Gate 仍阻断缺文件、损坏 JSON、非法路径和 Agent-visible PDF；
9. Stage07 修复流程不需要 `rm -rf`；
10. 并发槽位在单个 future 完成后立即启动下一篇。

## 4. 验证与方案对照

代码修改完成后依次运行：

```text
python -m pytest -q tests/test_stage0607_v25_task_completeness.py tests/test_stage0607_v26_contract_closure.py tests/test_stage0607_v27_terminal_gate.py
python -m compileall -q src
git diff --check
```

然后逐条对照 v27 方案：

- Stage06 科学拒绝是否有完整终态；
- Stage07 是否只使用合法 workflow decision；
- scientific audit 是否由 Agent 承担；
- Common Gate 是否只做机械检查；
- receipt 与 artifact 是否闭合；
- 无 `rm -rf` 依赖；
- 并发是否滚动调度。

一致性对照未通过前不启动模型回归。

## 5. 十篇回归配置

固定论文：

```text
paper_2aca1dd116799b28
paper_308bbee002d4560c
paper_30cec9ecf4782412
paper_3590deded767345e
paper_611000e1de080f6f
paper_76ae2dc25f0a5aeb
paper_8b7bf002cc6a4ba9
paper_9455a82229de2427
paper_9ec8c4761c4f171b
paper_a5564360a31f760b
```

运行要求：`gpt-5.6-sol`、Stage06/07 `high`、`max_parallel=10`、原定 endpoint 和 API key 环境变量，不把 key 写入文件。

## 6. 实施记录

### 2026-08-27：v27 方案确认

已确认 feasibility/task_quality 的科学判断交给 Agent，Common Gate 不承担科学拒绝；已记录两篇 v26 技术阻断的根因和修复边界。

### 2026-08-27：代码实施与定向验证

已完成以下实现：

- Stage06 将 `scientific_not_constructible` 视为合法终态；当 Agent 已写出合法
  `workflow_review.json` 但遗漏 `construction_receipt.json` 时，编排器仅在该拒绝分支
  恢复并写入符合 schema 的终态回执，构建任务分支仍严格报告缺失回执；拒绝原因会归一化
  为对象数组，避免字符串原因破坏回执 schema。
- Stage07 在 Agent 启动前把 candidate 复制到 `outputs/audited_task`，并显式恢复该副本的
  写权限。Agent 只做增量修改，不需要 `rm -rf` 或重新复制；实现版本更新为 v27。
- Stage07 approved/approved_with_repairs 继续要求 audited artifact 的
  `workflow_review.decision == candidate_ready`，修复状态只由 `audit_receipt` 表达。
- Common Gate 将 feasibility/task_quality 的未通过状态保留为 diagnostics，不再据此科学阻断；
  但非法 `workflow_review.decision` 仍作为协议结构错误阻断，以防止 `audited_with_repairs`
  等未定义状态进入发布。
- v27 Gate fixture 补充了两种 mode、合法 `unresolved_essential_inputs` 和完整最小任务包，
  并新增非法 workflow decision 的回归断言。

定向验证结果：

```text
python -m pytest -q tests/test_stage0607_v25_task_completeness.py \
  tests/test_stage0607_v26_contract_closure.py \
  tests/test_stage0607_v27_terminal_gate.py
20 passed
python -m compileall -q src
git diff --check
```

方案对照结论：Stage06/Stage07 的科学职责仍由 Agent 承担；Common Gate 只保留机械协议、
安全隔离和 runtime 可读取性检查；receipt、workflow review 与 release mode 的状态闭合已在
编排器中落实。下一步是提交本轮范围内的代码并运行十篇、并发 10 的回归任务。
