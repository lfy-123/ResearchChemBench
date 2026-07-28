from __future__ import annotations

import re

from researchchem_job import JobContext


ctx = JobContext.load()
text = ctx.input("quantum_output").read_text(encoding="utf-8", errors="replace")
energies = [
    float(value)
    for value in re.findall(r"FINAL SINGLE POINT ENERGY\s+(-?\d+(?:\.\d+)?)", text)
]
ctx.write_json("parsed", {"final_energy_hartree": energies[-1] if energies else None})
