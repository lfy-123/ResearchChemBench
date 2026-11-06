# Molecular optical response of PBNA

## Scientific question

What molecular electronic-state and relaxation account explains the supplied dilute-solution absorption and fluorescence of PBNA, and how far does the chosen molecular representation support that experimental interpretation?

## Input files

- `data/inputs/objects.json`: atom-indexed graph of experimental N-hexyl PBNA, C34H42B2N2, neutral singlet, 80 atoms.
- `data/inputs/identity_provenance.json`: identity and representation notes.
- `data/inputs/observations.json`: absorption bands, onset, emission bands and excitation wavelength in 10^-5 M dichloromethane at room temperature. These are given observations to explain.

## Scope

Study PBNA alone. Use the full experimental molecule or an explicitly mapped, chemically justified approximation. Identify retained atoms, changed substituents and caps, and justify the applicability of each optical claim. No optimized conformation or preferred electronic-state assignment is supplied. Distinguish orbital eigenvalues, vertical absorption, relaxed emission, equilibrium endpoint energies and measured spectral features. AIE, aggregates, crystal packing, two-photon cross sections and other substituted BN-anthracenes are outside scope; gaps and oscillator strengths alone do not establish photophysical rates.

## Required results

1. Give a quantitative molecular explanation of absorption, identifying the relevant computed transitions and state character and relating them to the supplied bands and onset without conflating observables.
2. Explain fluorescence and its relation to absorption using quantitative evidence for the relevant emitting state and relaxation or equivalent physical description.
3. Establish how the absorption account applies to the experimental N-hexyl molecule, with evidence for the role of retained and changed groups.
4. Establish the corresponding applicability for relaxed emission and identify the optical features that the evidence does and does not resolve. Absorption agreement alone does not settle this issue.

## Submission

Submit `report/results.json` and `report/report.md` following `submission_schema.json` and `submission_guide.md`. Link actual native calculations, model identities and reproducible analyses. Methods and supporting comparisons are yours to choose within the stated scope. Only final results earn points; no fixed calculation matrix is required. Use public inputs, available tools and general documentation. Do not access private evaluator files or verification archives.
