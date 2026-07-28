#!/usr/bin/env python3
"""Cache the pinned quantized MiniLM model and Action catalog embeddings."""

from __future__ import annotations

import hashlib
import sys
import urllib.request
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, TOOLBOX_ROOT.parent):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from researchchem_toolbox.catalog import action_specs, backend_specs
from researchchem_toolbox.discovery import _action_search_documents
from researchchem_toolbox.semantic_embeddings import (
    MODEL_ID,
    MODEL_REVISION,
    model_directory,
    write_embedding_cache,
)
from chemistry_toolbox.mcp.software_catalog import (
    software_document_chunks,
    software_document_search_text,
)


FILES = {
    "model.onnx": (
        "onnx/model_quint8_avx2.onnx",
        "b941bf19f1f1283680f449fa6a7336bb5600bdcd5f84d10ddc5cd72218a0fd21",
    ),
    "tokenizer.json": (
        "tokenizer.json",
        "be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037",
    ),
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _download(relative_path: str, destination: Path, expected_sha256: str) -> None:
    if destination.is_file() and _sha256(destination) == expected_sha256:
        return
    url = f"https://huggingface.co/{MODEL_ID}/resolve/{MODEL_REVISION}/{relative_path}"
    temporary = destination.with_suffix(destination.suffix + ".part")
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as response, temporary.open("wb") as output:
        while chunk := response.read(1024 * 1024):
            output.write(chunk)
    actual = _sha256(temporary)
    if actual != expected_sha256:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(
            f"Checksum mismatch for {relative_path}: expected {expected_sha256}, got {actual}"
        )
    temporary.replace(destination)


def main() -> int:
    model_cache_directory = model_directory()
    for destination_name, (source_name, checksum) in FILES.items():
        _download(source_name, model_cache_directory / destination_name, checksum)
    documents = _action_search_documents(list(action_specs().values()), backend_specs())
    cache = write_embedding_cache(documents)
    documentation_caches = []
    documentation_root = TOOLBOX_ROOT / "native_software_docs"
    for software_directory in sorted(documentation_root.iterdir()):
        if not software_directory.is_dir() or software_directory.name.startswith("_"):
            continue
        chunks = software_document_chunks(software_directory.name, include_cached=False)
        chunk_documents = {
            chunk["chunk_id"]: software_document_search_text(chunk)
            for chunk in chunks
        }
        destination = cache.parent / f"software_docs_{software_directory.name}.npz"
        write_embedding_cache(chunk_documents, destination)
        documentation_caches.append(destination)
    print(f"Cached {MODEL_ID}@{MODEL_REVISION} in {model_cache_directory}")
    print(f"Cached {len(documents)} Action embeddings in {cache}")
    print(f"Cached {len(documentation_caches)} software documentation indexes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
