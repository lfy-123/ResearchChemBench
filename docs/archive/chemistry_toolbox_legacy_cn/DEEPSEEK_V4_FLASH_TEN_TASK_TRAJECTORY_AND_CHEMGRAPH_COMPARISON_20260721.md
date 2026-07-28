# DeepSeek V4 Flash 十任务轨迹审计与 ChemGraph 工具对照报告

> 审计日期：2026-07-21
> Agent：OpenCode 1.14.41 + `deepseek/deepseek-v4-flash`
> 新工具箱：ResearchChemBench Chemistry MCP，完整原子 Action Catalog
> 原工具参考：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ChemGraph/src/chemgraph/tools`

## 1. 结论摘要

| 指标 | 最终结果 |
|---|---:|
| ChemGraph 原任务 | 10 |
| 正式得分 | **8/10** |
| 实际化学 MCP 调用 | **76** |
| 成功调用 | **71** |
| `invalid_request` | **5** |
| Backend 执行失败 / 超时 / 不可用 / 不支持 | **0** |
| MCP 调用成功率 | **93.4%** |
| 实际使用的独立 Actions | **9** |
| 实际使用的 Backend ID | **6** |

对用户问题的直接回答如下：

1. **从工具名称看，并不一致。** 新评测没有暴露 ChemGraph 的 `molecule_name_to_smiles`、`smiles_to_coordinate_file`、`run_ase` 等原函数，Agent 调用的是新工具箱的 Action 名称。
2. **从科学能力看，绝大部分一致。** 76 次调用中，71 次属于 ChemGraph 已有能力的等价替代或原子化拆分；只有 5 次 `standardize_structure` 是 ChemGraph 原公共工具中没有的新增预处理 Action。
3. **Agent 没有被大量新增软件或无关 Action 分散。** 十个任务只使用了 PubChem、RDKit、MACE、xTB、内部振动分析和内部热化学六个 Backend；没有调用 ORCA、Gaussian、GPAW、MD、周期材料、反应网络等与这些任务无关的新后端。
4. **最显著的结构变化是 `run_ase` 被拆开。** ChemGraph 的一个 `run_ase(driver="thermo")` 会隐式完成优化、Hessian、振动、对称性和热化学；新工具箱要求 Agent 显式编排 `optimize_geometry → calculate_hessian → derive_vibrational_modes → calculate_energy → derive_thermochemistry`。
5. **本轮轨迹证明原子 Action 方案能够工作。** CO2 热化学、氨合成反应热和修复后的甲烷燃烧反应热都由 Agent 自主编排完整依赖链并得到正确结果。

## 2. 最终采用的运行结果

最初十任务并发批次中，任务 005 和 024 在 OpenCode 启动阶段遇到共享 SQLite 数据库的 WAL 初始化竞争，未进入 MCP 调用。修复为每个 run 使用独立 `OPENCODE_DB` 后，两任务并发补跑成功。因此最终十任务由三个批次组合：

| 用途 | 批次目录 | 采用的任务 |
|---|---|---|
| 主十任务批次 | `workspaces/cli_runs/batch_20260721_120133_9a28b2` | 001、006、007、023、025、028、032 |
| SQLite 隔离补跑 | `workspaces/cli_runs/batch_20260721_121653_4c5925` | 005、024 |
| MCP 长调用超时修复验证 | `workspaces/cli_runs/batch_20260721_122734_5b947b` | 031 |

最后一次任务 031 重跑使用的是修复后的长调用超时配置；它替代了主批次中旧的 031 轨迹。

## 3. 十个任务逐项结果与工具映射

| Task | 任务目标 | 最终分数 | 新工具箱实际 Action | Backend | 与 ChemGraph 的关系 | 轨迹判断 |
|---|---|---:|---|---|---|---|
| 001 | SO2 名称转 SMILES | 1 | `resolve_chemical_identity` | PubChem | 等价于 `molecule_name_to_smiles`，但返回更完整的身份记录 | 简洁、正确 |
| 005 | MACE 优化 SO2 并报告能量 | 1 | `standardize_structure → generate_3d_structure → optimize_geometry` | RDKit、MACE | 前两步对应/扩展 SMILES 转坐标；优化对应 `run_ase(driver="opt")` | 合理，新增了显式标准化 |
| 006 | MACE 水分子振动频率 | 0 | `calculate_hessian → derive_vibrational_modes` | MACE、internal_vibrations | 对应 `run_ase(driver="vib")` 内部的 Hessian 与频率步骤 | 不完整：Agent 跳过了几何优化，数值偏差 |
| 007 | 800 K CO2 GFN2-xTB 热化学 | 1 | 身份解析、标准化、3D、优化、Hessian、振动、能量、热化学 | PubChem、RDKit、xTB、内部派生 | 完整展开 `molecule_name_to_smiles + smiles_to_coordinate_file + run_ase(thermo)` | 完整、正确 |
| 023 | SMILES 指定 CO2 的 800 K 热化学 | 1 | 标准化、3D、优化、Hessian、振动、能量、热化学 | RDKit、xTB、内部派生 | 完整展开 `smiles_to_coordinate_file + run_ase(thermo)` | 完整、正确 |
| 024 | CO 的 GFN2-xTB 偶极矩 | 0 | `standardize_structure → generate_3d_structure → calculate_dipole_moment` | RDKit、xTB | 对应 `smiles_to_coordinate_file + run_ase(driver="dipole")` | 工具均成功；评分失败来自单位语义不一致 |
| 025 | MACE 计算 N2 单点能 | 1 | `standardize_structure → generate_3d_structure → calculate_energy` | RDKit、MACE | 对应 `smiles_to_coordinate_file + run_ase(driver="energy")` | 简洁、正确 |
| 028 | GFN2-xTB 优化 CO | 1 | `generate_3d_structure → optimize_geometry` | RDKit、xTB | 对应 `smiles_to_coordinate_file + run_ase(driver="opt")` | 简洁、正确 |
| 031 | 300 K MACE 甲烷燃烧反应 Gibbs 能 | 1 | 对四个物种分别执行 3D、优化、Hessian、振动、能量、热化学 | RDKit、MACE、内部派生 | 四次展开 `run_ase(driver="thermo")`；反应算术由 Agent 完成 | 修复超时后全 MCP 链路正确 |
| 032 | 400 K GFN2-xTB 氨合成反应 Gibbs 能 | 1 | 对三个物种分别执行 3D、优化、Hessian、振动、能量、热化学 | RDKit、xTB、内部派生 | 三次展开 `run_ase(driver="thermo")`；反应算术由 Agent 完成 | 完整、正确 |

## 4. 实际 Action 使用统计

| Action | 调用数 | ChemGraph 对应 | 分类 |
|---|---:|---|---|
| `optimize_geometry` | 15 | `run_ase(driver="opt/vib/thermo/ir")` 的优化阶段 | 原能力的显式原子化 |
| `generate_3d_structure` | 13 | `smiles_to_atomsdata` / `smiles_to_coordinate_file` | 直接等价替代 |
| `calculate_hessian` | 11 | `run_ase(driver="vib/thermo/ir")` 中 ASE `Vibrations` 的有限差分阶段 | 原隐藏能力公开为原子 Action |
| `derive_vibrational_modes` | 10 | `run_ase(driver="vib/thermo/ir")` 中的频率解析 | 原隐藏能力公开为原子 Action |
| `calculate_energy` | 10 | `run_ase(driver="energy")`，以及优化/热化学流程中的电子能 | 原能力的显式原子化 |
| `derive_thermochemistry` | 9 | `run_ase(driver="thermo")` 中 ASE `IdealGasThermo` | 原隐藏能力公开为原子 Action |
| `standardize_structure` | 5 | 无直接公共工具；ChemGraph 只在 RDKit 转换过程中隐式处理部分结构 | **新增公共预处理 Action** |
| `resolve_chemical_identity` | 2 | `molecule_name_to_smiles` | 直接等价并扩展返回内容 |
| `calculate_dipole_moment` | 1 | `run_ase(driver="dipole")` | 原能力的显式原子化 |

按调用次数划分：

| 类型 | 调用数 | 占比 |
|---|---:|---:|
| ChemGraph 名称/结构工具的直接等价替代 | 15 | 19.7% |
| ChemGraph `run_ase` 内部能力的原子化调用 | 56 | 73.7% |
| ChemGraph 原公共 API 没有的新增预处理 Action | 5 | 6.6% |

因此，**93.4% 的实际调用位于 ChemGraph 原有科学能力范围内；新增 Action 只占 6.6%，而且只是 RDKit 结构标准化。**

## 5. 实际 Backend 使用统计

| Backend | 调用数 | 软件/实现 | ChemGraph 是否已有 | 说明 |
|---|---:|---|---|---|
| `mace` | 20 | MACE 0.3.16 | 是 | 同一软件家族；新工具箱显式选择模型、设备和下载许可 |
| `rdkit` | 18 | RDKit | 是 | ChemGraph 用于 SMILES 3D；新工具箱额外公开标准化 Action |
| `xtb` | 17 | standalone xTB 6.7.1 | **实现层面新增** | ChemGraph 任务期望通过 TBLite/ASE 使用 GFN2-xTB；科学方法相同，但后端程序路径不同 |
| `internal_vibrations` | 10 | NumPy/ASE 语义的 Hessian 质量加权与模式派生 | 隐式已有 | ChemGraph 将该步骤藏在 `run_ase` 中；新工具箱注册为独立 Backend |
| `internal_thermochemistry` | 9 | ASE `IdealGasThermo` 语义的 RRHO 热化学 | 隐式已有 | 原来由 `run_ase` 自动决定；现在要求 Agent 显式给温度、压力、几何、对称数和自旋 |
| `pubchem` | 2 | PubChem | 是 | 对应 ChemGraph 的名称转 SMILES 数据源 |

这些任务没有使用任何与原任务无关的新后端。因此，本轮没有证据表明“大工具箱”会自然诱导 Agent 随机选择不相关软件。

## 6. ChemGraph 原工具与新 Action 的结构差异

### 6.1 ChemGraph 相关公共工具

十个任务在原基准中主要依赖：

- `molecule_name_to_smiles`
- `smiles_to_atomsdata`
- `smiles_to_coordinate_file`
- `run_ase`
- `calculator`

`run_ase` 支持 `energy`、`dipole`、`opt`、`vib`、`thermo` 和 `ir` driver。对于 `vib`、`thermo` 和 `ir`，它会在一次调用中自动执行几何优化和有限差分振动；`thermo` 还会自动判断线性、计算旋转对称数、从多重度推导自旋，并调用 `IdealGasThermo`。

### 6.2 新工具箱的处理方式

新工具箱没有复刻 `run_ase`，而是公开可组合的科学动作：

```text
generate_3d_structure
        ↓
optimize_geometry
        ↓
calculate_hessian
        ↓
derive_vibrational_modes
        ↓
calculate_energy
        ↓
derive_thermochemistry
```

这个图只是十个任务中 Agent 实际选择出的依赖链，不是工具箱强制流程。Agent 可以跳过、替换、交叉比较或改用其他 Backend；任务 006 实际跳过优化并因此得到错误频率，正说明系统没有偷偷补齐固定流程。

## 7. 两个未得分任务的真实原因

### 7.1 ChemGraph_006：Agent 编排错误，不是后端故障

- MACE Hessian 和内部振动模式调用都成功。
- Agent 直接使用近似水分子坐标计算 Hessian，没有先执行 MACE 几何优化。
- 报告的非对称伸缩频率为 4097.87 cm⁻¹，而参考为 3723.82 cm⁻¹，偏差约 10%。
- 第一次 Hessian 调用还漏填显式 `displacement_angstrom`，被契约正确拒绝，随后修正。

如果工具箱自动补做优化，会提高这一题得分，但会违反 benchmark 评估 Agent 编排能力的目标。因此本报告不建议增加隐式预优化或默认回退。

### 7.2 ChemGraph_024：单位比较问题，不是计算失败

- 三次 MCP 调用全部成功。
- standalone xTB 输出的分量是原子单位，程序同时给出总模长 Debye；新适配器将主结果规范化为 Debye，Agent 报告 `[-0.635, 0, 0] D`。
- ChemGraph/TBLite 参考向量 `[-0.1278, 0, 0]` 的单位是 `e·Å`，评估器却直接比较了数值，没有换算单位。
- 本次 xTB 分量 `-0.25 e·a0` 换算为 `-0.13229 e·Å`，与参考 `-0.1278 e·Å` 的相对误差约 3.5%，实际处于 5% 容差内。

代码现已在 xTB 结果中同时返回：

- `dipole` / `dipole_debye`
- `dipole_e_angstrom`
- `dipole_atomic_units`
- `magnitude` / `magnitude_e_angstrom`

后续应让评估器按单位归一化后再比较，而不是改变物理结果去迎合无单位参考值。

## 8. 框架问题、修复及验证

### 8.1 并发 OpenCode SQLite 冲突

症状：首批并发启动时，005 和 024 报 `PRAGMA journal_mode = WAL` 相关错误，在 MCP 调用前退出。

修复：每个 run 创建独立的：

```text
<workspace>/_opencode/opencode.db
```

并设置独立的 `OPENCODE_DB` 和 `OPENCODE_WORKSPACE_ID`。005 与 024 随后并发补跑成功。

### 8.2 OpenCode MCP 默认 30 秒工具超时

旧 031 轨迹中，MACE Hessian 在服务端最终成功，但 OpenCode 对部分超过约 30 秒的调用先返回空错误。Agent 因此重复提交并最终绕过 MCP，直接使用 shell/Python 调 ASE。

OpenCode MCP 实现定义了 30,000 ms 默认值，并允许通过每个 MCP server 的 `timeout` 配置覆盖；参见 [OpenCode MCP source](https://github.com/anomalyco/opencode/blob/dev/packages/opencode/src/mcp/index.ts)。

修复：生成的 `opencode.json` 现在包含：

```json
{
  "mcp": {
    "researchchem_toolbox": {
      "timeout": 3600000
    }
  }
}
```

该值可通过 `RESEARCHCHEMBENCH_MCP_TOOL_TIMEOUT_MS` 配置。

验证结果：

| 031 轨迹 | 分数 | MCP 成功/总调用 | Bash 科学计算 | 结果 |
|---|---:|---:|---|---|
| 修复前旧轨迹 | 0 | 16/28 | 有，最终绕过 MCP | -8.06 eV |
| 修复后最终轨迹 | **1** | **24/28** | **无** | **-8.11027 eV** |

修复后的第一项 MACE Hessian运行了 54.818 秒，OpenCode 正常等待并接收结果；随后 Agent 继续调用全部振动、能量和热化学 Actions。

### 8.3 Agent 数据库不应成为科学 Artifact

独立数据库放入 workspace 后，trace 的文件差异扫描会把 `opencode.db-wal` 和 `opencode.db-shm` 当作工具生成文件。现已把 `_opencode` 加入追踪排除目录，避免运行时数据库污染科学 Artifact。

### 8.4 MACE 模型别名文字歧义

旧描述使用 `medium/MACE-MP-0-medium` 表示两个别名，Agent 曾把斜杠误解成相对文件路径。描述现改为四个带引号的独立精确值：

- `medium-mpa-0`
- `MACE-MPA-0-medium`
- `medium`
- `MACE-MP-0-medium`

没有添加模型自动猜测、默认模型或后端切换。

## 9. 最终 5 次非成功调用

最终十任务中只有 5 次 `invalid_request`：

| Task | 次数 | 原因 | 后续行为 |
|---|---:|---|---|
| 006 | 1 | MACE Hessian 漏填 `displacement_angstrom` | Agent 显式补为 0.01 Å，随后成功 |
| 031 | 4 | 四个物种首次 MACE 优化漏填 `allow_model_download` | Agent 显式补为 `false`，四次随后成功 |

这些是 Agent 未满足已公开调用契约的错误，不是服务端崩溃。保留显式拒绝是必要的，因为自动填 `0.01 Å` 或自动填 `allow_model_download=false` 都会削弱 benchmark 对参数选择能力的评估。

## 10. 轨迹是否合理

| 结论 | 任务 |
|---|---|
| 简洁且完全合理 | 001、005、025、028 |
| 原子链较长但依赖关系正确 | 007、023、031、032 |
| 工具运行正常，但 Agent 科学规划错误 | 006 |
| 工具运行正常，评分单位语义有问题 | 024 |

007、023、031 和 032 是最能体现新工具箱目标的轨迹：Agent 自主选择了结构工具、计算后端、模型/方法、优化、Hessian、振动派生和热化学参数，并将多个物种结果组合为最终科学结论。

## 11. 后续优化建议

1. **不要恢复 `run_ase` 式流程工具。** 当前结果已经证明原子 Action 能完成原任务，同时任务 006 能真实暴露 Agent 编排缺陷。
2. **继续增强 Backend-specific JSON Schema 的可见性。** 目标是让 `allow_model_download`、`displacement_angstrom` 等必填字段更醒目，但仍由 Agent 明确提供，不能自动补默认值。
3. **统一所有偶极 Backend 的标准单位。** xTB 已同时返回 Debye、`e·Å` 和原子单位；其他 Backend 也应统一主单位并保留原始单位。
4. **评估器采用能力等价与单位归一化。** 不应因 `run_ase` 被合理拆成多个 Action 就扣分，也不应直接比较不同单位的裸数值。
5. **保留每 run 独立 OpenCode 数据库和长 MCP timeout。** 这是并发科学评测稳定运行的必要框架配置，不影响 Agent 的科学选择权。

## 12. 验证记录

- 最终任务 031：score 1，完整 MCP 热化学链路，无 bash 科学计算。
- OpenCode 解析配置确认：`mcp.researchchem_toolbox.timeout = 3600000`。
- 针对性回归：35 tests passed in 76.88 s。
- 此前完整工具箱回归：183 tests passed in 442.70 s。
- Catalog：101 Actions、76 Backends、236 个 Action–Backend 组合均有调用证据；231 个成功组合，5 个仅受 PubChem 远端 503 影响。

## 13. 最终判断

这十个原 ChemGraph 任务在新工具箱中，Agent **主要选择的是 ChemGraph 已有科学能力的新 Action 表达**，而不是大量选择工具箱中新扩展的无关能力：

- 名称不同，是因为公共 API 已重构；
- 科学能力基本相同，但流程由一个 `run_ase` 拆成 Agent 自主编排的多个 Action；
- 唯一明显新增的公共科学步骤是 RDKit 结构标准化；
- standalone xTB 是新的后端实现选择，但执行的仍是任务要求的 GFN2-xTB 方法；
- 十任务没有使用扩展工具箱中的其他新领域软件。

因此，本轮结果符合“评估智能体自由选择、编排并调用多个科学工具”的设计目标。
