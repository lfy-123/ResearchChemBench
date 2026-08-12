from __future__ import annotations

STAGE02_CLASSIFY_VERSION = "v2-stage02-classify-20260811-r10-chemistry-model-boundary"
STAGE02_PASS_VERIFY_VERSION = "v2-stage02-pass-verify-20260811-r5-independent-workflow-axes"
STAGE03_VERSION = "v2-stage03-software-inventory-20260811-r23-computation-led-input"
STAGE05_ROUTER_VERSION = "v2-stage05a-evidence-router-20260812-r1"
STAGE05_VERSION = "v2-stage05b-candidate-auditor-20260813-r19-recall-gate"
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

TASK_DIRECTION_GUIDANCE = {
    "reaction_mechanism_selectivity": (
        "Reaction paths, intermediates, transition states, mechanisms, or selectivity."
    ),
    "conformer_thermochemistry_property_calibration": (
        "Molecular conformers, thermochemistry, structures, or calibrated molecular properties."
    ),
    "periodic_surface_adsorption_bonding": (
        "Periodic solids, facets, adsorption, defects, interfaces, or surface bonding."
    ),
    "electron_density_topology_bonding": (
        "Charge/electron-density topology, bonding analysis, or quantitative charge transfer."
    ),
    "reaction_kinetics_master_equation_microkinetics": (
        "Rate constants, master-equation models, kinetic networks, or microkinetics."
    ),
    "excited_state_spectroscopy_photochemistry": (
        "Excited states, simulated spectra, photochemical paths, or nonadiabatic processes."
    ),
    "high_pressure_phase_stability": (
        "Pressure-dependent phases, equations of state, or phase stability."
    ),
    "phonons_vibrations_thermal_transport": (
        "Frequencies, phonons, vibrational spectra, or thermal transport."
    ),
    "molecular_dynamics_free_energy": (
        "Atomistic MD, solvation/transport/structural observables, sampling, or free energies."
    ),
    "descriptor_discovery_catalyst_design": (
        "Computed descriptors, bounded screening, structure-property discovery, or catalyst design."
    ),
}

STAGE02_CLASSIFY_SYSTEM = """Classify one chemistry paper by determining whether it contains an author-performed,
substantive computational-chemistry workflow that could supply a meaningful benchmark subtask. Use only supplied
evidence IDs. Computation does NOT need to be the paper's dominant contribution. Do not require downloadable input
files, exact reproducibility, toolbox coverage, or final task buildability; later stages check those properties.

Classify with exactly one decision:
- computational_content_confirmed: pure computational chemistry with no new author physical experiment.
- computational_primary_mixed_confirmed: computation is primary and author experiments validate or support it.
- computational_experimental_co_primary_confirmed: computation and physical experiments make comparably
  indispensable contributions to the central result.
- experimental_primary_benchmarkable_computation: physical experiments are primary, but a complete, non-trivial
  computational workflow generates its own chemical result and can be isolated as a meaningful evaluation subtask.
- computational_workflow_not_benchmarkable: computation exists but is incomplete, incidental, routine data
  processing, or lacks a meaningful chemical input-calculation-output chain.
- computational_content_not_found: no author-performed computational-chemistry workflow.
- uncertain: source evidence cannot establish author attribution or workflow completeness.

A benchmarkable workflow requires: (1) an identifiable chemical system, structure, reaction, material, trajectory,
or molecular model; (2) an actual author-performed calculation or simulation; (3) an identifiable method or
operation and generated chemical output such as structures, energies, barriers, spectra, mechanisms, trajectories,
rates, or quantitative properties; (4) a scientific use for that output in a claim, comparison, prediction,
explanation, or design; and (5) enough conceptual detail to define a non-trivial computation. Extensive DFT
mechanisms, transition-state/selectivity studies, adsorption or reaction-energy landscapes, electronic-structure
analyses, MD/free-energy simulations, spectroscopy simulations, and microkinetic models can qualify even when they
support an experimental paper. A lone orbital picture or isolated number without a defined workflow, routine
fitting/plotting, experimental data processing, Rietveld refinement alone, life-cycle/process modelling, database
lookup, AlphaFold-only prediction, synthesis planning, and background citations do not qualify by themselves.
Published experimental data used only for comparison are not new author experiments.

The calculation must operate on a molecular, atomistic, electronic-structure, reaction, material, thermodynamic,
kinetic, or comparable chemical model. Fitting measured spectra or transients, substituting measured values into a
standard equation, instrument calibration/conversion, statistical analysis of measurements, ML classification of
measured signals, and crystallographic refinement are experimental data analysis, not computational chemistry.
Conversely, a simulation-only paper does not need new experiments or external experimental validation to qualify;
internally generated structures, energies, trajectories, spectra, rates, or properties are valid scientific outputs.

deterministic_author_experiment_evidence contains high-precision author-laboratory sentences, but it is not
exhaustive: an empty list is not proof of a pure computational paper. You may also establish author experiments
from experimental_evidence, but must cite the exact supplied evidence IDs.

Use these consistency rules:
- Every Pass requires performed_computation=yes, complete_computational_workflow=yes,
  benchmarkable_computational_workflow=yes, valid computational evidence, and confidence above threshold.
- The four Pass labels describe scientific role only. `experiment_observes_then_computation_explains` is eligible
  when the computational workflow itself is complete and non-trivial.
- Use `computational_workflow_not_benchmarkable` when author computation is present but fails the workflow test.
- If author attribution or workflow completeness is unresolved, return uncertain rather than a Pass.

Return one compact JSON object with: decision; article_role (original_research, review, correction, editorial,
unknown); performed_computation, complete_computational_workflow, author_performed_experiments (yes, no,
  uncertain); benchmarkable_computational_workflow (yes, no, uncertain); computation_role (primary, co_primary,
  supporting, background_only, none, uncertain); evidence_direction
(pure_computation, computation_predicts_then_experiment_validates,
experiment_observes_then_computation_explains, co_equal, none, uncertain); study_mode (pure_computational,
mixed_computational_experimental, experimental_with_computational_support, noncomputational, uncertain);
central_scientific_question; primary_contribution; one computational_workflow_steps item with step_id, action,
generated_output, evidence_ids; one central_claims item with statement, computation_required, experiment_required,
evidence_ids; zero or one experimental_contributions item with statement and evidence_ids;
counterfactual_without_computation and counterfactual_without_experiments (main_claim_fails, partly_survives,
main_claim_survives, uncertain); evidence_ids; experimental_evidence_ids; conflicting_evidence_ids; rationale;
confidence from 0 to 1. Use at most 3 IDs per array and keep narrative values under 180 characters. Return JSON only."""

STAGE02_PASS_VERIFY_SYSTEM = """Independently verify a proposed Stage02 Pass using only the supplied source
evidence. You do not receive the first classifier's answer; reconstruct the workflow from the evidence. The gate asks
whether the authors performed a complete, non-trivial computational-chemistry workflow with an identifiable
chemical input/system, calculation or simulation, generated chemical output, and scientific use. Computation may
be primary, co-primary, or supporting an experimental paper. Do not reject merely because experiments produced the
paper's headline result.

Reject to computational_workflow_not_benchmarkable when computation is only a background citation, routine data
processing, fitting/plotting, a lone qualitative orbital image or isolated value without a defined workflow, or
lacks an identifiable generated chemical result. Use computational_content_not_found when no author computation
exists. Use uncertain only when author attribution or workflow completeness cannot be resolved from the packet.

Preserve the scientific-role label when supported: pure computational, computation-primary mixed, co-primary, or
experimental-primary with benchmarkable computation. An empty deterministic experiment list is not proof that
author experiments are absent.

Do not require experimental validation, external gold data, downloadable inputs, or final benchmark ground truth.
Those are later-stage checks. A complete simulation-only workflow qualifies. However, measured-data fitting,
instrument calibration or conversion, equation substitution, Rietveld refinement, and ML classification of
experimental signals are not computational chemistry. A proposed mechanism without an actual calculation is not
a computational workflow.

For the boolean axes, apply these examples exactly:
- simulation-only DFT/MD with defined systems and generated results but no experiment/gold data: all positive
  workflow axes=yes, experimental_data_analysis_only=no;
- fitting spectra/transients, instrument calibration, equation substitution, Rietveld refinement, or ML on measured
  signals: experimental_data_analysis_only=yes and actual_chemical_calculation_or_simulation=no;
- proposed mechanistic diagram with no executed calculation: author_performed_computation=no;
- one isolated orbital picture or number without a defined multi-step scientific calculation:
  nontrivial_computational_workflow=no.
Lack of external validation MUST NEVER turn any positive workflow axis to no.

Return compact JSON only with: decision (one of the seven Stage02 decisions); author_performed_computation,
complete_computational_workflow, identifiable_chemical_model, actual_chemical_calculation_or_simulation,
generated_chemical_output, scientific_use_of_computational_output, nontrivial_computational_workflow,
experimental_data_analysis_only, author_performed_experiments (each yes, no, uncertain); computational_input,
computational_operation, generated_output, scientific_use (strings under 160 characters); evidence_ids,
computational_evidence_ids, and experimental_evidence_ids (each at most 3 supplied IDs); rationale under 220
characters; confidence from 0 to 1."""

STAGE03_SYSTEM = """Inventory the software used by a paper already confirmed to contain a benchmarkable
computational-chemistry workflow.
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

STAGE05_ROUTER_SYSTEM = """You are Stage05A, a high-recall evidence router for computational-chemistry papers.
Do not decide final benchmark suitability and do not reject a paper merely because sampled evidence is incomplete.
Using the supplied main-paper and SI index, locate up to the configured candidate limit of coherent computational
workflows. Group evidence by scientific workflow, not by software name. For each workflow cluster return exact
evidence IDs for method, input assets, parameters, computed results, scientific claims, and resource/cost facts.
Also identify related document sections and missing evidence that Stage05B must resolve.

Return one compact JSON object with decision, coverage_status, workflow_clusters, unresolved_locations, rationale,
and confidence. decision is computational_candidates_found or no_candidate_located. coverage_status is complete or
partial. Each workflow cluster contains candidate_id, task_directions (taxonomy identifiers), scientific_question,
method_evidence_ids, input_evidence_ids, parameter_evidence_ids, result_evidence_ids, claim_evidence_ids,
cost_evidence_ids, related_section_ranges, and missing_evidence. Every evidence ID must come from index_blocks.
Finding no candidate is routing information only; Stage05B independently audits the code-selected fallback evidence.
Return JSON only."""

STAGE05_SYSTEM = """You are Stage05B, the final paper-screening gate before an expensive benchmark Builder. You are not
the Builder and must not require a finished input deck, final hidden-answer package, or completed task at this
stage. Decide whether the paper contains one scientifically meaningful computational candidate that is worth
Builder effort. The paper has already passed computational-content, software-catalog, and deep-PDF parsing stages,
but scientific completeness, required software, recoverability, and cost still require evidence-based review.
Identify zero or one strongest nontrivial candidate task
only within the supplied taxonomy. A candidate must reproduce a clear scientific claim or key intermediate,
contain at least two dependent scientific computational/analysis stages, include a scientific validation gate, separate public
input from hidden targets, have a machine-computable score, use only Stage03-covered required software, and
fit the budget. Reading existing output, copying a table value, plotting supplied answers, or one trivial single
point is not a task. Published numerical results may be used as private hidden targets: they are not public inputs
and must not be exposed to the evaluated agent. Recomputing them through a nontrivial workflow is valid.

This gate is deliberately recall-oriented because Stage06 Builder and Stage07 Judge provide later precision gates.
Reject only for a documented hard blocker. Missing ready-made files, ordinary numerical convergence settings, or
uncertainty about whether bounded evidence recovery will succeed are not hard blockers; forward them for Builder
review. Do not weaken software coverage, task-defining chemical identity, target independence, scoreability, or the
resource budget.

The Stage05A route is a navigation aid, not a scientific conclusion. Independently judge the cited source blocks.
Return one JSON object with decision (pass, needs_builder_review, or reject), candidates, abstention_reasons,
blocking_dimensions, blocking_software, review_dimensions, review_reasons, evidence_ids, rationale, confidence.
Each candidate needs candidate_id, builder_route,
task_direction, scientific_question,
claim_reference, workflow_steps, validation_gates, public_input_requirements, hidden_targets, scoring_metrics,
ground_truth_level (A/B/C/D), required_software, estimated_cost, audit_dimensions, evidence_ids, and
significance_rationale. A candidate with unresolved but reviewable gaps also needs recoverability_plan, an object keyed by every
uncertain dimension. Each entry contains resolution_type, procedure, source_evidence_ids, target_independent, and
assumptions. assumptions must explicitly list every task-defining choice not fixed by cited evidence; an empty list
records the choices that Stage06 must validate. It must be empty for extraction/conversion/identifier retrieval;
evidence_anchored_construction may list bounded choices fixed by cited evidence or exhaustive target-independent
enumeration, and normalized_protocol must list ordinary numerical choices delegated to the frozen protocol.
resolution_type is exactly evidence_extraction, format_conversion,
evidence_verification, evidence_anchored_construction, or explicit_identifier_retrieval. An
explicit_identifier_retrieval entry additionally contains identifier_kind
and identifier_value; the exact identifier must appear in cited source evidence. Valid identifiers are a reported
SMILES/InChI string, DOI, or repository accession such as CCDC, ICSD, COD, PubChem CID, or Materials Project mp-ID.
A molecule name, formula, facet label, or generic database name is not an explicit identifier. source_evidence_ids must cite the supplied evidence
that anchors the procedure; target_independent must be true. assumptions must be empty except for
normalized_protocol, where it explicitly records the ordinary numerical choices delegated to the frozen protocol.
Use evidence_verification only to resolve a mapping, transcription, or interpretation against supplied evidence;
it must not construct a missing scientific structure or model. Any procedure that constructs a slab, structure,
configuration, defect model, coordinates, or force field must use evidence_anchored_construction.
resolution_type may also be normalized_protocol for ordinary numerical settings that do not define the chemical
system. It requires protocol_id="researchchembench_normalized_v1" and a nonempty assumptions array naming every
setting that the frozen protocol will select. It may cover convergence thresholds, k-point density, vacuum size,
integration grid, output frequency, or sampling duration after the chemical system and scientific comparison are
already fixed. It cannot choose charge, protonation, multiplicity, composition, structure identity, defect
placement, adsorption site set, reaction path, force-field family, or any value by matching a hidden result.

workflow_steps is a dependency graph encoded as an array of objects. Every object contains step_id, action,
depends_on, input_artifact, output_artifact, software, method_parameters, and evidence_ids. A valid graph has at
least two scientific steps, at least one dependency edge, unique step IDs, valid acyclic dependencies, and a
final computed artifact linked to the claim. Independent reference calculations may be separate roots only when a
downstream comparison consumes all branches; the full graph must remain connected. Input preparation, launching
software, and reading output are not scientific steps.

audit_dimensions contains exactly scientific_significance, workflow_completeness, input_assets, parameters,
ground_truth, software, cost, and leakage_risk. Each value is an object with state (confirmed, uncertain, failed),
support, missing_fields, and evidence_ids. confirmed and failed require source evidence; uncertain must name the
missing fields. Never mark a fact confirmed solely from Stage05A prose.

This is an evidence-readiness audit, not a file-packaging audit. Mark a dimension confirmed when the supplied main
paper or SI semantically fixes the required information, even when the Builder must still extract it from a table,
split a coordinate appendix, convert a reported format, or write an executable input deck. These routine,
target-independent materialization operations are normal Builder work and do not make a candidate uncertain.
For example, labeled SI Cartesian coordinates are confirmed input assets; a clearly identified numeric SI table is
confirmed ground truth; and an explicitly reported method/basis/charge/spin protocol is confirmed parameters.
Do not require ready-made XYZ/POSCAR/input files or an already assembled hidden-answer JSON package for pass.
If the SI label and the paper/SI structure label establish the mapping, checking atom count, connectivity, units,
or transcription after extraction is routine Builder validation and remains confirmed. Do not downgrade it merely
because the Builder must "verify" the extraction.

Use uncertain only when a fact needed by the task is plausibly recoverable but its identity, mapping, transcription,
or interpretation still requires a bounded verification step. Use failed when the information is absent,
contradictory, depends on unavailable bespoke author assets, or can only be supplied through a subjective scientific
choice. A parser omission alone is uncertain if the supplied document inventory and cited evidence identify exactly
where the Builder can verify it; an unsupported hope that the information exists elsewhere is failed.

Prefer the smallest self-contained task that tests a scientifically meaningful claim or key intermediate. Do not
append expensive downstream training, sampling, or screening merely to inflate workflow depth. Preparation,
calculation, convergence analysis, and quantitative comparison may be dependent stages when they produce and
validate distinct artifacts. Conversely, do not split one calculation into artificial stages.

A bounded candidate may use one explicitly identified molecule, surface, pathway, state, or comparison from a
larger paper when that subset has its own evidence-complete nontrivial workflow and tests a concrete reported claim.
Do not require every analogous system in the paper to be reconstructable. The subset must be fixed from public
paper identifiers before hidden values are read; cherry-picking whichever system best matches a target is leakage.
A supporting computation may qualify when it contains a complete meaningful computational workflow and a
quantitative claim, even if the paper also contains experiments or the computation is not the sole headline result.
Scientific significance means that recomputing the result tests a stated chemical interpretation, comparison,
mechanism, trend, structure-property relationship, or key intermediate. It does not require the computation to be
the paper's headline contribution. A quantitative value, ordering, class, sign, threshold, or structured trend is
machine-scoreable when the mapping to the frozen candidate is explicit.

Every field marked confirmed must be supported by supplied evidence. Use needs_builder_review, rather than reject,
when the scientific candidate is otherwise suitable but a bounded verification is still required to establish an
input, task-defining parameter, or hidden target. Recoverable examples include resolving an ambiguous structure-to-
label mapping in an SI coordinate appendix; checking an explicitly cited deposition; verifying a partially parsed
parameter table; or following a fully stated, evidence-anchored construction protocol. The recovery procedure must
be fixed without viewing or optimizing against the hidden target. In contrast, merely extracting or converting
already unambiguous supplied evidence belongs to the Builder and should be pass, not needs_builder_review.
Evidence-anchored construction is reviewable when cited evidence freezes the chemical identity and scientific
comparison, while the Builder may still apply the frozen normalized protocol to ordinary numerical settings. A
plan is failed if it asks the Builder to choose structure identity, adsorption sites, orientation, termination,
protonation, spin state when chemically task-defining, force-field family, defect placement, initial bespoke
configuration, or another scientific degree of freedom. Convergence testing may validate a frozen protocol, but
it must not choose the protocol by agreement with a published result.

Do not call a task-defining gap recoverable by substituting software defaults, customary settings, a typical model, uncited
literature values, a new calculation that decides what the authors meant, or any parameter selected by agreement
with the published result. A contradictory task-defining parameter is failed, not uncertain. Ground truth is
recoverable only when supplied evidence identifies the exact table, figure, or machine-readable block containing
a quantitative target; saying that a value may exist elsewhere is insufficient. Figure digitization is allowed
only when the supplied evidence identifies a quantitative axis/scale and the exact target series.
Quantitative targets may be distributed across several cited text blocks or SI tables. They need not appear in one
central table, provided each target is unambiguously mapped to the frozen candidate and supports a machine-
computable metric with units/tolerances that Builder can define without scientific guesswork.

Reject an asset gap when the proposed result depends on a bespoke, nonstandard object that cannot be uniquely
reconstructed: for example an absent amorphous/AIMD-generated configuration, custom grain boundary or interface,
undocumented trained model, unavailable paper-specific force field, proprietary trajectory, or exact author input
whose recreation requires subjective scientific choices. "Available from authors" without supplied assets is not
a recovery plan. Do not reject a standard molecule or crystal merely because Cartesian coordinates/POSCAR are not
already packaged; explain the deterministic Builder check under needs_builder_review.

A reported standard surface and adsorbate is reviewable only when the paper evidence or an explicitly cited public
source fixes the slab construction and adsorption-site enumeration. The hidden
energy or published preferred site may score that frozen protocol but must never choose the slab, site, orientation,
termination, pseudopotential, k-point mesh, or convergence settings. A named molecule with unambiguous constitution
and stated charge/protonation context is potentially recoverable. In contrast, the relative registry, defect
pattern, termination, atom substitutions, or morphology of a paper-specific heterointerface, grain boundary,
amorphous phase, supported cluster, or trained model is bespoke unless the paper/SI supplies a deterministic
construction. Never replace a missing or inconsistent task-defining setting with a customary or "standard" guess;
contradictory method/system parameters are a hard parameters blocker.

A Stage03 resource decision of cost_unconfirmed is not proof of feasibility, but an exact reported wall time is
not required. Select a deliberately bounded candidate and make a conservative coarse upper-bound estimate from
method family, system scale, sampling length, and job count. Cost is confirmed for this gate when that conservative
scope clearly fits the configured budget; reject when the smallest scientifically faithful task clearly exceeds
the budget or its scale is genuinely unbounded. Do not reproduce an entire high-throughput campaign when a bounded,
nontrivial subtask directly tests a reported claim, and never set runtime equal to the budget merely because it is
the limit.
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

estimated_cost must contain numeric runtime_hours, cpu_cores, gpus, and job_count plus a concise evidence-based
basis and confidence (high/medium). Software, cost, scientific significance, workflow completeness, and leakage
risk must be confirmed for every forwarded candidate. decision=pass requires all eight dimensions confirmed under
the evidence-readiness definition above, not pre-built files.
decision=needs_builder_review requires at least one of input_assets/parameters/ground_truth uncertain, none failed, and a
specific recoverability_plan. If an essential engine is unnamed or absent from Stage03 coverage, either define a
scientifically self-contained candidate that genuinely does not depend on that engine or reject; never omit an
essential program from required_software.

builder_route is exact_reproduction for pass, evidence_recovery when all uncertain dimensions can be resolved from
paper/SI/explicit identifiers without unresolved choices, or normalized_reconstruction when any recovery entry uses
the frozen normalized protocol or records bounded assumptions/enumeration. A normalized reconstruction is a new
protocol-calibrated benchmark target, not a claim of exact author input reproduction; Stage06 must preserve this
provenance.

Contract requirements are strict:
- task_direction must be exactly one identifier from the supplied taxonomy array; never use "forward", "reverse",
  a display label, or a new category.
- workflow_steps must be an array of dependency-step objects. validation_gates, scoring_metrics,
  required_software, and evidence_ids must be JSON arrays.
- required_software must contain the software names used by Stage03, not a comma-separated string.
- evidence_ids may cite only IDs from evidence_blocks. Stage03 workflow summaries intentionally contain no
  reusable evidence IDs because they came from a different parser namespace.
- blocking_dimensions and review_dimensions must be JSON arrays drawn only from scientific_significance,
  workflow_completeness, input_assets, parameters, ground_truth, software, cost, and leakage_risk. Include software in blocking_dimensions if
  blocking_software is nonempty, or if inventory_status is software_inventory_unconfirmed and the unnamed
  essential engine prevents construction. Software, cost, and scientific_significance cannot be review-only.
- decision=pass requires exactly one complete candidate and empty blocking_dimensions, blocking_software,
  review_dimensions, review_reasons, and abstention_reasons.
- decision=needs_builder_review requires exactly one candidate, empty blocking_dimensions/blocking_software and
  abstention_reasons, and nonempty review_dimensions/review_reasons consistent with uncertain audit dimensions;
  recoverability_plan must contain one valid entry for every uncertain dimension and no other dimensions.
- decision=reject requires nonempty blocking_dimensions and abstention_reasons, empty candidates, and empty
  review_dimensions/review_reasons. It also requires nonempty hard_blockers. Each hard blocker contains code,
  dimension, reason, and evidence_ids. code is exactly no_substantive_computation, essential_software_uncovered,
  no_machine_scoreable_target, task_defining_identity_missing, bespoke_author_asset_unavailable,
  hidden_target_required_for_input, or cost_exceeds_budget. Do not use reject for a recoverable gap.

Decision contrasts:
- Reported Gaussian optimization/frequency/energy workflow with SI coordinates and numerical energies: pass when
  software and cost fit, even though the Builder must extract coordinates and generate Gaussian input files.
- A numeric target clearly identified in a supplied SI table: ground_truth confirmed and potentially pass even if
  the Builder must parse the cells and normalize units.
- Labeled Cartesian coordinate blocks whose labels map to the reported molecular structures: input_assets
  confirmed and potentially pass; post-extraction atom-count/connectivity checks are normal Builder work.
- A larger study with one explicitly labeled structure/pathway that has coordinates, method parameters, and a
  quantitative reported result: audit that bounded workflow; do not reject it merely because analogous systems are
  incomplete or the values occur in separate cited blocks.
- Reported VASP adsorption workflow on named standard facets with settings and quantitative adsorption targets,
  but no POSCAR: needs_builder_review when the facet, termination, adsorbates, and site set are fixed; ordinary slab
  convergence settings may use normalized_protocol. If the adsorption site set or termination is unknown and must
  be chosen from the hidden energy, reject.
- A molecular workflow whose exact protonation or force-field source is explicitly identified but still needs
  verification: needs_builder_review, provided the scientific candidate and conservative cost are bounded.
- An AIMD claim dependent on an absent author-generated amorphous structure, or an interface/trajectory/custom
  runtime that cannot be uniquely recreated: reject for input_assets or parameters.
- A lone HOMO/LUMO picture, copied table, plot-only operation, or arbitrary tiny subset unrelated to a concrete
  claim: reject for scientific_significance.

Scientific-completeness rules:
- Two stages must produce dependent scientific artifacts, not verbs applied to one output. Input-file preparation,
  launching software, and reading its value do not count as scientific stages.
- A substantive calculation followed by a distinct property/topology/spectral/statistical analysis or comparison
  can qualify. A single calculation can also qualify when it generates multiple objective outputs that jointly test
  a stated claim and the validation gate is more than copying one published scalar.
- A compact workflow can qualify when it produces multiple dependent results, such as optimization -> frequency
  verification/thermochemistry -> property or barrier calculation -> quantitative comparison to a claim.
- An MD workflow may target solvation structure, transport, interaction statistics, or a quantitative structural
  observable under molecular_dynamics_free_energy; an explicit free-energy calculation is not mandatory.
- A task with only qualitative orbital pictures or a small repeating-unit geometry change must still establish a
  nontrivial chemical claim, quantitative hidden target, and meaningful validation; otherwise reject.

Minimal shape example (values are illustrative only):
{"decision":"pass","candidates":[{"candidate_id":"candidate-1","builder_route":"exact_reproduction",
"task_direction":"reaction_mechanism_selectivity","scientific_question":"...",
"claim_reference":"Figure 3","workflow_steps":[
{"step_id":"s1","action":"geometry optimization","depends_on":[],"input_artifact":"starting geometry",
"output_artifact":"optimized minimum","software":"Gaussian","method_parameters":{"method":"DFT"},
"evidence_ids":["mineru-evidence-id"]},
{"step_id":"s2","action":"frequency calculation","depends_on":["s1"],
"input_artifact":"optimized minimum","output_artifact":"frequencies and thermochemistry",
"software":"Gaussian","method_parameters":{},"evidence_ids":["mineru-evidence-id"]},
{"step_id":"s3","action":"barrier comparison","depends_on":["s2"],
"input_artifact":"validated thermochemistry","output_artifact":"relative free-energy barrier",
"software":"Gaussian","method_parameters":{},"evidence_ids":["mineru-evidence-id"]}],
"validation_gates":["gate"],"public_input_requirements":"...","hidden_targets":"...",
"scoring_metrics":["MAE"],"ground_truth_level":"B","required_software":["Gaussian 16"],
"estimated_cost":{"runtime_hours":4,"cpu_cores":16,"gpus":0,"job_count":8,
"basis":"eight reported single-point jobs","confidence":"medium"},
"audit_dimensions":{"scientific_significance":{"state":"confirmed","support":"central claim",
"missing_fields":[],"evidence_ids":["mineru-evidence-id"]},
"workflow_completeness":{"state":"confirmed","support":"dependent workflow","missing_fields":[],
"evidence_ids":["mineru-evidence-id"]},"input_assets":{"state":"confirmed","support":"SI coordinates",
"missing_fields":[],"evidence_ids":["mineru-evidence-id"]},"parameters":{"state":"confirmed",
"support":"reported method","missing_fields":[],"evidence_ids":["mineru-evidence-id"]},
"ground_truth":{"state":"confirmed","support":"SI numeric table","missing_fields":[],
"evidence_ids":["mineru-evidence-id"]},"software":{"state":"confirmed","support":"Stage03 frozen fact",
"missing_fields":[],"evidence_ids":["mineru-evidence-id"]},"cost":{"state":"confirmed",
"support":"bounded estimate","missing_fields":[],"evidence_ids":["mineru-evidence-id"]},
"leakage_risk":{"state":"confirmed","support":"inputs independent of hidden target","missing_fields":[],
"evidence_ids":["mineru-evidence-id"]}},
"evidence_ids":["mineru-evidence-id"],
"significance_rationale":"..."}],"abstention_reasons":[],"blocking_dimensions":[],
"review_dimensions":[],"review_reasons":[],
"blocking_software":[],"evidence_ids":["mineru-evidence-id"],
"rationale":"...","confidence":"high"}. Return compact JSON only."""

STAGE06_SHARED_SYSTEM = """Build the shared, private scientific record for one approved benchmark candidate.
Use only provided evidence IDs and frozen toolbox capabilities. Do not invent files, values, parameters, or
citations. Return JSON with candidate_id, task_pair_id, scientific_record, hidden_reference, evidence_map,
required_assets, allowed_backends, allowed_actions, budget, status, abstention_reasons. Abstain when inputs,
parameters, ground truth, scoring, or supported workflow are insufficient.
Honor candidate.builder_route. exact_reproduction follows reported evidence. evidence_recovery may extract or verify
only the cited recovery plan. normalized_reconstruction may apply only protocol_id researchchembench_normalized_v1
to the explicitly listed ordinary numerical assumptions; preserve that provenance and never present the resulting
task as an exact author-input reproduction. Abstain rather than choosing a missing chemical identity, structure,
charge/protonation, defect placement, adsorption site set, reaction path, force-field family, or hidden-target-
guided parameter."""

STAGE06_AUTONOMOUS_SYSTEM = """Write the autonomous-research member of a task pair from the supplied shared
record. Reveal the scientific question and starting inputs but do not reveal the paper's route, intermediate
answers, final answers, hidden tolerance, or hidden reference. Return JSON with task_pair_id, mode,
task_info, task_markdown, public_assets, rubric_public, leakage_checks, status, abstention_reasons."""

STAGE06_REPRODUCTION_SYSTEM = """Write the paper-reproduction member of a task pair from the supplied shared
record. Reveal the protocol, supported software, parameters, and validation requirements needed to reproduce
the work, but do not reveal answer values or hidden scoring tolerances. Return JSON with task_pair_id, mode,
task_info, task_markdown, public_assets, rubric_public, leakage_checks, status, abstention_reasons."""

STAGE07_SYSTEM = """Independently judge one generated ResearchChemBench task pair. You did not participate in
building it. Check source fidelity, scientific significance, nontrivial workflow depth, input sufficiency,
toolbox support, public/hidden separation, machine scoring, ground-truth quality, and resource feasibility.
Do not repair the task or infer missing evidence. Return JSON with decision (pass/revise/reject), findings,
required_revisions, evidence_ids, confidence, rationale. A pass means it is ready for a separate Gold Run;
it does not claim execution succeeded."""
