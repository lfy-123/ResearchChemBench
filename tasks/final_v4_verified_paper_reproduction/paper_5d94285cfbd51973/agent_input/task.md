# Molecular properties and antifungal observations

## Scientific question

Do calculated molecular polarity and frontier electronic properties of AZ1–AZ10 explain the differences in their supplied Candida albicans MIC observations, and what predictive information do these ten compounds support?

## Input files

- `data/inputs/systems.json` defines the ten complete neutral singlet molecular graphs and atom maps. These are identities, not optimized structures.
- `data/inputs/mic_observations.json` gives the one-organism MIC column in microgram/mL, including tied values.
- `data/inputs/problem_facts.json` defines the measurement limits and the distinction between association, prediction and causal explanation.

## Scope

Use the full ten-compound series and the supplied assay. Calculate and compare gas-phase neutral-singlet molecular descriptors with a consistent physical definition; identify the conformations represented and justify additional environmental/state models. The MIC observations are already known, so the task concerns their computational explanation and an assessment of predictive information. No additional organism, docking target, new analogue, permeability or clinical mechanism is required.

## Required results

1. Report the positive frontier orbital gap E(LUMO)−E(HOMO), in eV, for each of AZ1–AZ10, with the occupied/virtual energies and molecular model needed to interpret it. Distinguish this orbital gap from an optical or fundamental gap.
2. Determine the within-series relationship of each of molecular dipole magnitude, HOMO energy and frontier gap to the measured activity. Give calculated dipoles in D and orbital energies in eV; define the activity transformation and its direction. Preserve all ten identities and assay ties, and report the strength and limitations of the relationships actually found.
3. Assess whether those relationships account for the MIC differences or support prediction. Ground the assessment in specific descriptor/MIC agreement or discordance or a justified validation analysis, separating descriptive association from predictive and causal claims. The analysis method and relevant additional checks are yours to choose.

## Author baseline for reproduction

The source computes the full ten-compound series using gas-phase B3LYP/6-31G(d) and Gaussian16 (SI p7); SI Table S12, p41, reports frontier energies, gaps, derived descriptors and dipoles. Reproduce the disclosed baseline or justify a comparable substitution. Main pp4–7 discuss frontier/polarity descriptors in relation to activity; the supplied activity column is from SI Table S1, p31. No source coordinates or full article are required as public inputs.

The printed gap formula uses E(HOMO)−E(LUMO), while tabulated gaps are positive E(LUMO)−E(HOMO). Source definitions μ=−η and ω=η/2 differ from conventional finite-difference chemical potential/electrophilicity; label any literal reproduction and use physically explicit definitions. Source formulas and causal interpretations are not correctness targets. No fixed regression model, leave-one-out protocol, permutation count or docking study is prescribed.

## Submission

Submit `report/results.json` and `report/report.md` following `submission_guide.md` and `submission_schema.json`. Support final answers with inspectable native calculations and reproducible analyses. Final scientific results total 100 points; research-process completion carries no independent points. Use supplied inputs and available tools; general scientific/software documentation is allowed. Private evaluator files, prior verification archives and undisclosed target-paper answers are not public resources.
