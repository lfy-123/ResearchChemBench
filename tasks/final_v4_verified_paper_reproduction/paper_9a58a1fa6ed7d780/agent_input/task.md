## Scientific question

How does internal BN substitution change the low-energy singlet excitations and optical intensity distribution of BN-AkFlu relative to CC-AkFlu, and what molecular electronic explanation supports that difference?

## Author baseline for reproduction

The source uses Gaussian16 B3LYP/6-311G(d,p) for molecular geometries and electronic calculations and Multiwfn for hole–electron analysis (SI pp3,39). FigureS27 explicitly describes a single gas-phase molecule. TablesS11 and S14 give BN-AkFlu density descriptors and vertical transitions, while TableS15 gives CC-AkFlu transitions; TablesS21–S22 give geometries. The authors link BN insertion to altered frontier levels and excitation character. Main text describes a bright S4 for a broader BN-Flu discussion, while BN-AkFlu TableS14 places the large oscillator strength at S5; preserve molecule/root distinctions. Reproduction must disclose unresolved extraction/descriptor disagreement rather than force matching labels.

Interpret and reproduce the disclosed author approach within this task’s bounded question. Explain justified substitutions and distinguish replication, new checks and disagreement. Source agreement is not a substitute for valid evidence.

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

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the actual native inputs/outputs and analysis supporting each conclusion, with units, state identities and limitations. Method choice is independent unless a reproduction baseline is disclosed above. Evidence and research records support the final results and receive no separate process points. Use the supplied inputs, available scientific tools and general scientific/software documentation; private evaluation files and undisclosed source answers are not task inputs.
