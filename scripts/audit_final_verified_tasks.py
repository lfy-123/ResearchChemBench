#!/usr/bin/env python3
"""Audit final verified tasks and archive evidence-backed successful calculations.

The script is intentionally conservative.  It does not run quantum chemistry
jobs and it never reconstructs a result from evaluator targets.  It reads the
existing paper/group records, keeps only successful/validated result entries,
and writes evaluator-private Markdown records plus an aggregate audit report.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MODES = ("autonomous_research", "paper_reproduction")
GROUP_ROOTS = tuple(f"group_{i}" for i in range(1, 7))
STRUCTURE_SUFFIXES = {
    ".xyz", ".mol", ".mol2", ".sdf", ".pdb", ".cif", ".gjf", ".com",
    ".poscar", ".vasp",
}
# Scheduler bookkeeping files are useful for diagnosing a run, but they are
# mutable implementation metadata rather than part of the scientific
# calculation chain.  In particular, qzcli/slurm wrappers may rewrite these
# files during polling or cleanup.  Including them in the archived output
# inventory would make an otherwise unchanged audit appear to drift on every
# rerun.
VOLATILE_EXECUTION_FILENAMES = {
    "hpc_lifecycle.json",
    "hpc_start.txt",
    "hpc_finish.txt",
    "qzcli_submit.stdout",
    "qzcli_submit.stderr",
}
BAD_MARKER = re.compile(
    r"(?:failed?|failure|retry|migration|interrupted|queued?|running|pending|blocked|unresolved)",
    re.I,
)
# A free-text result/evidence field may legitimately point to a successful
# corrected run whose filename contains ``retry``.  Treat only a standalone
# status token (rather than any occurrence in prose/path text) as an
# unsuccessful list entry.
UNSUCCESSFUL_STATUS_VALUE = re.compile(
    r"^\s*(?:failed?|failure|retry(?:ing)?|migration(?:[-_ ]interrupted)?|"
    r"interrupted|queued?|running|pending|blocked|unresolved|cancelled|canceled|"
    r"timeout|timed[ _-]?out|killed|aborted|invalid|not[ _-]?converged)\s*$",
    re.I,
)
# Match endpoint markers as words.  ``unoptimized`` is an explicit safe
# starter label and must not be treated as an optimized endpoint merely
# because it contains the substring ``optimized``.
HIGH_RISK_MARKER = re.compile(
    r"(?:\boptimized\b|\boptimised\b|\brelaxed\b|transition[ _-]?state|\bts\d*\b|product|final)",
    re.I,
)
SI_MARKER = re.compile(r"\bSI\b|supplementary|supporting information", re.I)
ABSOLUTE_REF = re.compile(r"(?<![A-Za-z0-9])/(?:inspire|home|mnt|opt|usr|root)/")
SUCCESS_WORDS = {
    "success", "successful", "complete", "completed", "validated", "pass",
    "passed", "qualified", "advanced_validated", "converged", "true",
}
PARTIAL_WORDS = {
    "partial", "bounded_failure", "conditional", "pending", "in_progress",
    "blocked", "unverifiable", "not_established", "not available",
}

# Boundary metadata that is useful when replaying a verified chain.  These
# keys are extracted from public input files only; evaluator/private files are
# never used as a fallback.  The extraction is intentionally bounded so a
# coordinate array or large atom table cannot inflate every archive record.
INPUT_BOUNDARY_KEY = re.compile(
    r"(?:^|_)(?:charge|formal_charge|multiplicity|spin|units?|coordinate_units|"
    r"atom_(?:count|map|mapping|indices|index|order)|mapping|formula|smiles|"
    r"connectivity|lattice|cell|space_group|temperature|solvent)(?:$|_)",
    re.I,
)

# These changes were made while constructing the current final snapshot.
# Author-route verification may use private author endpoints.  Public-starter
# replay is a separate, optional claim and is not a release gate under the
# owner's accepted author-route verification policy.
CURRENT_FINAL_CHANGES = {
    "paper_0de37d01e35c27df": "Public norDTCO endpoint coordinates from SI Table S3 were replaced by an independent topology-only starter; the historical group verification used the author endpoint.",
    "paper_3a22e838133b906d": "Public neutral/anion endpoint coordinates from the SI DFT section were replaced by independent topology-only starters; the historical group verification used the author endpoints.",
    "paper_0dc85595cab7bc0a": "Public precursor was replaced by a deterministic displaced starter; group verification used the original SI endpoint.",
    "paper_221aafe4bd916a11": "Public 2a geometry was replaced by a deterministic displaced starter; group verification used the original author endpoint.",
    "paper_430b9cbe83c2c203": "Public cis/trans geometries were replaced by independently embedded topology-only starters; the group archive used the original author endpoints.",
    "paper_9d091f4337662e78": "Public conformer geometries were replaced by independently generated topology-preserving starters; the group archive used the original author-optimized endpoints.",
}
# Removing an answer-bearing TS coordinate from the public input does not
# invalidate the already-frozen evaluator-private target when the reference
# endpoint and evaluator are unchanged.  The group report explicitly records
# the strict-v2 PASS and states that no new Gaussian calculation is required;
# retain that provenance without claiming agent-visible independent discovery.
CURRENT_FINAL_REPLAY_NOT_REQUIRED = {
    "paper_e2d9397dff2a3f0f": "Public TS target.xyz was removed as an answer-bearing input; the strict-v2 group PASS uses the same reference/evaluator and retains the target only under evaluator-private inputs, with the group report stating no new Gaussian calculation is required.",
}

# Keep approved boundary changes visible when generated reference markdown is
# refreshed.  These are provenance annotations, not additional evaluator
# rules or newly computed scientific results.
REFERENCE_REPAIR_NOTES = {
    "paper_0de37d01e35c27df": (
        "The SI Table S3 neutral endpoint is retained only under "
        "`evaluation/private_inputs/`. The public 26-atom XYZ is an RDKit "
        "ETKDGv3 topology-only starter (seed 1337), with formula, atom order, "
        "and sulfur indices preserved. No new quantum calculation was run; "
        "the historical author-route result supports the evaluator target but "
        "does not certify reachability from this changed public starter."
    ),
    "paper_3a22e838133b906d": (
        "The SI neutral and anion optimized endpoints are retained only under "
        "`evaluation/private_inputs/`. The public XYZ files are RDKit ETKDGv3 "
        "topology-only starters (seeds 2337/3337), with composition, charge, "
        "multiplicity and P/O/B atom mapping preserved. No new quantum "
        "calculation was run; the historical author-route result supports the "
        "evaluator target but does not certify reachability from these changed "
        "public starters."
    ),
    "paper_1b285cf9f763f2cf": (
        "The public host is a complete, "
        "unoptimized 56-atom benchmark construction with explicit composition, "
        "fixed cell and neutral-electronic-compensation boundary. The archived "
        "UC-1/UC-2/UC-3 outputs remain historical evidence; this note does not "
        "claim an exhaustive site search or expose an optimized endpoint. "
        "The private boundary_repair_evidence.json release_reconciliation "
        "contains complete per-center bonds, angles, images and atom mappings. "
        "Use that explicit extraction rather than the legacy group composition "
        "labels or nearest-target angle summaries; these are provenance "
        "records, not replacements for the evaluator."
    ),
    "paper_534ae3b6e2fb695f": (
        "Global nucleophilicity, local "
        "nitrogen descriptors, ring-plane angles and bonded linker torsions are "
        "separate observables with explicit atom mappings. Existing outputs are "
        "replayed as arithmetic evidence only; no evaluator target is supplied "
        "to the agent. The private arithmetic replay covers global N, reference "
        "HOMO, local N, ring-plane angles and linker torsions, but does not "
        "by itself certify the revised schema. The later release_reconciliation "
        "in boundary_repair_evidence.json also records plane-fit residuals, "
        "geometry artifacts, atom mappings and convergence checks. Legacy "
        "descriptor_value and dihedral_deg must not substitute for those quantities."
    ),
    "paper_b815e2622b0d6085": (
        "Fundamental, Pb-framework "
        "interband and same-k gaps are separate quantities. Existing EIGENVAL "
        "and PROCAR outputs support sampled-mesh orbital-character analysis, "
        "but do not establish optical allowedness or full-zone extrema. "
        "The historical release_reconciliation contains character-first "
        "candidate selection and all lower edges, but its original second "
        "mesh lacked projections. The 2026-09-20 private "
        "verification_supplement.json records later independent 3x3x1 HSE06 "
        "projections, same-parent/PAW hashes, four distinct gap comparisons "
        "and sampled-domain identity review for all three crystals. A band "
        "ordinal alone is never the evidence. This closes the original gap "
        "without establishing optical allowedness, full-zone extrema or a "
        "stable Cl/Br fine ordering; release remains a separate decision."
    ),
    "paper_430b9cbe83c2c203": (
        "The author-endpoint XYZ "
        "files were replaced by independently embedded topology-only starters. "
        "The successful calculation archive still documents the historical "
        "author route; no calculation from those new starters was performed, "
        "and the original endpoints remain evaluator-private."
    ),
    "paper_9d091f4337662e78": (
        "The author-optimized "
        "conformer coordinates were replaced by independently generated "
        "topology-preserving starters. The successful calculation archive still "
        "documents the historical author route; no calculation from those new "
        "starters was performed, and the original endpoints remain "
        "evaluator-private."
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize_embedded_paths(value: Any) -> Any:
    """Make embedded provenance paths portable in generated archives.

    Historical result JSON sometimes stores the absolute checkout prefix in
    fields such as ``output_dir`` or ``evidence_directory``.  The source
    result is left untouched; only the evaluator-private Markdown rendering
    receives repository-relative paths so archives remain relocatable.
    """
    prefix = re.compile(
        r"/inspire/hdd/global_user/lifangyuan-253108110077/"
        r"lifangyuan/benchmark/ResearchChemBench/"
    )
    if isinstance(value, dict):
        return {key: normalize_embedded_paths(child) for key, child in value.items()}
    if isinstance(value, list):
        return [normalize_embedded_paths(child) for child in value]
    if isinstance(value, str):
        text = prefix.sub("", value)
        # Resolve the one historical wildcard used by the strict-v2 Ru
        # barrier record to the two successful, status-backed logs.  Earlier
        # pre-strict runs in the same directory tree are intentionally not
        # promoted to evidence.
        text = text.replace(
            "provenance/qzcli_hpc/*/1/gaussian.log copies",
            "provenance/qzcli_hpc/5bda_author_route_strict_v2/1/gaussian.log "
            "and provenance/qzcli_hpc/TS3bda_author_route_strict_v2/1/gaussian.log",
        )
        return text
    return value


def relpath(path: Path, repo: Path) -> str:
    try:
        return path.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return str(path)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def find_group(repo: Path, paper_id: str) -> Path | None:
    matches = [repo / "docs" / "verification" / name / paper_id for name in GROUP_ROOTS]
    matches = [path for path in matches if path.is_dir()]
    return sorted(matches)[0] if matches else None


def first_status(result: dict[str, Any], report: str) -> str:
    for key in ("status", "completion_status", "verification_status", "completion"):
        value = result.get(key)
        if isinstance(value, (str, int, float, bool)):
            return str(value)
    patterns = (
        r"最终严格(?:状态|判定)[^\n]{0,80}?(?:`|\*\*)?(PASS|QUALIFIED|CONDITIONAL|BLOCKED|IN_PROGRESS)(?:`|\*\*)?",
        r"最终(?:状态|判定)[^\n]{0,80}?(?:`|\*\*)?(PASS|QUALIFIED|CONDITIONAL|BLOCKED|IN_PROGRESS|FAIL|NOT_QUALIFIED)(?:`|\*\*)?",
        r"当前状态(?:快照)?[^\n]{0,80}?(?:`|\*\*)?(PASS|QUALIFIED|CONDITIONAL|BLOCKED|IN_PROGRESS|FAIL|NOT_QUALIFIED)(?:`|\*\*)?",
        r"(?:论文复现结论|evaluation 资格|评估任务资格)[^\n]{0,80}?(?:`|\*\*)?(PASS|QUALIFIED|CONDITIONAL|BLOCKED)(?:`|\*\*)?",
        r"(?:论文复现|author route|作者路线)[^\n]{0,100}?(?:`|\*\*)?(PASS|QUALIFIED|CONDITIONAL|BLOCKED)(?:`|\*\*)?",
    )
    for pattern in patterns:
        match = re.search(pattern, report, re.I)
        if match:
            return match.group(1)
    return "NOT_RECORDED"


def report_status_history(report: str) -> list[dict[str, Any]]:
    """Extract explicit terminal-status statements in document order.

    Verification reports commonly retain an early BLOCKED/CONDITIONAL
    snapshot followed by a later PASS after a repair.  Taking the first
    status made a valid final report look inconsistent with its results.json.
    Only lines with a terminal-status label are considered; job-table states
    and hypothetical ``if ... then downgrade`` prose are ignored.
    """
    rows: list[dict[str, Any]] = []
    status_re = re.compile(r"\b(PASS|QUALIFIED|CONDITIONAL|BLOCKED|IN_PROGRESS|FAIL|NOT_QUALIFIED)\b", re.I)
    anchors = re.compile(r"(?:最终(?:严格)?(?:状态|判定|结论)|最终三轴状态|当前(?:计算)?状态(?:快照)?|论文复现结论|evaluation 资格|评估任务资格|严格结论|本轮结果|(?:严格)?资格(?:记录)?\s*(?:为|=|:|is)|qualification(?:\s+record)?\s*(?:=|:|is))", re.I)
    for line_no, line in enumerate(report.splitlines(), 1):
        clean = line.strip()
        if not clean or not anchors.search(clean):
            continue
        matches = list(status_re.finditer(clean))
        if not matches:
            continue
        # Ignore hypothetical policy text such as “if ... downgrade to
        # CONDITIONAL”; an explicit report conclusion contains a status
        # adjacent to the anchor and is retained.
        match = matches[-1]
        if re.search(r"(?:如果|若|if).{0,50}(?:降级|downgrade|then)", clean, re.I):
            continue
        rows.append({"line": line_no, "status": match.group(1).upper(), "text": clean[:500]})
    return rows


def canonical_status(raw: str) -> str:
    text = raw.strip().casefold().replace("`", "")
    if text in SUCCESS_WORDS:
        return "SUCCESS_EVIDENCE_CANDIDATE"
    if any(word in text for word in PARTIAL_WORDS):
        return "PARTIAL_OR_BOUNDED"
    if text == "not_recorded" or not text:
        return "NOT_ESTABLISHED"
    if "complete" in text and not BAD_MARKER.search(text):
        return "SUCCESS_EVIDENCE_CANDIDATE"
    return "PARTIAL_OR_BOUNDED"


def json_path_exists(value: Any, path: str) -> bool:
    """Small JSONPath subset used by scoring bindings."""
    if path == "$":
        return True
    if not isinstance(path, str) or not path.startswith("$."):
        return False
    # Accept the small JSONPath dialect used by the evaluator files.  In
    # particular, ``items[]`` means "at least one item" and ``items[*]``
    # means "every/any item selected by the binding".  The former was
    # previously treated as a literal key and made valid result bindings look
    # missing in the audit report.
    parts = [part for part in path[2:].split(".") if part]

    def walk(obj: Any, index: int) -> bool:
        if index == len(parts):
            return True
        token = parts[index]
        match = re.fullmatch(r"([^\[\]]+)(?:\[([*0-9]*)\])?", token)
        if not match:
            return False
        key, selector = match.groups()
        if isinstance(obj, list):
            return any(walk(item, index) for item in obj)
        if not isinstance(obj, dict) or key not in obj:
            return False
        child = obj[key]
        if selector is None:
            return walk(child, index + 1)
        if not isinstance(child, list):
            return False
        if selector in {"", "*"}:
            return any(walk(item, index + 1) for item in child)
        position = int(selector)
        return position < len(child) and walk(child[position], index + 1)

    return walk(value, 0)


def json_path_values(value: Any, path: str) -> list[Any]:
    """Return values selected by the same small JSONPath dialect."""
    if path == "$":
        return [value]
    if not isinstance(path, str) or not path.startswith("$."):
        return []
    parts = [part for part in path[2:].split(".") if part]
    found: list[Any] = []

    def walk(obj: Any, index: int) -> None:
        if index == len(parts):
            found.append(obj)
            return
        token = parts[index]
        match = re.fullmatch(r"([^\[\]]+)(?:\[([*0-9]*)\])?", token)
        if not match:
            return
        key, selector = match.groups()
        if isinstance(obj, list):
            for item in obj:
                walk(item, index)
            return
        if not isinstance(obj, dict) or key not in obj:
            return
        child = obj[key]
        if selector is None:
            walk(child, index + 1)
        elif isinstance(child, list):
            if selector in {"", "*"}:
                for item in child:
                    walk(item, index + 1)
            else:
                position = int(selector)
                if position < len(child):
                    walk(child[position], index + 1)

    walk(value, 0)
    return found


def _bad_key(key: str) -> bool:
    # A successful job is often keyed by its retry-labelled run name. Only
    # explicit history fields are excluded here; record status decides the rest.
    return key.casefold() in {
        "failure", "failures", "failure_reason", "failure_context",
        "failed_attempts", "failed_jobs", "failed_candidates", "attempts",
        "submission_attempts", "queue", "running", "pending", "blocked",
        "unresolved", "retry", "migration",
    }


def explicitly_unsuccessful(payload: dict[str, Any]) -> bool:
    """Reject explicit failures, even if a conflicting wrapper says success.

    Inspect this record only: a successful result may legitimately include a
    separate failed-attempt history. Recursive filtering handles child records.
    """
    for name in ("status", "state", "outcome", "completion_status"):
        value = payload.get(name)
        if isinstance(value, str) and UNSUCCESSFUL_STATUS_VALUE.fullmatch(value):
            return True
    for name in ("return_code", "exit_code"):
        value = payload.get(name)
        if value is not None:
            try:
                if int(value) != 0:
                    return True
            except (ValueError, TypeError):
                return True
    return payload.get("normal_termination") is False or payload.get("error_termination") is True


def successful_execution_payload(payload: dict[str, Any]) -> bool:
    """Execution metadata gate, NOT proof of scientific convergence."""
    if explicitly_unsuccessful(payload):
        return False
    state = str(payload.get("status", payload.get("state", ""))).strip().casefold()
    rc = payload.get("return_code", payload.get("exit_code"))
    return state in {"success", "successful", "complete", "completed", "validated", "passed"} or rc in (0, "0")


def compact_success(value: Any, *, key: str = "", depth: int = 0) -> Any:
    """Filter failed records without truncating valid scientific dependencies."""
    if _bad_key(key) and key.casefold() not in {"conclusion", "limitations"}:
        return None
    if isinstance(value, dict):
        if explicitly_unsuccessful(value):
            return None
        result: dict[str, Any] = {}
        for child_key, child_value in value.items():
            if _bad_key(str(child_key)) and str(child_key).casefold() not in {"conclusion", "limitations"}:
                continue
            compact = compact_success(child_value, key=str(child_key), depth=depth + 1)
            if compact is not None:
                result[str(child_key)] = compact
        return result
    if isinstance(value, list):
        kept: list[Any] = []
        for item in value:
            if isinstance(item, dict):
                # Only an explicitly scalar status/outcome can classify an
                # entry as failed/retry.  ``outcome`` is often a structured
                # result object containing nested evidence paths (some of
                # which may mention an old retry); stringifying that object
                # would incorrectly discard the entire valid result.
                if explicitly_unsuccessful(item):
                    continue
            compact = compact_success(item, key=key, depth=depth + 1)
            if compact is not None:
                kept.append(compact)
        return kept
    if isinstance(value, str):
        # Do not carry retry/failure/queue references into the archived
        # standard chain even when they occur in a free-text evidence field.
        # A conclusion/limitation may mention that such work was excluded,
        # but the actual retry path and output are not retained here.
        if UNSUCCESSFUL_STATUS_VALUE.search(value) and key.casefold() not in {"conclusion", "limitations"}:
            return None
        return value
    return value


def collect_referenced_paths(value: Any, *, key: str = "") -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            found.update(collect_referenced_paths(child_value, key=str(child_key)))
    elif isinstance(value, list):
        for item in value:
            found.update(collect_referenced_paths(item, key=key))
    elif isinstance(value, str):
        if re.search(r"(?:path|file|artifact|evidence|provenance|stdout|checkpoint|input|output|log)", key, re.I):
            for match in re.findall(r"(?:docs/verification/|artifacts/|provenance/|native_workspace/|outputs/|logs/)[^\s,;`\"']+", value):
                candidate = match.rstrip(".)]")
                # Keep a path even when its filename says ``retry``; a
                # successful corrected run can legitimately use that label.
                # Free-text failure descriptions without a concrete path are
                # still ignored by this path-only collector.
                found.add(candidate)
    return found


def resolve_evidence_paths(raw: str, group: Path, repo: Path) -> list[Path]:
    """Resolve evidence references, including fragments, globs and dirs.

    Result records predate the archive format and may point at a JSON
    fragment (``file.json#field``), a glob such as ``qzcli_hpc/*/1/log`` or a
    run directory.  Resolve those references to durable files for the archive
    rather than emitting a misleading "not found" line.  A missing base file
    still returns an empty list and is retained as an explicit gap.
    """
    base = str(raw).split("#", 1)[0].rstrip(".)]")
    roots = [group / base, repo / base]
    # Some historical result fields were written relative to a workspace
    # rather than the paper directory (for example ``outputs/...`` under
    # ``native_workspace_batch``).  Try those explicit, repository-local
    # prefixes without guessing arbitrary external locations.
    if base.startswith("outputs/"):
        roots.extend(group / prefix / base for prefix in ("native_workspace_batch", "native_workspace"))
    matches: list[Path] = []
    for candidate in roots:
        if any(mark in str(candidate) for mark in ("*", "?", "[")):
            for path_text in glob.glob(str(candidate), recursive=True):
                path = Path(path_text)
                if not path.is_file():
                    continue
                # A wildcard can match abandoned/failed historical runs.  A
                # success status in the same run directory is required before
                # a wildcard match is called a retained evidence anchor.
                status_path = path.parent / "status.json"
                try:
                    status_payload = load_json(status_path) if status_path.is_file() else {}
                except Exception:
                    status_payload = {}
                state = str(status_payload.get("status", status_payload.get("state", ""))).casefold()
                rc = status_payload.get("return_code", status_payload.get("exit_code"))
                if successful_execution_payload(status_payload):
                    matches.append(path)
        elif candidate.is_file():
            matches.append(candidate)
        elif candidate.is_dir():
            # A directory is represented by its most useful durable records.
            for name in (
                "status.json", "parsed_observables.json", "collection.json",
                "hpc_collection_record.json", "normal_termination.marker",
                "complete.marker", "stdout.log", "input.com",
            ):
                child = candidate / name
                if child.is_file():
                    matches.append(child)
                    break
    unique: list[Path] = []
    seen: set[str] = set()
    for path in matches:
        resolved = path.resolve()
        if str(resolved) not in seen:
            seen.add(str(resolved))
            unique.append(resolved)
    return unique


def successful_report_lines(report: str) -> list[str]:
    lines: list[str] = []
    patterns = re.compile(
        r"normal termination|opt(?:imization)?(?:/|\s)freq|zero imaginary|frequency.{0,20}0|"
        r"all .*validated|evaluator.{0,30}(?:pass|closed|一致)|严格判定.{0,20}pass|"
        r"author route.{0,20}(?:pass|qualified)|科学闸门.{0,20}(?:pass|闭合)",
        re.I,
    )
    for line in report.splitlines():
        clean = line.strip()
        if not clean or BAD_MARKER.search(clean):
            continue
        if patterns.search(clean):
            lines.append(clean[:500])
        if len(lines) >= 12:
            break
    return lines


def unresolved_geometry_failure(run_dir: Path) -> bool:
    """Reject definite application-level failures despite a successful wrapper.

    This is a negative-evidence filter, not a generic convergence certificate.
    Missing logs or unfamiliar software still need scientific review. Scan
    complete textual logs so a long trailing footer cannot hide a failure.
    A later explicit convergence marker in the same log may close a retry.
    """
    marker = re.compile(
        r"FAILED TO CONVERGE GEOMETRY OPTIMIZATION|"
        r"THE OPTIMIZATION DID NOT CONVERGE|"
        r"GEOMETRY OPTIMIZATION CONVERGED|THE OPTIMIZATION HAS CONVERGED",
        re.I,
    )
    for name in ("stdout.log", "orca_stdout.log", "xtb.out", "xtb.log", "output.out"):
        path = run_dir / name
        if not path.is_file():
            continue
        last_failed = False
        with path.open(encoding="utf-8", errors="replace") as stream:
            for line in stream:
                for match in marker.finditer(line):
                    value = match.group().upper()
                    last_failed = "FAILED" in value or "DID NOT" in value
        if last_failed:
            return True
    return False


def successful_artifact_evidence(group: Path | None, *, limit: int | None = None) -> list[dict[str, Any]]:
    """Return a complete inventory of execution-candidate textual artifacts.

    ``results.json`` is a summary and is not by itself proof that a calculation
    ran.  A status record with a zero return code plus a nearby input/output or
    log is the minimum provenance anchor used here, not proof of scientific
    convergence. The raw application's criteria still require review. Failed/queued directories
    and explicitly retry-status records are excluded; a corrected calculation
    with a retry-labelled directory name is retained when its terminal status
    or return code is successful.
    """
    if group is None:
        return []
    rows: list[dict[str, Any]] = []
    status_files = sorted(group.rglob("status.json"))
    for status_path in status_files:
        try:
            payload = load_json(status_path)
        except Exception:
            continue
        state = str(payload.get("status", payload.get("state", ""))).casefold()
        rc = payload.get("return_code", payload.get("exit_code"))
        success = successful_execution_payload(payload)
        rel_status = status_path.relative_to(group).as_posix()
        # A directory name containing ``retry`` is not sufficient to discard
        # an otherwise successful calculation: the final, corrected run is
        # often deliberately stored under a retry-labelled directory.  Only
        # the recorded status/return code and explicit application failures
        # decide candidate eligibility here. The retry marker is retained as
        # path provenance for human review, not treated as a failure itself.
        if not success or unresolved_geometry_failure(status_path.parent):
            continue
        # Keep the status record and the concrete files in the same execution
        # directory.  Do not include another status file or bulky checkpoints
        # unless no textual/output artifact exists.
        run_dir = status_path.parent
        siblings = [
            p for p in sorted(run_dir.iterdir())
            if p.is_file()
            and p.name != "status.json"
            and p.name not in VOLATILE_EXECUTION_FILENAMES
        ]
        preferred = [
            p for p in siblings
            if p.suffix.casefold() in {".com", ".inp", ".gjf", ".log", ".out", ".xyz", ".sdf", ".json", ".csv", ".cif", ".hess", ".fchk"}
            or p.name in {"INCAR", "POSCAR", "CONTCAR", "KPOINTS", "OUTCAR", "EIGENVAL", "PROCAR", "DOSCAR", "OSZICAR"}
        ]
        chosen = preferred or siblings
        for path in [status_path, *chosen]:
            if path.name in VOLATILE_EXECUTION_FILENAMES:
                # Scheduler bookkeeping is intentionally not part of the
                # durable scientific artifact inventory.  Its path may still
                # appear in a separately recorded drift note from an earlier
                # audit, but it must not affect newly generated archives.
                continue
            rel = path.relative_to(group).as_posix()
            rows.append({"path": rel, "sha256": sha256(path), "size": path.stat().st_size, "role": "successful execution artifact" if path != status_path else "successful status record"})
            if limit is not None and len(rows) >= limit:
                return rows
    return rows


def successful_execution_steps(group: Path | None, *, limit: int | None = None) -> list[dict[str, Any]]:
    """Extract ordered, success-only execution metadata from status records."""
    if group is None:
        return []
    steps: list[dict[str, Any]] = []
    seen_jobs: set[str] = set()
    for status_path in sorted(group.rglob("status.json")):
        try:
            payload = load_json(status_path)
        except Exception:
            continue
        rel_status = status_path.relative_to(group).as_posix()
        state = str(payload.get("status", payload.get("state", ""))).casefold()
        rc = payload.get("return_code", payload.get("exit_code"))
        if not successful_execution_payload(payload) or unresolved_geometry_failure(status_path.parent):
            continue
        # See ``successful_artifact_evidence``: a successful corrected run may
        # retain ``retry`` in its directory name, while failed/running runs
        # are filtered by their explicit state/return code below.
        job_id = str(payload.get("job_id", ""))
        if job_id and job_id in seen_jobs:
            continue
        if job_id:
            seen_jobs.add(job_id)
        metadata = payload.get("metadata", {}) if isinstance(payload.get("metadata"), dict) else {}
        synopsis = metadata.get("invocation_synopsis") or payload.get("invocation_synopsis")
        if not synopsis:
            command = payload.get("command")
            synopsis = " ".join(str(x) for x in command) if isinstance(command, list) else command
        validation = metadata.get("input_deck_validation", {}) if isinstance(metadata.get("input_deck_validation"), dict) else {}
        segments = validation.get("segments", []) if isinstance(validation, dict) else []
        route = segments[0].get("route") if segments and isinstance(segments[0], dict) else None
        run_dir = status_path.parent
        outputs = [
            p.relative_to(group).as_posix()
            for p in sorted(run_dir.iterdir())
            if p.is_file()
            and p.name != "status.json"
            and p.name not in VOLATILE_EXECUTION_FILENAMES
        ]
        steps.append({
            "status_path": rel_status,
            "job_id": job_id or None,
            "label": metadata.get("label"),
            "calculation_intent": metadata.get("calculation_intent") or validation.get("calculation_intent"),
            "software_id": metadata.get("software_id"),
            "submitted_at": payload.get("submitted_at"),
            "started_at": payload.get("started_at"),
            "route": route,
            "invocation": synopsis,
            "outputs": outputs,
        })
    steps.sort(key=lambda row: (str(row.get("submitted_at") or row.get("started_at") or "~"), row["status_path"]))
    return steps if limit is None else steps[:limit]


def analytic_continuum_steps(group: Path | None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return the recorded non-scheduler chain for the nanoscroll task.

    The task was verified by a deterministic continuum calculation, so there
    is intentionally no scheduler ``status.json``.  The two durable artifacts
    and the mathematical operations below are the actual successful chain;
    this helper only indexes existing files and never recomputes them.
    """
    if group is None:
        return [], []
    artifact_dir = group / "artifacts"
    result = artifact_dir / "continuum_minimization.json"
    scan = artifact_dir / "continuum_energy_scan.csv"
    if not (result.is_file() and scan.is_file()):
        return [], []
    artifacts = [
        {"path": result.relative_to(group).as_posix(), "sha256": sha256(result), "size": result.stat().st_size, "role": "analytic minimization result"},
        {"path": scan.relative_to(group).as_posix(), "sha256": sha256(scan), "size": scan.stat().st_size, "role": "bounded branch scan"},
    ]
    output_paths = [result.relative_to(group).as_posix(), scan.relative_to(group).as_posix()]
    labels = [
        "Read the public two-segment continuum parameters and area-conserved joined Archimedean geometry.",
        "Evaluate total energy per width over the bounded 2001-point inner-radius scan and retain complete/incomplete branches.",
        "Minimize the admissible complete-turn branch with the bounded scalar minimizer.",
        "Independently solve the analytic complete-branch derivative with a Brent root and compare the radii.",
        "Check stationarity, positive second derivative, neighboring radii and incomplete-branch boundary before selecting the regime.",
    ]
    steps = [
        {
            "status_path": result.relative_to(group).as_posix(),
            "label": label,
            "calculation_intent": "analytic_continuum_step",
            "route": "recorded mathematical workflow; no scheduler job",
            "outputs": output_paths,
        }
        for label in labels
    ]
    return artifacts, steps


def instruction_audit(package: Path, mode: str) -> dict[str, Any]:
    task = package / "agent_input" / "task.md"
    text = task.read_text(encoding="utf-8", errors="replace") if task.is_file() else ""
    headings = [
        "# Scientific objective",
        "# Public inputs and scientific boundaries",
        "# Required scientific validation/investigation",
        "# Deliverables",
    ]
    if mode == "paper_reproduction":
        headings.insert(1, "# Author-provided scientific guidance")
    positions = [text.find(item) for item in headings]
    findings: list[str] = []
    if any(position < 0 for position in positions):
        findings.append("required_heading_missing")
    elif positions != sorted(positions):
        findings.append("required_heading_order_invalid")
    if mode == "autonomous_research":
        if "# Author-provided scientific guidance" in text:
            findings.append("author_guidance_exposed_in_autonomous_instruction")
        if not re.search(r"do not use.{0,80}(paper|SI)|不得读取.{0,40}(论文|SI)", text, re.I | re.S):
            findings.append("autonomous_no_paper_boundary_not_explicit")
    else:
        if "# Author-provided scientific guidance" not in text:
            findings.append("reproduction_guidance_section_missing")
    if not re.search(r"(?:failure|failed|bounded|失败|不确定|unresolved|停止|stop)", text, re.I):
        findings.append("failure_or_stopping_boundary_not_obvious")
    return {"format_ok": not findings, "findings": findings, "heading_positions": positions}


def _bounded_input_value(value: Any, *, depth: int = 0) -> Any:
    """Make a short, human-readable representation of a public boundary value."""
    if depth > 2:
        return "<nested value omitted>"
    if isinstance(value, (str, int, float, bool)) or value is None:
        if isinstance(value, str) and len(value) > 240:
            return value[:237] + "..."
        return value
    if isinstance(value, list):
        if len(value) > 8:
            return f"<list of {len(value)} items>"
        return [_bounded_input_value(item, depth=depth + 1) for item in value]
    if isinstance(value, dict):
        if depth >= 2:
            return f"<object with {len(value)} keys>"
        return {
            str(key): _bounded_input_value(child, depth=depth + 1)
            for key, child in list(value.items())[:16]
        }
    return str(value)[:240]


def _collect_input_boundary_fields(value: Any, *, prefix: str = "$", depth: int = 0) -> dict[str, Any]:
    """Collect charge/state/unit/identity fields from a public JSON payload."""
    if depth > 5:
        return {}
    found: dict[str, Any] = {}
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            child_path = f"{prefix}.{key_text}"
            if INPUT_BOUNDARY_KEY.search(key_text):
                found[child_path] = _bounded_input_value(child)
            found.update(_collect_input_boundary_fields(child, prefix=child_path, depth=depth + 1))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found.update(_collect_input_boundary_fields(child, prefix=f"{prefix}[{index}]", depth=depth + 1))
    return found


def _result_scalar_leaves(value: Any, *, prefix: str, limit: int | None = None) -> list[dict[str, Any]]:
    """Index every scalar result leaf by default; no silent candidate cutoff."""
    leaves: list[dict[str, Any]] = []

    def walk(obj: Any, path: str) -> None:
        if limit is not None and len(leaves) >= limit:
            return
        if isinstance(obj, dict):
            for key, child in obj.items():
                key_text = str(key)
                if _bad_key(key_text) and key_text.casefold() not in {"conclusion", "limitations"}:
                    continue
                walk(child, f"{path}.{key_text}")
                if limit is not None and len(leaves) >= limit:
                    return
        elif isinstance(obj, list):
            for index, child in enumerate(obj):
                walk(child, f"{path}[{index}]")
                if limit is not None and len(leaves) >= limit:
                    return
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            if isinstance(obj, str) and UNSUCCESSFUL_STATUS_VALUE.search(obj):
                return
            leaves.append({"path": path, "value": obj})

    walk(value, prefix)
    return leaves


def _numeric_leaves(value: Any) -> list[float | int]:
    """Return numeric leaves without using evaluator targets as outputs."""
    found: list[float | int] = []
    if isinstance(value, bool):
        return found
    if isinstance(value, (int, float)):
        return [value]
    if isinstance(value, dict):
        for key, child in value.items():
            if _bad_key(str(key)) and str(key).casefold() not in {"conclusion", "limitations"}:
                continue
            found.extend(_numeric_leaves(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(_numeric_leaves(child))
    return found


def _xyz_boundary_fields(lines: list[str]) -> dict[str, Any]:
    """Extract explicit state/unit hints from an XYZ comment without guessing."""
    if len(lines) < 2:
        return {}
    comment = lines[1]
    fields: dict[str, Any] = {}
    patterns = {
        "charge": r"\b(?:formal\s+)?charge\s*[:=]?\s*([+-]?\d+(?:\.\d+)?)",
        "multiplicity": r"\b(?:spin\s+)?multiplicity\s*[:=]?\s*(\d+)",
        "units": r"\b(?:coordinate\s+)?units?\s*[:=]?\s*([A-Za-zÅμ/^-]+)",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, comment, re.I)
        if match:
            fields[key] = match.group(1)
    if not fields and re.search(r"(?:angstrom|\bÅ\b|\bA\b)", comment, re.I):
        # A unit is recorded only when the comment explicitly names it.  Do
        # not infer Å merely from a common XYZ convention.
        fields["units_hint"] = "explicit angstrom marker"
    return fields


def input_audit(package: Path, task_info: dict[str, Any], paper_info: dict[str, Any]) -> dict[str, Any]:
    data_root = package / "agent_input" / "data"
    declared_missing: list[str] = []
    for item in task_info.get("data", []):
        raw_path = Path(str(item.get("path", "")))
        # task_info paths are relative to agent_input/data in some historical
        # packages and to agent_input in others.  Resolve both conventions;
        # never treat the repository root as an input fallback.
        declared = data_root / raw_path
        if not declared.exists():
            declared = package / "agent_input" / raw_path
        if not declared.exists():
            declared_missing.append(str(item.get("path", "")))
    parse_errors: list[str] = []
    xyz_invalid_rows: list[str] = []
    input_files: list[dict[str, Any]] = []
    if data_root.is_dir():
        for path in sorted(x for x in data_root.rglob("*") if x.is_file()):
            entry = {"path": path.relative_to(package).as_posix(), "sha256": sha256(path), "size": path.stat().st_size}
            if path.suffix.casefold() == ".json":
                try:
                    payload = load_json(path)
                    boundary_fields = _collect_input_boundary_fields(payload)
                    if boundary_fields:
                        entry["boundary_fields"] = boundary_fields
                except Exception as exc:  # pragma: no cover - diagnostic only
                    parse_errors.append(f"{entry['path']}:{type(exc).__name__}")
            if path.suffix.casefold() == ".xyz":
                try:
                    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
                    count = int(lines[0].strip())
                    entry["xyz_atom_count"] = count
                    if len(lines) > 1:
                        entry["xyz_comment"] = lines[1][:500]
                    xyz_fields = _xyz_boundary_fields(lines)
                    if xyz_fields:
                        entry["boundary_fields"] = xyz_fields
                    if len(lines) < count + 2:
                        parse_errors.append(f"{entry['path']}:xyz_truncated")
                    else:
                        for row_no, line in enumerate(lines[2 : count + 2], start=3):
                            fields = line.split()
                            if len(fields) != 4 or not re.fullmatch(r"[A-Z][a-z]?", fields[0]):
                                xyz_invalid_rows.append(f"{entry['path']}:{row_no}")
                except Exception as exc:
                    parse_errors.append(f"{entry['path']}:xyz_{type(exc).__name__}")
            input_files.append(entry)
    task_paper = task_info.get("paper", {}) if isinstance(task_info.get("paper"), dict) else {}
    title_match = bool(task_paper.get("title") and task_paper.get("title") == paper_info.get("title"))
    doi_match = bool(task_paper.get("doi") and str(task_paper.get("doi")).casefold() == str(paper_info.get("doi", "")).casefold())
    abs_refs = []
    task_path = package / "agent_input" / "task.md"
    if task_path.is_file():
        for line_no, line in enumerate(task_path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if ABSOLUTE_REF.search(line):
                abs_refs.append(f"task.md:{line_no}")
    return {
        "declared_data_missing": declared_missing,
        "declared_data": [
            {"path": str(item.get("path", "")), "description": str(item.get("description", ""))}
            for item in task_info.get("data", [])
            if isinstance(item, dict)
        ],
        "json_or_xyz_parse_errors": parse_errors,
        "xyz_invalid_element_rows": xyz_invalid_rows,
        "input_files": input_files,
        "paper_title_match": title_match,
        "paper_doi_match": doi_match,
        "absolute_agent_references": abs_refs,
        "identity_status": "MATCHED" if title_match and doi_match and not declared_missing and not parse_errors and not xyz_invalid_rows else "REVIEW_REQUIRED",
    }


def leakage_audit(package: Path) -> dict[str, Any]:
    candidates: list[dict[str, Any]] = []
    confirmed: list[dict[str, Any]] = []
    provenance_reviews: list[dict[str, Any]] = []
    data_root = package / "agent_input" / "data"
    if not data_root.is_dir():
        return {"potential_candidates": candidates, "confirmed_answer_bearing": confirmed, "si_provenance_reviews": provenance_reviews}
    task_text = (package / "agent_input" / "task.md").read_text(encoding="utf-8", errors="replace") if (package / "agent_input" / "task.md").is_file() else ""
    for path in sorted(x for x in data_root.rglob("*") if x.is_file()):
        relative = path.relative_to(package).as_posix()
        suffix = path.suffix.casefold()
        name_hit = bool(HIGH_RISK_MARKER.search(path.name))
        header = ""
        if suffix in STRUCTURE_SUFFIXES:
            header = "\n".join(path.read_text(encoding="utf-8", errors="replace").splitlines()[:3])
        if name_hit or HIGH_RISK_MARKER.search(header):
            candidates.append({"path": relative, "reason": "high-risk structure/name marker; manual semantic check required"})
            # A structure explicitly identified in the public task as an
            # optimized SI/transition-state result is not merely a filename
            # heuristic.  It is a confirmed answer-bearing geometry candidate
            # under the benchmark's no-final-result exposure policy.
            filename_match = re.search(re.escape(path.name), task_text, re.I)
            task_context = ""
            if filename_match:
                task_context = task_text[max(0, filename_match.start() - 180):filename_match.end() + 420]
            local_text = f"{path.name}\n{header}\n{task_context}"
            if SI_MARKER.search(local_text) and re.search(r"optimized|optimised|final|transition\s+state|TS[- _]?\d", local_text, re.I):
                confirmed.append({
                    "path": relative,
                    "reason": "public task/input identifies this as an SI optimized/final or transition-state geometry; remove or redesign when the geometry is itself a scored endpoint",
                })
        if SI_MARKER.search(header) or SI_MARKER.search(path.name):
            provenance_reviews.append({"path": relative, "reason": "SI provenance marker; not by itself proof of final-answer leakage"})
    return {"potential_candidates": candidates, "confirmed_answer_bearing": confirmed, "si_provenance_reviews": provenance_reviews}


def answer_value_leakage_audit(package: Path) -> list[dict[str, Any]]:
    """Find exact evaluator target literals in agent-visible text.

    This is deliberately a candidate detector: common physical numbers can
    occur legitimately in a boundary definition, so a hit requires manual
    interpretation against the task objective and paper route.
    """
    eval_root = package / "evaluation"
    targets: list[str] = []
    rules_path = eval_root / "scoring_rules.json"
    if rules_path.is_file():
        try:
            rules = load_json(rules_path)
            for row in rules.get("rules", []):
                if isinstance(row, dict) and isinstance(row.get("target"), (int, float)):
                    value = row["target"]
                    targets.extend({str(value), f"{value:g}"})
                if isinstance(row, dict) and isinstance(row.get("expected"), str) and len(row["expected"].strip()) >= 32:
                    targets.append(row["expected"].strip())
        except Exception:
            pass
    kp_path = eval_root / "reference_key_points.json"
    if kp_path.is_file():
        try:
            payload = load_json(kp_path)
            for row in payload.get("items", []):
                if isinstance(row, dict) and isinstance(row.get("expected"), (int, float)):
                    targets.append(str(row["expected"]))
                if isinstance(row, dict) and isinstance(row.get("statement"), str) and len(row["statement"].strip()) >= 48:
                    targets.append(row["statement"].strip())
        except Exception:
            pass
    targets = sorted(set(targets), key=len, reverse=True)
    if not targets:
        return []
    # Coordinates and crystallographic numeric fields naturally repeat values
    # that may also occur as evaluator targets.  They are handled by the
    # geometry/provenance audit instead; scan task prose and structured
    # metadata only to avoid reporting every coincidental coordinate match.
    visible: list[Path] = [
        p for p in (package / "agent_input").rglob("*")
        if p.is_file() and p.suffix.casefold() not in STRUCTURE_SUFFIXES
    ]
    findings: list[dict[str, Any]] = []
    for path in visible:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for target in targets:
            if len(target) < 4:
                continue
            if target in text:
                findings.append({"path": path.relative_to(package).as_posix(), "literal": target, "reason": "exact evaluator target/expected text appears in agent-visible content; manual semantic review required"})
    return findings


def _schema_required_paths(schema: Any, *, prefix: str = "$") -> set[str]:
    """Collect required object paths from a JSON-schema branch.

    This is deliberately limited to the object/``properties`` subset used by
    task submission schemas.  Arrays and free-form additional properties do
    not create a deterministic evaluator binding, so they are not expanded.
    """
    if not isinstance(schema, dict):
        return set()
    paths: set[str] = set()
    required = schema.get("required", [])
    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        properties = {}
    if isinstance(required, list):
        for key in required:
            key_text = str(key)
            child_path = f"{prefix}.{key_text}"
            paths.add(child_path)
            child_schema = properties.get(key)
            if isinstance(child_schema, dict):
                paths.update(_schema_required_paths(child_schema, prefix=child_path))
    return paths


def _evaluator_schema_branches(package: Path, result: dict[str, Any]) -> dict[str, Any]:
    """Resolve the applicable submission-schema ``oneOf`` branch, if any."""
    schema_path = package / "agent_input" / "submission_schema.json"
    if not schema_path.is_file():
        return {"schema_present": False, "matched_branch": None, "matched_required": set(), "inactive_required": set()}
    try:
        schema = load_json(schema_path)
    except Exception:
        return {"schema_present": True, "matched_branch": None, "matched_required": set(), "inactive_required": set(), "schema_error": True}
    result_schema = schema.get("result_schema", schema) if isinstance(schema, dict) else {}
    branches = result_schema.get("oneOf", []) if isinstance(result_schema, dict) else []
    if not isinstance(branches, list) or not branches:
        return {"schema_present": True, "matched_branch": None, "matched_required": set(), "inactive_required": set()}
    status = result.get("status") if isinstance(result, dict) else None
    matched: int | None = None
    branch_required: list[set[str]] = []
    for index, branch in enumerate(branches):
        branch_required.append(_schema_required_paths(branch))
        const = None
        if isinstance(branch, dict):
            props = branch.get("properties", {})
            status_schema = props.get("status", {}) if isinstance(props, dict) else {}
            if isinstance(status_schema, dict):
                const = status_schema.get("const")
        if const is not None and status == const:
            matched = index
    if matched is None:
        return {
            "schema_present": True,
            "matched_branch": None,
            "matched_required": set(),
            "inactive_required": set().union(*branch_required),
        }
    inactive = set().union(*(paths for i, paths in enumerate(branch_required) if i != matched))
    return {
        "schema_present": True,
        "matched_branch": matched,
        "matched_required": branch_required[matched],
        "inactive_required": inactive,
    }


def _field_is_branch_inapplicable(field: str, inactive_required: set[str]) -> bool:
    """Whether a missing evaluator field belongs only to another oneOf branch."""
    if not inactive_required:
        return False
    field_base = re.sub(r"\[[*0-9]*\]", "", str(field))
    for required in inactive_required:
        required_base = re.sub(r"\[[*0-9]*\]", "", required)
        if field_base == required_base or field_base.startswith(required_base + ".") or required_base.startswith(field_base + "."):
            return True
    return False


def _field_parent_has_bounded_failure(value: Any, path: str) -> bool:
    """Check whether the object containing a bound field is a bounded failure.

    Several task schemas encode success/bounded-failure as a nested ``oneOf``
    (for example, one branch per surface).  In those schemas a ``null`` or
    absent success-only observable is expected when that object's status is
    ``bounded_failure`` even though the top-level result object has no branch
    discriminator.
    """
    if not isinstance(path, str) or not path.startswith("$."):
        return False
    parts = [re.sub(r"\[[*0-9]*\]", "", token) for token in path[2:].split(".") if token]
    if not parts:
        return False
    parents: list[Any] = []

    def walk(obj: Any, index: int) -> None:
        if index == len(parts) - 1:
            parents.append(obj)
            return
        if isinstance(obj, list):
            for item in obj:
                walk(item, index)
            return
        if isinstance(obj, dict) and parts[index] in obj:
            walk(obj[parts[index]], index + 1)

    walk(value, 0)
    return any(
        isinstance(parent, dict)
        and str(parent.get("status", "")).casefold() in {"bounded_failure", "bounded-failure"}
        for parent in parents
    )


def evaluator_audit(package: Path, result: dict[str, Any]) -> dict[str, Any]:
    key_points = load_json(package / "evaluation" / "reference_key_points.json")
    conclusions = load_json(package / "evaluation" / "reference_conclusions.json")
    rules = load_json(package / "evaluation" / "scoring_rules.json")
    rule_rows = rules.get("rules", []) if isinstance(rules, dict) else []
    fields: list[str] = []
    bindings: list[dict[str, Any]] = []
    rule_specs: list[dict[str, Any]] = []
    bound_result_values: list[dict[str, Any]] = []
    bound_result_scalars: list[dict[str, Any]] = []
    numeric_target_checks: list[dict[str, Any]] = []
    seen_scalar_keys: set[str] = set()
    schema_branch = _evaluator_schema_branches(package, result)
    for row in rule_rows:
        binding = row.get("binding", {}) if isinstance(row, dict) else {}
        row_fields = binding.get("fields", []) if isinstance(binding, dict) else []
        applies_when = row.get("applies_when") if isinstance(row, dict) else None
        rule_applicable = True
        if isinstance(applies_when, dict):
            for condition_path, expected_value in applies_when.items():
                observed = json_path_values(result, str(condition_path))
                if isinstance(expected_value, list):
                    rule_applicable = rule_applicable and any(item in expected_value for item in observed)
                else:
                    rule_applicable = rule_applicable and any(item == expected_value for item in observed)
        fields.extend(str(field) for field in row_fields)
        bindings.append({
            "rule_id": row.get("rule_id"),
            "reference_id": row.get("reference_id"),
            "fields": row_fields,
        })
        rule_specs.append({
            "rule_id": row.get("rule_id"),
            "reference_id": row.get("reference_id"),
            "type": row.get("type"),
            "unit": row.get("unit"),
            "tolerance": row.get("tolerance"),
            "comparison": binding.get("comparison") if isinstance(binding, dict) else None,
            "applies_when": applies_when,
            "applicable_to_result": rule_applicable,
            "target_recorded_in_scoring_rules": "target" in row,
            "expected_recorded_in_scoring_rules": "expected" in row,
        })
        for field in row_fields:
            field_text = str(field)
            values = json_path_values(result, field_text)
            bound_result_values.append({
                "rule_id": row.get("rule_id"),
                "reference_id": row.get("reference_id"),
                "field": field_text,
                "present": bool(values),
                "values": [_bounded_input_value(value) for value in values[:8]],
            })
            for selected in values:
                for leaf in _result_scalar_leaves(selected, prefix=field_text):
                    scalar_key = f"{leaf['path']}={json.dumps(leaf['value'], ensure_ascii=False, sort_keys=True)}"
                    if scalar_key in seen_scalar_keys:
                        continue
                    seen_scalar_keys.add(scalar_key)
                    bound_result_scalars.append({
                        "rule_id": row.get("rule_id"),
                        "reference_id": row.get("reference_id"),
                        "field": field_text,
                        **leaf,
                    })
                    if len(bound_result_scalars) >= 240:
                        break
                if len(bound_result_scalars) >= 240:
                    break
            if len(bound_result_scalars) >= 240:
                break
        if isinstance(row, dict) and row.get("type") == "numeric" and isinstance(row.get("target"), (int, float)):
            tolerance = row.get("tolerance")
            tolerance_value = float(tolerance) if isinstance(tolerance, (int, float)) else 0.0
            numeric_values: list[float | int] = []
            for field in row_fields:
                numeric_values.extend(
                    number for selected in json_path_values(result, str(field))
                    for number in _numeric_leaves(selected)
                )
            target = float(row["target"])
            matches = [value for value in numeric_values if abs(float(value) - target) <= tolerance_value]
            branch_inapplicable = any(
                _field_is_branch_inapplicable(str(field), schema_branch.get("inactive_required", set()))
                for field in row_fields
            )
            nested_bounded_failure = any(
                _field_parent_has_bounded_failure(result, str(field)) for field in row_fields
            )
            applicable = rule_applicable and not (not numeric_values and (branch_inapplicable or nested_bounded_failure))
            numeric_target_checks.append({
                "rule_id": row.get("rule_id"),
                "reference_id": row.get("reference_id"),
                "target": row.get("target"),
                "unit": row.get("unit"),
                "tolerance": row.get("tolerance"),
                "result_numeric_values": numeric_values[:32],
                # Several selected values need a chemical/object identity
                # join. Never select whichever value happens to pass gold.
                "within_tolerance": bool(matches) if applicable and len(numeric_values) == 1 else None,
                "identity_binding_review_required": applicable and len(numeric_values) != 1,
                "applicable_to_result_branch": applicable,
            })
    unique_fields = sorted(set(fields))
    missing = [field for field in unique_fields if not json_path_exists(result, field)]
    expected_branch_missing = [
        field for field in missing
        if _field_is_branch_inapplicable(field, schema_branch.get("inactive_required", set()))
    ]
    missing = [field for field in missing if field not in expected_branch_missing]
    def has_payload(value: Any) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            return value.strip().casefold() not in {"", "null", "none", "todo", "tbd", "pending", "not_available"}
        if isinstance(value, dict):
            return any(has_payload(v) for v in value.values())
        if isinstance(value, list):
            return any(has_payload(v) for v in value)
        return True  # zero and False are genuine observations, not missing.
    empty_fields = [field for field in unique_fields if json_path_exists(result, field)
                    and not any(has_payload(v) for v in json_path_values(result, field))
                    and not _field_is_branch_inapplicable(field, schema_branch.get("inactive_required", set()))
                    and not _field_parent_has_bounded_failure(result, field)]
    if missing:
        structural_status = "MISSING_RESULT_FIELDS"
    elif empty_fields:
        structural_status = "EMPTY_OR_PLACEHOLDER_RESULT_FIELDS"
    elif expected_branch_missing:
        structural_status = "BRANCH_INAPPLICABLE_FIELDS_ONLY"
    else:
        structural_status = "PRESENT"
    return {
        "key_point_ids": [row.get("key_point_id") for row in key_points.get("items", []) if isinstance(row, dict)],
        "conclusion_ids": [row.get("conclusion_id") for row in conclusions.get("items", []) if isinstance(row, dict)],
        "rule_ids": [row.get("rule_id") for row in rule_rows if isinstance(row, dict)],
        "bindings": bindings,
        "rule_specs": rule_specs,
        "bound_result_values": bound_result_values,
        "bound_result_scalars": bound_result_scalars,
        "numeric_target_checks": numeric_target_checks,
        "unique_bound_fields": unique_fields,
        "result_fields_missing": missing,
        "result_fields_empty_or_placeholder": empty_fields,
        "expected_branch_inapplicable_fields": expected_branch_missing,
        "schema_branch": {
            "schema_present": schema_branch.get("schema_present", False),
            "matched_branch": schema_branch.get("matched_branch"),
            "matched_required": sorted(schema_branch.get("matched_required", set())),
            "inactive_required": sorted(schema_branch.get("inactive_required", set())),
        },
        "structural_field_status": structural_status,
    }


def historical_flags(package: Path, mode: str) -> dict[str, Any] | None:
    summary = package.parent / "FINAL_AUDIT_SUMMARY.json"
    if not summary.is_file():
        return None
    try:
        payload = load_json(summary)
    except Exception:
        return None
    for row in payload.get("rows", []):
        if row.get("paper_id") == package.name and row.get("mode") == mode:
            return {
                "decision": row.get("decision"),
                "reason": row.get("reason"),
                "changed_files": row.get("changed_files", []),
                "deleted_files": row.get("deleted_files", []),
            }
    return None


def prior_archive_drift(package: Path, group: Path | None, current_result: Any, current_compact: Any) -> dict[str, Any] | None:
    """Compare the prior per-task archive with current source records.

    The archive itself is the only durable pointer to the previous source
    hashes in this workspace.  Preserve a conservative drift note when a
    group report/result was edited after the previous audit; do not infer that
    a changed hash means a changed scientific conclusion.
    """
    archive = package / "evaluation" / "verified_computation_reference.md"
    if not archive.is_file() or group is None:
        return None
    text = archive.read_text(encoding="utf-8", errors="replace")
    # A drift note already recorded by an earlier re-audit is retained if the
    # source now matches that archive, so repeated audits remain idempotent.
    existing = re.search(r"<!-- source-drift-json: (\{.*?\}) -->", text)
    prior_note: dict[str, Any] | None = None
    if existing:
        try:
            prior_note = json.loads(existing.group(1))
        except Exception:
            prior_note = None
    # Older audits may have archived a drift note solely because a scheduler
    # lifecycle ledger changed.  Those files are intentionally excluded from
    # the durable artifact inventory now; clear such a stale note when the
    # result hash and top-level scientific excerpt are unchanged.
    if prior_note:
        prior_paths = prior_note.get("changed_artifact_paths", [])
        if (
            prior_paths
            and all(Path(str(path)).name in VOLATILE_EXECUTION_FILENAMES for path in prior_paths)
            and prior_note.get("previous_sha256") == prior_note.get("current_sha256")
            and not prior_note.get("changed_top_level_keys")
        ):
            prior_note = None
    result_path = group / "report" / "results.json"
    repo = package.parents[2]
    rel_result = relpath(result_path, repo) if result_path.is_file() else None
    old_hash_match = re.search(rf"^- `{re.escape(rel_result or '')}` — .*?SHA-256 `([0-9a-f]{{64}})`", text, re.M) if rel_result else None
    current_hash = sha256(result_path) if result_path.is_file() else None
    old_hash = old_hash_match.group(1) if old_hash_match else None
    old_hashes = {m.group(1): m.group(2) for m in re.finditer(r"^- `([^`]+)` — .*?SHA-256 `([0-9a-f]{64})`", text, re.M)}
    current_artifacts = successful_artifact_evidence(group)
    current_hashes = {f"docs/verification/{group.parent.name}/{package.name}/{row['path']}": row['sha256'] for row in current_artifacts}
    changed_paths = sorted(path for path, old_value in old_hashes.items() if path in current_hashes and current_hashes[path] != old_value)
    # qzcli lifecycle ledgers are periodically rewritten with polling
    # timestamps/status bookkeeping.  They are retained and hashed as
    # evidence, but a repeat audit should not create a new scientific-drift
    # finding solely because that volatile ledger changed again.
    meaningful_changed_paths = [path for path in changed_paths if Path(path).name not in VOLATILE_EXECUTION_FILENAMES]
    if changed_paths and not meaningful_changed_paths and prior_note:
        return prior_note
    if old_hash and current_hash and old_hash != current_hash:
        old_json_match = re.search(r"## Successful calculation chain\n.*?```json\n(.*?)\n```", text, re.S)
        old_compact: Any = None
        if old_json_match:
            try:
                old_compact = json.loads(old_json_match.group(1))
            except Exception:
                pass
        changed_top_keys: list[str] = []
        if isinstance(old_compact, dict) and isinstance(current_compact, dict):
            changed_top_keys = sorted(k for k in set(old_compact) | set(current_compact) if old_compact.get(k) != current_compact.get(k))
        classification = "RUNTIME_METADATA_ONLY" if changed_top_keys and set(changed_top_keys) <= {"current_recovery"} and not meaningful_changed_paths else "SOURCE_RESULT_RECORD_CHANGED_REQUIRES_REVIEW"
        return {"detected": True, "previous_sha256": old_hash, "current_sha256": current_hash, "changed_top_level_keys": changed_top_keys, "changed_artifact_paths": changed_paths, "classification": classification}
    if changed_paths:
        classification = "RUNTIME_METADATA_ONLY" if not meaningful_changed_paths else "EXECUTION_ARTIFACT_HASH_CHANGED_REQUIRES_REVIEW"
        return {"detected": True, "previous_sha256": old_hash, "current_sha256": current_hash, "changed_top_level_keys": [], "changed_artifact_paths": changed_paths, "classification": classification}
    return prior_note


def build_record(repo: Path, mode: str, package: Path) -> dict[str, Any]:
    paper_id = package.name
    group = find_group(repo, paper_id)
    paper_dir = repo / "papers" / paper_id
    paper_info = load_json(paper_dir / "paper_info.json") if (paper_dir / "paper_info.json").is_file() else {}
    task_info = load_json(package / "task_info.json") if (package / "task_info.json").is_file() else {}
    report_path = group / "verification_report.md" if group else None
    result_path = group / "report" / "results.json" if group else None
    report = report_path.read_text(encoding="utf-8", errors="replace") if report_path and report_path.is_file() else ""
    try:
        result = load_json(result_path) if result_path and result_path.is_file() else {}
    except Exception:
        result = {}
    raw_status = first_status(result, report)
    status = canonical_status(raw_status)
    # Verification reports are append-only in practice: an early BLOCKED or
    # CONDITIONAL snapshot may be followed by a repaired, explicit PASS.  Keep
    # the full terminal-status history and use its last explicit conclusion as
    # the report's current status; do not let the first historical snapshot
    # create a false result/report conflict.
    report_history = report_status_history(report) if report else []
    report_raw_status = report_history[-1]["status"] if report_history else (first_status({}, report) if report else "NOT_RECORDED")
    report_status = canonical_status(report_raw_status)
    compact = compact_success(result)
    if not isinstance(compact, dict):
        compact = {"result_excerpt": compact}
    source_drift = prior_archive_drift(package, group, result, compact)
    artifact_evidence = successful_artifact_evidence(group)
    execution_steps = successful_execution_steps(group)
    if paper_id == "paper_63a9254b8e68a23c":
        analytic_artifacts, analytic_steps = analytic_continuum_steps(group)
        if analytic_artifacts:
            # This task has no scheduler status records; retain the explicit
            # mathematical chain and its durable artifacts instead.
            artifact_evidence = analytic_artifacts
            execution_steps = analytic_steps
    artifact_suffixes = {Path(row["path"]).suffix.casefold() for row in artifact_evidence}
    has_concrete_input = bool(artifact_suffixes & {".com", ".inp", ".gjf", ".xyz", ".sdf", ".cif", ".json"})
    has_concrete_output = bool(artifact_suffixes & {".log", ".out", ".xyz", ".sdf", ".chk", ".fchk", ".json", ".csv"})
    evidence_status = "NOT_ESTABLISHED"
    if paper_id == "paper_63a9254b8e68a23c" and execution_steps and artifact_evidence:
        evidence_status = "EVIDENCE_COMPLETE"
    elif result_path and result_path.is_file() and compact and status == "SUCCESS_EVIDENCE_CANDIDATE":
        has_method = any(key in compact for key in ("method", "methods", "protocol", "calculation", "computational_approach", "workflow"))
        has_validation = any(key in compact for key in ("validation", "validation_evidence", "geometry_validation", "structure_validation", "frequency_validation", "stationary_point", "observables", "candidates", "states", "structures", "molecules", "systems"))
        evidence_status = "EVIDENCE_COMPLETE" if has_method and has_validation and has_concrete_input and has_concrete_output else "PARTIAL"
    elif result_path and result_path.is_file() and compact:
        evidence_status = "PARTIAL"

    refs = collect_referenced_paths(result)
    evidence_files: list[dict[str, Any]] = []
    for path in [report_path, result_path]:
        if path and path.is_file():
            evidence_files.append({"path": relpath(path, repo), "sha256": sha256(path), "size": path.stat().st_size, "role": "verification record"})
    for raw in sorted(refs):
        resolved_paths = resolve_evidence_paths(raw, group, repo) if group else []
        if not resolved_paths:
            evidence_files.append({"path": raw, "exists": False, "role": "reported evidence path; not found at audit time"})
        else:
            existing_paths = {row.get("path") for row in evidence_files}
            for resolved in resolved_paths:
                resolved_rel = relpath(resolved, repo)
                if resolved_rel not in existing_paths:
                    evidence_files.append({"path": resolved_rel, "sha256": sha256(resolved), "size": resolved.stat().st_size, "role": "referenced successful evidence"})
                    existing_paths.add(resolved_rel)

    paper_docs: list[dict[str, Any]] = []
    for doc in paper_info.get("documents", []):
        path = paper_dir / str(doc.get("path", ""))
        row = {"path": relpath(path, repo), "declared_sha256": doc.get("sha256"), "exists": path.is_file()}
        if path.is_file():
            row["actual_sha256"] = sha256(path)
            row["hash_match"] = row["actual_sha256"] == row["declared_sha256"]
        paper_docs.append(row)

    eval_audit = evaluator_audit(package, result) if (package / "evaluation" / "scoring_rules.json").is_file() else {}
    instr = instruction_audit(package, mode)
    inputs = input_audit(package, task_info, paper_info)
    leakage = leakage_audit(package)
    answer_leakage = answer_value_leakage_audit(package)
    current_change = CURRENT_FINAL_CHANGES.get(paper_id)
    replay_not_required = CURRENT_FINAL_REPLAY_NOT_REQUIRED.get(paper_id)
    current_applicability = "APPLICABLE_TO_CURRENT_FINAL" if not current_change else "AUTHOR_ROUTE_ONLY_PUBLIC_STARTER_NOT_REPLAYED"
    if current_change:
        current_applicability_reason = current_change + " Under the accepted author-route verification policy this starter difference is not itself a task/evaluator mismatch; no independent discovery or public-starter replay is claimed."
    elif replay_not_required:
        current_applicability_reason = replay_not_required
    else:
        current_applicability_reason = "No known public-input/endpoint rewrite was recorded in the final construction log; the author-route archive is applicable to the recorded scientific target, while evaluator contract consistency is checked separately."
    report_success_lines = successful_report_lines(report)
    issue_categories: list[str] = []
    historical = historical_flags(package, mode)
    if historical and historical.get("decision") not in {None, "EQUIVALENT_SAFE", "SAFE_WITH_SCHEMA_FIX"}:
        issue_categories.append("HISTORICAL_FINAL_HOLD_REVIEW")
    if len({item["status"] for item in report_history}) > 1:
        issue_categories.append("VERIFICATION_REPORT_STATUS_HISTORY")
    if report_raw_status != "NOT_RECORDED" and report_status not in {"SUCCESS_EVIDENCE_CANDIDATE"} and status == "SUCCESS_EVIDENCE_CANDIDATE":
        issue_categories.append("VERIFICATION_REPORT_RESULT_STATUS_CONFLICT")
    elif report_raw_status != "NOT_RECORDED" and report_status == "PARTIAL_OR_BOUNDED":
        issue_categories.append("VERIFICATION_REPORT_NOT_TERMINAL")
    if leakage["potential_candidates"]:
        issue_categories.append("POTENTIAL_DATA_LEAKAGE_REVIEW")
    if leakage.get("confirmed_answer_bearing"):
        issue_categories.append("CONFIRMED_ANSWER_BEARING_GEOMETRY_LEAKAGE")
    if answer_leakage:
        issue_categories.append("POTENTIAL_RESULT_VALUE_LEAKAGE")
    if instr["findings"]:
        issue_categories.append("INSTRUCTION_CLARITY")
    if inputs["identity_status"] != "MATCHED":
        issue_categories.append("INPUT_BOUNDARY_OR_IDENTITY")
    if inputs.get("xyz_invalid_element_rows"):
        issue_categories.append("XYZ_ELEMENT_PARSE_REVIEW")
    if eval_audit.get("result_fields_missing"):
        issue_categories.append("EVALUATOR_RESULT_FIELD_GAP")
    if any(
        check.get("applicable_to_result_branch", True)
        and check.get("within_tolerance") is False
        for check in eval_audit.get("numeric_target_checks", [])
    ):
        issue_categories.append("EVALUATOR_NUMERIC_TARGET_MISMATCH")
    if status != "SUCCESS_EVIDENCE_CANDIDATE":
        issue_categories.append("VERIFICATION_PARTIAL_OR_BOUNDED")
    if current_change:
        issue_categories.append("PUBLIC_STARTER_REPLAY_NOT_CLAIMED")
    if source_drift and source_drift.get("detected"):
        issue_categories.append("SOURCE_EVIDENCE_DRIFT_REVIEW")
    if not issue_categories:
        issue_categories.append("NO_STATIC_DEFECT_FOUND_SEMANTIC_REPLAY_REQUIRED")
    return {
        "paper_id": paper_id,
        "mode": mode,
        "package_path": relpath(package, repo),
        "group_path": relpath(group, repo) if group else None,
        "paper_path": relpath(paper_dir, repo),
        "paper": {"title": paper_info.get("title"), "doi": paper_info.get("doi"), "documents": paper_docs},
        "result_status_raw": raw_status,
        "result_status_class": status,
        "verification_report_status_raw": report_raw_status,
        "verification_report_status_class": report_status,
        "verification_report_status_history": report_history,
        "computation_chain_status": evidence_status,
        "current_final_applicability": current_applicability,
        "current_final_applicability_reason": current_applicability_reason,
        "source_evidence_drift": source_drift,
        "successful_report_evidence_lines": report_success_lines,
        "successful_artifact_evidence": artifact_evidence,
        "successful_execution_steps": execution_steps,
        "artifact_evidence_summary": {
            "count": len(artifact_evidence),
            "has_concrete_input": has_concrete_input,
            "has_concrete_output": has_concrete_output,
        },
        "successful_result_excerpt": compact,
        "evidence_files": evidence_files,
        "agent_input_files": inputs["input_files"],
        "instruction_audit": instr,
        "input_audit": inputs,
        "leakage_audit": leakage,
        "answer_value_leakage": answer_leakage,
        "evaluator_audit": eval_audit,
        "historical_stage08_flag": historical,
        "issue_categories": issue_categories,
        "excluded_from_standard_chain": "Failed or explicitly retry-status, migration-interrupted, queued/running, and evaluator-target-only entries were omitted; a retry-labelled path with an explicit successful terminal status is retained, while omitted entries are not evidence of a successful computation.",
    }


def markdown_record(record: dict[str, Any]) -> str:
    paper = record["paper"]
    eval_audit = record["evaluator_audit"]
    input_audit_data = record["input_audit"]
    answer_leak_summary = ", ".join(
        f"{item['path']}={item['literal']}" for item in record.get("answer_value_leakage", [])
    ) or "none detected"
    lines = [
        f"# Verified computation reference — {record['paper_id']} ({record['mode']})",
        "",
        "> Evaluator-private provenance archive, not the primary evaluator. It records evidence-backed historical calculations and their limits; scoring remains based on the task's intermediate key points and final conclusions. This file is not copied to `agent_input`.",
        "",
        "## Status",
        "",
        "Historical status below describes the archived group calculation; it is not a new run from any modified public starter.",
        "",
        f"- Computation-chain status: **{record['computation_chain_status']}**",
        f"- Group result status: `{record['result_status_raw']}` ({record['result_status_class']})",
        f"- Verification-report terminal status: `{record.get('verification_report_status_raw', 'NOT_RECORDED')}` ({record.get('verification_report_status_class', 'NOT_ESTABLISHED')})",
        f"- Applicability to current final package: **{record['current_final_applicability']}**",
        f"- Applicability note: {record['current_final_applicability_reason']}",
        "",
        "## Source identity",
        "",
        f"- Paper: {paper.get('title') or 'not recorded'}",
        f"- DOI: `{paper.get('doi') or 'not recorded'}`",
        f"- Task package: `{record['package_path']}`",
        f"- Verification group: `{record['group_path'] or 'not found'}`",
        f"- Paper documents: `{record['paper_path']}`",
        f"- Input identity audit: **{input_audit_data['identity_status']}** (title_match={input_audit_data['paper_title_match']}, doi_match={input_audit_data['paper_doi_match']})",
        "",
        "## Successful calculation chain",
        "",
        "The structured record below is derived from `report/results.json`. Explicit failed/cancelled/timed-out records and nonzero return codes are excluded recursively; valid scientific arrays are not truncated. Execution success and field presence do not certify scientific convergence or evaluator agreement.",
        "",
        "```json",
        json.dumps(normalize_embedded_paths(record["successful_result_excerpt"]), ensure_ascii=False, indent=2, sort_keys=True),
        "```",
        "",
    ]
    repair_note = REFERENCE_REPAIR_NOTES.get(record["paper_id"])
    if repair_note:
        if record["paper_id"] in {
            "paper_1b285cf9f763f2cf",
            "paper_534ae3b6e2fb695f",
            "paper_b815e2622b0d6085",
        }:
            heading = "Approved boundary repair"
        else:
            heading = "Public-input maintenance note"
        # Insert before the generated status history so the note remains the
        # first human-readable context after the archival disclaimer.
        lines[4:4] = [f"## {heading} (2026-09-14)", "", repair_note, ""]
    report_history = record.get("verification_report_status_history", [])
    if report_history:
        history_lines = [
            "Verification-report status history (explicit terminal-status statements):",
            "",
            "| line | status | statement |",
            "|---:|---|---|",
        ]
        for item in report_history:
            statement = str(item.get("text", "")).replace("|", "\\|")
            history_lines.append(f"| {item.get('line', '—')} | `{item.get('status', '—')}` | {statement} |")
        history_lines += [
            "",
            "The last explicit terminal statement is used as the report status. Earlier BLOCKED/CONDITIONAL snapshots remain historical evidence and are not by themselves a conflict with a later PASS.",
            "",
        ]
        lines[lines.index("## Source identity"):lines.index("## Source identity")] = history_lines
    drift = record.get("source_evidence_drift")
    if drift:
        lines += [
            "## Re-audit source-evidence drift",
            "",
            f"- Classification: **{drift.get('classification', 'REVIEW')}**",
            f"- Previous `results.json` SHA-256: `{drift.get('previous_sha256', 'not recorded')}`",
            f"- Current `results.json` SHA-256: `{drift.get('current_sha256', 'not recorded')}`",
            f"- Changed top-level result fields: `{', '.join(drift.get('changed_top_level_keys', [])) or 'not established'}`",
            f"- Changed execution-artifact paths: `{', '.join(drift.get('changed_artifact_paths', [])) or 'none detected'}`",
            "",
            "A source hash change is not treated as a new scientific result. Runtime-only changes remain metadata drift; any other change requires semantic comparison of the provenance record. This archive is not a scoring standard.",
            "",
            f"<!-- source-drift-json: {json.dumps(drift, ensure_ascii=False, sort_keys=True)} -->",
            "",
        ]
    document_lines = ["Paper/SI document hashes:", ""]
    for document in paper.get("documents", []):
        if document.get("exists"):
            document_lines.append(f"- `{document['path']}` — SHA-256 `{document.get('actual_sha256')}` (declared_match={document.get('hash_match')})")
        else:
            document_lines.append(f"- `{document['path']}` — **not found at audit time**")
    if not paper.get("documents"):
        document_lines.append("- No document manifest entry was recorded in paper_info.json.")
    document_lines.append("")
    lines.extend(document_lines)
    if record["successful_report_evidence_lines"]:
        lines += ["Report evidence lines retained:", ""]
        lines.extend(f"- {item}" for item in record["successful_report_evidence_lines"])
        lines.append("")
    else:
        lines += ["No success-specific report line matched the automatic text pattern; this is not itself an absent-calculation finding. The actual result, ordered steps and artifact anchors below remain the evidence to review.", ""]
    artifact_summary = record.get("artifact_evidence_summary", {})
    lines += [
        "## Provenance anchors for the retained chain",
        "",
        f"- Successful status/output inventory entries: **{artifact_summary.get('count', 0)}**",
        f"- Concrete input anchor present: **{artifact_summary.get('has_concrete_input', False)}**",
        f"- Concrete output/log anchor present: **{artifact_summary.get('has_concrete_output', False)}**",
        "",
        "The following paths are existing files under the historical group record and are hashed for traceability. Failed or explicitly retry-status, migration-interrupted, queued, and running execution directories are excluded; a retry-labelled directory is retained when its status and return code show successful completion.",
        "",
    ]
    for artifact in record.get("successful_artifact_evidence", []):
        lines.append(f"- `{record['group_path']}/{artifact['path']}` — {artifact['role']}; SHA-256 `{artifact['sha256']}`")
    if not record.get("successful_artifact_evidence"):
        lines.append("- No successful execution artifact could be anchored from a status record; treat this archive as evidence-insufficient.")
    lines.append("")
    lines += [
        "## Ordered successful execution steps",
        "",
        "Steps are ordered by the recorded `submitted_at`/`started_at` timestamps. Only status records with successful completion and non-failure status are retained, including successful jobs stored under a retry-labelled path; if the historical records do not contain timestamps, lexical path order is used and this limitation remains explicit.",
        "",
    ]
    if record.get("successful_execution_steps"):
        for index, step in enumerate(record["successful_execution_steps"], 1):
            label = step.get("label") or step.get("job_id") or step.get("status_path")
            details = [f"label={normalize_embedded_paths(label)}"]
            if step.get("submitted_at"):
                details.append(f"submitted_at={step['submitted_at']}")
            if step.get("software_id"):
                details.append(f"software={step['software_id']}")
            if step.get("calculation_intent"):
                details.append(f"intent={step['calculation_intent']}")
            if step.get("route"):
                details.append(f"route={normalize_embedded_paths(step['route'])}")
            if step.get("invocation"):
                details.append(f"command={normalize_embedded_paths(step['invocation'])}")
            lines.append(f"{index}. `{step['status_path']}` — " + "; ".join(details))
            for output in step.get("outputs", []):
                lines.append(f"   - output: `{record['group_path']}/{output}`")
    else:
        lines.append("- No ordered successful status records were found; no complete calculation chain is established.")
    lines.append("")
    lines += [
        "## Evaluator alignment",
        "",
        f"- Key-point IDs: `{', '.join(str(x) for x in eval_audit.get('key_point_ids', []))}`",
        f"- Conclusion IDs: `{', '.join(str(x) for x in eval_audit.get('conclusion_ids', []))}`",
        f"- Scoring-rule IDs: `{', '.join(str(x) for x in eval_audit.get('rule_ids', []))}`",
        f"- Bound result-field status: **{eval_audit.get('structural_field_status', 'NOT_ESTABLISHED')}**",
        f"- Missing bound fields in the archived group result: `{', '.join(eval_audit.get('result_fields_missing', [])) or 'none detected'}`",
        f"- Fields in an inapplicable submission-schema branch (expected for this result status): `{', '.join(eval_audit.get('expected_branch_inapplicable_fields', [])) or 'none detected'}`",
        f"- Submission-schema branch selected for the archived result: `{eval_audit.get('schema_branch', {}).get('matched_branch', 'not established')}`",
        f"- Verification-report status: `{record.get('verification_report_status_raw', 'NOT_RECORDED')}` ({record.get('verification_report_status_class', 'NOT_ESTABLISHED')}); any result/report disagreement requires manual semantic review.",
        "",
        "This field check is structural only. Semantic evaluator agreement is accepted only where the group report and actual result evidence explicitly support it; evaluator target values were never used to fill missing outputs.",
        "",
        "Evaluator rule units/tolerances and result correspondence:",
        "",
    ]
    if eval_audit.get("rule_specs"):
        for spec in eval_audit["rule_specs"]:
            lines.append(
                f"- rule `{spec.get('rule_id')}` → reference `{spec.get('reference_id')}`; type={spec.get('type') or 'not recorded'}; unit={spec.get('unit') or 'not recorded'}; tolerance={spec.get('tolerance') if spec.get('tolerance') is not None else 'not recorded'}; comparison={spec.get('comparison') or 'not recorded'}; evaluator_target_present={spec.get('target_recorded_in_scoring_rules', False)}"
            )
    else:
        lines.append("- No scoring rules were recorded.")
    lines.append("")
    if eval_audit.get("numeric_target_checks"):
        lines.append("Numeric evaluator-target checks (diagnostic only; targets were never inserted into the result):")
        lines.append("")
        for check in eval_audit["numeric_target_checks"]:
            applicability = "not applicable to result branch" if check.get("applicable_to_result_branch") is False else "applicable"
            lines.append(
                f"- rule `{check.get('rule_id')}` / reference `{check.get('reference_id')}`: target={check.get('target')} {check.get('unit') or ''}; tolerance={check.get('tolerance') if check.get('tolerance') is not None else 'not recorded'}; numeric result leaves={json.dumps(check.get('result_numeric_values', []), ensure_ascii=False)}; within_tolerance={check.get('within_tolerance', False)}; applicability={applicability}"
            )
        lines.append("")
    scalar_rows = eval_audit.get("bound_result_scalars", [])
    lines += [
        "Actual result scalars selected by evaluator bindings:",
        "",
        "These values are flattened from the archived group result (not copied from evaluator targets). Failure/retry metadata and large coordinate arrays are omitted; the paths preserve where each reported value came from.",
        "",
    ]
    if scalar_rows:
        for item in scalar_rows:
            encoded = json.dumps(normalize_embedded_paths(item.get("value")), ensure_ascii=False, sort_keys=True)
            lines.append(
                f"- rule `{item.get('rule_id')}` / reference `{item.get('reference_id')}` / field `{item.get('field')}` / result path `{item.get('path')}` = `{encoded[:500]}`"
            )
    else:
        lines.append("- No scalar result values were selected by evaluator bindings; check the missing-field status above.")
    lines.append("")
    historical = record.get("historical_stage08_flag")
    if historical:
        lines += [
            "## Historical final-assembly review flag",
            "",
            f"- Previous assembly decision: **{historical.get('decision', 'not recorded')}**",
            f"- Previous review reason: {historical.get('reason', 'not recorded')}",
            f"- Files changed in that review: `{', '.join(historical.get('changed_files', [])) or 'none recorded'}`",
            f"- Files deleted in that review: `{', '.join(historical.get('deleted_files', [])) or 'none recorded'}`",
            "",
            "This historical flag is retained as a review trail. It is not silently converted to a current PASS; current input/evaluator checks and any required replay remain authoritative.",
            "",
        ]
    lines += [
        "## Agent-visible input identity and boundaries",
        "",
        "Only files under `agent_input/data` are listed here. Hashes establish the exact public input snapshot used by the final package; boundary fields are copied only when explicitly present in the input payload or XYZ comment. Missing fields are reported as not recorded rather than inferred.",
        "",
    ]
    declared_data = input_audit_data.get("declared_data", [])
    if declared_data:
        lines.append("Declared public data:")
        lines.append("")
        for item in declared_data:
            description = item.get("description") or "description not recorded"
            lines.append(f"- `{item.get('path', '')}` — {description}")
        lines.append("")
    if input_audit_data.get("input_files"):
        lines.append("Public input files and hashes:")
        lines.append("")
        for item in input_audit_data["input_files"]:
            details = [
                f"SHA-256 `{item.get('sha256')}`",
                f"size={item.get('size')} bytes",
            ]
            if "xyz_atom_count" in item:
                details.append(f"xyz_atom_count={item['xyz_atom_count']}")
            if item.get("xyz_comment"):
                details.append(f"xyz_comment={item['xyz_comment']}")
            boundary_fields = item.get("boundary_fields", {})
            if boundary_fields:
                encoded = json.dumps(boundary_fields, ensure_ascii=False, sort_keys=True)
                details.append(f"explicit_boundary_fields={encoded[:1200]}")
            else:
                details.append("explicit_boundary_fields=not recorded")
            lines.append(f"- `{item.get('path')}` — " + "; ".join(details))
        lines.append("")
    else:
        lines.append("- No public input files were found under `agent_input/data`.")
        lines.append("")
    lines += [
        "## Input and visibility audit",
        "",
        f"- Declared data missing: `{', '.join(input_audit_data['declared_data_missing']) or 'none'}`",
        f"- JSON/XYZ parse errors: `{', '.join(input_audit_data['json_or_xyz_parse_errors']) or 'none'}`",
        f"- XYZ rows with non-element labels: `{', '.join(input_audit_data.get('xyz_invalid_element_rows', [])) or 'none'}`",
        f"- Absolute agent references: `{', '.join(input_audit_data['absolute_agent_references']) or 'none'}`",
        f"- Potential high-risk data markers: `{', '.join(x['path'] for x in record['leakage_audit']['potential_candidates']) or 'none detected'}`",
        f"- Exact evaluator-target/expected literals in agent-visible files: `{answer_leak_summary}`",
        f"- SI provenance markers requiring semantic review: `{', '.join(x['path'] for x in record['leakage_audit']['si_provenance_reviews']) or 'none'}`",
        "",
        "## Evidence files",
        "",
    ]
    for evidence in record["evidence_files"]:
        if evidence.get("exists", True):
            lines.append(f"- `{evidence['path']}` — {evidence.get('role', 'evidence')}; SHA-256 `{evidence.get('sha256')}`")
        else:
            lines.append(f"- `{evidence['path']}` — **not found at audit time** ({evidence.get('role')})")
    lines += [
        "",
        "## Exclusion policy",
        "",
        record["excluded_from_standard_chain"],
        "",
        "The successful chain archives author-route verification, which may use evaluator-private author endpoints or TS guesses. It does not prove independent discovery from public inputs. A changed public starter alone is not a task/evaluator mismatch under the accepted verification policy; new chemistry, scoring targets or missing essential inputs still require separate review.",
        "",
    ]
    return "\n".join(lines)


def aggregate_report(records: list[dict[str, Any]], generated_at: str, repo: Path | None = None) -> str:
    counts = Counter((record["mode"], record["computation_chain_status"]) for record in records)
    issue_counts = Counter(category for record in records for category in record["issue_categories"])
    autonomous_complete = counts[("autonomous_research", "EVIDENCE_COMPLETE")]
    reproduction_complete = counts[("paper_reproduction", "EVIDENCE_COMPLETE")]
    autonomous_partial = counts[("autonomous_research", "PARTIAL")]
    reproduction_partial = counts[("paper_reproduction", "PARTIAL")]
    autonomous_not_established = counts[("autonomous_research", "NOT_ESTABLISHED")]
    reproduction_not_established = counts[("paper_reproduction", "NOT_ESTABLISHED")]
    lines = [
        "# Final verified task cross-audit and computation archive report",
        "",
        f"Generated: {generated_at}",
        "",
        "本报告索引 final 任务、现有 evaluator 与 `papers/`、`docs/verification/group_1`–`group_6` 的已有证据。脚本不启动科学计算，不因公开 starter 不同要求 replay，也不自动证明作者结论。已知失败状态、非零返回码及明确的末次几何优化失败会从执行候选中排除；其余候选仍需应用层和科学身份检查。成功的 retry-labelled 作业可以保留。",
        "",
        "## Summary",
        "",
        f"- Packages audited: **{len(records)}** (autonomous={sum(r['mode']=='autonomous_research' for r in records)}, reproduction={sum(r['mode']=='paper_reproduction' for r in records)})",
        f"- Evidence-complete archives: autonomous={autonomous_complete}, reproduction={reproduction_complete}",
        f"- Partial archives: autonomous={autonomous_partial}, reproduction={reproduction_partial}",
        f"- Not established: autonomous={autonomous_not_established}, reproduction={reproduction_not_established}",
        "",
        "## Audit interpretation",
        "",
        "本次输出是现有文件的静态/档案检查，不是本次实施了修复、逐篇科学通过或启动了新计算的证明。历史修复和当前具体边界以任务包及人工维护报告为准；不得把硬编码的旧修复清单当作本轮事实。",
        "",
        "作者路线验证允许使用私有端点/TS。公开 starter 不同本身不触发重算要求；原始应用收敛、对象身份和 evaluator 必评结论仍需逐项核对。字段存在、包装器成功以及 EVIDENCE_COMPLETE 标签均不能单独证明科学通过。",
        "",
        "Issue-category counts (static/reported evidence, not new scientific judgments):",
        "",
    ]
    for category, count in sorted(issue_counts.items()):
        lines.append(f"- `{category}`: {count}")
    lines += [
        "",
        "## Per-package audit table",
        "",
        "| mode | paper_id | group | computation chain | current-final applicability | evaluator field check | potential leakage markers | issue categories | record |",
        "|---|---|---|---|---|---|---:|---|---|",
    ]
    for record in records:
        eval_status = record["evaluator_audit"].get("structural_field_status", "NOT_ESTABLISHED")
        leakage_count = len(record["leakage_audit"]["potential_candidates"])
        record_path = f"../../../tasks/final_verified_{record['mode']}/{record['paper_id']}/evaluation/verified_computation_reference.md"
        lines.append(
            f"| {record['mode']} | {record['paper_id']} | {record['group_path'] or '—'} | {record['computation_chain_status']} | {record['current_final_applicability']} | {eval_status} | {leakage_count} | {', '.join(record['issue_categories'])} | [record]({record_path}) |"
        )
    holds = [r for r in records if r.get("historical_stage08_flag") and (r["historical_stage08_flag"].get("decision") not in {None, "EQUIVALENT_SAFE", "SAFE_WITH_SCHEMA_FIX"})]
    if holds:
        lines += ["", "## Historical HOLD/review reasons", "", "| mode | paper_id | previous decision | reason | current applicability |", "|---|---|---|---|---|"]
        for record in holds:
            flag = record["historical_stage08_flag"]
            lines.append(f"| {record['mode']} | {record['paper_id']} | {flag.get('decision', '—')} | {flag.get('reason', 'not recorded')} | {record['current_final_applicability']} |")
    gaps = [r for r in records if r["evaluator_audit"].get("result_fields_missing")]
    if gaps:
        lines += ["", "## Evaluator structural field gaps", "", "These are missing JSON paths in the archived group result, not values filled from evaluator targets; semantic replay is required.", "", "| mode | paper_id | missing fields |", "|---|---|---|"]
        for record in gaps:
            fields = ", ".join(record["evaluator_audit"].get("result_fields_missing", []))
            lines.append(f"| {record['mode']} | {record['paper_id']} | `{fields}` |")
    instruction_rows = [r for r in records if r["instruction_audit"].get("findings")]
    if instruction_rows:
        lines += ["", "## Instruction-boundary findings", "", "| mode | paper_id | findings |", "|---|---|---|"]
        for record in instruction_rows:
            lines.append(f"| {record['mode']} | {record['paper_id']} | `{', '.join(record['instruction_audit']['findings'])}` |")
    leakage_rows = [r for r in records if r["leakage_audit"].get("potential_candidates")]
    if leakage_rows:
        lines += ["", "## Potential geometry/provenance leakage candidates", "", "| mode | paper_id | agent-visible path |", "|---|---|---|"]
        for record in leakage_rows:
            for candidate in record["leakage_audit"]["potential_candidates"]:
                lines.append(f"| {record['mode']} | {record['paper_id']} | `{candidate['path']}` |")
    confirmed_leak_rows = [r for r in records if r["leakage_audit"].get("confirmed_answer_bearing")]
    if confirmed_leak_rows:
        lines += ["", "## Confirmed answer-bearing geometry candidates", "", "These entries are confirmed by the public input/task provenance as SI optimized/final or transition-state geometries. They require removal/redesign only when the geometry is itself an endpoint the agent is expected to discover; a fixed-structure property task may retain a geometry with an explicit non-discovery scope.", "", "| mode | paper_id | agent-visible path | finding |", "|---|---|---|---|"]
        for record in confirmed_leak_rows:
            for candidate in record["leakage_audit"]["confirmed_answer_bearing"]:
                lines.append(f"| {record['mode']} | {record['paper_id']} | `{candidate['path']}` | {candidate['reason']} |")
    value_leak_rows = [r for r in records if r.get("answer_value_leakage")]
    if value_leak_rows:
        lines += ["", "## Potential evaluator-value/expected-text leakage candidates", "", "Exact literal matches are review candidates only; common values may be legitimate boundary constants and are not automatically classified as violations.", "", "| mode | paper_id | agent-visible path | literal |", "|---|---|---|---|"]
        for record in value_leak_rows:
            for candidate in record["answer_value_leakage"]:
                lines.append(f"| {record['mode']} | {record['paper_id']} | `{candidate['path']}` | `{candidate['literal']}` |")
    status_rows = [r for r in records if "VERIFICATION_REPORT_RESULT_STATUS_CONFLICT" in r["issue_categories"] or "VERIFICATION_REPORT_NOT_TERMINAL" in r["issue_categories"]]
    if status_rows:
        lines += ["", "## Verification-report/result status discrepancies", "", "The group report and `report/results.json` are separate records. The report column is the last explicit terminal statement; earlier BLOCKED/CONDITIONAL snapshots are retained in each per-task record. A true final-status discrepancy requires manual reconciliation before treating the chain as a verified evaluator standard.", "", "| mode | paper_id | group-report terminal status | history entries | results.json status |", "|---|---|---|---:|---|"]
        for record in status_rows:
            lines.append(f"| {record['mode']} | {record['paper_id']} | `{record.get('verification_report_status_raw', 'NOT_RECORDED')}` | {len(record.get('verification_report_status_history', []))} | `{record.get('result_status_raw', 'NOT_RECORDED')}` |")
    input_rows = [r for r in records if r["input_audit"].get("xyz_invalid_element_rows") or r["input_audit"].get("declared_data_missing") or r["input_audit"].get("json_or_xyz_parse_errors")]
    if input_rows:
        lines += ["", "## Input-boundary/parse findings", "", "| mode | paper_id | missing data | parse errors | invalid XYZ rows |", "|---|---|---|---|---|"]
        for record in input_rows:
            audit = record["input_audit"]
            lines.append(f"| {record['mode']} | {record['paper_id']} | `{', '.join(audit.get('declared_data_missing', [])) or 'none'}` | `{', '.join(audit.get('json_or_xyz_parse_errors', [])) or 'none'}` | `{', '.join(audit.get('xyz_invalid_element_rows', [])) or 'none'}` |")
    drift_rows = [r for r in records if r.get("source_evidence_drift")]
    if drift_rows:
        lines += ["", "## Source-evidence drift since the previous archive", "", "| mode | paper_id | classification | changed result fields | changed artifact paths | previous results SHA-256 | current results SHA-256 |", "|---|---|---|---|---|---|---|"]
        for record in drift_rows:
            drift = record["source_evidence_drift"]
            lines.append(f"| {record['mode']} | {record['paper_id']} | {drift.get('classification', 'REVIEW')} | `{', '.join(drift.get('changed_top_level_keys', [])) or 'not established'}` | `{', '.join(drift.get('changed_artifact_paths', [])) or 'none'}` | `{drift.get('previous_sha256', '—')}` | `{drift.get('current_sha256', '—')}` |")
    lines += [
        "",
        "## Current-final replay gate",
        "",
        "Public-starter changes are tracked separately from the historical author-route archive. Their platform/application state is read-only evidence; a changed starter is not promoted to current-final applicability until the relevant terminal calculation, validation diagnostics, and starter-to-endpoint identity checks are complete. This does not invalidate the author-route provenance or alter evaluator targets.",
        "",
    ]
    replay_status_path = ((repo or Path.cwd()) / "docs" / "verification" / "current_final_replays" / "replay_status.json")
    if replay_status_path.is_file():
        try:
            replay_payload = json.loads(replay_status_path.read_text(encoding="utf-8"))
            lines += ["| paper_id | job | platform status | group | priority | scientific gate |", "|---|---|---|---|---|---|"]
            for row in replay_payload.get("records", []):
                platform = row.get("platform") or {}
                lines.append(f"| {row.get('paper_id')} | `{platform.get('job_id', '—')}` | `{platform.get('status', '—')}` | `{platform.get('compute_group', '—')}` | `{platform.get('priority_name', '—')}` | `{row.get('scientific_status', '—')}` |")
        except (OSError, json.JSONDecodeError):
            lines.append("Replay status file exists but could not be parsed at report time.")
    else:
        lines.append("No current-final replay status snapshot is present.")
    lines += [
        "",
        "## Interpretation and limitations",
        "",
        "1. `EVIDENCE_COMPLETE` means that the existing group result has a success-like status, a method/protocol section, validation/result objects, and linked verification records (or, for the analytic nanoscroll task, the two durable continuum artifacts and explicit mathematical checks). It is an archive-completeness label, not the benchmark's scoring decision.",
        "2. `PARTIAL` or `NOT_ESTABLISHED` archives retain only confirmed successful portions or no chain, respectively. They must not be used as a complete evaluator standard.",
        "3. A potential leakage marker is a review candidate. Fixed-structure property inputs and explicitly labeled unverified starting candidates require semantic interpretation; filename/comment changes alone are not a clearance.",
        "4. Evaluator field coverage is a structural JSON-path check. It does not replace expert semantic comparison of key points, conclusions, tolerances, or method equivalence.",
        "5. The current final snapshot contains public-input changes for `paper_0de37d01e35c27df`, `paper_3a22e838133b906d`, `paper_0dc85595cab7bc0a`, `paper_221aafe4bd916a11`, `paper_430b9cbe83c2c203`, `paper_9d091f4337662e78` and `paper_e2d9397dff2a3f0f`; their original group chains remain archived as author-route evidence. For the displaced-starter cases the archive explicitly does not claim an independent public-starter replay; this is a scope annotation, not a scientific-objective failure. The approved TS-coordinate removal remains covered by the strict-v2 author-route evidence.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--write", action="store_true", help="write per-task records and aggregate report")
    parser.add_argument("--paper", action="append", help="exact paper_id; repeat to select multiple papers")
    parser.add_argument("--mode", action="append", choices=MODES, help="limit to explicit modes")
    parser.add_argument("--overwrite-references", action="store_true", help="explicitly replace selected existing references after review; never implied by --write")
    args = parser.parse_args()
    repo = args.repo.resolve()
    records: list[dict[str, Any]] = []
    if args.write and not args.paper:
        parser.error("--write requires explicit --paper selection; do not mass-overwrite curated references")
    for mode in args.mode or MODES:
        root = repo / "tasks" / f"final_verified_{mode}"
        for package in sorted(path for path in root.glob("paper_*") if path.is_dir()):
            if args.paper and package.name not in args.paper:
                continue
            reference_path = package / "evaluation" / "verified_computation_reference.md"
            if args.write and reference_path.exists() and not args.overwrite_references:
                parser.error(f"existing reference preserved: {reference_path}; preview and review before --overwrite-references")
            records.append(build_record(repo, mode, package))
    generated_at = datetime.now(timezone.utc).isoformat()
    aggregate = aggregate_report(records, generated_at, repo)
    if args.write:
        for record in records:
            path = repo / "tasks" / f"final_verified_{record['mode']}" / record["paper_id"] / "evaluation" / "verified_computation_reference.md"
            path.write_text(markdown_record(record), encoding="utf-8")
        # A selected-paper update must not replace the full scientific report
        # or index with an incomplete, automatically generated assessment.
        print(aggregate)
    else:
        print(aggregate)
    print(json.dumps({"records": len(records), "write": args.write}, ensure_ascii=False))


if __name__ == "__main__":
    main()
