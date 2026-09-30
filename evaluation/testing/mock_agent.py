"""Small subprocess agent used to test the benchmark harness without API calls."""

from __future__ import annotations

import argparse
import json
import os
import uuid
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--prompt-file", type=Path, required=True)
    args = parser.parse_args()

    recovery = os.environ.get("RESEARCHCHEMBENCH_RECOVERY_ENABLED") == "1"
    if recovery:
        from chemistry_toolbox.mcp.execution_store import ExecutionStore
        store = ExecutionStore(args.workspace, run_id=os.environ["RESEARCHCHEMBENCH_RUN_ID"])
        manifest = store.get_record("run", "manifest", {})
        session_id = manifest.get("provider_session_id") or str(uuid.uuid4())
        store.put_record("mock_session", session_id, {"cwd": str(args.workspace)}, immutable=True)
        print(json.dumps({"type": "thread.started", "thread_id": session_id}), flush=True)
        if os.environ.get("RCB_MOCK_SLEEP_SECONDS"):
            import time
            time.sleep(float(os.environ["RCB_MOCK_SLEEP_SECONDS"]))
        first = not store.get_record("mock", "disconnected")
        if os.environ.get("RCB_MOCK_DISCONNECT_ONCE") and first:
            store.put_record("mock", "disconnected", True)
            print(json.dumps({"type": "turn.completed", "turn_id": "mock-first", "usage": {"input_tokens": 7, "output_tokens": 3}}), flush=True)
            return 7

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
    if recovery:
        print(json.dumps({"type": "turn.completed", "turn_id": "mock-final", "usage": {"input_tokens": 5, "output_tokens": 2}}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
