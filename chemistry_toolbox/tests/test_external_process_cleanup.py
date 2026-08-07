import signal
import subprocess
import sys
import time

from chemistry_toolbox.src.backends.common import run_external


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


def test_run_external_interrupt_terminates_spawned_process_group(tmp_path):
    marker = tmp_path / "cancelled-child-output.txt"
    child_code = (
        "import pathlib,time; "
        "time.sleep(1.0); "
        f"pathlib.Path({str(marker)!r}).write_text('orphaned')"
    )
    external_code = (
        "import subprocess,sys,time; "
        f"subprocess.Popen([sys.executable, '-c', {child_code!r}]); "
        "time.sleep(10)"
    )
    wrapper_code = (
        "import signal,sys; "
        "from chemistry_toolbox.src.backends.common import run_external; "
        "signal.signal(signal.SIGTERM, lambda *_: (_ for _ in ()).throw(KeyboardInterrupt())); "
        f"run_external(executable=sys.executable, arguments=['-c', {external_code!r}], "
        f"directory=__import__('pathlib').Path({str(tmp_path)!r}), timeout_seconds=30)"
    )
    process = subprocess.Popen([sys.executable, "-c", wrapper_code])
    time.sleep(0.3)
    process.send_signal(signal.SIGTERM)
    process.wait(timeout=10)

    assert process.returncode != 0
    time.sleep(1.2)
    assert not marker.exists()
