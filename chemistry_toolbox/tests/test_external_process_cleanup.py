import sys
import time

from researchchem_toolbox.backends.common import run_external


def test_run_external_timeout_terminates_spawned_process_group(tmp_path):
    marker = tmp_path / "late-child-output.txt"
    child_code = (
        "import pathlib,time; "
        "time.sleep(1.0); "
        f"pathlib.Path({str(marker)!r}).write_text('orphaned')"
    )
    parent_code = (
        "import subprocess,sys,time; "
        f"subprocess.Popen([sys.executable, '-c', {child_code!r}]); "
        "time.sleep(10)"
    )

    result = run_external(
        executable=sys.executable,
        arguments=["-c", parent_code],
        directory=tmp_path,
        timeout_seconds=0.2,
    )

    assert result["returncode"] == 124
    assert result["timeout"] is True
    time.sleep(1.2)
    assert not marker.exists()
