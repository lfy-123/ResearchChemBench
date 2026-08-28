# Scientific objective

Test the authors' qualitative hypothesis that Li/F co-substitution followed by Si substitution changes local coordination and lowers local symmetry in Fe3+-activated ZnAl2O4. Independently plan and execute calculations for UC-1, UC-2 and UC-3, then report named local bond lengths/angles and whether the structural trend supports that hypothesis. The candidate class is substitution-site and charge-compensation arrangements in a 56-atom periodic spinel model.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`. ICSD 94156 is the unique host record. UC-1 is undoped; UC-2 contains one Li and one F substitution; UC-3 adds one Si substitution to UC-2. Fe3+ activation must be represented explicitly and documented. The measured objects are nearest-neighbor bonds and three-center angles at each substituted site, with atom identities retained. The paper's qualitative route is only a hypothesis; no target values, rankings or calculation recipe are supplied.

# Required scientific validation/investigation

Generate all chemically distinct arrangements allowed by the stated substitutions and your declared charge/magnetic model, deduplicate by symmetry or graph/connectivity equivalence, and retain candidate IDs. Relax each advanced candidate with a documented periodic electronic-structure method. A candidate is validated only when electronic and force/geometry convergence criteria are met and the final structure has no unreported atom loss or composition change. Extract the named local observables independently from the final geometry and include extraction definitions. Completion requires one validated candidate for every state plus a sensitivity/coverage report; if convergence or resource limits prevent this, report bounded failure with attempted candidates and evidence. Stop when all declared inequivalent arrangements are exhausted or when a documented, reproducible coverage/stopping rule is reached.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include state and candidate identities, method, convergence evidence, observables, comparisons, coverage, limitations, and a conclusion about the qualitative hypothesis. Never claim agreement from an unvalidated structure.
