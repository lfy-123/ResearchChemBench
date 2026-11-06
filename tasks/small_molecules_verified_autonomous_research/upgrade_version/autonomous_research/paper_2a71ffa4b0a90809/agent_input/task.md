# Scientific question

How do catalysts A–E promote the initial activation of the isoquinoline Mukaiyama–Mannich reaction, and which molecular differences explain their principal activity contrasts? This is an explanation task: the measured yields are given; the molecular explanation must come from your calculations.

# Input files

- `data/inputs/system.json` supplies the molecular identities, amounts, mixing order and conditions. A/B are separately prepared axial isomers; their relative iodine arrangements supplement the constitution-only SMILES.
- `data/inputs/observations.json` supplies seven time points for A–E and the uncatalyzed control. Replicate uncertainties are unavailable.
- `data/README.md` describes the input inventory.

# Scope

Study the supplied catalyst series with isoquinoline, 2,2,2-trichloroethyl chloroformate and the specified ketene silyl acetal in dry THF at 193.15 K and 0.5 mol% catalyst. Choose and test your own molecular models, hypotheses and computational methods. Address catalyst-level structure–activity relationships at initial activation; a complete reaction cycle, new catalysts or exact yield prediction is outside the required scope. Distinguish prepared A/B identities from conformational populations you infer for other catalysts.

# Required results

Provide independent calculation-supported answers for these comparisons:

1. Explain the principal A/B activity contrast.
2. Explain the principal C/D activity contrast and assess which molecular differences account for it.
3. Compare C and E within the catalyst series. Assess what your quantitative molecular evidence can explain about their relative behavior and where that initial-activation explanation stops when interpreting their changing time-dependent ordering.
4. Explain the catalyst-dependent enhancements relative to the uncatalyzed reaction.

Choose the physical explanations and tests independently, and include quantitative molecular comparisons sufficient to support each answer. The cause of the C/E time crossing may remain unresolved if the scope of the actual evidence is explained; a time-dependent kinetic model is not required. A generic statement of uncertainty without the molecular comparison does not answer the question.

Define molecular composition, atom correspondence, charge and spin for every calculated object. State units, conditions and reference states for all quantities; distinguish energies, enthalpies and free energies. For association free energies, identify the matched free components/conformers, retain the raw thermal convention and report any conversion to a common 1 M standard state separately. Do not silently replace a prepared conformer by an equilibrium ensemble. Support claimed structures, connections and electronic comparisons with appropriate validity evidence.

# Submission and permitted resources

Submit `report/results.json` and `report/report.md` under `submission_schema.json` and `submission_guide.md`, with retained native calculation artifacts and reproducible analysis. Use the supplied inputs and general scientific/software documentation; hidden evaluator files, reference answers and prior run outputs are excluded.
