from __future__ import annotations

import subprocess
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "create_sandbox_pool.sh"


def test_create_sandbox_pool_generate_only_writes_custom_source(tmp_path):
    source = tmp_path / ".sandboxes.local.yaml"
    inventory = tmp_path / ".sandbox_inventory.local.json"
    completed = subprocess.run(
        [
            "bash",
            str(SCRIPT),
            "--generate-only",
            "--count",
            "3",
            "--cpu",
            "12",
            "--available-cpu",
            "10",
            "--memory",
            "24Gi",
            "--reserve-memory-mb",
            "2048",
            "--lifecycle-minutes",
            "360",
            "--instance-capacity",
            "5",
            "--name-prefix",
            "test-pool",
            "--output",
            str(source),
            "--inventory",
            str(inventory),
        ],
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    payload = yaml.safe_load(source.read_text(encoding="utf-8"))
    assert payload["environment"]["name"] == "test-pool-12cpu"
    assert payload["environment"]["resources"] == {"cpu": "12", "memory": "24Gi"}
    assert payload["environment"]["instance_capacity"] == 5
    assert len(payload["workers"]) == 3
    assert [worker["worker_id"] for worker in payload["workers"]] == [
        "sandbox-1",
        "sandbox-2",
        "sandbox-3",
    ]
    assert all(worker["sandbox_id"] is None for worker in payload["workers"])
    assert all(worker["available_cpu_cores"] == 10 for worker in payload["workers"])
    assert all(worker["available_memory_mb"] == 22528 for worker in payload["workers"])
    assert not inventory.exists()
    assert source.stat().st_mode & 0o777 == 0o600


def test_create_sandbox_pool_refuses_to_overwrite_without_replace(tmp_path):
    source = tmp_path / ".sandboxes.local.yaml"
    source.write_text("existing: true\n", encoding="utf-8")
    completed = subprocess.run(
        [
            "bash",
            str(SCRIPT),
            "--generate-only",
            "--output",
            str(source),
            "--inventory",
            str(tmp_path / "inventory.json"),
        ],
        cwd=PROJECT_ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode == 2
    assert "--replace" in completed.stderr
    assert source.read_text(encoding="utf-8") == "existing: true\n"
