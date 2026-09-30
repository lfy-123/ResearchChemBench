# Scientific objective

Propagation versus backbiting in a defined organoboron chain end. Establish the conclusion from the finite comparison matrix and auditable raw evidence.

# Author-provided scientific guidance

The source attributes dilution tolerance to phosphonium/chain-oxygen interactions and Et3B association; original B3LYP-D3BJ/6-31G(d), ADCH (SI pp4–5) compared only free phosphine/PO/PA local models. The added short-chain graphs, propagation/backbite barriers and concentration competition are benchmark extensions. They must not be attributed to already validated author calculations.

# Public inputs and scientific boundaries

Retain the source phosphine and PA/PO zwitterion identities, but do not mistake them for a growing polycarbonate chain. The new finite active chain model is PA-derived acylphosphonium with a two-PO/one-CO2 segment and terminal O−, net-neutral singlet with internal P+/O−. species_registry.json supplies its complete graph and a matched no-PA chain. Include one Et3B bound to the chain O and one free Et3B for incoming PO activation, consistent with the local 1:2 catalyst inventory. Compare CO2 insertion/PO propagation with backbiting to a cyclic carbonate, retaining the shortened chain coproduct. Use THF continuum 353.15K, solutes1M, CO2 fugacity convention explicitly stated; source neat/THF dilution is represented only by a declared concentration control, not a bulk polymer model.

Use `data/inputs/species_registry.json`, `research_matrix.json`, the retained molecular files and `public_sources.json`. Explicit registry definitions supersede old context-only scope notes. Author TS/terminal coordinates, raw reference outputs and historical PASS records are private. Do not read the target paper/SI, evaluator or historical verification archive as agent inputs. The supplied experimental observations are authorized interpretation constraints, never blind held-out predictions. General software documentation may be consulted.

# Required scientific validation/investigation

Audit original free/PO/PA graphs and construct the explicit short-chain extension. Map the terminal alkoxide, carbonate carbon and neighbouring PO carbons for propagation/backbite.

Locate one connected propagation sequence and one backbiting path for PA and no-PA models. For propagation take the effective maximum of CO2 insertion and PO opening, not the lower convenient step.

Propagate standard-state and a tenfold PO concentration decrease into effective competition using computed barriers. Separate concentration terms from barrier uncertainty; no freely fitted polymerization network or molecular-weight prediction.

Preserve raw inputs, successful and failed searches, converged geometries, mode displacements, both path endpoints and analysis code. TS claims require one chemically relevant unstable mode and bidirectional connection or equally explicit mode-following/endpoint evidence; a scan maximum alone is not a TS. Genuine basin collapse or a resolved shallow pathway is allowed with complete observed profiles, mapping and limits. Missing core comparisons cannot be relabelled as uncertainty. Use one meaningful numerical, conformational or method sensitivity with actual changed calculations. Record real engine starts, allocated cores, summed job hours, core-hours and elapsed calendar hours separately.

First-version exclusions: Long polymer chains, molecular-weight distributions and complete kinetic networks are optional.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. Required result panels:

- `chain_paths`: Actual short-chain propagation/backbite with two Et3B reservoirs.
- `chain_end_audit`: Explicit chain connectivity, charge separation and coproduct balance.
- `concentration_test`: A retained concentration control with a transparent uncertainty range.

Include methods, actual calculation records, at least two evidence-tested hypotheses, quantitative sensitivity, resource accounting and an evidence-bound conclusion. All cited files must exist below workspace `outputs/`, `data/` or `code/`. IDs and atom maps must resolve unambiguously. `complete` requires the whole core matrix, while `bounded_failure` preserves genuine attempted work, diagnostics and missing endpoints without inventing quantities. A documented input/capability failure before any engine or analysis job uses `failure_report.stage=pre_engine`, empty `calculation_records`, empty `methods`, zero scientific job counters and real preparation diagnostics; no fictional job log is required. Format acceptance is not scientific acceptance. Supported, refuted and evidence-complete indistinguishable conclusions are equally eligible; an author winner is not required.
