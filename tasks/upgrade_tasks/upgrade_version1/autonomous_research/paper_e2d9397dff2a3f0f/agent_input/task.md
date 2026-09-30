# Scientific objective

Ru ligand intervention in local N–O cleavage versus ammonia attack. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Public inputs and scientific boundaries

The supplied 48-atom Ru-bda-Py starter has charge +1 and singlet multiplicity. Ru is map1, nitrido-derived N10, contacting carboxyl O5, carboxyl C28; the contact under test is N10–O5. There are two pyridines, not one. Freeze a bcs intervention by replacing the dangling C28 carboxylate with sulfonate S28, adding O49 and preserving the pyridyl C27 attachment; the coordinating carboxylate remains intact. Retain overall dianionic bda/bcs ligand convention, two neutral pyridines, nitrido inventory and total cation charge. This graph replacement does not prescribe a stable N–O bonded bcs minimum. Compare N–O opening then NH3 attack against direct NH3 attack on each ligand. Use MeCN 298.15 K, 1 M and the same NH3 reservoir. A 0.5 V vs Fc/pH15.1 source thermodynamic convention applies only when an electron/proton changes; it is not an electron-transfer activation barrier.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

First establish the bda N–O coordinate, actual saddle mode and bidirectional endpoints. A transverse imaginary mode is not cleavage evidence.

Build the single bda→bcs intervention independently. Compare direct ammonia attack and opening-assisted attack with identical total NH3 and proton inventory; report a spontaneous opening or collapse with a mapped path, not an invented saddle.

Separate electronic barriers, Gibbs barriers and oxidation reaction G. Test decisive conformer/method dependence before attributing a local effect to the ligand or extrapolating to the complete oxidation cycle.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: All three ligands and the full ammonia activation/PCET/N–N/NO network are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `local_paths`: For each ligand validate opening, subsequent NH3 attack and the competing direct attack. A lost N–O basin may be documented by a complete collapse profile; never invent a bound bcs minimum.
- `ligand_effect`: Compare direct attack with the complete opening-plus-attack sequence ending in the same N–N-connected composition on each ligand. Include every segment and preparation cost; an opening barrier alone is not comparable to the full NH3 attack. Compare only within-ligand barrier differences across ligand formulas.
- `mode_identity`: Actual cleavage displacement versus transverse modes; source oxidation G is not a chemical barrier.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
