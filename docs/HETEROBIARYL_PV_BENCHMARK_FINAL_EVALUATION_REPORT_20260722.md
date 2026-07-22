# Heterobiaryl P(V) Benchmark 最终构建与评估报告

日期：2026-07-22（UTC）

状态：六个任务均已构建并完成真实 Agent/Judge 评估；模型输入输出轨迹、子智能体轨迹、裁判历史和工具调用证据均已落盘。最终有效批次没有 API、进程、MCP 传输或评分解析失败。

## 1. 最终结论

本轮评估说明当前 ResearchChemBench 三层化学工具箱已经能够承载该论文型 benchmark：智能体可以自由选择预定义 Action、软件原生执行和自写 Python/Bash 分析，不需要为论文固定一个专用工作流。

`deepseek-v4-flash` 的表现呈现明显的任务难度分化：

- 对边界清晰、参考数值能从匿名记录中稳定重建的质子化势垒任务表现很好，Q1 得到 96/100。
- 对需要从匿名结构中同时完成路径赋值、构象/驻点选择和机理角色区分的任务表现明显较弱。
- 对完整端到端任务能够审计数据、编写脚本并形成可复现报告，但错误地选择了关键驻点和热化学口径，遗漏 P(V) 醇加成、stepwise/asynchronous apical-to-equatorial coupling 和 dearomatized intermediate，最终得到 53/100。
- 最终六项运行的 `objective_issue_flags` 均为空。低分来自模型的科学判断，而不是框架或接口失败。

## 2. 最终评分总览

Agent 与 Judge 均为 `bailian/deepseek-v4-flash`。

| 任务 | 最终分数 | Agent model steps / sessions | Scientific MCP 成功/总数 | Native 成功/总数 | 核心结果 |
|---|---:|---:|---:|---:|---|
| Q1 Protonation | 96/100 | 59 / 1 | 1/7 | 69/72 | 正确复现 P0/P1/P2 约 31.1/19.5/14.0 kcal mol⁻¹ |
| Q2 CC Selectivity | 22/100 | 90 / 3 | 0/0 | 109/122 | 路径/驻点赋值错误，错误判成热力学控制 |
| Q3 CC vs CO | 55/100 | 53 / 2 | 0/0 | 96/99 | 正确预测 C−C 主导，但 C−C 势垒算成 21.3 而非 14.3 |
| Q4 Coupling Mechanism | 36/100 | 21 / 1 | 4/10 | 36/36 | 错判 concerted，遗漏 dearomatized intermediate |
| Q5 Rate-Determining Step | 70/100 | 30 / 1 | 3/6 | 39/40 | 实验趋势正确，但把 ligand coupling 错判为整体决速步骤 |
| Q6 End-to-End | 53/100 | 36 / 1 | 0/0 | 61/63 | 数据审计和报告良好，但能量、机理和步骤角色存在系统性错误 |

五个子任务最终均分：55.8/100。

完整端到端任务：53/100。

有效批次：

- 五个子任务：`workspaces/cli_runs/batch_20260722_022026_75d612`
- 完整 E2E：`workspaces/cli_runs/batch_20260722_033901_2c5d7e`

## 3. Benchmark 参考结论

正式隐藏参考使用 353.15 K、1 M、乙醇环境、统一 mRRHO 热化学口径，并区分论文整数值与本项目复算值。

| 项目 | 参考答案 |
|---|---|
| 活性质子化态 | doubly protonated P2 |
| 优势路径 | pyridyl-pyridyl C−C coupling |
| 机理 | stepwise asynchronous apical-to-equatorial ligand coupling through a dearomatized intermediate |
| 整体决速步骤 | alcohol addition at phosphonium P before ligand coupling |
| 选择性决定步骤 | P(V) ligand-coupling transition state |
| P2 C−O 竞争路径 | 约 18 kcal mol⁻¹，比 P2 C−C 高约 4 kcal mol⁻¹ |

统一复算能量：

| 状态 | BiPy ΔG‡ | PhPy ΔG‡ | PhPy−BiPy ΔΔG‡ | BiPy ΔGreact | PhPy ΔGreact |
|---|---:|---:|---:|---:|---:|
| P0 | 30.91 | 37.32 | 6.41 | −32.38 | −32.54 |
| P1 | 19.81 | 26.86 | 7.05 | −30.53 | −28.51 |
| P2 | 14.30 | 25.57 | 11.27 | −31.35 | −31.85 |

论文发表式整数势垒为 BiPy 30/20/14、PhPy 37/27/25、P2 C−O 约 18 kcal mol⁻¹。

## 4. 逐任务详细分析

### 4.1 Q1：连续质子化对 BiPy 偶联势垒的影响

最终分数：96/100。

模型完成了较完整的匿名候选审计：

- 按 P0/P1/P2 分组；
- 用虚频区分 minima 与 TS；
- 用成键距离区分反应物侧和产物侧；
- 组合 DLPNO-CCSD(T)/CBS 电子能与统一的 DFT 热修正；
- 独立得到 P0/P1/P2 约 31.1/19.5/14.0 kcal mol⁻¹。

这与参考 30.91/19.81/14.30 高度一致。主要扣分来自使用普通 RRHO 而非参考 mRRHO，以及机理解释没有明确突出 migrating apical P−C bond 的极化/弱化。

工具情况：

- 59 个模型 step；1 个 session；79 个 OpenCode tool part。
- Scientific MCP：7 次，1 次成功、6 次科学状态失败。
- Native：72 次，69 成功、3 失败。
- 调用过 `parse_quantum_chemistry_output`、`analyze_thermochemical_selectivity`、`derive_thermochemistry`、`validate_thermochemistry_inputs`，并大量使用 Python/Bash。

失败主要是模型漏填公开 schema 中的必需字段、把 `max_array_elements` 设得过小或缺少热化学输入，并非 adapter 缺陷。模型随后用原生脚本成功恢复，因此不构成 objective issue。

### 4.2 Q2：BiPy 与 PhPy 选择性来自动力学还是热力学

最终分数：22/100。

参考要求是：

- BiPy 在 P0/P1/P2 均具有更低的偶联势垒；
- ΔΔG‡ 约 6.4/7.1/11.3 kcal mol⁻¹；
- 两类产物均强放能，产品热力学差异不能解释主要选择性；
- 因而选择性是动力学控制。

模型虽然进行了大量结构分析，但最终路径赋值失败：

- 把若干候选错误归为 BiPy/PhPy product 或 TS；
- P0 得到约 −28 kcal mol⁻¹ 的错误 ΔΔG‡，符号和数量级均与参考相反；
- P1/P2 没能找到可比较的 BiPy TS；
- 最终错误判定为热力学控制。

工具情况：

- 90 个模型 step；3 个 session，包括两个 `general` 子智能体。
- 主/子会话合计 122 个 native 事件，109 成功、13 失败。
- 未形成有效 Scientific MCP 调用，主要使用 `read`、`bash`、`write`、`edit`、`grep`、`glob` 和 `task`。

子智能体内部分析已经由 `_model_io.jsonl` 完整记录，并在最终评分时纳入；补充子会话证据后分数仍为 22，说明低分不是轨迹缺失，而是最终科学赋值和结论错误。

### 4.3 Q3：P2 中 C−C 与 C−O 哪条路径占优

最终分数：55/100。

参考要求是：

- 已支持的 P2 C−C 势垒约 14.3 kcal mol⁻¹；
- 公开包没有明确 C−O TS 记录，因此不应编造独立精确值；
- 可结合论文型证据认为 C−O 约 18 kcal mol⁻¹，比 C−C 高约 4 kcal mol⁻¹；
- C−C 应占主导。

模型的优点是正确识别了 C−O 记录缺失，并没有把缺失记录伪装成独立计算值；结合实验信息正确预测 C−C 为主、C−O 为次。

主要错误：

- 把 C−C 势垒算成 21.3 kcal mol⁻¹；
- 没有恢复 14.3 kcal mol⁻¹ 的正确基准；
- 用 298 K 自由能配合 353 K Eyring 公式，温度口径不一致；
- 原生 xTB 试算的 charge/multiplicity 命令格式错误；
- 两次拟调用 Scientific Action 的 JSON 是模型生成的畸形工具参数，未进入 MCP dispatcher。

工具情况：

- 53 个模型 step；2 个 session；99 个 native 事件，96 成功、3 失败。
- 加入子智能体内部轨迹后最终分数由 56 微调为 55，objective issue 仍为 0。

### 4.4 Q4：偶联是 concerted/stepwise、synchronous/asynchronous 中的哪一种

最终分数：36/100。

参考机理是 stepwise、asynchronous、apical-to-equatorial ligand coupling，并经过 dearomatized intermediate。

模型正确识别到成键过程具有 asynchronous 特征，也使用距离、频率和能量进行了结构审计；但关键机理判断错误：

- 把过程判成 concerted but asynchronous；
- 否定了 dearomatized intermediate；
- 没有识别 apical P−C bond 的断裂及 apical-to-equatorial 重排；
- 对 oxygen lone-pair participation 的结论缺少电子结构证据。

工具情况：

- 21 个模型 step；1 个 session。
- Scientific MCP：10 次，4 成功、6 失败，均为 `parse_quantum_chemistry_output`。
- Native：36/36 成功。

早期解析失败来自缺失必需参数和显式数组上限过小，模型调整后成功；这类探索性失败不属于框架问题。

### 4.5 Q5：标准条件下的整体决速步骤

最终分数：70/100。

模型正确完成了大部分实验—计算证据整合：

- 正确提取 OMe 0.16 < Me 0.37 < H 1.00 < Cl 1.89；
- 正确解释正 Hammett ρ 与 electrophilicity 的关系；
- 正确利用 EtONa 快速反应、NMR 未检出 P(V) 和低稳态浓度；
- 正确意识到配体偶联与选择性密切相关。

核心错误是把 intramolecular ligand coupling 判为整体 rate-determining step。参考答案要求：

1. 整体 RDS：alcohol attack/addition at phosphonium P；
2. 选择性决定：P(V) ligand coupling；
3. 不可逆阶段：dearomatized intermediate 的后续 collapse。

模型把前两类角色合并，因此相关两项大幅扣分。

工具情况：

- 30 个模型 step；1 个 session。
- Scientific MCP：6 次，3 成功、3 失败。
- Native：40 次，39 成功、1 失败。

### 4.6 Q6：完整端到端科研任务

最终分数：53/100。

模型的主要优点：

- 审计了 66 个结构和 198 份计算记录；
- 检查 normal termination、虚频、能量层和结构候选；
- 编写并修复了独立 Python 分析程序；
- 整合了取代基速率、EtONa、NMR 和 side-product 证据；
- 报告清晰地区分事实、推断、失败分析和不确定性。

主要科学差距：

| 项目 | 模型结论 | 参考结论 |
|---|---|---|
| P0/P1/P2 势垒 | 39.4/20.4/21.3 | 30.91/19.81/14.30 |
| 热化学口径 | 主要使用 298 K，未严格做 353.15 K、1 M mRRHO | 353.15 K、1 M、统一 mRRHO |
| 机理 | concerted C−C formation/P−C cleavage | stepwise asynchronous apical-to-equatorial coupling |
| 中间体 | 未识别 dearomatized intermediate | 必须经过 dearomatized intermediate |
| P(V) 阶段 | 认为不经过可检测 P(V) 并从 P(III) 直接偶联 | alcohol addition 先形成 P(V)，随后 ligand coupling |
| 整体 RDS | C−C ligand coupling | alcohol addition before ligand coupling |
| 选择性 | 未清晰独立于 RDS | P(V) ligand-coupling TS 决定选择性 |

工具情况：

- 36 个模型 step；1 个 session。
- 63 个 native 事件，61 成功、2 失败。
- 没有 Scientific MCP 调用，主要通过 Python/Bash 直接解析已有 Gaussian/ORCA 记录。
- 两个 native 失败是脚本语法/文件写入类错误，均被模型自行修复。

最终裁判从 54 重评为 53。重评修正了第一版裁判中“把错误的 C−C RDS 称为正确速率控制”的内部矛盾；两个分数都保存在 `_score_history.jsonl`。

## 5. 工具编排总体情况

六个最终任务合计：

- Agent model steps：289；
- Agent sessions：9；
- Scientific MCP 事件：23，其中 8 成功、15 失败；
- Native 主/子会话事件：432，其中 410 成功、22 失败；
- 当前裁判可见的总过程事件：455，其中 418 成功、37 失败。

这些失败不能简单解释成工具箱不可用：

| 失败类型 | 归属 | 处理 |
|---|---|---|
| 漏填公开 schema 必需字段 | Agent 参数错误 | 返回 `invalid_request`，模型修正后重试 |
| `max_array_elements` 过小 | Agent 显式资源/输出限制 | 返回清晰错误，不自动扩大 |
| 使用工作区外 `/tmp` 路径 | Agent 路径错误 | 工作区边界阻止访问 |
| 畸形工具 JSON | 模型生成错误 | 未进入 dispatcher，记录为 `invalid` |
| xTB charge/multiplicity CLI 写错 | Agent 原生软件调用错误 | 原生命令失败，保留轨迹 |
| Python/文件编辑语法错误 | Agent 自写程序错误 | 模型自行诊断并修复 |

框架没有增加 callback、默认参数回退、自动 Backend 切换或隐藏工作流。失败仍由智能体观察和处理，符合 benchmark 对自主工具编排的要求。

## 6. 模型调用次数与 token 审计

### 6.1 此前两轮子任务

此前两个批次为：

- `batch_20260721_194056_d964d2`
- `batch_20260721_200951_0fb6d9`

从隔离的 OpenCode SQLite 数据库重新统计，而不是只数主会话 stdout：

| 批次 | Agent 消息/调用记录 | 有 `step-finish` | sessions | 总 token | cache read |
|---|---:|---:|---:|---:|---:|
| 第一轮 | 197 | 197 | 5 | 43,953,614 | 42,576,512 |
| 第二轮 | 121 | 118 | 6 | 25,525,461 | 24,120,320 |
| 合计 | 318 | 315 | 11 | 69,479,075 | 66,696,832 |

因此，之前不是“10 个任务等于 10 次模型请求”，而是 10 次任务执行产生了 318 个已记录的 Agent 模型 step/请求记录；其中 315 正常结束，2 个在 Q3 人工终止时中断，1 个是 Q5 的 402 错误。

旧评分器会覆盖 `_score.json`。根据会话执行记录，此前另有约 15 次 Judge 调用；旧磁盘上只能保留 8 个最终 score artifact，无法仅靠旧文件逐次复核。该问题现已由 append-only `_score_history.jsonl` 修复。

### 6.2 最终有效评估阶段

| 批次 | Agent steps | sessions | Agent total tokens | cache read |
|---|---:|---:|---:|---:|
| 五子任务 | 253 | 8 | 55,424,491 | 53,535,616 |
| E2E | 36 | 1 | 7,837,609 | 7,574,784 |
| 合计 | 289 | 9 | 63,262,100 | 61,110,400 |

最终阶段共进行了 14 次 Judge 调用：

- 五个自动初评分；
- 五个修订裁判规则后的重评分；
- Q2/Q3 纳入完整子智能体轨迹后的各一次重评分；
- E2E 初评和一致性修订后的重评。

因此最终有效阶段共有 289 次 Agent 模型 step 加 14 次 Judge 调用，共 303 次模型调用记录。连接测试、OpenCode preflight 和被排除的旧路由失败批次不计入该科学评分统计。

新 provider 没有在 OpenCode 中配置价格表，因此日志 `cost=0` 仅表示“无法本地估价”，不表示实际免费。Agent token 中绝大多数为 cache read；高消耗的根本原因是每个任务都暴露完整工具箱 schema，并在多轮工具编排中反复携带长上下文。

## 7. 新增模型输入输出轨迹

每个运行工作区现在自动生成 `_model_io.jsonl`。

最终任务轨迹规模：

| 任务 | steps | sessions | 文件大小 |
|---|---:|---:|---:|
| Q1 | 59 | 1 | 796,280 bytes |
| Q2 | 90 | 3 | 1,615,410 bytes |
| Q3 | 53 | 2 | 973,112 bytes |
| Q4 | 21 | 1 | 705,420 bytes |
| Q5 | 30 | 1 | 485,765 bytes |
| Q6 | 36 | 1 | 567,517 bytes |

轨迹采用 event-sourced 格式：

- 初始 `input_message` 只保存一次；
- 每个 `model_step` 记录本步输入上下文引用、新增输入引用、模型输出、reasoning、工具调用/结果、token、cost 和 finish reason；
- 主智能体和子智能体按 `session_id` 分开，不错误混合上下文；
- `INSTRUCTIONS.md`、工具目录、provider config 和原始事件流通过路径和 SHA-256 引用；
- API key、Authorization、token 和常见 secret 自动脱敏；
- 不记录原始 HTTP 认证头，也不声称可以逐字节重放 provider 私有请求。

格式说明：`docs/MODEL_IO_TRAJECTORY_FORMAT.md`。

## 8. 评分器修订与稳定性

本轮发现并修复了三类评分问题：

1. 把 Agent 漏字段、错误路径、畸形 JSON 和原生 CLI 错误误标成 objective framework issue；
2. 裁判结论没有逐项交叉检查 `expected_result`，曾把错误的 RDS 描述为“正确区分速率控制”；
3. 只读取主会话 native trace，遗漏 `task` 子智能体内部过程。

修复后：

- 六个最终任务 `objective_issue_flags=[]`；
- 子会话工具事件通过 `_model_io.jsonl` 进入评分器并按 `callID` 去重；
- `invalid` 工具调用被记录为失败而不是成功；
- 每次评分都记录 model、timestamp、token usage 和历史分数。

Judge 仍是概率模型，分数存在一定方差。当前历史中最明显的是 Q5 从初评 35 调整到参考一致性修订后的 70。后续若用于正式排行榜，建议：

- 每题使用 3 次独立 Judge，报告中位数和离散度；
- 对数值、RDS/选择性角色和关键机理标签增加确定性检查；
- 保留 LLM Judge 对开放式证据质量、失败处理和不确定性的评分。

## 9. 本轮代码修订与 Git 记录

| Commit | 内容 |
|---|---|
| `560acaa` | 正确读取 `config.local.env` 的 OpenCode URL/model，并用运行时占位符传递新 Key |
| `14d438b` | 修订 objective issue 判定，增加 append-only Judge history、model、time、usage |
| `73c315f` | 新增主/子智能体 `_model_io.jsonl` 输入输出轨迹与格式文档 |
| `9d8b17f` | 将 YAML `max_turns` 实际传入 OpenCode build/general Agent |
| `64c034e` | 要求裁判逐项对照 expected result 并保持 RDS/选择性/critical failure 一致 |
| `d7f450f` | 将子智能体内部工具轨迹纳入过程评分并去重 |

最终完整回归测试：`210 passed in 414.16s`。

用户原有未跟踪文件未修改：

- `config.local copy.env`
- 四个 `core.*` 文件
- `tasks/Heterobiaryl_PV_Benchmark.zip`

## 10. 当前工具箱是否造成评估偏差

本轮最终结论是：没有证据表明有效六任务中的低分由工具箱客观故障造成。

支持这一结论的证据：

- 六项 Agent 均正常退出并写出报告；
- 六项 Judge 均正常解析；
- 所有 objective issue 最终为空；
- Q1 可用同一数据和工具环境准确恢复参考势垒；
- Q2/Q3 纳入完整子智能体轨迹后仍保持低分；
- Q4/Q5 的 MCP 参数错误均有明确、可操作的 schema 错误，并可被模型修正；
- E2E 的主要错误可以直接追溯到错误驻点选择、温度/标准态口径和机理推断。

因此当前分数可以用于评价该模型在本论文任务上的真实能力：它擅长局部数值重建和脚本化数据审计，但在匿名候选的化学角色赋值、竞争路径比较、P(V) 机理和“整体决速步骤 vs 选择性决定步骤”分离方面仍明显不足。

## 11. 仍建议的后续改进

1. 为正式 leaderboard 实施 3-judge 或 judge ensemble，报告方差。
2. 为明确的数值/标签参考增加确定性评分，与开放式 LLM Judge 并行。
3. 将完整工具 schema 改成可审计的分层发现机制，降低每轮 10 万级输入 token，但不能按任务隐藏候选工具或替智能体选择 Backend。
4. 继续保留 Action、软件原生执行和自写代码三层结构；本轮 E2E 证明模型确实会根据任务自主选择 native Python/Bash，而非被固定 Action 流程限制。
5. 对后续论文 benchmark 继续提供匿名化原始数据、显式数据限制、隐藏参考过程和过程级 rubric，不为每篇论文写固定工作流。

## 12. 总结

Heterobiaryl P(V) 六任务 benchmark 已完成从任务复核、数据匿名化、框架修复、真实运行、轨迹审计到最终评分的完整闭环。

当前工具箱能够支持这类开放式论文流程评估。它不需要为该论文新增专用 Action；智能体已经通过预定义 Action、原生软件解析和自写程序完成自主编排。最终结果也证明了该 benchmark 的区分度：同一模型可以在窄范围势垒重建上达到 96/100，但在完整机理整合上仅为 53/100。
