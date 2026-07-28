# 化学工具箱三层执行架构修改报告

日期：2026-07-21

## 1. 结论

本次重构已经把 ResearchChem 工具箱从 Action-only 改为三层并列架构，同时完整保留原有 101 个 Action。智能体现在既可以使用经过统一校验的常用 Action，也可以在没有合适 Action 时自行编写软件原生输入并调用软件，或者编写 Python 程序组合已有化学库完成论文特定操作。

三层均不提供固定科研流程。系统不会替智能体选择 Action、software、backend、runtime、方法或科学参数，不在失败后调用 callback，不更换默认参数，也不自动 fallback。

重构前状态已保存为 Git 提交：`2fb0583 Checkpoint toolbox before open execution layers`。

## 2. 最终规模

| 项目 | 数量 | 结果 |
|---|---:|---|
| Scientific Actions | 91 | 全部保留 |
| Data Actions | 10 | 全部保留 |
| Actions 合计 | 101 | MCP 第一层 |
| BackendSpecs | 76 | 原有显式 backend 选择保持不变 |
| 开放执行 MCP 工具 | 13 | 第二、三层及共用文件/产物工具 |
| MCP 工具总数 | 114 | 101 + 13 |
| 原生软件指南 | 56 | 机器可读且进入系统提示词 |
| 原生命令说明 | 69 | 68 个策略允许，1 个通用启动器禁用 |
| 当前可解析的原生命令 | 66 | 另外 2 个等待 MATLAB |
| 已配置 runtime | 45 | 主 backend runtime 与 auxiliary runtime 合并展示 |
| 当前可执行 Python 的 runtime | 41 | 其余 4 个为 MATLAB/EasySpin/VMD/VESTA 非 Python 环境 |
| 软件/库/接口联合清单记录 | 106 | Backend、文档和请求清单归并后的标识；其中 92 项至少有可用原生入口、Python 模块或内部 provider |

“联合清单记录”不是 106 个独立商业软件安装包的数量。它还包含程序库、数据接口、同一软件的 backend 变体和内部 provider，用于让智能体看到完整能力与可用状态。

## 3. 三层改造内容

### 3.1 第一层：预定义 Action

- 保留 101 个现有 Action 的名称、`ActionRequest`、backend 显式选择、执行逻辑和测试。
- `catalog_snapshot` 升级到 schema 5，明确记录三个执行层以及 Action 非强制。
- 系统提示词把 Action 描述为“常用、验证过的科学操作”，不再描述成工具箱能力边界。
- Action 失败后，下一步仍由智能体决定；提示词明确允许重新提交 Action、改用原生软件或编写程序。

### 3.2 第二层：软件原生执行

新增机器可读文件 `config/native_software_guides.yaml`。每个条目包括：

- `software_id` 与精确 runtime；
- 允许的 executable；
- 原生调用 synopsis；
- 参数、stdin 或 fixed-file 输入模式；
- 必需文件类型；
- 输出行为；
- 示例 argv；
- 软件特有的机械调用注意事项。

命令必须由 `BackendSpec.executables` 或 `requested_software.yaml` 明确登记。启动时会校验 40 个可执行 BackendSpec 全部有指南，也会校验 runtime-only 命令没有脱离原始软件清单。

除了已有 Backend executable，本次把以下未作为独立 Action backend 暴露的能力接入原生层：

| 软件/框架 | 原生入口 |
|---|---|
| QCEngine | `qcengine` |
| AiiDA | `verdi` |
| CENSO | `censo` |
| geomeTRIC CLI | `geometric-optimize` |
| Wannier90 | `wannier90.x` |
| Arkane | `Arkane.py` |
| AutoMeKin/MOPAC | `amk.sh`、`mopac`、`bbfs.exe` |
| KinBot | `kinbot`、`pes` |
| SHARC | `sharc.x`、`wfoverlap.x`（映射本地 ASCII build） |
| Newton-X | `nx_geninp`、`nx_moldyn`、`nx_test` |
| TheoDORE | `theodore` |
| Yambo | `p2y`、`yambo` |
| VMD | `vmd` text mode |
| VESTA | `VESTA`，GUI/headless 限制写入指南 |
| MATLAB/EasySpin | `matlab` 调用契约已写好，当前因许可证/安装缺失显示 unavailable |

新增的执行工具为：

1. `list_software`
2. `inspect_software`
3. `search_software_documentation`
4. `write_workspace_text`
5. `read_workspace_text`
6. `validate_native_job`
7. `submit_native_job`
8. `get_execution_job`
9. `collect_execution_job`
10. `cancel_execution_job`

原生执行器只接受列表形式 argv，始终 `shell=false`。`software_id` 和 executable 必须命中双重白名单；绝对 host 路径、`..`、symlink 路径和作业控制文件覆盖会被拒绝。所有源文件都必须显式映射到作业目录中的目标文件名。

子进程环境采用白名单继承：MCP 进程中的 API key、认证 token、SSH 变量和其他无关凭据不会传入 Agent 程序。runtime 明确声明的软件路径、数据库、许可证变量，以及有限的调度器/设备变量会保留。已提交的 `outputs/execution_jobs/` 也不能通过公开文本写入工具改写。

### 3.3 第三层：可编程科学分析

新增：

1. `list_analysis_runtimes`
2. `submit_analysis_program`
3. `declare_scientific_artifact`

主 runtime 与此前只用于审计的 `auxiliary_environments.yaml` 现在统一进入可查询 runtime 清单。智能体可以看到固定 Python 路径、模块与版本、已配置命令和相关 backends。AiiDA、atomate2、jobflow 等不需要 Action 的程序库可以直接在 `workflows` 环境中由智能体程序调用。

程序层只执行保存到 workspace 的完整 `.py` 文件，不提供隐藏 inline 代码。脚本、参数和每个输入都被复制并哈希；智能体必须明确选择 runtime。程序输出可以通过 `declare_scientific_artifact` 获得语义类型、媒体类型、生产者、SHA-256 和父 Artifact 关系。

## 4. 持久作业与超时设计

原生程序和 Agent 程序使用同一个持久作业监督器：

- `submit_*` 创建 `outputs/execution_jobs/job_<uuid>/` 后立即返回；
- 独立 supervisor 在 MCP 调用结束后继续执行；
- `status.json` 记录 queued、running、success、failed、timeout 或 cancelled；
- stdout、stderr、精确命令、输入哈希、返回码、CPU 使用、最大 RSS 和输出哈希持久化；
- walltime、CPU affinity/线程数和可选地址空间上限在子进程层实施；
- 超时或取消会终止目标进程组，不会启动替代计算。

因此 MCP/OpenCode 超时只需覆盖提交和查询，不必设置成一小时。科学计算可以拥有独立的 `resource_limits.walltime_seconds`。

## 5. MCP 与提示词

MCP 服务器当前注册 114 个工具，并提供三个资源：

- `researchchem://catalog`
- `researchchem://software`
- `researchchem://execution-policy`

系统提示词仍按化学领域分类列出所有 Action，同时增加 56 个软件的命令 synopsis。智能体被明确要求在原生调用前使用 `inspect_software`，由该工具返回本机实际 executable、输入模式、文件要求、输出行为、示例请求、本地缓存文档和官方来源。这样提供“如何调用”的事实，但不替智能体提供任务流程。

## 6. 可迁移性

- 包版本从 `0.2.0` 更新为 `0.3.0`。
- `runtime.py` 统一解析主 profiles、support environments 和 auxiliary environments。
- 精确 Conda/pip 环境锁及 `.software_cache`、`.model_cache` 管理方式保持不变。
- portable lock manifest 新增以下配置 SHA-256：
  - `config/native_software_guides.yaml`
  - `mcp/tool_config.json`
- 修改后的 `auxiliary_environments.yaml` SHA-256 同步到 lock manifest。
- bootstrap 会拒绝三层执行配置与锁记录不一致的 checkout，防止软件迁移后静默沿用不同的调用契约。

## 7. 验证结果

| 验证 | 结果 |
|---|---|
| `pytest -q chemistry_toolbox/tests` | `181 passed in 493.81s` |
| 新开放层聚焦测试 + MCP 注册 + portable bootstrap 测试 | `17 passed` |
| `verify_toolbox.py --no-write` | 5 个结构检查全部 pass；Action handler 无 missing/extra |
| `tool_manager validate` | 101 Actions、76 Backends、13 开放工具、56 软件指南通过 |
| `check_mcp_tools.py --smoke` | 三层 MCP 注册、4 个 Action、软件指南、Agent 程序、异步作业、Artifact 和 trace 全部通过 |
| 真实原生手工 smoke | Open Babel `obabel -V` 通过；作业状态 success |
| 真实程序手工 smoke | `core` runtime 脚本生成 JSON，查询、收集和哈希通过 |
| walltime 测试 | 睡眠程序被 supervisor 标记为 timeout |
| JSON/YAML/compile/diff 检查 | 全部通过 |

完整测试包含原有 Action/Backend、资源、runtime、MCP 和 bootstrap 测试，因此三层扩展没有改变旧 Action 的执行结果。

## 8. 当前尚未解决的外部条件

| 项目 | 当前状态 | 需要的处理 |
|---|---|---|
| MATLAB R2018a | 安装介质已缓存，但没有合法安装和许可证 | 提供合法 MathWorks File Installation Key 和 license file/server 后安装；随后重新探测 `matlab` |
| EasySpin | Toolbox 文件存在，调用契约完成 | 依赖上面的 MATLAB；MATLAB 可用后运行一个真实 EasySpin 谱模拟 smoke |
| 通用 MPI 启动 | `mpirun` 指南存在但 `enabled=false` | 不应开放任意进程启动器；多节点/rank 应由部署调度器或未来的受控 MPI 字段实现，只能启动已选白名单程序 |
| PDF/压缩手册全文搜索 | 文件会列出，但当前只搜索缓存文本/HTML | 如 benchmark 需要段落级 PDF 检索，可增加独立、只读的 PDF 文本索引，不影响执行层 |
| 可编程层安全 | 有资源和 workspace 约定，但不是完整 OS 沙箱 | 正式运行不可信代码时，把 MCP 放入无特权容器/调度作业并限制网络和挂载 |
| GUI 软件 | VESTA 依赖显示/Xvfb；VMD 推荐 text mode | 开放科研任务优先使用批处理/Tcl 输出；交互 GUI 不宜作为自动 benchmark 的关键步骤 |

Q-Chem、Molpro、TURBOMOLE、CRYSTAL、WIEN2k、OpenEye 仍遵守此前用户决定，不通过 MCP 暴露。Schrödinger 下载项经检查不是商业化学套件，仍保留为 rejected asset，不暴露。

## 9. 主要新增或修改文件

| 文件 | 作用 |
|---|---|
| `config/native_software_guides.yaml` | 56 个软件、69 个命令的版本化调用契约 |
| `mcp/execution_models.py` | 开放层强类型请求和路径/标识校验 |
| `mcp/software_catalog.py` | 软件清单、别名归并、指南、文档搜索和 runtime 发现 |
| `mcp/open_execution.py` | 文件工具、原生/程序提交、查询、取消、收集和 Artifact |
| `mcp/job_supervisor.py` | 独立持久作业监督、资源上限、进程组和状态持久化 |
| `mcp/open_tools.py` | 13 个 FastMCP 工具绑定和结构化错误返回 |
| `mcp/registry.py`、`mcp/server.py` | 三层注册、资源和系统提示词 |
| `src/researchchem_toolbox/runtime.py` | 主/辅助 runtime 的统一发现和 executable 解析 |
| `tests/test_open_execution_layers.py` | 指南、路径、真实脚本、原生 argv、Artifact 和超时测试 |
| `scripts/check_mcp_tools.py` | 三层端到端 MCP smoke |
| `scripts/verify_toolbox.py` | 三层结构统计和指南校验 |
| `docs/CHEMISTRY_TOOLBOX_THREE_LAYER_ARCHITECTURE.md` | 面向使用、部署和 benchmark 评分的详细架构说明 |

## 10. 后续扩充原则

遇到新论文中的科学步骤时，先判断已有 Action 是否精确表达；否则使用已登记软件的原生能力或编写程序。只有当一个操作跨任务反复出现、输入输出语义稳定、需要统一验证或跨 backend 对比时，才提升为新 Action。

因此后续无需为每篇论文预先实现一套 Actions。工具箱的开放能力来自软件原生接口、固定版本程序库和智能体可审计代码；Action catalog 只承担高价值的通用抽象。
