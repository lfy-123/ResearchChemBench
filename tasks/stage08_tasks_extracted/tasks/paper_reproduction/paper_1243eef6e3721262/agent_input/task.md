# Scientific objective

Determine whether the deposited HIAM-234b two-net framework or its one-net counterpart has lower solvent-free periodic electronic energy per net. Independently select and justify calculations, validate both endpoints, and conclude what the energy comparison does and does not establish.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that interpenetration can stabilize the pillar-layered HIAM-234b framework, with the experimentally observed two-net (2IP) structure energetically favored over a hypothetical one-net (NIP) counterpart.

**Candidate route or mechanism.**
The relevant comparison is between the deposited two-net Co6-bub-bpy tfz framework and a one-net model formed by retaining one complete chemically identical net in the same crystallographic cell. The claim concerns an intrinsic solvent-free framework-energy difference, rather than crystallization probability.

**Discriminating evidence.**
Use comparable fixed-cell periodic electronic-structure calculations on both endpoint models, optimize atomic coordinates, verify net identity and mapping, and compare total energies after normalization by net count. Structural validation and convergence or sensitivity evidence distinguish a meaningful energetic trend from a model-construction or numerical artifact.

# Public inputs and scientific boundaries

Use CCDC record 2478962 as the uniquely identified HIAM-234b starting structure, a Co6-bub-bpy tfz framework. Construct the comparison model by retaining exactly one of the two chemically identical, translationally interwoven complete nets, preserving the deposited cell and recording atom mapping. Use solvent-free periodic models, fixed cell, and energy per net in kcal mol−1. The paper, SI and general web are unavailable during evaluation.

# Required scientific validation/investigation

Independently choose a defensible electronic-structure approach and calculate both model endpoints. Verify connectivity, charge/spin treatment, net counts, cell identity and atom mapping before calculation. Optimize atomic coordinates at fixed cell or justify another endpoint protocol, obtain comparable energies, normalize by net count, and report convergence and sensitivity evidence. Completion requires converged endpoints and a reproducible difference, or a bounded failure with attempted settings and last state. Stop when that condition is met or when a documented set of alternatives cannot resolve convergence or identity; report search coverage and limitations.

# Deliverables

Write `report/results.json` containing model identities/mapping, independent method choice, convergence, raw and normalized energies, energy difference, direction, conclusion and limitations. If computation fails, use the schema's bounded-failure branch with truthful diagnostics. Do not claim a mechanistic route beyond what this energy comparison supports.
