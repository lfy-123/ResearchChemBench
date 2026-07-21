# Chemistry Toolbox 统一目录重构报告

> 完成日期：2026-07-21 UTC
>
> 目标：把化学工具箱的核心实现、MCP、配置、环境声明、脚本、测试和文档集中到一个边界清晰的子项目，同时不改变公开科学能力。

## 1. 最终目录

```text
ResearchChemBench/
├── chemistry_toolbox/
│   ├── src/researchchem_toolbox/
│   │   ├── actions/          # 101个Action，按9个科学领域拆分
│   │   ├── backends/         # 软件与算法适配器
│   │   ├── backend_specs.py  # 76个BackendSpec
│   │   ├── catalog.py        # 公共Catalog与提示词摘要
│   │   ├── service.py        # 统一分发器
│   │   ├── runtime.py        # 隔离运行环境调度
│   │   └── paths.py          # 统一路径发现
│   ├── mcp/                  # FastMCP Server、注册、trace与安装器
│   ├── config/               # runtime、软件和科学资源配置
│   ├── environment/          # 核心环境依赖声明
│   ├── scripts/              # 安装、审计、smoke与报告脚本
│   ├── tests/                # 工具箱专用测试
│   ├── docs/                 # 工具箱文档和状态报告
│   └── pyproject.toml        # 独立MCP/核心wheel构建入口
├── .software_cache/          # 软件本体，不进入源码树
├── .model_cache/             # 模型权重，不进入源码树
├── .tool_envs/               # 后端隔离环境，不进入源码树
└── .toolbox_env/             # 开发与审计环境
```

## 2. Action定义拆分

原来的单一 `specs.py` 已拆成9个领域模块：

- `scientific_data_interchange.py`
- `structure_and_system.py`
- `cheminformatics.py`
- `molecular_electronic.py`
- `reaction_and_kinetics.py`
- `molecular_dynamics.py`
- `periodic_and_phonons.py`
- `docking.py`
- `data_sources.py`

`researchchem_toolbox.specs` 继续作为兼容导出入口。Action顺序、字段、Backend选择策略和Catalog内容没有改变。

## 3. 兼容入口

下列旧路径现在是符号链接，不再保存第二份实现：

| 旧路径 | 规范路径 |
|---|---|
| `researchchem_toolbox/` | `chemistry_toolbox/src/researchchem_toolbox/` |
| `evaluation/mcp_tools/` | `chemistry_toolbox/mcp/` |
| `config/` | `chemistry_toolbox/config/` |
| `environment/` | `chemistry_toolbox/environment/` |
| `scripts/<toolbox script>` | `chemistry_toolbox/scripts/<toolbox script>` |
| `docs/tools/<toolbox doc>` | `chemistry_toolbox/docs/<toolbox doc>` |

旧Python导入和旧脚本命令仍可使用；新代码、文档和启动命令应优先使用规范路径。

## 4. Git版本

| 提交 | 作用 |
|---|---|
| `bdc332e` | 本次目录重构前的完整工具箱审计基线 |
| `0e4b935` | 将Action定义按科学领域拆分 |
| `4910926` | 把核心、MCP、配置、脚本、测试和文档迁入统一子项目 |

已有文档中的本地格式调整在迁移时得到保留。用户未跟踪的 `docs/tools/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX copy.md` 未被移动、修改或提交。

## 5. 验收结果

| 检查 | 结果 |
|---|---:|
| 公开Action | 101 |
| BackendSpec | 76 |
| Catalog摘要SHA-256 | `73ead83fb7c160fc410606a1283575e37ce4f5a3f990fa20e43dedf1af6244e9`，重构前后完全一致 |
| MCP注册与Artifact/trace smoke | 通过 |
| 全量Pytest | 150/150 passed，380.00秒 |
| 隔离运行环境 | 35/35 ready |
| 本地Backend健康检查 | 无意外不可用项 |
| 根项目wheel | 构建通过，无旧MCP或重复源码目录 |
| 独立chemistry_toolbox wheel | 构建通过，包含17个MCP文件和38个核心包文件 |

## 6. 推荐命令

```bash
# MCP目录与smoke
.toolbox_env/bin/python -m chemistry_toolbox.mcp.tool_manager validate
.toolbox_env/bin/python chemistry_toolbox/scripts/check_mcp_tools.py --smoke

# 完整测试
.toolbox_env/bin/python -m pytest -q \
  --junitxml=chemistry_toolbox/config/pytest_status.xml

# 运行环境检查
.toolbox_env/bin/python chemistry_toolbox/scripts/check_mcp_profile_envs.py \
  --timeout-seconds 240

# 独立构建
.toolbox_env/bin/python -m pip wheel --no-deps --no-build-isolation \
  ./chemistry_toolbox
```
