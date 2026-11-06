# Scientific question

How does removal of one electron change the sulfur–sulfur separation and electronic interaction in norDTCO and DTCO, and how does the constrained norDTCO framework affect the response relative to DTCO?

# Input files

- `data/inputs/objects.json` defines the complete atom-indexed norDTCO (C10H14S2) and DTCO (C6H12S2) graphs. Each neutral is a singlet; its radical cation has charge +1 and multiplicity 2. The graphs prescribe neither an S–S bond nor an optimized geometry.
- `data/inputs/observations.json` supplies gas-phase photoelectron measurements for context. They are known observations, not computational prediction targets.

# Scope

Compare isolated finite molecules at the neutral and first-oxidation levels. Declare the conformational family and atom correspondence used in each neutral/radical comparison. Limit structural conclusions to the basins actually established. These calculations alone do not determine dication chemistry, solution electrode potentials or protein electron-transfer rates. Absolute ionization energies are not required; any optional comparison must distinguish vertical, adiabatic and orbital-energy definitions.

# Required results

1. Report neutral and radical-cation S···S distances in Å for each molecule, the signed distance change Δd = d(neutral) − d(radical), and compare the two responses.
2. Give a calculated electronic interpretation of the first-oxidation sulfur interaction for each molecule. Identify the region of electron removal and unpaired spin, and explain the bonding implication using appropriate orbital or density evidence. Define population/spin conventions; a distance or charge label alone does not establish bonding.
3. Explain whether the difference between the two structural responses reflects framework restriction, a difference in electronic interaction, or both. State the extent to which the calculated local response supports that explanation.

Choose and justify your own models and electronic-structure method. Support each final claim with actual calculations and claim-appropriate evidence. Do not infer global populations from a single local geometry or turn a bonding descriptor into an exact integer bond order.

# Submission

Submit `report/results.json` and `report/report.md` following `submission_schema.json` and `submission_guide.md`. Link native inputs, outputs, structures and analysis to the reported results. Only final scientific propositions earn points; evidence and research operations have no separate score. Use the supplied inputs and general scientific/software resources described in `resources.md`.
