# 小分子 V3 最新运行监控

在 ResearchChemBench 根目录查看一次：

```bash
python3 scripts/results/check_small_molecules_status.py
```

每 60 秒刷新，按 Ctrl+C 退出：

```bash
python3 scripts/results/check_small_molecules_status.py --watch 60
```

默认覆盖 `tasks/small_molecules_verified_autonomous_research` 顶层的14个任务，以及 ARCHE/Codex 两类智能体。每个任务、每类智能体只选择 `workspaces/{arche,codex}_gpt61_high_small_molecules_v3/` 中启动时间最新的结果目录；旧版本结果不计入。按目录名中的启动时间排序，不按日志更新时间排序；最新运行失败或未完成时，也不会退回显示旧运行的评分。

显示运行服务器、执行状态、评分、调查完成数和最近记录更新时间。`--details` 显示完整主机名、结果路径、模型调用次数和诊断信息；`--agent arche` 或 `--agent codex` 只查看其中一类；`--json` 输出一次结构化结果。目录可通过 `--tasks-root`、`--workspaces` 指定。

远端进程仅能根据共享文件显示为“远端记录，未验活”；在对应服务器上执行才能检查保存的本机进程身份。运行结束和评分完成分别显示，0分也算已评分。脚本只读，不联网、不调用模型、不停止或恢复任务。

回归检查：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts/results -p 'test_check*.py' -v
```
