# V2 design audit

从固定两进攻位点与单水簇矩阵改为源环氧活化问题。补回实验K2CO3身份，保留真实终点数据但不把它当微观速率；作者仅电荷分析与本批后续机理调查明确区分。

[
  {
    "file": "systems.json",
    "action": "retain two catalyst identities; remove target-atom charge prompts and context TFAP",
    "reason": "Catalyst comparison remains source-specific without prescribing the electronic explanation."
  },
  {
    "file": "species_registry.json",
    "action": "retain reactants/additives without cluster_rule; add source K2CO3 and MeCN identities",
    "reason": "One-water/spectator-CO2 neutral cluster was a benchmark model, not a measured catalytic species."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "Remove mandatory terminal/benzylic paths, position restraints and association/barrier sequence."
  }
]

Agent decisions:
- Choose which molecular quantities can actually test an activation explanation.
- Construct chemically valid ion/solvent/substrate models and select relevant states and conformations.
- Decide the necessary comparisons and sensitivity without a fixed attack site, cluster composition or restraint.
- Determine what the molecular findings can and cannot explain about the endpoint experiment.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
