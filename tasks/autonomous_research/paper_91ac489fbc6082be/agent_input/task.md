# Scientific objective

Determine which of the two enantiomeric assignments of neutral compound 2 (formula C30H34O6) is supported by calculated VCD compared with the supplied experimental boundary. Report enantiomer-specific similarity metrics and a justified configuration conclusion. Independently formulate and test a computational route for the absolute configuration of compound 2 using calculations and the supplied experimental boundary; no author software, model chemistry or ordered protocol is prescribed.

# Public inputs and scientific boundaries

Use `data/inputs/system.json`, `data/inputs/compound2_conformer_2a.xyz`, and the supplied plotted experimental traces in `data/inputs/experimental_vcd_traces.csv` (with provenance in `experimental_vcd_traces_provenance.json`). The XYZ file is the complete 70-atom starting geometry for C30H34O6; formula, charge, multiplicity, units and VCD window are explicit. You may generate conformers and computational models, but do not use the paper, SI or general web. The measured quantity is VCD similarity for each enantiomer against the supplied CDCl3/C6D6 plotted traces; omit or explicitly handle the solvent-absorption region near 1330 cm-1 and report that the traces are digitized plotted observations rather than raw instrument data.

# Required scientific validation/investigation

Validate the supplied 70-atom geometry (C30H34O6, neutral, singlet), formulate and justify the computational approach, generate and deduplicate additional conformers if used, and state search coverage. Compute VCD for both enantiomers with a reproducible method, explain ensemble weighting and spectral processing, and provide frequencies/intensities or a machine-readable spectrum sufficient to audit similarity. Completion requires both comparisons plus a conclusion, or a bounded-failure report naming each failed calculation, the attempted assignment(s), and evidence obtained. Stop when added conformers no longer change the conclusion or resources prevent that test; quantify the limitation.

# Deliverables

Submit `report/results.json` matching submission_schema.json. Include method, structure checks, conformer records, both similarity values when available, comparison metric, conclusion, limitations and provenance.
