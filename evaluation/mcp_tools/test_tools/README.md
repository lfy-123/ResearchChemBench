# MCP 工具逐文件测试

本目录与 `../tools/` 一一对应：41 个公开 MCP 工具各有一个
`test_<tool_name>.py`。`_helpers.py` 只保存共享夹具和最小输入，不代表公开工具。

默认运行会：

- 根据 `config/mcp_profiles.yaml`，用每个工具所属的 `researchchem-*` Python
  环境运行对应测试，而不是把 41 个工具强行放进 core 环境；
- 实际执行 RDKit、ASE/EMT、xTB、CREST、cclib、PySCF、OpenMM、
  PDBFixer、MDAnalysis、Cantera、Psi4、Phonopy、Vina 和 CHGNet 等已配置后端；
- mock 无凭据的公共网络请求，使日常回归可重复；
- 对未安装/许可证后端要求返回结构化 `unavailable` 或 `error`，不能导入崩溃；
- 校验每个文件的 `TOOL_SPEC`、文件名和唯一 MCP 注册名称。

运行：

```bash
bash evaluation/mcp_tools/test_tools/run_tests.sh
```

真实测试 PubChem、RCSB PDB 和 Catalysis-Hub：

```bash
bash evaluation/mcp_tools/test_tools/run_tests.sh --live-network
```

同时刷新全工具状态报告：

```bash
bash evaluation/mcp_tools/test_tools/run_tests.sh --live-network --status-report
```

Materials Project 只有在安装 `mp-api` 并设置 `MP_API_KEY` 后才能进行真实查询；
当前测试会验证缺少凭据时返回明确的结构化不可用状态。

需要把原生 ABI RuntimeWarning 当作失败时，可以直接运行 profile runner：

```bash
.toolbox_env/bin/python scripts/run_mcp_profile_tool_tests.py \
  --warnings-as-errors
```
