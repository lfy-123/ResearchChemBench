# Scientific objective

Independently plan and perform a computational validation of the local [BiBr4]− fragment supplied in `data/inputs/bibr4_fragment.xyz`. The authors’ qualitative hypothesis is that a local isolated bromobismuthate model can reproduce local Bi(III) coordination and characteristic Bi–Br vibrational dynamics; test that hypothesis without assuming a method or result. Report optimized Bi–Br distances, Br–Bi–Br angles, six assigned low-frequency Raman frequencies, and quantitative comparison metrics.

# Public inputs and scientific boundaries

The only molecular input is the five-atom XYZ file: atom 1 is Bi and atoms 2–5 are Br, Cartesian coordinates are in Å, total charge is −1 and multiplicity is 1. Treat this as an isolated fragment. The measured structural references are the four direct Bi–Br contacts from the supplied fragment (Bi1–Br1 through Bi1–Br4) and the six unique direct Br–Bi–Br angles among Br1–Br4; symmetry-generated contacts in the crystal table are outside this isolated five-atom object. The spectral references are six low-frequency Raman bands in cm−1. Do not use the paper, SI, source PDFs, general web, or external databases. Crystal packing, the organic cation, water molecules, periodic chains, electronic band gaps and optical emission are outside scope.

# Required scientific validation/investigation

Choose and document a defensible electronic-structure route independently. Optimize all five atoms and establish that the returned structure is a minimum using a frequency calculation; report charge, multiplicity, method, basis/ECP, convergence and any spin or imaginary-frequency findings. Assign six distinct low-frequency modes in the 50–200 cm−1 region to the supplied Bi/Br atoms, retaining mode identity and computed wavenumber. Deduplicate only by explicit mode identity. Report each direct distance and angle with explicit atom-index identity and observable pairing, and each frequency with explicit mode identity and observed-band pairing; calculate MAE for the four direct distances, MAE for the six direct angles and RMSD for the six frequencies, with units and pairing rules. Completion requires a converged optimization, no unaccounted imaginary frequency, six identified modes, and all three metrics or a scientifically justified bounded-failure report. Stop when these conditions are met; if they cannot be met, stop after documenting the failed condition, attempted coverage and a limitation rather than fabricating values.

# Deliverables

Submit `report/results.json` following the schema. Include the computational provenance, optimized geometry, frequency assignments, mappings, metrics, validation status and a concise conclusion. A bounded-failure branch is allowed only with explicit reason and attempted work.
