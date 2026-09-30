# Scientific objective

Determine whether metal–ligand orbital mixing is needed to explain the Ir–Ir bonding response, using full and exactly truncated dimers, fixed fragment definitions and distance/twist interventions.

# Public inputs and scientific boundaries

Use Egan_identity.json and egan_identity.json for the true two-Ir dimers. Each ligand binds one Ir through its two iminoxolene N,O pairs; the ester oxygens are not assigned as donors in this dimer. Full Egan has four tert-butyl groups per ligand; truncated egan replaces exactly these with H and retains the ethylene-dianthranilate tether. Opposite local helicities define the A,C starting arrangement, but no final symmetry or distance is imposed. The former mononuclear cis-alpha/beta IrCl objects are excluded. retained_heavy_mapping.json gives the exact 36-atom retained map per ligand; apply it independently to A/B copies.

Use `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **For neutral doublet fragments A=(ligand)Ir and B=(ligand)Ir: E_int=E_AB-E_A(frozen)-E_B(frozen); E_def=sum[E_fragment(frozen)-E_fragment(relaxed)]; E_assoc=E_int+E_def, kcal/mol. Keep fragment charge/spin, basis/BSSE and relativistic definitions identical. This operational decomposition is not a unique partition of metal–metal versus ligand pi bonding.**.

This is an autonomous-research task. Formulate and test the explanation independently. Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.

# Required scientific validation/investigation

1. **True dimers, electronic states and paired truncation** Assemble full/truncated A,C dimers independently, test singlet/BS/triplet solutions and validate retained minima with spin/occupation evidence.

2. **Fixed-fragment interaction/deformation and distance/twist matrix** Using the fixed neutral-doublet decomposition, calculate equilibrium and rigid distance/twist controls, fragment relaxation terms and density differences at both model sizes.

3. **Cross-check orbital, density, bond-index and energy explanations** Compare orbital mixing, densities, bond indices and interaction response to identify which explanations survive truncation and method/fragment sensitivity.

The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.

Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.

Outside the mandatory first-version scope: Hap4Ir2 calibration, all oxidation states and large-scale dynamics are optional; licensed EDA is not mandatory.

# Completion and allowed outcomes

`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.

# Deliverables

Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.

- `dimer_states`: True dimers, electronic states and paired truncation
- `fragment_interventions`: Fixed-fragment interaction/deformation and distance/twist matrix
- `bonding_evidence`: Cross-check orbital, density, bond-index and energy explanations
