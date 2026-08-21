# Stage06/07 第9轮结果与第10轮最终元数据投影修复

## 第9轮测试结果

- 输出：`runs/stage06-07-v4-round9-deepseek10-concurrency10-20260821`
- 模型/Harness：`deepseek-v4-pro-0813` / Codex；并发10；10篇；CLI 10/10成功。
- Stage06：9篇 `provisional_constructed`，1篇 `provisional_not_constructible`。
- Stage07：9篇 `approved_with_repairs`，1篇 `rejected_scientific_unrepairable`。
- 机械合同：已完成的9篇全部通过；机械阻断0；发布就绪9篇。

这里的“9篇发布、1篇拒绝”不是通过率目标。`paper_63c76161e5b55a6a`的源坐标/必要输入
缺失，Stage06和Stage07拒绝是正确的科学职责履行；验收重点是角色边界和代码合同，而不是
强行发布每篇论文。

## 逐角色结论

- Stage06A：对可构建论文给出目标和闭合workflow；对`63c`保留源材料阻断，没有猜结构。
- Stage06B：对9个可构建任务完成自主表面中性化，保留物理边界；没有产生可见答案泄漏。
- Stage07：9篇均实际写出科学审计和修复；`63c`科学拒绝；未把机械诊断冒充科学裁决。
- 编排器：9篇机械通过并发布，未将安全匿名化差异误判为阻断。

## 第9轮发现的代码问题

`paper_98b6f8a0352f72c2`的最终自主`task_spec`包含公开方法约束和
`public_scientific_method_constraints`，但紧凑的`task_info`没有约束列表，归一化函数
只读取当前文件，导致`task_info.method_disclosure=no_paper_method`。这是代码侧跨文件
投影不完整，不是模型能力问题；第8轮的单文件修复不足以覆盖该压缩投影路径。

其余诊断（开放schema、JSONPath filter和匿名资产hash差异）仍是按设计保留的观察项，
没有阻断科学批准，也不应由代码推断化学含义。第9轮没有出现稳定的Stage07B触发条件。

## 第10轮修复

### 方案

在`canonicalize_mode_task_contract`开始时读取同目录`task_spec.json`一次；当处理
`task_info.json`且自身缺少scope/constraints时，使用task_spec的
`workflow_scope.autonomy_scope`和`method_constraints`推导披露字段。该操作只同步合同
元数据，不改变科学内容、Ground Truth或Agent决定。

### 修改与版本

| 文件 | 修改 |
|---|---|
| `src/stages/stage06_task_builder/validation.py` | 从兄弟task_spec继承scope/方法约束信号，统一紧凑投影。 |
| `tests/test_stage0607_agents.py` | 增加task_info缺少scope但task_spec含约束的回归测试。 |
| `git` | `67bb622 fix(stage06-07): derive compact mode metadata from task spec` |

### 验证

- 专项回归：4 passed（mode contract相关）。
- 全量测试：525 passed。
- 用第9轮`98b`最终产物临时回放：`task_info.method_disclosure`正确变为
  `public_scientific_method_constraints`；原始运行目录未被修改。

## 最终验收判断

截至本轮，没有发现新的通用代码或Prompt合同缺陷；科学拒绝和Agent修复行为符合预期。
下一步只做20篇并发10扩大回归，主要用于检验不同论文类型的角色稳定性。若20篇仍只出现
个别科学判断差异或开放schema diagnostic，不再增加代码死规则；只有出现重复的通用
合同故障才继续修复。Stage07B仍未达到触发条件。
