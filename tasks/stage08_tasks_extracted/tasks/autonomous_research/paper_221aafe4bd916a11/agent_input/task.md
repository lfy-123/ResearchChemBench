# Scientific objective

Determine the Gibbs free-energy activation barrier and mechanism for hydride transfer from the supplied singlet, monoprotonated bisphosphine 2a conformer to carbon dioxide in acetonitrile at 298 K. Independently identify and discriminate plausible direct and stepwise pathways, including whether a discrete intermediate is required. The scored endpoint is the barrier for the best-supported hydride-transfer path for this defined 2a + CO2 system.

# Public inputs and scientific boundaries

`data/inputs/2a_inout.xyz` is the 79-atom Cartesian geometry of protonated bisphosphine 2a in a defined in–out conformer, with charge +1 and singlet multiplicity. Carbon dioxide is the neutral molecule O=C=O (C and two O atoms, charge 0, singlet); generate its geometry independently. The physical boundary is the isolated 2a + CO2 reaction in implicit acetonitrile at 298 K, ending at a bisphosphine dication plus formate. Do not use the paper, SI, general web, or hidden coordinate/result files. Choose and report your own electronic-structure method and conformer/TS search choices.

# Required scientific validation/investigation

Propose at least two chemically distinct plausible pathway hypotheses before selecting a route. Generate a finite, explicitly described set of reactant, intermediate and transition-state candidates, deduplicate equivalent candidates, optimize advanced candidates, and validate every claimed minimum with no imaginary frequencies and every claimed TS with exactly one imaginary frequency. Confirm TS connectivity by IRC or another explicit path test. Compare surviving paths on a consistent free-energy basis, report candidates rejected and why, and state search coverage. Completion requires either a validated best-supported path and barrier, or a bounded-failure report with the attempted hypotheses, ledger, technical stopping reason and strongest defensible conclusion. Stop when additional independent searches no longer alter the selected path or resources prevent validation; state the limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include hypotheses, method, solvent/temperature treatment, charge/multiplicity, candidate ledger, frequencies, connectivity/path evidence, selected barrier and conclusion. A bounded failure branch is allowed, but it must still contain the investigation ledger, validation status and limitations.
