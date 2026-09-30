# Scientific objective

For neutral N-allyl gem-difluoroenamine Int1, independently determine and compare the lowest validated free-energy pathways for the thermal crossed [2+2] cycloaddition and the alternative aza-Claisen rearrangement. Generate and test your own candidate explanations and pathways. Report the overall Gibbs free-energy barrier from Int1 for each pathway, their difference, and the conclusion supported by the calculations. If the evidence does not discriminate the pathways, state that limitation rather than inventing a mechanism.

## Author-provided scientific guidance

**Author hypothesis or claim.** The authors proposed that the catalyst-free thermal cycloaddition can proceed by a stepwise open-shell-singlet mechanism rather than a concerted closed-shell event.

**Candidate route or mechanism.** Their candidate sequence begins with intramolecular attack at C1 to form an open-shell diradical, followed by C–C closure to the cycloaddition connectivity. They considered C2 attack leading to aza-Claisen imine connectivity as the competing pathway and examined alternative electronic-state descriptions.

**Discriminating evidence.** Compare consistently referenced solution free-energy profiles for the candidate pathways, including relevant conformers and electronic states. Use frequency analysis, wavefunction-stability or spin diagnostics, and IRC or equivalent connectivity evidence to distinguish validated minima and transition states and to test the proposed stepwise sequence.

# Public inputs and scientific boundaries

The public molecule is in `data/inputs/int1.smi`, with neutral charge and connectivity encoded there; `problem_definition.json` defines solvent, temperature, standard state, pathway endpoint definitions and observables. The scored system is one isolated Int1 molecule in implicit toluene at 298.15 K; do not add another molecule or explicit solvent. Do not use the paper, SI or general web. Choose software, model chemistry, conformer strategy and execution order independently.

# Required scientific validation/investigation

Explore and deduplicate plausible conformers and stationary-point candidates for both explicitly defined pathways. For every candidate retained for comparison, preserve an identity, starting structure, endpoint/connectivity assignment and validation record. Use frequencies to distinguish minima and TSs, investigate relevant electronic states, and validate critical TS connectivity with IRC or a justified alternative. Compute comparable solution-standard-state Gibbs barriers and report coverage. Completion requires either validated barriers for both pathways or a bounded-failure report that identifies the unvalidated route and the evidence needed. Stop when no new distinct lower validated candidate is found after the chosen search expansion, and document that stopping rule and limitations.

# Deliverables

Submit `report/results.json` following the schema. Use the public pathway identifiers `cycloaddition` and `aza_claisen` in the pathway records and identify every selected stationary point by a neutral structural/coordinate description. Include the independent search plan, candidate-level records, selected pathway barriers in kcal/mol when available, difference, evidence-based conclusion, uncertainty and completion status. Partial discovery is acceptable only with truthful candidate-level records and a bounded-failure explanation; unavailable barriers and comparisons must be reported as null rather than invented numbers.
