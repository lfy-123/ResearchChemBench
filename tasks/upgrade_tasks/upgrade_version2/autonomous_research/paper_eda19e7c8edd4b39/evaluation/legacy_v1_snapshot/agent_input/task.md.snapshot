# Scientific objective

Determine whether bulk vacancy energetics alone explain surface composition changes, using balanced bulk-to-surface and segregation comparisons with a distinct Ni3Al phase thermodynamic competitor.

# Public inputs and scientific boundaries

Use supplied B2 and L12 ideal prototype starts and explicit lattice_and_surface_definition.json. They are benchmark starts, not fabricated source CIFs or relaxed answers. Treat charge-neutral periodic systems with documented magnetic treatment (including fcc Ni). B2(100) both Ni and Al terminations and mixed B2(110) are mandatory. Static zero-temperature electronic energies are the primary observable, not finite-temperature rates.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **Ni-rich mu_Ni=E(fcc Ni)/atom and mu_Al=E(B2 NiAl)/formula_unit-mu_Ni. E_vac(X)=E(defect)-E(pristine)+mu_X. Atom-conserving E_seg=E(exchanged slab)-E(clean slab). Balanced transfer E_tr(X)=E(bulk V_X)+E(slab+X)-E(bulk)-E(slab). Ni3Al grand potential per formula unit=E(L12 Ni3Al)-3mu_Ni-mu_Al. Use the same converged Hamiltonian/reservoirs throughout.**.

This is an autonomous-research task. Formulate and test the explanation independently. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **Two vacancies with explicit reservoirs and supercell control** Calculate elemental/B2 reservoirs and both bulk vacancies at two sizes, with magnetic/numerical consistency and the declared Ni-rich reference.

2. **Three terminations with exchange and balanced transfer controls** Build three specified surface terminations, search top/bridge/hollow adatom placements and calculate atom-balanced exchange/transfer comparisons; preserve site/layer/count evidence.

3. **Ni3Al competitor and converged, bounded mechanism inference** Evaluate the L12 competitor, reservoir consistency and actual slab/k-point/vacuum sensitivity, then test whether bulk preference alone explains surface behavior.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: NEB barriers, coherent Ni3Al/B2 interfaces, finite-temperature precipitation kinetics and spectroscopy are optional.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `bulk_vacancies`: Two vacancies with explicit reservoirs and supercell control
- `surface_cycles`: Three terminations with exchange and balanced transfer controls
- `phase_and_convergence`: Ni3Al competitor and converged, bounded mechanism inference
