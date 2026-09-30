# V2 design audit

源文对近1:1质子解和稳定性作不同层级论证；保留实验近均衡结果而非把2.32kcal/mol公开成答案。公开构建图不保留构象/面选择矩阵。

[
  {
    "file": "species_registry.json",
    "action": "retain source identities in systems.json",
    "reason": "Preserve source50 stereochemistry, source-enol connectivity, CSA racemate and methanol; remove a prescribed acid weighting procedure."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "CSA_A/B × face_a/b, one-MeOH and two continuum calculations are old design choices, not obligatory research."
  },
  {
    "file": "public_sources.json",
    "action": "neutral factual source locators",
    "reason": "Keep solvent discrepancy and measured ratio; author product energies stay PR/private."
  }
]

Agent decisions:
- Determine what the reported diastereoselectivity actually constrains and what cannot be inferred from it.
- Select local species, conformational representation, treatment of the racemate and solvent, and a defensible method.
- Design evidence that distinguishes an explanation from an accidental endpoint-energy agreement.
- Decide whether the unresolved solvent ratio or model sensitivity limits the conclusion.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
