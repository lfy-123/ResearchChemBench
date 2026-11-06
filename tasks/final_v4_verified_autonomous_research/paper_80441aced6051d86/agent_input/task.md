# Scientific question

Which molecular association structures of G1 with CB[7] and CB[8] are consistent with the supplied aqueous observations, how do they differ from free G1 association, and how far can they explain the optical contrast?

# Input files

- `data/inputs/g1_monomer_identity.json`, `CB7_identity.json` and `CB8_identity.json` provide complete atom-mapped molecular graphs.
- `data/inputs/observations.json` provides emission maxima, known host:guest compositions and conflicting concentration annotations.
- `data/inputs/problem_context.json` summarizes the environment and input limitations.

# Scope

G1 is the C34H28N2 dication; CB[7] and CB[8] are neutral hosts. The observed 1:1 CB7:G1 and 1:2 CB8:G1 compositions specify stoichiometry, not binding geometry. Compare free monomer/pair association with these two complete host complexes in water. Declare chloride counterion treatment and the electronic state of each model. NMR compositions refer to D2O at 298 K.

Host optical concentration is unresolved: annotation A gives 0.02 mM G1 and annotation B gives 0.50 mM for the same host emission peaks. These are conflicting labels, not two independently measured series. Preserve both and compare within a clearly stated branch. Raw spectra and peak error bars are unavailable. CB[10], quantitative emission yields and a complete emission-kinetic mechanism are outside scope.

# Required results

1. Determine the structural change between isolated G1 and an associated free pair, using explicit atom-defined molecular conformation and relative packing descriptors.
2. Determine the molecular inclusion topology for CB7:G1: which guest regions lie in the cavity or near/outside its portals.
3. Determine the corresponding topology and relative guest arrangement for CB8:G1(2).
4. Compare free and CB8-contained guest-pair compactness and lateral displacement using the same atom sets and geometric definitions.
5. Explain the different host-associated optical responses using the computed structural findings and supplied observations. Assess whether a concentration change alone accounts for the host contrast. Delimit what these results establish about electronic coupling or charge transfer; geometry or a vertical excitation alone does not establish emission kinetics or excitonic coupling sign.

# Submission

Submit `report/results.json` and `report/report.md` according to the schema and guide. Support structural conclusions with actual molecular calculations and mapped geometry analysis; validate minima when making minimum claims. Link genuine native inputs/outputs and analysis. Supplied stoichiometry and emission values are observations to explain, not predictions that earn points when repeated. Choose models and methods appropriate to the final claims.
