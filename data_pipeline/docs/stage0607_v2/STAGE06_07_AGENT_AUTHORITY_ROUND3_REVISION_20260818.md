# Stage06/07 Agent Authority — Round 3

## Round 2 真实测试

- 代码：`e7fb258`
- 论文：`paper_6904a9c8c09855cc`
- 模型：`deepseek-v4-pro-0813`
- Stage06：`provisional_constructed`，核心子流程为 first N-H tautomerization barrier。
- Stage07：`approved_with_repairs`，`selected_workflow_preserved=true`，`toolbox_status=available`，`resource_status=feasible`。
- 发布：论文复现和自主科研两个目录均成功生成；没有再次被代码侧 semantic validator 否决。
- Agent 工具调用：Builder 34、Converter 31、Stage07 45；Stage07 约 3.03M tokens。

## 剩余通用问题

Stage06A Builder 的 Agent workspace 输入仍有 212 个文件、约 27.4MB，其中包括 105 张 JPG（约 17.6MB）、2 个 PDF（约 3.1MB）和 parser_structured JSON（约 5.5MB）。这些材料与 normalized Markdown、pypdf layout、derived tables/coordinates 重复，增加目录扫描和上下文选择成本。

## Round 3 修改

- Stage06A 默认提供 text-first source packet：保留 normalized/layout text、content blocks、derived tables/coordinates、metadata、evidence index、toolbox 和脚本。
- 默认排除 `images/`、`parser_structured/`、PDF 副本及 supplementary PDF。
- 增加 `stage06_include_visual_fallback` 配置开关；需要处理无法由结构化文本确认的图像/版面证据时可显式打开，不限制 Agent 的科学判断。
- 在 `visible_input_manifest.json` 中记录排除内容，方便追溯。
- 不改变 workflow 选择、科学判断、任务文件合同或 Stage07 Agent 权限。

## 验收

- 默认 Builder 输入不再包含 JPG/PDF/parser_structured。
- 显式 fallback 开关仍保留这些材料。
- 全量 pytest 通过。
- 用同一论文和 Pro-0813 做最后一次测试；若成功，停止迭代，不再添加论文特例。

| 版本 | Git commit | 测试状态 | 结果 |
|---|---|---|---|
| Round 3 | `d758b20` | Pro-0813 待运行 | 待运行 |

本地验证：Stage06/07 定向测试 121 passed；全量测试 506 passed。

### Round 3 最终测试结果

- 输出：`runs/stage06-07-agent-authority-round3-20260818-paper6904-pro0813`
- Stage06：`provisional_constructed`；Builder 输入从 Round 2 的 212 文件/27.4MB 降为 97 文件/1.81MB，保留 normalized/layout text、derived tables/coordinates 和必要脚本。
- Stage06 Agent 调用：Builder 41 次、2.37M tokens；Converter 25 次、0.77M tokens。输入显著缩小，但模型本次自主检索更充分，调用数不按比例下降，这是模型轨迹差异而非代码失败。
- Stage07：`approved_with_repairs`，`selected_workflow_preserved=true`，`toolbox_status=available`，`resource_status=feasible`，无 retry；82 次调用、约 5.04M tokens。
- 发布任务：论文复现目录 11 个文件，自主科研目录 8 个文件；不含 hidden reference、source materials、public manifest 或内部 handoff。
- Stage07 本次修复了自主输入命名/泄漏、submission binding、hidden policy、acceptance profile 和 manifest；最终 Agent 决策成功原样发布。

本轮达到设计目标。按照“最多三轮”约束停止代码迭代；Stage07 调用量的波动属于 Agent 科学审计路径差异，不再添加死规则压低调用量。
