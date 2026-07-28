from __future__ import annotations

from researchchem_job import JobContext


ctx = JobContext.load()
paths = sorted(ctx.input("file_list").read_text(encoding="utf-8").splitlines())
records = []
for relative_path in paths:
    path = ctx.root / relative_path
    records.append({"path": relative_path, "exists": path.is_file(), "size_bytes": path.stat().st_size if path.is_file() else None})
ctx.write_json("summary", {"files": records})
