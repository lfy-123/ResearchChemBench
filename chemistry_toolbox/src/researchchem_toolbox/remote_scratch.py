"""Per-job worker-local scratch isolation for distributed executions."""

from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path
from typing import MutableMapping


REMOTE_SCRATCH_ROOT_ENV = "RCB_DISTRIBUTED_REMOTE_SCRATCH_ROOT"
DEFAULT_REMOTE_SCRATCH_ROOT = Path("/tmp/researchchembench")


def prepare_remote_scratch(
    environment: MutableMapping[str, str], *, job_token: str
) -> Path:
    """Create one private scratch tree and update the child environment."""

    configured = str(environment.get(REMOTE_SCRATCH_ROOT_ENV) or "").strip()
    root = Path(configured).expanduser() if configured else DEFAULT_REMOTE_SCRATCH_ROOT
    if not root.is_absolute():
        raise ValueError(f"{REMOTE_SCRATCH_ROOT_ENV} must be an absolute path")
    root.mkdir(parents=True, exist_ok=True)
    safe_token = re.sub(r"[^A-Za-z0-9_.-]+", "-", job_token).strip("-._")
    prefix = f"rcb-{safe_token[:48]}-" if safe_token else "rcb-job-"
    scratch = Path(tempfile.mkdtemp(prefix=prefix, dir=root))
    for name in ("TMPDIR", "TMP", "TEMP"):
        environment[name] = str(scratch)
    if environment.get("GAUSS_SCRDIR"):
        gaussian_scratch = scratch / "gaussian"
        gaussian_scratch.mkdir(mode=0o700)
        environment["GAUSS_SCRDIR"] = str(gaussian_scratch)
    environment["RESEARCHCHEM_DISTRIBUTED_SCRATCH_ISOLATION"] = (
        "worker_local_ephemeral"
    )
    return scratch


def cleanup_remote_scratch(path: Path | None) -> None:
    if path is not None:
        shutil.rmtree(path, ignore_errors=True)


__all__ = [
    "DEFAULT_REMOTE_SCRATCH_ROOT",
    "REMOTE_SCRATCH_ROOT_ENV",
    "cleanup_remote_scratch",
    "prepare_remote_scratch",
]
