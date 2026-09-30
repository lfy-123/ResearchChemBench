# V2 design audit

保留同位素结果是已公开的实验证据，不把它们当待预测的赢家；问题改为这些观测与独立计算究竟支持何种分子解释。源保护实验可作事实，不强制再计算保护反应。

[
  {
    "file": "data/inputs/3aa_stereoisomers.json",
    "action": "private_snapshot_only",
    "reason": "E/Z candidate labels and a fixed stereoisomer comparison belong to old task; supply neutral observed product constitution instead."
  },
  {
    "file": "data/inputs/species_registry.json",
    "action": "replace_by_systems.json",
    "reason": "Retain experimental molecules and maps, remove preselected thiyl/iodine radical route seeds and construction instructions."
  },
  {
    "file": "data/inputs/research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "Remove substrate_O_candidate/competitive_alternative/OH-control mandatory design."
  },
  {
    "file": "data/inputs/public_sources.json",
    "action": "replace_with_local_source_locators",
    "reason": "Source page and factual provenance remain without copying author pathway or raw paper access."
  }
]

Agent decisions:
- Choose a chemically defensible model and scope of molecular claims for the source rearrangement.
- Propose, revise or reject explanations based on the supplied observations and new evidence, without a required list or number.
- Choose states, molecular representations, methods, searches and comparisons that can discriminate the actual claim.
- Decide when remaining ambiguity is structural/observational rather than an unfinished calculation and justify a stopping decision.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
