from __future__ import annotations

import threading
from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import Callable, TypeVar, cast

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")
CompletionCallback = Callable[[int, int, int, InputT, OutputT], None]


def ordered_parallel_map(
    function: Callable[[InputT], OutputT],
    items: list[InputT],
    *,
    max_workers: int = 1,
    on_complete: CompletionCallback[InputT, OutputT] | None = None,
) -> list[OutputT]:
    """Run independent work concurrently while preserving input order in the result."""
    workers = max(1, int(max_workers))
    total = len(items)
    if workers == 1 or total < 2:
        output = []
        for index, item in enumerate(items):
            result = function(item)
            output.append(result)
            if on_complete is not None:
                on_complete(index + 1, total, index, item, result)
        return output

    output: list[OutputT | None] = [None] * total
    executor = ThreadPoolExecutor(max_workers=min(workers, total))
    futures: dict[Future[OutputT], tuple[int, InputT]] = {
        executor.submit(function, item): (index, item) for index, item in enumerate(items)
    }
    try:
        for completed, future in enumerate(as_completed(futures), start=1):
            index, item = futures[future]
            result = future.result()
            output[index] = result
            if on_complete is not None:
                on_complete(completed, total, index, item, result)
    except BaseException:
        for future in futures:
            future.cancel()
        executor.shutdown(wait=True, cancel_futures=True)
        raise
    executor.shutdown(wait=True)
    return cast(list[OutputT], output)


def ordered_pipeline_map(
    functions: list[Callable[[object], object]],
    items: list[InputT],
    *,
    max_workers: list[int],
    buffer_size: int = 1,
) -> list[OutputT]:
    """Run dependent stages in separate bounded pools while preserving order.

    A boundary semaphore counts work queued or running in the next stage.  When a
    downstream stage is saturated, only the upstream completion callbacks block;
    unrelated downstream pools continue draining normally.
    """

    if not functions:
        raise ValueError("ordered_pipeline_map requires at least one stage")
    if len(functions) != len(max_workers):
        raise ValueError("max_workers must provide one value per pipeline stage")
    if any(int(value) < 1 for value in max_workers):
        raise ValueError("pipeline stage workers must be positive")
    if int(buffer_size) < 1:
        raise ValueError("pipeline buffer_size must be positive")
    if not items:
        return []

    executors = [ThreadPoolExecutor(max_workers=int(value)) for value in max_workers]
    boundaries = [threading.BoundedSemaphore(int(buffer_size)) for _ in functions[:-1]]
    completions: list[Future[object]] = [Future() for _ in items]

    def submit(stage_index: int, item_index: int, value: object, inbound=None) -> None:
        try:
            future = executors[stage_index].submit(functions[stage_index], value)
        except BaseException as exc:
            if inbound is not None:
                inbound.release()
            completions[item_index].set_exception(exc)
            return

        def completed(stage_future: Future[object]) -> None:
            if inbound is not None:
                inbound.release()
            try:
                result = stage_future.result()
                if stage_index == len(functions) - 1:
                    completions[item_index].set_result(result)
                    return
                outbound = boundaries[stage_index]
                outbound.acquire()
                submit(stage_index + 1, item_index, result, outbound)
            except BaseException as exc:
                completions[item_index].set_exception(exc)

        future.add_done_callback(completed)

    try:
        for index, item in enumerate(items):
            submit(0, index, item)
        output: list[object | None] = [None] * len(items)
        first_error: BaseException | None = None
        for index, completion in enumerate(completions):
            try:
                output[index] = completion.result()
            except BaseException as exc:
                first_error = first_error or exc
        if first_error is not None:
            raise first_error
        return cast(list[OutputT], output)
    finally:
        for executor in executors:
            executor.shutdown(wait=True, cancel_futures=False)


__all__ = ["ordered_parallel_map", "ordered_pipeline_map"]
