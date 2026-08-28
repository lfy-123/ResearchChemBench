# Scientific objective

Test the authors' proposed host-to-guest electronic-transfer explanation for the isolated [4]pseudorotaxane G2+@β-CD3. Independently construct and optimize the specified complex, determine whether the frontier orbitals support donor host / acceptor guest character, and measure the closest β-CD hydroxyl-oxygen to pyridinium-nitrogen contact. The requested observables are an optimized structure, convergence evidence, HOMO and LUMO fragment localization, the atom identities and value of the minimum O···N distance in Å, and a scoped mechanistic conclusion. The authors' qualitative hypothesis is that cyclodextrin hosts donate electron density to the viologen guest; this statement is a hypothesis to test, not a supplied result.

# Public inputs and scientific boundaries

Use `data/inputs/system_definition.json`. Retrieve exactly PubChem CID 444041 for β-cyclodextrin and the exact systematic-name viologen record specified there; record database query results and any deterministic hydrogenation/3-D conformer generation. Use one guest plus three hosts, total charge +2 and singlet multiplicity. The isolated complex excludes solvent, chloride counterions and crystal periodicity. The requested contact is the minimum Cartesian distance over every hydroxyl oxygen on any β-CD and either pyridinium ring nitrogen of G2plus; report the atom labels used. Orbital localization must be assigned to the β-CD host fragment versus the viologen pyridinium/phenylene guest fragment.

# Required scientific validation/investigation

Construct at least one threaded starting geometry consistent with the stated inclusion boundary, and document connectivity, stereochemistry, charge and multiplicity. Optimize it with a defensible method of your choice, then verify an actual convergence criterion, absence of severe clashes, intact host/guest connectivity and physically sensible complex geometry. Compute or otherwise analyze frontier orbitals on the optimized geometry; provide reproducible evidence (orbital populations, fragment contributions, plots or equivalent) for both HOMO and LUMO assignments. Enumerate the atom pairs used for the minimum O···N search and independently recompute that minimum from the final coordinates. The calculation is complete when one converged, validated optimized complex and both orbital assignments plus the contact measurement are documented. Stop after this endpoint and a stated sensitivity/limitation discussion; if convergence or orbital analysis fails, report the bounded failure with evidence and the attempted coverage rather than inventing values.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include methods, database retrieval identifiers, geometry/convergence evidence, orbital-localization evidence, the measured contact and atom pair, a mechanistic conclusion, and limitations. Include paths to supporting files when available; all numbers must carry units and provenance.
