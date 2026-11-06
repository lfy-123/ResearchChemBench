## Scientific objective

How does the homogeneous Ir(III)-catalyzed annulation of 3-(phenanthren-4-yl)-1H-indazole with diphenylacetylene form the specified diaza[6]helicene, and how does the specified axially chiral nitrile–phosphine oxide ligand influence helicity selection and the relative kinetic difficulty of the connected product-forming chemistry?

Develop an evidence-supported molecular account of this specific reaction, not merely an isolated energy, structure or ligand descriptor. The observed product connectivity and major helicity are starting observations; the scientific unknowns are how the reaction produces them, what role the ligand plays, and how stereochemical selection relates to the chemical difficulty of reaching product.

## Public inputs and scientific boundaries

Use `data/inputs/system.json` for the question and inputs PI1–PI6. Use `data/inputs/identities.json` for explicit molecular graphs, the starting indazole tautomer, the axial ligand enantiomer, the Cp substituents and the observed product identity. Atom IDs in that file are local graph labels. Build your own geometries; the axial sign specifies only an enantiomer, not a preferred shape.

- The organic partners are 3-(phenanthren-4-yl)-1H-indazole and diphenylacetylene. The latter is present at two equivalents.
- The precursor is the chloride-bridged Ir(III) dimer with 1-tert-butyl-2,3,4,5-tetramethylcyclopentadienyl ligands. Use the specified axial nitrile–phosphine oxide ligand and the stated silver triflate, water and dichloromethane context.
- The reaction conditions and loadings are in PI4: 50 °C, Ar, 36 h, substrate 0.10 mmol in 1.0 mL dichloromethane. The isolated product has 82% yield, 91% ee and M helicity. These endpoint facts do not identify an elementary step or determine a unique mechanism.
- The comparison without the chiral ligand is relevant to understanding its role in this same molecular system. Distinguish a controlled model comparison from a claim about an unprovided experimental rate or yield.

Address connected molecular product-forming chemistry and stereochemical competition within this system. Do not turn the task into substrate/catalyst generality, photophysical-property prediction, precursor activation-release kinetics, an experimental time-course fit or a requirement to close every catalyst-regeneration step. No complete network or exhaustive conformer/pathway search is required. Explain what your chosen molecular boundaries omit; do not treat an assumed catalytic species as an observed identity.

## Required investigation

Propose testable explanations and choose models and informative computational investigations that can discriminate among relevant possibilities. Actually execute research and retain its inputs, outputs, logs and analysis. A literature-only discussion, a proposed workflow without execution, or agreement with a reference value is insufficient.

Use your evidence to develop a connected account of product formation and ligand-dependent catalytic behavior, the M-versus-opposite-helicity competition, and the relationship between stereochemical selection and the relative difficulty of product-forming transformations. These outcomes must not disappear into an optional descriptor analysis. You choose the hypotheses, physical effects, methods and extent of testing; there is no fixed number of hypotheses, tests or calculations and no prescribed autonomous mechanism.

Track whether evidence supports, revises or leaves each explanation unresolved. State chemical identity, atom/charge/state mappings, numerical definitions, units, conditions and model limitations. Validation follows your claims: transition-state claims require appropriate stationary-point and reactant/product-connectivity evidence; a kinetic-model claim requires its equations, observation mapping and identifiability assessment. Do not label a geometric guess as a validated transition state or infer an experimental turnover law from a local energy comparison alone.

If author-provided scientific guidance is publicly supplied, execute and critically assess that disclosed baseline, documenting fidelity, ambiguities and justified substitutions in the investigation method/outcome records and readable report. Otherwise choose your approach independently. Undisclosed author mechanisms, descriptors and workflows are never mandatory, and a scientifically supported alternative is not a failure merely for differing from an author account.

## Deliverables and stopping conditions

Follow `submission_schema.json` and the unchanged `submission_guide.md`. Submit `report/results.json`, `report/report.md` and the actual research artifacts under `research/`. Link stable hypothesis, investigation, evidence and conclusion IDs to real artifact files; include failed attempts and error logs rather than inventing results. Explain your chosen models, actual execution and resource use in the readable report.

Separate research completion from question resolution using the guide's status fields. Stop when actual evidence supports the scope of the conclusions you claim and the remaining uncertainty is stated. Honest partial or execution-failed work is acceptable; careful completed research may still leave the question unresolved. Inconclusive work does not automatically establish a mechanism.

The shared evaluation allocates 60 points to hypothesis quality, informative investigation/model choices, reliable execution, evidence-driven decisions and reproducibility/uncertainty; 20 points to a supported connected formation/relative-kinetic-difficulty account; and 20 points to supported ligand-dependent helicity control. Resolution credit depends on evidence for those outcomes, not status labels or author agreement. There is no requirement to match hidden numerical energies or use a particular descriptor, and no fixed CPU, GPU, memory, walltime or job-count quota.
