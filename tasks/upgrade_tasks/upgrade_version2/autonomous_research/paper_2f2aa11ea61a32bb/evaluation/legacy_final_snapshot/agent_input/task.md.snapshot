# Scientific objective

Determine, for the four named neutral closed-shell N,O-bidentate difluoroboron complexes 1a–d, validated ground-state geometries and low-energy singlet electronic absorption features. Report wavelengths (nm), excitation energies, oscillator strengths, dominant orbital transition character, and how heteroaryl structure changes absorption position and intensity. Compare predictions with experimental UV-vis absorption maxima in toluene using the supplied experimental band definitions.

# Public inputs and scientific boundaries

Use `data/inputs/1a.xyz`, `1b.xyz`, `1c.xyz`, and `1d.xyz`. Each XYZ is a uniquely labeled SI Cartesian geometry in Å; atom order and element symbols are authoritative. The molecules are neutral and singlet (charge 0, multiplicity 1), with connectivity and protonation encoded by the supplied atoms. They are isolated molecules: do not add solvent molecules, counterions, salts, or crystal contacts unless separately labeled. The measured quantities are vertical singlet excitation energy, wavelength, oscillator strength, transition character, and experimental comparison.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

This is a fixed-structure property track: the supplied coordinates are public inputs for the named property comparison, not a scored structure discovery answer. Do not claim that the input geometry itself was rediscovered; report any optimization or conformer search separately.

Experimental comparison inputs are in data/inputs/experimental_absorption.json. The primary experimental features are the lower-energy toluene absorption bands for 1a-1d, not automatically each spectrum's strongest peak. Select the corresponding calculated low-energy transition using state energy, oscillator strength and orbital character, without selecting by closeness to an expected value. For 1c, analyze the separate stronger higher-energy band as a distinct feature and label it separately; do not swap it for the primary low-energy band.

# Required scientific validation/investigation

For every molecule, generate at least one reproducible electronic-structure calculation from the supplied geometry, optimize or justify the ground state, and validate it with frequencies or an explicitly documented alternative minimum/failed-validation path. Inspect enough low-lying singlet states to identify the principal calculated feature; state the assignment rule and retain state identity. Report convergence, imaginary-frequency count, failures. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus supporting logs under `report/` as needed. Preserve molecule identity and include validation, selected feature, experimental comparison, an explicit four-molecule series comparison, overall conclusion. Bounded failure must truthfully distinguish unavailable values from computed values.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
