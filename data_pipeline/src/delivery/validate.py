from __future__ import annotations

import hashlib
import sys
import tempfile
from pathlib import Path
from typing import Any

from src.core.io import read_json, sha256_file
from src.core.paths import DEFAULT_BENCHMARK_ROOT

_CHEMISTRY_VALIDATION_CACHE: dict[str, dict[str, Any]] = {}


def validate_dataset(
    root: str | Path,
    *,
    benchmark_root: str | Path | None = None,
    run_workspace_smoke: bool = True,
    require_tasks: bool = True,
) -> dict[str, Any]:
    """Validate staged tasks against the actual ResearchChemBench contract."""

    root = Path(root).resolve()
    benchmark = Path(benchmark_root).resolve() if benchmark_root else DEFAULT_BENCHMARK_ROOT
    manifest_path = root / "_pipeline_manifest.json"
    if not manifest_path.exists():
        return {"passed": False, "errors": ["missing _pipeline_manifest.json"], "warnings": []}
    manifest = read_json(manifest_path)
    errors: list[str] = []
    warnings: list[str] = []
    task_reports: list[dict[str, Any]] = []
    seen: set[str] = set()
    source_ids: set[str] = set()
    for item in manifest.get("tasks", []):
        task_id = item.get("task_id", "")
        task_dir = root / item.get("path", task_id)
        report = _validate_task(task_dir, task_id, benchmark, run_workspace_smoke)
        task_reports.append(report)
        errors.extend(f"{task_id}: {error}" for error in report["errors"])
        warnings.extend(f"{task_id}: {warning}" for warning in report["warnings"])
        if task_id in seen:
            errors.append(f"duplicate task id: {task_id}")
        seen.add(task_id)
        if report.get("ground_truth"):
            source_id = report["task_info"].get("source_id")
            if source_id in source_ids:
                errors.append(
                    f"{task_id}: more than one formal task was generated for source {source_id}"
                )
            source_ids.add(source_id)
    if require_tasks and not task_reports:
        errors.append("dataset contains no constructed tasks")
    if manifest.get("skipped"):
        warnings.append(
            f"{len(manifest['skipped'])} studies were skipped before package construction"
        )
    return {
        "passed": not errors,
        "format": manifest.get("pipeline_format"),
        "task_count": len(task_reports),
        "errors": errors,
        "warnings": warnings,
        "tasks": task_reports,
    }


def _validate_task(
    task_dir: Path,
    task_id: str,
    benchmark_root: Path,
    run_workspace_smoke: bool,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    required = (
        "task_info.json",
        "data/benchmark_data/README.md",
        "data/benchmark_data/input_manifest.json",
        "target_study/ground_truth.json",
    )
    for relative in required:
        if not (task_dir / relative).is_file():
            errors.append(f"missing {relative}")
    if errors:
        return {"task_id": task_id, "passed": False, "errors": errors, "warnings": warnings}

    task_info = read_json(task_dir / "task_info.json")
    ground_truth = read_json(task_dir / "target_study" / "ground_truth.json")
    data_root = task_dir / "data" / "benchmark_data"
    input_manifest = read_json(data_root / "input_manifest.json")

    if task_info.get("task_id") != task_id:
        errors.append("task_info task_id does not match directory")
    if not task_info.get("required_deliverables"):
        errors.append("required_deliverables is empty")
    if not task_info.get("scientific_requirements"):
        errors.append("scientific_requirements is empty")
    if ground_truth.get("evaluation_mode") != "dual_axis_100":
        errors.append("evaluation_mode must be dual_axis_100")

    try:
        _validate_schema(task_info, ground_truth, benchmark_root)
    except Exception as exc:
        errors.append(f"ResearchChemBench schema validation failed: {exc}")

    files = input_manifest.get("files") or []
    if not files:
        errors.append("input_manifest contains no solver-visible files")
    for record in files:
        relative = str(record.get("path") or "")
        try:
            path = _resolve_under(data_root, relative)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not path.is_file():
            errors.append(f"manifest file missing: {relative}")
            continue
        if path.is_symlink():
            errors.append(f"solver-visible symlink is not allowed: {relative}")
        if path.stat().st_size != record.get("size_bytes"):
            errors.append(f"size mismatch: {relative}")
        if sha256_file(path) != record.get("sha256"):
            errors.append(f"sha256 mismatch: {relative}")
    manifest_hash = hashlib.sha256((data_root / "input_manifest.json").read_bytes()).hexdigest()
    reference_hash = (ground_truth.get("reference_evidence") or {}).get("input_manifest_sha256")
    if manifest_hash != reference_hash:
        errors.append("ground truth input_manifest_sha256 mismatch")

    public_text = _read_public_text(task_dir)
    for forbidden in ("target_study", "ground_truth.json", "hidden_reference_files"):
        if forbidden.casefold() in public_text.casefold():
            errors.append(f"solver-visible package names hidden evaluation material: {forbidden}")
    if input_manifest.get("reference_answers") != 0:
        errors.append("reference_answers must be zero in the solver-visible manifest")

    chemistry_report = None
    molecular_systems = data_root / "molecular_systems.json"
    if molecular_systems.is_file():
        try:
            chemistry_report = _validate_molecular_systems(molecular_systems)
            errors.extend(chemistry_report["errors"])
            warnings.extend(chemistry_report["warnings"])
        except Exception as exc:
            errors.append(f"molecular input validation failed: {exc}")

    workspace_smoke = None
    if run_workspace_smoke and not errors:
        try:
            workspace_smoke = _run_workspace_smoke(task_dir, benchmark_root)
        except Exception as exc:
            errors.append(f"benchmark workspace smoke failed: {exc}")

    return {
        "task_id": task_id,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "workspace_smoke": workspace_smoke,
        "chemistry_validation": chemistry_report,
        "task_info": task_info,
        "ground_truth": ground_truth,
    }


def _validate_schema(
    task_info: dict[str, Any], ground_truth: dict[str, Any], benchmark_root: Path
) -> None:
    root = str(benchmark_root)
    if root not in sys.path:
        sys.path.insert(0, root)
    from evaluation.task_schema import GroundTruth, TaskInfo

    TaskInfo.model_validate(task_info)
    GroundTruth.model_validate(ground_truth)


def _run_workspace_smoke(task_dir: Path, benchmark_root: Path) -> dict[str, Any]:
    """Use the real TaskRunner workspace setup without touching benchmark tasks/."""

    root = str(benchmark_root)
    if root not in sys.path:
        sys.path.insert(0, root)
    import evaluation.run_task as run_task
    import evaluation.utils as utils

    tasks_root = task_dir.parent
    old_run_tasks = run_task.TASKS_DIR
    old_utils_tasks = utils.TASKS_DIR
    run_task.TASKS_DIR = tasks_root
    utils.TASKS_DIR = tasks_root
    try:
        with tempfile.TemporaryDirectory(prefix="rcb_pipeline_smoke_") as temp:
            runner = run_task.TaskRunner(
                task_dir.name,
                agent_key="mock",
                workspace_root=Path(temp),
                live_progress=False,
                progress_console=False,
            )
            runner.setup_workspace()
            visible_root = runner.workspace / "data" / "benchmark_data"
            if not visible_root.is_dir():
                raise RuntimeError("TaskRunner did not copy data/benchmark_data")
            if (runner.workspace / "target_study").exists():
                raise RuntimeError("TaskRunner exposed target_study to the agent workspace")
            copied = sorted(
                path.relative_to(runner.workspace).as_posix()
                for path in runner.workspace.rglob("*")
                if path.is_file() and "benchmark_data" in path.parts
            )
            return {
                "passed": True,
                "copied_input_files": len(copied),
                "instructions_bytes": runner.instructions_path.stat().st_size,
                "hidden_ground_truth_exposed": False,
            }
    finally:
        run_task.TASKS_DIR = old_run_tasks
        utils.TASKS_DIR = old_utils_tasks


def _resolve_under(root: Path, relative: str) -> Path:
    if not relative or Path(relative).is_absolute() or "\\" in relative:
        raise ValueError(f"unsafe manifest path: {relative!r}")
    resolved = (root / relative).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"manifest path escapes data root: {relative}") from exc
    return resolved


def _read_public_text(task_dir: Path) -> str:
    chunks = [(task_dir / "task_info.json").read_text(encoding="utf-8")]
    for path in (task_dir / "data").rglob("*"):
        if not path.is_file():
            continue
        try:
            chunks.append(path.read_text(encoding="utf-8"))
        except UnicodeDecodeError:
            continue
    return "\n".join(chunks)


def _validate_molecular_systems(path: Path) -> dict[str, Any]:
    cache_key = sha256_file(path)
    if cache_key in _CHEMISTRY_VALIDATION_CACHE:
        return _CHEMISTRY_VALIDATION_CACHE[cache_key]
    from rdkit import Chem
    from rdkit.Chem import AllChem

    records = read_json(path)
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    parsed = 0
    embedded = 0
    for item in records:
        molecule_id = str(item.get("molecule_id") or "").strip()
        smiles = str(item.get("smiles") or "").strip()
        if not molecule_id or not smiles:
            errors.append("each molecular system requires molecule_id and smiles")
            continue
        if molecule_id in seen:
            errors.append(f"duplicate molecule_id: {molecule_id}")
        seen.add(molecule_id)
        molecule = Chem.MolFromSmiles(smiles)
        if molecule is None:
            errors.append(f"invalid SMILES for {molecule_id}: {smiles}")
            continue
        parsed += 1
        declared_charge = item.get("charge")
        formal_charge = Chem.GetFormalCharge(molecule)
        if declared_charge is not None and int(declared_charge) != formal_charge:
            errors.append(
                f"formal charge mismatch for {molecule_id}: declared {declared_charge}, SMILES {formal_charge}"
            )
        multiplicity = item.get("multiplicity")
        if multiplicity is not None and int(multiplicity) < 1:
            errors.append(f"invalid multiplicity for {molecule_id}: {multiplicity}")
        # Ensure ordinary molecular inputs can be turned into an initial 3D guess.
        # Disconnected salts are intentionally left to a task-specific assembly step.
        if "." not in smiles and molecule.GetNumAtoms() <= 150:
            with_hydrogen = Chem.AddHs(molecule)
            parameters = AllChem.ETKDGv3()
            parameters.randomSeed = 42
            parameters.maxIterations = 1000
            status = AllChem.EmbedMolecule(with_hydrogen, parameters)
            if status != 0:
                errors.append(f"3D conformer generation failed for {molecule_id}")
            else:
                embedded += 1
    report = {
        "passed": not errors,
        "records": len(records),
        "parsed_smiles": parsed,
        "embedded_single_component_molecules": embedded,
        "errors": errors,
        "warnings": warnings,
    }
    _CHEMISTRY_VALIDATION_CACHE[cache_key] = report
    return report
