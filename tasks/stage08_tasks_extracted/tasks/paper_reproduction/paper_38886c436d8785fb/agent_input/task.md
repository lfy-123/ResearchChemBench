# Scientific objective

Determine computationally whether adding the explicitly defined ionic-liquid ion pair to the Tb·Pa molecular association changes the electronic interaction energy, and explain what that result does and does not establish about molecular preorganization. Independently formulate and discriminate plausible complex arrangements.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the explicitly modeled ionic-liquid ion pair [C8MIm][NTf2] strengthens association between 1,3,5-triformylbenzene and p-phenylenediamine, consistent with ionic-liquid-mediated molecular preorganization relevant to rapid, highly crystalline COF membrane formation. This is a qualitative mechanistic proposal; the isolated-complex calculation does not by itself establish a crystallization barrier or macroscopic causality.

**Candidate route or mechanism.**
The proposed comparison is between the binary Tb·Pa association and a ternary arrangement in which the explicit C8MIm/NTf2 ion pair participates in the local interaction network around Tb·Pa. The authors discuss orderly prearrangement through ion and hydrogen-bond contacts, with water encapsulation and acid-mediated kinetics as separate contributors. Treat these as candidate interpretations to test on the supplied molecular systems.

**Discriminating evidence.**
Relevant evidence includes consistently defined interaction energies for the two complexes, stationary-point validation and coverage across candidate arrangements, and analysis of noncovalent contact patterns such as hydrogen-bond and ion-mediated interaction regions. The paper also relates the molecular calculation qualitatively to experimental and molecular-dynamics observations, but those macroscopic observations are outside the scored isolated-complex observable.

# Public inputs and scientific boundaries

`data/inputs/molecular_system.json` uniquely defines 1,3,5-triformylbenzene, p-phenylenediamine, the 1-octyl-3-methylimidazolium cation, and the bis(trifluoromethylsulfonyl)imide anion by SMILES, charge and singlet multiplicity. It defines binary 1:1 and ternary ion-pair-containing 1:1:1:1 complexes and the interaction-energy convention. Treat the supplied cation and anion as one explicit ion pair. Generate 3-D structures yourself. The boundary is isolated molecular complexes with an explicitly stated electronic-structure model; solvent, periodic COF, polymer growth, transition states and membrane observables are outside scope.

# Required scientific validation/investigation

Propose plausible arrangements for each complex, generate and deduplicate them with a stated structural criterion, optimize them, and retain structures supported by a stationary-point check. Report search coverage, counts attempted/retained, advancement criteria, and stopping/limitation conditions. Compute component and complex energies consistently in kJ/mol, report the two interaction energies and their difference, and state whether the result is robust to retained arrangements or otherwise bounded by the search. Completion requires a validated retained structure for each target and all requested energies; if that cannot be achieved, submit the bounded-failure branch with the exact missing validation and evidence. Stop when newly generated arrangements are duplicates under the stated rule or the available search/compute boundary has been reached and coverage is documented.

# Deliverables

Submit `report/results.json` conforming to the schema. Include one or more independent hypotheses, candidate-level identities, scientific assignments and validation, raw and derived energies, coverage/stopping information, limitations, and a final conclusion about the effect of the ion pair. A truthful bounded-failure branch must identify the missing target and supporting evidence and must not fabricate success-only energies. Do not claim a mechanism beyond what the calculations support.
