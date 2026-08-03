# Stage 05-07 重构实施记录

## 2026-08-03：实施准备

- 确认 Stage 01-04 当前核心边界分别为清点去重、GROBID、Softcite 软件覆盖和资源审查。
- 确认本机已安装 Codex CLI 0.145.0、Claude Code 2.1.119 和 OpenCode 1.18.10。
- 确认 OpenCode 已配置 DeepSeek provider，并可选择 `deepseek/deepseek-v4-flash`。
- 更新设计方案，使 Stage 06 和 Stage 07 可独立选择 `codex`、`claude` 或 `opencode`。
- 新增 `STAGE_05_07_CODE_MODIFICATION_PLAN.md`，定义模块、删除范围、配置和测试策略。
- 当前未修改 Stage 01-04 代码。

## 2026-08-03：Agent 隔离要求补充

- Builder 和 Judge 每次调用使用独立工作目录、独立临时 HOME 和全新会话。
- 两个阶段分别保存 CLI 原生事件、规范化聊天记录、最终响应、stdout/stderr 和运行元数据。
- Judge 只接收显式构造的审计输入快照，不允许读取 Builder 的聊天记录或临时工作区。
- 本机支持 user/mount namespace 组合，可在实现中作为 CLI 自身 sandbox 之外的增强隔离。

后续每次结构性修改、测试发现和修复均追加记录到本文档。
