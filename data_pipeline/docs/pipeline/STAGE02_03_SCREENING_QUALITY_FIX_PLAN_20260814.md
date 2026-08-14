# Stage02/03 筛选质量修正方案

日期：2026-08-14

状态：用户已确认改进方向，待按本文实施与回归

## 1. 目标与边界

本轮只修正 Stage02 和 Stage03 已观察到的通用误判，不改变两个阶段的主流程：

- Stage02 判断论文是否为原创研究，并确认作者是否实际完成了完整、非平凡的计算化学工作流；
- Stage03 将 Stage02 冻结的工作流绑定到论文明确报告的软件，并只排除核心计算软件明确不在工具箱中的工作流；
- Stage03 不重新判断计算流程完整性，不审查资源成本；资源和最终可构建性仍由 Stage05 处理；
- 不添加 DOI、标题、期刊或单篇论文专用规则；
- 不在 Stage02 增加“计算化学领域边界”分类。只要作者完成的工作流满足现有计算化学证据合同，即按原有标准处理，不要求模型再判断其属于哪个计算化学子领域。

本轮不修改 Stage00、Stage01、Stage04、Stage05、Stage06、Stage07 的筛选语义。

## 2. 已确认的问题

### 2.1 Stage02：非原创论文可能被第二次调用重新放行

Stage02 首次分类已经能把 `article_role=review` 判为不通过，但当前第二次工作流验证可以覆盖第一次结果。验证器只检查计算工作流轴，没有锁定文章类型。因此，综述中对他人计算过程的完整描述可能被错误解释为作者实际完成的工作，并改写成通过标签。

问题不是计算化学领域范围，而是两个独立事实被混在一起：

1. 文献是不是原创研究；
2. 原创研究中是否存在作者执行的完整计算工作流。

两者必须同时成立，且工作流验证不能修改文章类型。

### 2.2 Stage03：辅助工具参与了核心软件否决

当前工作流门控把以下三个角色都计入阻断集合：

- `core_compute`
- `required_preprocessing`
- `required_analysis`

这会使 Gaussian、ORCA、VASP 等核心引擎已经覆盖的论文，因为 GaussView、IBOview、ChimeraX、AutoDockTools 等准备、查看或分析工具不在工具箱而被拒绝。Stage03 的职责只是核心计算软件的早期负向排除，这些辅助依赖应记录并交给 Stage05 判断任务是否真的可构建。

## 3. Stage02 修改方案

### 3.1 冻结文章类型

Stage02 首次分类后生成不可被验证器改写的文章类型状态：

- `original_research`：允许继续工作流验证；
- `review`、`correction`、`editorial`：最终统一输出 `non_original_article`，不得通过；
- `unknown`：保持 `uncertain`，不得由工作流验证直接升级为通过。

确定性首页/标题识别继续作为零调用快速路径。模型识别出的非原创类型则在第二次调用后再次执行最终硬门控，以覆盖确定性规则未识别的综述、Perspective、Commentary 等情况。

### 3.2 限制第二次调用的权限

工作流验证器只验证冻结候选的以下事实：

- 作者实际执行计算；
- 化学体系可识别；
- 存在实际计算或模拟；
- 计算产生新的化学结果；
- 结果被用于论文科学结论；
- 工作流不是实验数据处理或平凡后处理。

验证器不得：

- 把 `review/correction/editorial` 改成原创研究；
- 用综述中对他人工作的描述建立作者工作流；
- 在第一次调用未识别候选时发明替代工作流；
- 修改 Stage02 的领域范围。

如果首次分类与验证器冲突，按以下方式处理：

- 非原创类型具有最高优先级，结果为 `non_original_article`；
- 文章类型未知时结果为 `uncertain`；
- 原创研究的工作流轴冲突继续按现有证据合同裁决；
- API/JSON/token 失败仍为可恢复处理失败，不能解释成无计算内容。

### 3.3 输出一致性

最终写盘前执行一次论文级一致性归一化：

- `decision=non_original_article` 时 `passed=false`；
- 非原创或文章类型未知时 `confirmed_workflows=[]`；
- 顶层 `decision`、`passed`、`review.decision`、`review.passed` 保持一致；
- 保留原始两轮响应和冲突原因，方便审计；
- 新增/保留文章类型证据来源，不删除计算证据。

这样即使未来需要从综述中回收引用线索，统一记录仍保有模型输出，但综述不会进入 Stage03。

### 3.4 Prompt 调整

第一次调用明确要求：

- 先判断文章类型，再判断作者自己的工作；
- 综述对既有计算的详细复述不等于作者执行计算；
- 原创研究中的引用背景与作者方法必须通过证据归属区分。

第二次调用增加只读 `article_role` 和文章类型证据，要求原样返回确认；代码不信任其改写结果。只要求输出结构化检查结论，不要求展示思维链。

## 4. Stage03 修改方案

### 4.1 只让核心计算依赖阻断

将阻断角色缩小为：

```text
core_compute
```

以下角色全部记录但不参与 Stage03 拒绝：

```text
required_preprocessing
required_analysis
optional_auxiliary
visualization
instrumentation
background
unknown
```

普通可视化、GUI、结构查看、文件准备和结果展示工具不能成为 `core_compute`。如果一个扩展或插件实际改变核心科学计算，例如论文明确要求某个求解器扩展执行溶剂化计算，则它仍可被模型标为 `core_compute`，并按核心依赖审查。

### 4.2 工作流级通过规则

每个冻结工作流独立计算状态：

- `workflow_covered`：核心计算软件均覆盖；
- `workflow_coverage_probable`：核心软件名称可以高置信度映射但仍有轻微名称不确定性；
- `workflow_software_inventory_unconfirmed`：核心软件未报告或名称不能确认；
- `workflow_uncovered`：至少一个明确、实际使用、绑定到该工作流的 `core_compute` 软件不在工具箱。

论文级结果：

- 任一工作流为 covered，则 `software_covered`；
- 否则任一工作流为 probable，则 `software_coverage_probable`；
- 否则存在 unconfirmed，则 `software_inventory_unconfirmed`；
- 只有所有冻结工作流均为 uncovered，才输出 `core_software_uncovered`。

未报告软件继续通过到后续阶段，不因软件缺失直接拒绝。

### 4.3 审计字段

每个工作流分别保存：

- `core_software_results`：实际参与门控的核心软件；
- `nonblocking_software_results`：预处理、分析、可视化和辅助软件；
- `step_results`：冻结步骤的软件绑定状态；
- `status`：只由核心软件状态决定。

为兼容历史消费者，原 `required_software_results` 暂时保留，但其内容改为核心依赖别名，或在迁移期与 `core_software_results` 保持一致。Stage05 继续从完整 `software_mappings` 读取非阻断依赖。

### 4.4 软件名称规范化

名称解析只采用通用、可审计转换：

- 去除版本、revision、平台后缀和不配对的尾部括号；
- 合并“全称（缩写）”并同时尝试全称与缩写；
- 只使用冻结工具箱目录及其别名做精确/规范化映射；
- 方法、模块、算法和模型不得自动升级为独立软件；
- 无法可靠映射时标记 `unconfirmed`，不能猜成 covered 或 uncovered。

不为某篇论文或某个错误拼写写专用分支。需要新增别名时，应更新可复用的软件目录/别名数据并附来源。

### 4.5 Prompt 调整

Stage03 prompt 明确区分：

- 核心科学引擎：真正执行 DFT、MD、量子化学、动力学、对接等核心计算；
- 辅助依赖：输入准备、GUI、结果查看、绘图、格式转换或可替代后处理；
- 只有前者应标为 `core_compute`；
- GaussView/IBOview 类型工具即使实际使用，也通常是非阻断辅助项；
- 模型只抽取角色，最终覆盖决策由代码和冻结工具箱目录完成。

## 5. 测试计划

### 5.1 单元测试

Stage02 至少覆盖：

1. 首次分类为 review、验证器给出完整工作流，最终仍为 `non_original_article`；
2. article role 未知、验证器给出通过，最终保持 `uncertain`；
3. 原创研究且工作流六轴确认，仍按原有四类通过；
4. 非原创结果不携带 `confirmed_workflows`；
5. 顶层和 `review` 的 decision/passed 一致。

Stage03 至少覆盖：

1. Gaussian 覆盖、GaussView 未覆盖，工作流仍 covered；
2. ORCA/Multiwfn 覆盖、IBOview 未覆盖，工作流仍 covered；
3. 核心 Molpro 未覆盖，工作流 uncovered；
4. 一个 covered 工作流加一个 uncovered 工作流，论文通过；
5. 核心软件未报告，结果 unconfirmed 并继续；
6. 非阻断依赖仍完整保存在审计输出中。

### 5.2 历史 Stage01 回归

使用已停止任务的 Batch 1 Stage01 产物作为冻结输入，在独立回归目录重跑 Stage02 和 Stage03，不覆盖历史结果。比较：

- Stage02 决策分布、通过率和非原创文章数量；
- 原先被第二次调用从 review 改成通过的论文是否被阻断；
- Stage03 covered/probable/unconfirmed/uncovered 分布；
- 仅因预处理、分析或可视化软件未覆盖而拒绝的论文数量是否降为 0；
- 真正核心后端未覆盖的论文是否仍被拒绝；
- 模型调用失败、输出截断和结果合同错误数量。

至少人工抽查：所有 Stage02 非原创结果、所有 Stage03 uncovered 结果，以及由旧版 uncovered 变为通过/不确定的论文。回归只验证通用规则，不据此加入论文特例。

## 6. 验收标准

代码进入新批次前必须同时满足：

1. Stage02 不存在非原创文章被验证器重新放行；
2. Stage02 没有新增计算化学领域边界负担；
3. Stage03 的工作流状态只受核心计算软件约束；
4. GaussView、IBOview 等非核心工具不会单独导致拒绝；
5. 所有核心软件明确不覆盖的工作流仍能稳定拒绝；
6. 未知软件保持 unconfirmed 并继续；
7. 相关单元测试通过；
8. 历史 Stage01 回归无处理异常，人工抽查结果符合职责边界。

满足以上条件后，使用新的 run ID 重新提交 Stage00-Stage05 全流程；旧运行目录只读保留用于审计，不作为新运行缓存。
