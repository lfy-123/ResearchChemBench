# Scientific objective

Independently determine whether and how the substituents in the two fully specified benzothiophene-fused pentalenes 4a and 4c alter NICS(1.7)zz. Calculate the descriptor, validate the structures and probe construction, discriminate plausible explanations using the computed evidence, and report a scope-limited conclusion. Do not assume an author route, result direction, numerical target, or ordering.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the 1,4-substituents modulate the paratropic response of this benzothiophene-fused pentalene scaffold: electron-withdrawing substituents are expected to strengthen the antiaromatic response, whereas electron-donating substituents are expected to weaken it.

**Candidate route or mechanism.**
Compare the two specified endpoints as an electron-withdrawing versus electron-donating substitution pair and examine whether their differing electronic effects are reflected in the out-of-plane magnetic response of the pentalene core. Treat this as a candidate structure-property explanation to be tested for these two systems.

**Discriminating evidence.**
Use validated equilibrium geometries and ring-resolved NICS(1.7)zz values at the two centroid-normal ghost probes, their arithmetic means, and a meaningful method, basis, geometry, or orientation sensitivity check. Compare the two ring values and assess whether the observed ordering is consistent with the proposed substituent effect while recording methodological limitations.

# Public inputs and scientific boundaries

The only chemical systems are the two entries in `data/inputs/systems.json`, each identified by full systematic name, formula, neutral formal charge, singlet multiplicity, and explicit substituent attachment definition. Use gas-phase equilibrium electronic structures. The measured quantity is NICS(1.7)zz at ghost centers 1.700 Å from the centroids of the two central monocyclic five-membered carbon rings, normal to the least-squares pentalene-core mean plane; report both ring values and their arithmetic mean in ppm with the stated sign convention. Exclude solvent, crystal packing, finite-temperature/vibrational averaging, excited states, and kinetics.

# Required scientific validation/investigation

Plan and justify an independent computational route. Optimize each neutral singlet and validate a minimum by frequency analysis, or record bounded failure with the attempted calculation and evidence. Reproducibly construct and label both ring probes for each system, perform at least one meaningful sensitivity check or quantify why it was infeasible, and propose at least two plausible explanations for any observed difference before selecting the explanation best supported by your calculations. The investigation is complete when both systems have validated results or explicit bounded-failure records, probe geometry is auditable, the comparison is numerically reproducible, and the selected interpretation states its limitations. Stop at that point and do not broaden the compound set.

# Deliverables

Submit `report/results.json` conforming to the submission schema. Include independent method rationale, per-system geometry and frequency validation, ring-resolved and mean NICS values, sensitivity evidence, candidate explanations with discrimination evidence, comparison, and final scope-limited conclusion. If a calculation fails, use the bounded-failure branch with truthful partial evidence rather than invented values.
