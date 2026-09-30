# Scientific objective

Explain the measured absorption differences among B2N6 derivatives 1–4 in dichloromethane. Determine what molecular evidence supports the explanation and how reliably it distinguishes the effects associated with changing the boron substituents.

# Author-provided scientific guidance

The authors interpret boron-substituent-dependent absorption through changes in N6-related orbital energies and transition character (main pp3–4). The visible band is described as mainly HOMO→LUMO for1/4 but mainly HOMO−4→LUMO for2/3; this is a source assignment to assess, not a rule for selecting every calculated root. The disclosed computational route is Gaussian16 B3LYP/6-31+G(d), SMD dichloromethane; SI p16 additionally specifies DFT-D3BJ, which is omitted from the shorter main-text label. Main and SI excitation numbers are not identical: for example compound1 main prose gives3.52eV while SI TableS2 gives3.0119eV with f=0.3456. Report the actual chosen protocol and raw output rather than tuning to either printed number. The authors discuss limited dissociation of2 from its solvent-insensitive spectrum. V1 common-core freezes and effect partitioning were added benchmark interventions.

Reproduce the disclosed author baseline within this scope, or justify a substitute scientifically and assess its consequences. Clearly distinguish this reproduction from your additional investigation. Source conclusions are conditional evidence, not an answer that must be affirmed; scientifically justified corrections or unresolved results remain eligible. The V1 benchmark interventions were not part of the author protocol and are not required in this version.

# Public inputs and scientific boundaries

Use the four complete supplied neutral singlet molecular identities and dichloromethane absorption observations. Compound2 contains four covalently attached B–O–SO2CF3 groups; it is not a bare B2N6 ion accompanied by four free triflate counterions. Any alternative model of solution composition must be explicitly justified and balanced. Restrict conclusions to molecular solution absorption. Solid-state emission, electrochemical decomposition and device performance are not required endpoints.

Read `data/inputs/systems.json`, `problem_facts.json` and the observational files listed below. These are identity/observation inputs, not an optimized starting-answer set.

- `data/inputs/experimental_absorption.json`
- `data/inputs/problem_facts.json`
- `data/inputs/solution_observations.json`
- `data/inputs/systems.json`

The benchmark chemistry toolbox provides scientific/data actions, reviewed native software input routes and agent-authored Python analysis in selected runtimes. Its registered Gaussian and ORCA routes and Python graph/analysis tools are potential resources, not a prescribed workflow. Inspect the available tool catalog and native manuals in the execution environment before choosing a capability. Source authors' software versions do not guarantee identical installed versions. Runtime allocation is supplied by the execution environment; no paper-specific CPU-hour or accuracy budget has been measured here. Record actual usage, failed attempts and unmeasured costs honestly. Public observations are available from the outset and are retrospective data, not a hidden test set. Do not access private evaluation material, another task mode or source answer files.

# Required scientific validation/investigation

Design and carry out an investigation that can substantiate your answer within the stated scope. Choose and justify the model, method, evidence and any further comparisons needed for the claims you make. Explain the relationship between observations and inference, the important unresolved alternatives, and why the evidence is sufficient or insufficient. A supported negative answer or a bounded inability to distinguish explanations is a scientific outcome; a statement of uncertainty without relevant work is not completion.

Validate the identity, conditions, state and numerical meaning of every result used. Claims of equilibrium populations, minima, predictive performance or causal effects require evidence appropriate to those claims. AR selects its research route independently. PR reproduces the disclosed author baseline or explains a scientifically justified substitute and its consequences; additional investigation remains self-designed. The shared scientific-result criteria require neither a particular method nor an author outcome. No fixed hypothesis count, comparison matrix or search order is prescribed. Record concise research decisions linked to actual artifacts and tool traces; do not submit private internal reasoning. No claim of a prospective prediction follows merely from a self-authored timestamp.

# Deliverables

Submit `report/results.json` and a readable `report/report.md` using the accompanying contract. Include structured measured/calculated quantities with units, definitions and conditions, the models actually used, raw input/output or data-analysis artifacts, reproducible analysis, and supported findings. `partial`, `bounded_failure` and `blocked` submissions preserve credit for valid work but do not establish a complete answer. See `submission_guide.md`.
