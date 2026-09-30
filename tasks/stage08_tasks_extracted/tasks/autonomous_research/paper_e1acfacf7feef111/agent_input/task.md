# Scientific objective

Perform an independent computational validation of the supplied [BiBr4]− fragment. Determine whether the optimized local structure and its low-frequency vibrational dynamics can be quantitatively compared with experimental local geometry and Raman observables. Report optimized Bi–Br distances, Br–Bi–Br angles, six assigned low-frequency Raman frequencies, and comparison metrics.


# Public inputs and scientific boundaries

The only molecular input is `data/inputs/bibr4_fragment.xyz`: atom 1 is Bi, atoms 2–5 are Br, Cartesian coordinates are in Å, total charge is −1 and multiplicity is 1. Treat it as an isolated fragment; do not add a host or solvent. The measured structural references are the four direct Bi–Br contacts from the supplied fragment (Bi1–Br1 through Bi1–Br4) and the six unique direct Br–Bi–Br angles among Br1–Br4; symmetry-generated contacts in the crystal table are outside this isolated five-atom object. The spectral references are six low-frequency Raman bands in cm−1. Crystal packing, organic species, water, periodic chains, band gaps and emission are outside scope.

# Required scientific validation/investigation

Select and document a defensible electronic-structure route. Optimize all atoms and establish a minimum by frequency analysis; report charge, multiplicity, method, basis/ECP, convergence and imaginary-frequency findings. Identify six distinct Bi/Br vibrational modes between 50 and 200 cm−1 and retain their identities and wavenumbers. Report each direct distance and angle with explicit atom-index identity and observable pairing, and each frequency with explicit mode identity and observed-band pairing; calculate distance MAE over four direct contacts, angle MAE over six direct angles and six-frequency RMSD, with units and explicit pairing. Completion requires a converged optimization, no unaccounted imaginary frequency, six identified modes, and all metrics, or a scientifically justified bounded-failure report. Stop at that point; if completion fails, report the failed condition, attempted coverage and limitation without inventing results.

# Deliverables

Submit `report/results.json` following the schema, including provenance, optimized structure, mode assignments, mappings, metrics, validation status and conclusion. Use the bounded-failure branch only when justified by documented attempted work.
