# Third-Party Runtime Sources

All source checkouts required to reproduce the data pipeline live under this directory.

| Directory | Purpose | Pinned by |
|---|---|---|
| `grobid/` | Stage 02 PDF-to-TEI parsing | `scripts/bootstrap_grobid.sh` |
| `software-mentions/` | Stage 03 software mention extraction | `scripts/bootstrap_stage_gates.sh` |
| `delft/` | Softcite model runtime | `scripts/bootstrap_stage_gates.sh` |
| `grobid-quantities/` | Stage 04 quantity extraction | `scripts/bootstrap_stage_gates.sh` |
| `MinerU/` | Stage 05 PDF deep parsing | `scripts/bootstrap_mineru.sh` |

Stage 05 repository and dataset downloads are research assets, not runtime dependencies. They are stored in the run's content-addressed asset directory rather than in `third_party/`.

The Stage 05 Crossref, DataCite, OpenAlex, GitHub, Zenodo, OSF, and Materials Cloud integrations use maintained HTTP APIs directly. This avoids adding unneeded wrapper repositories while keeping every adopted runtime source under this directory.
