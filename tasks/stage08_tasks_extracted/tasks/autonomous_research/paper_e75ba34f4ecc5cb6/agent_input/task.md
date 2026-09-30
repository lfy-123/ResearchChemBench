# Scientific objective

Independently determine how the four explicitly defined ether-solvent records in the public inputs interact electronically with one K+ ion. Quantify the K+-solvent electronic binding energy and dipole moment for each record and use validated calculations to explain any differences among connectivity/conformation records. Formulate and discriminate plausible coordination explanations from your calculations.

# Public inputs and scientific boundaries

Use `data/inputs/solvents.json` as the complete molecular identity definition. Its SMILES define connectivity and atom order; no stereochemistry is specified or scored. Use `data/inputs/system_definition.json`: isolated solvents are neutral singlets, K+ is charge +1/singlet, and each complex is one K+ plus one solvent with overall charge +1/singlet. The target is gas-phase electronic structure; solvent models and thermal corrections are optional but must be declared. A binding energy means E(complex) − E(isolated solvent) − E(K+) using energies from a consistent stated electronic-structure level. Do not consult the paper, SI or general web during the investigation.

# Required scientific validation/investigation

For every named record, generate a finite set of plausible 3-D conformers and K+ placements, document the generation and deduplication rule, and optimize the retained candidates. Propose at least two scientifically plausible coordination explanations where the geometry permits, then discriminate them using validated energies/geometries and report remaining ambiguity. Advance a candidate only when optimization converges and connectivity/charge/multiplicity remain valid; report a bounded failure when this cannot be achieved. The investigation is complete when all four records have either a validated result or bounded failure, all needed component energies are present, and candidate coverage, selection rationale, stopping condition, and limitations are reported. Stop after this four-record scope and the declared candidate-generation space has been exhausted or a reproducible saturation/limitation criterion is met.

# Deliverables

Submit `report/results.json` conforming to the schema. Include exactly four records, in the public-input order DEGDME, DPGDME, DPGMPE-1, DPGMPE-2; each `id` must identify that record. Include per-record identities, candidate/geometry references, energies, binding energy in eV, dipole moment in Debye, validation evidence, independently proposed explanations, discrimination evidence, and a final conclusion. For a bounded failure, set the unavailable numeric fields to null and explain the failure and evidence in the validation object; do not fabricate values. Include a methods/coverage object and distinguish successful records from bounded failures. Conclusions must follow from the submitted investigation.
