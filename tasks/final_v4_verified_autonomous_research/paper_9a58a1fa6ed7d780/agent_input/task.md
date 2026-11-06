## Scientific question

How does internal BN substitution change the low-energy singlet excitations and optical intensity distribution of BN-AkFlu relative to CC-AkFlu, and what molecular electronic explanation supports that difference?

## Input files

- `data/inputs/objects.json` defines the complete atom-indexed graphs of BN-AkFlu5a (C22H14B2N2) and CC-AkFlu5b (C26H14), each a neutral 40-atom singlet. Atom IDs are local to each graph.
- `data/inputs/context.json` identifies the pair and isolated gas-phase setting.
- `submission_schema.json`, `submission_guide.md` and `resources.md` describe submission records and available resources.

## Scope

Compare these two complete isolated molecules at their respective ground-state equilibrium geometries. Define singlet vertical excitation energies relative to each S0 state in eV and oscillator strengths as dimensionless quantities. Keep orbital eigenvalue gaps distinct from excitation energies. This finite molecular comparison does not ask for other BN scaffolds, solid-state packing, emission yields, nonradiative rates or charge mobility.

## Required results

1. Give the lowest singlet excitation energy of each molecule and identify the principal optically bright transition in its low-energy singlet spectrum. Report that transition's energy and oscillator strength with physical state assignments.
2. Determine the distribution of intensity between the lowest excitation and other low-energy transitions for each molecule. Explain how the absorption pattern changes on substitution.
3. Explain the excitation difference using calculated electronic structure and physical correspondence between the molecular states. State which part of the comparison is supported across your chosen representations and which depends on unresolved state or model assumptions. Use quantitative evidence appropriate to your explanation; no particular orbital descriptor or decomposition is prescribed.

Choose methods and supporting calculations independently. Molecular identity, geometry validity, convergence and state matching support the final claims; they are not separate scored milestones.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the actual native inputs/outputs and analysis supporting each conclusion, with units, state identities and limitations. Choose computational methods independently. Evidence and research records support the final results and receive no separate process points. Use the supplied inputs, available scientific tools and general scientific/software documentation; private evaluation files are not task inputs.
