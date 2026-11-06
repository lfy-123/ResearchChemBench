# 本地 CPU 查看与进程清理

在 ResearchChemBench 根目录运行。只需 Linux `/proc` 和系统 Python 3；终止功能需要 Python >=3.9 及内核 pidfd 支持。

## 查看资源

```bash
# 默认只查看；采样 1 秒，显示 CPU、内存和占用最高的 20 个进程
bash scripts/clear/server_jobs.sh

# 显示更多进程及工作目录，便于确定属于哪个任务
bash scripts/clear/server_jobs.sh status --top 40 --paths

# 按命令/工作目录筛选项目进程；不携带项目路径的子进程可能不在列表中
bash scripts/clear/server_jobs.sh status --project-only --top 40 --paths

# 每 3 秒刷新一次；Ctrl+C 退出查看
watch -n 3 bash scripts/clear/server_jobs.sh status --top 20
```

进程 `CPU%=100` 表示约占用一个核，多线程进程可超过 100%。系统负载是排队/运行任务的指标，不是 CPU 使用率。脚本同时显示亲和性允许 CPU 的采样使用率；如可读取 cgroup v2，则显示当前组的 CPU 使用量、CPU 配额和内存上限。本级配额还可能受上级 cgroup 或调度器限制，不能简单把宿主可见内存视为当前容器可用内存。

## 终止指定作业

将示例中的 `12345` 换成查看结果中确认的作业主进程 PID。仅选中一个 ORCA 子进程可能导致上层 Agent 继续提交计算；想停止整项评估时，先使用原有评估取消入口，或明确选择评估主进程。

```bash
# 预览这个 PID 及其子孙进程，不发送任何信号
bash scripts/clear/server_jobs.sh stop --pid 12345

# 正常终止，先发送 SIGTERM，等待最多 10 秒
bash scripts/clear/server_jobs.sh stop --pid 12345 --yes

# 强制清理：SIGTERM 后等待 10 秒，对残留进程发送 SIGKILL
bash scripts/clear/server_jobs.sh stop --pid 12345 --yes --force

# 同时指定多个作业；改为等待 3 秒后强制清理
bash scripts/clear/server_jobs.sh stop --pid 12345 23456 --yes --force --grace 3
```

`--force` 单独使用仍然只是预览；只有 `--yes` 才真正执行。`--grace 0` 会不等待便升级为强制终止。脚本拒绝终止 PID 1、当前终端祖先进程和其他 UID 的进程，并使用 pidfd 与进程启动时间避免 PID 重用误杀。root 账号下仍可能有不同任务都属于 root，必须自行确认 PID。

脚本只处理当前节点可见、被选中的进程树，等待期间会补查其新子进程；无法保证捕获已脱离进程树的守护进程、其他节点作业或由外部管理器重新启动的作业。处于内核不可中断 I/O（D 状态）的进程可能在 SIGKILL 后仍需等待 I/O 返回。

## 正在运行的 ARCHE 评估

对完整评估优先使用其原有取消命令，让框架有机会写入状态并取消计算；将路径换成对应的任务结果目录：

```bash
bash scripts/run_arche_gpt56_eval.sh --cancel --run-dir /绝对路径/到/对应的paper_任务目录
```

进程强杀用于残留或无法退出的作业，不修改 benchmark 元数据，也不保证强杀点可以无损 resume。清理脚本不会删除任何结果文件、工作目录或缓存，也不会按 `python`、`orca`、`qemu` 等名字批量误杀进程。
