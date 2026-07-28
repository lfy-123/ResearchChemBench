from __future__ import annotations

from researchchem_job import JobContext


ctx = JobContext.load()
result = {"status": "complete", "observations": []}
ctx.write_json("result", result)
ctx.output("report").write_text(
    "# Analysis Report\n\nStatus: complete\n",
    encoding="utf-8",
)
ctx.register_output("report")
