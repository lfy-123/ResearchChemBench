# 前五阶段目录重构与测试报告

## 1. 工作范围

本次工作完成以下内容：

1. 按 Stage 业务、外部集成和共享基础设施重新编排 `src/`。
2. 保持 Stage 01-04 核心筛选算法不变，修正测试中暴露的边界状态问题。
3. 收紧 Stage 05 `supplementary_only`，确保只下载明确补充材料。
4. 为 Stage 05 增加按主机并发、429/5xx 重试和限流响应头处理。
5. 更新 README，只说明当前实际使用的 API 和运行时组件。
6. 使用两篇具有公开补充材料的论文完整测试 Stage 01-05，并分别测试 Stage 04、Stage 05 的跳过模式。

## 2. 新的 `src` 结构

```text
src/
├── agents/                         CLI Agent 隔离运行和会话保存
├── core/                           配置、路径、IO、日志和运行时工具
├── integrations/                   外部服务和工具适配
│   ├── grobid.py
│   ├── softcite.py
│   ├── grobid_quantities.py
│   ├── mineru.py
│   ├── pdf_fallback.py
│   ├── llm_client.py
│   ├── managed_service.py
│   ├── tei.py
│   └── http.py
├── orchestration/                  七阶段总编排
└── stages/
    ├── stage01_inventory/          清点、角色识别和去重
    ├── stage02_parsing/            GROBID 解析阶段门面
    ├── stage03_software_coverage/  软件识别和工具箱覆盖
    ├── stage04_resource_limits/    资源信息结构化和上限比较
    ├── stage05_asset_collection/   资产发现、下载、展开和解析
    ├── stage06_builder/            Builder Agent
    └── stage07_judge/              Judge Agent
```

旧的 `assets/`、`ingestion/`、`screening/`、`tasks/`、`curation/`、`delivery/` 和
`discovery/` 包已删除。总编排通过各 Stage 的稳定入口调用，不再依赖旧目录路径。

## 3. Stage 05 补充材料模式

### 3.1 实际发现流程

当 `download_scope="supplementary_only"` 时，当前流程为：

1. 从 Stage 02 TEI、正文和 MinerU 文本中保留明确 SI/ESM/MOESM 附件线索。
2. 查询 Crossref 和 DataCite 中明确的补充关系。
3. 访问 `https://doi.org/<DOI>` 对应的出版社落地页。
4. 只提取锚文本明确包含 Supplementary Information、Supporting Information、
   Supplementary Data、Supplementary Software 等含义的链接。
5. 下载附件并安全展开压缩包；压缩包子文件继承 `supplement` 角色。

该模式不会调用 OpenAlex，也不会主动扩展普通 GitHub、Zenodo、OSF 或 Materials Cloud
线索。只有出版社明确把补充材料链接指向这些仓库时，才调用对应仓库接口枚举文件。

### 3.2 `all` 模式实际使用的接口

当前代码直接适配以下接口，不依赖 `suppdata`、`citations-collector`、`zenodo_get`、
`osfclient` 等 wrapper：

| 接口 | 当前用途 |
|---|---|
| Crossref REST API | DOI 元数据和关联关系 |
| DataCite REST API | 数据 DOI、内容地址和关联标识符 |
| OpenAlex REST API | 补充学术元数据关系 |
| GitHub REST API | 解析正文明确给出的仓库并下载默认分支归档 |
| Zenodo Records API | 枚举和下载记录文件 |
| OSF API v2 | 枚举和下载节点文件 |
| Materials Cloud Archive API | 枚举和下载记录文件 |
| DOI/出版社 HTTPS 页面 | 查找明确标注的补充材料附件 |

## 4. 限流保护与大批量备选方案

### 4.1 已实现保护

新增 `integrations/http.py`，实现：

- 每个主机独立并发上限；
- `429`、`500`、`502`、`503`、`504` 有限重试；
- 优先遵守 `Retry-After` 和 `X-RateLimit-Reset`；
- 指数退避和小幅随机抖动；
- OpenAlex API key、GitHub token、OSF token、Zenodo token；
- Crossref、DataCite、OpenAlex 的联系邮箱标识；
- API 错误中的查询参数脱敏；
- DataCite 对非 DataCite DOI 返回 404 时记录为 `not_found`，不作为系统错误。

默认主要限制为：Crossref 1 并发、DataCite 2、OpenAlex 2、GitHub 2、OSF 1、Zenodo 2。

官方限制可参考：

- [Crossref REST API access](https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/)
- [DataCite API rate limits](https://support.datacite.org/docs/rate-limit)
- [OpenAlex authentication and pricing](https://developers.openalex.org/api-reference/authentication)
- [GitHub REST API rate limits](https://docs.github.com/en/rest/using-the-rest-api/rate-limits-for-the-rest-api)
- [OSF API v2](https://developer.osf.io/)
- [Zenodo developers](https://developers.zenodo.org/)

### 4.2 推荐的大批量运行策略

如果目标只是补充材料，优先使用 `supplementary_only`。它不需要 OpenAlex 和广泛仓库发现，
每篇论文通常只产生 Crossref、DataCite、DOI 落地页三类元数据请求，API 压力显著降低。

对于数百至数千篇论文，建议进一步采用：

1. 配置 `SCHOLARLY_API_MAILTO`、`OPENALEX_API_KEY` 和 `GITHUB_TOKEN`。
2. 将 `network_workers` 保持在 4 左右，不随论文数量线性放大。
3. 按出版社分批运行，避免短时间集中访问单一站点。
4. 对 `all` 模式建立持久 DOI/API 响应缓存；当前尚未实现跨运行缓存。
5. 更大规模关系发现使用 Crossref/OpenAlex/DataCite 官方快照建立本地索引，在线 API 只补查新增记录。
6. 出版社返回 403 时，将附件记为受限线索，后续通过人工下载、机构认证或出版社专用适配器补充。

当前 `asset_manifest.jsonl` 和事件日志可以用于审计，但还不是完整的下载断点恢复系统；重复运行
仍可能再次请求远程文件。这是下一步最有价值的 Stage 05 工程优化。

## 5. 测试论文

| 论文 | DOI | 选择原因 |
|---|---|---|
| Electron iso-density surfaces provide a thermodynamically consistent representation of atomic and molecular surfaces | `10.1038/s41467-024-50408-8` | Stage 03 直接覆盖；出版社提供 DOCX、PDF、XLSX、ZIP 补充附件 |
| Few-femtosecond electron transfer dynamics in photoionized donor-π-acceptor molecules | `10.1038/s41557-024-01620-y` | Stage 03 直接覆盖；出版社提供公开 Supplementary Information PDF |

测试输入只包含两篇正式论文，没有把已知补充材料提前放入输入目录，因此 Stage 05 结果来自真实
网络发现和下载。

## 6. 测试组合与结果

### 6.1 Stage 04 正常，Stage 05 仅补充材料

输出目录：

```text
runs/front5_validation_20260804/supplementary_only/outputs/
```

| 阶段 | 结果 |
|---|---|
| Stage 01 | 2 篇正式论文，0 重复，0 补充材料误入 |
| Stage 02 | 2/2 GROBID 成功；最终复跑复用已有 TEI |
| Stage 03 | 2/2 `direct_covered` |
| Stage 04 | 2/2 `no_explicit_resource`，全部放行 |
| Stage 04 模型用量 | prompt 771，completion 44，合计 815 tokens |
| Stage 05 | 2/2 `complete` |
| Stage 05 资产 | 31 个：2 个主论文，29 个 supplement |
| Stage 05 解析 | 31/31 success |
| Stage 05 线索 | 8/8 resolved |

直接下载的六个补充附件：

| 文件 | 大小 | 解析器 |
|---|---:|---|
| `41467_2024_50408_MOESM1_ESM.docx` | 79,864 B | DOCX |
| `41467_2024_50408_MOESM3_ESM.pdf` | 95,127 B | MinerU |
| `41467_2024_50408_MOESM4_ESM.xlsx` | 13,130 B | XLSX |
| `41467_2024_50408_MOESM5_ESM.zip` | 698,097 B | archive |
| `41467_2024_50408_MOESM6_ESM.zip` | 1,199 B | archive |
| `41557_2024_1620_MOESM1_ESM.pdf` | 3,569,255 B | MinerU |

两个 ZIP 在资产预算内展开并登记了 23 个子文件。没有下载 Nature 正文 HTML、正文 PDF、
GitHub 仓库、OpenAlex 资产或普通数据链接。

### 6.2 Stage 04 和 Stage 05 同时跳过

输出目录：

```text
runs/front5_validation_20260804/both_skipped/outputs/
```

- Stage 04：2/2 `decision="skipped"`，模型 token 为 0，没有启动资源解释调用。
- Stage 05：`skipped=true`，0 条线索，0 次元数据查询，0 次下载。
- Stage 05 只登记两篇主论文，解析器为 `grobid_fallback`，保持后续 Builder 接口完整。

### 6.3 Stage 04 正常，Stage 05 跳过

输出目录：

```text
runs/front5_validation_20260804/stage05_skipped/outputs/
```

- Stage 04：2/2 `no_explicit_resource`，模型正常调用，合计 815 tokens。
- Stage 05：`skipped=true`，只登记两篇主论文，没有联网、附件扫描或 MinerU 子进程。
- 结果证明 Stage 05 跳过不依赖 Stage 04 同时跳过。

## 7. 测试中发现并修复的问题

1. 嵌套配置文件无法覆盖 Stage 03 规则路径。
   已允许配置 `delft_directory`、`aliases_file`、`role_rules_file` 和
   `capability_map_file`。
2. `supplementary_only` 不主动解析出版社页面。
   已增加 DOI 落地页附件发现。
3. 与 Supplementary 文本相邻的论文 DOI/正文页面被误判为附件。
   已要求 URL 或关系本身具有明确补充材料特征。
4. 下载对象按哈希存储且无扩展名，导致 XLSX 和 MinerU PDF 解析失败。
   已在独立解析目录创建带原始文件名的符号链接，不复制原始大文件。
5. MinerU 从正文再次抽取论文自身 DOI，造成无意义 unresolved 状态。
   已忽略非 `paper_doi` 类型的自身 DOI。
6. Stage 04 在模型返回完全空结果时仍标记 `ambiguous`。
   已改为 `no_explicit_resource`；只有存在平台、聚合资源、物理时长或未解决信息时才保持
   `ambiguous`。
7. DataCite 404 被记录为失败并在日志中暴露 `mailto` 查询参数。
   已改为 `not_found` 并脱敏错误 URL。

## 8. 自动化验证

```text
pytest: 42 passed, 6 subtests passed
ruff: All checks passed
git diff --check: passed
旧模块导入检查: 0 条
```

## 9. 结论

本次重构后，代码结构已经与 Stage 语义一致，外部工具适配集中在 `integrations/`，总编排接口
保持稳定。Stage 04、Stage 05 的跳过参数均真实生效，并保持后续数据合同不变。

`supplementary_only` 已从“关键词过滤已有线索”改为真正的出版社补充材料发现模式。对于只需要
正文和 SI 的计算化学任务，这是当前更适合大批量运行的配置：调用来源少、误下载范围小，也更
容易控制 API 限额。主要剩余工程风险是出版社反爬/认证，以及缺少跨运行持久缓存和完整断点恢复。
