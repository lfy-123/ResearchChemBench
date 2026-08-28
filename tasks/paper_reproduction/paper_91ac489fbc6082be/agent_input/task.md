# Scientific objective

Determine which of the two enantiomeric assignments of neutral compound 2 (formula C30H34O6) is supported by calculated VCD compared with the supplied experimental boundary. Report enantiomer-specific similarity metrics and a justified configuration conclusion. The authors qualitatively use conformer-ensemble VCD calculations to test an absolute-configuration assignment. Independently test this route; do not assume its outcome.

# Public inputs and scientific boundaries

Use `data/inputs/system.json` and `data/inputs/compound2_conformer_2a.xyz`. The XYZ file is the complete 74-atom starting geometry; formula, charge, multiplicity, units and VCD window are explicit. You may generate conformers and computational models, but do not use the paper, SI or general web. The measured quantity is VCD similarity for each enantiomer; omit or explicitly handle the solvent-absorption region near 1330 cm-1.

# Required scientific validation/investigation

Validate the supplied 70-atom geometry (C30H34O6, neutral, singlet), generate and deduplicate additional conformers if used, and state search coverage. Compute VCD for both enantiomers with a reproducible method, explain ensemble weighting and spectral processing, and provide frequencies/intensities or a machine-readable spectrum sufficient to audit similarity. Completion requires both comparisons plus a conclusion, or a bounded-failure report naming each failed calculation, the attempted assignment(s), and evidence obtained. Stop when added conformers no longer change the conclusion or resources prevent that test; quantify the limitation.

# Deliverables

Submit `report/results.json` matching submission_schema.json. Include method, structure checks, conformer records, both similarity values when available, comparison metric, conclusion, limitations and provenance.
