from __future__ import annotations

import json
from pathlib import Path

from src.late_stage_runner import (
    _read_paths_for_paper,
    _resolve_paper_id_from_paths,
)


def test_historical_jsonl_loader_stream_filters_paper(tmp_path: Path) -> None:
    shard = tmp_path / "records.jsonl"
    shard.write_text(
        "\n".join(
            [
                json.dumps({"paper_id": "paper_other", "payload": "large" * 100}),
                json.dumps(
                    {
                        "paper_id": "paper_target",
                        "doi": "10.1000/target",
                        "payload": {"answer": 1},
                    }
                ),
                "{malformed-json}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    assert _read_paths_for_paper([shard], paper_id="paper_target") == [
        {
            "paper_id": "paper_target",
            "doi": "10.1000/target",
            "payload": {"answer": 1},
        }
    ]
    assert _resolve_paper_id_from_paths([[shard]], "10.1000/target") == (
        "paper_target"
    )
