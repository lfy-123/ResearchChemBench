# Scientific objective

Independently investigate whether positional isomerism of Bpin-substituted carbazole (CZ1B, CZ2B, CZ4B) changes excited-state structure and SOC in a way that can explain differences in blue RTP persistence in PVA films. Formulate and discriminate plausible explanations using calculations and report what the evidence does and does not establish.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors attribute differences among the positional isomers to changes in excited-state distribution and spin–orbit coupling, together with hydrogen-bonding interactions between the boronate ester and the PVA host. They discuss these effects as influences on intersystem crossing and suppression of nonradiative decay, while the isolated-molecule calculations can directly test only the molecular component.

**Candidate route or mechanism.**
Prioritize comparing locally concentrated versus spatially separated hole/electron or NTO character in S1 and the relevant triplet, and test whether the substitution site changes the energetic proximity and SOC of singlet–triplet pairs. Treat enhanced ISC propensity and reduced nonradiative loss as competing explanations for the film lifetime trend; host hydrogen bonding and solid-state packing are comparison hypotheses that require explicit evidence beyond an isolated-molecule calculation.

**Discriminating evidence.**
Use optimized-structure validation, state energies and energy gaps, SOC matrix elements, NTOs or equivalent hole/electron composition analysis, and common electronic descriptors such as electrostatic potential. Compare these consistently across CZ1B, CZ2B, and CZ4B, then relate the molecular findings cautiously to the reported PVA-film lifetime boundary.

# Public inputs and scientific boundaries

Use `data/inputs/molecules.json`. It defines the uniquely named neutral singlet molecules CZ1B (1-substituted), CZ2B (2-substituted), and CZ4B (4-substituted), all C18H20BNO2 with charge 0 and multiplicity 1. The scored system is each isolated molecule; do not add a host or solvent. The 0.5 wt% PVA film is the experimental measurement boundary for the lifetime comparison.

# Required scientific validation/investigation

Define a finite, reproducible candidate/state plan before calculation, including geometry alternatives if used, deduplication, advancement criteria, and a stopping rule. Attempt all three named molecules, optimize or otherwise validate usable ground-state structures, calculate S1 and nearby triplets, and define a quantitative near-state window or justify another common state-selection rule. For every retained SOC pair report state identity, energies, units, and validation evidence; provide NTOs or an equivalent state-character analysis and compare at least two plausible explanations for any lifetime trend. Completion requires three-molecule coverage, explicit search coverage/stopping, and a conclusion or bounded failure report. Stop after the planned candidate/state space is exhausted or all three systems have defensible validated calculations; preserve failed candidates and limitations instead of silently dropping them.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Include the search plan and coverage, per-candidate identity and validation context, computed observables, discriminated hypotheses, and a conclusion tied to the experimental PVA lifetime boundary. A bounded-failure branch must report what was attempted and why a final comparison could not be made. Do not invent a discovery story or claim that an uncomputed host effect was directly calculated.
