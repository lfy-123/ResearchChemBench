from __future__ import annotations


STAGE07B_REPAIR_VERSION = "v1-contract-only-20260823"


def contract_repair_instructions(
    *,
    paper_id: str,
    task_pair_id: str,
    findings: list[str],
    science_hash: str,
    max_tool_calls: int,
) -> str:
    return f"""You are Stage07B, a narrow post-audit contract repair Agent.

Scientific Stage07A has already approved this task pair. Your only job is to repair the exact
transport/contract findings listed below so the existing pair can be loaded and packaged safely.
Do not reconsider the paper, workflow, scientific importance, inputs, methods, physical boundaries,
answers, tolerances, acceptance semantics, or mode scope. Do not read source papers, SI, or any
source-material packet; they are intentionally unavailable.

Paper id: {paper_id}
Canonical task-pair id: {task_pair_id}
Scientific fingerprint before repair: {science_hash}
Allowed findings (all must be addressed or explicitly reported unresolved):
{findings}

The writable candidate tree is `outputs/task_pair/`. The immutable audit context is under
`inputs/`. You may edit only these contract files:
- `paper_reproduction/task_info.json`
- `paper_reproduction/submission_contract.json`
- `paper_reproduction/public_manifest.json`
- `autonomous_research/task_info.json`
- `autonomous_research/submission_contract.json`
- `autonomous_research/public_manifest.json`
- `hidden_reference/ground_truth_common.json` only for binding paths,
  comparison/projection transport fields, or missing binding containers.
- pair-level transport manifests or normalization provenance explicitly named by a finding.

Never edit `task.md`, `data/`, workflow/objective/evidence files, route content, canonical answers,
units, tolerances, propositions, evidence IDs, mode scope, Key Points, or conclusions. In the hidden
reference, only the explicitly named binding/path/comparison/projection transport fields may change;
the science fingerprint will reject any other change. Do not add files or rename scientific assets.
Do not invent scientific aliases, values, or conclusions. If a finding cannot be repaired without a
scientific choice, return `unresolved`.

For a finding beginning with `binding_schema_path_open:` the public
`submission_contract.json` contains a structured result path that is already
referenced by an existing binding but is reachable only through an open JSON
object.  Make that existing path explicit in the schema (including nested
object properties and `required` entries when the contract already marks the
binding as required), preserving all existing schema content and
`additionalProperties` policy.  Infer only transport types from the existing
schema/binding/acceptance kind; never copy a canonical answer, target,
tolerance, proposition, or scientific label into the public schema.  Do not
create a new result field or change a binding to point elsewhere.  If the
schema cannot be made explicit without a scientific inference, report the
finding unresolved.

Before finishing, reread the candidate files, list every actual changed path, and write exactly one
receipt to `outputs/stage07b_repair.json`. Return the same JSON object in your final response:
{{
  "status": "repaired | unresolved | rejected_scope",
  "changed_files": [],
  "findings_before": {findings},
  "findings_after": [],
  "science_hash_before": "{science_hash}",
  "science_hash_after": "",
  "summary": "..."
}}

Use at most {max_tool_calls} workspace calls. This is a single bounded repair attempt; do not
perform a broad scientific review or restart Stage07A.
"""
