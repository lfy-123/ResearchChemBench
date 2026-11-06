# V2 design audit

比较对象保持论文模型而非实验全配体。删除固定扫描与能量分解，仅给H2反应问题和完整连接；未将作者计算排序公开成已观测差异。

[
  {
    "file": "silylene_1_singlet.xyz/silylene_Vprime_singlet.xyz",
    "action": "replace coordinate seeds by full neutral connectivity",
    "reason": "Keep complete source-model identity; avoid inherited optimized states or geometry hints."
  },
  {
    "file": "species_registry.json",
    "action": "source molecule graphs only",
    "reason": "Remove matched-HH scan and fragmentation recipes; do not turn source truncation into experimental full molecule."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "No fixed strain/interaction decomposition or HH0.8/1.0/1.2/1.4Å mandatory points."
  }
]

Agent decisions:
- Choose a defensible representation and state treatment for the three source models.
- Determine how to establish whether H2 activation differs and what would explain any difference.
- Select useful reaction, electronic or comparative evidence without a mandatory decomposition scheme.
- Bound conformational, state and thermochemical uncertainty and decide when differences are unresolved.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
