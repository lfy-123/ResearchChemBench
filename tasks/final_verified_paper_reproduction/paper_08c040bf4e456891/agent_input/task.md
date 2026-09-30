# Scientific objective

Independently test the authors' qualitative proposal that CHClF2+ loses chlorine by comparatively simple C–Cl cleavage, while F loss requires a more involved rearranging cation path. Compute the adiabatic first ionization energy and appearance energies for CHF2+ + neutral Cl and CHFCl+ + neutral F. Report electronic energies in eV relative to optimized neutral CHClF2; identify whether each path is a simple coordinate scan or a multidimensional minimum-energy path based on your own calculations.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the two halogen-loss channels differ in their structural requirements: chlorine loss can proceed by simple C–Cl cleavage, whereas fluorine loss involves rearrangement of the cation.

**Candidate route or mechanism.**
For chlorine loss, consider C–Cl separation with relaxation of the remaining structure. For fluorine loss, consider a pathway in which chlorine motion maintains C–Cl bonding while C–F bonding weakens and fluorine separates as a neutral atom. The authors use relaxed scans to explore candidate structures and a nudged elastic band search to examine the full-coordinate pathway for this proposed rearrangement.

**Discriminating evidence.**
The authors examine relaxed-scan and minimum-energy-path energy profiles, structural changes and evolving fragment charges to distinguish the proposed descriptions. Optimized parent-state electronic energies and refined single-point energies establish ionization and dissociation energetics; changes in C–Cl and C–F bonding along the path connect these energetics to the proposed mechanism.

# Public inputs and scientific boundaries

The system is isolated gas-phase CHClF2, connectivity FC(F)Cl with one H bonded to C, atom order C,H,Cl,F1,F2, supplied in `data/inputs/system.json` and the XYZ starter files. Use charge 0/multiplicity 1 for neutral CHClF2 and charge +1/multiplicity 2 for CHClF2+. The two fixed channels are (i) CHF2+ + Cl(2P) and (ii) CHFCl+ + F(2P), with products separated far enough that interaction is negligible. The reference zero is the optimized neutral electronic energy. Choose and disclose computational methods; do not assume paper software or model chemistry. Do not score dication chemistry. Experimental appearance energies are context only and must not be substituted for computed values.

# Required scientific validation/investigation

Optimize the neutral and monocation, verify charge, multiplicity, connectivity and genuine stationary-point convergence, and calculate the adiabatic ionization energy from their electronic energies. For each named channel, generate at least one explicit reactant-to-separated-products path, retain its endpoint structures and per-image/scan energies, and demonstrate that the endpoint has the stated fragment identities and conserved total charge and electron count. Use a relaxed one-coordinate treatment only if it remains continuous and chemically valid; otherwise use a multidimensional path method and explain why. Repeat at least one key energy with a second reasonable method or basis and report the sensitivity. A calculation is complete when both channel endpoints are separated/converged, all three requested energies are reported with units and method provenance, and validation evidence is attached.

A continuous and chemically valid relaxed-coordinate path is admissible when the submitted endpoint, separation, charge and convergence checks support it. Full multidimensional minimum-energy-path proof is not required. Distinguish a validated path from a globally minimal path; state explicitly any rearrangement or mechanism not established by your trajectory. The numerical energies alone do not establish path validity.

# Deliverables

Submit `report/results.json` plus referenced geometry/path files. The JSON must state completion status, method, neutral/cation energies, AIE, per-channel endpoint identities, dissociation energies, appearance energies, validation observations, sensitivity result, and a conclusion comparing the two channels to the qualitative author hypothesis. Include enough candidate/image identity to make every claim auditable. Scientific completion requires validated results for both channels and every requested energy and comparison.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
