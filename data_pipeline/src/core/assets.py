from functools import lru_cache
from pathlib import Path

from src.core.io import read_json
from src.core.paths import PROJECT_ROOT

DEFAULT_PROMPT_EXAMPLES = PROJECT_ROOT / "assets" / "prompt_examples.json"


@lru_cache(maxsize=4)
def load_prompt_examples(path: str | Path = DEFAULT_PROMPT_EXAMPLES) -> dict[str, str]:
    examples = read_json(path)
    if not isinstance(examples, dict):
        raise ValueError("prompt examples must be a JSON object keyed by task type")
    if not all(isinstance(value, str) and value.strip() for value in examples.values()):
        raise ValueError("every prompt example must be one non-empty case string")
    return examples


def prompt_example(task_type: str, path: str | Path = DEFAULT_PROMPT_EXAMPLES) -> str:
    examples = load_prompt_examples(Path(path).resolve())
    try:
        return examples[task_type]
    except KeyError as exc:
        raise ValueError(f"missing prompt example for task type: {task_type}") from exc
