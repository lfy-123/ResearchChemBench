# Stage06/07 通用修复与六篇回归测试记录

## 运行约定

- 模型：`deepseek-v4-flash`
- Harness：`codex`
- 测试集合：每个 Stage05 人工层级各两篇，共六篇
- 不使用论文特例；每一轮只记录通用代码行为
- 软件版本号不参与匹配；只读取已安装软件及 aliases

## Iteration 0：修复前基线

- 代码基线：`ef1bc4c`（installed-software inventory refactor）
- 已知代码风险：Stage07 repair 主路径未执行最终 deterministic task-pair audit；发布门禁主要检查目录和文件存在；工具箱 requirement 未和 installed inventory alias 闭环匹配；输入和 Ground Truth 只做弱存在性检查。
- 代表性现象：Fusadiene 的 receipt 中存在高严重度缺失数据和 Ground Truth，但仍被标为 `approved_with_repairs`。

## Iteration 1：最终门禁、输入完整性和版本无关的软件匹配

- 代码基线：`ef1bc4c`
- 实施状态：代码修改和本地回归测试已完成，真实六篇 Flash 回归待提交。
- Stage06：
  - `provisional_constructed` 不再同时声称 `passed=true`，明确为等待 Stage07 科学审计的 handoff；
  - 对公开输入增加空文件、明显占位文本和全 null/空 JSON 检查；
  - 对 canonical answer 和文字命题增加“待从 SI 提取”“后续补充”等占位检查；
  - Prompt 明确软件版本号不参与缺失判断。
- Stage07：
  - Agent 和机械 public-surface guard 结束后，对最终任务树重新执行 deterministic audit；
  - 最终任务树仍有完整性 finding、Agent receipt 不自洽或仍有非软件 high/blocking 问题时，不能发布；
  - 对最终 JSON 全量收集 evidence 引用并与 `evidence_index.json` 对照；
  - requirement 与 installed inventory 按 ID、显示名和 alias 匹配，忽略版本、大小写和标点；
  - 软件缺口只作为 `needs_software`/建议，不改变科学通过状态；
  - Guard 修改继承文件后同步刷新 `derived_from.json`/`conversion_contract.json` 的来源哈希；
  - deterministic audit 规范化根目录软件缺口后再次刷新模式和任务对 manifests。
- 重复材料复核：Stage06 当前使用 `v2-canonical-deduplicated-inputs` 输入包，正文/SI 的 canonical source 只在只读 source workspace 保存一份，Agent 工作区通过 manifest/evidence index 定位；本轮不再新增复制层或论文特例。
- 静态检查：目标文件 `ruff check` 和 `py_compile` 均通过。
- 单元测试：`tests/test_stage0607_agents.py` 共 `114 passed`。
- 新增/更新回归覆盖：
  - Gaussian 09、Gaussian 16、G09、G16 的版本/alias 等价匹配；
  - 真正未安装软件仍产生 gap；
  - 空/占位输入和 Ground Truth 占位被拦截；
  - 未知 evidence ID 被拦截；
  - Guard 后派生哈希保持一致；
  - 高严重度未解决问题不能被 Agent receipt 直接批准；
  - objective-retry 流程不能把空 handoff 发布成有效任务。
- 本轮发现并修复的新增代码问题：Guard 会修改两个模式继承的输入，但旧的派生哈希仍指向修改前树，导致有效修复被最终门禁误判；现已在 Guard 完成后通用刷新既有 provenance，不跳过校验。

### Iteration 1 真实六篇回归

- Git：`3c8c20b`
- 输出：`runs/stage06-07-tiered-pilot-20260817-flash-r13-final-gate-3c8c20b`
- 时间：52 分 33 秒；六篇 runner 均正常完成，无 API/harness failure。
- Stage06：六篇均为 `provisional_constructed`；工具调用分别为 62、95、80、86、105、69。Gallaphosphene 出现 `input_assets` map/list schema drift，触发 `metadata_materialization_deferred:AttributeError`。
- Stage07：工具调用分别为 95、88、78、94、92、44。六篇 Agent 原始 receipt 均为 `approved_with_repairs`，但 post-Agent deterministic gate 将六篇全部覆盖为 `rejected_scientific_unrepairable`。
- Stage07 token：Codex stdout 中存在真实 `turn.completed.usage`，checkpoint 却全部记录为 0，确认 native Responses usage fallback 缺失。
- Fusadiene：Agent 同时返回 approved 和高严重度关键输入缺失，说明需要 receipt 自洽 recovery，而不是代码科学改判。
- Ni(111)：Stage06/07 Agent 把结构构建说明当成可替代坐标的输入。该现象应由 Stage07 科学审核处理，不在代码中加入论文或结构特例。

结论：Iteration 1 的事后确定性科学门禁与“Agent 负责科学裁决”的设计目标冲突，不能继续作为发布裁决。它的 findings 可用于离线诊断，但不应覆盖 Agent 结果。

## Iteration 2：恢复 Agent 科学裁决与通用编排修复

- 方案文档：`STAGE06_07_CODE_DEFECT_FIX_PLAN_20260817.md` 修订版。
- 实施中：
  - 移除 Stage07 post-Agent scientific gate；
  - approved receipt 若内部矛盾则触发 Agent recovery；
  - public-surface guard 改为 manifest/provenance-only，不修改科学内容；
  - Stage06 map/list 资产声明归一化并回退 task spec；
  - Stage07 预算提升至 120/160，finalization reserve 16；
  - Codex stdout token usage fallback；
  - 软件版本完全忽略，且 prompt 不再承诺代码替 Agent 修复泄漏。

本轮单元测试、Git 提交和第二轮六篇真实回归结果将在验证完成后补充。

## 后续记录模板

每轮记录：

1. git commit；
2. 六篇论文的 Stage06/07 状态和完成时间；
3. Agent 是否实际修改任务树；
4. 最终 deterministic findings、Agent outcomes、发布决策；
5. 发现的代码问题；
6. 下一轮通用修复方案；
7. 是否重新提交测试。

## Iteration 3：目标中心双 Agent Stage06/07 实测

- 方案：`STAGE06_07_OBJECTIVE_CENTERED_TWO_AGENT_REVISION_PLAN_20260817.md`
- 实现版本：`v6-objective-centered-two-agent-20260817` / `v6-objective-centered-audit-repair-20260817`
- 测试论文：`paper_6904a9c8c09855cc`，DOI `10.1002/anie.202525581`
- Harness/模型：`codex` + `deepseek-v4-flash`（API 仍来自 `config.local.env`）
- 输出：`runs/stage06-07-objective-centered-test-20260817-paper6904-codex`

### 本轮代码实现

- Stage06A 改为围绕一个科学目标抽取闭合 workflow，并生成论文复现任务、Objective Card、Key Points 和转换 manifest。
- Stage06B 在独立 workspace 中从复现目录复制并递归清理 autonomous public surface；转换范围覆盖 Markdown、JSON、输入元数据、嵌套文件名和 `data/`，不再依赖旧的四文件白名单。
- Stage07 继续由 Agent 审计和修复；编排器只负责 workspace、文件复制、receipt 和发布目录，不覆盖 Agent 的科学裁决。
- 发布时生成两个物理隔离的 mode bundle，不包含 hidden reference、paper_info、Stage06/07 轨迹或 route/evidence 内部文件。

### 测试结果

- Stage06：`provisional_constructed=1`，`retryable_failures=0`，`toolbox_gaps=0`。
- Stage07：`approved_with_repairs=1`，`selected_workflow_preserved=true`，`workflow_redesign=false`，`toolbox_status=available`，`resource_status=feasible`。
- Stage07 实际修复了 autonomous public surface 的 3 个通用问题：路线竞争信息、特定旋转步骤和特定环结构措辞；论文复现模式保留完整路线信息。
- 第二次 resume 运行确认旧 manifest 会被规范化为 `recursive_autonomous_public_surface`，且 Stage06B 能重新生成 autonomous 目录；Stage07 随后重新审计并发布两个 bundle。
- 发布目录各包含 10 个文件，未发现 hidden、paper_info、stage06、stage07、conversion、workflow、route 或 evidence 文件。
- 回归测试：`385 passed`；`python -m compileall -q src` 通过。

### 轨迹分析与后续建议

- 目标中心闭环、复现→自主转换、Stage07 优先修复原 workflow 的行为符合方案预期。
- 本次 Stage07 不是机械判定：它读取候选、发现公开面泄漏并直接修改三个任务文件，最终以 `approved_with_repairs` 返回。
- 仍需关注成本：Codex 轨迹显示 Stage06B/Stage07 会反复读取同一批公开文件，单篇测试的上下文和工具调用较大。下一步应从 workspace 输入 manifest 和 prompt 去重入手，避免重复材料；不应为本论文添加关键词特例。
- 轨迹中出现一次 Agent 自己编写的 shell 检查错误，随后自行修正，未影响最终产物；这属于 Agent 行为，不应在代码中加入论文特例。
- `direct_api` 仍不适合当前需要 workspace 工具调用的 Agent 角色；应继续使用 `codex`、`claude` 或 `opencode` harness。
