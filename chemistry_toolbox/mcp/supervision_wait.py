"""Drive identical supervision steps synchronously or without blocking MCP."""
from __future__ import annotations

import time
import threading

import anyio


_CHECK_LIMITER = anyio.CapacityLimiter(4)


def _advance(steps):
    try:
        return False, next(steps)
    except StopIteration as done:
        return True, done.value


def run_wait(steps, *, sleep_fn=time.sleep):
    try:
        while True:
            finished, value = _advance(steps)
            if finished:
                return value
            sleep_fn(value)
    finally:
        steps.close()


class _AsyncSteps:
    """Close safely even if native Task.cancel interrupts a worker step."""

    def __init__(self, steps):
        self.steps = steps
        self.lock = threading.Lock()
        self.closed = threading.Event()

    def advance(self):
        with self.lock:
            try:
                if self.closed.is_set():
                    return True, None
                return _advance(self.steps)
            finally:
                if self.closed.is_set():
                    self.steps.close()

    def close(self):
        self.closed.set()
        if self.lock.acquire(blocking=False):
            try:
                self.steps.close()
            finally:
                self.lock.release()


async def run_wait_async(steps):
    driver = _AsyncSteps(steps)
    try:
        while True:
            # A step can read/hash files. Bound that work independently of the
            # server loop. The worker never sleeps or owns a calculation.
            # Shield only this finite step so cancellation cannot race close().
            with anyio.CancelScope(shield=True):
                finished, value = await anyio.to_thread.run_sync(
                    driver.advance, limiter=_CHECK_LIMITER
                )
            await anyio.lowlevel.checkpoint()
            if finished:
                return value
            await anyio.sleep(value)
    finally:
        driver.close()
