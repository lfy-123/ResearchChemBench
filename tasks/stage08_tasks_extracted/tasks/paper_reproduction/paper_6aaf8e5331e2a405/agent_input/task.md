# Scientific objective

Independently compute and interpret the thermodynamic ORR overpotential and active-site sulfur p-band center for the specified Ni-substituted 2H-MoS2(001) basal-plane model, and determine whether the model supports activation of the basal plane under the stated CHE boundary. Propose and discriminate plausible adsorption-site/conformer explanations using calculations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that substitutional Ni doping can activate an otherwise inert basal-plane sulfur site through coupled structural and electronic reorganization. For Ni in the d7–d9 class, they associate the activity increase with Jahn–Teller-associated lattice distortion, orbital-level rearrangement, reduced charge transfer to sulfur, and an upward shift of the sulfur 3p-band center.

**Candidate route or mechanism.**
For this Ni-substituted model, examine a top-layer sulfur site in the immediate Ni neighborhood as a proposed active site. Consider whether local distortion and altered Ni–S electronic coupling change adsorption of the associative ORR intermediates OOH*, O*, and OH*. The authors' broader interpretation distinguishes distortion-driven reorganization for d7–d9 dopants from d–p hybridization for lower d-electron-count dopants; use the former as a focused hypothesis for Ni while testing the actual structure and adsorption states.

**Discriminating evidence.**
Use relaxed local geometry and stationarity checks together with the four CHE step free energies, the potential-determining step, and the sulfur 3p projected-band first moment. Charge or orbital-population analysis and comparison among distinct nearby sulfur sites or adsorption conformers can test whether the proposed activity change tracks local distortion, Ni–S electronic coupling, and the p-band descriptor.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`. Resolve host structure only from Materials Project record mp-2815 (2H-MoS2), cleave the (001) surface, make the stated 3x3x1 periodic slab with 15 Å vacuum, and replace exactly one Mo site with Ni. Preserve charge, stoichiometry, periodicity, and explicit atom indexing in every submitted structure. The measured quantities are CHE free energies for OOH*, O*, and OH* along the associative four-electron ORR sequence at U=0 V, pH=0, T=298.15 K, the resulting overpotential η, and the 3p projected-band first moment εp for one explicitly identified top-layer S atom directly bonded to the Ni neighborhood. No paper/SI or general-web searching is allowed; controlled database access is limited to mp-2815.

# Required scientific validation/investigation

Generate a finite, explicitly enumerated set of chemically distinct candidate active S sites and adsorption conformers, deduplicate by atom identity and geometry, and advance only candidates that remain attached to the stated surface after relaxation. Report coverage, rejected candidates and reasons, relaxation/stationarity diagnostics, magnetic/charge state, numerical settings, CHE corrections, and p-band integration definition. Identify the potential-determining step from the submitted ΔG values. Completion requires a converged validated result for at least one candidate plus a documented comparison of all candidates advanced under the declared stopping rule, or a bounded-failure report naming the missing observable and evidence. Stop when the declared site/conformer list and convergence tests are exhausted; if resources prevent that, report the explored fraction and limitations rather than asserting uniqueness.

# Deliverables

Submit `report/results.json` matching `submission_schema.json`, including candidate identities and validation context, numerical observables with units, four ΔG values, PDS, search coverage, and a final evidence-based conclusion. A bounded-failure branch is permitted but must contain truthful diagnostics and coverage.
