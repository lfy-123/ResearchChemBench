#!/usr/bin/env python3
"""Build the managed local documentation cache for toolbox software.

The tracked YAML stores reviewed official sources and candidate capabilities.
This script combines it with the current public catalog and requested-software
inventory, then writes per-software metadata under .software_cache.  Optional
downloads are bounded and retain URL, retrieval time, size, and SHA-256.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from researchchem_toolbox.specs import BACKEND_SPECS


SOURCE_CONFIG = TOOLBOX_ROOT / "config" / "software_capability_sources.yaml"
REQUESTED_STATUS = TOOLBOX_ROOT / "config" / "requested_software_status.json"


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


def _load() -> tuple[dict[str, Any], dict[str, Any]]:
    capability = yaml.safe_load(SOURCE_CONFIG.read_text(encoding="utf-8"))
    requested = json.loads(REQUESTED_STATUS.read_text(encoding="utf-8"))
    return capability, requested


def _requested_lookup(requested: dict[str, Any]) -> dict[str, dict[str, Any]]:
    values: dict[str, dict[str, Any]] = {}
    for item in requested.get("software", []):
        name = str(item.get("name") or "").strip()
        if name:
            values[_slug(name)] = item
    return values


def _current_actions(aliases: list[str]) -> list[str]:
    alias_slugs = {_slug(value) for value in aliases}
    actions: set[str] = set()
    for backend in BACKEND_SPECS:
        if _slug(backend.id) in alias_slugs or _slug(backend.display_name) in alias_slugs:
            actions.update(backend.capabilities)
    return sorted(actions)


def _version_candidates(item: dict[str, Any] | None, aliases: list[str] | None = None) -> list[str]:
    if not item:
        return []
    names = {_slug(str(item.get("name") or "")), *(_slug(value) for value in (aliases or []))}
    names.discard("")
    versions: set[str] = set()
    detail = item.get("environment_detail") or {}
    verification = item.get("verification") or {}
    for group in (detail.get("modules") or {}, verification.get("modules") or {}):
        if not isinstance(group, dict):
            continue
        for module_name, value in group.items():
            module_slug = _slug(str(module_name))
            if any(module_slug == name or module_slug.startswith(name + "_") or name.startswith(module_slug + "_") for name in names):
                if isinstance(value, dict) and value.get("version") and value.get("version") != "0.0.0":
                    versions.add(str(value["version"]))
    for package in [*(detail.get("conda_packages") or []), *(detail.get("pip_packages") or [])]:
        match = re.match(r"^([A-Za-z0-9_.+-]+)(?:==|=)([^=<> ]+)", str(package))
        if not match:
            continue
        package_slug = _slug(match.group(1))
        if any(package_slug == name or package_slug.startswith(name + "_") or name.startswith(package_slug + "_") for name in names):
            versions.add(match.group(2))
    if not versions:
        text = " ".join(
            [
                str(item.get("notes", "")),
                " ".join(map(str, (verification.get("commands") or {}).values())),
                " ".join(map(str, (verification.get("cache_paths") or {}).keys())),
            ]
        )
        for value in re.findall(r"\b(?:v|version\s*)?(\d+(?:\.\d+){1,3}(?:[-+._a-zA-Z0-9]*)?)\b", text):
            versions.add(value)
    return sorted(versions)


def _expanded_records(capability: dict[str, Any], requested: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Include every requested package and public backend, even before curation."""

    records = {key: dict(value) for key, value in capability.get("software", {}).items()}

    def alias_map() -> dict[str, str]:
        result: dict[str, str] = {}
        for key, value in records.items():
            for alias in [key, value.get("display_name", key), *(value.get("aliases") or [])]:
                result[_slug(str(alias))] = key
        return result

    aliases = alias_map()
    for item in requested.get("software", []):
        name = str(item.get("name") or "").strip()
        if not name:
            continue
        key = aliases.get(_slug(name))
        if key is None:
            key = _slug(name)
            source = []
            if item.get("official_url"):
                source.append(
                    {
                        "title": f"{name} official documentation or project page",
                        "url": item["official_url"],
                        "kind": "html",
                        "version_scope": "inventory",
                    }
                )
            records[key] = {
                "display_name": name,
                "aliases": [name],
                "official_sources": source,
                "candidate_actions": [],
            }
            aliases = alias_map()
        elif item.get("official_url"):
            sources = records[key].setdefault("official_sources", [])
            if not any(source.get("url") == item["official_url"] for source in sources):
                sources.append(
                    {
                        "title": f"{name} official documentation or project page",
                        "url": item["official_url"],
                        "kind": "html",
                        "version_scope": "inventory",
                    }
                )

    for backend in BACKEND_SPECS:
        key = aliases.get(_slug(backend.id)) or aliases.get(_slug(backend.display_name))
        if key is None:
            key = _slug(backend.id)
            records[key] = {
                "display_name": backend.display_name,
                "aliases": [backend.id, backend.display_name],
                "official_sources": [],
                "candidate_actions": [],
            }
            aliases = alias_map()
    return records


def _download(url: str, destination: Path, *, max_bytes: int) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "ResearchChemBench/1.0 documentation-cache"})
    hasher = hashlib.sha256()
    size = 0
    with urllib.request.urlopen(request, timeout=60) as response, destination.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > max_bytes:
                raise RuntimeError(f"download exceeds {max_bytes} bytes")
            hasher.update(chunk)
            handle.write(chunk)
        content_type = response.headers.get("content-type")
    return {"path": str(destination.relative_to(ROOT)), "bytes": size, "sha256": hasher.hexdigest(), "content_type": content_type}


def _recover_download_records(directory: Path, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rebuild snapshot metadata when older index generation dropped it."""

    recovered = []
    for number, source in enumerate(sources, start=1):
        suffix = ".pdf" if source.get("kind") == "pdf" else ".html"
        path = directory / f"official_{number}{suffix}"
        if not path.is_file():
            continue
        recovered.append(
            {
                "url": source["url"],
                "path": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "content_type": "application/pdf" if suffix == ".pdf" else "text/html",
                "recovered_from_local_snapshot": True,
            }
        )
    return recovered


def _local_document_records(values: list[str]) -> list[dict[str, Any]]:
    records = []
    for value in values:
        path = Path(str(value)).expanduser()
        if not path.is_absolute():
            path = ROOT / path
        path = path.resolve()
        item: dict[str, Any] = {"path": str(path)}
        try:
            item["path"] = str(path.relative_to(ROOT))
        except ValueError:
            pass
        if path.is_file():
            item.update(
                {
                    "available": True,
                    "bytes": path.stat().st_size,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                }
            )
        else:
            item.update({"available": False, "error": "local document missing"})
        records.append(item)
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--download", action="store_true", help="Download bounded official HTML/PDF snapshots")
    parser.add_argument("--max-mib", type=int, default=100)
    args = parser.parse_args()

    capability, requested = _load()
    requested_by_alias = _requested_lookup(requested)
    cache_root = ROOT / capability.get("cache_root", ".software_cache/documentation")
    cache_root.mkdir(parents=True, exist_ok=True)
    generated_at = datetime.now(timezone.utc).isoformat()
    index: list[dict[str, Any]] = []

    records = _expanded_records(capability, requested)
    for software_id, record in sorted(records.items()):
        aliases = list(record.get("aliases") or []) + [software_id, record.get("display_name", software_id)]
        requested_item = next((requested_by_alias.get(_slug(alias)) for alias in aliases if requested_by_alias.get(_slug(alias))), None)
        versions = [str(record["installed_version"])] if record.get("installed_version") else _version_candidates(requested_item, aliases)
        version_label = versions[0] if len(versions) == 1 else ("_".join(versions[:3]) if versions else "unknown")
        directory = cache_root / software_id / version_label
        directory.mkdir(parents=True, exist_ok=True)
        previous_metadata_path = directory / "metadata.json"
        previous_metadata = {}
        if previous_metadata_path.is_file():
            try:
                previous_metadata = json.loads(previous_metadata_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                previous_metadata = {}
        downloads = list(previous_metadata.get("downloads") or []) if not args.download else []
        errors = list(previous_metadata.get("download_errors") or []) if not args.download else []
        if not args.download and not downloads:
            downloads = _recover_download_records(directory, list(record.get("official_sources") or []))
        for number, source in enumerate(record.get("official_sources", []), start=1):
            if not args.download:
                continue
            suffix = ".pdf" if source.get("kind") == "pdf" else ".html"
            destination = directory / f"official_{number}{suffix}"
            try:
                downloads.append({"url": source["url"], **_download(source["url"], destination, max_bytes=args.max_mib * 1024 * 1024)})
            except Exception as exc:  # cache failures must not corrupt the catalog
                destination.unlink(missing_ok=True)
                errors.append({"url": source["url"], "error": str(exc)})

        metadata = {
            "software_id": software_id,
            "display_name": record.get("display_name", software_id),
            "generated_at": generated_at,
            "detected_versions": versions,
            "inventory_status": requested_item.get("status") if requested_item else None,
            "public_adapter": requested_item.get("public_adapter") if requested_item else None,
            "current_validated_actions": _current_actions(aliases),
            "candidate_actions": list(record.get("candidate_actions") or []),
            "official_sources": list(record.get("official_sources") or []),
            "local_documents": _local_document_records(
                list(record.get("local_documents") or [])
            ),
            "downloads": downloads,
            "download_errors": errors,
            "notes": requested_item.get("notes") if requested_item else None,
        }
        (directory / "metadata.json").write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        source_lines = "\n".join(f"- [{item['title']}]({item['url']}) ({item.get('version_scope', 'unspecified')})" for item in metadata["official_sources"]) or "- Not registered"
        local_lines = "\n".join(
            f"- `{item['path']}` — {'available' if item.get('available') else 'missing'}"
            + (f", SHA-256 `{item['sha256']}`" if item.get("sha256") else "")
            for item in metadata["local_documents"]
        ) or "- None"
        current_lines = "\n".join(f"- `{item}`" for item in metadata["current_validated_actions"]) or "- None"
        candidate_lines = "\n".join(f"- `{item}`" for item in metadata["candidate_actions"]) or "- None"
        readme = f"""# {metadata['display_name']} Local Capability Documentation\n\n- Detected versions: {', '.join(versions) if versions else 'unknown'}\n- Inventory status: {metadata['inventory_status'] or 'not listed'}\n- Generated at: {generated_at}\n\n## Official Sources\n\n{source_lines}\n\n## Package and Local Manuals\n\n{local_lines}\n\n## Current Validated MCP Actions\n\n{current_lines}\n\n## Candidate Actions\n\n{candidate_lines}\n\n## Management Note\n\nDownloaded files in this directory are local caches of official documentation. Their presence does not mean the corresponding scientific capability has been adapted or validated. Public status is defined by the repository catalog and tests.\n"""
        (directory / "README.md").write_text(readme, encoding="utf-8")
        index.append(metadata)

    (cache_root / "index.json").write_text(json.dumps({"generated_at": generated_at, "software": index}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"cache_root": str(cache_root), "software_count": len(index), "download": args.download}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
