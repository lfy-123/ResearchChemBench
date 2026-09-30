# Scientific objective

Determine whether the two supplied Ar-substituted triselenide structures can account for weak ^77Se features in the associated diselenide sample by calculating their relative energetics and three-site ^77Se chemical shifts, and state the strength and limits of the structural assignment.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that weak ^77Se signals in the diselenide sample arise from a minor Ar^F-substituted triselenide impurity, with the two supplied structures representing conformers that may exchange rapidly.

**Candidate route or mechanism.**
Treat the cis and trans triselenide structures as the focused candidate explanation for the minor spectral features, and assess whether their conformational energetics and selenium environments are compatible with that interpretation.

**Discriminating evidence.**
Use auditable geometry and stationarity validation, a common-zero relative-energy comparison, and site-resolved ^77Se chemical shifts with an explicit reference convention. Compare the resulting calculated features with the observed spectrum and use the comparison to distinguish support for the triselenide assignment from claims about a unique exchange mechanism.
# Public inputs and scientific boundaries

`data/inputs/cis.xyz` and `trans.xyz` are complete 25-atom neutral singlet C12F10Se3 structures; atom order is the identity key and the first three atoms are Se. `experimental_boundary.json` records observed ^77Se features of 422 and 816 ppm, approximately 2:1, in CDCl3 at 25 °C. Choose and justify the computational method and validation strategy from the supplied inputs and your scientific reasoning. The scored system is the isolated triselenide molecule; do not add a host or solvent.

# Required scientific validation/investigation

For each named structure, preserve identity/connectivity, optimize or justify the geometry, demonstrate stationarity for a minimum or explain a bounded alternative, identify each Se site by input atom index, and report relative energy with a common zero. Calculate three ^77Se shifts per conformer, state the reference convention, and compare them explicitly with the observed features. Generate and test your own explanations for the comparison. A calculation is complete when both structures and all requested observables have auditable outputs and limitations. If a scientifically justified bounded attempt cannot obtain an observable, report the affected object, missing observable, and diagnostic evidence in the bounded-failure branch; do not fabricate values. Stop after this fixed two-structure comparison; do not invent additional discovery candidates.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Include methods, per-conformer validation, per-Se shifts, relative energy, comparison, conclusion, and limitations. If a scientifically justified calculation fails, use the bounded-failure branch and document the affected object, missing observable, and diagnostic evidence.
