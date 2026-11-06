# Scientific question

How does propylene carbonate (PC) associate with TEA+, DED2+ and BF4−, and what can their local binding differences explain about the change in PC environment when DED salt is added to a TEA-BF4/PC electrolyte?

# Input files

- `data/inputs/objects.json` supplies complete atom-indexed molecular identities: tetraethylammonium TEA+ (C8H20N, +1), 1,4-diethyl-1,4-diazabicyclo[2.2.2]octane DED2+ (C10H22N2, +2), BF4− (−1) and PC (C4H6O3, neutral). Use the supplied closed-shell singlet states and preserve their connectivity. Coordinates are to be constructed. PC stereochemistry is unspecified; state the stereochemical choice in your models.
- `data/inputs/context.json` gives the 1 M TEA-BF4/PC background, DED-salt additions of 0, 0.1, 0.2 and 0.3 M, and the qualitative NMR/Raman observations. One added DED salt unit contains one DED2+ and two BF4−. These concentration-dependent observations are context to interpret.

# Scope

Determine the isolated gas-phase 1:1 electronic binding baseline for each ion X with one PC molecule:

`Eb(X·PC) = E(X·PC) − E(relaxed X) − E(relaxed PC)`.

Use matched electronic methods and energy conventions for each complex and its separated relaxed fragments, and report energies in kcal/mol or kJ/mol. This quantity includes fragment deformation relative to relaxed monomers; distinguish it from frozen-fragment interaction energy and association free energy. Define the sampled geometries and the evidence that supports each claimed association. No fixed orientation, conformer count or control grid is prescribed.

Use the local baseline to assess a conditional molecular explanation of the electrolyte observations. Bulk coordination distributions, the optimum addition concentration, electrode adsorption, electrochemical windows and device performance are outside this question.

Choose and justify the electronic method and molecular configurations independently.

# Required results

1. Report the binding energy and whether electronic association is favorable for each of TEA+–PC, DED2+–PC and BF4−–PC at the stated baseline.
2. Compare DED2+–PC with BF4−–PC and BF4−–PC with TEA+–PC, and state the resulting local binding-strength order with its model dependence.
3. Assess how adding DED salt could change the local PC environment. Support the interpretation with a composition- and charge-balanced PC-transfer comparison between TEA and DED, or an equivalent energy cycle. Explain what the molecular evidence establishes about competition for PC and how far it can account for the supplied concentration-dependent observations.

# Submission

Submit `report/results.json` and `report/report.md` following `submission_schema.json` and `submission_guide.md`. Link computed energies, molecular identities and physical inferences to genuine native outputs and reproducible analysis. Structures and validation support the final answers without separate process points. Consult `resources.md` for the available execution resources.
