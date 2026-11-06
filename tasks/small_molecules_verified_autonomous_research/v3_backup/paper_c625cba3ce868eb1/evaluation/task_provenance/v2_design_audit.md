# V2 design audit

保留(R)-4完整图、NBS和源实验观测，移走作者优化构象与固定脸/闭环/质子转移矩阵。源4/7的结构差异与两类溶剂不能被省略为“单变量证实”。保留六/七环拓扑纠错但不预给反应路径。

[
  {
    "file": "compound_4_R.xyz and compound_7.xyz",
    "action": "private_snapshot_only; retain explicit graph/stereochemical identities",
    "reason": "The SI coordinates are author optimized minima, not neutral experimental input."
  },
  {
    "file": "species_registry.json",
    "action": "retain identities without named closure bonds or forced intermediates",
    "reason": "Keep correct O/H identities and atom maps; let agent generate mechanistic objects."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "Remove prescribed faces, six/seven closure matrix and fixed NBS/Et3N cluster/proton-transfer sequence."
  }
]

Agent decisions:
- Choose the chemically relevant brominating and protonation states and molecular environment.
- Determine which pathway, structural or electronic evidence can explain selectivity without supplied candidates.
- Design comparisons that separate the claimed explanation from important confounding.
- Assess whether the DCM chemical model supports the experimental inference and state where it does not.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
