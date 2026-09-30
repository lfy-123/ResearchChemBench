# Scientific objective

Discover which bounded protonation/tautomer candidates, or mixtures, can jointly explain the measured acid/base optical and NMR response of 2a, while testing solvent and proton-reference sensitivity.

# Public inputs and scientific boundaries

Use the neutral mapped C30H20N6O4 parent and explicit candidate seed edits. Do not use former acidic/basic optimized coordinates, which are private. Preserve heavy-atom connectivity, allowing stated proton/bond tautomer rearrangements; charge must equal added proton count for this H+ exchange space. NMR is in DMSO-d6 and optical observations are in the separately reported aqueous pH conditions; compute each in its matching medium rather than treating them as the same solvent. candidate_seeds.json includes one explicit neutral lactim and four proton-site alternatives as unoptimized competitor graphs. All six required starts (including neutral_parent) must be attempted; none is preassigned as an endpoint.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **Within a fixed proton count compare like-solvated relative G. Across proton counts use a balanced proton-exchange cycle with a declared common acid/base reference and pH chemical-potential convention; raw different-charge total energies are not population rankings. Joint NMR/UV residuals use one predeclared error model per observable across all candidates.**.

This is an autonomous-research task. Formulate and test the explanation independently. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Explicit proton/tautomer candidates and conformer evidence** Construct the supplied site and tautomer alternatives, add further symmetry-distinct candidates only when motivated, and document conformers, charges and bond/proton maps without presupposing the acid/base assignment.

2. **Joint NMR/UV discrimination** Calculate matched-solvent NMR and UV predictions for all retained competitors; test individual and bounded-mixture interpretations with one uncertainty policy.

3. **Balanced speciation and robustness** Close proton-reference cycles, compare populations consistently and repeat the decisive solvent/reference/model choice. Report only assignments supported jointly by both observations.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Cellulose sensor morphology, full pH dynamics, all substituted dyes and gas-phase dianion calculations are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `candidate_registry`: Explicit proton/tautomer candidates and conformer evidence
- `joint_evidence`: Joint NMR/UV discrimination
- `thermodynamic_and_robustness`: Balanced speciation and robustness
