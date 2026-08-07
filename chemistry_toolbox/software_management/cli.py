"""Command-line interface for the managed chemistry software cache."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .manager import SoftwareManager
from .migrate import migrate_legacy_cache
from .migrate_v2 import migrate_v2, plan_v2, relocate_v2
from .repository_paths import rewrite_repository_paths


def _print(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="researchchem-software")
    parser.add_argument("--cache-root")
    parser.add_argument("--catalog")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init")
    status = subparsers.add_parser("status")
    status.add_argument("software_id", nargs="?")
    stage = subparsers.add_parser("stage")
    stage.add_argument("software_id")
    stage.add_argument("package")
    install = subparsers.add_parser("install")
    install.add_argument("software_id")
    install.add_argument("--package")
    verify = subparsers.add_parser("verify")
    verify.add_argument("software_id", nargs="?")
    migrate = subparsers.add_parser("migrate-legacy")
    migrate.add_argument("--legacy-root", required=True)
    migrate_v2_parser = subparsers.add_parser("migrate-v2")
    migrate_v2_parser.add_argument("--legacy-root", required=True)
    plan_v2_parser = subparsers.add_parser("plan-v2")
    plan_v2_parser.add_argument("--legacy-root", required=True)
    subparsers.add_parser("relocate-v2")
    rewrite = subparsers.add_parser("rewrite-paths")
    rewrite.add_argument("--apply", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    manager = SoftwareManager(args.cache_root, catalog_path=args.catalog)
    if args.command == "init":
        result = manager.initialize()
    elif args.command == "status":
        result = manager.status(args.software_id)
    elif args.command == "stage":
        result = manager.stage(args.software_id, args.package)
    elif args.command == "install":
        result = manager.install(args.software_id, package=args.package)
    elif args.command == "verify":
        result = manager.verify(args.software_id)
    elif args.command == "migrate-legacy":
        manager.initialize()
        result = migrate_legacy_cache(
            Path(args.legacy_root), manager.root, manager.catalog.values()
        )
    elif args.command == "migrate-v2":
        manager.initialize()
        result = migrate_v2(Path(args.legacy_root), manager.root)
    elif args.command == "plan-v2":
        result = plan_v2(Path(args.legacy_root))
    elif args.command == "relocate-v2":
        result = relocate_v2(manager.root)
    elif args.command == "rewrite-paths":
        result = rewrite_repository_paths(apply=args.apply)
    else:
        raise AssertionError(args.command)
    _print(result)
    if args.command == "verify" and any(item["status"] != "pass" for item in result):
        return 1
    return 0
