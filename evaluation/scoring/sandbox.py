"""Linux Landlock boundary for the Judge and all of its child processes."""
import ctypes
import json
import os
from pathlib import Path
import sys


def restrict(readable, writable):
    libc = ctypes.CDLL(None, use_errno=True)
    def check(result):
        if result < 0:
            error = ctypes.get_errno()
            raise OSError(error, os.strerror(error))
        return result
    class Ruleset(ctypes.Structure):
        _fields_ = [("access", ctypes.c_uint64)]
    class Beneath(ctypes.Structure):
        _pack_ = 1
        _fields_ = [("access", ctypes.c_uint64), ("parent", ctypes.c_int)]
    abi = check(libc.syscall(444, 0, 0, 1))
    access = (1 << 13) - 1
    if abi >= 2:
        access |= 1 << 13  # REFER
    if abi >= 3:
        access |= 1 << 14  # TRUNCATE
    rule = Ruleset(access)
    ruleset = check(libc.syscall(444, ctypes.byref(rule), ctypes.sizeof(rule), 0))
    for paths, allowed in ((readable, 1 | 4 | 8), (writable, access)):
        for path in paths:
            path = Path(path).resolve(strict=True)
            descriptor = os.open(path, os.O_PATH | os.O_CLOEXEC)
            rights = allowed if path.is_dir() else allowed & (1 | 2 | 4 | (1 << 14))
            beneath = Beneath(rights, descriptor)
            try:
                check(libc.syscall(445, ruleset, 1, ctypes.byref(beneath), 0))
            finally:
                os.close(descriptor)
    check(libc.prctl(38, 1, 0, 0, 0))  # no_new_privs
    check(libc.syscall(446, ruleset, 0))
    os.close(ruleset)


if __name__ == "__main__":
    policy = json.loads(Path(sys.argv[1]).read_text())
    restrict(policy["readable"], policy["writable"])
    os.execv(sys.argv[2], sys.argv[2:])
