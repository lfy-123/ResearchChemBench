# 暂缓发布的论文复现任务

## 2026-09-24：paper_641a923cbe5bbc48

按用户要求与自主包一起移入 hold：两模式共享正文硫脲与 SI/验证含氧模型的对象冲突。详细证据、补算范围和恢复条件见 [专门交接文档](../HOLD_paper_641a923cbe5bbc48_HANDOFF.md)。当前改进工作优先自主模式，本次不优化复现评分。下文各日期记录为历史批次，不是当前全目录清单。

## 2026-09-16 新批次已退回审查区

本批先前迁入的 7 个任务已按负责人要求完整退回 `tasks/verified_tasks/paper_reproduction/`。有问题并不授权agent自动移入hold；其问题和方案仍记录在 [MAINTENANCE_REPORT.md](../verified_tasks/MAINTENANCE_REPORT.md)，等待负责人确认后再修改及决定去向。本目录恢复为下列原批次3个任务，内容不变。

2026-09-15：按用户要求，从 `final_verified_paper_reproduction` 原样移入三篇任务：

- `paper_6492e1e5d38d23ae`（group_5）：表面模型与数值评分边界。
- `paper_8b7bf002cc6a4ba9`（group_5）：有效显式水构象链缺失。
- `paper_b815e2622b0d6085`（group_6）：第二网格框架电子态身份/稳定性证据不足。

这些任务不得纳入当前正式发布清单。任务输入、evaluator 和计算 reference 均未因迁移改变；结构校验通过不等于科学验证通过。`paper_84efbea3ab8e6e20` 仍在 final，沿用限定发布口径。

处理原因、按 group 分配的操作指令和恢复条件统一见 [HOLD_VERIFICATION_HANDOFF.md](../HOLD_VERIFICATION_HANDOFF.md)。可以私下按作者路线进行验证，但不得将最终答案、坐标或这些维护资料提供给被评估 agent。
