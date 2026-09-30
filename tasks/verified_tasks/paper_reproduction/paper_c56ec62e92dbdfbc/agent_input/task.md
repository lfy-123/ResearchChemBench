# Scientific objective

Locate and validate the lowest credible R- and S-forming pathways, report their Gibbs activation free energies at 298.15 K relative to separated neutral singlet 4i + 1a + 2a, calculate ΔΔG‡ = ΔG‡(S) − ΔG‡(R), and conclude which configuration is favored and whether the proposed event is enantiodetermining.

# Author-provided scientific guidance

Independently test the authors' qualitative hypothesis for the enantioselective oxa-Pictet–Spengler reaction defined in `data/inputs/system.json`: a monomeric molecule of chiral CBSCA catalyst 4i organizes a catalyst-bound oxocarbenium species, followed by intramolecular aromatic C–C bond formation, and this C–C-forming event controls whether (R)-3a or (S)-3a is produced.

# Public inputs and scientific boundaries

The only scientific inputs are `system.json` and the three XYZ files it names. `system.json` gives every component's identity, atom numbering, connectivity, formal charge, multiplicity and catalyst stereochemistry, as well as the known product identity and reaction conditions. XYZ atom order is authoritative and matches the bond lists. Treat one molecule each of 4i, 1a and 2a as the separated-reactants reference. Model a monomeric catalyst in solution; molecular sieves, explicit bulk solvent and catalyst aggregates are outside the required quantum model. Do not assume any transition-state geometry, favored configuration, conformer ranking, numerical barrier, software, density functional, basis set or solvation model from the source paper.

The measured quantities are the activation free energies of the lowest validated R- and S-forming pathways, their signed difference in kcal/mol, the product configuration of each path, stationary-point character, reaction-path connectivity and the identity of the selectivity-determining event. Use a defensible electronic-structure and thermal-correction model consistently across the compared candidates and state standard-state conventions.

# Required scientific validation/investigation

Generate distinct catalyst conformers and distinct catalyst–substrate binding arrangements capable of the proposed oxocarbenium formation and intramolecular arene attack. Enumerate both product configurations and any distinct facial/transient-stereocenter variants that can lead to them. Give every candidate a stable ID; deduplicate candidates by molecular connectivity, product configuration, forming-bond atom pair, catalyst binding topology and geometry similarity. Advance candidates using an explicitly justified energetic and structural rule, retaining any structurally distinct low-energy family that could change the R/S ordering.

For every candidate used in the final R/S comparison, provide a transition-state geometry, total charge and multiplicity, the number and value of imaginary frequencies, and evidence that the imaginary mode contains the intended bond-making/proton-transfer motion. Demonstrate bidirectional connectivity to chemically appropriate neighboring states by IRC, QRC with endpoint optimization, or an equivalently documented path-following test. Optimize relevant adjacent minima and place all reported energies on the same separated-reactants reference. Check conformational coverage around the best candidate for each product configuration and perform at least one meaningful sensitivity check (for example, a higher-level single point, alternative solvation treatment, or thermochemical treatment). Report individual validation evidence for each compared candidate.

Completion requires at least one fully validated R-forming and one fully validated S-forming pathway, no unadvanced distinct candidate family within the investigator's declared competitive energy window that could reverse the ordering, a common-reference ΔΔG‡, and an assessment of whether another step on either lowest pathway has a higher barrier. Stop when new sampling rounds produce no new distinct competitive family and all retained families have either been validated or rejected for a stated scientific reason. Record each considered route variant with a stable hypothesis ID, description, disposition and scientific rationale. If resources end first, use the bounded-failure branch and report generated/advanced/validated coverage, the unresolved families and why no defensible final ordering can be claimed; do not fabricate success values.

Set `status` explicitly to `success` or `bounded_failure`. A successful main comparison may coexist with failed extra attempts. For an unsuccessful candidate, set `validation.status` to `failed` or `partial`, provide `disposition` and `failure_reason`, and omit unavailable TS geometry, atom-pair, frequency or connectivity fields. Candidates used in the R/S comparison must have complete validation; their IDs must resolve uniquely. In a bounded failure, retain valid incomplete numerical work in `partial_results`, without fabricating success-only fields.

Generic limitations or uncertainty prose is optional and unscored. Keep the required scientific identities, computed evidence, coverage and actual failure diagnostics. Additional scientifically motivated calculations are allowed and should be separated from the primary results; optional work not performed needs no disclaimer.

All common-reference energies must be atom balanced. Include any detached coproducts with their actual stoichiometric coefficients when comparing a catalyst-bound structure with separated 4i + 1a + 2a; retain the reference species and conversion formula in the computational evidence.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. For a successful investigation it must contain method/reference definitions, search coverage, per-candidate identity and validation records, selected R/S pathway IDs and barriers, signed ΔΔG‡, favored configuration, step comparison, conclusion. For bounded failure it must contain the same method and coverage record, all investigated candidate records, unresolved scientific blockers; success-only numerical and ordering fields must be omitted.
