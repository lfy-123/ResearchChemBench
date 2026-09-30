"""Best-effort leader-process observations; never an execution verdict."""
import os
from pathlib import Path
import time

from .recovery_io import process_identity


def process_activity(pid, logs=(), previous=None):
    identity = process_identity(pid)
    result = {"observed_at": time.time(), "identity": identity, "coverage": "leader_only",
              "status": "partial", "cpu_seconds": None, "cpu_delta_seconds": None,
              "rss_bytes": None, "io_bytes": None, "logs": []}
    try:
        stat = Path(f"/proc/{pid}/stat").read_text()
        fields = stat[stat.rfind(")") + 2:].split()
        if int(fields[19]) != identity.get("start_ticks"):
            raise ValueError("process changed during observation")
        result.update(cpu_seconds=(int(fields[11]) + int(fields[12])) / os.sysconf("SC_CLK_TCK"),
                      rss_bytes=int(fields[21]) * os.sysconf("SC_PAGE_SIZE"))
        if previous and all(previous.get("identity", {}).get(k) == identity.get(k) for k in ("host", "boot_id", "pid", "start_ticks")):
            before = previous.get("cpu_seconds")
            if before is not None and result["cpu_seconds"] >= before:
                result["cpu_delta_seconds"] = result["cpu_seconds"] - before
        io = dict(line.split(":", 1) for line in Path(f"/proc/{pid}/io").read_text().splitlines())
        result["io_bytes"] = {k: int(io[k]) for k in ("read_bytes", "write_bytes")}
    except (OSError, ValueError, KeyError, IndexError) as exc:
        result.update(status="unknown" if result["cpu_seconds"] is None else "partial", diagnostic=str(exc))
    for log in logs:
        try:
            stat = Path(log).stat()
            result["logs"].append({"path": str(log), "size_bytes": stat.st_size, "modified_at": stat.st_mtime})
        except OSError:
            result["logs"].append({"path": str(log), "status": "unknown"})
    return result
