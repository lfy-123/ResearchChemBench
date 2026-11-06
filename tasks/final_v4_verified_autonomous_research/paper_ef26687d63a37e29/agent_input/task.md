# Scientific question

How does PA addition change the local structure and electronic interactions of the (Et2N)3P/Et3B system, and what do those molecular changes support about epoxide association and oxygen-containing chain-end interactions?

# Input files

- `data/inputs/systems.json`: chemical identities, atom mapping and any supplied starting structures. These do not establish stable states or pathways.
- `data/inputs/observations.json`: known observations; these are context to explain, not new predictions.
- `data/inputs/source_facts.json`: conditions and model boundaries.

# Scope

Use the supplied identities of (Et2N)3P, phthalic anhydride (PA), Et3B, propylene oxide (PO), CO2 and the TFPO/ethoxide probes. For the local molecular comparison, consider complete neutral singlet free phosphine and 1:1 phosphine/PO and phosphine/PA inventories (46, 56 and 61 atoms respectively); construct and justify their molecular arrangements. Report local geometry and ADCH atomic populations for comparable gas-phase ground-state structures. Separate this molecular reference from the bulk feed [PO]/[PA]/[(Et2N)3P]/[Et3B]=2000/1/1/2 at 80 °C and initial CO2 pressure 2.0 MPa. The supplied TFPO observations concern C6D6, while the ethoxide probe uses CDCl3 after THF preparation. These are known interaction observations, not measured reaction barriers or long-chain binding energies. Bulk productivity, molecular weight, full polymerization networks and other catalyst families are outside scope.

# Required results

1. Report the terminal oxygen–phosphorus separation (Å) for each complete phosphine/PO and phosphine/PA molecular adduct, and the signed phosphorus ADCH charge (e) for free phosphine and both adducts. Define the oxygen site and all mappings from connectivity.
2. Explain how the local oxygen contact network changes between the two adducts, including the N-ethyl CH2/CH3 hydrogen environments; do not infer interaction strength from distance alone.
3. Determine and interpret the spatial charge/electrostatic distribution of the PA-derived species, distinguishing signed electrostatic potential from electron density.
4. Assess its local contribution to epoxide association in the presence of Et3B using computed molecular evidence and the supplied probe context.
5. Assess what the molecular evidence supports about interactions with oxygen-containing chain ends, including the limits on extrapolation to polymer propagation or backbiting.

Choose computational methods and explanatory models independently. Support each answer with actual calculations or executed quantitative analysis. Define molecular states, units, energy references and conditions. Geometry, frequencies or connectivity evidence must support the claims that depend on them; no fixed search procedure or number of calculations is required.

# Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link reported quantities and claims to preserved inputs, native outputs and analysis artifacts. The existing record fields document provenance and earn no separate points. Use the supplied public inputs. Private evaluation files and other-mode or previous-run archives are not permitted inputs.
