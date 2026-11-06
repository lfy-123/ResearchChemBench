# Scientific question

How do the static molecular hyper-Rayleigh responses of helicenes 1, 3, 5 and 7 differ, and what do their response tensors establish about the relation between molecular structure and nonlinear response?

## Input files

- `data/inputs/systems.json` defines the four complete mapped molecular graphs, formulas, neutral charge and singlet state. No optimized geometry or response ordering is supplied.
- `data/inputs/problem_facts.json` defines the isotropically averaged HRS observable, optional depolarization ratio and static limit.

## Scope

Treat complete gas-phase neutral singlet molecules at zero optical frequency. The four formulas are C30H18, C36H20, C48H24 and C52H24 for 1, 3, 5 and 7. Define beta_HRS = sqrt(<beta_ZZZ²> + <beta_XZZ²>), with an isotropic orientational average and explicit laboratory axes. Report beta_HRS in 10^-30 esu and state the tensor derivative convention and unit conversion. A Cartesian component or beta_total is a different observable. Finite-frequency response, further derivatives, packing and bulk device performance are outside scope. Choose your geometries, response methods and checks appropriate to the comparison.

## Required results

1. Calculate and report the static isotropic beta_HRS of each of the four complete molecules.
2. Determine each molecule's dipolar/octupolar response character from calculated tensor or equivalent physical evidence, defining any invariants or polarization quantities used.
3. Quantify the signed response changes for 1→5 and 5→7 and determine whether these structural extensions give a monotonic relation. Compare the 3-versus-7 difference to these two changes, with uncertainty appropriate to any fine ordering.
4. Explain what the calculated response and molecular structure establish about the origin and limits of the structure–response relation. Distinguish a supported physical association from a uniquely isolated causal descriptor.

## Author baseline for reproduction

Reproduce and assess the disclosed baseline: unconstrained B3LYP/6-31G(d) ground-state optimization with frequency checks, followed by CAM-B3LYP/6-31+G(d) static response (Gaussian 09 in the source). Main Eqs. 15–18 define the isotropic HRS average, DR and dipolar/octupolar decomposition; DR=<beta_ZZZ²>/<beta_XZZ²>, <beta_ZZZ²>=(9/45)|beta_J=1|²+(6/105)|beta_J=3|², and <beta_XZZ²>=(1/45)|beta_J=1|²+(4/105)|beta_J=3|². The molecular response tensor must use consistent units and conventions. SI Table S9 contains additional functional comparisons, which are context rather than a required sweep. The full source family is broader than the four identities here. Document source ambiguities and physically justified substitutions and their effects on the reproduction. No fixed torsion perturbation is required.

## Submission

Submit `report/results.json` and `report/report.md` under the supplied schema and guide, with final values, comparisons and interpretation linked to actual native response outputs and reproducible averaging. Include the molecular identity, medium, state and uncertainty relevant to each claim. The evidence supports final-result scoring; calculation stages and reporting effort earn no separate credit. Use the available runtime tools and general documentation. Undisclosed target-paper/SI content, other modes, private evaluators and prior verification archives are not public task inputs.
