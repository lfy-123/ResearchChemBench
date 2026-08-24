# Stage06/07 v8 早期 Gate 实施日志

日期：2026-08-24
对应方案：[早期 Stage06A 预检与批量可靠性方案](STAGE06_07_V8_EARLY_STAGE06A_PREFLIGHT_AND_BATCH_RELIABILITY_FIX_PLAN_20260824.md)
状态：代码、回归测试、历史阻断样本副本回放和整体逻辑审查均已完成

## 1. 本轮目标与边界

本轮只修改 Stage06A、Stage06B、Stage07A/07B、Codex harness、通用任务合同和相关测试，不修改 Stage00–05 的筛选逻辑，也不加入论文 ID、分子名、软件名或特定化学体系规则。

完成标准不是让所有论文发布，而是：

- Stage06A、Stage06B、Stage07A 各有一次初检和最多一次同阶段修复；第二次 Gate 仍失败时写入 `bypassed_with_warnings` 并继续下游；
- 最终发布 Gate 保持严格，阶段 Gate 的 fail-open 不等于发布通过；
- Stage06A 检查至少一个原始 `claim_role=final`，代码不得根据名字、kind、rubric 或 acceptance profile 自动升级 claim；
- Stage06B 保持答案盲，只接收 reproduction public surface、公开转换包和上游 Gate warning；
- Stage07A 负责科学审计；Stage07B 只处理 allowlisted transport findings，不能重做科学审计；
- 缺少工具箱软件只登记为 `needs_software`，不成为科学拒绝；
- normalization 与 Gate 分离，最终 Gate 只读，所有确定性改写有 provenance；
- 原生 Codex resume 使用显式 session UUID；失败时回退文件恢复，不能使用并发不安全的 `--last`。

## 2. Git 基线

- 分支：`main`
- annotated baseline tag：`stage0607-v8-pre-early-gate-20260824`
- tag 指向提交：`996c4cff8e91e8110054ace28cc5d799343a087f`
- 基线提交说明：`fix(stage06): align binding prompt with package contract`
- 工作区原有 Stage00–05、toolbox 和其他文档改动均不纳入本轮提交。

说明：`6af2d6a` 是 annotated tag object 的短 ID，不是代码基线提交；本日志以 peeled commit `996c4cf` 为准。

## 3. 代码修改计划与完成状态

| 步骤 | 修改内容 | 状态 |
|---|---|---|
| A | 统一 JSON Schema path walker 与 rubric 无损容器归一化 | completed |
| B | Stage06A 窄 preflight、final claim 存在性检查、两次 Gate/fail-open | completed |
| C | Stage06B、Stage07A 两次 Gate，warning 传播与最终 Gate 严格隔离 | completed |
| D | Codex 显式 UUID native resume、paper/phase 会话隔离、文件恢复 fallback | completed |
| E | normalization provenance、最终 Gate 只读、Stage07B science freeze | completed |
| F | 通用回归、历史阻断样本副本回放、最终冗余与边界审查 | completed |

## 4. 实施记录

### 4.1 共享合同层

修改：

- `researchchembench_contracts/task_package.py`
- `researchchembench_contracts/__init__.py`
- `src/stages/stage06_task_builder/validation.py`
- `src/stages/stage07_task_judge/validation.py`

实施内容：

1. 增加唯一共享的 `schema_path_status()`，支持 `properties`、`patternProperties`、`additionalProperties`、数组 items、下标和通配路径；Stage07 不再维护第二套 walker。
2. `normalize_process_rubric()` 无损支持：
   - 顶层 list；
   - `criteria`、`items`、`rubric`、`key_points` wrapper；
   - `required_artifact`、`required_evidence`、`evidence_artifacts` 等价读取。
3. 未知非空 rubric wrapper 不再静默变成空列表，而是保留原对象并产生可见 finding。
4. evaluator dry-run 先按 `applies_to_modes` 过滤 profile；不适用于当前 mode 的 profile 只写 diagnostic，不检查该 mode 的 binding。
5. hidden Ground Truth 保留 mode-specific scope，不再无条件扩大到双模式。

边界：这些函数只解析合同形状，不判断科学值、容差、方法、论文中心性或输入是否科学完整。

### 4.2 Stage06A early Gate

修改：

- `src/stages/stage06_task_builder/stage.py`
- `src/stages/stage06_task_builder/bootstrap_task_pair.py`
- `src/stages/stage06_task_builder/prompts.py`

新增 `_stage06a_phase_gate_findings()`，只检查 Stage06A 当前有权交付的内容：

- `construction_receipt.json` 与 decision 一致；
- `workflow_review.json` 可读且满足候选合同；
- reproduction 的 `task.md`、元数据、submission、rubric、route/workflow/evidence 文件；
- `task_spec.input_assets` 所声明的公开输入文件确实存在且路径安全；
- `workflow_completeness_check.json`、`public_to_private_asset_map.json`、`toolbox_requirements.json`；
- hidden reference/private evidence map 可读且 transport ownership 闭合；
- Ground Truth 至少有一个原始 `claim_role=final`；
- reproduction 适用的 acceptance profile/binding 形状闭合。

明确不检查 autonomous surface，因为它尚未由 Stage06B 生成；科学负向 receipt 只检查负向合同，编排器预建的空目录 scaffold 不算半成品任务树。

`bootstrap_task_pair.py` 已删除“kind 名称含 final 就自动设为 final”的推断。缺 final 时 Gate 反馈 Agent，由 Agent 根据论文证据修复或保持 warning；代码不改 claim role。

### 4.3 Stage06B conversion Gate

Stage06B 使用同一个两次 Gate 执行骨架：

- explicit `needs_conversion_retry` 仍属于执行/Agent retry；
- 已交付 autonomous surface 的缺文件、JSON、mode、submission、rubric、公开输入和 forbidden artifact 属于 phase Gate；
- 第二次仍失败时 `bypassed_with_warnings`，不抛出新的 Stage06 终止异常；
- Gate 后 canonicalization 若仍发现问题，记录为 `stage06b_post_normalization_warning:*` 并继续 Stage07A。

Stage06B 输入仍不包含 hidden reference、canonical answer、正文/SI 或 private evidence。若 Stage06A fail-open，只提供一个不含答案的 `stage06a_gate_warning.json`。

### 4.4 Stage07A preflight 与最终发布 Gate

修改：

- `src/stages/stage07_task_judge/stage.py`
- `src/stages/stage07_task_judge/prompts.py`
- `src/stages/stage07_task_judge/validation.py`

Stage07A 在科学批准产物上执行结构/运输 preflight：

- 双模式最小文件树；
- hidden reference 可读；
- canonical task-pair ID；
- evaluator binding、schema 与 rubric transport closure。

第一次失败把 exact findings 反馈同一个 Stage07A 会话；第二次失败固定 fail-open，并把 status/findings 写入 response、checkpoint 和 `phase_gate_report.json`。非批准科学决定不运行该 Gate。

最终发布 Gate 保持严格且只读。生产路径顺序为：

```text
Stage07A Agent output
  -> provenance-recorded transport normalization
  -> Stage07A preflight (最多两次)
  -> audited task copy + provenance-recorded normalization
  -> read-only final mechanical Gate
  -> optional Stage07B
  -> read-only Gate + Task Package validation
```

旧的 `_synchronize_hidden_pair_identity()` 未记录写回已删除；缓存产物也统一经过 `normalize_stage07_transport_contract()`，文件前后 hash 写入 `orchestrator_normalizations.json`。

### 4.5 Codex 原生 resume

修改：

- `src/agents/harness.py`
- `src/agents/namespace_exec.py`

实现：

1. 首次 native-resume-enabled 调用不使用 `--ephemeral`；
2. 从 JSONL `thread.started` 事件提取明确 session/thread UUID；
3. 恢复命令使用 `codex exec ... resume <UUID>`，从不使用 `--last`；
4. session store 按 paper + phase 隔离：
   - Stage06：`codex_sessions/<paper>/<phase>`；
   - Stage07A：`codex_sessions/<paper>/audit_repair`；
5. mount namespace 把该目录绑定到隔离环境 `/home/agent/.codex`；
6. resume 失败时清除 session ID，使用保存的 outputs + `RECOVERY_CONTEXT.md` 做一次文件恢复；该基础设施失败不增加 Gate check 计数。

本机 `codex-cli 0.147.0` 已验证父命令 `-C`/sandbox 选项和 resume 子命令参数可解析；fake CLI smoke 验证首次 session→显式 resume 的完整调用路径。

### 4.6 Stage07B 安全修复

修改：

- `src/stages/stage07_contract_repair/stage.py`
- `src/stages/stage07_contract_repair/prompts.py`

Stage07B 仍为一次窄 Agent，不是第三次科学审计：

- 只接受 closed allowlist transport findings；
- shared binding 只有在完整的 applicable-mode matrix 存在、各行与 shared binding 归一化后等价时，才允许删除冗余 shared binding；
- matrix 缺行或不等价时 `not_eligible`/technical blocked；
- malformed/不支持的 selector 不自动改指向；
- `applies_to_modes` 在 science fingerprint 中按集合比较，避免纯顺序误报；
- canonical projection 单独冻结，不能借移动 shared/mode binding 容器静默改变答案投影；
- canonical answers、单位、容差、命题、evidence IDs、workflow、input、task.md 和 mode scope 均冻结；
- 修复后先做有 provenance 的 normalization，再运行只读 final Gate；science hash 或非 allowlisted 文件变化立即阻断。

### 4.7 死代码与重复测试清理

- 删除生产代码中已无调用的 `_task_pair_builder_transport_findings()`；其职责已被 Stage06A 窄 Gate 覆盖。
- 删除两条只为旧私有函数保留的重复回归，保留新版 Stage06A“不要求 autonomous”及 mode-specific binding 回归。
- 删除 Stage07 未记录 hidden identity 写回，统一走 normalization provenance。
- 没有引入大型 `CanonicalTask`、论文特例 Gate 或新的科学硬编码。

当前版本：

- Stage06 implementation：`v18-bounded-early-gates-native-resume-20260824`
- Stage07 implementation：`v17-bounded-preflight-read-only-gate-20260824`
- Stage06A/06B prompt：`v8-...-early-gate-20260824`
- Stage07A prompt：`v8-stage07-audit-bounded-preflight-20260824`
- Stage07B prompt：`v3-safe-binding-matrix-projection-freeze-20260824`

## 5. 自动化测试

最终命令：

```bash
python -m compileall -q src ../researchchembench_contracts

PYTHONPATH=..:. pytest -q \
  tests/test_stage0607_agents.py \
  tests/test_stage0607_v5_contracts.py \
  tests/test_stage0607_v7_round04_contracts.py \
  tests/test_stage0607_v7_round05_contracts.py \
  tests/test_stage0607_v8_task_packages.py \
  tests/test_stage0607_v8_early_gate.py \
  tests/test_stage07b_contract_repair.py \
  --maxfail=20
```

结果：`225 passed`。

覆盖重点：

- Stage06A/06B/07A 各自最多两次 Gate；
- Stage07A 第二次失败确实 warning-only；
- native resume 显式 UUID、无 `--last`/`--ephemeral`、失败 fallback；
- session store paper/phase 隔离；
- final Gate 只读；
- no-final 不自动升级；
- `patternProperties`、open/missing schema path；
- `key_points` rubric 无损；
- mode-specific `applies_to_modes`；
- Stage07B shared/matrix safety、mode set semantics、canonical projection freeze。

`git diff --check` 与 Python compileall 通过。环境未安装 ruff，因此未把 ruff 作为完成条件。

## 6. 历史被阻断任务副本回放

来源批次：

`runs/stage06-07-bulk-gpt-gpt582-concurrency20-20260824`

所有回放均使用 `TemporaryDirectory` 或只读调用；每组回放前后均计算源目录 hash，原批次没有被修改。

### 6.1 Stage06A 缺 final

以下 6 个历史 constructed 任务都得到 `stage06a_final_claim_missing`，且源文件 hash 不变：

- `paper_0bcc3a25c664788b`
- `paper_0de37d01e35c27df`
- `paper_1257710b003be407`
- `paper_13639735b154735a`
- `paper_1e3a1d290a02e5f0`
- `paper_2255608bbc69754e`

这证明缺 final 会在 Stage06A→Stage06B 之前反馈给原 Agent，而不是由 Stage07 才发现或由代码静默补写。

### 6.2 科学负向空 scaffold

以下 3 个 `scientific_not_constructible` 样本只有编排器空目录 scaffold，新 Gate finding 均为 0：

- `paper_08e12756dc70dcd5`
- `paper_0b1138e3cd28952e`
- `paper_1f32e85ed6914143`

Gate 不再把合法科学拒绝误当作半成品任务树。

### 6.3 shared binding / mode matrix

在“先 normalization、再 Stage07B 等价冗余删除、再只读 Gate”的真实顺序下：

| 样本 | 结果 | science hash |
|---|---|---|
| `paper_1255ed42fa7e12ff` | 7 个 shared rows 可安全删除，Gate failed→passed | unchanged |
| `paper_1bcf80caf9e64d55` | 11 个 shared rows 可安全删除，Gate failed→passed | unchanged |
| `paper_2aca1dd116799b28` | 5 个 shared rows 可安全删除，Gate failed→passed | unchanged |
| `paper_2f2aa11ea61a32bb` | 4 个 shared rows 可安全删除，Gate failed→passed | unchanged |
| `paper_0ab98c52d856f757` | 2 个 rows 的 matrix 不完整/不等价，保持 failed | unchanged |
| `paper_0dc85595cab7bc0a` | 4 个 rows 的 matrix 不完整/不等价，保持 failed | unchanged |

前四项证明 Stage07B 可以处理可证明安全的冗余合同；后两项证明它不会为了提高发布率而越过科学/语义边界。

### 6.4 schema walker 与 rubric

- `paper_084ee9610f1503dd`：旧 32 项 binding/schema finding 降为 24 项；`patternProperties` 已正确接受动态 asset key。剩余 24 项对应 `singlet_states[*]` 内部数值字段确实没有显式声明，不是 dynamic-key 误报。
- `paper_2add3fc3e8afd205`：reproduction/autonomous 的 rubric 都从 3 项保持为 3 项，不再因 `key_points` wrapper 清空；剩余 comparison/route-evidence finding 是独立真实合同缺口。

## 7. 最终整体逻辑审查

- [x] Stage06A、Stage06B、Stage07A Gate 最多检查两次；
- [x] 第一次失败反馈同一阶段；第二次失败可见告警并继续下游；
- [x] fail-open 不跳过最终严格发布 Gate；
- [x] scientific rejection、Agent execution failure、gate bypass、Stage07B unresolved、final mechanical block 状态可区分；
- [x] Stage06A 保留 `claim_role=final` 检查且不自动升级；
- [x] Stage06B 未获得 hidden/source-material 访问权；
- [x] Stage07A 仍负责科学审计，代码 Gate 不解释论文科学内容；
- [x] Stage07B 仅在 allowlist 内修改合同，答案/容差/projection/mode scope/input/workflow 均冻结；
- [x] 缺软件只登记，不科学拒绝；
- [x] normalization 有 provenance，最终 Gate 回放前后文件 hash 一致；
- [x] Codex resume 使用显式 UUID，失败 fallback 不增加 Gate 次数；
- [x] 没有论文 ID、特定分子、特定软件或关键词版科学规则；
- [x] 历史任务只在临时副本回放，原结果未覆盖；
- [x] 只准备提交本轮相关文件，保留基线 tag。

## 8. 本轮未做事项

- 没有要求所有历史阻断任务变成 published；真实不闭合合同继续阻断。
- 没有启动新模型批次；用户本轮指定使用之前被阻断任务测试，因此采用历史产物副本回放。
- 没有引入大型 canonical object 重构或新增评分政策。
- 没有修改 Stage00–05、toolbox 或实验验证数据管线。
