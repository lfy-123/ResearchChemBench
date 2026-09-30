# Scientific objective

Determine, for the isolated neutral singlet thione tautomer of compound 7a (4-(((5-(p-chlorophenoxy)-3-methyl-1-phenyl-1H-pyrazol-4-yl)methylene)amino)-5-methyl-4H-1,2,4-triazole-3-thione), how accurately independently chosen electronic-structure models reproduce the experimentally determined molecular geometry. Compare at least two defensible models and explain what the comparison supports within the stated physical boundary.

# Public inputs and scientific boundaries

Use `data/inputs/molecule.json` as the complete molecular identity: its mapped thione SMILES (source-label atom mapping; neutral thione C=S connectivity), formula, neutral charge and singlet multiplicity are authoritative. Use `data/inputs/atom_map.json` for the exact 13 bond, 23 angle and 11 torsion selectors (the repeated source angle is listed once). Generate starting 3D coordinates; crystal coordinates and author-computed geometry columns are withheld; pure SCXRD measurements are supplied in `data/inputs/experimental_geometry.csv`. The object is an isolated molecule, not a periodic crystal or solvated complex. Report all method, basis, dispersion, environment, optimization and frequency choices. Do not use the paper, SI or general web during the investigation.

# Required scientific validation/investigation

Choose and justify at least two models, then optimize the same public molecule independently with each. Verify connectivity, charge, multiplicity and thione tautomer; establish a genuine local minimum with a frequency/Hessian check or an explicit alternative stationarity test. Map every source atom label to submitted atoms, deduplicate equivalent records, and extract all public bond lengths (Å), angles (degrees), and signed torsions (degrees). Compare models using MAE and RMSE against the supplied experimental geometry table; use the minimum absolute circular difference for torsions. Completion requires converged structures, validation evidence, all extractable rows or documented row-specific failure, and a coverage/limitation statement. Stop after the planned model comparison and sensitivity statement; do not invent an unsupported discovery mechanism.

Compute MAE and RMSE separately for bond lengths, angles and torsions on the 13/23/11 unique rows. Use the minimum absolute circular difference for torsions. Report row coverage and preserve missing rows as failures, not zero error. Do not combine Angstrom and degree errors into an undeclared overall score or invent weights to favor a model. If the per-kind comparisons do not support an unambiguous overall preference, report the mixed/undetermined result. Model or row failures may use null metrics with explicit reasons and counts; complete results require both validated models and every required comparison.

# Deliverables

Submit `report/results.json` conforming to the schema. Include the independent model rationale and parameters, coordinates or coordinate artifact paths, convergence and stationarity evidence, atom mapping, per-row observables, aggregate MAE/RMSE, conclusion, and limitations. A bounded failure must identify failed models/rows and evidence produced rather than fabricating values.
