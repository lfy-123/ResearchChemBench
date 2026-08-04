from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from src.core.io import write_json, write_jsonl
from src.core.logging import log_progress, pipeline_logger, value_counts
from src.stages.stage05_asset_collection.clues import (
    deduplicate_clues,
    normalize_doi,
    seed_document_clues,
)
from src.stages.stage05_asset_collection.discovery import (
    metadata_clues,
    publisher_supplement_clues,
    resolve_clue_targets,
)
from src.stages.stage05_asset_collection.download import download_url, register_local_file
from src.stages.stage05_asset_collection.parsers import parse_asset


def run_asset_collection(
    documents: list[dict[str, Any]],
    output_dir: str | Path,
    config: dict[str, Any],
    mineru_config: dict[str, Any],
) -> dict[str, Any]:
    root = Path(output_dir).expanduser().resolve()
    object_root = root / "objects" / "sha256"
    parsed_root = root / "parsed"
    rounds_root = root / "rounds"
    for path in (object_root, parsed_root, rounds_root, root / "papers"):
        path.mkdir(parents=True, exist_ok=True)

    eligible = [
        item
        for item in documents
        if not item.get("duplicate_of") and (item.get("resource_limits") or {}).get("passed")
    ]
    limit = config.get("paper_limit")
    if limit is not None:
        eligible = eligible[: int(limit)]
    all_assets: list[dict[str, Any]] = []
    all_clues: list[dict[str, Any]] = []
    all_events: list[dict[str, Any]] = []
    paper_indexes: list[dict[str, Any]] = []
    for index, document in enumerate(eligible, start=1):
        result = _collect_paper(
            document,
            root=root,
            object_root=object_root,
            parsed_root=parsed_root,
            rounds_root=rounds_root,
            config=config,
            mineru_config=mineru_config,
        )
        all_assets.extend(result["assets"])
        all_clues.extend(result["clues"])
        all_events.extend(result["events"])
        paper_indexes.append(result["index"])
        write_json(root / "papers" / document["paper_id"] / "asset_index.json", result["index"])
        log_progress(
            "stage_05_asset_collection",
            index,
            len(eligible),
            str(document.get("title") or document["paper_id"]),
            status=result["index"]["status"],
        )

    write_jsonl(root / "asset_manifest.jsonl", all_assets)
    write_jsonl(root / "asset_events.jsonl", all_events)
    write_jsonl(root / "clue_manifest.jsonl", all_clues)
    write_jsonl(
        root / "unresolved_clues.jsonl",
        [item for item in all_clues if item.get("status") not in {"resolved", "duplicate"}],
    )
    write_jsonl(root / "paper_asset_index.jsonl", paper_indexes)
    summary = {
        "download_scope": config.get("download_scope", "all"),
        "papers": len(paper_indexes),
        "paper_statuses": value_counts(item.get("status") for item in paper_indexes),
        "assets": len(all_assets),
        "asset_roles": value_counts(item.get("role") for item in all_assets),
        "access_statuses": value_counts(item.get("access_status") for item in all_assets),
        "parse_statuses": value_counts(item.get("parse_status") for item in all_assets),
        "clues": len(all_clues),
        "clue_statuses": value_counts(item.get("status") for item in all_clues),
    }
    write_json(root / "stage_summary.json", summary)
    return {"assets": all_assets, "clues": all_clues, "papers": paper_indexes, "summary": summary}


def _collect_paper(
    document: dict[str, Any],
    *,
    root: Path,
    object_root: Path,
    parsed_root: Path,
    rounds_root: Path,
    config: dict[str, Any],
    mineru_config: dict[str, Any],
) -> dict[str, Any]:
    paper_id = str(document["paper_id"])
    max_rounds = int(config.get("max_rounds", 3))
    max_archive_depth = int(config.get("max_archive_depth", 3))
    max_assets = int(config.get("max_assets_per_paper", 500))
    max_clues = int(config.get("max_clues_per_paper", 500))
    max_archive_children = int(config.get("max_archive_children_per_archive", 300))
    download_scope = str(config.get("download_scope", "all"))
    assets: list[dict[str, Any]] = []
    clues: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    seen_hashes: dict[str, str] = {}
    seen_clues: set[tuple[str, str]] = set()
    archive_queue: list[dict[str, Any]] = []
    paper_doi = normalize_doi(document.get("doi"))

    def event(kind: str, **payload: Any) -> None:
        events.append({"event": kind, "paper_id": paper_id, **payload})
        pipeline_logger().info(
            "ASSET EVENT | paper_id=%s | event=%s | details=%s", paper_id, kind, payload
        )

    def add_clues(values: list[dict[str, Any]]) -> int:
        added = 0
        for clue in deduplicate_clues(values):
            if download_scope == "supplementary_only" and not _is_supplementary_clue(clue):
                event("CLUE_SKIPPED", clue_id=clue["clue_id"], reason="download_scope")
                continue
            canonical = str(clue.get("canonical_value") or "")
            clue_doi = normalize_doi(canonical)
            if clue_doi == paper_doi and clue.get("kind") != "paper_doi":
                event("CLUE_SKIPPED", clue_id=clue["clue_id"], reason="self_doi")
                continue
            key = (
                ("related_doi", clue_doi)
                if clue_doi and clue_doi != paper_doi
                else (str(clue.get("kind")), canonical)
            )
            if key in seen_clues or len(clues) >= max_clues:
                continue
            seen_clues.add(key)
            clues.append(clue)
            added += 1
            event("CLUE_DISCOVERED", clue_id=clue["clue_id"], round=clue["discovery_round"])
        return added

    def add_asset(asset: dict[str, Any], current_round: int) -> bool:
        digest = str(asset.get("sha256") or "")
        if digest in seen_hashes:
            asset["access_status"] = "duplicate"
            asset["duplicate_of"] = seen_hashes[digest]
            event("ASSET_DUPLICATE", asset_id=asset["asset_id"], duplicate_of=seen_hashes[digest])
            return False
        if len(assets) >= max_assets:
            event("ASSET_SKIPPED", asset_id=asset["asset_id"], reason="asset_budget_exhausted")
            return False
        seen_hashes[digest] = str(asset["asset_id"])
        event("PARSE_START", asset_id=asset["asset_id"], round=current_round)
        parsed, children, discovered = parse_asset(
            asset,
            parsed_root=parsed_root,
            mineru_config=mineru_config,
            next_round=current_round + 1,
            max_text_chars=int(config.get("max_text_chars", 2_000_000)),
            max_archive_files=int(config.get("max_archive_files", 5000)),
            max_archive_bytes=int(config.get("max_archive_expanded_bytes", 50 * 1024**3)),
        )
        assets.append(parsed)
        event("PARSE_DONE", asset_id=parsed["asset_id"], status=parsed["parse_status"])
        add_clues(_filter_discovered_clues(parsed, discovered))
        if children and int(parsed.get("archive_depth") or 0) < max_archive_depth:
            archive_queue.append(
                {
                    "parent": parsed,
                    "children": _prioritize_archive_children(
                        children, str(parsed.get("role") or "other")
                    )[:max_archive_children],
                    "cursor": 0,
                    "round": current_round,
                }
            )
        return True

    def drain_archive_queue() -> int:
        added = 0
        jobs = list(archive_queue)
        archive_queue.clear()
        while jobs and len(assets) < max_assets:
            remaining_budget = max_assets - len(assets)
            fair_share = max(1, (remaining_budget + len(jobs) - 1) // len(jobs))
            next_jobs: list[dict[str, Any]] = []
            for job in jobs:
                parent = job["parent"]
                children = job["children"]
                start = int(job["cursor"])
                stop = min(len(children), start + fair_share)
                for child in children[start:stop]:
                    if len(assets) >= max_assets:
                        break
                    try:
                        child_asset = register_local_file(
                            child,
                            paper_id=paper_id,
                            object_root=object_root,
                            role=_archive_child_role(child, str(parent.get("role") or "other")),
                            relation_type="archive_child",
                            discovered_by="archive_scan",
                            discovery_round=int(job["round"]),
                            parent_asset_id=str(parent["asset_id"]),
                            archive_depth=int(parent.get("archive_depth") or 0) + 1,
                        )
                        if add_asset(child_asset, int(job["round"])):
                            added += 1
                    except Exception as exc:
                        event(
                            "ARCHIVE_CHILD_FAILED",
                            path=str(child),
                            error=f"{type(exc).__name__}: {exc}",
                        )
                job["cursor"] = stop
                if stop < len(children):
                    next_jobs.append(job)
            if archive_queue:
                next_jobs.extend(archive_queue)
                archive_queue.clear()
            jobs = next_jobs
        for job in jobs:
            remaining = len(job["children"]) - int(job["cursor"])
            if remaining:
                event(
                    "ARCHIVE_CHILD_BUDGET_EXHAUSTED",
                    asset_id=job["parent"]["asset_id"],
                    remaining=remaining,
                )
        return added

    event("PAPER_START", title=document.get("title"))
    local_paths = _local_assets(
        document,
        bool(config.get("include_local_siblings", True)),
        download_scope=download_scope,
    )
    for local_index, (path, role) in enumerate(local_paths):
        asset = register_local_file(
            path,
            paper_id=paper_id,
            object_root=object_root,
            role=role,
            relation_type="pipeline_input" if local_index == 0 else "local_sibling",
            discovered_by="stage04" if local_index == 0 else "local_scan",
            discovery_round=0,
            fallback_text_path=(
                str(document.get("text_path") or document.get("grobid_text_path") or "")
                if local_index == 0
                else None
            ),
        )
        add_asset(asset, 0)
    drain_archive_queue()
    add_clues(seed_document_clues(document, max_clues=max_clues))
    network_enabled = bool(config.get("enable_network", True))
    if network_enabled and config.get("query_metadata", True):
        metadata_values, audits = metadata_clues(
            document,
            timeout_seconds=float(config.get("metadata_timeout_seconds", 30)),
            request_policy=config,
            download_scope=download_scope,
        )
        add_clues(metadata_values)
        for audit in audits:
            event("METADATA_QUERY", **audit)
    if network_enabled and config.get("discover_publisher_supplements", True):
        publisher_values, audit = publisher_supplement_clues(
            document,
            timeout_seconds=float(config.get("metadata_timeout_seconds", 30)),
            request_policy=config,
        )
        add_clues(publisher_values)
        event("METADATA_QUERY", **audit)

    for round_number in range(1, max_rounds + 1):
        if len(assets) >= max_assets:
            for clue in clues:
                if clue.get("status") == "pending":
                    clue["status"] = "skipped_by_budget"
                    clue["error"] = "asset budget exhausted"
            event("ROUND_EARLY_STOP", round=round_number, reason="asset_budget_exhausted")
            break
        frontier = [
            item
            for item in clues
            if item.get("status") == "pending"
            and int(item.get("discovery_round") or 1) <= round_number
        ]
        if not frontier:
            event("ROUND_EARLY_STOP", round=round_number, reason="empty_frontier")
            break
        round_dir = rounds_root / f"round_{round_number:02d}"
        round_dir.mkdir(parents=True, exist_ok=True)
        event("ROUND_START", round=round_number, frontier=len(frontier))
        if not config.get("enable_network", True):
            for clue in frontier:
                clue["status"] = "skipped_by_policy"
                clue["error"] = "network acquisition disabled"
            event("ROUND_EARLY_STOP", round=round_number, reason="network_disabled")
            break
        new_assets = 0
        workers = max(1, int(config.get("network_workers", 4)))
        direct_budget = max(1, max_assets - len(assets))
        per_clue_target_limit = max(1, direct_budget // max(1, len(frontier)))
        acquire_config = {
            **config,
            "max_targets_per_clue": min(
                int(config.get("max_targets_per_clue", 200)), per_clue_target_limit
            ),
        }
        acquired_by_clue: list[tuple[dict[str, Any], list[dict[str, Any]]]] = []
        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = {
                executor.submit(
                    _acquire_clue, clue, object_root, acquire_config, round_number
                ): clue
                for clue in frontier
            }
            for future in as_completed(futures):
                clue = futures[future]
                try:
                    event("DOWNLOAD_START", clue_id=clue["clue_id"], round=round_number)
                    acquired = future.result()
                    initial_status = (
                        "partial"
                        if acquired and clue.get("target_errors")
                        else "resolved"
                        if acquired
                        else "unresolved"
                    )
                    clue["status"] = initial_status
                    acquired_by_clue.append((clue, acquired))
                except Exception as exc:
                    clue["status"] = "failed"
                    clue["error"] = f"{type(exc).__name__}: {exc}"
                    event("DOWNLOAD_FAILED", clue_id=clue["clue_id"], error=clue["error"])
        accepted_by_clue: dict[str, int] = {}
        flattened = [(clue, asset) for clue, acquired in acquired_by_clue for asset in acquired]
        for clue, asset in sorted(flattened, key=lambda item: _acquisition_priority(item[1])):
            if add_asset(asset, round_number):
                new_assets += 1
                clue_id = str(clue["clue_id"])
                accepted_by_clue[clue_id] = accepted_by_clue.get(clue_id, 0) + 1
        new_assets += drain_archive_queue()
        for clue, acquired in acquired_by_clue:
            accepted = accepted_by_clue.get(str(clue["clue_id"]), 0)
            if acquired and not accepted:
                clue["status"] = "skipped_by_budget"
                clue["error"] = "asset budget exhausted before registration"
            elif accepted < len(acquired):
                clue["status"] = "partial"
                clue["error"] = "some acquisition targets exceeded the asset budget"
            event(
                "DOWNLOAD_DONE",
                clue_id=clue["clue_id"],
                assets=accepted,
                status=clue["status"],
            )
        write_jsonl(round_dir / f"{paper_id}_clues.jsonl", frontier)
        event("ROUND_SUMMARY", round=round_number, frontier=len(frontier), new_assets=new_assets)
        pending_next = any(
            item.get("status") == "pending"
            and int(item.get("discovery_round") or max_rounds + 1) <= max_rounds
            for item in clues
        )
        if not new_assets and not pending_next:
            event("ROUND_EARLY_STOP", round=round_number, reason="no_new_assets_or_clues")
            break

    for clue in clues:
        if clue.get("status") == "pending":
            clue["status"] = "round_limit"
            clue["error"] = "maximum discovery rounds reached"
    external = [item for item in assets if item.get("relation_type") != "pipeline_input"]
    failures = [item for item in assets if item.get("parse_status") == "failed"]
    unresolved = [item for item in clues if item.get("status") not in {"resolved", "duplicate"}]
    status = "complete"
    if not assets:
        status = "failed"
    elif failures or unresolved:
        status = "partial"
    elif not external:
        status = "no_external_assets"
    index = {
        "paper_id": paper_id,
        "title": document.get("title"),
        "doi": document.get("doi"),
        "status": status,
        "asset_ids": [item["asset_id"] for item in assets],
        "assets": len(assets),
        "external_assets": len(external),
        "clues": len(clues),
        "unresolved_clues": len(unresolved),
        "parse_failures": len(failures),
    }
    event("PAPER_COMPLETE", status=status, assets=len(assets), clues=len(clues))
    return {"assets": assets, "clues": clues, "events": events, "index": index}


def _acquire_clue(
    clue: dict[str, Any], object_root: Path, config: dict[str, Any], round_number: int
) -> list[dict[str, Any]]:
    if clue.get("kind") == "paper_doi":
        return []
    targets, _ = resolve_clue_targets(
        clue,
        timeout_seconds=float(config.get("metadata_timeout_seconds", 30)),
        request_policy=config,
    )
    supplementary_only = config.get("download_scope") == "supplementary_only"
    if supplementary_only and not _is_supplementary_clue(clue):
        return []
    output: list[dict[str, Any]] = []
    target_errors: list[dict[str, str]] = []
    for target in targets[: int(config.get("max_targets_per_clue", 200))]:
        if supplementary_only:
            target = {**target, "role": "supplement"}
        try:
            asset = download_url(
                target["url"],
                paper_id=str(clue["paper_id"]),
                object_root=object_root,
                role=str(target.get("role") or "other"),
                relation_type=str(target.get("relation_type") or "explicit_url"),
                discovered_by=str(target.get("discovered_by") or "document_link"),
                discovery_round=round_number,
                timeout_seconds=float(config.get("download_timeout_seconds", 120)),
                max_bytes=int(config.get("max_single_file_bytes", 10 * 1024**3)),
                headers=target.get("headers"),
                request_policy=config,
            )
            for key in ("identifier", "version", "file_name"):
                if target.get(key):
                    asset[key] = target[key]
            output.append(asset)
        except Exception as exc:
            target_errors.append(
                {
                    "url": str(target.get("url") or "").split("?", 1)[0],
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    if target_errors:
        clue["target_errors"] = target_errors
    if target_errors and not output:
        raise RuntimeError(
            f"all {len(target_errors)} acquisition target(s) failed: {target_errors[0]['error']}"
        )
    return output


def _local_assets(
    document: dict[str, Any], include_siblings: bool, *, download_scope: str = "all"
) -> list[tuple[Path, str]]:
    source = Path(str(document["source_path"])).expanduser().resolve()
    output = [(source, "main_paper")]
    if not include_siblings:
        return output
    study_root = (
        source.parent.parent
        if source.parent.name.casefold() in {"paper", "papers"}
        else source.parent
    )
    allowed = {
        ".pdf",
        ".zip",
        ".tar",
        ".gz",
        ".csv",
        ".tsv",
        ".xlsx",
        ".json",
        ".yaml",
        ".yml",
        ".txt",
        ".md",
        ".cif",
        ".xyz",
        ".pdb",
        ".mol",
        ".sdf",
    }
    for item in sorted(study_root.rglob("*")):
        if item == source or not item.is_file() or item.suffix.casefold() not in allowed:
            continue
        role = _local_role(item)
        if download_scope == "supplementary_only" and role != "supplement":
            continue
        output.append((item, role))
        if len(output) >= 100:
            break
    return output


def _local_role(path: Path) -> str:
    text = path.name.casefold()
    if path.stem.casefold() in {"si", "esi"} or any(
        term in text for term in ("supp", "supporting", "si_", "si-")
    ):
        return "supplement"
    if path.suffix.casefold() == ".pdf":
        return "other"
    if any(term in text for term in ("code", "script", "github")):
        return "code"
    if any(term in text for term in ("input", "structure", "cif", "xyz", "pdb")):
        return "input"
    return "source_data"


def _archive_child_role(path: Path, parent_role: str) -> str:
    return parent_role if parent_role in {"code", "supplement"} else _local_role(path)


def _is_supplementary_clue(clue: dict[str, Any]) -> bool:
    if clue.get("kind") == "paper_doi":
        return True
    if str(clue.get("relation_type") or "").casefold() in {
        "publisher_attachment",
        "is-supplemented-by",
        "issupplementedby",
        "is-supplement-to",
        "issupplementto",
    }:
        return True
    evidence = str(clue.get("evidence") or "").casefold()
    evidence_matches = any(
        term in evidence
        for term in (
            "supplementary",
            "supplemental",
            "supporting information",
            "supporting material",
            "is-supplemented-by",
            "issupplementedby",
            "issupplementto",
            "is supplement to",
        )
    )
    if not evidence_matches:
        return False
    if clue.get("kind") in {"url", "repository_url"}:
        value = str(clue.get("canonical_value") or clue.get("value") or "").casefold()
        return any(
            marker in value
            for marker in (
                "supp",
                "supporting",
                "moesm",
                "_esm",
                "-esm",
                "_si_",
                "-si-",
                "/si/",
            )
        )
    return True


def _acquisition_priority(asset: dict[str, Any]) -> tuple[int, str, str]:
    role_priority = {
        "source_data": 0,
        "input": 1,
        "supplement": 2,
        "code": 3,
        "other": 4,
    }
    return (
        role_priority.get(str(asset.get("role") or "other"), 5),
        str(asset.get("file_name") or ""),
        str(asset.get("source_url") or ""),
    )


def _filter_discovered_clues(
    asset: dict[str, Any], clues: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    if asset.get("role") != "code":
        return clues
    return [
        clue
        for clue in clues
        if "github.com" not in str(clue.get("canonical_value") or "").casefold()
    ]


def _prioritize_archive_children(children: list[Path], parent_role: str = "other") -> list[Path]:
    metadata_terms = ("readme", "citation", "license", "manifest")
    input_terms = ("config", "input", "script")

    def priority(path: Path) -> int:
        name = path.name.casefold()
        parts = {part.casefold() for part in path.parts}
        suffix = path.suffix.casefold()
        if any(term in name for term in metadata_terms):
            return 0
        if parent_role == "code":
            if suffix in {".py", ".sh", ".toml", ".yaml", ".yml", ".json"}:
                return 0
            if suffix in {".md", ".rst", ".txt"}:
                return 1
            return 3
        if "dft" in parts and name == "aiida.in":
            return 0
        if suffix in {".cif", ".xyz", ".pdb", ".mol", ".sdf", ".upf"}:
            return 0
        if any(term in name for term in input_terms):
            return 1
        if name == "aiida.in" or suffix in {".in", ".inp", ".com", ".gjf"}:
            return 1
        if name.startswith(("o-", "r-", "l-")) or suffix in {".out", ".log"}:
            return 3
        return 2

    return sorted(
        children,
        key=lambda path: (
            priority(path),
            len(path.parts),
            str(path),
        ),
    )
