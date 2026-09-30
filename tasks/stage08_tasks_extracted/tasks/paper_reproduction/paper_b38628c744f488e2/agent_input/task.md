# Scientific objective

Independently determine the single-methanol hydrogen-bonding response of 2,3,5,6-tetramethyl-1,4-benzoquinone across its radical-anion and dianion states. Compute ΔH1, ΔH2, ΔH_HB = ΔH2 − ΔH1, carbonyl-oxygen NAC1/NAC2, and OH···O distances, and explain what the validated calculations support within this molecular model.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that reduction increases the basicity of the quinone carbonyl oxygen and therefore strengthens hydrogen bonding to methanol. They attribute the reported contact geometry to methyl sterics, which may favor an out-of-plane approach.

**Candidate route or mechanism.**
For the one-methanol complexes, examine hydrogen bonding from methanol OH to a carbonyl oxygen, including an out-of-plane contact as a proposed candidate geometry. Compare the radical-anion and dianion states through the isolated-fragment-referenced complexation enthalpies and carbonyl-oxygen natural atomic charges.

**Discriminating evidence.**
Use optimized structures and frequency checks to establish minima, OH···O distances and atom mappings to characterize the contact, and consistent complex and fragment enthalpies plus population analysis to test the redox-dependent strengthening claim.


# Public inputs and scientific boundaries

Use `data/inputs/q_ch3_4_neutral.smi`, `methanol.smi`, and `system_definition.json`. The SMILES files define neutral connectivity but do not encode coordinates or a preferred contact. Assign a stable atom map when generating charged fragments and retain it in every complex and isolated-fragment calculation. Compute one-methanol complexes and isolated fragments in the listed charge/multiplicity states, with an acetonitrile continuum at 298.15 K and 1 atm. Choose and justify the electronic-structure method, conformer strategy, population analysis, and thermochemical convention. Do not use paper/SI/general web information and do not assume a preferred contact geometry.

# Required scientific validation/investigation

Formulate chemically distinct contact classes before optimization, explain why they span a reasonable hypothesis space, and compare them through a finite generation and deduplication protocol. Retain candidate identity and report optimization and frequency evidence for every advanced candidate. For a successful result, validate at least one minimum per state with frequency evidence, use consistent isolated-fragment references, identify the contacted methanol H and quinone O by atom map, and provide a structure file reference or unambiguous structural description for each selected candidate. Completion requires validated results for both states and the derived ΔH_HB, or a truthful bounded-failure report containing per-state attempted candidates, diagnostics, coverage, unresolved requirements, and next step. Stop when the candidate set is exhausted under the disclosed protocol and no new distinct contact class is found, or when a documented technical limit prevents completion; state which condition occurred.

# Deliverables

Write `report/results.json` conforming to `submission_schema.json`. Select the `success` branch only when both state results are validated; otherwise use the `bounded_failure` branch and do not fabricate numerical placeholders. Do not claim certainty beyond the submitted search and validation evidence.
