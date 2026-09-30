# Scientific objective

Determine, by independent computation, whether the supplied cyclohexyl-radical/CO/iodocyclohexane system can plausibly proceed through carbonylation and which of four explicitly supplied amines is favored in attack on cyclohexanecarbonyl iodide. Report relative Gibbs free energies, activation barriers, stationary-point character, and a mechanistic/selectivity conclusion. Generate and test your own explanations and pathways for the target transformation.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that an alkyl radical first captures CO, followed by iodine-atom transfer from an alkyl iodide to regenerate the radical and produce an acyl iodide. They further interpret amine selectivity through attack on that acyl iodide and the subsequent tetrahedral intermediate, with the four supplied amines providing the comparison.

**Candidate route or mechanism.**
Test the proposed radical chain as a candidate explanation: CO addition to the cyclohexyl radical, iodine-atom transfer involving the carbonylated species and iodocyclohexane, then nucleophilic attack of each amine on cyclohexanecarbonyl iodide toward amide formation. For the amine comparison, consider both the approach/activation event and the resulting tetrahedral intermediate rather than treating either one alone as the selectivity criterion.

**Discriminating evidence.**
Use validated minima and transition structures, their imaginary-frequency assignments and connectivities, relative Gibbs free energies and activation barriers for the radical sequence, and the relative free energies of the four tetrahedral intermediates. Compare the kinetic and thermodynamic patterns across aniline, N-ethylaniline, N-methylaniline, and morpholine, while limiting conclusions to the stated molecular model.

# Public inputs and scientific boundaries

`data/inputs/molecular_system.json` uniquely defines the supplied reactants and four amine candidates by SMILES and gives charge, multiplicity, and role. Generate all geometries independently, including any derived acyl-iodide intermediate; no result-bearing intermediate structure is supplied. The scored system is the isolated molecule: do not add a host, catalyst, or explicit solvent. The radical pathway is neutral doublet; amine attack is neutral singlet. Use an acetonitrile continuum or justify another solvent treatment, and state temperature and standard-state conventions. The task concerns molecular electronic structure and thermochemistry only, not photophysical electron transfer, explicit-solvent dynamics, or experimental yields.

# Required scientific validation/investigation

Propose plausible elementary pathways and discriminate them computationally. Generate a finite, explicitly listed set of starting conformers/approaches for CO capture, iodine transfer, and each amine attack; deduplicate by connectivity and geometry. Optimize candidates, calculate frequencies, and retain per-candidate identity and evidence. A minimum requires zero imaginary frequencies; a transition structure requires exactly one imaginary frequency assigned to the proposed event. Advance only connected candidates whose structures and modes support the claimed event. Continue until the proposed candidate set is exhausted and additional starts no longer yield a distinct validated stationary point; report coverage, unsuccessful searches, and limitations. Completion means every requested channel is either represented by a validated stationary point/free energy or accompanied by a bounded failure explanation.

# Deliverables

Submit `report/results.json` conforming to the local `submission_schema.json`. Include the proposed pathways, candidate identities and validation, relative ΔG‡/ΔG in kcal/mol, method and standard-state details, uncertainty/limitations, and a conclusion that identifies which explanation(s) are supported by the submitted calculations. Bounded failure or partial discovery is acceptable only with candidate-level search and validation records.
