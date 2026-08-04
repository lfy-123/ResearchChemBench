# MiniChem Toolbox 最终实现与整理报告

日期：2026-08-04 UTC

## 1. 当前结果

`minichem_toolbox/` 已整理为独立、可迁移的 ARCHE Case1 类分子机理工具箱。原有
`chemistry_toolbox/`、`.software_cache/`、`.model_cache/` 和 benchmark 其他代码未被修改。

当前状态：

- 37 个预定义 Action；
- 18 个 Backend，健康检查全部可用；
- 7 个原生软件接口；
- 1 个物理 Conda 环境 `.envs/minichem`；
- 8 个逻辑运行时，共享同一环境；
- Codex、Claude、OpenCode 三套隔离 harness；
- 所有受版本管理的配置均使用相对路径；
- 13 个自动化测试全部通过。

## 2. 整理后的目录

```text
minichem_toolbox/
├── README.md
├── TOOLBOX.md
├── environment.yml
├── requirements.txt
├── pyproject.toml
├── config/
├── docs/software/
├── scripts/
├── src/
│   ├── minichem_toolbox/
│   └── minichem_mcp_tools/
├── tests/
│   ├── harnesses/
│   └── test_*.py
├── .envs/minichem/
├── .mini_software_cache/
└── .mini_model_cache/
```

`environment.yml` 和 `requirements.txt` 是应纳入 Git 的复现声明，因此位于根目录；
`.envs/` 只存放本机生成的 Conda 环境。旧的 runtime pack、环境 manifest 和打包脚本已删除。

## 3. 删除内容

删除的主要内容包括：

- 分布式资源池、远程 worker、sandbox RPC、代理和远程启动器；
- 独立异步 Action supervisor 和未使用的 MCP adapter；
- 旧安装器、生成式工具目录、包目录 README 和重复工具目录；
- runtime pack 及其生成脚本；
- 空的辅助环境、软件下载状态、资源注册表等配置；
- 与材料 MLIP 相关且不属于 MiniChem 范围的 Backend 文件；
- 历史 `tests/results/`、无用 fixture、空 tests 包；
- Gaussian smoke 输出和上游测试集；
- Multiwfn 下载归档和上游示例集；
- Python bytecode、editable metadata 和可重建语义索引。

运行时仍保留真正需要的 Gaussian 程序树、Multiwfn 可执行文件、Conda 依赖和 MiniLM 模型。

## 4. 三层能力

### 预定义 Action

保留结构准备、构象、xTB/Gaussian 电子结构、振动、热化学、过渡态、反应路径和结果解析等
37 个稳定 Action。Agent 必须明确选择 Backend 和科学参数，不存在静默回退。

### 原生软件

保留 Gaussian、CREST、xTB、Open Babel、pysisyphus、GoodVibes 和 Multiwfn。Agent 可以自己编写
输入文件，执行器负责命令白名单、资源限制、异步状态、日志、产物和哈希记录。

### Python 程序

Agent 可在同一个 Conda 环境中使用 cclib、RDKit、ASE、QCElemental、NumPy、SciPy 等库，通过
`researchchem_job.JobContext` 读取声明输入并登记输出。

## 5. 环境与缓存

| 内容 | 相对位置 | 当前规模 |
| --- | --- | ---: |
| Conda 环境 | `.envs/minichem/` | 约 3.8 GiB |
| Gaussian 与 Multiwfn | `.mini_software_cache/` | 约 12 GiB |
| MiniLM 模型 | `.mini_model_cache/` | 约 23 MiB |

语义模型为 `sentence-transformers/all-MiniLM-L6-v2`。Gaussian 是商业软件，必须由使用者从合法
安装中提供，不能通过本工具箱重新分发。

复现命令：

```bash
bash scripts/bootstrap.sh
```

该脚本根据根目录环境声明创建或复用 `.envs/minichem`，安装 editable 包并运行验证。

## 6. Agent Harness

三套入口位于 `tests/harnesses/`：

```bash
bash tests/harnesses/run_codex.sh
bash tests/harnesses/run_claude.sh
bash tests/harnesses/run_opencode.sh
```

每次运行会创建独立工作区，保存聊天事件、stderr、CLI 状态、MCP 工具结果、输入文件、计算产物
和最终报告。`tests/results/` 是运行时目录，已被 Git 忽略，不再保存历史样例结果。

## 7. 清理后测试

自动化验证：

- `pytest tests -q`：13 passed；
- `scripts/verify_minichem.py`：37 Actions、18 Backends，0 个不可用；
- `minichem_mcp_tools.tool_manager validate`：9 个发现/调度工具、17 个开放执行工具、7 个原生指南；
- `MINICHEM_PIP_OFFLINE=1 bash scripts/bootstrap.sh`：已有环境离线复用成功；
- 从 `/tmp` 启动 MCP：成功。

真实计算验证：

- xTB/GFN2 水分子单点能成功，结果为 `-5.065772968305 hartree`；
- Gaussian 16 B3LYP/6-31G(d) 水分子单点作业成功，返回码 0；
- Gaussian 作业使用独立 `.tmp/gaussian` scratch，不再依赖旧远程 scratch 代码。

此前完成的 OpenCode + `deepseek-v4-flash` 三层端到端测试仍证明 Agent 能够完成 Action、Gaussian
原生输入和 cclib Python 分析；该历史工作区已按本次精简要求删除，不再作为项目文件保存。

## 8. 边界

- 工具箱针对小分子机理任务，不是材料、高通量、分子动力学或完整多尺度平台；
- Gaussian 的科学输入仍由 Agent 负责，工具箱不会自动决定 functional、basis、溶剂、构象或 TS；
- `JobContext` 是路径和审计辅助，不是操作系统级安全沙箱；
- Conda 环境建议在迁移目标上依据 `environment.yml` 重建，不建议直接复制前缀；
- Gaussian 和 Multiwfn 二进制需要与目标操作系统和 CPU 架构兼容。

## 9. 主要文档

- `minichem_toolbox/README.md`：安装、缓存、迁移和 Agent 接入；
- `minichem_toolbox/TOOLBOX.md`：三层架构、Action、Backend 和执行流程；
- `docs/mini_toolbox/IMPLEMENTATION_LOG.md`：逐步实现记录；
- `docs/mini_toolbox/FINAL_REPORT.md`：当前最终报告。

本次变更仅保存在本地 Git，不推送远程仓库。
