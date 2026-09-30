# Scientific objective

Determine how the enantioselective oxa-Pictet–Spengler reaction defined in `data/inputs/system.json` proceeds and what controls formation of (R)- versus (S)-3a. Independently propose and discriminate plausible catalytic mechanisms, locate and validate the lowest credible pathways to both product configurations, report their Gibbs activation free energies at 298.15 K relative to separated neutral singlet 4i + 1a + 2a, calculate ΔΔG‡ = ΔG‡(S) − ΔG‡(R), and identify the favored configuration and selectivity-determining event within the investigated scope.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that a monomeric chiral CBSCA catalyst organizes an oxocarbenium species, and that intramolecular aromatic C–C bond formation controls whether (R)-3a or (S)-3a is produced.

**Candidate route or mechanism.**
Evaluate a catalyst-bound oxocarbenium pathway in which arene attack forms the new C–C bond, including the relevant facial alternatives leading to the two product configurations. The authors associate this event with concerted phenol deprotonation and subsequent rearomatization, so those connected steps should be compared when assessing which event controls selectivity.

**Discriminating evidence.**
Use validated transition-state and neighboring-minimum structures, path-following connectivity, common-reference free energies for both configurations, conformational coverage, and comparison of subsequent rearomatization barriers. Structural interaction analysis and catalyst-distortion comparisons can help test the proposed origin of the preference.


# Public inputs and scientific boundaries

The only scientific inputs are `system.json` and the three XYZ files it names. `system.json` gives every component's identity, atom numbering, connectivity, formal charge, multiplicity and catalyst stereochemistry, as well as the known product identity and reaction conditions. XYZ atom order is authoritative and matches the bond lists. Treat one molecule each of 4i, 1a and 2a as the separated-reactants reference. Model a monomeric catalyst in solution; molecular sieves, explicit bulk solvent and catalyst aggregates are outside the required quantum model. No mechanism, transition-state geometry, favored configuration, conformer ranking, numerical barrier, software or model chemistry is supplied.

The measured quantities are activation free energies for the lowest validated R- and S-forming routes, their signed difference in kcal/mol, stationary-point character, reaction-path connectivity, product configuration, and the identity of the event responsible for selectivity. Use a defensible electronic-structure and thermal-correction model consistently across compared candidates and state standard-state conventions.

# Required scientific validation/investigation

Define plausible catalytic hypotheses from the supplied structures and reaction class, including materially distinct bond-forming, ion-pair/binding and proton-transfer arrangements that could alter stereochemical outcome. Generate distinct catalyst conformers and catalyst–substrate complexes for each advanced hypothesis. Enumerate both product configurations and facial/transient-stereocenter variants. Give each hypothesis and candidate stable IDs; deduplicate candidates by mechanism class, molecular connectivity, product configuration, forming/breaking atom pairs, catalyst binding topology and geometry similarity. State why hypotheses/candidates are advanced or rejected, while retaining structurally distinct low-energy families that could alter the R/S ordering.

For every candidate used in the final comparison, provide a transition-state geometry, charge and multiplicity, imaginary-frequency count/value, intended-mode assignment and bidirectional connectivity to appropriate neighboring states by IRC, QRC plus endpoint optimization, or equivalent documented path following. Optimize relevant adjacent minima and put all energies on the same separated-reactants reference. Check conformational coverage around the best candidate in each product channel and perform at least one meaningful model-sensitivity check. Per-candidate validation evidence is required; a global assertion is insufficient.

Completion requires at least two materially distinct mechanistic hypotheses to be considered, at least one fully validated R-forming and one fully validated S-forming pathway, no unadvanced distinct candidate family within the declared competitive window that could reverse the ordering, a common-reference ΔΔG‡, and comparison of the highest barriers along the lowest R and S routes. Record each hypothesis with a stable ID, its mechanistic description, whether it was advanced or rejected, and the scientific rationale; record the same disposition rationale for each candidate. Stop when additional hypothesis/candidate generation and sampling rounds produce no new distinct competitive family and every retained family is validated or rejected for a stated reason. If resources end first, use the bounded-failure branch and report hypotheses, generated/advanced/validated coverage, unresolved families and why a final ordering or mechanism cannot be defended; do not fabricate success values.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. A successful report contains method/reference definitions, hypothesis and candidate coverage, per-candidate identity/validation, selected R/S pathways and barriers, signed ΔΔG‡, favored configuration, selectivity-determining event, conclusion and limitations. A bounded-failure report contains method, hypotheses, coverage, all investigated candidates, unresolved blockers and limitations; success-only numeric and ordering fields must be omitted.
