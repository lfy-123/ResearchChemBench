# Scientific question

What electronic-state explanation accounts for the absorption differences among the four neutral boron chelates 1a–1d in toluene, including the two distinct absorption features of 1c?

# Input files

- `data/inputs/objects.json` gives complete atom-indexed chemical graphs, charges and starting multiplicities. 1a is C11H8BF2NO; 1b–1d are distinct C15H10BF2NO constitutional isomers. Generate appropriate geometries while preserving those identities.
- `data/inputs/observations.json` gives measured absorption maxima and extinction coefficients in toluene. These are observations to explain; their repetition is not a prediction or a new calculation.

# Scope

Study molecular absorption of these four compounds. Define each computed electronic state, environment and observable. Report excitation energies in eV or wavelengths in nm and transition strengths with their definitions. A vertical transition, frontier orbital gap and broadened absorption maximum are different quantities. Relate the chosen molecular model to the measured solution, with explicit solvent assumptions. No emission efficiency, crystal polymorphism, white-light emission or device performance is requested.

Choose and justify your electronic-structure methods and physical models independently.


# Required results

1. Assign the lower-energy absorption feature of each of 1a, 1b, 1c and 1d to physical electronic states. Support each assignment with computed energies, intensities and state character.
2. Explain the electronic relationship between molecular connectivity and the observed shifts of 1b–1d relative to 1a. Establish what the computed comparison supports and its limits.
3. Explain the intensity of the lower-energy 1c feature relative to those of 1b and 1d using calculated transition properties.
4. Assign the stronger higher-energy 1c feature and explain how its intensity relates to the lower-energy feature. Separate physical state correspondence from root numbering and experimental maxima from computed transitions.

# Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link each conclusion and quantitative result to actual inputs, native outputs and reproducible analyses. Structures, state checks and validation establish evidence quality; completing a workflow earns no separate points. Consult `resources.md` for available resources.
