# ResearchChemBench 数据管线 v1 到 v2 迁移方案

状态：兼容式迁移基线已执行；旧入口保留，v2 通过显式 contract 启用。

## 1. 迁移原则

1. 不在旧运行目录中原地升级或覆盖结果。
2. 不先删除旧阶段；先增加 v2 实现并 shadow run。
3. 只复用可由 hash、版本和来源证明等价的产物。
4. 旧“科学判定”不能因为字段相似而直接转换成 v2 判定。
5. 配置、缓存和输出契约独立版本化。
6. 所有迁移适配器只读旧数据，写入新的 v2 run directory。
7. 正式切换前保留一个只读 v1 入口，用于历史结果复现。

## 2. 阶段映射

| 当前实现 | v2.1 目标 | 迁移结论 |
| --- | --- | --- |
| Stage 00 `stage00_remote_corpus` | Stage 00 远端语料选择 | 大部分复用，补充统一 record header 和稳定 ID |
| Stage 01 `stage01_inventory` + Stage 04 `stage04_supplementary_acquisition` | v2.1 Stage 01 论文包闭合 | 复用 inventory/dedupe、publisher adapters/download；统一 package 与 normalization 输出 |
| Stage 02 `stage02_parsing` + Stage 06 `stage06_supplementary_extraction` | v2.1 Stage 01 低成本标准化 | 正文和所有已知 PDF SI GROBID-first，失败/低质量回退 `pdftotext`；旧 MinerU 结果不作为默认解析器 |
| Stage 03 `stage03_computation_relevance` | v2.1 Stage 02 | 复用 map/reduce 和确定性 guard，阶段编号及输出目录迁移 |
| Stage 05 `stage05_preliminary_coverage` + 旧 `stage04_resource_limits` | v2.1 Stage 03 | 复用 Softcite、别名、三层 capability resolver 和资源 gate；不在此阶段深解析 |
| 旧 Stage 04 的 MinerU 子流程 | v2.1 Stage 04 | 只对 Stage 03 通过者执行 MinerU；失败隔离为 `deep_parse_failed` |
| Stage 07 Builder | v2 Stage 06 | 改成 shared record + 两个隔离 Builder；旧单任务 schema 不兼容 |
| Stage 08 Judge | v2 Stage 07 | 扩展 paired-mode checks 和 Gold Run；旧结果不兼容 |
| 旧 Stage 05 asset collection | v2 第一版无对应主阶段 | 保留历史代码，不进入 v2 默认流程 |

## 3. 目录迁移

### 3.1 新代码目录

建议新增：

```text
data_pipeline/src/v2/
  contracts/
    common.py
    paper_package.py
    normalized_document.py
    computational_content.py
    workflow_inventory.py
    benchmark_candidate.py
    task_pair.py
  orchestration/
    pipeline.py
    microbatch.py
    services.py
  stages/
    stage00_remote_corpus/
    stage01_paper_package/
    stage02_document_normalization/
    stage03_computational_content/
    stage04_toolbox_resource_gate/
    stage05_benchmark_suitability/
    stage06_task_builder/
    stage07_task_judge/
```

不建议立即重命名现有 `src/stages/`。先使用独立 `src/v2/` 防止新旧 import 和 stage number 混淆；
v2 验收后再决定是否删除命名空间层级。

### 3.2 新运行目录

```text
runs/<run_id>/
  run_manifest.json
  config.resolved.json
  logs/
  stage_00_remote_corpus/
  stage_01_paper_package/
  stage_02_document_normalization/
  stage_03_computational_content/
  stage_04_toolbox_resource_gate/
  stage_05_benchmark_suitability/
  stage_06_task_builder/
  stage_07_task_judge/
  microbatches/
  services/
```

聚合输出和微批次输出都应引用同一个 content-addressed artifact，而不是复制多份大型 MinerU 结果。

## 4. 代码模块迁移

### 4.1 Stage 00

可复用：

- 远端枚举和复制；
- seeded sample、cursor 和历史排除；
- source record；
- hash/ETag；
- paper directory。

需要修改：

- `paper_id` 生成逻辑从选择序号中解耦；
- 每条记录增加 `pipeline_contract/record_schema_version/producer`；
- 复制错误按 paper 隔离；
- 生成 Stage 01 所需的明确 SI hints，区分已验证对象和未验证字符串。

旧 Stage 00 `selected_papers.jsonl` 可通过只读 adapter 转换成 v2 Stage 00 输入，只要主 PDF hash 一致。

### 4.2 Stage 01

从当前 Stage 01 复用：

- PDF 签名、页数和元数据读取；
- SHA-256 精确去重；
- document role 基础识别；
- paper grouping。

从当前 Stage 04 复用：

- publisher adapter registry；
- ACS、RSC、Elsevier、Wiley、Nature、MDPI 发现器；
- 下载校验、host 限速和超时；
- `support_path` 优先策略；
- supplementary retention policy。

需要新增：

- DOI/标题/版本级 paper dedupe；
- attachment relation evidence；
- `confirmed_no_si` 证据契约；
- atomic package freeze；
- package manifest；
- acquisition cache 和逐 DOI 重试状态。

旧 Stage 04 已下载文件可复用，但必须同时满足：

- SHA-256 可验证；
- MIME/文件签名正确；
- DOI 或 publisher attachment relation 与目标 paper 一致；
- 不是 HTML 错误页；
- 原始来源 URL/remote URI 可审计。

旧 `download_status=partial` 不能直接转换为 `complete_with_si`，必须重新执行完整性检查。

### 4.3 v2.1 Stage 01（标准化）

v2.1 Stage01 保持 GROBID-first 的低成本路线，正文和 SI 均全量参与前筛；MinerU 移到 Stage03 门控之后。
迁移步骤：

1. 抽出统一 `ParserAttempt` contract。
2. 将 GROBID 封装为正文和 PDF SI 的 primary parser attempt。
3. 将 `pdftotext -layout` 封装为 GROBID 请求失败、TEI 失败或低质量时的 fallback attempt。
4. Stage01 禁止调用 MinerU，非 PDF SI 使用对应结构化 parser。
5. 将现有 `integrations/mineru.py` 移交 v2.1 Stage04，通过软件/资源门控后解析正文和 PDF SI。
6. 为 Stage04 MinerU 增加 page-level quality report、独立 evidence namespace 和失败隔离。
7. 将 Stage 06 的 SI parsing/evidence 文件迁入统一 document artifacts。
8. 构建 `content_blocks.jsonl` 和稳定 evidence IDs。

旧缓存复用规则：

- MinerU 原始输出：只能复用到 Stage04 deep normalization，且 PDF hash、MinerU commit/model/config 完全一致；
- GROBID TEI：正文和 PDF SI 通过 v2 质量门后可作为 Stage02 默认选中结果；
- `pdftotext`：命令版本和 layout 参数一致时可复用；
- 旧 `text_quality.score` 不能直接当作 v2 quality pass，必须用新指标重算；
- 旧 Stage 06 已解析 SI 只有在原始文件 hash 和 parser metadata 完整时可导入 attempt cache。

### 4.4 v2.1 Stage 02

可复用：

- computational method ontology；
- evidence rules 和 negative contexts；
- evidence span 定位；
- OpenAI-compatible client；
- rlaunch/vLLM/gateway 基础脚本；
- request caching 和并发框架。

必须替换：

- `stage03-pure-computation-review-v2` prompt；
- pure computational、no experiments、original research 和 primary-only 路由；
- 只审 strong/weak 而跳过规则 reject 的逻辑；
- 24,000 字符单包截断策略；
- API/schema 错误时 fail closed 为科学 reject 的语义。

v2 改为 chunk map + paper reduce，所有可解析论文进入模型。旧 LLM cache 因 prompt 和输入契约变化全部失效；
旧规则 evidence 若能映射到新 content blocks，可以作为 recall hints 导入，但必须重新生成 evidence IDs。

### 4.5 v2.1 Stage 02/03 共用模型服务

当前 `stage03_llm_runtime.py` 和 `scripts/stage03_llm/` 需要泛化为：

```text
src/v2/integrations/screening_llm_runtime.py
scripts/screening_llm/
```

配置从 `stage03_computation_relevance.llm` 提升到顶层：

```json
{
  "models": {
    "screening": {
      "managed_rlaunch": true,
      "base_url": "...",
      "model": "Qwen3-30B-A3B-Instruct-2507",
      "stage03_max_inflight": 16,
      "stage04_max_inflight": 12
    }
  }
}
```

manager state 文件不再叫 `.stage03_llm_worker.local.json`，改为 `.screening_llm_worker.local.json`。
启动、健康检查和关闭都由 run-level service stack 负责。

### 4.6 v2.1 Stage 03

从当前 Stage 05 复用：

- Softcite client/pool；
- 多实例服务；
- software aliases；
- software role rules；
- toolbox profile/capability map；
- capability catalog hash；
- method family mapping；
- deterministic backend normalization。

从旧资源阶段复用：

- Grobid Quantities context recall；
- resource term regex；
- unit normalization；
- OpenAI-compatible structured interpretation；
- resource limit comparison框架。

必须修改：

- Softcite 不再是唯一软件来源；增加 LLM inventory/audit；
- 软件角色枚举改为 v2 contract；
- LLM 输出不能直接决定 covered；
- 覆盖检查加入 runtime snapshot；
- 区分 catalog、functional evidence 和 runtime verified；
- 对 range 同时检查上下界；
- `greater_than` 用下界判断，`less_than` 不能无条件当作限额内；
- 区分 single job、aggregate study 和 physical experiment；
- 单篇资源模型错误隔离；
- `no_explicit_resource` 不自动 pass，转为估算或 hold；
- 工具箱更新只失效 Stage 04+ 缓存。

旧 Stage 05 Softcite raw responses 可在 document hash、Softcite commit/model/config 一致时复用；旧
`direct_candidate/workflow_software_uncovered` 判定不能复用。

### 4.7 v2.1 Stage 04/05

新增独立 `benchmark_suitability` 阶段。它不从旧 Builder 代码中直接调用 Agent，而使用严格的
OpenAI-compatible JSON call 或受限 Agent：

- 输入 evidence manifest；
- 不允许网络；
- 不允许浏览整个 workspace；
- 输出 0-3 candidate records；
- 确定性验证 workflow DAG、evidence IDs 和 direction enum。

十个方向使用现有 `assets/chemistry_research_direction_taxonomy.json`，实现前需核对其枚举与 v2 文档一致。

### 4.8 Stage 06

现有 Stage 07 Builder 的 workspace isolation、Agent runner、context materialization 和基础 validation 可以复用。

需要重构：

- 从“一篇论文正好一个任务”改为“每个 candidate 一对任务”；
- 拆分 shared record、autonomous builder 和 reproduction builder；
- 新 task-pair schema；
- 新 public/hidden disclosure validator；
- Builder 只能读取 candidate 引用的 evidence；
- allowed software/actions 必须引用 frozen runtime snapshot；
- 不再读取旧 `preliminary_coverage` 嵌套对象。

旧 `candidate_task.json` 不能自动升级为 task pair，只能作为 Builder 回归样本。

### 4.9 Stage 07

现有 Stage 08 Judge 的独立 workspace、public input probe 和 audit report renderer 可以复用。

需要增加：

- paired-mode consistency；
- autonomous route leakage；
- reproduction answer leakage；
- workflow depth 和 validation gate；
- runtime verified capability；
- ground-truth grade、单位、参考态和 tolerance；
- Gold Run queue、沙箱执行、资源报告和 release decision。

旧 Judge pass 不能转换为 v2 pass，因为它未审计成对任务和 Gold Run。

## 5. 配置迁移

### 5.1 建议的 v2 配置骨架

```json
{
  "pipeline_contract": "researchchembench-data-pipeline/v2",
  "run_directory": "runs/v2-current",
  "stop_after": "stage07",
  "microbatch": {
    "size": 10,
    "concurrency": 5,
    "resume": true,
    "stage_limits": {
      "1": 5,
      "2": 5,
      "3": 5,
      "4": 5,
      "5": 2,
      "6": 2,
      "7": 1
    }
  },
  "models": {
    "screening": {
      "managed_rlaunch": true,
      "model": "Qwen3-30B-A3B-Instruct-2507",
      "stage03_max_inflight": 16,
      "stage04_max_inflight": 12
    },
    "suitability": {
      "model": "deepseek-v4-pro",
      "api_key_env": "SUITABILITY_API_KEY",
      "max_inflight": 4
    },
    "builder": {
      "model": "gpt5.6",
      "api_key_env": "BUILDER_API_KEY",
      "max_inflight": 2
    },
    "judge": {
      "model": "gpt5.6",
      "api_key_env": "JUDGE_API_KEY",
      "max_inflight": 1
    }
  },
  "stage01": {
    "supplementary_scope": "official_only",
    "publisher_adapters": ["acs", "rsc", "elsevier", "wiley", "nature", "mdpi"]
  },
  "stage02": {
    "parser_order": ["grobid", "pdftotext"]
  },
  "stage04": {
    "software_coverage_basis": "native_software_catalog_presence",
    "unknown_software_policy": "hold",
    "mineru": {"enabled": true, "method": "auto"}
  },
  "resource_budget": {
    "cpu_cores": 0,
    "gpus": 0,
    "memory_gb": 0,
    "single_job_hours": 0,
    "total_core_hours": 0,
    "total_gpu_hours": 0
  }
}
```

上例中的资源数值必须在实现前由用户按正式评测环境填写，不能沿用当前筛选沙箱的资源，也不能把
现有 `500 CPU/1000 GB` 当作默认科学预算。

### 5.2 旧配置字段映射

| v1 字段 | v2 字段/处理 |
| --- | --- |
| `stage00_remote_corpus` | `stage00`，字段大部分保留 |
| `stage01.workers` | `stage01.identity_workers` |
| `stage04_supplementary_acquisition` | `stage01.supplementary_acquisition` |
| `grobid` | `stage02.parsers.grobid` |
| `mineru` | `stage04.mineru`，仅处理工具箱/资源门控通过论文 |
| `stage06_supplementary_extraction` | 合并到 `stage02` |
| `stage03_computation_relevance.llm` | `models.screening` + `stage03` prompt config |
| `softcite` | `stage04.softcite` |
| `stage05_preliminary_coverage` | `stage04.coverage_policy` |
| `resource_interpretation/resource_limits` | `stage04.resource_extraction` + `resource_budget` |
| `stage07.agent` | `models.builder` 和 `stage06` |
| `stage08.agent` | `models.judge` 和 `stage07` |

不得继续使用 `config.py` 中“是否存在 `pdf_directory`”来判断新旧配置类型。v2 以 `pipeline_contract`
显式选择配置解析器。

## 6. 缓存迁移矩阵

| 旧产物 | 可否复用 | 条件 |
| --- | --- | --- |
| 原始正文 PDF | 是 | hash 和来源可审计 |
| 原始 SI | 是 | hash、MIME 和 paper mapping 重新验证 |
| Stage 01 PDF metadata/hash | 是 | 文件 hash 未变 |
| GROBID TEI/text | 部分 | 仅作为 v2 fallback attempt，parser 版本一致 |
| MinerU 原始结果 | 是 | PDF/model/config/commit hash 一致且新质量门通过 |
| `pdftotext` 文本 | 部分 | Poppler 和命令参数一致 |
| 旧 Stage 03 rule spans | 部分 | 能重映新 content block/evidence ID |
| 旧 Stage 03 LLM cache | 否 | prompt 语义不兼容 |
| Stage 04 下载 attempts | 是 | 作为 acquisition audit，不自动决定 package 完整性 |
| Stage 05 Softcite raw | 是 | document/Softcite model/config hash 一致 |
| Stage 05 coverage decision | 否 | 能力和角色语义已改变 |
| 旧资源模型 response | 否 | 旧 scope/range/error 语义不安全 |
| Stage 06 SI evidence bundle | 部分 | 原始解析产物可导入，决策不可导入 |
| Stage 07 candidate | 否 | 单任务 schema 与任务对不兼容 |
| Stage 08 audit | 否 | 未包含 paired-mode 和 Gold Run |

所有导入记录写明：

```json
{
  "imported_from": {
    "pipeline_contract": "legacy",
    "run_path": "...",
    "artifact_path": "...",
    "artifact_hash": "...",
    "adapter_version": "..."
  }
}
```

## 7. 编排迁移

### 7.1 v1 问题

当前 `screening_microbatch.py` 固定 Stage 02-06 名称和执行顺序，Stage 04 下载位于 Stage 03 后，
Stage 05 又在 Stage 06 新 SI 抽取之前，无法通过配置修复。

### 7.2 v2 调度

新的 stage registry 以名称和 contract 声明依赖：

```text
stage00 -> stage01 -> stage02 -> stage03 -> stage04 -> stage05 -> stage06 -> stage07
```

每个阶段实现统一接口：

```python
run_stage(input_manifest, output_dir, config, services) -> StageResult
load_stage(output_dir) -> StageResult
validate_stage_result(result) -> ValidationReport
```

不要让编排器知道具体 JSON 内部字段；阶段间只通过 manifest/contract 交互。

### 7.3 Resume

每个 paper 和 stage 保存：

- input signature；
- config/prompt/model/catalog hashes；
- output manifest；
- processing status；
- retry count；
- error；
- completed timestamp。

只有签名完全一致才 resume。工具箱更新只重新调度 Stage 04-07。

### 7.4 服务栈

run-level context manager 按需启动：

```text
MinerU runtime
GROBID
Softcite instance pool
screening LLM rlaunch worker
Builder/Judge clients
sandbox runtime
```

所有已启动服务在同一个 `finally` 栈中关闭。Stage 边界不关闭服务。

## 8. 测试迁移

### 8.1 单元测试

新增：

- paper identity、version 和 SI mapping；
- confirmed-no-SI 与 download-failed 区分；
- Stage02 GROBID-first、`pdftotext` 回退和 Stage04 通过后 MinerU 深解析；
- evidence ID 稳定性和 quote 回映；
- Stage 03 不包含 pure/original/no-experiment gate；
- Stage 04 used/background/core/aux 分类；
- LLM 补充 Softcite 漏项；
- LLM 不得改变 capability resolver；
- deleted backend 永不覆盖；
- resource range/less-than/greater-than/aggregate/physical-duration；
- paper-level model failure isolation；
- Stage 05 workflow DAG、三阶段、validation gate 和 scoring target；
- paired-mode leakage；
- Gold Run release gate。

### 8.2 标注集

从现有运行分层选择至少 300 篇：

- 旧 Stage 03 strong/weak/reject；
- 综述、实验计算混合、纯计算；
- SI-only 计算细节；
- Softcite 命中/漏掉/假阳性；
- 工具箱直接覆盖、未覆盖和未知；
- 十个方向尽可能覆盖；
- 多出版商和不同年份。

至少设置独立 holdout，不能全部用于 prompt 调整。

### 8.3 Shadow run

1. 20 篇 parser 与 package smoke；
2. 100 篇 Stage 00-05；
3. 500 篇 v1/v2 同源对照；
4. 只对 Stage 05 候选运行 Builder/Judge；
5. 对 Judge pass 运行 Gold Run。

对照必须报告论文级差异及证据，不能只报告通过数。

## 9. 分阶段实施计划

### Phase 0：冻结设计和基线

- 用户确认本目录设计；
- 保存当前 500 篇 run、测试结果、prompt 和能力快照；
- 确认正式评测资源预算；
- 确认模型 endpoint 和凭据变量名。

### Phase 1：contracts 和只读 adapter

- 实现公共 record headers 和 schemas；
- 实现旧 Stage 00/01/04 只读导入；
- 不改变默认入口。

### Phase 2：Stage 01 论文包闭合

- 合并 inventory 和 supplementary acquisition；
- 实现 identity/version/SI mapping；
- 20 篇多出版商测试。

### Phase 3：Stage 02 按角色解析

- 统一 parser attempts；
- 实现质量 selector 和 content blocks；
- 对正文、文本 SI、表格 SI、扫描 SI 分层测试。

### Phase 4：Stage 03/04 共用 screening LLM

- 泛化 rlaunch manager；
- 实现 Stage 03 map/reduce；
- 实现 Stage 04 inventory/audit/resolver/resource；
- 在标注集上选择 prompt、阈值和并发。

### Phase 5：Stage 05 suitability

- 实现十方向 schema 和强模型调用；
- 实现候选确定性校验；
- 人工审查候选 precision。

### Phase 6：Stage 06/07

- 实现 shared record 和两个 Builder；
- 实现 paired-mode deterministic validator；
- 扩展 Judge；
- 接入 Gold Run。

### Phase 7：完整 shadow 和切换

- 500 篇 v1/v2 对照；
- 修复 blocker；
- v2 成为默认入口；
- v1 标记 legacy read-only；
- 后续单独决定何时删除旧代码。

## 10. Git 管理

建议每个 Phase 独立提交到本地 `main`，不创建新分支，也不上传远端，直至用户确认：

```text
docs(data-pipeline): define v2 contracts and migration
feat(data-pipeline): add v2 paper package stage
feat(data-pipeline): add role-aware document normalization stage
feat(data-pipeline): add shared screening LLM stages
feat(data-pipeline): add benchmark suitability stage
feat(data-pipeline): build and audit paired tasks
test(data-pipeline): add v2 shadow and effectiveness evaluation
```

提交时只包含本 Phase 相关文件，不混入当前工作树中的 chemistry toolbox、sandbox inventory 或用户文件变化。

## 11. 回滚策略

- v2 使用独立入口、配置和 run directory；
- 在正式切换前，默认 v1 入口不改；
- v2 任一 Phase 失败时停止推进，不删除旧实现；
- 所有新服务 state 文件可独立清理；
- 不对旧 run 执行 destructive migration；
- 回滚只需切回 v1 config/entry point，不需要恢复数据文件。

## 12. 实现前必须由用户确认的项目

1. 正式 Benchmark 单任务和总任务的 CPU/GPU/内存/wall-time 预算。
2. Stage 04 对未命名实现或无法解析到活动软件 catalog 的情况采用 hold 还是 reject。
3. `complete_confirmed_no_si` 的出版商证据最低要求。
4. Stage 02 次要 SI 部分解析失败时是 hold 还是继续。
5. Stage 05 是否严格要求自主/复现两种模式都可构建。
6. D 级 ground truth 是否一律 hold。
7. Stage 07 `revise` 是否允许最多一次自动 Builder 修订。
8. Gold Run 由参考 Agent 还是人工/固定脚本执行。
