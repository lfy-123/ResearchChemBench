# Scientific objective

Independently determine how the two specified cis pseudohalide co-ligands affect isolated Fe(II) spin-state energetics in the neutral series `[Fe(LPh-TDA)(NCE)2]`: C1 (E=S), C2 (E=Se), and C3 (E=BH3). For each named complex, calculate the paper-defined electronic spin-transition energy `E_el^iso = E_HS − E_LS` between optimized HS (multiplicity 5) and LS (multiplicity 1) states, report it in kJ mol−1, and compare the three values. The object is an isolated molecule; do not report a crystal free energy or a transition temperature as the requested observable.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret the pseudohalide substitution as a ligand-field change that can alter the relative stabilization of the Fe(II) low-spin and high-spin states across C1 (E=S), C2 (E=Se), and C3 (E=BH3). They relate the isolated-molecule trend to, while distinguishing it from, packing-dependent solid-state spin crossover.

**Candidate route or mechanism.**
A focused comparison is to test whether the auxiliary-ligand series produces a monotonic change in the isolated HS-versus-LS electronic gap, with the N-bound pseudohalide pair as the varying chemical feature and the LPh-TDA coordination environment held fixed. Treat this as a proposed ligand-field explanation to be tested rather than as an assumed outcome.

**Discriminating evidence.**
Discriminate the explanation using like-for-like optimized HS and LS energies for all three complexes, with state-specific multiplicities, intact donor/atom mapping, convergence and stationary-point checks where feasible, spin contamination or density diagnostics, and an explicit sign/unit audit. Compare the within-method gaps and their uncertainty across C1–C3; isolated electronic energies are the relevant evidence, while crystal packing and thermal transition behavior are contextual rather than required observables.

# Public inputs and scientific boundaries

The complete identity specification is `data/inputs/system_spec.json`: LPh-TDA connectivity, neutral Fe(II), octahedral cis coordination, four LPh-TDA donor atoms, and two N-bound NCS−, NCSe−, or NCBH3− ligands. You may construct 3-D conformers and computational models from these inputs. Do not use the paper, SI, their coordinate files, or general web searches. Choose and justify your own method/software, state preparation, conformer strategy, and energy treatment. The three complexes and the two spin states are fixed; no author route or expected ordering is supplied. The scientific question is whether your independently obtained within-method results support a coherent ligand-substitution trend.

# Required scientific validation/investigation

Propose a defensible computational plan before execution. Generate a finite, explicitly reported set of conformers and HS/LS state initializations for each named complex, deduplicate converged structures using a stated criterion, and retain identity/mapping and validation context for every candidate. Advance only intact, converged candidates with the intended spin state. For every system and spin state, report attempted candidate identities, dispositions and rejection reasons. Validate every selected state separately with optimization diagnostics, stationary-point/frequency evidence when feasible (or a state-specific bounded-failure explanation), spin contamination/density diagnostics, intact-connectivity evidence, and an energy-unit/sign audit. Completion requires a selected validated HS and LS state for every complex and all three gaps, or a truthful bounded-failure branch after the declared per-system/per-state search budget is exhausted. Stop when that declared coverage is exhausted; report residual uncertainty and do not claim a global minimum beyond the explored space. A complete result must conclude with the three gaps, their ordering or lack of robust ordering, and the limits of the inference. A bounded failure must identify the unresolved states, retain any validated partial results, and avoid unsupported ordering claims.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the independent plan, method, per-candidate identities and validation, selected state structures or references, energies/gaps when obtained, coverage and stopping record, uncertainty, and final scientific conclusion. Do not include paper reference values.
