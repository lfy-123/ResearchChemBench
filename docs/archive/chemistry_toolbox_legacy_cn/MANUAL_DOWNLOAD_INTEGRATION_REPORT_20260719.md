# 手动下载软件接入与剩余处理报告（2026-07-19）

## 1. 本次范围与原则

- 输入目录：`download/public_downloads_twice/手动下载/`。
- 软件统一复制、解压或构建到 `.software_cache/<software>/<version>/`；Python/编译依赖隔离在 `.tool_envs/<runtime>/`。
- MATLAB 镜像仍未上传完整，按要求没有复制、挂载、解压、安装或编写适配器。
- 公共 MCP 仍固定暴露 40 个 Scientific Actions + 4 个 Data Actions。新增软件作为原子动作的可选 `backend_id`，没有新增 `run_gaussian`、`run_charmm`、`run_newtonx` 一类流程/脚本执行工具，也没有自动选择或 fallback。
- 修改前代码已由 Git 标签 `pre-manual-software-integration-20260719` 固定在提交 `8353793`。

## 2. 手动下载软件处理结果

| 软件 | 缓存/运行时 | 工具箱接入状态 | 实际验证 | 说明 |
|---|---|---|---|---|
| Gaussian 16 C.01 | `.software_cache/gaussian/g16` / `.tool_envs/gaussian` | `gaussian` 后端：`calculate_energy`、`calculate_hessian`、`optimize_geometry`、`calculate_dipole_moment` | 水 HF/STO-3G 能量 `-74.9629916389 Eh`；9×9 Hessian；优化与偶极均通过 | `formchk` 被用于结构化 Hessian解析；不接受任意 route deck |
| GAMESS 2024 R2 Patch 1 | `.software_cache/gamess/2024-r2-p1` / `.tool_envs/gamess` | `gamess` 后端：能量、几何优化、偶极 | 水能量 `-74.962991629 Eh`；水优化 `-74.9659012164 Eh`；偶极通过；官方 exam01 通过 | sockets DDI + OpenBLAS ILP64；方法、基组和收敛均由 Agent 显式给出 |
| NAMD 3.0.2 | `.software_cache/namd/3.0.2` / `.tool_envs/namd` | `namd` 后端：`minimize_system_energy`、`propagate_dynamics` | AVX-512 CPU 最小化和 NVE 单段传播通过，产生可继续传递的 `.coor/.vel/.xsc/.dcd` | CUDA 包已缓存，但当前无 GPU，公共后端不会自动切换到 CUDA |
| Amber 26 / PMEMD26 | `.software_cache/amber/26` / `.tool_envs/amber` | `amber_pmemd` 后端：最小化、单段动力学 | 串行最小化通过；2 进程 PMEMD MPI NVT 传播通过；原官方串/并行回归也通过 | `cpu_cores=1` 用串行 PMEMD，`>1` 用同规模 MPI；未构建 CUDA PMEMD |
| CHARMM c50b2 | `.software_cache/charmm/50b2` / `.tool_envs/charmm` | `charmm` 后端：最小化、NVE/NVT 单段动力学 | 蛋白小体系最小化、NVE、NVT 与 restart 链通过 | 显式输入 RTF/参数/PSF/坐标；长路径被安全暂存；不接受任意 CHARMM 脚本 |
| LOBSTER 5.1.0 | `.software_cache/lobster/5.1.0` / `.tool_envs/lobster` | 已验证 auxiliary runtime；暂不公开新 Action | Quantum ESPRESSO→LOBSTER 金刚石计算完成，绝对 charge spilling `1.12%` | 当前 40 个科学动作没有“周期成键分析”的准确契约；没有用任意 `lobsterin` runner 代替 |
| Newton-X New Series 3.5.3 | `.software_cache/newton-x/26a` / `.tool_envs/newtonx` | 已验证 auxiliary runtime；暂不公开新 Action | 1D analytical avoided-crossing 测试 `1/1` 通过 | 后续若新增原子动作，需显式表达电子态、耦合、跃迁算法和电子结构接口，不能封装整条工作流 |
| ORCA 6.1.1 no-DMRG 归档 | `.software_cache/orca/download/` | 仅缓存新归档；现有 `orca` 后端保持不变 | 原完整 ORCA 6.1.1 能量/Hessian/优化/偶极仍通过 | 新归档功能更少，因此没有覆盖已验证的活动安装 |
| VASP 6.3.2 重复归档 | `.software_cache/vasp/download/` | 仅缓存来源；现有 `vasp` 后端保持不变 | 已编译活动版本及 Si 测试继续可用 | 一般元素的生产计算仍需合法 PAW POTCAR 库 |
| MATLAB R2018a | 未处理 | 未适配 | 未测试 | 上传不完整且用户明确要求本次跳过 |

## 3. 全量状态

| 指标 | 结果 |
|---|---:|
| 用户清单总数 | 59 |
| configured | 45 |
| specification | 1 |
| partial | 2 |
| manual_required | 9 |
| manual_api_review | 2 |
| 公共 MCP Actions | 44（40 Scientific + 4 Data） |
| 可选 BackendSpecs | 54 |
| 后端执行环境 | 22/22 通过 |
| Pytest | 65/65 通过 |
| MCP 冒烟 | 44 个工具完整注册；显式工具/后端、Artifact 与 trace 链通过 |

逐项模块、命令、缓存、许可、环境和公共适配信息见：

- `chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_REQUESTED_SOFTWARE_STATUS.md`
- `chemistry_toolbox/docs/CHEMISTRY_TOOLBOX_TOOL_RESOURCE_MATRIX.md`
- `chemistry_toolbox/docs/MCP_PROFILE_STATUS.md`

## 4. 仍需处理：按建议顺序

| 顺序 | 软件/接口 | 当前状态 | 你需要做什么 | 收到后我可以做什么 |
|---:|---|---|---|---|
| 1 | MATLAB | manual_required | 完成合法 MATLAB 安装介质上传，并说明许可证激活方式/许可证服务器；不要只上传 crack 文件 | 安装或挂载 MATLAB，配置无界面模式，验证 EasySpin，随后设计原子 EPR/ESR 动作 |
| 2 | EasySpin | partial | 与 MATLAB 同步处理；EasySpin 本身的 6.0.12 文件已经齐全 | 跑官方验证、补 MATLAB path、验证 `pepper/chili` 等可调用能力 |
| 3 | Q-Chem | manual_required | 提供 Linux 安装包、版本、合法 license/许可证服务器信息 | 放入 `.software_cache`，建隔离 runtime，先做真实计算，再接入合适的电子结构原子动作 |
| 4 | Molpro | manual_required | 提供 Linux 发行包和许可证 token/key/服务器配置 | 安装、验证并按原子量化能力接入；不暴露任意输入 runner |
| 5 | TURBOMOLE | manual_required | 提供安装包和许可证环境说明 | 配置 runtime，并让 Agent 在 CENSO 等场景中显式选择，而不是预设流程 |
| 6 | CASTEP | manual_required | 提供 STFC 合法发行包/许可，以及需要覆盖的赝势数据 | 构建周期计算后端与显式赝势资源映射 |
| 7 | CRYSTAL | manual_required | 提供发行包、版本和许可证 | 安装、验证周期量化任务并设计对应原子适配器 |
| 8 | WIEN2k | manual_required | 提供注册发行包、版本与许可说明 | 编译/配置，并在有准确动作契约时接入 |
| 9 | OpenEye | manual_required | 若使用官方 Conda 包，可以不提供传统安装包；但仍需提供合法 OpenEye license 文件/许可证服务器和可用 Conda channel 信息 | 在隔离环境直接安装 Conda 包，验证许可证和 API，再决定对接/构象/性质类原子后端 |
| 10 | Schrödinger | manual_required | 提供站点安装包、版本、合法 license server 配置 | 配置命令环境并只接入可结构化表达的原子能力 |
| 11 | Arkane | partial | 暂时不需要下载新文件；如果你有已验证的 Arkane/RMG 环境导出或最小成功案例可提供 | 修复当前异常慢的顶层导入/运行，做有界真实热化学测试；该项主要由我继续处理 |
| 12 | NIST CCCBDB 接口 | manual_api_review | 若有官方 API 文档、授权方式或稳定数据出口，请提供；否则需确认是否接受只覆盖明确查询类型的接口 | 先审查条款和稳定性，再增加数据 Action；不会用脆弱 HTML 抓取冒充 API |
| 13 | NIST Chemistry WebBook 接口 | manual_api_review | 同上，提供官方接口/条款依据或明确允许的查询范围 | 设计有界、可追溯的数据 Action；继续避免通用网页抓取 |

## 5. 已配置但仍有范围限制的资源

| 项目 | 当前限制 | 是否阻塞现有工具 | 后续建议 |
|---|---|---|---|
| VASP PAW POTCAR | 目前只有测试用 Si POTCAR；一般元素库受 VASP 许可约束 | 不阻塞 Si 验证，阻塞其他元素生产任务 | 提供合法 POTCAR 根目录后按元素登记 ResourceRef |
| NAMD CUDA | 二进制已缓存，但当前节点未发现 GPU | 不阻塞 CPU NAMD 后端 | 有 GPU 节点后单独验证；仍由 Agent 显式选择设备/后端变体 |
| Amber CUDA PMEMD | 本次只构建 CPU serial/MPI | 不阻塞 CPU 后端 | 如 benchmark 确需 GPU，提供 CUDA 兼容节点后再构建和验证 |
| LOBSTER 公共动作 | 软件齐全，但缺准确的公共“周期成键分析”动作契约 | 不影响其他 44 个动作 | 后续单独评审并新增 typed Action，而不是增加 `run_lobster` |
| Newton-X 公共动作 | 软件齐全，但非绝热动力学契约尚未纳入当前 40 个科学动作 | 不影响其他 44 个动作 | 先定义状态/耦合/跃迁/接口的单段契约，再实现 |
