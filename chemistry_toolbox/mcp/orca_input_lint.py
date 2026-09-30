"""Bounded ORCA grammar checks, independent of any scientific task.

Coordinate forms follow the ORCA 6.1 manual, Essential Elements / Coordinates.
Uncovered syntax is reported as incomplete lint coverage, not a syntax error.
"""
from __future__ import annotations

import re
import shlex
from pathlib import PurePosixPath


_COMMENTS = re.compile(r'''("(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\#.*$)''')
_BLOCKS = {"basis", "casscf", "coords", "cpcm", "elprop", "freq", "geom", "mdci",
           "method", "output", "pal", "plots", "rel", "scf", "tddft", "neb"}
_SUBBLOCKS = {"coords", "pardef", "constraints", "scan", "modify_internal"}
_INLINE = {"xyz", "int", "internal", "gzmt"}
_EXTERNAL = {"xyzfile", "gzmtfile"}


def lint_orca_input(text, *, staged_targets, cpu_cores, memory_mb):
    lines = [_COMMENTS.sub(lambda m: "" if m[0].startswith("#") else m[0], line).strip()
             for line in text.splitlines()]
    if not any(lines):
        raise ValueError("orca_empty_input: input contains no instructions")
    segments = [[]]
    for number, line in enumerate(lines, 1):
        if re.fullmatch(r"\$(?:new_job|newjob)", line, re.I):
            segments.append([])
        else:
            segments[-1].append((number, line))
    sections, warnings, keyword_lines = [], [], []
    for segment_number, segment in enumerate(segments, 1):
        stack = []
        for number, line in segment:
            if line.startswith("!"):
                keyword_lines.append(line)
            match = re.match(r"^%([a-z0-9_]+)\b(.*)$", line, re.I)
            if match and match[1].casefold() in _BLOCKS:
                stack.append((match[1].casefold(), number))
                line = match[2].strip()
            elif match and match[1].casefold() not in {"maxcore", "base", "moinp"}:
                warnings.append(f"line {number}: %{match[1]} block syntax not covered")
            elif stack and line.split() and line.split()[0].casefold() in _SUBBLOCKS:
                stack.append((line.split()[0].casefold(), number))
            for _ in re.findall(r"\bend\b", line, re.I):
                if stack:
                    stack.pop()
        if stack:
            name, number = stack[-1]
            raise ValueError(f"orca_unclosed_block: %{name} opened on line {number} has no matching end in job {segment_number}")

        inline = None
        for number, line in segment:
            if not line:
                continue
            if inline:
                if line == "*":
                    inline = None
                    continue
                if line.startswith(("*", "%", "!")):
                    raise ValueError(f"orca_unclosed_coordinates: coordinate section on line {inline} has no final '*'")
                continue
            if not line.startswith("*") or line == "*":
                continue
            tokens = shlex.split(line)
            kind = tokens[1].casefold() if len(tokens) > 1 else ""
            if kind not in _INLINE | _EXTERNAL:
                warnings.append(f"line {number}: coordinate syntax {kind!r} not covered")
                continue
            if len(tokens) < 4 or not re.fullmatch(r"[+-]?\d+", tokens[2]) or not re.fullmatch(r"[1-9]\d*", tokens[3]):
                raise ValueError(f"orca_coordinate_header: line {number} requires charge and positive multiplicity")
            record = {"job": segment_number, "line": number, "kind": kind}
            if kind in _INLINE:
                if len(tokens) != 4:
                    raise ValueError(f"orca_coordinate_header: unexpected fields on line {number}")
                inline = number
            else:
                if len(tokens) == 4 and segment_number > 1:
                    record["source"] = "previous_job"
                elif len(tokens) == 5:
                    path = PurePosixPath(tokens[4])
                    if path.is_absolute() or ".." in path.parts:
                        raise ValueError(f"orca_geometry_path: external coordinates must remain inside job: {tokens[4]}")
                    if str(path) not in staged_targets:
                        raise ValueError(f"orca_missing_geometry: {tokens[4]!r} is absent from staged_inputs")
                    record["target"] = str(path)
                else:
                    raise ValueError(f"orca_coordinate_header: external coordinates on line {number} require a filename (or a preceding job)")
                if number == len(lines) and not text.endswith(("\n", "\r")):
                    raise ValueError("orca_coordinate_newline: external coordinate line requires a final newline")
            sections.append(record)
        if inline:
            raise ValueError(f"orca_unclosed_coordinates: coordinate section on line {inline} has no final '*' in job {segment_number}")

        segment_text = "\n".join(line for _, line in segment)
        nprocs = [int(value) for block in re.findall(r"%pal\b(.*?)\bend\b", segment_text, re.I | re.S)
                  for value in re.findall(r"\bnprocs\s+(\d+)", block, re.I)]
        nprocs += [int(value) for _, line in segment if line.startswith("!")
                   for value in re.findall(r"\bpal(\d+)\b", line, re.I)]
        if any(count > cpu_cores or count < 1 for count in nprocs):
            raise ValueError("orca_cpu_mismatch: requested ORCA parallelism exceeds resource_limits.cpu_cores")
        maxcore = [float(value) for value in re.findall(r"%maxcore\s+(\d+(?:\.\d+)?)", segment_text, re.I)]
        if any(value * max(nprocs, default=1) > memory_mb for value in maxcore):
            raise ValueError("orca_memory_mismatch: %maxcore times nprocs exceeds resource_limits.memory_mb")

    keywords = " ".join(keyword_lines)
    frequency = bool(re.search(r"\b(?:freq|numfreq|anfreq)\b", keywords, re.I))
    ts = bool(re.search(r"\boptts\b", keywords, re.I))
    opt = ts or bool(re.search(r"\bopt\b", keywords, re.I))
    intent = ("transition_state" if ts else "optimization_frequency" if opt and frequency else
              "geometry_optimization" if opt else "frequency" if frequency else "single_point")
    if not keyword_lines:
        warnings.append("Keyword-based calculation intent is not covered; supply calculation_intent explicitly")
        intent = None
    return {"lint_profile": "orca_high_frequency_v2", "keyword_line": keywords,
            "calculation_intent": intent, "coordinate_section_count": len(sections),
            "coordinate_sections": sections, "job_segment_count": len(segments),
            "warnings": warnings, "coverage": "partial" if warnings else "supported_subset",
            "checks": ["block_closure", "coordinate_closure", "external_geometry_staging", "cpu_mapping", "memory_mapping"]}
