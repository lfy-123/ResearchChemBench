# GEOM hierarchical conformer reranking reproduction

Starting only from the supplied GEOM-C3 SMILES, reconstruct a thermally relevant
conformer ensemble. Use RDKit for diverse embedding and clustering, xTB/CREST for
low-cost exploration, ORCA for r2SCAN-3c/C-PCM(water) refinement and Hessians, and
GoodVibes for 298.15 K thermochemistry. The paper result values are hidden.

Paper: 10.1038/s41597-022-01288-4.
