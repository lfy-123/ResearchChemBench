# Molecular optical response of PBNA

## Scientific question

What molecular electronic-state and relaxation account explains the supplied dilute-solution absorption and fluorescence of PBNA, and how far does the chosen molecular representation support that experimental interpretation?

## Input files

- `data/inputs/objects.json`: atom-indexed graph of experimental N-hexyl PBNA, C34H42B2N2, neutral singlet, 80 atoms.
- `data/inputs/identity_provenance.json`: identity and representation notes.
- `data/inputs/observations.json`: absorption bands, onset, emission bands and excitation wavelength in 10^-5 M dichloromethane at room temperature. These are given observations to explain.

## Scope

Study PBNA alone. Use the full experimental molecule or an explicitly mapped, chemically justified approximation. Identify retained atoms, changed substituents and caps, and justify the applicability of each optical claim. No optimized conformation or preferred electronic-state assignment is supplied. Distinguish orbital eigenvalues, vertical absorption, relaxed emission, equilibrium endpoint energies and measured spectral features. AIE, aggregates, crystal packing, two-photon cross sections and other substituted BN-anthracenes are outside scope; gaps and oscillator strengths alone do not establish photophysical rates.

## Author baseline for reproduction

`data/inputs/author_model.json` provides the N-methyl computational approximation C24H22B2N2 (50 atoms); `data/inputs/author_model_mapping.json` maps it to the experimental N-hexyl identity. The authors used Gaussian09 D01 with gas-phase B3LYP/6-31G(d) geometry and energy calculations (SI pp19–20, Tables S11–S12). Main Fig.3 reports HOMO −5.62 eV and LUMO −1.71 eV, with both orbitals concentrated on the BN-anthracene scaffold. Compute and report these two model-specific eigenvalues as part of the reproduction, keeping them separate from optical transitions. Reproduce this disclosed baseline or justify a physically comparable substitution; actual calculations are required, and copying targets earns no credit.

Main Table1/Fig.4 supplies the solution observations; the authors' localized-excitation/limited-charge-transfer interpretation from solvent behavior is a hypothesis to assess with physical evidence. Source use of the N-methyl approximation does not independently validate transfer to N-hexyl PBNA. Distinguish the published ground-state baseline from additional solution excited-state and relaxation analyses used to answer this task. No author motion/control matrix is prescribed.

## Required results

1. Give a quantitative molecular explanation of absorption, identifying the relevant computed transitions and state character and relating them to the supplied bands and onset without conflating observables.
2. Explain fluorescence and its relation to absorption using quantitative evidence for the relevant emitting state and relaxation or equivalent physical description.
3. Establish how the absorption account applies to the experimental N-hexyl molecule, with evidence for the role of retained and changed groups.
4. Establish the corresponding applicability for relaxed emission and identify the optical features that the evidence does and does not resolve. Absorption agreement alone does not settle this issue.

## Submission

Submit `report/results.json` and `report/report.md` following `submission_schema.json` and `submission_guide.md`. Link actual native calculations, model identities and reproducible analyses. Methods and supporting comparisons are yours to choose within this mode's baseline. Only final results earn points; no fixed calculation matrix is required. Use public inputs, available tools and general documentation. Do not access private evaluator files or verification archives.
