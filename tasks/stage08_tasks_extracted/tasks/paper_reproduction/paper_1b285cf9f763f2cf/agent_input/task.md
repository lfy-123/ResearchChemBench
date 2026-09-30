# Scientific objective

Determine, by independent computational investigation, how the stated Li/F and Li/F/Si substitutions alter local geometry in Fe3+-activated ZnAl2O4 spinel. Establish whether any defensible structural trend supports reduced local symmetry and explain competing site/defect hypotheses. The research object is the finite set of chemically distinct substitution and charge-compensation arrangements in three 56-atom periodic states.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that Li/F co-substitution followed by Si substitution changes local coordination around the substituted sites and increases local distortion, providing a structural basis for reduced local symmetry in Fe3+-activated ZnAl2O4.

**Candidate route or mechanism.**
Compare the undoped UC-1 environment with the Li/F co-substituted UC-2 environment and the further Si-substituted UC-3 environment. The proposed structural changes include locally different Li–O and Si–O coordination, a distinct Al–F environment relative to Al–O coordination, and altered three-center angles; these are candidate interpretations to test across plausible site and charge-compensation arrangements.

**Discriminating evidence.**
Use independently relaxed, converged periodic structures to compare substituted-site nearest-neighbor bond lengths and named three-center angles across UC-1, UC-2, and UC-3. Assess whether systematic bond-length changes and angle splitting or shifts are reproducible across validated candidates and distinguish local-symmetry reduction from site, defect, or model sensitivity.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`. ICSD 94156 uniquely defines the ZnAl2O4 normal-spinel host. UC-1 is undoped, UC-2 has one Li and one F substitution, and UC-3 adds one Si substitution. Fe3+ activation must be represented explicitly and documented. The scored system is the isolated periodic solid-state model; do not add a host, solvent, or other external environment. Report nearest-neighbor bond lengths and named three-center angles with atom identities retained.

# Required scientific validation/investigation

Generate plausible site and charge-compensation hypotheses, enumerate the chemically distinct arrangements within the stated substitutions, deduplicate them using declared symmetry/connectivity criteria, and preserve candidate IDs. Ask which hypotheses and pathways are supported by the calculations rather than assuming a route in advance. Relax advanced candidates using a documented periodic method. Validate each candidate by electronic and force/geometry convergence, composition and structural integrity, then extract local geometry using a reproducible definition. Completion requires one or more validated candidates per state, explicit comparison of hypotheses, coverage accounting, and a limitation report. Stop after the declared inequivalent candidate space is exhausted or under a documented reproducible stopping rule; bounded failure is acceptable only with attempted candidates and reasons.

# Deliverables

Write `report/results.json` conforming to the local `submission_schema.json`. Include hypotheses, candidates, validation evidence, observables, coverage, limitations, and an evidence-based conclusion. Do not invent a discovery narrative when direct calculations are inconclusive.
