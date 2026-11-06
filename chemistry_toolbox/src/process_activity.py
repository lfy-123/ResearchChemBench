"""Best-effort leader-process observations; never an execution verdict."""
import os
from pathlib import Path
import time

from .recovery_io import process_identity


def process_tree_usage(pid):
    """Host descendants, including runsc Sentry/gofer in separate process groups."""
    rows = {}
    for entry in Path('/proc').glob('[0-9]*/stat'):
        try:
            stat = entry.read_text(); fields = stat[stat.rfind(')') + 2:].split()
            rows[int(entry.parent.name)] = (int(fields[1]), int(fields[11]), int(fields[12]), int(fields[21]), int(fields[19]))
        except (OSError, ValueError, IndexError):
            continue
    selected = {pid}
    while True:
        expanded = selected | {p for p, row in rows.items() if row[0] in selected}
        if expanded == selected:
            break
        selected = expanded
    if pid not in rows:
        return None
    ticks = os.sysconf('SC_CLK_TCK')
    return {'cpu_seconds': sum(rows[p][1] + rows[p][2] for p in selected) / ticks,
            'rss_bytes': sum(rows[p][3] for p in selected) * os.sysconf('SC_PAGE_SIZE'),
            'host_process_count': len(selected),
            'process_cpu': {f'{p}:{rows[p][4]}': (rows[p][1] / ticks, rows[p][2] / ticks) for p in selected}}


def process_activity(pid, logs=(), previous=None, *, tree=False):
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
        if tree:
            usage = process_tree_usage(pid)
            if usage is None:
                raise ProcessLookupError('process tree exited')
            usage.pop('process_cpu')
            result.update(usage, coverage='host_process_tree_including_runtime')
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
