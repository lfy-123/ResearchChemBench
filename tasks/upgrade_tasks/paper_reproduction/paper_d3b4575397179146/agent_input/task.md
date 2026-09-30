# Scientific objective

SET versus oxygen sensitization necessary conditions for N-methyl oxidation. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Author-provided scientific guidance

Authors used B3LYP/6-311+G(d,p) geometries and TD-PBE0/6-311+G(d,p), IEFPCM MeCN, 18 singlet roots (SI p19) and interpret weak visible bands through substituent-dependent orbitals. Main Fig4 gives 1a, O2/MeCN/0°C and456nm conditions. The new substrate/O2 redox and triplet cycles were not established by the four vertical-state calculations; they test necessary conditions only.

# Public inputs and scientific boundaries

Use all four mapped heptazines and source substrate1a: N-methyl-N-(4-trifluoromethylphenyl)pivalamide. Pilot dFHeptZ/dOMeHeptZ first, then expand the same endpoint contract to dClHeptZ/dMeHeptZ. Use MeCN, 273.15 K, substrate0.1M, O2 1atm, 456nm source conditions; solute free energies use1M. Include substrate radical cation (charge+1,doublet), catalyst radical anion (−1,doublet), O2 triplet ground state, singlet oxygen and superoxide (−1,doublet). SET compares S+PC*→S+radical+PC−radical. EnT compares catalyst triplet deactivation with triplet-O2→singlet-O2; E00 and triplet gaps are not vertical S1 energies. A shared SCE reference may be used, but direct reaction G avoids arbitrary absolute-electrode shifts.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

Validate neutral/redox states and track physical excitations by NTO or equivalent character, including root-window expansion when needed. Separate E00, vertical excitation and relaxed triplet gap.

Compute balanced SET thermodynamics and oxygen sensitization thresholds for all four catalysts, including regeneration feasibility with oxygen; retain explicit charge/spin and reference conventions.

Use available oxygen/quenching constraints and actual method/state sensitivity to judge necessary conditions. If both routes are thermodynamically possible, state that thermochemistry alone cannot select the mechanism or predict yield.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: Full oxidation kinetics and all substrates are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `photoredox_matrix`: Four catalysts on a common SET/EnT and redox/state reference.
- `oxygen_states`: Correct oxygen state energetics and spin identity.
- `mechanism_discrimination`: Fair possibility of both routes being feasible; no exact oxidation-yield prediction.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
