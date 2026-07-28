# 化学工具箱问题核查与改进方案

核查日期：2026-07-28

本报告基于当前 `chemistry_toolbox` 代码、`workspaces` 下保留的根轨迹、原生/程序作业终态文件和典型 stdout/stderr。报告不修改工具箱代码，只确认问题、修正归因并给出可实施方案。

## 一、核查口径与主要结论

### 1. 当前轨迹统计

统计时排除了 `_tool_artifacts` 中对中间状态的快照，避免把同一个作业重复计数。

| 层级 | 当前保留轨迹或终态 | 结果 |
|---|---:|---|
| 预设 Action | 432 次 | success 331、partial_success 6、invalid_request 60、failed 32、timeout 3；成功或部分成功 337/432 = 78.0%，排除非法请求后为 337/372 = 90.6% |
| 可编程作业 | 101 个终态 | success 54、failed 38、cancelled 5、timeout 4，与问题描述完全一致 |
| 原生软件作业 | 当前 219 个终态 | success 84、failed 112、cancelled 23 |

原生软件的 `188 = 54 + 112 + 22` 是较早的历史快照。当前目录后续又增加了 30 个成功和 1 个取消作业，因此成功率不能继续写成当前值 28.7%；但 112 个失败仍然完整保留，失败性质没有改变。

当前 112 个原生失败按软件分布为：ORCA 54、Gaussian 53、LOBSTER 4、CREST 1。108/112 在 10 秒内失败，110/112 在 60 秒内失败，确认主要矛盾是输入和兼容性，不是算力不足。当前原生终态中没有 VASP failed；VASP 的坏 POTCAR、结构和参数失败主要出现在 Action 轨迹，因此原问题把两层的 VASP 失败混在了一起。

### 2. 需要修正的两项归因

1. `analyze_crystal_symmetry` 的 24 次 `invalid_request` 大部分不是 Agent 不理解 schema，而是 `workflows` runtime 未安装 ASE，读取 `.vasp` 时抛出 `No module named 'ase'`，随后被错误归类为 `backend_input_error/invalid_request`。这是环境依赖和错误分类问题。
2. 资源预算、统一超时和顶层异常清理已经有实现，不能表述为完全缺失；但单作业内存没有按申请值强制、正常退出没有活动作业终态门禁、取消没有原因字段、Agent 看不到剩余资源，因此执行契约仍不完整。

### 3. 总体判断

| 编号 | 问题 | 核查结论 |
|---:|---|---|
| 1 | 原生软件调用成功率偏低 | 确认，历史比例需注明快照时间 |
| 2 | 原生软件文档不完整 | 确认 |
| 3 | Action 搜索漏召回和误召回 | 确认，可稳定复现示例 |
| 4 | 其他目录搜索基础 | 确认 |
| 5 | 目录文档与代码版本偏差 | 确认，而且不止一份文档漂移 |
| 6 | Action 仍有输入失败 | 确认，但部分“非法请求”实际是环境故障误分类 |
| 7 | Action 覆盖范围有限 | 确认，属于预设目录的设计边界 |
| 8 | 通用编程接口成功率不高 | 确认，101 个终态与描述一致 |
| 9 | 编程接口缺少完整预检 | 确认 |
| 10 | ASE 权限边界不明确 | 架构风险确认；未在本次轨迹中发现 ASE 绕过原生层启动 ORCA/Gaussian 的明确实例 |
| 11 | 三层成功定义不统一 | 确认 |
| 12 | 资源和生命周期需完善 | 部分成立；已有基础机制，但缺少强制闭环 |

## 二、逐项证据与解决方案

### 1. 原生软件调用可靠性

**代码与轨迹证据**

- `validate_native_job` 只对 pysisyphus 实现了软件特定输入预检；ORCA、Gaussian、CREST、VASP 和 LOBSTER 没有对应 validator。
- ORCA 失败可见 `%geom` 中无效的 `TOLG/TOLRMS/TOLMAX`、`%scf` 无效字段、坐标块和引用文件错误。
- Gaussian 失败主要是 `QPErr`、标题被当作整数读取、`End of file in ZSymb`，均属于 route 或空行分段错误。
- CREST 唯一失败是把仅适用于 QCG runtype 的 flag 用在普通构象搜索。
- LOBSTER 失败作业虽生成部分文件，但投影恢复电子数为 `0.0000`，进程失败且科学结果不可用。
- 资源申请和输入 deck 内资源没有交叉校验，例如 ORCA `%pal/%maxcore`、Gaussian `%NProcShared/%Mem` 可以与作业申请不一致。

**解决方案：版本化 NativeAdapter 预检与诊断层**

为每个原生软件实现统一插件接口：

```text
NativeAdapter
  lint_input(request, staged_files) -> PreflightReport
  validate_compatibility(staged_files) -> CompatibilityReport
  reconcile_resources(request, parsed_input) -> ResourceReport
  assess_termination(job_directory) -> ApplicationStatus
  assess_convergence(job_directory) -> ScientificStatus
  diagnose(job_directory) -> StructuredDiagnostic[]
```

优先实现五个 adapter：

| 软件 | 预检内容 |
|---|---|
| ORCA 6.1.1 | `!` 行关键词、`%block/end` 配对、坐标块、外部文件引用、charge/multiplicity、`%pal nprocs` 和 `%maxcore` 与作业资源一致性 |
| Gaussian 16 C.01 | Link0、route、标题、charge/multiplicity、坐标、尾部空行、Gen/GenECP/ModRedundant/Link1 分段和 checkpoint 引用 |
| CREST 3.0.2 | 从锁定版本 help 生成 option schema，检查 runtype 与 flags、输入格式、charge/UHF、线程数 |
| VASP | 用 pymatgen/ASE 解析 INCAR/POSCAR/KPOINTS，校验元素顺序与 POTCAR 拼接、ENCUT、NBANDS、ISYM、LWAVE/LCHARG 和约束格式 |
| LOBSTER 5.1.0 | 校验 POSCAR/POTCAR/WAVECAR/vasprun.xml 一致性、VASP 版本、NBANDS/ISYM/LWAVE、投影基组覆盖和上游正常结束 |

预检只拒绝确定的语法、文件、版本和机械资源矛盾，不替 Agent 选择方法、泛函、基组或收敛阈值。诊断输出必须包含 `stage`、`code`、`evidence`、`likely_cause`、`candidate_fixes` 和 `retryable`，但不自动改输入或自动重试。

**验收标准**

- 建立当前 112 个失败输入的回放集，预检应在执行前拦截至少 90% 的 ORCA/Gaussian/CREST 确定性输入错误。
- 最小有效模板的真实 smoke 成功率必须达到 100%。
- 经过预检的原生作业，进程启动后 10 秒内输入失败率低于 5%。
- 资源 deck 与请求不一致必须在提交前返回结构化错误。

### 2. 原生软件文档体系

**代码与轨迹证据**

- 当前确有 56 个软件指南、69 个命令条目。
- 69 个命令全部有 synopsis/input mode/output behavior，但只有 56 个有 example arguments、32 个有 notes；没有统一的 `common_errors`、`normal_termination`、`scientific_convergence`、`resource_guidance` 或 `working_directory` 字段。
- PDF 和压缩文档在 `_searchable_text` 中被直接跳过。
- 所有根轨迹中，`inspect_software` 仅 24 次、`search_software_documentation` 仅 3 次，而 `submit_native_job` 有 218 次；显式 `validate_native_job` 仅 2 次。提交内部会机械校验，但 Agent 很少主动阅读完整文档或先做独立预检。

**解决方案：文档 schema、模板库和离线章节索引**

扩展 `native_software_guides.yaml`，每个命令必须包含：

```text
tested_versions
working_directory_contract
staging_rules
minimal_templates[]
task_templates[]
resource_mapping
required_upstream_artifacts
normal_termination_rules
scientific_convergence_rules
expected_outputs
common_errors[]
```

模板应作为独立、可测试的真实文件保存，而不是 YAML 中的长字符串。模板只能提供语法结构和显式占位符，不能隐含科学方法选择。每次发布用真实安装版本运行最小 smoke，并把 `template_version` 和测试结果写入指南。

缓存文档时使用 PyMuPDF 或 `pdftotext` 提取 PDF，保留标题、章节、页码、版本、来源 URL 和原文件 SHA-256，建立章节级 BM25 索引。扫描件再使用 OCR，提取失败必须显式记录。

**验收标准**

- 69/69 命令满足新文档 schema。
- ORCA、Gaussian、CREST、VASP、LOBSTER 每类至少有单点/优化或常见后处理模板和 5 个高频错误条目。
- PDF 文档查询可以返回页码、章节和原文件哈希。
- 提交原生作业时记录实际使用的 `guide_version/template_version`；未使用模板也要明确记为 `custom_input`。

### 3. Action 搜索

**代码与实测证据**

`_matches_all_terms` 对所有查询词执行 AND，仅有简单英文后缀截断；结果按 Action ID 排序。当前代码实测：

| 查询 | 结果 |
|---|---|
| `electron density surface` | 1 个，准确找到 `calculate_electron_isodensity_surface` |
| `molecular energy` | 10 个，包含多个宽泛自由能/热化学结果 |
| `single point energy` | 0 个 |
| `conformer energy` | 1 个，但不是 `calculate_energy` |
| `电子能量` | 0 个 |

**解决方案：可解释的混合检索，不做任务特定推荐**

为 ActionSpec 增加 `aliases`、`zh_aliases`、`keywords`、`capability_tags` 和 `scientific_entities`。检索按以下顺序执行：

1. Action ID 和别名精确匹配；
2. 字段加权 BM25，ID/alias 权重大于描述和 backend；
3. 字符 n-gram 处理拼写、连字符和中英文混合；
4. 本地科学文本 embedding 只做召回补充或同分重排；
5. 返回 `score`、`matched_fields`、`expanded_terms` 和 `ranking_reason`。

多词查询不再强制全部 AND。短语精确命中优先，其余使用 `minimum_should_match`；例如 `single point energy` 通过 alias 命中 `calculate_energy`，`conformer energy` 同时召回能量计算和构象排序，但按字段分数排序。

**验收标准**

- 上述五个查询进入固定回归测试。
- 为每个 Action 至少配置一个自然语言 alias；高频 Action 配置中文 alias。
- top-5 recall@5 在人工构建的 200 条中英查询集上不低于 95%。
- 结果仍来自完整冻结目录，不按具体 benchmark task 隐藏或推荐工具。

### 4. 其他目录搜索

**代码证据**

- 软件搜索是整段 substring。
- runtime 搜索也是整段 substring。
- 资源搜索复用 Action 的全词 AND，并按 resource ID 排序。
- Backend 只有 exact `inspect_backend`，没有独立 capability search。
- 文档搜索是逐文件 `str.find`，没有章节和相关性。

**解决方案：统一 SearchDocument，按对象采用不同检索策略**

统一索引协议但不强行共用一种算法：

| 对象 | 首选策略 |
|---|---|
| DOI、CAS、InChIKey、软件 ID、Action ID、Artifact ID | 规范化后 exact match，校验位或格式验证 |
| Action | aliases/tags + BM25 + 可选语义召回 |
| Backend | capability、system type、runtime、资源约束映射 |
| 软件 | ID/alias/executable/version 精确优先，描述 BM25 补充 |
| 文档 | 章节级 BM25/语义检索，返回页码和来源 |
| Resource | 元素覆盖、格式、版本、兼容 backend 和标识符过滤 |
| Artifact | semantic type、producer、parents、media type 和依赖图查询 |

所有检索接口统一返回 `object_type/id/score/matched_fields/exact_match/source_version`，并允许 `query_type=auto|identifier|text|capability`。DOI/CAS 等确定性标识符不得被语义近邻覆盖。

**验收标准**

- 每种对象建立独立查询集和 recall/precision 指标。
- exact identifier top-1 必须为 100%。
- Artifact 可按语义类型和父子 lineage 找到生产者与下游消费者。

### 5. Action 目录文档漂移

**代码与文档证据**

- 当前代码实际为 114 Actions：104 Scientific + 10 Data；77 BackendSpecs。
- `CHEMISTRY_TOOLBOX_THREE_LAYER_ARCHITECTURE.md` 仍写 101/76。
- `TOOLBOX_STATUS.md` 仍写 106/76。
- 自动生成的 `CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md` 已正确写 114/77。

**解决方案：单一事实源和 CI 文档漂移门禁**

所有数量、目录表、catalog hash 和 runtime 状态只从代码及机器可读配置生成。手写架构文档不得硬编码数量，应引用生成片段或在构建时替换标记区块。

CI 执行：

```text
verify_toolbox.py --no-write
tool_manager.py catalog --no-health
generate_tool_resource_matrix.py --check
git diff --exit-code <generated files>
```

再增加断言：所有公开文档中出现的 Action/Backend 总数必须等于当前 catalog，catalog hash 必须一致。

**验收标准**

- 修改 ActionSpec/BackendSpec 后若未更新生成文档，PR 必须失败。
- 发布包只保留一个当前 catalog hash；历史报告必须明确标注为历史快照。

### 6. Action 输入可靠性和错误分类

**代码与轨迹证据**

- 432 次 Action 中，非法请求 60 次、后端失败 32 次、超时 3 次，问题描述的总体统计准确。
- 真实非法输入包括结构 symbols/coordinates 不对齐、周期结构缺 3x3 cell、GPAW LCAO 缺 basis、xTB GFN2 不支持 ethanol ALPB、Artifact 类型链不匹配等。
- `analyze_crystal_symmetry` 的 24 次非法请求主要由 runtime 缺 ASE 导致，不应归咎于 Agent，也不应记为 `invalid_request`。

**解决方案：两阶段验证、运行时契约测试和错误分类修正**

1. `inspect_action` 继续提供完整 schema，但增加可复制的最小 request example、conditional requirement 和 Artifact 输入示例。
2. 执行前运行纯结构验证：输入 schema、单位、周期性、电荷/多重度、Artifact semantic type、backend 条件字段。
3. backend 健康检查必须覆盖真实 parser/import 路径；例如 spglib/pymatgen 读取 `.vasp` 的 smoke，而不只是 `find_spec(spglib)`。
4. 错误分层：`invalid_request` 只用于用户可在提交前修正的输入；缺模块为 `unavailable/runtime_dependency_missing`；程序崩溃为 `failed/backend_exception`；科学未收敛为 `partial_success` 或 `failed/scientific_nonconvergence`。
5. 错误返回中提供 `received`、`expected`、`field_path` 和合法示例。

**验收标准**

- 修复 runtime 后，现有 24 个 `.vasp` symmetry 输入全部不再因缺 ASE 返回非法请求。
- 对历史 60 个非法请求做回放，错误分类准确率达到 95%，且每个错误含字段级修复提示。
- 每个 Action/backend 组合至少有一个合法请求和一个关键非法请求契约测试。

### 7. Action 覆盖边界

**核查结论**

这是预设原子 Action 的天然边界，不应通过把每篇论文流程都固化成 Action 来解决。当前三层架构保留原生接口和编程接口是正确的。

**解决方案：基于轨迹的 Action 晋升机制**

建立 `capability_gap` 记录：未命中搜索、转入原生层/程序层的原因、软件、输入输出语义和是否重复出现。只有满足下列条件才晋升为 Action：

- 至少在多个任务中重复出现；
- 输入输出可以稳定类型化；
- 可以在不替 Agent 选择科学方法的前提下表达；
- 有至少两个真实端到端样例和失败测试；
- provenance 和收敛标准可以统一。

论文专用的一次性后处理继续留在第三层，但提供 Action SDK，使程序输出可声明 schema、父 Artifact、单位和验证规则。新软件先进入原生目录；成熟、重复的原子能力再增加 BackendSpec/Action。

**验收标准**

- 每月输出 top capability gaps、重复次数和处理决策。
- 新增 Action 必须有明确的晋升证据，不接受仅为单一 benchmark 答案定制的 Action。

### 8. 通用编程接口成功率

**代码与轨迹证据**

- 当前 101 个终态正好是 54 成功、38 失败、5 取消、4 超时。
- 作业的 cwd 是独立的 `outputs/execution_jobs/job_*`，不是任务 workspace 根目录。
- 典型失败包括直接读取 `data/benchmark_data/...`、写入未创建的 `report/` 或 `outputs/`、缺 pymatgen、错误 GPAW import、RDKit API 签名错误、None 参与格式化、Python 语法错误和 UTF-8 解码错误。
- 两个 return code `-9` 的长作业无 Python traceback，符合 OOM/外部强杀特征。

**解决方案：明确的 AnalysisJobContract**

把第三层请求改为显式契约：

```text
runtime
script
inputs: [{source_path, target_name, semantic_type, required}]
outputs: [{path, semantic_type, media_type, required, schema}]
result_manifest: outputs/result.json
resource_limits
```

所有输入默认 staging 到 `inputs/`，脚本位于 `code/agent_program.py`，输出只能写 `outputs/`，报告片段写 `report/`；执行前创建这些目录。提供轻量 SDK：

```python
from researchchem_job import input_path, output_path, write_json_result
```

SDK 返回 job-local 绝对路径，并自动创建父目录。环境变量同时公开 `RESEARCHCHEM_JOB_ROOT/INPUTS/OUTPUTS/REPORT`。文档必须明确 cwd 和 workspace 的关系。

**验收标准**

- 历史路径/staging 失败回放中至少 90% 在执行前被拒绝，或使用 SDK 后成功。
- 每个成功程序作业都有声明过的 result manifest 和输出 Artifact lineage。

### 9. 编程接口预检

**代码证据**

`submit_analysis_program` 当前检查 runtime、Python、普通 `.py` 文件、参数路径和资源，但不编译脚本、不解析 imports、不校验输入/输出声明，也不验证科学结果。

**解决方案：在选定 runtime 内执行确定性预检**

新增 `validate_analysis_program`，并由 `submit_analysis_program` 强制调用：

1. `py_compile`/AST 语法检查；
2. 静态提取 top-level imports，在所选 runtime 中用 `find_spec` 验证并返回版本；
3. 检查所有声明输入已 staging，禁止未声明的 workspace 相对路径；
4. 检查 output path 位于允许目录且无冲突；
5. 对输出 JSON 执行 schema、单位、shape、NaN/Inf 和 required fields 验证；
6. 把 preflight report、runtime lock hash 和 import versions 写入 provenance。

动态 import 无法完全静态判断时标记为 warning，并允许 Agent 显式声明 `required_modules`。不要尝试证明任意 Python 程序逻辑正确。

**验收标准**

- 历史语法、缺 import、缺输入文件三类错误在启动前 100% 拦截。
- 对 38 个历史失败作业回放，至少 75% 在实际运行前得到可操作诊断。
- 成功作业的 JSON 结果不得包含未显式编码的 NaN/Inf。

### 10. ASE 与第三层权限边界

**代码证据与风险边界**

- 多个 runtime 安装 ASE；`quantum` runtime 的 PATH 包含 ORCA/OpenMPI。
- `runtime_environment` 还把宿主 PATH 追加到程序 PATH。
- 第三层只靠作业目录和资源限制约束，Python 可以调用 `subprocess`，没有 executable allowlist。
- 已审轨迹中存在 Python/ASE 直接运行 GPAW 的实例，但 GPAW 是进程内 Calculator；未发现明确通过 ASE 启动 ORCA/Gaussian 并绕过原生层的实例。风险是真实可行的架构通道，不应虚报成已发生事件。

**解决方案：runtime 执行策略与子进程 provenance**

为 runtime 增加：

```text
execution_policy: in_process_only | declared_external
allowed_executables: []
```

- `in_process_only`：不继承宿主 PATH，不挂载原生软件可执行文件，只允许 Python 和必要的受控 helper；ASE 的结构、分析、优化器和进程内 Calculator 可用。
- `declared_external`：请求必须声明外部 backend、executable、参数模板和资源；supervisor 监控整个进程树的 exec 事件，为每次外部启动生成独立 `subcall_id`、argv hash、cwd、输入/输出 hash、资源和退出状态。
- ORCA、Gaussian、VASP、LOBSTER 等外部 executable 默认要求走 Action 或原生层。第三层需要它们时，使用受审计子调用代理，而不是直接依赖 ASE 自动启动。

仅清理 PATH 不构成强边界，因为程序仍可能调用绝对路径；应结合容器/mount namespace 隐藏可执行文件，或对 execve 做进程树审计。

**验收标准**

- `in_process_only` runtime 中，ASE ORCA/VASP Calculator 的外部启动测试必须被拒绝并产生结构化错误。
- `declared_external` 中每次子调用都形成独立 provenance；声明次数与监测到的 exec 次数必须一致。

### 11. 三层成功定义

**代码证据**

- Action 有结构化状态，部分 backend 会检查 `converged`，但规则不统一。
- 原生和程序 supervisor 只按 return code 0 写 `success`。
- `collect_execution_job` 只列文件和 SHA-256，不解释结果。
- `declare_scientific_artifact` 的 semantic type 和 parents 由 Agent 声明，工具明确不推断科学意义。

**解决方案：统一分层状态模型**

所有层统一返回下列状态，未知层级写 `not_assessed`，不能直接继承上一级成功：

| 层级 | 含义 |
|---|---|
| interface_status | 请求是否被工具接受 |
| execution_status | 进程是否启动、退出、超时或取消 |
| application_status | 软件是否正常结束，而不是仅 return code 0 |
| convergence_status | SCF/几何/频率/MD/拟合等科学收敛是否满足声明规则 |
| output_status | 必需文件是否存在、完整、非空、版本兼容 |
| parse_status | 预期数值和结构是否可解析、单位和 shape 是否有效 |
| evidence_status | 结果是否足以支持目标结论；通常由任务验证器/Judge 判定 |

顶层 `success` 只表示已达到该工具声明的最高责任边界，并同时返回 `highest_validated_stage`。例如原生 ORCA 进程正常但 SCF 未收敛，应为 `execution=success, application=success, convergence=failed`，不能是无条件成功。

**验收标准**

- 三层共享同一 JobOutcome schema。
- 每个主要软件有正常结束、未收敛、缺输出和不可解析四类 fixture。
- 评分器只接受达到任务要求 stage 的证据，不再把 exit code 0 自动计为科研成功。

### 12. 资源与生命周期

**已有实现**

- `reserve_resources` 使用文件锁统计活动 Action 和后台作业，能够拒绝总 CPU/内存/GPU 超额提交。
- walltime 由 evaluator 统一控制，Agent schema 中没有 walltime。
- supervisor 使用进程组终止超时作业。
- benchmark 在 timeout/stopped/runner_error 时会清理 detached jobs。
- 当前真实 job root 中所有作业均为终态，没有隐藏的 running/queued 作业；看到的 running/queued 文件都位于 `_tool_artifacts` 历史快照中。

**仍存在的缺口**

- supervisor 的 `RLIMIT_AS` 使用任务总预算 `evaluation_budget.memory_mb`，不是单作业申请的 `resources.memory_mb`。
- 正常 `process_exit` 不调用后台作业收集/清理门禁。
- `JobCancelRequest` 只有 job_id，没有取消原因。
- `resource_budget_record` 只返回总预算，不返回 reserved/remaining 和活动作业。
- CPU affinity/线程环境有实现，但缺少跨 MPI、子进程和真实并发的集成验证。

**解决方案：作业租约、cgroup 强制和顶层终态门禁**

1. 每个作业建立持久 lease，由 supervisor 持有到终态，避免仅靠状态文件推断。
2. Linux 上优先使用 cgroup v2 强制 `cpu.max/cpuset.cpus/memory.max/pids.max`；至少先把 `RLIMIT_AS` 改为单作业申请值。
3. 新增 `get_resource_status`，返回 total/reserved/remaining、活动 job ids 和顶层剩余 walltime。
4. 顶层任务所有退出路径都执行终态门禁：等待短 grace；仍活动则取消并记录原因；未收集的必需作业使运行标记为 incomplete。
5. `JobCancelRequest` 增加 `reason_code` 和 `reason`，区分 Agent 主动停止、替代方案、资源调整、顶层超时和 evaluator cleanup。
6. 清理后扫描 owned process tree/cgroup，发现残留则强杀并记录 PID、命令和作业归属。

**验收标准**

- 并发提交压力测试中总资源从不超预算。
- 单作业超过申请内存时被该作业的限制终止，而不是耗尽任务总内存。
- 正常退出、超时、停止、异常四条路径都保证无残留进程，并有状态记录。
- Agent 每次查询都能看到一致的剩余资源和剩余时间。

## 三、建议实施顺序

| 优先级 | 工作 | 原因 |
|---|---|---|
| P0 | ORCA/Gaussian/CREST/VASP/LOBSTER 预检；程序语法/import/path 预检；错误分类修正 | 直接消除多数秒级失败，收益最高 |
| P0 | 统一 JobOutcome；原生/程序正常结束与科学收敛分离 | 防止错误证据进入评估和报告 |
| P0 | 单作业内存强制、剩余资源查询、所有退出路径终态门禁 | 防止资源失控和后台作业丢失 |
| P1 | 原生模板与文档 schema、PDF 章节索引 | 降低输入构造错误并提高自助诊断能力 |
| P1 | Action/Backend/软件/资源/Artifact 分类型混合检索 | 解决工具存在但找不到的问题 |
| P1 | ASE runtime policy 与外部子调用 provenance | 封闭第三条不可细粒度审计的软件路径 |
| P1 | 目录自动生成与 CI 漂移门禁 | 保证分享、审计和评估使用同一事实源 |
| P2 | capability gap 统计和 Action 晋升流程 | 持续扩展覆盖面，同时避免论文专用 Action 污染目录 |

## 四、建议先做的最小闭环

第一阶段不需要重构三层架构，可以先完成四个小闭环：

1. 用当前 112 个原生失败和 38 个程序失败建立不可变回放数据集。
2. 实现五个 NativeAdapter 和 `validate_analysis_program`，以“实际执行前拦截率”为核心指标。
3. 引入统一 JobOutcome，同时保留现有 `status` 作为兼容字段。
4. 将检索查询集、模板 smoke、文档漂移和生命周期测试加入 CI。

完成这四项后，再评估是否需要向量检索、更多 Action 或更重的调度器。这样可以先解决已经被轨迹证明的失败，而不会推翻现有三层架构。

## 五、关键证据索引

| 证据 | 位置 |
|---|---|
| Action 全词 AND、简单词干化和 ID 排序 | `chemistry_toolbox/src/researchchem_toolbox/discovery.py:48`、`:70`、`:839` |
| Resource 使用相同词法匹配且不做相关性排序 | `chemistry_toolbox/src/researchchem_toolbox/discovery.py:1069` |
| 原生校验边界及仅有的 pysisyphus 特定 validator | `chemistry_toolbox/mcp/open_execution.py:220`、`:308` |
| 程序提交当前预检范围 | `chemistry_toolbox/mcp/open_execution.py:602` |
| 原生/程序 success 只取决于 return code | `chemistry_toolbox/mcp/job_supervisor.py:181` |
| PDF 被文档搜索跳过 | `chemistry_toolbox/mcp/software_catalog.py:637` |
| 程序 runtime 继承宿主 PATH | `chemistry_toolbox/src/researchchem_toolbox/runtime.py:115` |
| 单作业 `RLIMIT_AS` 错用任务总内存预算 | `chemistry_toolbox/mcp/job_supervisor.py:35` |
| 顶层只在 timeout/stopped/runner_error 清理后台作业 | `evaluation/run_task.py:1021` |
| 旧架构文档 101/76 与当前生成矩阵 114/77 | `chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_THREE_LAYER_ARCHITECTURE.md:21`、`chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md:9` |

典型失败回放样本：

| Job ID | 证据 |
|---|---|
| `job_9928ee07a3a94a16b470408b976a34bb` | ORCA `%geom` 无效关键词，约 0.2 秒失败 |
| `job_dc399446ec6a4f6abbb9b38e637717f3` | Gaussian 输入分段错误，约 1.2 秒失败 |
| `job_e2dbc955914145208850eb08874ea66d` | CREST flag 与 runtype 不兼容，约 0.27 秒失败 |
| `job_b542936f39c24213854784c82ab3af2c` | LOBSTER 投影恢复 0 个电子 |
| `job_ea6d21db63e847a1bbd821ec0472a670` | 程序错误地从 job cwd 读取 workspace 相对路径 |
| `job_b1a276964b134b7abcfaeb26557c7ae9` | ASE/GPAW API import 错误 |
| `job_d9048cd6e3dc485cb8c3ac4a0986ea48` | Python 语法错误直到实际运行才暴露 |
