# 数据管线脚本

脚本只保留四类稳定入口：

```text
scripts/
├── bootstrap/                    # 建立主 Conda 环境、第三方服务和模型缓存
├── patches/                      # 第三方固定版本补丁
├── stage03_llm/                  # rlaunch worker、vLLM 网关和 MinerU 服务切换
├── workflows/run_pipeline.sh     # 完整 Stage00-07 流程入口
├── workflows/run_stage00_04_batches.sh # 分轮复制并运行 Stage00-04
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
  --total 10000 --batch-size 1000 --stage04-concurrency 8 \
  --initial-delay-hours 5
python scripts/sync_toolbox_capabilities.py
```

`run_stage00_04_batches.sh` 严格串行处理外层批次：只有当前 1000 篇完成
Stage00-04 后才复制下一批；各批次共享一个沙箱和 GPU worker，并自动排除先前已选择的论文。
默认先等待 5 小时，再申请沙箱和唯一一个 GPU worker。worker 单次启动失败时整个任务立即结束，
不会再次申请 worker。

`run_pipeline.sh` 默认读取 `config.example.json`，并在存在时加载 `config.local.env`。
默认会调用项目代理初始化脚本；设置 `RCB_SETUP_PROXY=0` 可关闭此行为。

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
