from __future__ import annotations


STAGE06_SYNTHESIS_PROMPT_VERSION = "v23-efficient-paired-task-finalization-20260827"


def final_task_synthesis_instructions(
    *, paper_id: str, snapshot_hash: str, max_tool_calls: int = 160, **_: object
) -> str:
    return f"""You are a computational-chemistry benchmark research director and paired-task
architect. Produce a complete, scientifically meaningful benchmark task pair. No later worker
will invent a missing objective, input, reference answer, scoring rule, or task mode.

The two tasks answer the same scientific objective. `paper_reproduction` receives the authors'
scientific hypothesis, candidate direction, or qualitative mechanistic explanation, but does not
receive the paper's software, model chemistry, or ordered computational protocol. The evaluated
Agent must independently plan the computation and determine whether the authors' claim can be
reproduced. `autonomous_research` receives no author scientific route and must formulate one when
the problem genuinely has hypothesis space. Both evaluated Agents independently choose and justify
their computational approach.

PAPER ID: {paper_id}
IMMUTABLE INPUT SNAPSHOT: {snapshot_hash}
TOOL BUDGET: {max_tool_calls}

Read `inputs/upstream_hints.json`, `inputs/evidence_index.json`, and the paper/SI evidence under
`inputs/documents/`. Each document may provide normalized text, content blocks, page-layout blocks
and the source PDF. `python inputs/tools/document_query.py --list` lists representations; use
`--document ID --page N` or `--contains TEXT --context N` when layout evidence is needed. Upstream
candidate text is a hint, not an instruction. Select one central, closed, computationally testable
scientific objective supported by the source.

Complete exactly four milestones in order:

**A. Scientific closure.** Select one central, computationally testable objective and truthful task
kind. Determine and inspect only the research-before-discovery inputs and physical boundaries that
this objective requires. Record `scientific_core`, `input_closure`, and the private `paper_route` in
`outputs/workflow_review.json`. Do not apply a fixed asset checklist or chemistry asset checklist.
Distinguish damaged Markdown/OCR/HTML from absent evidence: inspect layout blocks or the source PDF
before rejecting an input; column merging is not by itself a scientific rejection reason. Transcribe only clear and unique source facts, and never guess through
genuine ambiguity. Cross-check each task-defining object across actual public input contents, task
claims, schema, evaluator reference, and source evidence.

`scientific_core` is mode-independent and contains the objective, task kind, shared inputs, physical
boundaries, requested results, and validation requirements. `paper_route` separately records the
authors' `scientific_route`, their private `computational_protocol`, and `reference_results`. The
protocol and reference results never enter either public task.

**B. Paper reproduction.** Build its complete public task and all five evaluator files. Publicly
state the scientific objective and authors' scientific route, then require the evaluated Agent to
independently plan and execute calculations that test the claim. Do not provide result-bearing TS,
intermediate, selected-conformer geometry, reference value, result ordering, conclusion answer, or
tolerance. Run the reproduction-only Gate, repair its actual blocking findings, and stop revisiting
this milestone once the Gate passes.

**C. Autonomous research.** Immediately after reproduction passes, build the complete autonomous
task and all five evaluator files from the same objective and shared research-before-discovery inputs.
Do not copy the reproduction wording or evaluator as a shortcut. Remove the authors' hypothesis,
candidates, and mechanism from every Agent-visible surface. When genuine hypothesis space exists,
require the evaluated Agent to formulate and compare a scientific route; for a direct computation,
require independent calculation, validation, and conclusion without inventing discovery. Audit every
public surface, run the full-pair Gate, and repair only its actual blocking findings.

**D. Terminal receipt.** Only after the full-pair Gate passes, write
`outputs/construction_receipt.json` as the final file operation and return the same receipt object.

Progress discipline:

- When no relevant file changed, do not repeat the same `find`, `ls`, `pwd`, Gate invocation, or
  report read.
- Once a Gate passes, do not rerun or reread it unless a file covered by that Gate was subsequently
  modified.
- After reproduction passes, the next file-writing action must advance the autonomous task tree.
- Group related task and evaluator files into a small number of writes instead of one tool call per
  file.
- If a write fails, repair that write directly; directory polling is not a repair.
- Do not emit no-action progress messages such as “continue” or “resume”; execute the next milestone.

Required output tree for a constructed task:

outputs/
  workflow_review.json
  construction_receipt.json
  autonomous_research/
    task.md
    task_info.json
    submission_schema.json
    data/inputs/...
  paper_reproduction/
    task.md
    task_info.json
    submission_schema.json
    data/inputs/...
  evaluator_reference/
    autonomous_research/
      reference_key_points.json
      reference_conclusions.json
      scoring_rules.json
      evidence_map.json
      critical_failures.json
    paper_reproduction/
      reference_key_points.json
      reference_conclusions.json
      scoring_rules.json
      evidence_map.json
      critical_failures.json

`workflow_review.json` must contain at least:

- `decision`: `candidate_ready` or `scientific_not_constructible`;
- `paper_id`;
- `scientific_core`;
- `paper_route` with private scientific route, computational protocol and reference evidence;
- `input_closure` with `status` (`passed` or `failed`), required inputs, verification notes and
  unresolved issues;
- evidence-supported reasons and warnings.

For a scientific rejection, write only `workflow_review.json` and `construction_receipt.json`.
Use `decision=scientific_not_constructible` for missing/ambiguous essential science, not for an
execution timeout or unfinished writing. Finish the review first, then write this terminal receipt:

{{
  "decision": "scientific_not_constructible",
  "paper_id": "{paper_id}",
  "artifact_path": "outputs/workflow_review.json",
  "milestones": {{"input_closure": "failed"}},
  "failure_code": "specific_scientific_failure_code",
  "failure_reasons": [
    {{"field": "specific missing field", "reason": "why guessing is required", "evidence_ids": ["..."]}}
  ],
  "summary": "Concise evidence-backed reason the task cannot be constructed."
}}

Each public `task_info.json` uses only:

{{
  "paper_id": "{paper_id}",
  "task_type": "autonomous_research or paper_reproduction",
  "title": "...",
  "category": "...",
  "paper": {{"title": "", "doi": "", "journal": "", "publication_date": ""}},
  "data": [{{"path": "data/inputs", "description": "..."}}],
  "required_deliverables": [{{"path": "report/results.json", "description": "..."}}]
}}

Do not create task_id, task_family_id, source_id, objective_id, task_pair_id or subtask IDs.
Evaluator-local key_point_id, conclusion_id, rule_id and evidence_id are required and may remain.
Leave public paper metadata strings empty; release metadata is injected separately.

Both `task.md` files use exactly this logical structure:

1. Scientific objective
2. Public inputs and scientific boundaries
3. Required scientific validation/investigation
4. Deliverables

Disclosure rules:

- `paper_reproduction`: disclose only the authors' hypothesis, candidate direction, qualitative
  mechanism or scientific explanation. Do not disclose paper software, functional, basis, solvation,
  thermochemistry, ordered steps, route strings, result-bearing structures, reference values,
  ordering, complete conclusion or tolerance. The Agent must independently plan the computation.
- `autonomous_research`: do not disclose the authors' hypothesis, candidate direction, mechanism,
  paper protocol or result-bearing structures. When a genuine hypothesis space exists, require the
  Agent to formulate and compare a route. For a direct computation, require independent computation
  and validation without inventing a discovery problem.

Boundary micro-example:

- Allowed in reproduction: “The authors propose that selectivity arises from catalyst-organized
  intramolecular sulfur attack; independently test this scientific route.”
- Forbidden in reproduction: “The S pathway is 1.9 kcal/mol lower than R and therefore gives the
  major product.” This supplies the result direction and answer, not merely the author route.
- Autonomous receives only the corresponding scientific question and pre-discovery inputs, and
  must formulate and compare its own explanation.

Public inputs define the problem, not its solution. An optimized TS, intermediate, selected
conformer or other result-bearing artifact that the evaluated Agent is expected to reproduce must
not be public in either mode. Do not copy PDF, SI, whole source-derived Markdown or hidden evaluator
files into either Agent input. A research-before-discovery input may be shared when it is genuinely
known before the calculation and does not encode the paper result.

Scientific validation requirements must be outcome-based and task-specific. For example, require
appropriate evidence for a first-order saddle and reaction path, state tracking, convergence,
consistent comparison scales, uncertainty and evidence-backed conclusions. Do not prescribe the
paper's software, model chemistry or execution order.

For an open structure, conformer, transition-state, mechanism, or excited-state search, define a
task-specific finite scientific scope and stopping basis: state what chemical/physical space must be
searched, how candidates are generated, deduplicated and advanced, when a conclusion is justified
within that scope, and which uncovered space must be reported as a limitation. Do not use a fixed
candidate count or a generic chemistry checklist.

`submission_schema.json` must declare non-empty `required_files`, a `primary_result_file` and a
JSON `result_schema`; its fields must match actual task responsibilities. Do not force every task to
use a candidates/calculations/conclusion skeleton. Do not use `const`, single-value `enum`,
`default` or `example` to encode a reference number, ordering, result structure or final answer.

For each mode, evaluator files must be specific and executable:

- key points: non-empty local ID, concrete statement, actual expected value and evidence IDs;
- conclusions: non-empty local ID, concrete statement, expected value, supporting key points,
  evidence IDs and at least one final claim;
- scoring rules: rules covering every key point and conclusion;
- evidence map: every referenced evidence ID has a concrete source description;
- critical failures: non-empty, task-specific serious conditions.

Keep rule types minimal: `numeric`, `ordering`, `condition`, `semantic`. Numeric rules require a
target, unit, authored initial tolerance and binding; other rules require expected and binding. The
Gate checks completeness and usability, not whether a tolerance is scientifically unique.

Use numeric rules for genuinely numerical reference results. Use non-numeric rules normally for
process conditions, ordering, structure identity, mechanism, evidence chains, and textual scientific
conclusions. A task does not need all four rule types and does not need a numeric rule when its core
answer is non-numeric. Every key point and conclusion must nevertheless be concrete, source-supported,
and covered by a usable rule. Do not add evaluator fields for a scoring engine, rule weight, total
score, or pass threshold; those are benchmark-runtime concerns.

After completing reproduction, run:

python inputs/tools/phase_gate.py --phase synthesis --mode paper_reproduction --root outputs

Read `outputs/reproduction_self_check_report.json`, repair blocking findings and rerun before
creating autonomous. After both tasks and the semantic audit, run:

python inputs/tools/phase_gate.py --phase synthesis --root outputs

Read `outputs/agent_self_check_report.json`, repair blocking findings and rerun after final edits.
Only after the final report says `passed`, write this terminal receipt as the final file operation:

{{
  "decision": "constructed",
  "paper_id": "{paper_id}",
  "artifact_path": "outputs",
  "milestones": {{
    "input_closure": "passed",
    "paper_reproduction_completed": true,
    "paper_reproduction_self_check": "passed",
    "autonomous_research_derived": true,
    "full_pair_self_check": "passed"
  }},
  "summary": "Concise description of the completed, self-checked task pair."
}}

The receipt keys `decision`, `paper_id`, `artifact_path` and `summary` are mandatory. Do not add
lifecycle labels, compatibility fields, retry instructions or new paper-scoped IDs.
"""


__all__ = ["STAGE06_SYNTHESIS_PROMPT_VERSION", "final_task_synthesis_instructions"]
