**使用 gpt-test2 的 GPT-5.6 评测 ARCHE**

**2026-10-08 交付更新：** 新任务默认使用内部 `isolated_v2`：每项 Investigation 完成 benchmark 报告，adapter 自动封存/登记，Finalization 只选一个候选，最终文件逐字节发布。运行命令和模型参数不变，旧任务 resume 保留原协议；全部调查的成本与失败照常记录。

共享存储上的新服务器接入见 [系统依赖安装说明](install_arche_dependencies.md)：使用 `scripts/install_arche_dependencies.sh` 只安装服务器系统工具并复用共享环境。

本入口运行 ARCHE：假设生成、调查和 Finalization 默认使用 `gpt-5.6-sol`，推理强度为 `high`。benchmark 正式评分默认使用相同模型，也可用 `--judge-model gpt-5.6-sol` 固定评分模型，同时用 `--model deepseek-v4-pro` 更换 Agent 模型。评分仍使用相同 API 和凭据，旧任务 resume 保留原评分配置。入口为 [run_arche_gpt56_eval.sh](run_arche_gpt56_eval.sh)，底层复用 [run_arche_eval.sh](run_arche_eval.sh)。

用户提供的凭据已保存到本机 `custom_agents/Arche-Harness/benchmark_adapter/gpt_test2.local.env`，权限 `0600`，Git 忽略。文档和运行命令不包含密钥。入口也接受环境变量 `RCB_CODEX_API_KEY`、`RCB_CODEX_BASE_URL`、`RCB_CODEX_MODEL`、`RCB_CODEX_REASONING_EFFORT`；显式 `ARCHE_EVAL_*` 设置优先。

**2026-10-05：重新测试四个硼配合物任务。** 已修复纯供应商限流占额度、本地预算耗尽后仍恢复、调查报告互相覆盖及最终导出沿用旧文件的问题，并为新运行增加跨进程 resume。化学工具失败原样交给 agent 决定后续计算；本轮没有加入扫描失败审查、自动换方法或自动重算。具体代码和验证见 [实施总结](../docs/handle/ARCHE限流计数假设隔离与Resume实施总结_20261005.md)。

**工具接口更新（2026-10-05）：** 新建运行自动使用与 benchmark 相同的普通工具/等待工具拆分方式，并同步后登记的 artifact 引用。运行命令和用户参数不变；历史压缩、工具摘要展示、等待聚合参数没有在本轮调整。旧会话恢复保留其原策略，使用下面命令新建任务才会启用新的拆分方式。

**参数补充更新：** 现有 `TOP_N` 支持 1–5，未新增运行参数，各项范围直接写在 sh 注释中。下面按最新要求生成初始 4 个候选、选择 Top 2、逐个调查，额度为 2000 次；仍开启联网并使用 `compact_v1`。保持标准模式，勿追加 `--smoke`。

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench

ARCHE_EVAL_PROFILE=standard \
ARCHE_EVAL_NUM_QUERIES=2 \
ARCHE_EVAL_HYPOTHESES_PER_QUERY=2 \
ARCHE_EVAL_TOP_N=2 \
ARCHE_EVAL_PARALLEL_INVESTIGATIONS=1 \
ARCHE_EVAL_HYPOTHESIS_BATCHES=1 \
ARCHE_EVAL_MAX_CALLS=2000 \
ARCHE_EVAL_MAX_TOKENS=null \
ARCHE_EVAL_TOOL_RESPONSE_PROFILE=compact_v1 \
ARCHE_EVAL_PAPER_SEARCH=true \
bash scripts/run_arche_gpt56_eval.sh --paper paper_2f2aa11ea61a32bb
```

入口默认使用 `gpt-5.6-sol/high`，读取已保存的私有凭据；默认单任务总时限 12 小时、单计算上限 4 小时、宿主配额 48 核/204800 MiB，联网目标 50 篇。来源论文及 SI 过滤保持启用。`2 × 2` 是初始候选数，原生合并可能使候选数减少；合并后不足 Top 2 仍报错，不人为补造候选。最终报告依据由模型选择，不是强制取排名第一项。

`MAX_CALLS` 限制应计调用数，本例为 `2000`，旧运行是 `400`；明确的纯限流不占其中额度；真实准入次数和全部已知 token 继续记录，缺失用量保持未知。已有部分输出后报限流、其他服务错误以及模型格式错误仍计数。此修改不解决供应商限流本身，额度也不保证任务必定完成。

结果仍在 `workspaces/arche_gpt56/paper_2f2aa11ea61a32bb_<UTC时间>_<标识>/`。实际 run 下的 `outputs/hypotheses/batch_*/hypothesis_*/` 分别保存各调查的说明、原生结果快照、草稿和证据索引；`selection.json` 保存最终模型选择，最终报告仍写入公开 schema 指定的 `report/`，再交给 judge。

新运行退出后，可使用下面的入口。示例增加累计额度 200 次，并明确给续跑 6 小时；两项均可先通过 `--check` 只读预检：

```bash
bash scripts/run_arche_gpt56_eval.sh --resume /absolute/path/to/new_paper_run \
  --extra-calls 200 --resume-timeout 21600 --check
bash scripts/run_arche_gpt56_eval.sh --resume /absolute/path/to/new_paper_run \
  --extra-calls 200 --resume-timeout 21600
```

这会继续原任务、会话、假设和作业回执，不清零消耗；本例 `2000 + 200 = 2200` 是追加后的累计上限。延长期限要求原计算和管理器已结束。保留任务目录及其中 `.rcb_recovery/`，并复用原部署设置。**10 月 4 日的旧 run 没有本版检查点，不能直接 resume；上面的新建命令用于本次复测。** 完整参数、目录和恢复限制见 [通用运行说明](run_arche_eval.md)。本轮只进行了自动化测试和 0 模型调用的部署预检，尚无新的正式化学任务成绩。

**单批流程（2026-10-03 修复）。** 默认 `max_hypothesis_batches=1` 现在生效：生成一批初始 9 个候选、选择 Top 5、分别调查后，进入原生 Finalization 汇总结论并导出提交。全部假设被否定时也能形成忠实报告；证据不足时保留 `unanswerable`。两种终态都可进入 benchmark 评分，最终分数仍由原评分器判断。这个修复修改了两个原生源文件，已更新源码校验及修改来源记录。

原生控制器回归及真实 MCP→规范提交→评分服务使用确定性夹具验证；未重启付费科学评估。详细结果见 [单批终局修复记录](../docs/benchmark/ARCHE单批终局修复与验证_20261003.md)。目前使用单批模式，多批流程另有历史 Result heads 校验冲突，尚未修复。

此前真实四分子测试完成首项调查（34 个成功作业）和普通 Review 后，因批次数上限未生效进入第二批，随后遇到模型服务错误和当时缺失的恢复交接而失败。回执及 provider 恢复接入现已修复；后续 PBNA 测试按用户要求停止。这些历史 run 没有规范最终答案或正式分数，见 [历史测试说明](../docs/benchmark/ARCHE单项接口验证与原生问题说明_20261003.md)。

| 参数 | 本入口默认值 |
| --- | --- |
| API 根地址 | `http://35.220.164.252:3888/v1`；用户提供裸地址时自动补 `/v1` |
| 模型／推理强度 | `gpt-5.6-sol` / `high`，包含假设生成、调查、Review 与 judge |
| 默认试跑任务 | `paper_3a22e838133b906d`，中性／阴离子的 P–O 和 O···B 结构变化 |
| 候选数／最终选择 | 初始 `3 × 3 = 9`，比较／合并后 Top 5；五项调查均执行 |
| 假设批次数 | `1`，完成本批调查后 Finalization，不生成第二批 |
| 调查并发 | `2`；不减少五项调查的总数 |
| 科学计算配额 | 整个任务共享 48 核、204800 MiB（200 GiB）、0 GPU；不是每个调查各占一份 |
| 单计算／总任务期限 | 4 h / 12 h |
| 模型调用预算 | 各 ARCHE 阶段共享最多 2000 次请求；无额外 token 上限；新 judge 评分无调用次数/累计用量配额，继续记账与分页读取 |
| 文献搜索 | 默认 `false`，为了缩短首测并保留离线基线条件 |
| 工具返回协议 | 默认 `compact_v1`：复用 benchmark 的分页、精准读取与返回预算；可用 `ARCHE_EVAL_TOOL_RESPONSE_PROFILE=legacy` 做兼容对照 |
| 输出 | `workspaces/arche_gpt56/paper_<ID>_<UTC时间>_<标识>/`，配置、任务快照、日志及结果集中保存 |

候选数不等于模型请求数。原生流程会先对候选两两判断关系，再对合并后的候选两两排序：9 个候选仅第一轮关系判断就有 `9 × 8 / 2 = 36` 对，排序还会增加请求，随后才是五项调查和 Finalization。这些属于 ARCHE 的科学决策流程，和计算等待期间的无事件轮询不同；本入口保留该流程，因此“简单任务”仍可能产生较多输入 token。这里的 token 统计是网关返回的用量，不能直接等同于费用或未缓存输入量。

2026-10-02：该网关的 `/v1/responses` 与 `/v1/chat/completions` 均已用指定模型、`high` 进行真实请求，返回 HTTP 200；Responses 的 JSON Schema 输出也通过。接口测试使用两个小请求，不能代替完整科学评估。脱敏记录见 [provider_probe/result.json](../workspaces/arche_gpt56_eval/provider_probe/result.json)。启动器现已支持用户提供的 HTTP 地址；适配器统一发送推理强度，避免原生假设生成阶段忽略该设置。

**结果目录（2026-10-03 更新）。** 每项任务及每次重复各建一个 `paper_<ID>_<UTC时间>_<标识>` 目录，根目录保存 `evaluation_config.yaml`、`test_settings.json`、`submission.json` 和 `task_snapshot/`；启动日志在 `launch/evaluator.log`，实际结果在 `runs/cli_runs/batch_*/<run_id>/`。后者包含任务要求的 `report/`、评分 `_score.json`、全部候选和调查记录 `outputs/arche/` 及计算作业 `outputs/execution_jobs/`。

`--dry-run`、`--check` 的输出位于 `workspaces/arche_gpt56/.runtime/preflight/`，每次正式运行的状态和独立部署位于其结果目录的 `.runtime/`，其中 `deployment/` 保存 guest、SSH/BGE 配置、PID 和日志。不同任务可并行启动，默认自动分配端口；任务结束后自动关闭自己的服务。管理指定任务使用 `--status/--cancel/--down --run-dir DIR`，恢复使用 `--resume DIR`。原有六条任务命令可继续使用。最新保留测试已迁入 `workspaces/arche_gpt56/paper_2f2aa11ea61a32bb_20261003_142511_ce7774/`；旧路径通过链接兼容，`--status` 只显示一次实际运行。较早的测试结果及诊断日志已按用户要求删除，下面历史记录中的附件链接可能失效。

**先跑一个简单任务。**

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench
bash scripts/run_arche_gpt56_eval.sh --paper paper_3a22e838133b906d
```

以上是完整流程。若只想先做简化的端到端验证，显式使用：

```bash
bash scripts/run_arche_gpt56_eval.sh --smoke --paper paper_3a22e838133b906d
```

`--smoke` 生成 `1 × 5 = 5` 个候选，保留原生 Top 5 筛选，在每次原生研究员确认接口仅执行排名第一的候选，其余四项使用 `cancel`。该参数同时设定调查并发 1、`max_hypothesis_batches=1`、单计算 1200 秒、MCP 1260 秒、总期限 3600 秒和 400 次模型请求。仍调用真实化学工具和原生 Finalization；只有原生任务闭合并导出合法提交后才进入 benchmark judge。公开任务及评分标准不变，不保证获得高分或在几分钟内结束。

`max_hypothesis_batches=1` 限制的是生成批数，不是候选数、计算作业数或模型调用次数。标准模式执行本批全部 Top N 调查（默认 Top 5）；`smoke` 只确认第一项。达到上限后直接终局成稿，不再通过普通 Review 请求返修或下一批假设；一项调查内部仍可能需要多个计算作业。证据必须齐全且提交必须合法，才会进入评分。

2026-10-03 的联网快速复测使用下面的参数。它保留简化调查范围，将单计算上限调为 30 分钟、总期限 2 小时、模型请求 600 次。自定义这些值时用 `ARCHE_EVAL_PROFILE=smoke`，不要再加 `--smoke`：命令行 `--smoke` 会将它们覆盖回上面的固定值。

```bash
ARCHE_EVAL_PROFILE=smoke \
ARCHE_EVAL_NUM_QUERIES=1 \
ARCHE_EVAL_HYPOTHESES_PER_QUERY=5 \
ARCHE_EVAL_PARALLEL_INVESTIGATIONS=1 \
ARCHE_EVAL_HYPOTHESIS_BATCHES=1 \
ARCHE_EVAL_PAPER_SEARCH=true \
ARCHE_EVAL_PAPER_SEARCH_TARGET=2 \
ARCHE_EVAL_MAX_CALLS=600 \
ARCHE_EVAL_COMPUTE_TIMEOUT=1800 \
ARCHE_EVAL_MCP_TIMEOUT=1860 \
ARCHE_EVAL_TIMEOUT=7200 \
bash scripts/run_arche_gpt56_eval.sh --paper paper_2f2aa11ea61a32bb --paper-search
```

简化模式还把明确的有限计算指导语写入研究问题、确认记录和运行提示：优先使用每个必要状态的一份公开起始结构，省略可选的大规模构象搜索和方法比较，保留必需的优化与最低点验证，诚实报告覆盖范围和未完成项。运行在 `outputs/arche/evaluation_profile.json` 中标为 `smoke`，不能作为完整 ARCHE 五调查流程的验证或与完整流程混合统计。省略 `--smoke` 时仍为完整默认流程；仅增加该参数不会启用联网。

2026-10-02 17:45 UTC：用户要求停止所有测试并改为自行运行。当前 evaluator 已退出、在途模型请求为 0，简化试跑**没有启动**。新增入口相关的生命周期、启动器及原生边界共 63 项测试通过，shell 语法检查通过；这些是接口回归检查，不能代替正式科学评估。

**第一次完整试跑未通过，没有科学成绩。** 2026-10-02 13:45:09 UTC 正式开始，14:42 左右发现持续空等待后主动取消，14:43:19 启动器结束。benchmark 状态为 `failed`；没有 `report/results.json` 或 `_score.json`，不能写成“0 分”或“已完成”。API、公开输入整理、9 候选／Top 5 和前两项调查的工具调用已跑通；五项调查尚未全部完成，也未到 Review 和 judge。

启动配置为 `workspaces/arche_gpt56_eval/launches/20261002T134232-a48391/`，运行目录为 `workspaces/arche_gpt56/cli_runs/batch_20261002_134457_b4bccc/autonomous_research-paper_3a22e838133b906d-arche-20261002_134457-bda25f/`。详细统计见 [first_test_audit.json](../workspaces/arche_gpt56_eval/first_test_audit.json)：

- 候选筛选结束前：80 次模型请求，1,927,587 tokens。
- 停止前累计：242 次已准入请求，已返回用量为输入 15,633,164、输出 218,553，合计 **15,851,717 tokens**。取消时还有 1 次请求在途，因此是已观察用量下限；不能据此计算账单。
- 两个调查共出现 **114 次原生 `functions.wait` 调用**。adapter 已吸收 MCP 空心跳，但外层 code mode 的执行单元仍周期返回“Script running”，促使模型继续等待。这是另一层工具调用接入问题，并非达到 2000 次预算，也不是 API 不可用。
- 共 23 个托管作业：4 个成功（构象生成／聚类）、6 个输入不合法、6 个 CREST 失败、7 个运行中的作业随取消终止。ORCA 已产生中间计算文件，但没有完成任务要求的双状态验证。不能把构象处理成功计为科学目标完成。

当时为解决该问题，adapter 把整个 `mcp__minichem_toolbox` 命名空间设为直接工具调用。2026-10-05 已修正该范围：新运行仅对独立的 `mcp__chemistry_wait` 使用直接调用，普通工具恢复 code-mode 合并调用；旧检查点保留原策略。设置在原生线程配置生成处接入，同时进入会话配置哈希和实际线程创建／恢复参数；其余原生权限校验照常执行。当时原始 ARCHE 的 2,685 个文件哈希一致；2026-10-03 的批次终局修复另有两处源文件修改记录。配置键依据[官方配置说明](https://learn.chatgpt.com/docs/config-file/config-reference)，并参照本 benchmark 的 Codex `host_event_wait` 实现；每次新运行记录 `outputs/arche/model_wait_policy.json`。

修复验证已通过：70 项协议、运行边界、生命周期与恢复测试通过；另外 68 项启动器／模型参数测试通过。真实原生运行使用同一个模型与 `high` 设置，调用诊断用的 `wait_execution_jobs`，连续等待 **65.02 秒，期间额外模型请求为 0**，最终正确读取工具随机回执并通过原生 JSON schema 校验，见 [direct_wait_probe_v2/result.json](../workspaces/arche_gpt56_eval/direct_wait_probe_v2/result.json)。这验证了外层重复等待的修复；诊断工具没有执行化学计算，不能作为科学任务完成证据。

**第二次完整试跑已按用户要求取消，没有正式分数。** 2026-10-02 16:05 UTC 开始，17:39 UTC 结束，运行目录为 `workspaces/arche_gpt56/cli_runs/batch_20261002_160520_540f16/autonomous_research-paper_3a22e838133b906d-arche-20261002_160520-a8f6f6/`。取消原因是用户选择改做简化快速验证，并非达到模型调用预算。取消前已完成候选筛选，前两项调查仍在计算；ARCHE 自行安排了 12 个中性与 12 个阴离子构象的 PBE0-D3BJ/def2-TZVP 优化，每作业 2 核。22 个仍运行的作业已取消；16 个成功作业是构象准备或分析，成功 DFT 优化为 0。另有 8 个失败作业（其中 3 个 ORCA 作业在 OpenMPI `vader` 通信中崩溃）和 11 个无效输入请求。没有 `report/results.json`、Review 或正式分数。该运行保留日志、配置和中间产物，不能算测试通过。

第二次试跑累计准入 209 次模型请求；从 16:55 到 17:21 UTC 保持不变，原生 `functions.wait` 调用为 **0**，而计算轨迹持续更新，说明真实长计算期间没有再出现外层空轮询。已观察输入 8,825,938、输出 204,687 tokens；19 次请求没有返回用量，以上不能当作完整账单。目前只确认接口及等待机制工作，不能承诺完整评估稳定成功。最新快照见 [second_test_progress.json](../workspaces/arche_gpt56_eval/second_test_progress.json)。

**后续六项由用户自行启动。** 选择来自原优先清单，兼顾 Codex 的低分、正式任务可用性和化学类型。分数是现有 Codex 历史分数，不是 ARCHE 成绩，完整依据见[分析文档](../docs/benchmark/ARCHE优先评测任务_Codex结果与适配分析_20261002.md)。

| 建议顺序 | 任务 ID | 原优先级 | Codex 分数 | 主要测试点 |
| --- | --- | --- | ---: | --- |
| 1 | `paper_2f2aa11ea61a32bb` | P0 | 79.12 | 四个硼配合物的激发态与轨道／NTO 证据 |
| 2 | `paper_0de37d01e35c27df` | 第二级 3 | 76.80 | 氧化前后 S–S 结构变化、构象和自旋 |
| 3 | `paper_60f4c45810428116` | P0 | 62.90 | 两个含硫前体的解离还原电位、热力学循环 |
| 4 | `paper_221aafe4bd916a11` | P0 | 54.00 | 氢负离子转移的多假设、TS、IRC 和定量势垒 |
| 5 | `paper_e2d9397dff2a3f0f` | P1 | 45.24 | Ru 配合物 N–O 断裂过渡态及势垒 |
| 6 | `paper_9a58a1fa6ed7d780` | P1 | 64.61 | BN-AkFlu 激发态和空穴／电子描述符 |

没有把旧分 76.50 的 4b 任务（fcc3）加入六项：其公开分子输入和二面角评分说明已有实质纠正，旧低分不适合作为优先挑选依据。0de3 的当前包也与历史评分包不同，但本次看到的公开变更主要是 partial/bounded_failure 报告分支；完整结果的 S–S 数值目标仍在。正式对照应冻结任务包版本和 judge，并补齐必要的新版本 Codex 基线。

前四项按顺序评估，使用默认 4 h 单计算、12 h 总期限：

```bash
bash scripts/run_arche_gpt56_eval.sh --paper \
paper_2f2aa11ea61a32bb,paper_0de37d01e35c27df,paper_60f4c45810428116,paper_221aafe4bd916a11
```

等待前一批结束后，再运行两项耗时测试。历史最长单作业约为 Ru 4.8 h、BN-AkFlu 11.6 h，因此显式设置 24 h 单计算、96 h 总任务期限。它们是每项任务的上限，不是预期运行时间：

```bash
ARCHE_EVAL_COMPUTE_TIMEOUT=86400 \
ARCHE_EVAL_MCP_TIMEOUT=86460 \
ARCHE_EVAL_TIMEOUT=345600 \
bash scripts/run_arche_gpt56_eval.sh --paper \
paper_e2d9397dff2a3f0f,paper_9a58a1fa6ed7d780
```

也可以每次只传表内一个 ID。上述两批共六个任务，脚本逐任务运行，不能同时启动两个批次。每项仍为 9 候选、Top 5、两项调查并发；2000 次请求限制不会因为增加计算期限而自动提高。五条调查可能重复部分科学计算，所以不能直接用一次 Codex 的耗时预测 ARCHE 的总成本。

要启用原生论文搜索与下载，在命令前设置 `ARCHE_EVAL_PAPER_SEARCH=true`。来源论文和 SI 的过滤继续强制生效；结果应标记为联网实验。首次快速试跑保持关闭。

可手动查看当前运行，或在新运行前仅检查参数：

```bash
bash scripts/run_arche_gpt56_eval.sh --status
bash scripts/run_arche_gpt56_eval.sh --dry-run --paper paper_2f2aa11ea61a32bb
```

六项命令已准备，本次助手仅执行一个简单任务，不启动这六项。
