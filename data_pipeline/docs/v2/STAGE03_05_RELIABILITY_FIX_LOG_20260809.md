# Stage03-05 可靠性修复记录

日期：2026-08-09

范围：基于 `runs/v2_shadow_2000_rlaunch_flash_20260808` 的逐记录审计，修复 Stage03、Stage04、
Stage05 的判定和接口合同。没有改写历史运行产物，也没有修改化学工具箱业务代码。

## 1. 审计基线

2000 篇历史运行的阶段结果为：

| 阶段 | 结果 |
| --- | --- |
| Stage00 | 选择 2000 篇 |
| Stage01 | 1785 pass，215 hold |
| Stage02 | 1785 个论文包，1776 个满足旧 Stage03 入口条件 |
| Stage03 | 80 confirmed，1300 not-pure，391 not-found，3 uncertain，1 background，1 failed |
| Stage04 | 5 covered，57 uncovered，16 inventory-unconfirmed，2 failed |
| Stage05 | 5 abstain，0 pass |

审计发现 Stage05 的 5 个 `abstain` 中，只有 1 个是模型明确认为科学证据不足；另 4 个模型实际输出
了候选任务，但字段名和 evidence namespace 不符合确定性验证器，被旧实现静默归入 `abstain`。

## 2. Stage02 与 Stage03

### 2.1 元数据和入口完整性

Stage02 的论文级记录现在透传 `title`、`doi`、`journal_name` 和 `article_url`。Stage03 仍只接受：

- 正文解析成功；
- Stage01 已确认无 SI，或所有已知 SI 均解析成功；
- 不存在 partial SI parse。

因此解析失败不会以缺失文本进入语义筛选，文章类型判断也不再丢失 Stage01 标题。

### 2.2 非原创文章的确定性隔离

在调用 LLM 前增加文章类型 guard。标题或首页明确为 correction、corrigendum、erratum、retraction、
review、perspective、editorial 或 commentary 时，输出 `non_original_article`，记录命中原文，并注明
`model_called=false`。规则不使用一般性的“overview”等宽泛词。

对 2000 篇历史文本离线回放命中 19 篇，其中 4 篇此前被误列为
`computational_content_confirmed`；其余主要是 correction、review 和 perspective。

### 2.3 作者实验归属

Stage03 map prompt 新增 `actor_text` 和 `current_paper_cue`，要求模型分别给出动作执行者和“本文作者”
线索。确定性校验只接受同时包含实体实验动作和实验上下文的原文；`reported by`、`et al.`、
`coworkers`、`colleagues`、`adapted with permission` 等外部归属不能证明当前作者做实验。

模型声称 mixed/not-pure，但没有通过校验的当前作者实验原文时，结果变为 `uncertain`，而不是直接通过
或硬淘汰。历史回放中 50 篇由 `not_pure_computational` 变为 `uncertain`，仍不进入 Stage04，但可以
独立复审。该变化修正淘汰理由，不放宽通过集。

## 3. Stage04

### 3.1 支持无关的软件清单

prompt 要求先完整抽取实际使用的软件和工作流，不向模型暗示“在 catalog 内才值得报告”。清洗器会
去除方法、参数、算法、损失函数、硬件和作者姓名，例如 PBE、Monkhorst-Pack、ReLU、Adamax、
Huber loss、HPE Cray，以及 `Singleton's Progdyn program` 中的 `Singleton`。软件名必须能回映到
同一 evidence block 的实际使用原文。

### 3.2 三层工具箱判定

能力快照同步器现在同时导出：

1. 预设 Action；
2. 原生 backend 及其别名、可执行程序和文档入口；
3. 当前 MCP profile 中实际配置的 Python 包，例如 ASE、NumPy、SciPy、pandas、scikit-learn、
   PyTorch、JAX、e3nn 和 Matplotlib。

Stage04 的硬门是“必要软件是否存在于原生 backend 或已配置 Python 包目录”，不是“是否已有对应
Action”。完整清单中短小、确定性的分析/后处理步骤可以由任务特定 Python 完成；未命名或缺失的核心
电子结构、动力学、采样引擎不能由此绕过。

被删除的 Q-Chem、TURBOMOLE、TeraChem、Molpro 和 CASTEP 不会重新出现在能力快照。

### 3.3 资源与稳定性

- 仅提取明确属于本文计算的资源/复杂度事实，排除反应、孵育、仪器采集等实验时间；
- 明确单任务超过配置预算时输出 `cost_exceeds_budget`；未知成本保留为 `cost_unconfirmed`，不冒充
  已确认低成本；
- 根据模型上下文窗口、输入字节和安全余量动态下调输出 token，避免输入加输出超过部署模型窗口；
- 单篇 schema/模型错误保持 `processing_failed`，不终止整批。

历史 Stage04 输出离线回放（不重新调用模型）中，15/78 个可解析旧记录发生变化：9 个
inventory-unconfirmed 和 5 个 uncovered 因当前三层能力目录变为 covered，另 1 个虚假软件被清理后
变为 inventory-unconfirmed。2 个历史模型响应本身缺少必需数组，仍保持处理错误，不能伪造科学结论。

## 4. Stage05

Stage05 只接收 Stage04 通过后由 MinerU 重新抽取的 evidence blocks。Stage04 中来自 GROBID 的旧
`evidence_ids` 在请求前递归删除，模型只能引用当前 packet 的 MinerU ID。

prompt 和验证器统一为以下合同：

- `task_direction` 必须是十个 taxonomy ID 之一；
- workflow、validation gate、score、required software 和 evidence ID 都是数组；
- required software 按 Stage04 的规范标识、backend 名或原始名称归一化；
- workflow 至少三步，并具备科学问题、claim/figure/table、公开输入、隐藏目标、验证门和机器评分；
- 模型输出 pass 但候选合同无效时，携带逐候选错误执行一次合同修复重试；
- 仍失败记为 `contract_invalid`，真正的科学性拒绝才记为 `abstain`。

这样不会再把字段/schema 错误解释为论文没有 benchmark 价值，也避免字符串软件列表被逐字符验证。

## 5. 修改后的流程

```text
Stage00 选择并按论文归档正文/SI
  -> Stage01 闭合论文包并确认 SI 状态
  -> Stage02 GROBID，失败回退 pdftotext；正文和全部已知 SI 质量门
  -> Stage03 非原创 guard -> LLM map/reduce -> 严格纯计算与作者实验归属门
  -> Stage04 软件/资源证据抽取 -> 三层工具箱确定性映射 -> 资源预筛
             -> 仅对通过论文执行 MinerU 深解析
  -> Stage05 强模型 suitability -> 确定性合同验证 -> 必要时合同修复重试
  -> Stage06 Builder
  -> Stage07 独立 Judge / Gold Run
```

微批次仍按 `Stage02 -> Stage03 -> Stage04 -> Stage05` 顺序推进；不同微批次可并行。Screening LLM
在 Stage03/04 共用一个 run-level 服务，沙箱和模型都在任务开始前启动、任务结束后统一停止。

## 6. 验证边界

本轮执行了单元/回归测试、能力快照一致性检查和历史产物离线回放。历史回放用于验证确定性规则的影响，
不等同于使用新 prompt 重新调用部署模型。下一次正式批量运行必须使用新 prompt/cache namespace，
并重点抽查：Stage03 的 19 个 article-type guard、`uncertain` 分层，Stage04 新增 Python 包覆盖，以及
Stage05 的 `pass/abstain/contract_invalid` 分布。

最终验证结果：`data_pipeline/tests` 为 `269 passed, 8 subtests passed`；能力快照 `--check`、示例
配置 JSON、Python `ruff check` 和 `git diff --check` 全部通过。
