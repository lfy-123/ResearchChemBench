# Scientific objective

Test the authors' qualitative hypothesis that weak ^77Se signals in a sample of diselenide 3s arise from an Ar^F-substituted triselenide that rapidly exchanges between cis and trans conformers. Independently calculate and validate the two supplied conformers, their relative energy, and their three-site ^77Se chemical shifts, then compare the computed spectrum with the observed minor features.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that weak ^77Se signals in the diselenide sample arise from a minor Ar^F-substituted triselenide impurity, with the two supplied structures representing conformers that may exchange rapidly.

**Candidate route or mechanism.**
Treat the cis and trans triselenide structures as the focused candidate explanation for the minor spectral features, and assess whether their conformational energetics and selenium environments are compatible with that interpretation.

**Discriminating evidence.**
Use auditable geometry and stationarity validation, a common-zero relative-energy comparison, and site-resolved ^77Se chemical shifts with an explicit reference convention. Compare the resulting calculated features with the observed spectrum and use the comparison to distinguish support for the triselenide assignment from claims about a unique exchange mechanism.

# Public inputs and scientific boundaries

`data/inputs/cis.xyz` and `trans.xyz` are the complete 25-atom neutral singlet C12F10Se3 structures; atom order is the identity key and the first three atoms are Se. `experimental_boundary.json` records the observed ^77Se features (422 and 816 ppm, approximately 2:1) for 3s in CDCl3 at 25 °C. You may choose software, electronic-structure model, solvation treatment, and conformer refinement. Do not use the paper/SI or general web. Report shifts relative to Me2Se or state your alternative reference explicitly. The scored object is the isolated triselenide molecule, not a crystal or a solvent complex.

# Required scientific validation/investigation

The supplied XYZ files are unoptimized, independently generated initial structures, not stationary-point results. `data/inputs/starting_geometry_definition.json` specifies the shared molecular graph, stereochemistry, one-based atom identities and broad initial conformer classes. The class windows distinguish the named starting states only: do not impose them as optimization constraints or interpret them as final torsion targets. Optimize and validate each named starting structure independently; retain its ID and report any basin change or convergence of two starters to the same endpoint rather than silently treating duplicate endpoints as distinct conformers.

For each input, preserve atom identity/connectivity and optimize or otherwise justify the geometry used. Demonstrate stationarity for an optimized minimum (or explain a bounded alternative), identify all three Se sites by input atom index, and report the common energy zero and cis–trans relative energy. Compute a ^77Se shift for each Se site in each conformer and give an explicit assignment to the two observed features or explain why assignment is inconclusive. A calculation is complete when both structures have auditable outputs, validation diagnostics, shifts and the energy difference. If a scientifically justified calculation fails, use the bounded-failure branch and document the affected observable and diagnostic evidence; do not invent values or placeholder structures.

# Deliverables

Submit `report/results.json` conforming to the schema. Include methods, per-conformer validation, per-Se shifts, relative energy, comparison, conclusion. If a scientifically justified calculation fails, use the bounded-failure branch and document the missing observable and diagnostic evidence.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
