# final_verified_paper_reproduction 逐论文审计总结

## 2026-09-17 本批最终审查及授权迁入

新批次 17 个论文复现任务已完成最终包审查，并按负责人“检查通过后移动到 final”的明确授权迁入。本模式当前共有 **89 个 final 任务**（2026-09-27 磁盘快照；上面的历史批次迁移叙述保留）；本批 `paper_a3968806251093cd` 因历史验证对象不符，继续保留在 hold，未纳入。逐篇清单、计算支持和限定范围见[维护报告第 13 节](../verified_tasks/MAINTENANCE_REPORT.md)。

本批审查不重新认证原有 53 个任务，不代表当前公开 starter 的盲测或部署访问隔离已验证。以下退回记录、旧计数和 Stage08 决策均为历史状态，当前迁移状态以本节为准。

## 2026-09-16 新批次已退回审查区

负责人明确要求先确认调整完成，再批准迁移。本批曾提前迁入本目录的 11 个任务已完整退回 `tasks/verified_tasks/paper_reproduction/`；本轮不再将它们计为已验收/可发布。本目录恢复为原批次 53 个任务，其内容未因退回而改动。复审问题与待确认方案见 [MAINTENANCE_REPORT.md](../verified_tasks/MAINTENANCE_REPORT.md)。

> **当前目录状态（2026-09-15）**：本模式现有 **53 个 final 任务**；`6492`、`8b7`、`b815` 三包已按用户要求原样移入 [hold_verified_paper_reproduction](../hold_verified_paper_reproduction)。按 group 的补充验证指令见 [HOLD_VERIFICATION_HANDOFF.md](../HOLD_VERIFICATION_HANDOFF.md)。`84ef` 留在 final，可支持有证据的 alternative，但不能声称论文 T4-HLCT 解释已复现。发布修复背景见 [FINAL_RELEASE_REMEDIATION_REPORT.md](../FINAL_RELEASE_REMEDIATION_REPORT.md)。下面的 56 包及 Stage08 决策是迁移前历史，不是当前目录清单或发布资格。作者 endpoint 合法用于私有验证；没有 public-starter replay 本身不是失败理由。本轮不修改 `docs/verification`。

> **历史行级门禁说明（2026-09-13 更新）**：下方逐论文的 `EQUIVALENT_SAFE/HOLD` 与“文件变化”记录是 Stage08 初审快照，不是当前 final 包的发布状态。当前 final 包已经以 verified 科学字段为基线完成指令统一和质量修复；当前权威汇总见 `docs/verification/final_verified_tasks/final_verified_task_repair_report.md`，删除前哈希见 `docs/verification/final_verified_tasks/verified_source_deletion_manifest.md`。本模式 56/56 包已通过标准模式路径下的 `validate_task_package`，并已重建 manifest。旧行记录保留用于追溯，不能据此判断修复后的坐标或 TS 是否仍在 agent 输入。

审计口径：只比较原验证目录对应任务。只有输入身份、科学目标、关键评估点、evaluator 结论、schema 与可计算性均不变，且无明确作者 optimized/TS/product/final 坐标泄露时才复制。启发式标记需人工复核。

- 当前 final 已从 verified 补齐：56/56；Stage08 初审时曾暂缓 33 个，现均已按要求复制 verified 原包。暂缓原因保留在逐条记录中，供后续修复。
- `EQUIVALENT_SAFE` 仍需发布前 evaluator 语义回放。
- `paper_0dc85595cab7bc0a` 当前保留在 final，但已改用确定性扰动的中立 starter；原 SI endpoint 位于该包 `evaluation/author_results/`，其作者路线验证资格不因 starter 不同而失效；未声称当前公开 starter 已盲测通过，不要求因此重算。

### 2026-09-14 维护续审

- `paper_0de37d01e35c27df`：根据正文/SI Table S3 的 26 原子计数确认研究对象为 C10H14S2；同步修正 task、system_definition、paper_route 和 reference 中的元数据，坐标未更换，科学目标和 evaluator 数值未改。
- `paper_f9d09d28c7d9adaa`：CF3 短轴迁移缺少论文定义的轴、公式、数值和阈值，已从必需定量指标降为可选定性补充证据；HOMO/LUMO 定位与 α3/β1 扭转仍是必评。论文复现模式保留作者的定性迁移假设，但要求未评估时明确 limitation，不设置人为数值阈值。
- 其余已处理论文保持既有 verified 科学对象、输入和 evaluator；涉及作者端点坐标、身份/schema 变化或自包含性问题的任务仍按历史 HOLD/复核门禁，不作未经验证的科学改写。

## 已复制任务二次审计

当前 final 以 verified 科学字段为基线，已完成 task.md 统一和第一轮质量修复；所有目录均在临时原模式路径上通过 `validate_task_package`。已检查 `task.md`、`task_info.json`、`submission_schema.json` 和 evaluator JSON；未发现缺失输入路径或 JSON 解析错误。下方逐论文决策仍是 Stage08 历史快照，当前适用性和泄露结论以 cross-audit 报告为准。

## paper_08c040bf4e456891

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_0a62b797f51de2c0

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_0dc85595cab7bc0a

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：明确需复核 agent_input 坐标来源
- 判断：SI Table S5 optimized precursor is exposed to a mechanism-discovery task; redesign with neutral connectivity and independently generated starting geometry.

## paper_0dcba54d6a1436bd

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_0de37d01e35c27df

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_1b285cf9f763f2cf

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, evaluation/reference_key_points.json, evaluation/scoring_rules.json, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：evaluator scoring changed

## paper_221aafe4bd916a11

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：SI optimized input leakage review

## paper_2c439196c2f349c9

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_2f0a4f80a37fbccd

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json, task_info.json, 删除:agent_input/data/inputs/experimental_xray_ir_boundary.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：experimental boundary input removed

## paper_2f2aa11ea61a32bb

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：明确需复核 agent_input 坐标来源
- 判断：Input comment identifies SI optimized in-out conformer; barrier/TS task receives an author endpoint geometry. Redesign starting geometry.

## paper_2f302589e5e9e420

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, evaluation/reference_key_points.json, evaluation/scoring_rules.json, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：evaluator scoring changed

## paper_3235db287859287e

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_3316e45a74258fb7

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_36722b90a0c12825

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_3a22e838133b906d

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json, task_info.json, 删除:agent_input/data/inputs/experimental_crystal_boundary.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：experimental boundary input removed

## paper_3c058fa17fa7c54e

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_3e4cad1d1d650d0c

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_430b9cbe83c2c203

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/submission_schema.json, agent_input/task.md, evaluation/critical_failures.json, package_manifest.json, paper_route.md
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：schema/critical-failure/route changed

## paper_4e9774f4128551d3

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/structure_S20.xyz, agent_input/task.md, package_manifest.json
- 结构泄露候选：明确需复核 agent_input 坐标来源
- 判断：SI S20 is an optimized author endpoint; Stage08 also regressed the verified coordinate repair. Restore repaired input and redesign the track.

## paper_4fa592965be9841e

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_51a03695e1ccb105

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/submission_schema.json, agent_input/task.md, package_manifest.json, task_info.json, 删除:agent_input/data/inputs/azotriazole_ts2_si.xyz
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：SI TS input removed; leakage fix needs redesign

## paper_5286f393dfa5a49a

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_534ae3b6e2fb695f

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/monomers.json, agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：monomer identity changed

## paper_60f4c45810428116

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_63a9254b8e68a23c

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_641a923cbe5bbc48

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：明确需复核 agent_input 坐标来源
- 判断：SI B3LYP/optimized conformer coordinates are agent-visible in a scored conformer-energy task; use neutral independently generated starts.

## paper_6492e1e5d38d23ae

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/anatase_bulk.POSCAR, agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：POSCAR identity changed

## paper_6943bfe5eeaa42b8

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_6e09640463562644

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/submission_schema.json, agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：submission schema changed

## paper_72f60526b64ce1b6

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：明确需复核 agent_input 坐标来源
- 判断：SI Cartesian geometry provenance is ambiguous and may be the author endpoint; confirm provenance before exposing it.

## paper_84efbea3ab8e6e20

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/molecules.json, agent_input/task.md, package_manifest.json, task_info.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：molecules.json identity changed

## paper_86a0b654270a8ce7

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/complex_1.xyz, agent_input/data/inputs/complex_2.xyz, agent_input/task.md, package_manifest.json, task_info.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：stale incomplete endpoint coordinates plus leakage

## paper_8b7bf002cc6a4ba9

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_94b0a8ae694590ea

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：明确需复核 agent_input 坐标来源
- 判断：Paper route identifies supplied SI optimized standard orientations; this can expose author geometries in the orbital-level task.

## paper_94e7481ded3b6a75

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/system.json, agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：formula/input mismatch

## paper_988bc12ae3768679

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：明确需复核 agent_input 坐标来源
- 判断：Paper route identifies supplied SI S0 optimized geometries; remove them from agent input or redesign as fixed-geometry property track.

## paper_98b6f8a0352f72c2

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/compound_12a.json, agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：compound SMILES changed

## paper_9a58a1fa6ed7d780

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/submission_schema.json, agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：submission schema changed

## paper_9aa6d5655edfeb52

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_9d091f4337662e78

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, evaluation/reference_key_points.json, evaluation/scoring_rules.json, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：evaluator scoring changed

## paper_9ec8c4761c4f171b

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_9f4c259696ad2f87

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：agent_input/data/inputs/compound_1_optimized.xyz
- 判断：SI optimized input leakage review

## paper_a6e8c57709329bdb

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/hl_ligand.json, agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：HL ligand identity changed

## paper_b1467cd61ca8022d

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_b276b18215cba283

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/cisoid.xyz, agent_input/data/inputs/transoid.xyz, agent_input/task.md, package_manifest.json
- 结构泄露候选：明确需复核 agent_input 坐标来源
- 判断：SI S0-optimized structures are exposed in the excitation comparison; Stage08 additionally regressed oxygen symbols to numeric 0.

## paper_b5c446c7067dd511

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/molecular_identities.json, agent_input/submission_schema.json, agent_input/task.md, package_manifest.json, task_info.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：identity/schema changed

## paper_b815e2622b0d6085

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/crystal_records.json, agent_input/task.md, package_manifest.json, task_info.json, 删除:agent_input/data/inputs/ccdc_2499860.cif, 删除:agent_input/data/inputs/ccdc_2499861.cif, 删除:agent_input/data/inputs/ccdc_2499862.cif
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：CIFs removed; external CCDC dependency

## paper_c625cba3ce868eb1

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_d3b4575397179146

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/heptazines.json, agent_input/submission_schema.json, agent_input/task.md, package_manifest.json, task_info.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：heptazine identities changed

## paper_d91572979a89303a

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, evaluation/reference_key_points.json, package_manifest.json, paper_route.md
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：evaluator/route changed

## paper_db6c4e0558113873

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：SI optimized scored endpoints leakage

## paper_e2d9397dff2a3f0f

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/reference.xyz, agent_input/data/inputs/target.xyz, agent_input/task.md, package_manifest.json, paper_route.md, task_info.json, 删除:agent_input/data/inputs/state_definition.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：charge/atom identity changed plus TS leakage

## paper_eda19e7c8edd4b39

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_f9d09d28c7d9adaa

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_fcc3c7f2c46a0fbe

- 决策：**EQUIVALENT_SAFE**
- Stage08：存在
- 文件变化：agent_input/task.md, package_manifest.json
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：Only wording/heading/schema-reference normalization; no input/evaluator semantic change.

## paper_fda8b9b53f8276db

- 决策：**HOLD**
- Stage08：存在
- 文件变化：agent_input/data/inputs/ccdc_record.json, agent_input/task.md, package_manifest.json, paper_route.md, task_info.json, 删除:agent_input/data/inputs/ccdc_2433822.cif
- 结构泄露候选：未发现文件名高风险标记；仍需人工复核
- 判断：CIF removed; external CCDC dependency

## 2026-09-27 本批任务迁入 final

负责人确认复查结果后，本批任务已从 `tasks/verified_tasks` 完整迁入本目录：8 个包（paper_0e835b370ddd37b6, paper_1a47bc00fd63b2f5, paper_2877efc02814175d, paper_72822e4ddb5d9b11, paper_8fefc96b015c4577, paper_9132719dbf91c978, paper_9ec32e81e2826041, paper_d83e607f125440cc）。迁移只改变目录位置及审计记录中的相对链接；公开输入、提交 schema、evaluator、科学目标、参考数值和私有验证档案均未改变。

迁移后检查：本批包契约全部通过，15 个包以显式 `TaskRepository.from_final` 清单加载成功，运行策略均为 `dual_axis_100.scientific_results.v1`；manifest 已按 final 路径重建，包内本地链接全部有效，旧 `verified_tasks` 中没有本批副本。`paper_2a71ffa4b0a90809` 仍保留在 `tasks/hold_verified_paper_reproduction/`，不在本次迁移范围。上述检查不等同于运行时挂载隔离或完整 LLM judge 稳定性认证。

## 当前 on-disk 快照（2026-09-27）

本目录当前包含 **89 个 final 任务包**；对应 `hold_verified_paper_reproduction` 包含 **10 个 hold 任务包**。本批迁移增加了 8 个包，源 `tasks/verified_tasks/paper_reproduction` 已清空。JSON 中早期 `rows`、`current_assembly` 和 `counts` 保留其历史批次语义；本节及 `latest_directory_snapshot` 是当前磁盘状态。
