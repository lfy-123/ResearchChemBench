#!/usr/bin/env python3
"""Normalize final task.md files using verified science and Stage08 layout.

The verified package supplies the scientific sections.  Stage08 is used only
for the reproduction-mode author-guidance section and for optional completion
sections.  This script deliberately does not touch input files, schemas,
evaluators, manifests, or paper routes.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

STANDARD = {
    "scientific objective": "Scientific objective",
    "public inputs and scientific boundaries": "Public inputs and scientific boundaries",
    "required scientific validation/investigation": "Required scientific validation/investigation",
    "deliverables": "Deliverables",
    "author-provided scientific guidance": "Author-provided scientific guidance",
}

AUTONOMOUS_BOUNDARY = (
    "This is an autonomous-research task. Do not use the paper, SI, author route, "
    "candidate ranking, optimized/final structure, transition-state or product "
    "coordinates, hidden reference values, or evaluator conclusions as input. "
    "Generate and validate the scientific candidates independently within the "
    "public boundary."
)


def parse_sections(text: str) -> list[tuple[str, str, int]]:
    """Return (normalized title, body, original heading level) in source order."""
    lines = text.splitlines()
    sections: list[tuple[str, str, int]] = []
    current_title: str | None = None
    current_level = 1
    body: list[str] = []
    heading = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

    def flush() -> None:
        nonlocal current_title, body, current_level
        if current_title is not None:
            sections.append((current_title, "\n".join(body).strip(), current_level))
        body = []

    for line in lines:
        match = heading.match(line)
        if match:
            flush()
            current_level = len(match.group(1))
            raw = match.group(2).strip()
            key = raw.casefold()
            current_title = STANDARD.get(key, raw)
        elif current_title is not None:
            body.append(line)
    flush()
    return sections


def section_map(sections: list[tuple[str, str, int]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for title, body, _level in sections:
        result.setdefault(title, body)
    return result


def collapse_adjacent_duplicate_lines(body: str) -> str:
    lines = body.splitlines()
    out: list[str] = []
    for line in lines:
        if out and line.strip() and line.strip() == out[-1].strip():
            continue
        out.append(line)
    return "\n".join(out).strip()


def sanitize_author_guidance(guidance: str) -> str:
    """Keep Stage08 guidance qualitative without re-introducing answer geometry.

    Stage08 was written before the input-boundary audit and one of its
    reproduction prompts describes the author's optimized TS as a supplied
    target.  Reproduction guidance may describe a route, but it must never
    turn a private endpoint into an agent-visible input.  Apply narrowly scoped
    wording repairs here so a future normalization run cannot undo the repair.
    """
    replacements = (
        (r"\bsupplied\s+singlet\s+target\s+saddle\b", "independently generated singlet candidate saddle"),
        (r"\bsupplied\s+target\s+saddle\b", "independently generated candidate saddle"),
        (r"\bfixed\s+structures\b", "reference and independently generated candidate"),
        (r"\btarget\.xyz\b", "the independently generated transition-state candidate"),
    )
    result = guidance
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


def normalize(verified: str, stage08: str | None, mode: str) -> str:
    v_sections = parse_sections(verified)
    v_map = section_map(v_sections)
    s_sections = parse_sections(stage08 or "")
    s_map = section_map(s_sections)

    required = [
        "Scientific objective",
        "Public inputs and scientific boundaries",
        "Required scientific validation/investigation",
        "Deliverables",
    ]
    missing = [title for title in required if title not in v_map]
    if missing:
        raise ValueError(f"verified task is missing sections: {missing}")

    chunks: list[str] = []
    chunks.append(f"# Scientific objective\n\n{collapse_adjacent_duplicate_lines(v_map['Scientific objective'])}")

    if mode == "paper_reproduction":
        guidance = s_map.get("Author-provided scientific guidance", "").strip()
        if not guidance:
            guidance = (
                "Use the author's qualitative hypothesis and computational route as a "
                "testable starting point only. Reproduce the stated sequence of model "
                "construction, calculation and validation, but generate and validate "
                "all structures and numerical results independently. Author final "
                "structures, transition states, energies, rankings and evaluator "
                "answers are not public inputs."
            )
        guidance = sanitize_author_guidance(guidance)
        chunks.append(f"# Author-provided scientific guidance\n\n{guidance}")

    boundary = collapse_adjacent_duplicate_lines(v_map["Public inputs and scientific boundaries"])
    if mode == "autonomous_research":
        # Normalize equivalent legacy labels to one explicit mode marker.  A
        # broad phrase search is insufficient here: some old tasks said only
        # “autonomous track” while omitting the concrete no-paper/no-answer
        # boundary.  Keep the scientific prose and add the canonical boundary
        # only when the full marker is absent.
        boundary = re.sub(
            r"This is (?:an )?autonomous-research (?:track|task)\.",
            "This is an autonomous-research task.",
            boundary,
            flags=re.I,
        )
        if "This is an autonomous-research task." not in boundary:
            boundary = f"{boundary}\n\n{AUTONOMOUS_BOUNDARY}"
    chunks.append(f"# Public inputs and scientific boundaries\n\n{boundary}")
    chunks.append(
        "# Required scientific validation/investigation\n\n"
        + collapse_adjacent_duplicate_lines(v_map["Required scientific validation/investigation"])
    )

    # Preserve task-specific completion/failure contracts from Stage08 without
    # allowing them to replace verified scientific sections.
    standard_titles = set(required) | {"Author-provided scientific guidance"}
    for title, body, _level in s_sections:
        if title in standard_titles or not body.strip():
            continue
        chunks.append(f"# {title}\n\n{body.strip()}")

    chunks.append(f"# Deliverables\n\n{collapse_adjacent_duplicate_lines(v_map['Deliverables'])}")
    return "\n\n".join(chunks).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verified-root", type=Path, default=Path("tasks"))
    parser.add_argument("--stage08-root", type=Path, default=Path("tasks/stage08_tasks_extracted/tasks"))
    parser.add_argument("--final-root", type=Path, default=Path("tasks"))
    parser.add_argument("--mode", choices=("autonomous_research", "paper_reproduction"), action="append")
    args = parser.parse_args()
    modes = args.mode or ["autonomous_research", "paper_reproduction"]
    changed = 0
    for mode in modes:
        v_root = args.verified_root / f"verified_{mode}"
        s_root = args.stage08_root / mode
        f_root = args.final_root / f"final_verified_{mode}"
        # The verified source directories are intentionally retired after a
        # final snapshot is cut.  In that state, normalize the current final
        # package in place rather than silently doing zero work; the final
        # package is already the verified scientific snapshot at this stage.
        source_root = v_root if v_root.is_dir() else f_root
        for v_pkg in sorted(source_root.glob("paper_*")):
            v_task = v_pkg / "agent_input" / "task.md"
            if not v_task.is_file():
                raise FileNotFoundError(v_task)
            s_task = s_root / v_pkg.name / "agent_input" / "task.md"
            f_task = f_root / v_pkg.name / "agent_input" / "task.md"
            if not f_task.parent.is_dir():
                raise FileNotFoundError(f_task.parent)
            normalized = normalize(
                v_task.read_text(encoding="utf-8"),
                s_task.read_text(encoding="utf-8") if s_task.is_file() else None,
                mode,
            )
            if f_task.read_text(encoding="utf-8") != normalized:
                f_task.write_text(normalized, encoding="utf-8")
                changed += 1
    print(f"normalized task.md files: {changed}")


if __name__ == "__main__":
    main()
