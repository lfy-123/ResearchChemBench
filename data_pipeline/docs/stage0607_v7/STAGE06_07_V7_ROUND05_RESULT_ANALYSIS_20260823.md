# Stage06/07 v7 Round05：实现与回归结果

日期：2026-08-23  
对应计划：[Round05 plan](STAGE06_07_V7_ROUND05_PLAN_AND_CONTRACT_BOUNDARY_FIX_20260823.md)  
基线：`22ea9df fix(stage06-07): close hidden evaluator transport contract`

## 1. 本轮实现

本轮只处理通用 hidden evaluator transport 和阶段边界，没有加入论文、分子、软件、数值
或化学判断规则：

- Stage06A 的 handoff binding 检查支持 `required_binding_modes`，只要求当前已生成的
  reproduction 行；Stage06B 尚未生成的 autonomous 行不会制造 Stage06A 重试。
- 在 hidden alias/投影前增加 ownership/scope preflight，报告并保留原始合同中的 orphan
  profile、重复 owner、shared 与 mode matrix 并存、truth/profile scope 不一致以及 ready
  合同空 Ground Truth。
- Stage07 finalizer 和 mechanical gate 在有上述结构 finding 时跳过所有可能有损的 hidden
  normalizer（包括 JSONPath 兼容投影），避免修复前文件被静默改写。
- profile 的显式 mode scope 与其唯一 owner 的 scope 必须一致；省略 profile scope 仍可由
  normalizer 从 owner 继承，以保持旧合同兼容。
- 新增 paper-neutral Round05 回归矩阵；去掉只用于判断旧嵌套 binding 的无调用 helper。

## 2. 兼容性修复

第一次专项回归发现 9 个旧测试失败：旧的轻量 evaluator fixture 没有 `status=ready`，
只有 `expected_result`，不应被当作生产 hidden contract。preflight 现在仅在明确
`status=ready`（或显式提供 Ground Truth）时执行 ownership 强检查；非 ready legacy
envelope 保持原有行为。该边界由 Round05 测试固定，生产 Stage06/07 路径仍对 ready 合同
严格检查。

## 3. 自动化验证

专项命令：

```text
PYTHONPATH=. pytest -q \
  tests/test_stage0607_v7_round04_contracts.py \
  tests/test_stage0607_v7_round05_contracts.py \
  tests/test_stage0607_v5_contracts.py \
  tests/test_stage0607_agents.py
```

结果：`198 passed`。

覆盖的 Round05 边界包括：

1. Stage06A partial mode matrix 不要求 autonomous 行；
2. Stage07 对所有适用 mode 行继续严格检查；
3. orphan profile 被阻断且原始 profile/路径保留；
4. 一个 profile 被多个 Ground Truth 共用时阻断；
5. shared binding 与 mode matrix 同时存在时阻断；
6. truth/profile scope 过窄或过宽时均阻断；
7. ready 合同没有 Ground Truth 时阻断；
8. 合法 shared/mode-specific profile 继续通过；
9. 非 ready legacy envelope 保持兼容。

全仓库验证：

```text
python -m compileall -q src/stages/stage06_task_builder src/stages/stage07_task_judge
git diff --check
PYTHONPATH=. pytest -q
```

结果：`584 passed`，compile、diff 检查均通过。

## 4. 归因与剩余验证

本轮没有发现新的科学任务选择问题；代码修复仅涉及合同所有权、适用 mode、归一化可见性
和阶段时序。后续模型测试仍需观察 Agent 是否能根据结构 finding 自行修复；若只出现单篇
模型遗漏而没有重复的通用合同问题，应归类为 Prompt 执行/模型能力或源材料差异，不继续
堆叠代码特例。

下一步提交同一样本的三种组合对照：DeepSeek→DeepSeek、GPT→GPT、DeepSeek Stage06→
GPT Stage07，记录实际模型、Codex harness、commit、样本、运行目录和每类终态。
