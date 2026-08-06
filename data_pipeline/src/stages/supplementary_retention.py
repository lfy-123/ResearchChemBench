from __future__ import annotations

from pathlib import Path
from typing import Any


def supplementary_retention(paper: dict[str, Any]) -> dict[str, Any]:
    """Apply the intentionally simple SI retention rule used by Stages 05/06."""
    if paper.get("has_local_supplementary") or paper.get("supplementary_documents"):
        return {"keep": True, "decision": "supplementary_available", "reason": "local_supplementary"}

    acquisition = paper.get("supplementary_acquisition") or {}
    attachments = acquisition.get("attachments") or []
    downloaded = [
        item
        for item in attachments
        if item.get("path") and Path(str(item["path"])).is_file()
    ]
    if downloaded:
        return {
            "keep": True,
            "decision": "supplementary_available",
            "reason": "publisher_supplementary_downloaded",
        }

    if acquisition.get("presence_status") == "absent_confirmed":
        return {
            "keep": True,
            "decision": "no_supplementary_confirmed",
            "reason": "publisher_absence_confirmed",
        }

    return {
        "keep": False,
        "decision": "supplementary_unavailable",
        "reason": "supplementary_not_confirmed_absent_or_downloaded",
    }
