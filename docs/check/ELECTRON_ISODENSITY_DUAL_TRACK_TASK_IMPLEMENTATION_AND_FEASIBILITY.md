# Electron Isodensity 双轨测试任务整理与工具箱可行性报告

日期：2026-07-24

## 1. 结论

已将 Alibakhshi 与 Schäfer 2024 年发表于 *Nature Communications* 的论文
“Electron iso-density surfaces provide a thermodynamically consistent
representation of atomic and molecular surfaces”（DOI:
`10.1038/s41467-024-50408-8`）整理成两套相互隔离的 benchmark：

- 5 个自主科研任务：只提供科学问题、分子身份和完成该问题必需的实验输入，
  不提供论文、公开构象、软件名、方法、基组、cutoff 或执行路线。
- 5 个论文复现任务：提供论文重建的方法、路线、公开构象和作者输入模板，
  但不提供作者波函数、量化输出、计算表面积、最优 cutoff 或参考答案。

当前 chemistry toolbox 已安装完成这些任务所需的全部核心软件。允许智能体使用
“直接编写输入并调用原生软件”的通道时，10 个任务均可判为 `solvable`；其中论文
复现 Q1 需要把论文所称的 CCSD(T) 密度明确实现为 ORCA 可计算的 CCSD 未弛豫密度，
可另外计算 CCSD(T) 能量，但不能声称得到了 ORCA 不支持的 CCSD(T) 一粒子密度。

不需要新增软件。为降低智能体编写交互命令和批量调度时的失败率，建议新增 3 个
类型化 Action；它们是可靠性与效率增强，不是当前任务的硬阻塞项。

## 2. Git 与改动边界

修改前基线已用 Git tag 保存：

`electron-isodensity-dual-track-baseline-20260724`

对应提交：`dafc4f63713f3b4c7dba8d66c3ee67be40651462`

本次只整理 Electron Isodensity 任务、对应测试、构建器和本文档。工作区中已有的
Heterobiaryl 输出、数据集 ZIP、core 文件和本地配置均未纳入本次改动。

## 3. 官方资料与联网补全结果

检查范围包括论文正式页面、PMC 全文包、论文数据可用性说明、全部补充文件以及
按 DOI、题名和作者进行的公开网络检索。

确认得到的官方资料：

- 论文 PDF 与 PMC XML 全文；
- Supplementary Information；
- Supplementary Data 1；
- Supplementary Data 2 坐标归档；
- Supplementary Software；
- Source Data。

没有发现独立的作者 GitHub、Zenodo 或其他数据仓库，也没有发现官方页面遗漏而
需要从非官方来源补入的关键数据。官方资料保存在仅供任务维护与评分使用的目录：

`tasks/_electron_isodensity_shared/reference/`

其来源、URL、SHA-256 和许可记录在 `source_manifest.json`。论文正文报告 104 个
分子的 1071 个构象，但公开 Supplementary Data 2 实际包含 1074 个 XYZ 文件、104
个唯一分子前缀。本报告保留这一出处差异，没有静默修改任一数字。

## 4. 新建任务

### 4.1 自主科研轨道

| 任务 | 科学目标 | 分子 | 可见实验 TE 数据 | 公开构象 |
|---|---|---:|---:|---:|
| `Electron_Isodensity_01_Method_Selection` | 独立建立电子密度方法层级并选择生产方法 | M1–M3 | 0 | 0 |
| `Electron_Isodensity_02_Conformer_Effects` | 独立研究构象采样对分子表面积的影响 | M5–M6 | 2 | 0 |
| `Electron_Isodensity_03_Cutoff_Calibration` | 独立标定电子密度 cutoff | M1–M3、M5–M7 | 6 | 0 |
| `Electron_Isodensity_04_Blind_Prediction` | 用 3 个校准分子盲测 M4 | M1–M4 | 3；M4 隐藏 | 0 |
| `Electron_Isodensity_05_End_to_End` | 端到端建立方法、构象、cutoff 与盲测流程 | M1–M7 | 6；M4 隐藏 | 0 |

每个任务的 `data/benchmark_data` 只包含：

- `README.md`；
- `molecular_systems.json`；
- `conditions.json`；
- 该任务确实需要时才存在的 `experimental_measurements/te_surfaces.json`；
- `input_manifest.json`，含文件大小和 SHA-256。

自主科研输入中没有 ORCA、Multiwfn、CREST、xTB、PBE、B3LYP、DSD-PBEP86、
CCSD、def2、marching tetrahedra、论文 DOI、论文 cutoff 网格或作者坐标。智能体必须
自己生成三维结构、选择方法和规划路线。

### 4.2 论文复现轨道

| 任务 | 复现目标 | 分子 | 公开构象数 |
|---|---|---:|---:|
| `Electron_Isodensity_Reproduction_01_Method_Selection` | 复现 PBE/B3LYP/DSD 与相关方法参考的比较 | M1–M3 | 3 |
| `Electron_Isodensity_Reproduction_02_Conformer_Effects` | 复现单构象与构象系综差异 | M5–M6 | 28 |
| `Electron_Isodensity_Reproduction_03_Cutoff_Calibration` | 在 6 个分子子集上复现 cutoff 标定 | M1–M3、M5–M7 | 34 |
| `Electron_Isodensity_Reproduction_04_Blind_Prediction` | 锁定 cutoff 后复现 M4 盲测 | M1–M4 | 4 |
| `Electron_Isodensity_Reproduction_05_End_to_End` | 复现完整七分子计算链 | M1–M7 | 35 |

复现任务在自主科研基础输入之外增加：

- `initial_structures/<molecule>/*.xyz`：从公开 Supplementary Data 2 中按任务复制，
  不是符号链接，也没有把全部公共构象复制到每个任务；
- `computational_protocol.json`：论文方法、参数、版本差异和可执行兼容策略；
- `workflow_requirements.json`：论文计算路线和证据要求；
- `author_input_templates/orca_input.in` 与 `Multiwfn.in`：作者补充软件原文；
- ORCA 6 和 Multiwfn 2026 的兼容模板。

复现任务没有输入任何 `.gbw`、`.wfn`、`.wfx`、`.out`、`.log`、作者计算表面积、
构象权重、最优 cutoff 或 Source Data 结果。M4 的实验 TE 值在自主和复现盲测任务
中均隐藏。

## 5. 论文路线重建

复现任务公开的论文路线为：

1. 论文用 CREST/GFN2-xTB 为每个分子搜索最多 25 个低能构象；本 benchmark 主复现
   路线直接使用作者公开构象，避免重复做不必要的构象搜索。
2. 方法比较使用 PBE、B3LYP、DSD-PBEP86 与论文标记的 CCSD(T)，基组为
   def2-TZVPD。
3. 生产密度使用 ORCA 5.0.3 的 DSD-PBEP86/def2-QZVPD、def2-TZVPD/C、D3BJ、
   NoFrozenCore、PModel、VeryTightSCF 和弛豫 MP2/双杂化密度。
4. Multiwfn 以 improved marching tetrahedra 计算表面积；cutoff 从 0.0008 到
   0.0025 a.u.，步长 0.0001，网格间距 0.1。
5. 298.15 K 下进行构象 Boltzmann 加权，再计算 MUPE 与 Pearson R。

可访问论文与作者模板没有唯一说明构象权重采用哪一种单独热化学能量。因此复现任务
要求采用一致、明确记录的能量定义，并做敏感性分析；不能凭空补写未公开的频率或自由
能协议。

## 6. 发现并处理的版本兼容问题

### 6.1 作者 ORCA 模板不是可直接运行的完整输入

作者补充模板最后一行为 `*xyzfile molecule.xyz`，缺少 ORCA 必需的电荷和多重度，
直接运行会立即失败。这是公开源模板的不完整，不是 toolbox 的 ORCA 安装故障。

复现任务保留作者原文作为 provenance，同时新增 `orca_6_compatible.in`，补入
`* xyzfile 0 1 molecule.xyz`，并在 `%mp2` 中明确请求 `Density relaxed` 和
`NatOrbs true`，使 `orca_2aim` 使用 `.mp2nat`，而不是静默退回普通参考轨道 GBW。

### 6.2 ORCA 不提供 CCSD(T) 一粒子密度

ORCA 6.1 官方手册明确说明 unrelaxed density 可与 CCSD/QCISD 使用，但 CCSD(T)
未弛豫密度不可用。复现任务采用以下可审计兼容策略：

- 用 canonical CCSD/def2-TZVPD 未弛豫密度作为相关密度参考；
- 如需论文能量层级，可另报同几何的 CCSD(T) 能量；
- 输出中必须明确写为 CCSD density substitution，不能声称是严格 CCSD(T) density。

已增加 `ccsd_density_orca_6.in`、`orca_plot_ccsd_density.menu` 和
`Multiwfn_2026_external_grid_surface.menu`，用于从 ORCA `.densities` 容器选择 MDCI
密度、导出 cube 并计算表面积。

### 6.3 Multiwfn 菜单版本变化

作者命令流对应旧版 Multiwfn。已保留作者原文，并为已安装的 Multiwfn 2026.7.15
增加两个实测可运行的菜单模板：普通 WFN/WFX 密度表面积与外部 cube 网格表面积。

## 7. 真实软件验证

验证使用的是新建复现任务中的公开 XYZ 和兼容模板，不读取作者量化输出。

### 7.1 软件与资源

| 软件 | 实际版本 | 用途 |
|---|---|---|
| ORCA | 6.1.1 | DFT、双杂化密度、CCSD 密度 |
| OpenMPI | 4.1.8 | ORCA 并行运行时 |
| Multiwfn | 2026.7.15 | improved marching tetrahedra 表面积 |
| CREST | 3.0.2 | 自主科研轨道构象搜索 |
| xTB | 6.7.1 | CREST 后端和快速结构计算 |

服务器可见 64 个逻辑 CPU 和约 503 GiB 内存。代表性 ORCA 作业使用 PAL16；并行
ORCA 必须由解析后的绝对路径启动，toolbox 的原生执行说明已经明确这一要求。

### 7.2 乙烷生产密度与完整 cutoff 扫描

输入：复现 Q1 的 `ISO-M1/995-1.xyz`。

| 步骤 | 后端 | 实际结果 |
|---|---|---|
| DSD-PBEP86/def2-QZVPD 单点与弛豫密度 | ORCA 6.1.1，PAL16 | 正常结束，约 11.4 s，能量 -79.731854631544 Eh，生成 `.mp2nat` |
| `.mp2nat` 转 WFN/WFX | `orca_2aim` | 正常结束，约 0.02 s，日志确认读取 `.mp2nat` |
| 0.0016 a.u. 表面积 | Multiwfn 2026.7.15 | 75.58673 Å²，约 4.1 s |
| 0.0008–0.0025 全 18 cutoff | Multiwfn 2026.7.15 | 全部成功，顺序总耗时约 70 s |

隐藏论文值在 0.0016 a.u. 为 75.61296 Å²；本次独立重算相差 0.02623 Å²，约
0.0347%。这验证了 ORCA 6 兼容模板、正确双杂化密度导出和 Multiwfn 表面积链路。

### 7.3 CCSD 相关密度路径

同一乙烷结构上的 CCSD/def2-TZVPD 未弛豫密度计算约 24.9 s，正常结束并生成 MDCI
密度。`orca_plot` 从 `.densities` 容器选择 MDCI 密度并导出 100×100×100 cube，
Multiwfn 在 0.0016 a.u. 得到 76.49432 Å²。由此确认复现 Q1 的高层相关密度比较
具有真实可执行路径，同时也确认不能把它错误标成严格 CCSD(T) 密度。

### 7.4 最大代表性分子

输入：复现 Q2 的 1-戊硫醇 `ISO-M6/1475-1.xyz`，18 个原子。

| 步骤 | 后端 | 实际结果 |
|---|---|---|
| DSD-PBEP86/def2-QZVPD 单点与弛豫密度 | ORCA 6.1.1，PAL16 | 正常结束，约 93.8 s，能量 -595.557660321457 Eh |
| `.mp2nat` 转 WFN/WFX | `orca_2aim` | 正常结束，约 0.2 s |
| 0.0016 a.u. 表面积 | Multiwfn 2026.7.15，16 threads | 159.55326 Å²，约 18.4 s |

因此代表性单次量化与单次表面积计算都远低于 10 分钟。复现 Q2/Q3/Q5 的主要成本
来自多个构象和多个 cutoff 的笛卡尔积，而不是单个作业过重。以该最大代表性构象
线性外推，18 个 cutoff 顺序运行约 5.5 分钟/构象；54–64 核机器可同时安排多个
Multiwfn 或 ORCA 作业，但必须控制总线程数避免过度订阅。完整 Q5 预计是几十分钟到
约 1–2 小时量级的批处理，而不是 Heterobiaryl 任务的 1–3 天量级。

## 8. 分任务可行性判断

| 任务 | 分类 | 判断依据与限制 |
|---|---|---|
| 自主 Q1 | `solvable` | 三个小分子；结构生成、DFT/双杂化、CCSD 密度和表面积均有后端；方法探索会增加调用数 |
| 自主 Q2 | `solvable` | CREST/xTB、ORCA、Multiwfn 均可用；构象搜索和筛选策略由智能体自行提出 |
| 自主 Q3 | `solvable` | 六分子实验 TE 数据齐全；cutoff 扫描可批量并行 |
| 自主 Q4 | `solvable` | M4 真值正确隐藏；校准、锁定、盲测流程可执行 |
| 自主 Q5 | `solvable` | 全链路软件齐全；属于批量调度任务，建议设总 walltime 与并发上限 |
| 复现 Q1 | `solvable`，带兼容声明 | 方法和坐标齐全；CCSD 密度替代必须明确，不能伪造 CCSD(T) 密度 |
| 复现 Q2 | `solvable` | 28 个公开构象齐全；论文未唯一公开权重能量定义，须报告约定与敏感性 |
| 复现 Q3 | `solvable` | 34 个公开构象、实验 TE、cutoff 网格和统计定义齐全 |
| 复现 Q4 | `solvable` | 四个公开构象齐全，M4 实验值隐藏，支持真正盲测 |
| 复现 Q5 | `solvable` | 35 个公开构象和完整路线齐全；运行量最大但单作业很轻，可并发完成 |

这里的 `solvable` 指能够依靠“任务输入 + 当前 toolbox”计算主要科学结论，不表示
能够逐位复现 ORCA 5.0.3 的全部作者数字，也不消除论文未公开热化学权重细节带来的
方法学不确定性。

## 9. 工具箱能力判断

### 9.1 是否需要新增软件

不需要。当前 ORCA、OpenMPI、Multiwfn、CREST 和 xTB 已覆盖结构生成、构象采样、
电子密度计算、相关密度导出、等密度面面积和批量统计所需的核心软件能力。NBO、
Gaussian、商业波函数分析软件或新的量化后端均不是本论文任务的必要条件。

### 9.2 直接调用软件能否弥补 Action 未覆盖

可以。toolbox 的 native software guide 已允许智能体自己编写 ORCA 输入和 Multiwfn
菜单流，并支持长作业异步提交。因此“没有预设等密度面 Action”不是不可完成的
理由。本次真实验证就是通过该能力完成的。

直接调用的弱点是：菜单号、密度来源、输出解析、文件关联、cutoff 循环和并发控制
都由智能体负责，容易出现“读取了错误 GBW 密度但程序仍正常结束”一类静默错误。

### 9.3 建议新增的 Action

1. `calculate_correlated_electron_density`
   - 输入：结构、方法、基组、charge、multiplicity、relaxed/unrelaxed、线程和内存；
   - ORCA 后端应显式返回 density source（SCF、MP2 relaxed、MDCI）、GBW、
     `.mp2nat`/`.densities` 和收敛信息；
   - 必须拒绝 ORCA 不支持的 `CCSD(T) density`，而不是静默降级。
2. `export_electron_density_grid`
   - 输入：ORCA 结果 Artifact、density source、网格范围/分辨率和输出格式；
   - 后端：`orca_2aim` 或 `orca_plot`；
   - 输出：WFN/WFX/cube、电子数积分检查、所选密度名称和 provenance。
3. `calculate_electron_isodensity_surface`
   - 输入：WFN/WFX/cube、一个或多个 cutoff、网格间距、线程；
   - 后端：Multiwfn；
   - 输出：每个 cutoff 的面积、体积、日志、版本、失败项和机器可读表格；
   - 应原生支持 cutoff 列表，避免 18 次重复手写菜单。

可选增加 `boltzmann_average_observable`，统一能量单位、温度、简并度、归一化、
截断阈值和不确定性；这一功能也可由智能体直接写短程序完成，因此优先级低于前三项。

## 10. 自动验证

新增测试：

`test_electron_isodensity_dual_track_tasks_are_decontaminated_and_complete`

覆盖：任务清单、双轨元数据、100 分 rubric、方法泄漏、ZIP/符号链接、文件哈希、
分子式、原子数、电荷、多重度、M4 隐藏真值、公开构象数量、兼容模板及双轨共享
原始值一致性。

执行结果：

```text
5 passed in 0.27s
```

构建器 `scripts/build_electron_isodensity_dual_track_tasks.py` 仅用于从固定官方来源
确定性重建 10 个任务并防止双轨漂移；它不代替任何化学计算，量化和表面积结果均由
ORCA 与 Multiwfn 真实运行获得。

