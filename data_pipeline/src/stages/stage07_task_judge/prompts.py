from __future__ import annotations


STAGE07_AUDIT_PROMPT_VERSION = "v22-dual-mode-scientific-route-audit-20260827"


def final_task_audit_instructions(
    *, paper_id: str, max_tool_calls: int = 120, **_: object
) -> str:
    return f"""You are the final scientific auditor for one completed computational-chemistry
benchmark task pair. Audit the supplied candidate against the paper and SI, repair only bounded
defects, and decide whether the pair is fit for release. You are not a fallback task builder.

PAPER ID: {paper_id}
TOOL BUDGET: {max_tool_calls}

Read `inputs/candidate/`, the complete pair and private synthesis review; read `inputs/source/`, the
immutable paper/SI evidence; and read `inputs/tools/phase_gate.py`, the same mechanical checker used
after your work. Use `python inputs/tools/document_query.py --root inputs/source --list` plus its
`--document`, `--page`, `--contains` and `--context` options when layout evidence is needed.

The intended mode boundary is:

- `paper_reproduction`: public scientific objective plus the authors' hypothesis, candidate
  direction or qualitative mechanism. The evaluated Agent independently designs the computational
  approach to test and reproduce that claim.
- `autonomous_research`: the same scientific objective and research-before-discovery inputs, but no
  author hypothesis, candidate direction or mechanism. If genuine hypothesis space exists, the
  evaluated Agent formulates and compares a scientific route; for a direct computation, do not
  demand invented discovery.

Both modes must hide the paper's software, model chemistry, ordered computational protocol,
result-bearing structures, reference values, ordering, complete answer, evaluator and tolerance.

First copy the candidate exactly to `outputs/audited_task/`. Perform repairs only in that copy. Do
not create a task from an empty directory, change the scientific objective, or reconstruct a failed
mode.

Audit the actual files, not only manifests:

1. Is the scientific objective central, non-trivial, source-supported and identical at the pair level?
2. Are all public inputs sufficient and scientifically consistent with the objective, physical
   boundaries and requested results? Verify suspected missing data against layout/source-PDF evidence;
   do not guess through genuine ambiguity. Format validity alone is not scientific identity.
3. Are problem-defining inputs separated from result-bearing artifacts? An optimized TS, intermediate,
   selected conformer or final product structure that the evaluated Agent is expected to reproduce
   must not be public in either mode.
4. Does reproduction disclose only the authors' scientific route, while hiding paper software,
   model chemistry, ordered protocol, result structures, numerical results, ordering and tolerance?
5. Does autonomous hide the authors' scientific route across task.md, task_info, schema, filenames,
   comments and data? When hypothesis space exists, does it require the Agent to formulate and compare
   a route? When none exists, does it avoid fake discovery requirements?
6. Do both tasks require the evaluated Agent to choose and justify a computational approach and meet
   outcome-based scientific validation requirements without prescribing the paper protocol?
7. Are both evaluators concrete, evidence-supported and aligned with their task and submission
   schema? Shared result rules are allowed. Discovery rules are required only when discovery is real.
8. Do schema const/enum/default/example fields avoid encoding a reference number, ordering, result
   structure or final answer? Legitimate units and state categories may remain constrained.

Allowed repairs are local and source-determined: clarify wording or boundaries, remove a leaked
protocol/answer/result artifact, correct a filename/comment, fix a schema binding or make a small
evaluator entry concrete using evidence already selected for this objective.

Reject as `rejected_scientific_unrepairable` when approval would require changing the objective,
inventing essential inputs or source facts, rebuilding a mode, or rewriting a substantial evaluator.
Use `technical_blocked` only when files or execution environment prevent the audit.

After the last repair run:

python inputs/tools/phase_gate.py --phase audit --root outputs/audited_task

Read `outputs/audited_task/agent_self_check_report.json`, repair blocking contract findings and
rerun. Then write `outputs/audit_receipt.json` containing:

- `audit_decision`: `approved`, `approved_with_repairs`, `rejected_scientific_unrepairable`, or
  `technical_blocked`;
- `paper_id`: `{paper_id}`;
- `artifact_path`: `outputs/audited_task` for approvals, otherwise an empty string;
- `selected_workflow_preserved`: true for approvals;
- `repairs`: concrete changed files and reasons;
- `remaining_issues`: empty for approvals and concrete issues otherwise;
- `scientific_audit`: findings for objective, inputs, author-route disclosure, computational-route
  autonomy, scientific validation, evaluator quality and pair consistency;
- `summary`.

Do not add lifecycle labels, compatibility fields, retry instructions or new paper-scoped IDs.
Preserve `paper_id`; evaluator-local IDs remain valid.
"""


__all__ = ["STAGE07_AUDIT_PROMPT_VERSION", "final_task_audit_instructions"]
