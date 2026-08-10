from __future__ import annotations

import threading
import time
from pathlib import Path
from types import SimpleNamespace

from src.integrations.mineru import run_mineru_queue


def test_mineru_queue_runs_documents_concurrently_and_preserves_order(
    monkeypatch, tmp_path: Path
) -> None:
    active = 0
    peak = 0
    lock = threading.Lock()

    def fake_run(command, **_kwargs):
        nonlocal active, peak
        target = Path(command[command.index("-o") + 1])
        document_id = target.name
        with lock:
            active += 1
            peak = max(peak, active)
        time.sleep(0.05)
        output = target / document_id
        output.mkdir(parents=True)
        (output / f"{document_id}.md").write_text("valid text", encoding="utf-8")
        (output / f"{document_id}_content_list_v2.json").write_text(
            '[{"page_idx": 0}]', encoding="utf-8"
        )
        with lock:
            active -= 1
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr("src.integrations.mineru._resolve_executable", lambda _command: "mineru")
    monkeypatch.setattr("src.integrations.mineru.subprocess.run", fake_run)
    queue = [
        {
            "document_id": f"document-{index}",
            "paper_id": f"paper-{index}",
            "source_path": str(tmp_path / f"source-{index}.pdf"),
            "expected_pages": 1,
        }
        for index in range(4)
    ]

    results = run_mineru_queue(
        queue,
        tmp_path / "output",
        execute=True,
        min_markdown_chars=1,
        max_workers=3,
    )

    assert peak == 3
    assert [row["document_id"] for row in results] == [row["document_id"] for row in queue]
    assert {row["status"] for row in results} == {"success"}


def test_mineru_queue_isolates_one_concurrent_failure(monkeypatch, tmp_path: Path) -> None:
    def fake_run(command, **_kwargs):
        target = Path(command[command.index("-o") + 1])
        if target.name == "document-1":
            raise RuntimeError("fixture failure")
        output = target / target.name
        output.mkdir(parents=True)
        (output / f"{target.name}.md").write_text("valid text", encoding="utf-8")
        (output / f"{target.name}_content_list_v2.json").write_text(
            '[{"page_idx": 0}]', encoding="utf-8"
        )
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr("src.integrations.mineru._resolve_executable", lambda _command: "mineru")
    monkeypatch.setattr("src.integrations.mineru.subprocess.run", fake_run)
    queue = [
        {
            "document_id": f"document-{index}",
            "paper_id": f"paper-{index}",
            "source_path": str(tmp_path / f"source-{index}.pdf"),
            "expected_pages": 1,
        }
        for index in range(3)
    ]

    results = run_mineru_queue(
        queue,
        tmp_path / "output",
        execute=True,
        min_markdown_chars=1,
        max_workers=3,
    )

    assert [row["status"] for row in results] == ["success", "failed", "success"]
    assert "fixture failure" in results[1]["error"]


def test_mineru_queue_batches_multiple_documents_in_one_request(
    monkeypatch, tmp_path: Path
) -> None:
    calls = []

    def fake_run(command, **_kwargs):
        calls.append(command)
        input_root = Path(command[command.index("-p") + 1])
        output_root = Path(command[command.index("-o") + 1])
        for source in input_root.iterdir():
            target = output_root / source.stem / "auto"
            target.mkdir(parents=True)
            (target / f"{source.stem}.md").write_text("valid text", encoding="utf-8")
            (target / f"{source.stem}_content_list_v2.json").write_text(
                '[{"page_idx": 0}]', encoding="utf-8"
            )
        return SimpleNamespace(returncode=0, stdout="ok", stderr="")

    monkeypatch.setattr("src.integrations.mineru._resolve_executable", lambda _command: "mineru")
    monkeypatch.setattr("src.integrations.mineru.subprocess.run", fake_run)
    queue = []
    for index in range(3):
        source = tmp_path / f"source-{index}.pdf"
        source.write_bytes(b"%PDF fixture")
        queue.append(
            {
                "document_id": f"document-{index}",
                "paper_id": f"paper-{index}",
                "source_path": str(source),
                "expected_pages": 1,
            }
        )

    results = run_mineru_queue(
        queue,
        tmp_path / "output",
        execute=True,
        min_markdown_chars=1,
        max_workers=1,
        request_batch_size=3,
    )

    assert len(calls) == 1
    assert [row["status"] for row in results] == ["success", "success", "success"]
    assert {row["request_batch_size"] for row in results} == {3}
