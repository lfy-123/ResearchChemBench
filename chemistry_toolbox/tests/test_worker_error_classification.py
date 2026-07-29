from __future__ import annotations

import io
import json
import sys

from researchchem_toolbox import worker


def test_worker_classifies_adapter_value_errors_as_invalid_requests(monkeypatch, capsys):
    def reject(*_args, **_kwargs):
        raise ValueError("unsupported explicit optimizer label")

    monkeypatch.setattr(worker, "execute_local", reject)
    monkeypatch.setattr(
        sys,
        "stdin",
        io.StringIO(
            json.dumps(
                {
                    "action_id": "locate_transition_state",
                    "backend_id": "pysisyphus",
                    "request": {},
                }
            )
        ),
    )

    assert worker.main() == 0
    value = json.loads(capsys.readouterr().out)
    assert value["status"] == "invalid_request"
    assert value["error"]["code"] == "backend_input_error"
    assert "unsupported explicit optimizer label" in value["error"]["message"]
    assert value["retryable"] is True
    assert value["error"]["retry_requires_changed_request"] is True
    assert value["error"]["inspect_action_request"] == {
        "action_id": "locate_transition_state",
        "backend_id": "pysisyphus",
        "detail_level": "contract",
    }
