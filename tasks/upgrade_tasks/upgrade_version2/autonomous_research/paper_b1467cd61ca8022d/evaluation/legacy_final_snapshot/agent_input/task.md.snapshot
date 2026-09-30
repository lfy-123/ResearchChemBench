# Scientific objective

Compute and validate the gas-phase electronic binding energy of one Li+ ion with one neutral TFPM molecule, and characterize the lowest validated complex found within a transparent conformer/orientation search. The goal is an independently reproducible calculation of Eb, not reproduction of a paper narrative.

# Public inputs and scientific boundaries

Use `data/inputs/tfpm_system.json`. TFPM is uniquely specified by SMILES `COCCC(F)(F)F`, neutral singlet; Li is +1 singlet; the complex is +1 singlet. The system is isolated and gas phase: exclude counterions, bulk solvent, periodicity, electrochemical cells, and free-energy corrections. Use the supplied definition `Eb = E(complex) - E(Li+) - E(TFPM)` and report eV plus the sign convention. The paper, SI, and general web are unavailable; choose and justify your own method and software.

This is an autonomous-research task. Use the authorized public inputs to investigate the stated scientific objective independently. Do not read hidden evaluator files, private reference calculations, the target paper or its SI, or import their answer structures, rankings or numerical results. Structures explicitly supplied as given objects are authorized for the properties requested here; independently generate any structure that the task asks you to find.

# Required scientific validation/investigation

Propose and execute a finite candidate-generation scheme spanning distinct TFPM conformers and Li orientations, including a coverage rationale. Optimize every advanced candidate, deduplicate structures with a stated criterion, and compare only converged candidates. Validate the selected stationary point by frequencies or a justified equivalent, and use consistent fragment calculations. Completion requires documented candidate coverage, convergence, minimum validation, fragment bookkeeping, and a reproducible Eb.

# Deliverables

Submit `report/results.json` conforming to the schema. Include the candidate inventory, validation evidence, energies, Eb in eV, selected structure identity and rationale, method/software, coverage, uncertainty. Do not infer or report any paper-specific route or hidden reference value.

Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
