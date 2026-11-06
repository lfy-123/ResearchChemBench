"""Grade saved V3 outputs with a native Codex Judge; never rerun the research."""
import argparse
import json
from pathlib import Path

from evaluation.provenance.evidence_archive import open_archive
from .service import score_workspace


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--workspace", type=Path)
    source.add_argument("--archive", type=Path)
    parser.add_argument("--rules", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--publish", action="store_true", help="Publish this scoring version to the original run")
    args = parser.parse_args(argv)
    result = score_workspace(args.archive / "workspace" if args.archive else args.workspace,
        rules_root=args.rules or (args.archive / "task_snapshot" if args.archive else None),
        output_dir=args.output_dir, evidence_index=open_archive(args.archive) if args.archive else None,
        publish=args.publish, resume=args.resume)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "scored" else 2


if __name__ == "__main__":
    raise SystemExit(main())
