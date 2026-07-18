#!/usr/bin/env python3
"""Probe backend runtimes; profiles no longer own public MCP tools or tests."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evaluation.mcp_tools.profiles import load_profile_config
from researchchem_toolbox.catalog import backend_specs, validate_catalog
from researchchem_toolbox.runtime import probe_all_backends


def comma_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", default="")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--require-available", action="store_true")
    parser.add_argument("--live-network", action="store_true", help="Compatibility flag; no network call is made by a health probe.")
    parser.add_argument("--warnings-as-errors", action="store_true", help="Compatibility flag retained for scripts.")
    args = parser.parse_args()
    del args.live_network, args.warnings_as_errors

    validate_catalog()
    config = load_profile_config()
    profiles = config["profiles"]
    selected = comma_list(args.profiles) or list(profiles)
    unknown = sorted(set(selected) - set(profiles))
    if unknown:
        raise SystemExit(f"Unknown profiles: {unknown}")
    ids = [backend for name in selected for backend in profiles[name]["backends"]]
    specifications = [backend_specs()[backend_id] for backend_id in ids]
    health = probe_all_backends(specifications)
    if args.json:
        print(json.dumps(health, ensure_ascii=False, indent=2))
    else:
        for name in selected:
            print(f"[{name}]")
            for backend_id in profiles[name]["backends"]:
                item = health[backend_id]
                print(f"  {backend_id:28s} {item['status']}")
    unavailable = [backend_id for backend_id, item in health.items() if not item["available"]]
    if args.require_available and unavailable:
        print("Unavailable backends: " + ", ".join(unavailable))
        return 1
    print(f"Probed {len(health)} backends across {len(selected)} runtimes; public catalog remains 44 tools")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
