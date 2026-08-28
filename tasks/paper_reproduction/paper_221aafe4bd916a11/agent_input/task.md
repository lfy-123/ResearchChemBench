# Scientific objective

Determine the Gibbs free-energy activation barrier for hydride transfer from the supplied singlet, monoprotonated bisphosphine 2a conformer to carbon dioxide in acetonitrile at 298 K, and test the qualitative author hypothesis that the phosphine orientation can permit a direct hydride-transfer route. Establish the reactant and transition-state structures and decide whether a discrete intermediate is required on the investigated path. The scored endpoint is the hydride-transfer barrier (kcal/mol) for this defined 2a + CO2 system.

# Public inputs and scientific boundaries

`data/inputs/2a_inout.xyz` is the 79-atom Cartesian geometry of protonated bisphosphine 2a in the in–out conformer, with charge +1 and singlet multiplicity. Carbon dioxide is the neutral molecule O=C=O (C and two O atoms, charge 0, singlet); generate its geometry independently. The physical boundary is the isolated 2a + CO2 reaction in implicit acetonitrile at 298 K, ending at a bisphosphine dication plus formate. Do not use the paper, SI, general web, or hidden coordinate/result files. Choose and report your own electronic-structure method and conformer/TS search choices; the paper’s exact recipe is not prescribed.

# Required scientific validation/investigation

Independently plan and execute a defensible stationary-point/pathway investigation guided by the qualitative hypothesis above. Generate a finite, explicitly described set of reactant and transition-state candidates, deduplicate equivalent candidates, optimize advanced candidates, and validate every claimed minimum with no imaginary frequencies and every claimed TS with exactly one imaginary frequency. Confirm that the TS connects the stated reactant-side and product-side chemical events by an IRC or another explicit connectivity/path validation. Report candidates rejected and why. Completion requires either a validated TS and barrier, or a bounded-failure report showing the candidates attempted, numerical/technical stopping reason, and the strongest defensible mechanistic conclusion. Stop when a validated path is obtained and additional independent searches no longer change the selected pathway, or when resources prevent validation; state coverage and limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method, solvent/temperature treatment, charge/multiplicity, candidate ledger, frequencies, connectivity/path evidence, barrier and conclusion. A bounded failure branch is allowed, but it must still contain the investigation ledger, validation status and limitations.
