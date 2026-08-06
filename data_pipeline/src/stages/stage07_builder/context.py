from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

from src.agents.workspace import make_input_read_only
from src.core.io import write_json, write_jsonl

PATH_KEYS = {
    "source_path",
    "text_path",
    "grobid_text_path",
    "grobid_tei_path",
    "softcite_raw_path",
    "grobid_quantities_raw_path",
    "model_input_path",
    "model_response_path",
}


def materialize_agent_context(
    input_dir: Path,
    *,
    document: dict[str, Any],
    assets: list[dict[str, Any]],
    toolbox: dict[str, Any],
    extra_files: list[tuple[str | Path, str]] | None = None,
    max_readable_bytes: int = 50 * 1024**2,
) -> list[dict[str, Any]]:
    sanitized_document = _without_external_paths(document)
    write_json(input_dir / "document.json", sanitized_document)
    write_json(input_dir / "document_summary.json", _document_summary(sanitized_document))
    write_json(input_dir / "toolbox.json", toolbox)
    copied = 0
    agent_assets: list[dict[str, Any]] = []
    for asset in assets:
        item = _without_external_paths(asset)
        item["logical_path"] = _asset_logical_path(asset)
        readable: list[str] = []
        for raw in _preferred_readable_paths(asset.get("readable_paths", [])):
            source = Path(str(raw))
            if not source.is_file() or copied + source.stat().st_size > max_readable_bytes:
                continue
            target = input_dir / "assets" / str(asset["asset_id"]) / source.name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            copied += source.stat().st_size
            readable.append(str(target.relative_to(input_dir)))
        item["agent_readable_paths"] = readable
        agent_assets.append(item)
    write_jsonl(input_dir / "asset_manifest.jsonl", agent_assets)
    (input_dir / "asset_overview.md").write_text(_asset_overview(agent_assets), encoding="utf-8")
    for source, relative in extra_files or []:
        source_path = Path(source)
        if not source_path.exists():
            continue
        target = input_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source_path.is_dir():
            shutil.copytree(source_path, target, dirs_exist_ok=True)
        else:
            shutil.copy2(source_path, target)
    make_input_read_only(input_dir)
    return agent_assets


def _without_external_paths(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_external_paths(item)
            for key, item in value.items()
            if key not in PATH_KEYS and not key.endswith("_path")
        }
    if isinstance(value, list):
        return [_without_external_paths(item) for item in value]
    return value


def _preferred_readable_paths(values: list[Any]) -> list[str]:
    paths = [str(value) for value in values]
    markdown = next((value for value in paths if Path(value).suffix.casefold() == ".md"), None)
    return [markdown or paths[0]] if paths else []


def _asset_logical_path(asset: dict[str, Any]) -> str:
    source = str(asset.get("source_local_path") or "")
    marker = "/extracted/"
    if marker in source:
        return source.split(marker, 1)[1]
    return str(asset.get("file_name") or "")


def _document_summary(document: dict[str, Any]) -> dict[str, Any]:
    return {
        "paper_id": document.get("paper_id"),
        "title": document.get("title"),
        "doi": document.get("doi"),
        "abstract": document.get("abstract"),
        "section_headings": document.get("section_headings", []),
        "computation_relevance": document.get("computation_relevance", {}),
        "preliminary_coverage": document.get("preliminary_coverage", {}),
        "supplementary_acquisition": document.get("supplementary_acquisition", {}),
        "supplementary_extraction": document.get("supplementary_extraction", {}),
    }


def _asset_overview(assets: list[dict[str, Any]]) -> str:
    lines = [
        "# Asset overview",
        "",
        "Read only the assets needed for the proposed task. Answer-bearing assets may support the hidden reference but must not be listed as public inputs.",
        "",
        "| asset_id | role | logical path | parser | bytes | readable | parent |",
        "|---|---|---|---|---:|---|---|",
    ]
    for asset in assets:
        readable = ", ".join(f"input/{path}" for path in asset.get("agent_readable_paths", []))
        lines.append(
            "| {asset_id} | {role} | {logical_path} | {parser} | {size} | {readable} | {parent} |".format(
                asset_id=asset.get("asset_id", ""),
                role=asset.get("role", ""),
                logical_path=str(asset.get("logical_path", "")).replace("|", "\\|"),
                parser=asset.get("parser", ""),
                size=asset.get("size_bytes", ""),
                readable=readable,
                parent=asset.get("parent_asset_id") or "",
            )
        )
    return "\n".join(lines) + "\n"
