# Stage06/07 第2轮实现与回归记录

日期：2026-08-21  
Git版本：`b6eca74`  
目标条款：v4 §3.4、§4.6、§6、§8、§9

## 测试配置

- 模型：`deepseek-v4-pro-0813`
- harness：`codex`
- 并发：10
- 样本：与第1轮相同的10篇分层样本
- 输出：`runs/stage06-07-v4-round2-deepseek10-concurrency10-20260821`

## 第2轮代码/Prompt修改

- Stage07 gate兼容 `mode_submission_bindings` 和 `submission_bindings_by_mode` 两种合同键，并优先当前键。
- `document`/`text`/`report` 语义绑定在声明了安全文档产物时不再被当作 JSONPath 阻断。
- 对只有 `required`、没有显式 `properties` 的嵌套开放对象，binding 由 finding降为 diagnostic；显式 properties 中确实不存在的字段仍阻断。
- Prompt新增 workflow redesign 后的完整文件合同闭合清单，并明确 reproduction rubric 必须包含正权重 `route_fidelity` criterion且总分100。

## 结果统计

| 指标 | 结果 |
|---|---:|
| 测试任务 | 10 |
| CLI完成 | 10 |
| Stage07科学审计通过/重设计 | 9 |
| Stage07科学拒绝 | 0 |
| mechanical通过并发布 | 6 |
| mechanical阻断 | 3 |
| Stage06 objective failure | 1 |

相比第1轮（2个机械通过、6个机械阻断），合同误报显著下降。第2轮新增暴露出一类通用兼容问题：部分 binding 使用允许的紧凑 dotted field mapping（如 `frontier_orbitals.gap_ev`），旧 gate只接受 `$` JSONPath。

## 问题归因

| 问题 | 样本 | 归因 | 是否共性 | 处理 |
|---|---|---|---|---|
| mode binding键兼容 | 第1轮6个阻断；第2轮已消失 | 代码 | 是 | 已修复 |
| document语义binding误报 | 第1轮多个；第2轮已消失 | 代码 | 是 | 已修复 |
| 嵌套开放schema误报 | 第1轮若干；第2轮已消失 | 代码 | 是 | 已修复 |
| dotted field mapping被判非法 | paper_5ea491c741fbd8d4 | 代码 | 通用合同兼容 | 第3轮修复为等价路径观察 |
| 重设计后 rubric/required files缺失 | paper_298959ead2e91023、paper_9897b87641707c46 | Stage07 Prompt执行/模型能力；不是机械gate误报 | 尚需观察 | Prompt已加强，保留明确机械阻断 |
| Stage06 objective failure | paper_884dc6e99e15db1d | 模型/源材料/API运行结果，当前未显示代码合同缺陷 | 单样本 | 不加特例，后续看是否复现 |

## 结论与下一轮

第2轮确认第一轮主要 gate 误报已修复，但仍有一个通用 binding 表达兼容问题，且 workflow redesign 后的 Agent 合同闭合仍不稳定。先补 dotted mapping 的回归修复并跑同批10篇；若机械阻断只剩真实缺文件或单一模型能力波动，则不实现 Stage07B，转入20篇扩大测试。
