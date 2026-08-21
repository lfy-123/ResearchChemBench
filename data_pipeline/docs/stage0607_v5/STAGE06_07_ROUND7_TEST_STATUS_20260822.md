# Stage06/07 v5 Round 7：DeepSeek 回归批次状态

日期：2026-08-22  
代码版本：`f80d5f3`  
模型/Harness：DeepSeek-v4-pro-0813 / Codex  
推理强度：high；并发：10；随机种子：`20260825`

## 批次

结果目录：

`runs/stage06-07-v5-round7-deepseek10-concurrency10-20260822`

论文：

`paper_1bcf80caf9e64d55`, `paper_72c3e34e4e3814e2`, `paper_4b4e0bec6df820fc`,
`paper_8d23f76050f65720`, `paper_b1197fa7792320e9`, `paper_1d3ae60b0873aff0`,
`paper_03455526ab937195`, `paper_4fe409b2ae308c1c`, `paper_738fd3ba350dd55a`,
`paper_849802730178edb8`。

已确认 `batch_status.json` 和 10 个 `run_status.json` 均已创建，10 个 worker 正常启动。提交后按约定不连续轮询，等待窗口结束后统一读取终态和 Stage06/07 产物。

## 审查重点

本轮需要逐篇对照正文/SI检查：

1. 是否先尝试完整计算主线；若降级，是否有成本、缺失输入或闭合证据；
2. 选定子流程是否确实支撑标题/摘要/主图/结论中的核心主张，而非外围易包装流程；
3. `representativeness_review` 是否使用对象字段 `claim_id`、`claim`、`coverage`、`evidence_ids`，候选是否记录 `scope_kind`、`closure`、资源观察和软件观察；
4. 工具箱缺口是否登记但未被误写成科学拒绝；
5. Stage06B 是否保持答案盲，只转换公共表面；
6. Stage07 是否独立审计并如实区分科学拒绝、可修复合同问题和模型/源数据限制；
7. 是否出现新的通用代码 bug、提示词/合同错位或孤儿 `RUNNING` 状态。

若发现重复且通用的问题，才记录 Round 8 方案；单篇论文的科学不可执行性、坐标缺失或模型判断错误不增加代码特例。
