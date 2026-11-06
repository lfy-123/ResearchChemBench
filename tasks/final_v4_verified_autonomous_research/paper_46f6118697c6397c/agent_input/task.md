# Scientific question

What electronic transitions account for the measured absorption bands of the four B2N6 derivatives in dichloromethane, and how do changes from tolyl to methyl, chloride and covalently bound triflate substituents explain their differences?

# Input files

- `data/inputs/systems.json` supplies the four complete mapped molecular graphs, formulas, neutral charges and singlet multiplicities. Compound 2 contains four covalent B–O–SO2CF3 groups.
- `data/inputs/experimental_absorption.json` supplies measured maxima in dichloromethane at 50 μM, with their measurement definition.
- `data/inputs/solution_observations.json` supplies the qualitative solvent dependence observed for compound 2, without a detection threshold.
- `data/inputs/problem_facts.json` distinguishes measured maxima, electronic transitions and orbital gaps.

# Scope

Explain molecular solution absorption for these four complete identities. The experimental peak positions are given observations: their restatement is not a computational prediction. An experimental band maximum is not automatically a calculated transition energy or orbital gap. Any alternative solution composition must preserve material and charge balance and have evidence for its relevance. Solid-state emission, redox decomposition and device performance are outside this question.

# Required results

1. Assign the electronic character of the absorption feature for each compound using calculated transition strengths and spatial electronic evidence. Report the assigned transition energies (eV or nm), strengths and the state-to-band correspondence; selecting an arbitrary first root or a numerically nearby root is insufficient.
2. Explain the measured difference between compounds 1 and 4 through the calculated response of the relevant occupied and unoccupied states to the substituent change. Compare the calculated shift with the observed trend and state what the model can resolve.
3. Explain the differences involving compounds 2 and 3, including their relation to 1/4 and to each other. Determine which electronic regions contribute to the assigned bands and how substituents alter those states. Bound any inference about solution dissociation by the supplied qualitative observation and your actual evidence.

Choose and justify the computational models and methods. Do not equate a frontier-orbital index with physical transition identity. A spectral assignment may be established by equivalent orbital, transition-density or wavefunction analyses. Quantify relevant discrepancies and distinguish stick transitions from broadened maxima.

# Submission

Submit `report/results.json` and `report/report.md` using the supplied schema and guide, with native calculation files and reproducible extraction/analysis linked to each final claim. Only supported final scientific results earn points. Use public inputs and general scientific/software documentation; private references and prior verification archives are not submission inputs.
