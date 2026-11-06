# Codex 原服务器停止后的跨主机恢复

`scripts/run_small_molecules_gpt61_eval.sh` 的 Codex resume 现在支持 `--migrate-from-host ORIGINAL_HOST`。该选项明确声明完整主机名所指的旧实例已经停止；不能仅因为新机器上找不到旧 PID 就推断旧机器已停止。

迁移保留原任务、会话、输入、科学结果、提交回执、累计用量和原截止时间。原主机留下的非终态单项作业，若有 job ID 与 launch token 相符的终态记录则采纳其真实结果，否则记为 `cancelled / source_host_stopped`。原计算文件保留，已成功的作业不改写；不会自动重新提交这些计算。恢复后的 Agent 根据已有记录决定是否需要续算。

迁移前校验原主机归属、执行锁、冻结公开文件、Codex 原生会话，以及 CLI 版本与路径。Codex CLI 必须匹配原任务冻结版本，不能通过改写版本记录跳过检查。默认只读迁移检查不发模型请求，也不启动作业；正式迁移会先备份执行账本，再记录迁移审计。当前入口拒绝尚未处理的活动 batch，以免猜测批次的提交与聚合语义。

跨主机允许重绑定 `PATH`、`LD_LIBRARY_PATH` 和默认主机资源池路径：用保存的环境值重建 MCP 配置，必须能匹配原始冻结哈希，才记录目标环境的新哈希。其他工具配置或科学设置的变化仍会阻止迁移。审计包含变更前后的 adapter 记录。

## paper_3c3d73b8715d5fcd（2026-10-24）

应恢复 `paper_3c3d73b8715d5fcd_20261024_075702_5eb857d4`，而非 07:57:27 创建的重复失败目录。原主机为 `lfy-54-cpu-test-1--39321836e970-6ame7agnxd`。检查时有 31 个 success、2 个 failed 和 3 个遗留 running 作业；最后日志在 08:49 UTC。原截止时间为 2026-10-28 07:57 UTC。

新服务器当前 Codex 为 0.164.0，原任务冻结的是 0.162.1。先在准备续跑的服务器安装匹配版本：

```bash
npm install -g @openai/codex@0.162.1
codex --version
```

预期输出 `codex-cli 0.162.1`。CLI 版本和模型不同；本任务继续使用原来的 gpt-6.1-sol/high。

在项目根目录恢复：

```bash
bash scripts/run_small_molecules_gpt61_eval.sh codex --resume \
  workspaces/codex_gpt61_high_small_molecules/paper_3c3d73b8715d5fcd_20261024_075702_5eb857d4 \
  --migrate-from-host lfy-54-cpu-test-1--39321836e970-6ame7agnxd
```

在命令末尾加 `--check` 仅预览迁移，不启动评估。它会检查迁移前提；正式 resume 仍会执行框架完整的任务快照和 MCP 配置校验。普通同主机续跑不需要迁移参数。

审计存放在原 run 的同级控制目录：`.rcb_recovery/<run_id>/host_migrations/<时间_标识>/`，包含迁移前 `execution.sqlite3` 和 `migration.json`。账本中同时保留 `host_migration/current` 与历史记录。原始计算文件和原生会话内容不清理。

## 验证

测试覆盖只读预览、成功结果和原生会话保留、未完成作业中断、真实终态优先、执行锁冲突、错误主机、混合主机作业、过期、取消、冻结输入变化、CLI 版本漂移、重复迁移，以及 shell 先迁移后 resume 的路由。

本次在隔离临时目录安装 0.162.1，对实际任务验证了版本／等待能力、MCP 配置哈希、冻结任务包、公开输入和原生会话兼容性。没有修改新服务器的全局 Codex 安装，没有对实际任务应用迁移，也没有启动付费模型或科学计算。
