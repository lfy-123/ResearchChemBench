## Scientific question

What ground-state electronic description and metal–ligand bonding picture are supported for the supplied nickel carbaporphyrin complex, and what do they imply about assigning nickel oxidation?

## Input files

- `data/inputs/complex4_identity.json` gives all 165 atom identities and adjacency for neutral C87H72Cl2N2NiO, including the two axial chlorides. Adjacency defines chemical identity; it does not assign bond order, electron distribution or an optimized structure.
- `data/inputs/problem_context.json` states the scientific boundary and input limitations.

## Scope

Retain the full composition, charge and connectivity. Investigate the isolated molecule's electronic state and bonding under a clearly stated model. Use consistent geometry/state and electronic-energy references when comparing alternatives; label any thermal or medium extension separately. The required answer concerns this complex only, without water-reactivity pathways, aromaticity, complete spectroscopy or rates.

## Required results

1. Determine the ground-state spin/electronic description and explain how the evidence distinguishes it from credible competing descriptions. Provide quantitative state evidence with units and references; specify the finite scope of the conclusion.
2. Describe the bonding character of the axial nickel–chloride and equatorial nickel–macrocycle interactions separately, supported by calculated electronic structure.
3. Give a justified formal valence account and determine how far the electronic evidence identifies a physical nickel oxidation state. Distinguish orbital composition, spin density and atomic population charge from formal oxidation bookkeeping.

Choose the calculations and representations needed for these conclusions. A computed geometry and electronic convergence are supporting evidence, not independently rewarded deliverables; no specific initial guess or convergence outcome is prescribed.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the actual native inputs/outputs and analysis supporting each conclusion, with units, state identities and limitations. Choose computational methods independently. Evidence and research records support the final results and receive no separate process points. Use the supplied inputs, available scientific tools and general scientific/software documentation; private evaluation files are not task inputs.
