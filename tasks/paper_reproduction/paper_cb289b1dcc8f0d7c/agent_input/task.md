# Scientific objective

Independently plan and execute calculations for the neutral BQ1–BQ7 boron(III) 8-hydroxyquinoline complex series in the supplied manifest. Test the authors' qualitative hypothesis that halogen substitution, especially heavy halogens, changes S1/T1 spin–orbit coupling and intersystem crossing and thereby helps explain fluorescence-yield differences. Report S0, S1, T1 and T2 state energies, S1–T1 gaps, S1/T1 SOC, ISC and fluorescence rates, calculated fluorescence yield, and a chemically reasoned comparison with the reported solution fluorescence trends.

# Public inputs and scientific boundaries

Use only `data/inputs/bq_series.json` and your own calculations. Every member is a neutral monomer (charge 0), with singlet S0/S1 and triplet T1/T2; B is bonded to two phenyl ipso carbons and the N/O atoms of one deprotonated 8-hydroxyquinolinate. Substitution positions and formulas are explicit in the manifest. The default boundary is an isolated monomer with implicit toluene; a BQ7 dimer in water is optional and must be separately identified. Do not use the paper, SI, general web, or hidden evaluator files. Software, functional, basis, relativistic treatment and execution order are your choice. Do not treat experimental values as computed targets.

# Required scientific validation/investigation

Generate a reproducible 3D starting structure for each named member, document atom identity and charge/multiplicity, and optimize the requested states. Validate each reported stationary point with an appropriate convergence/stationarity check and report failures. Establish that energies are compared to a common S0 reference and that units and state labels are consistent. Compute or estimate SOC and rates with a documented method; retain per-member provenance and uncertainty. The investigation is complete when every member has either all requested observables with validation evidence or an explicit bounded-failure record identifying the missing observable and attempted alternatives. Stop after the seven named monomers and, if attempted, the single explicitly defined BQ7 dimer; do not expand the chemical set.

# Deliverables

Write `report/results.json` following `submission_schema.json`. Include a per-member record with the explicit manifest ID, status, validation evidence, provenance (raw/log paths or hashes where available), numerical observables with units, calculated yield, notes, trend/conclusion text, limitations, and a completion status. For a fully successful member use the complete-observables branch. If any requested observable cannot be obtained, use that member's bounded-failure branch, list every attempted numeric observable that exists, list each missing observable by name, and explain the failure and alternatives in validation/provenance/notes; never use fabricated numeric placeholders. The top-level status is `complete` only if all seven members are complete, otherwise `bounded_failure`.
