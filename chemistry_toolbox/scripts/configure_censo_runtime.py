#!/usr/bin/env python3
"""Generate the relocatable CENSO runtime configuration for this checkout."""

from __future__ import annotations

import argparse
import configparser
import os
from pathlib import Path
import subprocess
import tempfile


ORCA_SECTIONS = (
    "prescreening",
    "screening",
    "optimization",
    "refinement",
    "nmr",
    "uvvis",
)
ORCA_SOLVENT_SECTIONS = ("screening", "optimization", "refinement")


def _prepend_path(environment: dict[str, str], key: str, entries: list[Path]) -> None:
    current = environment.get(key)
    values = [str(path) for path in entries]
    if current:
        values.append(current)
    environment[key] = os.pathsep.join(values)


def configure(project_root: Path, environment_root: Path) -> Path:
    project_root = project_root.resolve()
    environment_root = environment_root.resolve()
    prefix = environment_root / "kinetics-legacy"
    python = prefix / "bin/python"
    xtb = prefix / "bin/xtb"
    orca_dir = project_root / ".software_cache/installations/orca/6.1.1"
    orca = orca_dir / "orca"
    openmpi = project_root / ".software_cache/shared/mpi/openmpi/4.1.8-fortran"
    config_home = project_root / ".software_cache/state/censo/home"

    required = (python, xtb, orca, openmpi / "bin/mpirun")
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "Cannot configure CENSO; missing runtime file(s): " + ", ".join(missing)
        )

    config_home.mkdir(parents=True, exist_ok=True)
    environment = os.environ.copy()
    environment["OPAL_PREFIX"] = str(openmpi)
    _prepend_path(
        environment,
        "PATH",
        [orca_dir, openmpi / "bin", prefix / "bin"],
    )
    _prepend_path(
        environment,
        "LD_LIBRARY_PATH",
        [openmpi / "lib", orca_dir],
    )

    with tempfile.TemporaryDirectory(prefix="censo-config-") as temporary:
        generation_home = Path(temporary) / "home"
        generation_home.mkdir()
        environment["HOME"] = str(generation_home)
        completed = subprocess.run(
            [str(python), "-m", "censo", "--new-config"],
            cwd=temporary,
            env=environment,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if completed.returncode:
            raise RuntimeError(
                "CENSO failed to generate its default configuration:\n"
                + completed.stdout
            )
        generated = Path(temporary) / "censo2rc_NEW"
        if not generated.is_file():
            raise RuntimeError("CENSO did not create censo2rc_NEW")

        parser = configparser.ConfigParser()
        parser.read(generated, encoding="utf-8")

    for section in ORCA_SECTIONS:
        if section not in parser:
            raise KeyError(f"CENSO default configuration is missing [{section}]")
        parser[section]["prog"] = "orca"
    for section in ORCA_SOLVENT_SECTIONS:
        parser[section]["sm"] = "smd"

    # Keep the checked-in state relocatable.  The CENSO launcher expands these
    # project-relative values immediately before starting CENSO, so the state
    # file never embeds a server-specific checkout path.
    parser["paths"]["orcapath"] = ".software_cache/installations/orca/6.1.1/orca"
    parser["paths"]["xtbpath"] = ".envs/kinetics-legacy/bin/xtb"
    parser["paths"]["orcaversion"] = "6.1.1"

    destination = config_home / ".censo2rc"
    temporary_destination = destination.with_suffix(".tmp")
    with temporary_destination.open("w", encoding="utf-8") as handle:
        parser.write(handle)
    temporary_destination.replace(destination)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", required=True, type=Path)
    parser.add_argument("--environment-root", required=True, type=Path)
    arguments = parser.parse_args()
    destination = configure(arguments.project_root, arguments.environment_root)
    print(f"Configured CENSO runtime: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
