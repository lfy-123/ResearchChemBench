# Scientific objective

Determine the site-resolved unpaired-electron localization in the isolated neutral syringol phenoxy radical supplied in `data/inputs/syringol_phenoxy_radical.xyz`. Test the authors' qualitative hypothesis that the para ring carbon C4 is the dominant carbon-centered radical site and therefore a plausible site for C4–C4′ coupling. This task scores the independently obtained electronic-structure evidence, not a product structure or a coupling barrier.

# Public inputs and scientific boundaries

The XYZ file contains 20 atoms for neutral C8H9O3 2,6-dimethoxyphenoxy radical, charge 0, multiplicity 2. Its atom order defines the identity: atom 1 is phenoxy O1; atoms 2–7 are ring carbons C2, C3, C4, C5, C6 and C1 in that cyclic order, with O1 bonded to C1 (atom 7); atoms 8 and 9 are methoxy oxygens bonded to C2 (atom 2) and C6 (atom 6), and atoms 10 and 11 are their methyl carbons; atoms 12–20 are the nine hydrogens. Report results for O1 (atom 1), C2 (atom 2), C6 (atom 6), and C4 (atom 4), preserving these selectors. The physical boundary is an isolated gas-phase neutral doublet radical. Do not claim that this calculation directly supplies an enzyme effect, solvent effect, bimolecular transition state, reaction rate, or electrochemical capacity. You may generate conformers and choose a computational model, but must state software, functional, basis, charge, multiplicity, population scheme and all relevant convergence settings.

# Required scientific validation/investigation

Optimize the supplied radical or otherwise obtain a documented stationary structure, then calculate atom-resolved spin populations for all four named sites. Validate SCF and geometry convergence, verify the atom map survived, and use a stationary-point check or another scientifically justified structural validation. Check whether symmetry-equivalent C2 and C6 agree within the uncertainty you report; if not, investigate or explain the inequivalence. Completion requires a reproducible calculation record, a populated table for all four sites, and a comparison of site ordering. Stop when the chosen structure and population analysis pass the stated validation checks; if a check cannot be completed, stop and report bounded failure with the failed check, attempted coverage, evidence and limitations rather than inventing values or an ordering.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method and validation provenance, the four site populations with units/convention, any uncertainty or comparison basis, the site ordering, and a conclusion about whether the computed evidence supports C4-dominant localization and the limited coupling interpretation. Include bounded-failure details when applicable.
