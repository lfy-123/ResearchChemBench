# Scientific objective

Matched-coordinate origin of H2 activation barriers. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Public inputs and scientific boundaries

Compare complete source silylenes 1, V-prime and carbonyl analogue 4 with H2. All isolated reactants and the closed-shell activation surface are neutral singlets. Main Scheme2 p2 defines 4 as the six-membered lactam analogue of 1: replace the C(Me)2 adjacent to N with C=O while retaining N-phenyl and both SiMe3 groups. Species_registry.json gives the graph; no TS is supplied. Use benzene, 298 K, 1 atm for source-comparable G, and separated silylene+H2 as the common zero for each system. Do not subtract unlike full-system total energies across different formulas.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

Construct and validate each reactant, representative approach conformers, H–H activation saddle and both endpoints.

At the same H–H distances 0.80, 1.00, 1.20 and 1.40 Å, compare frozen-fragment electronic strain and interaction using fragments silylene/H2 with the same singlet states. Report a point as a constrained diagnostic, never a thermal minimum.

Close strain+interaction against total interaction-from-relaxed-reactants energy and test a decisive functional/conformer control. Determine whether barrier differences arise from deformation, interaction or an inseparable mixture.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: Acetylene, ammonia-borane and full CO2 catalytic networks are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `activation_paths`: Three actual H2 activation pathways with shared separated-reactant conventions.
- `matched_coordinate_decomposition`: Matched H–H coordinate strain and interaction terms with closure residuals.
- `causal_comparison`: Compare signed barriers and decomposition trends; isolated Si descriptors cannot establish causation.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
