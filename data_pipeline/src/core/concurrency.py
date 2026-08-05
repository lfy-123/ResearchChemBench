from __future__ import annotations

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


__all__ = ["ordered_parallel_map"]
