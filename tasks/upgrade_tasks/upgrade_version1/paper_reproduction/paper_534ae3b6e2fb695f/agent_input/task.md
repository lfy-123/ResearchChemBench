# Scientific objective

Does diamine nucleophilicity predict a matched first acylation barrier?. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Author-provided scientific guidance

Formal publisher SI (117 pages), Note8 pp10–12 describes ORCA5.0.4 B3LYP-D3BJ/def2-SVP geometries and def2-TZVP refinement, with some subsequent all-TZVP wording; keep one primary protocol and disclose this ambiguity. SI pp20–22/Note13 interprets electronic descriptors as ODA>6FODA>PFMB nucleophilicity; these are not acylation TS results. New TMC paths and distortion controls test that explanation. MD/diffusion discussion in SI p32 is separate and not scored here.

# Public inputs and scientific boundaries

Use full ODA, 6FODA, PFMB and TMC mapped graphs. The selected TMC site is acyl C2/Cl3; shift TMC maps by +1000 to avoid molecule-map collisions. For each amine, attack with the lowest-numbered supplied amine N and retain the second NH2 unchanged. Model the same net reaction TMC+diamine→monoamide+HCl, with departing chloride as the proton acceptor and no arbitrary free proton. This first-version local gas-phase model at 298.15 K/1 M is benchmark-authored and does not model the membrane interface. Retain source-comparable isolated gas-phase electronic descriptors on their defined scale as auxiliary tests. No polymer MD or membrane performance is required.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

Compare representative attack conformers for all three real diamines at the same TMC group; include tetrahedral addition, elimination and proton-transfer segments as needed for a balanced endpoint.

Validate the relevant path saddle(s), report the effective maximum relative to common separated reactants, and compare kinetic ordering with global/local descriptors.

At matched N–C distances, decompose electronic deformation and interaction with fixed fragments. Quantify preorganization and test a decisive conformer/method control before claiming intrinsic electronic causation.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: Polyamide fragment dynamics, interfacial diffusion and membrane MD are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `first_acylation`: Real connected first-acylation paths under identical proton/Cl bookkeeping.
- `descriptors_vs_barriers`: Identity-matched descriptor versus barrier comparison; contrary ordering is a valid result.
- `distortion_interaction`: Fixed TMC/diamine fragment comparison at matched N–C distances.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
