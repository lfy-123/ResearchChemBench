# Programmable Analysis Templates

These templates demonstrate the job contract and current APIs. They are starting points, not scientific defaults. Declare every input and output in `AnalysisJobRequest`, select a runtime that provides the listed modules, and adapt the scientific method explicitly.

| Template | Runtime/modules | Declared outputs |
|---|---|---|
| `json_csv_analysis.py` | core: json, csv | JSON summary and CSV table |
| `quantum_output_parser.py` | quantum: re | parsed JSON |
| `ase_structure.py` | core: ase | transformed XYZ |
| `pymatgen_structure.py` | periodic: pymatgen | structure summary JSON |
| `scipy_fit.py` | core: numpy, scipy | fit JSON |
| `matplotlib_plot.py` | core: matplotlib | PNG figure |
| `batch_files.py` | core: pathlib | batch summary JSON |
| `schema_report.py` | core: json | JSON result and Markdown report |

Use `ctx.input(name)` and `ctx.output(name)` only with names declared in the request. `JobContext` improves reliability and provenance but is not a filesystem security boundary.
