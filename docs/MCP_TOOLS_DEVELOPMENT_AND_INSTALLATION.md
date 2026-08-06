# MCP 化学工具的管理、扩展与维护

> 2026-07-18 更新：不再通过新增 `tools/run_*.py` 文件扩展工具箱。新增能力应修改 `ActionSpec`/`BackendSpec`、后端 handler 和 conformance test；全部 Actions 对所有任务可见。当前架构见 `chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_REFACTOR_REPORT.md`。

## 1. 当前设计解决什么问题

ResearchChemBench 将给 Agent 使用的化学能力放在：

```text
chemistry_toolbox/mcp/
```

当前实现首先考虑工具数量持续增加后的可维护性：

1. 一个公开 MCP tool 对应 `tools/` 下的一个 Python 文件。
2. 工具文件通过 `TOOL_SPEC` 自己声明名称、用途、后端和依赖等元数据。
3. `registry.py` 自动发现工具文件，不维护重复的中心工具清单。
4. `tool_config.json` 只控制启用策略和 server 文本，不重复保存工具描述。
5. 仓库采用显式 allow-list；新文件不会因为被放进 `tools/` 就立即暴露给 Agent。
6. `tool_manager.py` 统一处理创建、启用、停用、归档、恢复、校验和目录生成。
7. 工具调用使用统一的 workspace 边界、结果记录、trace 和过程文件快照。
8. 大型软件依赖在真正注册相应工具时才加载，工具发现层本身保持轻量。

这里的 MCP 层只负责把化学软件能力安全、可观测地暴露给外部 Agent。Agent 的规划和循环由 Codex、Claude、OpenCode 等 CLI 自己完成。

## 2. 目录结构与职责

```text
chemistry_toolbox/mcp/
├── __init__.py
├── models.py                 # ToolSpec 元数据契约
├── tool_config.json          # 显式启用/停用策略和 server 文本
├── registry.py               # 自动发现、导入、校验和注册
├── tool_manager.py           # 工具生命周期管理 CLI
├── TOOL_CATALOG.md           # 根据 TOOL_SPEC 自动生成的目录
├── server.py                 # FastMCP server 组装和 transport
├── workspace.py              # 输入/输出路径安全边界
├── tracing.py                # 结果、trace 和 artifact 快照
├── adapters/                 # 进程、HTTP 和软件注册表公共适配层
├── archived_tools/           # 已归档、不会被自动发现的工具文件
├── installer.py              # 可选的 Agent MCP 配置安装器
├── install.sh                # 可选的独立安装入口
├── pyproject.toml            # 独立 Python package 配置
├── README.md                 # 工具目录内的快速说明
└── tools/
    ├── __init__.py
    ├── calculator.py
    ├── run_ase.py
    ├── run_xtb.py
    ├── run_openmm.py
    ├── query_pubchem.py
    └── ...                   # 共 41 个公开工具，一工具一文件
```

职责边界如下：

| 层 | 负责内容 | 不负责内容 |
|---|---|---|
| `models.py` | 定义统一元数据结构并校验名称等基本约束 | 导入化学软件、注册 MCP tool |
| `registry.py` | 扫描文件、读取 `TOOL_SPEC`、应用启停策略、调用 `register(mcp)` | 实现具体工具、维护第二份工具元数据 |
| `tool_config.json` | server 名称、说明、显式启用和停用集合 | 工具描述、后端代码、参数 schema |
| `tool_manager.py` | 管理工具文件生命周期和生成目录 | 实现具体化学逻辑 |
| `tools/<name>.py` | 一个工具的元数据、MCP schema、输入安全处理和后端调用 | 管理其他工具或修改 server 主程序 |
| `workspace.py` | 约束文件读取和写入范围 | 解释化学参数 |
| `tracing.py` | 保存规范化调用记录、完整结果和变更文件 | Agent transcript 解析 |

## 3. 自动发现和显式启用

### 3.1 自动发现规则

`registry.py` 扫描 `chemistry_toolbox/mcp/tools/*.py`，但忽略：

- `__init__.py`；
- 文件名以 `_` 开头的内部辅助模块；
- 子目录中的实现文件，因为当前发现范围仅为 `tools/` 的直接子文件。

每个被发现的公开工具文件必须满足：

1. 文件名为 lower snake case，例如 `predict_logp.py`。
2. 文件中存在 `TOOL_SPEC = ToolSpec(...)`。
3. `TOOL_SPEC.name` 与文件名完全相同。
4. `TOOL_SPEC.name` 在全部工具中唯一。
5. 文件中存在可调用的 `register(mcp)`。
6. `description`、`category` 和 `version` 非空。

Server 的注册流程是：

```text
server.create_server()
→ registry.register_all_tools()
→ 扫描 tools/*.py
→ 导入工具模块并校验 TOOL_SPEC/register
→ 应用 tool_config.json 和环境变量启停策略
→ 只调用已启用工具的 register(mcp)
```

新增工具不需要修改 `server.py` 或 `registry.py`。

### 3.2 为什么新工具默认禁用

仓库中的 `tool_config.json` 使用显式 allow-list。当前 41 个已审核工具都被逐项列出；下面仅展示配置结构：

```json
{
  "server_name": "ResearchChem Managed Chemistry Tools",
  "server_instructions": "Use these chemistry tools inside the active workspace...",
  "enabled_tools": ["calculator", "... reviewed tool names ..."],
  "disabled_tools": []
}
```

因此，手工增加一个 `tools/new_tool.py` 时，它会被发现和展示，但在加入 `enabled_tools` 前不会注册给 Agent。`scaffold` 命令还会把新工具明确加入 `disabled_tools`。这样可以避免尚未实现、尚未安装依赖或尚未完成安全检查的工具意外上线。

`enabled_tools: ["*"]` 虽然受实现支持，但会让以后新增的文件自动启用，不适合作为本项目日常开发的默认策略。

临时运行时可以使用环境变量覆盖或补充策略：

```bash
export RESEARCHCHEM_MCP_ENABLED_TOOLS=calculator,molecule_name_to_smiles
export RESEARCHCHEM_MCP_DISABLED_TOOLS=run_ase
```

非空的 `RESEARCHCHEM_MCP_ENABLED_TOOLS` 会替代配置文件中的 enabled 集合；`RESEARCHCHEM_MCP_DISABLED_TOOLS` 会与配置文件中的 disabled 集合合并。环境变量适合单次实验，不应代替仓库中的长期配置。

## 4. ToolSpec：每个工具自己的元数据

`ToolSpec` 定义在 `models.py`，当前字段如下：

| 字段 | 必填 | 含义 |
|---|---:|---|
| `name` | 是 | 对外 MCP tool 名称，必须与文件名一致 |
| `description` | 是 | 给 Agent 的能力说明，应写清输入、输出和关键限制 |
| `category` | 是 | 管理分类，例如 `simulation`、`cheminformatics`、`utility` |
| `version` | 否 | 工具 wrapper 版本，默认 `1.0.0` |
| `backend` | 否 | ChemGraph 或外部软件名称 |
| `dependencies` | 否 | 所需 Python 包或软件依赖说明 |
| `tags` | 否 | 搜索、筛选和目录展示标签 |
| `requires_network` | 否 | 是否会访问网络 |
| `executables` | 否 | 需要调用的外部可执行文件 |
| `side_effects` | 否 | 会写文件、发请求或运行计算等副作用 |
| `deprecated` | 否 | 是否已废弃 |
| `aliases` | 否 | 迁移或检索时使用的别名 |

元数据与工具实现放在同一个文件中，可以避免修改参数或后端后忘记同步中心清单。`TOOL_CATALOG.md` 是生成物，不是元数据真源。

## 5. 一个工具文件的标准写法

下面是最小但完整的结构：

```python
"""MCP tool: compute one molecular property."""

from __future__ import annotations

from ..models import ToolSpec
from ..tracing import execute_traced


TOOL_SPEC = ToolSpec(
    name="my_property",
    description="Compute one documented molecular property from an input string.",
    category="property_prediction",
    version="1.0.0",
    backend="MySoftware",
    dependencies=("my-software-python-package",),
    tags=("molecule", "property"),
    requires_network=False,
    side_effects=(),
)


def register(mcp) -> None:
    # 可选或重量级依赖放在 register 内加载，避免阻塞工具发现。
    from my_software import predict

    @mcp.tool(name=TOOL_SPEC.name, description=TOOL_SPEC.description)
    def my_property(value: str) -> dict:
        if not value.strip():
            raise ValueError("value must not be empty")

        def call() -> dict:
            result = predict(value)
            return {"value": value, "result": result}

        return execute_traced(
            TOOL_SPEC.name,
            {"value": value},
            call,
        )
```

一个工具 wrapper 通常分成四层：

```text
ToolSpec 和 MCP description
        ↓
参数 schema 与语义校验
        ↓
workspace 路径和副作用约束
        ↓
外部软件 adapter / ChemGraph core 调用
```

不要在 wrapper 中复制一整套化学算法。可复用的软件客户端、命令构造和输出解析应放在独立 adapter 层；每个公开能力再由单独工具文件包装。

## 6. 工具生命周期管理命令

在 ResearchChemBench 根目录运行：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh <command> [arguments]
```

脚本会优先激活项目的 `.venv`，然后调用 `python -m evaluation.mcp_tools.tool_manager`。

### 6.1 查看工具

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh list
bash chemistry_toolbox/scripts/manage_mcp_tools.sh list --enabled-only
bash chemistry_toolbox/scripts/manage_mcp_tools.sh list --json
```

列表包含工具名、启用状态、分类和导入/契约错误。JSON 输出还会包含完整 `ToolSpec`，方便后续自动化管理。

### 6.2 创建新工具骨架

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh scaffold my_property \
  --description "Compute one molecular property" \
  --category property_prediction \
  --backend "MySoftware"
```

该命令会：

1. 校验名称是否为 lower snake case；
2. 创建 `tools/my_property.py`；
3. 写入 `TOOL_SPEC`、`register(mcp)` 和 `execute_traced()` 骨架；
4. 写入一个会抛出 `NotImplementedError` 的占位实现；
5. 把新工具设为 disabled。

不要在占位实现未替换、依赖未确认、测试未完成时启用工具。

### 6.3 校验

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh validate
```

校验会发现并检查工具文件的导入、名称、`TOOL_SPEC` 和 `register(mcp)`。配置文件引用不存在的工具文件也会被报告。已启用工具的错误会阻止 server 安全启动；禁用工具仍会显示其检查结果，便于在启用前修复。

### 6.4 启用和停用

完成实现和测试后启用：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh enable my_property
```

临时下线但保留源文件：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh disable my_property
```

命令会一致地更新 `enabled_tools` 和 `disabled_tools`，不要同时手工维护相互矛盾的状态。修改配置后需重启对应 MCP server/Agent 会话，正在运行的 server 不会自动热加载。

### 6.5 归档和恢复

安全归档：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh archive my_property --yes
```

归档会把文件从 `tools/` 移至 `archived_tools/`，使它退出自动发现，同时清理对应启停配置。`--yes` 用来防止误操作。

恢复：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh restore my_property
```

恢复后的文件会回到 `tools/`，但默认处于 disabled，必须重新检查后显式启用。

### 6.6 生成工具目录

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh catalog
```

该命令根据每个模块的 `TOOL_SPEC` 重新生成 `chemistry_toolbox/mcp/TOOL_CATALOG.md`。修改工具名称、描述、版本、分类、后端或依赖后应重新生成目录并提交变更。

## 7. 新增一个软件工具的推荐流程

以后增加大量化学软件能力时，对每个公开能力执行以下流程：

1. 确认一个工具只完成一个边界清楚的操作。
2. 判断是复用 ChemGraph core，还是新增独立软件 adapter。
3. 用 `scaffold` 创建默认禁用的文件。
4. 填写准确的 `ToolSpec`，尤其是依赖、网络、可执行文件和副作用。
5. 设计稳定的输入 schema；复杂结构优先使用 Pydantic。
6. 在调用后端前完成参数、单位和 workspace 路径校验。
7. 使用 `execute_traced()` 包裹真正的软件调用。
8. 为成功、非法参数、缺少依赖和后端失败分别添加测试。
9. 运行管理校验和 MCP tool-list 测试。
10. 在真实但尽量小的输入上运行 smoke test。
11. 显式启用工具并重新生成 catalog。
12. 使用至少一个 benchmark task 验证 Agent 能正确选择和调用它。

如果一个软件提供多个能力，例如“构象生成”“几何优化”“频率计算”，应创建多个工具文件。共享代码可以放在：

```text
chemistry_toolbox/mcp/adapters/<software>.py
```

或放在 `tools/_<software>_shared.py`。下划线开头的直接子文件不会被 registry 当作公开工具。

## 8. 修改、重命名和删除工具

### 8.1 修改实现或参数

修改工具自己的文件，并检查：

- MCP description 是否仍准确；
- `ToolSpec.version` 是否需要递增；
- `dependencies`、`executables`、`requires_network`、`side_effects` 是否同步；
- 参数变化是否影响任务 instruction、ground truth、scorer 或 Agent prompt；
- 返回结构是否仍能被 trace JSON 序列化；
- 新增的输出文件是否位于允许目录。

修改后至少运行：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh validate
bash chemistry_toolbox/scripts/manage_mcp_tools.sh catalog
pytest -q
```

### 8.2 重命名

工具名同时是 MCP API 名、文件名和 benchmark trace 中的标识。重命名属于破坏性变更，推荐：

1. 新建新名称的工具文件；
2. 在 `aliases` 中记录旧名称，必要时保留一个过渡 wrapper；
3. 更新 benchmark ground truth/tool mapping 和测试；
4. 启用并验证新工具；
5. 停用、归档旧工具。

不要只改 `TOOL_SPEC.name` 而不改文件名，registry 会把它判为错误。

### 8.3 删除

优先使用 `archive --yes`，确认没有任务、配置或历史复现实验依赖后，再在单独变更中永久删除归档文件和对应测试。这样比直接删除源文件更容易审查和恢复。

## 9. 懒加载和依赖隔离

工具模块顶层应尽量只导入：

- Python 标准库；
- `ToolSpec`；
- workspace/tracing 等轻量公共模块。

RDKit、ASE、MACE、TBLite、NumExpr 或外部软件客户端等可选/重量级依赖应放在工具实际执行的 core 函数内导入；`TOOL_SPEC` 元数据导入阶段不加载这些后端。当前工具均采用这一模式。

这样做的目的包括：

1. registry 可以在没有完整化学环境时读取和检查工具元数据；
2. 独立工具不会被无关的重量级依赖导入阻塞；
3. 缺少某个后端时，问题可以明确归因到相应的已启用工具；
4. 后续拆分不同软件依赖组更容易。

注意：已启用工具的 `register(mcp)` 会在 MCP server 创建时执行，因此该工具真正需要的依赖仍必须在 server 启动前安装。懒加载不是忽略依赖，而是把依赖边界放到正确工具上。

ResearchChemBench 工具直接从本仓库安装或源码运行，不需要外部源码 checkout。

## 10. Workspace、安全和过程记录

Workspace 定位顺序为：

1. `RESEARCHCHEM_MCP_WORKSPACE`；
2. `RESEARCHCHEMBENCH_WORKSPACE`；
3. MCP server 进程当前工作目录。

读取路径使用：

```python
resolve_workspace_path(path, must_exist=True)
```

写入路径使用：

```python
resolve_workspace_output_path(path)
```

默认只允许工具写入：

```text
outputs/
code/
report/
tool_logs/
```

路径穿越、workspace 外绝对路径、symlink 路径、benchmark 控制文件以及 `_tool_*` 保留位置会被拒绝。新工具不要自行使用未经检查的用户路径打开或覆盖文件。

真正的后端调用应通过 `execute_traced()` 执行。每次调用会保存：

```text
_tool_trace.jsonl
_tool_results/<sequence>_<tool>.json
_tool_artifacts/<sequence>/...
```

Trace 包含工具名、输入、状态、时间、耗时、完整结果路径、结果预览、错误和变更文件。sequence 使用持久化预留，MCP server 重启后不会从 1 开始覆盖旧结果。artifact 数量和大小可通过以下环境变量限制：

```text
RESEARCHCHEM_MCP_MAX_ARTIFACT_FILES
RESEARCHCHEM_MCP_MAX_ARTIFACT_BYTES
```

## 11. 当前工具

当前共有 41 个工具，覆盖 ChemGraph 原能力、数据服务、结构处理、量化、周期计算、声子、MD、反应动力学、对接和 MLIP。`TOOL_CATALOG.md` 是查看名称、分类、后端、依赖、网络和副作用的权威生成文档；`chemistry_toolbox/docs/TOOLBOX_STATUS.md` 是查看本机真实可用状态的权威文档。

## 12. 验证要求

常规开发验证：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh list
bash chemistry_toolbox/scripts/manage_mcp_tools.sh validate
bash chemistry_toolbox/scripts/manage_mcp_tools.sh catalog
python chemistry_toolbox/scripts/check_mcp_tools.py
pytest -q
```

涉及真实化学执行时再运行：

```bash
python chemistry_toolbox/scripts/check_mcp_tools.py --smoke
python chemistry_toolbox/scripts/verify_toolbox.py
bash chemistry_toolbox/scripts/run_toolbox_tests.sh
python chemistry_toolbox/scripts/run_data_source_smokes.py
python chemistry_toolbox/scripts/verify_toolbox.py --smoke
```

建议每个新增工具至少覆盖：

- `TOOL_SPEC` 和文件名契约；
- 未启用时不会注册；
- 正确输入的成功调用；
- 非法参数和路径被拒绝；
- 缺少依赖或后端失败时有明确错误；
- trace 和完整结果被写入；
- 预期过程文件被记录，非预期文件没有越界写入；
- MCP client 能看到启用后的 schema；
- Agent 在至少一个代表性任务上能选择该工具。

## 13. 常见问题

### 新文件出现在 list 中，但 Agent 看不到

这是显式 allow-list 的预期行为。完成实现和测试后运行：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh enable <tool_name>
```

然后重启 MCP server 或 Agent 会话。

### validate 提示文件名与 TOOL_SPEC.name 不一致

让 `tools/<name>.py`、`TOOL_SPEC.name` 和对外 `@mcp.tool` 名称保持一致。

### 一个禁用工具仍显示 import 错误

管理器会检查所有已发现文件，以便启用前发现问题；只有已启用工具的错误会阻止 server 注册。仍建议修复错误或将未维护文件归档。

### Server 启动时才提示缺少化学依赖

确认依赖导入位于该工具的 `register(mcp)` 内，并检查该工具是否已启用。已启用工具需要完整的运行依赖。

### 配置引用不存在的工具

不要仅手工删除 `tools/*.py`。使用 `archive` 会同步清理配置；若已删除，移除 `tool_config.json` 中的残留名称并重新运行 `validate`。

## 14. 独立安装与迁移附录

工具目录仍可作为独立 package 使用，但当前维护重点是工具生命周期，而不是 Agent 安装适配。

在 `chemistry_toolbox/mcp/` 中：

```bash
pip install .
```

安装后提供：

```text
researchchem-mcp-server
researchchem-mcp-install
researchchem-tool
```

源码内运行 server：

```bash
python -m evaluation.mcp_tools.server
```

独立安装后运行：

```bash
python -m researchchem_mcp_tools.server
```

`installer.py` 和 `install.sh` 保留 Codex、Claude Code 和 OpenCode 配置辅助能力。迁移时仍需携带或安装工具声明的后端依赖，但不需要外部 ChemGraph checkout。Agent API key 不应写入 `tool_config.json` 或工具源码。
