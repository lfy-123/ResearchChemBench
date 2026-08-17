# Stage06/07 模型协议策略实现记录（2026-08-17）

## 目标

让不同模型通过配置选择不同的 Agent 协议参数，尤其解决 GPT-5.6-sol 在自定义中转 API 上因 Codex 使用 `auto` 且未声明内置工具而零工具结束的问题，同时保持 DeepSeek 的既有调用方式。

## 本轮实现

### 配置驱动

在 `models.<role>` 增加并校验：

- `codex_wire_api`: `chat_completions` 或 `responses`；
- `tool_choice_policy`: `auto`、`required_until_artifact`、`required`、`none`；
- `response_format_policy`: `auto`、`json_schema`、`json_object`、`none`。

环境变量可按角色覆盖：

```text
RCB_BUILDER_CODEX_WIRE_API
RCB_BUILDER_TOOL_CHOICE_POLICY
RCB_BUILDER_RESPONSE_FORMAT_POLICY
RCB_JUDGE_CODEX_WIRE_API
RCB_JUDGE_TOOL_CHOICE_POLICY
RCB_JUDGE_RESPONSE_FORMAT_POLICY
```

优先级为：phase 显式覆盖 > 模型角色配置/环境变量 > 默认值。阶段配置中的旧 `codex_wire_api` 不再覆盖模型级协议选择。

### Bridge 行为

- `tool_choice_policy` 由 `ResponsesBridge` 在每个 upstream 请求上设置；
- `required_until_artifact` 在 artifact 未完成时设置 `tool_choice=required`，完成后恢复自动/终止路径；
- `response_format_policy` 独立控制 JSON Schema、JSON Object 或关闭响应格式；
- 当 Codex 对自定义模型 ID 发送空 `tools` 列表时，仅在显式 `required`/`required_until_artifact` 策略下补充兼容的 `exec_command` 声明；DeepSeek 默认 `auto` 不走该路径；
- Codex CLI 始终使用它支持的 `responses` wire 连接本地 bridge；模型级 `codex_wire_api` 只决定 bridge 到上游的协议，避免把 `chat_completions` 错传给 Codex CLI。

### 认证与直连

当选择直连 upstream Responses（bridge 不启用）时，Codex 子进程才会获得该角色的 `OPENAI_API_KEY`；bridge 模式下密钥仍只留在 Python bridge 进程中。

## 验证过程

### 回归测试

```text
PYTHONPATH=. pytest -q tests/test_stage0607_agents.py tests/test_pipeline.py tests/test_batch_workflow.py tests/test_resume.py
389 passed
```

另执行 `python -m compileall -q src` 与 `git diff --check`，均通过。

### GPT 工具调用 smoke

临时隔离 workspace 要求 Agent：读取 `inputs/probe.txt`，写入并验证 `outputs/probe.json`。结果：

- GPT-5.6-sol 真实执行 3 次 `exec_command`；
- artifact 存在且内容与输入一致；
- 最终响应通过 schema；
- 约 25.9k tokens；
- 说明 API、key、Codex、bridge 和主动工具调用链路均可用。

### 同论文完整测试

论文：`paper_6904a9c8c09855cc`（DOI `10.1002/anie.202525581`）。

输出目录：

```text
runs/stage06-07-revised-20260817-paper6904-gpt56sol-configured-r2
```

结果：

- Stage06：`provisional_constructed`；Builder 23 次工具调用；
- Stage06B：转换成功；Converter 28 次工具调用；
- Stage07：`approved_with_repairs`；Audit 19 次工具调用；
- Stage07 修复了 reproduction 元数据、两模式 process rubric 和 toolbox requirements 的格式/完整性问题；
- 最终发布目录包含 reproduction、autonomous、hidden reference、paper info 和输入结构，未包含 conversion contract/receipt 等内部来源合同。

## 发现的代码问题与修复

1. GPT 自定义模型下 Codex request 的 `tools` 为空，`auto` 允许模型直接结束。解决：配置策略 + required 策略下的最小 `exec_command` 兼容声明。
2. 阶段级默认 `tool_choice_policy=auto` 覆盖模型级 GPT 配置。解决：删除示例配置中的无必要阶段默认值，并将 phase 显式覆盖限定为专用 phase 字段。
3. `chat_completions` 被误传给 Codex CLI 的 `wire_api`。解决：Codex CLI 固定使用 `responses` 连接本地 bridge，`codex_wire_api` 仅用于 bridge upstream。
4. 直连 Responses 时 API key 未传给 Codex 子进程。解决：仅 bridge=None 时注入 `OPENAI_API_KEY`，不改变 bridge 的密钥隔离。
5. 旧 bridge trace 无法判断“Codex 未发工具”还是“上游未返回工具”。解决：trace 增加 incoming tools、实际发送的 tools、tool choice 和 response format 摘要。

## 仍需关注

- GPT builder 的输入材料很大，单篇测试的累计输入接近百万 token；这属于上下文/材料规模问题，不是工具协议失败。下一轮可独立优化证据包去重和阶段间材料裁剪。
- Stage07 仍应由 Agent 决定科学结论；代码只负责文件交接、受限合同恢复和发布边界检查。
- autonomous 任务允许公开科学目标和必要输入，但 route、方法、目标数值和结论仍应由 Stage07 动态审查；不能用固定关键词列表替代 Agent 判断。
