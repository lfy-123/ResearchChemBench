# Methoxy substitution and epoxy-fragment polarity

## Scientific question

How does ortho-methoxy substitution change the permanent polarity of the supplied EPI1/EPI2 fragments, what molecular features explain that change, and what does it imply for interpreting the supplied resin dielectric observations?

## Input files

- `data/inputs/systems.json`: full neutral-singlet molecular graphs and a common representative stereochemistry; these do not prescribe a three-dimensional conformation.
- `data/inputs/observations.json`: qualitative dielectric and temperature-dependent FTIR observations for cured materials. These are given context, not isolated-molecule dipole measurements.

## Scope

Study these full fragments under explicitly matched conditions. Distinguish a local conformation, a sampled population and a cured material. State environment and, for population averages, temperature and weighting. Quantitative polymer-network dielectric constants, water uptake and mechanical properties are outside scope.

## Required results

1. Quantify the polarity difference between EPI2 and EPI1 for your declared matched structures or population, including its sign, magnitude and scope. Define the observable and units; distinguish moment magnitudes and squared-moment averages.
2. Explain the computed effect using molecular and electronic evidence, and state how configuration affects the reach of that explanation.
3. Determine what the molecular result supports about the supplied dielectric trend, using the appropriate response statistic and distinguishing molecular evidence from bulk behavior.

## Submission

Submit `report/results.json` and `report/report.md` following the supplied schema and guide, with linked native calculations and analyses. Only final scientific conclusions receive points. Choose methods independently within the mode's scope. Use public inputs and available runtime tools; do not access private evaluator files, verification archives or the other mode's guidance. General scientific/software documentation is allowed.
