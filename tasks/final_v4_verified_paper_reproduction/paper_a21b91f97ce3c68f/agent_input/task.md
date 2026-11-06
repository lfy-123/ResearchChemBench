# Conformation and tin–carbon scalar coupling

## Scientific question

How do axial and equatorial conformations affect one-bond 119Sn–13C scalar coupling in the three supplied stannyl heterocycles, and what electronic explanation accounts for the similarities or differences between the scaffolds?

## Input files

`data/inputs/problem_context.json` lists the identity files `pair_6_identity.json`, `pair_7_identity.json` and `pair_13_identity.json`. They define complete neutral SnBu3 derivatives 6 (C17H36OSn), 7 (C16H34O2Sn) and 13 (C16H34S2Sn), retaining all three n-butyl chains. In each atom map, Sn is atom 5, its ring carbon is 14, and the directly bonded butyl carbons are 4, 6 and 10. The files define connectivity, not conformer endpoints or coupling values.

## Scope

Compare physically justified axial/equatorial forms of these three complete molecules, with a declared molecular environment and consistent isotope, sign and response convention. Treat total J in Hz separately from the Fermi-contact contribution, reduced coupling K and any empirical scaling. State the actual relativistic Hamiltonian treatment independently of basis-set naming. The result concerns conformer-specific coupling; a population average needs independent support for the populations. Choose the electronic analysis and methods independently. Do not infer a universal coupling law from three scaffolds.

## Author baseline for reproduction

The authors used CREST/GFN2-xTB conformer sampling and selected low-energy axial/equatorial structures. Gaussian16 GD3-B3LYP/def2-TZVPP gas-phase optimization/frequency calculations and NBO3.1 were followed by B3LYP spin–spin response with a TZP-ZORA basis, NMR=(SpinSpin,Mixed,ReadAtoms) and Integral=NoXCTest. The main text explicitly calls the Hamiltonian nonrelativistic despite the basis name; later relativistic wording is inconsistent and must not be silently used to relabel the calculation. They relate antiperiplanar donation into σ*(ring C–Sn) to coupling and apply an empirical factor −1.419 to some absolute predictions. This factor is a reported calibration, not a universal physical correction or an acceptance tolerance. SI S5–S6 identifies scaffolds 6/7/13 and defines the butyl quantity as the average over the three directly bonded carbons. Fixed torsion/distance interventions are not required source protocol; design any additional tests independently.

Reproduce this disclosed baseline or substantiate a physically applicable substitute and its consequences. Source values and assignments are comparison references; copied values alone earn no credit. Additional comparisons remain your choice.

## Required results

1. For each scaffold, calculate the total ring 119Sn–13C J in both conformations and determine its conformational dependence using a consistent signed or magnitude convention.
2. Separately calculate the three directly bonded butyl-carbon couplings, their arithmetic mean and the conformational dependence of that mean for each scaffold.
3. Determine which response contributions account for the ring-coupling contrast in each scaffold, retaining non-dominant terms when distinguishing a component from total J.
4. Explain the comparison across scaffolds using computed electronic interactions and coupling-response evidence. Determine whether a proposed common electronic descriptor accounts for all three pairs and state the supported scope of the explanation.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the native inputs, outputs and analysis that support each final result. State identities, physical definitions, units, uncertainty and the limits of the modeled system. Unsupported guesses, copied observations and workflow completion earn no scientific points. Use only the supplied public inputs and available tools; general scientific/software documentation is allowed. The full target article/SI, private evaluation files and prior verification archives are not public resources. Any author baseline explicitly disclosed in this task is authorized.
