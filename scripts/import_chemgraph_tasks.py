#!/usr/bin/env python3
"""Convert ChemGraph's bundled ground truth into ResearchChemBench tasks."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    PROJECT_ROOT.parent
    / "ChemGraph"
    / "src"
    / "chemgraph"
    / "eval"
    / "data"
    / "ground_truth.json"
)
DEFAULT_OUTPUT = PROJECT_ROOT / "tasks"


def import_tasks(source: Path, output: Path, *, force: bool = False) -> list[Path]:
    """Import all list-format ChemGraph ground-truth entries."""

    raw = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        raise ValueError("Expected ChemGraph ground_truth.json to contain a JSON list")

    output.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for index, entry in enumerate(raw, start=1):
        task_id = f"ChemGraph_{index:03d}"
        task_dir = output / task_id
        if task_dir.exists() and force:
            shutil.rmtree(task_dir)
        if task_dir.exists():
            raise FileExistsError(f"Task directory already exists: {task_dir}")

        data_dir = task_dir / "data"
        target_dir = task_dir / "target_study"
        data_dir.mkdir(parents=True)
        target_dir.mkdir(parents=True)

        task_info = {
            "task_id": task_id,
            "source_id": str(entry.get("id", index)),
            "category": entry.get("category", "uncategorized"),
            "task": entry["query"],
            "data": [],
        }
        answer = entry.get("answer", {})
        ground_truth = {
            "expected_tool_calls": answer.get("tool_calls", []),
            "expected_result": answer.get("result", ""),
            "expected_structured_output": answer.get("structured_output"),
        }

        (task_dir / "task_info.json").write_text(
            json.dumps(task_info, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        (target_dir / "ground_truth.json").write_text(
            json.dumps(ground_truth, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        (data_dir / ".gitkeep").touch()
        created.append(task_dir)

    return created


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    created = import_tasks(args.source.resolve(), args.output.resolve(), force=args.force)
    print(f"Imported {len(created)} tasks into {args.output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
