#!/usr/bin/env python3
"""Download a resumable, duplicate-free batch from an authorized Xinghe dataset."""

from __future__ import annotations

import argparse
import fcntl
import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

import boto3
from botocore.config import Config
from read_xinghe_dataset import check_path, read_access

DATASETS = {
    "en-paper-hzzj": "s3://private-cooperate-data/en-paper-hzzj/pdf/",
    "kps-20260603-bu": ("s3://private-cooperate-data/en-pdf-core-chemistry/KPS/20260603_bu/"),
    "kps-2026-06-18": ("s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-06-18/"),
    "kps-2026-05-07": ("s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-05-07/"),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--credentials", type=Path, required=True, help="path to xinghe.txt")
    parser.add_argument(
        "--dataset",
        help="dataset alias or an authorized s3:// prefix",
    )
    parser.add_argument("--count", type=int, help="number of new files")
    parser.add_argument(
        "--output",
        type=Path,
        help="output directory; defaults to datasets/<dataset alias>",
    )
    parser.add_argument(
        "--state-directory",
        type=Path,
        help="persistent manifest, cursor, and lock directory; defaults to --output",
    )
    parser.add_argument(
        "--suffix",
        default=".pdf",
        help="only download keys with this suffix; use an empty value for all objects",
    )
    parser.add_argument("--outside", action="store_true", help="use the outside endpoint")
    parser.add_argument(
        "--list-datasets", action="store_true", help="show supported aliases and exit"
    )
    return parser.parse_args()


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def read_state(path: Path, prefix: str) -> dict[str, Any]:
    if not path.exists():
        return {"dataset_prefix": prefix, "last_key": None}
    state = json.loads(path.read_text(encoding="utf-8"))
    if state.get("dataset_prefix") != prefix:
        raise ValueError(
            f"{path.parent} already contains state for {state.get('dataset_prefix')!r}; "
            "use a different output directory"
        )
    return state


def read_manifest(path: Path) -> set[str]:
    downloaded: set[str] = set()
    if not path.exists():
        return downloaded
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            record = json.loads(raw)
            downloaded.add(str(record["remote_uri"]))
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(f"invalid manifest record at {path}:{line_number}") from exc
    return downloaded


def append_manifest(path: Path, record: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def split_s3_uri(uri: str) -> tuple[str, str]:
    bucket_and_key = uri.removeprefix("s3://")
    bucket, separator, key = bucket_and_key.partition("/")
    if not separator or not bucket:
        raise ValueError(f"invalid S3 URI: {uri}")
    return bucket, key


def local_path_for_key(output: Path, prefix_key: str, key: str) -> Path:
    relative = key[len(prefix_key) :] if key.startswith(prefix_key) else key
    parts = [part for part in PurePosixPath(relative).parts if part not in ("", ".")]
    if not parts or ".." in parts:
        raise ValueError(f"unsafe object key: {key}")
    destination = output.joinpath(*parts).resolve()
    output_root = output.resolve()
    if destination != output_root and output_root not in destination.parents:
        raise ValueError(f"object key escapes output directory: {key}")
    return destination


def download_object(client: Any, bucket: str, key: str, destination: Path) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".part")
    response = client.get_object(Bucket=bucket, Key=key)
    try:
        with temporary.open("wb") as output:
            shutil.copyfileobj(response["Body"], output, length=1024 * 1024)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, destination)
    finally:
        response["Body"].close()
    return destination.stat().st_size


def main() -> int:
    args = parse_args()
    if args.list_datasets:
        for alias, prefix in DATASETS.items():
            print(f"{alias:20s} {prefix}")
        return 0
    if not args.dataset:
        raise ValueError("--dataset is required unless --list-datasets is used")
    if args.count is None or args.count < 1:
        raise ValueError("--count must be at least 1")

    access_key, secret_key, inside, outside, authorized_paths = read_access(
        args.credentials.expanduser().resolve()
    )
    requested = DATASETS.get(args.dataset, args.dataset)
    prefix = check_path(requested, authorized_paths).rstrip("/") + "/"
    endpoint = outside if args.outside else inside
    if not endpoint:
        raise ValueError("the requested endpoint is not present in the credential file")

    dataset_name = args.dataset if args.dataset in DATASETS else "custom"
    project_root = Path(__file__).resolve().parents[2]
    output = (args.output or project_root / "datasets" / dataset_name).resolve()
    output.mkdir(parents=True, exist_ok=True)
    state_directory = (args.state_directory or output).expanduser().resolve()
    state_directory.mkdir(parents=True, exist_ok=True)
    manifest_path = state_directory / "download_manifest.jsonl"
    state_path = state_directory / ".download_state.json"
    lock_path = state_directory / ".download.lock"

    bucket, prefix_key = split_s3_uri(prefix)
    suffix = args.suffix.casefold()
    client = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(
            connect_timeout=10,
            read_timeout=120,
            retries={"max_attempts": 5, "mode": "standard"},
            s3={"addressing_style": "path"},
        ),
    )

    with lock_path.open("w", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(f"another downloader is already using {output}") from exc

        state = read_state(state_path, prefix)
        downloaded_uris = read_manifest(manifest_path)
        last_key = state.get("last_key")
        downloaded_now = 0
        skipped_existing = 0
        scanned = 0

        while downloaded_now < args.count:
            request: dict[str, Any] = {
                "Bucket": bucket,
                "Prefix": prefix_key,
                "MaxKeys": 1000,
            }
            if last_key:
                request["StartAfter"] = last_key
            page = client.list_objects_v2(**request)
            objects = page.get("Contents", ())
            if not objects:
                break

            for item in objects:
                key = str(item["Key"])
                last_key = key
                scanned += 1
                state.update(
                    {
                        "dataset_prefix": prefix,
                        "last_key": last_key,
                        "updated_at": datetime.now(timezone.utc).isoformat(),
                    }
                )

                if suffix and not key.casefold().endswith(suffix):
                    atomic_write_json(state_path, state)
                    continue

                remote_uri = f"s3://{bucket}/{key}"
                destination = local_path_for_key(output, prefix_key, key)
                if (
                    remote_uri in downloaded_uris
                    and destination.exists()
                    and destination.stat().st_size > 0
                ):
                    skipped_existing += 1
                    atomic_write_json(state_path, state)
                    continue

                if destination.exists() and destination.stat().st_size > 0:
                    size = destination.stat().st_size
                    status = "adopted_existing"
                    skipped_existing += 1
                else:
                    size = download_object(client, bucket, key, destination)
                    status = (
                        "redownloaded_missing_local_file"
                        if remote_uri in downloaded_uris
                        else "downloaded"
                    )

                append_manifest(
                    manifest_path,
                    {
                        "remote_uri": remote_uri,
                        "local_path": str(destination),
                        "size_bytes": size,
                        "status": status,
                        "recorded_at": datetime.now(timezone.utc).isoformat(),
                    },
                )
                downloaded_uris.add(remote_uri)
                atomic_write_json(state_path, state)
                if status in ("downloaded", "redownloaded_missing_local_file"):
                    downloaded_now += 1
                    print(
                        f"[{downloaded_now:04d}/{args.count:04d}] "
                        f"{destination.relative_to(output)} ({size} bytes)"
                    )
                if downloaded_now >= args.count:
                    break

            if downloaded_now >= args.count or not page.get("IsTruncated"):
                break

        print(
            json.dumps(
                {
                    "dataset": args.dataset,
                    "prefix": prefix,
                    "output": str(output),
                    "state_directory": str(state_directory),
                    "requested": args.count,
                    "downloaded_now": downloaded_now,
                    "skipped_existing": skipped_existing,
                    "scanned_objects": scanned,
                    "manifest": str(manifest_path),
                    "last_key": last_key,
                },
                ensure_ascii=False,
            )
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
