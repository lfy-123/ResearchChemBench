# Stage06/07 v26 代码修改计划与实施记录

## 1. 实施目标

本轮按照
`STAGE06_07_V26_STAGE07_SCIENTIFIC_CONTRACT_CLOSURE_MODIFICATION_PLAN.md` 实施。核心目标是让 Stage07 对
Stage06 已存在模式完成逐模式的科学合同闭环审计，并在不改变 scientific objective 的前提下修复：

```text
公开任务要求
→ 合法完成/失败结果
→ submission schema
→ evaluator reference/rule
→ 唯一科学对象
```

Stage06 只增加生成约束；Common Gate 只增加标准 JSON Schema 分支解析；release、receipt、模式和文件布局不变。

## 2. 修改步骤

### 步骤 1：更新 Stage06 Prompt

修改 `src/stages/stage06_task_builder/prompts.py`：

1. 版本升级为 v26；
2. 明确 task.md 允许的成功、部分发现、bounded failure 和替代验证结果都必须能由 schema 诚实表达；
3. 固定体系特定 rule 必须唯一绑定；开放候选数组保留 candidate identity 和逐候选验证；
4. reproduction/autonomous evaluator 分别从各自公开问题推导，禁止无条件复制论文特定解释；
5. 不增加 Stage06 里程碑、Agent、文件、Gate 或工具预算。

### 步骤 2：重写 Stage07 Prompt 的审计方法

修改 `src/stages/stage07_task_judge/prompts.py`：

1. 版本升级为 v26；
2. 将角色明确为最终科学质量与评估合同审计员；
3. 对每个已有模式提取公开合同和合法结果；
4. 执行 task → schema 和 schema → evaluator 双向追踪；
5. 审计固定体系、开放候选、逐候选验证和论文内部标签映射；
6. 单独审计 reproduction/autonomous evaluator 公平性；
7. 同时检查答案泄露和隐藏评分要求；
8. 修复后重新阅读实际文件、运行 Gate 并最后写 receipt；
9. 保持不改 objective、不创建缺失模式、可移除不可修复模式的边界。

### 步骤 3：让 Common Gate 支持分支 schema

修改 `src/stages/phase_gate.py`：

1. 将 selector 解析扩展到 `oneOf`/`anyOf`；
2. 合并共同 properties、分支 properties 和 required chain；
3. selector 在至少一个适用分支存在且 required 时视为机械可用；
4. 多个可达 leaf 组合为通用 alternatives，复用现有 numeric leaf 分类；
5. 保持不存在字段、从未 required 和明确非数值 leaf 的阻断；
6. 不禁止 wildcard，不解析 system_id 语义，不添加论文或化学特例。

### 步骤 4：更新版本信息

修改 `src/stages/stage07_task_judge/stage.py`：

- 仅更新 implementation version；
- 不改变单次 Stage07 调用、错误收敛、单模式发布和 release 装配。

`src/agents/schemas.py`、`src/stages/stage07_task_judge/validation.py`、
`src/stages/stage07_task_judge/package.py` 和 `src/stages/evaluator_reference.py` 预期不修改。

### 步骤 5：增加定向测试

新增 `tests/test_stage0607_v26_contract_closure.py`：

1. Stage06 Prompt 包含合法结果、对象身份和分模式 evaluator 原则；
2. Stage07 Prompt 包含最终合同角色、逐模式闭环、标签审计和双向反演；
3. 成功/失败 `oneOf` schema 中的 success numeric binding 通过；
4. `anyOf` 分支 selector 通过；
5. 分支中不存在或从未 required 的 selector 阻断；
6. 分支中的明确非 numeric leaf 阻断；
7. 原有简单 schema 行为不变。

### 步骤 6：回归与静态检查

运行：

```text
python -m pytest -q tests/test_stage0607_v26_contract_closure.py
python -m pytest -q tests/test_stage0607_v19_contracts.py \
  tests/test_stage0607_v20_evidence_and_metadata.py \
  tests/test_stage0607_v22_dual_mode.py \
  tests/test_stage0607_v23_evaluator_and_finalization.py \
  tests/test_stage0607_v24_feasibility_and_release.py \
  tests/test_stage0607_v25_task_completeness.py
python -m compileall -q src
git diff --check
```

如定向回归通过，再运行完整 `tests/test_stage0607*.py`，确认没有恢复旧 Stage07B、旧 ID、兼容投影或旧目录。

### 步骤 7：方案一致性审计

逐条对照 v26 方案第 12 节，记录：

- 方案条目；
- 实际代码位置；
- 对应测试；
- 是否满足；
- 若存在偏差，原因和处理。

一致性审计通过前不启动昂贵模型回归。

### 步骤 8：十篇并发回归

固定样本：

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

固定运行要求：

- `harness=codex`；
- `model=gpt-5.6-sol`；
- Stage06/07 reasoning effort 均为 `high`；
- `max_parallel=10`；
- 使用新的 run root；
- 不复用旧 checkpoint；
- 凭据只通过环境变量注入，不写入文档、Git 或运行 manifest。

### 步骤 9：运行监督和最终质量分析

监督：

- 十个 Stage06 是否同时启动、是否一次正常结束；
- self-check、external Gate 和 Stage07 是否执行；
- Stage07 repair/rejection 是否保持 objective；
- 是否出现 technical_blocked、悬挂、额外 retry/resume 或旧阶段；
- release modes、文件隔离和 package manifest 是否正确。

逐个发布模式检查：

- task 指令与输入完整性；
- 成功/失败路径能否被 schema 表达；
- 过程关键点和最终结论是否充足；
- evaluator binding 是否唯一且逐对象；
- autonomous 是否存在作者路线或隐藏评分要求；
- 公开面是否泄露参考答案；
- Stage07 是否发现并修复本轮问题；
- 是否出现新的科学或工程问题。

## 3. Git 管理

采用小步提交：

1. v26 方案与代码计划文档；
2. Prompt 与版本修改；
3. branch-aware Gate 与定向测试；
4. 实施日志和最终分析文档。

只提交本任务修改的文件，不纳入工作区中既有 Stage00–05、toolbox 或其他用户修改。

## 4. 实施记录

### 2026-08-27：计划建立

- 已核对 v25 当前实现、v26 方案、Stage06/07 Prompt、Common Gate selector 和 Stage07 receipt validation；
- 已确认固定十篇论文 ID；
- 已确认 v26 不改变 release layout、receipt 八维结构和单模式发布逻辑；
- 下一步：按步骤 1–5 修改代码和测试。

### 2026-08-27：代码与定向测试完成

- `src/stages/stage06_task_builder/prompts.py` 已升级为 v26，并加入 truthful-outcome、对象身份和分模式
  evaluator 约束；未增加新的 Stage06 阶段、工具或输出；
- `src/stages/stage07_task_judge/prompts.py` 已升级为 v26，加入最终合同审计角色、逐模式合同提取、
  task→schema、schema→evaluator、对象身份、公开标签、模式公平性和双向反演检查；
- `src/stages/stage07_task_judge/stage.py` 仅更新 implementation version，单次审计、单模式保留和动态
  release 流程不变；
- `src/stages/phase_gate.py` 的 schema selector 已支持标准 `oneOf`/`anyOf` 分支，并保留不存在字段、未
  required 字段和非数值 leaf 的机械阻断；未加入 wildcard 禁止、论文特例或科学语义判断；
- 新增 `tests/test_stage0607_v26_contract_closure.py`，覆盖 Prompt 合同、分支 schema、required chain、
  numeric leaf 和原有简单 schema 行为。

定向结果：

```text
python -m pytest -q tests/test_stage0607_v25_task_completeness.py \
  tests/test_stage0607_v26_contract_closure.py
17 passed
```

静态结果：`python -m compileall -q src` 通过，`git diff --check` 通过。

## 5. 方案一致性审计与回归结果

| v26 方案要求 | 代码/测试证据 | 状态 |
|---|---|---|
| Stage07 为最终科学质量与评估合同审计员 | `stage07_task_judge/prompts.py` v26 角色段；Prompt 定向测试 | 通过 |
| Task → schema 合法结果审计 | Stage07 Prompt 的 Task to schema 段；Stage06 truthful-outcome 约束 | 通过 |
| Schema → evaluator 可追溯性审计 | Stage07 Prompt 的 Schema to evaluator 段 | 通过 |
| 固定体系/开放候选身份原则 | 两个 Prompt 的对象身份段；不禁止 wildcard | 通过 |
| 论文内部标签答案中性映射 | Stage07 Prompt Public labels 段 | 通过 |
| reproduction/autonomous evaluator 分开审计 | 两个 Prompt 的 mode-specific fairness 段 | 通过 |
| 答案泄露与隐藏要求双向审计 | Stage07 Prompt reverse fairness check | 通过 |
| Stage06 不增加新职责 | Stage06 仅追加三类约束；无新阶段/文件/调用 | 通过 |
| Gate 只做机械合同 | branch-aware selector helper；无科学关键词特例 | 通过 |
| `oneOf`/`anyOf` 分支 schema 可解析 | `tests/test_stage0607_v26_contract_closure.py` | 通过 |
| 保留八个 receipt 维度、单模式和 release layout | 未修改 `schemas.py`、`validation.py`、`package.py` | 通过 |
| 不恢复 Stage07B、旧 ID、兼容投影和额外 retry | 代码 diff 与现有模块检查 | 通过 |

已知测试边界：部分 v19–v24 历史测试仍断言已删除的旧 Prompt 标题、旧版本号或旧 receipt fixture，因此
不能通过恢复旧兼容代码来解决；v26 定向测试和 v25 当前合同测试通过即可作为现行契约依据。完整 v26 回归和
十篇昂贵模型测试在下一步执行。

### 2026-08-27：十篇 gpt-5.6-sol 回归完成

运行目录：`runs/stage0607-v26-gpt-5.6-sol-20260827-ten`；模型为 `gpt-5.6-sol`，Stage06/07 推理强度均为
`high`，并发数为 10。

| paper_id | Stage06 | Stage07/终态 |
|---|---|---|
| `paper_2aca1dd116799b28` | `provisional_not_constructible` | 科学拒绝（输入闭合失败） |
| `paper_308bbee002d4560c` | `provisional_constructed` | 发布（`approved_with_repairs`） |
| `paper_30cec9ecf4782412` | `provisional_not_constructible` | 科学拒绝（输入闭合失败） |
| `paper_3590deded767345e` | 已写出科学拒绝 review | 技术阻断：缺少终态 `construction_receipt.json`，进程后续被停止 |
| `paper_611000e1de080f6f` | `provisional_constructed` | 发布（`approved_with_repairs`） |
| `paper_76ae2dc25f0a5aeb` | `provisional_not_constructible` | 科学拒绝（输入闭合失败） |
| `paper_8b7bf002cc6a4ba9` | `provisional_constructed` | 发布（`approved_with_repairs`） |
| `paper_9455a82229de2427` | `provisional_constructed` | 发布（`approved_with_repairs`） |
| `paper_9ec8c4761c4f171b` | `provisional_constructed` | 技术阻断：Stage07 修复 patch 失败，审计 Gate 未通过 |
| `paper_a5564360a31f760b` | `provisional_not_constructible` | 科学拒绝（输入闭合失败） |

统计：4 篇发布、4 篇科学拒绝、2 篇技术阻断（其中 `paper_359...` 的底层 review 是科学拒绝，但运行终态因
缺少回执记录为技术阻断）。四篇发布任务均包含两个模式、独立 `agent_input` 与
`evaluation`、私有 `paper_route.md`，且最终 external Gate 为 `passed`。四篇发布任务的 Stage07 均实际执行
了 `approved_with_repairs`，修复了 schema 分支、候选身份、过程/结论绑定或碰撞能可达性等合同缺口。

回归暴露的工程问题：科学拒绝分支的 Prompt 没有足够明确地要求始终写入终态 construction receipt，导致
`paper_359...` 在 review 已完成后仍被编排器视为运行中；Stage07 Agent 使用受限的 `rm -rf` 和脆弱的文本
patch，导致 `paper_9ec...` 无法完成本可修复的审计。两者均不应归因于科学质量或 API。
