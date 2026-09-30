# Scientific objective

Determine whether the deposited HIAM-234b two-net framework or its one-net counterpart has lower solvent-free periodic electronic energy per net. Independently select and justify calculations, validate both endpoints, and conclude what the energy comparison does and does not establish.

# Public inputs and scientific boundaries

Use the supplied immutable HIAM-234b crystal input `data/inputs/ccdc_2478962.cif` directly; CCDC 2478962 is provenance only and CCDC database retrieval is not required or scored. Verify its archive ID, composition, occupancy/disorder, symmetry and cell as the deposited Co6-bub-bpy tfz framework. Construct the comparison model by retaining exactly one of the two chemically identical, translationally interwoven complete nets, preserving the deposited cell and recording atom mapping. Use solvent-free periodic models, fixed cell, and energy per net in kcal mol−1. The paper, SI and general web are unavailable during evaluation.

# Required scientific validation/investigation

Independently choose a defensible electronic-structure approach and calculate both model endpoints. Verify connectivity, charge/spin treatment, net counts, cell identity and atom mapping before calculation. Optimize atomic coordinates at fixed cell or justify another endpoint protocol, obtain comparable energies, normalize by net count, and report convergence and sensitivity evidence. Completion requires converged endpoints and a reproducible difference, or a bounded failure with attempted settings and last state. Stop when that condition is met or when a documented set of alternatives cannot resolve convergence or identity; report search coverage and limitations.

# Deliverables

Write `report/results.json` containing model identities/mapping, independent method choice, convergence, raw and normalized energies, energy difference, direction, conclusion and limitations. If computation fails, use the schema's bounded-failure branch with truthful diagnostics. Do not claim a mechanistic route beyond what this energy comparison supports.
