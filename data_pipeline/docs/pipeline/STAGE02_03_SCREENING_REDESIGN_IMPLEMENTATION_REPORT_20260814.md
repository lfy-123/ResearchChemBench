# Stage02/03 筛选重构实施与回归报告

日期：2026-08-14

状态：代码实现、隔离回归和人工逐篇审查已完成；未上传 GitHub

## 1. 结论

本轮重构完成了设计文档规定的职责拆分：

- Stage02 独占“是否存在作者实际执行、完整且非平凡的计算化学工作流”的判断；
- Stage03 只把软件证据绑定到 Stage02 冻结工作流，并执行高召回负向排除；
- Stage03 不再判断计算流程完整性、资源成本或 benchmark 科学意义；
- Stage03 只有在每个冻结工作流都明确依赖工具箱目录外的必要软件时才淘汰论文；
- 未报告软件、绑定不完整或归属不清统一以 `software_inventory_unconfirmed` 继续到 Stage04/05；
- 资源审计迁移到 Stage05 的 MinerU 高质量文本和候选任务范围上执行。

16 篇真实 API 回归中，Stage02 通过 16 篇并生成 1--3 个已确认工作流；这些论文原本均来自历史 Stage02 通过集，因此该结果用于验证新合同，不用于估计 Stage02 的总体通过率。Stage03 最终得到：

| Stage03 决策 | 数量 | 是否继续 |
|---|---:|---|
| `software_covered` | 3 | 是 |
| `software_inventory_unconfirmed` | 10 | 是 |
| `core_software_uncovered` | 3 | 否 |

逐篇人工检查确认 3 个终止拒绝都满足“单一冻结工作流存在必要目录外软件”的条件；其余 13 篇没有因辅助软件、可视化程序、软件未命名或其他工作流的不覆盖而被错误终止。当前样本未发现终止决策错误，但 16 篇规模不足以替代后续独立 holdout。

## 2. 旧任务停止情况

- 已终止旧 `stage00-05-kps-published-since-20260101-20260814` 工作流进程；
- 平台实查 32 个 MinerU 沙箱均为 `Terminated`；
- 另发现该 run 的 64 CPU 主沙箱仍为 `Running`，已单独停止并复查为 `Terminated`；
- 没有删除旧运行结果，也没有停止其他 run 的资源。

本地 `pool.json` 和 inventory 是创建时快照，可能仍保留旧 `Running` 字段；平台管理 API 的实时状态是本节采用的事实来源。

## 3. Stage02 修改

### 3.1 两次调用的职责

第一次调用同时完成论文分类和候选发现，最多输出三个相互独立的 `workflow_candidates`。每个候选记录稳定的 workflow/step ID、化学体系、计算动作、生成的科学产物、科学用途和证据 ID。

第二次调用一次性独立验证所有候选，不按候选增加调用次数。只有以下轴均获得证据支持的候选进入 `confirmed_workflows`：

- 作者实际执行计算；
- 化学体系可识别；
- 存在真实计算或模拟操作；
- 生成新的化学输出；
- 输出被用于论文科学结论；
- 工作流非平凡；
- 不是实验数据拟合、仪器处理或绘图冒充计算化学。

通过论文若没有任何已确认工作流，会确定性降级为 `uncertain`，不能传给 Stage03。

### 3.2 新数据合同

Stage02 决策记录新增：

- `workflow_contract_version`；
- `workflow_candidates`；
- `workflow_verification`；
- `confirmed_workflows`。

Stage03 只允许消费 `confirmed_workflows`。旧记录通过显式 legacy adapter 用于历史分析，新生产记录缺少新合同则返回 `upstream_contract_insufficient`，不会伪造科学拒绝。

## 4. Stage03 修改

### 4.1 冻结工作流

Stage03 模型只能为既有 workflow/step ID 补充软件绑定，不能新增、删除、合并或重新定义工作流。模型新增的工作流被忽略并记录审计警告。

### 4.2 软件解析

软件覆盖依据运行时生成的工具箱 capability snapshot、软件别名资产和外部软件资产，不在业务代码中硬编码论文、DOI、期刊或测试样本软件。

通用解析规则包括：

- 大小写、官方版本号、revision 和明确括号缩写可归一化到目录软件；
- 模型自行给出的 `normalized_hint` 不能单独证明目录命中；
- plugin、extension 和独立程序不能折叠到宿主软件；
- 方法、算法、基组、泛函、硬件、文件格式和数据资源不能作为软件；
- 明确命名、有有效正文证据、实际使用、绑定冻结工作流必要角色且目录未命中的独立运行时，才形成 `uncovered`；
- 未命名、归属不清或证据不足保持 `unconfirmed`。

工作流判定同时读取步骤级软件和绑定到 workflow 的必要软件清单，解决一个冻结步骤需要多个程序、但 `software` 字段只能容纳一个名称时的漏判。

### 4.3 论文级门控

```text
存在 workflow_covered
  -> software_covered
否则存在 workflow_coverage_probable
  -> software_coverage_probable
否则存在 workflow_software_inventory_unconfirmed
  -> software_inventory_unconfirmed
否则所有 frozen workflows 均为 workflow_uncovered
  -> core_software_uncovered
```

前三类通过，只有最后一类终止。

### 4.4 Prompt 清理

移除了 Stage03 prompt 中残留的资源抽取、最多两个工作流和最多五个步骤约束。当前 prompt 要求：

- 完整保留最多三个 Stage02 冻结工作流及其步骤；
- `resource_facts=[]`、`complexity_facts=[]`；
- 只提取软件证据和角色；
- 不展示自由思维链，只返回紧凑 JSON。

## 5. Stage05 边界适配

Stage05 现在：

- 接收 Stage03 的 covered、uncovered、unconfirmed 三类软件事实；
- 使用 Stage04 MinerU 正文/SI 对未确认软件做最终定位；
- 将深度文本中新发现的软件先记为 candidate，不未经模型绑定就当作实际使用；
- 在候选级抽取体系规模、方法、采样规模、job 数和论文报告资源，执行成本审计。

这保证 `software_inventory_unconfirmed` 在 Stage03 通过不等于最终认定工具箱覆盖。

## 6. 配置与模型链

Stage02 默认链：

```text
DeepSeek-V4-Pro -> Nex-N2-Pro -> DeepSeek-V4-Flash ->
Nex-N2-Pro-w8a8 -> DeepSeek-V4-Flash-DSpark -> MiniMax-M2.7 ->
Mimo-V2.5-Pro -> Qwen3.6-27B
```

Stage03 默认链：

```text
Nex-N2-Pro -> DeepSeek-V4-Pro -> DeepSeek-V4-Flash ->
Nex-N2-Pro-w8a8 -> DeepSeek-V4-Flash-DSpark -> MiniMax-M2.7 ->
Mimo-V2.5-Pro -> Qwen3.6-27B
```

两个阶段均关闭支持该参数的模型思考模式。输出预算为 Stage02A 12,288、Stage02B 6,144、Stage03 12,288 tokens。Fallback 只在请求执行失败时发生，不能用于寻找更宽松结论。

## 7. 回归方法

### 7.1 历史离线重放

对旧批次 96 篇 Stage02 通过论文使用 legacy adapter 和最终确定性门控重放：

| 决策 | 旧版 | 新版离线重放 |
|---|---:|---:|
| 明确不覆盖 | 58 | 16 |
| 覆盖 | 20 | 49 |
| 未确认继续 | 8 | 31 |
| 旧 mixed/probable | 10 | 已归入上述新标签 |

42 篇旧版 `core_software_uncovered` 被纠正为覆盖或未确认继续。由于旧 Stage02 没有新工作流合同，这组结果只用于迁移检查，不能作为最终精度指标。

### 7.2 真实 API 回归

从历史 Stage02 通过结果选取 16 篇分层样本，覆盖：目录软件、目录外软件、多工作流、软件未命名、版本/缩写和辅助软件边界。

- Stage02：DeepSeek-V4-Pro，32/32 请求成功，无 fallback，无 token 截断；
- Stage03：Nex-N2-Pro，16/16 请求成功，无 fallback，无 token 截断；
- Stage02 最大实际 completion 为 1,875 tokens；
- Stage03 最大实际 completion 为 3,324 tokens；
- 所有响应 `finish_reason=stop`。

耗时（4 并发）：

| 阶段 | 16 篇墙钟时间 | 折算墙钟/篇 | API 调用数 |
|---|---:|---:|---:|
| Stage02 | 1,187.58 s | 74.22 s | 32 |
| Stage03 | 354.36 s | 22.15 s | 16 |
| 合计 | 1,541.94 s | 96.37 s | 48 |

折算值是批次墙钟时间除以论文数，不是单请求延迟；Stage02 单请求平均 114.7 s，Stage03 单请求平均 83.0 s，并发掩盖了部分延迟。

## 8. 逐篇人工审查摘要

| DOI | Stage03 | 人工结论 |
|---|---|---|
| 10.1016/j.biomaterials.2025.123743 | 明确不覆盖 | 正确；唯一工作流必要使用 MOE/Schrödinger，均不在目录 |
| 10.1002/cmdc.202500961 | 明确不覆盖 | 正确；Vina 覆盖，但必要预处理/分析依赖目录外程序 |
| 10.1016/j.biomaterials.2025.123631 | 明确不覆盖 | 正确；Vina 覆盖，但必要 PDBQT 预处理依赖目录外程序 |
| 10.1002/anie.202518099 | 未确认继续 | 正确；VASP 覆盖，部分步骤软件归属未完全绑定 |
| 10.1016/j.biomaterials.2025.123482 | 覆盖 | 正确；冻结工作流由 Gaussian 完成 |
| 10.1002/asia.70544 | 覆盖 | 正确；冻结工作流由 Gaussian 完成 |
| 10.1002/anie.202521873 | 未确认继续 | 安全保留；VASP/LOBSTER 覆盖，个别分析步骤未绑定 |
| 10.1002/cctc.202501549 | 未确认继续 | 安全保留；核心 CREST/ORCA/Multiwfn/xTB 覆盖，存在未绑定步骤 |
| 10.1002/anie.202524596 | 未确认继续 | 安全保留；VASP 覆盖，分析实现未完全报告 |
| 10.1002/slct.202505016 | 未确认继续 | 正确；Gaussian 工作流可能覆盖，另有 CASTEP/AutoDock 工作流不覆盖 |
| 10.1002/anie.202525044 | 未确认继续 | 安全保留；ORCA/Multiwfn/VMD 覆盖，第二工作流绑定不完整 |
| 10.1002/slct.202505650 | 未确认继续 | 正确；Gaussian 工作流可能覆盖，Molegro 工作流不覆盖 |
| 10.1002/anie.202524449 | 覆盖 | 正确；至少一个完整 Gaussian 工作流覆盖 |
| 10.1002/anie.202520214 | 未确认继续 | 安全保留；VASP 覆盖，其余步骤待 Stage05 深度确认 |
| 10.1002/cctc.202501268 | 未确认继续 | 正确；VASPsol 工作流不覆盖，另一个 SISSO/Scikit-learn 工作流仍需确认 |
| 10.1016/j.biomaterials.2025.123496 | 未确认继续 | 正确；Stage02 确认计算，但正文/SI 没有可靠软件名称 |

`未确认继续` 是有意的高召回结果，不应计为“工具箱已覆盖”。其中若干论文很可能在 Stage05 被确认覆盖，也可能因 MinerU 全文发现必要目录外软件而拒绝。

## 9. 自动验证

- `ruff` 对本轮修改文件检查通过；
- Stage02/03 专项回归：248 passed；
- Git 已跟踪的数据管线测试（排除工作区中未提交的 Stage06/07 Agent 草稿测试）：359 passed；
- 当前全目录测试还会收集未提交的 `tests/test_stage0607_agents.py`，结果为 414 passed、1 failed；失败属于 Stage06 草稿的 `constructed`/`construction_invalid` 预期差异，不在本次提交范围；
- `git diff --check` 通过；
- diff 特例扫描没有发现测试 paper ID、DOI、期刊或样本软件名称进入 Stage02/03 业务代码；
- 官方版本、括号缩写、未知软件、外部软件、多工作流、未命名软件、模型新增工作流和资源延迟审计均有回归测试。

## 10. 输出位置

- 历史离线重放：`runs/stage00-05-kps-published-since-20260101-20260814/evaluations/stage02-03-redesign-20260814/offline-history/`
- 新版 Stage02 真实回归：同目录下 `live-api-16/model_run/stage_02_computational_content/`
- 最终 Stage03 真实回归：同目录下 `live-api-16-rerun-stage03/model_run/stage_03_toolbox_resource_gate/`
- 逐篇旧新对照：`live-api-16-rerun-stage03/comparison.jsonl`

## 11. 剩余风险与下一步

1. 本次真实回归是从历史 Stage02 通过集抽样，不能测量 Stage02 对全量论文的 precision/recall。下一次应建立包含正负样本的独立 holdout。
2. Stage03 的 10 篇未确认是设计上的高召回缓冲，不是最终成功。必须在 Stage04/05 统计“确认覆盖、确认不覆盖、仍未确认”的转化率。
3. 目录 snapshot 必须随化学工具箱更新重建并记录 hash；否则软件覆盖结论会过期。
4. 建议下一轮至少对 200 篇独立样本执行新版 Stage02/03，并人工复核全部 terminal reject 与随机抽取的 pass，而不是继续在这 16 篇上调提示词。
