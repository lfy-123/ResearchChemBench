# Scientific objective

Independently determine the S1 fluorescence emission wavelength of the isolated cationic G1 molecule from the supplied 242-atom geometry and characterize the electronic nature of the emitting transition. Formulate and test plausible explanations from the computed evidence; do not assume any author hypothesis.


## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret the emissive transition of G1 as predominantly intramolecular charge transfer within the guest, associated with a π to π* excitation.

**Candidate route or mechanism.**
A proposed electronic rearrangement places the hole on the internal or central phenyl region and the excited electron on a lateral or extreme phenyl region of G1. Treat this as a candidate assignment to test at the relaxed S1 endpoint, alongside any competing state character indicated by the calculation.

**Discriminating evidence.**
Use natural transition orbitals and complementary electron-hole, attachment/detachment, or transition-density analyses to locate donor and acceptor regions and assess whether the excitation is spatially separated across the molecule or remains locally confined. Compare these diagnostics with the computed emission endpoint and state tracking.

# Public inputs and scientific boundaries

The file `data/inputs/G1GS.xyz` is the complete SI Cartesian coordinate block labeled G1GS. It defines one isolated molecular system with 242 atoms; use charge +1 and singlet multiplicity unless a chemically justified alternative is explicitly tested and reported. You may choose software, electronic-structure model, basis, relativistic treatment, solvation approximation, conformer protocol and state-tracking procedure, but must disclose them. The scored system is the isolated molecule; do not add a host or solvent.

# Required scientific validation/investigation

Design and execute a reproducible workflow from the supplied geometry to a validated S1 emission endpoint. Establish charge/multiplicity, convergence, state identity and geometry provenance. Validate stationary points with a Hessian/frequency check or a scientifically equivalent diagnostic. Generate and compare any additional conformers or competing excited states that your method identifies as plausible, deduplicate them by structure/state identity, and report the search coverage and stopping rule. Analyze the emitting transition with NTOs, attachment/detachment densities, transition density, or an equivalent diagnostic, then discriminate among plausible transition-character explanations using the evidence. Completion requires either a validated emission endpoint plus conclusion, or a bounded failure explanation with attempted coverage and limitations. Stop when the selected endpoint and interpretation are stable under the reported checks; otherwise stop with a limitation report rather than inventing a result.

# Deliverables

Submit `report/results.json` and any supporting files referenced by it. The JSON must conform to the local `submission_schema.json`, including status, system identity, method, workflow, endpoint, validation, transition analysis, final conclusion, and limitations, with any mode-specific required fields. Report emission wavelength in nm when available and use `null` when bounded failure prevents a defensible wavelength. Include search coverage, stopping condition, and evidence paths as supported by the schema. A bounded failure must include failure stage, scientific cause, evidence paths and the additional work needed. Do not cite or reproduce hidden reference values or evaluator files.
