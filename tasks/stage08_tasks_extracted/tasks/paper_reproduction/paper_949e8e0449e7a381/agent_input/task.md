# Scientific objective

Determine how changing residue 395 from alanine to glycine in MnKstD2 affects the 4-PG/FAD enzyme complex and whether any computed structural change provides a defensible explanation for a change in catalytic competence. Quantify for WT and A395G the C1_sub–N5_FAD distance, C2_sub–OH_Y359 distance, OH_Y532–O3_sub hydrogen-bond occupancy, productive-frame fraction, and a stability observable (backbone RMSD/RMSF). Generate and test your own plausible structural explanations from the calculations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that replacing Ala395 with Gly relieves local steric restriction around the substrate, helping stabilize 4-PG in a pre-reaction arrangement near FAD and the catalytic Tyr359/Tyr532 residues. This is a qualitative structure–function hypothesis to test against the computed observables.

**Candidate route or mechanism.**
A candidate explanation is that the smaller side chain permits a substrate pose or conformational population with more favorable alignment toward FAD N5 and Tyr359, while also supporting the Tyr532–substrate interaction network. Compare this proposed local-geometry explanation with alternative structural explanations that remain consistent with the calculations.

**Discriminating evidence.**
Use matched WT/A395G distributions of the two specified distances, the explicitly defined productive-frame fraction, OH_Y532–O3_sub hydrogen-bond occupancy, and backbone RMSD/RMSF or another disclosed stability observable. Relaxation, sampling/convergence checks, and sensitivity analyses should establish whether any apparent geometric or interaction difference is persistent and discriminates the proposed explanation.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. Retrieve only NCBI Protein accession AHG53938 and PubChem CID 643975 through those controlled records; the substrate identity and atom labels are defined there. The scored molecular system is the enzyme–substrate–FAD complex for MnKstD2 in WT and single A395G states. Do not add a host or any other molecular component outside that defined system. Structure generation, protonation, cofactor placement, conformer/pose search, solvent treatment, model chemistry, and sampling are open choices and must be disclosed. The reported kinetic direction is an external qualitative validation boundary only.

# Required scientific validation/investigation

Generate a finite, identity-preserving set of starting complexes and deduplicate them by an explicit structural criterion. Advance candidates using stated scientific criteria, then validate the selected state(s) with relaxation, matched WT/A395G sampling, convergence evidence, and sensitivity analysis. Define productive frames and all distance/hydrogen-bond cutoffs explicitly; report distributions, coverage, rejected candidates and limitations. Completion requires converged comparative observables and a discriminated explanation, or a bounded-failure report showing why the evidence cannot discriminate and what test would resolve it. Stop at the declared search/sampling boundary once convergence and sensitivity criteria are met; the investigator chooses candidate count and reports coverage rather than using an imposed universal count.

# Deliverables

Write `report/results.json` following the local `submission_schema.json`. In a complete result, include candidate identities, deduplication context, advancement or rejection reason, per-candidate validation context and artifact paths, state-level distributions and observables, productive-frame definitions, model disclosure, coverage/stopping record, and a conclusion that distinguishes supported, weakened, and unresolved explanations. If the search or validation cannot discriminate an explanation within the declared boundary, submit the bounded-failure branch with evidence, coverage, limitations, stopping record, and the additional test needed; do not fabricate candidate or state observables.
