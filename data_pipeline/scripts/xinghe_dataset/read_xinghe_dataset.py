#!/usr/bin/env python3
"""Read the prefix-scoped Xinghe datasets through Petrel.

The credential file is never copied into source code.  It is parsed at
runtime and converted into a temporary mode-0600 Petrel configuration that
is deleted when the client exits.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Iterator

DEFAULT_PREFIX = "s3://private-cooperate-data/en-paper-hzzj/pdf/"
_CREDENTIAL_RE = re.compile(r"^(AK|SK)\s*[:：]\s*(.+)$", re.IGNORECASE)


class AccessError(ValueError):
    """Raised for malformed credentials or unauthorized object paths."""


def read_access(path: Path) -> tuple[str, str, str, str | None, tuple[str, ...]]:
    """Read AK/SK, endpoints, and explicitly authorized S3 prefixes."""
    if not path.is_file():
        raise AccessError(f"credential file not found: {path}")

    values: dict[str, str] = {}
    endpoints: list[str] = []
    prefixes: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        match = _CREDENTIAL_RE.match(line)
        if match:
            values[match.group(1).upper()] = match.group(2).strip()
        elif line.startswith(("http://", "https://")):
            endpoints.append(line.rstrip("/"))
        elif line.startswith("s3://"):
            prefixes.append(line.rstrip("/") + "/")

    if not values.get("AK") or not values.get("SK"):
        raise AccessError(f"{path} must contain AK and SK")
    if not endpoints:
        raise AccessError(f"{path} contains no object-storage endpoint")
    if not prefixes:
        raise AccessError(f"{path} contains no authorized s3:// prefix")

    inside = next((item for item in endpoints if "inside" in item), endpoints[0])
    outside = next((item for item in endpoints if "outside" in item), None)
    return values["AK"], values["SK"], inside, outside, tuple(dict.fromkeys(prefixes))


def check_path(remote_path: str, prefixes: tuple[str, ...]) -> str:
    path = remote_path.strip()
    if not path.startswith("s3://"):
        raise AccessError("remote path must start with s3://")
    if not any(path == prefix.rstrip("/") or path.startswith(prefix) for prefix in prefixes):
        raise PermissionError(
            "remote path is outside the prefixes authorized in the credential file"
        )
    return path


class XingheReader:
    """Read-only Petrel client for the paths in one credential file."""

    def __init__(self, credential_file: Path, *, outside: bool = False):
        try:
            from petrel_client.client import Client
        except ImportError as exc:  # pragma: no cover - depends on environment
            raise RuntimeError(
                "Petrel SDK is missing; install petrel-oss-sdk and boto3 in this environment"
            ) from exc

        ak, sk, inside, outside_endpoint, prefixes = read_access(credential_file)
        if outside and not outside_endpoint:
            raise AccessError("no outside endpoint is present in the credential file")
        self.prefixes = prefixes
        endpoint = outside_endpoint if outside else inside
        descriptor, name = tempfile.mkstemp(prefix="petrel-xinghe-", suffix=".conf")
        self._config_path = Path(name)
        try:
            with os.fdopen(descriptor, "w", encoding="utf-8") as config:
                config.write(
                    "[default]\n"
                    "default_cluster = cluster1\n"
                    "[cluster1]\n"
                    f"access_key = {ak}\n"
                    f"secret_key = {sk}\n"
                    f"host_base = {endpoint}\n"
                    "request_timeout = 10000\n"
                )
            self._client = Client(str(self._config_path))
        except Exception:
            self.close()
            raise

    def list_objects(
        self, remote_path: str, *, limit: int = 20, recursive: bool = False
    ) -> Iterator[str]:
        if limit < 1:
            raise ValueError("limit must be at least 1")
        target = check_path(remote_path, self.prefixes)
        bucket = target.removeprefix("s3://").split("/", 1)[0]
        items = self._client.list(target, page_size=limit, no_paginate=True, recursive=recursive)
        for index, item in enumerate(items):
            if index >= limit:
                break
            item = str(item)
            yield item if item.startswith("s3://") else f"s3://{bucket}/{item.lstrip('/')}"

    def contains(self, remote_path: str) -> bool:
        return bool(self._client.contains(check_path(remote_path, self.prefixes)))

    def size(self, remote_path: str) -> int:
        return int(self._client.size(check_path(remote_path, self.prefixes)))

    def download(self, remote_path: str, destination: Path, *, overwrite: bool = False) -> Path:
        if destination.exists() and not overwrite:
            raise FileExistsError(f"destination exists: {destination}; use --overwrite")
        payload = self._client.get(check_path(remote_path, self.prefixes))
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
        return destination.resolve()

    def close(self) -> None:
        if getattr(self, "_client", None) is not None:
            self._client = None
        config_path = getattr(self, "_config_path", None)
        if config_path is not None:
            config_path.unlink(missing_ok=True)
            self._config_path = None

    def __enter__(self) -> "XingheReader":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--credentials", type=Path, required=True, help="path to xinghe.txt")
    parser.add_argument("--outside", action="store_true", help="use the outside endpoint")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("datasets", help="print authorized S3 prefixes")
    listing = commands.add_parser("list", help="list objects below a prefix")
    listing.add_argument("remote_path")
    listing.add_argument("--limit", type=int, default=20)
    listing.add_argument("--recursive", action="store_true")

    for name in ("size", "contains"):
        command = commands.add_parser(name)
        command.add_argument("remote_path")

    download = commands.add_parser("download", help="download one object")
    download.add_argument("remote_path")
    download.add_argument("destination", type=Path)
    download.add_argument("--overwrite", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        with XingheReader(args.credentials, outside=args.outside) as reader:
            if args.command == "datasets":
                for prefix in reader.prefixes:
                    print(prefix)
            elif args.command == "list":
                for item in reader.list_objects(
                    args.remote_path, limit=args.limit, recursive=args.recursive
                ):
                    print(item)
            elif args.command == "size":
                print(reader.size(args.remote_path))
            elif args.command == "contains":
                print(reader.contains(args.remote_path))
            elif args.command == "download":
                print(reader.download(args.remote_path, args.destination, overwrite=args.overwrite))
        return 0
    except (OSError, PermissionError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
