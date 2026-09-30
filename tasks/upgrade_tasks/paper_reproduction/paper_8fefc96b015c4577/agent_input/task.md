# Scientific objective

Tether–solvent competition in radical aryl cyclization. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Author-provided scientific guidance

Main Scheme3c p4 compares benzyl-aryl versus sulfonyl-aryl closure and attributes tether effects to strain/electronics. SI p34 uses B3LYP-D3/def2-TZVPP, SMD DMSO for short and DCE for long. Source local long-chain gap is only about0.52kcal/mol, so a robust reversal is not guaranteed. The full solvent cross and bidirectional connections are new required controls, while full photoredox/additive networks remain outside scope.

# Public inputs and scientific boundaries

Use the short C21H24F2NO4S radical and long C22H26F2NO4S homologue, both charge0/doublet. The sole long-chain edit inserts CH2 between short-map13 (N-benzyl carbon) and aromatic ipso14, retaining the radical at map10 and every other atom. For each chain independently compare DMSO and1,2-DCE at298.15K/1atm and two aryl closures: radical10 to either ortho carbon of the N-alkyl-tethered aryl or arenesulfonyl aryl ring. System-specific separated-reactant and uncyclized-radical zeros must be distinguished. Source experimental protocols also change additives; this solvent cross is a controlled model and does not isolate all experimental causes.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

Generate deduplicated conformers and two aryl-connectivity families for each of the four chain/solvent combinations. Do not reuse author TS coordinates or source atom row numbers from a different ordering.

Validate both paths in each condition by real modes and bidirectional endpoints; compare local and common-zero G including conformer preparation.

Compare chain/solvent double differences and matched-coordinate geometric strain proxies. Probe a decisive method/low-frequency/conformer uncertainty, allowing close competition instead of requiring a significant reversal.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: The full radical network, every additive and exact product ratios are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `crossed_paths`: Full2×2×2 local competition; eight combinations are not eight engine calls.
- `factorial_contrasts`: Double differences of within-system channel G barriers, never unlike absolute total energies.
- `strain_and_robustness`: Actual matched-progress deformation and long-chain sensitivity, with no forced sign.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
