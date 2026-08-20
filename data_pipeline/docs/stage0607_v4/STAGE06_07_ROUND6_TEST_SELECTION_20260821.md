# Stage06/07 第6轮20篇扩大测试抽样

日期：2026-08-21  
代码：`7dd439b`  
模型：`deepseek-v4-pro-0813`；harness `codex`；并发10

从既有批量运行结果按 Stage06 历史结果分层，使用随机种子 `20260821` 抽取20篇：

| 历史类别 | paper_id |
|---|---|
| provisional_constructed | paper_6b32cd680ee1afd4 |
| provisional_constructed | paper_9e76a3b15026ccd8 |
| provisional_constructed | paper_3e2d7e8370a8dc83 |
| provisional_constructed | paper_9d091f4337662e78 |
| provisional_constructed | paper_7574d99707125e60 |
| provisional_constructed | paper_8f891f94d53054e4 |
| provisional_constructed | paper_9bf81c340f85769b |
| artifact_delivery_failure_retryable | paper_0f779cb03ad78ef5 |
| artifact_delivery_failure_retryable | paper_585288a5a5265d55 |
| artifact_delivery_failure_retryable | paper_23ab5e60dd8e8983 |
| artifact_delivery_failure_retryable | paper_03455526ab937195 |
| artifact_delivery_failure_retryable | paper_575b732fe6d00d73 |
| provisional_not_constructible | paper_72d95769f7cf9016 |
| provisional_not_constructible | paper_108e6a1fb1e8f309 |
| provisional_not_constructible | paper_4ee9947f568c29ba |
| provisional_not_constructible | paper_298959ead2e91023 |
| provisional_not_constructible | paper_63c76161e5b55a6a |
| objective_failure_retryable | paper_56da7f9591ef00f2 |
| objective_failure_retryable | paper_09c8aaf14b70371f |
| objective_failure_retryable | paper_98b6f8a0352f72c2 |

验收仍按 v4目标逐篇检查科学任务质量、双模式隔离、Stage07科学决定、机械状态、evaluator加载和公开目录；不把历史类别当作本轮结论。
