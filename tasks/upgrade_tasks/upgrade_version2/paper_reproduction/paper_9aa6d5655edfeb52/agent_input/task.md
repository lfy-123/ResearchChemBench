# Scientific objective

What molecular explanation can be supported for the absorption and emission of arene-fused o-carborane2a in THF solution? Investigate the relevant electronic/structural description and establish which assignments are robust or remain unresolved.

# Author-provided scientific guidance

The source Gaussian09 B3LYP/6-31G(d,p), IEF-PCM(THF) optimizations and TDDFT calculations are described on SI p19, with2a excitations on p22. Authors discuss arene-localized versus charge-transfer behavior and environment-sensitive cage C-C motion, and compare2a with C(2)-I rather than its brominated precursor1a (main pp3–4). Their solid-state/AIE interpretation is beyond an isolated solution molecule calculation. Reproduce the disclosed2a molecular baseline or justified substitutions; the old mandatory1a/cage-motion benchmark was a later extension, not author evidence for pure fusion causation.

Interpret and reproduce the disclosed author approach within this task’s bounded question. Explain justified substitutions and distinguish replication, new checks and disagreement. Source agreement is not a substitute for valid evidence.

# Public inputs and scientific boundaries

The source compound2a is C18H20B10, a neutral singlet with a12-vertex closo cage and the supplied arene-fusion connectivity. Cage adjacency encodes a multicenter cluster topology, not an assertion that every cage edge is an ordinary localized two-center bond. Use the same molecule under THF solution conditions; the source measured absorption and emission quantities are public facts. Molecular conformations and excited states are to be investigated, not supplied as answers.

Read `data/inputs/objects.json` for atom-indexed chemical identity and the other supplied input files for known facts. Generate and justify the models needed for your investigation.

The task concerns solution molecular photophysics. Do not claim the solid-state539nm band, aggregation-induced emission, fluorescence quantum yield or the causal effect of fusion relative to a different molecule from these finite results alone. Precursor1a differs by Br/H composition and is not a chemically matched geometry-only control.

# Required scientific validation/investigation

Develop and execute a scientifically justified investigation that answers the question within these boundaries. You choose the explanations or models to examine, their number, the methods, searches, comparisons and evidence needed, and how the investigation changes in response to findings. Justify the adequacy and limits of the evidence for your claims. AR chooses its route independently. PR must reproduce the disclosed author baseline or justify scientifically grounded substitutions; additional investigations are independently designed. Neither mode is required to recover an author outcome or follow a fixed candidate/control grid.

Distinguish observed absorption and emission conditions and define calculated electronic states/geometry. A state-character or relaxation claim needs supporting electronic/structural evidence, with limitations from method, sampling and solvent model. Finite-state calculations cannot alone identify an aggregate or predict a photoluminescence yield.

A well-supported negative or unresolved answer is eligible for scientific credit. Explain what the evidence establishes and what it leaves open. Nonconvergence, missing calculations or a self-declared uncertainty flag do not establish non-identifiability. Report genuine model/basin collapse with the corresponding evidence.

# Deliverables

Submit `report/results.json` under the structured submission contract and a readable `report/report.md`. Preserve actual inputs, native outputs, identity/state mappings, analysis code and execution records. Quantitative evidence must be recoverable from linked artifacts. Record concise decisions, failures, revisions, resource use and limitations; consult `submission_guide.md` and `resources.md`.
