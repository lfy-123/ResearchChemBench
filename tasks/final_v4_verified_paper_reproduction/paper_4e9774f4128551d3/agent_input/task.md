# Scientific question

What can the relative stability of the trans and cis ketoesters establish about reversible epimerization and the observed two-pot enolization/protonolysis outcome, and what remains undetermined about the finite-time stereoselectivity?

# Input files

- `data/inputs/systems.json`: chemical identities, atom mapping and any supplied starting structures. These do not establish stable states or pathways.
- `data/inputs/observations.json`: known observations; these are context to explain, not new predictions.
- `data/inputs/source_facts.json`: conditions and model boundaries.

# Scope

Study the intact neutral C20H30O3 ketoester pair obtained by inversion only at atom map 6 of `50_graph`; retain all other stereocenters. The supplied `enol_TMS` graph defines the intervening tetrasubstituted O-TMS enol ether. Preparation uses HMDS (2.0 equiv) and TMSI (1.4 equiv) in CH2Cl2 at 23 °C for 30 min, followed in a second pot by racemic camphorsulfonic acid (1.0 equiv) at 23 °C for 30 min. The supplied records disagree on the THF/MeOH volume ratio (1:1 versus 10:1); declare the interpretation and model medium used. Observed reversible epimerization returns trans material, whereas the two-pot sequence gives a 1.1:1 trans:cis mixture. Three recycling rounds give 70% isolated cis material. These are known observations to explain. Full synthesis, acid screening, exact yields and identification of a unique protonation transition state are outside scope.

# Reproduction baseline

The authors sought cis material despite calculations favouring trans-50 by 2.32 kcal/mol. They report that reversible epimerization gave trans, whereas isolated silyl-enol-ether protonolysis with (±)-CSA gave 1.1:1 trans:cis. Their DFT comparison is a product thermodynamic rationale, not a calculated protonation mechanism. SI p71 specifies Gaussian09, B3LYP-D3/6-31G(d,p) optimization, B3LYP-D3/6-311++G(d,p) single points and IEF-PCM methanol (epsilon32.63), with thermal corrections; tables S35–S38 provide structures/frequencies. Reproduce/audit that disclosed baseline and assess its explanatory limits. A solvent inconsistency remains between main Scheme5 and SI pp20–21; document which interpretation is used. Acid-face pathways, single-MeOH clusters and mandatory weighted kinetic matrices were added by the benchmark, not established by the source.

# Required results

1. Report G(cis) − G(trans) in kcal/mol for comparable intact endpoints and interpret their relative stability, stating temperature, medium and conformational scope.
2. Calculate the equilibrium implication of that energy difference and relate it to both the reversible experiment and the 1.1:1 two-pot observation.
3. Determine whether endpoint thermodynamics uniquely specifies the 30 min product ratio; support the answer with an explicit consistent quantitative analysis.
4. Explain the local stereochemical change through the supplied enol-ether graph and its relation to access to the two epimers; distinguish single-pass selectivity from cumulative recycling yield.

Reproduce and assess the disclosed baseline; explain scientifically justified substitutions. Support each answer with actual calculations or executed quantitative analysis. Define molecular states, units, energy references and conditions. Geometry, frequencies or connectivity evidence must support the claims that depend on them; no fixed search procedure or number of calculations is required.

# Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link reported quantities and claims to preserved inputs, native outputs and analysis artifacts. The existing record fields document provenance and earn no separate points. Use the supplied inputs and disclosed baseline; do not consult undisclosed source documents, private evaluation files or previous runs.
