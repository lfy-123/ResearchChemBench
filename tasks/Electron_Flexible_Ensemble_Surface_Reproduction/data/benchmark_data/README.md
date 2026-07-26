# Flexible-conformer electron-isodensity reproduction

Use the 25 published ISO-M6 conformers as a search pool. RDKit and xTB/CREST must
validate and cluster the pool; select 4-6 conformers for high-level refinement using
both energy and structural diversity. Obtain thermochemical weights, generate the
paper production density with ORCA, export a wavefunction, and calculate surfaces
with Multiwfn. Paper surface values are hidden.

Paper: 10.1038/s41467-024-50408-8.
