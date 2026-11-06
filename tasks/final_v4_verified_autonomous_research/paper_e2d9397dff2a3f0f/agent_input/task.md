# Local nitrogen coupling at a ruthenium complex

## Scientific question

For the supplied Ru–bda–Py nitrogen-containing composition, is N–N bond formation with NH3 better supported by direct attack on a locally stable structure or by local activation before attack? What molecular role does the ligand environment play?

## Input files

- `data/inputs/systems.json` defines the ligand graphs, NH3 atom map, solvent and complete model inventory: one Ru, one dianionic bda ligand, two pyridines and one additional N, giving RuC22H16N5O4 with charge +1. It supplies composition, not optimized complex coordinates or an assigned electronic state.
- `data/inputs/source_facts.json` gives conditions and model boundaries.
- `data/inputs/observations.json` supplies whole-cycle electrolysis observations and identifies the distinction between the Py computational models and NH3-ligated experimental catalysts. These observations are context, not local kinetic measurements or prediction targets.

## Scope

Study the intact Ru–bda–Py local nitrogen model and neutral NH3 in MeCN at 298.15 K. Establish chemically defensible coordination and electronic states rather than inferring oxidation state or spin from net charge. Choose the local activation mechanism and computational methods independently. The supplied bcs analogue is available if useful; a paired analogue survey is not required.

Report Gibbs activation energies in kcal/mol with a 1 M solution standard state. Define a unimolecular local-activation barrier as G(transition state) − G(local initial state), and a direct-association barrier as G(transition state) − G(local initial state) − G(separated NH3). Apply concentration and thermal corrections consistently and only once. Keep electronic path energies distinct from Gibbs energies and from electron/proton-reservoir thermodynamics. The supplied 0.50 V versus Fc+/0 and MeCN pH reference of 15.1 do not themselves define chemical activation barriers.

The scope is local molecular reactivity. Whole-cycle N2 production, turnover frequency, diffusion coefficients and the global rate-determining step are outside this task.

## Required results

1. Determine the Gibbs activation costs for direct NH3-mediated N–N formation and for a chemically justified local activation of the initial nitrogen-containing complex. Establish the physical states and connections needed to interpret those barriers.
2. Determine whether N–N formation is accessible after the local activation, using computed approach/path and product evidence. Report any resolved additional electronic barrier over the examined range and the limits of that path evidence.
3. Explain which local route is better supported by the combined activation and onward-reaction results, including how the initial bonding environment affects access to the nitrogen site. State what this establishes about local reactivity.
4. Determine the ligand environment's role in the resulting N–N/proton-transfer chemistry using atom-resolved structural or electronic evidence.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link the native inputs, outputs and analysis that support each final result. State identities, physical definitions, units, uncertainty and the limits of the modeled system. Unsupported guesses, copied observations and workflow completion earn no scientific points. Use only the supplied public inputs and available tools; general scientific/software documentation is allowed. Private evaluation files and prior verification archives are not public resources.
