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

## 2026-08-03：代码替换

- 删除旧 Stage 05 之后的搜索、筛选、抽取、候选生成、模型集成、人工队列和发布实现。
- 新增 `src/assets/`，实现线索抽取、API 发现、下载、内容哈希、安全解压、解析路由和 Stage 05 编排。
- 新增 `src/agents/`，实现 Codex、Claude、OpenCode 三种 CLI 适配、隔离 HOME、独立工作区、重试、心跳、token 统计和会话保存。
- 新增 `src/tasks/`，实现 Builder、Judge、JSON Schema、确定性校验、公共输入探针和任务包物化。
- 修改总编排为七阶段，并增加从已有 Stage 04 JSONL 直接运行 Stage 05-07 的入口。
- 更新配置、依赖和运行脚本；Stage 01-04 的核心筛选逻辑未改动。

## 2026-08-03：Stage 05 监督测试和修复

测试论文：

`Towards high-throughput many-body perturbation theory: efficient algorithms and automated workflows`

DOI：`10.1038/s41524-023-01027-2`

测试期间依次发现并修复：

1. Crossref、OpenAlex 和出版社 HTML 原始内容召回 ORCID、ROR、参考文献等无关链接。改为提取结构化关系字段，并只在 HTML 中保留附件和数据链接。
2. 单个超大文件失败会中断同一记录内其他小文件。改为目标级错误隔离，记录 `target_errors` 后继续下载。
3. 下载接口先读取完整响应再检查大小。改为流式下载，并在读取正文前检查 `Content-Length`。
4. 论文 DOI 被当作未解决资产线索。改为 `paper_identity`，不进入下载前沿。
5. GitHub 在当前代理环境解析为 `100.64.x.x`，被 SSRF 防护误判。只对明确的 GitHub 官方 HTTPS 域名增加有限信任，其他私网地址仍拒绝；随后成功下载 `aiida-yambo` 4.47 MB 仓库归档。
6. 并发完成顺序导致第一个 GitHub 压缩包占满全部资产预算。改为每轮先收齐直接资产、按资产角色排序，再在多个压缩包之间公平分配展开预算。
7. 大量同名 `aiida.in` 抢占优先级，QE SCF/NSCF 输入没有进入有限资产集合。改为优先保留 DFT 基础输入、结构、赝势、README 和配置，再保留参数扫描输入，输出文件最后处理。
8. 代码仓库 README 召回依赖仓库，造成递归主题漂移。代码资产不再继续扩张 GitHub 依赖，但仍保留指向数据仓库的线索。

最终 Stage 05 测试目录：

`runs/stage05_network_mbpt_20260803_v8/outputs/stage_05_asset_collection/`

最终结果：

- 100 个资产：主论文 1、论文源数据 5、计算输入 32、代码 61、其他 1。
- 99 个解析成功；1 个零字节 `__init__.py` 记为 `partial`。
- 7 条线索：4 resolved、1 partial、2 skipped_by_budget。
- `partial` 来自测试单文件上限 100 MiB：498 MB 的 AiiDA 归档被跳过，其余 Materials Cloud 文件继续下载。
- 成功保留 2D-hBN 的 QE SCF/NSCF 输入、Yambo 参数输入、`gaps.json`、README、原始输入输出归档和两个相关代码仓库。

## 2026-08-03：Agent Runner 修复

- OpenCode 在终端手工运行成功，但 Python Runner 首次调用持续返回 `UnknownError`。
- 根因是 `Popen(cwd=...)` 不会更新继承环境中的 `PWD`；OpenCode 把会话绑定到 `data_pipeline` 根目录，而不是隔离工作区。
- 在隔离环境中显式设置 `PWD` 和 `INIT_CWD` 后，OpenCode 结构化探针首次调用成功。
- 增加父进程中断时终止子 CLI 的处理，避免遗留 Agent 进程。
- 资产清单移除主机绝对路径，同时增加安全的 `logical_path`，例如 `raw_input_output/2D-hBN/DFT/scf/aiida.in`。
- Builder/Judge 提示词限制定向读取数量，避免面对大量同名压缩包成员时逐个扫描。

## 2026-08-03：Stage 06 真实测试

最终 Builder 输出：

`runs/stage06_07_opencode_mbpt_20260803_v5/outputs/stage_06_builder/`

结果为 `abstain`。主要理由：

- 工具箱没有 GW/G0W0 动作，Yambo 只有接口级支持。
- QE 输入引用的 ONCV/Si 赝势没有出现在资产集合中。
- 完整原始归档同时包含输入和答案输出，不能整体公开。
- `gaps.json` 是答案资产，不能作为公开输入。

运行信息：

- CLI：OpenCode 1.18.10。
- 模型：`deepseek-v4-flash`。
- 状态：success / abstain。
- 用时：461.512 秒。
- OpenCode 累计 token：172,978，其中缓存读取 165,376。
- 会话、原生事件和工作目录均已保存。

该判断总体合理。模型错误地声称归档中的输出成员“不可读”，但这不影响最终弃权结论；真正的阻断项是工具箱无 GW 动作和赝势缺失。累计 token 和时延仍偏高，作为后续优化项保留。

## 2026-08-03：Stage 07 真实负例测试

首先将 Builder 的明确 abstain 包强制伪装为 candidate。Judge 返回 `pass`，因为它把该包理解为正确的弃权记录。真实流水线不会把 abstain 送入 Judge，新增的确定性校验也会拦截 `NOT ISSUED`、`not constructed` 和占位评分内容，因此该测试不构成 Judge 失败。

随后构造一个真正的不可执行候选：候选声称可以使用 QE+Yambo 计算 2D-hBN 的 G0W0 能隙，选择的动作和资产 ID 均能通过基础 Python 校验，但公开资产缺少赝势、没有公开 Yambo/SAVE 输入，工具箱也没有 GW 动作。

最终 Judge 输出：

`runs/stage06_07_opencode_mbpt_20260803_v6/outputs/stage_07_judge/`

结果为 `reject`，准确识别：

- 数据不充分。
- 工具箱不支持核心计算。
- 公开论文 Table 1 已泄漏 6.84 eV 和收敛参数。
- 评分项包含不可执行和可直接抄录的内容。

运行信息：

- CLI：OpenCode 1.18.10。
- 模型：`deepseek-v4-flash`。
- 状态：success / reject。
- 用时：145.1 秒。
- OpenCode 累计 token：54,871，其中缓存读取 42,752。
- Judge 使用独立 workspace、HOME、session ID 和 `conversation.jsonl`，未读取 Builder 聊天记录。

## 2026-08-03：质量检查

- `pytest`：29 passed，另有 6 个 subtests passed。
- `ruff check src tests`：通过。
- `ruff format`：通过。
- `git diff --check`：通过。
- `vulture src --min-confidence 80`：清理旧参数后无高置信度死代码。
- 未推送 GitHub，仅准备本地 Git 提交。
