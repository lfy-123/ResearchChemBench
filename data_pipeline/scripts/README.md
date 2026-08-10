# 数据管线脚本

脚本只保留四类稳定入口：

```text
scripts/
├── bootstrap/                    # 建立主 Conda 环境、第三方服务和模型缓存
├── patches/                      # 第三方固定版本补丁
├── stage03_llm/                  # rlaunch worker、vLLM 网关和 MinerU 服务切换
├── workflows/run_pipeline.sh     # 完整 Stage00-07 流程入口
├── sync_toolbox_capabilities.py  # 刷新只读工具箱能力快照
└── test_publisher_access.sh      # 诊断出版商网页连通性
```

不为单独阶段维护 shell 包装器。通过配置中的 `stop_after` 控制结束阶段，通过
`microbatch` 和 `microbatch.stage_concurrency` 控制并发。

常用命令：

```bash
bash scripts/bootstrap/bootstrap_all.sh
bash scripts/workflows/run_pipeline.sh /absolute/path/to/config.local.json
python scripts/sync_toolbox_capabilities.py
```

`run_pipeline.sh` 默认读取 `config.example.json`，并在存在时加载 `config.local.env`。
默认会调用项目代理初始化脚本；设置 `RCB_SETUP_PROXY=0` 可关闭此行为。
