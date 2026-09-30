# Scientific objective

Independently determine the dominant computationally supported mechanism and free-energy span for the Zn/proline-catalyzed coupling of R1 and R2, and assess whether the computed kinetics can explain the experimentally specified use of elevated temperature. Generate and test your own mechanistic explanations without assuming a particular oxidation-state pathway or mechanism.

# Public inputs and scientific boundaries

Use `data/inputs/system.json`; IDs, connectivity, charge and multiplicity are explicit. The scored system is the isolated molecule; do not add a host or solvent. The measured objects are candidate catalyst states, intermediates, transition states, product connectivity, frequencies, connectivity validation and Gibbs free energies at a declared temperature and standard-state convention. Choose and disclose computational methods and solvent treatment. The reactants define the reaction endpoint; product connectivity may be reported as route evidence, but no product structure is supplied and it is not separately scored.

# Required scientific validation/investigation

Generate and deduplicate plausible competing mechanisms within the chemical system, including mechanistically distinct alternatives when chemically defensible. Retain identity, generation rationale and validation context per candidate. Advance candidates using stated outcome-based criteria; characterize minima and TSs, validate connectivity by IRC or a justified alternative, and calculate a comparable free-energy profile/span. Completion has two truthful outcomes: (i) a validated route and evidence-based conclusion, or (ii) a bounded-failure report with missing evidence and search coverage. Submit the corresponding branch of the local `submission_schema.json`; do not invent energies, a selected mechanism or a conclusion when validation fails. Stop when the declared candidate-generation space is exhausted or further searches yield no distinct validated states; report limitations and sensitivity.

# Deliverables

Write `report/results.json` conforming to the local `submission_schema.json`. Include the schema-required status, methods, candidate records, coverage and limitations, and, when the success branch is supported, the selected mechanism or route, span and temperature interpretation; include validation and energy evidence where available.
