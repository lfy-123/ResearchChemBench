# 数据管线架构与契约

## 设计边界

当前管线的筛选目标是：找到包含完整计算化学科研流程、所需核心软件存在于当前化学工具箱、
资源成本可接受，并能进一步构建为可评分任务的论文。软件覆盖按工具箱三层能力理解，但 Stage03
只门控论文明确依赖的命名核心软件是否存在于原生软件目录，不要求预设 Action 已覆盖全部参数。

所有阶段以稳定 `paper_id` 关联。每篇论文在 Stage00 中是一个目录，正文、远端已有 SI 和
`paper.json` 放在一起。每个阶段必须先写 registry 再允许删除 Stage00-03 淘汰论文的原始目录。

## 阶段输入输出

| 阶段 | 输入 | 主要输出 | 通过条件 |
|---|---|---|---|
| Stage00 | 远端数据集、数量、抽样配置、排除清单 | 论文目录、`source_manifest.jsonl`、选择清单 | 正文复制成功且 PDF 有效；SI 缺失不在本阶段淘汰 |
| Stage01 | Stage00 corpus | `package/papers.jsonl`、`documents.jsonl`、`paper_bundles.jsonl`、解析尝试与质量报告 | SI 已存在、成功补齐或官方确认不存在；正文和全部已知 SI 均可解析 |
| Stage02 | Stage01 结构化文本块 | `decisions.jsonl`、map/reduce 审查、错误记录 | 当前作者完成完整计算化学流程，且没有当前作者实施的物理实验；所有混合实验论文均不进入下游 |
| Stage03 | Stage02 证据、Stage01 全文、软件别名和工具箱快照、资源预算 | 软件/工作流/资源清单、工具箱映射、`decisions.jsonl` | 必需的命名核心软件均存在于工具箱，软件清单可确认，且没有明确资源超限 |
| Stage04 | Stage03 通过论文及其文档 | MinerU 高质量正文/SI、解析尝试、`decisions.jsonl` | 正文和所需文档通过 MinerU 质量门控 |
| Stage05 | Stage04 高质量证据、Stage02/03 判定 | benchmark 候选、方向、科学问题、目标和证据引用 | 至少一个候选对应允许的科学方向、完整计算流程和机器可评分目标 |
| Stage06 | Stage05 candidate、冻结证据、工具箱 | 共享科学记录、自主科研任务、论文复现任务、隐藏答案和 rubric | Builder 输出通过结构、证据引用和信息泄漏检查 |
| Stage07 | Stage06 task pair | 确定性审计、独立 Judge、可选 Gold Run、发布判定 | 所有硬性检查通过，Judge 接受，启用时 Gold Run 成功 |

## 调度和服务生命周期

Stage01-03 是第一段微批流水线：一个微批完成 Stage01 后即可进入 Stage02，再进入 Stage03，
不等待整批论文完成。Stage02/03 共用 screening LLM。第一段全部完成后释放或保留同一个 GPU
worker，并按配置切换为 MinerU；Stage04-05 构成第二段微批流水线。Stage06/07 按候选任务并发。

沙箱在整个 `run_pipeline` 外层创建一次并在 `finally` 中清理。GROBID、Softcite、screening LLM
和 MinerU 均由上下文管理器负责启动、复用和异常清理。单篇模型或解析错误必须记录为该论文的
错误状态，不能破坏其他微批的已完成产物。

## 持久记录

`src/registry/` 维护 SQLite 事实表和 JSONL 导出。至少保存：远端 URI、本地路径、hash、论文与
SI 关系、每阶段输入 hash、判定、原因、结构化识别结果、模型与 prompt 版本、原始响应 hash、
工具箱快照 hash、错误和资产删除状态。运行目录是可重建缓存，registry 是筛选历史的权威索引。

## 源码边界

- `src/stages/` 只包含阶段业务逻辑，每个阶段一个目录。
- `src/integrations/` 只封装外部服务和存储协议，不做论文筛选决策。
- `src/core/` 只提供无领域状态的并发、IO 和日志工具。
- `src/pipeline.py` 只负责阶段连接、微批调度、缓存和服务生命周期。
- `src/config.py` 是唯一配置加载与校验入口。
- 不提供旧阶段编号、旧配置布局或 `src/v2` 兼容层。
