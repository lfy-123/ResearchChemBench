# 使用 ResearchChemBench 评测 ARCHE

共享存储上的新服务器接入见 [系统依赖安装说明](install_arche_dependencies.md)：使用 `scripts/install_arche_dependencies.sh` 只安装服务器系统工具并复用共享环境。

入口：`scripts/run_arche_eval.sh`。全部可调整参数集中在脚本顶部，按任务/模型、科学流程、资源/预算、目录/解释器和部署分组；同名 `ARCHE_EVAL_*` 环境变量可以覆盖默认值。

**2026-10-07 修复：** 明确的加密历史拒绝现在可通过模型网关进行一次兼容恢复，保留工具历史并如实计数；公共工具箱修复扫描坐标错配及子模块导入误报。无需新增参数。实现、测试和旧运行限制见 [三项缺陷修复总结](../docs/handle/ARCHE三项缺陷修复验证_20261007/修改与测试总结.md)。

**2026-10-06 部署更新：** 每次新评估独占 QEMU、SSH、BGE 和代理，部署文件保存在该任务结果目录的 `.runtime/deployment/`。不同任务可以在多个终端或服务器并行启动；同机仅部署启动阶段短暂排队，评估阶段不共用项目锁。端口默认自动分配。任务结束后自动关闭自己的服务，文件保留以供诊断与恢复。管理某次运行使用 `--run-dir DIR`，恢复仍使用 `--resume DIR`。

**2026-10-05 更新：** 明确的纯供应商限流不再占 `MAX_CALLS`；本地预算耗尽准确停止。新运行将各项假设放入独立目录，最终由原生模型选择主要依据，并一次提交完整报告。新增 `--resume` 跨进程恢复；只支持带新检查点的运行，2026-10-04 的旧失败记录不能直接续跑。实现、验证与本任务复测命令见 [修复总结](../docs/handle/ARCHE限流计数假设隔离与Resume实施总结_20261005.md)。

当前节点已具备 Python 环境、BGE-M3、QEMU、解包内核和私有凭据文件。脚本会为新任务启动独立部署，执行原生预检，再调用 ResearchChemBench 官方 evaluator 和 judge。原生批次上限修复涉及两个源文件，原始哈希及修改后哈希均记录在 `benchmark_adapter/source_snapshot.json`；启动时仍校验全部 2,685 个文件。

默认流程：**读取一个公开评估任务 → 检索公开输入 → 生成 3 个研究查询、每个查询 3 个候选（初始共 9 个）→ 原生关系比较、合并和排序 → 选择 Top 5 → 五项调查 → 原生 Finalization（读取证据、汇总结论）→ 规范最终答案 → benchmark 正式评分。默认只生成一批，不根据否定结果生成第二批。**

显式传入 `--smoke` 可做简化验证：生成 5 个候选，保留 Top 5 筛选，每次原生确认只执行排名第一项调查，本批调查完成后进入原生 Finalization，终态提交后才正式评分；单计算上限 20 分钟、总计 1 小时、400 次模型请求。该模式附带有限计算指导语并记录 `evaluation_profile=smoke`，不是完整五调查评估。参数细节、当前验证状态与 GPT-5.6 命令见 [GPT-5.6 运行说明](run_arche_gpt56_eval.md)。

**2026-10-03 单批收束修复：** 标准生成流程现在按冻结的 `max_hypothesis_batches` 和已完成的 `HypothesisBatchRecord` 判断是否终局。默认上限为 1，全部已确认调查完成后直接使用原有 Finalization 合同；保留 `refuted` 等真实结果。证据足够时给出结论，不足时输出 `unanswerable` 及限制说明，两种终态都通过规范 `FinalAnswerRecord` 导出、提交，再交给 benchmark 评分。批次数达到上限后不再启动普通 Review 的返修或重新生成循环。证据缺失、模型格式错误、预算耗尽仍可能导致失败。

本次验证包含原生控制器回归和真实 MCP 作业→证据读取→规范导出→评分服务的集成夹具；模型和 judge 使用固定响应，不是新的付费化学任务评估，也没有产生新的正式科学成绩。测试结果与范围见 [单批终局修复记录](../docs/benchmark/ARCHE单批终局修复与验证_20261003.md)。

当前按单批运行：多批流程还存在原生账本对历史 Result heads 的校验冲突，已单独记录，不能由本次单批验证推断其可用。此前回执顺序及 provider 恢复接入已经修复；真实四分子试跑及后续 PBNA 停止记录仍见 [历史测试说明](../docs/benchmark/ARCHE单项接口验证与原生问题说明_20261003.md)，这些旧 run 没有正式分数。

benchmark 默认关闭论文联网搜索。用户显式设置 `ARCHE_EVAL_PAPER_SEARCH=true` 或传入 `--paper-search`，即可让 ARCHE 搜索、下载并使用通过来源过滤的论文，覆盖任务文本的禁网默认；不再要求任务声明允许联网。来源论文、SI、隐藏评估材料仍禁止使用，过滤不可关闭。本次运行会记录用户覆盖设置，原始任务文件不改写。

本入口当前面向 `autonomous_research` 任务；接入和测试通过不代表所有任务均已完成实测。每个任务的科学目标、可用输入、联网限制和提交格式由该任务自身规定。

新运行默认使用 benchmark 执行协议：独立作业可并发或批量提交，wait 自动收集结果，模型无需先 get 再 collect。无结果的 MCP 等待心跳在 adapter 内处理；新运行只将 `mcp__chemistry_wait` 的等待工具设为直接调用，避免外层 code mode 通过 `functions.wait` 周期唤醒模型；普通 `minichem_toolbox` 工具可以合并调用。启动命令和预算参数沿用原设置。2026-10-02 的 GPT-5.6 首测暴露了后一层问题，试跑主动取消，修复与验证记录见 [GPT-5.6 运行说明](run_arche_gpt56_eval.md)。

## 直接使用

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench

# 查看参数说明；不启动任何服务。
bash scripts/run_arche_eval.sh --help

# 配置预检；不启动服务、不调用模型、不要求密钥。
bash scripts/run_arche_eval.sh --dry-run

# 创建独立部署，检查原生沙箱、源文件、BGE、MCP 和代理，完成后关闭；不调用模型。
bash scripts/run_arche_eval.sh --check

# 正式评估：单批原生假设生成、Top 5、五项调查、Finalization、最终答案、正式 judge。
# 会使用配置中的模型 API；不同任务可并行，同一次运行不能重复恢复。
bash scripts/run_arche_eval.sh
```

脚本默认评估 `paper_72f60526b64ce1b6`，所有生成角色和 judge 都使用 `deepseek-v4.1-flash`。启动前可查看运行：

```bash
bash scripts/run_arche_eval.sh --status
```

如果需要关闭终端后继续运行：

```bash
mkdir -p workspaces/arche_eval
nohup bash scripts/run_arche_eval.sh > workspaces/arche_eval/console.log 2>&1 < /dev/null &
tail -f workspaces/arche_eval/console.log
```

## 选择评估任务

任务位于：

```text
tasks/final_verified_autonomous_research/<paper_id>/agent_input/
```

`paper_id` 是任务目录名，例如 `paper_72f60526b64ce1b6`，不是论文标题、DOI 或完整目录路径。可只列出任务 ID：

```bash
python - <<'PY'
from pathlib import Path
for task in sorted(Path('tasks/final_verified_autonomous_research').glob('*/agent_input/task.md')):
    print(task.parent.parent.name)
PY
```

开始前阅读所选任务的公开 `agent_input/task.md` 及其中引用的输入和提交说明。被测 ARCHE 默认只接收 benchmark 发布的公开输入；显式开启搜索后还可使用通过来源过滤的论文。不要把 `task_info.json`、来源论文、SI 或隐藏评分材料手动加入它的工作区。

```bash
# 一项任务：先检查配置，再正式启动。
bash scripts/run_arche_eval.sh --dry-run --paper paper_72f60526b64ce1b6
bash scripts/run_arche_eval.sh --paper paper_72f60526b64ce1b6

# 多项任务：逗号分隔，按配置顺序评估；不会同时启动多个 run。
# 示例中的两个 ID 均存在，但尚未逐一完成真实评估验证。
bash scripts/run_arche_eval.sh --paper paper_72f60526b64ce1b6,paper_08c040bf4e456891

# 同一任务独立重复两次，每次产生新的 run 和结果。
ARCHE_EVAL_REPEATS=2 bash scripts/run_arche_eval.sh --paper paper_72f60526b64ce1b6
```

`ARCHE_EVAL_TASKS_ROOT` 默认是项目的 `tasks/`，不是 `tasks/final_verified_autonomous_research/`。更换任务库时保持相同子目录结构，并通过该变量指定新的 `tasks` 根目录。当前脚本固定 `task_type: autonomous_research`、`max_concurrent_runs: 1`；它不提供切换到论文复现任务的命令行参数。

## 候选假设、Top N 与调查并发

| 完整环境变量 | 默认值 | 对应原生参数 | 作用 |
| --- | --- | --- | --- |
| `ARCHE_EVAL_NUM_QUERIES` | `3` | `num_queries` | 每批形成多少个研究查询／研究角度；这里不是模型调用次数 |
| `ARCHE_EVAL_HYPOTHESES_PER_QUERY` | `3` | `num_hypotheses_per_query` | 每个查询生成多少个初始候选假设 |
| `ARCHE_EVAL_TOP_N` | `5` | `top_n_hypotheses` | 最终入选调查数，整数 1–5；2026-10-05 起 benchmark 标准 research_task 入口支持可配置数量 |
| `ARCHE_EVAL_PARALLEL_INVESTIGATIONS` | `5` | `max_parallel_investigations` | 最多同时执行多少项调查；不改变入选总数 |
| `ARCHE_EVAL_GENERATION_WORKERS` | `3` | `hypothesis_generation_workers` | 候选生成的并行 worker 数；不增加候选总数 |
| `ARCHE_EVAL_COMPARISON_WORKERS` | `3` | `hypothesis_comparison_workers` | 关系比较／排序阶段的并行 worker 数 |
| `ARCHE_EVAL_HYPOTHESIS_BATCHES` | `1` | `max_hypothesis_batches` | 标准生成批次数上限；默认一批，全部已确认调查完成后进入 Finalization；当前使用 1，多批限制见上方 |

**初始候选数 = `NUM_QUERIES × HYPOTHESES_PER_QUERY`。** 默认 `3 × 3 = 9`；原生流程会比较候选关系并可能合并，因此进入最终排序的候选数不一定仍为 9。最后从剩余候选中选出 5 个，适配器原样确认执行，不人工重写或补造假设。

当前约束和区别：

- `TOP_N` 可设为 `1` 到 `5`，默认仍为 `5`。生成入口、选择、确认和账本按冻结数量衔接，不增加额外开关。
- 初始候选乘积必须 >=`TOP_N`，合并后的实际候选也必须足够；不足时仍报错，不补造候选。此前 `1 × 5`、Top 5 出现过合并后不足的情况。
- 调查并发 `1` 表示顺序执行全部 Top N；并发参数接受 1–5，实际不超过入选数。每项调查内部可提交多个计算作业。

所有现有环境变量的含义、范围、单位、默认值与优先级已直接写在 [run_arche_eval.sh](run_arche_eval.sh)。GPT 入口只保留原有覆盖项，此次没有新增运行参数。历史 `top5_selection` 专用入口仍固定五项，本次扩展面向 benchmark 当前标准 research_task 链路。
- 五项调查并发不等于五个计算作业都能同时占满资源。科学作业共享总 CPU／内存配额，例如总共 8 核、每个作业申请 4 核时，最多同时满足两个这样的作业。
- 候选更多会增加关系比较、排序和模型调用的开销；修改后先运行 `--dry-run`，并重新评估运行预算。

保留默认研究规模，降低调查并发的示例：

```bash
ARCHE_EVAL_NUM_QUERIES=3 \
ARCHE_EVAL_HYPOTHESES_PER_QUERY=3 \
ARCHE_EVAL_TOP_N=5 \
ARCHE_EVAL_PARALLEL_INVESTIGATIONS=1 \
bash scripts/run_arche_eval.sh --dry-run --paper paper_72f60526b64ce1b6
```

确认输出配置后，用相同变量重新执行并去掉 `--dry-run` 才会启动评估。上述改变只影响新运行，不会修改已经运行中的配置。

## 如何设置参数

可以编辑 `.sh` 顶部的默认值，也可以在命令前设置同名环境变量。命令行 `--paper`、`--model`、`--deployment`、`--paper-search` / `--no-paper-search`、`--no-score` 会覆盖对应环境变量；其他参数使用环境变量设置。不要直接编辑已经启动的 run 的 YAML 或预算账本来改变其行为。

工具返回默认使用 `ARCHE_EVAL_TOOL_RESPONSE_PROFILE=compact_v1`，与 benchmark 的
新运行默认设置一致。它启用结果分页、带哈希的精准读取及公共返回预算；原始计算
文件和 Review 证据完整保留。adapter 使用同一套公共实现，并在追加回执引用后
生成角色页面。无需修改现有运行命令。兼容对照可显式设为 `legacy`；此参数只应用于
新运行，不修改历史运行的冻结协议，也不改变假设数量、计算方法或模型上下文窗口。

以下为一组完整的常用参数配置；先预检，正式启动时保留变量并去掉 `--dry-run`：

```bash
ARCHE_EVAL_NUM_QUERIES=3 \
ARCHE_EVAL_HYPOTHESES_PER_QUERY=3 \
ARCHE_EVAL_TOP_N=5 \
ARCHE_EVAL_PARALLEL_INVESTIGATIONS=5 \
ARCHE_EVAL_HYPOTHESIS_BATCHES=1 \
ARCHE_EVAL_GENERATION_WORKERS=3 \
ARCHE_EVAL_COMPARISON_WORKERS=3 \
ARCHE_EVAL_PAPER_SEARCH=false \
ARCHE_EVAL_CPU_CORES=8 \
ARCHE_EVAL_MEMORY_MB=32768 \
ARCHE_EVAL_MAX_CALLS=2000 \
ARCHE_EVAL_MAX_TOKENS=null \
ARCHE_EVAL_TIMEOUT=43200 \
ARCHE_EVAL_COMPUTE_TIMEOUT=1800 \
ARCHE_EVAL_REPEATS=1 \
bash scripts/run_arche_eval.sh --dry-run \
  --paper paper_72f60526b64ce1b6 --model deepseek-v4.1-flash
```

## 凭据

默认读取已存在的 `custom_agents/Arche-Harness/benchmark_adapter/deepseek_flash.local.env`。该文件必须属于当前用户，且组和其他用户没有访问权限（通常为 `0600`）。文件内使用 `ARCHE_CHEM_API_KEY`，或通过环境变量提供 `ARCHE_EVAL_API_KEY`。不要把密钥写进脚本、YAML 或提交到 Git。

指定另一个私有文件：

```bash
ARCHE_EVAL_ENV_FILE=/absolute/path/to/private.env bash scripts/run_arche_eval.sh
```

私有文件只用于凭据；任务和运行参数在脚本顶部或命令环境中配置。`--status`、`--dry-run`、`--cancel`、`--down` 不读取私有 env 文件。`--check` 验证凭据变量是否配置，不调用远端模型，也不验证余额。

### 更换 API Key、URL 和模型

本入口使用以下变量，不需要修改原生 ARCHE 配置：

| 设置 | 变量 | 示例／说明 |
| --- | --- | --- |
| API Key | `ARCHE_EVAL_API_KEY` | 未设置时回退到私有文件中的 `ARCHE_CHEM_API_KEY` |
| API 根地址 | `ARCHE_EVAL_BASE_URL` | 例如 `https://your-provider.example/v1`；按服务商给出的根地址填写 |
| 模型名 | `ARCHE_EVAL_MODEL` 或 `--model` | 使用该服务商实际支持的模型 ID |
| 评分模型 | `ARCHE_EVAL_JUDGE_MODEL` 或 `--judge-model` | 新任务可独立指定；留空时跟随 Agent 模型 |

启动器 `child_environment()` 会将模型设置传给 chemistry、hypothesis、investigation 和 review；judge 默认跟随，也可以通过 `--judge-model gpt-5.6-sol` 单独指定。API、凭据和推理强度仍共用。评分模型写入运行配置和参数快照，旧任务 resume 使用原配置。通过本脚本启动时，单独设置 `ARCHE_CODEX_BASE_URL` 等底层角色变量会被入口的统一设置覆盖。

使用用户配置的 `gpt-test2` / `gpt-5.6-sol` 网关，可直接使用 [run_arche_gpt56_eval.sh](run_arche_gpt56_eval.sh)，参数和六项任务命令见 [GPT-5.6 运行说明](run_arche_gpt56_eval.md)。该入口支持 `RCB_CODEX_*` 环境变量和独立私有凭据文件。`ARCHE_EVAL_REASONING` 现在通过适配层统一发送给 Chat Completions 与 Responses，各角色的实际覆盖值记录在 `model_transport_policy.json` 和模型调用事件中；judge 同步使用该设置。

URL 应填写 API 根地址（例如该服务要求的 `/v1`），不要追加 `/responses` 或 `/chat/completions`；网关会自行追加请求路径。启动器支持用户指定的 HTTP 或 HTTPS 地址，与底层模型网关保持一致；不接受 URL 内嵌凭据、查询串或 fragment。原生 ARCHE 的部分角色使用 Chat Completions，调查和 Review 的 Codex runtime 使用 Responses，因此新服务必须支持这两种接口及对应模型的工具调用。`ARCHE_EVAL_JUDGE_WIRE_API=chat_completions` 只切换 judge 的协议，不会将整个 ARCHE 转换成 Chat Completions 客户端。

下面使用交互输入新 key，不将 key 字面值写进命令历史。`ARCHE_EVAL_ENV_FILE=/dev/null` 会跳过旧凭据文件（脚本只 source 普通文件），确保本次使用新输入的 key：

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench

read -r -s -p '新的 API Key: ' ARCHE_EVAL_API_KEY
printf '\n'
export ARCHE_EVAL_API_KEY

ARCHE_EVAL_ENV_FILE=/dev/null \
ARCHE_EVAL_BASE_URL='https://your-provider.example/v1' \
ARCHE_EVAL_PAPER_SEARCH=true \
ARCHE_EVAL_WAIT_HEARTBEAT=600 \
ARCHE_EVAL_PARALLEL_INVESTIGATIONS=2 \
bash scripts/run_arche_eval.sh \
  --paper paper_2f0a4f80a37fbccd \
  --model deepseek-v4.1-flash
```

将示例 URL 和模型名换成实际服务的设置；上述命令会启动正式评估。只检查配置时追加 `--dry-run`，它不验证新 API 的连通性、协议支持或余额。保留原 key、只更换 URL 时，可以省略交互输入与 `/dev/null` 设置，继续读取现有私有文件。

也可以编辑私有文件中的 `ARCHE_CHEM_API_KEY`，或用 `ARCHE_EVAL_ENV_FILE=/absolute/path/to/private.env` 指定另一个权限为 `0600` 的凭据文件。私有文件只放 key：它在脚本解析命令行之后被 source，如果里面另外赋值了 `ARCHE_EVAL_BASE_URL`、`ARCHE_EVAL_MODEL` 等变量，会覆盖此前的环境／命令行设置。

## 模型、资源和预算参数

| 参数 | 默认值 | 含义 |
| --- | --- | --- |
| `ARCHE_EVAL_PAPERS` | `paper_72f60526b64ce1b6` | `final_verified_autonomous_research` 下的任务；逗号分隔多个任务，顺序执行 |
| `ARCHE_EVAL_TASKS_ROOT` | `<项目>/tasks` | 包含 `final_verified_autonomous_research/` 的任务库根目录 |
| `ARCHE_EVAL_MODEL` | `deepseek-v4.1-flash` | 所有生成角色及正式 judge |
| `ARCHE_EVAL_BASE_URL` | `https://apicz.boyuerichdata.com/v1` | 模型 API 端点 |
| `ARCHE_EVAL_MAX_CALLS` | `2000` | 每个 run 的 ARCHE 应计模型调用上限，对应 `max_turns`；明确的纯供应商限流不占额度，工具作业数另计 |
| `ARCHE_EVAL_MAX_TOKENS` | `null` | ARCHE 已观察 token 的准入阈值；默认不设置 token／费用上限 |
| `ARCHE_EVAL_TIMEOUT` | `43200` | 每个独立 run 的任务执行总期限，秒；默认 12 小时 |
| `ARCHE_EVAL_CPU_CORES` | `8` | 宿主科学计算 CPU 配额 |
| `ARCHE_EVAL_MEMORY_MB` | `32768` | 宿主科学计算内存配额 |
| `ARCHE_EVAL_GPU_COUNT` | `0` | 科学计算 GPU 配额 |
| `ARCHE_EVAL_COMPUTE_TIMEOUT` | `1800` | 单个计算动作超时，秒 |
| `ARCHE_EVAL_REPEATS` | `1` | 每个任务重复次数 |
| `ARCHE_EVAL_JUDGE_ENABLED` | `true` | 完成后执行正式评分；`--no-score` 可明确关闭 |
| `ARCHE_EVAL_MIN_FREE_GIB` | `100` | 正式启动前的最低剩余空间，GiB |
| `ARCHE_EVAL_STATE_DIR` | `workspaces/arche_eval/.runtime` | 预检/旧部署兼容目录；新任务自动改用该次结果目录/.runtime |
| `ARCHE_EVAL_OUTPUT_ROOT` | `workspaces/arche_eval` | 每项任务的外层目录根；任务结果放入各自 runs/ 下 |

所有生成角色和 judge 使用相同的模型名及 API 端点；BGE-M3 仅做语义嵌入。`MAX_CALLS` 是 ARCHE 各阶段共享的模型准入额度，judge 使用独立的 benchmark 原生评分预算：最多 6 个请求，每个最多 8,192 输出 tokens。

从本版开始，HTTP 429 的明确限流拒绝，以及 HTTP 200 SSE 内嵌的 `response.failed/rate_limit_exceeded`，在没有模型输出时释放预留额度。已有部分文本、推理、工具调用或正的输出 token 用量仍计数；超时、未知断流、余额不足、认证错误及模型格式错误也不豁免。此规则不消除供应商限流，也不保证 400 次足够完成科学任务。

`outputs/arche/model_budget.json` 保存 `admitted_calls`（真实准入尝试数）、`counted_calls`（应计次数）、`rate_limited_calls`（已豁免次数）、`inflight_calls`、已知 tokens、未知用量次数及逐请求记录。真实尝试数可以超过上限，应比较 `counted_calls + inflight_calls` 与 `limits.max_turns`。限流有 usage 时仍计入已知 token；缺失字段保留未知。额度耗尽会留下 `budget_stop.json` 和 `adapter_outcome.json`，不会再误入供应商恢复循环。

`MAX_TOKENS` 不是服务商硬计费上限：已在途请求可能超过阈值，缺失用量也不会被当作零。设为正整数时适配器按已观察用量限制后续准入，出现未知用量会停止后续准入；设为 `null` 时继续累计已知用量并单列未知调用，主要受请求数和执行期限限制。

| 其他运行参数 | 默认值 | 含义 |
| --- | --- | --- |
| `ARCHE_EVAL_REASONING` | `high` | 生成／Review 配置及 judge 使用的推理强度 |
| `ARCHE_EVAL_HYPOTHESIS_PROVIDER` | `agent_a1` | 原生候选生成路由，支持 `agent_a1` 或 `codex`；不改变统一模型名 |
| `ARCHE_EVAL_MODEL_TIMEOUT` | `1800` | 单个模型请求的读等待秒数，仍受任务期限约束 |
| `ARCHE_EVAL_HTTP2` | `true` | 模型传输启用 HTTP/2 |
| `ARCHE_EVAL_JSON_OBJECT` | `true` | 显式请求 Responses JSON-object 输出；仍需原生 schema 校验 |
| `ARCHE_EVAL_TRANSPORT_RESUMES` | `3` | 原生流程在存活进程内允许的有界传输恢复配置，取值 0–6 |
| `ARCHE_EVAL_CONTRACT_REANSWERS` | `1` | 已完成但格式无效的回复最多一次原生格式重答；支持 0 或 1 |
| `ARCHE_EVAL_JUDGE_WIRE_API` | `responses` | judge API 协议，另支持 `chat_completions` |
| `ARCHE_EVAL_JUDGE_TIMEOUT` | `300` | judge 请求超时，秒 |
| `ARCHE_EVAL_FAST_TIMEOUT` | `60` | 快速工具动作超时，秒 |
| `ARCHE_EVAL_MCP_TIMEOUT` | `1860` | MCP 调用超时，秒；默认长于单作业限额 |
| `ARCHE_EVAL_WAIT_HEARTBEAT` | `120` | benchmark 内部等待心跳间隔，秒；适配器合并无结果心跳，不按此周期唤醒模型 |
| `ARCHE_EVAL_EVENT_SETTLE` | `1` | 作业事件稳定等待，秒 |
| `ARCHE_EVAL_EVENT_BATCH` | `5` | 作业事件批处理最大等待，秒 |

调整超时时应保持 MCP 和模型等待设置与任务总期限相容。所有默认值以 `.sh` 顶部为准。

覆盖示例（只在没有活跃运行时启动）：

```bash
ARCHE_EVAL_MAX_CALLS=2000 \
ARCHE_EVAL_TIMEOUT=43200 \
ARCHE_EVAL_CPU_CORES=8 \
ARCHE_EVAL_MEMORY_MB=32768 \
bash scripts/run_arche_eval.sh --paper paper_72f60526b64ce1b6 --model deepseek-v4.1-flash
```

12 小时是运行期限，不是完成保证。科学工具故障、API 等待、模型输出或预算耗尽都可能导致没有正式得分；缺失分数不能解释为零分。

## 检索方式与来源论文排除

### 联网开关：默认关闭，显式开启覆盖任务禁网默认

两种等价的关闭方式：

```bash
bash scripts/run_arche_eval.sh --no-paper-search
ARCHE_EVAL_PAPER_SEARCH=false bash scripts/run_arche_eval.sh
```

`deploy/launch_evaluation.py` 默认生成：

```yaml
agent_definitions:
  arche:
    options:
      paper_search:
        enabled: false
```

关闭联网时，原生 Retrieval 阶段仍然存在：适配器对本次 benchmark 发布的公开输入做分块，使用 BGE-M3 嵌入并通过 FAISS 进行语义检索；“3 个研究查询”不意味着发起 3 次联网搜索。此开关控制的是外部论文搜索，不会关闭模型 API、BGE 或 MCP 服务通信。

| 环境变量 | 默认值 | 作用 |
| --- | --- | --- |
| `ARCHE_EVAL_PAPER_SEARCH` | `false` | 是否启用带来源排除的原生论文搜索；仅接受 `true` / `false` |
| `ARCHE_EVAL_PAPER_SEARCH_TARGET` | `50` | 全局去重后通过过滤的 PDF 目标数量，沿用原生正式检索默认值；不是假设数量 |
| `ARCHE_EVAL_PAPER_SEARCH_TIMEOUT` | `600` | 单关键词搜索时间上限，秒；仍受任务总期限约束，并非整轮搜索总时长；resume 沿用保存值 |

`--paper-search` 等价于设置 `ARCHE_EVAL_PAPER_SEARCH=true`，`--no-paper-search` 等价于 `false`。命令行开关覆盖对应环境变量；重复提供时最后一个生效。

**`true` 就是用户对本次联网检索的显式授权。** 启动器和适配器均不再用任务中的 `Do not use general web` 等文字否决它，也无需另设强制开关。默认或 `false` 仍然关闭搜索。来源排除清单、任务覆盖、参数类型等检查仍须通过。

先进行不联网、不调用模型的配置预检：

```bash
bash scripts/run_arche_eval.sh --dry-run --paper-search \
  --paper paper_2f0a4f80a37fbccd
```

正式运行示例：这是《计算化学Rebuttal优先评测案例.md》中 P0 的 Ir nitrate complex，任务 ID `paper_2f0a4f80a37fbccd`。

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench

ARCHE_EVAL_PAPER_SEARCH=true \
ARCHE_EVAL_PAPER_SEARCH_TARGET=50 \
ARCHE_EVAL_PAPER_SEARCH_TIMEOUT=600 \
ARCHE_EVAL_NUM_QUERIES=3 \
ARCHE_EVAL_HYPOTHESES_PER_QUERY=3 \
ARCHE_EVAL_TOP_N=5 \
ARCHE_EVAL_PARALLEL_INVESTIGATIONS=5 \
ARCHE_EVAL_MAX_CALLS=2000 \
ARCHE_EVAL_TIMEOUT=43200 \
ARCHE_EVAL_COMPUTE_TIMEOUT=14400 \
ARCHE_EVAL_MCP_TIMEOUT=14460 \
bash scripts/run_arche_eval.sh \
  --paper paper_2f0a4f80a37fbccd --model deepseek-v4.1-flash
```

这会执行原生检索、初始 9 候选、Top 5、五项调查、Finalization、提交及正式评分。上例总执行期限 12 小时、单计算动作限额 4 小时；时间与调用预算不保证科学任务一定成功。已有活跃 ARCHE 评估时，重复启动保护仍然生效。

适配器向本次运行的研究任务、检索阶段、调查和 Review 指令附加用户授权说明，明确允许使用经来源过滤的文献，避免模型被原任务的禁网文字阻挡。原 `task.md` 和公开输入不改写；科学目标、提交格式和评分器沿用原配置。`test_settings.json`、`outputs/arche/retrieval_permission.json` 和联网时的 `search_policy.json` 记录 `permission_source: explicit_user_setting`、`overrides_task_search_restrictions: true`。分析结果时可以据此区分联网与默认离线运行。

### 保留的原生搜索流程

启用时仍调用 ARCHE 原生 `RetrievalAgent.extract_keywords()` 和 `search_papers()`；正式路由固定为 `pypaperbot_scholar`，使用 Scholar 候选、原生 Crossref 元数据补充和公开 PDF 下载。检索代码沿用该原生实现；本次两个原生文件的批次终局修复不涉及搜索引擎或来源过滤。

其余搜索参数通过原生 `normalize_paper_search_config()` 补齐，保持原生默认：每关键词最多 3 页、每页 10 个结果、每页最多 3 个 Crossref 补充候选；关键词间隔 45 秒加至多 45 秒随机等待，Scholar 请求间隔 15 秒加至多 15 秒随机等待，首次等待 10 秒加至多 20 秒随机等待，下载间隔 1 秒；限流基础退避 900 秒、最大 3,600 秒、连续限流 1 次即停机。验证码和限流继续按原生规则处理。

`target_papers` 是目标值；过滤、公开 PDF 可用性或限流可能导致实际不足。`search_policy.json` 记录目标、实际接受数、`target_reached` 和有效原生参数，不能将不足的数量报告为已达到目标。任务级搜索不允许自行指定缓存／manifest 路径，避免绕过隔离；低层独立诊断脚本保留原有兼容 provider，但一键正式流程不自动切换 provider。

### 来源论文过滤与排除策略

过滤由 `rcb_adapter/source_filter.py`、`guarded_retrieval.py` 实现。联网启动时，脚本自动从所选 `TASKS_ROOT` 的 `final_verified_*/*/task_info.json.paper` 书目字段生成私有策略，覆盖该任务库全部 final 来源论文，并校验覆盖本次每个任务；不读取评分答案。策略保存在本次 launch 的 `source_exclusions.private.json`，权限 `0600`，以 `RCB_ARCHE_SOURCE_EXCLUSIONS` 传给适配器。不会复用环境中可能已过期的排除文件，也不会把排除书目放入模型提示词。

检查位置：候选元数据 → 下载前信息 → 隔离下载后的 PDF 正文／元数据 → 复制入语料前 → 建立索引前。匹配 DOI、URL／编码变体、出版商 DOI 后缀／SI 路径、标题及近似标题。没有足够可提取文本的 PDF 会被拒绝；原生 HTTP 不跟随重定向。来源标识明确的候选在下载前拦截，伪装元数据的 PDF 若内容命中来源则在隔离目录中丢弃。搜索缓存和恢复记录同样留在临时隔离目录，只有通过检查的 PDF 才进入任务语料。

缺失、不可匹配或未覆盖当前任务的排除策略会报错，不会降级到未过滤搜索。参数快照记录策略哈希与来源数量；`outputs/arche/source_exclusion_audit.json` 只记录阶段、哈希、允许／拒绝及原因。已有语料目录不能未经复核直接复用。

低层 `make_config.py --paper-search` 同样视为用户显式授权，不再受任务禁网文字阻挡，但仍要求手动提供私有策略。需要独立生成策略时：

```bash
.envs/arche-benchmark/bin/python \
  custom_agents/Arche-Harness/benchmark_adapter/rcb_adapter/source_filter.py \
  --tasks-root tasks --output workspaces/arche_source_exclusions.json
export RCB_ARCHE_SOURCE_EXCLUSIONS="$PWD/workspaces/arche_source_exclusions.json"
```

该文件已存在时拒绝覆盖；生成文件本身不会联网，是否搜索由显式开关控制。一键入口会自行生成当次策略，无需执行上述命令。更多独立诊断用法见 [适配器 README](../custom_agents/Arche-Harness/benchmark_adapter/README.md#来源论文自动排除)。

过滤会保守地连带拒绝引用来源 DOI／标题的其他论文；它不能保证识别所有改写或未标注镜像，也不能消除模型预训练记忆。联网功能和来源过滤已有本地确定性测试；本次修改没有启动新的付费评估。

### 2026-10-01 下载与来源过滤实测

2026-10-01 10:30:49–10:32:40 UTC，在独立目录 `workspaces/arche_download_validation_20261001/` 完成真实联网测试。调用正式适配层 `prepare_safe_corpus()`，使用 `paper_2f0a4f80a37fbccd` 的公开任务文本和覆盖 89 篇来源论文的私有策略；`paper_search.enabled=true`、PDF 目标 1、单关键词超时 180 秒，其余 Scholar 参数保持原生默认。本次以显式诊断关键词 `molecular dipole moment density functional theory` 跳过模型生成关键词，使用现有本地 BGE-M3 服务排序；没有启动完整评估或调用付费模型。

- **真实下载成功**：Scholar 返回 HTTP 200，获得 10 个候选；Crossref 请求正常。ACS 与 ChemRxiv 的两个 PDF 请求返回 403，原生流程随后从 Scholar 候选已有的 arXiv 链接下载成功，没有切换检索 provider。
- **接受 1 篇有效 PDF**：38 页、376,380 字节、11,385 个可提取词，通过候选、下载前、PDF 内容及入语料前检查；`search_policy.json` 为 `status: completed`、`accepted_pdfs: 1`、`target_reached: true`，记录显式用户授权覆盖任务禁网默认。SHA-256 为 `1a542fa694ea07edaea9b29d44d72198206bfd6032228c2e4ccfeb3cba585cde`。
- **真实检索与拦截测试分开取证**：此次在线返回的候选未命中排除清单，在线审计 `blocked_checks: 0`。另外用真实来源清单做确定性测试：89 篇来源论文的 DOI 和标题共 178 项匹配均拒绝；当前任务的 DOI、标题、大小写／双重编码 URL、DOI 后缀 SI 链接和换行 DOI 均在下载前拒绝，下载 HTTP 调用数为 0。
- **隔离路径通过**：使用模拟 HTTP 响应运行原生 Scholar 解析及下载链路，来源候选不下载，元数据伪装但 PDF 正文含当前来源 DOI 的文件在隔离区拒绝，只有无关对照 PDF 进入语料。PDF 元数据含来源标题、空白／不可提取文本 PDF 和损坏 PDF 同样拒绝。该组为确定性夹具测试，不能计为额外的真实联网下载。
- **测试结果**：14 组真实策略过滤检查通过；`test_source_filter.py` 的 24 项回归测试通过。公开任务文件未改变，正式评估未启动，原生 ARCHE 源码未改动。本次验证下载及过滤，不代表默认目标 50 篇已达成，也不代表完整评估已完成。

证据：[真实联网结果](../workspaces/arche_download_validation_20261001/live_result.json)、[HTTP 状态](../workspaces/arche_download_validation_20261001/live_http.json)、[运行权限与数量](../workspaces/arche_download_validation_20261001/live/search_policy.json)、[在线过滤审计](../workspaces/arche_download_validation_20261001/live/source_exclusion_audit.json)、[确定性过滤结果](../workspaces/arche_download_validation_20261001/filter_result.json)、[回归日志](../workspaces/arche_download_validation_20261001/filter_pytest.log)。证据保存在本地 workspace；不要将私有排除清单、测试夹具或本目录整体作为 Agent 输入。

### 既有真实运行的检索证据

本轮 `paper_72f60526b64ce1b6` 的公开任务明确禁止使用来源论文、SI、general web 和隐藏评估材料。已核对本轮的真实记录：

- `outputs/arche/search_policy.json`：`{"enabled": false, "reason": "public_inputs_only"}`。
- `outputs/arche/retrieval_sources.json`：`source_kind` 为 `benchmark_public_inputs`，语料仅包含 `task.md`、`data/inputs/AD_isolated.xyz`、`data/inputs/system.json`，共 3 个文本块。
- 本轮没有联网搜索，因此没有生成 `source_exclusion_audit.json`，这是关闭联网后的正常行为，不能解释为进行过未过滤的外部搜索。

**该既有离线运行的结论：没有将来源论文下载或纳入检索语料；它通过不进行外部检索遵守任务限制，而不是联网搜索后过滤掉来源论文。** 这与上面的独立联网测试是两次不同运行。

## 部署与控制

默认 `--deployment managed`：每次新评估创建独立 QEMU 部署。新任务的 `auto` 同样使用独立部署，不借用其他任务的服务；`existing` 仅用于恢复旧任务的冻结配置。每个任务的 SSH 密钥、配置、guest 控制文件、PID、端口、BGE 令牌和服务日志都保存在自己的 `.runtime/deployment/`，结束后关闭服务、保留文件。

QEMU guest 运行原生协调器和沙箱，MCP 科学计算与 BGE 在宿主执行，默认 guest 为 4 vCPU、8 GiB 内存。四个部署端口默认 `0`，由启动器自动分配并保存，恢复时复用。也可显式指定 `1024..65535` 的空闲端口；同机并行推荐保留自动分配。当前实现使用容器 root 账户，不需要修改宿主内核。

同机只在启动部署期间持有 `/run` 下的短期锁，避免服务尚未监听时其他启动器选中同一端口；服务就绪后立即释放，不覆盖科学评估过程。不同服务器的启动锁互不影响。Unix socket 有长度限制，仍放在本机 `/run/arche-eval-<本任务路径摘要>/`；位置记录在本任务的 `deployment.json.local_runtime`。共享存储上的认证文件无法被本机 sshd 正常读取，因此同一临时目录还保存该任务专属的认证副本；原件、持久配置和日志均在任务结果目录内。

不同终端分别执行单任务命令即可并行，无需手工设置部署目录或端口；单条命令传多个论文 ID 仍按顺序执行。化学作业继续使用 benchmark 的资源管理；同机多任务应合理分配各自 `CPU_CORES`、`MEMORY_MB`，并给 guest 和 BGE 留出资源。

依赖路径可在脚本中修改：三个 Python 环境、BGE 模型目录、QEMU/virtiofsd、已解包的 Linux 内核及模块、共享根目录。脚本不会安装宿主内核，也不会自动下载缺失的模型或 Python 环境。项目、解释器和状态目录须在 guest 可访问的共享路径内；默认参数已经在当前节点验证。

```bash
# 查看运行列表；指定目录时只看该任务。
bash scripts/run_arche_eval.sh --status
bash scripts/run_arche_eval.sh --status --run-dir /完整路径/paper_ID_时间_标识

# 经官方 benchmark 接口取消指定任务；部署预检阶段则通知该任务的启动器退出。
bash scripts/run_arche_eval.sh --cancel --run-dir /完整路径/paper_ID_时间_标识

# 手工关闭指定任务的闲置部署；存在活跃使用者时拒绝关闭。
bash scripts/run_arche_eval.sh --down --run-dir /完整路径/paper_ID_时间_标识
```

`--check` 的新部署检查完成后自动关闭；`--up` 检查后保留部署。`--up --run-dir DIR` 可重启该任务原部署，不执行科学评估。控制命令从任务快照加载原路径和端口，不依赖当前 shell 的部署参数。新任务的停止、重启和 resume 必须在记录的原主机执行；在其他服务器可以查看状态，不会将远端 PID 误判为已经退出。旧任务保留原部署配置，不自动迁移到新布局。

### 恢复本版创建的运行

本版生成的 ARCHE 配置声明 `resume_protocol: arche-checkpoint-v1`。把 `--resume` 指向外层 `paper_<ID>_<时间>_<标识>` 目录：

旧共享部署的恢复也按本任务加锁，启动器状态放在该结果目录 `.runtime/`，冻结的 SSH/模型端点路径保持不变。旧快照未保存主机名时，从 benchmark 执行账本核对原主机；必须在该主机执行。启动器会健康检查本任务保存的部署端点，不使用已被其他服务器覆盖的共享 PID 文件重建或关闭服务。端点不可用时明确停止，避免借用另一台虚拟机。检查点通过只表示可以尝试恢复，不代表已回滚的未完成模型 turn 能逐条无损续接；计算文件和作业账本保留，无效扫描仍需 agent 重新判断和计算。

```bash
# 只检查检查点、作业证据及剩余额度，不启动部署、不调用模型。
bash scripts/run_arche_gpt56_eval.sh --resume /absolute/path/to/new_paper_run \
  --extra-calls 200 --resume-timeout 21600 --check

# 继续同一个 run；历史次数不清零，成功提交后仍按原设置评分。
bash scripts/run_arche_gpt56_eval.sh --resume /absolute/path/to/new_paper_run \
  --extra-calls 200 --resume-timeout 21600
```

`--extra-calls 200` 将原累计上限增加 200（例如 400 → 600），不是额外重置一个 200 次的新 run；未用尽时可以省略。`--resume-timeout 21600` 从本次续跑开始给出 6 小时的新期限；未过期时可以沿用旧期限。相应环境变量是 `ARCHE_EVAL_RESUME_DIR`、`ARCHE_EVAL_EXTRA_CALLS`、`ARCHE_EVAL_RESUME_TIMEOUT`。`--check` 不提交这些修改，结果为 `resume_needs_budget` 时需明确补充时间或额度。

续跑恢复原任务、假设、native session、作业回执、未读结果页和累计预算；完成作业继续复用，失败/取消作业不会被代码自动重置或重新提交。原任务请求及工具配置保持冻结，模型/API、检索和部署配置从该任务快照加载，凭据仍由私有 env 文件或进程环境提供。保留外层目录及 `runs/cli_runs/batch_*/.rcb_recovery/`；本地端口被占用时需先解决冲突。延长期限要求原计算已处于终态且管理器已退出。

#### 原主机停止后迁移到新主机

如果原实例已经停止，可以在新主机使用 `--migrate-from-host 原完整主机名`。这表示操作者已经确认旧实例停止；程序不会把“本机找不到旧 PID”当作远端已停止的证明。只支持独立 managed 部署、未完成但已终止的 run，且所有作业都必须为终态；未知或仍在运行的作业不会被自动重置。

```bash
# 在新服务器执行，--check 只检查，不改绑、不启动模型或部署。
bash scripts/run_small_molecules_gpt61_eval.sh arche --resume 原结果目录 \
  --migrate-from-host 原完整主机名 --check

# 检查通过后继续同一任务。
bash scripts/run_small_molecules_gpt61_eval.sh arche --resume 原结果目录 \
  --migrate-from-host 原完整主机名
```

小分子 GPT-6.1 入口将这些参数转交给原 ARCHE 恢复入口。普通同主机 resume 命令不变，Codex 入口不接受 ARCHE 的迁移参数。

迁移先检查原 checkpoint，再取得共享存储上的 launcher、controller、coordinator、manager 锁，核对执行账本终态及目标机的原端口可用性。正式执行时备份原部署与提交配置到 `launch/host_migrations/`，只更新任务部署的所属主机；不改历史 PID、作业状态、模型调用预算、原生线程或科学结果。部署服务在新主机使用原冻结端口重建；端口冲突会明确停止，不悄悄改端口。默认按主机隔离的计算资源池在运行时改用当前主机，自定义资源池和已保存配置保留。

同一目标主机重复使用同一个迁移参数不会重复改绑。若原实例仍可能运行、缺少检查点、作业状态不明、共享锁被占用，必须先解决相应问题，不要直接改 `test_settings.json` 的 host 绕过检查。

续跑审计在 `launch/resumes/`、实际 run 的 `_agent_protocol/resume_attempts/` 和 `outputs/arche/resume_attempts/`。已完成的运行拒绝再次 resume。缺少新账本或冻结端点检查点的旧 run 会明确拒绝，不会默默重新生成假设、重算旧调用或修改旧记录。`paper_2f2aa11ea61a32bb_20261004_133807_16bcd4` 属于此类，当前应新建复测。存活进程内的有限传输恢复和格式重答仍受原边界约束。

调查阶段的 provider failure 最多自动恢复一次：原生有限重试后，adapter 复用 benchmark 的等待策略（默认约 60–66 秒；有有效 `Retry-After` 时至少等到指定时间）。若等待超出剩余任务时间或 benchmark 等待预算则直接停止；恢复后再次失败也停止并保留检查点。明确的请求格式、上下文超限、认证或余额错误直接停止，不等待重试。JSON 与 SSE 错误均保存安全的分类、状态码及有限正文的哈希，不保存供应商回显的请求正文。这与假设生成阶段的 `ARCHE_EVAL_TRANSPORT_RESUMES` 相互独立。

重复启动保护覆盖整个 evaluator 生命周期：即使 Agent 已完成，只要正式 judge 或证据收尾的 evaluator 仍存活，也会拒绝第二次启动。`--status` 中的 `evaluator_active` 可用于区分执行终态与评估器退出。

## 输出与成功判定

每篇论文的每次正式评估创建一个独立目录；逗号分隔多个任务时逐项建目录并顺序执行。`ARCHE_EVAL_REPEATS` 的每次重复也单独保存，不会覆盖旧结果。

```text
workspaces/arche_eval/                 # GPT-5.6 入口改为 arche_gpt56/
├── paper_<ID>_<UTC时间>_<标识>/
│   ├── submission.json               # 提交身份、运行路径、退出状态
│   ├── test_settings.json            # 实际参数、模型、资源和部署信息（无密钥）
│   ├── evaluation_config.yaml        # 本次 evaluator 配置
│   ├── task_snapshot/autonomous_research/<paper_id>/
│   ├── launch/
│   │   ├── source_exclusions.private.json  # 仅联网时存在，过滤组件专用
│   │   ├── preflight.log              # 正式执行或 --check 的部署检查
│   │   ├── deployment_preflight.json
│   │   ├── evaluator.log
│   │   ├── evaluator_identity.json
│   │   └── result.json
│   └── runs/cli_runs/batch_<...>/
│       ├── results.json
│       ├── eval_report.json
│       ├── eval_report.md
│       ├── .rcb_recovery/
│       └── <run_id>/
│           ├── _meta.json
│           ├── _score.json            # 成功完成评分后才生成
│           ├── report/
│           └── outputs/
│               ├── arche/           # 原生记录、预算、最终发布记录和恢复审计
│               ├── execution_jobs/  # 原始计算产物，不搬动或重复复制
│               └── hypotheses/
│                   ├── index.json
│                   ├── selection.json  # Finalization 模型的选择及理由
│                   └── batch_<摘要>/hypothesis_<序号>_<摘要>/
│                       ├── manifest.json
│                       ├── investigation_result.json  # 最近一次通过证据引用验证的原生结果
│                       ├── results/                  # 按内容摘要保存历史原生结果
│                       ├── evidence_index.json
│                       ├── code/
│                       ├── outputs/
│                       └── report/                   # 本假设的模型草稿，以实际文件为准
└── .runtime/
    ├── preflight/                    # --dry-run、--check、--up 的独立检查目录
    ├── deployment/                   # 自建部署（借用时不另建完整部署）
    ├── launch.lock
    └── active_run.json
```

正式启动会先复制本次任务包并保存版本哈希。evaluator 子进程通过 `RESEARCHCHEMBENCH_TASKS_DIR` / `RESEARCHCHEMBENCH_TASK_ROOTS` 读取本次 `task_snapshot`，通过 `RESEARCHCHEMBENCH_WORKSPACES_DIR` 写入本次 `runs/`；采用与 Codex pilot 相同的 canonical 任务快照结构。Agent 仍只接收公开输入，私有评分文件及来源排除策略不进入其任务材料。

终态写入本任务的 `submission.json` 和 `launch/result.json`；预检失败也留在所属目录中。预检过程不混入正式任务列表。`--status` 和 `--cancel` 自动发现新旧布局，旧路径与迁移后的路径按实际位置去重；重复启动保护仍覆盖整个 evaluator 生命周期。

`report/results.json` 等提交文件以任务的公开 schema 为准；所有候选、排名、Top 5、调查和最终答案仍保存在 run 的 `outputs/arche/`。完整成功需同时具备原生调查结果、Finalization、规范最终答案、合法导出和实际 judge 的 `_score.json`；预检成功与固定模型夹具不能当作真实科研任务已完成评分。

新运行使用 `hypothesis_output_layout: isolated_v2`。Investigation 在自己的目录中直接准备完整 benchmark 报告与附件；adapter 校验、封存并自动登记证据。Finalization 只返回当前候选的 ID 与理由，adapter 原样复制所选文件并写 selection.json，不重写数值、正文或坐标。合法 partial/bounded_failure 报告也可选择，科学失败状态不改变；没有可交付候选时明确失败。旧任务恢复沿用冻结的 v1/legacy，未选中的调查和全部过程成本继续保留。附件可用本调查 outputs/submission_files.json 的“最终路径→已收集 artifact ID”映射，运行参数不变。

新任务的冻结包必须包含全部必需文件；旧 v1 任务仍要求最终 `files` 映射显式包含这些文件。两种模式均不把另一假设的旧 Markdown 补进新 JSON。整组文件先校验并暂存，再发布并记录 hash；`outputs/arche/final_submission.json` 只有 `state: committed` 才表示本组文件完成发布。它不是评分成功标记。化学计算失败仍通过 benchmark 原协议交给 agent，由它决定修改参数、另选计算路线或如实报告失败。

2026-10-03 保留的最新 GPT-5.6 测试已迁入 `workspaces/arche_gpt56/paper_2f2aa11ea61a32bb_20261003_142511_ce7774/`。旧 `cli_runs/batch_...` 和 `workspaces/arche_gpt56_eval` 只作为兼容路径保留，不重复存储计算产物。原始失败记录与文件内容保留；旧测试产物已按用户要求清理，历史报告中的原始附件链接可能失效。

## 大型计算结果归档

ORCA 等计算可能留下数百 GiB 的二进制中间文件。默认归档会复制这些文件，需要额外磁盘空间。确认 evaluator、guest Agent、计算作业和执行管理器全部退出后，可在同一文件系统上显式选择：

```bash
.envs/researchchembench/bin/python -m evaluation.provenance.evidence_archive export \
  /absolute/path/to/completed_run \
  --output /absolute/path/to/new_archive --compress-logs --link-large-files
```

该选项仅对执行作业目录下至少 1 MiB 的二进制文件共享磁盘存储，记录 SHA-256；日志和 SQLite 仍独立复制，秘密信息照常过滤。活动运行或作业会被拒绝；跨文件系统链接失败时也会报错，不会悄悄改为占用大量空间的复制。归档后源文件与归档中的硬链接必须保持只读使用；删除其中一处路径不会删除另一处内容，但原地改写任一处会影响另一处。需要编辑时先制作独立副本。

## 当前实测进展快照

以下是 **2026-10-01 13:03 UTC（北京时间 21:03）** 的一次性只读检查。此前完整试跑已结束，状态为 `failed`，没有正式分数；不要将下载／过滤测试成功等同于完整科学评估成功。

| 项目 | 实测状态 |
| --- | --- |
| 任务 | `autonomous_research/paper_72f60526b64ce1b6`：22 原子孤立中性单重态分子的零场偶极矩及验证 |
| 运行开始 | 2026-10-01 02:26:51 UTC |
| 原生候选流程 | 初始 9 候选、36 项关系比较、1 次合并、28 项排序比较及 Top 5 确认已完成 |
| 终止记录 | `results.json` 于 2026-10-01 12:16:52 UTC 写出；`status: failed`、`exit_code: 1`，运行约 9 小时 49 分钟 |
| 调查 | 停在调查阶段，应用记录 `provider_failed`／`TemporarilyUnavailable`；没有完成全流程汇总 |
| 作业 | 199 个登记作业，199 个已收集，0 个活跃；166 success、4 partial_success、13 failed、9 timeout、3 cancelled、4 invalid_request |
| 模型用量 | 2,000 / 2,000 次准入上限，0 次在途；239,132,470 输入 tokens、1,883,959 输出 tokens，另有 1 次用量未知 |
| Review／最终答案 | Review 为 `not_started`；无规范最终答案。存在中间 `report/results.json`，不能当成正式提交或评分成功 |
| 正式评分 | `score.available: false`、`scoring.evaluation_status: not_started`；无本任务 `_score.json` |

运行目录：

```text
workspaces/cli_runs/batch_20261001_022651_8c29c1/
  autonomous_research-paper_72f60526b64ce1b6-arche-20261001_022651-a30383/
```

本轮由此前的 `qemu/launch_eval.sh` 启动；新的 `scripts/run_arche_eval.sh --status` 能识别它。当前 evaluator 已退出，不再因这次旧运行阻止启动新任务。该旧运行未开启论文联网搜索。退出日志为 `ARCHE suspended without an active benchmark job: provider_failed`。

2026-10-02 进一步核对原始调查会话：最后未完成的调查于 2026-10-01 12:14:40.949 UTC 报 `exceeded retry limit, last status: 429 Too Many Requests`。共享账本恰好用满 2,000 次，适配器 `RunBudget.begin()` 在此上限之后拒绝新请求，模型网关将其返回为 HTTP 429。结合这条代码路径和终止记录，失败指向本地共享请求预算耗尽，随后被原生流程归类为 `provider_failed`；脱敏 trace 未保留最后 429 的原始响应正文。当前没有为 Review 单独保留请求额度，耗尽预算也不会自动生成最终答案。

用量交叉核对：已知输入 239,132,470 tokens、输出 1,883,959 tokens，合计 **241,016,429 tokens**，另有一次用量未知。2,000 次请求中，调查路由占 1,927 次；有用量记录的请求平均输入约 119,626 tokens。五项调查的原生会话累计用量与网关调查账本完全一致，其中输入缓存命中 208,532,736 / 237,461,203 tokens（约 87.8%，已包含在输入总数中）。累计输入包括反复携带的历史和工具结果，不能把全部 tokens 按未缓存价格当作实际账单。诊断证据见 [failure_analysis_20261002.json](../workspaces/arche_eval/failure_analysis_20261002.json)。

同日进一步审计调用用途：**552 次模型请求只等待，200 次只查询作业／队列／资源状态**。其中 343 次是在同一作业返回心跳、没有新完成作业之后再次只等待，占 2,000 次额度的 17.15%，累计输入 51,179,463 tokens；这是可减少的模型唤醒开销。模型共调用等待工具 567 次，其中 371 次返回心跳。另有 26 次缺少终态 get 就 collect、16 次旧作业未收集就提交新作业、4 次缺少 submission_key 的拒绝。状态确认与结果收集有必要步骤，不能将以上所有操作都计为浪费；工具调用次数与模型请求次数也不相等。详见 [调用审计报告](../workspaces/arche_eval/call_audit_20261002/report.md)。

### 重复调用的原因及与原生 Codex 的区别

2026-10-02 对同一任务 `paper_72f60526b64ce1b6` 的两次历史运行进行只读对照：

| 项目 | 2026-09-21 原生 Codex | 2026-10-01 ARCHE |
| --- | --- | --- |
| `model_wait_strategy` | `host_event_wait` | `provider_default` |
| 实际等待行为 | 专用 `chemistry_wait` 等待作业事件，不因周期心跳返回模型 | 默认 heartbeat 模式，120 秒可能返回一次心跳 |
| 运行状态 | `completed` | `failed`，共享 2,000 次模型准入额度耗尽 |

Codex 证据位于 `workspaces/codex_gpt56/paper_72f60526b64ce1b6_20260921_220614_ef7ff9/runs/cli_runs/batch_20260921_220617_2e812b/autonomous_research-paper_72f60526b64ce1b6-codex-20260921_220617-6b871a/_meta.json`；ARCHE 证据为上方运行目录的 `_meta.json`、`recovery/run.json` 和 MCP 配置。两次运行的模型及科学流程不同，这个对照能确认等待配置差异，不能用来量化修复后的整体节省量。

旧版问题位于等待接入和协议衔接，代码证据如下（下面已记录本次修复）：

- **等待方式未对齐。** `evaluation/execution/runner.py` 和 `evaluation/agent_plugins/external.py` 当前限制 `host_event_wait` 只用于已验证的原生 Codex；ARCHE 作为 external agent 只能使用 `provider_default`。化学工具箱 `chemistry_toolbox/mcp/open_execution.py` 已支持事件等待。旧运行配置 120 秒心跳，旧接入层将这些响应交回模型，导致模型反复决定“继续等”。工具箱内部检查状态不调用模型，心跳返回后产生的新模型请求才消耗模型调用额度和输入 tokens。
- **两套作业说明存在冲突。** benchmark 通用 `INSTRUCTIONS.md` 告诉模型等待会自动收集，通常不必再 get/collect；ARCHE 原生 `investigation/codex_runtime.py::_capture_job_progress()` 却要求同一原生 turn 内先取得匹配作业的终态 get，再 collect。旧适配器 `rcb_adapter/application.py` 追加后一要求，`rcb_adapter/tools.py` 执行检查。因此模型可能按通用说明跳过步骤而收到拒绝。46 次前置条件错误包括这类问题；不能仅凭日志证明每一次都是提示冲突造成。
- **长历史放大每次低价值唤醒的成本。** 五项调查各自维持上下文，调查路由累计输入约 2.375 亿 tokens，其中约 87.8% 被报告为缓存输入。37 次相同 collect 和 71 次相同文件读取也存在重复，部分可能用于上下文恢复，不能全部删去或全按未缓存价格计费。

2026-10-02 已在 adapter 实施 benchmark 执行协议接入，新运行默认生效，不需要新增开关：

- 模型直接使用 `execute_action`、`submit_native_job`、`submit_analysis_program` 和 Action batch 工具，保留 benchmark 输入 schema、状态与诊断。同一调查可提交多个独立作业，计算配额和队列由 benchmark 管理。
- `wait_execution_jobs` / `wait_execution_events` 的无结果心跳由 adapter 内部继续等待，不产生新的模型请求。部分结果、错误、阻塞、资源警告和结果分页及时返回；取消和截止时间会打断等待。
- wait 自动收集；模型无需额外执行“先 get，再 collect”。需要诊断时 get，需要详细结果时 collect。后台只为 ARCHE Review 取得稳定证据回执及必要分页，核验路径、哈希和所属调查。
- ARCHE 原生恢复账本收到的是有明确来源的 benchmark 回执导入，实际并发执行仍由 benchmark 管理。模型提前结束一轮时保留未读结果，原生会话继续读取；不会因模型给出最终文字就假定任务完成。
- 运行中保持稳定的工具超时配置，同时执行实际任务截止时间；缺失恢复证据或不可安全恢复的暂停会退出，避免无进展循环。共享 `MAX_CALLS` / `MAX_TOKENS` 预算继续有效。

external agent 的 runner 配置仍使用 `provider_default`；adapter 内部合并心跳实现上述行为，不需要把 YAML 改成目前不受 external agent 支持的 `host_event_wait`。`ARCHE_EVAL_WAIT_HEARTBEAT` 现在只影响内部 MCP 心跳频率。审计记录位于 `outputs/arche/bridge/wait-*.json`（`requests`、`suppressed_heartbeats`、`duration_seconds`）；真实作业/批次及证据映射在 `identities.json`，原生导入来源在 `native-import-*.json`。

同日 GPT-5.6 的真实科研试跑又发现外层 code mode 的 `functions.wait` 会周期返回空结果，即使内部 MCP 心跳已被合并，仍会唤醒模型。当时 adapter 将整个 `mcp__minichem_toolbox` 设为直接调用。2026-10-05 已按 benchmark 的做法收窄为 `features.code_mode.direct_only_tool_namespaces=["mcp__chemistry_wait"]`；普通工具恢复合并调用，等待仍由宿主完成。新运行使用拆分策略，旧 checkpoint 恢复沿用原冻结策略。这个设置不改变 external runner 的 YAML 字段，也不修改 benchmark 的科学工具协议。真实试跑结果和长等待验证见 [GPT-5.6 专项说明](run_arche_gpt56_eval.md)；之前只覆盖 MCP 心跳的夹具测试不足以证明外层执行器不会空等待。

此前协议改造于 2026-10-02 完成首轮验证：适配器 **261 项单元测试通过**，真实 MCP **10 项集成测试通过**，原始 ARCHE **2,685 个文件哈希一致**。这些是外层 code mode 修复前的验证记录；该修复另通过 70 项相关回归测试和 65 秒真实原生等待验证，期间额外模型请求为 0，详见上方专项说明。首轮测试覆盖并发提交、批量事件与分页、失败诊断、取消、提交响应丢失后的查询恢复、格式重答和提前结束后的继续执行。完整流程夹具中，五项调查各提交两个作业，模型只提交并等待，随后原生 Review 读取真实产物并完成规范导出和归档；恢复时没有重复提交计算。并发回调更新作业记录与持久化共用锁，避免保存期间修改记录导致中断。

等待回归测试还验证了连续 12 次空心跳合并在一次模型可见 wait 中，模型调用数及 token 计量不增加。集成测试的模型响应是固定夹具，计算、MCP、Review 证据读取和归档是真实链路。本次未启动新的付费 DeepSeek 科研评估，尚未测量完整真实任务的 token 节省比例；不能把这些工程测试计为正式科学得分。

启动方式不变。例如此前的 DeepSeek 单任务配置仍可使用：

```bash
ARCHE_EVAL_PAPER_SEARCH=true \
ARCHE_EVAL_WAIT_HEARTBEAT=600 \
ARCHE_EVAL_PARALLEL_INVESTIGATIONS=2 \
bash scripts/run_arche_eval.sh \
  --paper paper_2f0a4f80a37fbccd \
  --model deepseek-v4.1-flash
```

该组合于 2026-10-02 06:31 UTC 通过 `--dry-run` 配置预检；仍是初始 9 候选、Top 5、2,000 次调用上限和正式 judge，只将五项调查的同时执行上限降为 2。600 秒现在是内部 MCP 心跳间隔；无新结果时由 adapter 合并，作业完成可提前返回。也可省略这一环境变量沿用默认 120 秒。该真实科学评估仍待实测，不能用配置预检或工程夹具宣称已经稳定取得评分。

同日 13:03 UTC，`ARCHE_EVAL_PAPER_SEARCH=true bash scripts/run_arche_eval.sh --dry-run --paper paper_2f0a4f80a37fbccd` 返回 `preflight_ready`，新建策略覆盖 89 篇来源论文。该命令只验证配置，没有启动新评估。当前脚本可用于发起新任务，但此前完整真实试跑尚未取得成功评分。

此前联网开关与来源过滤通过 225 项适配器回归测试和 4 项 benchmark 集成测试。其中原生 Scholar HTTP 边界夹具验证来源/SI 候选拦截、PDF 内容复核、干净 PDF 放行。后续按用户要求将权限语义修正为“默认关闭，显式 true 覆盖任务禁网默认”，原先“当前任务开启必报错”的行为已经取消；不会追溯改变以上旧运行的离线配置。

该权限修正通过 229 项适配器回归测试和 4 项 benchmark 集成测试；原始 2,685 个文件哈希一致。`paper_2f0a4f80a37fbccd` 和明确写有禁网条款的 `paper_221aafe4bd916a11` 均通过开启搜索的 `--dry-run`，自动生成覆盖 89 篇来源的私有策略；关闭搜索仍通过。预检不发起真实搜索或模型调用，不能据此声称某次真实检索已下载了 50 篇论文。

此前工程验证已记录 4 项 benchmark 集成测试、五调查→Review→规范导出的独立完整夹具、真实 judge 的独立评分协议测试通过；大型文件归档选项另通过 22 项归档测试。这些证明接口及相应工程链路可执行，不能替代本任务的真实科学分数。

需要 DeepSeek 旧运行状态时手动执行一次 `bash scripts/run_arche_eval.sh --status`；本次 GPT-5.6 首测使用独立目录，状态入口为 `bash scripts/run_arche_gpt56_eval.sh --status`。GPT-5.6 首测已主动取消，尚无正式科学分数，修复后的长等待诊断已通过；完整记录见 [GPT-5.6 专项说明](run_arche_gpt56_eval.md)。
