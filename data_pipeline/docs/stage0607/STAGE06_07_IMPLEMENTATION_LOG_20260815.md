# Stage06/07 单 Agent 改造实施记录

日期：2026-08-15
依据：`STAGE06_07_CURRENT_CODE_REVISION_PLAN_20260815.md`
状态：核心实现与本地验证完成，六篇分层真实论文试运行待执行

## 1. 实施目标

- Stage06 默认每篇论文只调用一个构建 Agent；
- Agent 以 PDF、正文和 SI 为主要证据，Stage02-05 只作为检索提示；
- 优先选取整篇论文的完整计算化学流程，在不可构建时选择最大的完整复杂子流程；
- 先制作论文复现模式，再由固定复制程序生成自主科研模式基线并做受限改写；
- 两种模式共享输入、提交合同、Ground Truth 和结论评分，只允许路线披露与过程 rubric 不同；
- 科学信息不完整、客观执行失败、构建产物无效和工具箱能力缺口分开记录；
- Stage07 客观审计范围选择、复杂度、完整性、泄漏、工具箱和成本。

## 2. 修改计划

1. 建立当前代码和测试基线。
2. 修复证据、边界条件、坐标、表格、Ground Truth 和失败分类的确定性问题。
3. 增加单 Agent 的 Stage06 schema、prompt 和输出合同。
4. 增加单 Agent 编排、里程碑、复现任务先生成和复制后自主模式改写。
5. 增加范围、复杂度、共享 Ground Truth、复制完整性和泄漏校验。
6. 调整 Stage07 的审计合同和结果映射。
7. 运行静态检查、单元测试、模拟 Harness、端到端和真实论文回归。
8. 输出独立分析报告。

## 3. 基线记录

### 3.1 工作树

仓库在修改前已经包含 Stage06/07、Agent harness、配置和测试等大量未提交改动。本次工作以这些文件为现有基线，只做增量修改，不回退用户已有内容。

### 3.2 当前实现

- Stage06 当前默认依次调用 `scientific_review`、`autonomous_task`、`paper_reproduction`、`hidden_reference` 四个 Agent phase。
- 当前生成顺序是自主模式在前、复现模式在后，与已确认方案相反。
- Stage05 候选在 prompt 中虽声明为提示，但早期严格 review contract 和 validator 仍容易把前序缺陷放大为论文拒绝。
- Stage07 已有完整性、工具箱、成本和泄漏审计基础，但尚无明确的 full/major/partial 范围和非平凡复杂度审计。

### 3.3 测试环境

- 系统 Python 和项目 `.venv` 均为 Python 3.11.15。
- 当前 `.venv` 只是指向现有 Conda Python 的轻量环境，尚未安装 `pytest`、`jsonschema`、`pypdf` 等项目依赖。
- 首次基线命令 `.venv/bin/python -m pytest -q tests/test_stage0607_agents.py` 因 `No module named pytest` 未能执行；后续将按 `uv.lock` 安装开发依赖后重跑。

## 4. 变更批次

### 4.1 P0 确定性修复

修改文件：

- `src/stages/stage06_task_builder/validation.py`
- `src/stages/stage06_task_builder/stage.py`
- `tests/test_stage0607_agents.py`

完成内容：

- evidence map 递归读取单数 `evidence_id`、复数 `evidence_ids` 和以实际 evidence 集合作为 key 的映射，不再依赖 `ev_` 前缀；
- route/public boundary 改为相同边界类型的结构化值比较，数值允许带单位表达，并避免其他 JSON 字段中的偶然字符串命中；
- 周期体系不再被机械要求提供分子 multiplicity；
- 坐标标签排除页码、`S40`、图表号、页眉和 URL，并记录 `label_confidence`；
- 表格提取新增 Markdown pipe table，始终写 `derived_tables/coverage.json`，区分 complete、partial、failed，并记录 parser/layout/image fallback；
- Ground Truth 增加 required/forbidden 自冲突、数值符号与文字冲突、Acceptance Profile target 和 submission projection 一致性检查；
- 旧 reproduction materializer 会保留 Agent 合法的 task_spec 修改，同时冻结两模式必须一致的科学字段；
- scientific failure 新合同必须记录全文 workflow inventory、full-paper 检查、替代范围搜索、checked sources 和证据。

### 4.2 Stage06 单 Agent 默认路径

修改文件：

- `src/agents/schemas.py`
- `src/stages/stage06_task_builder/prompts.py`
- `src/stages/stage06_task_builder/stage.py`
- `src/stages/stage06_task_builder/validation.py`
- `src/config.py`
- `config.example.json`

完成内容：

- 新增小型 `STAGE06_TASK_PAIR_BUILDER_SCHEMA` receipt 和文件化 `STAGE06_WORKFLOW_REVIEW_SCHEMA`；
- `mode_generation_strategy` 默认值改为 `single_agent`；历史四 phase 实现保留为兼容路径；
- 每篇论文默认只运行一个 `task_pair_builder` Agent phase；
- snapshot 新增原始主论文 PDF、SI、完整解析材料、coverage manifest、上游 hint、工具箱内容 hash、resource policy、task contract 和固定 helper scripts；
- Agent 必须先完成全文计算工作流 inventory，依次尝试 full、major、partial scope，并只接受 medium/high 非平凡复杂度；
- 成功时先生成 `paper_reproduction/`，运行固定校验和复制脚本，再在 allowlist 内改写 `autonomous_research/`；
- 两模式冻结输入、submission contract、科学问题、scope、complexity 和 deliverables；
- 共同 hidden reference 同时支持数值、结构、类别、排序、趋势、中间文字结论和最终文字结论；
- 正式目录只在 receipt、workflow review、两个任务、hidden reference 和 deterministic audit 全部通过后原子提交；
- 单 Agent checkpoint fingerprint 包含 PDF/解析材料、上游 hints、工具箱内容、资源、prompt、schema 和 helper script；
- objective failure、scientific not constructible 和 construction invalid 分开输出。

### 4.3 Stage07 范围和复杂度审计

修改文件：

- `src/stages/stage07_task_judge/prompts.py`
- `src/stages/stage07_task_judge/stage.py`
- `src/stages/stage07_task_judge/validation.py`

完成内容：

- 修正旧 prompt 中错误的模式派生方向，明确 autonomous 由 reproduction 固定复制后改写；
- audit packet 新增 workflow scope、complexity profile、全文 inventory 状态、Stage05 disposition 和定向 source evidence bundle；
- 新增 `scope_underselected` 和 `task_not_challenging` 审计要求，并映射到 `workflow_incomplete`；
- deterministic finding-to-outcome 改为显式 code/prefix map，避免任意子串误分类；
- 继续把缺软件、能力未知、缺数据、缺 Ground Truth、成本过高和隔离问题作为可并存的客观 outcome。

### 4.4 当前验证状态

- `python -m py_compile`：通过；
- `git diff --check`：通过；
- 全量 `uv sync --extra dev --frozen`：因大型 wheel 下载超时停止，未改动锁文件；
- 已改为使用当前环境中可用的项目依赖完成回归，最终测试结果见 4.7。

### 4.5 单 Agent 契约脚手架与恢复修复（本轮）

修改文件：

- `src/stages/stage06_task_builder/bootstrap_task_pair.py`
- `src/stages/stage06_task_builder/stage.py`
- `src/stages/stage06_task_builder/validation.py`
- `src/stages/stage06_task_builder/prompts.py`
- `tests/test_stage0607_agents.py`

完成内容：

- 新增 `bootstrap_task_pair.py`，由 `workflow_review.json` 确定性生成复现任务的文件
  contract、公共输入副本、模式 ID、提交路径、scope/complexity 冻结字段和 typed
  Ground Truth scaffold；脚本不生成科学输入、方法或答案；
- `task_contract.json` 明确列出允许的字段别名和禁止自动补造的科学字段；
- 在 Python 语义校验前归一化常见 Agent 别名（scope、complexity、step output、GT
  item），但仍要求公共输入、路线闭合、证据和 Ground Truth 由源材料支持；
- recovery attempt 会移除过期 construction receipt、保留 partial tree、写入
  `TASK_PAIR_RECOVERY_STATUS.json`，并明确不能把构建格式错误改写为科学拒绝；
- reproduction validator/copy helper 接受 Agent 常用的 `...py outputs` 简写；
- 对畸形 JSON 数组元素返回结构化 finding，不再由 `.get()` 抛出未分类异常；
- 约束提示要求先运行脚手架，再批量写任务，减少 Agent 猜 schema 和无效调用。

### 4.6 验证与真实回归记录

- Stage06/07 专项测试：`86 passed`；
- 全量测试：`464 passed`；
- `py_compile`、`git diff --check`：通过；
- 真实论文 `paper_0543918936df2fba`（DOI `10.1016/j.cej.2025.172097`）的旧回归中，
  Agent 虽抽取了 VASP workflow 和结果，但没有提供可执行的 slab/分子输入。新规则将
  其归入 `scientific_not_constructible` 候选，而不是为了提高通过率制造输入；该回归期间
  网关曾长时间无响应，未把它伪装成科学失败；
- 真实论文 `paper_6904a9c8c09855cc`（DOI `10.1002/anie.202525581`）回归首次成功调用
  脚手架并生成 review、复现目录和 hidden reference，但 Agent 误将 `outputs` 传给旧复制
  脚本，导致 `construction_invalid`。离线用修复后的脚本复核，`outputs` 简写可正确生成
  autonomous 目录；后续离线合同复核结果见 4.7。

### 4.7 r2 确定性合同收口

实现版本：

- Stage06：`v4-single-agent-full-workflow-first-20260816-r2`；
- task-pair prompt：`v4-stage06-single-agent-builder-20260816-r2`；
- Stage07：`v4-scope-complexity-objective-audit-20260815-r1`。

新增修复：

- 从 `workflow_inventory`、`workflow_scope`、复现任务文件恢复 Agent 漏写或写错的顶层
  review 字段，不以格式漂移替代科学判断；
- 规范 workflow step、依赖、输入输出和 step type，并根据真实依赖图重算
  `dependency_edge_count`；
- 规范 Ground Truth 类型、别名、单位和容差，将共享 Acceptance Profile 展开为逐
  Ground Truth item 的类型化 profile；
- 冻结两种模式的 scope、complexity、科学问题、公共输入、边界条件、deliverables 和
  submission contract；
- 修复 mode、task ID、disclosure 枚举漂移，强制先从 reproduction 复制数据，再删除
  autonomous 中的论文路线文件；
- 恢复 reproduction route-fidelity rubric、frozen Ground Truth、submission binding、
  conclusion rubric 和 hidden sidecar 包装合同；
- 支持工具箱快照中的 `available/missing/incompatible/unknown` 布尔表达；
- recovery 读取只读的 `inputs/frozen_workflow_review.json`，防止第二次 Agent 调用覆盖已
  验证的科学选择；
- prompt 明确要求公共输入必须作为真实文件落盘，不能只在 JSON 中声明路径。

最终验证：

- 定向 Stage06/07 测试：`86 passed`；
- 新增“故意破坏任务合同后确定性修复”测试：`1 passed`；
- 项目全量测试：`465 passed in 10.31s`；
- `python -m py_compile`：通过；
- `git diff --check`：通过。

对 `paper_6904a9c8c09855cc` 的离线副本进行 r2 规范化后，mode、scope、complexity、
两模式冻结字段、hidden profile、rubric、sidecar、工具箱状态、路线 rubric 和自主模式
路线泄漏等格式/合同问题均已消除。但该次 Agent 产物仍声明了 22 个 XYZ 公共输入路径，
实际 `outputs/*/data/inputs/structures/` 中没有对应文件，且一条 Ground Truth 引用了不在
canonical evidence index 中的 evidence ID。因此该产物必须继续判为构建无效，代码不会从
论文或 SI 中猜测、补造输入。六篇分层真实论文试运行将重点验证新版 prompt 能否促使 Agent
从 SI 中恢复并真实落盘这些资产。

## 5. 下一轮真实试运行

固定使用六篇论文，每个手工适宜度层级两篇；以 Codex harness、当前
`config.local.env` API 配置、最多两篇并发运行。每篇保留一个 `runner.log` 和一个
`run_status.json`，根目录只保留一个 `run_status.json`，不再生成大量零散计数/时间文本文件。

试运行完成后逐篇检查：科学失败与客观失败分类、输入文件真实性、full-paper-first 范围、
非平凡复杂度、复现路线完整性、自主模式泄漏、共享 Ground Truth/Acceptance Profile、
Stage07 客观 outcome 和 Agent 恢复轨迹。发现代码问题时，在本日志追加版本、提交号、复现
样本、修复和复测结果后再启动下一轮。

### 5.1 r3：真实资产、证据引用与恢复路径收口

实现版本：

- Stage06：`v4-single-agent-full-workflow-first-20260816-r3`；
- task-pair prompt：`v4-stage06-single-agent-builder-20260816-r3`；
- Stage07 保持 `v4-scope-complexity-objective-audit-20260815-r1`。

r3 针对六篇旧调用产物的离线 replay 暴露的问题完成以下修复：

- 首轮总预算提高到 72 次工具调用，其中前 36 次为检索预算，并保留 2 次 finalization
  调用；recovery 使用 24 次调用并保留 2 次 finalization 调用，防止 Agent 在读完 SI 后
  没有预算写完 receipt；
- recovery 不再无条件重新运行脚手架或覆盖已经完成的论文复现任务；如果复现任务有效而
  自主模式缺失，只要求运行确定性复制脚本并修改自主模式 allowlist 内的路线披露文件；
- validation 先执行字段别名归一化和只允许唯一来源的可信恢复，再执行严格 JSON Schema
  校验；兼容 workflow、scope、complexity、step、boundary 和 Ground Truth 的常见 Agent
  表达差异；
- 将 `missing_input_assets`、`missing_essential_input_assets` 等同义科学失败归一到
  `missing_core_input`，但 API、harness、解析和构建故障仍不得伪装成科学失败；
- construction receipt 从已验证的 `workflow_review.json` 确定性投影；Codex final message
  即使被网关截断或格式畸形，只要落盘 review 与任务产物合法，也可恢复 receipt；
- evidence ID 支持 exact ID、同文档 block index、derived hash 和 wildcard block ID 映射，
  仅在 canonical evidence index 中存在唯一映射时替换，绝不凭语义猜测证据；
- 公共输入必须与只读 workspace 中的 source/derived 文件逐字节一致，才可标为可信输入；
  `best-effort`、`approximate`、`reconstructed`、`verify` 等 Agent 暂存资产保持未验证，不能
  因为文件存在就自动升级为 `source_copy`；
- 可信输入可优先从论文复现模式恢复；对真实 XYZ 的 comment 行做确定性中性化，以移除
  作者计算路线披露，同时保持原子数、元素和坐标不变，并记录 transform provenance；
- `late_stage_runner.py` 改为按 paper ID 流式过滤上游 JSONL，避免每篇启动时解析整个历史
  run 中的所有大文件；
- 收紧自主模式路线泄漏规则，同时排除 `Barrier comparison table` 和一般 stationary-point
  validation 等不构成作者路线披露的误报。

离线 replay 结果：

- `paper_98946f2af94e53f9`（Salen-COF）维持
  `scientific_not_constructible/missing_core_input`，离线合同 findings 为 0；
- `paper_10679580b3d561b4`（Ni(111)）维持科学不可构建：缺少 slab、吸附结构和精确
  Ground Truth，离线合同 findings 为 0；
- `paper_6904a9c8c09855cc`（gallaphosphene）的 18 个 XYZ 均通过 canonical source hash
  校验，输入完整性恢复为 `confirmed`，evidence ID 与 workflow output 问题消除；二次 replay
  稳定，仅剩旧调用没有生成自主模式目录，需由新版 recovery 在线补齐；
- `paper_5286f393dfa5a49a`（helitwistacene）的 3 个 138 原子 XYZ 均可信恢复，输入完整性
  为 `confirmed`；旧调用仍缺自主模式和一条 validation evidence ID，需在线补齐；
- `paper_6a0e549ed50c8b49`（fusadiene NMR）的 best-effort SMILES 与近似 NMR CSV 被正确保留
  为未验证资产，不能作为可复现输入通过；
- `paper_23e9206ce48858f7`（selenium radical）旧产物没有 `workflow_review.json`，无法安全
  离线恢复，必须重新运行 Agent。

r3 验证结果：

- Stage06/07 及 runner 专项测试：`93 passed`；
- 项目全量测试：`471 passed in 15.03s`；
- `python -m py_compile`：通过；
- 下一步为单篇当前 API 端到端验证，通过后重提固定六篇。
