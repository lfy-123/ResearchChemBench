# V2 design audit

去掉33/55键编辑提示和±120度强制干预；明确原文3a的实质依据在正文Figure5与SI第2页，而SI第5页溶剂分析属于其他体系。保留真实图、态和公共基准要求，未知路径与构象留给agent。

[
  {
    "file": "3a.xyz",
    "action": "private_snapshot_only; retain mapped graph",
    "reason": "Remove inherited reactive conformation as a starting-route cue."
  },
  {
    "file": "species_registry.json",
    "action": "remove bond_edits and geometric_control; preserve3a graph/stereochemistry",
    "reason": "The bond edits and ±120 degree torsions disclose the proposed routes and intervention."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "Remove forced [3,3]/[5,5], multi-start count and opposite-torsion control matrix."
  }
]

Agent decisions:
- Generate relevant rearrangements and conformers from the supplied graph.
- Choose electronic-state and pathway methods sufficient for the proposed interpretation.
- Design tests that assess the role of molecular organization and distinguish model artifacts.
- Determine what static evidence can establish and whether additional dynamic claims are warranted.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
