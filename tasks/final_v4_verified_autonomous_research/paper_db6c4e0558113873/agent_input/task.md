# Scientific question

What molecular explanation accounts for the observed local regioselectivity and Z stereoselectivity of chlorosulfonylation of allenoate 6b, and how far does the calculated evidence support that explanation?

6b is ethyl 4-phenyl-2-propyl-2,3-butadienoate. It reacts with benzenesulfonyl chloride in MeCN under N2 at 40 °C (313.15 K), with Cu(acac)2 (10 mol%), 4CzIPN (1 mol%) and 427 nm irradiation. The mechanistic experiments use 0.05 M 6b and two equivalents of sulfonyl chloride. The observed product has chlorine at the benzylic terminus, phenylsulfonyl at the central allene carbon and Z alkene geometry. These are observations to explain.

# Input files

- `data/inputs/systems.json`: reactant and ligand identities, molecular graphs, atom maps, charges and spin assignments for the supplied species. Atom maps are local to each species.
- `data/inputs/observations.json`: catalyst-omission, radical-trapping, voltammetry and quenching observations.
- `data/inputs/source_facts.json`: experimental conditions and the bounded system.

# Scope

Focus on local C–Cl bond formation and selectivity of this substrate/reagent pair. The full photoredox cycle, other substrates and quantitative yield are outside scope. Preserve molecular identity and justify any inferred active copper coordination or electronic state. Choose the explanatory models and methods independently.

# Required results

1. A calculation-supported explanation of the benzylic chlorine placement relative to the alternative allene terminus.
2. A calculation-supported explanation of the Z alkene geometry, connecting local molecular arrangement and relative energetics to the product configuration.
3. A conclusion about what your calculated quantities and the supplied controls establish under the reaction conditions, including any remaining distinction between thermodynamic preference and kinetic selectivity.

Use genuine calculations or reproducible scientific analyses with explicit atom/state mapping, conditions, units and references. Supplied observations or copied reference values are not independent results. A claim of a minimum, transition state or kinetic mechanism needs evidence appropriate to that claim; no fixed calculation sequence is required.

# Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link final conclusions to native inputs, outputs and analyses; report supported, contradicted and unresolved results accurately. Use the supplied task inputs and the tools and general documentation available in the runtime. Explain the stated experimental observations without presenting them as computational predictions.
