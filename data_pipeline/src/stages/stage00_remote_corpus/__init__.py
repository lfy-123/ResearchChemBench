"""Stage 00: select remote papers and materialize grouped local paper bundles."""

from src.stages.stage00_remote_corpus.stage import DATASETS, prepare_remote_corpus

__all__ = ["DATASETS", "prepare_remote_corpus"]
