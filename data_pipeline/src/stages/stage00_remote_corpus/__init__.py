"""Stage 00: select remote papers and materialize grouped local paper bundles."""

from src.stages.stage00_remote_corpus.remote import DATASETS, prepare_remote_corpus
from src.stages.stage00_remote_corpus.stage import run_stage00

__all__ = ["DATASETS", "prepare_remote_corpus", "run_stage00"]
