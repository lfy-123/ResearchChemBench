# GoodVibes 4.3.0 Backend 与调用指南

## 1. 定位

`goodvibes` 是量子化学输出的后处理 Backend，不负责选择或运行 Gaussian、ORCA、NWChem、Q-Chem、xTB 等上游计算。智能体先自行决定电子结构软件、方法、结构集合和计算顺序，得到完整输出文件后，再按需要选择 GoodVibes Action 或原生命令。

当前固定版本为 **GoodVibes 4.3.0**，运行环境为 `.tool_envs/goodvibes`，官方 `v4.3.0` 源码、测试数据和示例保存在 `.software_cache/goodvibes/4.3.0/source`。

## 2. 预定义 Actions

| Action | 主要作用 | 必需输入 | 主输出 |
|---|---|---|---|
| `derive_thermochemistry` | 对一个已完成的量化输出计算 RRHO/准谐振热化学 | `output_file` | `ThermochemistryResult` |
| `scan_thermochemistry_temperature` | 在智能体显式给出的温度点逐点计算热化学 | `output_files`, `temperatures_kelvin` | `ThermochemistryTemperatureSeries` |
| `analyze_thermochemical_ensemble` | 计算构象/结构集合的逐结构热化学和 Boltzmann 群体 | `output_files` | `ThermochemicalEnsembleResult` |
| `validate_thermochemistry_inputs` | 检查程序/理论级别/溶剂/电荷多重度/频率/重复结构等一致性 | `output_files` | `ThermochemistryValidationReport` |
| `analyze_thermochemical_selectivity` | 对两个或更多显式标签的构象集合计算群体和选择性 | `output_files`, `label_groups` | `ThermochemicalSelectivityResult` |
| `analyze_reaction_free_energy_profile` | 按智能体编写的 PES YAML 计算反应路径相对能量 | `output_files`, `profile_definition_file` | `ReactionFreeEnergyProfileResult` |

这些 Actions 都只做一个明确的科学操作，不会自动产生构象、补跑频率、选择量化软件或在失败后换 Backend。

## 3. 支持的上游输出

GoodVibes 4.3.0 官方支持 Gaussian 09/16、ORCA 5/6、NWChem、Q-Chem 6、xTB 和 ASE `extxyz`。实际文件必须包含对应 Action 所需的数据；例如只有单点能、没有频率的输出不能产生完整的 H/S/G。

Boltzmann、选择性和反应剖面通常要求参与比较的文件使用可比的理论级别。`validate_thermochemistry_inputs` 可先检查这些文件，但是否接受不同理论级别仍由智能体根据任务决定。

## 4. 显式科学参数

所有预定义 GoodVibes Actions 都要求智能体明确给出以下核心选择：

| 字段 | 可选值/格式 | 含义 |
|---|---|---|
| `standard_state` | `gas_1atm`, `solution_1mol_l`, `custom_concentration` | 标准态；自定义浓度还需 `concentration_mol_l` |
| `entropy_model` | `rrho`, `grimme`, `truhlar` | 标准 RRHO、Grimme mRRHO 或 Truhlar 低频修正 |
| `enthalpy_model` | `rrho`, `head_gordon` | 标准 RRHO 或 Head-Gordon 准谐振焓修正 |
| `frequency_scale_factor` | 正数或 `auto` | 配分函数频率缩放；`auto` 表示让 GoodVibes 按理论级别查询 |
| `zpe_scale_factor` | 正数、`auto` 或 `same_as_frequency` | ZPE 缩放；显式频率缩放与独立 `auto` ZPE 无法由 CLI 忠实表达，因此会被拒绝 |
| `symmetry_correction` | `true` / `false` | 是否用 pymsym 重新检测点群并施加外部对称性熵修正 |
| `imaginary_frequency_policy` | `retain`, `invert_below_threshold` | 保留虚频，或翻转小于显式阈值的虚频 |

条件参数：

- `entropy_model=grimme|truhlar`：必须给 `entropy_frequency_cutoff_cm1`。
- `entropy_model=grimme`：必须给 `free_rotor_inertia_model=global|per_conformer`。
- `enthalpy_model=head_gordon`：必须给 `enthalpy_frequency_cutoff_cm1`。
- `imaginary_frequency_policy=invert_below_threshold`：必须给正的 `imaginary_frequency_threshold_cm1`。
- `standard_state=custom_concentration`：必须给正的 `concentration_mol_l`。
- 集合/选择性 Action：必须给 `population_basis=electronic_energy|quasi_harmonic_gibbs` 和显式布尔量 `deduplicate_structures`。
- 启用去重时：必须给能量、转动常数和可空 RMSD 三个阈值。

`method_spec` 还可显式给出：

- `single_point_correction_suffix`：对应 GoodVibes `--spc`；配套单点文件必须已存在于频率输出旁。
- `custom_file_extensions`：额外文件扩展名列表。
- `exclude_pattern`：排除文件的 glob。
- `free_space_solvent`：GoodVibes 自由体积溶剂修正名称。

## 5. Action 调用示例

### 5.1 单文件热化学

```json
{
  "backend_id": "goodvibes",
  "inputs": {"output_file": "calculations/conf_01.log"},
  "method_spec": {},
  "action_settings": {
    "temperature_kelvin": 298.15,
    "standard_state": "solution_1mol_l",
    "entropy_model": "grimme",
    "enthalpy_model": "head_gordon",
    "entropy_frequency_cutoff_cm1": 100.0,
    "enthalpy_frequency_cutoff_cm1": 100.0,
    "free_rotor_inertia_model": "per_conformer",
    "frequency_scale_factor": 0.99,
    "zpe_scale_factor": 0.98,
    "symmetry_correction": true,
    "imaginary_frequency_policy": "retain"
  },
  "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300}
}
```

注意：振动缩放映射到 `-v/--vscal`；`--fs` 是熵低频截断值，不是缩放因子。

### 5.2 构象群体

在上述设置基础上增加：

```json
{
  "inputs": {"output_files": ["conf_01.log", "conf_02.log", "conf_03.log"]},
  "action_settings": {
    "population_basis": "quasi_harmonic_gibbs",
    "deduplicate_structures": true,
    "duplicate_energy_cutoff_kcal_mol": 0.05,
    "duplicate_rotational_cutoff_fraction": 0.01,
    "duplicate_rmsd_cutoff_angstrom": 0.125
  }
}
```

### 5.3 N-way 选择性

`label_groups` 使用精确文件成员，不使用框架猜测文件名：

```json
{
  "inputs": {
    "output_files": ["R_1.log", "R_2.log", "S_1.log", "S_2.log"],
    "label_groups": {
      "R": ["R_1.log", "R_2.log"],
      "S": ["S_1.log", "S_2.log"]
    }
  }
}
```

两个标签时返回群体、优势标签、ee 和以 Hartree 表示的 ΔΔG；三个或更多标签时返回规范化 N-way 群体。

### 5.4 反应自由能剖面

智能体自行编写 GoodVibes PES YAML，例如：

```yaml
pathways:
  reaction_1: ["reactants", "transition_state", "products"]
species:
  reactants: {files: ["R_conf1.log", "R_conf2.log"]}
  transition_state: {files: "TS_*.log"}
  products: {files: ["P_conf1.log", "P_conf2.log"]}
zero:
  reaction_1: reactants
format:
  units: kcal/mol
  decimals: 2
```

`profile_ensemble_mode` 的含义：

- `gconf`：GoodVibes 默认构象集合自由能处理。
- `lowest_conformer`：每个物种仅采用最低 qh-G 构象。
- `boltzmann_without_gconf`：保留构象 Boltzmann 汇总，但禁用 Gconf 集合修正。

## 6. 软件原生执行层

当论文需要预定义 Action 尚未暴露的 GoodVibes 功能时，智能体可通过 `execute_native_software` 调用 `software_id=goodvibes`, `executable=goodvibes`，并自行编排完整参数。常用形式：

```text
goodvibes output.log --temp 298.15 --conc 1.0 --qs grimme --qh \
  --fs 100 --fh 100 -v 0.99 --zpe-vscal 0.98 --json result.json
```

```text
goodvibes conf_*.log --temp 298.15 --boltz gibbs --dedup \
  --e_cutoff 0.05 --ro_cutoff 0.01 --rmsd_cutoff 0.125 --json ensemble.json
```

```text
goodvibes *.log --temp 298.15 --selectivity labels.yaml --boltz gibbs \
  --json selectivity.json
```

```text
goodvibes *.log --temp 298.15 --pes profile.yaml --pes-plot profile.png \
  --json profile.json
```

原生层还可使用 `--csv`、`--parquet`、`--xyz`、`--strip-plot`、`--pes-plot`、`--cpu`、`--media`、`--import/--export` 等能力。参数含义和调用顺序由智能体负责；执行层只做文件隔离、命令白名单、资源限制和溯源记录。

## 7. 输出与溯源

预定义 adapter 读取 GoodVibes 4.3.0 的结构化 JSON，并保留：

- `schema_version` 与 `goodvibes_version`；
- 每个文件的程序、版本、电荷、多重度、溶剂、结构、频率和原始热化学字段；
- 智能体选择的 H/S 模型对应的 `selected_thermochemistry`；
- Boltzmann、选择性或 PES 专用结构化区块；
- 精确命令、stdout/stderr、GoodVibes `.dat` 和 JSON 文件。

GoodVibes 4.3.0 的 JSON 标记为 schema `1.0`，但上游仍将 v5 之前的结构描述为 preview；下游比较器应按版本读取，而不应假定未来版本字段永远不变。

## 8. 已验证范围

本次实际验证包括：Gaussian 16 输出、ORCA 6 输出、三点温度扫描、两成员构象集合、四成员二分类选择性、输入一致性/重复结构检查和 YAML 反应自由能剖面。所有六个 Actions 均成功返回 GoodVibes 4.3.0 结构化结果。

官方资料：

- https://github.com/patonlab/GoodVibes
- https://pypi.org/project/goodvibes/4.3.0/
- https://goodvibespy.readthedocs.io/en/latest/
- https://doi.org/10.12688/f1000research.22758.1
