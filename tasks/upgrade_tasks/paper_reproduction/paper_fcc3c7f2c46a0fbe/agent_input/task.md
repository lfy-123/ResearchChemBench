# Scientific objective

Site-correct HAT, SET/PT and SPLET competition in four antioxidants. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Author-provided scientific guidance

The authors used B3LYP/6-311+G(d,p) geometries/descriptors and linked acidic 4c/4i to HAT; discussion of methoxy derivatives invoked SPLET and phenoxide (main pp8–9). That phenoxide explanation must be tested against actual connectivity, not adopted. The new cycles and HAT controls were not computed in the source. The assay medium is ethanol (main p4), not the NMR solvent DMSO or a presumed methanol assay.

# Public inputs and scientific boundaries

Use E-configured 4b, 4c, 4h and 4i with the graphs in species_registry.json. 4c/4i contain a carboxylic OH; 4h/4i contain OMe, not phenolic OH. Retain actual C–H donors for 4b/4h and compare the carboxylic O–H and N-linked methylene/methyl sites where present. The DPPH assay is ethanol, room temperature, 30 min, 517 nm; use 298.15 K/1 M for the declared model. SI TableS5 gives IC50 for 4b/c/h/i of 692.52/11.89/26.63/26.15 µM; these are public interpretation constraints, not exact computed-activity targets. 4e is insoluble, not inactive. Use the same solvated proton/electron or explicit acceptor convention throughout thermochemical cycles.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

Enumerate actual hydrogen sites using explicit atom IDs and generate AH, A radical, A− and AH+ radical states with correct charge/multiplicity. Do not construct phenoxide by deleting a methyl group.

Compute balanced HAT, SET→PT and PT→ET cycles in ethanol for all four molecules; report both E and G. Use explicit DPPH/DPPH-H for a decisive local HAT comparison of an acid and a nonacid (4c and 4h), or a rigorously equivalent matched acceptor control.

Compare thermodynamic feasibility with actual local path evidence and test solvation/conformer sensitivity. A low HOMO–LUMO gap does not prove the mechanism or exact IC50.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: Exact IC50 prediction and biological oxidation networks are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `thermochemical_cycles`: Real donor sites and charge-balanced cycle closure, not descriptor correlation.
- `decisive_local_paths`: Matched explicit-acceptor HAT paths spanning acidic and nonacidic structures.
- `activity_boundary`: Mechanistic discrimination with correct experimental endpoint limits.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
