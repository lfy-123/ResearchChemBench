# V2 design audit

本篇必须实质修复源模型错配：1h的回原料叙述不能移给1a。新题研究1a网格能识别什么，不再要求错误五池网络全算。保留原阻塞的历史证据，明确新参考未完成；数据分析问题本身输入完整。

[
  {
    "file": "kinetic_observations.json",
    "action": "retain exact25 rows, remove mandatory holdout instruction",
    "reason": "Preserve source categories and S2_23/S2_24 trace corrections; no prescribed fitting split."
  },
  {
    "file": "species_registry.json/species.json",
    "action": "replace with source precursor/products/solvent identities",
    "reason": "Remove carbanion/thiolate seeds and fixed electrochemical-fragment/reference setup from public design."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "No fixed five-pool network, back_quench parameter, four rate constants or three heldouts."
  }
]

Agent decisions:
- Choose an empirical or kinetic model and explain what its parameters mean relative to post-quench GC observations.
- Determine data treatment, censor/missingness handling and scientifically meaningful validation.
- Test which rates or combinations can be inferred and revise the model if evidence does not identify them.
- Choose stopping and report a bounded inference without inventing new independent observations.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
