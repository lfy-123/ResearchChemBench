# 化学工具箱可靠性与检索改进方案 V3

日期：2026-07-29

## 修改总结

第三版方案以第二版 10 个完整任务的真实运行轨迹为依据，保留现有三层架构和已经有效的改动，不重复实现已经完成的能力。最高优先级从“继续扩充文档”调整为“修正软件手册、示例请求和运行状态的语义正确性”。

本次基线为：495 次 Chemistry MCP 调用中，453 次成功、41 次 `invalid_request`、1 次后端直接失败；discovery 返回 2,137,800 bytes，其中 68 次 `inspect_action` 返回 1,339,413 bytes；11 次 Action 搜索在第二版运行时均未真正使用 embedding。当前语义环境已修复，但尚未经过新的完整 Agent 任务端到端验证。

第二版共有 23 个通用程序作业提交，终态为 19 成功、3 失败、1 取消。5 个 Agent 程序导入过 `JobContext`，但通过 `ctx.root.parents[2]` 或 `Path.cwd().parents[2]` 绕回任务 workspace，没有合规使用 `ctx.input()`、`write_json()` 或 `register_output()`，因此合规采用率仍为 0。

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
| Heterobiaryl/PV manifest 必须补齐 | 采纳，重跑前置条件 | 为自主和复现任务同步提供无结果数值的逐文件角色与配对 manifest |
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

为自主任务和对应复现任务提供完全相同的英文 manifest，每条记录包含：

- archive state 和原始相对路径；
- normalized structure id、stationary-point role、path family 和 conformer id；
- charge、multiplicity 和 calculation type；
- frequency、DLPNO、QZ 文件的显式配对和 SHA-256；
- 是否满足该路径所需的 minimum/TS/intermediate/product 角色。

manifest 不包含能量、势垒、排序、选择性或论文结论。新增 validator 检查每个评估路径所需角色和文件配对是否完整。该项是 Heterobiaryl/PV 重跑的前置条件。

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
