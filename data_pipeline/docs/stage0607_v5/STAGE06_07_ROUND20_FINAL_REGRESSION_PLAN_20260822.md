# Stage06/07 v5 Round 20 最终回归计划

日期：2026-08-22

代码基线：`586d4c5`

总目标：`STAGE06_07_V5_OPTIMIZATION_OBJECTIVE_AND_BOUNDARIES_20260821.md` v5.2

## 1. 配置

- 模型：DeepSeek-v4-pro-0813
- Harness：Codex
- reasoning：high
- 样本：Stage05 通过集合随机 10 篇
- seed：`20260861`
- 并发：10
- 结果目录：`runs/stage06-07-v5-round20-final-deepseek10-concurrency10-20260822`

## 2. 验证目标

1. `TaskInfo.data` 已声明 path 时不再因缺少展示名称而被 evaluator 机械阻断。
2. Stage06A/Stage07 对结构化科学输入使用适用的完整格式 parser/schema，并在私有审计中记录 parser/tool 与结果；不能用后缀、行数或局部坐标替代完整解析。
3. 涉及原子、位点、bead、residue 等整数索引的公共任务明确索引基准，并与结果字段/private binding 一致。
4. 自主模式对近简并、构象敏感或方法敏感量不强制无证据的严格全序；允许 mode-specific acceptance、tie group、partial order 或稳健端点/分组趋势。
5. 完整论文计算主线仍为默认；降级时必须选最高中心性闭合子流程并给出数据、资源或科学闭合证据。软件缺口只登记。
6. 科学拒绝、科学批准、机械发布状态和恢复失败保持可观察；不把论文是否获批当作代码质量指标。

## 3. 审查方法

批次结束后逐篇阅读正文、SI、Stage06 workflow review、Stage07 audit、公开任务、hidden Ground Truth 和机械报告。每篇分别归因到：正确处理、源材料不闭合、代码 bug、Prompt/角色设计、模型未执行现有要求。Round 20 是预算内最后一轮；之后不因个别模型误判继续添加论文/格式特例或扩张机械科学 gate。

Stage07B 仍仅在至少 2/10 出现同类、科学批准后的简单合同阻断时评估；中心性、输入真实性、acceptance 语义和成本不属于 Stage07B。
