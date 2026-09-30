# Scientific objective

For the two explicitly defined isolated organic molecules AQ and EQ, independently determine whether their electronic structures differ in a way that is relevant to low-energy intersystem crossing. Calculate and compare the first singlet–triplet gap ΔE_ST = E(T1) − E(S1), HOMO–LUMO gaps, dipole moments, and frontier-orbital localization, then state what those calculations do and do not support. Formulate your own physical explanation from the computed evidence.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that cyano functionalization of the anthraquinone-derived molecule strengthens its acceptor character, increases intramolecular charge transfer, and changes the singlet–triplet separation in a way that may promote intersystem crossing. Treat this as a claim to test against the supplied AQ and EQ calculations.

**Candidate route or mechanism.**
A candidate comparison is donor-localized HOMO to acceptor-localized LUMO character, with the cyano-substituted EQ molecule representing the stronger-acceptor case. Consider whether the AQ-to-EQ electronic change and any associated charge-transfer character provide a consistent explanation for differences in the requested observables.

**Discriminating evidence.**
Use the computed ΔE_ST, HOMO–LUMO gap, dipole, and spatial localization of frontier orbitals to distinguish the proposed acceptor-strengthening and charge-transfer interpretation from explanations that do not predict the observed comparison. Validate the interpretation on the isolated monomers and report method or conformer sensitivity.

# Public inputs and scientific boundaries

Use `data/inputs/molecular_systems.json`. It defines each molecule's constitution, formula, neutral charge (0), and singlet multiplicity (1). Construct and report an exact machine-readable structure for each. The scored object is the isolated gas-phase AQ and EQ monomer pair. Solvent, DPPC, ultrasound, ROS chemistry, bacteria, and biological performance are excluded. Dimers or other aggregate models are optional, unscored extensions and must be labeled as such. Report electronic energies in eV, ΔE_ST in eV, dipoles in Debye, HOMO–LUMO gaps in eV, and qualitative orbital localization.

# Required scientific validation/investigation

Plan and execute a reproducible calculation without relying on the paper or general web. Generate a declared conformer set, deduplicate it using a stated rule, optimize candidates, and select final structures using a stated energy/stationarity criterion. Verify charge and multiplicity and validate the ground-state stationary point by frequencies or an equivalent check. Compute excited states sufficient to identify S1 and T1 consistently, show ΔE_ST arithmetic and units, and inspect frontier-orbital localization. Report method sensitivity or a justified limitation. Completion requires validated structures and requested observables for both systems, or a bounded-failure report containing the attempted scope, evidence, blocked fields, and scientific limitation. Stop when the declared search/validation scope is exhausted and no unresolved validation issue remains; report coverage and do not invent a discovery story.

# Deliverables

Submit `report/results.json` using `submission_schema.json`. Include exact structures, computational provenance, candidate and validation context, per-system values, comparison, an evidence-based conclusion, and limitations. If completion is bounded failure, use the failure branch and explain it; do not insert placeholder or fabricated numbers. Provide output/log references or hashes sufficient for audit.
