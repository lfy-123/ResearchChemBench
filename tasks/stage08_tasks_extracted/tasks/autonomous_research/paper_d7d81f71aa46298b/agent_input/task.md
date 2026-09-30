# Scientific objective

For the fixed isotactic PVC oligomer under tensile activation, independently determine whether a force-assisted route to HCl formation is kinetically more accessible than thermal activation, and quantify the best-supported force-induced and thermal free-energy barriers. Develop and discriminate plausible pathways from calculations rather than assuming a named mechanism.

# Public inputs and scientific boundaries

The sole molecular input is `data/inputs/iso_pvc_r_f1000.xyz`: a 38-atom isotactic PVC oligomer, neutral charge and doublet multiplicity, with persistent atom ordering. Tensile force acts on the two terminal methyl groups; identify and report their atom indices from the geometry. The physical boundary is this finite oligomer and the two activation regimes. The measurement boundary is computed Gibbs free-energy barriers in kJ/mol at 298.15 K and 1 atm, with all model choices disclosed.

# Required scientific validation/investigation

Generate and compare plausible force-induced and thermal HCl-forming pathways. Define your candidate-generation scope, deduplicate by atom mapping/connectivity, and advance candidates using stated chemical and energetic criteria. For every advanced transition state, report candidate identity, reactant/product identities, charge and multiplicity, imaginary-frequency count, and IRC or another explicit connectivity test. Completion requires validated barriers for both regimes, or a bounded-failure report documenting candidates, validation attempts, coverage, and stopping reason. If multiple pathways survive, report the lowest supported barrier in each regime and retain the alternatives and uncertainty.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include hypothesis/pathway records, protocol, atom/site identity, validation evidence, selected force and thermal barriers when available, comparison, coverage, and limitations. Numeric values are kJ/mol. Bounded failure must retain truthful candidate and validation fields rather than only a status string.
