"""ResearchChemBench data pipeline v2.

The v2 namespace is intentionally isolated from the legacy stage modules.  Existing
commands and caches remain valid until a configuration explicitly selects v2.
"""

from src.v2.pipeline import run_pipeline_v2

__all__ = ["run_pipeline_v2"]
