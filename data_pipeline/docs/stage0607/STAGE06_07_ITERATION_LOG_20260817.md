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

真实回归运行目录、提交 ID、六篇结果和后续轨迹问题将在任务启动后继续追加。

## 后续记录模板

每轮记录：

1. git commit；
2. 六篇论文的 Stage06/07 状态和完成时间；
3. Agent 是否实际修改任务树；
4. 最终 deterministic findings、Agent outcomes、发布决策；
5. 发现的代码问题；
6. 下一轮通用修复方案；
7. 是否重新提交测试。
