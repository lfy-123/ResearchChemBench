"""Build evidence or rescore saved outputs without launching an agent/job."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluation.provenance.evidence_archive import build_run_index, open_archive, write_index
from .evidence import build_evidence_bundle


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--workspace", type=Path)
    source.add_argument("--archive", type=Path)
    parser.add_argument("--rules", type=Path, help="Explicit task repository root for new rules")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--evidence-only", action="store_true")
    parser.add_argument("--resume", action="store_true", help="Resume the scoring version in --output-dir")
    parser.add_argument("--retry-in-doubt", action="store_true", help="Explicitly accept a possible duplicate billed request")
    parser.add_argument("--budget", type=Path, help="JSON ScoringBudget overrides, frozen per scoring version")
    parser.add_argument("--max-format-repairs", type=int, help="Bounded contract repair rounds, frozen per scoring version (new default: 2)")
    parser.add_argument("--evidence-max-chars", type=int, default=250000,
                        help="Explicit evidence text budget; insufficient key evidence yields needs_review")
    args = parser.parse_args(argv)
    index = open_archive(args.archive) if args.archive else build_run_index(args.workspace)
    if args.evidence_max_chars < 1: parser.error("--evidence-max-chars must be positive")
    workspace = args.archive / "workspace" if args.archive else args.workspace
    rules = args.rules or (args.archive / "task_snapshot" if args.archive else None)
    if args.evidence_only:
        bundle = build_evidence_bundle(index, {"max_chars": args.evidence_max_chars})
        args.output_dir.mkdir(parents=True, exist_ok=False)
        write_index(index, args.output_dir)
        (args.output_dir / "evidence.json").write_text(json.dumps(bundle, ensure_ascii=False, indent=2))
        print(json.dumps(bundle["coverage"], ensure_ascii=False))
        return 0
    from .service import score_workspace
    result = score_workspace(workspace, rules_root=rules, output_dir=args.output_dir,
                             evidence_index=index, evidence_max_chars=args.evidence_max_chars, publish=False,
                             budget=json.loads(args.budget.read_text()) if args.budget else None,
                             resume=args.resume, retry_in_doubt=args.retry_in_doubt, max_format_repairs=args.max_format_repairs)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    from ..execution.resume_policy import execution_exit_code
    return execution_exit_code("completed", result.get("evaluation_status", "unknown"))


if __name__ == "__main__":
    raise SystemExit(main())
