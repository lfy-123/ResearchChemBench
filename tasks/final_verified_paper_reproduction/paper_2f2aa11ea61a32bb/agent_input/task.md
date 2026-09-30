# Scientific objective

Independently test the authors’ qualitative hypothesis that extending the heteroaryl pi system from pyridine to isoquinoline/quinoline can shift absorption and that transition intensity depends on heteroaryl connectivity. Determine, for 1a–d, validated ground-state structures and low-energy singlet absorption features: wavelength, energy, oscillator strength, orbital character, and comparison with toluene UV-vis bands.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors relate the absorption changes across complexes 1a–1d to extension and connectivity of the heteroaryl pi system. They also indicate that the lowest transition of the 3-isoquinolyl derivative can be weak, so transition intensity and orbital character should be considered alongside wavelength.

**Candidate route or mechanism.**
Compare the four supplied neutral difluoroboron complexes by examining how the pyridyl, isoquinolyl, and quinolyl connectivities alter the conjugated electronic structure. Treat a red or blue shift and a weak lowest transition as competing, testable explanations for the observed spectral differences rather than as predetermined results.

**Discriminating evidence.**
Use validated ground-state structures, a low-energy singlet state window, oscillator strengths, dominant orbital or transition-density character, and a consistent comparison with the solution absorption bands to distinguish changes in transition energy from changes in intensity.

# Public inputs and scientific boundaries

Use `data/inputs/1a.xyz`, `1b.xyz`, `1c.xyz`, and `1d.xyz`. Atom order and element symbols are authoritative Cartesian coordinates in Å. Each is neutral, closed-shell, charge 0, multiplicity 1. Treat the molecules as isolated; do not add solvent, ions, or crystal contacts unless separately labeled. The measured quantities are vertical singlet excitation energy, wavelength, oscillator strength, transition character, and comparison with experimental solution absorption maxima.

This is a fixed-structure property track: the supplied coordinates are public inputs for the named property comparison, not a scored structure discovery answer. Do not claim that the input geometry itself was rediscovered; report any optimization or conformer search separately.

Experimental comparison inputs are in data/inputs/experimental_absorption.json. The primary experimental features are the lower-energy toluene absorption bands for 1a-1d, not automatically each spectrum's strongest peak. Select the corresponding calculated low-energy transition using state energy, oscillator strength and orbital character, without selecting by closeness to an expected value. For 1c, analyze the separate stronger higher-energy band as a distinct feature and label it separately; do not swap it for the primary low-energy band.

# Required scientific validation/investigation

For each named molecule, perform or justify a ground-state calculation and validate it with frequencies or a documented alternative minimum/failure. Inspect a low-energy singlet window and state how the selected principal feature is chosen using energy, oscillator strength, or a spectrum rule; preserve state identity. Report convergence, imaginary-frequency count, failures. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with per-molecule validation, selected transition, wavelength, energy, oscillator strength, orbital character, experimental comparison, an explicit four-molecule series comparison, overall conclusion. Supporting logs may be under `report/`. Bounded failure must identify the affected molecule and distinguish unavailable values from computed values.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
