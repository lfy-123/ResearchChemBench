# Heterobiaryl P(V) 开放发现评估提交说明

## 1. 本轮目标

本轮不替智能体规定软件、Backend、Action 或调用顺序，而是固定科研问题、输入边界和科学证据标准：

- Q1–Q5：`focused_open_discovery`，问题范围明确，研究计划、程序选择、参数、分支和停止条件由智能体决定。
- Q6：`independent_open_discovery`，智能体需要自主提出并修订端到端研究计划，覆盖质子化、BiPy/PhPy 选择性、C–C/C–O 竞争、反应坐标机理和动力学角色。

修改前代码保存在 Git 标签 `before-heterobiaryl-open-discovery-20260723`，对应提交 `539d0a26d62f325e1a360d1c08812d627b32e4d1`。

## 2. 解决的主要问题

| 原问题 | 本轮处理 |
|---|---|
| Q6 只完成一条容易路径便提前结束 | 明确五类核心假设必须分别得到支持、证伪或有记录的失败/不确定尝试；一条成功路径不再等于端到端完成。 |
| 任务没有要求先形成研究计划 | 六个任务均要求在数值计算前写资源分层计划并记录修订；Q6 要求独立假设树、验证门和停止条件。 |
| 未筛选全部输入种子 | Q1/Q2/Q6 要求审计全部九个种子；聚焦 P2 的任务要求审计全部 P2 种子，或给出计算支持的排除理由。 |
| 高阶鞍点被误当成 TS、势垒或上界 | 过渡态必须有且仅有一个化学相关虚频，并有正反向连通性或等价直接反应坐标证据；高阶鞍点本身不构成严格上界。 |
| 不同温度、标准态或方法被混成同一能量剖面 | 主剖面要求统一使用 353.15 K、1 M、乙醇条件和兼容的能量参考；敏感性结果必须单列。 |
| Q3 定性顺序正确但数量级严重错误仍获满分 | 新增 C–C、C–O、可比条件和参考尺度协调四个证据门；裁判报告失败门后，框架会确定性应用分数上限。 |
| Q5/Q6 混淆 RDS、选择性决定步骤和不可逆步骤 | 评分明确分别核对醇加成决速、P(V) 配体偶联选控和后偶联塌陷强不可逆。 |
| 只交一份叙述报告，不便审计 | Q1–Q5 增加计划、证据摘要和失败日志；Q6 增加驻点表、能量剖面、机理证据和机器可读最终答案。 |

证据文件是审计产物，不是固定工作流。智能体仍可自由决定具体计算路线和软件组合。

## 3. 两组评估设置

两组设置使用相同 URL 和 key，不在提交脚本中覆盖凭据。

| 设置 | 评估智能体 | 裁判模型 | 输出根目录 |
|---|---|---|---|
| Flash | `bailian/deepseek-v4-flash` | `bailian/deepseek-v4-pro` | `workspaces/heterobiaryl_open_discovery/agent_deepseek-v4-flash__judge_deepseek-v4-pro` |
| Pro | `bailian/deepseek-v4-pro` | `bailian/deepseek-v4-pro` | `workspaces/heterobiaryl_open_discovery/agent_deepseek-v4-pro__judge_deepseek-v4-pro` |

Q1–Q5 串行运行，单任务上限 14,400 秒、280 turns；Q6 单独运行，上限 21,600 秒、400 turns。串行设置用于避免量化化学后端争用并提高两个模型设置之间的可比性，这些上限不是要求模型必须消耗完。

## 4. 提交命令

先检查计划，不调用 API：

```bash
bash scripts/submit_heterobiaryl_open_discovery.sh all --dry-run
```

分别提交两组完整六任务评估：

```bash
bash scripts/submit_heterobiaryl_open_discovery.sh flash
bash scripts/submit_heterobiaryl_open_discovery.sh pro
```

也可以只提交某一阶段：

```bash
bash scripts/submit_heterobiaryl_open_discovery.sh flash --stage subtasks
bash scripts/submit_heterobiaryl_open_discovery.sh flash --stage q6
```

每个阶段的终端日志保存在对应模型输出根目录的 `logs/` 下；运行 workspace 继续位于该目录的 `cli_runs/batch_*` 下。

## 5. 本轮保留的上一轮结果

清理策略只保留上一轮最终采用的六个运行目录：

1. `workspaces/cli_runs/batch_20260722_181426_80351d/Heterobiaryl_PV_01_Protonation_opencode_20260722_181426_e93dad`
2. `workspaces/cli_runs/batch_20260722_171802_f29209/Heterobiaryl_PV_02_CC_Selectivity_opencode_20260722_171802_8f7287`
3. `workspaces/cli_runs/batch_20260722_154657_f0a605/Heterobiaryl_PV_03_CC_vs_CO_opencode_20260722_154657_e19409`
4. `workspaces/cli_runs/batch_20260722_170358_6e0c89/Heterobiaryl_PV_04_Coupling_Mechanism_opencode_20260722_170358_72e08d`
5. `workspaces/cli_runs/batch_20260722_171802_f29209/Heterobiaryl_PV_05_Rate_Determining_Step_opencode_20260722_173155_5a5a43`
6. `workspaces/cli_runs/batch_20260722_183934_38fb51/Heterobiaryl_PV_06_End_to_End_opencode_20260722_183934_cd2877`

作废复跑、旧批次和后端 smoke workspace 已删除。旧报告若仍引用这些诊断运行，对应文件已不再保留；验证报告生成器在后续重新生成时会将缺失路径标记为“已按 workspace 保留策略清理”。

## 6. 重要边界

- 本轮只准备任务、评分和提交脚本，没有实际提交任何模型评估。
- 裁判模型通过 `--judge-model` 单次覆盖；`JUDGE_API_BASE`、`JUDGE_API_KEY`、Agent URL 和 key 仍由现有本地环境文件提供。
- 分数上限只由裁判明确报告的证据门失败和可观测 managed-computation 指标触发，不按固定工具名或固定调用顺序打分。
