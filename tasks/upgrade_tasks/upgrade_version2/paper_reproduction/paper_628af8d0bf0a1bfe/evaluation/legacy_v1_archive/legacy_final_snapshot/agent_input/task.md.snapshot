# Scientific objective

Independently calculate and compare the magnetic antiaromaticity descriptor NICS(1.7)zz for systems 4a and 4c in `data/inputs/systems.json`. Report ring-resolved values for the two central monocyclic five-membered carbon rings and their arithmetic mean in ppm.

# Author-provided scientific guidance

The SI computational route uses M06-2X/6-31++G(d) geometries and 6-311+G(2d,p) shielding. The main-text shielding basis label differs. This is route guidance, not a requirement to match an undisclosed method; document the route used and the probe definition.

Test the authors' qualitative hypothesis that substituent electronics modulate the pentalene paratropic response, without assuming any numerical result, ordering, or winning computational protocol.

# Public inputs and scientific boundaries

Use the atom-mapped central pentalene carbon set for the common least-squares plane. For each probe report NICSzz = −nᵀσn, where n is the declared plane normal and σ the shielding tensor in the same coordinates. Report the two ring values and arithmetic mean. A coordinate rotation aligning n with z is equivalent; do not use an unrelated laboratory z component.

The public systems are fully identified by systematic name, formula, neutral formal charge, singlet multiplicity, and attachment definitions in `data/inputs/systems.json`; do not substitute a different protonation, connectivity, stereochemistry, or model compound. Use gas-phase equilibrium electronic structures. Solvent, crystal packing, finite-temperature and vibrational averaging, excited states, and kinetics are outside scope. Define the pentalene mean plane as the least-squares plane through the pentalene-core carbons. Define each ring centroid as the arithmetic mean of its five carbon nuclei. Place one ghost center 1.700 Å along a consistently chosen normal from each centroid and report the zz shielding-derived NICS value using the sign convention in the input file.

# Required scientific validation/investigation

Choose and justify an electronic-structure route independently. Optimize each neutral singlet and demonstrate a minimum with a frequency analysis or report bounded failure if that cannot be completed. Calculate both ring probes for both named systems, preserve ring identity, and show that the reported molecular value is the mean of the two ring values. Perform at least one meaningful method, basis, geometry, or orientation sensitivity check, or state why it was not feasible and identify the failed control and its effect on what was computed. The investigation is complete when both systems have validated ring-resolved results, the probe construction is reproducible, and the comparison and scientific interpretation are documented.

A complete outcome requires the requested scientific results and their validation evidence. If only part succeeds, use the existing failure/partial pathway and submit completed results plus the specific missing calculations and diagnostics; do not fabricate values. Extra exploratory attempts are allowed and do not invalidate completed main results. General limitations or stopping statements are optional, not scored deliverables.

# Deliverables

For an early or partial failure, a compact alternative submission is `status: bounded_failure` with `failure_report: {reason, missing_endpoint, completed_artifacts}`. Use nonempty reasons, identify the missing calculation, and list only artifacts that exist (the list may be empty if failure preceded computation). Include any available partial results; never fill unavailable scientific values. This branch is a valid submission, not successful completion.

Submit `report/results.json` conforming to the submission schema. Include per-system geometry status, frequency/minimum evidence, probe definitions, two ring values, mean value, sensitivity information, comparison, and a scientific conclusion. A bounded-failure branch is acceptable only when it identifies the failed system/step, attempted route, evidence produced, and specific failure cause; do not fabricate missing numbers.
