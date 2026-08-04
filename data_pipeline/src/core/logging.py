from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Iterable

LOGGER_NAME = "chem_pipeline"


def configure_pipeline_logging(log_path: str | Path, verbose: bool = True) -> logging.Logger:
    path = Path(log_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    for handler in list(logger.handlers):
        handler.close()
        logger.removeHandler(handler)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler = logging.FileHandler(path, mode="a", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if verbose:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    logger.info("LOG INITIALIZED | file=%s", path)
    return logger


def pipeline_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)


def log_progress(
    stage: str,
    current: int,
    total: int,
    label: str = "",
    *,
    status: str | None = None,
) -> None:
    total = max(total, 1)
    current = min(max(current, 0), total)
    width = 30
    filled = round(width * current / total)
    bar = "#" * filled + "-" * (width - filled)
    percent = 100.0 * current / total
    suffix = f" | status={status}" if status else ""
    pipeline_logger().info(
        "PROGRESS | %s | [%s] %d/%d %5.1f%% | %s%s",
        stage,
        bar,
        current,
        total,
        percent,
        label,
        suffix,
    )


def value_counts(values: Iterable[Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = "unknown" if value is None else str(value)
        counts[key] = counts.get(key, 0) + 1
    return counts
