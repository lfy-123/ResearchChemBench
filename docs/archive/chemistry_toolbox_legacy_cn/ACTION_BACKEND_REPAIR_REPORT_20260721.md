# 11个失败 Action–Backend 组合修复报告

> 修复日期：2026-07-21 UTC。基线提交：`b797ed3`。

## 1. 最终状态

| 状态 | 组合数 | 说明 |
|---|---:|---|
| 已修复并真实运行成功 | 6 | Psi4 2个、CP2K 2个、GROMACS 1个、Catalysis-Hub 1个 |
| 代码侧修复完成，但被外部网络状态阻塞 | 5 | 5个 PubChem Actions；本服务器出口仍收到 `503 PUGREST.ServerBusy` |
| 本地适配器遗留失败 | 0 | 原有5个本地失败均已清除 |

当前完整覆盖统计为：101个 Actions、76个 Backends、233个组合；228个组合有成功证据，5个仅有失败证据，0个未测试。76/76个 Backends 均至少有一个成功 Action。

## 2. 逐组合处理结果

| Backend | Action | 原因 | 修复 | 现场结果 |
|---|---|---|---|---|
| `psi4` | `calculate_dipole_moment` | 使用已废弃的 `SCF DIPOLE X/Y/Z` 标量变量，且忽略新API的原子单位变化 | 读取向量变量 `SCF DIPOLE`，验证3个分量并乘 `2.541746473` 转为 Debye | **成功**，10.865 s |
| `psi4` | `calculate_orbitals` | 多不可约表示的 Psi4 Vector 不能直接转为 NumPy 数组 | 按 irrep 调用 `to_array()`，逐块展平；用 `nalphapi()/nbetapi()`按同一顺序生成占据数 | **成功**，2.604 s |
| `cp2k` | `calculate_periodic_forces` | 未显式打印力；CP2K 2026 输出带 `FORCES\|` 前缀 | 生成 `FORCE_EVAL/PRINT/FORCES ON`，解析新格式并保留旧格式兼容 | **成功**，12.400 s |
| `cp2k` | `calculate_periodic_stress` | 未显式打印应力；解析器只识别旧式 GPa 输出 | 生成 `STRESS_TENSOR ANALYTICAL` 与 `PRINT/STRESS_TENSOR ON`；解析 CP2K 2026 的 bar 输出并转换为 GPa | **成功**，6.993 s |
| `gromacs` | `propagate_dynamics` | NVE仍写入温控/压控参数；没有明确的速度初始化选择 | NVE/NVT/NPT分别生成耦合字段；要求智能体显式选择是否生成速度及随机种子；NVT/NPT要求显式温控组 | **成功**，1.572 s |
| `catalysis_hub` | `search_catalysis_records` | 远端曾出现503和读取超时 | 加入有界重试、退避、明确 User-Agent、重定向处理和 `retryable` 错误语义 | **成功**，3.164 s |
| `pubchem` | `resolve_chemical_identity` | PUG REST 503 | 见第3节 | 代码路径已修复；服务器出口仍被远端阻塞 |
| `pubchem` | `retrieve_compound_properties` | PUG REST 503 | 见第3节 | 代码路径已修复；服务器出口仍被远端阻塞 |
| `pubchem` | `retrieve_compound_structure` | PUG REST 503 | 见第3节 | 代码路径已修复；服务器出口仍被远端阻塞 |
| `pubchem` | `search_similar_compounds` | PUG REST 503 | 见第3节 | 代码路径已修复；服务器出口仍被远端阻塞 |
| `pubchem` | `search_substructures` | PUG REST 503 | 见第3节 | 代码路径已修复；服务器出口仍被远端阻塞 |

## 3. PubChem专项结论

### 3.1 与 ChemGraph 的实现对照

ChemGraph 的实现位于：

`<legacy-workspace>/ChemGraph/src/chemgraph/tools/cheminformatics_core.py`

其名称查询核心逻辑也是：

```python
comps = pubchempy.get_compounds(name, "name")
```

ChemGraph 没有使用另一套 PubChem API，也没有额外重试或缓存。只有面向 ALCF 的示例启动脚本显式设置了 ALCF 专用代理；本服务器当前没有配置 HTTP/HTTPS 代理。因此，ResearchChemBench 之前的503并不是因为与 ChemGraph 使用了不同的 PubChem 调用方式。

### 3.2 当前服务器连通性证据

最新探测记录：[`pubchem_connectivity_status.json`](../config/pubchem_connectivity_status.json)。

| 层级 | 结果 |
|---|---|
| DNS | 成功，解析到 `34.107.134.59` |
| PubChem HTTPS 首页 | HTTP 200 |
| PUG REST 单CID查询 | HTTP 503 |
| PubChemPy 名称查询 | `ServerBusyError` / HTTP 503 |
| 代理环境 | 未设置 |

PUG REST 响应头为：

```text
Retry-After: 30
X-Throttling-Control: Request Count status: Green (0%), Request Time status: Green (0%), Service status: Green (0%), too many requests per second or blacklisted
```

这说明 DNS、TCP/TLS 和普通网站访问均正常，失败发生在 PubChem PUG REST 服务层；最可能是本服务器共享出口IP处于 PubChem 动态限流或临时黑名单状态。PubChem 官方要求不超过5 requests/s，并说明503可能来自请求过多、维护或容量不足，且应稍后重试：<https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest>。

### 3.3 已完成的代码侧改进

- 全部 PubChem Actions 共用有界重试策略。
- 对 HTTP 客户端保留并遵守 `Retry-After`。
- 在 `.software_cache/pubchem/request_rate.state` 上使用跨 worker 文件锁，默认请求间隔0.25秒，使本工具箱自身低于5 requests/s。
- 完整化合物记录改由可读取限流响应头的 HTTP 客户端请求，再交给 `pubchempy.Compound` 解析，避免丢失503诊断信息。
- 503、429、超时和传输错误返回 `remote_service_unavailable` 且 `retryable=true`，不伪造成功，也不隐藏切换数据源。
- 结构检索继续保留智能体选择的相似度阈值、立体化学、电荷、同位素和记录上限。

## 4. 如何在服务器上检查 PubChem

### 4.1 一键分层检查

```bash
cd ${PROJECT_ROOT}
.tool_envs/services/bin/python chemistry_toolbox/scripts/check_pubchem_connectivity.py \
  --name water --cid 962 --timeout 20 \
  --output chemistry_toolbox/config/pubchem_connectivity_status.json
```

该脚本依次检查 DNS、HTTPS 首页、直接 PUG REST GET 和 ChemGraph 同款 PubChemPy 名称查询，并记录 `Retry-After` 与 `X-Throttling-Control`。

### 4.2 只查看官方限流响应头

```bash
curl -sS --connect-timeout 10 --max-time 30 -D - -o /dev/null \
  'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/962/property/ConnectivitySMILES,MolecularFormula/JSON'
```

重点检查状态码、`Retry-After` 和 `X-Throttling-Control`。如果仍包含 `blacklisted`，应停止连续重试并检查共享 NAT/代理出口。

### 4.3 单独复现 ChemGraph 的调用方式

```bash
.tool_envs/services/bin/python -c \
  "import pubchempy as pcp; c=pcp.get_compounds('water','name'); print(len(c), c[0].cid if c else None)"
```

### 4.4 网络侧恢复后的复测

```bash
.toolbox_env/bin/python chemistry_toolbox/scripts/run_action_gap_smokes.py --network-only
.toolbox_env/bin/python chemistry_toolbox/scripts/audit_action_test_coverage.py
.toolbox_env/bin/python chemistry_toolbox/scripts/generate_action_backend_completion_report.py
```

恢复后的目标是：233个组合成功、0个失败、0个未测试。

## 5. 验证结果

- 62个原缺口组合：62/62通过。
- 5个本地修复组合：5/5真实后端通过。
- Catalysis-Hub：真实GraphQL查询通过。
- MCP Catalog：101 Actions、76 Backends，显式选择、无自动 fallback，校验通过。
- 完整测试集：`152 passed in 414.44s`。
