# Scientific objective

Determine how moving one pinacol boronate ester (Bpin) substituent among the 1-, 2-, and 4-positions of carbazole changes the isolated-molecule excited states and spin–orbit coupling (SOC), and assess the molecular evidence relevant to room-temperature phosphorescence (RTP) persistence in 0.5 wt% PVA films. The authors' qualitative hypothesis to test independently is that substitution position changes excited-state distribution and ISC propensity, with molecular/host interactions influencing persistence.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors attribute differences among the positional isomers to changes in excited-state distribution and spin–orbit coupling, together with hydrogen-bonding interactions between the boronate ester and the PVA host. They discuss these effects as influences on intersystem crossing and suppression of nonradiative decay, while the isolated-molecule calculations can directly test only the molecular component.

**Candidate route or mechanism.**
Prioritize comparing locally concentrated versus spatially separated hole/electron or NTO character in S1 and the relevant triplet, and test whether the substitution site changes the energetic proximity and SOC of singlet–triplet pairs. Treat enhanced ISC propensity and reduced nonradiative loss as competing explanations for the film lifetime trend; host hydrogen bonding and solid-state packing are comparison hypotheses that require explicit evidence beyond an isolated-molecule calculation.

**Discriminating evidence.**
Use optimized-structure validation, state energies and energy gaps, SOC matrix elements, NTOs or equivalent hole/electron composition analysis, and common electronic descriptors such as electrostatic potential. Compare these consistently across CZ1B, CZ2B, and CZ4B, then report the computed cross-isomer differences and explain what isolated molecular calculations cannot establish about PVA-film lifetimes.

# Public inputs and scientific boundaries

Use `data/inputs/molecules.json`. The three uniquely named neutral singlet molecules are CZ1B = 1-(4,4,5,5-tetramethyl-1,3,2-dioxaborolan-2-yl)-9H-carbazole, CZ2B = the corresponding 2-substituted isomer, and CZ4B = the corresponding 4-substituted isomer; each is C18H20BNO2, charge 0, multiplicity 1, with no stereochemical specification. The listed CCDC identifiers are provenance metadata only: no CIF is supplied or required, and CCDC database retrieval is not required or scored. Generate molecular geometries from the explicit names and positional identities. Computation is on isolated molecules; PVA (0.5 wt% guest loading) is an experimental boundary only. Do not use the paper or SI as an Agent input. Choose and document a reproducible geometry source/model, and do not treat an explicit PVA calculation as required.

Experimental lifetimes and their ordering are not supplied. The evaluator will compare your molecular evidence with its private experimental reference. You are not required to reproduce or infer that hidden experimental ranking, predict absolute film lifetimes, or access the paper. Submit `conclusion.computed_comparison`, `interpretation`; all required SOC and state-character evidence remains mandatory.

# Required scientific validation/investigation

For all three named molecules, generate and deduplicate at least one chemically valid starting geometry, optimize a ground-state structure, and report convergence and whether the final structure is usable as a stationary point (frequency or another defensible check). Compute S1 and a documented set of triplet states, identify every triplet within ±0.30 eV of S1 or state that none exists, and report the SOC quantity and units for each retained pair. Validate state labels against energies rather than paper atom labels. Supply NTOs or an equivalent orbital/state-localization analysis for S1 and the SOC-relevant triplet. Compare common computed descriptors across isomers and discuss the isolated-molecule/PVA boundary without guessing unprovided experimental lifetimes. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json` and include method/software, geometry provenance, per-molecule energies/SOC/state identity, validation artifacts or paths, and a concise conclusion. A successful result must state the computed cross-isomer comparison and its supporting calculation evidence; a bounded-failure result must preserve all attempted object identities and validation context. Do not report hidden source numerical SOC targets as if they were known beforehand.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
