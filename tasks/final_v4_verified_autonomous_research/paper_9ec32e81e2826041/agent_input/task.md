# Scientific question

What molecular configurations and electronic response of Z-cAACCy can explain the optical contrast between its two crystal samples, and what can an isolated-molecule account establish about their shared yellow solution?

## Input files

- `data/inputs/system.json` provides the full 80-atom C35H43NZn graph, atom identities and bonds, including N-Dipp and cyclic groups. It defines a neutral singlet complex without coordinates or an assigned conformation.
- `data/inputs/observations.json` provides approximate diffuse-reflectance edges for colorless and yellow crystals and the observation that both give the same yellow solution. These are facts to explain.

## Scope

Compare orientations of the carbene five-membered ring and zincafluorene five-membered ring within the complete molecule, including near-orthogonal and more-coplanar possibilities. Identify configurations by their mapped ring-plane angles; determine their molecular stability and optical response without assigning a color from the label alone. Use gas-molecular singlet vertical excitations at justified ground-state geometries. Define the lowest singlet transition, oscillator strength and accepting-orbital composition consistently across configurations. A normalized Zn 4p contribution is the sum over the entire 4p angular subspace in the LUMO, reported in percent; state its population definition and establish comparability if using an alternative.

Thermal comparisons use matched compositions and conditions near room temperature. Crystal reflectance edges are different observables from molecular vertical transitions; solution populations and rates are not directly measured by the supplied colors. Other zinc complexes, luminescence lifetimes, triplet photocatalysis and full crystal calculations are outside the required scope.

## Required results

1. For the distinct molecular orientations, report the lowest singlet vertical excitation energy (eV), oscillator strength (dimensionless) and normalized LUMO Zn 4p contribution (%), with structural and state assignments that make the comparison meaningful.
2. Quantify the signed excitation contrast and explain how molecular orientation and orbital interactions relate to the observed optical contrast, including the role of Zn if supported.
3. Determine the thermal accessibility of the configurations from a signed conformer free-energy difference (kJ/mol), its temperature/reference and relevant thermal or noncovalent sensitivity. Explain whether a population preference is resolved.
4. Assess what the molecular findings imply for the shared yellow solution and where they cease to determine crystal or solution behavior.

## Submission

Submit `report/results.json` and `report/report.md` using the existing schema and guide. Link final findings to actual native calculations and reproducible analyses, preserving molecular/state mapping, physical definitions and claim-specific validity evidence. Structures and calculation stages earn no independent points. Use the supplied task inputs and the tools and general documentation available in the runtime. Define and justify the computational settings used for the stated physical question.
