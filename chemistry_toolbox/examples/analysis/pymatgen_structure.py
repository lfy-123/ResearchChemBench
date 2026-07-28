from __future__ import annotations

from pymatgen.core import Structure

from researchchem_job import JobContext


ctx = JobContext.load()
structure = Structure.from_file(ctx.input("structure"))
ctx.write_json(
    "summary",
    {
        "formula": structure.composition.reduced_formula,
        "site_count": len(structure),
        "volume_angstrom3": float(structure.volume),
    },
)
