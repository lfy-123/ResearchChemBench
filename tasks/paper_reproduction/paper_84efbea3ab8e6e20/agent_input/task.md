# Scientific objective

Determine how moving one pinacol boronate ester (Bpin) substituent among the 1-, 2-, and 4-positions of carbazole changes the isolated-molecule excited states and spin–orbit coupling (SOC), and assess whether those computed quantities support the observed room-temperature phosphorescence (RTP) lifetime differences in 0.5 wt% PVA films. The authors' qualitative hypothesis to test independently is that substitution position changes excited-state distribution and ISC propensity, with molecular/host interactions influencing persistence.

# Public inputs and scientific boundaries

Use `data/inputs/molecules.json`. The three uniquely named neutral singlet molecules are CZ1B = 1-(4,4,5,5-tetramethyl-1,3,2-dioxaborolan-2-yl)-9H-carbazole, CZ2B = the corresponding 2-substituted isomer, and CZ4B = the corresponding 4-substituted isomer; each is C18H20BNO2, charge 0, multiplicity 1, with no stereochemical specification. Computation is on isolated molecules; PVA (0.5 wt% guest loading) is an experimental boundary only. Do not use the paper or SI as an Agent input. Choose and document a reproducible geometry source/model, and do not treat an explicit PVA calculation as required.

# Required scientific validation/investigation

For all three named molecules, generate and deduplicate at least one chemically valid starting geometry, optimize a ground-state structure, and report convergence and whether the final structure is usable as a stationary point (frequency or another defensible check). Compute S1 and a documented set of triplet states, identify every triplet within ±0.30 eV of S1 or state that none exists, and report the SOC quantity and units for each retained pair. Validate state labels against energies rather than paper atom labels. Supply NTOs or an equivalent orbital/state-localization analysis for S1 and the SOC-relevant triplet. Compare common descriptors across isomers and discuss the reported PVA-film lifetime boundary. Completion requires all three molecules, state-selection evidence, SOC/state-character evidence, and a conclusion or bounded failure report. Stop when all three systems have been attempted with documented convergence/coverage; if a state or SOC calculation fails, report the failed object, attempted remedies, and the limitation rather than silently substituting another object.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json` and include method/software, geometry provenance, per-molecule energies/SOC/state identity, validation artifacts or paths, and a concise conclusion. A successful result must state the lifetime comparison and its evidential limitations; a bounded-failure result must preserve all attempted object identities and validation context. Do not report hidden source numerical SOC targets as if they were known beforehand.
