# Scientific question

What molecular redistribution can explain the local B/O/P structural changes between neutral phosphonate–borane 2a and its deethylated anion in the lithium salt, and how far does a molecular model account for the crystal observations?

## Input files

- `data/inputs/objects.json` supplies atom-indexed identities for neutral 2a (C22H36BO3P), its deethylated anion (C20H31BO3P−), Li+ and MeCN. The supplied starting states are closed-shell singlets. Atom IDs are local to each object.
- `data/inputs/observations.json` supplies experimental crystal B–O and corresponding P–O distances in angstrom, their measurement uncertainties, and the salt's observed crystal association. These are facts to explain.

## Scope

Study the local structure of this neutral/deethylated pair, with any approximation explicitly mapped to the full identities. Choose a defensible molecular representation and computational evidence for that question. The salt is an inversion-related crystal dimer with two bridging Li ions and two MeCN molecules per Li; that observation does not prescribe a computational dimer or establish solution aggregation. Separate isolated molecules from Li-containing or crystal environments. A simplified model does not automatically give the geometry of the full salt. No reaction pathway, kinetic prediction, battery property or full association ladder is requested.

## Author baseline

The author comparison uses isolated singlet methyl models: replace both B-bound cyclohexyl groups by methyl and the ethoxy groups by methoxy, removing one O-methyl group in the anion. The charges are 0 and −1. Gaussian 16 C.01 B3LYP-D3(BJ)/6-311++G(2d,p) optimizations were checked by frequencies (Scheme 2; SI S78–S81). The reported neutral B–O and B-bound P–O lengths are 1.696 and 1.517 Å; the anionic B–O, B-bound P–O and dealkylated P–O lengths are 1.579, 1.558 and 1.485 Å. The authors ascribe part of the model/crystal mismatch to omitted Li coordination. Reproduce this disclosed baseline with actual calculations, or justify a scientifically comparable substitution, retaining separate source and computed results.

## Required results

- Report the five baseline bond lengths above from your calculations, as well as the neutral-to-anion signed B–O and B-bound P–O changes and the relative anionic P–O lengths. The five calculated lengths support the structural-response and bonding conclusions; individual author-value matching windows are not used for scoring.
- Give a computationally supported electronic explanation of the local bond changes, separating the B-interacting, dealkylated and remaining alkoxy oxygens. Explain what the actual electronic evidence adds beyond the reported distances.
- Compare the calculated changes with the crystal changes quantitatively. State what is explained and what remains attributable only provisionally to omitted environment or representation, with evidence appropriate to any specific causal claim.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the actual inputs, native outputs, geometries, mapped numerical results and analysis supporting each final answer. Report length units, model charge/spin, environment and uncertainty. Choose the necessary methods and comparisons; there is no required hypothesis count or search matrix. Only final scientific results receive points. Follow `resources.md` for permitted resources.
