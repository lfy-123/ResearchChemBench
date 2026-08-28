# ResearchChemBench Data Pipeline

该目录包含用于筛选和构建计算化学 benchmark 任务的数据管线。当前实现只有一套，按
Stage 00-07 组织在 `src/stages/` 中；不再保留旧版阶段、旧编排器或 `src/v2` 兼容层。

## 当前流程

| 阶段 | 职责 | 主要实现 |
|---|---|---|
| Stage 00 | 从远端选择指定数量论文，将正文和已知 SI 复制到同一论文目录 | `src/stages/stage00_remote_corpus/` |
| Stage 01 | 去重、论文/SI 归组、补齐正式 SI、GROBID 低成本解析并在失败时回退 `pdftotext` | `src/stages/stage01_document_preparation/` |
| Stage 02 | 使用 screening LLM 判断是否为纯计算化学原创研究；混合实验论文不进入下游 | `src/stages/stage02_computational_content/` |
| Stage 03 | 提取实际使用的软件和资源，按工具箱原生软件目录与资源预算筛选 | `src/stages/stage03_toolbox_resource_gate/` |
| Stage 04 | 只对 Stage03 通过论文执行 MinerU 高质量解析 | `src/stages/stage04_mineru_normalization/` |
| Stage 05 | 判断完整科研流程和 benchmark 方向适用性 | `src/stages/stage05_benchmark_suitability/` |
| Stage 06 | 独立 Agent 审查完整工作流，先构建自主科研任务，再复制增补为论文复现任务，并生成共同隐藏评分合同 | `src/stages/stage06_task_builder/` |
| Stage 07 | 在独立只读工作区执行确定性检查和 Agent 客观审计，报告数据、软件、成本、隔离与评分问题 | `src/stages/stage07_task_judge/` |

Stage01-05 采用有界微批流水线。Stage02/03 可以分别调用 OpenAI-compatible API，API-only
模式不会创建 rlaunch worker；旧配置仍可显式使用共享的部署模型。沙箱在整次任务开始前创建，
并在任务结束或异常退出时按配置停止或删除。

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
│   ├── stage03_llm/        # 可选的旧式 screening LLM / MinerU 共享 GPU worker
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
- Stage02/03 默认分别使用 `models.stage02_screening` 和 `models.stage03_screening`；如需兼容
  旧式部署方式，可将两者的 `model_role` 改回 `screening`。
- Stage05 使用 `stage05_router` 做高召回证据路由，再由 `suitability` 审核候选；Stage06、07
  分别使用 `builder`、`judge` 模型配置，并通过 `harness` 选择 `codex`、`claude` 或
  `opencode`。默认使用 `codex`；`direct_api` 仅用于旧配置兼容。
- Stage06/07 Agent 只读取冻结的化学工具箱能力快照，不修改工具箱。工具箱暂缺会进入
  `toolbox_requirements.json` 和 Stage07 `needs_software` outcome，不会让 Stage06 自动淘汰论文。
- Stage06/07 每个 phase 使用独立工作区和输入指纹 checkpoint。模型/API 波动时可逐 phase
  重试与 resume；正式任务只在全部校验通过后原子提交。
- `models.screening.existing_worker` 可填写一个已运行 worker 的完整 SSH 地址。此时管理脚本
  跳过 `rlaunch`，只部署/切换 Qwen 与 MinerU；流水线退出时不会停止该外部 worker。
- `models.screening.preserve_worker_on_exit` 只供外层批处理控制器使用。启用后各轮复用同一个
  managed worker，并由外层控制器在全部轮次完成或异常退出时统一释放。
- `models.screening.allow_worker_creation=false` 要求复用已经存在且健康的 managed worker；
  worker 缺失或失效时直接失败，不会自动申请替代 worker。
- `stop_after` 可设置为 `stage00` 至 `stage07`。
- `microbatch.stage_concurrency` 分别限制 Stage01-05 的在途微批数量。

## 验证

```bash
PYTHONPATH="$PWD" .envs/researchchem-data-pipeline/bin/python -m pytest -q tests
.envs/researchchem-data-pipeline/bin/ruff check src tests scripts
```
