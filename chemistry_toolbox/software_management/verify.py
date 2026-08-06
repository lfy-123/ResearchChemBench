"""Structural and command-level verification for managed installations."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

from .models import SoftwareManifest
from .paths import within


def verify_manifest(root: Path, manifest: SoftwareManifest) -> dict[str, Any]:
    installation = within(root, manifest.installation_path, field="installation target")
    entrypoints: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    if manifest.installation_required and not installation.is_dir():
        errors.append(f"Missing installation: {installation.relative_to(root)}")
    for name, relative in manifest.entrypoints.items():
        path = installation / relative
        record = {
            "path": str(path.relative_to(root)),
            "exists": path.is_file(),
            "executable": path.is_file() and os.access(path, os.X_OK),
        }
        entrypoints[name] = record
        if not record["exists"]:
            errors.append(f"Missing entrypoint {name}: {record['path']}")
        elif not record["executable"]:
            errors.append(f"Entrypoint is not executable {name}: {record['path']}")

    probes: list[dict[str, Any]] = []
    if not errors:
        for specification in manifest.verification:
            command = [str(item) for item in specification.get("command") or []]
            if not command:
                continue
            for index, token in enumerate(command):
                if token.startswith("{entrypoint:") and token.endswith("}"):
                    name = token[len("{entrypoint:") : -1]
                    if name not in manifest.entrypoints:
                        raise ValueError(f"Unknown entrypoint in verification: {name}")
                    command[index] = str(installation / manifest.entrypoints[name])
            accepted = {int(item) for item in specification.get("accepted_returncodes", [0])}
            timeout = int(specification.get("timeout", 60))
            completed = subprocess.run(
                command,
                cwd=installation,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=timeout,
                check=False,
            )
            output = completed.stdout[-4000:]
            expected = str(specification.get("output_contains") or "")
            ok = completed.returncode in accepted and (not expected or expected in completed.stdout)
            probes.append(
                {
                    "command": command,
                    "returncode": completed.returncode,
                    "output_tail": output,
                    "ok": ok,
                }
            )
            if not ok:
                errors.append(f"Verification command failed: {command}")
    return {
        "software_id": manifest.software_id,
        "version": manifest.version,
        "installation": str(installation.relative_to(root)),
        "entrypoints": entrypoints,
        "probes": probes,
        "status": "pass" if not errors else "fail",
        "errors": errors,
    }
