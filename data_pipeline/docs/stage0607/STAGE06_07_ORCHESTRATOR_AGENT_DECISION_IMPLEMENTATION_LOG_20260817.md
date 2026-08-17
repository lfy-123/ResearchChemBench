# Stage06/07 编排器文件管理边界实施记录

日期：2026-08-17  
依据：`STAGE06_07_ORCHESTRATOR_AGENT_DECISION_BOUNDARY_PLAN_20260817.md`

## 实施目标

- 编排器只负责 workspace、文件、路径、hash、manifest、retry、resume 和发布管理；
- Stage06/07 Agent 独占科学通过、修复、重设计和拒绝的决策权；
- 代码发现交付问题时只能触发 objective recovery，不能生成科学裁决；
- 不为六篇测试论文增加任何论文、分子、软件或 workflow 特例；
- 完成后只用六篇中的一篇运行 `deepseek-v4-flash` 真实回归。

## 修改计划

1. 审计当前工作树和 Stage06/07 实际决策链路；
2. 删除 Stage07 post-Agent scientific gate；
3. 将 Stage07 receipt 检查收缩为文件交付事实；
4. 分离 Agent 工具箱判断与编排器库存观察，禁止覆盖 Agent 字段；
5. 将 Stage06 legacy 语义 validator 降为诊断，不再生成代码侧科学裁决；
6. 放宽 Agent transport receipt schema，只保留编排所需字段；
7. 更新回归测试并运行 ruff、py_compile 和定向 pytest；
8. 选择一篇论文用 Flash 模型运行 Stage06/07；
9. 分析 Agent 轨迹、最终决定和编排器行为并记录结论。

## Iteration 0：修改前审计

### 已确认的实际主路径

- Stage06 默认 `mode_generation_strategy=single_agent`，由一个 Agent 阅读论文、选择 workflow 并生成两个任务模式；
- Stage06 主路径没有显式传入 legacy `semantic_validator`，Agent receipt 是科学决定来源；
- Stage07 主路径由一个 audit-repair Agent 审核、修复、重设计或拒绝；
- 最近六篇真实运行中，Stage07 Agent 全部返回 `approved_with_repairs`，旧 post-Agent deterministic gate 随后将六篇全部覆盖为科学拒绝。

### 当前仍需修复的问题

- Stage07 `_approved_receipt_contract_findings()` 仍解释 `resource_status` 和高严重度 remaining issue，超出文件管理职责；
- Stage07 `_finalize_stage07_response()` 仍会重写 `toolbox_requirements.json` 并覆盖 Agent 的工具箱判断；
- `_require_reported_stage07_changes()` 会静默改写 Agent receipt，而不是让 Agent recovery 修正声明；
- Stage07 仍保留可直接执行 deterministic scientific audit 的兼容入口；
- Stage06 legacy 多阶段路径仍会把 semantic validator finding 转成 `construction_invalid`；
- Stage06/07 transport receipt schema 要求了大量非编排必需字段；
- 当前工作树包含上一轮未提交的部分修复，必须在其基础上继续，不能覆盖其他用户修改。

## 后续迭代记录

## Iteration 1：Agent 决策权与文件管理边界

### Stage06

- 默认并且唯一允许的生成策略为 `single_agent`；旧的 `legacy_multi_phase` 和
  `isolated_converter` 路径被禁用，避免旧语义 validator 覆盖 Agent 的科学判断；
- Stage05 candidate 和上游记录继续作为参考材料，Stage06 Agent receipt 是
  `constructed` 或 `scientific_not_constructible` 的科学决定来源；
- `input_assets` 同时接受 list 和 map 形式，只做语法归一化和已有文件恢复，不由代码
  创造科学输入；
- 编排器不再覆盖 Agent 已写入的 `toolbox_requirements.json`；
- 实现版本更新为
  `v5-provisional-builder-handoff-20260817-r3-agent-authority`。

### Stage07

- 删除 post-Agent scientific validator 的最终发布 gate；
- high/critical/blocking remaining issue、资源状态和工具箱状态不再触发代码侧科学改判；
- approved receipt 只检查用于定位交付树的 `artifact_path=outputs/task_pair`；
- Agent 声称修复但文件未改变时，作为 objective contract failure 交回同一 Agent recovery，
  不转换为科学拒绝；
- 编排器不再改写 Agent 的 `toolbox_requirements.json`、`toolbox_status` 或
  `required_additions`；库存匹配仅写入独立的
  `orchestrator_inventory_observation.json`，并明确标记为非权威文件管理观察；
- public-surface guard 只刷新 manifest 和 copy provenance，不改写任务正文、科学 JSON、
  输入结构文件或 rubric；
- 旧 deterministic audit 兼容入口被显式禁用；
- 实现版本更新为
  `v5-repair-first-audit-redesign-20260817-r17-file-manager`。

### 最小 transport contract

- Stage06 receipt 最低字段收缩为 `decision`、`task_pair_id`、`artifact_path`、`summary`；
- Stage07 receipt 最低字段收缩为 `audit_decision`、`artifact_path`、`summary`；
- 其他科学字段仍允许 Agent 输出并完整保留，但不作为编排器二次裁决依据。

### 自动化验证

- `PYTHONPATH=. pytest -q tests/test_stage0607_agents.py`：`116 passed`；
- `PYTHONPATH=. pytest -q tests/test_pipeline.py tests/test_late_stage_runner.py tests/test_stage_layout.py`：
  `253 passed`；
- `python -m py_compile`：通过；
- `git diff --check`：通过；
- 当前环境未安装 `ruff`，因此没有声称完成 ruff 验证。

## Iteration 2：单篇真实 Flash 回归

运行目录：

`runs/stage06-07-agent-authority-single-paper6904-20260817-r1-flash`

输入论文：`paper_6904a9c8c09855cc`，DOI `10.1002/anie.202525581`。

模型和 harness：Stage06/07 均为 `deepseek-v4-flash`，harness 为 `codex`，API 从
`config.local.env` 经 CLI 加载；没有启动另外五篇论文。

### Stage06 结果

- Agent 决定：`constructed`；编排阶段记录为 `provisional_constructed`；
- workflow：`full_paper_computational_workflow`；复杂度：`high`；
- 选取了包含几何优化、频率、单点能、G70% 自由能、过渡态/中间体和分支机理比较的
  完整 DFT workflow，而非单次计算；
- 生成了论文复现模式、由其复制并转换的自主科研模式、共享 hidden reference 以及 24
  个 SI 坐标输入；
- Agent 在第一个 bootstrap 调用中暴露了 `public_task_basis.input_assets` 的字符串/list
  形态漂移，随后在同一会话中修复并继续完成，未触发代码侧科学拒绝；
- Agent 运行记录：61 个工具调用，约 2,527,044 tokens，耗时约 371 秒。

### Stage07 结果

- Agent 决定：`approved_with_repairs`；编排阶段记录保持完全相同的决定；
- Agent 保留 Stage06 workflow，没有执行 workflow redesign；
- Agent 修复了三类小问题：补齐 `paper_info.json` 的科学问题和真实标题；移除自主模式
  中暴露的 SMD/G70% 方法路线信息；移除自主模式中带有具体计算含义的压力描述；
- Agent 判断 Gaussian 16 可用、无软件补充要求、资源策略可行、没有剩余问题；
- Agent 运行记录：79 个工具调用，约 3,114,970 tokens，耗时约 251 秒。

### 编排器边界核对

- 最终 `stage07_audit.json` 的 `audit_decision` 与 Agent 原始 receipt 一致，未出现
  `rejected_scientific_unrepairable` 覆盖；
- `orchestrator_inventory_observation.json` 标记
  `role=non_authoritative_file_management_observation`、`scientific_decision_authority=stage07_agent`、
  `versions_ignored=true`、`preset_actions_considered=false`；
- Agent 的 `toolbox_status=available` 和 `required_additions=[]` 未被库存对账覆盖；
- 编排器只生成/刷新 manifest、provenance 和观察文件，未改写任务正文、XYZ、rubric 或
  Ground Truth；
- 没有 objective recovery、没有编排器科学裁决，也没有 workflow redesign。

## Iteration 3：通用 helper schema 修复

真实轨迹暴露的 bootstrap helper 仍只遍历 list，无法直接接受方案要求的 keyed map 形式
`input_assets`。修改：

- `src/stages/stage06_task_builder/bootstrap_task_pair.py` 新增 list/map 归一化；
- 支持 map key 作为路径、map value 为 asset object 或描述字符串；
- 不为没有路径或内容的声明生成虚假科学输入；
- 新增 keyed-map 回归测试。

验证结果：

- `PYTHONPATH=. pytest -q tests/test_stage0607_agents.py`：`117 passed`；
- 合并 Stage06/07、pipeline、late-stage runner 和 layout 回归：`370 passed`；
- `python -m py_compile src/stages/stage06_task_builder/bootstrap_task_pair.py`：通过；
- `git diff --check`：通过。

该 helper 修复使用合成 map 回归测试验证；Iteration 2 的真实论文运行已证明主流程和
Agent recovery 可完成，未为样本增加任何特殊规则。其余五篇未提交、未运行。

## 当前结论与剩余风险

本轮真实运行符合“编排器只管理文件、科学决定归 Agent”的目标。Stage07 确实执行了
审计和小修复，并将 Stage06 的 provisional 结果提升为 Agent-authoritative 的
`approved_with_repairs`。

仍需关注：Stage06/07 Agent 会读取较多已生成文件，Flash 模型在单篇任务上的累计 token
消耗较高；这是上下文/Agent 行为成本，不是编排器裁决问题。后续可单独优化材料摘要和
Agent 读取策略，但不应重新加入代码侧科学 gate。

## Iteration 4：转换报告与公开任务目录边界修复（2026-08-17）

本轮针对 Pro 轨迹中出现的 `conversion_report` 只出现在最终响应、而顶层文件不存在的
情况，以及任务目录泄漏内部来源合同的问题，做了通用修复：

- Stage06B Prompt 不再要求 `conversion_receipt.json`，也不要求
  `conversion_contract.json`/`derived_from.json`/额外 manifest；只保留可选的内部
  `outputs/conversion_report.json`。
- 新增 `_normalize_converter_report()`：按“顶层文件、autonomous 子目录文件、Agent
  response 对象”的顺序恢复一份 pair-level `conversion_report.json`。这是文件合同归一化，
  不读取或裁决科学内容，因此不会替代 Agent。
- Stage06B 恢复脚本和 pair materializer 不再向 `paper_reproduction/` 或
  `autonomous_research/` 写来源合同；旧合同会被清理。
- Stage06/07 验证不再因当前模式目录缺少 `derived_from.json` 而失败；旧格式仅保留兼容读取。
- Stage07 发布包只复制评估任务需要的五类核心文件和 `data/`，不再携带
  `public_manifest.json` 或 `published_manifest.json`。
- 修正复制脚本的可写权限：任务正文仍可被编排器完成最终 materialize，非编辑资产保持只读。

验证结果：

- `PYTHONPATH=. pytest -q tests/test_stage0607_agents.py`：118 passed；
- `PYTHONPATH=. pytest -q tests/test_pipeline.py tests/test_batch_workflow.py tests/test_resume.py`：268 passed；
- `python -m compileall -q src`：通过；
- 新增转换报告从 Agent 响应或嵌套文件恢复的回归测试；
- Pro 与 GPT 同论文实测结果待本轮运行完成后追加。

## Iteration 5：本地 API 兼容性与同论文对照测试（2026-08-17）

又发现并修复两个通用运行问题：

- `config.py` 现在自动识别 `localhost`/`127.0.0.1`/`::1` API，并关闭该角色的外部代理，
  避免本地 GPT API 被误送到集群代理；远程模型仍保留原代理行为。
- `ResponsesBridge` 遇到兼容 API 对宽松 JSON Schema 返回
  `invalid_json_schema/additionalProperties` 时，只对当前终端请求回退到
  `response_format=json_object`；探索阶段的工具协议和其他模型不变。
- Stage06 在 Agent 明确 `scientific_not_constructible` 时，不再先读取成功路径的
  `workflow_review.json`，允许只有科学拒绝 receipt 的合法终止。

回归：`tests/test_stage0607_agents.py` 与 `tests/test_pipeline.py` 共 358 passed，
`compileall` 通过。

同论文（`paper_6904a9c8c09855cc`, DOI `10.1002/anie.202525581`）对照：

- Flash 旧轨迹：Stage06/07 完成，Stage07 `approved_with_repairs`；但发布包仍含
  `public_manifest/published_manifest`，且 Flash 生成的 acceptance profile 语义项为空。
- Pro 新轨迹：Stage06 成功，Stage06B 53 次工具调用后生成 pair-level
  `conversion_report.json`，没有合同重试；Stage07 71 次调用并返回
  `approved_with_repairs`。发布目录只含核心任务文件和 `data/inputs/`，不含来源合同。
- GPT `gpt-5.6-sol`：本地 API 关闭代理后可正常响应，但 Codex 轨迹中工具调用数为 0，
  Stage06 Agent 通过协议恢复返回 `scientific_not_constructible`；Stage07 同样没有可审计
  的任务文件，返回 `objective_failure_retryable`。这表明该模型/中转适配没有执行 Codex
  workspace 工具调用能力，不是 Stage06 科学规则拒绝。修复 Stage06 合法拒绝路径后，结果被
  正确记录为 `provisional_not_constructible`，没有再伪装成 filesystem failure。

完整对照、token 与剩余问题见同目录的
`STAGE06_07_REVISED_CONTRACT_TEST_REPORT_20260817.md`。
