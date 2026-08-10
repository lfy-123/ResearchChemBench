# ResearchChemBench Data Pipeline

该目录包含用于筛选和构建计算化学 benchmark 任务的数据管线。当前实现只有一套，按
Stage 00-07 组织在 `src/stages/` 中；不再保留旧版阶段、旧编排器或 `src/v2` 兼容层。

## 当前流程

| 阶段 | 职责 | 主要实现 |
|---|---|---|
| Stage 00 | 从远端选择指定数量论文，将正文和已知 SI 复制到同一论文目录 | `src/stages/stage00_remote_corpus/` |
| Stage 01 | 去重、论文/SI 归组、补齐正式 SI、GROBID 低成本解析并在失败时回退 `pdftotext` | `src/stages/stage01_document_preparation/` |
| Stage 02 | 使用 screening LLM 判断是否包含目标计算化学科研流程 | `src/stages/stage02_computational_content/` |
| Stage 03 | 提取实际使用的软件和资源，按工具箱原生软件目录与资源预算筛选 | `src/stages/stage03_toolbox_resource_gate/` |
| Stage 04 | 只对 Stage03 通过论文执行 MinerU 高质量解析 | `src/stages/stage04_mineru_normalization/` |
| Stage 05 | 判断完整科研流程和 benchmark 方向适用性 | `src/stages/stage05_benchmark_suitability/` |
| Stage 06 | 构建自主科研与论文复现两种任务 | `src/stages/stage06_task_builder/` |
| Stage 07 | 确定性检查、独立 Judge 和可选 Gold Run | `src/stages/stage07_task_judge/` |

Stage01-05 采用有界微批流水线。Stage02/03 共用一次部署的 screening LLM；当 Stage03
全部结束后，同一个 GPU worker 可以切换为 MinerU 服务。沙箱在整次任务开始前创建，并在
任务结束或异常退出时按配置停止或删除。

每篇论文的来源、各阶段判定、证据和删除状态统一记录在 SQLite registry，并导出 JSONL。
Stage00-03 未通过论文可以在记录落盘后删除其 Stage00 论文目录；Stage04-07 不删除原始论文。

更详细的数据流见 [PIPELINE_ARCHITECTURE.md](docs/PIPELINE_ARCHITECTURE.md)。模型职责和
输出约束见 [LLM_PROMPTS_AND_SCHEMAS.md](docs/LLM_PROMPTS_AND_SCHEMAS.md)。

## 目录

```text
data_pipeline/
├── assets/                 # 工具箱快照、软件别名和计算方法规则
├── docs/                   # 当前架构与维护记录
├── scripts/
│   ├── bootstrap/          # 环境、第三方服务和模型缓存准备
│   ├── patches/            # 固定第三方版本所需补丁
│   ├── stage03_llm/        # screening LLM / MinerU 共享 GPU worker
│   └── workflows/          # 一键运行入口
├── src/
│   ├── core/               # 通用并发、IO 和日志
│   ├── integrations/       # GROBID、MinerU、Softcite、远端存储和 LLM
│   ├── registry/           # 全量论文筛选记录
│   ├── sandbox/            # OpenSandbox 生命周期管理
│   └── stages/             # 唯一的 Stage00-07 业务实现
├── tests/
├── config.example.json
└── environment.yml
```

本地运行数据不进入 Git：`.envs/`、`.model_cache/`、`datasets/`、`runs/`、`registry/`、
本地配置和 worker 状态均由 `.gitignore` 排除。

## 运行

环境和第三方组件统一安装到主环境：

```bash
cd data_pipeline
bash scripts/bootstrap/bootstrap_all.sh
cp config.local.env.example config.local.env
```

编辑本地环境变量和基于 `config.example.json` 创建的本地 JSON 配置，然后运行：

```bash
bash scripts/workflows/run_pipeline.sh /absolute/path/to/config.local.json
```

也可直接使用 CLI：

```bash
.envs/researchchem-data-pipeline/bin/python -m src.cli run \
  --config config.local.json \
  --stop-after stage05
```

沙箱模式可在配置中设置 `execution.backend=sandbox`，或传入 `--sandbox`。Stage00 单独准备：

```bash
.envs/researchchem-data-pipeline/bin/python -m src.cli prepare-remote-corpus \
  --count 1000 \
  --output runs/corpus-1000
```

## 配置原则

- `config.example.json` 只提供结构和非敏感默认值；密钥放在 `config.local.env`。
- 工具箱范围以 `assets/toolbox_capabilities.json` 为准，通过
  `scripts/sync_toolbox_capabilities.py` 从当前工具箱刷新。
- Stage02/03 固定使用 `models.screening`；Stage05、06、07 分别使用 `suitability`、
  `builder`、`judge` 模型配置。
- `stop_after` 可设置为 `stage00` 至 `stage07`。
- `microbatch.stage_concurrency` 分别限制 Stage01-05 的在途微批数量。

## 验证

```bash
PYTHONPATH="$PWD" .envs/researchchem-data-pipeline/bin/python -m pytest -q tests
.envs/researchchem-data-pipeline/bin/ruff check src tests scripts
```
