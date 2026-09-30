# Scientific objective

Determine whether the two supplied Ar-substituted triselenide structures can account for weak ^77Se features in the associated diselenide sample by independently calculating their relative energetics and three-site ^77Se chemical shifts, and state the strength and limits of the structural assignment.

# Public inputs and scientific boundaries

`data/inputs/cis.xyz` and `trans.xyz` are complete 25-atom neutral singlet C12F10Se3 structures; atom order is the identity key and the first three atoms are Se. `experimental_boundary.json` records observed ^77Se features of 422 and 816 ppm, approximately 2:1, in CDCl3 at 25 °C. Choose and justify the computational method and validation strategy independently. Do not use the paper/SI or general web. The scored object is the isolated triselenide molecule, not a crystal or solvent complex.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

# Required scientific validation/investigation

The supplied XYZ files are unoptimized, independently generated initial structures, not stationary-point results. `data/inputs/starting_geometry_definition.json` specifies the shared molecular graph, stereochemistry, one-based atom identities and broad initial conformer classes. The class windows distinguish the named starting states only: do not impose them as optimization constraints or interpret them as final torsion targets. Optimize and validate each named starting structure independently; retain its ID and report any basin change or convergence of two starters to the same endpoint rather than silently treating duplicate endpoints as distinct conformers.

For each named structure, preserve identity/connectivity, optimize or justify the geometry, demonstrate stationarity for a minimum or explain a bounded alternative, identify each Se site by input atom index, and report relative energy with a common zero. Calculate three ^77Se shifts per conformer, state the reference convention, and compare them explicitly with the observed features. A calculation is complete when both structures and all requested observables have auditable outputs. If a scientifically justified bounded attempt cannot obtain an observable, report the affected object, missing observable, and diagnostic evidence in the bounded-failure branch; do not fabricate values.

# Deliverables

Submit `report/results.json` conforming to the schema. Include methods, per-conformer validation, per-Se shifts, relative energy, comparison, conclusion. If a scientifically justified calculation fails, use the bounded-failure branch and document diagnostics and missing observables.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
