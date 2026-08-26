# Stage06/07 v17 十篇论文测试结果分析

## 测试与判定口径

批次：`runs/stage0607-v17-gpt-5.6-sol-20260826`。Stage06A、Stage06B、Stage07 均使用 `gpt-5.6-sol`，推理强度 `high`，并发 4，输入为此前相同的十篇 Stage05 候选论文。

本报告以每篇已经落盘的 Stage06/Stage07 summary、audit receipt 和任务包为事实依据。批次父进程在最后一篇完成前退出，所以批次级 `batch_status.json` 不是完整终态；最后一篇另行标记为基础设施失败，未伪造科学结论。

## 总体结果

| 论文 | Stage06 | Stage07 / 发布 | 原因 |
|---|---|---|---|
| `paper_2aca1dd116799b28` | 构建；A/B Gate 通过 | `approved_with_repairs`；两种模式发布，`approved_needs_software` | 仅缺 Gaussian 或等价软件依赖，不是 Gate 阻断 |
| `paper_308bbee002d4560c` | `provisional_not_constructible` | 未运行（预期） | 缺 charge/multiplicity，坐标传输异常，TS6 endpoint/IRC 不闭合 |
| `paper_30cec9ecf4782412` | `provisional_not_constructible` | 未运行（预期） | 缺有限片段边界、端基、charge、multiplicity，中心偶极无法无猜测构建 |
| `paper_3590deded767345e` | 构建；A Gate 报告 evaluator 问题 | `rejected_scientific_unrepairable` | 44.8 kcal/mol 被绑定到错误的 N–O scission 分支；真正 TS 未找到，修复需换目标/工作流或猜答案 |
| `paper_611000e1de080f6f` | 构建；A/B Gate 通过 | Stage07 科学通过；原 assembler 阻断；修复后无模型重组两种模式均通过 | Stage06 私有 `data[*].role` 进入严格 TaskInfo v1；现在在包边界过滤 |
| `paper_76ae2dc25f0a5aeb` | 构建；A Gate 捕获 2 个 evaluator 问题 | `approved_with_repairs`；两种模式发布 | frequency 规则类型/形状错误，`con_ddg` 缺规则；Stage07 在原目标内修复 |
| `paper_8b7bf002cc6a4ba9` | `provisional_not_constructible` | 未运行（预期） | Stage06 科学可执行性不足 |
| `paper_9455a82229de2427` | 构建；Gate 通过 | `approved_with_repairs`；两种模式发布 | 修复 species-specific numeric binding、ordering proposition 和 submission schema |
| `paper_9ec8c4761c4f171b` | `provisional_not_constructible` | 未运行（预期） | 选定 workflow/输入不能闭合；不允许 Stage07 猜测重建 |
| `paper_a5564360a31f760b` | 构建；A/B Gate 通过 | 未完成 | Stage07 动态 API 端口 `41675` 已拒绝连接，Agent 等待响应；属于 harness/API 失败，不是科学拒绝或 Gate 失败 |

九篇已完成论文的统计为：Stage06 科学构建 6 篇、不可构建 3 篇；进入 Stage07 的 6 篇中科学通过 5 篇、科学拒绝 1 篇。原批次包发布成功 4 篇，`paper_611...` 仅因旧 assembler 失败；当前 assembler 无模型重组后，该篇两种模式均 `passed`。因此代码修复后已有 5 篇发布候选，另 1 篇需重新执行 Stage07，3 篇应保持科学拒绝/不可构建。

## 逐篇归因

### `paper_2aca1dd116799b28`

三系统 Bergman 环化任务的科学目标、九个 XYZ 输入、气相中性单重态边界和 evaluator 均闭合。Stage07 的两项 bounded repair 是：删除 autonomous 中作者特定 B3LYP/QST3 路线，保留验证义务；对齐 autonomous process rubric 的 key-point ID。三条 per-system numeric 规则和一条 exact ordering 规则均有具体 target、单位、容差、binding。发布通过；Gaussian 缺失被正确记录为软件依赖。

### `paper_308bbee002d4560c`

输入不包含完整电子态信息，坐标表传输和 TS6 endpoint/IRC 也不闭合。Stage07 不运行是正确行为；若继续会迫使模型猜 charge/multiplicity 或结构，违背“只审计/有限修复”。

### `paper_30cec9ecf4782412`

`missing_source_input` 的根因是中心偶极对象缺唯一有限片段边界、端基、charge 和 multiplicity。不是 JSON 或路径问题，不能由 Gate 放宽解决。

### `paper_3590deded767345e`

Stage06A 已报告结论 supporting key point 和两个 binding selector 缺失。Stage07 进一步确认科学错配：44.8 kcal/mol 属于另一条 nitrite N–O scission 分支，而 `intA→3Ph*` 的真正 TS 未找到，SI 对应 cell 为空。该缺陷只有换 scored quantity/workflow 或猜测答案才能补齐，因此拒绝且不重建，符合 v17 设计。

### `paper_611000e1de080f6f`

科学审计和四条 numeric evaluator 规则均通过。原失败是严格 `TaskInfoV1` 拒绝 autonomous `task_info.json` 中私有的 `role=input_geometry` 字段。`src/stages/stage07_task_judge/package.py` 现在只向公共包投影 `name/path/type/description`；重新组装结果：paper reproduction `passed`，autonomous research `passed`。无需再次调用模型。

### `paper_76ae2dc25f0a5aeb`

Stage06A checker 捕获了真实合同错误：两个计数的 numeric map 被声明为 `condition`，且 `con_ddg` 没有 scoring rule。Stage07 将 frequency 修为 numeric map（count、zero tolerance），并补充 `con_ddg` numeric binding；目标和输入不变，最终 Gate 通过。

### `paper_9455a82229de2427`

Stage07 为四个独立能量补 species-specific result field binding，为 ordering 写入 `P1 lower than P2` proposition，并在两种 submission contract 声明 selector。CBS-QB3 目标、四个 XYZ 输入和反应能定义均未改变，最终 crosswalk 完整，两种模式发布成功。

## reproduction → autonomous 检查

已发布或重组通过的四篇都保留同一个科学目标、物理输入、reference 和结果交付，只对 public surface 做转换：删除作者路线、私有证据 ID 和答案泄露，使用中性输入名，保留 `report/results.json` 与 `report/report.md`。`paper_2aca...` 的 autonomous 已移除 B3LYP/QST3；`paper_76...` 和 `paper_611...` 仍出现方法约束，是其 conversion contract 声明的 problem-defining constraint，不是路线泄露。

## 剩余工程问题

1. **API runner 无穷等待。** `paper_a556...` 的 41675 端口拒绝连接，但 Stage07 Agent 没有快速写出 technical-failure receipt，导致悬挂。需要在 runner 层增加连接/调用超时并落盘明确技术失败；不要用 retry 或续接对话掩盖。
2. **批次状态枚举误报。** 旧 helper 把 Stage06 科学拒绝记为 `FAILED stage07_not_run`；应改成明确的科学拒绝终态。
3. **兼容性 warning 表达。** `split_reference_compatibility_projection_warning:ValidationError` 不阻断发布，但应作为非阻断诊断单独呈现，避免被误认为 Gate 失败。

## 验证

```text
python -m pytest -q tests/test_stage0607_v17* tests/test_stage0607_v13_split_reference.py tests/test_stage0607_v8_task_packages.py
27 passed
```

此前 v17 定向回归为 `72 passed`，其中新增 v17 覆盖为 `22 passed`。对 `paper_611...` 使用当前 assembler 的无模型重组验证为：

```text
paper_reproduction: passed
autonomous_research: passed
```

结论：v17 已解决 Stage07 重建导致的科学边界失控，以及科学通过后被 package boundary 机械阻断的主要问题；剩余问题集中在 API runner 的失败收敛、批次状态分类和非阻断 warning 的表达。
