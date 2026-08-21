# Stage06/07 v5 Round 5：DeepSeek 10 篇批次的阶段性审查

日期：2026-08-22  
批次：`runs/stage06-07-v5-round5-deepseek10-concurrency10-20260822`  
模型：DeepSeek-v4-pro-0813，Codex harness，并发 10

## 1. 运行状态边界

按本轮约定，提交后等待超过 30 分钟再分析，不因为单篇论文尚未完成而重复提交或停止批次。当前批次仍有子进程运行，部分论文已完成 Stage06A/Stage06B 并进入 Stage07，尚未形成最终 `late_stage_run_summary.json`。因此下面的科学判断是阶段性判断，不能替代最终发布/拒绝状态。

已形成 Stage06 summary 的论文显示：`provisional_constructed=1`；软件缺口只在需要时作为非阻断信息记录。尚未完成的论文仍处于模型工具调用阶段，不应被统计为科学拒绝或代码失败。

## 2. 与总目标的阶段性对照

已读到的 workflow review 大体执行了“完整路线优先、必要时选择最重要核心子过程”的规则：

- 选取六类 Li/BC2N-graphene 吸附比较，替代只覆盖一个系统/位点的上游候选；
- 选取六类 Ca²⁺离子对静态 DFT 比较，因全量 AIMD MetaD 成本过高而降级，并记录完整路线与成本原因；
- 对 HCN 论文，在精确 slab 坐标缺失且完整表面/Wulff 路线成本较高时保留直接支撑电场催化主张的 HCN 链电场子过程；
- 对配合物论文保留完整的三候选异构体、各自旋态、Mössbauer 与 TD-DFT 联合路线；
- 对结构/药化论文，DFT 构象/FMO 被选为可闭合核心，Discovery Studio docking 和 Hirshfeld 分支因缺少可复现协议或坐标而列为未选分支；缺失 Spartan/08 仅写入 `toolbox_requirements.json`，未导致科学拒绝。

这些样例符合总目标：外围、容易包装但不能代表主线的廉价流程没有被用来提高通过率。最终仍须以 Stage07 对论文正文、摘要、主图、结论和 SI 的审计为准。

## 3. 发现的通用合同/提示问题

在一个 Stage06A 产物及其 Stage07 输入中发现了重复资产路径：

`data/inputs/compound_1_structure.json` 与 `data/inputs/data/inputs/compound_1_structure.json` 同时存在。

这不是该论文的科学特例，也没有改变必需资产的内容；更可能是 Agent 在把已带有 `data/inputs/` 前缀的逻辑路径物化时重复拼接了目录前缀。它属于可泛化的输出卫生/Prompt 清晰度问题，不应通过论文名或文件名特例修复。Stage07 当前仍能找到规范路径，但冗余文件可能进入审计输入和最终 bundle，增加歧义。

本轮对 Stage06A、Stage06B、Stage07 提示增加了两条通用约束：

1. 每个 `data/inputs/...` 声明只物化一次，明确禁止 `data/inputs/data/inputs/...`；
2. 在 Codex 隔离工具中避免 `rm`/`rm -rf` 等 shell 清理命令，采用新目录/定向文件写入，减少因工具安全拒绝造成的模型循环和超长等待。

这两条只约束文件运输和操作方式，不判断化学闭合、代表性或答案语义，也不包含论文/分子特例规则。

## 4. 当前不能下结论的事项

- Stage07 是否能修复重复路径、完成输入闭合和 mode-aware evaluator binding；
- 机械 gate 是否仍有误阻断；
- Stage06B `needs_conversion_retry` 是否在本批次被已有恢复循环正确处理；
- 最终科学批准/科学拒绝与发布树之间的状态是否一致。

这些项目必须等每篇论文写出 Stage07 审计和 late-stage summary 后逐篇核对。若最终只剩个别论文的坐标缺失、来源本身未定义、路线成本或模型判断差异，应记录为源材料/科学或模型问题，不新增代码特例。

## 5. 下一步

继续保留当前批次运行；终态出现后逐篇检查 Stage06A 的完整路线盘点、子流程降级证据、软件缺口登记、Stage06B 答案盲转换、Stage07 科学审计和最终 mechanical/publish 状态。只有同类问题在多篇论文重复出现，才进入下一轮通用修复；单篇论文不满足闭合条件本身是允许的科学拒绝。
