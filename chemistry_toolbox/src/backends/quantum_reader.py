"""Shared, explicit reader for saved quantum chemistry output."""
from pathlib import Path
from typing import Any
import traceback

from .common import relative_workspace_path


def read_quantum_output(source: Path) -> tuple[Any, dict[str, Any]]:
    from cclib.io import ccopen
    from cclib.parser.orcaparser import ORCA
    from .orca_parser import CompatibleORCA

    parser = None
    details: dict[str, Any] = {}
    try:
        parser = ccopen(str(source), loglevel=40)
        if parser is None:
            raise RuntimeError("cclib did not recognize the supplied quantum-chemistry output")
        if isinstance(parser, ORCA):
            parser = CompatibleORCA(parser.inputfile, loglevel=40)
        details["parser_class"] = type(parser).__name__
        parsed = parser.parse()
        details.update({
            "diagnostics": getattr(parser, "diagnostics", []),
            "incomplete_properties": sorted(getattr(parser, "incomplete_properties", ())),
            "property_sources": getattr(parser, "property_sources", {}),
            "source_termination": getattr(parser, "source_termination",
                "normal" if parsed.metadata.get("success") else "not_observed"),
        })
        return parsed, details
    except Exception as exc:
        reader = getattr(parser, "inputfile", None)
        try:
            source_path = relative_workspace_path(source)
        except (ValueError, RuntimeError):
            source_path = str(source.resolve())
        details["error"] = {
            "category": "output_parsing", "failure_stage": "output_parsing",
            "source_path": source_path,
            "parser_class": type(parser).__name__ if parser else "unrecognized",
            "section": getattr(parser, "section", "cclib parsing"),
            "line_number": getattr(reader, "line_number", None),
            "line_preview": getattr(reader, "last_line", "").strip()[:400],
            "exception_type": type(exc).__name__, "reason": str(exc),
            "traceback": traceback.format_exc(),
        }
        return None, details
    finally:
        if parser is not None:
            parser.inputfile.close()
