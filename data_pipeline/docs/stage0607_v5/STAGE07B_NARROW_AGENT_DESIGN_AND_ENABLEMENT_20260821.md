# Stage07B 窄合同修复 Agent：设计与启用条件

## 定位

Stage07B 是可选的 transport-contract recovery 阶段，不是第二个科学审计员，也不是发布批准员。它只在 Stage07 已完成科学批准后处理明确、低风险、可由已有私有映射和任务文件确定的合同缺陷。

## 启用条件

先完成 v5 第一轮通用 gate 修复并重新跑回归。若一个 10 篇 DeepSeek 批次中至少 2 篇，或连续两批重复出现相同类别的“Stage07 科学批准 + 简单合同阻断”，且这些问题不是 gate 自身误报、不是科学输入缺失、也不需要重新解释论文，则记录证据并启用 Stage07B。若只是零星个案，继续修代码或保留机械阻断，不增加 Agent。

## 输入

- Stage07 的 immutable `scientific_audit`/`audit_decision`；
- 已批准 task pair 的 public tree；
- `ground_truth_common.json` 的只读 ID/适用 mode 摘要；
- `public_to_private_asset_map.json` 等不含答案的映射；
- mechanical gate findings 和 schema/manifest诊断。

Stage07B 不读取论文正文来重新作科学选择，也不接触可用于改变答案的自由编辑接口。

## 允许修复

- 安全相对路径、必需文件清单和目录布局；
- `mode_submission_bindings` 的明确 mode 键、字段路径和容器包装；
- `criteria`/`items` 等无科学含义的 rubric 容器投影；
- 已由 Stage07 给出映射的匿名资产名、manifest/hash和发布树清理；
- 仅限 transport 的类型/枚举/ID后缀同步。

## 禁止操作

- 改变科学问题、workflow步骤、输入资产内容或物理边界；
- 修改 Ground Truth 数值、结论、排序、容差、Key Point 数量或含义；
- 添加/删除科学结论或选择评分模式；
- 依据论文、分子名、固定数字或关键词作判断；
- 把无法确定的 finding 猜测成可修复。

## 输出与状态

输出一次结构化 `repair_patch`、`changed_files`、`unchanged_scientific_fields` 和 `mechanical_blocked_unresolved`（如适用）。编排器应用 patch 后只复检一次。Stage07B 不写 `approved`；最终状态仍由 Stage07 的科学决定与机械 gate 分开记录：`published`、`mechanical_blocked` 或 `mechanical_blocked_unresolved`。

## 实施顺序

1. 先以普通代码修复消除 mode applicability、binding 和 scope 的共性 bug；
2. 收集至少一批 10 篇回归证据；
3. 只有达到启用条件才添加最小 prompt/schema/调用路径和正反回归 fixture；
4. 若启用后仍无法确定，终止发布并留下可见 finding，不重启完整 Stage07 科学审计。

