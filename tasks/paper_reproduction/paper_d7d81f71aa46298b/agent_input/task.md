# Scientific objective

Test the authors' qualitative hypothesis that tensile-force activation of an isotactic PVC oligomer can open a mechanoradical H-atom-transfer/HCl-release pathway, and quantify the force-induced HAT barrier and the thermal activation barrier for the same model. Independently choose and justify a computational protocol; the requested observables are Gibbs free-energy barriers in kJ/mol at 298.15 K and 1 atm.

# Public inputs and scientific boundaries

The sole molecular input is `data/inputs/iso_pvc_r_f1000.xyz`: a 38-atom isotactic PVC oligomer, neutral charge and doublet multiplicity, with the SI Cartesian coordinates of the force-labeled reactant. Treat its atom ordering as persistent identity. The force is tensile and acts on the two terminal methyl groups; identify those sites from the terminal methyl geometry and state your atom indices. The physical boundary is this finite oligomer and the force-induced versus thermal pathways; do not infer bulk-polymer kinetics. The measurement boundary is electronic/thermal free-energy barriers from your stated model, reported in kJ/mol. The qualitative author hypothesis supplied for independent testing is terminal radical HAT followed by HCl release; no author geometry, barrier, or winning transition state is supplied.

# Required scientific validation/investigation

Plan and execute calculations sufficient to identify a force-induced HAT/HCl-release transition state and a thermal activation transition state, or report bounded failure with the attempted candidates and limitation. For every advanced transition state, report the candidate identity, reactant/product identities, charge and multiplicity, number of imaginary frequencies, and an IRC or other explicit connectivity test. Use frequency corrections consistently for compared states and state temperature/pressure. Deduplicate equivalent candidates by atom mapping and connectivity. Completion requires either validated barriers for both channels or a reproducible bounded-failure report after documenting all generated candidates, validation attempts, and the stopping reason. Do not claim the mechanism is established from a single unvalidated saddle point.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. It must include the chosen protocol, atom/site identity, candidate and validation records, force HAT barrier when found, thermal barrier when found, comparison statement, and limitations. Numeric values must be in kJ/mol. A bounded-failure branch is allowed only when it contains the attempted search and explicit reason for stopping.
