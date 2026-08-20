# Stage06/07 第1轮共性合同与机械Gate修复方案

日期：2026-08-21

基线：be07585

## 本轮目标

修复批量结果暴露的通用运输合同、机械检查和状态记录问题；不修改论文科学规则，不改变Stage07 Agent的科学裁决权，本轮暂不实现Stage07B。

## 已确认的共性问题

1. 机械Gate逐字比较两个模式的 required_files，并对输入做原始字节哈希，导致自主安全脱敏被误报为 mode_pair_submission_contract_mismatch 或 mode_pair_input_assets_mismatch。
2. submission contract存在 required_file、primary_file、required_artifacts 等别名，rubric存在 criteria/items 包装。
3. evaluator dry-run主要验证schema加载，没有确认 observed_fields 是否能落到 results_schema 的实际字段。
4. Agent批准但机械阻断的单篇记录缺少统一 publication_state 和 blocking_phase。

## 修改方案

### 1. 收窄模式比较

- 每个模式单独验证required_files、路径安全、合同和公开目录。
- 两模式不再逐字比较 required_files 和 submission_path。
- 结果schema只比较中性结构；名称差异写diagnostic，不阻断。
- 输入跨模式差异只写diagnostic，不由代码判断科学等价性；输入是否被误删交Stage07依据正文/SI和私有映射审计。

### 2. 运输字段归一化

- 将 required_file、submission_file、primary_file、required_artifacts、artifact_paths 投影到 required_files。
- 将 criteria/items/rubric包装投影为顶层数组。
- 只变换字段和容器形状，不修改科学数值、结论、排序、容差或Ground Truth。

### 3. evaluator binding观察

- 支持 $.field、$.nested.field 和简单数组下标。
- 支持 submission_bindings_by_mode，并回退到共同 submission_binding。
- 显式schema中不存在的绑定字段产生finding。
- 开放schema只产生diagnostic；空且未声明开放属性的schema在存在binding时产生unbound finding。

### 4. 发布状态

增加 publication_state（not_applicable、publish_ready、mechanical_blocked、published）和 blocking_phase（prepublish_mechanical、published_bundle），不改变Agent的audit_decision。

### 5. Prompt

要求Stage07最终重新读取task_info、submission_contract、process_rubric、results_schema和每个Ground Truth binding；无法确定绑定时保留finding，不得仅凭receipt自报passed。

## 验证

- 增加安全脱敏、合同别名、rubric包装和JSONPath错误绑定测试。
- 运行Stage06/07测试全集和compileall。
- 不修改历史运行结果，不修改Stage00–05。

## 暂不处理

Stage07B暂不实现，先观察10篇测试是否仍稳定出现可窄修的合同阻断；不将化学计量、物理边界或参考态写成代码死规则。

