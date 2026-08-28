# paper_reproduction

## Scientific objective

Independently test the authors’ qualitative hypothesis that extending the heteroaryl pi system from pyridine to isoquinoline/quinoline can shift absorption and that transition intensity depends on heteroaryl connectivity. Determine, for 1a–d, validated ground-state structures and low-energy singlet absorption features: wavelength, energy, oscillator strength, orbital character, and comparison with toluene UV-vis bands.

## Public inputs and scientific boundaries

Use `data/inputs/1a.xyz`, `1b.xyz`, `1c.xyz`, and `1d.xyz`. Atom order and element symbols are authoritative Cartesian coordinates in Å. Each is neutral, closed-shell, charge 0, multiplicity 1. Treat the molecules as isolated; do not add solvent, ions, or crystal contacts unless separately labeled. The measured quantities are vertical singlet excitation energy, wavelength, oscillator strength, transition character, and comparison with experimental solution absorption maxima.

## Required scientific validation/investigation

For each named molecule, perform or justify a ground-state calculation and validate it with frequencies or a documented alternative minimum/failure. Inspect a low-energy singlet window and state how the selected principal feature is chosen using energy, oscillator strength, or a spectrum rule; preserve state identity. Report convergence, imaginary-frequency count, failures, and limitations. Completion requires four molecule-specific results or bounded failure records, a consistent comparison table, and a conclusion about the qualitative hypothesis. Stop after a validated ground state and sufficient low-energy singlet window establish the feature; if validation fails, stop retries after recording settings and an alternative.

## Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with per-molecule validation, selected transition, wavelength, energy, oscillator strength, orbital character, experimental comparison, an explicit four-molecule series comparison, overall conclusion, and limitations. Supporting logs may be under `report/`. Bounded failure must identify the affected molecule and distinguish unavailable values from computed values.
