# Scientific objective

Independently calculate and compare the magnetic antiaromaticity descriptor NICS(1.7)zz for systems 4a and 4c in `data/inputs/systems.json`. Test the authors' qualitative hypothesis that substituent electronics modulate the pentalene paratropic response, without assuming any numerical result, ordering, or winning computational protocol. Report ring-resolved values for the two central monocyclic five-membered carbon rings and their arithmetic mean in ppm.

# Public inputs and scientific boundaries

The public systems are fully identified by systematic name, formula, neutral formal charge, singlet multiplicity, and attachment definitions in `data/inputs/systems.json`; do not substitute a different protonation, connectivity, stereochemistry, or model compound. Use gas-phase equilibrium electronic structures. Solvent, crystal packing, finite-temperature and vibrational averaging, excited states, and kinetics are outside scope. Define the pentalene mean plane as the least-squares plane through the pentalene-core carbons. Define each ring centroid as the arithmetic mean of its five carbon nuclei. Place one ghost center 1.700 Å along a consistently chosen normal from each centroid and report the zz shielding-derived NICS value using the sign convention in the input file.

# Required scientific validation/investigation

Choose and justify an electronic-structure route independently. Optimize each neutral singlet and demonstrate a minimum with a frequency analysis or report bounded failure if that cannot be completed. Calculate both ring probes for both named systems, preserve ring identity, and show that the reported molecular value is the mean of the two ring values. Perform at least one meaningful method, basis, geometry, or orientation sensitivity check, or state why it was not feasible and quantify the limitation. The investigation is complete when both systems have either validated ring-resolved results or an explicit bounded-failure record, the probe construction is reproducible, and the comparison and scientific interpretation are documented. Stop after this contract is satisfied; do not expand to additional compounds unless used only as clearly labeled context.

# Deliverables

Submit `report/results.json` conforming to the submission schema. Include per-system geometry status, frequency/minimum evidence, probe definitions, two ring values, mean value, sensitivity information, comparison, and a scope-limited conclusion. A bounded-failure branch is acceptable only when it identifies the failed system/step, attempted route, evidence produced, and scientific limitation; do not fabricate missing numbers.
