# Stage 03 计算化学相关性混合筛选方案

日期：2026-08-06

实施更新：2026-08-07。规则优先、边界样本模型复核已经实现；正式本地模型确定为
`Qwen3-30B-A3B-Instruct-2507`。因当前 GPU 资源紧张，本轮 100 篇 shadow run 临时使用
`deepseek-v4-flash`，本地模型部署测试延期，不改变统一的 OpenAI-compatible 接口契约。

## 1. 目标

Stage 03 只判断论文作者是否在本文中实际执行了可复现的计算化学过程，不判断软件是否
被工具箱覆盖，也不判断补充材料是否可下载。2026-08-07 起按用户确认切换为高精度模式：
允许漏筛，但不允许未确认样本继续。

## 2. 当前结果和主要误差

1000 篇旧运行结果为 290 strong、245 weak、465 reject。限制重复命中贡献并扩充词形后，
规则回放为 291 strong、299 weak、410 reject。

抽查发现两类主要错误：

1. 假阳性：综述引用他人的 DFT、MD 或优化结果，句子仍命中方法、结果和被动执行模板。
   例如 `optimization was conducted by Guan and his colleagues` 被当成本文作者执行。
2. 假阴性：真实计算论文包含大量 DFT、第一性原理或机器学习计算，但写法没有命中有限
   的 `we performed` 模板，或方法和执行动作分布在相邻句子/正文与 SI 中。

RSC 的 9 个规则候选中有 7 篇标题和官方类型明显属于 Review，说明文章类型和执行主体
归属必须进入判定，单纯增加关键词不能解决精度问题。

## 3. 推荐流程

```text
正文 + 已有 SI
      |
      v
03A 规则召回与证据切片
      |
      +-- 明确本文执行且证据完整 ----------> strong_candidate
      |
      +-- 明确非研究文章/纯引用背景 --------> not_computational
      |
      +-- 其余边界样本 --------------------> 03B 小模型审查
                                                |
                                                +-- performed
                                                +-- not_performed
                                                +-- uncertain
```

小模型不读取整篇 PDF，只读取标题、摘要、文章类型线索、方法/结果章节和规则命中前后文。
每篇输入控制在约 4,000-8,000 tokens。

## 4. Stage 03A 规则改进

### 4.1 文章类型线索

从 Crossref/出版社元数据、标题和正文首页提取：

- `research_article`
- `review_or_perspective`
- `correction_or_retraction`
- `editorial_masthead_news`
- `unknown`

Correction、Retraction、Masthead 和纯 Editorial 可直接淘汰。Review/Perspective 不直接
淘汰，但必须进入小模型审查；只有模型找到本文新增的计算过程才能保留。

### 4.2 执行主体归属

正证据要求方法或动作附近出现本文执行主体，例如：

- `we calculated/performed/simulated`
- `calculations were performed in this work`
- 本文 Methods/Computational details 中连续给出方法、参数和输出

负证据增加：

- `X et al. calculated/reported/demonstrated`
- `previous/recent studies`
- 带引用编号的第三方归属句
- `can be modeled/simulated` 等能力描述

不再让任意 `optimization was conducted` 单独贡献 `performed_here_evidence`。

### 4.3 同一上下文内组合证据

将单词级累计改为句子/段落级组合：

- 方法：DFT、TDDFT、ab initio、MD、MC、QM/MM、microkinetic 等；
- 执行：performed、computed、optimized、simulated；
- 参数/软件：functional、basis set、cutoff、k-points、time step、software；
- 输出：energy、barrier、geometry、spectrum、trajectory、band structure。

强候选至少需要一个“本文执行”片段，以及方法与参数/输出之一。只有方法名或只有结果词
不直接成为 strong。

### 4.4 规则路由

- 自动 strong：本文执行主体明确，且方法与参数/结果证据在同一段或相邻段。
- 自动 reject：非研究文章，或只有引用/背景证据。
- 模型审查：现有 weak、Review/Perspective、method-only 高分 reject、主体归属冲突样本。

预计只需调用模型处理约 30%-50% 的 Stage 03 输入，而不是全部论文。

## 5. Stage 03B 小模型

### 5.1 部署和临时后端

正式本地后端选用 `Qwen3-30B-A3B-Instruct-2507`，通过 vLLM 和轻量 FastAPI gateway
暴露 OpenAI-compatible API。部署脚本使用 `rlaunch` 申请单张 H200，环境和模型分别
固定在 `data_pipeline/.envs/` 与 `/mnt/shared-storage-user/liyuqiang/mdoels/`。Stage 03
只依赖统一 HTTP 接口，不与具体模型运行时耦合。

- GPU 资源可用时：由管线启动一个 Qwen worker，整次任务复用，任务结束精确停止；
- GPU 资源紧张时：关闭 managed rlaunch，指向 `deepseek-v4-flash` 外部接口；
- 完全禁用模型时：只执行规则判定；
- API 不健康、调用异常、JSON 非法或证据无法回映时：单篇回退规则结果，不拖垮批次。

该任务是短文本分类，不启用长链式思考。温度设为 0，原始响应和响应哈希必须缓存。
严格模式复核规则产生的全部 strong、weak 和 rule error 候选；规则 reject 不再为提高
召回而调用模型。`recall` 兼容模式仍可只审边界样本。

### 5.2 输出 schema

```json
{
  "performed_computation": "yes | no | uncertain",
  "article_role": "original_research | review | correction | editorial | unknown",
  "computation_role": "primary | supporting | background_only | none",
  "method_families": ["electronic_structure"],
  "author_execution_evidence": [
    {
      "document_id": "...",
      "quote": "...",
      "reason": "authors report calculations performed in this work"
    }
  ],
  "confidence": 0.0,
  "reason": "..."
}
```

模型必须引用提供的证据片段；引用不能映射回原文时结果无效并按 `uncertain` 处理。

### 5.3 最终判定

- `yes`、原创研究、primary/supporting、置信度至少 0.85 且至少有一个可验证执行证据：保留；
- `no`：淘汰；
- `uncertain`、低置信度、响应错误或证据无法回映：`llm_unconfirmed`，淘汰；
- Review/Perspective 在严格模式淘汰。

## 6. 数据和评估

先从当前 1000 篇分层标注 200-300 篇：

- strong、weak、reject 各取样；
- 强制包含 Review、Correction、方法名密集但无执行模板、SI-only 计算；
- 划分开发集和独立 holdout。

最低报告指标：

- 计算过程判定 precision/recall；
- Review 假阳性率；
- 原创计算论文漏筛率；
- 每 1000 篇进入 Stage 04 的数量；
- 每篇模型调用 tokens、时间和成本；
- 规则自动判定比例与模型审查比例。

上线优先保证 precision。Stage 05 的工具箱覆盖判断仍然独立，不能反向影响 Stage 03
的“是否执行了计算”判定。

## 7. 实施顺序

1. 增加文章类型和第三方归属规则，建立 200-300 篇标注集。
2. 实现证据切片器和模型 JSON schema，不改变现有最终路由，先 shadow run。
3. 用 `deepseek-v4-flash` 和本地 Qwen3-30B-A3B 在标注集上对比。
4. 选择阈值，先让模型接管 weak/Review/method-only 边界样本。
5. 在 1000 篇上对比旧规则、修复规则和混合方案，再决定是否默认启用。

## 8. 实现位置

- `scripts/stage03_llm/`：环境、模型下载、vLLM、gateway 和 rlaunch 生命周期脚本；
- `src/stages/stage03_computation_relevance/llm_review.py`：证据切片、并发调用、缓存、
  schema 校验和规则回退；
- `src/integrations/stage03_llm_runtime.py`：整次管线共享 worker 的生命周期；
- `src/orchestration/screening_microbatch.py`：Stage 02-06 微批次流水线。
