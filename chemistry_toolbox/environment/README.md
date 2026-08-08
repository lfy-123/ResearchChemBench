# Chemistry environment specifications

This directory contains every reproducible environment definition used by the
benchmark. The framework environment and each chemistry runtime have one
self-contained directory; there are no nested `merged`, `framework`, or
central lock directories.

Each environment contains:

- `environment.yml`: human-maintained Conda requirements and ABI constraints;
- `requirements.txt`: pip-only packages, including exact VCS revisions where
  applicable;
- `linux-64.explicit.txt`: exact Conda artifact URLs captured from the tested
  server;
- `linux-64.pip-freeze.txt`: the corresponding pip inventory.

`environments.yaml` maps logical runtime names to the seven chemistry
prefixes. `researchchembench/` contains the framework Conda, pip, constraints,
and exact-lock inputs. `lock-manifest.json` records hashes for chemistry locks,
and `system-requirements.txt` lists host libraries that Conda cannot provide.

Use `chemistry_toolbox/scripts/build_environments.sh` for a portable
rebuild.  The human-maintained definitions are preferred across platforms;
the explicit lock files are intended for exact Linux x86-64 replay.

## Build and select the layout

Install the host packages listed in `system-requirements.txt`, then run from
the repository root:

```bash
# Cross-platform dependency solve from the maintained specifications.
bash chemistry_toolbox/scripts/build_environments.sh all

# Exact replay of the tested linux-64 Conda artifacts.
bash chemistry_toolbox/scripts/build_environments.sh --from-lock all

# Refresh locks after an intentional environment change.
bash chemistry_toolbox/scripts/capture_environment_locks.sh
```

The toolbox always uses the consolidated layout. Operators may relocate all seven
prefixes without changing profile configuration:

```bash
export RESEARCHCHEMBENCH_ENV_ROOT=/path/to/researchchem-envs
```

## Compatibility boundaries

- OpenFF/AmberTools requires NumPy 1.x, so it is separate from the modern
  NumPy 2.x quantum-analysis runtime.
- CatMAP 0.3.1 requires ASE 3.17 and is isolated from modern ASE consumers.
- CP2K 2026.1 requires MPICH 5 and libxc 7. ABINIT 10.0.3 and LAMMPS use the
  MPICH-4 reaction/kinetics environment rather than the CP2K environment.
- AmberTools 26 declares a conflict with the standalone Packmol package.
  Packmol is therefore installed once in the general environment and shared
  with the molecular-dynamics runtime through its configured PATH.
- Yambo remains with its OpenMPI-4 stack and therefore does not share the
  OpenMPI-5 general runtime.
- gmx_MMPBSA 1.6.5 requires Python 3.11 and AmberTools 23.6, so it remains
  isolated from the Python 3.12/AmberTools 26 molecular-simulation runtime.
- xTB 6.7.1 runs in the reaction/kinetics prefix because its tblite dependency
  conflicts with the older tblite ABI required by DFTB+ 25.1 in the general prefix.
