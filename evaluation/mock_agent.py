"""Small subprocess agent used to test the benchmark harness without API calls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    args = parser.parse_args()

    prompt = args.prompt_file.read_text(encoding="utf-8")
    print(json.dumps({"type": "system", "subtype": "init", "model": "mock-agent"}))
    print(json.dumps({"type": "assistant", "content": "Mock benchmark execution"}))
    report = args.workspace / "report" / "report.md"
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        "# Mock Chemistry Report\n\n"
        "This report was produced by the local harness smoke-test agent.\n\n"
        "## Prompt received\n\n"
        f"{prompt[:1000]}\n",
        encoding="utf-8",
    )
    print(json.dumps({"type": "result", "report": "report/report.md"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
