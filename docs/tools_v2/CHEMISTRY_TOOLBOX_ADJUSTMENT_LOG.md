# Chemistry Toolbox Adjustment Log

更新时间：2026-08-06

## 结论

- 请求软件清单现有 58 项：57 项 `configured`，1 项 `specification`（QCSchema，不是独立软件），没有 `partial`、`manual review` 或 `not found`。
- 本轮指定排查的软件均已达到可命令调用状态；AiiDA daemon 是唯一有意未启用的可选组件，不影响本地同步工作流。
- NIST CCCBDB 不纳入工具箱，不开发网页爬取接口。它不是论文复现任务的必要执行软件，且无稳定公开 API；现有 NIST WebBook 已承担受控的单分子参考数据查询。
- 本文件对应“化学工具箱清理简化版”Git 快照；准确提交号以仓库历史为准。

## 版本范围

- Git 快照包含软件清单清理、runtime/profile 配置、环境 YAML、lock/freeze、审计脚本、原生软件手册、smoke 输入和回归测试。
- `.software_cache` 和 `.model_cache` 只向 Git 提交 README、布局配置、校验元数据和目录占位；软件/模型二进制、许可证文件、伪势、实算输出及 `.envs` 本机环境仍不进入 Git。
- `reaction-kinetics/environment.yml` 固定 `censo==2.1.2`、`CoolProp==8.0.0` 和 `numdifftools==0.9.42`；`general-modern-openmpi5/environment.yml` 固定 SHARC 所需的 `numba==0.66.0`、`llvmlite==0.48.0`、`netCDF4==1.7.4`、`cftime==1.6.5` 和 `threadpoolctl==3.6.0`。

## 已完成调整

### RMG CLI 与 Arkane

- 将 `CoolProp` 固定为 8.0.0、`numdifftools` 固定为 0.9.42，消除导入卡顿和 NumPy 1.26 不兼容。
- `rmg.py --help`、`Arkane.py --help`、RMG superminimal 机理生成和 Arkane H 热化学实例均通过。

### AiiDA

- 已初始化 SQLite profile `researchchembench`，本地同步 `run` 可用，真实 `calcfunction` 计算得到 2 + 3 = 5，process state 为 `finished`。
- 未安装 RabbitMQ，也不启动 daemon。AiiDA 官方说明中 broker 只对 daemon、`submit`、暂停/恢复/终止后台任务必需；当前 Benchmark 的受限本地任务无需它。[官方安装说明](https://aiida.readthedocs.io/projects/aiida-core/en/stable/installation/guide_quick.html)

### CENSO

- 新增独立 `censo` runtime，配置 CENSO 2.1.2、ORCA 6.1.1、xTB 和与 ORCA 匹配的 OpenMPI 4.1.8。
- `.censo2rc` 中所有电子结构阶段改用 ORCA，避免依赖已删除的 TURBOMOLE。
- 两构象 PBE-D4 prescreen 实算完成，输出 `CENSO all done`。
- `.software_cache/censo/home/.censo2rc` 含绝对路径，迁移服务器后必须按新根目录重写。[CENSO 配置说明](https://xtb-docs.readthedocs.io/en/latest/CENSO_docs/censorc.html)

### SHARC 与 Newton-X

- SHARC runtime 增加 `numba`、`netCDF4`、`threadpoolctl`，补齐 `source/lib` 的 `PYTHONPATH`，配置 ORCA 6.1.1、OpenMolcas 25.10 和匹配的 OpenMPI。
- SHARC-ORCA H2 能量/梯度接口实算完成；PySHARC 仍为可选项，文件式 SHARC 轨迹不依赖它。[SHARC 手册](https://sharc-md.org/wp-content/uploads/2025/05/SHARC_Manual.pdf)
- Newton-X 配置 ORCA、OpenMPI 和软件包自带的 CIOVERLAP；1.5 fs ORCA-TDDFT 非绝热轨迹通过，日志为 `Normal termination of Newton-X`。[Newton-X 下载说明](https://newtonx.org/download/)

### Wannier90 与 Yambo

- conda 的 Wannier90 3.1.0 在真实 QE 工作流中稳定段错误；已从官方 v3.1.0 源码用本地 gfortran/OpenBLAS 重编译并置于 QE runtime 的 PATH 首位。
- QE -> `pw2wannier90.x` -> Wannier90 的 Si 四带实算完成，最终 spread 为 4.037017340 Angstrom^2，输出 `All done`。[Wannier90 下载](https://wannier.org/download/)；[QE 接口](https://wannier.org/pwscf-interface/)
- 为 Yambo 下载 NIST/QE 官方 norm-conserving `Si.pbe-rrkj.UPF`，SHA256 为 `d42702eef81fd417a503bc33e1756081d012b398c46ad9c2955aad963a1760c7`。
- 八带 QE NSCF 数据经 `p2y` 转换并完成 Yambo 初始化；四带输入因没有空带被正确拒绝。[Yambo QE 示例](https://wiki.yambo-code.eu/wiki/index.php/Bulk_material%3A_h-BN)
- `.software_cache/wannier90/3.1.0-source/make.inc` 含绝对路径，迁移后应在目标机重新生成并编译；伪势文件可直接复制。

### LOBSTER、Critic2、Multiwfn 与 VESTA

- LOBSTER 5.1.0 已完成 QE 金刚石 COHP/投影链路，absolute charge spilling 1.12%；没有缺少运行依赖，但它仍受现有许可证约束。[官方支持接口](https://schmeling.ac.rwth-aachen.de/cohp/index.php?menuID=6)
- 重新生成缺失的 `ICOHPLIST.lobster`、`COHPCAR.lobster`、`DOSCAR.lobster` 和 `POSCAR.lobster.vasp` smoke 夹具；ICOHP 断言改用 0.001 eV 绝对容差，允许 QE/LOBSTER 数值实现差异但仍检查解析结果、曲线和 spilling 门槛。
- Critic2 1.2.1081 已有源码构建和真实 QTAIM smoke；Multiwfn 2026.7.15 noGUI 已有波函数分析 smoke，二者无需再补软件。
- VESTA 的本地 GTK/Cairo/OpenGL 依赖保持有效，状态改为 `runnable_headless_gui`；命令可在 Xvfb 中启动。迁移时必须复制完整 `.software_cache/vesta/deps` 目录，不能只复制其中两个 `.so`，因为当前目录还包含 GLU、OpenGL、GStreamer/WebKit 等传递依赖及其链接。

### 清理与审计修正

- 从 requested software 中移除 CCCBDB；保留 NIST WebBook 的受限查询 Action。
- 清除能力目录中 HOOMD-blue、CCCBDB、NIST WebBook、QCSchema 四个过时的“当前不可用”标签；HOOMD-blue 和 WebBook 已可用，QCSchema 是规范，CCCBDB 已排除。
- requested-software audit 现在会应用 runtime 的 `prepend_path_entries` 与 `prepend_library_path_entries`，审计结果与实际启动环境一致。
- toolbox-resource probe 同样支持可迁移的 PATH/LD_LIBRARY_PATH 前缀；ORCA OpenMPI 4.1.8 的版本和 Fortran binding 探测由 fail 修复为 pass。
- 更新 requested software、辅助环境、MCP profile、native manual profile、生成手册、状态清单和测试断言。
- 新增可追踪 smoke 输入：`examples/integration/censo_orca_smoke`、`sharc_interfaces`、`qe_wannier_yambo`。

## 删除的软件

已从活动清单、runtime、手册和测试假设中移除 MATLAB、EasySpin、Q-Chem、Molpro、TURBOMOLE、CASTEP、CRYSTAL、WIEN2k、OpenEye 和 Schrodinger Suite。历史缓存没有物理删除；通用解析器仍可解析用户提供的外部输出，这不代表能够启动这些商业软件。

## 迁移清单

除仓库文件外，迁移时还要同步以下未由 Git 管理的内容：

- `.envs/kinetics-legacy` 中的 `censo 2.1.2`、`CoolProp 8.0.0`、`numdifftools 0.9.42`，以及 `.envs/general-modern-openmpi5` 中的 `numba 0.66.0`、`llvmlite 0.48.0`、`netCDF4 1.7.4`、`cftime 1.6.5`、`threadpoolctl 3.6.0`；优先按已提交的 `environment.yml` 和 lock/freeze 重建，不直接搬整个环境。
- `.software_cache/vesta/3.90.5a` 和完整 `.software_cache/vesta/deps`；配置要求把 `.software_cache/vesta/3.90.5a` 与 `.software_cache/vesta/deps/root/usr/lib/x86_64-linux-gnu` 放入 `LD_LIBRARY_PATH`。目标机还需要可用的 Xvfb，交互式 GUI 则需要 DISPLAY/OpenGL 图形环境。
- `.software_cache/wannier90/3.1.0-source`：目标机重新编译并更新 QE profile 路径。
- `.software_cache/resources/qe_pseudos/yambo/Si.pbe-rrkj.UPF`。
- `.software_cache/censo/home/.censo2rc`：复制后重写绝对路径。
- `.software_cache/lobster/5.1.0/smoke/qe_diamond`：包含测试使用的四个重建输出和既有 `lobsterout`；LOBSTER 安装包本身仍按许可证迁移。
- 既有的 ORCA、OpenMPI、SHARC、Newton-X、Yambo、LOBSTER、Multiwfn、Critic2、VESTA cache 仍需按各自许可证和原目录结构迁移。

## 验证证据

| 软件链 | 结果 | 本地证据 |
|---|---|---|
| AiiDA | SQLite profile + 同步 process 完成 | AiiDA repository/profile |
| CENSO -> ORCA | 两构象 PBE-D4 prescreen 完成 | `.software_cache/censo/smoke_prescreen3` |
| SHARC -> ORCA | H2 energy/gradient 接口完成 | `.software_cache/sharc/smoke/orca_h2/QM.out` |
| Newton-X -> ORCA | 1.5 fs TDDFT-NAD 轨迹完成 | `.software_cache/newton-x/26a/smoke/orca_test_cio/orca/01-MD-TDDFT-NAD-CIO/md.log` |
| QE -> Wannier90 | `All done`，spread 4.037017340 | `.software_cache/wannier90/smoke/qe_si_sourcebuild` |
| QE -> Yambo | `P2Y completed` + `Game Over` | `.software_cache/yambo/smoke/qe_si_8band` |

## 最终自动化验证

- requested software audit：48/48 完整，47 `configured` + 1 `specification`。
- managed resource probe：27/27 pass；ORCA OpenMPI 版本及 `mpif.h`/`use mpi` Fortran bindings 均通过。
- toolbox verify：catalog、runtime profiles、native guides、semantic retrieval、handler coverage、legacy-tool removal 全部 pass。
- 相关 pytest：39 passed（包含环境 YAML/requirements 依赖一致性回归）；native manual 生成一致性检查通过；`git diff --check` 通过。
- 全测试目录可收集 423 项；没有把会进入长等待的全量执行计入上述通过数字。

## 2026-08-06 目录整理与可迁移发布

- 核心 Python 包从 `chemistry_toolbox/src/researchchem_toolbox/` 扁平化到 `chemistry_toolbox/src/`，正式导入统一为 `chemistry_toolbox.src`；MCP 对外服务名 `researchchem_toolbox` 保持不变。
- 根 `pyproject.toml` 成为唯一打包配置，并提供 benchmark、MCP server、MCP installer、tool manager 和 software manager 入口；删除重复子项目打包文件和无调用方的 MCP adapter/registry/models/tools 兼容层。
- 环境定义改成 `chemistry_toolbox/environment/<environment>/` 自包含 `environment.yml`、`requirements.txt` 和 Linux 锁；框架环境位于 `environment/researchchembench/`，runtime 映射位于 `environment/environments.yaml`。
- 生成状态从 `config/` 移到 `evidence/status/`，旧 native smoke 基线移到 `evidence/archive/`；`config/` 只保留人工维护的运行配置。
- Git 缓存骨架包含两份缓存 README、`.software_cache/.layout.json`、模型来源/校验文本和固定目录 `.gitkeep`，大文件仍由忽略规则排除。
- pmx 源码快照从错误的 `installations/` 移到 `sources/pmx/develop-0dd5f0a`；可执行 pmx 继续由 `.envs/molecular-simulation-openff` 提供。software manager 状态为 37/37 installed。
- 验证：工具箱全量执行 494 passed、1 skipped，并定位修复 1 个旧目录深度导致的模型缓存路径失败；修复后的路径/语义/MACE 相关回归 46 passed。根 benchmark 97 passed，pmx/清单/缓存管理/profile 回归 48 passed，错误级 Ruff、Shell 语法、Git whitespace、14 个环境锁哈希、wheel 仓库外导入和命令入口均通过。
- 当前缓存重建和迁移应以根 README、`.software_cache/README.md`、`.model_cache/README.md` 及本节新路径为准；本文件前部保留的旧 `.software_cache/<software>` 路径仅记录历史修补过程。
