"""Stage 00: select remote papers and materialize grouped local paper bundles."""

from src.stages.stage00_remote_corpus.remote import (
    DATASETS,
    build_publication_index,
    prepare_remote_corpus,
)
from src.stages.stage00_remote_corpus.stage import run_stage00

__all__ = ["DATASETS", "build_publication_index", "prepare_remote_corpus", "run_stage00"]
