# Stage06/07 单 Agent 改造分析报告

日期：2026-08-16
对应方案：`STAGE06_07_CURRENT_CODE_REVISION_PLAN_20260815.md`
当前结论：核心代码已达到六篇真实论文分层试运行条件，但尚不能据一次离线修复宣称真实任务构建已完全稳定。

## 1. 设计是否符合目标

当前 Stage06 的主路径已经回到两个核心职责：先基于论文 PDF、SI 和完整解析材料独立判断
计算化学流程是否完整、可复现且具有 benchmark 价值；通过后，在同一个 Agent workflow 中
先制作论文复现任务，再由确定性复制程序派生自主科研任务。Stage02-05 只提供检索提示，
不再是不可推翻的拒绝门槛。

任务选择采用 full-paper-first：优先保留整篇论文支持主要 claim 的完整计算流程；只有更大
范围确有关键数据或过程缺失时，才允许选择最大的完整 major/partial 子流程，并记录降级原因。
一次调用即可直接读出答案的低复杂度任务不进入正式 benchmark。

两个模式共享公共输入、科学问题、边界条件、提交合同、Ground Truth、Acceptance Profile
和结论 rubric。复现模式额外公开作者路线、软件、方法和参数；自主模式删除这些路线披露，
过程 rubric 可以不同。Stage07 在独立 workspace 和新 Agent 会话中只做客观审计，不自动
修改 Stage06 产物。

## 2. 代码层面的关键改进

- 单 Agent 替代默认四 phase 调用，降低重复阅读、token、延迟和 API 波动暴露面；
- 原始 PDF、全部 SI、MinerU/pypdf 解析、表格、坐标和 evidence index 一并快照，Agent 可
  自主推翻上游候选；
- 构建先落到临时 workspace，只有 receipt、review、两个任务、hidden reference 和
  deterministic audit 全部通过才原子发布；
- helper 脚本负责复现任务脚手架、复制、冻结字段和合同校验，模型负责科学抽取而不是猜
  目录 schema；
- 科学不可构建、低复杂度、构建产物无效、API/harness/解析等客观失败使用不同语义；
- 工具箱只读，缺软件作为需求和 Stage07 outcome 保留，不导致 Stage06 科学拒绝；
- Codex、Claude 和 OpenCode 使用统一 harness 接口，模型与 URL 由配置和环境变量提供；
- 运行状态收敛为根/论文各一个 JSON 和每篇一个日志，便于续跑且避免碎片文件。

## 3. 验证证据

本地验证结果：

- 全量测试 `465 passed in 10.31s`；
- Stage06/07 专项测试 `86 passed`；
- 新增合同漂移修复回归测试通过；
- Stage06/07 关键模块 `py_compile` 通过；
- `git diff --check` 通过。

专项测试覆盖 harness 适配、workspace 隔离、失败分类、恢复、full/major/partial scope、复杂度、
公共/隐藏信息隔离、复现到自主复制、Ground Truth 类型化验收、Stage07 outcome 和常见 Agent
字段漂移。

## 4. 真实论文回归给出的结论

`paper_6904a9c8c09855cc` 的旧真实调用证明 Agent 能定位论文/SI 的计算流程、调用脚手架并生成
两个模式与 hidden reference，但也暴露出“JSON 声明了输入路径，实际文件没有落盘”的问题。
r2 确定性规范化可修复 mode、scope、complexity、sidecar、rubric、工具箱状态等合同漂移，
却不会补造 22 个缺失 XYZ，也不会接受不存在的 evidence ID。这种保守行为是正确的：格式
问题可以机械修复，科学资产缺失必须由 Agent 回到 SI 恢复，恢复不了就判构建失败。

因此当前最大的未知量不再是 Python schema，而是不同论文上 Agent 是否会稳定执行“定位
资产 -> 复制真实文件 -> 引用 canonical evidence -> 完成两个任务”的长工作流。六篇分层
试运行正是为验证这一点。

## 5. 当前风险与处理原则

### 5.1 输入只声明不落盘

这是最高优先级风险。最终 validator 必须继续同时检查 manifest、路径、文件存在性、非空、
两模式复制一致性和必要时的内容 hash。不能用自动生成占位 XYZ 的方式提高通过率。

### 5.2 单 Agent 已看到隐藏答案

单 Agent 方案只能实现文件和代码级硬隔离，不能实现模型上下文级遗忘。当前通过受限复制、
自主目录路线扫描、hidden/reference 路径禁止、公共内容答案泄漏扫描和独立 Stage07 审计降低
风险。如果真实试运行仍频繁泄漏，应启用预留的独立 converter，而不是继续扩大同一 prompt。

### 5.3 确定性恢复掩盖科学错误

规范化只允许修复 schema 别名、可由已冻结产物唯一恢复的字段和可计算统计量。结构、电子态、
计算方法、参数、Ground Truth、evidence 和真实输入文件不得推测。相关测试应保持为回归门槛。

### 5.4 通过率不是唯一目标

高优先级样本也可能因论文未公开关键资产而合理失败；低适宜度样本也可能被 Agent 在 SI 中
找到完整子流程而合理通过。审查重点是决策是否有可追溯证据、失败类型是否正确，而不是强迫
六篇达到某个通过数。

## 6. 六篇试运行验收方法

逐篇核对以下事实：

1. Stage06 是否真实读取 PDF/SI，Stage05 仅作为提示；
2. workflow inventory 是否覆盖全文，并优先尝试 full-paper scope；
3. 所有公开输入路径是否真实存在、非空且在两个模式中一致；
4. 复现模式是否包含可执行路线，自主模式是否没有作者路线和隐藏答案泄漏；
5. Ground Truth 是否覆盖关键中间文字结论和最终结论，而非只有数值；
6. Acceptance Profile 是否逐 item 类型化，并与 submission contract 和 rubric 对齐；
7. 工具箱缺口是否记录为建议而非科学拒绝；
8. Stage07 是否输出客观、可并存的通过、缺软件、缺数据、成本过高等审计结论；
9. API/harness/解析故障是否保持为可恢复的客观失败；
10. 失败时是否没有发布半成品任务目录。

只有真实运行轨迹满足上述合同，才进入下一批规模化构建。发现实现缺陷时按“记录样本和版本 ->
最小修复 -> 单元测试 -> Git 提交 -> 只重跑受影响论文”的顺序闭环。
