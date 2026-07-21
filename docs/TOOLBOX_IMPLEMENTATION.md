# 化学工具箱初版实现说明

> 2026-07-20 更新：旧 41 个文件式工具已经由 40 Scientific Actions、5 Data Actions 和 55 BackendSpecs 取代。当前实现报告见 `chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_REFACTOR_REPORT.md`，完整目录见 `chemistry_toolbox/mcp/TOOL_CATALOG.md`。下文旧接口说明仅作为迁移历史。

## 1. 实现范围

本版保留 ChemGraph 原有 5 个 MCP 工具，并增加 36 个逻辑工具，共 41 个公开工具。
所有公开工具都遵循“一工具一文件”：

```text
chemistry_toolbox/mcp/tools/<tool_name>.py
chemistry_toolbox/mcp/test_tools/test_<tool_name>.py
```

ChemGraph 原工具：

- `calculator`
- `extract_output_json`
- `molecule_name_to_smiles`
- `run_ase`
- `smiles_to_coordinate_file`

新增工具按能力分组如下：

- 管理：`list_toolbox_capabilities`、`check_backend_availability`；
- 数据服务：`query_pubchem`、`query_rcsb_pdb`、`query_materials_project`、`query_catalysis_hub`；
- 结构/信息学：`standardize_molecule`、`convert_structure`、`generate_3d_structure`、`generate_conformers_rdkit`；
- 构象/量化：`generate_conformers_crest`、`refine_ensemble_censo`、`run_xtb`、`run_orca`、`run_psi4`、`run_pyscf`；
- 分析/反应路径：`analyze_wavefunction`、`find_transition_state`、`run_irc`、`compute_thermochemistry`；
- 周期/催化/声子：`run_quantum_espresso`、`run_cp2k`、`run_periodic_calculation`、`run_catmap`、`run_phonopy`；
- 分子动力学：`prepare_md_system`、`run_gromacs`、`run_openmm`、`run_lammps`、`run_plumed`、`analyze_md_trajectory`；
- 动力学/对接/机器学习势：`run_reaction_kinetics`、`run_cantera`、`run_docking`、`run_mlip`；
- 结果检查：`validate_computation`。

完整参数、后端、依赖和副作用见自动生成的
`chemistry_toolbox/mcp/TOOL_CATALOG.md`。

## 2. 公共管理层

新增公共 adapter：

```text
chemistry_toolbox/mcp/adapters/runtime.py
chemistry_toolbox/mcp/adapters/http.py
chemistry_toolbox/mcp/adapters/toolbox_registry.py
```

职责分别是：

- 检测 Python 模块、可执行程序和管理员环境变量；
- 不经 shell 执行外部程序，限制超时并保存 stdout/stderr；
- 对远程 JSON/GraphQL API 做有超时的请求；
- 读取 `config/toolbox_registry.yaml` 的软件元数据。

可选后端只在工具实际调用时导入。缺少包、命令、模型、凭据或许可证时返回：

```json
{
  "status": "unavailable",
  "backend": "backend name",
  "available": false,
  "reason": "machine-readable reason",
  "manual_action": "how to configure it"
}
```

因此缺少一个大型软件不会阻塞其他 40 个工具的发现或 MCP server 启动。

## 3. 软件注册表

`config/toolbox_registry.yaml` 覆盖需求文档中的开源、远程、人工安装和许可证软件。
每个条目继承统一默认字段，并可覆盖：能力、官网、许可类别、安装方法、模块、命令、
adapter、MCP 工具、状态、失败原因和人工操作。

注册表描述“支持和配置意图”；`chemistry_toolbox/docs/TOOLBOX_STATUS.json` 则记录当前机器的实际检测和
真实 smoke 结果。两者分开可以避免把某台机器的绝对路径或凭据写入可复用注册表。

## 4. 外部程序适配规则

命令行工具统一通过 `run_external()`：

1. 只从 PATH 或审核过的 `CHEMGRAPH_*_COMMAND` 解析命令；
2. 使用参数数组和 `shell=False`；
3. 输入文件必须位于当前 benchmark workspace；
4. 输出目录必须位于允许写入区域；
5. 设置超时；
6. 保存 `stdout.log`、`stderr.log` 和结构化返回值；
7. 再由 `execute_traced()` 保存 tool trace、完整结果和 artifact 快照。

Phonopy 适配器同时兼容旧版 `phonopy -c` 和 Phonopy 4 的
`phonopy-init -c`/`phono3py-init -c`。

## 5. 测试设计

`chemistry_toolbox/mcp/test_tools/` 下有 41 个 `test_<tool>.py`，与工具文件一一对应。公共 helper 负责：

- 校验文件名、`TOOL_SPEC.name`、元数据和 `register(mcp)`；
- 对已安装的轻量 Python 后端执行最小功能输入；
- 对外部程序 wrapper 模拟安全进程边界，避免单元测试依赖许可证或大型计算；
- 对远程服务 mock HTTP 返回；
- 检查缺依赖时返回结构化状态。

真实验证另由 `chemistry_toolbox/scripts/verify_toolbox.py` 执行。它不会把“mock 单元测试通过”当作
“后端工作”，状态报告只把实际最小计算/API 请求成功记为 `正常工作`。

## 6. 增加、修改、删除工具

新增：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh scaffold new_tool \
  --description "What the tool does" \
  --category simulation \
  --backend "SoftwareName"
```

实现 `new_tool_core()` 和 `register(mcp)` 后，增加：

```text
chemistry_toolbox/mcp/test_tools/test_new_tool.py
```

然后执行：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh validate
pytest -q chemistry_toolbox/mcp/test_tools/test_new_tool.py
bash chemistry_toolbox/scripts/manage_mcp_tools.sh enable new_tool
bash chemistry_toolbox/scripts/manage_mcp_tools.sh catalog
```

临时停用、归档和恢复：

```bash
bash chemistry_toolbox/scripts/manage_mcp_tools.sh disable new_tool
bash chemistry_toolbox/scripts/manage_mcp_tools.sh archive new_tool --yes
bash chemistry_toolbox/scripts/manage_mcp_tools.sh restore new_tool
```

`registry.py` 自动发现文件，因此新增工具不需要修改 `server.py` 或中心注册函数。

## 7. 本版明确未做的事情

- 没有未经授权下载 ORCA、Gaussian、VASP 等许可证软件；
- 没有用网页抓取替代 NIST 的稳定程序接口；
- 没有自动下载未审查的 MLIP 模型；
- 没有把所有软件伪装成 ASE calculator；
- 没有修改 ChemGraph 或 ResearchClawBench 源码。

未完成后端、安装状态、失败原因和人工步骤统一见 `chemistry_toolbox/docs/TOOLBOX_STATUS.md`。

## 8. Agent 工具选择

41 个工具都能由 MCP server 注册，但不建议对每个任务无差别暴露全部 schema。实际
DeepSeek V4 Flash/OpenCode 回归表明：当前 ChemGraph 查询任务使用所需 5 工具时稳定
完成并获得 judge `score=1`；一次暴露全部 41 工具时，该模型/CLI 组合出现工具参数 JSON
解析失败。

因此 shell 入口默认使用：

```bash
--mcp-tools chemgraph-core
```

未来新任务应显式选择需要的工具，例如：

```bash
bash scripts/run_agent_eval.sh --agent opencode --task <task> \
  --mcp-tools query_pubchem,generate_3d_structure,run_xtb,validate_computation \
  --no-score
```

`--mcp-tools all` 仍可用于工具发现、能力较强的 Agent 或专门的工具选择研究。
