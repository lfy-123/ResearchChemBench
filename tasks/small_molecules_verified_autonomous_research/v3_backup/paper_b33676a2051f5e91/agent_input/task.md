# Scientific question

Starting from the supplied oxygen-centered radical Int-3 derived from sec-butylbenzene, what local chemistry explains acetophenone formation, and which of the two supplied carbon–carbon beta-scission channels is kinetically favored? This is a local explanation task; product structures are supplied and must be supported by independently calculated formation evidence.

# Input files

`data/inputs/local_cleavage_structures.json` and its SDF files define Int-3 (C10H13O, charge 0, doublet), the contextual hydroperoxide Int-2 (C10H14O2, charge 0, singlet), and the two candidate product sets: acetophenone plus ethyl radical, and propiophenone plus methyl radical. The structures share explicit atom maps. SDF coordinates are two-dimensional depictions, not optimized geometries. No absolute substrate stereochemistry is experimentally assigned.

`molecular_identity.json`, `sec_butylbenzene.sdf` and `sec_butylbenzene.xyz` retain the original experimental inventory and starting-substrate context. `reaction_conditions.json` distinguishes experimental oxidation conditions from the local comparison convention (MeCN, 298.15 K, 1 atm). `experimental_observations.json` supplies the acetophenone observation and controls; no competing-ketone ratio or quantitative coproduct inventory is supplied. Hydroperoxide detection by NMR concerned an ethylbenzene analogue, not direct experimental identification of this sec-butylbenzene-derived Int-2. Int-2 and Int-3 are supplied mechanistic models.

# Scope

The required calculations start at Int-3. Compare its two local beta-scission routes with consistent molecular inventory, atom mapping, charge/spin, thermochemistry and physically connected precursor references. Account for the ketone and alkyl-radical coproduct in each channel. State how independently optimized precursor conformers relate to a common energy zero.

Formation of Int-2 or Int-3, peroxide-bond cleavage, benzylic hydrogen abstraction, generation of chlorine/hydroperoxyl radicals, bismuth photophysics, singlet-oxygen alternatives, catalyst turnover and polymer degradation are outside the required scope. Int-2 provides chemical context only. Distinguish local formation preference from an overall oxidation profile, experimental branching ratio or isolated yield.

# Required results

1. Explain the mapped bond changes and local accessibility of acetophenone formation from Int-3, reporting its activation Gibbs free energy from a physically connected precursor.
2. Explain the local formation pathway and accessibility of propiophenone plus methyl radical from Int-3, with mapped bond changes and reaction-path connection evidence. Report its local activation Gibbs free energy and the barrier difference on the same precursor reference. Determine and explain the supported local preference and its relation to the acetophenone observation.

Choose conformations, reaction hypotheses and computational methods independently. Verify minima, transition structures, reactive modes and chemical connections as appropriate to the claims. The supplied product drawings, an isolated saddle or product stability alone do not establish either outcome. Report units, conditions, energy definitions, electronic states and uncertainty, with recoverable native evidence.

# Submission and permitted resources

Submit `report/results.json` and `report/report.md` using the existing schema and guide. Use supplied public inputs and available computational tools; retain independently generated native inputs, outputs and analysis supporting every final inference.
