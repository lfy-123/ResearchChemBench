# Scientific question

What structural features of the specified prochiral rotaxane can differentiate its two enantiotopic para sites in the first electrophilic amination, and what can substrate-level calculations establish about local site susceptibility and the limits of an enantioselectivity inference? This is an explanation task; the reaction observations are known context.

# Input files

`data/inputs/system.json` defines substrate S (neutral, singly threaded [2]rotaxane, C48H60F6N2O7), its complete macrocycle/axle connectivity, alpha/beta site numbering, dibenzyl azodicarboxylate R, CHCl3/25 °C reaction conditions, and the monoamination observation. Alpha-C4 and beta-C4 are the compared para positions. No particular three-dimensional pose or catalytic model is supplied.

# Scope

Investigate the substrate's solution structure and relative aryl-site response. Preserve its two covalent components and mechanical threading; an unthreaded mixture is a different system. Choose your own conformations, hypotheses, electronic descriptors and methods. State how each solvent or reduced model relates to the experimental system. A single local structure does not establish a solution ensemble or exchange rate.

The required explanation is at substrate level for the first amination only. Subsequent di-amination, kinetic resolution and time-dependent enrichment are outside scope. Explicit catalyst complexes, a complete catalytic pathway, reaction barriers, absolute mechanical stereochemical assignment, quantitative enantiomer ratio and time-course fitting are not required.

# Required results

1. Give a calculation-supported structural account of S and explain whether its modeled three-dimensional organization produces different para environments. Identify the interactions or equivalent physical effects supporting your account.
2. Report a numerical, consistently defined comparison of the two para-site responses and infer whether, and under which modeled circumstances, it supports different susceptibility to electrophilic amination. Distinguish a descriptor from a rate or activation barrier.
3. Explain what the structural/site results and any relevant symmetry relationships of your calculated states imply about local first-amination site susceptibility and whether a net enantiomeric excess can be inferred from substrate-only evidence. Identify the supported inference and the specific missing physics needed for stronger claims.

A supported equivalence or alternative explanation is legitimate when its physical model and actual computational evidence justify it. Distinguish equivalence within a conformation from any justified ensemble average; an assumed symmetry alone is insufficient. Preserve site mapping, charge/spin, quantity definitions, units and uncertainty. Validate claimed minima or reaction paths in proportion to the claim; no fixed number of searches or conformers is prescribed.

# Submission and permitted resources

Submit `report/results.json`, `report/report.md` and `research/` using the existing schema and guide. Use the supplied public identities and available computational tools. Link final conclusions to actual inputs, native outputs and analyses; report unsuccessful or unresolved work honestly.
