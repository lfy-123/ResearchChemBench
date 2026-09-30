# V2 design audit

取消预给1-cis构象、邻位配对生成规则与固定路径诊断矩阵，回到真实前体和氧化光环化条件。既不提前给作者终产物结构，也不把S0最低能候选冒充可达性证明；允许有实证边界的候选集合。

[
  {
    "file": "precursor_1_cis.xyz and species_registry.json",
    "action": "replace cis model/coordinates by source precursor constitutional graph and experimental preparation facts",
    "reason": "The source computational1-cis is a proposed reactive geometry, not a measured starting ensemble."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "Remove ortho-pair enumeration rule, fixed candidate layers, prescribed representative scans and vertical-state sampling."
  }
]

Agent decisions:
- Generate chemically plausible transformations and structures from the precursor and source conditions.
- Choose how to establish candidate coverage or other evidence sufficient for the claimed outcome.
- Choose ground/excited-state descriptions and tests that match the asserted accessibility claim.
- Determine whether the available evidence supports a unique product, a restricted set or only partial constraints.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
