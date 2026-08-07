from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_stage_01_04_batches.py"
SPEC = importlib.util.spec_from_file_location("run_stage_01_04_batches", SCRIPT)
assert SPEC and SPEC.loader
batch_script = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(batch_script)


def _args(**overrides):
    values = {
        "dataset": "en-paper-hzzj",
        "count": 1000,
        "outside": False,
        "disable_publisher_network": False,
        "disable_mineru": False,
        "stage01_workers": 32,
        "stage02_workers": 32,
        "stage03_workers": 32,
        "stage04_workers": 16,
        "stage05_workers": 16,
        "stage06_workers": 16,
        "microbatch": True,
        "microbatch_size": 10,
        "microbatch_concurrency": 5,
        "stage03_llm": True,
        "stage03_llm_managed_rlaunch": False,
        "stage03_llm_concurrency": 16,
        "stage03_llm_base_url": "https://api.deepseek.com/v1",
        "stage03_llm_model": "deepseek-v4-flash",
        "stage03_llm_api_key_env": "JUDGE_API_KEY",
        "screening_policy": "strict",
        "stage03_llm_cpu": 16,
        "stage03_llm_memory_mib": 196000,
        "stage03_llm_image": "test-image",
        "backend": "sandbox",
        "sandbox_cpu": 128,
        "sandbox_memory": "256Gi",
        "sandbox_lifecycle_minutes": 1440,
        "sandbox_cleanup": "stop",
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def test_batch_config_prepares_grouped_remote_corpus_and_stops_after_stage06(tmp_path):
    template = tmp_path / "config.json"
    template.write_text(
        json.dumps({"pdf_directory": "papers", "grobid": {}, "softcite": {}, "toolbox": {}}),
        encoding="utf-8",
    )
    credentials = tmp_path / "xinghe.txt"
    credentials.write_text("credentials", encoding="utf-8")
    config = batch_script._build_config(_args(), template, tmp_path / "work", credentials)
    assert config["stop_after"] == "stage06"
    assert config["exclude_supplementary"] is False
    assert config["stage00_remote_corpus"] == {
        "enabled": True,
        "dataset": "en-paper-hzzj",
        "count": 1000,
        "output_directory": str(tmp_path / "work" / "stage_00_remote_corpus"),
        "credentials": str(credentials),
        "outside": False,
        "resume": True,
        "selection": "seeded_sample",
        "seed": 20260806,
        "copy_existing_supplementary": True,
    }
    assert config["stage03_computation_relevance"]["use_llm"] is True
    assert config["stage03_computation_relevance"]["screening_policy"] == "strict"
    assert config["stage03_computation_relevance"]["llm"]["review_all_candidates"] is True
    assert config["stage03_computation_relevance"]["llm"]["allowed_computation_roles"] == [
        "primary"
    ]
    assert config["stage03_computation_relevance"]["llm"]["required_study_modes"] == [
        "pure_computational"
    ]
    assert config["microbatch"]["enabled"] is True
    assert config["microbatch"]["size"] == 10
    assert config["microbatch"]["concurrency"] == 5
    assert config["resume_completed_stages"] is True
    assert config["stage05_preliminary_coverage"]["softcite_instances"] == 5
    assert config["stage05_preliminary_coverage"]["screening_policy"] == "strict"
    assert config["stage05_preliminary_coverage"]["accepted_validation_levels"] == [
        "functional"
    ]
    assert config["stage05_preliminary_coverage"]["require_all_core_software"] is True
    assert config["stage05_preliminary_coverage"]["require_all_method_families"] is True
    assert config["stage05_preliminary_coverage"]["require_complete_software_inventory"] is True
    assert config["grobid"]["workers"] == 32
    assert config["softcite"]["workers"] == 16


def test_batch_config_can_enable_managed_stage03_llm(tmp_path):
    template = tmp_path / "config.json"
    template.write_text(
        json.dumps({"pdf_directory": "papers", "grobid": {}, "softcite": {}, "toolbox": {}}),
        encoding="utf-8",
    )
    credentials = tmp_path / "xinghe.txt"
    credentials.write_text("credentials", encoding="utf-8")
    config = batch_script._build_config(
        _args(stage03_llm=True, stage03_llm_managed_rlaunch=True),
        template,
        tmp_path / "work",
        credentials,
    )
    stage = config["stage03_computation_relevance"]
    assert stage["use_llm"] is True
    assert stage["llm"]["managed_rlaunch"] is True
    assert stage["llm"]["concurrency"] == 16
    assert stage["llm"]["positive_tag"] == "h200"


def test_batch_config_can_use_external_flash_stage03_llm(tmp_path):
    template = tmp_path / "config.json"
    template.write_text(
        json.dumps({"pdf_directory": "papers", "grobid": {}, "softcite": {}, "toolbox": {}}),
        encoding="utf-8",
    )
    credentials = tmp_path / "xinghe.txt"
    credentials.write_text("credentials", encoding="utf-8")
    config = batch_script._build_config(
        _args(stage03_llm=True, stage03_llm_managed_rlaunch=False),
        template,
        tmp_path / "work",
        credentials,
    )
    llm = config["stage03_computation_relevance"]["llm"]
    assert llm["managed_rlaunch"] is False
    assert llm["thinking"] == "disabled"
    assert llm["base_url"] == "https://api.deepseek.com/v1"
    assert llm["api_key_env"] == "JUDGE_API_KEY"
    assert llm["model"] == "deepseek-v4-flash"


def test_batch_command_uses_one_large_sandbox_until_pipeline_exit(tmp_path):
    command = batch_script._pipeline_command(
        _args(),
        Path("/python"),
        tmp_path / "config.json",
        tmp_path / "summary.json",
    )
    assert command.count("--execution-backend") == 1
    assert command[command.index("--execution-backend") + 1] == "sandbox"
    assert command[command.index("--sandbox-cpu") + 1] == "128"
    assert command[command.index("--sandbox-memory") + 1] == "256Gi"
    assert command[command.index("--sandbox-cleanup") + 1] == "stop"


def test_batch_command_omits_sandbox_options_for_local_backend(tmp_path):
    command = batch_script._pipeline_command(
        _args(backend="local"),
        Path("/python"),
        tmp_path / "config.json",
        tmp_path / "summary.json",
    )
    assert "--sandbox-cpu" not in command
    assert command[command.index("--execution-backend") + 1] == "local"


def test_relative_work_root_is_resolved_from_pipeline_root():
    assert batch_script._pipeline_path("runs/example") == (
        batch_script.PIPELINE_ROOT / "runs/example"
    ).resolve()


def test_strict_batch_rejects_disabled_stage03_llm():
    try:
        batch_script.main(["--screening-policy", "strict", "--no-stage03-llm"])
    except ValueError as exc:
        assert "requires --stage03-llm" in str(exc)
    else:
        raise AssertionError("strict mode must require Stage 03 LLM confirmation")
