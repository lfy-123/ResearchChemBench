# Scientific question

Compare the competitive behavior of the [3,3] and [5,5] σ-sigmatropic rearrangements of 1,2-dibutadienecyclopropane (3a).

# Inputs and scope

`data/inputs/3a.xyz` specifies the complete 25-atom neutral closed-shell starting structure in Å. Atom order is fixed for reported structures. The required scope is isolated-molecule electronic structure and Gibbs energy at 298.15 K for the two named channels. Solvent models, experiments and general-web lookup are excluded.

# Required results

Provide both channel-specific activation free energies in kcal/mol relative to 3a, their assigned transition structures and validity evidence, and the resulting comparison. A valid transition state requires a stationary point with exactly one reaction-relevant imaginary frequency and a displacement or connectivity assignment to the stated channel. Report conformer references and consistent thermochemical conditions.

# Submission

Submit `report/results.json` under `submission_schema.json`, including the actual search record, candidate identities, validation evidence, methods, results and unresolved attempts. Status is `completed` for two validated channels, `partial` for one, and `failed` for neither. A `validated_success` channel requires numerical results and cited successful checks; `bounded_failure` requires actual attempt diagnostics. Auxiliary results are separate from the primary results.
