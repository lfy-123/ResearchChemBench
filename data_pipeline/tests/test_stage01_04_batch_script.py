from __future__ import annotations

import argparse
import importlib.util
import json
import time
from pathlib import Path

import pytest

from src.core.concurrency import ordered_parallel_map

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_stage_01_04_batches.py"
SPEC = importlib.util.spec_from_file_location("run_stage_01_04_batches", SCRIPT)
assert SPEC and SPEC.loader
batch_script = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(batch_script)


def _args() -> argparse.Namespace:
    return argparse.Namespace(
        stage01_workers=4,
        stage02_workers=3,
        stage03_workers=2,
        stage04_workers=1,
    )


def test_ordered_parallel_map_preserves_input_order():
    completed = []

    def work(value: int) -> int:
        time.sleep(0.01 * (3 - value))
        return value * 10

    result = ordered_parallel_map(
        work,
        [1, 2, 3],
        max_workers=3,
        on_complete=lambda _done, _total, index, _item, _result: completed.append(index),
    )

    assert result == [10, 20, 30]
    assert completed != [0, 1, 2]


def test_batch_config_stops_after_resource_limits_and_sets_concurrency(tmp_path):
    template = tmp_path / "config.json"
    template.write_text(
        json.dumps(
            {
                "pdf_directory": "papers",
                "run_directory": "runs/current",
                "grobid": {},
                "softcite": {},
                "grobid_quantities": {},
                "toolbox": {},
            }
        ),
        encoding="utf-8",
    )

    config = batch_script._batch_config(template, tmp_path / "input", tmp_path / "run", _args())

    assert config["stop_after"] == "resource_limits"
    assert config["stage01"]["workers"] == 4
    assert config["grobid"]["workers"] == 3
    assert config["softcite"]["workers"] == 2
    assert config["stage04"]["workers"] == 1
    assert Path(config["softcite"]["aliases_file"]).is_absolute()


def test_records_for_output_selects_only_current_batch(tmp_path):
    current = tmp_path / "current"
    previous = tmp_path / "previous"
    current.mkdir()
    previous.mkdir()
    current_pdf = current / "current.pdf"
    previous_pdf = previous / "previous.pdf"
    current_pdf.write_bytes(b"current")
    previous_pdf.write_bytes(b"previous")
    manifest = tmp_path / "download_manifest.jsonl"
    manifest.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "remote_uri": "s3://bucket/previous.pdf",
                        "local_path": str(previous_pdf),
                        "size_bytes": 8,
                    }
                ),
                json.dumps(
                    {
                        "remote_uri": "s3://bucket/current.pdf",
                        "local_path": str(current_pdf),
                        "size_bytes": 7,
                    }
                ),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    rows = batch_script._records_for_output(manifest, current)

    assert [row["remote_uri"] for row in rows] == ["s3://bucket/current.pdf"]


def test_safe_remove_batch_only_deletes_direct_batch_child(tmp_path):
    workspaces = tmp_path / "workspaces"
    batch = workspaces / "batch_0001"
    batch.mkdir(parents=True)
    (batch / "temporary.pdf").write_bytes(b"pdf")

    batch_script._safe_remove_batch(batch, workspaces)

    assert not batch.exists()
    unsafe = tmp_path / "not-a-batch"
    unsafe.mkdir()
    with pytest.raises(RuntimeError, match="unsafe batch path"):
        batch_script._safe_remove_batch(unsafe, workspaces)


def test_retain_selected_pdfs_records_remote_provenance(tmp_path):
    input_root = tmp_path / "batch" / "input"
    outputs = tmp_path / "batch" / "run" / "outputs"
    relative = Path("journal") / "paper.pdf"
    (input_root / relative).parent.mkdir(parents=True)
    (input_root / relative).write_bytes(b"batch")
    selected = outputs / "stage_04_resource_limits" / "selected_pdf_paths.jsonl"
    selected.parent.mkdir(parents=True)
    selected.write_text(
        json.dumps({"document_id": "doc-1", "pdf_path": str(input_root / relative)}) + "\n",
        encoding="utf-8",
    )

    retained = batch_script._retain_selected_pdfs(
        batch_number=1,
        input_root=input_root,
        outputs=outputs,
        retained_root=tmp_path / "retained",
        source_by_relative={str(relative): {"remote_uri": "s3://bucket/journal/paper.pdf"}},
    )

    assert retained[0]["remote_uri"] == "s3://bucket/journal/paper.pdf"
    assert (tmp_path / "retained" / relative).read_bytes() == b"batch"


def test_sandbox_fallbacks_only_move_to_smaller_cpu(monkeypatch, tmp_path):
    args = argparse.Namespace(
        sandbox_cpu=64,
        sandbox_memory="128Gi",
        sandbox_fallback_resource=["96:192Gi", "32:96Gi"],
    )
    requests = []

    def create(_python, action, current_args):
        assert action == "create"
        requests.append((current_args.sandbox_cpu, current_args.sandbox_memory))
        if current_args.sandbox_cpu == 64:
            raise batch_script.subprocess.CalledProcessError(1, ["sandbox", "create"])

    monkeypatch.setattr(batch_script, "_sandbox_command", create)
    monkeypatch.setattr(batch_script, "_delete_failed_sandbox_pool", lambda *_args: None)
    state = {}
    state_path = tmp_path / "state.json"

    batch_script._create_sandbox_with_fallback(Path("python"), args, state, state_path)

    assert requests == [(64, "128Gi"), (32, "96Gi")]
    assert state["effective_sandbox"] == {"cpu": 32, "memory": "96Gi"}
