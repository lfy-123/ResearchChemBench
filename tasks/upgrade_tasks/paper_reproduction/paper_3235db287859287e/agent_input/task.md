# Scientific objective

Local oxygen-transfer pathways constrained by isotope observations. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Author-provided scientific guidance

The authors propose thiyl-radical addition, iodine capture, an iodide-assisted H relay and cyclic S–O reorganization, with substrate hydroxyl oxygen entering the sulfoxide. Main pp5–7 and SI p100 support this proposal; SI uses Gaussian09, SMD MeCN, 298 K/1 atm, 6-31G(C,H), 6-311G**(O,S), aug-cc-pVDZ-PP(I). The functional is not specified in the extracted SI paragraph, so do not invent one. This benchmark adds independent competing routes and reservoir-balanced barriers; the original E/Z thermochemistry did not establish kinetic selectivity.

# Public inputs and scientific boundaries

Use methyl 2-(hydroxy(phenyl)methyl)acrylate 1a and benzenethiol 2a, not benzylthiol. The local reaction uses MeCN, 298.15 K and a declared 1 M solution convention. Experimental context is 1 mmol of each substrate, 5 mL 0.1 M KI, Pt electrodes, 10 mA, room temperature, N2 (main PDF p7). Compare a finite radical/ionic and substrate-O/water-O candidate space. Reservoir species are I−/I radical, H2O, H+/electron with explicitly matched electron/proton chemical potentials; the electrochemical cell is not modeled. The unlabelled product constitution is a comparison endpoint, not an energetic winner. Isotope observations are public constraints, not blind predictions.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

Generate atom-balanced local O-transfer candidates starting from the supplied graphs; track substrate hydroxyl oxygen separately from water oxygen. Compare the most competitive substrate-O radical route with an ionic or external-water-O alternative. Do not prescribe an author intermediate as the only starting route.

Validate decisive paths using relevant modes and bidirectional connections on the same electronic surface. Correct unequal reservoir composition before comparing effective barriers. A monotonic electronic scan is neither a TS nor proof of zero free-energy cost.

Compare both labelled-oxygen experiments and one OH-protection control; evaluate how each calculation supports, contradicts or leaves open the explanations. E/Z endpoint stability alone is insufficient.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: Full electrode processes, all substrates and the full reaction network are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `paths`: Two chemically different, connected local oxygen-transfer routes with common reservoir bookkeeping.
- `oxygen_tests`: Atom-source predictions and computed protection perturbation, bound to actual paths.
- `path_comparison`: Compare reference-corrected barriers, not merely E/Z product G.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
