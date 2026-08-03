# Stage 05-07 代码修改方案

> 状态：实施基线。
>
> 原则：Stage 01-04 核心逻辑保持不变；后半段只保留 Stage 05-07。

## 1. 当前代码问题

当前数据管线在 Stage 04 之后拆分为 MinerU 队列、解析质量、文本合并、Study Bundle、
ScientificRecord、任务类型选择、包生成、质量门控、多模型审计、人工队列和数据集发布。
这些阶段存在三类问题：

1. 资产发现只记录 URL，没有形成下载、递归展开、增量解析和统一溯源闭环。
2. ScientificRecord、任务选择和包生成由多个 API 调用分段完成，容易产生跨阶段不一致。
3. 多模型审计、人工队列和发布不符合当前“Builder Agent + Judge Agent 后结束”的目标。

## 2. 保持不变的代码边界

以下 Stage 01-04 核心调用和判断规则不修改：

```text
inventory_corpus
extract_documents_with_grobid
assess_software_coverage
assess_resource_limits
```

允许的外围修改仅包括：

- 新的下游调用和输出路径。
- `stop_after` 新阶段名称。
- 阶段索引和汇总字段。
- 为新阶段传递已有字段，不改变筛选判定。

## 3. 新模块划分

### 3.1 `src/assets/`

```text
models.py       资产、线索、事件和状态 Schema
clues.py        DOI、URL、仓库、数据库编号和文件名提取
discovery.py    三轮 frontier 调度和来源适配器
download.py     下载、重试、哈希、内容寻址存储和 URL 安全
archive.py      ZIP/TAR 安全递归展开
parsers.py      文件类型识别、轻量解析和 MinerU 路由
manifest.py     asset_manifest.jsonl 和事件日志物化
stage.py        Stage 05 顶层入口
```

首版必须实现的来源：

- 本地正文和已登记附件。
- GROBID/MinerU 文本显式 DOI、URL、GitHub、Zenodo、OSF 和 Dataverse 线索。
- Crossref、DataCite、OpenAlex 元数据关系。
- GitHub API 搜索及仓库快照。
- Zenodo、OSF、Dataverse 下载。
- 通用 HTTP 文件下载。

DataStet、suppdata、citations-collector、SOMEF、Pooch、zenodo_get、pyDataverse、
waybackpy 和 ro-crate-py 通过可选适配器接入。缺少可选依赖时记录 `adapter_unavailable`，
不能影响内置主路径。

### 3.2 `src/agents/`

```text
models.py       Agent 请求、运行结果和错误 Schema
runner.py       统一 AgentRunner 接口
codex.py        codex exec 适配器
claude.py       claude --print 适配器
opencode.py     opencode run 适配器
events.py       三种 CLI 事件流解析与 token 统计
workspace.py    独立工作目录、输入快照、临时 HOME 和访问边界
transcript.py   原生事件保存、统一聊天记录和敏感信息脱敏
```

统一输入：

```text
cli
command
model
working_directory
prompt_path
schema_path
timeout_seconds
environment
```

统一输出：

```text
status
cli
model
command
started_at/finished_at/duration_seconds
return_code
session_id
input_tokens/output_tokens/cost
event_log_path
conversation_path
stdout_path/stderr_path/final_response_path
parsed_response
error
```

每次运行建立独立 `agent_runs/<run_id>/`，保存 `workspace/input`、`workspace/work`、
`workspace/output`、临时 HOME、原生事件、统一聊天记录和运行元数据。Builder 与 Judge
不共享会话或工作目录。Judge 只能读取正式候选包和显式复制的审计证据，不能读取 Builder
的聊天记录、原生事件或临时文件。

### 3.3 `src/tasks/`

```text
schemas.py      Builder 和 Judge JSON Schema
context.py      从 Stage 05 清单构造受限上下文
builder.py      Stage 06 调度、prompt 和候选包落盘
validation.py   确定性任务校验
probe.py        public-only smoke probe
judge.py        Stage 07 调度、prompt 和审计报告
```

## 4. 编排修改

`run_corpus_pipeline()` 保留 Stage 01-04 代码块，Stage 04 通过记录直接进入：

```text
run_asset_collection(...)
run_builder_stage(...)
run_judge_stage(...)
```

新增独立命令，便于复用 Stage 04 结果测试：

```text
chem-pipeline run-late-stages \
  --input resource_screened_documents.jsonl \
  --config config.json \
  --workspace runs/<name>/outputs
```

`stop_after` 支持：

```text
asset_collection
builder
judge
```

## 5. 删除范围

从主流程和 CLI 删除以下旧职责：

- 旧 Stage 05-10 MinerU 队列、质量、合并和 Study Bundle 编排。
- 旧 ScientificRecord API 增强。
- 旧任务类型分类阶段。
- 旧 package generation API 阶段。
- 旧 model ensemble。
- 人工 curation queue。
- dataset build/release 作为流水线阶段的编排。

只有确认没有新代码引用后，才删除对应模块。仍被独立工具使用且有明确价值的底层函数可保留，
但不能继续出现在主数据管线阶段中。

## 6. 配置修改

将旧 `llm.extraction/classification/generation/review` 和 `model_ensemble` 替换为：

```text
stage05
stage06.agent
stage07.agent
```

默认测试配置：

```yaml
stage06.agent.cli: opencode
stage06.agent.model: deepseek/deepseek-v4-flash
stage07.agent.cli: opencode
stage07.agent.model: deepseek/deepseek-v4-flash
```

## 7. 测试方案

### 7.1 单元测试

- URL/DOI/仓库线索抽取和规范化。
- SSRF、路径穿越和压缩炸弹保护。
- URL、SHA-256 和仓库版本去重。
- 三轮提前停止和预算耗尽。
- MinerU 成功、降级、失败和复用。
- 三种 CLI 命令构造和事件解析。
- Builder/Judge 工作空间、会话和聊天记录隔离。
- 聊天记录脱敏及原生事件持久化。
- Builder/Judge Schema 和确定性校验。
- public/hidden 泄漏检查。

### 7.2 集成测试

- 使用本地 HTTP fixture 模拟下载和递归链接。
- 使用假 Agent CLI 模拟 codex/claude/opencode 事件流。
- 复用 Stage 04 的正式论文输出执行 Stage 05。

### 7.3 真实测试

- CLI：OpenCode。
- 模型：`deepseek/deepseek-v4-flash`。
- 先运行一篇论文验证接口和输出，再扩大到可控样本。
- 实时监督 `pipeline.log`、Agent 事件、资产清单和任务审计结果。
- 任何代码错误、Schema 错误或明显偏离设计的结果都修复后重跑。

## 8. Git 策略

实施过程只提交到当前本地分支，不推送 GitHub。建议本地提交点：

1. 设计与迁移方案。
2. Stage 05 资产系统。
3. Agent CLI 和 Stage 06/07。
4. 旧代码删除与文档更新。
5. 测试修复与最终报告。
