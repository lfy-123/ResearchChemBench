from __future__ import annotations

import threading

import pytest

from src.core.concurrency import ordered_pipeline_map


def test_ordered_pipeline_map_runs_stages_independently_and_preserves_order() -> None:
    second_upstream_item_started = threading.Event()

    def upstream(value: int) -> int:
        if value == 1:
            second_upstream_item_started.set()
        return value

    def slow_downstream(value: int) -> int:
        if value == 0:
            assert second_upstream_item_started.wait(timeout=2)
        return value * 2

    assert ordered_pipeline_map(
        [upstream, slow_downstream],
        [0, 1, 2],
        max_workers=[1, 1],
        buffer_size=1,
    ) == [0, 2, 4]


def test_ordered_pipeline_map_propagates_stage_failure() -> None:
    def fail_on_one(value: int) -> int:
        if value == 1:
            raise RuntimeError("fixture failure")
        return value

    try:
        ordered_pipeline_map(
            [lambda value: value, fail_on_one],
            [0, 1, 2],
            max_workers=[2, 2],
            buffer_size=2,
        )
    except RuntimeError as exc:
        assert str(exc) == "fixture failure"
    else:
        raise AssertionError("pipeline stage failure was not propagated")


def test_ordered_pipeline_map_stops_downstream_after_failure() -> None:
    visited: list[int] = []

    def downstream(value: int) -> int:
        visited.append(value)
        if value == 0:
            raise RuntimeError("endpoint unavailable")
        return value

    with pytest.raises(RuntimeError, match="endpoint unavailable"):
        ordered_pipeline_map(
            [lambda value: value, downstream],
            list(range(100)),
            max_workers=[1, 1],
            buffer_size=1,
        )

    assert len(visited) < 100
