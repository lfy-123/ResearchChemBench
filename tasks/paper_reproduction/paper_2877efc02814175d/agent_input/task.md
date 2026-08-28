## Scientific objective

Independently test the authors' qualitative hypothesis that coordination of the DQCS coumarin/8-hydroxyquinoline Schiff-base probe by divalent metals changes its frontier electronic structure across the Cd(II)/Co(II)/Ni(II) comparison. Compute the HOMO-LUMO gap, chemical hardness, and electrophilicity index for each named 1:1 complex, then determine whether the calculations support a metal-dependent electronic-response trend. This is a computational comparison, not a request to reproduce an experimental binding constant.

## Public inputs and scientific boundaries

The three public files are `data/inputs/cd_complex.xyz`, `co_complex.xyz`, and `ni_complex.xyz`. Each is a 65-center Cartesian geometry for, respectively, DQCS+Cd2+, DQCS+Co2+, and DQCS+Ni2+, transcribed from the SI coordinate tables; the first two lines identify the object and state that total charge is +2 and multiplicity is 1. Treat the listed atomic numbers and coordinates as the complete molecular systems. Use an implicit DMSO representation or clearly state and justify a controlled alternative. Do not add counterions or explicit solvent. You may optimize the supplied structures or perform a justified single-point calculation, but must state which. The measured quantities are HOMO-LUMO gap (eV), chemical hardness (eV), and electrophilicity index (eV), with formulas/units and software/method details. The paper's reported computational settings are context for the hypothesis only; do not assume they are mandatory.

## Required scientific validation/investigation

For every named complex, verify that the input contains 65 centers, one Cd/Co/Ni center as appropriate, and the stated +2 singlet state; report any change after optimization. Demonstrate electronic-structure convergence (or give a bounded-failure record identifying the failed object and the last valid quantities). Define how frontier orbitals were selected and how hardness/electrophilicity were calculated from reported orbital or ionization/electron-affinity quantities. Use the same decision rule for all three complexes. A completed comparison requires valid values for every successfully completed object; if an object cannot be completed, submit its identity, validation/convergence evidence, and a bounded-failure explanation instead of invented numbers. Stop after all three objects have been attempted, convergence/validation evidence has been recorded, and one final comparison and limitation statement is made; do not claim more than this fixed set supports.

## Deliverables

Submit `report/results.json` conforming to the submission schema. Include method, solvent treatment, state checks, per-complex observables, validation evidence, comparison, and limitations. The result must distinguish calculated values from interpretation and must not cite the private paper route as an input.
