# v2.1 阶段重排与共享 GPU worker 实现记录

日期：2026-08-09
范围：Stage 01-05 的阶段边界、微批次调度、Qwen -> MinerU 服务切换，以及旧 2000 篇运行结果的迁移审计。

## 1. 目标与不变项

本次修改落实以下约束：

- Stage 01 同时负责论文包闭合（正文、已有 SI、缺失 SI 的发现/下载/确认）和低成本文本标准化；
- Stage 02 只做计算化学内容筛选；
- Stage 03 只做软件覆盖与资源预筛，不再在此阶段运行 MinerU；
- Stage 04 只对 Stage 03 通过论文做 MinerU 深度标准化；
- Stage 05、06、07 的科学任务适用性、Builder 和 Judge 合同保持原 v2 语义；
- 原有 strict/shadow 判定规则没有因为改阶段编号而放宽，旧运行目录不原地改写；
- Stage 02 和 Stage 03 共用同一个 screening LLM worker，Stage 04 在同一个 rlaunch worker 上切换为 MinerU API。

## 2. 新旧阶段映射

| 旧阶段/产物 | 新阶段 | 处理内容 | 新输出目录 |
| --- | --- | --- | --- |
| Stage 00 | Stage 00 | 远端复制、批次选择、正文/SI 目录整理 | `stage_00_remote_corpus` |
| Stage 01 inventory + Stage 04 SI acquisition | Stage 01 package 子步骤 | 去重、paper grouping、SI 发现/下载/确认、完整性审计 | `stage_01_document_preparation/package` |
| Stage 02 parsing + Stage 06 SI extraction | Stage 01 normalization 子步骤 | GROBID-first；失败或质量不达标回退 `pdftotext`；正文和全部已知 SI 参与 | `stage_01_document_preparation/raw`、`documents.jsonl` |
| 旧 Stage 03 | Stage 02 | 原创、纯计算、计算为主、作者实验归属的 map/reduce 审查 | `stage_02_computational_content` |
| 旧 Stage 05 + resource gate | Stage 03 | 规则/Softcite/LLM 软件清单、三层工具箱映射、资源预筛 | `stage_03_toolbox_resource_gate` |
| 旧 Stage 04 MinerU 子步骤 | Stage 04 | 通过 Stage 03 的正文和 PDF SI 的高质量解析 | `stage_04_mineru_deep_normalization` |
| 旧 Stage 05 suitability | Stage 05 | 十类科学任务和完整科研闭环适用性 | `stage_05_benchmark_suitability` |
| Builder/Judge | Stage 06/07 | 任务构建、独立审核、Gold Run | 原有 v2 Stage06/07 目录 |

`data_pipeline/src/v2/config.py` 会识别旧 v2 配置并一次性转换上述字段；显式设置
`"stage_layout": "v2.1-split-normalization"` 的配置不会再次迁移。配置迁移只改变路由和文件路径，
不会把旧科学判定自动当作新判定。

## 3. 调度与服务生命周期

### 3.1 两个全局 phase

为了避免 Qwen 和 MinerU 同时争抢同一张 GPU，编排器采用一个全局屏障：

```text
phase 1: 所有微批次各自 Stage01 -> Stage02 -> Stage03
          （Stage02/03 可按 stage_concurrency 并发）
          ↓ 全部 Stage03 完成
phase 2: 每个微批次 Stage04 -> Stage05
          （Stage04 完成一个微批次后，该批可立即进入 Stage05）
          ↓
Stage06 -> Stage07
```

因此 Stage 04 不会在另一个批次仍运行 Qwen Stage 03 时启动 MinerU。phase 2 内部仍是微批次流水，
不是等待所有 MinerU 完成后才开始 Stage 05。每个阶段有独立 `BoundedSemaphore`，由
`microbatch.stage_concurrency` 控制；`microbatch.concurrency` 是总体 worker 数上限。

### 3.2 同一个 rlaunch worker 的状态机

当 `models.screening.managed_rlaunch=true` 且 `stage04.mineru.managed_gpu=true` 时：

```text
absent -> qwen(screening) -> idle(release-screening)
                              -> mineru(start-mineru) -> stopped
```

1. pipeline 进入 Stage 02 前调用 `ensure_managed_screening_worker`；manager 负责 rlaunch 申请、SSH、
   Qwen 健康检查和本地 tunnel。
2. phase 1 的最后一个 screening context 退出时只执行 `release-screening`，不会停止 worker。
3. `start_managed_mineru_service` 调用同一 manager 的 `start-mineru`，更新 state 中的 18084 tunnel，
   并把 `--api-url` 注入 MinerU CLI 参数。
4. Stage 04/05 结束后，外层 `finally` 执行 `stop`，同时关闭 MinerU 服务、SSH tunnel 和 rlaunch worker。
5. 任一阶段异常也经过同一 `finally`；state 文件保留到 manager 成功清理或用户手工执行 stop，避免泄漏资源。

没有 managed GPU 时，Stage 04 仍可使用本地 `mineru` 命令或已有 API；旧配置和旧调用者不受影响。

## 4. 关键代码变更

- `src/v2/stages/_document_normalization.py`：旧 Stage 02 的 GROBID/pdftotext 逻辑改写为 Stage 01
  normalization，取消排除 SI，论文级门控要求正文和所有已知 SI 成功。
- `src/v2/stages/_computational_content.py`：阶段记录和目录改为 Stage 02，语义 prompt/guard 保持原版本。
- `src/v2/stages/_toolbox_resource.py`：拆出 `run_toolbox_resource_screening`（Stage 03）和
  `run_mineru_deep_normalization`（Stage 04）。Stage 04 仅消费 `passed=true` 记录。
- `src/v2/stages/stage02.py`、`stage03.py`、`stage04.py`：提供新入口，并保留旧测试/调用者所需的兼容导出。
- `src/v2/pipeline.py`：替换旧的单阶段循环为 phase 1/phase 2 调度，阶段 hash、缓存读取和聚合目录同步更新。
  Stage 01 聚合报告现在同时统计 package hold 和 normalization attempt，不再隐藏 SI 获取失败论文。
- `src/v2/config.py`：旧布局迁移、新 MinerU GPU 路径解析、managed GPU 校验、Stage01-05 并发校验。
- `src/v2/runtime.py`：支持保留 worker、切换 MinerU、最终统一停止。
- `scripts/stage03_llm/manage_rlaunch_worker.sh`、`remote_manager.sh`：新增
  `release-screening`、`start-mineru`、MinerU 18084 tunnel 和状态记录。
- `scripts/mineru_gpu/bootstrap_environment.sh`：复用统一的
  `data_pipeline/.envs/researchchem-data-pipeline`；Qwen/vLLM、MinerU 和数据管线不再创建独立 Python
  环境。安装使用节点本地 `/tmp`、PJLab PyPI 镜像和 uv 并行下载；统一约束文件保护
  TensorFlow/Softcite 所需的 NumPy、Protobuf 和 Transformers 版本。
- `scripts/workflows/run_pipeline_v2.sh`：默认使用 pipeline conda Python，可选加载 `config.local.env`；
  仅在 `RCB_SETUP_PROXY=1` 时加载代理脚本。

## 5. 旧 2000 篇运行结果按新阶段重解释

来源：

- 原始运行：`runs/v2_shadow_2000_rlaunch_flash_20260808`；
- Stage 03/04/05 纠偏重跑：`runs/v2_shadow_2000_stage04_05_rerun_20260809`。

### 5.1 计数

| 新阶段 | 输入 | 通过/保留 | 主要分布 |
| --- | ---: | ---: | --- |
| Stage 00 | 2000 | 2000 | 正文 2000；远端已有 SI 1737；有 SI 的论文 1712；确认无 SI 288 |
| Stage 01 package | 2000 | 1785 | `complete_with_si` 1759；`complete_confirmed_no_si` 26；不可用/可重试 215 |
| Stage 01 normalization | 1785 | 1776 | GROBID 3586 docs；pdftotext 27；结构化 asset 6；解析失败/缺失 9 篇 |
| Stage 02 | 1776 | 76（纠偏后） | 计算内容确认 76；非纯计算 1300；无计算内容 391；background 1；uncertain 3；处理失败 1；另排除非原创 4 |
| Stage 03 | 76 | 17 | 软件覆盖 17；未覆盖 44；清单不确定 14；处理失败 1 |
| Stage 04 | 17 | 16 | MinerU 成功 16；深解析失败 1（337 页 SI，CPU 运行超时） |
| Stage 05 | 16 | 不可判定 | 16 条均为网络超时 `processing_failed`，不是科学上的 0 个候选 |

Stage 02 的 76/1776（4.28%）与“纯计算化学、优先高精度”的目标一致；但这是 precision 优先的离线
纠偏结果，不是新 prompt 的重新调用结果。Stage 03 的 17/76（22.4%）也符合“论文中所有核心软件
必须可由当前三层工具箱执行”的严格口径。

### 5.2 逐项问题判断

1. Stage 02 原始 80 个通过中有 4 篇是 review/correction 等非原创文章；纠偏目录已用确定性 article guard
   排除，说明语义模型结果必须始终经过标题/首页 guard。
2. Stage 03 的 44 个未覆盖不是“Action 缺失”造成的：决策使用 native backend、软件文档适配和已配置
   Python 层的冻结 capability snapshot；Q-Chem、TURBOMOLE、TeraChem、Molpro、CASTEP 均不在快照。
   对于 CATKINAS、ADF/pyfrag、ChemShell/TURBOMOLE、GIMIC/NBO/AIMAll、TensorFlow 等，至少一个论文所需
   核心软件不在快照，严格淘汰是符合目标的。
3. 14 个 `software_inventory_unconfirmed` 被 hold 而非 pass，表示模型/Softcite/正文证据不能确认完整
   软件清单；这会牺牲召回，但不会把未知工具误放入正式集。
4. 1 个 Stage 03 processing failure 是 Qwen context overflow（约 10241 input + 6144 output）。新实现
   将 token 估算改为更保守的字节/ token 比率，并保留单篇错误隔离；仍建议对真实 endpoint 做 preflight 和
   失败重试回放。
5. Stage 04 的 1 个 MinerU 失败属于资源/解析耗时问题，不是软件覆盖误判；GPU 持久 API 和微批次并发正是
   针对该问题的工程修复。
6. Stage 05 的 16 个 timeout 全部是 `URLError [Errno 110]`，外部 deepseek endpoint 在该次运行不可达。
   新代码会把全量处理失败标记为 `run_status=infrastructure_failed`，顶层 run summary 也会标为
   `completed_with_infrastructure_errors`，不能解释成筛选通过率为 0；恢复网络后只需从 Stage 05
   cache 断点重跑。
7. 旧运行中的 Stage 02/03 记录缺少 title/DOI 等元数据，导致人工审计只能依赖 paper_id。新 normalization
   和 Stage 02/03 记录会透传 title、DOI、期刊和文章 URL；旧 JSONL 保持只读，不做回写。

## 6. 验证与未完成项

已完成：

- `pytest test_v2_stage_layout.py test_v2_pipeline.py`：120 passed；
- `ruff check data_pipeline/src/v2 ...`：通过；
- shell 语法检查：通过；
- 示例配置 JSON 和 capability snapshot：已校验。

待完成：

- 已在联网 CPU 节点完成 `bootstrap_environment.sh`；仍需在有 GPU 的 rlaunch worker 上执行一次
  `start -> health -> release-screening -> start-mineru -> health -> stop` 集成验收；
- 网络恢复后只重跑旧 2000 篇 Stage 05，不能将当前 16 个 timeout 当科学结果；
- 新布局首次真实运行前，抽查 Stage 01 汇总中的 package hold 与 Stage 02 的完整 SI 准入。

## 7. 可复现命令

```bash
cd /mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline
python -m pytest -q tests/test_v2_stage_layout.py tests/test_v2_pipeline.py
python -m ruff check src/v2 tests/test_v2_stage_layout.py
bash scripts/mineru_gpu/bootstrap_environment.sh
```

旧结果只读统计可直接查看各目录的 `stage_summary.json`；不要删除或覆盖这两个历史 run。
