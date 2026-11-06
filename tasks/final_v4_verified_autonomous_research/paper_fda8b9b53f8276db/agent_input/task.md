# Local molecular structure and crystal comparison

## Scientific question

What does a molecular investigation of the free 6,7-dimethyl-2-(pyridin-2-yl)quinoxaline ligand establish about its local bonding and pyridyl orientation relative to the supplied crystal structure? Which conclusions remain dependent on the molecular model and phase?

## Input files

- `data/inputs/objects.json` defines the full neutral singlet C15H13N3 ligand (31 atoms) and maps graph IDs to CIF labels.
- `data/inputs/ccdc_2433822.cif` supplies the experimental crystal coordinates measured at 150 K; these are observations available for analysis.
- `data/inputs/experimental_bonds.json` supplies six bond measurements and their marginal standard uncertainties. These measurements are comparison data, not newly calculated molecular results.
- `data/inputs/crystal_provenance.json` records attribution and a metadata conflict: the refined atom table and formula_sum/moiety describe C15H13N3, whereas the legacy oxdiff field says C12H12N2O. Use the consistent refined identity and preserve the CIF bytes.

## Scope

Study the free ligand as an isolated neutral singlet molecule. The selected local structural comparison concerns the candidate with the pyridyl N1 and adjacent quinoxaline N2 on the same side about C1–C2 (cis-like); the opposite-side orientation is termed trans-like. These labels specify candidate identity, not an assumed minimum, preferred conformer or experimental orientation. Determine whether the selected candidate is a valid unconstrained local structure and identify its actual orientation. Choose and justify the calculation and structural analysis; no fixed software, search count or control matrix is prescribed.

The problem concerns this local molecular structure and its comparison with the experimental crystal. It does not require a global conformer search, a separately optimized trans control, solvent series or lattice simulation. Re-complex properties and antimicrobial activity are outside the question.

## Required results

1. Report the selected local molecular structure's C1–C2, C2–C3, N1–C1, N2–C2, N3–C3 and C1–C10 bond lengths in angstrom, with the atom mapping and evidence needed to establish their physical meaning.
2. Determine the pyridyl orientation in that molecular structure and in the supplied crystal using a defined torsional or equivalent geometric comparison. If the candidate is not locally stable under your model, report the supported result and its limits.
3. Interpret the six signed bond residuals and a clearly defined aggregate statistic: what do they establish about the local bonding framework? Distinguish the experimental marginal standard uncertainties from rounding and model error; no covariance matrix is supplied.
4. Explain what the combined local-bond and orientation evidence does and does not establish about molecular conformer preference and phase-dependent structure. Do not infer crystal populations or a unique packing cause from an isolated local minimum.

## Submission

Submit `report/results.json` and `report/report.md` following `submission_guide.md` and `submission_schema.json`. Support final answers with inspectable native calculations and reproducible analyses. Final scientific results total 100 points; research-process completion carries no independent points. Use only the supplied inputs, resources made available for this task and general scientific/software documentation. Private evaluator material and prior verification archives are not public resources.
