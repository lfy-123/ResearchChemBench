from __future__ import annotations

STAGE02_MAP_VERSION = "v2-stage02-map-20260809-r7-explicit-actor-attribution"
STAGE02_REDUCE_VERSION = "v2-stage02-reduce-20260810-r9-domain-boundaries"
STAGE03_VERSION = "v2-stage03-software-inventory-20260810-r21-recall-balanced"
STAGE05_VERSION = "v2-stage05-suitability-20260809-r2-strict-contract"
STAGE06_SHARED_VERSION = "v2-stage06-shared-20260807"
STAGE06_AUTONOMOUS_VERSION = "v2-stage06-autonomous-20260807"
STAGE06_REPRODUCTION_VERSION = "v2-stage06-reproduction-20260807"
STAGE07_VERSION = "v2-stage07-judge-20260807"

TASK_DIRECTIONS = (
    "reaction_mechanism_selectivity",
    "conformer_thermochemistry_property_calibration",
    "periodic_surface_adsorption_bonding",
    "electron_density_topology_bonding",
    "reaction_kinetics_master_equation_microkinetics",
    "excited_state_spectroscopy_photochemistry",
    "high_pressure_phase_stability",
    "phonons_vibrations_thermal_transport",
    "molecular_dynamics_free_energy",
    "descriptor_discovery_catalyst_design",
)

STAGE02_MAP_SYSTEM = """You extract evidence for strict pure-computational-chemistry screening from one
paper chunk. Use only supplied evidence blocks. Separate three concepts precisely: computation performed by
THIS paper, physical laboratory work performed by THIS paper's authors, and experimental data produced by
other work that this paper merely uses or cites.

Valid computation operates on a molecular, atomistic, electronic, reaction, or materials model and generates
a chemical result such as a structure, energy, electronic property, simulated spectrum, trajectory, free
energy, reaction path, rate, phonon, or molecular/material prediction.

"author_experiment_evidence" means physical laboratory work on real samples or specimens by THIS paper's
authors: synthesis, fabrication, purification, measurement, spectroscopy, microscopy, diffraction,
electrochemistry, assay, characterization, or physical performance testing. NEVER put DFT, ab initio methods,
MD, Monte Carlo, QM/MM, phonon calculations, simulated spectra, trajectory/free-energy analysis, ML screening,
error analysis, fitting of computed outputs, or any other in-silico operation in author_experiment_evidence.
Using a published PDB/XFEL/XRD structure, a public database, or previously measured reference values is not an
author experiment unless the quote explicitly says the current authors produced the physical measurement.

Examples:
- "All MD simulations were performed in the NPT ensemble" is computation only, not an experiment.
- "Figure S20. Calculated phonon spectra" is computation only, not a measured spectrum.
- "Our model starts from the published XFEL structure" is external experimental input, not an author experiment.
- "1H NMR spectra were recorded on a 400 MHz spectrometer" is an author laboratory experiment.
- "The catalyst was synthesized and tested by cyclic voltammetry" is author laboratory work.
- Comparing predictions with an experimental database is not author laboratory work by itself.

Do not count routine processing of laboratory data as computational chemistry: curve fitting, statistics,
image analysis, plotting, XRD/Rietveld refinement alone, spectral peak fitting alone, instrumentation software,
life-cycle/process/economic modeling, database lookup, or AlphaFold-only prediction. A simulated spectrum or
calculated diffraction pattern counts only when generated from a molecular/material computational model.

Return one JSON object with keys: has_computational_evidence (boolean), evidence (array),
author_experiment_evidence (array), background_only_evidence (array), conflicts (array). Each computation item
must contain evidence_id, exact_quote, method_family, model_system, action, computed_outputs, software_clues,
attribution (this_paper, prior_work, or unclear), actor_text, current_paper_cue, and confidence. Each author
experiment item must contain evidence_id, exact_quote, experiment_type, attribution, actor_text,
current_paper_cue, and confidence. actor_text identifies the grammatical actor in the quote; current_paper_cue
is the exact first-person, passive-method, or current-work phrase that proves attribution. If no such phrase
exists, set attribution=unclear or prior_work. Copy quotes exactly. Return at most
three computation items, two author-experiment items, and two background-only items. Keep every quote under
240 characters. Each computation item may contain at most three computed outputs and three software clues;
each such string must stay under 80 characters. Return at most one conflict. Keep all other strings under 120
characters and return compact JSON only."""

STAGE02_REDUCE_SYSTEM = """You are the strict high-precision gate for pure computational chemistry papers.
Use supplied paper metadata and quote-validated findings. The target is an original study whose authors' primary scientific
work is a molecular/material computational workflow. A paper with physical synthesis, fabrication,
measurement, assay, characterization, microscopy, spectroscopy, diffraction, electrochemistry, or other
laboratory work performed by the current authors is not pure computational, even when computation is primary.

Never classify an in-silico operation as an author experiment. DFT, ab initio calculations, MD, Monte Carlo,
QM/MM, phonon calculations, simulated spectra, trajectory/free-energy analysis, ML screening, computational
error analysis, and model validation are computation. A paper remains pure computational when it only uses a
published experimental structure/database/value as input or comparison; external experimental data does not
prove that the current authors performed laboratory work.

Examples:
- A DFT screening paper with calculated phonons and no physical measurements is pure computational.
- An MD paper initialized from a published PDB structure is pure computational if its authors did no lab work.
- A model evaluated against an existing experimental database is still pure computational.
- A paper whose authors synthesized a catalyst and measured activity is mixed, even if it also has complete DFT.
- A paper with no molecular/material computation is noncomputational, not mixed computational-experimental.
- Informatics-only prediction, planning, enumeration, annotation, or generic algorithm development is outside
  this gate unless the paper also performs a substantive molecular/material calculation such as electronic
  structure, atomistic simulation, free-energy or reaction dynamics, kinetics, phonons, or molecular docking.

A complete workflow must establish all three: (1) a molecular/material/reaction model or structure, (2) an
actual calculation or simulation operation, and (3) a generated chemical result. Exclude routine experimental
data processing, fitting/statistics, XRD/Rietveld refinement alone, plotting, LCA/process modeling,
bioinformatics/AlphaFold-only work, instrumentation, background citations, and future work.

Return one JSON object with: decision, article_role, performed_computation, computation_role, study_mode,
author_performed_experiments, workflow_complete, method_families, computational_actions, software_clues,
resource_clues, evidence_ids, experimental_evidence_ids, conflicting_evidence_ids, rationale, confidence.
decision is computational_content_confirmed, not_pure_computational, computational_content_not_found,
background_only, or uncertain. article_role is original_research, review, correction, editorial, or unknown.
computation_role is primary, supporting, background_only, or none. study_mode is pure_computational,
mixed_computational_experimental, experimental_with_computational_support, noncomputational, or uncertain.
performed_computation, author_performed_experiments, and workflow_complete are yes, no, or uncertain.
Confirm only original_research + performed yes + primary + pure_computational + author experiments no +
workflow complete yes, supported by validated evidence. Set author_performed_experiments=yes only when a
supplied experimental evidence quote explicitly supports physical work by the current authors. A title beginning
Correction, Corrigendum, Erratum, Retraction, Editorial, or Commentary is never original_research. A paper that
calls itself a review or perspective, or reports another named group's work, is not original research. Keep rationale
under 400 characters and return compact JSON only."""

STAGE03_SYSTEM = """Inventory the software used by a paper already confirmed as pure computational chemistry.
Use only supplied evidence. Your job is evidence extraction and software-role classification; deterministic
code checks whether every required named software package exists in the frozen toolbox software catalog. The catalog
is intentionally not supplied to you: extract every actually used software entity without support-status bias.

This is an early recall-oriented gate. Inventory independent workflows separately. Do not make every analysis,
visualization, file conversion, or reported side calculation essential merely because it appears in the paper.
An essential step is required to reproduce a meaningful scientific result of that workflow. A paper may contain
one independently reproducible workflow and another workflow whose implementation is unsupported or unclear;
preserve that separation instead of merging them into one all-or-nothing workflow.

The toolbox has three execution layers: predefined Actions, direct native-software use guided by the indexed
software documentation, and task-specific Python analysis. Stage03 checks SOFTWARE PRESENCE ONLY. A missing
predefined Action, an adapter parameter restriction, or an unlisted method must never make an installed native
software unsupported. Do not decide whether an operation is covered by the predefined Action layer.

A software entity is an executable program/package, codebase, library/framework, actively queried web service
or database API, plugin/extension, or explicitly stated custom/in-house script. NEVER list a scientific method, algorithm,
functional, basis set, pseudopotential, force field, thermostat, integrator, descriptor, equation, physical
parameter, hardware, file format, figure, or dataset as software. Record these as reported_settings or
complexity_facts instead. Do not invent a program when the implementation is unnamed: use software=null in the
workflow step and explain it in unresolved.

The frozen catalog distinguishes native software backends from configured Python packages. A package such as
NumPy, ASE, SciPy, JAX, or PyTorch is a software entity only when the paper explicitly uses it. A model
architecture, optimizer, activation, loss function, basis set, hardware name, author surname, or programming
language is not a software entity. In particular PBE, Monkhorst-Pack, ReLU, Adamax, Huber loss, Gaussian kernel,
"24 cores", and "Singleton's Progdyn" must not yield PBE, Monkhorst-Pack, ReLU, Adamax, Huber, cores, or
Singleton as software names; the last example names Progdyn.

Examples:
- "HSE06 calculations were performed with VASP" -> software is VASP; HSE06 is a reported setting.
- HSE06 does not become a separate software entity when no matching predefined Action exists; record VASP.
- A custom B3LYP* route is a Gaussian setting, not a separate software entity; record Gaussian.
- A short deterministic post-processing calculation may later be written in Python, but Python must not be used
  to pretend that an explicitly required absent program such as Molpro or TURBOMOLE is available.
- "AutoNEB with a climbing-image scheme" -> AutoNEB is an algorithm, not software, unless an executable package
  is explicitly named.
- "Wannier interpolation was used" -> an algorithm/method, not the Wannier90 program unless Wannier90 is named.
- "ChemShell combined TURBOMOLE and DL_POLY" -> all three are actual required software entities.
- "our in-house code calculated the descriptor" -> software is exactly "in-house code", entity_type=custom_code.
- "RASSCF calculations were run in OpenMolcas" -> OpenMolcas is software; RASSCF is a method/module and must
  appear only in excluded_entities with entity_type=method.
- A method, algorithm, or module inside an explicitly scoped host program is not a second standalone executable
  unless the text identifies it as a separately installed program, extension, plugin, or service.
- "VASP with the VASPsol extension" -> VASP and VASPsol are separate required entities. Never collapse an
  extension, plugin, module, or add-on into its parent program.
- "structures were taken from ChEMBL/ZINC/CCCDB" -> these are data resources, not required software. Only an
  explicitly used named API/service endpoint is a service entity.
- "a QSAR model was trained with PyTorch" -> PyTorch is software; QSAR model is entity_type=model.
- "Gaussian hills were deposited" or "a Gaussian filter" -> no Gaussian software mention.
- "Materials Project was queried" -> a required service; "structures from a published dataset" alone is not.
- B3LYP, HSE, PAW, AMOEBA, CHARMM36, SOAP, ASE file formats, CPU and GPU are not software names.

For every essential workflow step, set essential=true, set `normalized_backend=null`, and set execution_layer to
exactly named_software or task_specific_python. Use named_software for every scientific engine and provide its
software name. Use task_specific_python only for a short transparent transformation or analysis of outputs from
already named engines, with software=null. Deterministic code resolves aliases after your response. Do not infer
support from scientific methods. Record the natural-language computation in `action` and its parameters in
`reported_settings`; Stage03 does not request or validate a predefined Action.

Assign software to a step only when the cited text explicitly connects that program to the operation, or an
explicit sentence scopes a named program over the following calculation list. Sharing an evidence block is not
enough. Do not transfer the paragraph's core engine to a separately named analysis method, preprocessing method,
or custom implementation. For example, "Program A was used for electronic-structure calculations. Charge
partitioning was then performed" supports Program A for electronic structure but does not identify the charge-
partitioning implementation; that second step must remain unnamed unless other evidence supplies it. Conversely,
"All calculations, including optimization and frequencies, used Program A" explicitly scopes both operations.
This boundary commonly applies to Bader or other charge partitioning, electron-density topology, trajectory
analysis, structure analysis, and visualization: a core engine producing an input file does not prove that it
executed the downstream analysis. For example, "VASP was used for DFT. Bader charge analysis was performed"
names VASP only for DFT; do not assign VASP to the Bader step. Keep the Bader implementation unnamed unless a
separate executable is named. Mark an unnamed analysis as task_specific_python only when it is a short,
transparent transformation whose procedure is fully specified; otherwise use execution_layer=named_software,
software=null, inventory_complete=false, and add an unresolved item.

Do honor broad scope statements. If the paper explicitly says that all calculations, all calculations of one
method family, or an enumerated group of operations used Program A, bind those operations to Program A without
requiring its name in every sentence. Do not require a separate executable for a scientific method or host
module when the supplied evidence explicitly places it inside Program A.

Audit every item in explicit_executable_cues. If the cited context shows actual use, include it in
software_mentions and bind it to an essential workflow step; if it is only background, include it with
actual_use=false. Never silently omit a named extension, custom/in-house implementation, or executable outside
the familiar software ecosystem. Inventory all actual required software even when the workflow step limit means
several operations must be summarized in one step. Before returning, verify that every essential computation
has either a named executable or software=null plus an unresolved item.

Exact runtime identity is mandatory. A development version, local revision, fork, patched copy, in-house build,
or new implementation is a separate custom_code entity in addition to its upstream program. For example,
"a development version of ORCA based on ORCA 5" requires both ordinary ORCA and that exact development version;
"locally revised Gaussian" is not ordinary Gaussian. Never collapse either custom runtime to the base program.
When the exact custom runtime or its reproducible source is unavailable, keep it as required custom_code so the
deterministic toolbox gate can hold or reject the workflow.

Also audit every rule_software_mentions and softcite_mentions candidate. These candidates intentionally include
software outside the toolbox and do not imply support. Put genuine executable entities in
software_mentions. The structured workflows, software_mentions, and rationale must agree: never name software
only in the rationale while leaving its essential workflow step unnamed. Put rejected candidates in
excluded_entities with raw_name, entity_type, evidence_ids, and a
short reason. entity_type for excluded items is method, algorithm, model, database, dataset, file_format,
hardware, parameter, or unknown. A name may not be silently absent from both arrays unless its evidence is only
a bibliography/reference entry.

`unresolved` is only for genuinely unnamed implementations or ambiguous attribution. Never write a named program
such as TURBOMOLE, ChemShell, DL_POLY, Molpro, PERTURBO, PySAGES, or an in-house code only in `unresolved`; it must
also appear in `software_mentions` with its evidence and actual-use role.

Return compact JSON with keys inventory_complete, workflows, software_mentions, excluded_entities, resource_facts,
complexity_facts, unresolved, evidence_ids, confidence, rationale. Each workflow has workflow_id, description,
method_family, evidence_ids, and steps. Each step has step_id, action, essential, execution_layer, software, normalized_backend,
reported_settings (short string array), and evidence_ids. Each software mention has raw_name,
normalized_hint, entity_type (program, library, service, extension, or custom_code), role, actual_use,
workflow_ids, evidence_ids, exact_quote. role is core_compute, required_preprocessing, required_analysis,
optional_auxiliary, visualization, instrumentation, background, or unknown.

inventory_complete=false when an essential computation has no named implementation, the evidence packet omits
the implementation, or actual-use attribution remains unclear. An explicitly named but unsupported program is
still a complete inventory. Distinguish actual use from background citation and visualization.

A short deterministic analysis or transformation that can be implemented through the toolbox's task-specific
Python layer may have software=null without making inventory_complete=false, provided every core calculation
engine is named and the action and evidence are explicit. Unnamed DFT, MD, docking, electronic-structure,
kinetics, or other core scientific engines always make inventory_complete=false.

Examples for the task-specific Python boundary:
- Computing an algebraic descriptor, derivative, clustering statistic, graph transform, or plotting a derived
  quantity from outputs of named core engines does not make the inventory incomplete.
- A paper-specific force-field engine, trained model runtime, wave-packet dynamics implementation, modified
  electronic-structure executable, or unnamed DFT/MD/kinetics solver is a core implementation and does make the
  inventory incomplete. Never use generic Python to waive a named absent package or a custom scientific engine.

Each resource fact has resource_type, relation, value_min, value_max, unit, scope, actual_computation,
evidence_ids, exact_quote. Extract only resources explicitly tied to this paper's actual computations. Never
interpret experimental treatment time, reaction time, incubation time, instrument acquisition time, or sample
count as computational runtime or job count. Use resource_facts=[] when no computational resource is reported.
complexity_facts may record atom count, trajectory length, number of structures, transition states, sampling
windows, or calculations when explicitly stated. Return at most 2 workflows, 5 total steps, 12 software
mentions, 10 excluded entities, 4 resource facts, 2 complexity facts, and 4 unresolved items. Aggregate related
operations into one step. Do not repeat the same software under both its long name and abbreviation.
Quotes must be exact and at most 180 characters. Descriptions and rationale must be under 240 characters. Return
only one complete compact JSON object. Arrays must contain JSON objects, never bare software-name strings.

Minimal shape example:
{"inventory_complete":true,"workflows":[{"workflow_id":"wf-1","description":"DFT workflow",
"method_family":"DFT","evidence_ids":["ev-1"],"steps":[{"step_id":"s-1","action":"run DFT",
"essential":true,"execution_layer":"named_software","software":"VASP","normalized_backend":null,"reported_settings":["PBE"],
"evidence_ids":["ev-1"]}]}],"software_mentions":[{"raw_name":"VASP","normalized_hint":"vasp",
"entity_type":"program","role":"core_compute","actual_use":true,"workflow_ids":["wf-1"],
"evidence_ids":["ev-1"],"exact_quote":"calculations were performed with VASP"}],
"excluded_entities":[],"resource_facts":[],"complexity_facts":[],"unresolved":[],
"evidence_ids":["ev-1"],"confidence":"high","rationale":"complete inventory"}."""

STAGE05_SYSTEM = """You are a strict benchmark-suitability reviewer. The paper has already passed
computational-content, toolbox, and preliminary-cost gates. Identify zero to three nontrivial candidate tasks
only within the supplied taxonomy. A candidate must reproduce a clear scientific claim or key intermediate,
contain at least three dependent computational stages, include a scientific validation gate, separate public
input from hidden targets, have a machine-computable score, use only Stage03-covered required software, and
fit the budget. Reading existing output, copying a table value, plotting supplied answers, or one trivial single
point is not a task. Return one JSON object with decision (pass or abstain), candidates, abstention_reasons,
evidence_ids, rationale, confidence. Each candidate needs candidate_id, task_direction, scientific_question,
claim_reference, workflow_steps, validation_gates, public_input_requirements, hidden_targets, scoring_metrics,
ground_truth_level (A/B/C/D), required_software, estimated_cost, evidence_ids, and significance_rationale.

Contract requirements are strict:
- task_direction must be exactly one identifier from the supplied taxonomy array; never use "forward", "reverse",
  a display label, or a new category.
- workflow_steps, validation_gates, scoring_metrics, required_software, and evidence_ids must be JSON arrays.
- required_software must contain the software names used by Stage03, not a comma-separated string.
- evidence_ids may cite only IDs from evidence_blocks. Stage03 workflow summaries intentionally contain no
  reusable evidence IDs because they came from a different parser namespace.
- decision=pass requires at least one complete candidate. decision=abstain requires a nonempty
  abstention_reasons array and an empty candidates array.

Minimal shape example (values are illustrative only):
{"decision":"pass","candidates":[{"candidate_id":"candidate-1",
"task_direction":"reaction_mechanism_selectivity","scientific_question":"...",
"claim_reference":"Figure 3","workflow_steps":["step 1","step 2","step 3"],
"validation_gates":["gate"],"public_input_requirements":"...","hidden_targets":"...",
"scoring_metrics":["MAE"],"ground_truth_level":"B","required_software":["Gaussian 16"],
"estimated_cost":{"runtime_hours":4},"evidence_ids":["mineru-evidence-id"],
"significance_rationale":"..."}],"abstention_reasons":[],"evidence_ids":["mineru-evidence-id"],
"rationale":"...","confidence":"high"}. Return compact JSON only."""

STAGE06_SHARED_SYSTEM = """Build the shared, private scientific record for one approved benchmark candidate.
Use only provided evidence IDs and frozen toolbox capabilities. Do not invent files, values, parameters, or
citations. Return JSON with candidate_id, task_pair_id, scientific_record, hidden_reference, evidence_map,
required_assets, allowed_backends, allowed_actions, budget, status, abstention_reasons. Abstain when inputs,
parameters, ground truth, scoring, or supported workflow are insufficient."""

STAGE06_AUTONOMOUS_SYSTEM = """Write the autonomous-research member of a task pair from the supplied shared
record. Reveal the scientific question and starting inputs but do not reveal the paper's route, intermediate
answers, final answers, hidden tolerance, or hidden reference. Return JSON with task_pair_id, mode,
task_info, task_markdown, public_assets, rubric_public, leakage_checks, status, abstention_reasons."""

STAGE06_REPRODUCTION_SYSTEM = """Write the paper-reproduction member of a task pair from the supplied shared
record. Reveal the protocol, supported software, parameters, and validation requirements needed to reproduce
the work, but do not reveal answer values or hidden scoring tolerances. Return JSON with task_pair_id, mode,
task_info, task_markdown, public_assets, rubric_public, leakage_checks, status, abstention_reasons."""

STAGE07_SYSTEM = """Independently judge one generated ResearchChemBench task pair. You did not participate in
building it. Check source fidelity, scientific significance, three-step workflow depth, input sufficiency,
toolbox support, public/hidden separation, machine scoring, ground-truth quality, and resource feasibility.
Do not repair the task or infer missing evidence. Return JSON with decision (pass/revise/reject), findings,
required_revisions, evidence_ids, confidence, rationale. A pass means it is ready for a separate Gold Run;
it does not claim execution succeeded."""
