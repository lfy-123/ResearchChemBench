# Codex 评估脚本

入口为 `scripts/codex/test_codex_gpt56.sh`，支持一次指定多篇论文和一种评估模式。按命令中的论文顺序逐个执行 Agent 和 Judge，前一篇退出后才启动下一篇。带 `--resume` 时自动定位各篇最近一次运行；没有历史运行才创建独立输出目录。单篇恢复、运行或评分失败后继续后续论文，命令最终返回非零状态；手动中断会停止后续任务。启动前统一检查需要新建的任务包，预检失败则不会开始评估。

它是 `scripts/test_codex_gpt56.sh` 的副本，已调整仓库根目录定位；原脚本仍可使用。原来的 `scripts/codex/run_evaluations.sh` 只有参数转发作用，已移除。

## 直接运行

以下示例从仓库根目录执行。脚本为前台运行，长任务建议在 `tmux` 会话中启动。

```bash
cd /inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench

# 单篇自主科研评估
bash scripts/codex/test_codex_gpt56.sh --resume paper_2f2aa11ea61a32bb

# 多篇自主科研评估，依次完成
bash scripts/codex/test_codex_gpt56.sh --mode autonomous_research --resume \
  paper_2f2aa11ea61a32bb paper_60f4c45810428116

# 多篇论文复现评估
bash scripts/codex/test_codex_gpt56.sh --mode paper_reproduction --resume \
  paper_2f2aa11ea61a32bb paper_60f4c45810428116
```

选择其中一条启动命令执行即可；增加任务时，在末尾继续添加论文 ID。同一命令中的论文使用相同模式，不允许重复 ID。

| `--mode` | 任务来源，相对仓库根目录 |
| --- | --- |
| `autonomous_research`（默认） | `tasks/final_verified_autonomous_research/<paper_id>/` |
| `paper_reproduction` | `tasks/final_verified_paper_reproduction/<paper_id>/` |

新建评估时，指定模式下必须存在对应的最终验证任务包；不会使用 `hold` 或其他任务目录作为替代。恢复历史运行时使用其冻结的任务快照，不要求当前发布目录仍保留相同任务。

## 配置与常用参数

脚本自动读取仓库根目录的 `config.local.env`，直接使用已有配置即可，不需要新建配置文件。

| 配置变量 | 用途 |
| --- | --- |
| `RCB_CODEX_API_KEY` | API 密钥，真实运行必填 |
| `RCB_CODEX_BASE_URL` | API 地址；仅填写域名或 IP 及端口时会补上 `/v1` |
| `RCB_CODEX_MODEL` | Agent 和 Judge 的模型，默认 `gpt-5.6-sol` |
| `RCB_CODEX_REASONING_EFFORT` | 推理强度，默认 `high` |

需要另选配置文件时，设置 `RESEARCHCHEMBENCH_LOCAL_CONFIG=/绝对路径/配置.env`。配置文件内的赋值优先于启动前已有的同名环境变量。框架默认使用 `.envs/researchchembench/bin/python`，无需手动激活环境。

| 参数 | 默认值或行为 |
| --- | --- |
| `--timeout-seconds` | 每篇 Agent 总墙钟预算 `345600` 秒，即 96 小时 |
| `--job-timeout-seconds` | 单个工具作业 `86400` 秒，即 24 小时；同时受任务总截止时间约束 |
| `--cpu-cores` | 每篇可用 CPU 核数 `48` |
| `--memory-mb` | 每篇可用内存 `204800` MiB，即 200 GiB |
| `--max-tokens` | 默认不设总 token 上限；指定后累计各次尝试上报的输入、输出 token |
| `--output-dir` | 强制新建，绕过自动查找历史运行；单篇时指定新提交目录，多篇时指定新父目录。必须尚不存在，相对路径以仓库根目录为基准 |
| `--no-score` | 跳过 Judge 评分 |
| `--dry-run` | 新任务准备配置和任务快照并校验；自动选中旧运行时只预览目标。均不启动 Agent、计算工具或 Judge，不验证 API 连通性 |
| `--resume` | 按论文 ID 自动恢复最近一次运行；没有历史运行则新建并启用有次数和等待预算限制的自动恢复 |
| `--no-resume` | 新建运行，保存检查点，但基础设施故障后停止，不自动恢复；不带这两个参数时也新建运行 |

入口还设置每篇最多 600 个已完成的模型轮次，这与工具调用次数不同。多篇评估共享上述参数，但分别计算资源预算和用量；任务按顺序执行。

仅检查任务包，例如：

```bash
bash scripts/codex/test_codex_gpt56.sh --mode autonomous_research \
  paper_2f2aa11ea61a32bb paper_60f4c45810428116 --dry-run

bash scripts/codex/test_codex_gpt56.sh --help
```

新任务的 `--dry-run` 会创建独立的新提交目录。`--resume --dry-run PAPER_ID` 找到旧运行时只输出选中的目录、运行 ID 和已记录状态，不改写旧文件。它仅验证选择结果，不代表服务器、进程、环境和会话已通过实际恢复校验。

## 恢复已有任务

从 2026-09-28 起，**`--resume PAPER_ID` 自动查找 `workspaces/codex_gpt56` 下该论文、该评估模式的最近一次 Codex 运行**，无需填写原工作目录或 `run_id`。它读取各提交目录的 `runs/cli_runs/batch_*/<run_id>/_meta.json`，按原始启动时间排序，不按会被日志更新改变的文件修改时间排序。只有预检、尚未创建真实运行的目录不算历史运行。

```bash
bash scripts/codex/test_codex_gpt56.sh --mode autonomous_research --resume \
  paper_35a6749f3bae345b paper_8d8940710de08f7f

# 只查看会选择哪一条运行
bash scripts/codex/test_codex_gpt56.sh --mode autonomous_research --resume --dry-run \
  paper_35a6749f3bae345b paper_8d8940710de08f7f
```

| 最近一次运行的情况 | 行为 |
| --- | --- |
| 没有历史运行 | 新建并启用自动恢复 |
| 已完成且最新评分已成功 | 跳过，保留评分，不重新调用 Agent 或 Judge |
| Agent 已完成、评分未完成 | 交给原恢复流程处理评分，不重跑计算 |
| 暂停或中断 | 交给原恢复流程，保留原目录、会话和计算记录 |
| 进程仍在运行、服务器不匹配、环境或历史会话校验失败 | 按原规则阻止恢复；不回退到更早运行，也不自动新建重算 |
| 历史元数据损坏或最新时间有多个候选 | 报错，要求明确指定旧运行 |

批量命令会在轮到每篇时重新查找，避免排队期间仍使用过时的目标。查找不按“可恢复”“未完成”筛选：最新运行即使已经完成、正在运行或不可恢复，也不会自动改选更早的目录。单独一个 `--resume` 仍需提供论文 ID，不能推断要恢复哪篇。

需要恢复更早的某一轮，或恢复默认查找范围之外的自定义目录时，仍可明确指定：

```bash
bash scripts/codex/test_codex_gpt56.sh --resume \
  --run-root "/原任务完整工作目录" \
  --run-id "原run_id"
```

这里的工作目录是包含 `_meta.json` 的那一层，目录名就是 `run_id`，也可在 `_meta.json` 中查看。一次恢复一条原运行，保留原目录、会话和已提交作业；Agent 已结束而评分未完成时，继续评分环节。不要为恢复指定 `--output-dir`。

恢复默认沿用原任务预算和资源。自动查找模式下，显式传入与原预算相同的 `--timeout-seconds` 视为沿用，不重置截止时间。若需要延长，数值必须大于原总预算，并使新截止时间晚于当前时间。显式 `--run-root --run-id` 模式保留原语义：传入的时限必须是有效延长，不能重复传相同数值。

预算从原始启动时刻计算，包含暂停时间，并非恢复后重新计时。延长预算要求作业管理器空闲、没有活跃作业；不能同时更改 CPU、内存、单作业时限或 token 预算。自动定位只省去目录和 ID 参数，不绕过原服务器、冻结环境、运行锁和会话校验。

## 输出和进展

单篇和批量运行均按论文分别保存到 `workspaces/codex_gpt56/<paper_id>_<UTC日期>_<时间>_<随机后缀>/`。例如，一次运行两篇会生成两个同级目录：

```text
workspaces/codex_gpt56/
├── paper_2f0a4f80a37fbccd_20260920_120000_a1b2c3/
└── paper_2f2aa11ea61a32bb_20260920_140000_d4e5f6/
```

每篇目录包含自己的配置、任务快照、计算文件和评分结果。不带 `--resume` 或显式指定新的 `--output-dir` 会创建新目录；自动或显式恢复已有任务时继续使用原目录。

| 位置，相对提交目录 | 内容 |
| --- | --- |
| `submission.json`、`evaluation_config.yaml`、`test_settings.json` | 提交状态、运行配置和设置 |
| `task_snapshot/` | 本次评估使用的任务包快照 |
| `runs/cli_runs/batch_*/eval_report.json`、`results.json` | 批次评估报告和汇总 |
| `runs/cli_runs/batch_*/<run_id>/_meta.json` | 原运行 ID、状态和元数据 |
| `runs/cli_runs/batch_*/<run_id>/_live_progress.log` | Agent 和工具的实时进展 |
| `runs/cli_runs/batch_*/<run_id>/_score.json` | 评分结果，评分成功后生成 |
| `runs/cli_runs/batch_*/<run_id>/report/results.json` | Agent 提交的结构化科研结果，需 Agent 实际产出 |

计算输入、原始输出、中间文件和报告保留在各自的原运行目录中。需要恢复或后续复评时，应保留整个提交目录及其中的隐藏目录。

查看某条运行的日志：

```bash
tail -f "/原任务完整工作目录/_live_progress.log"
```

## Judge 恢复控制

新任务可使用 `--resume --retry-in-doubt`，显式允许 Judge 超时后有限恢复。歧义请求默认最多自动重试一次，同时受总请求和等待预算限制；策略和次数保存在原运行中，普通 resume 不重置次数。恢复已有运行时也可以显式指定 `--retry-in-doubt`，对原账本进行一次手动重试。可能重复计费，旧请求与未知用量仍保留；默认不重发此类请求，`--no-resume` 禁用自动重试。

`JUDGE_TIMEOUT_SECONDS`（默认 600）控制 Judge 客户端的网络超时；这是传输超时，不是严格的总墙钟时限。已完成计算的评分恢复不启动计算。
