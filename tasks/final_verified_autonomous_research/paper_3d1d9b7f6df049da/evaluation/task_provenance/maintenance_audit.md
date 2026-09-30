# 已批准修复记录（2026-09-23）

授权：负责人同意 MAINTENANCE_REPORT 第 15 节方案及 D1–D7。正文/SI 为主，验证计算为辅；只在 verified_tasks 修复，无新量化计算、无迁移授权。

已按批准方案分离 PR guidance，取消普通 limitation/停止表态的 required 和独立得分，显式采用 scientific_results 策略；保留真实失败诊断、对象/态/收敛/敏感性证据与原科学数值容差，修复已发现的 [] 选择器并接回必要关键点。

收尾复查：修复清理后的残句及“失败也称 complete”矛盾；保留主结果要求，提供不必虚构数值/结构的早期失败格式。针对主对象重复/缺失与成功状态做契约检查；普通免责声明不作为必需字段或成果。

计算档案已补成有效链、源方法/验证差异、原始输入输出和当前 4 个关键点/2 条科学结论对应；不把 reference 变成 evaluator、不写入虚构计算。

## 2026-09-23 二次回查：定义与提交契约修复

SI Tables S3a/b 的主对照为每异构体四个 Y2 横向模式。旧 schema 允许 modes 超过四个，numeric selector 却读取整个数组与四参考配对。现将 complete 主数组限定四项，额外候选用 additional_modes，不限制探索总数；mode_id 去重由显式物理指认规则判断，schema uniqueItems 只阻止完全相同的重复记录，不冒称能自动判定所有物理重复。真实两异构体各四模式结果保留，原频率及 ±12 cm⁻¹ 容差不变。

本次只澄清既定科学子目标，不改数值 target/tolerance、不增加 limitation 评分；未重算、未运行 LLM judge、未迁移目录。

## 2026-09-24 补齐原文出处摘要

直接核读 SI PDF p21 Table S3a 第4–7行：Ih 四模参考为 49.9、54.9、65.2、68.9 cm⁻¹。当前评分和 reference 本已包含四项，closure_20260921 的实际四模计算也完整，遗漏只在 evidence_map 的该条 text。本次补入 68.9，未改 target/tolerance、选模方法、公开输入或历史频率。无新增计算或迁移；测试及本轮结果见 MAINTENANCE_REPORT.md 第19节。
