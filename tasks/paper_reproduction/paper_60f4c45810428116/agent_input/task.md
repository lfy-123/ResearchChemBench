# Scientific objective

Determine the calculated one-electron dissociative reduction potentials, in V versus the ferrocene/ferrocenium reference couple, for the explicitly defined sulfur-containing precursors 1a and 1h. In reproduction mode, test the authors' qualitative hypothesis that a thiophenyl leaving group has unusually low reducibility and can delay formation of the reactive carbenoid; do not assume that hypothesis is correct. The measured endpoints are two potentials and their ordering/difference.

# Public inputs and scientific boundaries

`data/inputs/species.json` defines every species by SMILES, formal charge, multiplicity, reaction role, and (for the metal reference) explicit coordination semantics. 1a is benzyl chloromethyl sulfide, `ClCSCc1ccccc1` interpreted as connectivity `C(Cl)H2-S-CH2-Ph`; 1h is the corresponding `PhS-CH2-S-CH2-Ph` precursor. The products are the carbon-centered neutral radicals plus chloride or benzenethiolate anion for 1a/1h, and Fc/Fc+ are the reference states. Each Fc state is one bis(eta5-cyclopentadienyl)iron sandwich complex, not separated formal fragments; generate its three-dimensional coordination geometry from this identity. THF solution and 298 K are the physical boundary. The task scores potentials versus Fc/Fc+; it does not score a particular geometry, conformer, software, or method. The author's qualitative route is the hypothesis to test, not a required protocol.

# Required scientific validation/investigation

Independently choose and document a defensible computational thermochemistry route. Generate and deduplicate any conformers or electronic states you use, optimize the named states, and validate minima with frequencies or an explicitly justified equivalent. Check charge, multiplicity, atom identity, fragment stoichiometry, and the sign/convention of the one-electron dissociative reaction. Report method, solvation, thermal convention, reference construction, convergence, and limitations. Completion requires a reproducible value or a bounded-failure report for both named reactions; stop when both endpoints have validated calculations and additional conformers/states no longer change the reported conclusion under the stated convergence criterion, or report the limitation and coverage.

# Deliverables

Submit `report/results.json` matching the schema. It must contain per-reaction values or a truthful bounded-failure branch, validation evidence, method details, and a final comparison of 1a versus 1h.
