# Molecular absorption of two organoboron dyes

## Scientific question

What electronic explanation accounts for the solution absorption of the two supplied organoboron dyes and its response to changing chloroform to methanol? Determine which effects of methoxy substitution and solvent the molecular calculations support, and how accurately the model describes the observed bands.

## Input files

- `data/inputs/objects.json` gives complete atom-indexed graphs of neutral singlet dye1 (C23H20BNO3) and dye2 (C24H22BNO4). Both retain the 3,5-dimethylphenyl group bonded to boron; dye2 has the additional mapped methoxy substituent.
- `data/inputs/observations.json` gives measured absorption bands in CHCl3 and MeOH, with measurement limitations. These are known observations to explain.
- `resources.md` describes the resource and access boundary.

## Scope

Study the intact dyes and their molecular solution absorption. Declare the geometry, solvent representation and excited-state/band correspondence used. Distinguish vertical transition energies from measured absorption maxima. Choose the calculation and analysis methods independently. The two solvents differ in polarity, specific solvation and viscosity; their comparison alone cannot identify viscosity as the cause. Photobleaching, hydrolytic lifetime, cell staining and biological efficacy are outside scope.

## Required results

1. Assign the electronic character and participating molecular regions of each dye's low-energy absorption from actual excitation evidence.
2. Explain the substitution-dependent difference between corresponding low-energy absorptions using calculated energies and electronic distributions.
3. For each dye, calculate its absorption response to changing solvent and explain what differential electronic/solvation effects account for the supplied observations.
4. Quantitatively compare predicted transitions with the supplied bands and determine separately which relative changes and absolute band positions the model explains. Report residuals and justified assignment limitations.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the native inputs, outputs and analysis that support each final result. State identities, physical definitions, units, uncertainty and the limits of the modeled system. Unsupported guesses, copied observations and workflow completion earn no scientific points. Use only the supplied public inputs and available tools; general scientific/software documentation is allowed. Private evaluation files and prior verification archives are not public resources.
