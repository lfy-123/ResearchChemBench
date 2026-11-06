# SiN + isoprene: H-loss products and formation

## Scientific question

Which product structures and formation explanation are supported for the atomic-H-loss channel of SiN reacting with isoprene in isolated gas-phase single collisions, and how specifically can the products be identified?

## Input files

- `data/inputs/objects.json` supplies mapped identities for SiN (neutral doublet), isoprene C5H8 (neutral singlet) and atomic H (neutral doublet).
- `data/inputs/observations.json` supplies the observed SiNC5H7 + H composition, collision energy 25 ± 1 kJ/mol and channel reaction energy −162 ± 27 kJ/mol relative to separated reactants.

## Scope

Investigate the product connectivity and electronic state without altering the full atom inventory. The reactant system has total doublet spin. Use 0 K channel energies E0 = electronic energy + zero-point vibrational energy relative to separated SiN + isoprene, including the separated H coproduct; state any alternative convention explicitly. The experimental energy comes from collision/translational-energy conservation and is not a 298 K solution Gibbs energy.

Choose your candidate structures, methods and route investigation. The product comparison must address distinct regioisomeric candidates associated with the two inequivalent orientations of the methyl-substituted diene relative to SiN. Determine their actual connectivities and states rather than assuming that one found endpoint covers the comparison. This does not prescribe a ring size, entry atom or winning pathway. The required scope is product structures, their channel energies, a connected formation explanation for a compatible product, and the limits of identification. Exhaustive isomer enumeration, two complete formation networks, branching fractions and interstellar production rates are not required.

## Required results

1. Identify the distinct product structures supported by your investigation, including their connectivity, methyl substitution, charge and spin. Give the computed E0 of each supported product + H relative to the common reactants in kJ/mol and compare it with the measured channel interval.
2. Explain a physically connected formation route from intact reactants to a supported product + H. Show how actual chemical connections and energy heights make that account viable or nonviable at the supplied collision energy. Validate the particular minima, saddles or finite entry/exit claims used in the explanation.
3. State what the observed channel energy and your formation evidence distinguish among products, and what remains unresolved. Separate energetic compatibility, demonstrated formation and branching; bind exclusions to the chemical space actually investigated.

## Submission

Submit `report/results.json` and `report/report.md` following `submission_guide.md` and `submission_schema.json`. Support final answers with inspectable native calculations and reproducible analyses. Final scientific results total 100 points; research-process completion carries no independent points. Use only the supplied inputs, resources made available for this task and general scientific/software documentation. Private evaluator material and prior verification archives are not public resources.
