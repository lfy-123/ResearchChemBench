## Scientific question

Explain how the specified visible-light reaction of buta-1,3-diene, sodium difluoromethanesulfinate and methyl pentafluorobenzoate forms the observed polyfluoroaryl sulfone. What explains its 1,4-versus-1,2 competition and E preference, and the reversal to 1,2 addition for the specified terminal-phenyl diene? This is an explanation task: observed products and preferences are supplied starting facts.

## Input files

`data/inputs/system.json` specifies the common reactants (PI1–PI3), distinct reaction conditions and 4CzIPN identity (PI4), butadiene products/observations (PI5), terminal-phenyl diene (PI6), and its product (PI7). Number the diene chain from the terminal CH2 end; phenyl is on C4. Net 1,2/1,4 labels specify attachment positions, not a reaction sequence. `submission_schema.json` and `submission_guide.md` define the output format.

## Scope

Address connected molecular product formation, both butadiene selectivities and the phenyl-system reversal. Retain the specified DMSO/THF versus DMF conditions, base difference and illumination conditions. The two systems are not a controlled substituent-only comparison. No absolute configuration at the phenyl product's sulfur-bearing carbon is supplied. Isolated yields are not rate constants and no numerical byproduct detection limit is known. Detailed photocatalyst excitation, full solution speciation, ion-exchange kinetics, global reaction rates and a complete substrate library are outside scope. Choose and justify reactive molecular species, charge/spin and environmental boundaries.

## Required results

1. Give a connected molecular and energetic explanation for the target sulfone formation from the specified inputs, explaining the bond changes, chemical driving factors and limits of the model.
2. Explain butadiene's 1,4 preference using competing formation evidence, reporting a comparable free-energy difference and its physical origin.
3. Explain its E preference with computed energetics and explicit assumptions about precursor states and any interconversion; distinguish local activation differences from energies on a common reference.
4. Explain and quantify the competing 1,2/1,4 preference of the terminal-phenyl system and its reversal relative to butadiene under the different conditions.

Choose hypotheses and methods independently; no particular intermediate, descriptor, calculation count or exhaustive search is prescribed. Support claimed minima, transition states and connections with suitable actual evidence. Balance molecular and electronic inventories and state units, references and model conditions. Distinguish a local reaction free energy from a whole photoredox reaction, and molecular connectivity from verified experimental kinetics. The observed preferences cannot substitute for calculated explanations.

## Submission and permitted resources

Submit `report/results.json`, `report/report.md` and actual calculation inputs, outputs, logs and analyses under `research/`. Use the provided public files and your independently generated calculations with chosen software. Link final claims to indexed native evidence, record actual resource use and disclose unresolved findings. Preserve failed attempts. Scientific credit concerns supported final outcomes only; there is no separate research-process score.
