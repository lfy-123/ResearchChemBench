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

### 5.2 v5-r1：Stage06 provisional handoff 与 Stage07 repair-first

对应方案：`STAGE06_07_AGENT_REPAIR_REDESIGN_PLAN_20260816.md`。

本次职责修正：

- Stage06 默认单 Agent 路径不再调用内容级 semantic validator，不再根据 rubric、路线泄漏、
  Ground Truth、scope 或其他科学 finding 输出 `construction_invalid`；
- Stage06 成功候选改为 `provisional_constructed`，暂定不可构建改为
  `provisional_not_constructible`，两者都写入独立交接目录并进入 Stage07；
- Stage06 只对 API、harness、JSON receipt、路径、文件交付和文件系统故障执行客观恢复；
- Stage07 改为独立 Audit-Repair Agent，复制 Stage06 目录及完整论文/SI/解析快照到新的只读
  inputs，并只在自己的 `outputs/task_pair/` 副本中修复；
- Stage07 prompt 增加显式 `REPAIR-FIRST RULE`：原工作流可修复时禁止切换，只有记录有证据的
  不可修复阻断后，才允许寻找其他完整工作流；
- Stage07 支持 `approved`、`approved_with_repairs`、
  `approved_after_workflow_redesign`、`rejected_scientific_unrepairable` 和
  `objective_failure_retryable`；缺软件以正交 `toolbox_status=needs_software` 表达；
- Stage07 active path 不再调用 deterministic scientific audit，也不合并代码生成的科学
  outcome；代码只验证 receipt JSON、相对路径和 Agent 是否实际交付了非空任务目录；
- approved 任务发布到 `audited_tasks/<paper_id>/`，科学拒绝保存在
  `rejected_tasks/<paper_id>/`，Stage06 原候选保持不变；
- runner 将 Stage06 的构建候选和暂定不可构建交接包都传给 Stage07；Codex、OpenCode、Claude
  继续共用同一 harness 合同。

本地验证（真实 API 调用前）：

- Stage06/07 与历史 runner 专项测试：`95 passed`；
- 新增“Stage06 部分任务不做内容重试、直接交 Stage07”测试，三次允许尝试配置下实际只调用
  一次 Agent；
- 新增 Stage07 repair-first prompt 顺序测试；
- 全量测试：`472 passed`，唯一失败为无关 Stage01 测试启动系统不存在的 `pdfinfo` 时，当前
  shell PATH 中一个外部目录返回 `ESTALE`；使用纯系统 PATH 复跑该测试为 `1 passed`；
- 关键模块 `py_compile` 和 `git diff --check` 通过。

下一步：提交 v5-r1 代码快照，使用 gallaphosphene 做真实 Stage06/07 单篇验证。若 Agent
轨迹、任务交付或状态仍有问题，记录为 v5-r2 并修复；单篇达到方案预期后再异步提交固定六篇。

### 5.3 v5-r2：Stage07 真实修复交付与中转工具别名

首轮真实端到端样本：

- 论文：`paper_6904a9c8c09855cc`，DOI `10.1002/anie.202525581`；
- run：`stage06-07-v5-single-paper6904-20260816-r1`；
- Stage06 在一次 Agent 调用中输出 `provisional_constructed`，选择 NH3 活化的
  `major_paper_workflow`：18 个来源可追溯 XYZ、三组分支路径、高复杂度、9 条数值与文字
  Ground Truth；
- Stage07 正确保留原工作流，并发现 autonomous 文件中的论文方法与机理路线泄漏。

该次运行同时暴露两个客观交付缺陷：

- 中转站在长上下文后将 Codex 的 `exec_command` 偶发返回为 `Bash`、`shell`、`bash`。
  三次协议恢复均未执行修复命令，最终只通过 `submit_final_json` 写入审计 JSON；
- 审计 JSON 声称修改了 3 个 autonomous 文件，但发布树与 Stage06 对应目录逐字节相同；
  Agent 还重复执行 `cp -r inputs/stage06_candidate outputs/task_pair`，使发布树额外包含
  `stage06_candidate/` 嵌套副本。因此该次 `approved_with_repairs` 不能作为有效验收结果。

v5-r2 修复：

- Responses bridge 仅在请求实际声明 `exec_command` 时，将中转返回的
  `Bash/shell/bash` 及其 `command/script/input` 参数窄映射为 Codex `exec_command.cmd`；
  未声明 `exec_command` 的 harness 或真实同名工具不受影响；
- Stage07 prompt 明确 `outputs/task_pair/` 已预填充，禁止重新复制 Stage06 handoff，要求每个
  `changed_files` 在返回前实际写入并与只读基线 diff；
- Stage07 代码只做客观交付一致性检查，不判断科学内容：`approved_with_repairs` 必须至少有
  一个报告的文件真实改变；报告但未交付、未改变或夹带嵌套 `stage06_candidate/` 时，归为
  可重试的 Agent 交付故障；
- recovery 会清理精确定位的冗余嵌套候选副本，避免污染跨尝试传播。

修复后本地验证：

- Stage06/07 专项测试：`100 passed`；
- 项目全量：`478 passed`，唯一失败仍为无关 Stage01 的外部 PATH `pdfinfo` `ESTALE`；纯
  `/usr/bin:/bin` PATH 单独复跑：`1 passed`；
- Ruff、`py_compile`、`git diff --check`：通过。

下一步：使用新 prompt fingerprint 重跑同一单篇，确认 Stage07 的实际文件 diff、无嵌套副本、
自主模式路线隔离、共享输入与 hidden Ground Truth 后，再提交固定六篇。

### 5.4 v5-r3：自主模式完整公开面审计

v5-r2 的客观交付检查通过后，对最终发布目录进行人工科学验收，发现 Stage07 只清理了
`task_info.json` 和 `task_spec.json` 中的部分方法信息，却错误地声称 `task.md` 已经干净。
自主模式仍通过多个公开面泄漏论文答案路线：

- `task.md` 和公开 JSON 直接列出 `Int-*`、`TS-*` 的顺序与分支；
- 四元环、六元环、额外 NH3 质子穿梭和已知优选路径被直接写入任务要求；
- `process_rubric.json` 把论文的具体分支划分当成评分步骤；
- XYZ 文件名暴露中间体/过渡态角色，第二行注释暴露 PBE0-D3BJ/def2-SVP 和 SI 页码。

该问题属于 Agent 审计职责缺失，不增加代码侧科学内容 validator。v5-r3 将 Stage07 prompt
扩展为强制的 autonomous public-surface audit：

- 递归检查自主任务目录中的说明、spec/info、rubric、manifest、submission contract、全部
  输入路径以及输入文件头，禁止只检查 `task.md` 或少数 JSON；
- 明确定义方法、论文标签与顺序、分支映射、环尺寸、质子穿梭、已知优选路径、趋势和论文
  中间/最终结论均属于自主模式泄漏；
- 路线型文件名必须在两种模式中同步改为稳定中性 ID，论文标签映射只保留在 reproduction
  专用路线文件或 hidden reference 中；
- XYZ 只允许确定性替换自由文本注释行，原子数、元素和坐标必须保持原样，并在两种模式中
  使用完全相同的相对路径与字节内容；
- 公共自主过程 rubric 只评价通用的方法选择、探索、验证、溯源和科学推理，不枚举论文解法；
- 审计摘要必须记录检查过的公开面、两份输入树是否逐字节一致，以及是否仍有禁披露信息。

版本更新为 `v5-stage07-repair-first-auditor-20260816-r3` 与
`v5-repair-first-audit-redesign-20260816-r3`，保证已有 Stage06 checkpoint 可复用，同时仅使
Stage07 的旧 checkpoint 失效。新增 prompt 回归测试覆盖所有公开面、路线型文件名、XYZ
注释中性化和双模式输入字节一致性要求。

### 5.5 v5-r4：允许 Stage07 修复公开输入资产

v5-r3 单篇复跑首次暴露出 mount namespace 的路径匹配缺陷。隔离器原先递归查找所有名为
`inputs` 的目录并绑定为只读；这不仅保护了 workspace 顶层的 canonical `inputs/`，也错误地
冻结了待修复任务中的：

- `outputs/task_pair/paper_reproduction/data/inputs/`；
- `outputs/task_pair/autonomous_research/data/inputs/`。

因此 Stage07 能修改任务说明和 JSON，却无法中性化 XYZ 文件名与注释。Agent 又把整体移动
挂载目录得到的 `Device or resource busy` 误判成全部输入不可写，并在恢复调用中报告了并未
落盘的修复。r2 已有的客观交付检查成功拦截该结果，没有发布虚假
`approved_with_repairs`。

v5-r4 将 mount namespace 的只读范围收窄为 workspace 顶层 `inputs/` 和
`private_input/` 两个 canonical 根目录。输出任务中同名的 `data/inputs/` 保持可写，而真正的
论文、SI、工具箱快照和其他输入仍通过递归只读 bind mount 隔离。新增测试明确验证嵌套公开
输入不进入只读路径集合。

同时补充 Stage07 操作合同：

- 原地修改/重命名输入树的子文件，不整体替换 `data/inputs/` 父目录；
- 父目录 `EBUSY` 不等于子文件只读，必须用一个子文件操作确认；
- `repairs[].changed_files` 和 `workflow_redesign.changed_files` 必须相对
  `outputs/task_pair/`，不能带 `outputs/task_pair/` 前缀；
- 批量重命名可报告两个模式各自的相对输入目录，由客观 diff 校验实际变化。

版本更新为 `v5-stage07-repair-first-auditor-20260816-r4` 与
`v5-repair-first-audit-redesign-20260816-r4`，再次只使 Stage07 checkpoint 失效。

### 5.6 v5-r5/r6：中转内容审查恢复与真实改动 receipt

后续单篇运行确认 Codex 与 `deepseek-v4-flash` 的工具协议已经兼容，但中转站会对累积的
assistant/tool transcript 再做内容审查。论文原文、SI 表格和大量命令输出进入历史后，上游
偶发返回 `data_inspection_failed`，Codex CLI 随后不断重连，表现为 Stage07 长时间不结束。

Responses-to-Chat bridge 增加一次性、窄范围恢复：只有明确命中
`data_inspection_failed`、`content inspection` 或同类 relay 错误时，保留阶段合同、最终
schema 和当前文件系统状态，丢弃旧 assistant/tool transcript，再继续同一个 Agent 回合。
普通 direct API、Stage02-05 和其他 HTTP 400 不走该分支。

同时修正低成本 Agent 的 receipt 漂移：Agent 有时把已检查但字节未变化的文件列为
`changed_files`。代码现在剔除这些虚假声明，但仍坚持 `approved_with_repairs` 至少交付一个
相对 Stage06 基线真实变化的文件；完全没有实际修改仍归为可重试的客观交付故障。

真实运行 `r5/r6` 证明：中转内容审查可恢复，Stage07 能输出
`approved_with_repairs`、`toolbox_status=needs_software` 和 `resource_status=high_cost`，而
不是把 relay 故障伪装成科学拒绝。

### 5.7 v5-r7/r8/r9：嵌套公开元数据与确定性交付护栏

人工递归验收 r6 发布树时发现，Flash 已清理自主模式的主要说明文件和 XYZ，但
`task_info.json`、`task_spec.json` 的嵌套 `workflow_scope` 中仍残留 workflow/claim ID 和
路线型目标措辞。r7/r8 的定向 Agent 能识别问题，却偶发只在 final JSON 中声明修复而没有
实际写文件；客观交付门禁正确返回 `objective_failure_retryable`。

r9 因此加入一个职责很窄的 public-surface guard。它不选择工作流、不判断科学完整性，也不
生成 Ground Truth，只在 Agent 已给出 approved 类决策后执行不可妥协的公开/隐藏隔离：

- 递归清理 autonomous JSON key/value 和 Markdown 中的已知路线、方法与 claim 标识；
- 删除自主模式中误复制的 reproduction 专用路线文件；
- 同步刷新两个模式的 `public_manifest.json` 和 pair-level manifest；
- 将 guard 的真实文件改动追加到 Stage07 receipt，再由原有客观交付检查验证。

### 5.8 v5-r10：全部 XYZ 的通用中性化与单篇最终验收

r9 的完整论文测试选择了比旧测试更大的 full-paper workflow，共恢复 20 个 SI 坐标。它暴露
了一个 recovery 边界：失败尝试的旧 `Int-*`/`TS-*` 文件可能与 Agent 新生成的
`structure-*` 副本同时被复制到下一尝试。早期 guard 只认识少量固定文件名，无法处理整篇
论文的全部坐标。

r10 将这部分改为论文无关、幂等的确定性处理：

- 枚举两种模式 `data/inputs/` 下的全部 XYZ；
- 用去除自由文本 comment 后的科学 payload 识别 recovery 重复副本，仅删除重复旧名；
- 为所有保留坐标分配稳定的 `structure-NNN.xyz`，两种模式使用同一映射；
- 只把第二行改成 `# structure-NNN`，原子数、元素和坐标记录保持不变；
- 同步改写路径引用、刷新 manifest，并将 Agent receipt 中的旧路径映射到实际交付路径；
- receipt 只保留最终存在的路径，避免重命名前的旧路径再次触发无效 recovery。

真实验收：

- Stage06/07 完整运行：
  `runs/stage06-07-v5-single-paper6904-20260816-r9-guard-flash`；
- 使用同一 Stage06 handoff 的最终 Stage07 验证：
  `runs/stage06-07-v5-single-paper6904-20260816-r10-stage07-guard2-flash`；
- 论文：`paper_6904a9c8c09855cc`，DOI `10.1002/anie.202525581`；
- Stage06：`provisional_constructed`、
  `full_paper_computational_workflow`、high complexity，恢复全文计算流程和 20 个 SI XYZ；
- Stage07：`approved_with_repairs`，保留原工作流，没有 workflow redesign；
- 两种模式的 20 个输入相对路径和 SHA256 全部相同；
- 自主模式对 `Int-*`、`TS-*`、方法名、workflow/claim ID、已知路线词的递归扫描为 0；
- public task 下没有 PDF、source bundle 或 hidden reference；
- 工具箱缺口为 Gaussian 16，成本状态为 `high_cost`，两者均未被错误当成科学拒绝。

验证结果：

- Stage06/07 专项测试：`104 passed`；
- 项目全量：`482 passed`，唯一失败仍为无关 Stage01 外部 PATH 中 `pdfinfo` 的
  `ESTALE`；以 `PATH=/usr/bin:/bin` 单独复跑该测试为 `1 passed`；
- Ruff、`compileall` 和 `git diff --check`：通过。
