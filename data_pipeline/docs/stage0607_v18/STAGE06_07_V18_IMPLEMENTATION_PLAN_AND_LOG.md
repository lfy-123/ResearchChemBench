# Stage06/07 v18 实施计划与修改日志

## 1. 实施原则

- 只实现已确认的 v18 方案；不引入新的兼容字段或 fallback。
- 论文唯一身份为 `paper_id`；评估内部 `key_point_id`、`conclusion_id`、`rule_id`
  保留。
- Stage06/07 不做 Agent 对话 retry；进程断点缓存只能复用完全成功且 fingerprint
  一致的结果，不恢复失败对话。
- Stage07A 是唯一模型审计/有限修复入口；删除 Stage07B。
- split evaluator 五个文件是唯一权威，不再生成或读取 legacy reference projection。
- 不修改 Stage00–05、API runner、chemistry toolbox 的既有工作。

## 2. 修改顺序

### Step 1：建立 canonical evaluator/Gate 边界

目标文件：

- `src/stages/evaluator_reference.py`
- `src/stages/stage07_task_judge/validation.py`
- `src/stages/stage07_task_judge/package.py`
- `src/stages/stage06_task_builder/validation.py`

动作：删除 legacy split↔reference 投影、stub、legacy hidden fallback；让 split 文件
直接进入 Stage07 Gate 和 package assembly；把 evaluator 完整性检查作为共同 blocking
契约；保留 tolerance 科学选择的开放性。

### Step 2：清理 Stage06

目标文件：

- `src/stages/stage06_task_builder/stage.py`
- `src/stages/stage06_task_builder/prompts.py`

动作：删除旧 multi-phase builder、旧 recovery/resume/retry、旧 Gate fallback 和
legacy strategy；固定 one-shot Stage06A/06B 流程；只保留成功 checkpoint cache；所有
身份写成 `paper_id`；删除 `phase_gate_report.json` fallback。

### Step 3：清理 Stage07

目标文件：

- `src/stages/stage07_task_judge/stage.py`
- `src/stages/stage07_task_judge/prompts.py`
- `src/stages/stage07_contract_repair/`（删除主流程、配置和测试引用，确认无调用方后移除）

动作：删除不可达旧审计、旧 retry/resume、legacy Gate、Stage07B 二次修复和二次装配；
Stage07A 一次审计/修复后只执行一次代码 Gate 和 package assembly；失败分类为科学拒绝
或技术阻断。

### Step 4：清理配置和批次终态

目标文件：

- `src/config.py`
- `config.example.json`
- `scripts/workflows/run_stage06_07_gpt_batch.py`

动作：删除 Stage06/07 retry、backoff、resume、recovery、Stage07B、legacy strategy
字段；保留 timeout、tool-call、finalization、worker、checkpoint cache 和资源策略；
科学拒绝写成 completed/scientific_rejection。

### Step 5：测试迁移

动作：

1. 新增 split canonical fixture：完整、空模板、缺 expected、缺 comparison、无效
   binding、引用断裂、科学拒绝、技术阻断、paper_id 唯一性。
2. 删除或改写依赖 task_pair_id 多重身份、legacy reference round-trip、Stage07B、
   retry/resume 和 phase_gate_report fallback 的旧测试。
3. 运行 Stage0607 定向测试，再运行相关全量测试；失败必须归因于测试契约迁移，不用
   兼容分支掩盖。

### Step 6：一致性审查与测试任务

- 用 `rg` 检查 active Stage06/07 代码不再引用旧入口、旧配置、legacy projection。
- 逐项对照 v18 修改方案和本实施日志。
- 仅提交上一轮十篇中成功合成评估任务的论文，节省 token；不提交科学不可构建论文。
- 监督每篇任务的 Stage06A、Stage06B、Stage07A、Gate、发布路径和终态，形成分析报告。

## 3. 修改日志

| 时间 | 步骤 | 状态 | 说明 |
|---|---|---|---|
| 2026-08-26 | 方案确认 | completed | 用户确认删除 Stage07B 和全部旧兼容投影 |
| 2026-08-26 | Step 1 | completed | Stage06/07 active paths now read the five split evaluator files; bootstrap no longer creates hidden/evaluator answer scaffolds. |
| 2026-08-26 | Step 2 | completed | Removed Stage07B and old retry/resume/recovery paths; Stage07 transport validation is read-only; failed Gate artifacts retain diagnostics. |
| 2026-08-26 | Step 3 | completed | Replaced obsolete tests that imported deleted compatibility APIs with canonical split-evaluator fixtures; 452 relevant tests pass. |
| 2026-08-26 | Audit | completed | Confirmed deleted Stage07B/legacy projection helpers have no production callers. Retained source parsing, input snapshot, Stage06B conversion, Stage07A audit, package assembly, and shared evaluator validation. |
| 2026-08-26 | Final cleanup | completed | Removed the Stage07B source package, stale Stage06 review/task Agent prompts, hidden-reference validators, dual-ID call signatures, and retryable Stage06/07 terminal labels. Fixed Stage07 exception paths to use the single-paper-ID signature. |
| 2026-08-26 | Batch terminal contract | completed | Batch runner now writes only `completed/published`, `completed/scientific_rejection`, or `failed/technical_blocked`; it does not inspect or schedule late-stage retries. |
| 2026-08-26 | Prompt alignment | completed | Stage06A now builds only the reproduction surface and five split evaluator files; Stage06B alone derives the autonomous surface. Removed the contradictory instruction to build autonomous content twice. |
| 2026-08-26 | Final regression | completed | Canonical Stage06/07 and batch tests: 70 passed. Pipeline integration tests: 241 passed. |
| 2026-08-26 | Receipt timing fix | completed | Agent self-check no longer requires the final `construction_receipt.json`, because the prompt writes it after self-check. The external post-write Gate still requires it. Added a regression test for this temporal boundary; the combined late-stage suite now has 312 passing tests. |
| 2026-08-26 | Superseded batch cleanup | completed | Stopped the pre-fix five-paper batch and its stale Agent processes. Its partial artifacts are retained only as defect evidence and are not treated as formal v18 results. |
| 2026-08-26 | Timeout artifact recovery | completed | The rerun exposed a one-shot gap: Stage06B wrote a Gate-passing autonomous tree but timed out before returning JSON, so Stage07 was skipped. Added a trusted, declared-file recovery receipt for this case; it performs no retry or conversation resume and still runs the external Gate and Stage07 audit. |

## 4. 验收标准

- Stage07B 不再被导入、配置启用或调用。
- `legacy_reference_from_split`、`split_legacy_reference`、compatibility stub 和
  `phase_gate_report.json` fallback 不存在于 active path。
- Stage06/07 只产生一次模型调用；失败不恢复旧对话。
- split evaluator 缺失/空模板/引用断裂/不可执行 binding 会被共同 Gate 阻断；tolerance
  具体数值不会因固定格式规则被机械阻断。
- scientific rejection 不被记为 Stage07 未运行技术失败。
- 通过任务的 reproduction/autonomous 两种 package 都使用同一个 `paper_id`。

## 7. 删除安全审计记录

本轮没有依据代码行数直接删除当前能力。审计方法是：先从 `run_stage06()`、
`run_stage07()` 和 `assemble_task_packages()` 反向追踪生产调用，再对被删除符号执行
`src/`、`scripts/`、契约包和测试的全仓引用检查。确认无生产调用、且仅服务
Stage07B、legacy hidden envelope、双向 reference projection 或失败对话恢复的函数才删除。

保留的当前能力包括：输入快照和 PDF/表格/坐标解析、Stage06A scientific review、
Stage06A/06B 一次 Agent 调用与共享 Gate、autonomous public-surface 转换、Stage07A
科学审计和白名单修复、五文件 evaluator 校验、Task Package v1 装配与 manifest/hash
校验。bootstrap 仍负责公共文件语法和真实输入复制，但不再生成任何答案或 evaluator
占位内容，避免模型把模板误认为科学结果。

最终删除复核还发现并修复了两个旧接口残留：Stage07 异常处理仍向单 `paper_id`
函数传入两个身份参数；Stage06 技术失败仍写成 `*_retryable`。二者均已改为单身份、
一次执行后的 `technical_blocked` 终态。Stage00–05 的断点续跑没有被修改。

旧测试中直接依赖已删除 API 的文件已移除或改写为 canonical fixture；Stage00–05
测试保持不变。定向 Stage06/07 测试 47 passed；排除明确旧契约测试后的相关全量测试
452 passed。
