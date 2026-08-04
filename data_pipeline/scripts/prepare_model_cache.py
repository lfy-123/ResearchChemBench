from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare the local data-pipeline model cache")
    parser.add_argument("--root", default=Path(__file__).resolve().parents[1])
    parser.add_argument("--cache")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    cache = (
        Path(args.cache).expanduser().resolve() if args.cache else (root / ".model_cache").resolve()
    )
    source_home = root / "third_party" / "grobid" / "grobid-home"
    if not source_home.is_dir():
        raise SystemExit(f"GROBID home is missing: {source_home}")

    _consolidate_mineru_cache(cache)
    runtime_home = cache / "grobid-home"
    _sync_tree(source_home, runtime_home)

    softcite_models = root / "third_party" / "software-mentions" / "resources" / "models"
    if softcite_models.is_dir():
        _sync_tree(softcite_models, runtime_home / "models")
        compressed = softcite_models / "software" / "model.wapiti.gz"
        if compressed.is_file():
            target = runtime_home / "models" / "software" / "model.wapiti"
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.is_file():
                with gzip.open(compressed, "rb") as source, target.open("wb") as destination:
                    shutil.copyfileobj(source, destination)

    quantities = root / "third_party" / "grobid-quantities"
    quantities_models = quantities / "resources" / "models"
    if quantities_models.is_dir():
        _sync_tree(quantities_models, runtime_home / "models")
    cleanlp_source = quantities / "resources" / "clearnlp" / "models"
    cleanlp_target = cache / "grobid-quantities" / "clearnlp-models"
    if cleanlp_source.is_dir():
        _sync_tree(cleanlp_source, cleanlp_target)

    config_root = cache / "config"
    config_root.mkdir(parents=True, exist_ok=True)
    _write_config(
        source_home / "config" / "grobid.yaml",
        runtime_home / "config" / "grobid.yaml",
        runtime_home,
        working_directory=root / "third_party" / "grobid",
    )
    _write_config(
        root / "third_party" / "software-mentions" / "resources" / "config" / "config.yml",
        config_root / "software-mentions.yml",
        runtime_home,
        working_directory=root / "third_party" / "software-mentions",
    )
    _write_config(
        quantities / "resources" / "config" / "config.yml",
        config_root / "grobid-quantities.yml",
        runtime_home,
        working_directory=quantities,
        cleanlp_target=cleanlp_target,
    )
    mineru_config = _rewrite_mineru_config(cache)

    manifest = {
        "cache_root": ".",
        "grobid_home": "grobid-home",
        "mineru_config": (mineru_config.relative_to(cache).as_posix() if mineru_config else None),
        "sources": {
            "grobid": "https://github.com/grobidOrg/grobid tag 0.9.0",
            "softcite": (
                "https://github.com/softcite/software-mentions "
                "commit c7c83852a3cad8f2d9d07ce3de6fbe852e23c19a"
            ),
            "softcite_models": "https://huggingface.co/sciencialab/software-mentions-models",
            "grobid_quantities": (
                "https://github.com/lfoppiano/grobid-quantities "
                "commit d0d55592f4d0ddbe6a549e06613349adaa2d1cd7"
            ),
            "mineru": (
                "https://github.com/opendatalab/MinerU "
                "commit 79d6d8d79fb8f3ddba5cc34c07a16f0ec36f56c7"
            ),
            "mineru_pipeline_huggingface": (
                "https://huggingface.co/opendatalab/PDF-Extract-Kit-1.0"
            ),
            "mineru_pipeline_modelscope": (
                "https://modelscope.cn/models/OpenDataLab/PDF-Extract-Kit-1.0"
            ),
        },
    }
    (cache / "model_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


def _consolidate_mineru_cache(cache: Path) -> None:
    legacy = cache.parent / "mineru"
    target = cache / "mineru"
    if not legacy.is_dir() or legacy.resolve() == target.resolve():
        return
    cache.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.move(str(legacy), str(target))
        return
    _sync_tree(legacy, target)
    shutil.rmtree(legacy)


def _rewrite_mineru_config(cache: Path) -> Path | None:
    config_path = cache / "mineru" / "mineru.json"
    if not config_path.is_file():
        return None
    config = json.loads(config_path.read_text(encoding="utf-8"))
    models = config.get("models-dir") or {}
    rewritten: dict[str, str] = {}
    for model_type, raw_path in models.items():
        path = Path(str(raw_path)).expanduser()
        candidates = [path] if not path.is_absolute() else []
        candidates.extend([cache / "mineru" / path.name, cache / path.name])
        resolved = next((candidate for candidate in candidates if candidate.exists()), None)
        if resolved is None:
            resolved = cache / "mineru" / path.name
        try:
            rewritten[str(model_type)] = resolved.resolve().relative_to(cache).as_posix()
        except ValueError:
            rewritten[str(model_type)] = str(raw_path)
    config["models-dir"] = rewritten
    config_path.write_text(
        json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return config_path


def _sync_tree(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for item in source.rglob("*"):
        relative = item.relative_to(source)
        destination = target / relative
        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue
        if item.is_symlink():
            if destination.exists() or destination.is_symlink():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.symlink_to(os.readlink(item))
            continue
        if destination.is_file() and destination.stat().st_size == item.stat().st_size:
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.unlink(missing_ok=True)
        try:
            os.link(item, destination)
        except OSError:
            shutil.copy2(item, destination)


def _write_config(
    source: Path,
    target: Path,
    runtime_home: Path,
    *,
    working_directory: Path,
    cleanlp_target: Path | None = None,
) -> None:
    if not source.is_file():
        return
    lines = source.read_text(encoding="utf-8").splitlines()
    output = []
    replaced_home = False
    relative_home = os.path.relpath(runtime_home, working_directory)
    relative_cleanlp = (
        os.path.relpath(cleanlp_target, working_directory) if cleanlp_target else None
    )
    for line in lines:
        stripped = line.lstrip()
        indent = line[: len(line) - len(stripped)]
        if not replaced_home and stripped.startswith("grobidHome:"):
            output.append(f'{indent}grobidHome: "{relative_home}"')
            replaced_home = True
        elif cleanlp_target is not None and stripped.startswith("cleanlpModelPath:"):
            output.append(f'{indent}cleanlpModelPath: "{relative_cleanlp}"')
        else:
            output.append(line)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(output) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
