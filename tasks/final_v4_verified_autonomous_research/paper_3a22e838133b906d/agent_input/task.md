# Scientific question

What molecular redistribution can explain the local B/O/P structural changes between neutral phosphonate–borane 2a and its deethylated anion in the lithium salt, and how far does a molecular model account for the crystal observations?

## Input files

- `data/inputs/objects.json` supplies atom-indexed identities for neutral 2a (C22H36BO3P), its deethylated anion (C20H31BO3P−), Li+ and MeCN. The supplied starting states are closed-shell singlets. Atom IDs are local to each object.
- `data/inputs/observations.json` supplies experimental crystal B–O and corresponding P–O distances in angstrom, their measurement uncertainties, and the salt's observed crystal association. These are facts to explain.

## Scope

Study the local structure of this neutral/deethylated pair, with any approximation explicitly mapped to the full identities. Choose a defensible molecular representation and computational evidence for that question. The salt is an inversion-related crystal dimer with two bridging Li ions and two MeCN molecules per Li; that observation does not prescribe a computational dimer or establish solution aggregation. Separate isolated molecules from Li-containing or crystal environments. A simplified model does not automatically give the geometry of the full salt. No reaction pathway, kinetic prediction, battery property or full association ladder is requested.

## Required results

- Report calculated B–O and B-bound P–O lengths for comparable neutral/anion models, their signed changes (anion minus neutral), and the anionic dealkylated P–O length relative to the B-bound P–O. Determine the structural responses from your calculations; the experimental directions alone are not a computed explanation.
- Give a computationally supported electronic explanation of the local bond changes, separating the B-interacting, dealkylated and remaining alkoxy oxygens. Explain what the actual electronic evidence adds beyond the reported distances.
- Compare the calculated changes with the crystal changes quantitatively. State what is explained and what remains attributable only provisionally to omitted environment or representation, with evidence appropriate to any specific causal claim.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the actual inputs, native outputs, geometries, mapped numerical results and analysis supporting each final answer. Report length units, model charge/spin, environment and uncertainty. Choose the necessary methods and comparisons; there is no required hypothesis count or search matrix. Only final scientific results receive points. Follow `resources.md` for permitted resources.
