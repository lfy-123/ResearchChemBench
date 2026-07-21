"""Portable ChemGraph discovery and MCP runtime settings."""

from __future__ import annotations

import os
import sys
from pathlib import Path


CHEMGRAPH_ROOT_ENV = "CHEMGRAPH_ROOT"


def _as_chemgraph_root(path: Path) -> Path | None:
    candidate = path.expanduser().resolve()
    if (candidate / "src" / "chemgraph").is_dir():
        return candidate
    if candidate.name == "src" and (candidate / "chemgraph").is_dir():
        return candidate.parent
    return None


def chemgraph_root() -> Path:
    """Locate a ChemGraph checkout without depending on ResearchChemBench."""

    configured = os.environ.get(CHEMGRAPH_ROOT_ENV, "").strip()
    if configured:
        root = _as_chemgraph_root(Path(configured))
        if root is None:
            raise RuntimeError(
                f"{CHEMGRAPH_ROOT_ENV} does not contain src/chemgraph: {configured}"
            )
        return root

    search_bases = [Path.cwd(), *Path.cwd().parents]
    module_path = Path(__file__).resolve()
    search_bases.extend(module_path.parents)
    seen: set[Path] = set()
    for base in search_bases:
        for candidate in (base, base / "ChemGraph"):
            resolved = candidate.resolve()
            if resolved in seen:
                continue
            seen.add(resolved)
            root = _as_chemgraph_root(resolved)
            if root is not None:
                return root

    raise RuntimeError(
        "ChemGraph was not found. Set CHEMGRAPH_ROOT to a checkout containing "
        "src/chemgraph before starting the MCP server."
    )


def chemgraph_src() -> Path:
    return chemgraph_root() / "src"


def ensure_chemgraph_on_path() -> Path:
    """Add ChemGraph source to sys.path and return the source directory."""

    source = chemgraph_src()
    source_text = str(source)
    if source_text not in sys.path:
        sys.path.insert(0, source_text)
    return source

