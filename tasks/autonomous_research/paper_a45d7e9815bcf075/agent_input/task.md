# Scientific objective

Determine whether a reproducible local-fragment computational investigation can recover the global AMI/FMI correlation landscape of the specified two-chain human insulin structure, and identify which chemically meaningful correlations and long-range contacts are robust to the chosen locality design. Propose and discriminate plausible locality/overlap explanations from your calculations; do not assume an author route.

# Public inputs and scientific boundaries

Use every field in `data/inputs/system_spec.json` and retrieve exactly PDB 3I40 from RCSB. Preserve chain A/B and residue identities. The measured objects are orbital MI, atom-pair AMI and residue-pair FMI; report matrix indexing, symmetry convention, units (nat for information), diagonal handling and cap-atom exclusion. The quantum system is protein-only after solvent/ion removal. Choose and disclose charge/multiplicity, electronic-structure method, geometry treatment and fragment design. The known insulin connectivity and disulfides define the system, not the answer.

# Required scientific validation/investigation

Before computation, state the hypothesis space for locality reconstruction and generate a finite candidate set of fragment/overlap designs or computational routes. Retain unique candidate identities and per-candidate geometry, coverage and validation context; state deduplication, advancement and stopping rules. For each advanced candidate, compute or obtain defensible AMI/FMI observables, validate atom/residue mapping, symmetry, cap exclusion and coverage, and compare candidates using explicitly reported metrics or qualitative evidence. Test chemically meaningful objects including the three disulfide pairs and Glu17(A)-Arg22(B), while distinguishing a missing pair from an uncomputed pair. Completion requires a machine-readable result, candidate coverage, discrimination rationale and either a completed endpoint comparison or a bounded failure report. Stop after the declared candidate set has been evaluated and additional candidates are unlikely to change the stated conclusion under your coverage criterion; report that criterion and all limitations. Do not claim unperformed calculations.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`, including explicit system identity and atom mapping, state and geometry provenance, and one record per candidate with its design, generation rule, per-candidate mapping/symmetry/cap/coverage validation, named disulfide-pair and Glu17(A)-Arg22(B) observations, observables and artifacts. The selection record must identify the comparison criterion, selected candidate identities, coverage and stopping rule. The structured conclusion must cover locality, disulfides and radius sensitivity. A bounded-failure branch must preserve candidate-generation and validation evidence and identify the uncompleted endpoint; do not fabricate unavailable matrices or comparisons.
