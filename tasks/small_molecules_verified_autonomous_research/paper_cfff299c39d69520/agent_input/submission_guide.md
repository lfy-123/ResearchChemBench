# Reproducible evidence submission

Use agent-defined IDs for models, operations, artifacts, quantitative results, claims and validations. Record complete molecular identities, charge and electronic state, relevant stereochemistry, method, solvent, temperature, standard state, stoichiometry and the reference defining each result. Link every quantitative claim to actual inputs, native outputs and an extraction location; preserve generated evidence under outputs/ and analysis scripts under code/.

Result arrays may be empty when no physical result was obtained. Do not invent barriers, winners, endpoints or numerical values to fill the schema. For an abnormally terminated run, provide failure_report with the affected scope, cause and any available evidence; record attempts and surviving results. The schema checks representation, not scientific validity. 

For claims about minima, saddles, states and mechanistic connections provide the evidence necessary to support those claims. For energy comparisons document a balanced common reference and distinguish electronic energy, enthalpy, free energy, local activation barriers and overall energy spans. Provide uncorrected terms and conversion formulas when conventions differ. Do not treat a scan maximum, a normal program exit or an unconnected imaginary mode as a validated reaction barrier.

Methods and exploration are your choices. No hypothesis count, named intermediate sequence, fixed grid or number of calculations is required. Explain decisions in report/report.md. Use the supplied public inputs, available computational tools and general scientific/software documentation.

Use Gibbs free energies in kcal/mol at 298.15 K with a consistent 1 atm thermochemical convention for the primary profile. Give all species and their stoichiometric coefficients in each profile reference, including base, acid/base products, leaving ions and ligand reservoirs. Catalyst formation from precatalyst, local activation barriers and finite-path energy heights have different references. State each balanced expression and identify the principal activation demand within the tested path. No catalyst-regeneration calculation, full-cycle energy span or steady-state turnover frequency is required. For temperature interpretation, distinguish a conditional constant-ΔG Eyring illustration from an actual temperature-dependent free-energy calculation; do not silently treat ΔG(298.15 K) as a computed ΔG(398.15 K).

## Final scientific conclusions

Address each required result explicitly in the final answer and connect it to the existing results/claims/artifacts records. Link the supporting calculations and validation evidence to each conclusion. Use the existing schema.
