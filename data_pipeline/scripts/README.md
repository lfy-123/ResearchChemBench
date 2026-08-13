# 数据管线脚本

脚本只保留四类稳定入口：

```text
scripts/
├── bootstrap/                    # 建立主 Conda 环境、第三方服务和模型缓存
├── patches/                      # 第三方固定版本补丁
├── stage03_llm/                  # rlaunch worker、vLLM 网关和 MinerU 服务切换
├── WORKER_LAUNCH_GUIDE.md        # worker 资源、创建和复用规范
├── workflows/run_pipeline.sh     # 完整 Stage00-07 流程入口
├── workflows/run_stage00_04_batches.sh # 分轮复制并运行 Stage00-04
├── workflows/run_stage04_05_resume.py  # 从已完成 Stage03 的运行目录恢复 Stage04-05
├── run_stage04_05_resume.sh            # Stage04-05 恢复入口
├── sync_toolbox_capabilities.py  # 刷新只读工具箱能力快照
└── test_publisher_access.sh      # 诊断出版商网页连通性
```

不为单独阶段维护 shell 包装器。通过配置中的 `stop_after` 控制结束阶段，通过
`microbatch` 和 `microbatch.stage_concurrency` 控制并发。

常用命令：

```bash
bash scripts/bootstrap/bootstrap_all.sh
bash scripts/workflows/run_pipeline.sh /absolute/path/to/config.local.json
bash scripts/workflows/run_stage00_04_batches.sh \
  --run-root runs/stage00-04-batches-10000 \
  --total 10000 --batch-size 1000 --stage04-api-concurrency 8 \
  --stage04-microbatch-concurrency 1 --worker-memory-mib 160000 \
  --initial-delay-hours 5
python scripts/sync_toolbox_capabilities.py
```

`run_stage00_04_batches.sh` 严格串行处理外层批次：只有当前 1000 篇完成
Stage00-04 后才复制下一批；各批次共享一个沙箱和 GPU worker，并自动排除先前已选择的论文。
默认先等待 5 小时，再申请沙箱和唯一一个 GPU worker。worker 单次启动失败时整个任务立即结束，
不会再次申请 worker。
批处理沙箱默认申请 64 CPU/128 GiB；可通过 `--sandbox-cpu` 和 `--sandbox-memory` 显式覆盖。
脚本先等待沙箱进入 Running，再创建 GPU worker，避免 OpenSandbox 排队时提前占用 GPU。沙箱默认
最多等待 14400 秒，可通过 `--sandbox-startup-timeout-seconds` 调整。未传 `--existing-worker` 时，
脚本只调用一次 rlaunch 自动创建 worker；创建或服务启动失败时任务立即结束。

worker 启动命令和资源约束见 [WORKER_LAUNCH_GUIDE.md](WORKER_LAUNCH_GUIDE.md)。

`run_pipeline.sh` 默认读取 `config.example.json`，并在存在时加载 `config.local.env`。
默认会调用项目代理初始化脚本；设置 `RCB_SETUP_PROXY=0` 可关闭此行为。

API-only 批处理可用 `--stop-after stage03` 暂停在 MinerU 之前。Stage02、Stage03 和
Stage05 的模型角色都支持 `models.<role>.fallback_models` 有序候选列表：单个模型完成自身重试后
仍发生连接、HTTP、超时或无效 JSON 错误，才切换到下一模型；正常返回的科学筛选结论不会触发
切换。每次切换都会记录在 LLM cache 的 `model_failures`、`fallback_used` 和
`fallback_index` 字段中。

从已完成 Stage03 的运行目录继续处理：

```bash
bash scripts/run_stage04_05_resume.sh \
  --run-root runs/stage00-05-api-batches-10000-20260813 \
  --mineru-sandbox-count 4 \
  --mineru-sandbox-cpu 64 --mineru-sandbox-memory 160Gi \
  --stage04-microbatch-concurrency 4 --watch
```

该入口不会重新执行 Stage00-03。它只消费已经存在且 `stage_cache.json` 为
`completed` 的微批次，按 Stage04 -> Stage05 顺序处理；再次启动会自动跳过两阶段都已完成的
微批次。`--start-stage`/`--stop-stage` 可选 `4` 或 `5`，例如只重跑 Stage04 使用
`--start-stage 4 --stop-stage 4`。`--mineru-sandbox-count` 是显式的多沙箱开关，默认值为
1，保持旧版单沙箱行为。每个沙箱同一时刻只运行一个 MinerU job，池内不同沙箱并行领取任务。
脚本结束时默认停止这些沙箱；调试时可传 `--mineru-sandbox-cleanup keep`。

复用已经运行的 GPU worker：

```bash
bash scripts/stage03_llm/manage_rlaunch_worker.sh start \
  --state .screening_llm_worker.local.json \
  --existing-worker '<完整 SSH 地址>' \
  --skip-bootstrap \
  --skip-download
```

也可以把相同地址写入 `models.screening.existing_worker`，由流水线自动执行以上过程。
外部 worker 会在状态文件中标为 `external`；`stop` 只关闭数据管线服务和 SSH 隧道，
不会停止外部 worker。省略 `--existing-worker` 时仍由脚本创建并管理 rlaunch worker。
