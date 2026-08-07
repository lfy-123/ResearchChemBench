# ResearchChemBench 化学工具箱渐进式发现重构报告

日期：2026-07-22  
核心实现提交：`dfc5b21 Add progressive chemistry toolbox discovery`

## 1. 结论

化学工具箱已经从“每轮预加载全部 Action 工具与长说明”改为默认的渐进式发现模式，同时保留 `full` 兼容模式用于回归和严格 A/B 对照。

重构后的默认 MCP 首屏由 119 个工具降为 20 个：

- 7 个目录发现/显式 Action 执行工具；
- 13 个软件原生执行与可编程分析原语。

全部 106 个 Action、76 个 Backend 和 27 个注册科学资源仍然对每个任务完整可见。系统没有引入任务分类路由、候选推荐、自动 Backend 选择、默认参数补全、失败回调、自动重试或自动 fallback。

在同一任务、同一 DeepSeek V4 Flash 模型、同一 API URL/key、同一当前代码环境下进行 `full` 与 `progressive` A/B 测试，结果如下：

- 总记录 token：减少 **55.10%**，约 **5.51 成**；
- 首轮模型 token：减少 **86.84%**，约 **8.68 成**；
- 非缓存输入 token：减少 **79.23%**，约 **7.92 成**；
- cache-read token：减少 **50.55%**，约 **5.05 成**；
- 首屏 MCP schema 字符数：减少 **94.41%**，约 **9.44 成**。

两种模式均正确完成了 SO₂/MACE 几何优化，得到相同能量 `-16.815807706 eV`；与任务参考值 `-16.815808019 eV` 的绝对差为 `3.13×10^-7 eV`。

## 2. 重构目标与边界

本次重构遵守以下约束：

1. Agent 仍然自主决定科学计划、Action 顺序、Backend、软件、方法、资源、参数、失败恢复和停止条件。
2. 每个 benchmark 任务面对同一个完整 Catalog，不按任务内容裁剪工具。
3. 渐进式发现仅改变“schema 何时进入上下文”，不改变可用能力集合。
4. 不新增 `run_ase` 一类预编排流程工具。
5. `execute_action` 只是显式 Action ID 的统一传输入口，不制定科学流程，也不自动选择 Backend。
6. 预定义 Action、软件原生执行和 Agent 编写程序三层仍然并列存在。
7. 所有执行继续保留真实 Action ID、Backend、输入参数、ArtifactRef 和 provenance。

## 3. 新的分层发现结构

```text
L0 任务 system prompt
   └─ 领域名称、数量、发现协议、三层执行规则
        │
        ▼
L1 紧凑目录发现
   ├─ list_action_domains：一次返回按领域分组的全部 action_id
   ├─ search_actions：Agent 自己提供关键词/领域/Backend 过滤条件
   └─ search_resources：Agent 自己提供资源过滤条件
        │
        ▼
L2 精确契约检查
   ├─ inspect_action：Action 输入、选择策略、Backend 专用必填字段
   ├─ inspect_backend：一个 Backend 的全部 Action 能力、环境与资源
   ├─ inspect_resource：一个资源的完整选择语法与元数据
   ├─ inspect_software：一个软件的安装状态与 reviewed invocation guide
   └─ search_software_documentation：按需读取本地缓存文档
        │
        ▼
L3 Agent 显式执行
   ├─ execute_action：执行一个明确 action_id
   ├─ submit_native_job：执行 Agent 编写的原生软件输入
   └─ submit_analysis_program：执行 Agent 编写的分析程序
```

### 3.1 L0：不再预加载完整 Action 说明

旧模式会把全部 Action 名、Backend 健康状态和资源说明写入 `INSTRUCTIONS.md`，同时 FastMCP 又把 106 个 Action 的详细 schema 和长描述发送给模型。

新模式的 L0 只包含：

- 9 个科学领域及 Action 数量；
- 完整 Catalog 的总数；
- 中立发现工具的使用规则；
- `execute_action` 的统一请求字段；
- 软件原生执行和可编程分析层的入口说明；
- 禁止自动选择、默认补全和 fallback 的规则。

### 3.2 L1：完整但紧凑的名称索引

`list_action_domains` 默认一次返回全部 106 个 `action_id`，按 9 个领域分组。这里只返回名称，不加载每个 Action 的长 schema。

`search_actions` 支持 Agent 显式指定：

- `query`；
- `category`；
- `backend_id`；
- `action_kind`；
- `available_only`；
- `limit/offset`。

结果按稳定 Action ID 顺序返回，不进行相关性排序或任务推荐。搜索增加了通用的确定性词形归一，例如 `optimization` 能匹配 `optimize`；它不包含化学任务同义词表，也不推断任务意图。

### 3.3 L2：按需加载精确契约

`inspect_action` 返回：

- ActionSpec；
- 输入语义、必填和可选输入；
- provider selection policy；
- Backend 列表及健康状态；
- Backend 专用 `inputs`、`method_spec` 和 `action_settings` 必填字段；
- 允许值；
- component backend 角色；
- 资源、环境和参数说明。

当 Action 有很多 Backend 时，第一次检查返回紧凑 provider 摘要；Agent 可再次传入 `backend_id` 获取该 Backend 的完整契约，避免把所有 Backend 的重复说明一次性注入上下文。

### 3.4 L3：统一入口不改变科学语义

默认模式不再为每个 Action 注册独立 MCP tool，而是注册一个 `execute_action`：

```json
{
  "action_id": "optimize_geometry",
  "backend_id": "mace",
  "component_backends": {},
  "source_id": null,
  "inputs": {},
  "method_spec": {},
  "action_settings": {},
  "resource_limits": {}
}
```

这个入口仍调用原有 `researchchem_toolbox.service.execute_action`。验证规则、Backend worker、ArtifactRef 和结果结构没有改写。

轨迹记录使用真实 `action_id`，而不是记录成笼统的 `execute_action`。因此评分、审计和 provenance 仍然能看到 `generate_3d_structure`、`optimize_geometry` 等真实科学行为。

## 4. MCP 工具表面变化

### 4.1 默认 progressive 模式

目录与 Action 执行工具：

1. `list_action_domains`
2. `search_actions`
3. `inspect_action`
4. `inspect_backend`
5. `search_resources`
6. `inspect_resource`
7. `execute_action`

原生软件与可编程分析工具保持不变：

1. `list_software`
2. `inspect_software`
3. `search_software_documentation`
4. `write_workspace_text`
5. `read_workspace_text`
6. `validate_native_job`
7. `submit_native_job`
8. `list_analysis_runtimes`
9. `submit_analysis_program`
10. `get_execution_job`
11. `collect_execution_job`
12. `cancel_execution_job`
13. `declare_scientific_artifact`

总计：20 个首屏 MCP 工具。

### 4.2 full 兼容模式

`full` 模式继续注册：

- 106 个独立 Action MCP tool；
- 13 个原生/可编程执行工具。

总计：119 个工具。该模式用于回归、历史复现和 token A/B，不再是默认模式。

使用方式：

```bash
# 默认渐进模式
bash scripts/run_agent_eval.sh --agent opencode --task ChemGraph_005 \
  --tool-discovery-mode progressive --no-score

# 历史全量模式
bash scripts/run_agent_eval.sh --agent opencode --task ChemGraph_005 \
  --tool-discovery-mode full --no-score
```

批量 YAML 也可设置：

```yaml
tool_discovery_mode: progressive
```

## 5. 静态上下文体积

| 项目 | full | progressive | 降幅 |
|---|---:|---:|---:|
| 首屏 MCP 工具数 | 119 | 20 | 83.19% |
| MCP `list_tools` schema 字符数 | 482,034 | 26,960 | 94.41% |
| ChemGraph_005 `INSTRUCTIONS.md` | 37,284 B | 6,549 B | 82.43% |
| 完整 `_toolbox_catalog.json` 审计快照 | 416,428 B | 416,446 B | 不适用 |

`_toolbox_catalog.json` 仍完整写入 workspace，用于冻结运行时 Catalog、健康状态、hash 和事后审计；progressive 模式不会把这 416 KB 文件自动放入模型上下文。Agent 只能通过发现工具按需读取 Catalog 事实。

## 6. 同环境真实 A/B 测试

### 6.1 任务

任务：`ChemGraph_005`

> Run geometry optimization for sulfur dioxide and report its energy using the mace_mp calculator with the medium-mpa-0 model.

共同条件：

- Agent：OpenCode；
- 模型：DeepSeek V4 Flash；
- provider：当前 `bailian` OpenAI-compatible route；
- 相同 URL、key、任务数据、工具箱代码和 Backend 安装；
- 不调用 LLM judge，以免把 judge token 混入 Agent token；
- token 从各 workspace 的 OpenCode SQLite `message.tokens` 聚合。

### 6.2 对照 workspace

- full：`workspaces/cli_runs/batch_20260722_062333_c5ec8e/ChemGraph_005_opencode_20260722_062333_6dd566`
- progressive 最终版：`workspaces/cli_runs/batch_20260722_063810_52eaf0/ChemGraph_005_opencode_20260722_063810_fad10e`

### 6.3 Token 结果

| Metric | full | progressive | 降幅 |
|---|---:|---:|---:|
| 总记录 token | 860,623 | 386,455 | **55.10%** |
| 非缓存输入 token | 142,856 | 29,677 | **79.23%** |
| cache-read token | 715,904 | 354,048 | **50.55%** |
| cache-write token | 0 | 0 | N/A |
| 输出 token | 1,159 | 1,906 | -64.45% |
| reasoning token | 704 | 824 | -17.05% |
| 首轮总 token | 140,430 | 18,474 | **86.84%** |

总 token 仍下降 55.10%，即使 progressive Agent 因发现和自主恢复执行了更多轮次。主要收益来自避免在每轮上下文中重复携带 106 个 Action schema。

输出 token 略增是预期现象：Agent 需要输出发现调用和检查结果。增加量只有 747 token，远小于输入侧减少的 474,168 token。

### 6.4 轨迹对比

| 指标 | full | progressive |
|---|---:|---:|
| 模型步骤 | 6 | 14 |
| MCP 调用 | 4 | 13 |
| Catalog discovery 调用 | 0 | 7 |
| 预定义 Action 调用 | 3 | 3 |
| 失败调用 | 0 | 1 |

full 的科学 Action：

1. `standardize_structure`
2. `generate_3d_structure`
3. `optimize_geometry`

progressive 的成功科学 Action：

1. `generate_3d_structure`
2. `optimize_geometry`（CPU 成功）

progressive 中唯一失败调用是 Agent 明确选择 `device=cuda` 和 `gpu_count=1`，而当前运行节点没有可用 CUDA。框架没有改参数、没有回调到 CPU，也没有自动重试。Agent 阅读错误后自行再次调用 `optimize_geometry`，显式改为 `device=cpu` 并成功。这是可观察的 Agent 决策与恢复，不是隐藏 fallback。

### 6.5 科学结果一致性

| 来源 | 优化能量 |
|---|---:|
| full | `-16.8158 eV` |
| progressive | `-16.815807706029652 eV` |
| benchmark 参考值 | `-16.815808019358535 eV` |

progressive 与参考值绝对差：`3.1333×10^-7 eV`，远低于 benchmark 5% 数值容差。结构、模型、Backend 和优化设置均符合任务要求。

## 7. 辅助旧轨迹对比

历史修改前 workspace：

`workspaces/cli_runs/batch_20260721_121653_4c5925/ChemGraph_005_opencode_20260721_121653_283e8c`

该轨迹总 token 为 782,949，首轮为 127,548。与第一轮 progressive 实现的 368,493/18,503 相比，总 token 降低 52.94%，首轮降低 85.49%。由于历史轨迹使用了修改前的 provider 路由，这组结果只作为旁证；正式结论采用第 6 节的同环境 A/B。

## 8. 测试与验证

已完成：

- progressive MCP stdio 握手；
- 20 个工具枚举；
- 目录、Action 搜索、Backend 检查、资源搜索与资源检查；
- progressive `execute_action` 成功执行 QCElemental Action；
- 真实 Action ID trace 保留；
- full 兼容模式 119 工具枚举；
- TaskRunner prompt、MCP 配置和 workspace Catalog 模式验证；
- OpenCode model I/O 轨迹加入 `tool_catalog_delivery`；
- token 聚合与对比工具；
- 全量 pytest：第一次核心实现后 **217 passed**；
- 最后一轮 L0 Action ID 索引与词形匹配针对性测试：**30 passed**。

可复现 token 对比：

```bash
.toolbox_env/bin/python -m evaluation.provenance.token_usage \
  <full-workspace> <progressive-workspace>
```

## 9. 启动异常记录

第一次 progressive OpenCode 提交在模型调用前出现一次瞬时 `JSON Parse error: Unrecognized token NUL`：

- workspace：`workspaces/cli_runs/batch_20260722_060549_b6482d/ChemGraph_005_opencode_20260722_060549_3dc664`；
- model step：0；
- MCP 调用：0；
- 化学计算：0。

独立检查结果：

- progressive MCP stdio 初始化、`list_tools` 和 `list_action_domains` 均成功；
- API 普通 JSON 请求成功；
- API SSE 流式请求成功，响应无 NUL 且每行 JSON 合法；
- 随后相同配置重试成功。

因此该失败没有纳入 token A/B，也没有证据表明它由 progressive MCP schema 或化学 Backend 引起。当前保留原始失败 workspace 便于审计。

## 10. 主要代码变更

- `chemistry_toolbox/src/researchchem_toolbox/catalog.py`
  - discovery mode 解析；
  - Catalog schema v6；
  - compact progressive overview；
  - full/progressive prompt 兼容。
- `chemistry_toolbox/src/researchchem_toolbox/discovery.py`
  - 完整目录、Action、Backend 和资源的中立查询逻辑。
- `chemistry_toolbox/mcp/discovery_models.py`
  - 渐进发现与统一 Action 执行的 Pydantic 请求模型。
- `chemistry_toolbox/mcp/discovery_tools.py`
  - FastMCP 发现工具；
  - 真实 Action ID trace 的统一 dispatcher。
- `chemistry_toolbox/mcp/registry.py`
  - `register_progressive_tools`；
  - `register_public_tools`；
  - full 兼容注册。
- `chemistry_toolbox/mcp/server.py`
  - `--discovery-mode progressive|full`。
- `evaluation/run_task.py`
  - 模式写入 MCP 环境、Catalog、prompt 和 `_meta.json`。
- `evaluation/instructions_tmpl.py`
  - 去除“必须预先收到全部独立 schema”的旧协议。
- `evaluation/model_io.py`
  - 记录 Catalog 的实际 delivery mode。
- `evaluation/trace.py`
  - 分别统计 discovery、Action 与 open-execution 调用。
- `evaluation/token_usage.py`
  - 从 OpenCode SQLite 聚合并比较实际 token。
- `scripts/run_agent_eval.sh`
  - 新增 `--tool-discovery-mode`。

## 11. 已知权衡与后续建议

1. progressive 会增加少量目录调用和模型输出，但输入侧节省远大于这些开销。
2. 单次 Agent 运行具有随机性；本报告使用同环境 A/B，并保留全部 workspace，但更稳健的统计应在 10–30 个不同领域任务上重复运行。
3. 建议后续报告同时给出：首轮 token、总 token、cache-read、模型步骤和发现调用数，不能只看一个指标。
4. 可以继续增加一个紧凑、任务无关的运行节点资源查询，让 Agent 在选择 CPU/GPU 前获得客观硬件事实；不能由系统替 Agent 改写 `device`。
5. 不建议动态隐藏“看起来不相关”的 Action，因为这会把 benchmark 从评估 Agent 编排能力变成评估系统路由器。

## 12. 最终判断

此次重构实现了真正的渐进式加载：完整能力空间不变，首屏 token 大幅下降，Agent 仍需自行发现、检查、选择和执行科学工具。

对于本次真实任务，总 token 减少约 **5.5 成**，首轮 token 减少约 **8.7 成**；科学结果与完整模式和 benchmark 参考答案一致。该结构适合作为 ResearchChemBench 后续开放式、多软件计算化学任务的默认工具暴露方式。
