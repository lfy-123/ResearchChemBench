# V2 design audit

关键来源纠偏：正文详细SET/EnT、Stern–Volmer和氧捕获机制测试对应9a/24，不能写成1a证据。新题限定四heptazine对1a的局部光化学能力，开放态/机制/比较设计，保留真实1a终点观测与严格态基准约束。

[
  {
    "file": "heptazines.json",
    "action": "retain four catalyst identities in systems.json",
    "reason": "Remove mandatory state-cycle instruction while preserving the studied catalyst family."
  },
  {
    "file": "species_registry.json",
    "action": "retain substrate and oxygen feed; remove state_recipes and imposed excited/redox-state list",
    "reason": "The agent chooses states required by its mechanistic claims."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "Remove forced SET versus EnT, all-catalyst oxygen-state matrix and dF/dOMe pilot order."
  }
]

Agent decisions:
- Choose the molecular or photophysical quantities needed to address initiation in the specified reaction.
- Select and track physically meaningful electronic states, references and environmental assumptions.
- Design relevant comparison across the catalyst family and test whether it supports a mechanistic explanation.
- Distinguish necessary energetic conditions from rates, competing processes and observed product yield.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
