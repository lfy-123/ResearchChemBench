# Scientific objective

Determine, from an independent computational investigation of the isolated G2+@β-CD3 complex, whether its electronic structure is consistent with intermolecular charge transfer between the cyclodextrin hosts and viologen guest. Construct and validate the complex, characterize frontier-orbital fragment localization, and measure the closest β-CD hydroxyl-oxygen to pyridinium-nitrogen contact. Report the optimized structure, convergence evidence, HOMO/LUMO localization, atom identities and minimum O···N distance in Å, then state the strongest conclusion justified by the calculations and its limitations.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. Retrieve exactly PubChem CID 444041 for β-cyclodextrin and the exact systematic-name viologen record specified there. Use one guest plus three hosts, total charge +2 and singlet multiplicity. The isolated complex excludes solvent, chloride counterions and crystal periodicity. The contact is the minimum Cartesian distance over all β-CD hydroxyl oxygens and either pyridinium ring nitrogen of G2plus. Assign orbital localization to the β-CD host fragment or viologen pyridinium/phenylene guest fragment, with evidence. Formulate and test plausible donor/acceptor explanations from the computed data.

# Required scientific validation/investigation

Choose and document a reproducible construction and computational protocol. Validate exact retrieved connectivity, stereochemistry, charge and multiplicity; validate optimization convergence, no severe clashes and intact host/guest geometry. Analyze both frontier orbitals with fragment populations, plots or equivalent evidence and explain how the evidence discriminates plausible charge-transfer directions. Enumerate the atom pairs used for the minimum distance and recompute it from final coordinates. Completion requires one converged, validated optimized complex, both orbital assignments, the contact measurement and a reasoned conclusion. Stop at that endpoint plus a stated sensitivity/limitation assessment; if the endpoint cannot be reached, report bounded failure and coverage honestly without fabricating numeric or structural results.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, including retrieval identifiers, methods, validation evidence, per-orbital localization, the contact atom pair and value, an independent mechanistic conclusion, and limitations. Link supporting computational artifacts where available.
