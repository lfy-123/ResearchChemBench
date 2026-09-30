# Scientific objective

Determine computationally whether adding the explicitly defined ionic-liquid ion pair to the Tb·Pa molecular association changes the electronic interaction energy, and explain what that result does and does not establish about molecular preorganization. Independently formulate and discriminate plausible complex arrangements; no author mechanism, candidate route, or expected direction is supplied.

# Public inputs and scientific boundaries

`data/inputs/molecular_system.json` uniquely defines 1,3,5-triformylbenzene, p-phenylenediamine, the 1-octyl-3-methylimidazolium cation, and the bis(trifluoromethylsulfonyl)imide anion by SMILES, charge and singlet multiplicity. It defines binary 1:1 and ternary ion-pair-containing 1:1:1:1 complexes and the interaction-energy convention. Treat the supplied cation and anion as one explicit ion pair. Generate 3-D structures yourself. The boundary is isolated molecular complexes with an explicitly stated electronic-structure model; solvent, periodic COF, polymer growth, transition states and membrane observables are outside scope.

# Required scientific validation/investigation

Use the reference groups in the input to compare diamine binding to the aldehyde and to the preassociated ion-pair–aldehyde host. Total assembly from four isolated molecular energies is a different observable. Verify that intended noncovalent partners retain their covalent identities; real frequencies alone do not validate a rearranged molecule. Disclose relaxed-versus-frozen fragment and correction conventions. Do not infer an unreported solvent or external reference convention from whichever choice makes a result look favorable.

Propose plausible arrangements for each complex, generate and deduplicate them with a stated structural criterion, optimize them, and retain structures supported by a stationary-point check. Report search coverage, counts attempted/retained, advancement criteria, and stopping/limitation conditions. Compute component and complex energies consistently in kJ/mol, report the two interaction energies and their difference, and state whether the result is robust to retained arrangements or otherwise bounded by the search. Completion requires a validated retained structure for each target and all requested energies; if that cannot be achieved, submit the bounded-failure branch with the exact missing validation and evidence. Stop when newly generated arrangements are duplicates under the stated rule or the available search/compute boundary has been reached and coverage is documented.

# Deliverables

Submit `report/results.json` conforming to the schema. Include one or more independent hypotheses, candidate-level identities, scientific assignments and validation, raw and derived energies, coverage/stopping information, limitations, and a final conclusion about the effect of the ion pair. A truthful bounded-failure branch must identify the missing target and supporting evidence and must not fabricate success-only energies. Do not claim a mechanism beyond what the calculations support.
