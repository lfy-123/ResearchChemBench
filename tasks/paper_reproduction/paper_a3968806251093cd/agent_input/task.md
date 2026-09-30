# Scientific objective

Study the isolated neutral singlet thione tautomer of compound 7a, 4-(((5-(p-chlorophenoxy)-3-methyl-1-phenyl-1H-pyrazol-4-yl)methylene)amino)-5-methyl-4H-1,2,4-triazole-3-thione. Compare at least two electronic-structure models, including one conventional hybrid and one long-range-corrected/range-separated model.

# Author-provided scientific guidance

Independently plan and execute calculations that test the authors' qualitative hypothesis that a DFT geometry can reproduce the experimentally determined molecular geometry and that a range-separated hybrid may improve agreement.

# Public inputs and scientific boundaries

Use `data/inputs/molecule.json` as the complete molecular identity: its mapped thione SMILES (source-label atom mapping; neutral thione C=S connectivity), formula, neutral charge and singlet multiplicity are authoritative. Use `data/inputs/atom_map.json` for the exact 13 bond, 23 angle and 11 torsion selectors (the repeated source angle is listed once). Generate starting 3D coordinates; crystal coordinates and author-computed geometry columns are withheld; pure SCXRD measurements are supplied in `data/inputs/experimental_geometry.csv`. The object is an isolated molecule, not a periodic crystal or solvated complex. Report all method, basis, dispersion, environment, optimization and frequency choices. Do not use the paper, SI or general web during the investigation.

# Required scientific validation/investigation

For each model, verify that the optimized structure preserves the public connectivity, charge, multiplicity and thione tautomer. Establish a genuine local minimum with a frequency/Hessian check, or provide an explicit alternative stationarity test and limitation. Map every source atom label to an atom in the submitted coordinates, deduplicate equivalent records, and extract all public bond lengths (Å), angles (degrees), and signed torsions (degrees). Compare models using MAE and RMSE against the supplied experimental geometry table; use the minimum absolute circular difference for torsions. A complete calculation requires both models to have converged, validated structures and all 47 required rows per model; missing rows or failed models must be reported as bounded_failure, not as complete. Stop after the two-model comparison and a documented sensitivity/coverage statement; do not claim more than the computed evidence supports.

Compute MAE and RMSE separately for bond lengths, angles and torsions on the 13/23/11 unique rows. Use the minimum absolute circular difference for torsions. Report row coverage and preserve missing rows as failures, not zero error. Do not combine Angstrom and degree errors into an undeclared overall score or invent weights to favor a model. If the per-kind comparisons do not support an unambiguous overall preference, report the mixed/undetermined result. Model or row failures may use null metrics with explicit reasons and counts; complete results require both validated models and every required comparison.

For the primary reproduction comparison use B3LYP and CAM-B3LYP, each with 6-311+G(d,p), for the isolated gas-phase neutral singlet thione. Other methods are supplementary, not replacements for this primary pair. No model ranking is supplied.

# Deliverables

Submit `report/results.json` conforming to the schema. Include model identities and parameters, coordinates or coordinate artifact paths, convergence and stationarity evidence, atom mapping, per-row observables, aggregate MAE/RMSE, model comparison, limitations, and a truthful completion status. A bounded failure must identify the failed model/rows and the evidence produced rather than fabricating values.
