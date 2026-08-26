# Stage06/07 v22 五篇回归测试分析

## 1. 测试范围与终态

本轮使用 v22 双模式逻辑，Stage06 与 Stage07 均使用 `gpt-5.6-sol`、high reasoning，
并发 5，端点为 `http://127.0.0.1:50917/v1`。测试运行目录为：

`runs/stage0607-v22-gpt-5.6-sol-20260827-dual-mode-five`

终态如下：

| paper_id | Stage06 | Stage07 | 最终结果 |
|---|---|---|---|
| `paper_2aca1dd116799b28` | constructed candidate，self-check passed | approved_with_repairs，Gate passed | published |
| `paper_611000e1de080f6f` | constructed candidate，self-check passed | approved_with_repairs，Gate passed | published |
| `paper_76ae2dc25f0a5aeb` | Agent 成功退出但 autonomous 文件未写出 | 未运行 | technical_blocked |
| `paper_9455a82229de2427` | constructed candidate，self-check passed | approved_with_repairs，Gate passed | published |
| `paper_a5564360a31f760b` | scientific_not_constructible | 未运行 | scientific_rejection |

发布率为 3/5。`a556` 的拒绝是有证据支持的输入闭合失败，不是代码错误：来源没有唯一、
机器可读的 methyl-truncated p-2BN/m-2BN 分子图和原子映射。`76ae` 是技术阻断，不应被
解释为科学不可构建。

旧的 v19 回归孤儿进程已停止；本报告只分析 v22 目录。

## 2. 方案目标的验证结果

### 2.1 已达到的部分

- 两种模式都使用 `paper_id`，没有生成 `task_id`、`task_family_id`、`task_pair_id` 等额外
  论文级 ID。
- 发布包采用 `tasks/{autonomous_research,paper_reproduction}/{paper_id}`，论文材料位于
  `release/papers/{paper_id}/documents/`；PDF/SI 没有复制到 Agent-visible 的
  `agent_input`。
- 两种模式均包含完整的 `task.md`、`task_info.json`、`submission_schema.json` 和分开的
  evaluator 文件，最终外部 Gate 均通过。
- `611`：reproduction 暴露了作者的 TICT 科学路线，但没有暴露软件、泛函、基组、计算顺序、
  结果结构、数值或预期排序；autonomous 隐藏 TICT 路线并要求比较多个自主假设。
- `945`：reproduction 暴露了作者提出的两种 H-loss 环状产物路线，autonomous 改为自主提出
  产物假设和搜索空间；两者的计算 protocol 仍由 Agent 自主选择。
- `611` 和 `2aca` 的 Stage07 审计均做了有界修复，且最终 `agent_self_check_report.json`
  和 external Gate 均为 passed。

### 2.2 未完全达到的部分

#### (a) `paper_2aca...` reproduction 仍泄露结果方向

公开文件：

`runs/stage0607-v22-gpt-5.6-sol-20260827-dual-mode-five/papers/paper_2aca1dd116799b28/release/tasks/paper_reproduction/paper_2aca1dd116799b28/agent_input/task.md`

其中 Scientific objective 直接写出：

`16` 的 barrier 被 preferentially stabilized、`15` intermediate、`17` least reactive，
并在 conclusion 要求验证 `17 > 15 > 16`。这不是单纯的作者科学路线提示，而是论文结果的
方向性答案。与 v22 方案“reproduction 可公开假设/候选/机理，但隐藏数值、排序、完整结论”
不一致。

Stage07 的 `stage07_audit.json` 将该内容判为“qualitative route”，因此没有修复；这说明当前
审计 Prompt 对“作者机理解释”和“结果方向/完整结论”的边界仍不够清楚。外部 Gate 是机械
合同 Gate，本来就不会发现此类科学泄露，所以 Gate passed 不能证明无答案泄露。

#### (b) `paper_76ae...` autonomous 未生成

Stage06 Agent 运行 1454 秒、消耗 152 次工具调用后正常退出，但只留下 reproduction 文件。
外部检查报告明确指出 autonomous 的 `task.md`、`task_info.json`、`submission_schema.json`、
五个 evaluator 文件全部缺失，故编排器将其标记为 `technical_blocked`。这不是 API 失败，也
不是 self-check 发现科学问题，而是 Agent 在 reproduction self-check 通过后继续反复执行
`find outputs`/状态检查，最终未在预算内完成第二模式。

### 2.3 其它观察

- `2aca` 和 `611` 的 scoring rules 数值 tolerance 只生成 diagnostics
  `tolerance_requires_scientific_review`，没有阻断，符合“规则完整但 tolerance 由人工复核”的
  设计。
- `2aca` 的公开输入包含通用 `toolbox_capabilities.json`。它不是论文 protocol，但文件很大，
  仍会增加上下文和工具搜索成本；后续可考虑保留与任务实际可执行性有关的能力子集，但不应
  通过论文特例硬编码。
- `a556` 的 scientific rejection receipt 给出了具体证据和缺失字段，没有错误地把模型超时
  当作科学拒绝，符合方案。

## 3. 根因归因

1. **答案泄露根因**：Stage06 Agent 把“作者解释为何会有该趋势”与“趋势的具体方向”混写在
   reproduction 的 objective 中；Stage07 审计 Prompt 允许把这类方向性断言归入 route，未做
   结果泄露的语义拦截。机械 Gate 不负责科学语义，因此不会阻断。
2. **76ae 技术阻断根因**：不是重试或 resume，而是单次 Agent 工作流的阶段切换控制不足。
   Agent 已完成 reproduction self-check，却没有把 autonomous 构建当作紧接着的强制里程碑；
   重复目录检查耗尽了可用于写文件的调用预算。当前代码正确地拒绝发布不完整包，但不能把
   incomplete artifact 误判为科学拒绝。
3. **质量差异**：611/945 的双模式科学内容符合目标，2aca 的科学目标本身合理但公开 contract
   泄露了答案；因此本轮不能宣称“所有已发布任务都完全符合 v22 语义”。

## 4. 后续最小修正建议

这些建议不改变 Gate 的机械边界，也不添加论文特例：

1. 在 Stage06 和 Stage07 Prompt 中把 reproduction 的 author route 明确拆成两类：允许作者的
   假设、候选方向、定性机理；禁止作者结果的数值、排序、优先级、最终结构和“因此 X 更低/更快”
   等方向性答案。要求使用“检验作者关于……的解释”而不是把答案写入 objective。
2. 在 Stage07 科学审计清单中增加一个通用语义检查：逐段检查 task.md、schema、文件名和公开
   输入，发现任何 reference value/order/final verdict 即要求移除或改写；只有真正作为研究前
   输入的对象才可保留。该检查属于 Agent 科学审计，不是 Gate 关键词黑名单。
3. 在 Stage06 Prompt 的 reproduction self-check 通过后加入短而明确的终止式里程碑：立即复制并
   完成 autonomous 的全部文件，禁止再次搜索已验证的目录；将“完整 autonomous tree”作为
   下一次写入目标。必要时仅调高通用 finalization reserve，不引入 retry/resume 或代码生成
   科学内容。
4. 保留当前编排器对缺失文件的技术阻断逻辑；它正确防止半成品进入 release。对 `76ae` 应
   重新运行一次验证修正后的 prompt/预算，而不是把半成品补齐后发布。

## 5. 结论

v22 已解决旧版“两模式只差方法名/简单复制”的主要结构问题：611 和 945 明确表现出
“作者科学路线提示”与“自主提出路线”的差异，且 PDF/SI 没有泄露给被评测 Agent。可是本轮
仍暴露出一个重要语义缺陷（2aca reproduction 的结果方向泄露）和一个流程缺陷（76ae 在完成
reproduction 后未及时进入 autonomous）。因此当前代码可以作为 v22 的有效中间版本，但在
宣称完全符合方案或扩大批量运行前，应先完成第 4 节的两个最小 Prompt/流程修正并重新回归。
