from __future__ import annotations

import importlib.util
from pathlib import Path


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = TOOLBOX_ROOT / "scripts" / "check_english_only.py"


def _load_checker():
    spec = importlib.util.spec_from_file_location("check_english_only", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_active_toolbox_is_english_only() -> None:
    checker = _load_checker()
    assert checker.find_violations(TOOLBOX_ROOT) == []


def test_checker_reports_cjk_with_location(tmp_path: Path) -> None:
    checker = _load_checker()
    sample = tmp_path / "sample.md"
    sample.write_text("English\nnot English: \u5316\u5b66\n", encoding="utf-8")
    assert checker.find_violations(tmp_path) == ["sample.md:2: not English: \u5316\u5b66"]
