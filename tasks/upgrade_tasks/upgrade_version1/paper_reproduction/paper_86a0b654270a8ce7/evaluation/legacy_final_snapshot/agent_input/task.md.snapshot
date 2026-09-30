# Scientific objective

Determine whether the two supplied neutral singlet Ir(III)–salen-NHC isomers have different solution-phase Gibbs free energies at 339 K, and quantify the resulting ΔΔG(1–2) and Boltzmann population ratio [2]/[1]. The authors' qualitative hypothesis is that intramolecular π–π stacking helps stabilize isomer 2; independently plan and execute calculations that test this thermodynamic hypothesis. Do not assume any numerical result or preferred isomer before calculation.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that isomer 2 is thermodynamically favored and interpret intramolecular π–π stacking involving its ligand framework as a contribution to its stabilization. This is a hypothesis to test against the computed thermochemistry and structural evidence.

**Candidate route or mechanism.**
Focus comparative analysis on the two constitutional/coordination arrangements, including whether the arrangement assigned to isomer 2 permits a favorable intramolecular π–π contact absent or less favorable in isomer 1. Treat this as a candidate structural explanation rather than a predetermined outcome.

**Discriminating evidence.**
Use optimized geometries, vibrational confirmation of minima, solution-phase Gibbs energies, and a Boltzmann ratio at 339 K to distinguish the thermodynamic preference. Structural inspection of relevant aromatic contacts can assess whether the proposed stacking interpretation is consistent with the calculated endpoint structures; sensitivity to the chosen computational model should qualify the conclusion.

# Public inputs and scientific boundaries

`data/inputs/complex_1.xyz` and `complex_2.xyz` are the complete Cartesian geometries for the two named isomers, with element symbols and Å coordinates. Each is neutral (charge 0) and closed-shell singlet (multiplicity 1). Use the molecules as isolated complexes with implicit THF solvent at 339 K. The requested endpoint is the molecular Gibbs free energy for each labeled input and the difference ΔΔG(1–2) = G(1) − G(2), in kJ mol−1, plus [2]/[1]. Do not add a crystal lattice, counterion, explicit solvent, or kinetic model.

This is a fixed-structure property track: the supplied coordinates are public inputs for the named property comparison, not a scored structure discovery answer. Do not claim that the input geometry itself was rediscovered; report any optimization or conformer search separately.

Report the computed two-state free energies and population ratio for THF at 339 K. Comparison with the experimental mixture is performed privately by the evaluator; the submitted calculation does not need to supply or guess experimental numbers.

# Required scientific validation/investigation

Choose and document a defensible computational protocol, including electronic structure method, basis/ECP treatment, solvation, thermal standard state, and software/version. Optimize each labeled input and establish whether the resulting structure is a minimum using vibrational information; report imaginary modes or a bounded failure if a minimum cannot be established. Obtain Gibbs free energies at 339 K, convert units consistently, and independently recompute [2]/[1] from ΔΔG using the stated gas constant and temperature. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result. Report any uncertainty estimate or method-sensitivity comparison with its computational evidence.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include per-isomer method and minimum-validation records, G values when available, ΔΔG, ratio, equations/constants, and a conclusion about the thermodynamic hypothesis. A bounded-failure branch is allowed only with concrete failure details and the attempted-system record; do not invent missing numerical values.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
