# Scientific question

Why do the two successive Mallory photocyclizations of precursor 1-cis lead to the supplied product 2, and what thermodynamic and site-specific electronic factors distinguish plausible alternative closure sites? This is an explanation task using an isolated-molecule model; the observed product connectivity is supplied.

# Input files

`data/inputs/precursor_1_cis.xyz` is a displaced starting geometry of the neutral singlet C30H22 precursor (52 atoms; coordinates in angstrom). Use the one-based atom order as the precursor mapping and preserve an explicit correspondence in generated species. The geometry is not a validated minimum. `data/inputs/molecular_structures.json` and `product_2.sdf` supply the observed C30H18 product graph and its correspondence to precursor atom indices. The SDF contains a two-dimensional depiction, not an optimized geometry. Product identity is an input; competing sites and their explanations remain to be established.

# Scope

Compare chemically plausible first-closure sites and sequential second-closure sites, allowing changes of hydrogen inventory associated with aromatization. Choose your own hypotheses, candidate structures and methods. Compare energies only at a common physical definition and stoichiometry, or use an explicitly balanced reaction reference. Endpoint energetics and orbital/site evidence support a selectivity rationale; distinguish this from excited-state kinetics or a predicted branching ratio.

Explicit solvent, iodine, propylene oxide, crystal packing, excited-state dynamics and device properties are outside the required calculation scope.

# Required results

1. State the first-closure regioisomer preference with numerical, same-composition energetic comparisons and an independent site-specific electronic or structural explanation.
2. Establish the sequential second-closure preference with comparable quantitative energetics and its independent site explanation on the appropriate scaffold.
3. Explain the supported ordering of cyclization and aromatization events, accounting for atoms and hydrogen changes without treating unrelated absolute energies as reaction energies.
4. Relate the supported sequence to the supplied product graph with explicit atom/hydrogen correspondence, and define the extent to which the comparisons support selectivity. Restating the supplied product identity is not an independent scientific result.

Report quantity definitions, electronic states, conditions, standard states and conformer treatment. Geometries, frequencies and any claimed reaction-path evidence must justify the scientific assertions made, without a fixed software, search count or mandatory transition-state inventory.

# Submission and permitted resources

Submit `report/results.json` under `submission_schema.json`. Record generated chemically distinct candidates, mappings, results and recoverable native evidence in the existing interface; identify unavailable quantities and unresolved alternatives. Use only supplied public inputs and available computational tools. Private evaluation files and archived answers are excluded.
