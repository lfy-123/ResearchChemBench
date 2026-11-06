# Scientific question

What electronic transitions account for the measured absorption bands of the four B2N6 derivatives in dichloromethane, and how do changes from tolyl to methyl, chloride and covalently bound triflate substituents explain their differences?

# Input files

- `data/inputs/systems.json` supplies the four complete mapped molecular graphs, formulas, neutral charges and singlet multiplicities. Compound 2 contains four covalent B–O–SO2CF3 groups.
- `data/inputs/experimental_absorption.json` supplies measured maxima in dichloromethane at 50 μM, with their measurement definition.
- `data/inputs/solution_observations.json` supplies the qualitative solvent dependence observed for compound 2, without a detection threshold.
- `data/inputs/problem_facts.json` distinguishes measured maxima, electronic transitions and orbital gaps.

# Scope

Explain molecular solution absorption for these four complete identities. The experimental peak positions are given observations: their restatement is not a computational prediction. An experimental band maximum is not automatically a calculated transition energy or orbital gap. Any alternative solution composition must preserve material and charge balance and have evidence for its relevance. Solid-state emission, redox decomposition and device performance are outside this question.

# Disclosed reproduction baseline

The author route is Gaussian 16, B3LYP-D3BJ/6-31+G(d), SMD dichloromethane for optimization and TD-DFT (SI p16; the short main-text label omits D3BJ). Main pp3–4 attributes absorption to N6-related orbitals: mainly HOMO→LUMO for 1/4 and HOMO−4→LUMO for 2/3, with benzyl-localized frontier levels in 2/3. These are assignments to assess, not fixed root-selection instructions. The source discusses limited triflate dissociation from the solvent-insensitive spectrum. Main prose and SI are inconsistent: C1 is 3.52 eV in the prose but 3.0119 eV, f=0.3456 in SI Table S2. SI gives C4 3.1220 eV/f=0.5223, C3 3.4440 eV/f=0.3870 and C2 3.8436 eV/f=0.4243; prose gives 3.97/4.33 eV for C3/C2. Keep these definitions separate when reporting discrepancies.

# Required results

1. Assign the electronic character of the absorption feature for each compound using calculated transition strengths and spatial electronic evidence. Report the assigned transition energies (eV or nm), strengths and the state-to-band correspondence; selecting an arbitrary first root or a numerically nearby root is insufficient.
2. Explain the measured difference between compounds 1 and 4 through the calculated response of the relevant occupied and unoccupied states to the substituent change. Compare the calculated shift with the observed trend and state what the model can resolve.
3. Explain the differences involving compounds 2 and 3, including their relation to 1/4 and to each other. Determine which electronic regions contribute to the assigned bands and how substituents alter those states. Bound any inference about solution dissociation by the supplied qualitative observation and your actual evidence.

Reproduce and assess the disclosed author baseline, or justify a physically comparable substitution and explain its consequences. Do not equate a frontier-orbital index with physical transition identity. A spectral assignment may be established by equivalent orbital, transition-density or wavefunction analyses. Quantify relevant discrepancies and distinguish stick transitions from broadened maxima.

# Submission

Submit `report/results.json` and `report/report.md` using the supplied schema and guide, with native calculation files and reproducible extraction/analysis linked to each final claim. Only supported final scientific results earn points. Use public inputs and general scientific/software documentation; private references and prior verification archives are not submission inputs.
