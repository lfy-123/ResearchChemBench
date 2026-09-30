# Scientific objective

Independently determine the gas-phase electronic activation barriers for Bergman cycloaromatization of the three supplied triazolyl enediyne–amino-acid reactants EDY 15, EDY 16 and EDY 17, and infer what electronic and geometric features explain differences among them. Compute ΔE‡ = E(TS) − E(reactant) in kcal/mol and assess whether a common explanation is supported by the calculations.

# Public inputs and scientific boundaries

Public files `data/inputs/edy_15.xyz`, `edy_16.xyz`, and `edy_17.xyz` are uniquely labeled SI reactant geometries with atom identities and Cartesian coordinates in Å. Each is neutral, singlet and gas phase. EDY 15, 16 and 17 are fixed named systems; their terminal substituent identities are D–D, D–A1 and A1–A1 respectively, where D is para-methoxyphenyl and A1 is para-cyanophenyl. The target is the intramolecular Bergman cycloaromatization TS and its electronic barrier. No author route, expected trend, reference value, paper software or ordered protocol is supplied.

# Required scientific validation/investigation

Plan and execute an independent finite conformer/TS search for each named reactant. Deduplicate candidates by connectivity and geometry, optimize them, and retain only reactants with zero imaginary frequencies and TSs with exactly one cyclization-associated imaginary frequency. Validate connectivity to the cyclized product by IRC, constrained displacement, or a justified equivalent. Stop after each molecule has a validated lowest barrier among the reported search set; if not achieved, report bounded failure, attempted candidates, coverage and the precise limitation. Propose plausible electronic/geometric explanations and discriminate them using computed observables rather than assuming a mechanism.

# Deliverables

Submit `report/results.json` following the schema. Include status, per-molecule energies and structures or bounded failures, validation evidence, method/search details, coverage, comparative ordering when supported, proposed explanations and a limitation statement. Completion is three validated barriers or an honest bounded-failure report.
