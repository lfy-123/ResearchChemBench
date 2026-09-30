# Scientific objective

Determine, for the four named neutral closed-shell N,O-bidentate difluoroboron complexes 1a–d, validated ground-state geometries and low-energy singlet electronic absorption features. Report wavelengths (nm), excitation energies, oscillator strengths, dominant orbital transition character, and how heteroaryl structure changes absorption position and intensity. Compare predictions with experimental UV-vis absorption maxima in toluene, treating solution-versus-molecule differences as a limitation.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors relate the absorption changes across complexes 1a–1d to extension and connectivity of the heteroaryl pi system. They also indicate that the lowest transition of the 3-isoquinolyl derivative can be weak, so transition intensity and orbital character should be considered alongside wavelength.

**Candidate route or mechanism.**
Compare the four supplied neutral difluoroboron complexes by examining how the pyridyl, isoquinolyl, and quinolyl connectivities alter the conjugated electronic structure. Treat a red or blue shift and a weak lowest transition as competing, testable explanations for the observed spectral differences rather than as predetermined results.

**Discriminating evidence.**
Use validated ground-state structures, a low-energy singlet state window, oscillator strengths, dominant orbital or transition-density character, and a consistent comparison with the solution absorption bands to distinguish changes in transition energy from changes in intensity.

# Public inputs and scientific boundaries

Use `data/inputs/1a.xyz`, `1b.xyz`, `1c.xyz`, and `1d.xyz`. Each XYZ is a uniquely labeled SI Cartesian geometry in Å; atom order and element symbols are authoritative. The molecules are neutral and singlet (charge 0, multiplicity 1), with connectivity and protonation encoded by the supplied atoms. They are isolated molecules: do not add solvent molecules, counterions, salts, or crystal contacts unless separately labeled. The measured quantities are vertical singlet excitation energy, wavelength, oscillator strength, transition character, and experimental comparison.

# Required scientific validation/investigation

For every molecule, generate at least one reproducible electronic-structure calculation from the supplied geometry, optimize or justify the ground state, and validate it with frequencies or an explicitly documented alternative minimum/failed-validation path. Inspect enough low-lying singlet states to identify the principal calculated feature; state the assignment rule and retain state identity. Report convergence, imaginary-frequency count, failures, and limitations. Completion requires four molecule-specific results or bounded failure records, all requested observables, a consistent comparison, and a conclusion. Stop after each molecule has a validated ground state and a sufficient low-energy singlet window; if validation fails, stop retries after recording settings and a scientifically justified alternative.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus supporting logs under `report/` as needed. Preserve molecule identity and include validation, selected feature, experimental comparison, an explicit four-molecule series comparison, overall conclusion, and limitations. Bounded failure must truthfully distinguish unavailable values from computed values.
