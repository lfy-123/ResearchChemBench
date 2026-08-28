# Scientific objective

Determine the BSSE-corrected electronic interaction energy for each of three isolated neutral-singlet complexes: Tau+(2 Im), Tau+(2 Gly), and Tau+(2 MEA), where Tau is taurine, Im is imidazole, Gly is glycerol, and MEA is ethanolamine. Report signed energies in kJ/mol, their strongest-to-weakest ordering, and a scientifically bounded interpretation of the interaction character. The authors qualitatively motivate a donor-organized hydrogen-bonding explanation for Tau selectivity; independently test that hypothesis rather than assuming it.

# Public inputs and scientific boundaries

Use `data/inputs/chemical_system.json` as the complete identity specification. It fixes the canonical connectivity, explicit names, neutral zwitterionic Tau representation, total charge 0, singlet multiplicity, and one Tau:two-donor stoichiometry for every complex. The scored quantity is the electronic interaction energy, ΔE = E(complex) − E(Tau) − 2E(donor) + BSSE, with the sign convention stated in the report. This is an isolated-molecule electronic-energy comparison; do not interpret it as a solution free energy, extraction yield, or periodic MD result. You may choose software, model chemistry, conformer generation, and optimization settings independently, but must disclose them and apply them consistently.

# Required scientific validation/investigation

Generate a finite, explicitly described set of distinct Tau:donor:donor poses for each of Im, Gly, and MEA; deduplicate using a stated structural criterion; optimize candidates; and retain only candidates that are genuine minima under your chosen method (frequency or another justified stationary-point validation). Compute monomer and complex energies with a stated counterpoise/BSSE procedure and consistent charge/multiplicity. Advance candidates using an outcome-based rule tied to energy and validation, not a paper atom label. Stop when additional generated poses no longer produce a new validated low-energy basin under the stated coverage protocol, or report bounded failure and the explored coverage. Completion requires either three validated energies plus validation evidence for every retained structure, or a truthful bounded-failure report identifying the missing system and why it could not be validated. Report method sensitivity or conformer limitations where they affect interpretation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. It must preserve object identity for all three named complexes, include the candidate/validation record for each system, signed energies or an explicit bounded-failure branch, the ordering when all three are available, the independently tested qualitative interpretation, computational protocol, and limitations. Do not include paper text or claim numerical agreement without showing the calculation and validation basis.
