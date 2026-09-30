# Scientific objective

Determine the electronic/bonding character of the four Au(I)···Au(I) contacts in the Au1-derived tetranuclear cation. Independently identify and test plausible explanations for the contacts using quantitative electronic-structure evidence. Report the four edge-contact AIM/QTAIM descriptors, delocalization indices (DIs), an interaction classification, and any complementary electronic interpretation. The scored object is the anion-free +4 singlet molecular cluster, not the crystal lattice or solution speciation.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. Retrieve exactly CCDC Access Structures record 2500223 (Au1·ClO4), remove only perchlorate counterions and crystallographic solvent molecules, retain the four ligands and all atom labels/connectivity, and use charge +4 and multiplicity 1. The four scored contacts are Au1-Au2, Au2-Au3, Au3-Au4 and Au4-Au1 in the retained cyclic labels. You may generate conformers or analysis files, but do not use the paper/SI or general web. Results are limited to this finite molecular model.

# Required scientific validation/investigation

Propose at least one plausible electronic explanation and a calculation route capable of discriminating it from alternatives. Software and model chemistry are your choice. Validate input identity, atom count/connectivity, charge and multiplicity before calculation. Optimize or otherwise justify a stationary molecular geometry, document convergence, and show that four edge Au···Au contacts and four corresponding BCPs are found. For each named contact retain its identity and report ρ, ∇²ρ, ELF, H, V, G, |V|/G and DI when available; if a descriptor is unavailable, state why and provide the closest validated alternative. Explain candidate generation, deduplication, validation, and why the search/analysis was stopped. Completion requires a reproducible calculation record plus either all four validated contact rows or a bounded-failure report identifying the missing rows and evidence. Submit exactly one row for each named contact: a validated row has numeric descriptors, while an unavailable descriptor uses JSON null and a specific explanation in `notes`; do not invent placeholders. Set `completion_status` to `complete` only when all four rows are validated, otherwise set it to `bounded_failure`. Stop after the chosen explanation has been tested against the quantitative descriptors and additional reasonable checks no longer change the conclusion; report remaining limitations and unresolved alternatives.

# Deliverables

Submit `report/results.json` and any supporting files declared there. The JSON must include system/provenance, hypothesis alternatives and discrimination evidence, validation records, per-contact observables, interaction classification, conclusion, limitations, and a completion status. Do not copy source-paper text or hidden reference values into the submission.
