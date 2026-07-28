from __future__ import annotations

import csv
import json

from researchchem_job import JobContext


ctx = JobContext.load()
records = json.loads(ctx.input("records").read_text(encoding="utf-8"))
values = [float(item["value"]) for item in records]
ctx.write_json("summary", {"count": len(values), "mean": sum(values) / len(values)})
with ctx.output("table").open("w", encoding="utf-8", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["index", "value"])
    writer.writerows(enumerate(values))
ctx.register_output("table")
