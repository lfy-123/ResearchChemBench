# V2 design audit

去除直接泄露待判N–O结构的reference.xyz；改供源配体SMILES、Ru/双Py/单N的完整库存及电荷，旋态和配位让agent判断。保留局部氮化学问题，不升级为全电催化周转预测。

[
  {
    "file": "reference.xyz/species_registry.json reference",
    "action": "private_snapshot_only; replace with constituent identity and inventory",
    "reason": "Source optimized N–O geometry would reveal the feature under study. Supply complete ligand connectivity and local composition without answer coordinates."
  },
  {
    "file": "state_definition.json",
    "action": "replace by source model inventory",
    "reason": "Remove fixed singlet and C28→S28 intervention instructions; keep source-supported bda/bcs identities."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "Remove six prescribed opening/direct-attack channels."
  }
]

Agent decisions:
- Establish the relevant local molecular and electronic states without receiving an optimized mechanistic answer.
- Choose how to investigate ammonia interaction and any role of the ligand environment.
- Select enough evidence to support or falsify a local mechanistic claim, without prescribed opening/attack branches.
- Determine which uncertainties prevent stronger causal or catalytic inference.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
