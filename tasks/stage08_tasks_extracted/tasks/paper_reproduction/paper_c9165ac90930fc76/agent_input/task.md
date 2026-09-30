# Scientific objective

Determine, within a reproducible finite molecular-complex investigation, whether association of an HDC-containing ligand package is selective for SnI2 versus PbI2 relative to FAI, and quantify the binding energies for the six BX2/ligand-family combinations. If the computed evidence does not support selectivity, explain the alternative conclusion rather than forcing a positive claim.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that HDC coordinates preferentially with Sn(II)-iodide precursor species relative to Pb(II)-iodide species. Their interpretation concerns molecular-complex association and its possible relationship to differing Sn/Pb crystallization behavior.

**Candidate route or mechanism.**
The proposed comparison includes BX2 (B = Sn or Pb) associated with FAI, HDC, or an HDC–DMSO package. The authors consider stronger HDC-containing association with Sn, including coordination involving the HDC–DMSO package, as the candidate explanation for selectivity.

**Discriminating evidence.**
Test the proposal by comparing the six molecular-complex binding energies under the declared convention: SnI2–FAI, SnI2–HDC, SnI2–HDC–DMSO and the corresponding PbI2 complexes. Converged complex and isolated-fragment energies, independent structural checks, and comparisons of matched ligand packages across metals provide the evidence for or against the proposed selectivity.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. It defines SnI2 and PbI2, FAI, HDC, DMSO, the three ligand families, stoichiometry, charge/multiplicity, binding-energy convention, and finite-cluster scope. No author route, preferred mechanism, result, ranking, selected structure, or paper method is provided. You may use controlled chemical databases only to verify the supplied component identities, recording stable IDs and transformations; do not use the paper/SI or general literature.

# Required scientific validation/investigation

Propose plausible coordination/protonation models for each family and discriminate them by a bounded conformer/structure search. Define your generation rules before searching, preserve stoichiometry and atom mapping, deduplicate candidates, and advance only SCF- and geometry-converged local minima. Validate the selected candidate in every system with an independent start or sensitivity check, and compute isolated fragments consistently. Completion requires all six validated binding energies or a bounded-failure account naming missing systems and causes. Stop when your predeclared generation rules are exhausted or new starts cease to produce distinct minima; report search coverage and limitations. Conclusions must be restricted to the modeled species and search scope.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include proposed models, candidate identities and validation context, method and settings, energies and binding energies in eV, comparisons by metal and ligand family, the supported scientific conclusion, and limitations or bounded failure details.
