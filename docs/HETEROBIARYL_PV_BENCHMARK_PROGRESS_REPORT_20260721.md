# Heterobiaryl P(V) Benchmark 阶段性构建与评估报告

> 本文档是 2026-07-21 的阶段性记录，已由
> [`HETEROBIARYL_PV_BENCHMARK_FINAL_EVALUATION_REPORT_20260722.md`](HETEROBIARYL_PV_BENCHMARK_FINAL_EVALUATION_REPORT_20260722.md)
> 取代。最终报告包含新 API 修复、五子任务有效重跑、完整 E2E、模型调用统计和主/子智能体 `_model_io.jsonl` 轨迹。

日期：2026-07-21（UTC）

状态：六个任务及其数据、隐藏参考答案和 100 分制评分规则已完成构建；五个子任务已完成一轮诊断评估和一轮修复后评估。第三轮五子任务及完整端到端任务因 DeepSeek Agent API 返回 HTTP 402 `Insufficient Balance` 暂未提交。

## 1. Benchmark 目标

本 benchmark 用于评估智能体在不给出软件、Backend、Action 或固定调用顺序的条件下，能否：

1. 审计匿名实验与计算数据；
2. 自主形成科学假设和计算计划；
3. 自主选择预定义 Action、软件原生执行或自写分析程序；
4. 正确处理驻点、构象集合、热化学口径、反应路径和实验约束；
5. 保留失败轨迹、数据来源和不确定性；
6. 得到可与论文参考过程和结论比较的科学报告。

任务指令中没有出现 Gaussian、ORCA、GoodVibes、MCP、Backend、Action 名称或指定的软件调用顺序。系统提示词仍向所有任务公开同一套完整三层工具箱，由智能体自行编排。

## 2. 论文与原始任务包复核

### 2.1 论文核心参考结论

- BiPy 路径发表势垒：P0/P1/P2 = 30/20/14 kcal mol⁻¹。
- PhPy 路径发表势垒：P0/P1/P2 = 37/27/25 kcal mol⁻¹。
- PhPy−BiPy 势垒差：7/7/11 kcal mol⁻¹。
- P2 竞争 C−O 路径发表势垒约 18 kcal mol⁻¹，比 C−C 高约 4 kcal mol⁻¹。
- 关键配体偶联为 stepwise、asynchronous、apical-to-equatorial 过程，并经过 dearomatized intermediate。
- 取代基相对速率：OMe 0.16 < Me 0.37 < H 1.00 < Cl 1.89。
- 标准酸性条件下最可能的决速步骤是醇对 phosphonium 磷中心的加成；P(V) 内部配体偶联主要决定选择性。

### 2.2 原始任务包中发现并修正的问题

1. 原实验证据 E03 把质子化 NMR 位置写成 Figs. S17–S18；正文实际引用 Fig. S12，公开输入已更正为 Fig. S12。
2. 原任务指令含有 Action/软件建议，正式任务已全部移除。
3. 原任务包没有归档 IRC 轨迹、键级/孤对电子轨迹或明确的 C−O 过渡态记录。
4. 因此 Q3 与 Q4 的评分明确允许“证据不足”的谨慎结论，不鼓励根据缺失记录编造精确数值或把“未归档”解释成“路径不存在”。
5. 发表整数值与当前统一口径复算值被分开保存，禁止把论文取整数值冒充独立复算结果。

## 3. 正式输入数据包

公开匿名输入包：`tasks/_heterobiaryl_pv_shared/public/computational_records.zip`

SHA-256：`97fa402aec3fa9191d0352485c7c4a8c77415d47d7c917dcb1cc0548f04d495d`

| 项目 | 数量/状态 |
|---|---:|
| ZIP 条目 | 298 |
| 解压后大小 | 240,266,644 bytes |
| 匿名候选结构 | 66 |
| P0/P1/P2 候选数 | 17/25/24 |
| 反应物侧起始构象 | 27 |
| Gaussian 优化/频率记录 | 66 |
| Gaussian 大基组单点记录 | 66 |
| ORCA 相关单点记录 | 66 |
| 计算记录总数 | 198 |
| 实验观察 | E01–E12，共 12 条 |
| 结构哈希、记录哈希、原子数校验 | 全部通过 |
| 作者、机构、原始任务名和路径标签泄漏扫描 | 0 命中 |

真实工作区展开测试确认：每个任务得到 298 个公开输入文件；隐藏论文、gold answer、private mapping 和 `ground_truth.json` 均不会进入智能体工作区。

## 4. 六个正式任务

| 任务 ID | 科学问题 | 评分重点 |
|---|---|---|
| `Heterobiaryl_PV_01_Protonation` | 连续 N-质子化如何改变 BiPy 偶联势垒 | 驻点/构象集合、统一热化学、31/20/14 趋势、电子结构解释 |
| `Heterobiaryl_PV_02_CC_Selectivity` | BiPy 与 PhPy 选择性是动力学还是热力学控制 | 两路径赋值、ΔΔG‡、反应自由能、动力学/热力学判别 |
| `Heterobiaryl_PV_03_CC_vs_CO` | P2 中 C−C 与 C−O 哪条路径占优 | 已支持的 C−C 势垒、缺失 C−O 记录的处理、产物预测 |
| `Heterobiaryl_PV_04_Coupling_Mechanism` | 偶联是 concerted/stepwise、synchronous/asynchronous 中的哪一种 | 驻点序列、P−C/C−C 重组、dearomatized intermediate、氧孤对 |
| `Heterobiaryl_PV_05_Rate_Determining_Step` | 标准条件下的决速步骤是什么 | 取代基速率、EtONa/NMR、决速与选择性决定步骤分离 |
| `Heterobiaryl_PV_06_End_to_End` | 从匿名证据自主重建完整机理和能量图景 | 问题形成、工具编排、全部计算/实验整合、失败与不确定性 |

所有任务使用 `rubric_100`，每项 rubric 权重之和严格为 100。评分不要求唯一软件、唯一 Backend 或唯一调用顺序。

## 5. 隐藏参考热化学口径

统一口径为 353.15 K、1 M、乙醇环境；Grimme mRRHO 熵、100 cm⁻¹ 截断、global free-rotor inertia、RRHO 焓、频率和 ZPE scale factor 1.0、仅翻转 −5 到 0 cm⁻¹ 的微小虚频、不启用额外对称性修正，并组合作者归档的相关单点能。

| 状态 | BiPy ΔG‡ | PhPy ΔG‡ | ΔΔG‡ | BiPy ΔGreact | PhPy ΔGreact |
|---|---:|---:|---:|---:|---:|
| P0 | 30.91 | 37.32 | 6.41 | −32.38 | −32.54 |
| P1 | 19.81 | 26.86 | 7.05 | −30.53 | −28.51 |
| P2 | 14.30 | 25.57 | 11.27 | −31.35 | −31.85 |

这些复算反应自由能与论文图中整数值相差约 6–9 kcal mol⁻¹，因此两套值在 ground truth 中明确分栏。

## 6. 为公平评估实施的框架和工具箱修复

| 修复 | 原问题 | 当前状态 |
|---|---|---|
| 安全任务 ZIP 展开 | 大型共享输入无法在运行时安全展开 | 校验 SHA-256、路径穿越、重复目标、特殊文件、条目数和 5 GB 上限 |
| 100 分 rubric judge | 原框架只有 0/1 ChemGraph 判分 | 支持逐 criterion 分数、critical failure、objective issue、归一化分数 |
| 裁判总分一致性 | 裁判总分可能不等于 criterion 之和 | 对各项分数限幅并以 rubric 项目之和作为最终总分 |
| 三层执行轨迹送审 | 裁判只看 MCP，忽略 Bash/Python/代码，曾把真实分析判为“伪造” | 同时送入 MCP、原生 shell/file 事件和 Agent-authored code/artifacts |
| GoodVibes `--check --spc` | GoodVibes 4.3.0 原生组合触发内部 `TypeError` | 分开执行 frequency check 与 SPC 元数据一致性检查，保留显式 workaround provenance |
| GoodVibes 溶剂警告 | 正常 SMD/CPCM caution 被误判为输入不一致 | 警告仍保留，但不再使 `consistent=false` |
| Gaussian/ORCA typed solvation | 缺少 SMD/CPCM 的结构化参数 | 已增加 `solvation_model` 与 `solvent`，并验证输入渲染 |
| cclib 参数可发现性 | tool description 未列出 property group 与其他字段语义 | 已列出完整 property group、frame、boolean 和数组上限说明 |
| cclib 解析 ORCA 4 DLPNO | 首个 SCF block 缺 RMS-density target，cclib 1.8.1 `IndexError` | 保存缺失 target 为 NaN，仅修复 parser metadata；电子能不变，并返回 compatibility warning |
| `file_path` 引用 | 模型使用显式 `{"file_path": ...}`，框架只接受字符串/`path` | 已作为同义显式路径接入，仍执行工作区边界检查 |
| Agent/MCP 子进程清理 | 停止父进程后 `.opencode`/MCP 可能成为孤儿并保持 stdout | 每次运行使用独立 POSIX process group，停止、超时和父进程先退出时清理整组 |

修复没有加入科学默认值、自动回退、失败 callback 或自动 Backend 切换。

## 7. 验证结果

- 完整 pytest：205 passed。
- 脱敏 P0 记录经 GoodVibes 处理，与原始记录的 selected Gibbs energy 最大差值为 0 Hartree。
- 真实 cclib Gaussian 解析：P0_C009 得到唯一虚频 −420.5351 cm⁻¹。
- 真实 GoodVibes SPC validation：`status=success`、`consistent=true`、workaround 被记录。
- 修复后的 cclib 可成功解析 P0_C001 的 ORCA DLPNO 输出，并返回非空 SCF energies。

## 8. 第一轮诊断评估

批次：`workspaces/cli_runs/batch_20260721_194056_d964d2`

第一轮在修订后的三层评分器下重新评分：

| 任务 | 分数 | MCP 成功/总数 | Native 事件 | 主要模型表现 |
|---|---:|---:|---:|---|
| Q1 Protonation | 52 | 0/0 | 57 | 做了完整解析，但热化学/构象选择导致势垒趋势错误 |
| Q2 CC Selectivity | 84 | 0/4 | 34 | 正确得到动力学选择性；温度使用 298 K 而非 353.15 K |
| Q3 CC vs CO | 63 | 4/4 | 62 | 正确谨慎处理缺失 C−O 数据，但未可靠复现 14.3 kcal mol⁻¹ C−C 势垒 |
| Q4 Mechanism | 31 | 20/35 | 34 | 正确识别 asynchronous 部分，但错误判为 concerted 且否定 intermediate |
| Q5 RDS | 56 | 6/18 | 49 | 提取实验趋势正确，但把配体偶联误判为整体决速步骤 |

均分：57.2/100。

第一轮最重要的客观发现是旧裁判只看 MCP 事件。Q2 原先因此被错误判为 0 分；三层轨迹修复后重新评分为 84 分。

## 9. 第二轮修复后评估

批次：`workspaces/cli_runs/batch_20260721_200951_0fb6d9`

| 任务 | 状态/分数 | 说明 |
|---|---:|---|
| Q1 Protonation | completed，67/100 | 11 次 Scientific Action 成功；TS/构象选择仍使 41.4/22.3/22.1 偏离参考趋势 |
| Q2 CC Selectivity | completed，93/100 | ΔΔG‡ 约 6.25/7.64/11.54，动力学选择性判断正确；主要使用自主 Python/Bash |
| Q3 CC vs CO | failed，无分数 | 远程模型请求连续 30 分钟无输出；本地进程仍存活，手动按监控阈值终止 |
| Q4 Mechanism | completed，68/100 | P−C/C−C 异步重组证据很好，但仍把总体过程判成 concerted 并否定 dearomatized intermediate |
| Q5 RDS | failed，无分数 | Agent API 返回 HTTP 402 `Insufficient Balance`，报告写入前退出 |

三个可评分任务均分：76.0/100。该均分不能与完整五任务均分直接比较，因为 Q3/Q5 是外部 API 失败而非低分。

## 10. Git 版本记录

| Commit | 内容 |
|---|---|
| `c75626d` | Heterobiaryl benchmark 集成前检查点 |
| `fd7768d` | 六任务、脱敏数据、rubric、GoodVibes/溶剂与评测框架基线 |
| `5809e05` | 裁判接入原生 Agent 执行轨迹 |
| `02f643b` | 裁判接入 Agent-authored code |
| `14a4d4d` | 修复 cclib 对 ORCA convergence block 的解析 |
| `41225dc` | 接受受控的显式 `file_path` 引用 |
| `af7c572` | Agent 和 MCP 子进程组统一清理 |

未提交且未修改的用户文件：四个 `core.*` dump 和原始 `tasks/Heterobiaryl_PV_Benchmark.zip`。

## 11. 当前阻塞与用户需要处理的事项

唯一阻塞是 DeepSeek Agent API 账户余额不足。错误来自 Agent 使用的 `OPENAI_API_KEY` 对应账户，而 Judge API 仍可正常评分。

请为 `config.local.env` 中 `OPENAI_API_KEY` 对应的 DeepSeek/OpenAI-compatible 账户补充余额，或替换为另一个可调用 `deepseek-v4-flash` 的 Agent API key。不要把 key 发到对话中，直接在本机更新 `config.local.env` 即可。

余额恢复后剩余顺序：

1. 从全部修复后的 Git 版本重新运行五个子任务；
2. 检查是否还存在客观失败；
3. 五项可公平评估后运行 `Heterobiaryl_PV_06_End_to_End`；
4. 用 `deepseek-v4-flash` 裁判完整端到端报告；
5. 更新本报告为最终六任务总报告，逐任务比较工具调用、参考流程、数值差距和模型能力边界。
