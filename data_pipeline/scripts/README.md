# 数据管线脚本目录

本目录按用途组织脚本。根目录保留一个历史名称兼容入口，用于指定数量远端论文的
Stage 00-06 shadow run。

```text
scripts/
├── run_stage_01_04_batches.py       # 兼容名：远端正文/SI 分组并运行 Stage 00-06
├── run_stage_01_04_batches.sh       # 上述任务的一键入口，默认 1000 篇
├── workflows/                       # 可复用运行流程
│   ├── run_pipeline.sh              # 完整数据管线
│   └── run_stage_01_04_screening.sh # 旧 Stage 01-04 结果复现入口
├── bootstrap/                       # 环境、服务和模型缓存准备
├── xinghe_dataset/                  # Xinghe 数据集只读访问与可恢复下载
└── patches/                         # 固定第三方版本所需补丁
```

不再为每个阶段分别维护 shell 脚本。需要停在某个阶段时，直接在配置中设置
`stop_after`；需要固定组合流程时，再在 `workflows/` 中提供稳定入口。

常用命令：

```bash
# 准备全部运行依赖
bash scripts/bootstrap/bootstrap_all.sh

# 执行完整管线
bash scripts/workflows/run_pipeline.sh

# 仅执行 Stage 01-04（需要传入 stop_after=resource_limits 的配置）
bash scripts/workflows/run_stage_01_04_screening.sh --config CONFIG

# 1000 篇正文及其 SI，单个 128 CPU/256 GiB 沙箱，停止在 Stage 06
bash scripts/run_stage_01_04_batches.sh

# 只查看计划，不创建沙箱或访问远端
bash scripts/run_stage_01_04_batches.sh --plan-only

# 小规模真实冒烟
bash scripts/run_stage_01_04_batches.sh --count 2
```
