# Scientific question

How does PA addition change the local structure and electronic interactions of the (Et2N)3P/Et3B system, and what do those molecular changes support about epoxide association and oxygen-containing chain-end interactions?

# Input files

- `data/inputs/systems.json`: chemical identities, atom mapping and any supplied starting structures. These do not establish stable states or pathways.
- `data/inputs/observations.json`: known observations; these are context to explain, not new predictions.
- `data/inputs/source_facts.json`: conditions and model boundaries.

# Scope

Use the supplied identities of (Et2N)3P, phthalic anhydride (PA), Et3B, propylene oxide (PO), CO2 and the TFPO/ethoxide probes. For the local molecular comparison, consider complete neutral singlet free phosphine and 1:1 phosphine/PO and phosphine/PA inventories (46, 56 and 61 atoms respectively); construct and justify their molecular arrangements. Report local geometry and ADCH atomic populations for comparable gas-phase ground-state structures. Separate this molecular reference from the bulk feed [PO]/[PA]/[(Et2N)3P]/[Et3B]=2000/1/1/2 at 80 °C and initial CO2 pressure 2.0 MPa. The supplied TFPO observations concern C6D6, while the ethoxide probe uses CDCl3 after THF preparation. These are known interaction observations, not measured reaction barriers or long-chain binding energies. Bulk productivity, molecular weight, full polymerization networks and other catalyst families are outside scope.

# Reproduction baseline

The authors propose that PA reacts with the Lewis base to generate an intramolecular phosphonium/carboxylate zwitterion, interacting with Et3B and influencing both epoxide activation and chain-end association (main pp9–10). Their DFT comparison concerns free(Et2N)3P, the PO adduct and the PA adduct, not a full polymer propagation/backbiting network. SI pp4–5 specifies Gaussian16 B3LYP/6-31G(d) with D3(BJ), with ADCH populations from Multiwfn using vibrational-analysis wavefunctions. The source does not explicitly specify a continuum solvent for these molecular calculations. Main p10 reports PO-adduct O···P1.828 Å versus PA-adduct2.651 Å and differing O···H contacts/populations; those local observations support an interpretation but do not directly prove suppressed backbiting. Reproduce and assess the local molecular baseline or justify controlled substitutions. NMR probe results use TFPO/C6D6 and sodium ethoxide/CDCl3, with preparation details inSI p4. Source polymer kinetics and dilution behavior are a separate scale. The fixed PA-containing two-PO/one-CO2 oligomer, no-PA chain pair, two-Et3B path inventory and tenfold-PO test inV1 were benchmark additions.

Source-coordinate limitation: SI physical pp39-40 lists 51 atoms (C14H30N3O3P) for the PA adduct; the complete stoichiometric (Et2N)3P + PA model has 61 atoms (C20H34N3O3P), a C6H4 difference. The complete PA reagent connectivity in systems.json remains valid. Reconstruction must identify retained source atoms, added atoms and the resulting graph; a reconstructed model is not an unchanged source geometry. No missing coordinates are supplied or invented here. For main physical p8 Figure 6 and p10, distinguish a specified H-site ADCH population, the nearest-contact H and a declared alpha/beta-H family statistic. Define sites from the N-ethyl CH2/CH3 graph and map them explicitly; do not equate a figure-labelled H with a nearest site or family mean without evidence. Report signed electrostatic potential with its units and surface definition separately from electron density; source colour/prose alone is not a density measurement. These local observables do not by themselves establish polymer propagation or backbiting rates.

# Required results

1. Report the terminal oxygen–phosphorus separation (Å) for each complete phosphine/PO and phosphine/PA molecular adduct, and the signed phosphorus ADCH charge (e) for free phosphine and both adducts. Define the oxygen site and all mappings from connectivity.
2. Explain how the local oxygen contact network changes between the two adducts, including the N-ethyl CH2/CH3 hydrogen environments; do not infer interaction strength from distance alone.
3. Determine and interpret the spatial charge/electrostatic distribution of the PA-derived species, distinguishing signed electrostatic potential from electron density.
4. Assess its local contribution to epoxide association in the presence of Et3B using computed molecular evidence and the supplied probe context.
5. Assess what the molecular evidence supports about interactions with oxygen-containing chain ends, including the limits on extrapolation to polymer propagation or backbiting.

Reproduce and assess the disclosed baseline; explain scientifically justified substitutions. Support each answer with actual calculations or executed quantitative analysis. Define molecular states, units, energy references and conditions. Geometry, frequencies or connectivity evidence must support the claims that depend on them; no fixed search procedure or number of calculations is required.

# Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link reported quantities and claims to preserved inputs, native outputs and analysis artifacts. The existing record fields document provenance and earn no separate points. Use the supplied inputs and disclosed baseline; do not consult undisclosed source documents, private evaluation files or previous runs.
