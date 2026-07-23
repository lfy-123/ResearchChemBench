# ResearchChemBench Heterobiaryl P(V) 六任务可行性审计

- 审计日期：2026-07-23
- 审计对象：`Heterobiaryl_PV_01` 至 `Heterobiaryl_PV_06`
- 工具箱：`chemistry_toolbox`
- 论文输入：`tasks/_heterobiaryl_pv_shared/reference/paper.pdf`
- 真实计算证据：`docs/check/heterobiaryl_task_feasibility_audit/`

## 1. 结论摘要

本次审计的判断对象是“任务指令 + 整理后的原始数据 + 当前化学工具箱”是否足以完成科学问题，不是评估语言模型是否能猜中论文结论。

| 任务 | 主要问题 | 可行性 | 是否能由当前输入与工具箱复现论文主要结果 |
|---|---|---|---|
| Q1 | 质子化对 Py–Py 偶联势垒的影响 | `partially_solvable` | 否；能筛选 P0/P1/P2 最小值，但只验证了 P2 的一条局部路径，不能得到可比的 30/20/14 kcal mol⁻¹ 趋势 |
| Q2 | Py–Py 与 Ph–Py C–C 选择性 | `partially_solvable` | 否；P2 Py–Py 路径可验证，Ph–Py 扫描超时，缺少同条件驻点、IRC 和自由能比较 |
| Q3 | P2 中 C–C 与 C–O 竞争 | `partially_solvable` | 否；C–C 路径可验证，C–O 产物及原子映射不唯一且搜索未完成，不能复现 14 vs 18 kcal mol⁻¹ |
| Q4 | 偶联机理 | `partially_solvable` | 部分；真实 TS、单一目标虚频、双向 IRC 和键级支持一条 stepwise/asynchronous/apical-to-equatorial 路径，但不能排除替代路径，也不能计算氧孤对电子占据 |
| Q5 | 决速步骤 | `not_solvable` | 否；输入从醇加成后的 P(V)-OMe 中间体开始，缺少决定“醇加成为决速步骤”所必需的上游反应体系与动力学原始数据 |
| Q6 | 完整端到端机理 | `not_solvable` | 否；继承 Q1–Q5 的缺口，尤其缺少 Q5 上游物种、完整竞争路径和论文级统一溶液自由能流程 |

因此，六个任务中没有一个能在当前条件下完整复现论文全部主要数值与机理结论。Q4 最接近可完成，但仍达不到 `solvable` 的证据标准。

## 2. 证据口径

本报告使用以下标签区分证据来源：

- **本次计算**：本次审计实际调用工具箱或受管化学软件新生成的结果。
- **论文参考**：仅用于事后比较的论文或参考答案结论，不作为本次计算输入。
- **推断**：由实验数据和本次计算共同支持、但没有被直接计算证明的解释。
- **未解决**：输入、Action、后端、参数能力或资源不足，不能给出可靠结论。

探索性扫描最大点、未收敛结构和高于一阶的鞍点均不被当作已验证过渡态，也不被当作精确势垒或严格上下界。

## 3. 修改前 Git 基线

修改任务文件前已保存当前受跟踪版本：

- commit：`9a7046a8e25f928447fb1c262041b863559d5c3b`
- tag：`before-heterobiaryl-feasibility-audit-20260723`
- commit message：`Checkpoint repository before Heterobiaryl feasibility audit`

审计开始前已经存在的无关未跟踪文件、core dump 和大型 ZIP 未被删除或纳入本次修改。

## 4. 原任务数据发现的问题

六个任务原先的 `data/` 都只链接到同一个 `autonomous_inputs.zip`。这不满足“直接可读取、任务专用、最小原始输入”的要求。

更严重的是，旧公共种子不是独立生成的原始结构。旧构建逻辑从作者 Gaussian 优化/频率输出中取最终坐标，再对每个笛卡尔坐标加入约 ±0.14 Å 扰动：

- 与作者驻点的坐标 RMS 仍仅约 0.132–0.152 Å；
- 保留了作者选择的轴向/赤道构象和反应路径信息；
- 扰动后出现约 0.78–0.89 Å 的不合理 C–H/N–H 距离。

这类数据既有作者计算结果泄漏，也不是合格的未优化起始结构。六个任务现在不再使用该 ZIP。旧共享归档仅保留在共享参考区域用于追溯实验测量来源，并在 `tasks/_heterobiaryl_pv_shared/public/README.md` 中标记为 legacy/provenance-only。

## 5. 整理后的输入数据

### 5.1 通用结构与条件

新结构由有序 SMILES 独立进行 RDKit ETKDG 三维嵌入，不读取作者优化坐标、过渡态或反应能。每个质子化态提供 3 个未优化构象种子。

| 状态 | 分子式 | 原子数 | 总电荷 | 多重度 | 质子化定义 |
|---|---:|---:|---:|---:|---|
| P0 | C23H21N2OP | 48 | 0 | 1 | 两个吡啶 N 均未质子化 |
| P1 | C23H22N2OP | 49 | +1 | 1 | N18 质子化 |
| P2 | C23H23N2OP | 50 | +2 | 1 | N18、N24 均质子化 |

公共零基原子映射为：甲氧基 C0、O1、P2、P–Ph ipso C3/C9、P–Py ipso C15/C21、吡啶 N18/N24。

条件文件固定记录：353.15 K、1 M、乙醇、酸性条件；HCl 对应标准反应条件，TfOH 对应速率实验。当前输入不含显式乙醇、酸、反离子或质子转移络合物。配位氧配体是 methoxy，而不是一个显式乙醇分子。

新种子的最短原子间距为 1.039–1.061 Å；同一状态不同种子的重原子 RMSD 约 1.59–3.56 Å，没有重复结构或明显原子碰撞。

### 5.2 六个任务的文件清单

所有文件均为普通文件，无符号链接、无 ZIP、无作者优化驻点、无过渡态、无能垒、无参考答案。

| 任务 | 整理后的输入文件 |
|---|---|
| Q1 | `README.md`、`conditions.json`、`molecular_systems.json`、`input_manifest.json`；`initial_structures/P0/P0_SEED_01..03.xyz`、`P1/P1_SEED_01..03.xyz`、`P2/P2_SEED_01..03.xyz` |
| Q2 | 与 Q1 相同的 9 个独立 P0/P1/P2 种子及 4 个元数据文件 |
| Q3 | 4 个元数据文件；`initial_structures/P2/P2_SEED_01..03.xyz`；`experimental_measurements/measurements.json`，仅含 E02、E10、E11、E12 |
| Q4 | 与 Q1 相同的 9 个独立 P0/P1/P2 种子及 4 个元数据文件 |
| Q5 | 4 个元数据文件；`initial_structures/P2/P2_SEED_01..03.xyz`；`experimental_measurements/measurements.json`，仅含 E01、E02、E04–E12 |
| Q6 | 4 个元数据文件；9 个 P0/P1/P2 种子；`experimental_measurements/measurements.json`，仅含 E01、E02、E04–E12 |

保留 E12 是因为它记录竞争性 protio-dephosphination/产物平衡，对 Q3 的竞争路径和 Q5/Q6 的机理解释有直接作用。E03 未进入 Q5/Q6，因为源数据中没有可用的 E03 原始记录。

输入 manifest SHA-256：

| 任务 | manifest SHA-256 |
|---|---|
| Q1 | `fa76412bfa0a628902f42f0d6a47916d5cbeac3d61b50794e9b0d6b6860d6611` |
| Q2 | `1ba6e481ef312e2409cd06d76388a90783837f7fe3b0608fedbe5b4349acc714` |
| Q3 | `b99e0b579a3e7119bd9d74b9d379572d5fceda6864f2ec72effa4bf82e84a3a3` |
| Q4 | `b7a2b4c5ea5c575340b775894ecca7295ca35ad146a213e65988943826027568` |
| Q5 | `3a0cb9cec5eed0370b4f705c3dae88a24cad8a824022a36306863b1793060b84` |
| Q6 | `1fd0d7255df4e1474c6956d2090f2c97748551b043664e0ea20a580463bdbfdb` |

## 6. 实际调用的工具箱 Action 与后端

本次共发起 38 次工具箱化学 Action：37 次成功，1 次失败。另发起 5 个受管原生 xTB 松弛扫描任务。请求、返回值、摘要、软件日志和输出结构均保存在证据目录中。

| Action | backend | 次数 | 结果与用途 |
|---|---|---:|---|
| `generate_conformer_ensemble` | `rdkit_etkdg` | 3 | 成功；独立生成 P0/P1/P2 初始构象 |
| `optimize_geometry` | `xtb` | 11 | 成功；9 个种子筛选及 2 个 IRC 端点优化 |
| `calculate_hessian` | `xtb` | 6 | 成功；P0/P1/P2 代表最小值、TS、两个 IRC 端点中的关键结构 |
| `derive_vibrational_modes` | `internal_vibrations` | 6 | 成功；驻点与 TS 虚频分类 |
| `calculate_bond_orders` | `xtb` | 3 | 成功；反应物、TS、产物侧 Wiberg 键级 |
| `calculate_energy` | `xtb` | 2 | 成功；验证后的 P2 Py–Py 反应物和 TS 电子能 |
| `derive_thermochemistry` | `internal_thermochemistry` | 2 | 成功；353.15 K、1 M 等效压力的气相 RRHO 诊断 |
| `locate_transition_state` | `pysisyphus` + xTB | 1 | 成功；P2 Py–Py 局部 TS |
| `trace_intrinsic_reaction_coordinate` | `pysisyphus` + xTB | 1 | 成功；P2 Py–Py 双向 IRC |
| `calculate_energy` | ORCA 6.1.1 | 3 | SMD 1 次失败；CPCM(ethanol) 反应物/TS 单点 2 次成功 |

原生 xTB 扫描使用 GFN2-xTB 和 `--cosmo 24.55` 的通用介电常数近似，每条最多 40 分钟：

| 路径 | 状态 | 结果 | 获得帧数 |
|---|---|---|---:|
| Py–Py | P0 | 失败，进程被终止 | 1/5 |
| Py–Py | P1 | 超时 | 2/5 |
| Py–Py | P2 | 成功 | 5/5 |
| Ph–Py | P2 | 超时 | 1/5 |
| C–O | P2 | 超时 | 2/5 |

这里的 COSMO 24.55 只是介电环境探索，不等同于论文的乙醇 SMD，也没有完整表达 353.15 K、显式酸/反离子和溶液标准态。

### 6.1 Codex 隔离执行说明

审计期间尝试过让 Codex CLI 使用 `gpt-5.6-sol` 在只复制任务 `data/`、不运行评分的目录中独立执行，但当前 CLI 认证返回 HTTP 401，未获得任何可用化学结果。并且现有同主机 runner 即使不复制 `target_study`，其沙箱仍可能读取原仓库路径，不能构成对参考答案和论文的硬隔离。因此本报告没有使用或评估任何 Codex 输出；可行性结论完全来自上表所列的真实化学工具和软件运行。若以后要做严格盲测，应使用独立容器/账户，只挂载任务指令、整理后的 `data/` 和工具箱服务。

## 7. 本次计算的主要结果

### 7.1 P0/P1/P2 种子筛选

9 个种子均完成气相 GFN2-xTB loose 优化。各状态最低种子分别为 P0 seed 1、P1 seed 2、P2 seed 1。三个代表最低结构的频率分析均无小于 -20 cm⁻¹ 的显著虚频，可作为该方法下的局部最小值。

| 状态 | seed 1 相对能 | seed 2 相对能 | seed 3 相对能 | 最低 seed |
|---|---:|---:|---:|---|
| P0 | 0.000 | 0.342 | 0.666 | 1 |
| P1 | 9.137 | 0.000 | 3.313 | 2 |
| P2 | 0.000 | 15.091 | 10.055 | 1 |

单位为 kcal mol⁻¹，且只能在同一化学组成/质子化态内比较。不同质子化态的绝对能不能用来代替活化势垒。

### 7.2 P2 Py–Py 路径

P2 Py–Py 是唯一获得完整局部验证的反应路径：

- xTB 扫描中形成 C15–C21 距离由 2.770 Å 经 2.162 Å 变为 1.542 Å，断裂 P2–C21 由 2.005 Å 经 2.453 Å 变为 2.896 Å；
- `pysisyphus` TS 收敛，TS 中 C15–C21 = 2.206 Å、P2–C21 = 2.492 Å；
- TS 只有一个显著虚频：-227.82 cm⁻¹，目标模式对应 C–C 形成/P–C 断裂；
- 双向 IRC 成功连接到反应物样端点 C–C 2.584 Å/P–C 2.116 Å，以及产物样端点 C–C 1.543 Å/P–C 2.682 Å；
- 产物侧端点重新优化并做频率后无显著虚频，是该方法下的局部最小值。

气相 GFN2-xTB 优化端点与 TS 给出：

- 反应物端点：-72.457819320389 Eh；
- TS：-72.439057333894 Eh；
- 产物端点：-72.502878097245 Eh；
- 相对于该 IRC 反应物端点的电子能垒：11.77 kcal mol⁻¹；
- 产物端点相对反应物端点：-28.27 kcal mol⁻¹。

但是，扫描从 P2 seed 3 出发，该构象比本次找到的 P2 seed 1 高 10.055 kcal mol⁻¹。该 IRC 反应物端点是否与全局最低 P2 构象属于同一可快速平衡盆地没有被证明。因此 11.77 kcal mol⁻¹ 只是局部路径电子能差，不能直接作为任务的正式活化势垒；若机械地相对最低 seed 比较，TS 差约 21.69 kcal mol⁻¹，同样不能在缺少构象互变路径时称为总势垒。

内部 RRHO 在 353.15 K、1 M 等效理想气体平移压力下给出气相 ΔG‡ = 6.46 kcal mol⁻¹。该流程忽略虚频、没有乙醇溶剂和 GoodVibes 低频/准谐处理，只是诊断值，不是论文的 14 kcal mol⁻¹。

ORCA 验证结果：

- 请求 `PBE0-D3BJ/def2-SVP SMD(ethanol)` 时，工具箱生成的 `%cpcm smd true solvent "ethanol" end` 输入被 ORCA 6.1.1 拒绝，报错 `Solvent name not provided`；这是当前 typed SMD 合同/渲染问题；
- 改用 `PBE0-D3BJ/def2-SVP CPCM(ethanol)` 后，反应物和 TS 单点均成功，电子能差为 18.95 kcal mol⁻¹；
- 这只是 GFN2-xTB 气相几何上的低基组 CPCM 单点，不是溶剂优化后的频率自由能，也不是论文的 ωB97XD/6-31+G(d) SMD + 高级单点 + GoodVibes 流程。

### 7.3 P2 Py–Py 机理探针

本次 Wiberg 键级显示：

| 结构 | WBO(P2–C21) | WBO(C15–C21) | WBO(P2–O1) |
|---|---:|---:|---:|
| 反应物端点 | 0.761 | <0.02 | 1.211 |
| TS | 0.258 | 0.279 | 1.409 |
| 产物端点 | <0.02 | 1.003 | 1.409 |

反应物 O1–P2–C21 角为 170.61°，说明迁移的 C21 吡啶基处于与 O1 近共线的轴向位置，接受体 C15 为赤道向，因此这条路径支持 apical-to-equatorial 偶联。

产物侧吡啶环 C15–C20 键级从近芳香平均分布变为明显单双键交替，支持 dearomatized post-coupling intermediate。形成键和断裂键在 TS 中均只有部分键级，且 IRC 后仍存在稳定中间体，支持这条局部路径的 stepwise、asynchronous 描述。

但 P–O 键级和距离在本次结构中有明显变化，工具箱没有 NBO/自然布居或氧孤对电子占据分析 Action。因此不能由这些 Wiberg 键级复现论文“氧孤对电子参与变化很小”的特定电子结构结论。

## 8. 六个任务逐项审计

### Q1 — Heterobiaryl_PV_01_Protonation

**任务所需原始输入**

- 正确的 P0、P1、P2 分子身份、质子化位点、电荷和多重度；
- 每个状态足够覆盖 P(V) 轴向/赤道排列及构象的未优化种子；
- 统一的乙醇、353.15 K、1 M 条件定义；
- Py–Py 反应的原子映射或反应物/产物连接关系。后者当前仍未作为明确产品输入提供。

**本次实际计算**

- 3 次 RDKit ETKDG 构象生成；
- 9 次 xTB 几何优化；
- P0/P1/P2 最低候选的 Hessian 和振动分析；
- P0/P1/P2 Py–Py 原生扫描各 1 条；只有 P2 完成并进一步得到 TS、频率和 IRC。

**与论文参考的比较**

- 论文参考：P0/P1/P2 Py–Py 势垒约 30/20/14 kcal mol⁻¹，连续质子化降低势垒。
- 本次计算：只能验证 P2 的一条局部 Py–Py 路径；P0 只有 1 帧，P1 只有 2 帧，均没有一阶 TS 和连接性证据。

**为什么当前工具箱不能复现作者结果**

1. 当前工具箱没有 NEB、GSM、string 或稳健的双端反应路径 Action；`locate_transition_state` 是单端局部优化，不能从未优化种子自动发现 P0/P1/P2 对应 TS。
2. xTB Action 不暴露溶剂参数，`pysisyphus` TS/IRC 也没有乙醇溶剂；原生 COSMO 扫描与论文 SMD 条件不等价。
3. 没有自动枚举 P(V) 轴向/赤道异构体、Berry pseudorotation 和构象预平衡的能力；少量 ETKDG seed 不能保证找到每个质子化态的正确反应构象。
4. P0/P1 扫描在 40 分钟资源上失败或超时，不能产生三个状态的同条件驻点、频率、IRC 和自由能。
5. ORCA typed SMD(ethanol) 输入当前渲染失败；工具箱也没有复现论文 ωB97XD/SMD 优化、DLPNO-CCSD(T) 外推和 GoodVibes 组合自由能的完整自动流程。

**判定：`partially_solvable`。** 可建立并验证三个质子化态的局部最小值，也能对 P2 做路径验证；不能计算可比较的 P0/P1/P2 活化自由能趋势。

**要变为 solvable 需补充**：明确 Py–Py 产物/原子映射；更多独立 P(V) 构象；带乙醇溶剂的双端路径搜索；P0/P1/P2 全部 TS+频率+IRC；可工作的 SMD、统一 353.15 K/1 M 准谐热化学及高水平单点后端。

### Q2 — Heterobiaryl_PV_02_CC_Selectivity

**任务所需原始输入**

- Q1 的 P0/P1/P2 体系；
- Py–Py 和 Ph–Py 两条路径的无歧义成键/断键映射或产品结构；
- 各路径相关的轴向/赤道反应构象，而不只是同一个未标注 P(V) seed 集合。

**本次实际计算**

- 共用 Q1 的 9 个种子筛选；
- 对 P2 Py–Py 和 P2 Ph–Py 进行了相同类型的原生 xTB 松弛扫描；
- P2 Py–Py 完成 TS/频率/IRC；P2 Ph–Py 在第一帧后超时。

**与论文参考的比较**

- 论文参考：Py–Py 的 P0/P1/P2 势垒约 30/20/14，Ph–Py 约 37/27/25 kcal mol⁻¹；选择性主要为动力学控制。
- 本次计算：没有任何同一状态下完整验证的 Py–Py/Ph–Py 成对势垒，不能计算 ΔΔG‡ 或可靠选择性。

**为什么当前工具箱不能复现作者结果**

1. Ph–Py 路径没有收敛扫描、TS、目标虚频或 IRC；单个起始帧不构成势垒证据。
2. 输入没有给出两个产品和断裂 P–C 键的明确映射，工具箱也没有从分子图自动枚举“哪一个轴向配体向哪一个赤道配体迁移”的 P(V) 反应生成器。
3. 少量未标注构象不足以保证 Py–Py 与 Ph–Py 都从各自最低反应构象出发；构象代价可能与选择性差值同量级。
4. 缺少带溶剂的稳健双端搜索和统一自由能流程，无法在共同条件下得到论文 14 vs 25 kcal mol⁻¹ 等比较。
5. 当前 40 分钟扫描资源已证明对 Ph–Py 不足；更高水平 DFT 路径优化和频率将需要显著更多资源。

**判定：`partially_solvable`。** 能定义并尝试两条 C–C 路径，且能验证其中一条 P2 Py–Py 局部路径；不能得出论文级选择性结论。

**要变为 solvable 需补充**：Py–Py/Ph–Py 映射产品；两类反应构象集合；双端路径 Action；两条路径的同方法 TS、频率、IRC、353.15 K/1 M 乙醇自由能；足够的 DFT 计算资源。

### Q3 — Heterobiaryl_PV_03_CC_vs_CO

**任务所需原始输入**

- P2 正确结构和构象；
- C–C 与 C–O 两条竞争路径的产品结构及无歧义原子映射；
- 与产物分布有关的实验观测。当前保留 E02、E10、E11、E12，但这些观测不能替代路径计算。

**本次实际计算**

- P2 三种 seed 优化筛选；
- P2 Py–Py 扫描、TS、频率、IRC、端点优化和键级分析；
- P2 C–O 探索性扫描。第二帧相对第一帧约 +11.87 kcal mol⁻¹，O1–C15 从 2.273 Å 到 2.073 Å，P2–C15 从 1.855 Å 到 2.091 Å，但任务在 2/5 帧超时。

**与论文参考的比较**

- 论文参考：P2 C–C 约 14，C–O 约 18 kcal mol⁻¹，C–C 为主路径。
- 本次计算：C–C 有一条局部验证路径；C–O 没有收敛扫描、TS、目标虚频、IRC 或稳定产品，不能做 14 vs 18 比较。

**为什么当前工具箱不能复现作者结果**

1. 数据只给 P2 反应物，没有 C–O 产品或 atom-mapped reaction。审计尝试了“形成 O1–C15、断裂 P2–C15”的一种假设，但另一种 P–O 断裂/不同配体迁移定义也可能合理，当前输入无法判定作者所指具体支路。
2. 工具箱没有 P(V) 竞争反应自动枚举器，也没有双端 NEB/GSM/string Action；局部 TS 搜索必须先有人为提供足够接近的猜测。
3. C–O 扫描在 40 分钟内只完成 2 帧，不能把 +11.87 kcal mol⁻¹ 的未收敛点当作势垒或上界。
4. C–C 和 C–O 没有在同一套溶剂、构象、频率和标准态条件下获得完整驻点，无法比较 ΔΔG‡。
5. 产物比例、EtONa 或 NMR 观测可以约束机理，但不能唯一反演两条微观活化自由能。

**判定：`partially_solvable`。** C–C 分支可做局部验证，C–O 分支的定义和计算均不完整，因此主要竞争结论不可完成。

**要变为 solvable 需补充**：明确 atom-mapped C–O 产品/候选产品集；各候选的 P(V) 反应构象；双端路径搜索；C–C/C–O 同条件 TS+频率+IRC；统一乙醇溶液自由能和更长计算资源。

### Q4 — Heterobiaryl_PV_04_Coupling_Mechanism

**任务所需原始输入**

- P0/P1/P2 的正确未优化结构；
- 目标 Py–Py 反应的成键/断键定义；
- 足以区分 concerted/stepwise、同步/异步和 apical/equatorial 迁移的路径与电子结构分析能力。

**本次实际计算**

- 对 P2 Py–Py 定位一阶 TS；
- Hessian/振动显示一个目标虚频 -227.82 cm⁻¹；
- 双向 IRC 连接反应物样端点与 dearomatized 产物侧局部最小值；
- 对反应物、TS、产物侧端点计算 Wiberg 键级和环内键级；
- 根据 O1–P2–C21 = 170.61° 识别 axial donor / equatorial acceptor。

**与论文参考的比较**

- 本次局部路径与论文的 stepwise、asynchronous、apical-to-equatorial 及 dearomatized intermediate 结论相符。
- 氧的特定“lone-pair participation changes little”没有被复现。

**为什么当前工具箱仍不能完整复现作者结果**

1. 只验证了一条由人为二维扫描引导的局部 P2 路径；没有自动系统搜索其他轴向/赤道排列、协同路径或低能 pseudorotation 路径，因此不能严格排除 concerted 替代机制。
2. `locate_transition_state` 本身是单端局部优化，反应物/产物输入不会自动形成双端反应通道；成功高度依赖预先构造的近 TS 猜测。
3. TS/IRC 使用气相 GFN2-xTB，与作者乙醇 SMD DFT 路径的势能面不同；CPCM DFT 仅做单点，不能证明溶剂下仍为同一驻点和连接关系。
4. 工具箱只有 Wiberg 键级，没有 NBO、自然占据数、孤对轨道占据或沿 IRC 的等价电子布居 Action，不能直接检验氧孤对电子结论。
5. 没有完整的动力学/动态轨迹来检验 IRC 后中间体寿命与后续 collapse；这里只能证明该方法下存在一个局部最小值。

**判定：`partially_solvable`。** 这是六个任务中证据最完整的一个，但“支持一条参考机理路径”不等于“排除所有竞争机理并复现全部电子结构结论”。

**要变为 solvable 需补充**：系统 P(V) 异构体/路径枚举；溶剂 DFT TS+IRC；替代 concerted 路径搜索；NBO/孤对占据分析；必要时后续 collapse 的路径与动力学验证。

### Q5 — Heterobiaryl_PV_05_Rate_Determining_Step

**任务所需原始输入**

- 醇加成前的 phosphonium salt；
- EtOH/EtO⁻、酸、反离子及可能的质子转移络合物；
- OMe、Me、H、Cl 取代系列的所有反应物结构；
- 醇加成、P(V) 偶联、dearomatized 中间体 collapse 的反应物/产物映射；
- 速率实验的原始时间序列、重复测量和误差，而不只是四个取整相对速率。

**本次实际计算**

- 对输入中的 P2 P(V)-OMe 做三构象筛选；
- 新计算一条下游 P2 Py–Py ligand-coupling TS/IRC；
- 使用 E01、E02、E04–E12 的实验摘要，能读取 OMe 0.16、Me 0.37、H 1.00、Cl 1.89 的相对速率次序。

**与论文参考的比较**

- 论文参考：醇向 phosphonium P 的加成为决速步骤；P(V) ligand coupling 为选择性决定步骤；dearomatized 中间体 collapse 为强不可逆步骤。
- 本次计算：只直接计算了第二个角色的一条下游 ligand-coupling 路径；没有计算醇加成或 collapse。

**为什么当前工具箱不能复现作者结果**

1. 当前三个结构已经是醇加成后的 P(V)-OMe 中间体，决定总体速率的上游 phosphonium + alcohol 反应根本不在输入中。缺少反应物时，任何 Action 都无法计算其势垒。
2. 没有显式乙醇、酸、反离子和质子接力模型，无法定义醇加成究竟是中性 EtOH 进攻、EtO⁻ 进攻还是耦合质子转移。
3. 缺少 OMe/Me/H/Cl 四个底物的结构，不能计算取代基效应并与相对速率对照。
4. 只有四个取整相对速率，没有原始动力学曲线、重复和误差，不能完成任务要求中的不确定度估计，也不能可靠拟合 Hammett/速率模型。
5. 缺少 post-coupling collapse 的产品/副产物结构及路径；本次只找到 dearomatized 局部最小值，不能直接证明后续 collapse 强不可逆。
6. 工具箱没有自动多分子反应网络、质子转移/显式溶剂采样或增强采样 Action；即使补结构，也需要明确反应模型和较高计算资源。

**判定：`not_solvable`。** 虽然实验速率次序可读取、下游偶联可部分计算，但核心问题“哪一步决速”所需的上游反应物和原始动力学证据不存在，不能靠工具箱补猜。

**要变为 solvable 需补充**：完整 phosphonium/EtOH/酸/反离子体系；四个取代底物；atom-mapped 醇加成和 collapse 反应；动力学原始数据与误差；显式或可靠连续介质质子转移路径能力；三阶段统一自由能计算。

### Q6 — Heterobiaryl_PV_06_End_to_End

**任务所需原始输入**

- Q1–Q5 的全部结构、反应映射、实验原始数据和统一反应条件；
- 从 phosphonium 醇加成、P(V) 构象/质子化、Py–Py/Ph–Py/C–O 竞争、dearomatized 中间体到 collapse 产物的完整反应网络。

**本次实际计算**

- 完成 P0/P1/P2 种子筛选；
- 对五条探索路径启动扫描；
- 完整验证一条 P2 Py–Py 局部 TS/IRC，并做频率、键级、气相热化学和 ORCA CPCM 单点；
- 保存所有失败、超时与未解决分支。

**与论文参考的比较**

- 能局部支持“双质子化 P(V) 可发生 Py–Py ligand coupling，并形成 dearomatized 中间体”的子结论。
- 不能建立 P0/P1/P2 完整势垒趋势、Py–Py/Ph–Py/C–O 完整排序、总体决速步骤和最终 collapse 的端到端自由能网络。

**为什么当前工具箱不能复现作者结果**

1. Q6 继承 Q1 的 P0/P1 TS 缺失、Q2 的 Ph–Py 路径缺失、Q3 的 C–O 定义/驻点缺失以及 Q5 的上游 phosphonium/醇加成硬缺口。
2. 当前数据没有完整 atom-mapped 反应网络；工具箱不能只凭一个 P(V) 反应物自动生成所有可能产品、配体迁移和 collapse 路径。
3. 当前后端组合不能自动执行论文级 ωB97XD/SMD 几何与频率、DLPNO-CCSD(T) 外推、GoodVibes 353.15 K/1 M 统一后处理；typed ORCA SMD 还存在实际渲染失败。
4. 多条 xTB 扫描在每条 40 分钟下超时，说明当前资源不足以系统完成所有质子化态、构象和竞争通道，更不用说完整 DFT 复核。
5. 缺少 NBO/孤对分析、显式质子转移和反应网络/构象自由能汇总能力，无法自动形成论文同等级的端到端机理证据链。

**判定：`not_solvable`。** 已完成的子计算不足以回答完整端到端任务，核心缺失不是语言推理可弥补的。

**要变为 solvable 需补充**：先补齐 Q1–Q5 所列数据和工具能力，再提供完整反应网络、可恢复/并行的长时路径搜索、统一溶剂 DFT 驻点验证、高水平单点及准谐溶液热化学工作流。

## 9. 当前工具箱的关键能力缺口

归纳来看，影响六个任务可复现性的不是“Action 数量少”，而是以下几个关键链条没有闭合：

1. **反应定义缺口**：没有 atom-mapped 产品和完整反应网络时，工具箱不能可靠猜测 P(V) 中究竟哪条 P–C/P–O 键断裂、哪对原子成键。
2. **路径搜索缺口**：没有 NEB、GSM、string 等双端路径 Action；单端 TS 优化需要高质量近 TS 猜测。
3. **P(V) 构象学缺口**：没有轴向/赤道异构体、Berry pseudorotation 和反应构象自动枚举/排序。
4. **溶剂链条不一致**：xTB Action 和 pysis TS/IRC 无溶剂；原生 COSMO 只是近似；ORCA typed SMD(ethanol) 实际失败；CPCM 仅完成单点。
5. **论文级热化学缺口**：当前内部 RRHO 不是 GoodVibes 准谐/低频流程，也没有自动组合 DFT 频率修正、DLPNO-CCSD(T) 外推和 353.15 K、1 M 溶液标准态。
6. **电子结构分析缺口**：有 Wiberg 键级，但无 NBO/自然占据/氧孤对轨道分析。
7. **上游反应数据缺口**：Q5/Q6 缺 phosphonium、EtOH/EtO⁻、酸/反离子、取代系列及 collapse 产物，属于输入硬缺失。
8. **实验不确定度缺口**：只有汇总相对速率，没有原始时间序列、重复和误差，无法做可信的不确定度传播。
9. **计算资源缺口**：5 条低成本扫描中只有 1 条完成；系统 DFT 路径枚举需要更长 walltime、并行与可恢复计算。

## 10. 保存的真实证据

证据根目录：`docs/check/heterobiaryl_task_feasibility_audit/`，约 263 MB。

关键文件：

- `calculations/seed_screen_summary.json`：9 个种子优化、结构审计、相对能和代表最小值频率；
- `calculations/selected_representatives.json`：各状态代表结构；
- `pathway_probes/summary.json`：5 条原生扫描状态；
- `pathway_probes/records/*.json`：各扫描请求、帧数、距离和失败/超时；
- `pathway_validations/P2_PyPy/validation_summary.json`：TS、虚频和 IRC；
- `pathway_validations/P2_PyPy/mechanism_probe_summary.json`：端点优化、Wiberg 键级、构型和 dearomatization；
- `pathway_validations/P2_PyPy/thermochemistry_probe_summary.json`：气相 RRHO 诊断及局限；
- `pathway_validations/P2_PyPy/orca_smd_ethanol_single_point_summary.json`：SMD 合同失败；
- `pathway_validations/P2_PyPy/orca_cpcm_ethanol_single_point_summary.json`：CPCM 单点结果；
- `calls/**/{request,result,summary}.json`：种子生成、优化、Hessian、振动等真实调用；
- `pathway_validations/P2_PyPy/calls/**/{request,result,summary}.json`：TS/IRC/能量/键级/热化学/ORCA 调用；
- `outputs/execution_jobs/*`：原生 xTB 作业请求、日志和软件输出；
- `_tool_artifacts/index.jsonl` 与 `_tool_artifacts/objects/`：工具箱 artifact 索引和内容对象。

本次新增的两个脚本只用于可重复整理和留存真实调用，不是用脚本替代化学计算：

- `scripts/organize_heterobiaryl_task_inputs.py`：从独立生成的种子和最小实验记录构建六个任务的直接可读数据目录；
- `scripts/run_heterobiaryl_feasibility_audit.py`：按固定参数调用工具箱完成种子筛选并保存 request/result/summary。

路径扫描、TS、IRC、频率、键级、热化学和 ORCA 均由真实化学后端执行；脚本本身不写入预设能垒或论文答案。

## 11. 最终建议

1. 保留当前整理后的数据目录，废止六任务共用作者输出衍生 ZIP 的设计。
2. Q1–Q4 可继续作为“允许失败并考查证据门控”的高难部分可解任务，但任务说明应承认当前工具箱不能保证完成全部路径。
3. Q5 在补齐 phosphonium/醇加成体系、取代系列和动力学原始数据前，不应被标为可独立计算完成。
4. Q6 在 Q1–Q5 数据与工具链闭合前，不应作为可稳定完成的端到端示例。
5. 若 benchmark 期望答案必须数值复现论文，应先增加明确的 atom-mapped 产品、反应构象或双端路径输入、可工作的乙醇 SMD、长时 DFT 资源及统一 GoodVibes/高水平单点流程；否则评分应奖励正确报告失败和缺口，而不是奖励猜中 30/20/14 等参考数值。

最终结论：当前六个示例可以测试智能体是否会正确整理输入、调用工具、验证驻点并诚实处理失败，但不能被宣称为六个都能仅凭现有输入和当前工具箱稳定复现论文结果的“可完成示例”。
