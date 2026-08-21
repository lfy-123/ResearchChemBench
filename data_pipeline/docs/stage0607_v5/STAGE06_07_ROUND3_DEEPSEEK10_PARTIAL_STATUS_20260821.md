# Round 3 DeepSeek 10 篇测试：30 分钟状态记录

测试目录：`runs/stage06-07-v5-round3-deepseek10-concurrency10-20260821-retry`  
提交方式：`codex` harness，`deepseek-v4-pro-0813`，`high`，并发 10，脚本随机种子 `20260821`。  
抽样集合由批处理脚本在同一进程内生成并写入 `batch_status.json`，避免手工复制论文 ID。

## 30 分钟检查

10/10 子进程仍处于 `RUNNING`，根批次也处于 `RUNNING`，因此当前没有 Stage07 科学批准、科学拒绝或机械发布结果可下结论。已生成 Stage06A 工作流审查的论文均包含 `representativeness_review`，并出现 `execution_readiness=ready` 或 `conditional`；没有观察到“软件缺口导致科学拒绝”的代码路径。

这只是运行中状态，不是质量结论。完整审查必须等待每篇的 Stage07 receipt、`stage_summary.json`、发布树和对应正文/SI 证据；在此之前不能把 Stage06A 的 provisional 构造当作最终任务通过。

## 初步可见现象

- Stage06A 新增的候选比较字段已被模型实际填写，说明 prompt 约束进入了执行轨迹。
- 个别原始 `workflow_scope` 使用了兼容别名 `scope_kind`，Stage06 的规范化层负责投影为 canonical `kind`；这属于已有兼容层行为，待最终发布树检查是否正确冻结。
- 当前延迟来自 codex harness 的长时间 Agent 子任务，不是批处理状态孤儿：每篇仍有活跃子进程和 `run_status.json`。

## 后续动作

继续保留任务运行。下一次检查逐篇读取 Stage07 决策、代表性审计、工具箱登记、输入闭合/绑定和公开任务内容，并与正文主图/结论核对；若发现共性代码或 prompt 问题，再在下一轮记录和修改，不依据单篇源材料不可执行而添加特例规则。
