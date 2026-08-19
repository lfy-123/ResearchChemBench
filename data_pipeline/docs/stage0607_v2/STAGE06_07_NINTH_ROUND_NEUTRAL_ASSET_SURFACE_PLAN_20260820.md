# Stage06/07 第九轮自主资产表面修复方案（2026-08-20）

## 1. 触发原因

第八轮回归已通过机械合同和 evaluator 加载，但 autonomous 发布包仍在 `task.md`、`task_spec.json` 和输入表中使用了 `activated-complex candidate`、`minimum`、`product-side`、`reference geometry` 等角色化描述。它们没有泄漏作者软件或数值答案，但会把中性输入预先分类为路线状态，削弱自主模式对状态识别、路径组织和验证设计的评估价值。

这是 Stage06B/Stage07 Prompt 执行不彻底的问题，不增加代码侧化学规则，也不把 candidate 编号与具体论文路线绑定。

## 2. 修改方案

### P1：Stage06B 最终资产角色中性化

要求转换器在 autonomous 公共表面中把每个结构的 `role` 和自然语言描述统一为 `input_geometry`/`public_input` 这类中性表述；只能保留定义科学问题所必需的物理事实（例如电荷、自旋、溶剂和计量关系），不能声明某个文件是过渡态、最低点、产物、反应物、路径位置或作者中间体。

### P2：Stage07 逐文件终审

在六行科学审计表之外，要求 Stage07 对 `task.md`、`task_info.json`、`task_spec.json`、`submission_contract.json`、rubric、manifest、XYZ comment 和文件名做一次语义终审：确认所有资产只以中性公共 ID 出现；若平衡参考必须使用某个 ID，只写计算关系，不把该 ID 命名为某种路线状态。这个检查由 Agent 完成，不由代码关键词表裁决。

### P3：保留必要物理边界

中性化不能删除 THF、温度/压力、总电荷/自旋、原子计量和定义比较所必需的参考组合；只删除作者路线标签和实现方法。自主任务仍可要求 Agent 自己识别哪个输入在频率分析后是 minimum/transition state，并在报告中给出证据。

## 3. 验收与边界

- reproduction 模式保留作者路线和状态标签；
- autonomous 模式不含作者方法、路线顺序、答案值或状态角色标签；
- 代码只负责运输、路径、manifest、schema 和发布，不新增论文/分子关键词规则；
- 使用 DeepSeek-v4-pro-0813 + Codex 对 paper 6904 做一次回归，检查 Stage07 是否实际修复该问题；
- 若仍只剩模型偶发漏审，不继续扩张代码，记录为 Prompt/模型能力问题；最多五轮。

## 4. 修改记录

待第九轮 Prompt 修改、测试和轨迹分析后追加。
