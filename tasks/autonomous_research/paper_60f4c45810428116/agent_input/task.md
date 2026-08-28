# Scientific objective

Compute and compare the one-electron dissociative reduction potentials, in V versus the ferrocene/ferrocenium reference couple, for two explicitly defined organosulfur precursors: 1a and 1h. Report both endpoint values, their ordering, and what the comparison supports about relative ease of electron transfer under the stated model boundary. Do not infer or reproduce an author-specific mechanism; this is an independent calculation and interpretation task.

# Public inputs and scientific boundaries

`data/inputs/species.json` defines every species by isomeric SMILES, formal charge, multiplicity, and reaction role. 1a is benzyl chloromethyl sulfide, with connectivity `Cl-CH2-S-CH2-Ph`; 1h is `PhS-CH2-S-CH2-Ph`. Their dissociative one-electron products are the corresponding neutral carbon-centered radicals plus chloride or benzenethiolate anion. Ferrocene and ferrocenium are the reference states. THF solution and 298 K define the physical boundary. The target observable is potential versus Fc/Fc+, not a particular structure or software result.

# Required scientific validation/investigation

Plan and execute an independent, reproducible calculation. Enumerate and deduplicate the conformers/electronic states actually considered, optimize named states, and validate minima with frequencies or a justified equivalent. Verify charge, multiplicity, fragment stoichiometry, reaction sign, and reference-electrode convention. Completion requires validated endpoints for both named reactions, or a bounded-failure report identifying exactly which endpoint or validation failed. Stop when both endpoints are converged under the reported criterion and added candidates no longer alter the comparison, or document coverage and limitation.

# Deliverables

Submit `report/results.json` matching the schema, including both reaction records when available, validation/coverage evidence, method details, and an independent final comparison.
