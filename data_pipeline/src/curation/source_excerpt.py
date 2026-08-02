from __future__ import annotations

import re
from pathlib import Path

SECTION_PATTERNS = (
    r"computational methods?",
    r"computational details?",
    r"theoretical methods?",
    r"materials? and methods?",
    r"methodology",
    r"results? and discussion",
    r"mechanis(?:m|tic)",
    r"reaction pathway",
    r"transition state",
    r"free energ",
    r"data availability",
    r"code availability",
    r"supporting information",
    r"conclusions?",
    r"limitations?",
)


def evidence_excerpt(paths: list[str], max_chars: int) -> str:
    existing = [Path(raw) for raw in paths if Path(raw).is_file()]
    if not existing or max_chars <= 0:
        return ""
    share = max(4_000, max_chars // len(existing))
    chunks = []
    remaining = max_chars
    for path in existing:
        if remaining <= 0:
            break
        text = path.read_text(encoding="utf-8", errors="replace")
        excerpt = compact_evidence_text(text, min(share, remaining))
        chunks.append(f"SOURCE_FILE: {path.name}\n{excerpt}")
        remaining -= len(chunks[-1])
    return "\n\n".join(chunks)[:max_chars]


def compact_evidence_text(text: str, budget: int) -> str:
    text = re.sub(r"\x00", "", text)
    if len(text) <= budget:
        return text
    windows: list[tuple[int, int]] = []
    head = max(2_000, budget // 5)
    tail = max(1_000, budget // 10)
    windows.extend([(0, head), (max(0, len(text) - tail), len(text))])
    window_size = max(1_200, min(3_000, budget // 12))
    for pattern in SECTION_PATTERNS:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            start = max(0, match.start() - window_size // 4)
            windows.append((start, min(len(text), start + window_size)))
            if len(windows) >= 24:
                break
        if len(windows) >= 24:
            break
    merged: list[tuple[int, int]] = []
    for start, end in sorted(windows):
        if merged and start <= merged[-1][1] + 200:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))
    output = []
    used = 0
    for start, end in merged:
        chunk = text[start:end].strip()
        if not chunk:
            continue
        allowed = budget - used
        if allowed <= 0:
            break
        output.append(f"[char {start}:{min(end, start + allowed)}]\n{chunk[:allowed]}")
        used += len(output[-1])
    return "\n\n".join(output)[:budget]
