# Scientific objective

Determine the relative configuration of pyrethalkaline A (compound 1) by independently calculating and comparing 13C NMR observables for the two supplied diastereomeric geometries. The research object is neutral singlet C30H45N3O3 pyrethalkaline A; the measured data are 30 assigned carbon chemical shifts in ppm and a per-candidate statistical assignment probability. This task tests relative configuration only, not absolute configuration or biological activity.

# Public inputs and scientific boundaries

`data/inputs/experimental_13C_shifts.json` gives compound identity, charge, multiplicity, solvent context, and 30 carbon-site shifts. `candidate_8R_9aR_12aR.xyz` is candidate A, labeled 8R*,9aR*,12aR*; `candidate_8S_9aR_12aR.xyz` is candidate B, labeled 8S*,9aR*,12aR*. Each XYZ is one complete 81-atom C30H45N3O3 geometry with fixed element/coordinate order. `input_manifest.json` defines mapping and permitted conformer generation. Preserve formula, charge, multiplicity, stereochemical identity, and carbon labels. Additional conformers are allowed only without changing connectivity or protonation.

# Required scientific validation/investigation

Verify atom count and formula for each input, document mapping of the 30 carbon sites to experimental labels, and perform a defensible quantum-chemical shielding-to-shift workflow for both candidates. Combine conformers transparently if used and calculate a reproducible fit statistic and DP4+ or a clearly justified equivalent statistical comparison. Validate that both candidates were treated comparably, probabilities are normalized, and the assignment follows submitted calculations. Complete successfully when both candidates have predictions for all 30 mapped carbon sites, provenance, statistical comparison, conclusion, validation evidence, and limitations. Stop after both candidates and any conformers meeting the stated coverage criterion have been evaluated. If a candidate, site mapping, or required calculation cannot be completed within the declared resources, submit `status: bounded_failure`, identify the affected candidate(s) and missing evidence in the candidate records and `failure_reason`, and do not invent shifts, fit values, probabilities, or an assignment.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, containing status, per-candidate input validation, fit statistics, normalized probabilities when available, conclusion, validation evidence, and limitations.

Each additional `*_conf2.xyz` contains a separate second conformer of the same diastereomer; never concatenate conformers into a single quantum-chemical system.
