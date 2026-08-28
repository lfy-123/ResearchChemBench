# Scientific objective

For neutral N-allyl gem-difluoroenamine Int1, independently determine the lowest validated free-energy route between the thermal crossed [2+2] cycloaddition and the alternative aza-Claisen rearrangement. Report the overall Gibbs free-energy barrier from Int1 for each route, their difference, and the conclusion supported by the calculations. If the evidence does not discriminate the routes, state that limitation rather than inventing a mechanism.

# Public inputs and scientific boundaries

The public molecule is in `data/inputs/int1.smi`, with neutral charge and connectivity encoded there; `problem_definition.json` defines solvent, temperature, standard state, pathway endpoint definitions and observables. The boundary is one isolated Int1 molecule in implicit toluene at 298.15 K. Do not use the paper, SI or general web. Choose software, model chemistry, conformer strategy and execution order independently. No product structure, TS geometry or mechanism answer is supplied.

# Required scientific validation/investigation

Explore and deduplicate plausible conformers and stationary-point candidates for both explicitly defined pathways. For every candidate retained for comparison, preserve an identity, starting structure, endpoint/connectivity assignment and validation record. Use frequencies to distinguish minima and TSs, investigate relevant electronic states, and validate critical TS connectivity with IRC or a justified alternative. Compute comparable solution-standard-state Gibbs barriers and report coverage. Completion requires either validated barriers for both pathways or a bounded-failure report that identifies the unvalidated route and the evidence needed. Stop when no new distinct lower validated candidate is found after the chosen search expansion, and document that stopping rule and limitations.

# Deliverables

Submit `report/results.json` following the schema. Use the public pathway identifiers `cycloaddition` and `aza_claisen` in the pathway records and identify every selected stationary point by a neutral structural/coordinate description. Include the independent search plan, candidate-level records, selected pathway barriers in kcal/mol when available, difference, evidence-based conclusion, uncertainty and completion status. Partial discovery is acceptable only with truthful candidate-level records and a bounded-failure explanation; unavailable barriers and comparisons must be reported as null rather than invented numbers.
