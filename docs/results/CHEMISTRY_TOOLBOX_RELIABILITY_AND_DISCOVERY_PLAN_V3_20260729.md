# 化学工具箱可靠性与检索改进方案 V3

日期：2026-07-29

## 修改总结

第三版修改已经按本方案完成。工具箱仍保持“预设 Action、原生软件接口、通用编程接口”三层通用架构，没有新增按评测任务名称、论文名称或特定数据集分支的 MCP 运行时逻辑，也没有新增论文专用 Action、专用批处理接口或自动科研路线。

本次完成了 56 个软件的显式示例合同和手册语义审计、软件可用性与 smoke 分层、canonical trace 直接交付 Judger、Action discovery 减负与解释字段、embedding 缓存常驻及自动刷新、JobContext 合规诊断、资源阻塞诊断、通用 batch-safe Action、Hessian/EOS/拟合产物校验，以及 Heterobiaryl/PV 复现输入的文件级角色清单。`results.json` 现在直接暴露完整 process metrics，包括 Discovery 字节数、语义检索状态、JobContext 合规数和非受管解释器调用数。最终完整测试为 `422 passed in 455.09s`。

第三版真实轨迹复核后，又对 Action 调用流程做了通用减负：保留 hybrid 检索、分类浏览和完整审计能力，默认 `inspect_action(detail_level=contract)` 改为返回紧凑可执行模板；输入预检和后端适配错误会返回同一 Action/Backend 的修正模板及一次重试规则。该补充修改不改变检索排序、后端实现或科学路线，也不包含评估任务专属分支。补充修改后的化学工具箱完整测试为 `366 passed in 519.56s`。

真实复现 canary `Electron_Isodensity_Reproduction_04_Blind_Prediction` 使用官网 DeepSeek API 和 `deepseek-v4-flash` 完成，21 次 Chemistry MCP 调用全部成功，12 次受管科学 Action 全部成功，结论分 100、过程分 95、最终分 95。canonical trace 的路径、SHA-256、字节数、行数和非法行数已进入 `results.json` 并提供给 Judger。

首次自主 canary 暴露出 Action catalog 变化后 MCP 进程只报告 `stale_embedding_cache`、不会自动重建的问题。该任务已停止，随后在通用语义索引层加入文件锁、原子替换和自动重建；真实英文查询现均返回 `semantic_status=available`，包括 transition-state 自然表达查询。后续 canary 又暴露了 shell 解释器绕行和 JobContext helper 未采用问题，均通过通用提示、预检与审计解决，没有加入任务专属分支。最终自主 canary 的结果记录在本文“真实验收”部分。

## 实施状态与通用性边界

| 范围 | 状态 | 通用性说明 |
|---|---|---|
| MCP Action 检索与执行 | 已完成 | 仅依据 ActionSpec、BackendSpec、输入合同和资源状态运行，不读取 task id 或论文信息 |
| 原生软件文档、lint 与 smoke | 已完成 | 依据软件 id、命令合同和环境证据工作，不包含特定论文路线 |
| 通用程序合同与 JobContext | 已完成 | 对所有 Python 程序统一执行 AST、路径、输入输出和产物合同检查 |
| canonical trace 与 Judger | 已完成 | 由评估运行器统一生成和交付，与具体科学任务无关 |
| Heterobiaryl/PV 文件角色 manifest | 已完成 | 属于 benchmark 输入数据修复，不进入工具箱运行时；只在复现任务中提供，以免向自主任务泄露论文实现路径 |
| 既有 Heterobiaryl smoke evidence | 未改动 | `heterobiaryl_reaction_action_smoke_status.json` 是既有离线覆盖审计证据，不参与 MCP 路由或自动推荐 |
| 模型/API 路由 | 已核对 | 使用 `https://api.deepseek.com/v1` 和原始模型名，不添加 `bailian/` 前缀 |

运行时代码差异检查未发现新增的 `Heterobiaryl`、`Electron_Isodensity`、`PV_CC_CO` 或具体复现任务分支。评估框架中的 `task_id` 仅用于加载任务、结果和评分材料，不影响工具候选、参数、后端选择或失败恢复。

## 实施记录

### 1. 软件手册与示例合同

- 新增 `native_software_example_contracts.yaml`，覆盖 56 个软件和 69 个显式命令合同。
- 每个合同明确声明 `enabled`、`example_kind`、`arguments`、`inputs`、`outputs`、`stdin` 和资源申请，不再根据扩展名猜测 staged input。
- 生成器校验输入输出不重叠、内部并行不超过申请 CPU、stdin 模式合法、disabled 命令不进入可运行示例。
- 修正 OpenMolcas `25.10` 字符串版本、包含冒号的正常结束 marker、Amber launcher、CREST/Psi4/GAMESS/GROMACS/NAMD 资源映射等问题。
- 54 个可运行或可验证条目生成完整的 `INDEX.md`、`QUICKSTART.md`、`COMMON_TASKS.md` 和 `TROUBLESHOOTING.md`；MATLAB 和 EasySpin 因安装/许可不可用，仅保留明确的限制说明，不伪造可运行示例。

### 2. 软件可用性与 smoke 证据

- `list_software` 和 `inspect_software` 分离 executable resolution、接口可提交性、interface smoke 和 scientific smoke。
- 返回 `known_runtime_blockers`、smoke evidence、精确文档 topic 和示例路径。
- VESTA、Arkane、RMG 等已知失败不再仅因 executable 可解析而显示为无条件可用。
- Pysisyphus 的 H2/xTB 最小优化统一记录为 scientific smoke。

### 3. Canonical trace 交付

- `evaluation/trace.py` 对根目录 `_tool_trace.jsonl` 计算 SHA-256、字节数、有效行数、事件数和非法行数。
- `results.json` 新增权威 `canonical_tool_trace` 对象。
- Judger 严格读取该不可变文件；缺失、截断或非法 JSONL 不再静默按空轨迹评分。
- Agent 自建的 `report/tool_trace.jsonl` 只作为普通产物，不能覆盖运行器轨迹。

### 4. Discovery 与 embedding

- `search_actions` 和 category browse 默认返回 compact summary；`inspect_action` 支持 `summary`、`contract`、`full` 三档。
- 返回 `predicted_categories`、`matched_fields`、`ranking_reason`、BM25/semantic 分数和 selected-provider 合同。
- 当智能体指定的 category 隐藏了其他 category 中的精确 Action/alias 匹配时，返回 `category_filter_advisory`、建议 category 和建议 Action；category 仍保持严格过滤语义，不静默混入跨类结果。
- 使用英文 `sentence-transformers/all-MiniLM-L6-v2`，固定模型 revision 和本地 SHA-256，不引入外部向量数据库或中文索引。
- ONNX Session 和向量矩阵常驻进程内存；真实搜索响应约 6–12 KiB，selected-provider contract 约 18–28 KiB。
- canary 发现 stale cache 后，增加跨进程文件锁、临时文件原子替换和 catalog digest 自动重建。索引缺失或 catalog 改变时，首个 hybrid 查询直接重建并返回 `available`，后续查询复用常驻状态。

### 5. JobContext 与通用程序合同

- AST 预检把程序分为 `compliant`、`partial`、`bypassed` 和 `not_adopted`。
- 检测 `ctx.root.parents[...]`、`Path.cwd().parents[...]` 和硬编码 workspace 路径，并返回 `job_context_contract_bypass` warning 及 helper 修复建议。
- 该检查是可靠性诊断，不宣称阻止普通 Python 使用 `open()`、绝对路径或其他库读取文件。
- 评估结果增加提交数、审计数、import 数、合规数、partial 数、bypass 数和未采用数。
- 任务指令和 runtime discovery 均给出相同的最小 JobContext 模板；普通文件写入或不需要程序计算的任务不会被强制制造程序作业。
- `JobContext.input()`、`output()`、`write_json()` 和 `register_output()` 仍是推荐入口，产物收集阶段继续执行 schema、NaN/Inf、表格、图像和 manifest 校验。

### 6. 资源、批处理与科学产物

- 资源拒绝返回 active job、占用资源、阻塞者和 `retry_when` 条件；保护性拒绝与后端执行失败分开统计。
- 新增通用 `submit_action_batch`，最多 32 个子请求；仅 `ActionSpec.batch_safe=true` 的无依赖 Action 可使用，每个子作业保留独立状态、资源、产物和 provenance。
- 首批 batch-safe Action 为 `calculate_energy`、`calculate_hessian`、`optimize_geometry` 和 `calculate_periodic_energy`，接口不包含论文或任务名称。
- Hessian JSON 校验方阵、有限值、对称性和 coverage；EOS 校验有限且唯一的体积-能量点；拟合结果记录状态、样本数、参数、残差和失败原因。
- 明确保持机械有效、软件收敛、产物可解析和科学结论正确为不同层级，最终科学结论仍由 Judger 评价。

### 7. 真实 canary 驱动的通用修复

- `resource_limits: null` 统一映射为既有默认资源，避免可选对象被误判为非法请求。
- 电子密度 Action 合同明确要求 `ElectronDensityResult` ArtifactRef，并给出下一步 artifact-id 示例，不允许把 `.gbw` 路径误当密度结果。
- `cutoffs_au` discovery 合同修正为数值数组，声明范围和示例；Multiwfn 后端同时兼容清晰的逗号/空白分隔历史输入，并在 warning/provenance 中记录规范化。
- CREST、ORCA、Multiwfn 等修复均依据通用输入类型和软件合同实现，没有对 canary 任务设置条件分支。

## 真实验收

### 已完成的论文复现 canary

| 指标 | 结果 |
|---|---:|
| 任务 | `Electron_Isodensity_Reproduction_04_Blind_Prediction` |
| 模型 / Judge | `deepseek-v4-flash` / `deepseek-v4-flash` |
| API | `https://api.deepseek.com/v1` |
| 运行时长 | 447.148 s |
| Chemistry MCP 调用 | 21 成功 / 0 失败 |
| 受管科学 Action | 12 成功 / 0 失败 |
| 工具运行时间 | 290.432606 s |
| 结论分 / 过程分 / 最终分 | 100 / 95 / 95 |
| Agent token | 1,702,071（含 cache read 1,578,624） |
| Judge token | 89,405 |
| canonical trace | 21 行，87,412 bytes，0 非法行 |
| trace SHA-256 | `317c476630e2043470c3ebc5c1c64ca5c081d27a6218b4f514382a243fe5957a` |

该 canary 完整执行了 ORCA correlated density、ArtifactRef 传递、波函数导出和 Multiwfn isodensity surface。唯一扣分是四个独立分子顺序运行，未充分利用并发；没有输入失败或后端失败。

### 已完成的自主科研 canary

| 指标 | 结果 |
|---|---:|
| 任务 | `Electron_Isodensity_04_Blind_Prediction` |
| 模型 / Judge | `deepseek-v4-flash` / `deepseek-v4-flash` |
| API | `https://api.deepseek.com/v1` |
| 运行目录 | `workspaces/v3_program_canary_compliant/runs/cli_runs/batch_20260729_132126_4b700f` |
| 运行时长 | 433.63 s |
| Chemistry MCP 调用 | 43 成功 / 0 失败 |
| 受管科学 Action | 26 成功 / 0 失败 |
| 非法 Chemistry 请求 / 后端失败 | 0 / 0 |
| hybrid 搜索 | 4 次，4 次 `semantic_status=available` |
| Discovery 返回量 | 135,176 bytes |
| `inspect_action` 返回量 | 114,830 bytes |
| 编程接口 | 本任务未提交程序作业；未通过 shell 启动解释器 |
| 结论分 / 过程分 / 最终分 | 100 / 89 / 89 |
| Agent token | 3,732,654（含 cache read 3,570,944） |
| Judge token | 75,840 |
| canonical trace | 43 行，190,379 bytes，0 非法行 |
| trace SHA-256 | `e4f368ed781a36b8b3db5e64a203173e46d7842574ef59372bd106d2f065eb7d` |

该任务独立完成 RDKit 结构生成、GFN2-xTB 优化、CREST 构象检查、ORCA 密度计算、WFN 导出和 Multiwfn 等密度面分析。科研过程扣分来自只验证一套电子密度协议和独立计算顺序执行，不是工具失败。原生 Agent 轨迹中有一次把 MCP 工具写成无前缀 `list_analysis_runtimes` 的无效调用，下一步立即使用实际暴露的工具名成功恢复；该事件不属于 Chemistry MCP 后端失败。

四次 hybrid 搜索中，前三次 Top-1 与意图一致。第四次将 `geometry optimization` 错误限定在 `structure_and_system`，因严格 category 过滤隐藏了 `molecular_electronic` 中的精确 alias。为解决这类通用分类误用，检索响应现会返回跨分类精确匹配 advisory；直接回归查询建议 `optimize_geometry` 和 `molecular_electronic`，同时保留 category 的严格过滤合同。

### 回归测试

- 最终完整测试：`422 passed in 455.09s`。
- embedding 自动刷新与 progressive discovery 专项测试：`18 passed in 7.50s`。
- catalog 变化后的真实英文查询：`electron isodensity surface`、`find a stationary structure with one negative curvature`、`conformer free energy ranking` 均返回 `semantic_status=available`，Top-1 分别为 `calculate_electron_isodensity_surface`、`locate_transition_state`、`rank_conformers_from_results`。

## 一、评价采纳结论

| 评价 | 结论 | V3 处理 |
|---|---|---|
| 软件手册和示例存在语义错误 | 采纳，最高优先级 | 增加显式输入/输出角色、资源映射、版本和 smoke 状态 schema，取消扩展名猜测 |
| discovery 返回体需要压缩 | 采纳并收窄范围 | `list_analysis_runtimes` 已有 `include_details`，不重复改造；重点处理 `search_actions`、category browse 和 `inspect_action` |
| JobContext 应作为默认入口 | 采纳 | 统计合规使用而非 import 次数，并诊断绕过 helper 的路径写法 |
| canonical trace 应由运行器交付 | 采纳，最高优先级 | `results.json` 记录不可变 trace 的路径、SHA-256、行数和大小，Judger 直接读取 canonical 文件 |
| 批量 Action 应通用化 | 采纳 | 实现通用 `submit_action_batch`，由 `ActionSpec.batch_safe` 控制，不增加论文专用 Action |
| 资源查询需要补全 | 部分采纳 | 查询接口和 budget/reserved/available 已存在，只补 active jobs、阻塞者和重试条件 |
| 文档检索应嵌入失败恢复 | 采纳但依赖手册修正 | 先保证手册和示例正确，再由 inspect/lint 返回精确章节和已测试示例 |
| interface/scientific smoke 需要统一 | 采纳，最高优先级 | 将 executable resolution、interface smoke、scientific smoke 和可提交性分开暴露 |
| 科学产物验证需要继续增加 | 部分采纳 | 不重复 MDCI cube 电子数积分和 GoodVibes 基本元数据，只补 Hessian coverage、EOS 和拟合结果校验 |
| Heterobiaryl/PV manifest 必须补齐 | 采纳，重跑前置条件 | 复现任务提供无结果数值的逐文件角色与配对 manifest；自主任务不暴露论文路径角色 |
| 必须用真实任务验收 | 采纳 | 先运行一个低成本 canary，达标后再决定是否批量重跑 |

## 二、P0 必须修正项

### 1. 修复软件手册和示例请求的语义正确性

当前结构覆盖已经完成，但语义正确性尚未完成。已确认的问题包括：

- `generate_native_software_manuals.py` 的 `_specific_targets()` 根据文件扩展名猜测 staged input，导致 Psi4 的 `output.dat` 等输出参数被错误 staged。
- CREST、Psi4、GAMESS、GROMACS 和 NAMD 的 Quickstart 请求申请 1 CPU，但示例命令使用 4 线程或 4 进程。
- NAMD、OpenMolcas、PLUMED、SIESTA 和 Wannier90 的部分正常结束标志因未加引号的冒号被 YAML 解析为字典。
- OpenMolcas `25.10` 被 YAML 数值解析并生成成 `25.1`。
- Amber PMEMD 明确说明通用 `mpirun` 未开放，但生成文档仍把 `mpirun` 列为支持命令。
- smoke 失败、取消或仅到达 executable 的状态没有进入 `inspect_software` 的结构化返回。

修改方案：

1. `native_software_guides.yaml` 的每个命令显式声明 `inputs`、`outputs`、`arguments`、`stdin`、`fixed_files`、`resource_mapping`、`enabled` 和 `example_kind`，不再从扩展名或参数位置猜测文件角色。
2. 所有版本号和包含冒号的 marker 强制使用字符串；生成器拒绝 marker 中的 dict/list 和非字符串版本。
3. 示例请求的 `cpu_cores` 必须大于等于命令内部线程、MPI rank 或 worker 数；无法可靠推断时，示例不写并行参数。
4. disabled/unresolved launcher 不进入“支持命令”表和 Quickstart 主示例，只在限制说明中出现。
5. 每个示例同时声明 expected outputs；提交前验证 staged inputs 与 outputs 不重叠。
6. 重新生成 56 个目录并逐项运行 schema lint。可调用软件的示例必须通过 `validate_native_job`；科学 smoke 只对具有合法最小科学输入的条目声明。

验收标准：

- 56 个软件 profile 和 guide 全部通过结构及类型校验。
- 生成示例中输出文件被 staged 的数量为 0。
- 示例内部并行参数超过申请 CPU 的数量为 0。
- YAML marker 被解析为非字符串的数量为 0。
- disabled/unresolved 命令被展示为可用命令的数量为 0。
- 文档版本与实际检测版本逐字符串一致；`25.10` 不再变成 `25.1`。

### 2. 统一软件可用性和 smoke 状态

当前 `available=true` 主要表示 executable 或 Python runtime 可以解析，不代表软件能在当前环境中完成接口调用或科学任务。例如 VESTA 缺少 GUI 共享库仍返回 available，Arkane/RMG 超过 smoke 截止时间也没有在 inspect 结果中暴露。

`list_software` 和 `inspect_software` 增加以下独立字段：

- `executable_resolved`：命令路径是否存在。
- `interface_smoke_status`：`passed`、`started_input_required`、`failed`、`cancelled`、`skipped` 或 `not_tested`。
- `scientific_smoke_status`：`passed`、`failed`、`not_tested` 或 `not_applicable`。
- `available_for_submission`：当前接口是否允许提交，不代表科学成功。
- `known_runtime_blockers`：缺失库、许可、GUI、数据库或长期启动问题。
- `smoke_evidence`：manifest 路径、测试时间和 hash。

Pysisyphus 的 H2/xTB 最小优化已经真实收敛，应将其证据级别统一为 `scientific_smoke`。VESTA、Arkane 和 RMG 不得仅因 executable 可解析而显示为无条件可用。

### 3. 由运行器向 Judger 交付 canonical trace

canonical `_tool_trace.jsonl` 在 10 个完整任务中均存在且可读取，但 Agent 自建的 `report/tool_trace.jsonl` 有空文件和极小占位文件。审计证据不应由被评估 Agent 自己复制或重写。

修改方案：

- `results.json` 的 `artifacts.tool_trace` 改为对象，记录相对路径、SHA-256、字节数、有效 JSONL 行数和生成者 `evaluation_runner`。
- Judger 始终从 workspace 根目录读取 canonical trace，并在评分输入中携带上述完整性元数据。
- `report/tool_trace.jsonl` 不再是 Agent 必须生成的交付物；若存在，只作为普通 Agent 产物，不能覆盖 canonical trace。
- trace 不复制到 report，避免产生两个可能漂移的真实来源。

验收标准：10/10 历史完整任务都能重新生成相同 trace hash/line metadata；缺失、截断或非法 JSONL 会在评分前明确失败，而不是静默按空轨迹评分。

### 4. 补齐 Heterobiaryl/PV 文件级角色与配对 manifest

现有 `author_output_manifest.json` 主要停留在 zip 的 state/path/size/hash，无法告诉 Agent 哪个 Gaussian frequency 文件对应哪个 DLPNO 或 QZ 文件，也无法可靠映射原始 `Py/Ph/OMe/ax` 名称与评估路径角色。

为复现任务提供英文文件角色 manifest，每条记录包含：

- archive state 和原始相对路径；
- normalized structure id、stationary-point role、path family 和 conformer id；
- charge、multiplicity 和 calculation type；
- frequency、DLPNO、QZ 文件的显式配对和 SHA-256；
- 是否满足该路径所需的 minimum/TS/intermediate/product 角色。

manifest 不包含能量、势垒、排序、选择性或论文结论。自主任务继续使用与复现任务相同的公开分子和原始输出输入边界，但不获得论文 stationary-point/path-family 配对标签，避免把论文实现方法和路径直接泄露给自主科研 Agent。新增 validator 检查复现任务每个评估路径所需角色和文件配对是否完整。该项是 Heterobiaryl/PV 重跑的前置条件。

## 三、P1 可靠性与成本改进

### 5. 压缩 discovery 返回体

`list_analysis_runtimes` 已支持 `include_details`，保留现状。主要修改：

- `search_actions` 默认只返回 action id、category、短描述、输入输出语义类型、provider ids、relevance 和 ranking reason；不为每个结果重复返回资源预算、timeout、provider health、完整 aliases/keywords。
- category browse 使用同一 summary schema。
- `inspect_action` 增加 `detail_level=summary|contract|full`：`summary` 用于比较候选，`contract` 只返回选定 provider 的执行合同，`full` 用于调试和审计。
- 资源预算放在响应顶层一次；provider health 只在显式请求或 full 模式返回。

验收以第二版同一批 discovery 调用回放为准：总返回量至少降低 50%，`inspect_action` 返回量至少降低 60%，真实查询 Top-1/Top-5 相关性不得下降。

### 6. 提高 JobContext 合规采用率

不能只统计是否 import `JobContext`。合规使用定义为：声明 inputs/outputs，使用 `ctx.input()`/`ctx.output()`/`write_json()`/`register_output()`，且不通过 `ctx.root.parents[...]`、`Path.cwd().parents[...]` 或硬编码 workspace 路径绕过合同。

修改方案：

- runtime discovery 继续返回可执行最小模板，但模板正文直接展示命名 input 和 registered output 的完整路径。
- Python AST 预检对上述绕过写法返回 `job_context_contract_bypass` warning，并给出等价 helper 修复；它是可靠性诊断，不是 OS 权限边界。
- results/process metrics 增加 `job_context_import_count`、`job_context_compliant_job_count` 和 `job_context_bypass_count`。
- canary 中所有声明式程序作业应达到 100% 合规；确需非标准路径时必须在合同中显式声明并保留 provenance。

### 7. 补齐资源阻塞和重试信息

保留现有 `get_execution_resources` 及 budget/reserved/available，不重复建设接口。增加：

- active job id、job type、申请资源和当前状态；
- 哪些 active jobs 阻塞本次请求；
- `retry_when` 条件，例如可用 CPU/内存达到请求值或指定 job 进入终态；
- 资源拒绝继续计为 protective rejection，不计入 backend execution failure。

### 8. 增加通用 batch-safe Action

实现通用 `submit_action_batch`，批次元素共享 action id 和 backend id，各自保留独立 inputs、状态、资源、产物和 provenance。只有 `ActionSpec.batch_safe=true` 的无相互依赖 Action 可以批量提交。

首批允许 ORCA optimization/Hessian 和 VASP single-point/EOS 采样等真实轨迹中重复度高的 Action，但接口和数据模型不得包含任务名称或论文逻辑。部分子作业失败不应抹掉其他子作业结果。

### 9. 在手册修正后接入失败恢复

手册通过 P0 语义审计后：

- `inspect_software` 根据 calculation intent 返回一个推荐 topic、一个经过验证的 example path 和当前 smoke 边界。
- 原生 lint 错误返回精确 troubleshooting 文档、section 和错误代码。
- 只有无法精确路由时才执行文档 BM25/semantic 搜索。

不强制正常调用读取完整手册，也不把官方手册全文注入上下文。

## 四、P2 科学证据与真实验收

### 10. 只补尚未完成的科学产物验证

以下能力已经存在，不重复开发：MDCI cube 的电子数积分、误差百分比和严格验证；GoodVibes 的 population basis、温度和标准态记录。

新增范围限定为：

- ensemble 结果记录有效 Hessian 数量、总构象数量、coverage 比例和缺失构象 id；
- EOS 表格检查必需列、单位、有限值、体积单调性和每点状态；
- 拟合结果记录模型、成功/失败状态、参数、残差摘要、样本数和失败原因；
- 科学产物机械有效不等同于科学结论正确，最终结论仍由 Judger 评分。

### 11. 使用一个低成本 canary 做端到端验收

代码和离线查询通过后，选择一个能覆盖 discovery、Action、至少一个程序作业和 canonical trace 的低成本代表任务。canary 必须同时满足：

- 所有 hybrid 搜索均为 `semantic_status=available`，Top-1 人工相关；
- discovery 返回字节数达到压缩目标；
- 所有声明式程序作业合规使用 JobContext；
- canonical trace path/hash/lines/bytes 进入 results 和 Judger；
- 软件 inspect 显示真实 smoke 和 blocker，不出现已知假阳性 available；
- 无输出文件误 staged、无内部并行超过申请资源；
- 请求拒绝、保护性拒绝和后端失败分开统计。

canary 达标后再决定是否重跑第二版任务集。离线固定查询、单元测试和 smoke 证据仍是回归保障，但不能替代 Agent 端到端轨迹。

## 五、明确不做的改动

- 不推翻 Action、原生软件和通用编程三层架构。
- 不增加外部向量数据库、多 embedding 模型或中文检索；继续使用英文 `all-MiniLM-L6-v2`。
- 不建设 56 个软件的完整语法解析器，只校验明确且高频的执行合同错误。
- 不把 JobContext 描述成 Python 权限沙箱。
- 不增加论文专用批处理接口或把论文结论写入公共 manifest。
- 不重复实现已经存在的 density electron-count 和 GoodVibes 基本元数据功能。

## 六、完成定义

第三版完成不能只以测试通过或文件存在判断。必须同时满足：软件手册语义 lint 全通过、inspect 软件状态与 smoke 证据一致、canonical trace 自动进入评分材料、Heterobiaryl/PV manifest validator 通过、discovery 真实回放达到减负目标、JobContext 合规率可统计、资源重试信息完整、batch 子作业可独立审计、剩余科学产物校验生效，以及一个真实 canary 端到端通过。

## 七、补充修改记录：简化 Action 调用流程

### 问题确认

第三版仍然要求智能体按照 `search_actions -> inspect_action -> execute_action` 调用 Action，但默认 selected-provider contract 同时包含完整参数元数据、后端固定参数、健康状态、资源预算和执行策略。真实轨迹中，智能体在主流程 Action 上通常会先 inspect，但在失败后的 xTB、ASE、RDKit 等备选 Action 上会直接调用，随后因缺少必填字段或输入类型不匹配而失败。典型问题包括：

- xTB 几何优化缺少 `action_settings.optimization_level`；
- ASE 几何优化缺少 `fmax_ev_per_angstrom` 和 `optimizer`；
- RDKit 聚类缺少 `random_seed` 或把 JSON 摘要路径当作构象文件；
- CREST 收到多构象集合，而不是一个带坐标的起始结构；
- 失败响应只有缺字段或异常文本，没有可直接修改的同后端请求模板。

这些问题属于通用 Action 合同和失败恢复问题，不属于 hybrid 检索错误。此次修改没有回退 BM25、aliases、分类检索、MiniLM semantic recall、排序解释或 embedding 缓存。

### 已完成修改

1. `inspect_action` 的 `contract` 档改为紧凑执行合同，只保留最小请求模板、必填输入、必填方法和设置、枚举值、关键可选输入、条件约束、输出类型和一次重试规则。provider 信息使用 compact summary；健康、运行时、完整资源和固定参数仍可通过 `detail_level=full` 获取。
2. `execute_action` 工具说明明确要求从精确 Action/Backend 的 compact template 开始填写。收到 `repair_guidance` 后，应先修正同一请求并重试一次，再考虑切换后端；工具箱仍不自动选择科学参数、自动重试或自动 fallback。
3. 通用输入类型合同补充 `molecule`、`initial_structure` 和 `ensemble`。构象集合明确接受 typed `ConformerEnsemble` ArtifactRef、结构化 ensemble/conformers mapping、SDF/MOL 或多帧 XYZ；明确拒绝 JSON 摘要路径和单结构替代多构象集合。
4. CREST 合同明确要求一个完整、有坐标的起始结构，拒绝 ensemble/trajectory；同时声明 `inputs.initial_structure` 存在时覆盖 `inputs.molecule`，提交前必须显式选择一帧。
5. Action 预检对缺失 inputs、backend-specific inputs、component roles、method fields、action settings 和非法枚举值返回：`missing_fields`、`allowed_values`、`inspect_action_request`、`corrected_request_template`、`repair_guidance` 和 `retryable=true`。修复模板保持原 Action 和 Backend，不替智能体选择科学值。
6. Worker 对 adapter `ValueError` 返回结构化 `backend_input_error`，要求修改请求后再重试；对 CREST、xTB、ASE 等已知输入敏感的运行失败补充输入要求。未知运行时异常不会被无条件标记为可重试。

### 返回体与兼容性

代表性 selected-provider 响应的 compact/full JSON 比例如下：

| Action / Backend | compact 字节 | full 字节 | compact/full |
|---|---:|---:|---:|
| `optimize_geometry` / `xtb` | 4,494 | 13,251 | 33.9% |
| `cluster_conformers` / `rdkit` | 4,514 | 11,308 | 39.9% |
| `generate_conformer_ensemble` / `crest` | 4,341 | 16,580 | 26.2% |

`detail_level=full` 的原有 `sections`、`backend_fixed_parameters`、资源上限、参数 impact 和审计信息保持不变，现有完整目录验证和审计调用继续兼容。默认 MCP `ActionInspectRequest` 仍使用 `contract`，因此正常执行路径自动获得更小、更直接的合同。

### 验证结果

- 新增 compact contract 测试，覆盖 contract/full 分层、RDKit 构象格式、JSON 摘要拒绝、CREST 单结构和 `initial_structure` 覆盖规则。
- 新增 Action 修复提示测试，覆盖 xTB 缺少必填设置和非法枚举值时的修正模板、allowed values、同 Backend 保持和 retryable 语义。
- 更新 Worker 错误分类测试，验证 changed-request 重试要求和精确 `inspect_action` 请求。
- 相关定向回归：`50 passed in 45.61s`。
- 化学工具箱完整回归：`366 passed in 519.56s`。
- `check_english_only.py` 和 `git diff --check` 均通过。

### 通用性检查

本次运行时代码只根据 `ActionSpec`、`BackendSpec`、action id、backend id 和公共输入语义生成合同与诊断。没有读取 benchmark task id、论文名称、真实答案或工作空间任务目录；没有新增论文专用 Action、专属后端分支或固定科研路线。RDKit、CREST、xTB 和 ASE 的提示是软件/Action 公共输入合同，适用于所有使用这些能力的任务。
