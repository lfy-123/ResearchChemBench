# Stage06/07 v5 Round 7：代表性比较证据字段的最小增强

日期：2026-08-22  
基线：`e1cfe92`（Round 6 测试仍在运行）

## 1. 本轮目标与边界

本轮只处理一个通用的流程证据问题：Stage06A 已经被要求先比较完整路线、再选择核心子流程，但 `representativeness_review.candidate_workflows` 原先只在提示词中要求记录闭合、成本、软件状态和主张覆盖，代码没有检查这些记录是否存在。模型如果只提交一个“容易打包”的候选，Stage07 就缺少比较依据。

本轮不做以下事情：

- 不根据论文标题、分子名、软件名、数字或关键词计算科学中心性；
- 不把成本、工具箱缺口或字段缺失直接解释为科学拒绝；
- 不增加 Stage07B；
- 不改变 Stage06B 的答案盲隔离；
- 不修改 Stage00–05 或已有任务数据。

## 2. 修改内容

### 2.1 Stage06A prompt

明确要求每个候选工作流显式提供：`workflow_id`、`scope_kind`、`closure`、`claim_coverage`、一个资源/成本观察（`cost`、`resource_assessment` 或 `estimated_cost`）以及一个软件观察（`software_gap_status`、`toolbox_status` 或 `software_status`）。空值或不确定值可以保留，但不能省略字段。

### 2.2 Stage06 结构验证

`validate_representativeness_review()` 只增加字段存在性检查。它不解释字段内容、不比较候选优先级，也不检查某个候选是否“真的核心”。缺少字段时返回可解释的结构 finding，交由 Agent/Stage07 补全或审计。

### 2.3 Stage07 prompt

要求 Stage07 对每个候选核对上述四类信息；缺失或无证据的记录必须进入审计 finding，不能被当作“已证明闭合的替代路线”。最终科学判断仍由 Stage07 根据论文正文/SI完成。

### 2.4 字段合同与提示词对齐

Round 6 的中间产物显示，模型将 `paper_computational_claims` 写成字符串或只有 `claim`/`evidence_ids` 的对象，而验证器需要 `claim_id`、`claim`、`coverage`、`evidence_ids`；部分候选也省略了 `scope_kind`。本轮在 Stage06A/Stage07 prompt 中明确这些字段，保持验证器的通用结构检查不变。

## 3. 验证计划

1. 运行 Stage06/07 相关单测及全量回归；
2. 检查当前 Round 6 批次，不停止其运行；
3. Round 6 终态后，逐篇审查完整路线优先、核心子流程中心性、软件缺口登记和角色边界；
4. 若需要验证本轮提示词/结构字段，另行随机抽取 10 篇 Stage05 通过论文，用 DeepSeek-v4-pro-0813、Codex harness、high reasoning、并发 10 运行；提交后等待至少 30 分钟，再进行结果审查；
5. 只有出现重复且通用的后置缺陷才进入下一轮，不能因单篇论文源数据缺失增加代码特例。

## 4. 预期验收

- 每个候选工作流都有可审计的闭合、资源、软件和主张覆盖记录；
- Stage07 能明确指出外围/容易包装流程，而不是被结构完整性掩盖；
- 软件缺口只登记，不导致科学拒绝；
- 代码仍只做合同/证据形状检查，科学代表性不被机械规则替代。
