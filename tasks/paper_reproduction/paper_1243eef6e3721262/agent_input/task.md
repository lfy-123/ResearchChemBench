# Scientific objective

Test the authors' qualitative hypothesis that interpenetration can stabilize an expanded pillar-layered MOF: independently calculate and compare the normalized solvent-free periodic electronic energies of the deposited HIAM-234b two-net structure and its one-net counterpart. Report whether the observed 2IP model is energetically favored, without assuming the answer.

# Public inputs and scientific boundaries

Use the supplied immutable HIAM-234b crystal input `data/inputs/ccdc_2478962.cif` directly; CCDC 2478962 is provenance only and CCDC database retrieval is not required or scored. Verify its archive ID, composition, occupancy/disorder, symmetry and cell as the deposited Co6-bub-bpy tfz framework. Construct the NIP comparator by retaining exactly one of the two chemically identical, translationally interwoven complete nets, preserving the deposited cell and recording atom mapping. Use solvent-free periodic models, fixed cell, and energy per net in kcal mol−1. The paper, SI and general web are unavailable during evaluation.

# Required scientific validation/investigation

Plan and execute an independent calculation for both models. Verify connectivity, charge/spin treatment, net counts, cell identity and atom mapping before calculation. Optimize atomic coordinates at fixed cell, obtain comparable total energies, normalize each by its net count, and report convergence evidence. A calculation is complete when both models have converged endpoints and a reproducible energy difference, or when a bounded failure records the attempted settings, last state and reason. Stop after both endpoints are converged, or after a documented set of alternative settings fails or gives unresolved model identity; report coverage and limitations.

# Deliverables

Write `report/results.json` containing model identities/mapping, methods, convergence, raw and normalized energies, energy difference, direction, conclusion and limitations. Every claim must be traceable to logged calculations or the public CCDC record. If computation fails, use the schema's bounded-failure branch with truthful diagnostics.
