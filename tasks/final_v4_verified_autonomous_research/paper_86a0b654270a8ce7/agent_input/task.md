# Relative stability of two iridium coordination isomers

## Scientific question

What relative Gibbs stability and molecular explanation are supported for the two supplied Ir–salen–NHC coordination isomers in THF at 339 K? Determine the resolution of the preference and the thermodynamic implications that follow from the molecular model.

## Input files

`data/inputs/objects.json` gives the two complete 130-atom, neutral singlet C60H63IrN4O2 identities, including atom-indexed connectivity and categorical trans-donor pairs. These pairs distinguish the coordination isomers; they do not specify optimized geometries or preferred stability. `data/inputs/conditions.json` specifies THF and 339 K. `resources.md` describes the available resource boundary.

## Scope

Compare the two intact coordination identities using compatible molecular states, thermal treatment and a declared common standard state. Define ΔG = G(isomer2) − G(isomer1), in kJ/mol. Describe which conformers or finite molecular states the result represents and the uncertainty material to a small difference. Choose methods and explanatory tests independently. The task concerns molecular thermodynamics; it does not establish formation kinetics, isolated synthetic yields, emission efficiency or device behavior.

## Required results

1. Calculate ΔG at 339 K in THF, identify the supported relative preference and state its resolution under the model used.
2. Explain the relative stability using computed molecular/electronic evidence. Assess how the structural differences relate to the energy difference and which contributions can or cannot be distinguished by that evidence.
3. Derive the conditional equilibrium population ratio or a supported range from your thermochemistry. State the conditions needed to interpret that ratio and whether the calculations establish a synthetic yield prediction.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the native inputs, outputs and analysis that support each final result. State identities, physical definitions, units, uncertainty and the limits of the modeled system. Unsupported guesses, copied observations and workflow completion earn no scientific points. Use only the supplied public inputs and available tools; general scientific/software documentation is allowed. Private evaluation files and prior verification archives are not public resources.
