# Scientific question

What molecular explanation accounts for the observed local regioselectivity and Z stereoselectivity of chlorosulfonylation of allenoate 6b, and how far does the calculated evidence support that explanation?

6b is ethyl 4-phenyl-2-propyl-2,3-butadienoate. It reacts with benzenesulfonyl chloride in MeCN under N2 at 40 °C (313.15 K), with Cu(acac)2 (10 mol%), 4CzIPN (1 mol%) and 427 nm irradiation. The mechanistic experiments use 0.05 M 6b and two equivalents of sulfonyl chloride. The observed product has chlorine at the benzylic terminus, phenylsulfonyl at the central allene carbon and Z alkene geometry. These are observations to explain.

# Input files

- `data/inputs/systems.json`: reactant and ligand identities, molecular graphs, atom maps, charges and spin assignments for the supplied species. Atom maps are local to each species.
- `data/inputs/observations.json`: catalyst-omission, radical-trapping, voltammetry and quenching observations.
- `data/inputs/source_facts.json`: experimental conditions and the bounded system.
- `data/inputs/author_baseline.json` and its four `data/structures/*.xyz` files: the author model identities, source coordinates, electronic/thermal table and relative-energy targets for reproduction. Coordinates are source inputs; they do not replace new evidence of model validity.

# Author baseline

The proposed route is oxidative quenching of excited 4CzIPN by CuII, reduction of sulfonyl chloride by CuI, sulfonyl-radical addition, capture by CuII(acac)Cl and reductive elimination from allyl–CuIII. The computational comparison concerns four neutral singlet, 65-atom allyl–Cu/acac/Cl minima, not transition states. C1 is the benzylic allene terminus and C3 the ester/propyl-substituted terminus; syn,syn and syn,anti labels refer to the supplied structures.

The source baseline is Gaussian 16: B3LYP-D3(BJ)/6-31G(d,p), LANL2DZ on Cu, geometry optimization and frequencies; M06/6-311+G(d,p), SDD on Cu, single-point energies with SMD MeCN. Add the low-level thermal correction once to the solution electronic energy. The authors favor C1 capture and use a roughly 2.3 kcal/mol C1 conformer difference plus structural distortion to rationalize Z selectivity. Their panel-local C4 labels denote different substituent roles; compare actual mapped atoms.

The printed SI table labels a column G273.15, but the author thermochemical temperature is unresolved. Its Gsol differences relative to C1 syn,syn are 2.292292 (C1 syn,anti), 10.712842 (C3 syn,syn) and 6.435737 (C3 syn,anti) kcal/mol. Reproduce these source-column quantities with explicit electronic and thermal components and state any reconstruction assumptions. Keep their comparison separate from the experimental 313.15 K condition; agreement at an assumed temperature does not prove an author typo.

# Scope

Focus on local C–Cl bond formation and selectivity of this substrate/reagent pair. The full photoredox cycle, other substrates and quantitative yield are outside scope. Preserve molecular identity and justify any inferred active copper coordination or electronic state. Reproduce and assess the disclosed author baseline; explain scientifically justified substitutions or unresolved protocol details.

# Required results

1. A calculation-supported explanation of the benzylic chlorine placement relative to the alternative allene terminus.
2. A calculation-supported explanation of the Z alkene geometry, connecting local molecular arrangement and relative energetics to the product configuration.
3. A conclusion about what your calculated quantities and the supplied controls establish under the reaction conditions, including any remaining distinction between thermodynamic preference and kinetic selectivity.
4. The three reproduced source-column relative solution Gibbs energies defined above, with the source-temperature ambiguity retained.

Use genuine calculations or reproducible scientific analyses with explicit atom/state mapping, conditions, units and references. Supplied observations or copied author values are not independent results. A claim of a minimum, transition state or kinetic mechanism needs evidence appropriate to that claim; no fixed calculation sequence is required.

# Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link final conclusions to native inputs, outputs and analyses; report supported, contradicted and unresolved results accurately. Use only the public task material and disclosed author baseline; do not consult undisclosed article/SI, private evaluation files or prior run archives.
