# Stage00-05 Resume 实现记录

日期：2026-08-13
依据：`STAGE00_05_RESUME_DESIGN_20260813.md`

## 已实现范围

- `run_root/resume/resume_state.sqlite` 保存永久选样账本、论文/文档 work item、不可变
  attempt、artifact manifest、运行 generation 和 lease。
- Stage00 使用整个 `run_root` 的 URI/DOI 账本去重；累计 `--total` 增大时冻结旧批次，
  只追加新目标槽位和新批次。Stage00-03 淘汰后即使源文件已删除，历史 URI 仍不会重选。
- Stage01 按论文包和文档恢复；Stage02/03 按论文恢复；Stage04 按 MinerU 文档恢复；
  Stage05 分别 checkpoint Router、Auditor 原始响应和最终确定性合同结论。
- 正常科学拒绝与正常 uncertain 直接复用；Stage02-05 的 API、MinerU、沙箱等客观失败以及
  从未开始的任务重新入队。上游未通过时，下游状态为 `blocked_by_upstream`。
- Stage01 是例外的文档完整性终止门：任何未通过结果（包括解析失败、pending、retryable 和
  uncertain）先写入 registry，再删除正文/SI 和 Stage01 下载附件并标为 `pruned_terminal`。
  Stage02/03 的客观失败、pending、running 和 blocked 仍禁止删除原始资产。
- 同一 `run_root` 使用 OS 文件锁加 SQLite 心跳 lease，下一次恢复会把陈旧 running
  转为 `retryable_failed/interrupted_external`。
- 旧 JSONL 首次迁移使用带版本的完成标记；后续启动不再反复扫描同一批次，迁移中断时
  不写完成标记，因此可安全重试。
- 普通恢复使用冻结的科学配置和当前运行端点；科学配置变化必须显式
  `--invalidate-stage`，且失效会传播到下游。指定 `--batch` 时只失效所选批次。
- Stage06/07 未接入本机制，继续按 `../stage0607/STAGE06_07_RESUME_DESIGN_20260813.md`
  在 Agent 重构后实现候选级恢复。

## 命令

只生成计划，不创建沙箱、不调用 API，也不提前创建扩容批次：

```bash
bash scripts/resume_pipeline.sh \
  --run-root runs/stage00-05-api-batches-10000-20260813 \
  --total 10000 --start-stage stage00 --stop-stage stage05 --dry-run
```

执行计划：

```bash
bash scripts/resume_pipeline.sh \
  --run-root runs/stage00-05-api-batches-10000-20260813 \
  --total 10000 --start-stage stage00 --stop-stage stage05
```

只重试客观失败，不执行 never-started：

```bash
bash scripts/resume_pipeline.sh \
  --run-root runs/stage00-05-api-batches-10000-20260813 \
  --total 10000 --batch 2 --retry-only
```

累计扩容到 20,000 篇：

```bash
bash scripts/resume_pipeline.sh \
  --run-root runs/stage00-05-api-batches-10000-20260813 \
  --total 20000 --batch-size 1000
```

## 落盘产物

```text
run_root/resume/
├── resume_state.sqlite
├── config_snapshots/batch-XXXX.json
├── runtime_configs/generation-XXXX/batch-XXXX.json
├── migration_report.json
├── resume_plan.json
├── resume_summary.json
├── selection_ledger.jsonl
├── attempts.jsonl
└── unresolved.jsonl
```

原始 `config.snapshot.json` 不会被恢复调用覆盖；每个恢复 generation 的实际运行配置写到
批次下的 `resume_attempts/generation-XXXX/config.snapshot.json`。

## 验证

- 数据管线完整测试：342 passed。
- 独立 CLI `--dry-run`：从累计 2 规划到 4，仅报告 `batch-0002`，没有创建该配置、
  sandbox 管理文件或外部资源。
- 真实旧 Batch01 临时迁移：导入 1000 个永久选择身份，SQLite `integrity_check=ok`；
  能区分正常拒绝、客观失败、未开始和上游阻塞。演练只使用符号链接读取原产物，临时
  约 153 MiB 状态目录已删除，生产运行目录未写入。
- Stage05 离线 checkpoint 测试确认：Router/Auditor 响应已保存时，最终合同校验可恢复，
  且两类模型 API 调用次数均为零。
