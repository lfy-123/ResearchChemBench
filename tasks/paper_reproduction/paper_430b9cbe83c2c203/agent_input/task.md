# Scientific objective

Test the authors' qualitative hypothesis that weak ^77Se signals in a sample of diselenide 3s arise from an Ar^F-substituted triselenide that rapidly exchanges between cis and trans conformers. Independently calculate and validate the two supplied conformers, their relative energy, and their three-site ^77Se chemical shifts, then compare the computed spectrum with the observed minor features.

# Public inputs and scientific boundaries

`data/inputs/cis.xyz` and `trans.xyz` are the complete 25-atom neutral singlet C12F10Se3 structures; atom order is the identity key and the first three atoms are Se. `experimental_boundary.json` records the observed ^77Se features (422 and 816 ppm, approximately 2:1) for 3s in CDCl3 at 25 °C. You may choose software, electronic-structure model, solvation treatment, and conformer refinement. Do not use the paper/SI or general web. Report shifts relative to Me2Se or state your alternative reference explicitly. The scored object is the isolated triselenide molecule, not a crystal or a solvent complex.

# Required scientific validation/investigation

For each input, preserve atom identity/connectivity and optimize or otherwise justify the geometry used. Demonstrate stationarity for an optimized minimum (or explain a bounded alternative), identify all three Se sites by input atom index, and report the common energy zero and cis–trans relative energy. Compute a ^77Se shift for each Se site in each conformer and give an explicit assignment to the two observed features or explain why assignment is inconclusive. A calculation is complete when both structures have auditable outputs, validation diagnostics, shifts, energy difference, and uncertainty/limitations. If a scientifically justified calculation fails, use the bounded-failure branch and document the affected observable and diagnostic evidence; do not invent values or placeholder structures. Stop after both named conformers and the requested comparison are covered; do not expand to an unbounded conformer search.

# Deliverables

Submit `report/results.json` conforming to the schema. Include methods, per-conformer validation, per-Se shifts, relative energy, comparison, conclusion, and limitations. If a scientifically justified calculation fails, use the bounded-failure branch and document the missing observable and diagnostic evidence.
