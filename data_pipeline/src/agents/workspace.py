from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
from pathlib import Path
from typing import Any, Iterable

from src.contracts import canonical_hash, now_utc, write_json

IGNORED_MANIFEST_NAMES = {
    "output_manifest.json",
    "public_manifest.json",
    "task_pair_manifest.json",
    "audit_manifest.json",
    "published_manifest.json",
    "phase_state.json",
    "_agent_stdout.jsonl",
    "_agent_stderr.log",
    "_final_message.txt",
}


def prepare_clean_directory(path: Path) -> Path:
    """Create an empty, narrowly resolved work directory."""

    target = path.expanduser().resolve()
    if target.exists():
        make_writable(target)
        shutil.rmtree(target)
    target.mkdir(parents=True, exist_ok=False)
    return target


def copytree_exact(source: Path, destination: Path) -> Path:
    source = source.expanduser().resolve()
    destination = destination.expanduser().resolve()
    if destination.exists():
        # Recovery targets can contain immutable input snapshots. Restore only
        # the copied destination tree before replacing it; the canonical source
        # remains untouched and read-only.
        make_writable(destination)
        shutil.rmtree(destination)
    shutil.copytree(source, destination, symlinks=False)
    return destination


def agent_recovery_context(result: Any) -> str | None:
    """Build a bounded, auditable handoff from a failed isolated Agent run."""

    if result is None:
        return None
    sections = [
        "# Previous Agent Attempt",
        (
            "The previous isolated attempt failed to return a valid receipt. Use this trace "
            "only as a search summary; verify every scientific fact against the unchanged "
            "read-only inputs."
        ),
        f"Failure class: {getattr(result, 'failure_class', None) or 'unknown'}",
    ]
    error = getattr(result, "error", None)
    if isinstance(error, dict) and error:
        error_type = str(error.get("error_type") or "AgentError")[:160]
        error_message = str(error.get("message") or "").strip()[:4000]
        sections.extend(
            [
                "## Validation failure to repair",
                f"{error_type}: {error_message}" if error_message else error_type,
            ]
        )
    final_value = getattr(result, "final_message_path", None)
    final_path = Path(final_value) if final_value else None
    if final_path and final_path.is_file():
        final_message = final_path.read_text(encoding="utf-8", errors="replace").strip()
        if final_message:
            sections.extend(["## Previous final message", final_message[-2000:]])
    stdout_value = getattr(result, "stdout_path", None)
    stdout_path = Path(stdout_value) if stdout_value else None
    if stdout_path and stdout_path.is_file():
        action_summaries: list[str] = []
        for line in stdout_path.read_text(
            encoding="utf-8", errors="replace"
        ).splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") != "item.completed":
                continue
            item = event.get("item") or {}
            item_type = str(item.get("type") or "unknown")
            if item_type == "command_execution":
                command = " ".join(str(item.get("command") or "").split())[:320]
                action_summaries.append(
                    f"- command exit={item.get('exit_code')} status={item.get('status')}: "
                    f"{command}"
                )
            elif item_type == "agent_message":
                message = " ".join(str(item.get("text") or "").split())[:500]
                if message:
                    action_summaries.append(f"- agent message: {message}")
            elif item_type in {"error", "reasoning"}:
                message = " ".join(
                    str(item.get("message") or item.get("text") or "").split()
                )[:500]
                if message:
                    action_summaries.append(f"- {item_type}: {message}")
        if action_summaries:
            sections.extend(
                ["## Recent completed actions", "\n".join(action_summaries[-12:])]
            )
    workspace_value = getattr(result, "workspace", None)
    workspace = Path(workspace_value) if workspace_value else None
    if workspace and workspace.is_dir():
        artifacts: list[str] = []
        for directory_name in ("outputs", "task"):
            directory = workspace / directory_name
            if not directory.is_dir():
                continue
            for path in sorted(directory.rglob("*")):
                if path.is_file() and path.name not in IGNORED_MANIFEST_NAMES:
                    artifacts.append(
                        f"- {path.relative_to(workspace).as_posix()} "
                        f"({path.stat().st_size} bytes)"
                    )
        if artifacts:
            sections.extend(["## Preserved partial artifacts", "\n".join(artifacts[:80])])
    return "\n\n".join(sections)[:8000] + "\n"


def copy_recovery_artifacts(
    previous: Path | None,
    destination: Path,
    *,
    directory_names: Iterable[str] = ("outputs", "task"),
    include_evidence_trace: bool = False,
) -> None:
    """Copy partial artifacts between isolated attempts without sharing a workspace."""

    if previous is None:
        return
    for name in directory_names:
        source = previous / name
        target = destination / name
        # Phase setup may create an empty task/ directory (or a clean reproduction
        # baseline) before recovery is applied. A non-empty previous artifact must
        # supersede that initialization so isolated retries can continue file-first
        # work instead of starting over.
        if source.is_dir() and any(path.is_file() for path in source.rglob("*")):
            copytree_exact(source, target)
    if include_evidence_trace:
        _write_recovery_evidence_trace(previous, destination / "RECOVERY_EVIDENCE.md")


def _write_recovery_evidence_trace(
    previous: Path, destination: Path, *, max_characters: int = 240_000
) -> None:
    """Render prior read-only command results as a bounded private Agent handoff."""

    stdout = previous / "_agent_stdout.jsonl"
    if not stdout.is_file():
        return
    inherited = previous / "RECOVERY_EVIDENCE.md"
    if inherited.is_file():
        sections = [
            inherited.read_text(encoding="utf-8", errors="replace")[:max_characters],
            "\n# Additional Recovery Attempt Evidence\n",
        ]
    else:
        sections = [
            "# Private Recovery Evidence",
            "",
            (
                "This is a deterministic handoff of completed commands and their outputs from "
                "the previous isolated Agent workspace. It is not a public task artifact. Use "
                "the cited canonical evidence IDs; do not repeat these searches."
            ),
        ]
    used = sum(len(section) + 1 for section in sections)
    for line in stdout.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") != "item.completed":
            continue
        item = event.get("item") or {}
        if item.get("type") != "command_execution":
            continue
        command = str(item.get("command") or "").strip()[:2_000]
        output = str(item.get("aggregated_output") or "").strip()[:24_000]
        section = (
            f"\n## Completed command ({item.get('status')}, exit={item.get('exit_code')})\n\n"
            f"```text\n{command}\n```\n\n"
            f"```text\n{output}\n```\n"
        )
        remaining = max_characters - used
        if remaining <= 0:
            break
        sections.append(section[:remaining])
        used += min(len(section), remaining)
    destination.write_text("\n".join(sections).rstrip() + "\n", encoding="utf-8")


def recovery_instructions(phase: str, *, max_tool_calls: int | None = None) -> str:
    budget = (
        f"The recovery budget is exactly {max_tool_calls} tool calls; this replaces any "
        "larger budget stated in the base phase instructions. After those calls, the next "
        "available workspace call is for writing the fixed artifact only."
        if max_tool_calls is not None
        else "The recovery attempt has a reduced tool budget."
    )
    return f"""

RECOVERY ATTEMPT FOR `{phase}`:
{budget}
Read `RECOVERY_CONTEXT.md` first with `sed -n '1,240p' RECOVERY_CONTEXT.md` (it is a file in the workspace root;
do not infer that it is absent from a partial directory listing). The unchanged canonical inputs remain authoritative.
Use the ordinary shell even if an optional Codex code-mode host reports that it is unavailable; that warning does
not imply a filesystem failure. Once a shell command exits zero and shows workspace content, do not repeat `pwd`,
`ls`, or equivalent access probes. Continue directly with the named repair and grouped verification.
If the context file is unavailable, continue from any existing `outputs/` artifacts and the validation failure; do
not convert that execution/transport problem into a scientific rejection. Do not repeat broad searches
already recorded there. If `RECOVERY_EVIDENCE.md` exists, do not page through the full file: use at most one
targeted grouped search for the exact missing paths, then start writing. The recovery budget is for delivering
the artifact, not for rereading the entire prior trace. Use one `/usr/bin/python3` batch edit for repeated files,
then one grouped diff/hash verification before submitting the receipt.
When `RECOVERY_CONTEXT.md` contains a `Validation failure to repair` section, its exact findings are the primary
work order. Inspect the existing artifact once and patch those findings before any new evidence search; do not spend
the recovery budget revalidating fields that were not named by the validator.
Ensure `outputs/` exists, then inspect any partial `outputs/` or `task/` files, resolve only the concrete missing facts,
then write or repair the required artifact and return the small receipt. This attempt is for completion, not a
fresh review. If the evidence remains insufficient, return the phase's explicit
terminal negative decision with precise reasons instead of requesting more searches.
"""


def make_read_only(path: Path) -> None:
    """Remove write bits from a copied input tree.

    This is defense in depth. The original source is never mounted in an Agent
    workspace, so changing permissions on a copy cannot mutate pipeline inputs.
    """

    target = path.resolve()
    if not target.exists():
        return
    for child in sorted(target.rglob("*"), reverse=True):
        mode = child.stat().st_mode
        if child.is_dir():
            child.chmod(mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
        else:
            child.chmod(mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
    mode = target.stat().st_mode
    target.chmod(mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))


def make_writable(path: Path) -> None:
    target = path.resolve()
    if not target.exists():
        return
    target.chmod(target.stat().st_mode | stat.S_IWUSR)
    for child in target.rglob("*"):
        child.chmod(child.stat().st_mode | stat.S_IWUSR)


def directory_manifest(
    root: Path,
    *,
    ignored_names: Iterable[str] = IGNORED_MANIFEST_NAMES,
) -> dict[str, Any]:
    root = root.expanduser().resolve()
    ignored = set(ignored_names)
    files: list[dict[str, Any]] = []
    if root.exists():
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                raise ValueError(f"manifest tree contains a symbolic link: {path}")
            if not path.is_file() or path.name in ignored:
                continue
            relative = path.relative_to(root).as_posix()
            files.append(
                {
                    "path": relative,
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256_file(path),
                }
            )
    return {
        "format": "researchchembench.directory-manifest.v1",
        "created_at": now_utc(),
        "root_name": root.name,
        "files": files,
        "content_hash": canonical_hash(
            [{key: row[key] for key in ("path", "size_bytes", "sha256")} for row in files]
        ),
    }


def write_manifest(root: Path, path: Path | None = None) -> dict[str, Any]:
    manifest = directory_manifest(root)
    write_json(path or root / "output_manifest.json", manifest)
    return manifest


def verify_manifest(root: Path, manifest: dict[str, Any]) -> list[str]:
    actual = directory_manifest(root)
    findings: list[str] = []
    if actual["content_hash"] != manifest.get("content_hash"):
        findings.append("content_hash_mismatch")
    expected_files = {row["path"]: row for row in manifest.get("files") or []}
    actual_files = {row["path"]: row for row in actual["files"]}
    if set(expected_files) != set(actual_files):
        findings.append("file_set_mismatch")
    for path in sorted(set(expected_files) & set(actual_files)):
        if expected_files[path].get("sha256") != actual_files[path].get("sha256"):
            findings.append(f"file_hash_mismatch:{path}")
    return findings


def validate_relative_path(value: str) -> str:
    normalized = str(value or "").replace("\\", "/").strip()
    path = Path(normalized)
    if not normalized or path.is_absolute() or ".." in path.parts or "\x00" in normalized:
        raise ValueError(f"unsafe relative path: {value!r}")
    return normalized


def write_text_asset(root: Path, relative_path: str, content: str) -> Path:
    relative = validate_relative_path(relative_path)
    target = (root.resolve() / relative).resolve()
    target.relative_to(root.resolve())
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(str(content), encoding="utf-8")
    return target


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def input_fingerprint(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def atomic_commit_tree(source: Path, destination: Path) -> None:
    """Commit a validated tree without exposing a partially copied task."""

    source = source.resolve()
    destination = destination.resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.parent / f".{destination.name}.commit-{os.getpid()}"
    if temporary.exists():
        make_writable(temporary)
        shutil.rmtree(temporary)
    shutil.copytree(source, temporary, symlinks=False)
    if destination.exists():
        backup = destination.parent / f".{destination.name}.previous-{os.getpid()}"
        if backup.exists():
            make_writable(backup)
            shutil.rmtree(backup)
        os.replace(destination, backup)
        try:
            os.replace(temporary, destination)
        except Exception:
            os.replace(backup, destination)
            raise
        make_writable(backup)
        shutil.rmtree(backup)
    else:
        os.replace(temporary, destination)
