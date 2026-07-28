"""Path helper for Agent-authored programmable analysis jobs.

This SDK validates declared logical names and resolves paths inside the job
layout. It cannot prevent ordinary Python code from using ``open()``, absolute
paths, subprocesses, or other libraries directly; it is a reliability and
audit helper, not an OS security boundary.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class JobContext:
    root: Path
    contract: dict[str, Any]

    @classmethod
    def load(cls) -> "JobContext":
        root = Path(os.environ.get("RESEARCHCHEM_EXECUTION_JOB_DIRECTORY", Path.cwd()))
        contract_path = root / "analysis_contract.json"
        if not contract_path.is_file():
            raise RuntimeError(f"Analysis contract does not exist: {contract_path}")
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        return cls(root=root.resolve(), contract=contract)

    def _declared_path(self, group: str, name: str) -> Path:
        records = {item["name"]: item for item in self.contract.get(group, [])}
        if name not in records:
            raise KeyError(f"Undeclared {group[:-1]} name: {name!r}")
        relative = records[name].get("target_path") or records[name].get("path")
        path = (self.root / relative).resolve()
        path.relative_to(self.root)
        return path

    def input(self, name: str) -> Path:
        path = self._declared_path("inputs", name)
        if not path.is_file():
            raise FileNotFoundError(f"Declared input does not exist: {path}")
        return path

    def output(self, name: str) -> Path:
        path = self._declared_path("outputs", name)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    @property
    def outputs_dir(self) -> Path:
        return self.root / "outputs"

    @property
    def report_dir(self) -> Path:
        return self.root / "report"

    @property
    def logs_dir(self) -> Path:
        return self.root / "logs"


__all__ = ["JobContext"]
