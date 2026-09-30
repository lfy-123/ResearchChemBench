# Scientific objective

Determine, using independent periodic calculations, how noble-metal identity and CoO film thickness affect CO + surface lattice oxygen → CO2 + oxygen-vacancy energetics, activation barriers and oxide–metal charge transfer, and formulate and discriminate plausible physical explanations for the observed trends.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that electron transfer from the outermost CoO layer to the noble-metal support polarizes surface Co–O bonds, making lattice-oxygen removal by CO more favorable. They associate stronger oxide-to-metal transfer with greater reactivity, with the effect expected to be more pronounced for a one-layer film than for a two-layer film.

**Candidate route or mechanism.**
Examine CO reaction with a surface lattice oxygen to form CO2 while leaving an oxygen vacancy, and compare one- and two-layer CoO films across Pt, Pd, Au and Ag supports. Treat interfacial charge transfer and Co–O polarization as a candidate explanation, while testing whether coordination or strain provides a competing explanation for thickness and support trends.

**Discriminating evidence.**
Use converged reaction energies and validated pathway barriers together with Bader charge transfer for the outermost CoO layer, and compare those observables across support identity and film thickness. Structural descriptors of the selected oxygen site and Co–O geometry, plus sensitivity or uncertainty checks, can help distinguish electronic-transfer effects from coordination or strain effects.


# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`, `data/inputs/co.xyz`, and `data/inputs/co2.xyz`. The allowed systems are stoichiometric epitaxial CoO on fcc(111) Pt, Pd, Au and Ag in the specified 2×2, six-layer, 3.15 Å model. Select a surface-O site using a reproducible structural criterion and identify it unambiguously in every submitted structure; no result-bearing site or geometry is supplied. Charge transfer means the Bader sum for the outermost CoO layer relative to the metal slab, with sign convention explicitly reported. The reaction endpoint is CO2 plus a vacancy at the selected site.

# Required scientific validation/investigation

Propose at least two physically distinct hypotheses before selecting a primary explanation (for example, electronic charge transfer versus coordination/strain), and design calculations that discriminate them. Generate and deduplicate candidate adsorbate geometries, magnetic states or pathways as scientifically justified; retain identities and per-candidate validation context. Relax and convergence-check primary endpoints, validate transition-state connectivity if a barrier is reported, and quantify sensitivity or uncertainty. A completed case must report converged endpoints, reaction energy and charge transfer, and either a validated barrier or an explicit no-validated-barrier record. A bounded-failure case must contain a truthful attempted-case record, failed stage and evidence, with unavailable observables null. Completion requires all declared primary support/thickness cases to satisfy one of these branches, plus an evidence-backed hypothesis conclusion. Stop at that point or when resources prevent further cases, reporting coverage and limitations.

# Deliverables

Write `report/results.json` following the schema. Include proposed hypotheses, candidate inventory, model settings, per-case observables, validation evidence, coverage, selected explanation, alternative explanations considered and limitations. Bounded failure is valid only with truthful attempted-case records and evidence.
