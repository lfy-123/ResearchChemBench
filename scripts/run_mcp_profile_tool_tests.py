#!/usr/bin/env python3
"""Run every one-file-per-tool test in its owning MCP profile environment."""

from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_ROOT = ROOT / "evaluation" / "mcp_tools" / "test_tools"


def comma_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", default="")
    parser.add_argument("--live-network", action="store_true")
    parser.add_argument("--warnings-as-errors", action="store_true")
    args = parser.parse_args()

    from evaluation.mcp_tools.profiles import (
        load_profile_config,
        profile_environment_path,
        profile_runtime_environment,
    )

    config = load_profile_config()
    profiles = config["profiles"]
    selected = comma_list(args.profiles) or list(profiles)
    unknown = sorted(set(selected) - set(profiles))
    if unknown:
        raise SystemExit(f"Unknown profiles: {unknown}")

    failed: list[str] = []
    tested = 0
    for name in selected:
        profile = dict(profiles[name])
        profile["name"] = name
        python = profile_environment_path(profile) / "bin" / "python"
        if not python.is_file():
            print(f"FAIL {name}: missing Python at {python}")
            failed.append(name)
            continue
        tests = [TEST_ROOT / f"test_{tool}.py" for tool in profile["tools"]]
        missing = [path for path in tests if not path.is_file()]
        if missing:
            print(f"FAIL {name}: missing tests: {', '.join(str(path) for path in missing)}")
            failed.append(name)
            continue

        environment = os.environ.copy()
        environment.update(profile_runtime_environment(name))
        environment["CHEMGRAPH_ROOT"] = str((ROOT.parent / "ChemGraph").resolve())
        environment["PYTHONPATH"] = os.pathsep.join(
            [str(ROOT), str(ROOT.parent / "ChemGraph" / "src"), environment.get("PYTHONPATH", "")]
        )
        if args.live_network:
            environment["RESEARCHCHEM_LIVE_NETWORK_TESTS"] = "1"
        else:
            environment.pop("RESEARCHCHEM_LIVE_NETWORK_TESTS", None)

        command = [str(python), "-m", "pytest", "-q"]
        if args.warnings_as_errors:
            command.extend(["-W", "error::RuntimeWarning"])
        command.extend(str(path) for path in tests)
        print(
            f"\n=== {profile['conda_name']} ({name}): {len(tests)} tools ===",
            flush=True,
        )
        completed = subprocess.run(command, cwd=ROOT, env=environment, check=False)
        tested += len(tests)
        if completed.returncode:
            failed.append(name)

    print(f"\nProfile tool tests: {tested} tool files across {len(selected)} profiles")
    if failed:
        print("Failed profiles: " + ", ".join(failed))
        return 1
    print("All selected profile tool tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
