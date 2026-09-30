# Scientific objective

Compute and validate the gas-phase electronic binding energy of one Li+ ion with one neutral TFPM molecule, and characterize the lowest validated complex found within a transparent conformer/orientation search. The goal is an independently reproducible calculation of Eb.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that Li+ is stabilized in TFPM through complementary coordination involving the ether oxygen and a fluorine site, producing a chelating complex.

**Candidate route or mechanism.**
Prioritize testing candidate arrangements in which Li+ can contact both O and F, including geometries that could close a chelate-like ring, while retaining competing arrangements with only one principal contact for comparison. Treat these as candidate explanations to test during the search.

**Discriminating evidence.**
Use optimized relative electronic energies and binding energies, stationary-point validation by harmonic frequencies or an equivalent check, and direct geometric analysis of Li–O and Li–F contacts and ring topology to distinguish the proposed dual-contact arrangement from alternatives.

# Public inputs and scientific boundaries

Use `data/inputs/tfpm_system.json`. TFPM is uniquely specified by SMILES `COCCC(F)(F)F`, neutral singlet; Li is +1 singlet; the complex is +1 singlet. The scored system is the isolated molecule pair in the gas phase: do not add counterions, bulk solvent, periodicity, electrochemical cells, or free-energy corrections. Use the supplied definition `Eb = E(complex) - E(Li+) - E(TFPM)` and report eV plus the sign convention. Choose and justify your own method and software.

# Required scientific validation/investigation

Generate and test a finite candidate set spanning distinct TFPM conformers and Li orientations, including a coverage rationale. Optimize every advanced candidate, deduplicate structures with a stated criterion, and compare only converged candidates. Validate the selected stationary point by frequencies or a justified equivalent, and use consistent fragment calculations. Completion requires documented candidate coverage, convergence, minimum validation, fragment bookkeeping, and a reproducible Eb. Stop when the declared generation scheme is exhausted and additional starts no longer produce a distinct candidate, or report bounded failure with the exact unresolved limitation.

# Deliverables

Submit `report/results.json` conforming to the local schema. Include the candidate inventory, validation evidence, energies, Eb in eV, selected structure identity and rationale, method/software, coverage, stopping condition, uncertainty, and limitations.
