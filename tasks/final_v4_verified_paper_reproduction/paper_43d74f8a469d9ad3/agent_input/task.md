# Molecular absorption of two organoboron dyes

## Scientific question

What electronic explanation accounts for the solution absorption of the two supplied organoboron dyes and its response to changing chloroform to methanol? Determine which effects of methoxy substitution and solvent the molecular calculations support, and how accurately the model describes the observed bands.

## Input files

- `data/inputs/objects.json` gives complete atom-indexed graphs of neutral singlet dye1 (C23H20BNO3) and dye2 (C24H22BNO4). Both retain the 3,5-dimethylphenyl group bonded to boron; dye2 has the additional mapped methoxy substituent.
- `data/inputs/observations.json` gives measured absorption bands in CHCl3 and MeOH, with measurement limitations. These are known observations to explain.
- `resources.md` describes the resource and access boundary.

## Scope

Study the intact dyes and their molecular solution absorption. Declare the geometry, solvent representation and excited-state/band correspondence used. Distinguish vertical transition energies from measured absorption maxima. Choose the calculation and analysis methods independently. The two solvents differ in polarity, specific solvation and viscosity; their comparison alone cannot identify viscosity as the cause. Photobleaching, hydrolytic lifetime, cell staining and biological efficacy are outside scope.

## Author baseline for reproduction

The source general electronic calculations use Gaussian16 M06-2X/6-311++G(d,p) (main §2.5 and Table6). A separate rotational study compares dyes1 and3 at PBE0/def2-SVP using15-degree ground-state single-point rotations (main p11, SI FigS57); it is a distinct protocol and is not a source calculation of a dye1/dye2 excited-state scan. The authors discuss donor substitution, restricted phenyl rotation and steric protection, while observed absorption and fluorescence are tabulated separately (Tables4–5). Some source SI coordinate labels conflict with Scheme1 chemistry, so reconstruct/check identities before reproduction and record any ambiguity. The old added state-tracked S1 scan grid was a benchmark extension, not a prerequisite for reproducing the author baseline.

The graph-bound source gas-phase S1 reference values are dye1 3.3556 eV and f=0.1978, dye2 3.4573 eV and f=0.3736 (dimensionless). Report independently calculated baseline energies and oscillator strengths as reproduction results, separately from the solution-band assessment. These calculated energies and oscillator strengths support the state-assignment and comparative absorption conclusions; individual author-value matching windows are not used for scoring.

Reproduce this disclosed baseline or substantiate a physically applicable substitute and its consequences. Source values and assignments are comparison references; copied values alone earn no credit. Additional comparisons remain your choice.

## Required results

1. Assign the electronic character and participating molecular regions of each dye's low-energy absorption from actual excitation evidence.
2. Explain the substitution-dependent difference between corresponding low-energy absorptions using calculated energies and electronic distributions.
3. For each dye, calculate its absorption response to changing solvent and explain what differential electronic/solvation effects account for the supplied observations.
4. Quantitatively compare predicted transitions with the supplied bands and determine separately which relative changes and absolute band positions the model explains. Report residuals and justified assignment limitations.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the native inputs, outputs and analysis that support each final result. State identities, physical definitions, units, uncertainty and the limits of the modeled system. Unsupported guesses, copied observations and workflow completion earn no scientific points. Use only the supplied public inputs and available tools; general scientific/software documentation is allowed. The full target article/SI, private evaluation files and prior verification archives are not public resources. Any author baseline explicitly disclosed in this task is authorized.
