# Stage06/07 v6 Round 4：公共 mode scope 修补回归

日期：2026-08-22

## 目的

验证 Round 3 的最小 Prompt 修补是否解决了 DeepSeek→DeepSeek 生成非公开
`hidden_reference_only` acceptance profile，以及是否让 Stage07 在公共答案扫描修复后正确闭合审计状态。

## 配置

三组使用同一批 5 篇论文并同时提交，Codex harness、high reasoning、并发 5：

- DeepSeek→DeepSeek：`stage06-07-v6-round4-scopefix-same5-deepseek-deepseek-20260822`
- GPT→GPT：`stage06-07-v6-round4-scopefix-same5-gpt-gpt-20260822`
- DeepSeek→GPT：`stage06-07-v6-round4-scopefix-same5-deepseek-gpt-20260822`

论文集合：

`paper_5be4368e659d4b40`、`paper_9774cf028b321785`、`paper_75221561972a5c9c`、
`paper_f171fa1f83158f7c`、`paper_525ba02ec147f066`。

## 验收重点

1. `paper_525...` 的 hidden reference 不再产生无公开 mode 适用范围的 scored profile；
2. 若仍出现，Stage07 必须明确修复/拒绝，并在审计 receipt 中留下可见原因，不能由 gate 静默吞掉；
3. 合法 profile 的 reproduction-only、autonomous-only、shared 绑定仍按 mode 过滤；
4. `public_answer_leakage` 在完成修复后必须为 `closed`，且与 `disclosure_status=passed` 一致；
5. 五篇论文的科学批准或拒绝仍由源材料闭合性和模型判断决定，不以提高通过率为目标。
