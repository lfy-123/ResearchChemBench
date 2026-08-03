# Stage 05-07 实现与测试结果报告

日期：2026-08-03

## 1. 任务范围

本次重构保留 Stage 01-04 核心逻辑，删除旧的后续筛选、抽取、模型集成、人工审核和发布代码，实现：

- Stage 05：有边界的资产发现、下载、溯源、安全展开和增量解析。
- Stage 06：可选择 Codex、Claude 或 OpenCode 的 Builder Agent。
- Stage 07：与 Builder 完全隔离的 Judge Agent。
- Agent 工作区隔离和聊天记录持久化。
- OpenCode + `deepseek-v4-flash` 真实监督测试。

代码仅保存在本地 Git，不推送 GitHub。

## 2. Stage 05 功能

### 2.1 输入和线索

Stage 05 接收 Stage 04 通过的论文记录，使用：

- 论文 DOI。
- GROBID 文本和 TEI 中的 Data/Code Availability。
- 正文及新资产中的 URL、相关 DOI、仓库地址和文件名。
- Crossref、DataCite、OpenAlex 的结构化关系。

论文 DOI 只作为身份，不作为待下载资产。

### 2.2 三轮有限循环

每轮执行：

1. 解析当前待处理线索。
2. 并发查询和下载直接资产。
3. 按 source data、input、supplement、code 优先级登记资产。
4. 在多个压缩包之间公平分配递归展开预算。
5. 立即解析新资产，并将新线索放入下一轮。
6. 无新资产时提前结束，最多三轮。

### 2.3 下载和安全

- 流式下载，先检查 `Content-Length`，再按块限制真实下载大小。
- SHA-256 内容寻址存储和跨来源去重。
- HTTP 重定向逐跳检查。
- 默认拒绝私网、localhost 和非 HTTP(S) 地址。
- 对当前代理环境中的 GitHub 官方 HTTPS 域名作有限例外。
- ZIP/TAR 路径穿越、符号链接、设备文件、文件数量和展开体积检查。

### 2.4 解析

- PDF：MinerU；主论文可回退到 GROBID 文本。
- JSON/YAML、CSV/TSV、XLSX、DOCX、HTML 和普通文本：结构化解析。
- 压缩包：安全展开并递归登记子资产。
- 其他二进制科学文件：保留原始文件、哈希和元数据，不强行文本化。

核心输出是 `asset_manifest.jsonl`，同时保存 `clue_manifest.jsonl`、`asset_events.jsonl` 和未解决线索。

## 3. Stage 06 功能

Builder 输入：

- Stage 02-04 结构化论文信息。
- 工具箱软件和动作清单。
- Stage 05 资产清单、逻辑路径和可读内容。
- Builder JSON Schema。

Builder 输出：

- 科学记录。
- 候选任务正文。
- 公开资产列表。
- 隐藏参考答案。
- 100 分评分规则。
- 论文和资产证据映射。

证据不足时返回 `abstain`，不伪造任务。候选还要经过 Python 确定性校验，包括资产 ID、核心软件、工具箱动作、评分总分、证据引用、隐藏结果泄漏和占位内容检查。

## 4. Stage 07 功能

Judge 使用独立会话，不读取 Builder 聊天和临时文件。输入包括正式候选快照、公共输入探针、论文证据、资产清单和工具箱。

审计维度：

- 论文忠实性。
- 数据充分性。
- 工具箱支持。
- 答案泄漏。
- 评分质量。
- 资源可行性。

输出 `pass`、`revise` 或 `reject`，并保存结构化 JSON 和 Markdown 报告。

## 5. Agent 隔离和记录

每次 Agent 调用创建独立：

- `workspace/input`、`workspace/work`、`workspace/output`。
- 临时 HOME、XDG 配置、缓存和数据目录。
- CLI session ID。
- `prompt.md`、`response_schema.json`。
- `native_events.jsonl`、`conversation.jsonl`。
- 每次尝试的 stdout/stderr。
- `final_response.json` 和 `run_metadata.json`。

输入快照改为只读；主机绝对路径从 Agent 清单中删除，压缩包成员使用相对 `logical_path`。OpenCode 禁止编辑、shell、外部目录和网络工具。

Codex、Claude 或 OpenCode 如需使用本地 CLI 认证，只在执行期间将必要凭据复制到本次隔离 HOME；进程结束或异常退出后立即删除凭据。长期保存的运行目录只保留 prompt、Schema、聊天、CLI 事件、stdout/stderr 和统计信息。

## 6. 测试对象

论文：

`Towards high-throughput many-body perturbation theory: efficient algorithms and automated workflows`

DOI：`10.1038/s41524-023-01027-2`

该论文适合验证：

- Materials Cloud 关联数据发现。
- GitHub 代码仓库下载。
- 大型 AiiDA/原始输入输出归档。
- QE、Yambo、AiiDA 和 Wannier90 资产关系。
- 不完整公开输入和工具箱能力门控。

## 7. Stage 05 测试结果

输出：

`runs/stage05_network_mbpt_20260803_v8/outputs/stage_05_asset_collection/`

统计：

| 项目 | 数量 |
|---|---:|
| 论文 | 1 |
| 总资产 | 100 |
| 主论文 | 1 |
| 论文源数据 | 5 |
| 计算输入 | 32 |
| 代码资产 | 61 |
| 其他 | 1 |
| 解析成功 | 99 |
| 解析 partial | 1 |
| 线索 resolved | 4 |
| 线索 partial | 1 |
| 线索 skipped_by_budget | 2 |

成功发现和保留：

- Materials Cloud 的 README、`files_description.md`、`gaps.json` 和 `raw_input_output.tar.gz`。
- `aiida-yambo` 与 `aiida-yambo-wannier90` GitHub 仓库。
- 2D-hBN、Si、C、MoS2、ZnO、bulk hBN、TiO2 的 QE SCF/NSCF 输入。
- 2D-hBN 的多个 Yambo 收敛输入。

测试单文件上限设置为 100 MiB，因此 498 MB 的 `automatedMBPT.aiida` 被明确记录为超预算，其他文件不受影响。生产配置默认上限为 10 GiB。

Stage 05 最终调度不再受并发完成顺序控制，论文源数据和代码仓库都获得了递归展开预算。

## 8. Stage 06 测试结果

输出：

`runs/stage06_07_opencode_mbpt_20260803_v5/outputs/stage_06_builder/`

结果：`abstain`。

合理阻断项：

1. ResearchChemBench 工具箱没有 GW/G0W0 动作。
2. Yambo 当前只有接口级支持，不能证明可以完成数值 GW 计算。
3. QE 输入引用的 B、N、Si 赝势没有被收集。
4. 完整原始归档混合输入和答案输出，不能整体作为公开输入。
5. `gaps.json` 包含参考结果，只能作为隐藏证据。

运行统计：

| 项目 | 值 |
|---|---|
| CLI | OpenCode 1.18.10 |
| 模型 | deepseek-v4-flash |
| 用时 | 461.512 秒 |
| 累计 token | 172,978 |
| 缓存读取 token | 165,376 |
| 最终状态 | success / abstain |

Builder 判断总体正确，但存在一个文本错误：它称归档输出成员不可读。实际 Stage 05 已将部分成员独立登记；不过测试预算没有保留答案输出内容，且真正的弃权依据仍是工具箱无 GW 动作和赝势缺失。

性能方面，`logical_path` 已把同名资产读取从 34 个降到约 12 个，但 DeepSeek 多轮自检仍导致较高累计 token 和约 7.7 分钟时延。后续可增加 CLI 级硬性 step/tool-call 预算，或由 Python 预先生成更小的科学资产摘要。

## 9. Stage 07 测试结果

输出：

`runs/stage06_07_opencode_mbpt_20260803_v6/outputs/stage_07_judge/`

负例构造：

- 声称可以用 QE+Yambo 计算 2D-hBN G0W0 能隙。
- 资产 ID、核心软件、动作名称、评分总分和证据引用均通过基础 Python 校验。
- 实际缺少赝势、Yambo/SAVE 公开输入和 GW 工具箱动作。

Judge 结果：`reject`。

识别出的关键问题：

1. 工具箱不能执行核心 G0W0 方法。
2. QE 输入缺少 B/N/Si 赝势。
3. 没有公开 Yambo/SAVE 和 GW 收敛输入。
4. 主论文 Table 1 已公开 2D-hBN 最小能隙 6.84 eV 和收敛参数，造成答案泄漏。
5. 评分规则同时包含不可执行和可直接抄录的项目。

运行统计：

| 项目 | 值 |
|---|---|
| CLI | OpenCode 1.18.10 |
| 模型 | deepseek-v4-flash |
| 用时 | 145.1 秒 |
| 累计 token | 54,871 |
| 缓存读取 token | 42,752 |
| 最终状态 | success / reject |

该结果符合设计要求，并证明 Judge 能发现基础 schema 和静态校验无法判断的科学可执行性、资产充分性和答案泄漏问题。

## 10. 自动化质量检查

- `pytest`：29 passed，另有 6 subtests passed。
- `ruff check src tests`：通过。
- `ruff format`：通过。
- `vulture src --min-confidence 80`：无高置信度死代码。
- `git diff --check`：通过。
- OpenCode 结构化最小探针：通过。
- GitHub 代理 DNS 下载探针：通过。

## 11. 结论

Stage 05-07 已按设计落地，并完成真实论文、真实外部资产、真实 OpenCode/DeepSeek Agent 的监督测试。当前代码可以：

- 有边界地收集和解析研究资产。
- 保留完整来源、哈希和父子关系。
- 在隔离工作区运行可切换 CLI 的 Builder/Judge。
- 保存完整聊天和运行记录。
- 在证据不足时由 Builder 主动弃权。
- 由 Judge 拒绝科学上不可执行、数据不足或泄漏答案的候选任务。

当前主要剩余风险不是功能错误，而是 Agent token/时延控制和部分出版社受限资产的覆盖率。Builder-Judge 自动循环修订按要求暂不实现。
