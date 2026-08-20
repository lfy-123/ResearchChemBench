# Stage07B 合同修复 Agent 设计方案

日期：2026-08-20

## 1. 是否有必要

有必要，但它不是新的科学审计阶段，也不是用来绕过机械 gate 的“放行 Agent”。

本批次表明：Stage07 已经对一部分任务作出科学批准，但其最终文件仍无法加载或发布；同时，当前机械 gate 又把安全脱敏误报为模式不一致。如果所有机械 finding 都重新调用 Stage07，成本高且会重复科学阅读；如果直接忽略 finding，则会发布真实坏包。

因此需要一个一次性的窄职责 Stage07B，专门处理：

> Stage07 已批准、科学内容不需要重新裁决、但运输合同或可验证绑定仍未闭合的任务包。

Stage07B 不应处理 Stage07 科学拒绝，也不应处理 Stage07 尚未完成或 API/文件系统失败的任务。

## 2. 目标与非目标

### 目标

- 将科学上已批准的任务投影为 evaluator 可加载、可发布的合同；
- 修复字段类型、目录树、路径、模式身份和明显 binding 结构错误；
- 区分安全脱敏造成的表面差异与真正科学输入缺失；
- 保留 Stage07 的科学决策，不让编排器替换 Agent 的科学判断；
- 一次修复后给出明确的 publish-ready 或 mechanical-blocked 终态。

### 非目标

Stage07B 不得：

- 重新选择 scientific objective 或 workflow scope；
- 修改科学问题、Ground Truth 数值、结论、排序或容差；
- 猜测缺失结构、参考态、物理边界或论文结果；
- 重新决定任务是否科学可用；
- 用论文标题、分子名或关键词写死规则；
- 因为 Agent 自报 approved 就强制发布。

## 3. 推荐工作流

```text
Stage06A 科学构建
        ↓
Stage06B 自主公共表面转换
        ↓
Stage07 科学审计/科学修复/科学拒绝
        ↓
最小机械观察与确定性运输归一化
        ├─ 通过 → 发布
        └─ 阻断且 Stage07 科学批准
                    ↓
              Stage07B 合同修复 Agent（最多一次）
                    ↓
              机械检查 + evaluator schema/binding 检查
                 ├─ 通过 → 发布
                 └─ 失败 → mechanical_blocked_unresolved
```

Stage07B 不应形成无限循环，也不应触发完整 Stage07 重跑。

## 4. Stage07B 输入

Stage07B读取：

1. Stage07最终任务包；
2. Stage07审计 receipt 和机械 finding；
3. `audit_index.json`；
4. evaluator合同/schema定义；
5. Stage06 handoff中的 `public_to_private_asset_map`、转换记录和必要的源材料映射；
6. 必要时只读正文/SI，用于判断“文件是否只是匿名化”或“科学输入是否被删除”。

源材料和私有映射仅用于修复判断，不得复制到任一公开模式目录。

## 5. Stage07B可修复的问题

### 5.1 运输字段和文件结构

- 补齐 evaluator 明确要求、且可由已有任务身份确定的运输字段，例如 `category`、`task_pair_id`、模式派生字段；
- 将 rubric 从包装对象投影为正式顶层数组；
- 将 `required_file`、`primary_file`、`required_artifacts` 等明显别名统一为正式 `required_files`；
- 修复相对路径、提交目录和公开目录中的 staging/handoff/hidden_reference 残留；
- 重新生成 manifest/hash，但不改变科学载荷。

### 5.2 安全脱敏等价性

- 将作者文件名转换成中性公共文件名；
- 将答案无关的 JSON 标签、来源标签、路线角色名中性化；
- 保留坐标、SMILES、分子式、电荷、多重度、实验观测、溶剂/温度/压力等问题定义事实；
- 用私有映射记录前后资产对应关系。

若发现文件被删除、原子/连接/数值改变或必需边界条件丢失，Stage07B不得自行补造，必须返回 unresolved，交由 Stage07 科学修复或拒绝。

### 5.3 结构化 binding

- 检查每个 Ground Truth item 是否有唯一的 mode-specific artifact/field binding；
- 检查支持的 JSONPath 是否能落到 `results_schema` 的真实字段；
- 检查类型是否与 numeric/text/document acceptance profile兼容；
- 检查两个模式的字段名可以不同，但科学 key point 和绑定角色必须可对应。

只修复可以从现有字段和私有映射确定的错误，例如 `$ .value` 应绑定到任务合同中唯一的数值字段。无法唯一确定时不得猜测。

## 6. Stage07B输出合同

输出一个简短的 `stage07b_repair_receipt.json`，至少包含：

```json
{
  "decision": "repaired_and_ready | unresolved_mechanical_block",
  "source_stage07_decision": "approved_with_repairs",
  "findings_before": [],
  "repairs": [
    {
      "category": "schema | path | disclosure_surface | binding | asset_equivalence",
      "details": "...",
      "changed_files": [],
      "evidence_ids": []
    }
  ],
  "findings_after": [],
  "scientific_content_changed": false,
  "publish_ready": false,
  "remaining_issues": []
}
```

`scientific_content_changed`必须始终为`false`。如果修复需要改变科学内容，Stage07B必须返回 `unresolved_mechanical_block`，而不是把修改写入任务包。

## 7. 机械 gate配套调整

Stage07B只有在 gate 比较语义先修正后才有意义：

1. `required_files`比较交付角色/类型/绑定，不逐字比较自主文件名；
2. 输入比较使用规范化科学载荷，而不是对所有JSON做原始字节哈希；
3. gate提供 findings 和 diagnostics，不生成科学 approve/reject；
4. evaluator dry-run至少检查支持的JSONPath是否存在于结果schema；
5. `approved + blocked`必须在 summary中显式记录 `mechanical_publish_blocked` 和 `mechanical_approved_but_unpublished`。

否则 Stage07B会被迫反复修复由 gate 自己制造的误报。

## 8. 触发条件与终止条件

### 触发

同时满足：

- Stage07科学决策为 `approved`、`approved_with_repairs` 或 `approved_after_workflow_redesign`；
- Stage07已有完整任务包；
- 机械 gate仅报告合同、路径、公开树或binding问题；
- 没有科学输入缺失、科学目标未闭合或API/文件系统执行失败。

### 不触发

- Stage07为 `rejected_scientific_unrepairable`；
- Stage07为 `objective_failure_retryable`；
- finding表明输入资产被删除或科学内容改变且无法由私有映射恢复；
- finding需要修改 Ground Truth 数值、容差、结论或workflow。

### 终止

- 最多一次 Stage07B Agent尝试；
- 修复后再次运行机械检查；
- 通过则发布；
- 仍失败则写 `mechanical_blocked_unresolved`，保留所有 findings，不再自动重试。

## 9. 成本控制

- 首次调用只读取 `audit_index.json`、机械报告和合同摘要；
- 使用分组 Python 检查，不逐文件重复打印；
- 不重复阅读整篇论文，除非需要判定输入等价性；
- 不生成第二份完整 process trace；
- 一次修复、一轮复检，不进入 Stage07/Stage07B循环。

## 10. 回归测试要求

至少建立以下通用 fixture：

1. 缺 `category`、缺 common GT、rubric包装错误：Stage07B应修复或明确 unresolved，不能发布未闭合包；
2. 安全文件名/JSON标签脱敏：不得再触发误报；
3. 删除SMILES或必要输入：必须保持阻断；
4. 空 `results_schema` 或 `$ .value`错绑：必须被发现；
5. 公开目录含 `hidden_reference`：必须阻断；
6. 科学拒绝和运行失败：不得进入Stage07B。

## 11. 最终建议

应增加Stage07B，但先修正机械gate的比较语义和binding观察能力，再接入Stage07B。Stage07B的正确定位是“一次性合同修复与等价性确认 Agent”，而不是新的科学审计者或发布裁判。科学权利仍归Stage07，发布权由最终机械状态决定。

