#!/usr/bin/env python3
"""Generate portable metadata for MiniChem software, environment, and model payloads."""

from __future__ import annotations

import hashlib
import importlib
import importlib.metadata
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOFTWARE_CACHE = ROOT / ".mini_software_cache"
ENV_ROOT = ROOT / ".envs"
MODEL_CACHE = ROOT / ".mini_model_cache"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, base: Path) -> dict[str, object]:
    return {
        "path": path.relative_to(base).as_posix(),
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def directory_size(path: Path) -> int:
    completed = subprocess.run(
        ["du", "-sb", str(path)], check=True, text=True, capture_output=True
    )
    return int(completed.stdout.split()[0])


def package_versions() -> dict[str, str]:
    names = (
        "ase",
        "cclib",
        "fastmcp",
        "goodvibes",
        "jax",
        "mcp",
        "numpy",
        "onnxruntime",
        "pysisyphus",
        "qcelemental",
        "rdkit",
        "scipy",
        "sella",
        "tokenizers",
    )
    result: dict[str, str] = {}
    for name in names:
        try:
            version = importlib.metadata.version(name)
            if version == "0.0.0":
                version = str(getattr(importlib.import_module(name), "__version__", version))
            result[name] = version
        except importlib.metadata.PackageNotFoundError:
            result[name] = "not-installed"
    return result


def write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    gaussian = SOFTWARE_CACHE / "gaussian" / "g16" / "install" / "g16"
    multiwfn = (
        SOFTWARE_CACHE
        / "multiwfn"
        / "2026.7.15"
        / "Multiwfn_2026.7.15_bin_Linux_noGUI"
    )
    runtime = ENV_ROOT / "minichem"
    software_files = [gaussian / "g16", gaussian / "formchk", multiwfn / "Multiwfn_noGUI"]
    missing = [path for path in software_files if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing software cache files: " + ", ".join(map(str, missing)))
    components: dict[str, object] = {
        "gaussian_16_c01": {
            "license": "commercial; redistribution is not permitted by MiniChem",
            "size_bytes": directory_size(SOFTWARE_CACHE / "gaussian"),
            "files": [file_record(path, SOFTWARE_CACHE) for path in software_files[:2]],
        },
        "multiwfn_2026_7_15": {
            "license": "upstream Multiwfn terms and citation requirements apply",
            "size_bytes": directory_size(SOFTWARE_CACHE / "multiwfn"),
            "files": [file_record(software_files[2], SOFTWARE_CACHE)],
        },
    }
    write(
        SOFTWARE_CACHE / "manifest.json",
        {
            "schema_version": 1,
            "portable_root": ".mini_software_cache",
            "components": components,
        },
    )

    environment_components: dict[str, object] = {
        "minichem_runtime": {
            "path": "minichem",
            "size_bytes": directory_size(runtime),
            "python": "3.11",
            "package_versions": package_versions(),
        }
    }
    runtime_pack = ENV_ROOT / "runtime_packs" / "minichem.tar.gz"
    if runtime_pack.is_file():
        environment_components["runtime_pack"] = file_record(runtime_pack, ENV_ROOT)
    write(
        ENV_ROOT / "manifest.json",
        {
            "schema_version": 1,
            "portable_root": ".envs",
            "components": environment_components,
        },
    )

    model_files = sorted(
        path
        for path in MODEL_CACHE.rglob("*")
        if path.is_file() and path.name not in {"manifest.json", "*.lock"} and not path.name.endswith(".lock")
    )
    write(
        MODEL_CACHE / "manifest.json",
        {
            "schema_version": 1,
            "portable_root": ".mini_model_cache",
            "source_model": "sentence-transformers/all-MiniLM-L6-v2",
            "purpose": "optional offline semantic recall for Actions and software documentation",
            "files": [file_record(path, MODEL_CACHE) for path in model_files],
        },
    )


if __name__ == "__main__":
    main()
