# V2 design audit

将原强制CuIII/自由基两出口矩阵改为源观测驱动的局部C–Cl问题。公开金属前体身份不固定活性态；SI表头G273.15与实验40°C均如实保存。

[
  {
    "file": "species_registry.json",
    "action": "retain reactant graphs; remove intermediate seeds",
    "reason": "CuIII_allyl/acac/Cl and allyl/sulfonyl radical structures are candidate models, not fixed starting facts."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "Remove CuIII exit vs direct radical chlorine-transfer named branches and mandatory spin/temperature matrix."
  },
  {
    "file": "public_sources.json",
    "action": "neutral observations and scope",
    "reason": "Keep observed selectivity and source conditions; do not publish source optimized intermediates or their energies."
  }
]

Agent decisions:
- Choose chemically defensible local copper/reagent models and states.
- Determine which molecular explanations can connect selectivity to measured controls.
- Choose appropriate evidence and search strategies without prescribed intermediates.
- Assess whether intermediate energies, barriers or other observables support the claimed degree of mechanism discrimination.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
