"""Read-only native error excerpts with real source positions, never repairs."""
from __future__ import annotations

import re
from pathlib import Path


_SIGNATURES = (
    ("input_read_error", "invalid_input", r"End of file in ZSymb|QPErr|Error reading|input error|unrecognized.*keyword|Unrecognized symbol"),
    ("nonconvergence", "numerical_nonconvergence", r"SCF (?:NOT CONVERGED|failed to converge)|convergence failure|\.sccnotconverged"),
    ("native_error", "software_error", r"Error termination|ORCA finished by error|ERROR:|segmentation fault|fatal error"),
)


def native_diagnostic(paths, *, root: Path, software_id: str = "unknown", fallback=None):
    evidence, matches = [], []
    for raw_path in paths:
        path = Path(raw_path)
        if not path.is_file() or not path.resolve().is_relative_to(root.resolve()):
            continue
        relative = str(path.relative_to(root))
        evidence.append({"path": relative})
        with path.open(errors="replace") as stream:
            for line_no, line in enumerate(stream, 1):
                for priority, (code, category, pattern) in enumerate(_SIGNATURES):
                    if re.search(pattern, line, re.I):
                        matches.append((priority, code, category, {"path": relative,
                            "line_start": line_no, "line_end": line_no, "excerpt": line.strip()[:1200]}))
                        matches.sort(key=lambda item: item[0])
                        del matches[16:]
                        break
        # Only diagnostic excerpts are kept in memory, never an entire large log.
    if matches:
        matches.sort(key=lambda item: item[0])
        _, code, category, primary = matches[0]
        return {"code": code, "category": category, "message": primary["excerpt"],
                "stage": "software_execution", "origin": "native_output", "software_id": software_id,
                "evidence": [m[3] for m in matches[:4]] + evidence}
    if fallback:
        return {**fallback, "stage": "process", "origin": "supervisor", "evidence": evidence}
    return None
