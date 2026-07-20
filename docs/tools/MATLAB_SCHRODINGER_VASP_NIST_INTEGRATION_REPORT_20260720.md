# MATLAB、Schrödinger、VASP POTCAR 与 NIST 接入报告

> 完成日期：2026-07-20。Git 修改前基线标签：`pre-matlab-schrodinger-potcar-nist-20260720`，对应提交 `478b1d5`。

## 1. 本轮结论

| 项目 | 处理结果 | MCP 暴露状态 | 结论 |
|---|---|---|---|
| MATLAB R2018a | 两张官方 Linux ISO 已复制到 `.software_cache/matlab/R2018a/installation_media/` 并完成 SHA-256 复核 | 不暴露；仅作为 EasySpin 的宿主 runtime | 安装介质完成，合法许可证信息缺失，因此尚未安装 MATLAB |
| EasySpin 6.0.12 | 现有 toolbox 与 MATLAB 预留路径已衔接 | `runtime_only`，当前无公共原子 Action | 文件完成，执行验证仍被 MATLAB 许可证阻塞 |
| Schrödinger | 下载包已核验并隔离到 `.software_cache/schrodinger/rejected/` | 不暴露 | 下载的是 Dirac 视频编解码库，不是 Schrödinger 化学套件，不能安装为化学后端 |
| VASP POTCAR | `potpaw54.zip` 已复制、解压、逐文件索引并登记 5 个资源族 | 通过现有 `vasp` Backend 暴露为 Agent 显式选择的只读 ResourceRef | 735 个精确变体全部通过路径和 SHA-256 校验，PBE Si 真实 VASP 计算通过 |
| Q-Chem、Molpro、TURBOMOLE、CRYSTAL、WIEN2k、OpenEye | 按 operator 要求标记为无许可/暂不需要 | 明确不进入 BackendSpecs 和 MCP catalog | 已屏蔽，无需继续下载安装 |
| NIST CCCBDB | 保留为人工网页查询边界 | 不暴露 | 无公开、文档化 REST/JSON API，不增加脆弱 HTML 抓取工具 |
| NIST Chemistry WebBook | 新增 `lookup_nist_webbook_species` 原子 Data Action | 已通过统一 MCP server 暴露 | 使用官方参数化 CGI 做单物种有界查询；不声称存在 REST/JSON API |

公共目录由 44 个工具更新为 **45 个工具：40 个 Scientific Actions + 5 个 Data Actions**。BackendSpec 总数由 54 更新为 **55**，新增后端只有 `nist_webbook`。所有任务仍接收同一份完整目录，系统不按任务筛工具、不替 Agent 选择后端，也不做自动 fallback。

## 2. MATLAB 与 EasySpin

### 2.1 已缓存的官方介质

| 文件 | 缓存路径 | SHA-256 | 状态 |
|---|---|---|---|
| R2018a DVD1 | `.software_cache/matlab/R2018a/installation_media/R2018a_glnxa64_dvd1.iso` | `780717eeeaf11855a119ffe5e3e8be3443df4b1b79a2dcb04feb4c3ea7eb693e` | 源文件与缓存副本一致 |
| R2018a DVD2 | `.software_cache/matlab/R2018a/installation_media/R2018a_glnxa64_dvd2.iso` | `485467b9662b7d2f6bbf92b84b18b95fed93a9d6fc6ead4c806b1b67e9296997` | 源文件与缓存副本一致 |

下载目录中的 `Matlab2018aLinux64Crack.tar.gz` 没有被复制、打开、解压或使用。当前容器不能 loop-mount ISO；这不是主要阻塞，因为 MATLAB R2018a 离线安装本身仍需要合法的 MathWorks File Installation Key 和许可证文件，或可访问的许可证服务器。

已在 `config/auxiliary_environments.yaml` 中增加 `matlab` 宿主 runtime，并让 `easyspin` runtime 预留 `.software_cache/matlab/R2018a/install/bin`。一旦完成合法安装，审计会自动发现 `matlab` 命令，再进行 EasySpin 的真实 `pepper`/`chili` 等有界验证。

## 3. Schrödinger 包核验

下载文件：

`download/public_downloads_twice/手动下载/Schrödinger/schroedinger-1.0.11-7-x86_64.pkg.tar.zst`

包内 `.PKGINFO` 明确给出：

- 包名：`schroedinger 1.0.11-7`
- 描述：ANSI C 实现的 Dirac video codec
- 上游：`https://launchpad.net/schroedinger`
- 内容：`libschroedinger-1.0.so`、视频编解码头文件和 GTK 文档

它与商业 Schrödinger 分子建模套件没有关系。为保留审计证据，文件被复制到：

`.software_cache/schrodinger/rejected/dirac-video-codec/schroedinger-1.0.11-7-x86_64.pkg.tar.zst`

SHA-256 为 `41906fcce0eeb74edcaf50ee46635c2f336703692d956782dba7dd1f419187b7`。该包未安装，也不会通过 MCP 暴露。

## 4. VASP POTCAR 显式资源

原始归档缓存：`.software_cache/vasp/potcars/download/potpaw54.zip`，SHA-256：`e987c9d8a0789bdeac2ff7d49fa26944145b9c363b81016ba25aac0d0e0c006f`。

供应目录中的通用 README 与 MIT 模板不能证明 POTCAR 可以按 MIT 许可传播。本项目因此按更严格边界处理：所有 POTCAR 均视为 operator 提供的 VASP 许可数据，仅限本地使用，不提交 Git、不重新分发。

| Resource ID | 本地目录 | XC / 类型 | 精确变体数 | 元素数 | Agent 选择示例 |
|---|---|---|---:|---:|---|
| `vasp_uspp_lda_legacy` | `pot/USPP_LDA` | LDA / legacy USPP | 102 | 66 | `resource://vasp_uspp_lda_legacy/Si` |
| `vasp_uspp_gga_legacy` | `pot_GGA/USPP_GGA` | legacy GGA / USPP | 8 | 8 | `resource://vasp_uspp_gga_legacy/Si` |
| `vasp_paw_lda_54` | `potpaw/PAW_LDA` | LDA / PAW | 316 | 81 | `resource://vasp_paw_lda_54/Fe_pv` |
| `vasp_paw_pw91_54` | `potpaw_GGA/PAW_GGA_PW91` | PW91 / PAW | 5 | 5 | `resource://vasp_paw_pw91_54/Fe` |
| `vasp_paw_pbe_54` | `potpaw_PBE/PAW_GGA_PBE` | PBE / PAW | 304 | 96 | `resource://vasp_paw_pbe_54/Fe_pv` |

资源对象形式也可写为 `{"resource_id":"vasp_paw_pbe_54","selection":"Fe_pv"}`。工具箱不会在 `Fe`、`Fe_pv`、`Fe_sv`、GW 变体或不同资源族之间做默认选择。VASP 输入仍要求 Agent 同时明确给出每个元素的 POTCAR、`ENCUT`、k 点、XC、展宽、SCF 收敛和其他方法参数。

新增保护规则会读取已登记变体元数据；例如把 `resource://vasp_paw_pbe_54/Fe_pv` 映射到结构中的 `Si` 会在启动 VASP 前被拒绝。

真实验证：

| 用例 | VASP | ResourceRef | 参数摘要 | 结果 | 耗时 |
|---|---|---|---|---|---:|
| `vasp_paw_pbe_54_si_energy` | 6.3.2 | `resource://vasp_paw_pbe_54/Si` | PBE，ENCUT 300 eV，Gamma 1×1×1，1 CPU | success，energy=`0.25831787 eV` | 3.46 s |
| `vasp_6_3_2_testsuite_si_energy` | 6.3.2 | `resource://vasp_6_3_2_testsuite_si_potcar` | 原测试资源 | success，energy=`-0.27428657 eV` | 6.99 s |

这些数值只用于确认程序、资源解析和结果解析链可运行，不是收敛后的科学参考结果。

## 5. NIST 数据接口边界

### 5.1 CCCBDB

CCCBDB 继续保持 `manual_api_review`，不进入 MCP。原因是目前只有交互网页，没有公开、文档化的通用 REST/JSON API；项目不会把页面抓取包装成稳定 API。

### 5.2 Chemistry WebBook

新增 Data Action：`lookup_nist_webbook_species`，固定数据后端：`nist_webbook`。

输入示例：

```json
{
  "inputs": {
    "query": {
      "identifier": "7732-18-5",
      "namespace": "cas"
    }
  },
  "method_spec": {},
  "action_settings": {
    "units": "SI",
    "max_records": 1,
    "timeout_seconds": 30
  }
}
```

边界如下：

- 只访问官方 `https://webbook.nist.gov/cgi/cbook.cgi`。
- 支持 CAS、精确名称和精确分子式；名称/分子式通配符不暴露。
- 分子式查询必须由 Agent 明确指定 `match_isotopes` 与 `exclude_ions`。
- 单次最多返回 20 个物种候选，HTML 响应上限 2 MiB。
- 当前只结构化物种标识、通用元数据和页面可用数据分区，不镜像完整 NIST 数据表。
- 返回结果包含 SRD 69 引用和 NIST 权利说明入口。

实时 CAS 查询已通过：1.90 秒返回 1 条记录。官方依据：[WebBook 首页](https://webbook.nist.gov/chemistry/)、[查询指南](https://webbook.nist.gov/chemistry/guide/)、[名称查询](https://webbook.nist.gov/chemistry/name-ser/)、[分子式查询](https://webbook.nist.gov/chemistry/form-ser/)、[NIST SRD 权利说明](https://www.nist.gov/open/copyright-fair-use-and-licensing-statements-srd-data-software-and-technical-series-publications)。

## 6. 验证汇总

| 检查 | 结果 |
|---|---|
| Git 基线 | 标签 `pre-matlab-schrodinger-potcar-nist-20260720` 已建立 |
| POTCAR manifest 重放 | 5/5 资源族一致，735/735 变体一致 |
| 注册科学资源 | 27/27 通过 |
| 真实科学资源冒烟 | 24/24 通过 |
| MCP runtime / 模型 | 22/22 runtime 通过；55/55 BackendSpec 可用 |
| 公共 MCP 工具 | 45/45 注册 |
| Pytest | 71 passed |
| 在线数据源 | 4/5；NIST WebBook 通过，Catalysis-Hub 当次返回 HTTP 503 |

Catalysis-Hub 的失败是远端服务返回 503；本地 `catalysis_hub` BackendSpec、依赖和工具注册均健康，没有改用其他后端，也没有隐藏失败。

## 7. 当前仍需处理的事项

### 需要用户决定或提供

| 顺序 | 项目 | 用户需要做什么 | 收到后本项目会做什么 |
|---:|---|---|---|
| 1 | MATLAB / EasySpin | 提供合法 MathWorks File Installation Key，并提供 `license.dat`/许可证文件路径或许可证服务器信息 | 离线安装到 `.software_cache/matlab/R2018a/install`，配置 headless 启动并真实验证 EasySpin |
| 2 | Schrödinger（如果仍需要） | 提供真正的 Linux Schrödinger Suite 安装器、准确版本和合法 license server/许可证配置；当前同名包不正确 | 建立隔离 runtime，先验证供应商命令，再决定是否增加结构化原子能力 |
| 3 | CASTEP（如果仍需要） | 提供 STFC 合法发行包/许可和目标版本，或明确将 CASTEP 也暂时屏蔽 | 安装、验证并仅在有清晰原子契约时接入，不增加任意输入 runner |

### 用户不需要再处理

- Q-Chem、Molpro、TURBOMOLE、CRYSTAL、WIEN2k、OpenEye：已按要求屏蔽。
- NIST CCCBDB：按已确认的接口事实保持不暴露。
- VASP POTCAR：已完成缓存、登记、校验和真实计算。
- NIST WebBook：已完成有限 CGI 接入和实时验证。

### 项目侧后续，不要求用户下载

- Arkane 仍为 `partial`：命令和数据库存在，但当前构建的顶层导入超过 20 秒，官方 H 热化学示例曾超过 300 秒；需另行分析 runtime 性能或版本兼容性。
- Catalysis-Hub：等待远端 503 恢复后重跑在线 smoke。

## 8. 重放命令

```bash
.toolbox_env/bin/python scripts/import_vasp_potcar_library.py --check
.toolbox_env/bin/python scripts/configure_toolbox_resources.py --verify-only
.toolbox_env/bin/python scripts/run_scientific_resource_smokes.py
.toolbox_env/bin/python scripts/run_data_source_smokes.py
.toolbox_env/bin/python scripts/audit_requested_software.py --timeout-seconds 20
.toolbox_env/bin/python -m pytest -q
.toolbox_env/bin/python scripts/verify_toolbox.py --smoke
.toolbox_env/bin/python scripts/generate_tool_resource_matrix.py
```
