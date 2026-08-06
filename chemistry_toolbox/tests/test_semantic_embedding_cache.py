from __future__ import annotations

from pathlib import Path

import numpy as np

from chemistry_toolbox.src import semantic_embeddings


def test_default_semantic_cache_is_repository_scoped(monkeypatch) -> None:
    repository_root = Path(__file__).resolve().parents[2]
    monkeypatch.delenv(semantic_embeddings.MODEL_DIRECTORY_ENV, raising=False)
    monkeypatch.delenv(semantic_embeddings.EMBEDDING_CACHE_ENV, raising=False)

    assert semantic_embeddings.model_directory() == (
        repository_root / ".model_cache" / "all-MiniLM-L6-v2"
    )
    assert semantic_embeddings.embedding_cache_path() == (
        repository_root / ".model_cache" / "action_embeddings.npz"
    )


def test_default_toolbox_environment_provisions_semantic_retrieval() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    pip_requirements = (
        repository_root / "chemistry_toolbox/environment/researchchembench/requirements.txt"
    ).read_text(encoding="utf-8")
    constraints = (
        repository_root / "chemistry_toolbox/environment/researchchembench/constraints.txt"
    ).read_text(encoding="utf-8")
    setup_script = (
        repository_root / "chemistry_toolbox/scripts/setup_toolbox_env.sh"
    ).read_text(encoding="utf-8")

    assert "onnxruntime==1.23.2" in pip_requirements
    assert "tokenizers==0.22.2" in pip_requirements
    assert "onnxruntime==1.23.2" in constraints
    assert "tokenizers==0.22.2" in constraints
    assert "cache_minilm_model.py" in setup_script


def test_semantic_runtime_reuses_encoder_and_vector_matrix(
    tmp_path: Path, monkeypatch
) -> None:
    documents = {"action_a": "alpha energy", "action_b": "beta structure"}
    model = tmp_path / "model"
    model.mkdir()
    (model / "model.onnx").write_bytes(b"model")
    (model / "tokenizer.json").write_text("{}", encoding="utf-8")
    cache = tmp_path / "actions.npz"
    np.savez_compressed(
        cache,
        ids=np.asarray(["action_a", "action_b"]),
        vectors=np.asarray([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32),
        digest=np.asarray(semantic_embeddings.document_digest(documents)),
        model_id=np.asarray(semantic_embeddings.MODEL_ID),
    )
    created = 0

    class FakeEncoder:
        def __init__(self, _directory: Path):
            nonlocal created
            created += 1

        def encode(self, _texts):
            return np.asarray([[1.0, 0.0]], dtype=np.float32)

    monkeypatch.setenv(semantic_embeddings.MODEL_DIRECTORY_ENV, str(model))
    monkeypatch.setenv(semantic_embeddings.EMBEDDING_CACHE_ENV, str(cache))
    monkeypatch.setattr(semantic_embeddings, "MiniLMEncoder", FakeEncoder)
    semantic_embeddings.clear_semantic_runtime_cache()

    first, first_status = semantic_embeddings.semantic_scores("alpha", documents)
    second, second_status = semantic_embeddings.semantic_scores("alpha", documents)

    assert first_status == second_status == "available"
    assert first == second
    assert created == 1
    assert semantic_embeddings._resident_embedding_cache.cache_info().hits >= 1


def test_semantic_runtime_rebuilds_stale_cache_atomically(
    tmp_path: Path, monkeypatch
) -> None:
    current_documents = {
        "action_a": "alpha energy",
        "action_b": "beta structure",
    }
    stale_documents = {"action_a": "old alpha energy"}
    model = tmp_path / "model"
    model.mkdir()
    (model / "model.onnx").write_bytes(b"model")
    (model / "tokenizer.json").write_text("{}", encoding="utf-8")
    cache = tmp_path / "actions.npz"
    np.savez_compressed(
        cache,
        ids=np.asarray(["action_a"]),
        vectors=np.asarray([[1.0, 0.0]], dtype=np.float32),
        digest=np.asarray(semantic_embeddings.document_digest(stale_documents)),
        model_id=np.asarray(semantic_embeddings.MODEL_ID),
    )

    class FakeEncoder:
        def __init__(self, _directory: Path):
            pass

        def encode(self, texts):
            if len(texts) == 1:
                return np.asarray([[1.0, 0.0]], dtype=np.float32)
            return np.asarray(
                [[1.0, 0.0], [0.0, 1.0]], dtype=np.float32
            )

    monkeypatch.setenv(semantic_embeddings.MODEL_DIRECTORY_ENV, str(model))
    monkeypatch.setenv(semantic_embeddings.EMBEDDING_CACHE_ENV, str(cache))
    monkeypatch.setattr(semantic_embeddings, "MiniLMEncoder", FakeEncoder)
    semantic_embeddings.clear_semantic_runtime_cache()

    scores, status = semantic_embeddings.semantic_scores("alpha", current_documents)

    assert status == "available"
    assert scores == {"action_a": 1.0, "action_b": 0.0}
    with np.load(cache, allow_pickle=False) as rebuilt:
        assert rebuilt["digest"].item() == semantic_embeddings.document_digest(
            current_documents
        )
        assert rebuilt["ids"].tolist() == ["action_a", "action_b"]
    assert not list(tmp_path.glob(".actions.npz.*.npz"))
