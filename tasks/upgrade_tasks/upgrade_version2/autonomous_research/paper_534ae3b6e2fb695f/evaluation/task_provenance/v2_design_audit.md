# V2 design audit

原首酰化/Cl质子受体/应变矩阵不是作者已有证据。V2限定三种原单体与TMC的分子反应性解释，保留完整连接，开放环境、反应模型和判别方法；严格区分分子描述符、基元动力学与膜尺度。真实SI与审稿文件明确分开。

[
  {
    "file": "monomers.json",
    "action": "retain identity graphs/maps/formulas as systems.json",
    "reason": "Remove mandatory first-acylation roles and prescribed torsion indices while preserving all four source monomers."
  },
  {
    "file": "research_matrix.json and species_registry.json",
    "action": "private_snapshot_only",
    "reason": "Remove forced gas-phase first acylation, chloride-assisted proton transfer, strain decomposition and fixed per-monomer TS searches."
  }
]

Agent decisions:
- Define what intrinsic reactivity means for a stated local chemical environment.
- Select quantities, conformations and chemical states that can discriminate the monomer comparison.
- Decide whether molecular descriptors, explicit reaction modeling or another valid analysis can support the claimed interpretation.
- Test relevant uncertainty and determine which film-scale conclusions remain unsupported.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
