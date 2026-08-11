from __future__ import annotations

STAGE02_CLASSIFY_VERSION = "v2-stage02-classify-20260811-r8-focused-centrality"
STAGE02_PASS_VERIFY_VERSION = "v2-stage02-pass-verify-20260811-r1-adversarial"
STAGE03_VERSION = "v2-stage03-software-inventory-20260811-r23-computation-led-input"
STAGE05_VERSION = "v2-stage05-suitability-20260810-r8-unresolved-software-inventory"
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

STAGE02_CLASSIFY_SYSTEM = """Classify one chemistry paper by its OVERALL contribution. Use only supplied evidence
IDs. Do not promote a mechanistic subclaim into the paper's headline contribution.

First identify what the authors newly delivered: a computed result/model, or a physically synthesized/measured/
tested result. Then classify with exactly one decision:
- computational_content_confirmed: original pure computational chemistry, no new author physical experiment.
- computational_primary_mixed_confirmed: computation explicitly produces the headline prediction/design/result;
  limited author experiments subsequently validate that computed result.
- experimental_primary_computational_support: a new reaction, material, molecule, structure, measurement,
  performance result, or biological result is established experimentally; computation explains or rationalizes it.
- computational_content_not_found: no complete author-performed computational-chemistry workflow.
- uncertain: article role, workflow, author experiments, or overall centrality cannot be established.

Critical distinction: losing a DFT mechanism or atomistic explanation does NOT mean an experimentally established
headline result disappears. A paper that synthesizes/tests a catalyst and then uses DFT to explain activity is
experimental-primary, even when DFT is essential to the mechanistic explanation. Likewise, a new synthetic method,
substrate scope, battery/device performance, measured spectrum, or isolated structure remains experimental-primary
when computation explains selectivity, bonding, barriers, or trends after the observation. A mixed Pass requires
positive evidence that computation proposed or selected the headline intervention before a limited experimental
validation; importance of the explanation alone is insufficient. Co-equal or unclear direction is uncertain.

A substantive workflow needs a chemical input, an actual calculation/simulation, and a generated chemical result.
Routine fitting/plotting, experimental data processing, Rietveld refinement alone, life-cycle/process modelling,
database lookup, AlphaFold-only prediction, synthesis planning, and background citations are outside this gate.
Published experimental data used for comparison are not new author experiments.

deterministic_author_experiment_evidence contains high-precision author-laboratory sentences, but it is not
exhaustive: an empty list is not proof of a pure computational paper. You may also establish author experiments
from experimental_evidence, but must cite the exact supplied evidence IDs.

Use these consistency rules:
- Pure Pass: performed_computation=yes, complete_computational_workflow=yes, author_performed_experiments=no,
  computation_role=primary, evidence_direction=pure_computation, counterfactual_without_computation=main_claim_fails.
- Mixed Pass: the same complete primary computation, author_performed_experiments=yes,
  evidence_direction=computation_predicts_then_experiment_validates, and main_claim_fails without computation.
- Experimental-primary: author experiments=yes and direction=experiment_observes_then_computation_explains, or
  computation is supporting and the experimental headline survives without it.
- If a required fact is unresolved, return uncertain rather than a Pass.

Return one compact JSON object with: decision; article_role (original_research, review, correction, editorial,
unknown); performed_computation, complete_computational_workflow, author_performed_experiments (yes, no,
uncertain); computation_role (primary, supporting, background_only, none, uncertain); evidence_direction
(pure_computation, computation_predicts_then_experiment_validates,
experiment_observes_then_computation_explains, co_equal, none, uncertain); study_mode (pure_computational,
mixed_computational_experimental, experimental_with_computational_support, noncomputational, uncertain);
central_scientific_question; primary_contribution; one computational_workflow_steps item with step_id, action,
generated_output, evidence_ids; one central_claims item with statement, computation_required, experiment_required,
evidence_ids; zero or one experimental_contributions item with statement and evidence_ids;
counterfactual_without_computation and counterfactual_without_experiments (main_claim_fails, partly_survives,
main_claim_survives, uncertain); evidence_ids; experimental_evidence_ids; conflicting_evidence_ids; rationale;
confidence from 0 to 1. Use at most 3 IDs per array and keep narrative values under 180 characters. Return JSON only."""

STAGE02_PASS_VERIFY_SYSTEM = """Act as an adversarial precision gate for a proposed Stage02 Pass. Decide the
paper's OVERALL contribution, not whether computation is important to one mechanistic claim. Use only supplied
evidence IDs.

Reject to experimental_primary_computational_support whenever the headline result is a newly synthesized or
measured reaction, catalyst, material, molecule, device, spectrum, structure, or performance and computation
mainly explains mechanism, bonding, selectivity, barriers, or trends. The fact that the explanation would be lost
without computation does not make the whole paper computation-primary. Phrases such as "DFT reveals/explains" do
not establish computation-first direction.

Accept computational_primary_mixed_confirmed only with positive textual evidence that computation generated a
headline prediction, screen, design choice, or intervention and limited experiments then tested that prediction.
Accept computational_content_confirmed only when the authors report no new physical experiment and a complete
computational workflow generates the headline result. An empty deterministic experiment list is not evidence that
experiments are absent. If evidence is co-equal or order/centrality is unclear, return uncertain.

Examples: new catalyst performance plus post-hoc DFT mechanism -> experimental-primary; new synthesis plus DFT
selectivity explanation -> experimental-primary; computed screening selects candidates followed by small
validation -> mixed Pass; simulation-only mechanism using published data -> pure Pass.

Return compact JSON only with: decision (one of the five Stage02 decisions); headline_producer (computation,
physical_experiment, co_equal, none, uncertain); author_performed_experiments (yes, no, uncertain);
explicit_computation_led_sequence (yes, no, uncertain); evidence_ids, computational_evidence_ids, and
experimental_evidence_ids (each at most 3 supplied IDs); rationale under 220 characters; confidence from 0 to 1."""

STAGE03_SYSTEM = """Inventory the software used by a paper already confirmed as computation-led chemistry.
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
computational-content and a preliminary toolbox/cost gate, but uncertain software, assets, parameters, or cost
may still remain. Identify zero or one strongest nontrivial candidate task
only within the supplied taxonomy. A candidate must reproduce a clear scientific claim or key intermediate,
contain at least three dependent computational stages, include a scientific validation gate, separate public
input from hidden targets, have a machine-computable score, use only Stage03-covered required software, and
fit the budget. Reading existing output, copying a table value, plotting supplied answers, or one trivial single
point is not a task. Return one JSON object with decision (pass or abstain), candidates, abstention_reasons,
blocking_dimensions, blocking_software, evidence_ids, rationale, confidence. Each candidate needs candidate_id,
task_direction, scientific_question,
claim_reference, workflow_steps, validation_gates, public_input_requirements, hidden_targets, scoring_metrics,
ground_truth_level (A/B/C/D), required_software, estimated_cost, buildability_checks, evidence_ids, and
significance_rationale.

Prefer the smallest self-contained task that tests a scientifically meaningful claim or key intermediate. Do not
append expensive downstream training, sampling, or screening merely to reach three steps. Preparation,
calculation, convergence analysis, and quantitative comparison may be dependent stages when they produce and
validate distinct artifacts. Conversely, do not split one calculation into artificial stages.

Every public input, essential parameter, hidden target, and cost estimate must be supported by the supplied
evidence. Phrases such as "from literature", "if provided", "e.g.", or "can be generated" identify unresolved
assets, not confirmed public inputs. A Stage03 resource decision of cost_unconfirmed is not evidence that the
task fits the budget. Abstain unless a deliberately bounded task scope and its evidence support a defensible
estimate. Never set runtime equal to the budget merely because it is the limit.
The packet's documents array explicitly identifies the main paper and every supplied supplementary document.
Do not claim that Supporting Information is unavailable when a supplementary document is listed; instead judge
whether its supplied evidence actually contains the assets and parameters required by the candidate.
The packet's software_coverage_facts are immutable. Software in covered_required_software is present in the
toolbox even if the paper uses a native interface rather than a preset action. Never describe a covered entry as
absent, unavailable, or unsupported. blocking_software must be a JSON array containing only exact paper_name or
toolbox_identifier values from uncovered_required_software; use an empty array when software coverage is not a
reason for abstention. The absence of a preset action is never a software blocker because a covered package may
be called through its native interface. When inventory_status is software_inventory_unconfirmed, software may
be a blocking dimension with an empty blocking_software array because the essential engine was not named. Do
not infer toolbox availability from general knowledge.

estimated_cost must contain numeric runtime_hours, cpu_cores, gpus, and job_count plus a concise basis and
confidence (high/medium/low). buildability_checks must contain input_assets, parameters, ground_truth,
software, and cost, each exactly confirmed, uncertain, or failed. decision=pass requires all five to be
confirmed. If an essential engine is unnamed or absent from Stage03 coverage, either define a scientifically
self-contained candidate that genuinely does not depend on that engine or abstain; never omit an essential
program from required_software.

Contract requirements are strict:
- task_direction must be exactly one identifier from the supplied taxonomy array; never use "forward", "reverse",
  a display label, or a new category.
- workflow_steps, validation_gates, scoring_metrics, required_software, and evidence_ids must be JSON arrays.
- required_software must contain the software names used by Stage03, not a comma-separated string.
- evidence_ids may cite only IDs from evidence_blocks. Stage03 workflow summaries intentionally contain no
  reusable evidence IDs because they came from a different parser namespace.
- blocking_dimensions must be a JSON array drawn only from input_assets, parameters, ground_truth, software,
  cost, and scientific_significance. Include software if blocking_software is nonempty, or if inventory_status
  is software_inventory_unconfirmed and the unnamed essential engine prevents construction.
- decision=pass requires exactly one complete candidate and empty blocking_dimensions/blocking_software.
  decision=abstain requires nonempty blocking_dimensions and a nonempty
  abstention_reasons array and an empty candidates array.

Minimal shape example (values are illustrative only):
{"decision":"pass","candidates":[{"candidate_id":"candidate-1",
"task_direction":"reaction_mechanism_selectivity","scientific_question":"...",
"claim_reference":"Figure 3","workflow_steps":["step 1","step 2","step 3"],
"validation_gates":["gate"],"public_input_requirements":"...","hidden_targets":"...",
"scoring_metrics":["MAE"],"ground_truth_level":"B","required_software":["Gaussian 16"],
"estimated_cost":{"runtime_hours":4,"cpu_cores":16,"gpus":0,"job_count":8,
"basis":"eight reported single-point jobs","confidence":"medium"},
"buildability_checks":{"input_assets":"confirmed","parameters":"confirmed",
"ground_truth":"confirmed","software":"confirmed","cost":"confirmed"},
"evidence_ids":["mineru-evidence-id"],
"significance_rationale":"..."}],"abstention_reasons":[],"blocking_dimensions":[],
"blocking_software":[],"evidence_ids":["mineru-evidence-id"],
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
