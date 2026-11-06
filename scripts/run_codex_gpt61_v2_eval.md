# Final V2：Codex + gpt-6.1-sol 运行说明

2026-10-24。入口为 `scripts/run_codex_gpt61_v2_eval.sh`，可运行 `tasks/final_v2_verified_autonomous_research` 中任意有效单题。当前目录共 45 题。每次新启动创建独立目录，结果自动评分后写入 `workspaces/codex_gpt61_v2/paper_ID_UTC时间_随机后缀/`。

Agent 和 Judge 均为 **gpt-6.1-sol / high**，在加载本地配置之后固定，避免旧的 gpt-5.6-sol 配置覆盖。任务与评分文件逐字节复制，沿用题目当前的 `paper_science_v2`，不改变科学问题或评分规则。Agent 仅获得框架允许公开的输入。

复用现有 `scripts/test_codex_gpt56.sh` 和正式评估框架；该底层脚本名中的 gpt56 不会覆盖本入口设置的模型。默认资源与当前 Codex pilot 一致：48 核、204800 MB、总期限 345600 秒（四天）、单项计算上限 86400 秒、600 个已完成 Codex turn；不另设总 token 上限。turn 不等同于工具调用次数。

新启动同时传入唯一 `--output-dir` 和框架 `--resume`：前者确保创建新实验，后者只开启本次实验的有限自动恢复，不会选择旧目录。已有恢复流程可处理受支持的暂时 API 故障及拒绝加密历史的错误；服务器进程被关闭后仍需手动 resume。不得把反复执行新启动命令当作续跑。

## 推荐的五题

筛选依据是公开任务中的科学决策空间、关键证据难度和解释可辨识性，而非统一的 `hard` 标签，也不是 gpt-6.1-sol 实测难度排名。

| 论文 ID | 科学问题 | 自主科研决策与难点 | 结论边界 |
|---|---|---|---|
| `paper_a3892396b1843698` | 二丁二烯基环丙烷 3a 的热重排行为 | 自行生成构象、候选变换和电子态，发现并验证竞争通道；起始结构并非已认证极小值，路径连接和势垒解释必须有证据。 | 不要求定量动力学轨迹分支，也不能把几何变化当作新物种。 |
| `paper_db6c4e0558113873` | 光／铜条件下联烯酸酯氯磺酰化的区域和立体选择性 | 从已知选择性提出局部 C–Cl 成键解释，自行确定铜的价态、配位模型和候选中间体，区分结构稳定性与实际反应选择性。 | 已知产物是待解释的观测，不是隐藏预测；不要求完整光氧化还原循环或产率。 |
| `paper_d83e607f125440cc` | 为什么甲硫基取代苄醇在黄素介导电光化学条件下氧化较差 | 自行提出并检验取代基、电子结构和化学转化解释，设计分子间比较；正确区分电子解离能、自由能势垒、自由基分布和宏观转化率。 | 分子结果不能单独证明完整催化剂／电极网络或定量产率。 |
| `paper_60f4c45810428116` | 微流反应的停留时间／温度数据究竟能确定哪些动力学信息 | 自行建立生成与消耗模型，处理淬灭后间接观测及分类数据；检验模型非唯一性与参数可辨识性。难点主要是研究设计和推断，计算量可能较小。 | 数据不支持未经检验的唯一基元机理、精确基元速率或连续最优条件。 |
| `paper_3e4cad1d1d650d0c` | 芴负离子的激发态还原能力及与 4-氯苯甲醚的相互作用 | 联合氧化还原、光谱、寿命和猝灭证据建立解释，判断不同解释能否区分，处理溶液模型近似和源数据条件不一致。 | 不要求完整催化循环、断键速率或产率；单一强度变化不能自动证明唯一猝灭机制。 |

这五题都允许自主选择模型、假设和计算路线，没有规定统一的假设数量或固定计算顺序。但它们仍是有明确科学范围、依据论文关键科学结果评分的自主科研评估，并不意味着任意合理探索路线都能得到满分。

五题的 `reference_qualification.json` 均记录 `formal_scoring_permitted=true`、`current_scope_verified=true`，沿用已验证的限定范围；同时 `release_ready=false`，表示专家／发布校准与当前运行评分资格是分开的。这里没有把历史参考验证解释为覆盖所有新假设的验证。

当前 final V2 与早期 `workspaces/codex_gpt56_v2` 不是天然严格配对实验：旧入口确实配置 gpt-5.6-sol/high，但任务和评分后来有更新。新入口保留每次运行的任务快照与内容哈希；如比较模型，应先核对双方任务包和评分版本。`paper_a3892396b1843698` 在当前小分子目录也出现过，但两个目录的任务文本和包哈希不同。

## 五台服务器分别运行

每台服务器先进入项目：

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench
```

1. 热重排通道：

```bash
bash scripts/run_codex_gpt61_v2_eval.sh paper_a3892396b1843698
```

2. 光铜反应选择性：

```bash
bash scripts/run_codex_gpt61_v2_eval.sh paper_db6c4e0558113873
```

3. 苄醇氧化差异：

```bash
bash scripts/run_codex_gpt61_v2_eval.sh paper_d83e607f125440cc
```

4. 微流动力学与机理可辨识性：

```bash
bash scripts/run_codex_gpt61_v2_eval.sh paper_60f4c45810428116
```

5. 激发态还原与猝灭：

```bash
bash scripts/run_codex_gpt61_v2_eval.sh paper_3e4cad1d1d650d0c
```

在命令末尾添加 `--dry-run` 仅做本地预检，不启动 Agent、Judge 或科学计算，不验证在线 API。预检会产生明确标记的预检目录。

## 恢复与结果位置

用终端打印的真实输出目录替换下面的 `paper_ID_UTC时间_随机后缀`，在原运行主机恢复：

```bash
bash scripts/run_codex_gpt61_v2_eval.sh --resume \
  workspaces/codex_gpt61_v2/paper_ID_UTC时间_随机后缀
```

需要显式修复被 API 拒绝的加密历史时，追加 `--repair-history`。该参数只适用于对应错误，不能作为通用重试选项。普通续跑保留原期限；`--timeout-seconds TOTAL_SEC` 是从首次启动算起的**总时限**，必须比旧值大且使新截止时间仍在未来。例如八天总时限为 `691200`，不是恢复后再给八天。这与 ARCHE 的 `ARCHE_EVAL_RESUME_TIMEOUT` 语义不同。

每个结果目录中的 `test_settings.json` 和 `evaluation_config.yaml` 记录模型与资源；`task_snapshot/autonomous_research/<paper_id>/` 保存冻结任务；`runs/cli_runs/batch_*/autonomous_research-*/` 下的 `_live_progress.log`、`report/report.md` 和 `_score.json` 分别记录执行、最终报告和评分。`.runtime/task_sources/<运行名>/source.json` 记录原始 final V2 来源、主机与包哈希。

## 已完成的检查

- `bash -n` 通过。
- 五题实际入口 `--dry-run` 全部为 `preflight_ready`，Agent/Judge 均为 gpt-6.1-sol/high，自动恢复开启。
- 五题原任务与运行快照全部文件的 SHA-256 一致。
- 临时隔离环境中检查了显式 resume、历史修复／时限参数传递、旧模型配置覆盖、缺失题目和歧义检查点拒绝；均通过，输出未泄露测试密钥。
- 未启动这五题的正式评估或付费 API 调用；本次产生的五个仅预检目录在核验后清理，结果保存在 `docs/handle/V2_gpt61_五题启动检查_20261024.json`。
