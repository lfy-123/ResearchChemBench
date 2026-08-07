"""Exec a command that must not outlive its expected Linux parent process."""

from __future__ import annotations

import ctypes
import os
import signal
import sys


def request_parent_death_signal(expected_parent_pid: int) -> bool:
    """Arm PR_SET_PDEATHSIG and reject a parent that died before setup."""

    if not sys.platform.startswith("linux"):
        return True
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(1, signal.SIGTERM, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    return os.getppid() == expected_parent_pid


def main() -> int:
    if len(sys.argv) < 3:
        print(
            "usage: parent_bound_exec.py EXPECTED_PARENT_PID PROGRAM [ARG ...]",
            file=sys.stderr,
        )
        return 64
    try:
        expected_parent_pid = int(sys.argv[1])
    except ValueError:
        print("EXPECTED_PARENT_PID must be an integer", file=sys.stderr)
        return 64
    if expected_parent_pid <= 0:
        print("EXPECTED_PARENT_PID must be positive", file=sys.stderr)
        return 64
    try:
        parent_is_alive = request_parent_death_signal(expected_parent_pid)
    except OSError as exc:
        print(f"failed to configure parent-death signal: {exc}", file=sys.stderr)
        return 70
    if not parent_is_alive:
        print("expected parent exited before child setup", file=sys.stderr)
        return 143
    os.execvp(sys.argv[2], sys.argv[2:])
    return 70


if __name__ == "__main__":
    raise SystemExit(main())
