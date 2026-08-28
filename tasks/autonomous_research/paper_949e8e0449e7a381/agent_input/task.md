# Scientific objective

Determine how changing residue 395 from alanine to glycine in MnKstD2 affects the 4-PG/FAD enzyme complex and whether any computed structural change provides a defensible explanation for a change in catalytic competence. Quantify for WT and A395G the C1_sub–N5_FAD distance, C2_sub–OH_Y359 distance, OH_Y532–O3_sub hydrogen-bond occupancy, productive-frame fraction, and a stability observable (backbone RMSD/RMSF). Propose and discriminate plausible structural explanations from the calculations.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. Retrieve only NCBI Protein accession AHG53938 and PubChem CID 643975 through those controlled records; the substrate identity and atom labels are defined there. Build WT and single A395G. Structure generation, protonation, cofactor placement, conformer/pose search, solvent, model chemistry, and sampling are open choices and must be disclosed. The source paper and general web search are unavailable. The reported kinetic direction is an external qualitative validation boundary only.

# Required scientific validation/investigation

Generate a finite, identity-preserving set of starting complexes and deduplicate them by an explicit structural criterion. Advance candidates using stated scientific criteria, then validate the selected state(s) with relaxation, matched WT/A395G sampling, convergence evidence, and sensitivity analysis. Define productive frames and all distance/hydrogen-bond cutoffs explicitly; report distributions, coverage, rejected candidates and limitations. Completion requires converged comparative observables and a discriminated explanation, or a bounded-failure report showing why the evidence cannot discriminate and what test would resolve it. Stop at the declared search/sampling boundary once convergence and sensitivity criteria are met; the investigator chooses candidate count and reports coverage rather than using an imposed universal count.

# Deliverables

Write `report/results.json` following the schema. In a complete result, include candidate identities, deduplication context, advancement or rejection reason, per-candidate validation context and artifact paths, state-level distributions and observables, productive-frame definitions, model disclosure, coverage/stopping record, and a conclusion that distinguishes supported, weakened, and unresolved explanations. If the search or validation cannot discriminate an explanation within the declared boundary, submit the bounded-failure branch with evidence, coverage, limitations, stopping record, and the additional test needed; do not fabricate candidate or state observables.
