# Stage06/07 三模型对比报告（paper_6904a9c8c09855cc）

## 测试目录

| 模型 | 运行目录 | Stage06 | Stage07 |
|---|---|---|---|
| DeepSeek-V4-Flash | `runs/stage06-07-objective-centered-test-20260817-paper6904-codex` | constructed | approved_with_repairs |
| DeepSeek-V4-Pro | `runs/stage06-07-revised-20260817-paper6904-pro` | constructed | approved_with_repairs |
| GPT-5.6-sol（配置修复后） | `runs/stage06-07-revised-20260817-paper6904-gpt56sol-configured-r2` | constructed | approved_with_repairs |

旧 GPT 目录 `runs/stage06-07-revised-20260817-paper6904-gpt56sol-final` 保留为故障对照：Stage06/07 工具调用均为 0，分别得到 `provisional_not_constructible` 和 `objective_failure_retryable`。

## Agent 工具调用与 token

| 模型 | Builder calls | Converter calls | Judge calls | 备注 |
|---|---:|---:|---:|---|
| Flash | 65 | 53（两次历史尝试） | 92 + 95 失败 + 56 recovery | 工具调用和恢复次数最高 |
| Pro | 45 | 53 | 71 | 构建完整，Stage07 修复 autonomous 泄漏 |
| GPT configured | 23 | 28 | 19 | 三阶段均成功主动调用工具 |

GPT configured 的 Codex stdout 汇总约为：

- Builder：输入 926,383，缓存命中 612,352，输出 6,805；
- Converter：输入 483,091，缓存命中 386,432，输出 6,916；
- Judge：输入 1,290,152，缓存命中 1,057,664，输出 7,992。

## 质量差异

- Flash 选择了较大的 `major_paper_workflow`，Stage07 做了 3 项 autonomous route disclosure 修复；
- Pro 选择 `full_paper_computational_workflow`，Stage07 修复两模式空 scientific_question、claim ID、excluded-work、复杂度和方法泄漏；
- GPT 选择 `partial_computational_subworkflow`，聚焦第一步 NH3 辅助与分子内 tautomerization barrier，Stage07 保留该 objective-centered workflow，并补齐 reproduction 元数据、过程 rubric 和 toolbox 文件格式；
- 三个模型均保留了结构输入、优化/频率验证、能量/热化学中间产物和最终 barrier/conclusion 的可评分链路；GPT 任务规模较小但仍不是单次调用任务。

## 结论

协议故障已解决：GPT API 不是“不支持 Codex 工具”，而是自定义模型 ID 下 Codex 没有声明内置工具，且旧 bridge 使用 `auto`。配置驱动的 required policy 和兼容工具声明使 GPT 能够主动读写 workspace；DeepSeek 的默认 `auto` 行为保持不变。

当前最值得继续优化的是输入材料的去重/摘要，而不是增加更多死规则：GPT Builder 单篇已接近百万输入 token，若批量使用应优先减少重复 evidence、重复 parser 内容和跨阶段无关文件。

## GPT-5.6-sol 成本粗估

根据 `模型价格表-国外.md` 的 `long_context` 档（输入超过 272K）：输入 $10/M、缓存读取 $1/M、输出 $45/M。按上述 Codex 汇总估算：

- Builder：约 `$4.06`；
- Converter：约 `$1.66`；
- Judge：约 `$3.74`；
- 单篇 Stage06+07 合计约 `$9.46`。

这是按 relay 返回 token 的粗略估算，未计失败重试、网关内部计费差异和未记录的缓存写入；实际账单应以供应商 usage 为准。
