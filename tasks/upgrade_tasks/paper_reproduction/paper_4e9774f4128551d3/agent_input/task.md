# Scientific objective

Facial protonation of one silyl-enol precursor. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Author-provided scientific guidance

Main p6 proposes soft enolization then CSA protonolysis, giving a nearly balanced cis/trans mixture and permitting recycling; this is not equilibrium control. Source calculations only compare 50/S20 using B3LYP-D3/6-31G(d,p), larger-basis SP and PCM methanol (SI p71). The new face-specific proton-transfer paths are benchmark extensions, not source-validated TSs. Disclose the main/SI THF:MeOH discrepancy rather than selecting the convenient condition.

# Public inputs and scientific boundaries

The precursor is the tetrasubstituted O-TMS enol ether made from 50: transform C6–C47 to double, C47=O52 to single, replace H7 on C6 by an O52–SiMe3 group; retain all other mapped stereocentres. It is neutral singlet C23H38O3Si. Reprotonate C6 from the two faces using racemic camphorsulfonic acid (CSA), not a bare proton. Model both acid enantiomers in an achiral medium or demonstrate the appropriate symmetry equivalence. Stage 1: HMDS/TMSI in DCM at 23°C. Stage 2: CSA in THF/MeOH at 23°C; SI pp20–21 specifies 6/0.60 mL (10:1), whereas main Scheme5 says 1:1. Use a THF continuum plus one explicit MeOH in every cluster for the primary local model and a MeOH-continuum matched sensitivity; neither is an exact mixed-solvent model. Use 296.15 K and 1 M. Keep CSA− and the protonated silyl ether in the same neutral cluster; downstream desilylation is outside the required path segment.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

Construct the mapped silyl enol ether and racemic acid contact conformers. The two faces create alternative configurations at C6, with the other stereocentres fixed.

Locate both facial proton-transfer saddles for each distinguishable acid enantiomer, inspect O–H/C–H motion and follow both endpoints. Compare local barriers and the common separated enol+acid+MeOH reference, including precursor approach cost.

Combine racemic-acid contributions only using explicit weighting assumptions; quantify the effect of solvation and precursor conformation. Product cis/trans G is a thermodynamic control, not a kinetic answer.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: Full silylation/desilylation networks and every substrate are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `facial_paths`: Two faces under racemic CSA with symmetry-supported equivalence allowed through explicit records.
- `facial_comparison`: Same-reference facial barrier differences and preorganization.
- `racemate_control`: Racemate and solvent-composition sensitivity, without equating endpoint stability and protonation selectivity.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
