from __future__ import annotations

from pathlib import Path

import numpy as np

from researchchem_toolbox import semantic_embeddings


def test_default_toolbox_environment_provisions_semantic_retrieval() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    pip_requirements = (
        repository_root / "chemistry_toolbox/environment/toolbox-pip.txt"
    ).read_text(encoding="utf-8")
    constraints = (
        repository_root / "chemistry_toolbox/environment/toolbox-constraints.txt"
    ).read_text(encoding="utf-8")
    setup_script = (
        repository_root / "chemistry_toolbox/scripts/setup_toolbox_env.sh"
    ).read_text(encoding="utf-8")

    assert "onnxruntime>=1.17" in pip_requirements
    assert "tokenizers>=0.15" in pip_requirements
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
