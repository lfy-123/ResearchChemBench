# GoodVibes 4.3.0 Backend 实施报告

## 1. 完成结论

GoodVibes 已从原先仅支持 `derive_thermochemistry`、且错误地把频率缩放映射到 `--fs` 的 3.2 适配，升级为独立的 **GoodVibes 4.3.0 Backend**。现在提供 6 个通用 Actions、完整的结构化 JSON 解析、独立 runtime、软件原生调用指南、版本资料缓存、真实 smoke、单元测试和可迁移环境声明。

实现遵循 ResearchChemBench 的智能体自主编排目标：GoodVibes 不会选择上游量化软件，不会自动生成构象/补跑频率/改变标准态，也不会在失败后切换参数或 Backend。

## 2. 版本与资源

| 项目 | 当前值 |
|---|---|
| 软件 | GoodVibes |
| 版本 | 4.3.0 |
| 官方 tag | `v4.3.0` |
| 官方 commit | `1d5cb41547fddfcf953010dc361a21e00aad9a06` |
| Runtime | `.tool_envs/goodvibes`，Python 3.11.15 |
| 安装声明 | `goodvibes[full]==4.3.0` |
| 依赖检查 | `pip check` 通过 |
| 源码/示例缓存 | `.software_cache/goodvibes/4.3.0/source` |
| 本地资料索引 | `.software_cache/documentation/goodvibes/4.3.0` |
| 精确环境锁 | `chemistry_toolbox/environment/locks/linux-64/goodvibes` |
| Backend ID | `goodvibes` |
| License | MIT |

独立 runtime 健康检查确认 `goodvibes=4.3.0`、`numpy=2.4.6`、`pandas=3.0.3`、`pyarrow=25.0.0`、`PyYAML=6.0.3` 和 `goodvibes` 可执行文件均可用。当前 36 个已登记 runtime 全部通过健康检查。

可迁移锁包含 44 行 Conda explicit lock、85 个精确 pip requirement 及带来源类型的 pip metadata；主 manifest 已保留其他 42 个既有环境并新增 `goodvibes`，没有覆盖或丢失已有环境锁。

## 3. 新增/升级 Actions

| Action | 功能 | 真实测试 |
|---|---|---|
| `derive_thermochemistry` | 单个量化输出的 RRHO/准谐振热化学 | Gaussian 16、ORCA 6 均通过 |
| `scan_thermochemistry_temperature` | 对显式温度列表逐点产生结构化热化学 | 273.15/298.15/350 K 通过 |
| `analyze_thermochemical_ensemble` | 构象/结构集合热化学与 Boltzmann 群体 | 两成员 Gaussian 集合通过 |
| `validate_thermochemistry_inputs` | 程序、理论级别、溶剂、电荷、多重度、频率和重复结构检查 | 成功识别测试集合中的潜在重复结构 |
| `analyze_thermochemical_selectivity` | 显式标签集合的 N-way 群体和选择性 | 四成员 exo/endo 示例通过，优势标签为 endo |
| `analyze_reaction_free_energy_profile` | 智能体自编 PES YAML 的相对能量剖面 | 两节点 YAML 路径通过 |

Catalog 因此从 101 增加到 **106 个 Actions**；BackendSpec 总数仍为 **76**。Action–Backend 声明组合从 236 增加到 **241**。新增 5 个组合均有成功证据，当前总计 236 个成功组合、5 个既有 PubChem 远端失败组合、0 个未观察组合。

## 4. 核心实现

### 4.1 参数契约

智能体必须显式选择标准态、熵模型、焓模型、振动/ZPE 缩放、对称性处理和虚频策略。条件参数也由 adapter 严格验证，例如：

- Grimme/Truhlar 需要显式低频截断；Grimme 还需要转动惯量模型。
- Head-Gordon 需要显式焓截断。
- 自定义浓度需要显式浓度值。
- 小虚频翻转需要显式阈值。
- 去重启用时需要显式能量、转动常数和 nullable RMSD 阈值。
- `frequency_scale_factor` 正确映射到 `--vscal`；`--fs` 只映射熵低频截断。
- CLI 无法忠实表达的“显式频率缩放 + 独立自动 ZPE 缩放”等组合会直接拒绝，不会偷偷改成继承值。

### 4.2 结构化结果

Adapter 请求 GoodVibes schema `1.0` JSON，并保留：

- 量化程序/版本、结构、电荷、多重度、溶剂、频率和原始热化学字段；
- 按智能体选择的 H/S 模型组合计算的 `selected_thermochemistry`；
- ensemble Boltzmann、N-way selectivity、lowest-conformer selectivity 和 PES 区块；
- `goodvibes_version`、`schema_version`、精确 argv、stdout/stderr、`.dat` 与 JSON 文件。

### 4.3 三层执行结构

- 第一层：6 个常用、可验证的预定义 Actions。
- 第二层：`software_id=goodvibes`、`executable=goodvibes` 的原生命令执行，覆盖 CSV/Parquet、绘图、XYZ、CPU 汇总、media/free-space、import/export 等未预定义能力。
- 第三层：智能体可在 `goodvibes` runtime 编写 Python 分析程序，组合 GoodVibes API 或解析产物。

## 5. 测试结果

| 测试 | 结果 |
|---|---:|
| GoodVibes 实际 smoke | **7/7 通过**，覆盖 6/6 Actions |
| GoodVibes/目录/原生指南专项回归 | **25/25 通过** |
| 完整工具箱测试 | **186/186 通过**，耗时 413.69 秒 |
| MCP runtime 健康 | GoodVibes available，36/36 runtimes ready |
| Native execution smoke | `goodvibes --help` 作业正常结束 |
| Catalog validation | 106 Actions / 76 Backends / 241 pairs，通过 |

机器可读 smoke 结果位于 `chemistry_toolbox/config/goodvibes_action_smoke_status.json`。测试脚本使用临时 workspace，不会在仓库根目录遗留输出。

## 6. 文档与管理入口

- 详细调用指南：`chemistry_toolbox/docs/GOODVIBES_BACKEND_GUIDE.md`
- 软件原生指南：`chemistry_toolbox/config/native_software_guides.yaml`
- Backend/Action 契约：`chemistry_toolbox/src/researchchem_toolbox/backend_specs.py`
- 实现：`chemistry_toolbox/src/researchchem_toolbox/backends/goodvibes.py`
- Runtime：`chemistry_toolbox/config/mcp_profiles.yaml`
- 能力资料源：`chemistry_toolbox/config/software_capability_sources.yaml`
- 全工具矩阵：`chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md`

## 7. 已知边界

1. GoodVibes 是后处理器；上游量化输出缺少频率或正常终止信息时，不会伪造完整热化学。
2. Boltzmann/选择性比较需要可比理论级别；框架不替智能体决定是否接受异构理论数据。
3. `--spc` 要求约定命名的配套单点文件已存在于频率输出旁。
4. GoodVibes 4.3.0 输出 schema 标记为 `1.0`，但上游仍提示 v5 前字段可能调整，因此 adapter 记录并检查版本。
5. 预定义温度扫描接受显式浮点温度列表；原生 `--ti` 仍可用于 GoodVibes 自带的整数区间文本报告。

## 8. 复现命令

```bash
PYTHONPATH=chemistry_toolbox/src .toolbox_env/bin/python \
  chemistry_toolbox/scripts/run_goodvibes_action_smokes.py

PYTHONPATH=chemistry_toolbox/src .toolbox_env/bin/python -m pytest -q \
  chemistry_toolbox/tests/test_goodvibes_actions.py

PYTHONPATH=chemistry_toolbox/src .toolbox_env/bin/python -m pytest -q \
  chemistry_toolbox/tests
```
