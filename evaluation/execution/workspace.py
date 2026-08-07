"""Workspace construction, input extraction, and run instructions."""

from __future__ import annotations

import hashlib
import json
import shutil
import stat
from pathlib import Path, PurePosixPath
from typing import Any
from zipfile import ZipFile

from chemistry_toolbox.src.catalog import catalog_snapshot, toolbox_overview
from chemistry_toolbox.src.distributed_pool import pool_snapshot

from .instructions import INSTRUCTIONS_TEMPLATE


class WorkspaceLifecycleMixin:
    def _execution_resource_guidance(self) -> str:
        if self.execution_mode == "local":
            return (
                "This run has an evaluator-controlled per-task resource envelope:\n\n"
                f"- CPU: {self.available_cpu_cores} logical cores\n"
                f"- Memory: {self.available_memory_mb} MiB\n"
                f"- GPU: {self.available_gpu_count}\n\n"
                "You may choose the resources for each managed calculation within this envelope. "
                "The sum of all concurrently queued or running managed jobs must also remain "
                "within it. Requests above the budget are rejected rather than silently reduced. "
                "Parallelize independent calculations only when their combined CPU, memory, and "
                "GPU reservations fit this budget."
            )
        snapshot = pool_snapshot()
        cpu_label = (
            "physical cores"
            if snapshot.get("cpu_core_semantics") == "physical"
            else "logical CPUs"
        )
        topology_note = (
            "- SMT sibling threads are excluded from scientific scheduling\n"
            if snapshot.get("cpu_core_semantics") == "physical"
            else (
                f"- Physical cores backing the pool: "
                f"{snapshot['physical_cpu_cores_backing_pool']}\n"
            )
        )
        return (
            "This run uses a toolbox-managed distributed CPU compute pool. The coordinator node "
            "runs the Agent, model calls, MCP services, and scheduler only; it is not available "
            "for scientific calculations.\n\n"
            f"- Compute workers: {snapshot['worker_count']} anonymous nodes\n"
            f"- Total schedulable CPU: {snapshot['total_cpu_cores']} {cpu_label}\n"
            f"{topology_note}"
            f"- Total schedulable memory: {snapshot['total_memory_mb']} MiB\n"
            f"- Maximum per job: {snapshot['maximum_cpu_cores_per_job']} {cpu_label} and "
            f"{snapshot['maximum_memory_mb_per_job']} MiB\n"
            f"- Reference memory ratio: 2000 MiB per {cpu_label[:-1] if cpu_label.endswith('s') else cpu_label}; "
            "this is planning guidance, "
            "not a hard CPU-to-memory ratio\n"
            "- One job never crosses nodes; CPU and memory are requested and reserved independently\n\n"
            "You choose which scientifically independent calculations to submit together and the "
            "CPU/memory request for each, but never choose a worker. Use "
            "`submit_action_batch_async` for independent predefined Actions and "
            "`wait_execution_events` for evaluator-controlled stable completion/failure feedback. "
            "Build one complete unique item list for each independent stage, submit it once, and "
            "let the toolbox queue excess items; do not split overlapping batches or repeat pilot "
            "inputs. Submit "
            "independent native and analysis jobs together, then pass all their IDs to "
            "`wait_execution_jobs`; the toolbox performs internal supervision, automatic terminal "
            "collection, and stable batched notification while queues continue to fill. Waiting requests are "
            "ordered by CPU, then "
            "memory, from largest to smallest. Submit currently known independent work together "
            "so large jobs are visible before small jobs fragment capacity. Treat effective pool "
            "utilization as an execution objective: when independent work is ready, submit enough "
            "concurrent jobs for their combined CPU requests to approach current available capacity. "
            "For CPU-scalable work, request the highest core count likely to reduce wall time, up "
            "to the per-job limit. A programmable analysis job requesting multiple cores must "
            "actually implement multiprocessing or use a parallel numerical library; do not "
            "inflate requests for serial or I/O-bound work. Keep dependent stages sequential, "
            "and use the resource snapshot returned by `wait_execution_jobs` when replanning after "
            "completions or failures."
        )
    def _build_instructions(self) -> str:
        data_parts = []
        for item in self.task_info.get("data", []):
            type_text = f" [{item.get('type')}]" if item.get("type") else ""
            data_parts.append(
                f"- **{item.get('name', '')}**{type_text} "
                f"(`{item.get('path', '')}`): {item.get('description', '')}"
            )
        data_text = "\n".join(data_parts) if data_parts else "No additional input files."
        scientific_requirements = self.task_info.get("scientific_requirements") or []
        requirements_text = (
            "\n".join(
                f"{index}. {requirement}"
                for index, requirement in enumerate(scientific_requirements, start=1)
            )
            if scientific_requirements
            else "Follow the scientific validity requirements stated in the task."
        )
        deliverables = self.task_info.get("required_deliverables") or []
        deliverable_lines = []
        for item in deliverables:
            if isinstance(item, str):
                deliverable_lines.append(f"- `{item}`")
                continue
            path = str(item.get("path") or "").strip()
            description = str(item.get("description") or "").strip()
            if path:
                deliverable_lines.append(
                    f"- `{path}`" + (f": {description}" if description else "")
                )
        required_deliverables = (
            "\n".join(deliverable_lines)
            if deliverable_lines
            else "- `report/report.md`: final answer and artifact-linked scientific account."
        )
        return INSTRUCTIONS_TEMPLATE.format(
            workspace=str(self.workspace.resolve()),
            task_desc=self.task_info["task"],
            category=self.task_info.get("category", "uncategorized"),
            data_text=data_text,
            scientific_mode=self.task_info.get(
                "scientific_mode", "standard_autonomous_investigation"
            ),
            scientific_mode_description=self.task_info.get(
                "scientific_mode_description",
                "The objective is fixed, while scientific planning and execution remain autonomous.",
            ),
            scientific_requirements=requirements_text,
            execution_resource_guidance=self._execution_resource_guidance(),
            required_deliverables=required_deliverables,
            toolbox_overview=toolbox_overview(
                discovery_mode=self.tool_discovery_mode,
                include_health=True,
                snapshot=(
                    json.loads((self.workspace / "_toolbox_catalog.json").read_text(encoding="utf-8"))
                    if (self.workspace / "_toolbox_catalog.json").is_file()
                    else None
                ),
            ),
        )

    def _required_deliverable_status(self) -> list[dict[str, Any]]:
        """Record task-specific evidence-product presence without making it a run gate."""

        values: list[dict[str, Any]] = []
        root = self.workspace.resolve()
        for item in self.task_info.get("required_deliverables") or []:
            specification = {"path": item} if isinstance(item, str) else dict(item)
            relative = str(specification.get("path") or "").strip()
            if not relative or Path(relative).is_absolute():
                continue
            path = (root / relative).resolve()
            try:
                path.relative_to(root)
            except ValueError:
                continue
            exists = path.is_file()
            size = path.stat().st_size if exists else 0
            allow_empty = bool(specification.get("allow_empty", False))
            values.append(
                {
                    "path": relative,
                    "exists": exists,
                    "size_bytes": size,
                    "satisfied": exists and (allow_empty or size > 0),
                    "allow_empty": allow_empty,
                }
            )
        return values

    @staticmethod
    def _resolve_under(base: Path, relative_path: str, *, field: str) -> Path:
        if not relative_path or Path(relative_path).is_absolute():
            raise ValueError(f"{field} must be a non-empty relative path")
        base = base.resolve()
        resolved = (base / relative_path).resolve()
        try:
            resolved.relative_to(base)
        except ValueError as exc:
            raise ValueError(f"{field} escapes the task data directory") from exc
        return resolved

    def _extract_task_archives(self) -> None:
        data_root = (self.workspace / "data").resolve()
        for specification in self.task_info.get("archive_extractions", []):
            source = self._resolve_under(
                data_root,
                str(specification["source"]),
                field="archive_extractions.source",
            )
            destination = self._resolve_under(
                data_root,
                str(specification["destination"]),
                field="archive_extractions.destination",
            )
            if not source.is_file():
                raise FileNotFoundError(f"Task data archive not found: {source}")
            expected_sha256 = str(specification.get("sha256") or "").strip().lower()
            if expected_sha256:
                actual_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
                if actual_sha256 != expected_sha256:
                    raise ValueError(
                        f"Task data archive SHA-256 mismatch for {source.name}: "
                        f"expected {expected_sha256}, received {actual_sha256}"
                    )
            with ZipFile(source) as archive:
                infos = archive.infolist()
                if len(infos) > 100_000:
                    raise ValueError("Task data archive contains too many entries")
                total_size = sum(info.file_size for info in infos)
                if total_size > 5_000_000_000:
                    raise ValueError("Task data archive expands beyond the 5 GB safety limit")
                targets: set[Path] = set()
                for info in infos:
                    name = info.filename
                    member = PurePosixPath(name)
                    mode = (info.external_attr >> 16) & 0o170000
                    if (
                        not name
                        or member.is_absolute()
                        or ".." in member.parts
                        or "\\" in name
                        or "\x00" in name
                        or info.flag_bits & 0x1
                        or (
                            mode
                            and mode not in {stat.S_IFREG, stat.S_IFDIR}
                        )
                    ):
                        raise ValueError(f"Unsafe task archive member: {name!r}")
                    target = destination.joinpath(*member.parts)
                    try:
                        resolved_target = target.resolve()
                        resolved_target.relative_to(destination.resolve())
                    except ValueError as exc:
                        raise ValueError(f"Task archive member escapes destination: {name!r}") from exc
                    if resolved_target in targets:
                        raise ValueError(f"Duplicate task archive target: {name!r}")
                    targets.add(resolved_target)
                destination.mkdir(parents=True, exist_ok=False)
                for info in infos:
                    member = PurePosixPath(info.filename)
                    target = destination.joinpath(*member.parts)
                    if info.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(info) as source_handle, target.open("wb") as target_handle:
                        shutil.copyfileobj(source_handle, target_handle)

    def setup_workspace(self) -> None:
        if not self.task_dir.is_dir():
            raise FileNotFoundError(f"Task not found: {self.task_id}")
        self.workspace.mkdir(parents=True, exist_ok=False)
        source_data = self.task_dir / "data"
        if source_data.exists():
            shutil.copytree(source_data, self.workspace / "data", dirs_exist_ok=True)
        else:
            (self.workspace / "data").mkdir()
        self._extract_task_archives()
        for directory in (
            "code",
            "outputs",
            "report",
            "report/images",
            "tool_logs",
            "_tool_results",
            "_tool_artifacts",
        ):
            (self.workspace / directory).mkdir(parents=True, exist_ok=True)

        # Input data is copied but made read-only for the normal benchmark path.
        for path in (self.workspace / "data").rglob("*"):
            if path.is_file():
                path.chmod(0o444)

        catalog = catalog_snapshot(
            include_health=True,
            discovery_mode=self.tool_discovery_mode,
            resource_budget=self.resource_budget_record(),
        )
        (self.workspace / "_toolbox_catalog.json").write_text(
            json.dumps(
                catalog,
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        self.instructions_path.write_text(self._build_instructions(), encoding="utf-8")
        self._write_claude_mcp_config()
        self._write_opencode_config()
        catalog_path = self.workspace / "_toolbox_catalog.json"
        self._write_meta(
            "ready",
            {
                "instruction_bytes": self.instructions_path.stat().st_size,
                "catalog_snapshot_bytes": catalog_path.stat().st_size,
                "mcp_public_tool_count": len(self._mcp_server_specs()[0].get("tools", [])),
            },
        )
