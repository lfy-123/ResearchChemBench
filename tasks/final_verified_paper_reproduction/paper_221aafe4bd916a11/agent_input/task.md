# Scientific objective

Determine the Gibbs free-energy activation barrier for hydride transfer from the supplied singlet, monoprotonated bisphosphine 2a conformer to carbon dioxide in acetonitrile at 298.15 K, and test the qualitative author hypothesis that the phosphine orientation can permit a direct hydride-transfer route. Establish the reactant and transition-state structures and decide whether a discrete intermediate is required on the investigated path. The scored endpoint is the hydride-transfer barrier (kcal/mol) for this defined 2a + CO2 system.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that the defined in–out orientation of protonated bisphosphine 2a can enable hydride transfer to CO2 through a comparatively accessible direct event.

**Candidate route or mechanism.**
The author-proposed route is a single-step hydride transfer from 2a to CO2, connecting the reactant-side complex directly to the bisphosphine dication plus formate without requiring a discrete intermediate. Treat this as the route to investigate and test for this defined system.

**Discriminating evidence.**
Use optimized stationary points and Gibbs free energies, verify minima by all-positive frequencies and transition states by exactly one imaginary frequency, and use an IRC or another explicit connectivity/path test to determine whether the candidate transition structure connects the hydride-transfer reactant and product-side chemical event.

# Public inputs and scientific boundaries

`data/inputs/2a_inout.xyz` is the independently displaced 79-atom Cartesian starter for protonated bisphosphine 2a in the in–out connectivity, with charge +1 and singlet multiplicity. Carbon dioxide is the neutral molecule O=C=O (C and two O atoms, charge 0, singlet); generate its geometry independently. The physical boundary is the isolated 2a + CO2 reaction in implicit acetonitrile at 298.15 K, ending at a bisphosphine dication plus formate. Do not use the paper, SI, general web, or hidden coordinate/result files. Choose and report your own electronic-structure method and conformer/TS search choices; the paper’s exact recipe is not prescribed.

Primary barrier definition: ΔG‡ = G(TS) - G(2a) - G(CO2), in kcal/mol, using the separately validated reactant species as the zero (not a preassociated complex). Use implicit acetonitrile and a consistent 298.15 K, 1 atm standard-pressure harmonic thermochemistry convention for every term. Report the electronic-energy level and thermal correction separately; if using higher-level single points, apply the same composite-energy definition to all species. A 1 M standard-state barrier or a barrier relative to a preassociated complex may be reported separately, with an explicit conversion to the primary definition. This definition does not prescribe a numerical barrier or a unique search method.

# Required scientific validation/investigation

Independently plan and execute a defensible stationary-point/pathway investigation guided by the qualitative hypothesis above. Generate a finite, explicitly described set of reactant and transition-state candidates, deduplicate equivalent candidates, optimize advanced candidates, and validate every claimed minimum with no imaginary frequencies and every claimed TS with exactly one imaginary frequency. Confirm that the TS connects the stated reactant-side and product-side chemical events by an IRC or another explicit connectivity/path validation. Report candidates rejected and why. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include method, solvent/temperature treatment, charge/multiplicity, candidate ledger, frequencies, connectivity/path evidence, barrier and conclusion. A bounded failure branch is allowed, but it must still contain the investigation ledger, validation status.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
