# Electron Isodensity source curation audit

The official Nature Communications article, PubMed Central package, article
supplements, source data, and general web results were checked.  The public
record contains Supplementary Information, Supplementary Data 1, the complete
Supplementary Data 2 coordinate archive, Supplementary Software, and Source
Data.  No separate author GitHub or data repository was identified.

The paper reports 1071 conformers for 104 molecules, whereas the public
Supplementary Data 2 archive contains 1074 XYZ files with 104 unique molecule
prefixes.  This discrepancy is retained as provenance.  The benchmark uses
only seven named molecules and copies only task-relevant conformers into each
guided-reproduction task.

Agent-visible task data never include the paper PDF, Supplementary Data 1,
Source Data, author-computed surface areas, wavefunctions, ORCA outputs, or the
paper's optimal cutoff.  Public conformer coordinates are exposed only in the
guided-reproduction track.
