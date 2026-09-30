# Scientific objective

Test whether a local, overlapping-fragment quantum workflow can reconstruct the global atomic mutual-information (AMI) and residue-level fragment mutual-information (FMI) correlation map of the specified two-chain human insulin structure.

# Author-provided scientific guidance

The reproduction mode additionally asks whether the authors' qualitative locality/cut-wise hypothesis is supported: local calculations should recover chemically meaningful correlations while potentially omitting weak long-range interactions.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json` and the supplied original experimental `data/inputs/3I40.pdb`; no network retrieval is required. Preserve chain A/B and residue identities. The measured objects are orbital MI, atom-pair AMI and residue-pair FMI; report matrix indexing, symmetry convention, units (nat for information), diagonal handling and cap-atom exclusion. The quantum system is protein-only after solvent/ion removal. You may choose software and model chemistry, but must disclose them and the selected charge/multiplicity. The author hypothesis is qualitative only; no winning candidate, numerical target, or paper protocol is provided.

# Required scientific validation/investigation

Define and enumerate your fragment candidates before calculations, retaining center residue/atom, radius, included atoms, caps and geometry provenance. Deduplicate identical candidates and state the advancement rule. Compute AMI/FMI from your own fragment electronic-structure results for the selected set, stitch atom pairs using a stated overlap rule, and validate symmetry, atom/residue mapping, cap exclusion and coverage. An additional independent full-system comparison is optional: omitting it does not prevent completion of the required fragment reconstruction and contact checks. Copying author-released matrices is not a substitute for fragment calculations. Report whether the reconstructed map contains the three known insulin disulfide pairs and the Glu17(A)-Arg22(B) contact, and whether radius sensitivity changes that contact. Completion requires a machine-readable result plus provenance for every reported matrix and explicit calculation coverage.

The primary spherical comparison uses one center at each of the 51 residue Cα atoms. From one consistently prepared/protonated full-protein geometry, include a whole residue if any of its atoms (including H) lies within the stated radius; determine membership before adding caps or relaxing fragments. Cap severed peptide valences with NH2/COOH groups, record other boundary-bond treatment, and exclude cap atoms from the MI map. Independently prepare the experimental input, retain its chain/residue mapping, and document geometry preparation; no prepared answer geometry is supplied. These are common comparison definitions, not a prescribed electronic-structure method. Extra fragment designs must be reported separately.

For the primary comparison, reconstruct the protein-wide 5.0 Å map and evaluate the Glu17(A)–Arg22(B) contact at 4.0, 5.0 and 6.0 Å; extra radii and designs are allowed. The 4/6 Å cases require the named contact and all contributing fragments, not three complete global maps. Use the positive MI definition, nat units, cap exclusion and atom-pair averaging before residue aggregation in `system_spec.json`. Record uncovered pairs separately from computed zeros; do not infer interaction absence from lack of coverage.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. The result must contain explicit system identity and atom mapping; state and geometry provenance; one record per fragment with center, radius, included atoms, caps and geometry provenance; validation checks and coverage; separate entries for each of the three named disulfide pairs and the Glu17(A)-Arg22(B) radius cases; AMI/FMI definitions, matrix artifacts and metrics; and a structured conclusion covering locality, disulfides and radius sensitivity. For `partial`, `failed` or `bounded_failure`, provide `system.pdb_id` and a `failure_report` with completed artifacts, missing endpoint and reason; include other fields only when available. Do not fabricate unavailable matrices, mappings or comparison values.
