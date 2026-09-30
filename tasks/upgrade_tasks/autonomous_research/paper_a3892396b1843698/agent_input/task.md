# Scientific objective

Connected sigmatropic paths and a controlled preorganization intervention. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Public inputs and scientific boundaries

Use full C11H14 3a singlet gas-phase298.15K/1atm. Source mapped reactive sequences are cyclopropyl bond1–2, left butadienyl1–8–10–14–16 and right2–11–13–18–20. [3,3] forms10–13; [5,5] forms16–20 while breaking1–2 and shifting corresponding pi bonds. Compare the original relaxed precursor with an explicitly geometric opposite-sign torsional control: constrain torsions10–8–1–2 and13–11–2–1 to the alternative opposite-sign ±120° values, report the relaxed precursor-to-constrained preparation cost, then search/follow both rearrangement channels. This is a geometric intervention on the same composition, not a claimed synthesized bridged derivative. Release all constraints before classifying true TS/minima; constrained profiles are diagnostics only.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

Use more than one independent initial approach for both rearrangements, validate reaction-coordinate modes and both endpoints, preserving atom/bond mapping.

Perform both paths from the geometric preorganization control, including preparation energy and release/collapse evidence. If relaxation returns to the original family, document that collapse and do not invent a separate minimum or free-energy barrier.

Report electronic and Gibbs barriers separately and compare the total common-reference cost. Negative electronic differences are not negative activation G. Static evidence alone cannot establish a trajectory branching ratio.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: Large trajectory ensembles and every bridged derivative are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `rearrangement_paths`: Both original and matched geometric-control paths, allowing evidenced collapse of the control.
- `preorganization`: Quantify geometric preparation, distinguish constraints from free stationary points.
- `channel_response`: Intervention response with electronic/Gibbs separation and genuine endpoint evidence.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
