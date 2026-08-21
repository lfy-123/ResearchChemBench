# Stage06/07 第8轮代表性回归分析

## Git与目标对照

- 代码基线：`d89fc3a`（随后在第9轮修复为 `6d7404c`、`1191846`）。
- 目标文档：`STAGE06_07_ITERATION_OBJECTIVES_AND_ACCEPTANCE_CRITERIA_20260821.md`。
- 对照重点：职责边界、双模式隔离、最小机械合同、科学审计由Agent完成，以及不引入论文特例规则。

## 测试配置

- 输出：`runs/stage06-07-v4-round8-deepseek5-concurrency10-20260821`
- 模型：`deepseek-v4-pro-0813`
- Harness：Codex；推理强度：high；并发：10（实际5篇）
- 样本：从第6轮/第7轮不同结果类别中选取 `03455526`、`575b732`、`585288a`、`7574d997`、`9e76a3b`。

## 结果统计

- CLI完成：5/5；运行失败：0
- Stage06 provisional constructed：5/5
- Stage07 scientific approved_with_repairs：5/5
- scientific rejection：0
- mechanical contract passed：5/5
- published：5/5
- Stage07B：未实现、未触发

## 逐篇审计

| 样本 | 主要结果 | 代码/Prompt/模型归因 |
|---|---|---|
| `03455526` | Stage07修正了SCF目标定义、模式绑定和自主字段中性化；机械通过。开放schema相关项仅为diagnostic。 | 代码与Prompt符合预期；科学修复由Agent完成。 |
| `575b732` | 修正提交字段、mode-specific binding和TS保留型优化；能量与SI文字存在源材料矛盾，Agent记录为非阻断观察。机械通过。 | 源材料/科学事实矛盾，不是代码缺陷。 |
| `585288a` | 修正原子标签配对、XYZ注释、结果schema和binding；任务可发布。 | Agent科学修复有效；但最终自主元数据出现方法约束与`no_paper_method`不一致，属于代码归一化缺陷。 |
| `7574d997` | 文档型报告绑定不再被误判；修正自主结论提示、普通字符串requirements和发射波长绑定；机械通过。 | 第7轮代码修复有效。 |
| `9e76a3b` | 修正自主Bader/DFT标签、字段绑定和模式评分；机械通过。过滤JSONPath和模式输入hash差异均为diagnostic而非阻断。 | 代码按设计提供观察，科学语义由Agent处理。 |

## 第8轮发现的问题及归因

### 已解决/无共性缺陷

1. 文档型`observed_fields`不再被当成错误JSONPath；`7574`成功发布。
2. mode-specific Ground Truth binding在真实任务中可用；没有出现第7轮`034`式机械阻断。
3. 自主公开面保留物理边界，删除作者路线和答案提示；未发现固定论文、分子或数值规则。
4. `task.md`中的JSON文件名仅作为“不要读取第二指令源”的否定提醒，不构成第二任务指令。

### 需要修复的通用缺陷

`585288a`的自主`task.md`和`task_spec.method_constraints`明确要求CAM-B3LYP/cc-pVTZ，
但`task_info.method_disclosure`仍为`no_paper_method`，且`task_spec.workflow_scope`被Agent
重写后缺失。这是归一化逻辑只读取`workflow_scope.autonomy_scope`、没有把非空公开
`method_constraints`作为约束信号的代码/协议问题；不是模型不会做科学选择。

其余`evaluator_binding_schema_open`、复杂filter未检查和模式输入hash差异均是已记录的
诊断信息：开放结果schema、过滤表达式和中性文件名差异不能由编排器臆测科学语义，不能升级
为代码侧科学拒绝。

## 第8轮结论

第8轮没有发现需要Stage07B的稳定阻断类别：5/5的机械合同均通过，且阻断前的安全等价性
已由主流程修复。进入第9轮，仅修复方法约束元数据投影，并在Prompt中要求最终自主
`workflow_scope.autonomy_scope`显式存在；不新增论文特例规则，不扩大代码科学裁决范围。
