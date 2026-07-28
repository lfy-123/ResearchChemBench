from __future__ import annotations

from ase.io import read, write

from researchchem_job import JobContext


ctx = JobContext.load()
atoms = read(ctx.input("structure"))
atoms.center(vacuum=5.0)
write(ctx.output("centered_structure"), atoms)
ctx.register_output("centered_structure")
