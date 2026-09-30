# Scientific objective

Copper-mediated and direct chlorine-transfer exits of one allyl radical. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Author-provided scientific guidance

The authors propose reduction to CuI, sulfonyl-radical generation, allyl capture by CuII and CuIII reductive elimination; they explain Z preference using Cu-organized allylic geometry. Original B3LYP-D3BJ/LANL2DZ(Cu)/6-31G(d,p) geometries and M06/SDD(Cu)/6-311+G(d,p), SMD MeCN SPs only establish a local intermediate comparison. New exit barriers, radical Cl transfer and spin checks are benchmark additions.

# Public inputs and scientific boundaries

Freeze allenoate 6b (ethyl 4-phenyl-2-propylbuta-2,3-dienoate), PhSO2Cl and an acac-supported copper local model. Compare C–Cl formation from the CuIII allyl(acac)Cl singlet against chlorine-atom transfer to the matching allyl radical from PhSO2Cl. Include CuII(acac)Cl doublet and CuI(acac) singlet reservoirs as required by the ledger; do not compare isolated Cu-bound and metal-free total energies. Main pp6–8 and SI pp56–65 define the source system. Use MeCN, 313.15 K (experimental 40°C), 1 M; reproduce the former 298.15 K endpoint only as a separately labelled baseline. Full photoredox catalyst and regeneration network are outside this local exit comparison.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

Build the allene-derived allyl graph, enumerate both stereochemical approaches and relevant open-shell alternatives, and document Cu oxidation-state/electron bookkeeping. Use the acac ligand, not a bare CuCl shortcut.

Locate connected C–Cl-forming exits for the Cu path and the direct transfer alternative, with doublet/singlet surfaces and reactant reservoir energies explicitly distinguished.

Compare effective barriers and lower alternative conformers, including Cu association free energy and stereochemical mapping. Intermediate stability or C–C–C distortion alone cannot determine exit selectivity.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: The full photoredox/copper cycle and all substrates are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `exit_paths`: Cu-organized and free-radical chlorine exits with real endpoint validation.
- `reservoir_ledger`: Charge/spin/chemical-potential ledger connecting different molecularities.
- `stereochemical_control`: Competing stereochemical exits, conformation and spin sensitivity.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
