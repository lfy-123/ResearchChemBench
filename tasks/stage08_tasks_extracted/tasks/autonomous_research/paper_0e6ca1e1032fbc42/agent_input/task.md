# Scientific objective

Determine, using independent periodic calculations, how noble-metal identity and CoO film thickness affect CO + surface lattice oxygen → CO2 + oxygen-vacancy energetics, activation barriers and oxide–metal charge transfer, and formulate and discriminate plausible physical explanations for the observed trends.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`, `data/inputs/co.xyz`, and `data/inputs/co2.xyz`. The allowed systems are stoichiometric epitaxial CoO on fcc(111) Pt, Pd, Au and Ag in the specified 2×2, six-layer, 3.15 Å model. Select a surface-O site using a reproducible structural criterion and identify it unambiguously in every submitted structure; no result-bearing site or geometry is supplied. Charge transfer means the Bader sum for the outermost CoO layer relative to the metal slab, with sign convention explicitly reported. The reaction endpoint is CO2 plus a vacancy at the selected site.

# Required scientific validation/investigation

Propose at least two physically distinct hypotheses before selecting a primary explanation (for example, electronic charge transfer versus coordination/strain), and design calculations that discriminate them. Generate and deduplicate candidate adsorbate geometries, magnetic states or pathways as scientifically justified; retain identities and per-candidate validation context. Relax and convergence-check primary endpoints, validate transition-state connectivity if a barrier is reported, and quantify sensitivity or uncertainty. A completed case must report converged endpoints, reaction energy and charge transfer, and either a validated barrier or an explicit no-validated-barrier record. A bounded-failure case must contain a truthful attempted-case record, failed stage and evidence, with unavailable observables null. Completion requires all declared primary support/thickness cases to satisfy one of these branches, plus an evidence-backed hypothesis conclusion. Stop at that point or when resources prevent further cases, reporting coverage and limitations.

# Deliverables

Write `report/results.json` following the schema. Include proposed hypotheses, candidate inventory, model settings, per-case observables, validation evidence, coverage, selected explanation, alternative explanations considered and limitations. Bounded failure is valid only with truthful attempted-case records and evidence.
