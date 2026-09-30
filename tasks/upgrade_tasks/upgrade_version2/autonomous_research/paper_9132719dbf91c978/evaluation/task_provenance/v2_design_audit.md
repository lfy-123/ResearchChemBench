# V2 design audit

原固定η2-H2→游离H2→单DMAc序列释放为研究决定。给出全XantPhos连接和Pd/2H库存，保留源气体实验，避免把气体实验当局部机制验证。

[
  {
    "file": "int_g.xyz",
    "action": "private_snapshot_only; neutral ligand graph/inventory supplied",
    "reason": "Remove inherited optimized endpoint coordinates and retain a reconstructible full-ligand starting-model definition."
  },
  {
    "file": "species_registry.json",
    "action": "retainDMAc/H2; replace metal seed by explicit inventory",
    "reason": "Do not prescribe eta2-H2, separated gas and one-DMAc endpoints."
  },
  {
    "file": "research_matrix.json",
    "action": "private_snapshot_only",
    "reason": "Remove fixed formation/release/regeneration order and forced solvent-capture conformer matrix."
  }
]

Agent decisions:
- Choose conformers, electronic states and solvent representation within the local inventory.
- Determine the evidence needed to establishH2 formation, escape and the nature of the recoveredPd species.
- Select relevant comparisons and references without prescribed endpoints or order.
- Distinguish experimentally observed gas generation from model-specific mechanistic conclusions.

The private rubric was replaced, not hidden. It assesses evidence capability, with no V1 named matrix requirement. Full scientific/judge calibration remains pending.
