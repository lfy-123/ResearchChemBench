# 数据管线脚本目录

本目录按用途组织脚本，根目录只保留不能复用的“一万篇分批筛选”特例入口。

```text
scripts/
├── run_stage_01_04_batches.py       # 特例：下载 10 批并依次执行四阶段筛选
├── run_stage_01_04_batches.sh       # 上述特例的一键入口
├── workflows/                       # 可复用运行流程
│   ├── run_pipeline.sh              # 完整数据管线
│   └── run_stage_01_04_screening.sh # 固定的 Stage 01-04 筛选流程
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

# 一万篇分批任务
bash scripts/run_stage_01_04_batches.sh

# 每轮1000篇，内部每10篇一个微批次，最多5批并行，自动创建5个Softcite实例
bash scripts/run_stage_01_04_batches.sh \
  --microbatch --microbatch-size 10 --microbatch-concurrency 5
```
